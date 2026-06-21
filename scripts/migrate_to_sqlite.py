#!/usr/bin/env python3
"""Migrate current GEO Optimizer files into SQLite.

Data flow: run index, target URL files, gap markdown, and proposal markdown are parsed into
the V1.1 tables. Pitfalls: the migration is idempotent, keeps files in place, and intentionally
does not backfill sources/source_insights because the spec starts those fresh on run_004.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import db


RUN_INDEX = ROOT / "memory" / "run_index.md"
TARGET_URLS = ROOT / "sources" / "website" / "target_urls.md"
URL_REGISTRY = ROOT / "sources" / "website" / "radisson_url_registry.csv"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def clean_inline(value: str) -> str:
    value = re.sub(r"`([^`]+)`", r"\1", value or "")
    value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    return re.sub(r"\s+", " ", value).strip(" -\n\t")


def block_value(text: str, label: str) -> str:
    pattern = (
        rf"^\s*\*\*{re.escape(label)}\*\*\s*\n"
        rf"(.*?)(?=^\s*\*\*(?:\d+\.\s*)?[^*\n]+?\*\*\s*$|^\s*###\s+|^\s*---\s*$|\Z)"
    )
    match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1).strip()
    pattern = rf"^\s*\*\*{re.escape(label)}:\*\*\s*(.*?)(?=^\s*\*\*[^*\n]+:\*\*|^\s*###\s+|^\s*---\s*$|\Z)"
    match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""


def field_value(text: str, label: str) -> str:
    patterns = [
        rf"^\s*\*\*{re.escape(label)}:\*\*\s*([^\n]+)",
        rf"^\s*[-*]\s*\*\*{re.escape(label)}:\*\*\s*([^\n]+)",
        rf"^\s*\d+\.\s+\*\*{re.escape(label)}:\*\*\s*([^\n]+)",
        rf"^\s*\d+\.\s+\*\*{re.escape(label)}\*\*\s*\n([^\n]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
        if match:
            return clean_inline(match.group(1))
    return clean_inline(block_value(text, label))


def split_sections(text: str, heading_re: str) -> list[str]:
    return [chunk.strip() for chunk in re.split(rf"(?=^{heading_re})", text or "", flags=re.MULTILINE) if chunk.strip()]


def parse_run_index(path: Path = RUN_INDEX) -> list[dict[str, Any]]:
    runs: list[dict[str, Any]] = []
    for line in read_text(path).splitlines():
        match = re.match(r"^(run_(\d{3,}))\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|", line.strip())
        if not match:
            continue
        runs.append({"run_id": match.group(1), "run_number": int(match.group(2)), "run_date": match.group(3)})
    for index, item in enumerate(runs):
        item["previous_run_id"] = runs[index - 1]["run_id"] if index else None
    return runs


def parse_target_urls(path: Path = TARGET_URLS) -> list[dict[str, str]]:
    urls: list[dict[str, str]] = []
    seen: set[str] = set()
    current_priority = ""
    for line in read_text(path).splitlines():
        heading = re.match(r"^##\s+(.+)$", line)
        if heading:
            current_priority = clean_inline(heading.group(1))
        match = re.match(r"^\s*[-*]\s*(https?://\S+)", line)
        if not match:
            continue
        url = match.group(1).rstrip(".,;)]}\"'")
        if url in seen:
            continue
        seen.add(url)
        urls.append(
            {
                "url": url,
                "brand": infer_brand(url),
                "region": "",
                "page_type": infer_page_type(url, current_priority),
                "location_confidence": "low" if current_priority else "",
            }
        )
    return urls


def parse_registry(path: Path = URL_REGISTRY) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        values: list[dict[str, str]] = []
        for row in reader:
            url = row.get("normalized_url") or row.get("canonical_url") or row.get("url") or ""
            if not url:
                continue
            values.append(
                {
                    "url": url,
                    "brand": row.get("brand") or "",
                    "region": row.get("region") or row.get("locale_region") or "",
                    "page_type": row.get("page_type") or row.get("content_group") or "",
                    "location_confidence": row.get("location_confidence") or "",
                    "selected_for_next_run": truthy(row.get("selected_for_next_run")),
                }
            )
        return values


def truthy(value: Any) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "y", "selected"}


def infer_brand(url: str) -> str:
    lowered = url.lower()
    if "radisson-blu" in lowered:
        return "Radisson Blu"
    if "radisson-collection" in lowered:
        return "Radisson Collection"
    if "radisson-red" in lowered:
        return "Radisson RED"
    if "park-plaza" in lowered:
        return "Park Plaza"
    if "park-inn" in lowered:
        return "Park Inn by Radisson"
    return "Radisson"


def infer_page_type(url: str, priority_label: str = "") -> str:
    lowered = url.lower()
    if "/brand/" in lowered:
        return "brand"
    if "/destination" in lowered:
        return "destination"
    if "/meeting" in lowered:
        return "meetings"
    if "/rewards" in lowered:
        return "loyalty"
    if "/hotel-deals" in lowered:
        return "offers"
    return priority_label or "page"


def parse_criteria(path: Path, run_id: str) -> list[dict[str, str]]:
    criteria: list[dict[str, str]] = []
    for section in split_sections(read_text(path), r"##\s+C\d+"):
        heading = re.match(r"^##\s+(C\d+)\s+[—-]\s+(.+)$", section, flags=re.MULTILINE)
        if not heading:
            continue
        description = field_value(section, "Signal name") or clean_inline(heading.group(2))
        passing = field_value(section, 'What "passing" looks like')
        if passing:
            description = f"{description}: {passing}"
        criteria.append({"run_id": run_id, "code": heading.group(1), "description": description})
    return criteria


def parse_gaps(path: Path, run_id: str) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    for section in split_sections(read_text(path), r"###\s+GAP-\d+"):
        heading = re.match(r"^###\s+(GAP-\d+)", section)
        if not heading:
            continue
        criterion = field_value(section, "Criterion")
        criterion_code = re.search(r"\b(C\d+)\b", criterion)
        severity_match = re.search(r"\d+", field_value(section, "Severity") or "")
        recurring = field_value(section, "New or recurring")
        gaps.append(
            {
                "source_gap_id": heading.group(1),
                "gap_id": migrated_gap_id(run_id, heading.group(1)),
                "run_id": run_id,
                "url": field_value(section, "Page URL"),
                "criterion_code": criterion_code.group(1) if criterion_code else "",
                "gap_type": (field_value(section, "Gap type") or "WEAK").upper(),
                "severity": int(severity_match.group(0)) if severity_match else 2,
                "status": "RECURRING" if "recurr" in recurring.lower() else "NEW",
                "description": field_value(section, "Gap description"),
            }
        )
    return gaps


def proposal_number(value: str) -> int | None:
    match = re.search(r"PROP-(\d+)", value or "")
    return int(match.group(1)) if match else None


def run_number(run_id: str) -> int:
    match = re.search(r"(\d+)$", run_id)
    return int(match.group(1)) if match else 0


def migrated_gap_id(run_id: str, source_gap_id: str) -> str:
    return f"{run_id}_{source_gap_id}"


def migrated_proposal_id(run_id: str, source_number: int) -> int:
    return run_number(run_id) * 1000 + source_number


def parse_proposals(path: Path, run_id: str) -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []
    for section in split_sections(read_text(path), r"###\s+PROP-\d+"):
        heading = re.match(r"^###\s+(PROP-\d+)(?:\s+[—-]\s+(.+))?", section)
        if not heading:
            continue
        gap_refs = re.findall(r"\bGAP-\d+\b", section)
        gap_match = gap_refs[0] if gap_refs else ""
        proposed_change = (
            field_value(section, "1. Proposed change")
            or block_value(section, "1. Proposed change")
            or field_value(section, "Proposed change")
        )
        priority = (
            field_value(section, "6. Priority tier")
            or field_value(section, "Priority tier")
            or field_value(section, "Priority")
            or "P3"
        )
        impact = (
            field_value(section, "5. Directional impact estimate")
            or field_value(section, "Directional impact estimate")
            or field_value(section, "Impact estimate")
        )
        number = proposal_number(heading.group(1))
        if not number or not gap_match or not proposed_change:
            continue
        proposals.append(
            {
                "proposal_id": migrated_proposal_id(run_id, number),
                "source_proposal_id": heading.group(1),
                "gap_id": migrated_gap_id(run_id, gap_match),
                "gap_refs": [migrated_gap_id(run_id, ref) for ref in gap_refs],
                "run_id": run_id,
                "proposed_change": clean_inline(proposed_change),
                "priority_tier": clean_inline(priority).upper()[:2] if clean_inline(priority).upper().startswith("P") else "P3",
                "impact_estimate": clean_inline(impact),
            }
        )
    return proposals


def source_counts() -> dict[str, int]:
    runs = parse_run_index()
    parsed_urls = {item["url"] for item in (parse_registry() or parse_target_urls())}
    criteria_count = 0
    gap_ids: set[str] = set()
    proposal_count = 0
    for item in runs:
        run_id = item["run_id"]
        criteria_count += len(parse_criteria(ROOT / "framework" / f"{run_id}_criteria.md", run_id))
        run_dir = next(iter(sorted((ROOT / "runs").glob(f"{run_id}_*"))), None)
        if run_dir:
            gaps = parse_gaps(run_dir / "gap_analysis.md", run_id)
            gap_ids.update(item["gap_id"] for item in gaps)
            parsed_urls.update(item["url"] for item in gaps if item["url"])
            proposals = parse_proposals(run_dir / "optimization_proposal.md", run_id)
            for proposal in proposals:
                gap_ids.add(proposal["gap_id"])
            proposal_count += len(proposals)
    return {
        "runs": len(runs),
        "urls": len(parsed_urls),
        "criteria": criteria_count,
        "gaps": len(gap_ids),
        "proposals": proposal_count,
    }


def migrate(db_path: Path = db.DB_PATH) -> dict[str, Any]:
    db.initialize_database(db_path)
    parsed_counts = source_counts()
    with db.connection(db_path) as conn:
        for item in parse_run_index():
            db.upsert_run(conn, item["run_id"], item["run_number"], item["run_date"], "COMPLETED", item["previous_run_id"])

        for item in parse_registry() or parse_target_urls():
            db.upsert_url(
                conn,
                item["url"],
                brand=item.get("brand") or None,
                region=item.get("region") or None,
                page_type=item.get("page_type") or None,
                location_confidence=item.get("location_confidence") or None,
                selected_for_next_run=item.get("selected_for_next_run") if "selected_for_next_run" in item else None,
            )

        for run_item in parse_run_index():
            run_id = run_item["run_id"]
            for item in parse_criteria(ROOT / "framework" / f"{run_id}_criteria.md", run_id):
                db.upsert_criterion(conn, run_id, item["code"], item["description"])

            run_dirs = sorted((ROOT / "runs").glob(f"{run_id}_*"))
            if not run_dirs:
                continue
            run_dir = run_dirs[-1]
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
            for item in parse_proposals(run_dir / "optimization_proposal.md", run_id):
                existing_gap = conn.execute("SELECT gap_id FROM gaps WHERE gap_id = ?", (item["gap_id"],)).fetchone()
                if not existing_gap:
                    db.upsert_gap(
                        conn,
                        item["gap_id"],
                        run_id,
                        url_id=None,
                        criterion_id=None,
                        gap_type="WEAK",
                        severity=1,
                        status="RECURRING",
                        description="[NEEDED: gap details referenced by optimization_proposal.md but absent from gap_analysis.md]",
                    )
                db.upsert_proposal(
                    conn,
                    item["proposal_id"],
                    item["gap_id"],
                    run_id,
                    proposed_change=item["proposed_change"],
                    priority_tier=item["priority_tier"],
                    impact_estimate=item["impact_estimate"],
                )
                db.build_jira_tickets(conn, run_id)

        actual_counts = db.table_counts(conn)

    mismatches = {
        table: {"parsed": parsed_counts[table], "actual": actual_counts[table]}
        for table in ("runs", "urls", "criteria", "gaps", "proposals")
        if parsed_counts[table] != actual_counts[table]
    }
    return {
        "db_path": str(db_path),
        "parsed_counts": parsed_counts,
        "actual_counts": actual_counts,
        "valid": not mismatches,
        "mismatches": mismatches,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate GEO Optimizer flat files into SQLite.")
    parser.add_argument("--db", default=str(db.DB_PATH), help="SQLite DB path")
    parser.add_argument("--json", action="store_true", help="Print JSON validation output")
    args = parser.parse_args()
    result = migrate(Path(args.db))
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Migrated {result['db_path']}")
        print(f"Valid: {result['valid']}")
        if result["mismatches"]:
            print(json.dumps(result["mismatches"], indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
