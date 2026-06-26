#!/usr/bin/env python3
"""Import historical run artifacts into the dashboard-ready SQLite read model.

Data flow: markdown artifacts remain preserved as raw run_artifacts while normalized tables
power dashboard reads. Pitfall: this importer is idempotent; it deletes only derived rows for
the target run and rebuilds them from source files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.parse
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import db
from scripts.migrate_to_sqlite import (  # noqa: E402
    block_value,
    clean_inline,
    field_value,
    infer_brand,
    migrate,
    migrated_gap_id,
    parse_criteria,
    parse_gaps,
    parse_proposals,
    parse_run_index,
    split_sections,
)


ARTIFACTS = {
    "context_brief": "context_brief.md",
    "gap_analysis": "gap_analysis.md",
    "gap_research": "gap_research.md",
    "metadata_snapshot": "metadata_snapshot.md",
    "optimization_proposal": "optimization_proposal.md",
    "log_reflection": "log_reflection.md",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def hash_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()


def key_for(*parts: str) -> str:
    return hashlib.sha1("|".join(parts).encode("utf-8", errors="replace")).hexdigest()[:18]


def urls_in(text: str) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    for raw in re.findall(r"https?://[^\s)<>\]\"']+", text or ""):
        url = raw.rstrip(".,;)]}\"'")
        if url not in seen:
            values.append(url)
            seen.add(url)
    return values


def domain_for(url: str | None) -> str:
    if not url:
        return ""
    return urllib.parse.urlsplit(url).netloc.removeprefix("www.")


def first_sentence(text: str, fallback: str) -> str:
    clean = clean_inline(re.sub(r"\s+", " ", text or "")).strip()
    if not clean:
        return fallback
    sentence = re.split(r"(?<=[.!?])\s+", clean)[0]
    return sentence[:500]


def scorecard_for(text: str) -> dict[str, Any]:
    lowered = (text or "").lower()
    return {
        "source_count": max(1, len(urls_in(text))),
        "has_urls": bool(urls_in(text)),
        "mentions_schema": any(term in lowered for term in ("schema", "json-ld", "structured data", "lodgingbusiness")),
        "mentions_ai_engine": any(term in lowered for term in ("chatgpt", "perplexity", "gemini", "claude", "ai engine", "ai search")),
        "mentions_traveler": any(term in lowered for term in ("traveler", "bleisure", "business travel", "american", "us-to-europe")),
    }


def run_dir_for(run_id: str) -> Path | None:
    matches = sorted((ROOT / "runs").glob(f"{run_id}_*"))
    return matches[-1] if matches else None


def store_artifacts(conn, run_id: str, run_dir: Path | None) -> None:
    paths: dict[str, Path] = {
        "literature_sources": ROOT / "literature" / f"{run_id}_sources.md",
        "criteria": ROOT / "framework" / f"{run_id}_criteria.md",
    }
    if run_dir:
        paths.update({kind: run_dir / filename for kind, filename in ARTIFACTS.items()})
    for artifact_type, path in paths.items():
        text = read_text(path)
        if not text:
            continue
        db.upsert_run_artifact(
            conn,
            run_id=run_id,
            artifact_type=artifact_type,
            path=rel(path),
            content_hash=hash_text(text),
            raw_text=text,
        )


def reset_derived_rows(conn, run_id: str) -> None:
    conn.execute("DELETE FROM proposal_sources WHERE run_id = ?", (run_id,))
    conn.execute(
        "DELETE FROM gap_insights WHERE gap_id IN (SELECT gap_id FROM gaps WHERE run_id = ?)",
        (run_id,),
    )
    conn.execute("DELETE FROM source_insights WHERE run_id = ?", (run_id,))
    conn.execute("DELETE FROM sources WHERE run_id = ?", (run_id,))
    conn.execute("DELETE FROM proposal_changes WHERE run_id = ?", (run_id,))
    conn.execute("DELETE FROM metadata_snapshots WHERE run_id = ?", (run_id,))
    conn.execute("DELETE FROM run_url_targets WHERE run_id = ?", (run_id,))


def import_core_rows(conn, run_id: str, run_dir: Path | None) -> None:
    for item in parse_criteria(ROOT / "framework" / f"{run_id}_criteria.md", run_id):
        db.upsert_criterion(conn, run_id, item["code"], item["description"])
    if not run_dir:
        return
    for item in parse_gaps(run_dir / "gap_analysis.md", run_id):
        url_id = db.upsert_url(conn, item["url"], brand=infer_brand(item["url"])) if item["url"] else None
        db.upsert_gap(
            conn,
            item["gap_id"],
            run_id,
            url_id=url_id,
            criterion_id=db.criterion_id_for_code(conn, run_id, item["criterion_code"]),
            gap_type=item["gap_type"],
            severity=item["severity"],
            status=item["status"],
            description=item["description"],
        )
    details = parse_proposal_details(run_dir / "optimization_proposal.md", run_id)
    for item in parse_proposals(run_dir / "optimization_proposal.md", run_id):
        detail = details.get(item["proposal_id"], {})
        if not conn.execute("SELECT gap_id FROM gaps WHERE gap_id = ?", (item["gap_id"],)).fetchone():
            db.upsert_gap(
                conn,
                item["gap_id"],
                run_id,
                url_id=None,
                criterion_id=None,
                gap_type="WEAK",
                severity=1,
                status="NEW",
                description="[NEEDED: proposal references a gap not present in gap_analysis.md]",
            )
        db.upsert_proposal(
            conn,
            item["proposal_id"],
            item["gap_id"],
            run_id,
            source_proposal_id=item.get("source_proposal_id"),
            proposed_change=item["proposed_change"],
            source_citation=detail.get("source_citation"),
            current_state=detail.get("current_state"),
            implementation_status=detail.get("implementation_status"),
            priority_tier=item["priority_tier"],
            impact_estimate=item["impact_estimate"],
        )
        import_proposal_change(conn, run_id, item, detail)


def parse_proposal_details(path: Path, run_id: str) -> dict[int, dict[str, str]]:
    values: dict[int, dict[str, str]] = {}
    for section in split_sections(read_text(path), r"###\s+PROP-\d+"):
        heading = re.match(r"^###\s+(PROP-(\d+))(?:\s+[—-]\s+(.+))?", section)
        if not heading:
            continue
        proposal_id = int(run_id.rsplit("_", 1)[-1]) * 1000 + int(heading.group(2))
        values[proposal_id] = {
            "source_proposal_id": heading.group(1),
            "title": clean_inline(heading.group(3) or heading.group(1)),
            "source_citation": field_value(section, "2. Source citation") or block_value(section, "2. Source citation"),
            "current_state": field_value(section, "3. Current state") or block_value(section, "3. Current state"),
            "implementation_status": field_value(section, "4. Inferred implementation status") or block_value(section, "4. Inferred implementation status"),
        }
    return values


def infer_change_type(text: str) -> str:
    lowered = text.lower()
    if any(term in lowered for term in ("json-ld", "schema", "structured data", "faqpage", "memberprogram", "aggregaterating", "review markup", "review json-ld")):
        return "schema_update"
    if any(term in lowered for term in ("chatgpt app", "openai apps sdk", "connector", "distribution roadmap", "hotel-search/feed", "review summary", "review pages", "aggregaterating/review")):
        return "trust_distribution"
    if any(term in lowered for term in ("cloudflare", "robots.txt", "llms.txt", "crawler", "crawlable", "403", "waf", "http 200", "sitemap", "access-restricted", "blocked", "noindex")):
        return "html_visibility"
    if any(term in lowered for term in ("title", "meta description", "metadata", "open graph", "canonical", "hreflang", "og field")):
        return "metadata_update"
    return "content_update"


def import_proposal_change(conn, run_id: str, proposal: dict[str, Any], detail: dict[str, str]) -> None:
    proposed = proposal.get("proposed_change") or ""
    current = detail.get("current_state") or ""
    change_type = infer_change_type(f"{proposed} {current}")
    target_page = first_url(proposed) or gap_url(conn, proposal.get("gap_id")) or ""
    conn.execute(
        """
        INSERT INTO proposal_changes(
            change_id, proposal_id, run_id, change_type, target_page,
            target_field_or_section, current_value, proposed_value, warning
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(change_id) DO UPDATE SET
            change_type=excluded.change_type,
            target_page=excluded.target_page,
            target_field_or_section=excluded.target_field_or_section,
            current_value=excluded.current_value,
            proposed_value=excluded.proposed_value,
            warning=excluded.warning
        """,
        (
            f"{run_id}:{proposal['proposal_id']}:primary",
            proposal["proposal_id"],
            run_id,
            change_type,
            target_page,
            label_for_change(change_type),
            current,
            proposed,
            "" if target_page or proposal.get("gap_id") else "warning: selector not inferred",
        ),
    )


def gap_url(conn, gap_id: str | None) -> str:
    if not gap_id:
        return ""
    found = conn.execute(
        """
        SELECT u.url
        FROM gaps g
        JOIN urls u ON u.url_id = g.url_id
        WHERE g.gap_id = ?
        """,
        (gap_id,),
    ).fetchone()
    return str(found["url"]) if found and found["url"] else ""


def first_url(text: str) -> str:
    found = urls_in(text)
    return found[0] if found else ""


def label_for_change(change_type: str) -> str:
    return {
        "schema_update": "Structured data / JSON-LD",
        "metadata_update": "Title or metadata field",
        "html_visibility": "Crawler or rendered HTML access",
        "trust_distribution": "Trust, reviews, or AI distribution",
        "content_update": "Page section",
    }.get(change_type, "Page section")


def import_metadata(conn, run_id: str, run_dir: Path | None) -> None:
    if not run_dir:
        return
    path = run_dir / "metadata_snapshot.md"
    text = read_text(path)
    for section in split_sections(text, r"##\s+Page\s+\d+:"):
        heading = re.match(r"^##\s+Page\s+\d+:\s+(\S+)(?:\s+\(([^)]+)\))?", section)
        url = field_value(section, "URL") or (heading.group(1) if heading else "")
        if not url:
            continue
        label = heading.group(2) if heading and heading.group(2) else clean_inline(url)
        url_id = db.upsert_url(conn, url, brand=infer_brand(url))
        fetch_timestamp = field_value(section, "Fetch timestamp")
        conn.execute(
            """
            INSERT OR IGNORE INTO run_url_targets(
                run_id, url_id, selection_source, selected_at, audit_profile, model
            )
            VALUES(?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                url_id,
                "artifact_import",
                fetch_timestamp or None,
                "metadata_light",
                "artifact_import",
            ),
        )
        conn.execute(
            """
            INSERT INTO metadata_snapshots(
                run_id, url_id, page_label, title, meta_description, fetch_status,
                raw_excerpt, source_path, captured_at
            )
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(run_id, url_id) DO UPDATE SET
                page_label=excluded.page_label,
                title=excluded.title,
                meta_description=excluded.meta_description,
                fetch_status=excluded.fetch_status,
                raw_excerpt=excluded.raw_excerpt,
                source_path=excluded.source_path,
                captured_at=excluded.captured_at
            """,
            (
                run_id,
                url_id,
                label,
                field_value(section, "Extracted title").strip('"'),
                (
                    field_value(section, "Extracted meta description")
                    or field_value(section, "Extracted meta/brand copy")
                    or field_value(section, "Extracted meta description (inferred from SERP/secondary)")
                ).strip('"'),
                field_value(section, "Fetch status"),
                section[:5000],
                rel(path),
                fetch_timestamp,
            ),
        )


