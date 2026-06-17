#!/usr/bin/env python3
"""Local API server for the Radisson GEOptimizer research dashboard."""

from __future__ import annotations

import csv
import hashlib
import html
import io
import json
import mimetypes
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


DASHBOARD_ROOT = Path(__file__).resolve().parent
REPO_ROOT = DASHBOARD_ROOT.parent
RUNS_ROOT = REPO_ROOT / "runs"
STATE_FILE = RUNS_ROOT / "active_run.json"
RUN_INDEX = REPO_ROOT / "memory" / "run_index.md"
TARGET_URLS = REPO_ROOT / "sources" / "website" / "target_urls.md"
URL_REGISTRY_CSV = REPO_ROOT / "sources" / "website" / "radisson_url_registry.csv"
NEXT_GEO_RUN_CSV = REPO_ROOT / "sources" / "website" / "run_targets" / "next_geo_run.csv"
MAX_ACTIVE_TARGETS_FOR_RUN_SCOPE = 500

ARTIFACT_NAMES = [
    "metadata_snapshot.md",
    "context_brief.md",
    "gap_analysis.md",
    "gap_research.md",
    "optimization_proposal.md",
    "log_reflection.md",
    "run_state_completed.json",
]

PHASE_ORDER = [
    "PHASE_0_LITERATURE_REFRESH",
    "PHASE_1_CONTEXT_BRIEF",
    "PHASE_2_AUDIT_GAP_ANALYSIS",
    "PHASE_2_5_TARGETED_GAP_RESEARCH",
    "PHASE_3_OPTIMIZATION_PROPOSAL",
    "PHASE_4_LOG_AND_LEARN",
]

PHASE_LABELS = {
    "PHASE_0_LITERATURE_REFRESH": "Phase 0 - Literature Refresh",
    "PHASE_1_CONTEXT_BRIEF": "Phase 1 - Context Brief",
    "PHASE_2_AUDIT_GAP_ANALYSIS": "Phase 2 - Audit and Gap Analysis",
    "PHASE_2_5_TARGETED_GAP_RESEARCH": "Phase 2.5 - Targeted Gap Research",
    "PHASE_3_OPTIMIZATION_PROPOSAL": "Phase 3 - Optimization Proposal",
    "PHASE_4_LOG_AND_LEARN": "Phase 4 - Log and Learn",
}

URL_RE = re.compile(r"https?://[^\s)<>\]\"']+")
MODEL_PRICES_PER_MILLION = {
    "gpt-5.4-mini": {"input": 0.75, "output": 4.50},
    "gpt-5.4": {"input": 2.50, "output": 15.00},
    "gpt-5.5": {"input": 5.00, "output": 30.00},
    "gpt-5.3-codex": {"input": 1.75, "output": 14.00},
}
AUDIT_PROFILES = {
    "metadata_light": {
        "label": "Metadata light",
        "input_tokens_per_url": 1500,
        "output_tokens_per_url": 300,
        "description": "Metadata, sitemap fields, and focused GEO checks.",
    },
    "page_summary": {
        "label": "Page summary",
        "input_tokens_per_url": 3000,
        "output_tokens_per_url": 500,
        "description": "Rendered/page excerpt summary plus metadata check.",
    },
    "full_page_medium": {
        "label": "Full page medium",
        "input_tokens_per_url": 10000,
        "output_tokens_per_url": 750,
        "description": "Medium full-page text pass for deeper content auditing.",
    },
}


@dataclass
class CommandResult:
    exit_code: int
    stdout: str
    stderr: str


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def safe_repo_path(value: str) -> Path:
    candidate = (REPO_ROOT / value).resolve()
    root = REPO_ROOT.resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError("Path escapes repository root")
    return candidate


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def clean_inline(value: Any) -> str:
    value = str(value or "")
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip(" -\n\t")


def strip_md(value: str) -> str:
    value = re.sub(r"```[\s\S]*?```", "", value)
    value = re.sub(r"^#+\s*", "", value, flags=re.MULTILINE)
    value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    value = re.sub(r"`([^`]+)`", r"\1", value)
    return re.sub(r"\n{3,}", "\n\n", value).strip()


def stable_id(prefix: str, value: str) -> str:
    digest = hashlib.sha1(value.encode("utf-8", errors="replace")).hexdigest()[:12]
    return f"{prefix}_{digest}"


def canonicalize_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url.strip())
    path = parsed.path.rstrip("/") or "/"
    return urllib.parse.urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, "", ""))


def trim_url(url: str) -> str:
    return url.rstrip(".,;)]}\"'")


def urls_in(text: str) -> list[str]:
    seen: set[str] = set()
    values: list[str] = []
    for raw in URL_RE.findall(text or ""):
        url = trim_url(raw)
        if url not in seen:
            values.append(url)
            seen.add(url)
    return values


