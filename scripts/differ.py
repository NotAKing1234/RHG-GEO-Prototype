#!/usr/bin/env python3
"""Compare metadata snapshots and generate a run context brief."""

from __future__ import annotations

import argparse
import json
import logging
import re
import urllib.parse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = ROOT / "runs" / "active_run.json"
URL_RE = re.compile(r"https?://[^\s)<>'\"]+")

FIELD_LABELS = {
    "fetch_status": ["Fetch status"],
    "title": ["Extracted title", "Title"],
    "meta_description": ["Extracted meta description", "Extracted meta/brand copy", "Meta Description"],
    "schema": ["JSON-LD Schema Types", "Structured data blocks", "Structured data"],
    "open_graph": ["Open Graph tags", "OG tags"],
    "headings": ["Heading outline", "Headings"],
    "faq": ["FAQ / Q&A presence", "FAQ/Q&A", "FAQ presence"],
}

ABSENT_MARKERS = (
    "NONE",
    "NOT CONFIRMABLE",
    "NOT DETECTED",
    "ACCESS RESTRICTED",
    "YOUR ACCESS HAS BEEN RESTRICTED",
    "PENDING MANUAL",
    "FETCH FAILED",
    "403",
    "BLOCKED",
    "SKIPPED",
    "MOCK",
    "UNAVAILABLE",
    "ABSENT",
)


@dataclass
class SnapshotPage:
    url: str
    label: str
    fields: dict[str, str]


def repo_path(path: str | Path | None) -> Path | None:
    if path is None:
        return None
    path = Path(path)
    return path if path.is_absolute() else ROOT / path


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def canonicalize_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url.strip().rstrip(".,;]"))
    path = parsed.path or "/"
    return urllib.parse.urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path.rstrip("/") or "/", "", ""))


def clean_inline(value: str) -> str:
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip(" -\n\t")


def truncate(value: str, limit: int = 140) -> str:
    value = clean_inline(value)
    if len(value) <= limit:
        return value
    return value[: limit - 3].rsplit(" ", 1)[0].rstrip(" ,;:") + "..."


def normalize_field_label(label: str) -> str:
    label = label.lower().strip()
    label = re.sub(r"\s*\([^)]*\)", "", label)
    label = label.replace(" / ", "/")
    return label


def extract_bold_block(section: str, labels: list[str]) -> str:
    normalized_labels = [normalize_field_label(item) for item in labels]
    lines = section.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r"\*\*([^*]+):\*\*\s*(.*)", line.strip())
        if not match:
            continue
        label = normalize_field_label(match.group(1))
        if not any(label.startswith(expected) for expected in normalized_labels):
            continue
        value = match.group(2).strip()
        continuation: list[str] = []
        for follow in lines[index + 1 :]:
            stripped = follow.strip()
            if not stripped:
                if continuation:
                    break
                continue
            if re.match(r"\*\*[^*]+:\*\*", stripped) or stripped.startswith("## "):
                break
            if stripped.startswith("```"):
                break
            continuation.append(stripped)
            if len(" ".join(continuation)) > 500:
                break
        combined = " ".join([value, *continuation]).strip()
        return clean_inline(combined) or "NONE"
    return "NONE"


def parse_page_label(header: str, url: str) -> str:
    label = header
    label = re.sub(r"^##\s+Page\s+\d+[^:]*:\s*", "", label).strip()
    label = label.replace(url, "").strip(" -()")
    return label or url


