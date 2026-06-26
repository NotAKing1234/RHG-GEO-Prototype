#!/usr/bin/env python3
"""Generate flat-file views from the SQLite system of record.

Data flow: DB tables render markdown and CSV artifacts for humans, the runner, and Jira import.
Pitfalls: generated files are never read back as authority, and Jira column order stays pinned to
RHG JIRA EXPORT.csv / scripts.db.JIRA_FIELDS.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import db
from scripts.dashboard_domain import READY_TO_SEND, handoff_readiness_for, stakeholder_email_lines
from scripts.dashboard_read_model import dashboard_payload


TARGET_URLS = ROOT / "sources" / "website" / "target_urls.md"
NEXT_GEO_RUN = ROOT / "sources" / "website" / "run_targets" / "next_geo_run.csv"
READY_TO_SEND_DIRNAME = "ready-to-send"
JIRA_ITEM_FILENAME = "jira-ticket.csv"
JIRA_VALIDATION_REPORT = "jira-validation-report.md"
JIRA_ALLOWED_PRIORITIES = {"Highest", "High", "Medium", "Low", "Lowest"}
FORMULA_PREFIXES = ("=", "+", "@", "\t", "\r")
RUN_ID_PATTERN = re.compile(r"^run_[A-Za-z0-9][A-Za-z0-9_-]*$")


def validate_run_id(run_id: str) -> str:
    value = str(run_id or "")
    if not RUN_ID_PATTERN.fullmatch(value):
        raise ValueError(f"Invalid run_id: {value!r}")
    return value


def run_dir_for(run_id: str) -> Path:
    run_id = validate_run_id(run_id)
    matches = sorted((ROOT / "runs").glob(f"{run_id}_*"))
    if matches:
        return matches[-1]
    return ROOT / "runs" / run_id


def render_target_urls(conn) -> str:
    lines = ["# Radisson Website - Target URLs for GEO Audit", ""]
    urls = db.list_urls(conn)
    for item in urls:
        bits = [item["url"]]
        metadata = ", ".join(str(item.get(field) or "") for field in ("brand", "region", "page_type") if item.get(field))
        if metadata:
            bits.append(f"<!-- {metadata} -->")
        lines.append(f"- {' '.join(bits)}")
    lines.append("")
    return "\n".join(lines)


def write_next_geo_run(conn, path: Path = NEXT_GEO_RUN, run_id: str | None = None) -> None:
    rows = db.run_target_urls(conn, run_id) if run_id else []
    if not rows:
        rows = db.selected_urls(conn)
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["url", "brand", "region", "page_type", "location_confidence", "selected_for_next_run", "selected_at", "last_audited_run"]
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                csv_safe_row({
                    "url": row["url"],
                    "brand": row.get("brand") or "",
                    "region": row.get("region") or "",
                    "page_type": row.get("page_type") or "",
                    "location_confidence": row.get("location_confidence") or "",
                    "selected_for_next_run": "true",
                    "selected_at": row.get("selected_at") or "",
                    "last_audited_run": row.get("last_audited_run") or "",
                })
            )


def render_optimization_proposal(conn, run_id: str) -> str:
    rows = db.rows(
        conn,
        """
        SELECT p.proposal_id, p.proposed_change, p.priority_tier, p.impact_estimate,
               g.gap_id, g.description AS gap_description, g.gap_type, g.severity,
               u.url, c.code AS criterion_code
        FROM proposals p
        JOIN gaps g ON g.gap_id = p.gap_id
        LEFT JOIN urls u ON u.url_id = g.url_id
        LEFT JOIN criteria c ON c.criterion_id = g.criterion_id
        WHERE p.run_id = ?
        ORDER BY p.proposal_id
        """,
        (run_id,),
    )
    lines = [f"# Optimization Proposal - {run_id}", "", "## Proposal Entries", ""]
    for item in rows:
        lines.extend(
            [
                f"### PROP-{int(item['proposal_id']):03d} - {item['gap_id']}",
                "",
                "**1. Proposed change**",
                item["proposed_change"] or "[NEEDED: proposed change]",
                "",
                "**2. Source citation**",
                item.get("criterion_code") or "[NEEDED: criterion]",
                "",
                "**3. Current state**",
                item.get("gap_description") or "[NEEDED: current state]",
                "",
                "**4. Inferred implementation status**",
                "N/A",
                "",
                "**5. Directional impact estimate**",
                item.get("impact_estimate") or "[NEEDED: impact estimate]",
                "",
                "**6. Priority tier**",
                item.get("priority_tier") or "P3",
                "",
                "---",
                "",
            ]
        )
    return "\n".join(lines)


def render_sources(conn, run_id: str) -> str:
    rows = db.rows(
        conn,
        """
        SELECT s.source_id, s.url, s.domain, s.title, s.source_type, s.credibility,
               i.claim, i.theme, i.weight
        FROM sources s
        LEFT JOIN source_insights i ON i.source_id = s.source_id
        WHERE s.run_id = ?
        ORDER BY s.source_id, i.insight_id
        """,
        (run_id,),
    )
    lines = [f"# Literature Sources - {run_id}", ""]
    if not rows:
        lines.append("[NEEDED: sources and source_insights start fresh after V1.1 migration]")
        lines.append("")
        return "\n".join(lines)
    for item in rows:
        title = item.get("title") or item.get("url") or f"Source {item['source_id']}"
        lines.extend(
            [
                f"## {title}",
                f"- Type: {item.get('source_type') or 'other'}",
                f"- URL: {item.get('url') or '[NEEDED: source URL]'}",
                f"- Claim: {item.get('claim') or '[NEEDED: extracted insight]'}",
                f"- Theme: {item.get('theme') or '[NEEDED: theme]'}",
                "",
            ]
        )
    return "\n".join(lines)


def jira_csv_from_rows(rows_to_write: list[dict[str, str]], *, expected_story_count: int | None = None, context: str = "jira_csv") -> str:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=db.JIRA_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(csv_safe_row(row) for row in rows_to_write)
    content = output.getvalue()
    errors = validate_jira_csv_content(content, expected_story_count=expected_story_count)
    if errors:
        raise ValueError(f"{context} failed Jira CSV validation: {'; '.join(errors)}")
    return content


def validate_jira_csv_content(content: str, *, expected_story_count: int | None = None) -> list[str]:
    errors: list[str] = []
    reader = csv.DictReader(io.StringIO(content))
    if reader.fieldnames != db.JIRA_FIELDS:
        errors.append(f"header must be {db.JIRA_FIELDS}, got {reader.fieldnames}")
        return errors
    rows = list(reader)
    if not rows:
        errors.append("CSV has no Jira rows")
        return errors
    if rows[0].get("Issue Type") != "Epic":
        errors.append("first Jira row must be the Epic container")
    story_rows = [row for row in rows if row.get("Issue Type") != "Epic"]
    if expected_story_count is not None and len(story_rows) != expected_story_count:
        errors.append(f"expected {expected_story_count} story row(s), got {len(story_rows)}")
    for index, row in enumerate(rows, start=2):
        if None in row:
            errors.append(f"line {index} has extra columns")
        for field in db.JIRA_FIELDS:
            if field not in row:
                errors.append(f"line {index} missing field {field}")
        for field in ("Issue Type", "Epic Name", "Summary", "Description", "Priority", "Labels", "Component", "Acceptance Criteria"):
            if not str(row.get(field) or "").strip():
                errors.append(f"line {index} has blank {field}")
        if row.get("Priority") and row["Priority"] not in JIRA_ALLOWED_PRIORITIES:
            errors.append(f"line {index} has unsupported priority {row['Priority']}")
    return errors


def validate_jira_csv_file(path: Path, *, expected_story_count: int | None = None) -> list[str]:
    return validate_jira_csv_content(path.read_text(encoding="utf-8"), expected_story_count=expected_story_count)


def jira_csv_content(conn, run_id: str, proposal_id: str | int | None = None) -> str:
    if not db.jira_export_rows(conn, run_id):
        db.build_jira_tickets(conn, run_id)
    expected_story_count = 1 if proposal_id not in (None, "") else None
    content = jira_csv_from_rows(
        db.jira_export_rows(conn, run_id, proposal_id=proposal_id),
        expected_story_count=expected_story_count,
        context=f"{run_id}:{proposal_id or 'all'}",
    )
    conn.execute(
        """
        INSERT INTO jira_exports(run_id, proposal_id, export_type, csv_content, created_at)
        VALUES(?, ?, 'jira_csv', ?, ?)
        """,
        (run_id, str(proposal_id) if proposal_id not in (None, "") else None, content, db.utc_now()),
    )
    return content


def csv_content(fieldnames: list[str], rows_to_write: list[dict[str, Any]]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in rows_to_write:
        writer.writerow({field: csv_safe_value(row.get(field, "")) for field in fieldnames})
    return output.getvalue()


def csv_safe_value(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    if not value:
        return value
    if value.startswith(FORMULA_PREFIXES):
        return f"'{value}"
    if value.startswith("-") and len(value) > 1 and value[1] in "0123456789=+-@(":
        return f"'{value}"
    return value


def csv_safe_row(row: dict[str, Any]) -> dict[str, Any]:
    return {key: csv_safe_value(value) for key, value in row.items()}


def slug(value: Any) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", str(value or "").strip())
    return cleaned.strip("-") or "item"


def display_proposal_id(rec: dict[str, Any]) -> str:
    return str(rec.get("source_proposal_id") or f"PROP-{rec.get('proposal_id')}")


def readiness_for(rec: dict[str, Any]) -> tuple[str, list[str]]:
    readiness = handoff_readiness_for(rec)
    return readiness.status, list(readiness.blockers)


def source_rows_for(rec: dict[str, Any], sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_ids = {int(value) for value in rec.get("evidence_source_ids") or [] if str(value).isdigit()}
    proposal_id = str(rec.get("proposal_id") or "")
    matched = [
        source
        for source in sources
        if int(source.get("source_id") or 0) in source_ids
        or proposal_id in [str(value) for value in source.get("related_recommendations") or []]
    ]
    return matched


def write_markdown(path: Path, lines: list[str]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return str(path)


def write_csv(path: Path, fieldnames: list[str], rows_to_write: list[dict[str, Any]]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(csv_content(fieldnames, rows_to_write), encoding="utf-8")
    return str(path)


def write_single_proposal_jira_csv(conn, path: Path, run_id: str, proposal_id: str) -> str:
    rows_to_write = db.jira_export_rows(conn, run_id, proposal_id=proposal_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        jira_csv_from_rows(rows_to_write, expected_story_count=1, context=f"{run_id}:{proposal_id}:{path.name}"),
        encoding="utf-8",
    )
    return str(path)


def render_recommendation_brief(rec: dict[str, Any], sources: list[dict[str, Any]], status: str, blockers: list[str]) -> list[str]:
    ticket = rec.get("jira_ticket") or {}
    lines = [
        f"# {display_proposal_id(rec)} - {rec.get('title') or 'Recommendation'}",
        "",
        f"- Run proposal ID: {rec.get('proposal_id')}",
        f"- Status: {status}",
        f"- Priority: {rec.get('priority_tier') or ticket.get('priority') or ''}",
        f"- Surface: {rec.get('surface') or ''}",
        f"- Component: {ticket.get('component') or ''}",
        f"- Pages: {', '.join(rec.get('page_refs') or ['Portfolio-wide / run-level'])}",
    ]
    if blockers:
        lines.append(f"- Review notes: {'; '.join(blockers)}")
    lines.extend(
        [
            "",
            "## Proposed Change",
            rec.get("proposed_change") or "",
            "",
            "## Current State",
            rec.get("current_state") or "",
            "",
            "## Rationale",
            rec.get("source_citation") or "",
            "",
            "## Impact",
            rec.get("impact_estimate") or "",
            "",
            "## Jira Summary",
            ticket.get("summary") or "",
            "",
            "## Jira Description",
            ticket.get("description") or "",
            "",
            "## Acceptance Criteria",
            ticket.get("acceptance_criteria") or "",
            "",
            "## Evidence Sources",
        ]
    )
    if not sources:
        lines.append("- Source evidence is available in the run research files, but no proposal-source link was imported.")
    for source in sources:
        lines.append(f"- S{source.get('source_id')}: {source.get('title_or_url') or source.get('url')}")
        if source.get("url"):
            lines.append(f"  {source.get('url')}")
    return lines


def render_handoff_note(rec: dict[str, Any], status: str) -> list[str]:
    ticket = rec.get("jira_ticket") or {}
    return [
        f"# {display_proposal_id(rec)} Handoff Note",
        "",
        f"Subject: {ticket.get('summary') or rec.get('title') or 'GEO recommendation'}",
        "",
        f"Status: {status}",
        "",
        "Recommended change:",
        rec.get("proposed_change") or "",
        "",
        "Why this matters:",
        rec.get("impact_estimate") or rec.get("source_citation") or "",
        "",
        "Requested next action:",
        "Review the attached Jira CSV row, confirm ownership/component, and import or paste the ticket into the delivery tracker.",
    ]


def render_acceptance_checklist(rec: dict[str, Any]) -> list[str]:
    ticket = rec.get("jira_ticket") or {}
    criteria = [line.strip("- ").strip() for line in str(ticket.get("acceptance_criteria") or "").splitlines() if line.strip()]
    lines = [f"# {display_proposal_id(rec)} Acceptance Checklist", ""]
    if criteria:
        lines.extend(f"- [ ] {item}" for item in criteria)
    else:
        lines.append("- [ ] Confirm the proposed change is implemented.")
        lines.append("- [ ] Rerun the GEO audit and confirm the linked gap is closed or downgraded.")
    lines.extend(["", "## Validation URL(s)"])
    for page in rec.get("page_refs") or ["Portfolio-wide / run-level"]:
        lines.append(f"- {page}")
    return lines


def render_source_evidence(rec: dict[str, Any], sources: list[dict[str, Any]]) -> list[str]:
    lines = [f"# {display_proposal_id(rec)} Source Evidence", ""]
    if rec.get("source_citation"):
        lines.extend(["## Proposal Citation", rec.get("source_citation") or "", ""])
    if not sources:
        lines.append("No linked source rows were imported for this proposal.")
        return lines
    for source in sources:
        lines.extend(
            [
                f"## S{source.get('source_id')} - {source.get('title_or_url') or source.get('url')}",
                f"- URL: {source.get('url') or ''}",
                f"- Finding group: {source.get('finding_group') or ''}",
                f"- Assessment: {source.get('ai_assessment_prose') or ''}",
                "",
            ]
        )
    return lines


def remap_written_paths(written: dict[str, str], old_root: Path, new_root: Path) -> dict[str, str]:
    remapped: dict[str, str] = {}
    for key, value in written.items():
        path = Path(value)
        try:
            remapped[key] = str(new_root / path.relative_to(old_root))
        except ValueError:
            remapped[key] = value
    return remapped


def publish_ready_dir(work_dir: Path, final_dir: Path) -> None:
    backup_dir = final_dir.with_name(f".{final_dir.name}.previous")
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    if final_dir.exists():
        final_dir.rename(backup_dir)
    try:
        work_dir.rename(final_dir)
    except Exception:
        if final_dir.exists():
            shutil.rmtree(final_dir)
        if backup_dir.exists():
            backup_dir.rename(final_dir)
        raise
    if backup_dir.exists():
        shutil.rmtree(backup_dir)


def export_ready_to_send_bundle(conn, run_id: str, run_dir: Path) -> dict[str, str]:
    run_id = validate_run_id(run_id)
    payload = dashboard_payload(conn, run_id)
    final_ready_dir = run_dir / READY_TO_SEND_DIRNAME
    ready_dir = run_dir / f".{READY_TO_SEND_DIRNAME}.building"
    if ready_dir.exists():
        shutil.rmtree(ready_dir)
    ready_dir.mkdir(parents=True, exist_ok=True)

    recs = payload.get("recommendations") or []
    sources = payload.get("sources") or []
    pages = payload.get("radisson_pages") or []
    changes = payload.get("metadata_changes") or []
    copy_blocks = payload.get("copy_blocks") or []
    written: dict[str, str] = {}
    recommendation_rows: list[dict[str, Any]] = []
    manifest_assets: list[str] = []
    validation_rows: list[dict[str, str]] = []
    core_assets = [
        "README.md",
        "stakeholder-email.md",
        "qa-checklist.md",
        f"{run_id}-jira-import.csv",
        JIRA_VALIDATION_REPORT,
        "recommendation-tracker.csv",
        "source-evidence.csv",
        "page-coverage.csv",
        "metadata-changes.csv",
        "copy-blocks.csv",
        "manifest.json",
    ]

    source_export_rows = [
        {
            "source_id": source.get("source_id"),
            "title_or_url": source.get("title_or_url"),
            "url": source.get("url"),
            "finding_group": source.get("finding_group"),
            "related_recommendations": ";".join(source.get("related_recommendations") or []),
            "assessment": source.get("ai_assessment_prose"),
        }
        for source in sources
    ]
    written["source_evidence_csv"] = write_csv(
        ready_dir / "source-evidence.csv",
        ["source_id", "title_or_url", "url", "finding_group", "related_recommendations", "assessment"],
        source_export_rows,
    )
    written["page_coverage_csv"] = write_csv(
        ready_dir / "page-coverage.csv",
        ["url", "page_label", "brand", "page_type", "fetch_status", "recommendations"],
        [
            {
                "url": page.get("canonical_url"),
                "page_label": page.get("page_label"),
                "brand": page.get("brand"),
                "page_type": page.get("page_type"),
                "fetch_status": (page.get("metadata_snapshot") or {}).get("fetch_status"),
                "recommendations": ";".join(page.get("recommendations") or []),
            }
            for page in pages
        ],
    )
    written["metadata_changes_csv"] = write_csv(
        ready_dir / "metadata-changes.csv",
        ["proposal_id", "page", "field_name", "current_value", "proposed_value", "warning"],
        [
            {
                "proposal_id": item.get("proposal_id"),
                "page": item.get("page"),
                "field_name": item.get("field_name"),
                "current_value": item.get("current_value"),
                "proposed_value": item.get("proposed_value"),
                "warning": item.get("warning"),
            }
            for item in changes
        ],
    )
    written["copy_blocks_csv"] = write_csv(
        ready_dir / "copy-blocks.csv",
        ["proposal_id", "target_page", "target_field_or_section", "format_type", "export_value"],
        [
            {
                "proposal_id": item.get("proposal_id"),
                "target_page": item.get("target_page"),
                "target_field_or_section": item.get("target_field_or_section"),
                "format_type": item.get("format_type"),
                "export_value": item.get("export_value"),
            }
            for item in copy_blocks
        ],
    )
    full_jira_path = ready_dir / f"{run_id}-jira-import.csv"
    full_jira_path.write_text(jira_csv_content(conn, run_id), encoding="utf-8")
    written["ready_jira_csv"] = str(full_jira_path)
    full_errors = validate_jira_csv_file(full_jira_path)
    validation_rows.append(
        {
            "asset": full_jira_path.relative_to(ready_dir).as_posix(),
            "scope": "full-run",
            "status": "PASS" if not full_errors else "FAIL",
            "notes": "; ".join(full_errors),
        }
    )

    for rec in recs:
        status, blockers = readiness_for(rec)
        rec_sources = source_rows_for(rec, sources)
        display_id = display_proposal_id(rec)
        folder = ready_dir / "recommendations" / f"{slug(display_id)}_{slug(rec.get('proposal_id'))}"
        recommendation_rows.append(
            {
                "proposal_id": rec.get("proposal_id"),
                "display_id": display_id,
                "status": status,
                "priority": rec.get("priority_tier"),
                "title": rec.get("title"),
                "component": (rec.get("jira_ticket") or {}).get("component"),
                "pages": ";".join(rec.get("page_refs") or []),
                "sources": ";".join(f"S{source.get('source_id')}" for source in rec_sources),
                "review_notes": "; ".join(blockers),
            }
        )
        jira_ticket_path = Path(
            write_single_proposal_jira_csv(
                conn,
                folder / JIRA_ITEM_FILENAME,
                run_id,
                str(rec.get("proposal_id")),
            )
        )
        item_errors = validate_jira_csv_file(jira_ticket_path, expected_story_count=1)
        validation_rows.append(
            {
                "asset": jira_ticket_path.relative_to(ready_dir).as_posix(),
                "scope": f"proposal:{rec.get('proposal_id')}",
                "status": "PASS" if not item_errors else "FAIL",
                "notes": "; ".join(item_errors),
            }
        )
        paths = [
            write_markdown(folder / "brief.md", render_recommendation_brief(rec, rec_sources, status, blockers)),
            str(jira_ticket_path),
            write_markdown(folder / "handoff-note.md", render_handoff_note(rec, status)),
            write_markdown(folder / "acceptance-checklist.md", render_acceptance_checklist(rec)),
            write_markdown(folder / "source-evidence.md", render_source_evidence(rec, rec_sources)),
        ]
        for path in paths:
            manifest_assets.append(str(Path(path).relative_to(ready_dir)))

    written["recommendation_tracker_csv"] = write_csv(
        ready_dir / "recommendation-tracker.csv",
        ["proposal_id", "display_id", "status", "priority", "title", "component", "pages", "sources", "review_notes"],
        recommendation_rows,
    )
    ready_count = sum(1 for row in recommendation_rows if row["status"] == READY_TO_SEND)
    needs_review = len(recommendation_rows) - ready_count
    validation_failures = [row for row in validation_rows if row["status"] != "PASS"]
    if validation_failures:
        details = "; ".join(f"{row['asset']}: {row['notes']}" for row in validation_failures)
        raise ValueError(f"Ready-to-send Jira CSV validation failed: {details}")
    written["jira_validation_report"] = write_markdown(
        ready_dir / JIRA_VALIDATION_REPORT,
        [
            f"# Jira CSV Validation - {run_id}",
            "",
            f"- Assets checked: {len(validation_rows)}",
            "- Status: PASS",
            "",
            "| Asset | Scope | Status | Notes |",
            "| --- | --- | --- | --- |",
            *[
                f"| {row['asset']} | {row['scope']} | {row['status']} | {row['notes']} |"
                for row in validation_rows
            ],
        ],
    )
    summary_lines = [
        f"# Ready-to-Send Bundle - {run_id}",
        "",
        f"- Recommendations: {len(recommendation_rows)}",
        f"- Ready-to-send: {ready_count}",
        f"- Needs review: {needs_review}",
        f"- Jira CSV validation: PASS ({len(validation_rows)} assets checked)",
        f"- Pages audited: {len(pages)}",
        f"- Sources linked: {len(sources)}",
        "",
        "## Core Files",
        "- recommendation-tracker.csv",
        f"- {run_id}-jira-import.csv",
        f"- {JIRA_VALIDATION_REPORT}",
        "- source-evidence.csv",
        "- page-coverage.csv",
        "- metadata-changes.csv",
        "- copy-blocks.csv",
        "",
        "## Recommendation Folders",
    ]
    summary_lines.extend(f"- recommendations/{slug(row['display_id'])}_{slug(row['proposal_id'])}/" for row in recommendation_rows)
    written["index"] = write_markdown(ready_dir / "README.md", summary_lines)
    written["stakeholder_email"] = write_markdown(
        ready_dir / "stakeholder-email.md",
        stakeholder_email_lines(run_id, ready_count, recommendation_rows),
    )
    written["qa_checklist"] = write_markdown(
        ready_dir / "qa-checklist.md",
        [
            f"# Ready-to-Send QA Checklist - {run_id}",
            "",
            "- [ ] Confirm the Jira import CSV opens with the expected RHG columns.",
            f"- [ ] Confirm `{JIRA_VALIDATION_REPORT}` shows PASS for the full-run CSV and every per-recommendation `{JIRA_ITEM_FILENAME}`.",
            f"- [ ] Confirm every recommendation folder has a brief, `{JIRA_ITEM_FILENAME}`, handoff note, acceptance checklist, and source evidence file.",
            "- [ ] Confirm source-evidence.csv contains cited sources for implementation rationale.",
            "- [ ] Confirm page-coverage.csv includes every selected run URL.",
            "- [ ] Confirm any team-specific owner/component overrides before sending.",
        ],
    )
    manifest = {
        "run_id": run_id,
        "ready_dir": str(final_ready_dir),
        "recommendations": len(recommendation_rows),
        "ready_to_send": ready_count,
        "needs_review": needs_review,
        "assets": sorted([*core_assets, *manifest_assets]),
    }
    manifest_path = ready_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    written["manifest"] = str(manifest_path)
    publish_ready_dir(ready_dir, final_ready_dir)
    return remap_written_paths(written, ready_dir, final_ready_dir)


def export_all(run_id: str, db_path: Path = db.DB_PATH, *, overwrite_artifacts: bool = False) -> dict[str, str]:
    run_id = validate_run_id(run_id)
    written: dict[str, str] = {}
    with db.connection(db_path) as conn:
        TARGET_URLS.parent.mkdir(parents=True, exist_ok=True)
        TARGET_URLS.write_text(render_target_urls(conn), encoding="utf-8")
        written["target_urls"] = str(TARGET_URLS)

        write_next_geo_run(conn, run_id=run_id)
        written["next_geo_run"] = str(NEXT_GEO_RUN)

        current_run_dir = run_dir_for(run_id)
        current_run_dir.mkdir(parents=True, exist_ok=True)
        proposal_path = (
            current_run_dir / "optimization_proposal.md"
            if overwrite_artifacts
            else current_run_dir / f"{run_id}_optimization_proposal_export.md"
        )
        proposal_path.write_text(render_optimization_proposal(conn, run_id), encoding="utf-8")
        written["optimization_proposal"] = str(proposal_path)

        sources_path = (
            ROOT / "literature" / f"{run_id}_sources.md"
            if overwrite_artifacts
            else ROOT / "literature" / f"{run_id}_sources_export.md"
        )
        sources_path.parent.mkdir(parents=True, exist_ok=True)
        sources_path.write_text(render_sources(conn, run_id), encoding="utf-8")
        written["sources"] = str(sources_path)

        jira_path = current_run_dir / f"{run_id}_jira_import.csv"
        jira_path.write_text(jira_csv_content(conn, run_id), encoding="utf-8")
        written["jira_csv"] = str(jira_path)

        ready_bundle = export_ready_to_send_bundle(conn, run_id, current_run_dir)
        written.update({f"ready_to_send_{name}": path for name, path in ready_bundle.items()})
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate GEO Optimizer exports from SQLite.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--db", default=str(db.DB_PATH))
    parser.add_argument("--overwrite-artifacts", action="store_true", help="Overwrite phase-authored markdown artifacts instead of writing *_export views.")
    args = parser.parse_args()
    written = export_all(args.run_id, Path(args.db), overwrite_artifacts=args.overwrite_artifacts)
    for name, path in written.items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