def import_literature_sources(conn, run_id: str) -> None:
    path = ROOT / "literature" / f"{run_id}_sources.md"
    text = read_text(path)
    for section in split_sections(text, r"##\s+FINDING\s+\d+"):
        heading = re.match(r"^##\s+(.+)$", section)
        group = clean_inline(heading.group(1)) if heading else "Literature finding"
        source_urls = urls_in(section)
        for index, url in enumerate(source_urls, start=1):
            source_id = db.upsert_source(
                conn,
                run_id=run_id,
                source_key=f"literature:{key_for(run_id, group, url, str(index))}",
                url=url,
                domain=domain_for(url),
                title=domain_for(url) or group,
                source_type="literature",
                headline=group,
                finding_group=group,
                full_excerpt=section[:6000],
                ai_assessment_prose=first_sentence(section, group),
                scorecard=scorecard_for(section),
                fetched_at=None,
            )
            db.insert_source_insight(
                conn,
                source_id=source_id,
                run_id=run_id,
                claim=f"{group}: {first_sentence(section, 'Literature source consulted')}",
                theme="literature",
                evidence_url=url,
                excerpt=section[:1500],
            )


def gap_research_sections(text: str) -> list[str]:
    starts = [match.start() for match in re.finditer(r"(?m)^(?:###\s+|\*\*)GAP-\d+", text or "")]
    if not starts:
        return []
    starts.append(len(text))
    return [text[starts[index] : starts[index + 1]].strip() for index in range(len(starts) - 1)]