def parse_snapshot(filepath: str | Path) -> dict[str, SnapshotPage]:
    path = repo_path(filepath)
    if path is None or not path.exists():
        raise FileNotFoundError(f"Snapshot not found: {filepath}")

    text = path.read_text(encoding="utf-8")
    sections = re.split(r"(?=^##\s+Page\s+\d+)", text, flags=re.MULTILINE)
    pages: dict[str, SnapshotPage] = {}
    for section in sections:
        lines = section.splitlines()
        if not lines or not lines[0].startswith("## "):
            continue
        header = lines[0]
        url_match = re.search(r"\*\*URL:\*\*\s*(\S+)", section)
        if not url_match:
            url_match = URL_RE.search(header)
        if not url_match:
            continue
        url = canonicalize_url(url_match.group(1))
        fields = {
            field: extract_bold_block(section, labels)
            for field, labels in FIELD_LABELS.items()
        }
        pages[url] = SnapshotPage(url=url, label=parse_page_label(header, url), fields=fields)
    return pages


def value_is_absent(value: str) -> bool:
    value_upper = clean_inline(value).upper()
    if not value_upper:
        return True
    return any(marker in value_upper for marker in ABSENT_MARKERS)


def normalized_value(value: str) -> str:
    return clean_inline(value).strip('"').strip("'")


def classify_change(field: str, previous: str, current: str) -> str:
    prev = normalized_value(previous)
    curr = normalized_value(current)
    if prev == curr:
        return "UNCHANGED"
    if value_is_absent(prev) and value_is_absent(curr):
        return "UNCHANGED"
    if value_is_absent(prev) and not value_is_absent(curr):
        return "IMPLEMENTED"
    if field == "fetch_status" and ("403" in prev or "BLOCKED" in prev.upper()) and "200" in curr:
        return "IMPLEMENTED"
    if field in {"title", "meta_description"} and not value_is_absent(curr):
        return "IMPLEMENTED"
    if field == "schema" and value_is_absent(prev) and not value_is_absent(curr):
        return "IMPLEMENTED"
    return "CHANGED"