def field_value(text: str, label: str) -> str:
    patterns = [
        rf"^\s*[-*]?\s*\*\*{re.escape(label)}:\*\*\s*([^\n]+)",
        rf"^\s*\d+\.\s+\*\*{re.escape(label)}:\*\*\s*([^\n]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
        if match:
            return clean_inline(match.group(1))
    block = block_value(text, re.escape(label))
    if block:
        return clean_inline(block)
    return ""


def block_value(text: str, label_pattern: str) -> str:
    heading = rf"(?:\d+\.\s*)?{label_pattern}"
    boundary = rf"^\s*(?:[-*]\s*)?\*\*(?:\d+\.\s*)?[^*\n]+:?\*\*\s*$|^\s*(?:[-*]\s*)?\*\*[^*\n]+:\*\*|^###\s+|^##\s+|\Z"
    patterns = [
        rf"^\s*(?:[-*]\s*)?\*\*({heading}):\*\*\s*(.*?)(?={boundary})",
        rf"^\s*\d+\.\s+\*\*({label_pattern}):\*\*\s*(.*?)(?={boundary})",
        rf"^\s*(?:[-*]\s*)?\*\*({heading})\*\*\s*\n(.*?)(?={boundary})",
        rf"^\s*\d+\.\s+\*\*({label_pattern})\*\*\s*\n(.*?)(?={boundary})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
        if match:
            return match.group(2).strip()
    return ""


def split_heading_sections(text: str, heading_re: str) -> list[str]:
    chunks = re.split(rf"(?=^{heading_re})", text or "", flags=re.MULTILINE)
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def priority_tier_value(priority: str) -> int:
    match = re.search(r"P(\d)", priority or "", flags=re.IGNORECASE)
    if not match:
        return 3
    return max(1, 5 - int(match.group(1)))


def score_from_text(value: str) -> int:
    upper = (value or "").upper()
    if "VERY HIGH" in upper or "CRITICAL" in upper:
        return 5
    if "HIGH" in upper:
        return 4
    if "MEDIUM-HIGH" in upper:
        return 4
    if "MEDIUM" in upper:
        return 3
    if "LOW" in upper:
        return 2
    return 3


def count_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = row.get(key)
        if value in (None, ""):
            continue
        label = str(value)
        counts[label] = counts.get(label, 0) + 1
    return counts


def run_runner(*args: str) -> CommandResult:
    proc = subprocess.run(
        [sys.executable, "run.py", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        timeout=180,
    )
    return CommandResult(proc.returncode, proc.stdout, proc.stderr)


def parse_run_index() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    text = read_text(RUN_INDEX)
    pattern = re.compile(
        r"^(run_\d+)\s*\|\s*([^|]+)\|\s*(\d+)\s+gaps found\s*\|\s*(\d+)\s+implemented since last run\s*\|\s*key theme:\s*(.+)$"
    )
    for line in text.splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        run_id, date, gaps, implemented, theme = match.groups()
        rows.append(
            {
                "run_id": run_id,
                "runId": run_id,
                "date": date.strip(),
                "gapsFound": int(gaps),
                "implemented": int(implemented),
                "theme": theme.strip(),
                "run_dir": find_run_dir(run_id),
                "runDir": find_run_dir(run_id),
            }
        )
    return rows


def find_run_dir(run_id: str) -> str | None:
    matches = sorted(RUNS_ROOT.glob(f"{run_id}_*"))
    return rel(matches[-1]) if matches else None


def get_runs() -> list[dict[str, Any]]:
    indexed = parse_run_index()
    seen = {row["run_id"] for row in indexed}
    for path in sorted(RUNS_ROOT.glob("run_[0-9][0-9][0-9]_*")):
        run_id = "_".join(path.name.split("_")[:2])
        if run_id in seen:
            continue
        indexed.append(
            {
                "run_id": run_id,
                "runId": run_id,
                "date": path.name.replace(f"{run_id}_", ""),
                "gapsFound": None,
                "implemented": None,
                "theme": "Run folder present; not listed in run_index.md",
                "run_dir": rel(path),
                "runDir": rel(path),
            }
        )
    for row in indexed:
        run_dir = row.get("run_dir")
        row["artifacts"] = run_artifacts(run_dir)
        row["imported"] = bool(run_dir and (REPO_ROOT / run_dir / "dashboard_data.json").exists())
    return indexed


def run_artifacts(run_dir: str | None) -> list[dict[str, Any]]:
    if not run_dir:
        return []
    base = REPO_ROOT / run_dir
    return [
        {"name": name, "path": rel(base / name), "size": (base / name).stat().st_size}
        for name in ARTIFACT_NAMES
        if (base / name).exists()
    ]


def parse_target_urls() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    text = read_text(TARGET_URLS)
    targets: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []
    seen: dict[str, int] = {}
    priority = "Uncategorized"
    for line_number, line in enumerate(text.splitlines(), start=1):
        heading = re.match(r"^##\s+(.+)$", line.strip())
        if heading:
            priority = heading.group(1).strip()
        if re.match(r"^\s*-\s*$", line):
            issues.append({"type": "blank_target_url", "line": line_number, "message": "Blank target URL bullet"})
        for raw in URL_RE.findall(line):
            source_url = trim_url(raw)
            canonical = canonicalize_url(source_url)
            if canonical in seen:
                issues.append(
                    {
                        "type": "duplicate_target_url",
                        "line": line_number,
                        "firstLine": seen[canonical],
                        "url": canonical,
                    }
                )
                continue
            seen[canonical] = line_number
            targets.append(
                {
                    "source_url": source_url,
                    "canonical_url": canonical,
                    "registry_priority": priority,
                    "line_number": line_number,
                }
            )
    return targets, issues


def read_url_registry() -> list[dict[str, Any]]:
    if not URL_REGISTRY_CSV.exists():
        return []
    with URL_REGISTRY_CSV.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def read_url_registry_fieldnames() -> list[str]:
    if not URL_REGISTRY_CSV.exists():
        return []
    with URL_REGISTRY_CSV.open(encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        return next(reader, [])


def registry_field_value(row: dict[str, Any], field: str) -> str:
    return row.get(field) or "Unspecified"


def selected_url_key(row: dict[str, Any]) -> str:
    return row.get("normalized_url") or row.get("canonical_url") or row.get("url") or ""


def parse_nonnegative_int(value: str, default: int, maximum: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return max(0, min(parsed, maximum))


def has_active_registry_filter(filters: dict[str, str]) -> bool:
    exact_fields = ["brand", "region", "country", "locale", "page_type", "content_group", "location_confidence"]
    return bool(filters.get("query")) or any(filters.get(field, "all") != "all" for field in exact_fields)


def registry_filter_from_query(query: dict[str, list[str]]) -> dict[str, str]:
    return {
        "query": query.get("query", [""])[0].strip(),
        "brand": query.get("brand", ["all"])[0] or "all",
        "region": query.get("region", ["all"])[0] or "all",
        "country": query.get("country", ["all"])[0] or "all",
        "locale": query.get("locale", ["all"])[0] or "all",
        "page_type": query.get("page_type", ["all"])[0] or "all",
        "content_group": query.get("content_group", ["all"])[0] or "all",
        "location_confidence": query.get("location_confidence", ["all"])[0] or "all",
        "audit_profile": query.get("audit_profile", ["metadata_light"])[0] or "metadata_light",
        "model": query.get("model", ["gpt-5.4-mini"])[0] or "gpt-5.4-mini",
    }


def registry_filter_from_payload(payload: dict[str, Any]) -> dict[str, str]:
    values = payload.get("filters") if isinstance(payload.get("filters"), dict) else payload
    return {
        "query": str(values.get("query") or "").strip(),
        "brand": str(values.get("brand") or "all"),
        "region": str(values.get("region") or "all"),
        "country": str(values.get("country") or "all"),
        "locale": str(values.get("locale") or "all"),
        "page_type": str(values.get("page_type") or "all"),
        "content_group": str(values.get("content_group") or "all"),
        "location_confidence": str(values.get("location_confidence") or "all"),
        "audit_profile": str(values.get("audit_profile") or "metadata_light"),
        "model": str(values.get("model") or "gpt-5.4-mini"),
    }


def filter_registry_rows(rows: list[dict[str, Any]], filters: dict[str, str]) -> list[dict[str, Any]]:
    query = filters.get("query", "").lower()
    exact_fields = ["brand", "region", "country", "locale", "page_type", "content_group", "location_confidence"]
    filtered: list[dict[str, Any]] = []
    for row in rows:
        if any(filters.get(field, "all") != "all" and registry_field_value(row, field) != filters[field] for field in exact_fields):
            continue
        if query:
            haystack = " ".join(
                str(row.get(field, ""))
                for field in ["normalized_url", "brand", "country", "region", "locale", "page_type", "hotel_name", "content_group"]
            ).lower()
            if query not in haystack:
                continue
        filtered.append(row)
    return filtered


def registry_options(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    option_fields = ["brand", "region", "country", "locale", "page_type", "content_group", "location_confidence"]
    options: dict[str, list[dict[str, Any]]] = {}
    for field in option_fields:
        counts: dict[str, int] = {}
        for row in rows:
            value = registry_field_value(row, field)
            counts[value] = counts.get(value, 0) + 1
        options[field] = [
            {"value": value, "label": value, "count": count}
            for value, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        ]
    return options


def estimate_registry_cost(row_count: int, profile_id: str, model_id: str) -> dict[str, Any]:
    profile = AUDIT_PROFILES.get(profile_id) or AUDIT_PROFILES["metadata_light"]
    model = MODEL_PRICES_PER_MILLION.get(model_id) or MODEL_PRICES_PER_MILLION["gpt-5.4-mini"]
    input_tokens = row_count * int(profile["input_tokens_per_url"])
    output_tokens = row_count * int(profile["output_tokens_per_url"])
    input_cost = (input_tokens / 1_000_000) * model["input"]
    output_cost = (output_tokens / 1_000_000) * model["output"]
    return {
        "row_count": row_count,
        "profile_id": profile_id if profile_id in AUDIT_PROFILES else "metadata_light",
        "profile": profile,
        "model_id": model_id if model_id in MODEL_PRICES_PER_MILLION else "gpt-5.4-mini",
        "model_prices_per_million": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "input_cost_usd": round(input_cost, 2),
        "output_cost_usd": round(output_cost, 2),
        "total_cost_usd": round(input_cost + output_cost, 2),
        "batch_total_cost_usd_estimate": round((input_cost + output_cost) * 0.5, 2),
    }


def registry_payload(filters: dict[str, str], *, limit: int = 250, offset: int = 0) -> dict[str, Any]:
    rows = read_url_registry()
    filtered = filter_registry_rows(rows, filters)
    selected_rows = read_next_geo_run_rows()
    selected_urls = {selected_url_key(row) for row in selected_rows}
    for row in filtered:
        row["selected_for_next_run"] = "true" if row.get("normalized_url") in selected_urls else row.get("selected_for_next_run", "false")
    return {
        "registry_path": rel(URL_REGISTRY_CSV),
        "next_run_path": rel(NEXT_GEO_RUN_CSV),
        "total_records": len(rows),
        "filtered_count": len(filtered),
        "selected_count": len(selected_rows),
        "filters": filters,
        "options": registry_options(rows),
        "audit_profiles": AUDIT_PROFILES,
        "model_prices_per_million": MODEL_PRICES_PER_MILLION,
        "cost_estimate": estimate_registry_cost(len(filtered), filters.get("audit_profile", "metadata_light"), filters.get("model", "gpt-5.4-mini")),
        "rows": filtered[offset : offset + limit],
        "limit": limit,
        "offset": offset,
    }


def read_next_geo_run_rows() -> list[dict[str, Any]]:
    if not NEXT_GEO_RUN_CSV.exists():
        return []
    with NEXT_GEO_RUN_CSV.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def write_next_geo_run(rows: list[dict[str, Any]]) -> None:
    NEXT_GEO_RUN_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else read_url_registry_fieldnames() or [
        "url",
        "canonical_url",
        "normalized_url",
        "brand",
        "region",
        "locale",
        "page_type",
    ]
    with NEXT_GEO_RUN_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            updated = dict(row)
            updated["selected_for_next_run"] = "true"
            writer.writerow(updated)


def save_registry_selection(payload: dict[str, Any]) -> dict[str, Any]:
    rows = read_url_registry()
    filters = registry_filter_from_payload(payload)
    has_explicit_selection = "selected_urls" in payload
    explicit_urls = set(str(url) for url in payload.get("selected_urls", []) if url)
    if has_explicit_selection:
        selected = [
            row for row in rows
            if selected_url_key(row) in explicit_urls
        ]
    else:
        if not has_active_registry_filter(filters):
            raise ValueError("Refusing to save the entire registry as the next run. Choose filters or selected URLs first.")
        selected = filter_registry_rows(rows, filters)
        if len(selected) > MAX_ACTIVE_TARGETS_FOR_RUN_SCOPE and not payload.get("confirm_large_selection"):
            raise ValueError(
                f"Selection contains {len(selected)} URLs. Refusing to write more than "
                f"{MAX_ACTIVE_TARGETS_FOR_RUN_SCOPE} without confirm_large_selection=true."
            )
    write_next_geo_run(selected)
    return {
        "next_run_path": rel(NEXT_GEO_RUN_CSV),
        "selected_count": len(selected),
        "selection_mode": "explicit_urls" if has_explicit_selection else "filters",
        "filters": filters,
        "cost_estimate": estimate_registry_cost(len(selected), filters.get("audit_profile", "metadata_light"), filters.get("model", "gpt-5.4-mini")),
    }


def artifact_paths(run: dict[str, Any]) -> dict[str, Path]:
    run_dir = REPO_ROOT / str(run.get("run_dir") or run.get("runDir") or "")
    run_id = run.get("run_id") or run.get("runId")
    return {
        "metadata_snapshot": run_dir / "metadata_snapshot.md",
        "context_brief": run_dir / "context_brief.md",
        "gap_analysis": run_dir / "gap_analysis.md",
        "gap_research": run_dir / "gap_research.md",
        "optimization_proposal": run_dir / "optimization_proposal.md",
        "log_reflection": run_dir / "log_reflection.md",
        "literature_sources": REPO_ROOT / "literature" / f"{run_id}_sources.md",
        "criteria_framework": REPO_ROOT / "framework" / f"{run_id}_criteria.md",
    }


def parse_metadata_snapshot(text: str) -> dict[str, dict[str, Any]]:
    pages: dict[str, dict[str, Any]] = {}
    for section in split_heading_sections(text, r"##\s+Page\s+\d+(?:\s*\([^)]*\))?:"):
        url = field_value(section, "URL")
        if not url:
            heading_url = urls_in(section.splitlines()[0] if section.splitlines() else "")
            url = heading_url[0] if heading_url else ""
        if not url:
            continue
        canonical = canonicalize_url(url)
        pages[canonical] = {
            "url": canonical,
            "source_url": field_value(section, "Source URL") or url,
            "priority": field_value(section, "Priority"),
            "fetch_status": field_value(section, "Fetch status"),
            "fetch_method": field_value(section, "Fetch method"),
            "fetch_timestamp": field_value(section, "Fetch timestamp"),
            "title": field_value(section, "Extracted title"),
            "meta_description": field_value(section, "Extracted meta description")
            or field_value(section, "Extracted meta/brand copy"),
            "schema_types": field_value(section, "JSON-LD Schema Types"),
            "priority_schema_matches": field_value(section, "Priority Schema Matches"),
            "structured_data": block_value(section, "Structured data blocks"),
            "open_graph": block_value(section, "Open Graph tags"),
            "headings": block_value(section, "Heading outline"),
            "faq": field_value(section, "FAQ / Q&A presence"),
            "alt_text": block_value(section, "Alt text observations"),
            "query_notes": block_value(section, "Query compatibility notes") or field_value(section, "Query compatibility notes"),
            "entity_notes": block_value(section, "Entity signal notes") or field_value(section, "Entity signal notes"),
            "raw_excerpt": section[:6000],
        }
    return pages


def metadata_pages_audited_count(snapshot_text: str, metadata_pages: dict[str, dict[str, Any]]) -> int:
    value = field_value(snapshot_text, "Pages audited")
    if value:
        numeric = re.match(r"\s*(\d+)\s*$", value)
        if numeric:
            return int(numeric.group(1))
    return len(metadata_pages)


def recommendation_page_refs(recommendations: list[dict[str, Any]]) -> set[str]:
    refs: set[str] = set()
    for rec in recommendations:
        for ref in rec.get("page_refs", []) or []:
            if isinstance(ref, str) and ref.startswith("http"):
                refs.add(canonicalize_url(ref))
    return refs


def scoped_run_targets(
    targets: list[dict[str, Any]],
    metadata_pages: dict[str, dict[str, Any]],
    recommendations: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    scope = {
        "active_target_count": len(targets),
        "metadata_page_count": len(metadata_pages),
        "scoped_from_large_active_target_file": False,
    }
    if len(targets) <= MAX_ACTIVE_TARGETS_FOR_RUN_SCOPE or not metadata_pages:
        scope["dashboard_target_count"] = len(targets)
        return targets, scope

    wanted = set(metadata_pages) | recommendation_page_refs(recommendations)
    scoped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for target in targets:
        canonical = target.get("canonical_url") or ""
        if canonical in wanted and canonical not in seen:
            scoped.append(target)
            seen.add(canonical)
    for canonical, snapshot in metadata_pages.items():
        if canonical in seen:
            continue
        scoped.append(
            {
                "source_url": snapshot.get("source_url") or canonical,
                "canonical_url": canonical,
                "registry_priority": snapshot.get("priority") or "From metadata snapshot",
                "line_number": None,
            }
        )
        seen.add(canonical)
    scope.update(
        {
            "dashboard_target_count": len(scoped),
            "scoped_from_large_active_target_file": True,
            "scope_note": (
                "Active target file looked like a full registry export; dashboard pages were scoped "
                "to metadata snapshot pages and proposal-linked URLs for this run."
            ),
        }
    )
    return scoped, scope


def parse_criteria(text: str) -> dict[str, dict[str, Any]]:
    criteria: dict[str, dict[str, Any]] = {}
    priority_map: dict[str, str] = {}
    for match in re.finditer(r"^\|\s*(C\d+)\s*\|[^|]*\|\s*(P\d)\s*\|", text, flags=re.MULTILINE):
        priority_map[match.group(1)] = match.group(2)
    for section in split_heading_sections(text, r"##\s+C\d+"):
        heading_line = section.splitlines()[0] if section.splitlines() else ""
        heading = re.match(r"^##\s+(C\d+)\s+[—-]\s+(.+)$", heading_line)
        if not heading:
            continue
        criterion_id = heading.group(1)
        criteria[criterion_id] = {
            "criterion_id": criterion_id,
            "title": clean_inline(heading.group(2)),
            "signal_name": field_value(section, "Signal name"),
            "why_it_matters": field_value(section, "Why it matters"),
            "passing_rule": field_value(section, "Passing"),
            "how_to_check": field_value(section, "How to check"),
            "bleisure_relevance": field_value(section, "Bleisure relevance"),
            "priority": priority_map.get(criterion_id, ""),
            "raw_excerpt": section[:5000],
        }
    return criteria


def parse_gaps(text: str) -> dict[str, dict[str, Any]]:
    gaps: dict[str, dict[str, Any]] = {}
    for section in split_heading_sections(text, r"###\s+GAP-\d+"):
        heading = re.match(r"^###\s+(GAP-\d+)", section)
        if not heading:
            continue
        gap_id = heading.group(1)
        criterion = field_value(section, "Criterion")
        criterion_id_match = re.search(r"\b(C\d+)\b", criterion)
        page_url = field_value(section, "Page URL")
        gaps[gap_id] = {
            "gap_id": gap_id,
            "page_url": page_url,
            "canonical_page_url": canonicalize_url(page_url) if page_url.startswith("http") else page_url,
            "criterion": criterion,
            "criterion_id": criterion_id_match.group(1) if criterion_id_match else "",
            "current_state": field_value(section, "Current state") or field_value(section, "Current metadata state"),
            "gap_type": field_value(section, "Gap type"),
            "description": field_value(section, "Gap description"),
            "severity": int(re.search(r"\d+", field_value(section, "Severity") or "0").group(0))
            if re.search(r"\d+", field_value(section, "Severity") or "")
            else None,
            "recurrence_status": field_value(section, "Status"),
            "raw_excerpt": section[:6000],
        }
    return gaps


def parse_gap_research(text: str) -> dict[str, dict[str, Any]]:
    research: dict[str, dict[str, Any]] = {}
    for section in split_heading_sections(text, r"###\s+GAP-\d+"):
        heading_line = section.splitlines()[0] if section.splitlines() else ""
        heading = re.match(r"^###\s+(GAP-\d+)\s*\|\s*(.+)$", heading_line)
        if not heading:
            continue
        gap_id = heading.group(1)
        fix = (
            block_value(section, "Specific proposed fix(?:\\s+[—-][^:]*)?")
            or block_value(section, "Best practice and proposed fix")
        )
        research[gap_id] = {
            "gap_id": gap_id,
            "title": clean_inline(heading.group(2)),
            "best_practice": block_value(section, "Best practice for closing it"),
            "competitor_example": block_value(section, "Competitor or OTA example doing this well"),
            "specific_fix": fix,
            "directional_impact": block_value(section, "Directional impact(?: for bleisure traveler discovery)?"),
            "code_blocks": re.findall(r"```([a-zA-Z0-9_-]*)\n([\s\S]*?)```", section),
            "tables": re.findall(r"((?:^\|.+\|\n?)+)", section, flags=re.MULTILINE),
            "urls": urls_in(section),
            "raw_excerpt": section[:9000],
        }
    return research


def parse_literature_sources(text: str) -> dict[str, dict[str, Any]]:
    sources: dict[str, dict[str, Any]] = {}
    for section in split_heading_sections(text, r"##\s+FINDING\s+\d+"):
        heading = section.splitlines()[0].replace("##", "").strip() if section.splitlines() else "Literature finding"
        excerpt = strip_md(section)
        headline = excerpt.splitlines()[0] if excerpt else heading
        for url in urls_in(section):
            source_id = stable_id("src", url)
            sources[source_id] = {
                "source_id": source_id,
                "title_or_url": url,
                "url": url,
                "finding_group": heading,
                "headline": headline,
                "full_excerpt": excerpt,
                "ai_assessment_prose": summarize_source_assessment(section),
                "scorecard": source_scorecard(section),
                "related_criteria": sorted(set(re.findall(r"\bC\d+\b", section))),
                "related_gaps": sorted(set(re.findall(r"\bGAP-\d+\b", section))),
                "related_recommendations": [],
            }
    return sources


def summarize_source_assessment(text: str) -> str:
    lines = [clean_inline(line) for line in text.splitlines() if clean_inline(line)]
    useful = [line for line in lines if not line.startswith(("http", "Source", "#", "- https"))]
    return " ".join(useful[:3])[:700]


def source_scorecard(text: str) -> dict[str, Any]:
    urls = urls_in(text)
    return {
        "source_count": len(urls),
        "has_urls": bool(urls),
        "mentions_schema": bool(re.search(r"schema|structured data|JSON-LD", text, flags=re.IGNORECASE)),
        "mentions_ai_engine": bool(re.search(r"ChatGPT|Perplexity|Gemini|Claude|AI Overview", text, flags=re.IGNORECASE)),
        "mentions_traveler": bool(re.search(r"traveler|bleisure|business|leisure|American", text, flags=re.IGNORECASE)),
    }


def parse_proposals(text: str) -> dict[str, dict[str, Any]]:
    proposals: dict[str, dict[str, Any]] = {}
    for section in split_heading_sections(text, r"###\s+PROP-\d+"):
        heading_line = section.splitlines()[0] if section.splitlines() else ""
        heading = re.match(r"^###\s+(PROP-\d+)\s+[—-]\s+(.+)$", heading_line)
        if not heading:
            continue
        proposal_id = heading.group(1)
        gap_ref = field_value(section, "Gap ref")
        gap_refs = sorted(set(re.findall(r"GAP-\d+", gap_ref)))
        proposals[proposal_id] = {
            "proposal_id": proposal_id,
            "title": clean_inline(heading.group(2)),
            "gap_ref": gap_ref,
            "gap_refs": gap_refs,
            "proposed_change": field_value(section, "Proposed change"),
            "source_citation": field_value(section, "Source citation"),
            "current_state": field_value(section, "Current state"),
            "inferred_implementation_status": field_value(section, "Inferred implementation status"),
            "directional_impact_estimate": field_value(section, "Directional impact estimate"),
            "priority_tier": field_value(section, "Priority tier"),
            "raw_excerpt": section[:9000],
            "urls": urls_in(section),
            "code_blocks": re.findall(r"```([a-zA-Z0-9_-]*)\n([\s\S]*?)```", section),
        }
    return proposals


def source_from_citation(text: str, recommendation_id: str) -> dict[str, dict[str, Any]]:
    sources: dict[str, dict[str, Any]] = {}
    citation = clean_inline(text)
    if not citation:
        return sources
    urls = urls_in(text)
    if urls:
        for url in urls:
            source_id = stable_id("src", url)
            sources[source_id] = {
                "source_id": source_id,
                "title_or_url": url,
                "url": url,
                "finding_group": f"Citation for {recommendation_id}",
                "headline": citation[:180],
                "full_excerpt": citation,
                "ai_assessment_prose": citation[:700],
                "scorecard": source_scorecard(citation),
                "related_criteria": sorted(set(re.findall(r"\bC\d+\b", citation))),
                "related_gaps": sorted(set(re.findall(r"\bGAP-\d+\b", citation))),
                "related_recommendations": [recommendation_id],
            }
    else:
        source_id = stable_id("src", f"{recommendation_id}:{citation}")
        sources[source_id] = {
            "source_id": source_id,
            "title_or_url": citation[:120],
            "url": "",
            "finding_group": f"Citation for {recommendation_id}",
            "headline": citation[:180],
            "full_excerpt": citation,
            "ai_assessment_prose": citation[:700],
            "scorecard": source_scorecard(citation),
            "related_criteria": sorted(set(re.findall(r"\bC\d+\b", citation))),
            "related_gaps": sorted(set(re.findall(r"\bGAP-\d+\b", citation))),
            "related_recommendations": [recommendation_id],
        }
    return sources


def infer_surface(text: str) -> str:
    lower = text.lower()
    if any(token in lower for token in ["cloudflare", "crawler", "robots.txt", "llms.txt", "chatgpt app", "perplexity", "gbp", "google business"]):
        return "Strategic / infrastructure"
    if any(token in lower for token in ["title", "meta", "schema", "json-ld", "structured data", "open graph", "memberprogram"]):
        return "Metadata / structured data"
    if any(token in lower for token in ["copy", "paragraph", "opening", "section", "faq", "page", "content"]):
        return "Front-end content"
    return "Audit recommendation"


def infer_section_label(text: str) -> str:
    lower = text.lower()
    for label, tokens in [
        ("Page title", ["title"]),
        ("Meta description", ["meta description", "meta"]),
        ("JSON-LD schema", ["json-ld", "schema", "structured data"]),
        ("Opening copy", ["opening", "first 80 words"]),
        ("FAQ section", ["faq"]),
        ("Crawler access", ["cloudflare", "crawler", "robots.txt"]),
        ("Destination content", ["destination"]),
        ("Rewards content", ["rewards", "loyalty"]),
    ]:
        if any(token in lower for token in tokens):
            return label
    return "Page section"


def build_before_after(proposal: dict[str, Any], gap_rows: list[dict[str, Any]]) -> dict[str, str]:
    text = proposal.get("proposed_change", "")
    replace_match = re.search(
        r"(?:Replace|from):\s*[\"“](.+?)[\"”]\s+(?:with|to):\s*[\"“](.+?)[\"”]",
        text,
        flags=re.IGNORECASE,
    )
    if replace_match:
        return {"before": replace_match.group(1), "after": replace_match.group(2)}
    from_to = re.search(r"from\s+[\"“](.+?)[\"”]\s+to\s+[\"“](.+?)[\"”]", text, flags=re.IGNORECASE)
    if from_to:
        return {"before": from_to.group(1), "after": from_to.group(2)}
    current = proposal.get("current_state") or (gap_rows[0].get("current_state") if gap_rows else "")
    return {"before": current, "after": text}


def extract_copy_blocks(proposal: dict[str, Any], research_rows: list[dict[str, Any]], page_urls: list[str]) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    target_page = page_urls[0] if page_urls else ""
    proposed = proposal.get("proposed_change", "")
    if proposed:
        blocks.append(
            {
                "copy_block_id": f"{proposal['proposal_id']}_summary",
                "proposal_id": proposal["proposal_id"],
                "target_page": target_page,
                "target_field_or_section": infer_section_label(proposed),
                "format_type": infer_copy_format(proposed),
                "original_text": proposal.get("current_state", ""),
                "adjusted_text": "",
                "copy_label": "Proposed change",
                "cms_profile_id": "generic",
                "export_value": proposed,
            }
        )
    for index, row in enumerate(research_rows, start=1):
        fix = row.get("specific_fix", "")
        if fix:
            blocks.append(
                {
                    "copy_block_id": f"{proposal['proposal_id']}_research_{index}",
                    "proposal_id": proposal["proposal_id"],
                    "target_page": target_page,
                    "target_field_or_section": infer_section_label(fix),
                    "format_type": infer_copy_format(fix),
                    "original_text": "",
                    "adjusted_text": "",
                    "copy_label": f"Research fix {row.get('gap_id', index)}",
                    "cms_profile_id": "generic",
                    "export_value": strip_md(fix),
                }
            )
        for code_index, (language, code) in enumerate(row.get("code_blocks", []), start=1):
            code = code.strip()
            if not code:
                continue
            blocks.append(
                {
                    "copy_block_id": f"{proposal['proposal_id']}_code_{index}_{code_index}",
                    "proposal_id": proposal["proposal_id"],
                    "target_page": target_page,
                    "target_field_or_section": infer_section_label(code),
                    "format_type": "JSON-LD / schema" if language.lower() == "json" or "@context" in code else "Plain text",
                    "original_text": "",
                    "adjusted_text": "",
                    "copy_label": f"{language.upper() or 'Code'} snippet",
                    "cms_profile_id": "generic",
                    "export_value": code,
                }
            )
    return blocks


def infer_copy_format(text: str) -> str:
    lower = text.lower()
    if "json-ld" in lower or "@context" in lower or "schema" in lower:
        return "JSON-LD / schema"
    if "title" in lower or "meta description" in lower or "og:" in lower:
        return "Metadata field text"
    if "cms" in lower:
        return "CMS-ready"
    return "Plain text"


def build_recommendations(
    proposals: dict[str, dict[str, Any]],
    gaps: dict[str, dict[str, Any]],
    research: dict[str, dict[str, Any]],
    criteria: dict[str, dict[str, Any]],
    sources: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]]]:
    recommendations: list[dict[str, Any]] = []
    copy_blocks: list[dict[str, Any]] = []
    additional_sources: dict[str, dict[str, Any]] = {}

    for proposal_id, proposal in proposals.items():
        gap_rows = [gaps[gap_id] for gap_id in proposal.get("gap_refs", []) if gap_id in gaps]
        research_rows = [research[gap_id] for gap_id in proposal.get("gap_refs", []) if gap_id in research]
        page_refs = sorted({row.get("canonical_page_url") or row.get("page_url") for row in gap_rows if row.get("page_url")})
        criterion_ids = sorted({row.get("criterion_id") for row in gap_rows if row.get("criterion_id")})
        evidence_sources = source_from_citation(proposal.get("source_citation", ""), proposal_id)
        additional_sources.update(evidence_sources)
        for row in research_rows:
            for url in row.get("urls", []):
                source_id = stable_id("src", url)
                evidence_sources[source_id] = {
                    "source_id": source_id,
                    "title_or_url": url,
                    "url": url,
                    "finding_group": f"Gap research {row.get('gap_id')}",
                    "headline": row.get("title", url),
                    "full_excerpt": strip_md(row.get("raw_excerpt", "")),
                    "ai_assessment_prose": summarize_source_assessment(row.get("raw_excerpt", "")),
                    "scorecard": source_scorecard(row.get("raw_excerpt", "")),
                    "related_criteria": criterion_ids,
                    "related_gaps": [row.get("gap_id")],
                    "related_recommendations": [proposal_id],
                }
                additional_sources[source_id] = evidence_sources[source_id]
        evidence_ids = sorted(evidence_sources.keys())
        for source_id in evidence_ids:
            if source_id in sources:
                sources[source_id].setdefault("related_recommendations", [])
                if proposal_id not in sources[source_id]["related_recommendations"]:
                    sources[source_id]["related_recommendations"].append(proposal_id)
        severity = max([int(row.get("severity") or 1) for row in gap_rows] or [1])
        priority_components = default_priority_components(proposal, gap_rows, research_rows, evidence_ids, criteria)
        combined = combined_score(priority_components)
        selector_status = "Warning: selector not inferred"
        selector = ""
        if infer_section_label(proposal.get("proposed_change", "")) in {"Page title", "Meta description", "JSON-LD schema"}:
            selector_status = "Metadata field target"
            selector = f"meta:{infer_section_label(proposal.get('proposed_change', '')).lower().replace(' ', '_')}"
        recommendation = {
            "proposal_id": proposal_id,
            "title": proposal.get("title", proposal_id),
            "gap_refs": proposal.get("gap_refs", []),
            "page_refs": page_refs or [row.get("page_url") for row in gap_rows if row.get("page_url")],
            "surface": infer_surface(" ".join([proposal.get("title", ""), proposal.get("proposed_change", "")])),
            "section_label": infer_section_label(" ".join([proposal.get("title", ""), proposal.get("proposed_change", "")])),
            "inferred_dom_selector": selector,
            "selector_status": selector_status,
            "current_state": proposal.get("current_state") or (gap_rows[0].get("current_state") if gap_rows else ""),
            "proposed_change": proposal.get("proposed_change", ""),
            "before_after": build_before_after(proposal, gap_rows),
            "source_citation": proposal.get("source_citation", ""),
            "evidence_source_ids": evidence_ids,
            "evidence_tier": "Implementation-ready" if len(evidence_ids) >= 2 else "Medium evidence" if len(evidence_ids) == 1 else "Validation error",
            "priority_tier": proposal.get("priority_tier", ""),
            "priority_components": priority_components,
            "combined_score": combined,
            "severity": severity,
            "impact_estimate": proposal.get("directional_impact_estimate", ""),
            "implementation_status": proposal.get("inferred_implementation_status", ""),
            "raw_excerpt": proposal.get("raw_excerpt", ""),
            "criterion_ids": criterion_ids,
            "diagram": {
                "nodes": [proposal_id, *proposal.get("gap_refs", []), *criterion_ids, *evidence_ids],
                "edges": build_recommendation_edges(proposal_id, proposal.get("gap_refs", []), criterion_ids, evidence_ids),
            },
        }
        recommendations.append(recommendation)
        copy_blocks.extend(extract_copy_blocks(proposal, research_rows, page_refs))
    return recommendations, copy_blocks, additional_sources


def default_priority_components(
    proposal: dict[str, Any],
    gap_rows: list[dict[str, Any]],
    research_rows: list[dict[str, Any]],
    evidence_ids: list[str],
    criteria: dict[str, dict[str, Any]],
) -> dict[str, int]:
    severity = max([int(row.get("severity") or 1) for row in gap_rows] or [1])
    impact_text = " ".join([proposal.get("directional_impact_estimate", ""), *(row.get("directional_impact", "") for row in research_rows)])
    impact = max(score_from_text(impact_text), min(5, severity + 2))
    criterion_priorities = [criteria.get(row.get("criterion_id", ""), {}).get("priority", "") for row in gap_rows]
    geo_relevance = max([priority_tier_value(item) for item in criterion_priorities if item] or [priority_tier_value(proposal.get("priority_tier", ""))])
    evidence = 5 if len(evidence_ids) >= 2 else 3 if len(evidence_ids) == 1 else 0
    lower = " ".join([proposal.get("title", ""), proposal.get("proposed_change", "")]).lower()
    if any(token in lower for token in ["title", "meta", "copy", "paragraph", "llms.txt"]):
        ease = 5
    elif any(token in lower for token in ["schema", "json-ld", "faqpage"]):
        ease = 3
    elif any(token in lower for token in ["chatgpt", "perplexity", "partnership", "pms", "crs"]):
        ease = 1
    else:
        ease = 3
    return {
        "business_impact": int(max(1, min(5, impact))),
        "geo_relevance": int(max(1, min(5, geo_relevance))),
        "evidence_strength": int(max(0, min(5, evidence))),
        "ease_of_implementation": int(max(1, min(5, ease))),
    }


def combined_score(components: dict[str, Any]) -> int:
    impact = int(components.get("business_impact") or 0)
    geo = int(components.get("geo_relevance") or 0)
    evidence = int(components.get("evidence_strength") or 0)
    ease = int(components.get("ease_of_implementation") or 0)
    return round(((impact * 0.35) + (geo * 0.30) + (evidence * 0.25) + (ease * 0.10)) * 20)


def build_recommendation_edges(proposal_id: str, gaps: list[str], criteria: list[str], sources: list[str]) -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    for gap in gaps:
        edges.append({"from": proposal_id, "to": gap, "label": "addresses"})
    for criterion in criteria:
        for gap in gaps or [proposal_id]:
            edges.append({"from": gap, "to": criterion, "label": "measured by"})
    for source in sources:
        edges.append({"from": source, "to": proposal_id, "label": "supports"})
    return edges


def build_pages(
    targets: list[dict[str, Any]],
    metadata_pages: dict[str, dict[str, Any]],
    recommendations: list[dict[str, Any]],
    run_dir: Path,
) -> list[dict[str, Any]]:
    page_map: dict[str, dict[str, Any]] = {}
    for target in targets:
        canonical = target["canonical_url"]
        page_map[canonical] = {
            "canonical_url": canonical,
            "source_url": target["source_url"],
            "registry_priority": target["registry_priority"],
            "page_label": page_label(canonical),
            "live_capture_refs": latest_capture_refs(run_dir, canonical),
            "metadata_snapshot": metadata_pages.get(canonical, {}),
            "recommendations": [],
            "diagram": {"nodes": [canonical], "edges": []},
        }
    for canonical, snapshot in metadata_pages.items():
        if canonical not in page_map:
            page_map[canonical] = {
                "canonical_url": canonical,
                "source_url": snapshot.get("source_url") or canonical,
                "registry_priority": snapshot.get("priority") or "From metadata snapshot",
                "page_label": page_label(canonical),
                "live_capture_refs": latest_capture_refs(run_dir, canonical),
                "metadata_snapshot": snapshot,
                "recommendations": [],
                "diagram": {"nodes": [canonical], "edges": []},
            }
    for recommendation in recommendations:
        for ref in recommendation.get("page_refs", []):
            canonical = canonicalize_url(ref) if str(ref).startswith("http") else ref
            if canonical in page_map:
                page_map[canonical]["recommendations"].append(recommendation["proposal_id"])
                page_map[canonical]["diagram"]["nodes"].append(recommendation["proposal_id"])
                page_map[canonical]["diagram"]["edges"].append(
                    {"from": canonical, "to": recommendation["proposal_id"], "label": "has recommendation"}
                )
    return list(page_map.values())


def page_label(url: str) -> str:
    path = urllib.parse.urlsplit(url).path.strip("/")
    if not path or path == "en-us":
        return "Homepage"
    last = path.split("/")[-1].replace("-", " ")
    return last.title()


def latest_capture_refs(run_dir: Path, canonical_url: str) -> dict[str, Any]:
    capture_dir = run_dir / "browser_captures" / stable_id("page", canonical_url)
    result_path = capture_dir / "capture.json"
    if not result_path.exists():
        return {"status": "not_captured", "capture_dir": rel(capture_dir)}
    data = read_json(result_path) or {}
    screenshot = data.get("screenshot_path")
    if screenshot:
        data["screenshot_url"] = f"/api/capture-file?path={urllib.parse.quote(screenshot)}"
    return data


def build_metadata_changes(recommendations: list[dict[str, Any]], pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    page_by_url = {page["canonical_url"]: page for page in pages}
    rows: list[dict[str, Any]] = []
    for rec in recommendations:
        text = " ".join([rec.get("title", ""), rec.get("proposed_change", ""), rec.get("section_label", "")]).lower()
        if not any(token in text for token in ["title", "meta", "schema", "json-ld", "structured data", "llms.txt", "robots.txt"]):
            continue
        field_name = rec.get("section_label") or "Metadata / structured field"
        for page_ref in rec.get("page_refs", []) or [""]:
            canonical = canonicalize_url(page_ref) if str(page_ref).startswith("http") else page_ref
            snapshot = page_by_url.get(canonical, {}).get("metadata_snapshot", {})
            if field_name == "Page title":
                current = snapshot.get("title") or rec.get("before_after", {}).get("before") or rec.get("current_state", "")
            elif field_name == "Meta description":
                current = snapshot.get("meta_description") or rec.get("before_after", {}).get("before") or rec.get("current_state", "")
            else:
                current = rec.get("before_after", {}).get("before") or rec.get("current_state", "")
            rows.append(
                {
                    "metadata_change_id": f"{rec['proposal_id']}_{stable_id('field', canonical + field_name)}",
                    "proposal_id": rec["proposal_id"],
                    "page": canonical,
                    "field_name": field_name,
                    "current_value": current,
                    "live_value": page_by_url.get(canonical, {}).get("live_capture_refs", {}).get("metadata", {}).get("title", "")
                    if field_name == "Page title"
                    else "",
                    "proposed_value": rec.get("before_after", {}).get("after") or rec.get("proposed_change", ""),
                    "warning": metadata_warning(snapshot, page_by_url.get(canonical, {}).get("live_capture_refs", {}), field_name),
                    "evidence_source_ids": rec.get("evidence_source_ids", []),
                }
            )
    return rows


def metadata_warning(snapshot: dict[str, Any], capture: dict[str, Any], field_name: str) -> str:
    metadata = capture.get("metadata") or {}
    if not metadata:
        return ""
    if field_name == "Page title" and snapshot.get("title") and metadata.get("title") and snapshot["title"] != metadata["title"]:
        return "Live title differs from imported audit metadata"
    if field_name == "Meta description" and snapshot.get("meta_description") and metadata.get("description"):
        if snapshot["meta_description"] != metadata["description"]:
            return "Live meta description differs from imported audit metadata"
    return ""


def validate_dashboard(data: dict[str, Any], target_issues: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = list(target_issues)
    for rec in data.get("recommendations", []):
        if not rec.get("evidence_source_ids"):
            errors.append(
                {
                    "type": "missing_source_evidence",
                    "proposal_id": rec.get("proposal_id"),
                    "message": "Actionable recommendation has no source evidence",
                }
            )
        if not rec.get("page_refs"):
            warnings.append({"type": "missing_page_ref", "proposal_id": rec.get("proposal_id")})
        if rec.get("selector_status", "").startswith("Warning"):
            warnings.append({"type": "unvalidated_selector", "proposal_id": rec.get("proposal_id")})
    rec_ids_with_copy = {block.get("proposal_id") for block in data.get("copy_blocks", [])}
    for rec in data.get("recommendations", []):
        if rec.get("proposal_id") not in rec_ids_with_copy:
            warnings.append({"type": "missing_copy_block", "proposal_id": rec.get("proposal_id")})
    return {
        "status": "failed" if errors else "passed",
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }


def build_dashboard_data(run_id: str, record_history: bool = True) -> dict[str, Any]:
    run = next((row for row in get_runs() if row["run_id"] == run_id), None)
    if not run:
        raise ValueError(f"Run not found: {run_id}")
    if not run.get("run_dir"):
        raise ValueError(f"Run directory not found for {run_id}")

    paths = artifact_paths(run)
    targets, target_issues = parse_target_urls()
    metadata_snapshot_text = read_text(paths["metadata_snapshot"])
    metadata_pages = parse_metadata_snapshot(metadata_snapshot_text)
    criteria = parse_criteria(read_text(paths["criteria_framework"]))
    gaps = parse_gaps(read_text(paths["gap_analysis"]))
    research = parse_gap_research(read_text(paths["gap_research"]))
    proposals = parse_proposals(read_text(paths["optimization_proposal"]))
    sources = parse_literature_sources(read_text(paths["literature_sources"]))
    recommendations, copy_blocks, additional_sources = build_recommendations(proposals, gaps, research, criteria, sources)
    sources.update(additional_sources)
    run_dir = REPO_ROOT / str(run["run_dir"])
    scoped_targets, run_scope = scoped_run_targets(targets, metadata_pages, recommendations)
    pages = build_pages(scoped_targets, metadata_pages, recommendations, run_dir)
    pages_audited = metadata_pages_audited_count(metadata_snapshot_text, metadata_pages)
    run_scope["pages_audited"] = pages_audited
    metadata_changes = build_metadata_changes(recommendations, pages)
    data = {
        "schema_version": "geo_dashboard.v1",
        "run": {
            "run_id": run_id,
            "date": run.get("date"),
            "run_dir": run.get("run_dir"),
            "previous_run_id": previous_run_id(run_id),
            "imported_at": datetime.now().isoformat(timespec="seconds"),
            "source_files": {key: rel(path) for key, path in paths.items()},
            "scope": run_scope,
            "validation_errors": [],
        },
        "radisson_pages": pages,
        "sources": sorted(sources.values(), key=lambda item: (item.get("finding_group") or "", item.get("title_or_url") or "")),
        "criteria": sorted(criteria.values(), key=lambda item: item["criterion_id"]),
        "gaps": sorted(gaps.values(), key=lambda item: item["gap_id"]),
        "recommendations": sorted(recommendations, key=lambda item: item.get("combined_score", 0), reverse=True),
        "copy_blocks": copy_blocks,
        "metadata_changes": metadata_changes,
        "source_diagrams": build_source_diagrams(sources, recommendations, pages),
        "cms_profiles": [
            {
                "cms_profile_id": "generic",
                "name": "Generic CMS",
                "field_labels": {},
                "note": "Radisson CMS field labels are not known yet; add templates here later.",
            }
        ],
        "summary": {
            "pages": pages_audited or len(pages),
            "sources": len(sources),
            "criteria": len(criteria),
            "gaps": len(gaps),
            "recommendations": len(recommendations),
            "copy_blocks": len(copy_blocks),
            "metadata_changes": len(metadata_changes),
            "implementation_ready": sum(1 for rec in recommendations if len(rec.get("evidence_source_ids", [])) >= 2),
            "selector_warnings": sum(1 for rec in recommendations if rec.get("selector_status", "").startswith("Warning")),
        },
    }
    attach_jira_ticket_fields(run_id, data)
    validation = validate_dashboard(data, target_issues)
    data["run"]["validation_errors"] = validation["errors"]
    write_json(run_dir / "dashboard_data.json", data)
    write_json(run_dir / "dashboard_validation.json", validation)
    if record_history:
        record_import_history(run_dir, run_id, data, validation, paths)
    overrides_path = run_dir / "dashboard_overrides.json"
    if not overrides_path.exists():
        write_json(overrides_path, {"run_id": run_id, "overrides": {}, "updated_at": None})
    return apply_overrides(data, read_json(overrides_path) or {})


def record_import_history(
    run_dir: Path,
    run_id: str,
    data: dict[str, Any],
    validation: dict[str, Any],
    paths: dict[str, Path],
) -> None:
    imported_at = data.get("run", {}).get("imported_at") or datetime.now().isoformat(timespec="seconds")
    import_id = f"{run_id}_{datetime.now().strftime('%Y%m%dT%H%M%S%f')}"
    import_dir = run_dir / "dashboard_imports" / import_id
    import_dir.mkdir(parents=True, exist_ok=True)
    data_snapshot = import_dir / "dashboard_data.json"
    validation_snapshot = import_dir / "dashboard_validation.json"
    write_json(data_snapshot, data)
    write_json(validation_snapshot, validation)

    history_path = run_dir / "dashboard_import_history.json"
    history = read_json(history_path) or {"run_id": run_id, "imports": []}
    history.setdefault("imports", [])
    history["imports"].append(
        {
            "import_id": import_id,
            "run_id": run_id,
            "imported_at": imported_at,
            "dashboard_data": rel(data_snapshot),
            "dashboard_validation": rel(validation_snapshot),
            "source_file_mtimes": {
                key: path.stat().st_mtime
                for key, path in paths.items()
                if path.exists()
            },
            "summary": data.get("summary", {}),
            "validation_status": validation.get("status"),
            "validation_errors": validation.get("error_count", 0),
            "validation_warnings": validation.get("warning_count", 0),
        }
    )
    history["updated_at"] = datetime.now().isoformat(timespec="seconds")
    write_json(history_path, history)


def previous_run_id(run_id: str) -> str | None:
    match = re.search(r"run_(\d+)", run_id)
    if not match:
        return None
    number = int(match.group(1))
    return f"run_{number - 1:03d}" if number > 1 else None


def build_source_diagrams(
    sources: dict[str, dict[str, Any]],
    recommendations: list[dict[str, Any]],
    pages: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "source_graph": {
            "nodes": [*sources.keys(), *(rec["proposal_id"] for rec in recommendations)],
            "edges": [
                {"from": source_id, "to": rec["proposal_id"], "label": "supports"}
                for rec in recommendations
                for source_id in rec.get("evidence_source_ids", [])
            ],
        },
        "page_maps": {
            page["canonical_url"]: page.get("diagram", {"nodes": [], "edges": []})
            for page in pages
        },
        "recommendation_chains": {
            rec["proposal_id"]: rec.get("diagram", {"nodes": [], "edges": []})
            for rec in recommendations
        },
    }


def get_dashboard_data(run_id: str) -> dict[str, Any]:
    run = next((row for row in get_runs() if row["run_id"] == run_id), None)
    if not run or not run.get("run_dir"):
        raise ValueError(f"Run not found: {run_id}")
    run_dir = REPO_ROOT / str(run["run_dir"])
    data_path = run_dir / "dashboard_data.json"
    if not data_path.exists() or source_newer_than_dashboard(run, data_path):
        return build_dashboard_data(run_id)
    data = read_json(data_path) or build_dashboard_data(run_id)
    overrides = read_json(run_dir / "dashboard_overrides.json") or {}
    return apply_overrides(data, overrides)


def source_newer_than_dashboard(run: dict[str, Any], data_path: Path) -> bool:
    paths = artifact_paths(run)
    data_mtime = data_path.stat().st_mtime
    for path in paths.values():
        if path.exists() and path.stat().st_mtime > data_mtime:
            return True
    return False


def apply_overrides(data: dict[str, Any], overrides_payload: dict[str, Any]) -> dict[str, Any]:
    overrides = overrides_payload.get("overrides", {})
    if not overrides:
        data["team_overrides"] = {}
        attach_jira_ticket_fields(data.get("run", {}).get("run_id", "run"), data)
        return data
    data = json.loads(json.dumps(data))
    data["team_overrides"] = overrides
    for rec in data.get("recommendations", []):
        override = overrides.get(rec["proposal_id"], {})
        if not override:
            continue
        rec["team_override"] = override
        if override.get("adjusted_priority_components"):
            rec["priority_components_adjusted"] = override["adjusted_priority_components"]
            rec["combined_score"] = combined_score(override["adjusted_priority_components"])
        if override.get("selector_override"):
            rec["inferred_dom_selector"] = override["selector_override"]
            rec["selector_status"] = "Team override selector"
    for block in data.get("copy_blocks", []):
        override = overrides.get(block.get("proposal_id"), {})
        adjusted_copy = override.get("adjusted_copy", {}).get(block["copy_block_id"]) if override else None
        if adjusted_copy:
            block["adjusted_text"] = adjusted_copy
            block["export_value"] = adjusted_copy
    data["recommendations"] = sorted(data.get("recommendations", []), key=lambda item: item.get("combined_score", 0), reverse=True)
    attach_jira_ticket_fields(data.get("run", {}).get("run_id", "run"), data)
    return data


def update_overrides(run_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    run = next((row for row in get_runs() if row["run_id"] == run_id), None)
    if not run or not run.get("run_dir"):
        raise ValueError(f"Run not found: {run_id}")
    path = REPO_ROOT / str(run["run_dir"]) / "dashboard_overrides.json"
    current = read_json(path) or {"run_id": run_id, "overrides": {}}
    current.setdefault("overrides", {})
    proposal_id = payload.get("proposal_id")
    if not proposal_id:
        raise ValueError("proposal_id is required")
    existing = current["overrides"].get(proposal_id, {})
    merged = {**existing, **payload.get("override", {})}
    merged["timestamp"] = datetime.now().isoformat(timespec="seconds")
    current["overrides"][proposal_id] = merged
    current["updated_at"] = merged["timestamp"]
    write_json(path, current)
    return current


def capture_run(run_id: str, url: str | None = None) -> dict[str, Any]:
    data = get_dashboard_data(run_id)
    run_dir = REPO_ROOT / data["run"]["run_dir"]
    pages = data.get("radisson_pages", [])
    selected = [page for page in pages if not url or page["canonical_url"] == canonicalize_url(url)]
    if url and not selected:
        selected = [{"canonical_url": canonicalize_url(url), "source_url": url, "page_label": page_label(url)}]
    results = [capture_page(run_dir, page["source_url"] or page["canonical_url"]) for page in selected]
    # Rebuild metadata refs after capture.
    refreshed = build_dashboard_data(run_id, record_history=False)
    return {"captured": results, "data": refreshed}


def capture_page(run_dir: Path, url: str) -> dict[str, Any]:
    canonical = canonicalize_url(url)
    capture_dir = run_dir / "browser_captures" / stable_id("page", canonical)
    capture_dir.mkdir(parents=True, exist_ok=True)
    script = DASHBOARD_ROOT / "capture.mjs"
    if script.exists():
        try:
            proc = subprocess.run(
                ["node", str(script), url, str(capture_dir)],
                cwd=DASHBOARD_ROOT,
                text=True,
                capture_output=True,
                timeout=45,
            )
            if proc.returncode == 0 and proc.stdout.strip():
                result = json.loads(proc.stdout)
                result["capture_method"] = "playwright"
                result["url"] = canonical
                result["captured_at"] = datetime.now().isoformat(timespec="seconds")
                if result.get("screenshot_path"):
                    result["screenshot_path"] = rel(Path(result["screenshot_path"]))
                if result.get("dom_snapshot_path"):
                    result["dom_snapshot_path"] = rel(Path(result["dom_snapshot_path"]))
                write_json(capture_dir / "capture.json", result)
                return result
            fallback = fallback_http_capture(url, capture_dir)
            fallback["playwright_error"] = (proc.stderr or proc.stdout or "Playwright capture returned no data")[-1200:]
            return fallback
        except Exception as exc:
            fallback = fallback_http_capture(url, capture_dir)
            fallback["playwright_error"] = str(exc)
            return fallback
    return fallback_http_capture(url, capture_dir)


def fallback_http_capture(url: str, capture_dir: Path) -> dict[str, Any]:
    result = {
        "capture_method": "http_fallback",
        "status": "failed",
        "url": canonicalize_url(url),
        "source_url": url,
        "captured_at": datetime.now().isoformat(timespec="seconds"),
        "metadata": {},
        "selector_candidates": [],
        "sections": [],
        "warnings": ["Playwright capture unavailable; used HTTP metadata fallback"],
    }
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 GEOptimizerDashboard/1.0"})
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read(2_000_000).decode("utf-8", errors="replace")
            result["status"] = f"HTTP {response.getcode()}"
            title = re.search(r"<title[^>]*>(.*?)</title>", body, flags=re.IGNORECASE | re.DOTALL)
            desc = re.search(
                r"<meta[^>]+name=[\"']description[\"'][^>]+content=[\"']([^\"']+)[\"']",
                body,
                flags=re.IGNORECASE,
            )
            result["metadata"] = {
                "title": html.unescape(clean_inline(title.group(1))) if title else "",
                "description": html.unescape(clean_inline(desc.group(1))) if desc else "",
            }
    except Exception as exc:
        result["status"] = "blocked_or_unavailable"
        result["warnings"].append(str(exc))
    write_json(capture_dir / "capture.json", result)
    return result


JIRA_CSV_FIELDS = [
    "Issue Type",
    "Epic Name",
    "Summary",
    "Description",
    "Priority",
    "Labels",
    "Component",
    "Acceptance Criteria",
]


def export_jira_csv(run_id: str, data: dict[str, Any]) -> dict[str, Any]:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=JIRA_CSV_FIELDS, lineterminator="\n")
    writer.writeheader()

    epic_name = f"RHG GEO Optimizer Audit Actions - {run_id}"
    evaluation = geo_visibility_evaluation(data)

    blocks_by_proposal: dict[str, list[dict[str, Any]]] = {}
    for block in data.get("copy_blocks", []):
        blocks_by_proposal.setdefault(block.get("proposal_id"), []).append(block)

    for rec in data.get("recommendations", []):
        writer.writerow(jira_story_row(run_id, epic_name, rec, blocks_by_proposal.get(rec.get("proposal_id"), []), evaluation))

    return {"type": "csv", "content": output.getvalue()}


def jira_story_row(
    run_id: str,
    epic_name: str,
    rec: dict[str, Any],
    copy_blocks: list[dict[str, Any]],
    evaluation: dict[str, Any],
) -> dict[str, str]:
    draft = rec.get("team_override", {}).get("ticket_draft", {}) or {}
    proposal_type = infer_jira_proposal_type(rec, copy_blocks)
    target_urls = target_urls_for_rec(rec)
    target_component = infer_jira_target_component(rec)
    page_type = infer_jira_page_type(rec, target_urls)
    proposed_value = infer_jira_proposed_value(rec, copy_blocks)
    summary = jira_summary({"title": draft.get("summary") or rec.get("title") or rec.get("proposal_id")})
    target_url_text = ", ".join(target_urls) or ", ".join(rec.get("page_refs", []) or []) or "[NEEDED: target URL]"
    required_change = rec.get("proposed_change") or "[NEEDED: recommended change]"
    generated_developer_change_specs = [
        f"Change type: {proposal_type}",
        f"Page type: {page_type}",
        f"Target component: {target_component or '[NEEDED: target component]'}",
        f"Target URL(s): {target_url_text}",
        f"Current state: {rec.get('current_state') or '[NEEDED: current state]'}",
        f"Required change: {required_change}",
        f"Evidence tier: {rec.get('evidence_tier') or 'Not set'}",
        f"Evidence sources: {', '.join(rec.get('evidence_source_ids', [])) or 'None linked'}",
    ]
    if proposed_value and clean_inline(proposed_value) != clean_inline(required_change):
        generated_developer_change_specs.insert(6, f"Proposed value/state: {proposed_value}")
    developer_change_specs = draft.get("developer_change_spec") or generated_developer_change_specs
    validation_steps = draft.get("validation_steps") or build_jira_validation_steps(proposal_type, target_urls[0] if target_urls else "")
    acceptance_criteria = draft.get("acceptance_criteria") or build_jira_acceptance_criteria(proposal_type)
    seo_rationale = build_jira_seo_rationale(proposal_type)
    generated_description = " ".join(
        [
            jira_section_text("Dev change specs", developer_change_specs),
            jira_section_text("SEO/GEO rationale", [seo_rationale]),
            jira_section_text("Validation steps", validation_steps),
            jira_section_text(
                "GEO visibility score",
                [
                    f"Run score: {evaluation['rating']}/100",
                    f"Proposal score: {rec.get('combined_score', 'Not set')}",
                    f"Readiness status: {ticket_readiness_label(rec)}",
                ],
            ),
        ]
    )
    description = draft.get("description") or generated_description

    return {
        "Issue Type": "Story",
        "Epic Name": epic_name,
        "Summary": summary,
        "Description": description,
        "Priority": jira_priority(rec),
        "Labels": jira_labels(run_id, rec, proposal_type),
        "Component": jira_component(rec, proposal_type),
        "Acceptance Criteria": jira_bullet_inline(acceptance_criteria),
    }


def attach_jira_ticket_fields(run_id: str, data: dict[str, Any]) -> dict[str, Any]:
    blocks_by_proposal: dict[str, list[dict[str, Any]]] = {}
    for block in data.get("copy_blocks", []):
        blocks_by_proposal.setdefault(block.get("proposal_id"), []).append(block)

    epic_name = f"RHG GEO Optimizer Audit Actions - {run_id}"
    evaluation = geo_visibility_evaluation(data)
    required_fields = list(JIRA_CSV_FIELDS)
    recommendations = data.get("recommendations", [])
    for rec in recommendations:
        row = jira_story_row(run_id, epic_name, rec, blocks_by_proposal.get(rec.get("proposal_id"), []), evaluation)
        labels = [label for label in row["Labels"].split(";") if label]
        rec["jira_ticket"] = {
            "format": "jira_csv",
            "required_fields": required_fields,
            "issue_type": row["Issue Type"],
            "name": row["Summary"],
            "epic_name": row["Epic Name"],
            "summary": row["Summary"],
            "description": row["Description"],
            "priority": row["Priority"],
            "labels": labels,
            "component": row["Component"],
            "acceptance_criteria": row["Acceptance Criteria"],
            "csv_fields": row,
        }

    data.setdefault("jira_export", {})
    data["jira_export"].update(
        {
            "format": "jira_csv",
            "fields": required_fields,
            "epic_name": epic_name,
            "ticket_count": len(recommendations),
        }
    )
    data.setdefault("summary", {})["jira_tickets"] = len(recommendations)
    return data


def geo_visibility_evaluation(data: dict[str, Any]) -> dict[str, int]:
    recommendations = data.get("recommendations", [])
    summary = data.get("summary", {}) or {}
    warnings = int(summary.get("selector_warnings") or 0)
    errors = len(data.get("run", {}).get("validation_errors", []) or [])
    implementation_ready = int(summary.get("implementation_ready") or 0)
    ready_to_send = max(0, implementation_ready - warnings)
    average_score = (
        sum(float(rec.get("combined_score") or 0) for rec in recommendations) / len(recommendations)
        if recommendations
        else 0
    )
    crawl = geo_crawlability_metrics(data)
    uncapped_rating = average_score - warnings * 0.8 - errors * 4 - crawl["penalty"]
    rating = round(max(0, min(99, min(uncapped_rating, crawl["cap"]))))
    return {
        "rating": rating,
        "ready_to_send": ready_to_send,
        "needs_review": warnings,
        "blocked_pages": crawl["blocked_pages"],
    }


def geo_crawlability_metrics(data: dict[str, Any]) -> dict[str, int | bool]:
    page_statuses = []
    for page in data.get("radisson_pages", []) or []:
        metadata = page.get("metadata_snapshot", {}) or {}
        live_capture = page.get("live_capture_refs", {}) or {}
        status_text = " ".join(
            str(value or "")
            for value in [
                metadata.get("fetch_status"),
                metadata.get("raw_excerpt"),
                live_capture.get("status"),
                (live_capture.get("metadata", {}) or {}).get("title"),
                (live_capture.get("sections") or [{}])[0].get("text"),
            ]
        )
        checked = bool(metadata.get("fetch_status") or (live_capture.get("status") and live_capture.get("status") != "not_captured"))
        page_statuses.append(
            {
                "checked": checked,
                "blocked": checked and bool(re.search(r"\b403\b|blocked|access restricted|temporarily restricted", status_text, flags=re.IGNORECASE)),
            }
        )

    checked_pages = sum(1 for page in page_statuses if page["checked"])
    blocked_pages = sum(1 for page in page_statuses if page["blocked"])
    access_evidence = " ".join(
        [
            *(
                f"{rec.get('title', '')} {rec.get('current_state', '')} {rec.get('proposed_change', '')}"
                for rec in data.get("recommendations", []) or []
            ),
            *(
                f"{item.get('current_value', '')} {item.get('proposed_value', '')}"
                for item in data.get("metadata_changes", []) or []
            ),
            *(f"{item.get('original_text', '')}" for item in data.get("copy_blocks", []) or []),
        ]
    )
    robots_blocked = bool(
        re.search(
            r"robots\.txt.{0,160}(403|blocked|unreadable)|(403|blocked|unreadable).{0,160}robots\.txt",
            access_evidence,
            flags=re.IGNORECASE,
        )
    )
    sitewide_blocked = (checked_pages >= 3 and blocked_pages == checked_pages) or bool(
        re.search(r"all WebFetch attempts.{0,180}(403|blocked)|WAF.{0,120}Block AI", access_evidence, flags=re.IGNORECASE)
    )
    blocked_ratio = blocked_pages / checked_pages if checked_pages else 0
    page_penalty = 6 + round(blocked_ratio * 8) + min(blocked_pages, 4) if blocked_pages else 0
    penalty = min(18, page_penalty + (2 if robots_blocked else 0) + (2 if sitewide_blocked else 0))
    cap = 72 if sitewide_blocked else 84 if blocked_pages else 99
    return {
        "checked_pages": checked_pages,
        "blocked_pages": blocked_pages,
        "robots_blocked": robots_blocked,
        "sitewide_blocked": sitewide_blocked,
        "penalty": penalty,
        "cap": cap,
    }


def jira_summary(rec: dict[str, Any]) -> str:
    title = rec.get("title") or rec.get("proposal_id") or "GEO proposal"
    return re.sub(r"^GEO\s*-\s*", "", clean_inline(title), flags=re.IGNORECASE)


def target_urls_for_rec(rec: dict[str, Any]) -> list[str]:
    seen: set[str] = set()
    urls: list[str] = []
    for ref in rec.get("page_refs", []) or []:
        value = str(ref or "")
        if value.startswith("http") and value not in seen:
            urls.append(value)
            seen.add(value)
    return urls


def infer_jira_proposal_type(rec: dict[str, Any], copy_blocks: list[dict[str, Any]]) -> str:
    text = f"{rec.get('title', '')} {rec.get('proposed_change', '')} {rec.get('section_label', '')} {rec.get('surface', '')}".lower()
    block_text = " ".join(
        f"{block.get('target_field_or_section', '')} {block.get('format_type', '')} {block.get('copy_label', '')}".lower()
        for block in copy_blocks
    )
    if re.search(r"\b(json-ld|schema|structured data|memberprogram|faqpage)\b", block_text):
        return "schema_update"
    if re.search(r"\b(json-ld|schema|structured data|memberprogram|faqpage)\b", text):
        return "schema_update"
    if re.search(r"title|meta description|metadata|open graph|og:", text):
        return "metadata_update"
    if re.search(r"javascript|html|visible|crawler|bot|rendered|cloudflare|llms\.txt", text):
        return "html_visibility"
    return "content_visibility"


def infer_jira_target_component(rec: dict[str, Any]) -> str:
    section = rec.get("section_label")
    if section and section != "Page section":
        return section
    text = f"{rec.get('title', '')} {rec.get('proposed_change', '')}".lower()
    if "room" in text:
        return "Rooms"
    if "service" in text:
        return "Services"
    if "faq" in text:
        return "FAQ"
    if "title" in text:
        return "Page title"
    if "meta" in text:
        return "Metadata"
    if "cloudflare" in text:
        return "Cloudflare / crawler access"
    if "llms.txt" in text:
        return "llms.txt"
    return rec.get("surface") or "Page content"


def infer_jira_page_type(rec: dict[str, Any], target_urls: list[str]) -> str:
    joined = " ".join(target_urls or rec.get("page_refs", []) or []).lower()
    if "/brand/" in joined:
        return "brand_page"
    if "/rewards" in joined:
        return "rewards"
    if "/destination" in joined:
        return "destination"
    if "/rooms" in joined:
        return "rooms"
    if "/services" in joined:
        return "services"
    if "/offers" in joined:
        return "offers"
    if "/hotel" in joined:
        return "hotel_detail"
    return "portfolio_or_other"


def infer_jira_proposed_value(rec: dict[str, Any], copy_blocks: list[dict[str, Any]]) -> str:
    schema_block = next(
        (
            block
            for block in copy_blocks
            if re.search(r"json-ld|schema", f"{block.get('format_type', '')} {block.get('copy_label', '')}", flags=re.IGNORECASE)
        ),
        None,
    )
    if schema_block and schema_block.get("export_value"):
        return schema_block["export_value"]
    return rec.get("before_after", {}).get("after") or rec.get("proposed_change") or ""


def build_jira_seo_rationale(proposal_type: str) -> str:
    if proposal_type == "html_visibility":
        return "This change improves crawler and AI-engine access to content in delivered HTML without depending on client-side rendering."
    if proposal_type == "schema_update":
        return "This change improves structured data coverage and gives search and AI systems clearer machine-readable entity signals."
    if proposal_type == "metadata_update":
        return "This change improves machine-readable metadata quality for search surfaces and AI retrieval workflows."
    return "This change improves crawler and AI-engine access to visible page content and user-facing signals."


def build_jira_validation_steps(proposal_type: str, target_url: str) -> list[str]:
    url = target_url or "[NEEDED: target URL]"
    if proposal_type == "html_visibility":
        return [
            f"Open {url}.",
            "Disable JavaScript and reload the page.",
            "Inspect the delivered HTML or page source.",
            "Confirm the target content is present without a client-side dependency.",
            "Confirm no visible page regression when JavaScript is enabled.",
        ]
    if proposal_type == "schema_update":
        return [
            f"Open {url}.",
            "Inspect the rendered JSON-LD or structured data output.",
            "Confirm the required schema field or value is present.",
            "Validate that the updated schema still parses correctly.",
            "Confirm no visible page regression.",
        ]
    if proposal_type == "metadata_update":
        return [
            f"Open {url}.",
            "Inspect the page head metadata in the delivered HTML.",
            "Confirm the updated metadata field contains the expected value.",
            "Verify the value matches the ticket copy exactly.",
            "Confirm no visible page regression.",
        ]
    return [
        f"Open {url}.",
        "Inspect the target page output.",
        "Confirm the required content or value is present in the expected location.",
        "Verify the change matches the ticket description.",
        "Confirm no visible page regression.",
    ]


def build_jira_acceptance_criteria(proposal_type: str) -> list[str]:
    baseline = [
        "Required content or value is present in the delivered page output.",
        "Change applies to the listed target URL or page set.",
        "Existing visible behavior remains unchanged unless specified in the ticket.",
        "Evidence is attached before the ticket moves to validation.",
    ]
    if proposal_type == "html_visibility":
        return [
            "Target content is present in server-delivered HTML when JavaScript is disabled.",
            *baseline[1:],
        ]
    if proposal_type == "schema_update":
        return [
            "Updated structured data field or object is present in the rendered output.",
            *baseline[1:],
        ]
    return baseline


def jira_priority(rec: dict[str, Any]) -> str:
    priority = str(rec.get("priority_tier") or "").upper()
    if "P1" in priority:
        return "Highest"
    if "P2" in priority:
        return "High"
    if "P3" in priority:
        return "Medium"
    score = float(rec.get("combined_score") or 0)
    if score >= 90:
        return "Highest"
    if score >= 80:
        return "High"
    return "Medium"


def jira_component(rec: dict[str, Any], proposal_type: str) -> str:
    surface = str(rec.get("surface") or "").lower()
    if "strategic" in surface or proposal_type == "html_visibility":
        return "Platform"
    if proposal_type == "schema_update":
        return "SEO / Schema"
    if proposal_type == "metadata_update":
        return "SEO / Metadata"
    if "content" in surface:
        return "Content"
    return "SEO/GEO"


def ticket_readiness_label(rec: dict[str, Any]) -> str:
    if "warning" in str(rec.get("selector_status") or "").lower():
        return "Need review"
    if rec.get("evidence_tier") == "Implementation-ready":
        return "Ready to send"
    return rec.get("evidence_tier") or "Review"


def jira_labels(run_id: str, rec: dict[str, Any], proposal_type: str) -> str:
    labels = [
        "GEO",
        "GEO-Visibility",
        "Performance-Evaluation",
        run_id,
        str(rec.get("proposal_id") or "proposal"),
        proposal_type.replace("_", "-"),
    ]
    return ";".join(labels)


def jira_bullet_inline(items: Any) -> str:
    if isinstance(items, str):
        values = [clean_inline(line.lstrip("-").strip()) for line in items.splitlines() if line.strip()]
    else:
        values = [clean_inline(item) for item in (items or []) if clean_inline(item)]
    return " ".join(f"- {item}" for item in values)


def jira_section_text(title: str, items: Any) -> str:
    return f"{title}: {jira_bullet_inline(items)}".strip()


def bullet_text(items: Any) -> str:
    if isinstance(items, str):
        values = [line.strip().lstrip("-").strip() for line in items.splitlines() if line.strip()]
    else:
        values = [str(item).strip() for item in (items or []) if str(item).strip()]
    return "\n".join(f"- {item}" for item in values)


def export_dashboard(run_id: str, export_type: str) -> dict[str, Any]:
    data = get_dashboard_data(run_id)
    if export_type == "json":
        return {"type": "json", "content": json.dumps(data, indent=2, ensure_ascii=False)}
    if export_type == "jira_csv":
        return export_jira_csv(run_id, data)
    if export_type == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=[
                "run_id",
                "proposal_id",
                "score",
                "priority_tier",
                "surface",
                "page_refs",
                "selector",
                "selector_status",
                "evidence_tier",
                "source_ids",
                "proposed_change",
            ],
        )
        writer.writeheader()
        for rec in data.get("recommendations", []):
            writer.writerow(
                {
                    "run_id": run_id,
                    "proposal_id": rec["proposal_id"],
                    "score": rec["combined_score"],
                    "priority_tier": rec.get("priority_tier"),
                    "surface": rec.get("surface"),
                    "page_refs": "; ".join(rec.get("page_refs", [])),
                    "selector": rec.get("inferred_dom_selector"),
                    "selector_status": rec.get("selector_status"),
                    "evidence_tier": rec.get("evidence_tier"),
                    "source_ids": "; ".join(rec.get("evidence_source_ids", [])),
                    "proposed_change": rec.get("proposed_change"),
                }
            )
        return {"type": "csv", "content": output.getvalue()}
    include_original = export_type == "audit"
    lines: list[str] = [f"# Radisson GEOptimizer Handoff — {run_id}", ""]
    by_page: dict[str, list[dict[str, Any]]] = {}
    for rec in data.get("recommendations", []):
        for page in rec.get("page_refs", []) or ["Portfolio-wide"]:
            by_page.setdefault(page, []).append(rec)
    blocks_by_proposal: dict[str, list[dict[str, Any]]] = {}
    for block in data.get("copy_blocks", []):
        blocks_by_proposal.setdefault(block["proposal_id"], []).append(block)
    for page, recs in by_page.items():
        lines.extend([f"## {page}", ""])
        for rec in recs:
            lines.extend(
                [
                    f"### {rec['proposal_id']} — {rec['title']}",
                    f"- Score: {rec['combined_score']}",
                    f"- Surface: {rec['surface']}",
                    f"- Target: {rec.get('section_label')} | {rec.get('inferred_dom_selector') or rec.get('selector_status')}",
                    f"- Evidence: {rec.get('evidence_tier')} ({len(rec.get('evidence_source_ids', []))} sources)",
                    "",
                ]
            )
            for block in blocks_by_proposal.get(rec["proposal_id"], []):
                lines.append(f"**{block['copy_label']} ({block['format_type']})**")
                if include_original and block.get("original_text"):
                    lines.extend(["Original:", "```text", block["original_text"], "```"])
                lines.extend(["Copy:", "```text", block.get("export_value") or "", "```", ""])
    return {"type": export_type, "content": "\n".join(lines)}


def status_payload() -> dict[str, Any]:
    state = read_json(STATE_FILE)
    status_result = run_runner("--status")
    return {
        "hasActiveRun": state is not None,
        "activeRun": state,
        "phaseLabel": PHASE_LABELS.get(state.get("current_phase")) if state else None,
        "phaseOrder": PHASE_ORDER,
        "phaseLabels": PHASE_LABELS,
        "statusCommand": status_result.__dict__,
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "RadissonGeoDashboard/1.0"

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        try:
            if path == "/api/dashboard/runs":
                self.send_json({"runs": get_runs()})
            elif path == "/api/dashboard/data":
                run_id = query.get("run_id", [""])[0] or latest_run_id()
                self.send_json(get_dashboard_data(run_id))
            elif path == "/api/dashboard/validation":
                run_id = query.get("run_id", [""])[0] or latest_run_id()
                data = get_dashboard_data(run_id)
                run_dir = REPO_ROOT / data["run"]["run_dir"]
                self.send_json(read_json(run_dir / "dashboard_validation.json") or {})
            elif path == "/api/dashboard/export":
                run_id = query.get("run_id", [""])[0] or latest_run_id()
                export_type = query.get("type", ["clipboard"])[0]
                self.send_json(export_dashboard(run_id, export_type))
            elif path == "/api/capture-file":
                target = safe_repo_path(query.get("path", [""])[0])
                self.send_file(target)
            elif path == "/api/status":
                self.send_json(status_payload())
            elif path == "/api/runs":
                self.send_json({"runs": get_runs()})
            elif path == "/api/url-registry":
                filters = registry_filter_from_query(query)
                limit = parse_nonnegative_int(query.get("limit", ["250"])[0], 250, 1000)
                offset = parse_nonnegative_int(query.get("offset", ["0"])[0], 0, 1_000_000)
                self.send_json(registry_payload(filters, limit=limit, offset=offset))
            elif path == "/api/targets":
                self.send_json({"path": rel(TARGET_URLS), "content": TARGET_URLS.read_text(encoding="utf-8")})
            elif path == "/api/artifact":
                target = safe_repo_path(query.get("path", [""])[0])
                self.send_json({"path": rel(target), "content": target.read_text(encoding="utf-8")})
            else:
                self.send_error(404, "Not found")
        except Exception as exc:
            self.send_json({"error": str(exc)}, status=500)

    def do_POST(self) -> None:
        path = urllib.parse.urlparse(self.path).path
        payload = self.read_body()
        try:
            if path == "/api/dashboard/import":
                run_id = payload.get("run_id") or latest_run_id()
                self.send_json(build_dashboard_data(run_id))
            elif path == "/api/dashboard/capture":
                run_id = payload.get("run_id") or latest_run_id()
                self.send_json(capture_run(run_id, payload.get("url")))
            elif path == "/api/run/init":
                if STATE_FILE.exists():
                    self.send_json({"error": "An active run already exists.", "status": status_payload()}, status=409)
                    return
                result = run_runner("--init")
                self.send_json({"command": result.__dict__, "status": status_payload()})
            elif path == "/api/run/next":
                args = ["--next"]
                if payload.get("skip_scrape"):
                    args.append("--skip-scrape")
                result = run_runner(*args)
                self.send_json({"command": result.__dict__, "status": status_payload()}, status=200 if result.exit_code == 0 else 409)
            elif path == "/api/url-registry/selection":
                self.send_json(save_registry_selection(payload))
            else:
                self.send_error(404, "Not found")
        except Exception as exc:
            self.send_json({"error": str(exc)}, status=500)

    def do_PUT(self) -> None:
        path = urllib.parse.urlparse(self.path).path
        payload = self.read_body()
        try:
            if path == "/api/dashboard/overrides":
                run_id = payload.get("run_id") or latest_run_id()
                update_overrides(run_id, payload)
                self.send_json(get_dashboard_data(run_id))
            elif path == "/api/targets":
                content = str(payload.get("content", ""))
                TARGET_URLS.write_text(content, encoding="utf-8")
                self.send_json({"path": rel(TARGET_URLS), "content": content})
            else:
                self.send_error(404, "Not found")
        except Exception as exc:
            self.send_json({"error": str(exc)}, status=500)

    def read_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw) if raw else {}

    def send_json(self, payload: dict[str, Any], status: int = 200) -> None:
        data = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(data)

    def send_file(self, path: Path) -> None:
        if not path.exists() or not path.is_file():
            self.send_error(404, "File not found")
            return
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def latest_run_id() -> str:
    runs = get_runs()
    if not runs:
        raise ValueError("No runs found")
    return runs[-1]["run_id"]


def main() -> int:
    server = ThreadingHTTPServer(("127.0.0.1", 8787), Handler)
    print("Dashboard API listening at http://127.0.0.1:8787")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping dashboard API.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