def gap_research_heading(section: str) -> tuple[str, str, str] | None:
    heading = re.match(
        r"^(?:###\s+|\*\*)(GAP-\d+)\s*(?:[|—-]\s*([^|*\n]+?))?(?:\s*[|—-]\s*(C\d+))?(?:\*\*)?",
        section,
    )
    if not heading:
        return None
    return heading.group(1), clean_inline(heading.group(2) or ""), heading.group(3) or ""


def import_gap_research_sources(conn, run_id: str, run_dir: Path | None) -> None:
    if not run_dir:
        return
    text = read_text(run_dir / "gap_research.md")
    for section in gap_research_sections(text):
        heading = gap_research_heading(section)
        if not heading:
            continue
        source_gap, title, criterion_code = heading
        gap_id = migrated_gap_id(run_id, source_gap)
        criterion_id = db.criterion_id_for_code(conn, run_id, criterion_code)
        urls = urls_in(section)
        for index, url in enumerate(urls, start=1):
            source_id = db.upsert_source(
                conn,
                run_id=run_id,
                source_key=f"gap_research:{key_for(run_id, source_gap, url, str(index))}",
                url=url,
                domain=domain_for(url),
                title=domain_for(url) or source_gap,
                source_type="gap_research",
                headline=f"{source_gap} {title}".strip(),
                finding_group=source_gap,
                full_excerpt=section[:8000],
                ai_assessment_prose=first_sentence(
                    block_value(section, "Best practice for closing it") or section,
                    f"Research evidence for {source_gap}",
                ),
                scorecard=scorecard_for(section),
                related_criteria=[criterion_code] if criterion_code else [],
                related_gaps=[gap_id],
                fetched_at=None,
            )
            insight_id = db.insert_source_insight(
                conn,
                source_id=source_id,
                run_id=run_id,
                claim=first_sentence(section, f"Evidence for {source_gap}"),
                theme=source_gap,
                evidence_url=url,
                excerpt=section[:1800],
                criterion_id=criterion_id,
            )
            if conn.execute("SELECT gap_id FROM gaps WHERE gap_id = ?", (gap_id,)).fetchone():
                conn.execute(
                    "INSERT OR IGNORE INTO gap_insights(gap_id, insight_id, role) VALUES(?, ?, ?)",
                    (gap_id, insight_id, "supporting_evidence"),
                )