def compare_snapshots(
    previous_pages: dict[str, SnapshotPage],
    current_pages: dict[str, SnapshotPage],
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    rows: list[dict[str, Any]] = []
    previous_urls = set(previous_pages)
    current_urls = set(current_pages)
    common_urls = sorted(previous_urls & current_urls)

    for url in common_urls:
        previous = previous_pages[url]
        current = current_pages[url]
        for field in FIELD_LABELS:
            previous_value = previous.fields.get(field, "NONE")
            current_value = current.fields.get(field, "NONE")
            status = classify_change(field, previous_value, current_value)
            rows.append(
                {
                    "url": url,
                    "page": current.label or previous.label or url,
                    "field": field,
                    "previous_value": previous_value,
                    "current_value": current_value,
                    "status": status,
                }
            )

    new_pages = sorted(current_urls - previous_urls)
    missing_pages = sorted(previous_urls - current_urls)
    return rows, new_pages, missing_pages


def markdown_table(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Page | Field | Previous Value | Current Value | Status |",
        "|------|-------|----------------|---------------|--------|",
    ]
    for row in rows:
        lines.append(
            "| {page} | {field} | {previous} | {current} | {status} |".format(
                page=truncate(row["page"], 70).replace("|", "\\|"),
                field=row["field"].replace("_", " ").title(),
                previous=truncate(row["previous_value"], 120).replace("|", "\\|"),
                current=truncate(row["current_value"], 120).replace("|", "\\|"),
                status=row["status"],
            )
        )
    return lines


def summarize_rows(rows: list[dict[str, Any]], status: str) -> list[dict[str, Any]]:
    return [row for row in rows if row["status"] == status]


def generate_context_brief(
    *,
    run_id: str,
    run_date: str,
    current_snapshot: Path,
    previous_snapshot: Path | None,
    rows: list[dict[str, Any]],
    new_pages: list[str],
    missing_pages: list[str],
) -> str:
    implemented = summarize_rows(rows, "IMPLEMENTED")
    unchanged = summarize_rows(rows, "UNCHANGED")
    changed = summarize_rows(rows, "CHANGED")

    previous_label = rel(previous_snapshot) if previous_snapshot else "None - first run or previous snapshot missing"
    lines: list[str] = [
        f"# Context Brief — {run_id} | {run_date}",
        "",
        "## Previous Run Used for Comparison",
        previous_label,
        "",
        "## Summary of Detected Metadata Changes",
        f"Current snapshot: {rel(current_snapshot)}",
        "",
    ]

    if not previous_snapshot:
        lines.extend(
            [
                "No previous metadata snapshot was available. This context brief establishes the baseline for future diffs.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                f"Compared {len(rows)} fields across {len(set(row['url'] for row in rows))} shared pages.",
                f"- Implemented/positive changes inferred: {len(implemented)}",
                f"- Other changed fields: {len(changed)}",
                f"- Unchanged fields: {len(unchanged)}",
                f"- New pages in current snapshot: {len(new_pages)}",
                f"- Pages missing from current snapshot: {len(missing_pages)}",
                "",
                "### Prefilled Comparison Table",
                "",
            ]
        )
        lines.extend(markdown_table(rows))
        lines.append("")

    lines.extend(["## Implemented Recommendations Inferred from Diff", ""])
    if implemented:
        for row in implemented:
            lines.append(
                f"- {row['page']} - {row['field'].replace('_', ' ')} changed from "
                f"`{truncate(row['previous_value'], 90)}` to `{truncate(row['current_value'], 90)}`."
            )
    else:
        lines.append("NONE CONFIRMED from metadata diff.")

    lines.extend(["", "## Unchanged Recommendations Inferred from Diff", ""])
    if unchanged:
        for row in unchanged[:30]:
            lines.append(f"- {row['page']} - {row['field'].replace('_', ' ')} unchanged: `{truncate(row['current_value'], 100)}`.")
        if len(unchanged) > 30:
            lines.append(f"- ... {len(unchanged) - 30} additional unchanged fields.")
    else:
        lines.append("No comparable unchanged fields were found.")

    lines.extend(["", "## Other Changed Fields", ""])
    if changed:
        for row in changed[:30]:
            lines.append(
                f"- {row['page']} - {row['field'].replace('_', ' ')} changed: "
                f"`{truncate(row['previous_value'], 90)}` -> `{truncate(row['current_value'], 90)}`."
            )
        if len(changed) > 30:
            lines.append(f"- ... {len(changed) - 30} additional changed fields.")
    else:
        lines.append("None.")

    lines.extend(["", "## New and Missing Pages", ""])
    if new_pages:
        lines.append("New in current snapshot:")
        for url in new_pages:
            lines.append(f"- {url}")
    else:
        lines.append("No new pages detected in current snapshot.")
    if missing_pages:
        lines.append("")
        lines.append("Missing from current snapshot:")
        for url in missing_pages:
            lines.append(f"- {url}")

    lines.extend(
        [
            "",
            "## Persistent Gaps Now Recurring for 2 or More Runs",
            "",
            "Use this automated diff as evidence. Fields marked UNCHANGED on pages that already carried gaps in the previous run should be treated as recurring unless Phase 2 scoring finds stronger current evidence.",
            "",
            "## Implications for Scoring and Prioritization in the Current Run",
            "",
            "1. Treat unchanged blocked fetch status, absent schema, weak titles, and weak meta descriptions as recurring implementation failures.",
            "2. Treat any IMPLEMENTED rows as candidate closed gaps, but verify the current page still passes the run criteria before lowering severity.",
            "3. Treat new pages as first-audit surfaces; score them normally and mark gaps as NEW unless prior evidence exists elsewhere.",
            "",
        ]
    )

    return "\n".join(lines)


def detect_previous_run_dir(run_id: str) -> Path | None:
    match = re.search(r"run_(\d+)", run_id)
    if not match:
        return None
    previous_number = int(match.group(1)) - 1
    if previous_number < 1:
        return None
    matches = sorted((ROOT / "runs").glob(f"run_{previous_number:03d}_*"))
    return matches[-1] if matches else None


def load_active_state() -> dict[str, Any] | None:
    if not STATE_FILE.exists():
        return None
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Diff metadata snapshots and create context_brief.md.")
    parser.add_argument("--current-run-dir", help="Current run directory. Defaults to active_run.json run_dir.")
    parser.add_argument("--previous-run-dir", help="Previous run directory. Defaults to run_NNN-1 if available.")
    parser.add_argument("--current-snapshot", help="Current metadata snapshot path.")
    parser.add_argument("--previous-snapshot", help="Previous metadata snapshot path.")
    parser.add_argument("--output", help="Output context brief path. Defaults to CURRENT_RUN_DIR/context_brief.md.")
    parser.add_argument("--run-id", help="Current run id.")
    parser.add_argument("--run-date", help="Current run date.")
    parser.add_argument("--summary-json", help="Optional path for machine-readable diff summary.")
    return parser


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    args = build_parser().parse_args(argv)
    state = load_active_state() or {}

    run_id = args.run_id or state.get("run_id") or "run_unknown"
    run_date = args.run_date or state.get("run_date") or datetime.now().strftime("%Y-%m-%d")

    current_run_dir = repo_path(args.current_run_dir or state.get("run_dir"))
    if current_run_dir is None:
        logging.error("--current-run-dir is required when active_run.json is absent.")
        return 2
    current_snapshot = repo_path(args.current_snapshot) or current_run_dir / "metadata_snapshot.md"
    if current_snapshot is None or not current_snapshot.exists():
        logging.error("Current snapshot not found: %s", current_snapshot)
        return 2

    previous_run_dir = repo_path(args.previous_run_dir or state.get("previous_run_dir"))
    if previous_run_dir is None:
        previous_run_dir = detect_previous_run_dir(run_id)
    previous_snapshot = repo_path(args.previous_snapshot) if args.previous_snapshot else None
    if previous_snapshot is None and previous_run_dir is not None:
        previous_snapshot = previous_run_dir / "metadata_snapshot.md"
    if previous_snapshot is not None and not previous_snapshot.exists():
        logging.warning("Previous snapshot not found: %s", previous_snapshot)
        previous_snapshot = None

    current_pages = parse_snapshot(current_snapshot)
    rows: list[dict[str, Any]] = []
    new_pages: list[str] = sorted(current_pages)
    missing_pages: list[str] = []
    if previous_snapshot:
        previous_pages = parse_snapshot(previous_snapshot)
        rows, new_pages, missing_pages = compare_snapshots(previous_pages, current_pages)

    output_path = repo_path(args.output) or current_run_dir / "context_brief.md"
    if output_path is None:
        logging.error("Could not determine output path.")
        return 2

    context = generate_context_brief(
        run_id=run_id,
        run_date=run_date,
        current_snapshot=current_snapshot,
        previous_snapshot=previous_snapshot,
        rows=rows,
        new_pages=new_pages,
        missing_pages=missing_pages,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(context, encoding="utf-8")
    logging.info("Wrote %s", rel(output_path))

    summary = {
        "row_count": len(rows),
        "implemented": summarize_rows(rows, "IMPLEMENTED"),
        "changed": summarize_rows(rows, "CHANGED"),
        "unchanged": summarize_rows(rows, "UNCHANGED"),
        "new_pages": new_pages,
        "missing_pages": missing_pages,
        "current_snapshot": rel(current_snapshot),
        "previous_snapshot": rel(previous_snapshot) if previous_snapshot else None,
        "output": rel(output_path),
    }
    if args.summary_json:
        summary_path = repo_path(args.summary_json)
        if summary_path is not None:
            summary_path.parent.mkdir(parents=True, exist_ok=True)
            summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
            logging.info("Wrote %s", rel(summary_path))

    logging.info(
        "Diff summary: %s implemented, %s changed, %s unchanged",
        len(summary["implemented"]),
        len(summary["changed"]),
        len(summary["unchanged"]),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
