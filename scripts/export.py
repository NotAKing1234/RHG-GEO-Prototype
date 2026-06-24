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
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import db


TARGET_URLS = ROOT / "sources" / "website" / "target_urls.md"
NEXT_GEO_RUN = ROOT / "sources" / "website" / "run_targets" / "next_geo_run.csv"


def run_dir_for(run_id: str) -> Path:
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
                {
                    "url": row["url"],
                    "brand": row.get("brand") or "",
                    "region": row.get("region") or "",
                    "page_type": row.get("page_type") or "",
                    "location_confidence": row.get("location_confidence") or "",
                    "selected_for_next_run": "true",
                    "selected_at": row.get("selected_at") or "",
                    "last_audited_run": row.get("last_audited_run") or "",
                }
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


def jira_csv_content(conn, run_id: str, proposal_id: str | int | None = None) -> str:
    if not db.jira_export_rows(conn, run_id):
        db.build_jira_tickets(conn, run_id)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=db.JIRA_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(db.jira_export_rows(conn, run_id, proposal_id=proposal_id))
    content = output.getvalue()
    conn.execute(
        """
        INSERT INTO jira_exports(run_id, proposal_id, export_type, csv_content, created_at)
        VALUES(?, ?, 'jira_csv', ?, ?)
        """,
        (run_id, str(proposal_id) if proposal_id not in (None, "") else None, content, db.utc_now()),
    )
    return content


def export_all(run_id: str, db_path: Path = db.DB_PATH) -> dict[str, str]:
    written: dict[str, str] = {}
    with db.connection(db_path) as conn:
        TARGET_URLS.parent.mkdir(parents=True, exist_ok=True)
        TARGET_URLS.write_text(render_target_urls(conn), encoding="utf-8")
        written["target_urls"] = str(TARGET_URLS)

        write_next_geo_run(conn, run_id=run_id)
        written["next_geo_run"] = str(NEXT_GEO_RUN)

        current_run_dir = run_dir_for(run_id)
        current_run_dir.mkdir(parents=True, exist_ok=True)
        proposal_path = current_run_dir / "optimization_proposal.md"
        proposal_path.write_text(render_optimization_proposal(conn, run_id), encoding="utf-8")
        written["optimization_proposal"] = str(proposal_path)

        sources_path = ROOT / "literature" / f"{run_id}_sources.md"
        sources_path.parent.mkdir(parents=True, exist_ok=True)
        sources_path.write_text(render_sources(conn, run_id), encoding="utf-8")
        written["sources"] = str(sources_path)

        jira_path = current_run_dir / f"{run_id}_jira_import.csv"
        jira_path.write_text(jira_csv_content(conn, run_id), encoding="utf-8")
        written["jira_csv"] = str(jira_path)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate GEO Optimizer exports from SQLite.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--db", default=str(db.DB_PATH))
    args = parser.parse_args()
    written = export_all(args.run_id, Path(args.db))
    for name, path in written.items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