def link_proposals_to_sources(conn, run_id: str, run_dir: Path | None) -> None:
    if not run_dir:
        return
    proposals = parse_proposals(run_dir / "optimization_proposal.md", run_id)
    for proposal in proposals:
        source_ids: set[int] = set()
        for gap_id in proposal.get("gap_refs") or [proposal["gap_id"]]:
            for item in db.rows(
                conn,
                """
                SELECT DISTINCT si.source_id
                FROM gap_insights gi
                JOIN source_insights si ON si.insight_id = gi.insight_id
                WHERE gi.gap_id = ?
                """,
                (gap_id,),
            ):
                source_ids.add(int(item["source_id"]))
        for source_id in source_ids:
            conn.execute(
                """
                INSERT OR IGNORE INTO proposal_sources(proposal_id, source_id, run_id, role)
                VALUES(?, ?, ?, 'evidence')
                """,
                (proposal["proposal_id"], source_id, run_id),
            )
        related = [str(proposal["proposal_id"])]
        if source_ids:
            for source_id in source_ids:
                conn.execute(
                    """
                    UPDATE sources
                    SET related_recommendations_json = ?
                    WHERE source_id = ?
                    """,
                    (json.dumps(related), source_id),
                )


def import_run(conn, run_id: str) -> dict[str, int]:
    run_dir = run_dir_for(run_id)
    store_artifacts(conn, run_id, run_dir)
    reset_derived_rows(conn, run_id)
    import_core_rows(conn, run_id, run_dir)
    import_metadata(conn, run_id, run_dir)
    import_literature_sources(conn, run_id)
    import_gap_research_sources(conn, run_id, run_dir)
    link_proposals_to_sources(conn, run_id, run_dir)
    db.build_jira_tickets(conn, run_id)
    return db.table_counts(conn)


def import_all_runs(db_path: Path = db.DB_PATH) -> dict[str, Any]:
    migrate(db_path)
    db.initialize_database(db_path)
    imported: dict[str, dict[str, int]] = {}
    with db.connection(db_path) as conn:
        for item in parse_run_index():
            imported[item["run_id"]] = import_run(conn, item["run_id"])
        counts = db.table_counts(conn)
    return {"db_path": str(db_path), "runs_imported": sorted(imported), "counts": counts}


def main() -> int:
    parser = argparse.ArgumentParser(description="Import run artifacts into dashboard SQLite tables.")
    parser.add_argument("--db", default=str(db.DB_PATH))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = import_all_runs(Path(args.db))
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Imported runs into {result['db_path']}")
        print(json.dumps(result["counts"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
