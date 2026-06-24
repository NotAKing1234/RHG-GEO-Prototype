#!/usr/bin/env python3
"""Dashboard read model for the DB-backed Radisson GEO Optimizer.

Data flow: normalized SQLite rows are shaped into the existing React dashboard contract.
Pitfall: keep frontend field names stable while the storage model changes underneath.
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

from scripts import db


def latest_run_id(conn) -> str | None:
    found = conn.execute("SELECT run_id FROM runs ORDER BY run_number DESC LIMIT 1").fetchone()
    return str(found["run_id"]) if found else None


def dashboard_runs(conn) -> list[dict[str, Any]]:
    return db.rows(
        conn,
        """
        SELECT run_id, run_number, run_date AS date, status, previous_run_id
        FROM runs
        ORDER BY run_number
        """,
    )


def proposal_public_id(value: Any) -> str:
    return str(value)


def priority_score(priority_tier: str | None, severity: int | None, source_count: int) -> int:
    base = {"P1": 88, "P2": 72, "P3": 55}.get((priority_tier or "P3").upper(), 48)
    severity_boost = max(0, int(severity or 0) - 1) * 3
    evidence_boost = min(4, source_count)
    return min(99, base + severity_boost + evidence_boost)


def selector_status_for(change_type: str | None, target_page: str | None) -> str:
    if change_type in {"schema_update", "metadata_update"}:
        return "metadata field target"
    if target_page:
        return "team override selector"
    return "warning: selector not inferred"


def surface_for(change_type: str | None, fallback: str | None) -> str:
    if change_type == "schema_update":
        return "Metadata / Structured Data"
    if change_type == "metadata_update":
        return "Metadata"
    if change_type == "html_visibility":
        return "Strategic / Infrastructure"
    return fallback or "Front-end content"


def source_ids_for_proposal(conn, proposal_id: int) -> list[int]:
    return [
        int(item["source_id"])
        for item in db.rows(
            conn,
            "SELECT source_id FROM proposal_sources WHERE proposal_id = ? ORDER BY source_id",
            (proposal_id,),
        )
    ]


def jira_ticket_for(conn, run_id: str, proposal_id: int) -> dict[str, Any]:
    found = db.row(
        conn,
        """
        SELECT issue_type, epic_name, summary, description, priority, labels, component, acceptance_criteria
        FROM jira_tickets
        WHERE run_id = ? AND proposal_id = ?
        ORDER BY jira_ticket_id DESC
        LIMIT 1
        """,
        (run_id, proposal_id),
    )
    if not found:
        return {}
    return {
        "issue_type": found["issue_type"],
        "epic_name": found["epic_name"],
        "summary": found["summary"],
        "description": found.get("description") or "",
        "priority": found["priority"],
        "labels": found.get("labels") or "",
        "component": found.get("component") or "",
        "acceptance_criteria": found.get("acceptance_criteria") or "",
    }


def proposal_changes(conn, run_id: str) -> list[dict[str, Any]]:
    return db.rows(
        conn,
        """
        SELECT change_id, proposal_id, run_id, change_type, target_page, target_field_or_section,
               current_value, proposed_value, warning
        FROM proposal_changes
        WHERE run_id = ?
        ORDER BY proposal_id, change_id
        """,
        (run_id,),
    )


def first_change_by_proposal(changes: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    values: dict[int, dict[str, Any]] = {}
    for item in changes:
        values.setdefault(int(item["proposal_id"]), item)
    return values


def recommendations(conn, run_id: str) -> list[dict[str, Any]]:
    changes = proposal_changes(conn, run_id)
    change_by_proposal = first_change_by_proposal(changes)
    overrides = db.dashboard_overrides_for_run(conn, run_id)
    values = db.rows(
        conn,
        """
        SELECT p.proposal_id, p.source_proposal_id, p.proposed_change, p.source_citation,
               p.current_state, p.implementation_status, p.priority_tier, p.impact_estimate,
               p.handoff_status, g.gap_id, g.gap_type, g.severity, g.status AS gap_status,
               g.description AS gap_description, u.url, u.brand, u.page_type,
               c.code AS criterion_code, c.description AS criterion_description
        FROM proposals p
        JOIN gaps g ON g.gap_id = p.gap_id
        LEFT JOIN urls u ON u.url_id = g.url_id
        LEFT JOIN criteria c ON c.criterion_id = g.criterion_id
        WHERE p.run_id = ?
        ORDER BY p.priority_tier, g.severity DESC, p.proposal_id
        """,
        (run_id,),
    )
    recs: list[dict[str, Any]] = []
    for item in values:
        proposal_id = int(item["proposal_id"])
        change = change_by_proposal.get(proposal_id, {})
        evidence_ids = source_ids_for_proposal(conn, proposal_id)
        public_id = proposal_public_id(proposal_id)
        current_state = item.get("current_state") or item.get("gap_description") or ""
        proposed_change = item.get("proposed_change") or ""
        score = priority_score(item.get("priority_tier"), item.get("severity"), len(evidence_ids))
        change_type = change.get("change_type")
        recs.append(
            {
                "proposal_id": public_id,
                "source_proposal_id": item.get("source_proposal_id") or "",
                "title": db.summarize_change(proposed_change),
                "combined_score": score,
                "surface": surface_for(change_type, item.get("page_type")),
                "page_refs": [item["url"]] if item.get("url") else [],
                "section_label": change.get("target_field_or_section") or item.get("criterion_code") or "Page section",
                "inferred_dom_selector": change.get("target_field_or_section") or "",
                "selector_status": selector_status_for(change_type, item.get("url")),
                "evidence_tier": "Implementation-ready" if evidence_ids else "Need review",
                "evidence_source_ids": evidence_ids,
                "priority_tier": item.get("priority_tier") or "",
                "priority_components": {
                    "business_impact": min(5, max(1, int(item.get("severity") or 1) + 2)),
                    "geo_relevance": 5 if evidence_ids else 3,
                    "evidence_strength": min(5, max(1, len(evidence_ids))),
                    "ease_of_implementation": 3,
                },
                "current_state": current_state,
                "proposed_change": proposed_change,
                "source_citation": item.get("source_citation") or item.get("criterion_description") or "",
                "impact_estimate": item.get("impact_estimate") or "",
                "implementation_status": item.get("implementation_status") or "",
                "before_after": {"before": current_state, "after": proposed_change},
                "jira_ticket": jira_ticket_for(conn, run_id, proposal_id),
                "team_override": overrides.get(public_id) or {},
                "gap_refs": [item.get("gap_id")],
                "criterion_refs": [item.get("criterion_code")] if item.get("criterion_code") else [],
                "diagram": {
                    "nodes": [public_id, item.get("gap_id"), *(f"S{sid}" for sid in evidence_ids)],
                    "edges": [
                        {"from": public_id, "to": item.get("gap_id"), "label": "addresses"},
                        *[{"from": f"S{sid}", "to": public_id, "label": "supports"} for sid in evidence_ids],
                    ],
                },
            }
        )
    return recs


def metadata_changes(conn, run_id: str) -> list[dict[str, Any]]:
    values = []
    for item in proposal_changes(conn, run_id):
        values.append(
            {
                "metadata_change_id": item["change_id"],
                "proposal_id": proposal_public_id(item["proposal_id"]),
                "page": item.get("target_page") or "",
                "field_name": item.get("target_field_or_section") or item.get("change_type") or "Implementation field",
                "current_value": item.get("current_value") or "",
                "proposed_value": item.get("proposed_value") or "",
                "warning": item.get("warning") or "",
                "evidence_source_ids": source_ids_for_proposal(conn, int(item["proposal_id"])),
            }
        )
    return values


def copy_blocks(conn, run_id: str, recs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rec_by_id = {item["proposal_id"]: item for item in recs}
    blocks: list[dict[str, Any]] = []
    for item in proposal_changes(conn, run_id):
        public_id = proposal_public_id(item["proposal_id"])
        override = rec_by_id.get(public_id, {}).get("team_override") or {}
        adjusted = override.get("adjusted_copy") if isinstance(override.get("adjusted_copy"), dict) else {}
        block_id = f"copy:{item['change_id']}"
        blocks.append(
            {
                "copy_block_id": block_id,
                "proposal_id": public_id,
                "target_page": item.get("target_page") or "",
                "target_field_or_section": item.get("target_field_or_section") or "",
                "copy_label": item.get("target_field_or_section") or "Proposed copy",
                "format_type": item.get("change_type") or "content_update",
                "original_text": item.get("current_value") or "",
                "export_value": item.get("proposed_value") or "",
                "adjusted_text": adjusted.get(block_id) or "",
            }
        )
    return blocks


def pages(conn, run_id: str, recs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    recs_by_url: dict[str, list[str]] = {}
    for rec in recs:
        for url in rec.get("page_refs") or []:
            recs_by_url.setdefault(url, []).append(rec["proposal_id"])
    values = db.rows(
        conn,
        """
        SELECT ms.snapshot_id, ms.page_label, ms.title, ms.meta_description, ms.fetch_status,
               ms.raw_excerpt, ms.source_path, ms.live_capture_json, ms.captured_at,
               u.url, u.brand, u.region, u.page_type
        FROM metadata_snapshots ms
        JOIN urls u ON u.url_id = ms.url_id
        WHERE ms.run_id = ?
        ORDER BY ms.snapshot_id
        """,
        (run_id,),
    )
    if not values:
        values = db.rows(
            conn,
            """
            SELECT DISTINCT u.url, u.brand, u.region, u.page_type
            FROM gaps g
            JOIN urls u ON u.url_id = g.url_id
            WHERE g.run_id = ?
            ORDER BY u.url
            """,
            (run_id,),
        )
    results: list[dict[str, Any]] = []
    for item in values:
        capture = db.json_loads(item.get("live_capture_json"), None) if "live_capture_json" in item else None
        url = item["url"]
        results.append(
            {
                "canonical_url": url,
                "source_url": url,
                "page_label": item.get("page_label") or label_for_url(url),
                "brand": item.get("brand") or "",
                "page_type": item.get("page_type") or "",
                "recommendations": recs_by_url.get(url, []),
                "metadata_snapshot": {
                    "title": item.get("title") or "",
                    "meta_description": item.get("meta_description") or "",
                    "fetch_status": item.get("fetch_status") or "",
                    "raw_excerpt": item.get("raw_excerpt") or "",
                    "source_path": item.get("source_path") or "",
                },
                "live_capture_refs": capture or {"status": "not_captured"},
            }
        )
    return results


def label_for_url(url: str) -> str:
    path = urllib.parse.urlsplit(url).path.strip("/") or "Homepage"
    return path.split("/")[-1].replace("-", " ").title()


def sources(conn, run_id: str) -> list[dict[str, Any]]:
    values = db.rows(
        conn,
        """
        SELECT source_id, source_key, url, domain, title, source_type, headline, finding_group,
               full_excerpt, ai_assessment_prose, scorecard_json, related_criteria_json,
               related_gaps_json, related_recommendations_json
        FROM sources
        WHERE run_id = ?
        ORDER BY source_id
        """,
        (run_id,),
    )
    return [
        {
            "source_id": item["source_id"],
            "source_key": item.get("source_key") or "",
            "url": item.get("url") or "",
            "title_or_url": item.get("title") or item.get("url") or f"Source {item['source_id']}",
            "headline": item.get("headline") or item.get("title") or "",
            "finding_group": item.get("finding_group") or item.get("source_type") or "",
            "full_excerpt": item.get("full_excerpt") or "",
            "ai_assessment_prose": item.get("ai_assessment_prose") or "",
            "scorecard": db.json_loads(item.get("scorecard_json"), {}) or {},
            "related_criteria": db.json_loads(item.get("related_criteria_json"), []) or [],
            "related_gaps": db.json_loads(item.get("related_gaps_json"), []) or [],
            "related_recommendations": [proposal_public_id(value) for value in db.json_loads(item.get("related_recommendations_json"), []) or []],
        }
        for item in values
    ]


def summary_for(run: dict[str, Any], recs: list[dict[str, Any]], source_values: list[dict[str, Any]], page_values: list[dict[str, Any]], changes: list[dict[str, Any]]) -> dict[str, Any]:
    ready = [item for item in recs if item.get("evidence_tier") == "Implementation-ready" and not str(item.get("selector_status", "")).startswith("warning")]
    return {
        "recommendations": len(recs),
        "ready_to_send": len(ready),
        "needs_review": len(recs) - len(ready),
        "sources": len(source_values),
        "pages": len(page_values),
        "metadata_changes": len(changes),
        "copy_blocks": len(changes),
        "average_score": round(sum(int(item.get("combined_score") or 0) for item in recs) / max(1, len(recs)), 1),
        "selector_warnings": sum(1 for item in recs if str(item.get("selector_status", "")).startswith("warning")),
        "crawl": {
            "blockedPages": sum(1 for page in page_values if re.search(r"403|blocked|restricted", page.get("metadata_snapshot", {}).get("fetch_status", ""), re.I)),
        },
    }


def source_graph(source_values: list[dict[str, Any]], recs: list[dict[str, Any]]) -> dict[str, Any]:
    edges: list[dict[str, str]] = []
    for source in source_values:
        source_id = f"S{source['source_id']}"
        for proposal_id in source.get("related_recommendations") or []:
            edges.append({"from": source_id, "to": proposal_id, "label": "supports"})
    return {"nodes": [{"id": f"S{source['source_id']}"} for source in source_values] + [{"id": rec["proposal_id"]} for rec in recs], "edges": edges}


def dashboard_payload(conn, run_id: str | None = None) -> dict[str, Any]:
    run_id = run_id or latest_run_id(conn)
    if not run_id:
        return {
            "run": {"run_id": "", "date": "", "validation_errors": ["No runs imported."]},
            "recommendations": [],
            "radisson_pages": [],
            "sources": [],
            "copy_blocks": [],
            "metadata_changes": [],
            "source_diagrams": {"source_graph": {"nodes": [], "edges": []}},
            "summary": {},
        }
    run = db.row(conn, "SELECT run_id, run_number, run_date AS date, status FROM runs WHERE run_id = ?", (run_id,))
    recs = recommendations(conn, run_id)
    source_values = sources(conn, run_id)
    page_values = pages(conn, run_id, recs)
    changes = metadata_changes(conn, run_id)
    copies = copy_blocks(conn, run_id, recs)
    validation_errors = []
    if not source_values:
        validation_errors.append("No sources imported for this run.")
    if not recs:
        validation_errors.append("No proposals imported for this run.")
    payload = {
        "run": {**(run or {"run_id": run_id, "date": "", "status": "UNKNOWN"}), "validation_errors": validation_errors},
        "recommendations": recs,
        "radisson_pages": page_values,
        "sources": source_values,
        "copy_blocks": copies,
        "metadata_changes": changes,
        "source_diagrams": {"source_graph": source_graph(source_values, recs)},
        "summary": summary_for(run or {}, recs, source_values, page_values, changes),
    }
    return payload


def capture_page(conn, run_id: str, url: str) -> dict[str, Any]:
    status = "captured"
    title = ""
    description = ""
    error = ""
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 GEOptimizer local dashboard"})
        with urllib.request.urlopen(request, timeout=8) as response:
            body = response.read(250_000).decode("utf-8", errors="replace")
            status = f"http_{response.status}"
            title_match = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
            desc_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', body, re.I)
            title = re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else ""
            description = re.sub(r"\s+", " ", desc_match.group(1)).strip() if desc_match else ""
    except urllib.error.HTTPError as exc:
        status = f"http_{exc.code}"
        error = str(exc)
    except Exception as exc:  # noqa: BLE001 - dashboard should record capture failure, not crash.
        status = "capture_failed"
        error = str(exc)
    url_id = db.upsert_url(conn, url)
    capture = {
        "status": status,
        "capture_method": "http_fallback",
        "captured_at": datetime.now().isoformat(timespec="seconds"),
        "playwright_error": error,
        "metadata": {"title": title, "description": description},
        "selector_candidates": [],
    }
    conn.execute(
        """
        INSERT INTO metadata_snapshots(run_id, url_id, page_label, fetch_status, live_capture_json, captured_at)
        VALUES(?, ?, ?, ?, ?, ?)
        ON CONFLICT(run_id, url_id) DO UPDATE SET
            live_capture_json=excluded.live_capture_json,
            captured_at=excluded.captured_at,
            fetch_status=COALESCE(metadata_snapshots.fetch_status, excluded.fetch_status)
        """,
        (run_id, url_id, label_for_url(url), status, json.dumps(capture), capture["captured_at"]),
    )
    return capture


def csv_export(payload: dict[str, Any]) -> str:
    import csv
    import io

    output = io.StringIO()
    fieldnames = ["proposal_id", "title", "score", "priority", "surface", "pages", "sources", "proposed_change"]
    writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for rec in payload.get("recommendations", []):
        writer.writerow(
            {
                "proposal_id": rec.get("proposal_id"),
                "title": rec.get("title"),
                "score": rec.get("combined_score"),
                "priority": rec.get("priority_tier"),
                "surface": rec.get("surface"),
                "pages": ";".join(rec.get("page_refs") or []),
                "sources": ";".join(str(value) for value in rec.get("evidence_source_ids") or []),
                "proposed_change": rec.get("proposed_change"),
            }
        )
    return output.getvalue()


def clipboard_export(payload: dict[str, Any]) -> str:
    lines = [f"GEOptimizer handoff - {payload.get('run', {}).get('run_id', '')}", ""]
    for rec in payload.get("recommendations", [])[:20]:
        lines.extend(
            [
                f"{rec.get('proposal_id')} | {rec.get('priority_tier')} | {rec.get('title')}",
                f"Pages: {', '.join(rec.get('page_refs') or ['Portfolio-wide'])}",
                f"Change: {rec.get('proposed_change')}",
                "",
            ]
        )
    return "\n".join(lines)


def audit_export(payload: dict[str, Any]) -> str:
    lines = [clipboard_export(payload), "Sources", ""]
    for source in payload.get("sources", [])[:60]:
        lines.extend([f"- {source.get('title_or_url')}", f"  {source.get('url')}", f"  {source.get('ai_assessment_prose')}", ""])
    return "\n".join(lines)
