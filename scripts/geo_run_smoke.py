#!/usr/bin/env python3
"""Smoke-test a completed GEO run against prior repo failure modes.

Data flow: checks read SQLite plus generated run artifacts. They do not mutate run data.
Pitfalls: this is a send gate for /geo-run; keep checks concrete and tied to user-facing failures.
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

from scripts import db  # noqa: E402
from scripts.dashboard_domain import READY_TO_SEND  # noqa: E402
from scripts.dashboard_read_model import dashboard_payload  # noqa: E402
from scripts.export import slug, validate_jira_csv_file  # noqa: E402

STATE_FILE = ROOT / "runs" / "active_run.json"


class SmokeFailure(Exception):
    """Raised when a completed run violates a /geo-run send gate."""


def run_dir_for(run_id: str) -> Path:
    matches = sorted((ROOT / "runs").glob(f"{run_id}_*"))
    if matches:
        return matches[-1]
    return ROOT / "runs" / run_id


def active_or_latest_run_id(conn, requested: str | None = None) -> str:
    if requested:
        return requested
    if STATE_FILE.exists():
        try:
            state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            if state.get("run_id"):
                return str(state["run_id"])
        except json.JSONDecodeError:
            pass
    found = conn.execute("SELECT run_id FROM runs ORDER BY run_number DESC LIMIT 1").fetchone()
    if not found:
        raise SmokeFailure("No run_id supplied and no runs exist in SQLite.")
    return str(found["run_id"])


def assert_true(condition: Any, message: str) -> None:
    if not condition:
        raise SmokeFailure(message)


def load_manifest(ready_dir: Path) -> dict[str, Any]:
    manifest_path = ready_dir / "manifest.json"
    assert_true(manifest_path.exists(), f"Missing ready-to-send manifest: {manifest_path}")
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SmokeFailure(f"Invalid ready-to-send manifest JSON: {exc}") from exc


def csv_rows(path: Path) -> list[dict[str, str]]:
    assert_true(path.exists(), f"Missing CSV: {path}")
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def selected_target_urls(conn, run_id: str) -> list[str]:
    return [str(row["url"]) for row in db.run_target_urls(conn, run_id)]


def metadata_snapshot_urls(conn, run_id: str) -> set[str]:
    rows = db.rows(
        conn,
        """
        SELECT u.url
        FROM metadata_snapshots ms
        JOIN urls u ON u.url_id = ms.url_id
        WHERE ms.run_id = ?
        """,
        (run_id,),
    )
    return {str(row["url"]) for row in rows}


def metadata_snapshot_artifact_records(snapshot_path: Path) -> dict[str, str]:
    if not snapshot_path.exists():
        return {}
    text = snapshot_path.read_text(encoding="utf-8", errors="replace")
    records: dict[str, str] = {}
    for section in re.split(r"(?=^##\s+Page\s+\d+:)", text, flags=re.MULTILINE):
        if not re.match(r"^##\s+Page\s+\d+:", section):
            continue
        url_match = re.search(r"^\*\*URL:\*\*\s*(\S+)", section, flags=re.MULTILINE)
        status_match = re.search(r"^\*\*Fetch status:\*\*\s*(.+?)\s*$", section, flags=re.MULTILINE)
        if not url_match:
            continue
        records[url_match.group(1).strip()] = (status_match.group(1).strip() if status_match else "")
    return records


def urls_in_text(text: str) -> set[str]:
    values: set[str] = set()
    for raw in re.findall(r"https?://[^\s)<>\]\"']+", text or ""):
        values.add(raw.rstrip(".,;:)]}\"'"))
    return values


def gap_analysis_artifact_urls(gap_path: Path) -> set[str]:
    if not gap_path.exists():
        return set()
    return urls_in_text(gap_path.read_text(encoding="utf-8", errors="replace"))


def smoke_full_target_coverage(conn, run_id: str, run_dir: Path) -> list[str]:
    targets = selected_target_urls(conn, run_id)
    snapshot_urls = metadata_snapshot_urls(conn, run_id)
    missing = [url for url in targets if url not in snapshot_urls]
    snapshot_path = run_dir / "metadata_snapshot.md"
    gap_path = run_dir / "gap_analysis.md"
    artifact_records = metadata_snapshot_artifact_records(snapshot_path)
    artifact_missing = [url for url in targets if url not in artifact_records]
    status_missing = [url for url in targets if url in artifact_records and not artifact_records[url]]
    gap_urls = gap_analysis_artifact_urls(gap_path)
    gap_missing = [url for url in targets if url not in gap_urls]
    assert_true(targets, f"{run_id} has no run_url_targets snapshot.")
    assert_true(snapshot_path.exists() and snapshot_path.stat().st_size > 0, f"Missing metadata snapshot for {run_id}.")
    assert_true(gap_path.exists() and gap_path.stat().st_size > 0, f"Missing gap analysis for {run_id}.")
    assert_true(not missing, f"{run_id} metadata snapshots are missing {len(missing)} selected URL(s): {missing[:5]}")
    assert_true(not artifact_missing, f"{run_id} metadata_snapshot.md is missing {len(artifact_missing)} selected URL(s): {artifact_missing[:5]}")
    assert_true(not status_missing, f"{run_id} metadata_snapshot.md has {len(status_missing)} selected URL(s) without fetch status: {status_missing[:5]}")
    assert_true(not gap_missing, f"{run_id} gap_analysis.md is missing {len(gap_missing)} selected URL(s): {gap_missing[:5]}")
    return [f"target coverage: {len(targets)} selected URL(s) represented in metadata_snapshots, metadata_snapshot.md, and gap_analysis.md"]


def smoke_active_run_exports(run_id: str, run_dir: Path) -> list[str]:
    jira_path = run_dir / f"{run_id}_jira_import.csv"
    export_path = run_dir / f"{run_id}_optimization_proposal_export.md"
    assert_true(jira_path.exists(), f"Missing active-run Jira export: {jira_path}")
    assert_true(export_path.exists(), f"Missing active-run proposal export: {export_path}")
    assert_true(run_id in jira_path.name and run_id in jira_path.read_text(encoding="utf-8"), f"Jira export does not identify {run_id}.")
    assert_true(run_id in export_path.name and run_id in export_path.read_text(encoding="utf-8"), f"Proposal export does not identify {run_id}.")
    stale_exports = [path for path in run_dir.glob("*jira_import.csv") if run_id not in path.name]
    assert_true(not stale_exports, f"Run dir contains stale Jira export(s): {[path.name for path in stale_exports]}")
    return [f"active exports: {jira_path.name} and {export_path.name}"]


def smoke_dashboard_coverage(conn, run_id: str) -> list[str]:
    payload = dashboard_payload(conn, run_id)
    summary = payload.get("summary") or {}
    suggestions = summary.get("change_suggestions") or {}
    changes = payload.get("metadata_changes") or []
    recs = payload.get("recommendations") or []
    if changes:
        expected_total = len({str(item.get("metadata_change_id") or item.get("proposal_id")) for item in changes})
    else:
        expected_total = len({str(item.get("proposal_id")) for item in recs})
    assert_true(summary.get("recommendations") == len(recs), "Dashboard recommendation count does not match payload.")
    assert_true(suggestions.get("total") == expected_total, f"Change suggestion total expected {expected_total}, got {suggestions.get('total')}.")
    assert_true(set((suggestions.get("labels") or {}).keys()) == set((suggestions.get("by_type") or {}).keys()), "Change suggestion labels and type counts diverged.")
    return [f"dashboard coverage: {expected_total} distinct change suggestion(s)"]


def smoke_ready_to_send_bundle(conn, run_id: str, run_dir: Path) -> list[str]:
    ready_dir = run_dir / "ready-to-send"
    assert_true(ready_dir.exists(), f"Missing ready-to-send bundle for {run_id}.")
    manifest = load_manifest(ready_dir)
    dashboard_summary = (dashboard_payload(conn, run_id).get("summary") or {})
    tracker_rows = csv_rows(ready_dir / "recommendation-tracker.csv")
    ready_rows = [row for row in tracker_rows if row.get("status") == READY_TO_SEND]
    actual_files = sorted(path.relative_to(ready_dir).as_posix() for path in ready_dir.rglob("*") if path.is_file())
    manifest_assets = sorted(manifest.get("assets") or [])
    required_core = {
        "README.md",
        "stakeholder-email.md",
        "qa-checklist.md",
        "jira-validation-report.md",
        f"{run_id}-jira-import.csv",
        "recommendation-tracker.csv",
        "source-evidence.csv",
        "page-coverage.csv",
        "metadata-changes.csv",
        "copy-blocks.csv",
        "manifest.json",
    }
    assert_true(required_core.issubset(set(actual_files)), f"Ready bundle missing core assets: {sorted(required_core - set(actual_files))}")
    assert_true(manifest_assets == actual_files, "Ready bundle manifest assets do not match files on disk.")
    assert_true(int(manifest.get("recommendations") or 0) == len(tracker_rows), "Manifest recommendation count does not match tracker.")
    assert_true(int(manifest.get("ready_to_send") or 0) == len(ready_rows), "Manifest ready_to_send count does not match tracker.")
    assert_true(int(dashboard_summary.get("ready_to_send") or 0) == len(ready_rows), "Dashboard ready_to_send count does not match ready-to-send tracker.")
    assert_true(not list(ready_dir.glob("recommendations/*/jira.csv")), "Stale per-item jira.csv files remain; expected jira-ticket.csv only.")
    report_text = (ready_dir / "jira-validation-report.md").read_text(encoding="utf-8")
    assert_true("Status: PASS" in report_text, "Jira validation report is not PASS.")
    for row in ready_rows:
        assert_true(row.get("sources"), f"Ready item {row['display_id']}_{row['proposal_id']} has no linked source evidence.")
        folder = ready_dir / "recommendations" / f"{slug(row['display_id'])}_{slug(row['proposal_id'])}"
        for filename in ("brief.md", "jira-ticket.csv", "handoff-note.md", "acceptance-checklist.md", "source-evidence.md"):
            assert_true((folder / filename).exists(), f"Missing {filename} for ready item {row['display_id']}_{row['proposal_id']}.")
        errors = validate_jira_csv_file(folder / "jira-ticket.csv", expected_story_count=1)
        assert_true(not errors, f"{folder / 'jira-ticket.csv'} failed validation: {errors}")
    full_errors = validate_jira_csv_file(ready_dir / f"{run_id}-jira-import.csv")
    assert_true(not full_errors, f"Full-run Jira CSV failed validation: {full_errors}")
    return [f"ready-to-send: {len(ready_rows)} item Jira CSV(s), {len(actual_files)} manifest asset(s)"]


def smoke_execution_log(run_id: str) -> list[str]:
    path = ROOT / "memory" / "execution_log.md"
    assert_true(path.exists() and path.stat().st_size > 0, "Missing local execution log.")
    text = path.read_text(encoding="utf-8", errors="replace")
    assert_true(run_id in text, f"Execution log does not mention {run_id}.")
    return ["execution log: present and run-aware"]


def smoke_gap_research(conn, run_id: str, run_dir: Path) -> list[str]:
    path = run_dir / "gap_research.md"
    assert_true(path.exists() and path.stat().st_size > 0, f"Missing Phase 2.5 gap research for {run_id}.")
    proposal_links = conn.execute(
        """
        SELECT COUNT(*)
        FROM proposal_sources ps
        JOIN proposals p ON p.proposal_id = ps.proposal_id
        WHERE p.run_id = ?
        """,
        (run_id,),
    ).fetchone()[0]
    assert_true(proposal_links > 0, f"{run_id} has no proposal-source evidence links.")
    return [f"gap research: {proposal_links} proposal-source link(s)"]


def run_smoke(run_id: str | None = None) -> list[str]:
    db.initialize_database(db.DB_PATH)
    messages: list[str] = []
    with db.connection(db.DB_PATH) as conn:
        resolved_run_id = active_or_latest_run_id(conn, run_id)
        run_dir = run_dir_for(resolved_run_id)
        assert_true(run_dir.exists(), f"Run directory does not exist for {resolved_run_id}: {run_dir}")
        messages.append(f"run: {resolved_run_id}")
        messages.extend(smoke_full_target_coverage(conn, resolved_run_id, run_dir))
        messages.extend(smoke_gap_research(conn, resolved_run_id, run_dir))
        messages.extend(smoke_dashboard_coverage(conn, resolved_run_id))
        messages.extend(smoke_active_run_exports(resolved_run_id, run_dir))
        messages.extend(smoke_ready_to_send_bundle(conn, resolved_run_id, run_dir))
        messages.extend(smoke_execution_log(resolved_run_id))
    return messages


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke-test a completed GEO run against known failure modes.")
    parser.add_argument("--run-id", help="Run ID to check. Defaults to runs/active_run.json, then latest DB run.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output.")
    args = parser.parse_args()
    try:
        messages = run_smoke(args.run_id)
    except SmokeFailure as exc:
        if args.json:
            print(json.dumps({"ok": False, "error": str(exc)}, indent=2))
        else:
            print(f"FAIL: {exc}")
        return 1
    if args.json:
        print(json.dumps({"ok": True, "checks": messages}, indent=2))
    else:
        print("GEO run smoke checks passed:")
        for message in messages:
            print(f"- {message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
