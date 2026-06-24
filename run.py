#!/usr/bin/env python3
"""DB-backed CLI orchestrator for the Radisson GEO Optimizer.

Data flow: run state lives in SQLite and a small active_run.json pointer; phase agents still write
the same markdown artifacts. Pitfalls: URL selection comes from urls.selected_for_next_run, while
next_geo_run.csv is only an export view for inspection.
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Any

from scripts import db
from scripts.export import export_all
from scripts.import_run_artifacts import import_all_runs
from scripts.migrate_to_sqlite import infer_brand, migrate, parse_criteria, parse_gaps, parse_proposals


ROOT = Path(__file__).resolve().parent
STATE_FILE = ROOT / "runs" / "active_run.json"

PHASE_0 = "PHASE_0_LITERATURE_REFRESH"
PHASE_1 = "PHASE_1_CONTEXT_BRIEF"
PHASE_2 = "PHASE_2_AUDIT_GAP_ANALYSIS"
PHASE_2_5 = "PHASE_2_5_TARGETED_GAP_RESEARCH"
PHASE_3 = "PHASE_3_OPTIMIZATION_PROPOSAL"
PHASE_3_5 = "PHASE_3_5_JIRA_PREP"
PHASE_4 = "PHASE_4_LOG_AND_LEARN"

PHASE_ORDER = [PHASE_0, PHASE_1, PHASE_2, PHASE_2_5, PHASE_3, PHASE_3_5, PHASE_4]

PHASE_LABELS = {
    PHASE_0: "Phase 0 - Literature Refresh",
    PHASE_1: "Phase 1 - Context Brief",
    PHASE_2: "Phase 2 - Audit and Gap Analysis",
    PHASE_2_5: "Phase 2.5 - Targeted Gap Research",
    PHASE_3: "Phase 3 - Optimization Proposal",
    PHASE_3_5: "Phase 3.5 - Jira Prep",
    PHASE_4: "Phase 4 - Log and Learn",
}


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def load_state() -> dict[str, Any] | None:
    if not STATE_FILE.exists():
        return None
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid state file {rel(STATE_FILE)}: {exc}") from exc


def save_state(state: dict[str, Any]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def detect_next_run_number(conn) -> int:
    row = conn.execute("SELECT MAX(run_number) FROM runs").fetchone()
    current = int(row[0] or 0)
    return current + 1


def previous_run_id(conn) -> str | None:
    row = conn.execute("SELECT run_id FROM runs ORDER BY run_number DESC LIMIT 1").fetchone()
    return str(row[0]) if row and row[0] else None


def expected_files(state: dict[str, Any], phase: str | None = None) -> list[Path]:
    phase = phase or state["current_phase"]
    run_id = state["run_id"]
    run_dir = ROOT / state["run_dir"]
    if phase == PHASE_0:
        return [ROOT / "literature" / f"{run_id}_sources.md", ROOT / "framework" / f"{run_id}_criteria.md"]
    if phase == PHASE_2:
        return [run_dir / "metadata_snapshot.md", run_dir / "gap_analysis.md"]
    if phase == PHASE_2_5:
        return [run_dir / "gap_research.md"]
    if phase == PHASE_3:
        return [run_dir / "optimization_proposal.md"]
    if phase == PHASE_4:
        return [run_dir / "log_reflection.md", ROOT / "memory" / "master_summary.md"]
    return []


def missing_required_files(state: dict[str, Any], phase: str | None = None) -> list[Path]:
    return [path for path in expected_files(state, phase) if not path.exists() or path.stat().st_size == 0]


def urls_in(text: str) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    for raw in re.findall(r"https?://[^\s)<>\]\"']+", text or ""):
        url = raw.rstrip(".,;)]}\"'")
        if url not in seen:
            values.append(url)
            seen.add(url)
    return values


def source_title_for(url: str) -> str:
    host = urllib.parse.urlsplit(url).netloc or url
    return host.removeprefix("www.")


def sync_phase_to_db(state: dict[str, Any], phase: str) -> None:
    run_id = state["run_id"]
    run_dir = ROOT / state["run_dir"]
    with db.connection() as conn:
        if phase == PHASE_0:
            conn.execute("DELETE FROM source_insights WHERE run_id = ?", (run_id,))
            conn.execute("DELETE FROM sources WHERE run_id = ?", (run_id,))
            conn.execute("DELETE FROM criteria WHERE run_id = ?", (run_id,))
            for item in parse_criteria(ROOT / "framework" / f"{run_id}_criteria.md", run_id):
                db.upsert_criterion(conn, run_id, item["code"], item["description"])
            literature_text = (ROOT / "literature" / f"{run_id}_sources.md").read_text(encoding="utf-8", errors="replace")
            for url in urls_in(literature_text):
                parsed = urllib.parse.urlsplit(url)
                cur = conn.execute(
                    """
                    INSERT INTO sources(run_id, url, domain, title, source_type, credibility, fetched_at)
                    VALUES(?, ?, ?, ?, 'literature', 1.0, ?)
                    """,
                    (run_id, url, parsed.netloc, source_title_for(url), datetime.now().isoformat(timespec="seconds")),
                )
                conn.execute(
                    """
                    INSERT INTO source_insights(source_id, run_id, claim, theme, weight)
                    VALUES(?, ?, ?, 'literature_source', 1.0)
                    """,
                    (cur.lastrowid, run_id, f"Literature source consulted: {url}"),
                )
        elif phase == PHASE_2:
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
        elif phase == PHASE_3:
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
                        status="NEW",
                        description="[NEEDED: proposal references a gap not present in gap_analysis.md]",
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
        elif phase == PHASE_3_5:
            db.build_jira_tickets(conn, run_id)
        elif phase == PHASE_4:
            conn.execute("UPDATE runs SET status = 'COMPLETED' WHERE run_id = ?", (run_id,))
            conn.execute(
                """
                UPDATE urls
                SET last_audited_run = ?
                WHERE url_id IN (SELECT url_id FROM run_url_targets WHERE run_id = ?)
                """,
                (run_id, run_id),
            )


def print_phase_prompt(state: dict[str, Any]) -> None:
    phase = state["current_phase"]
    run_id = state["run_id"]
    run_dir = state["run_dir"]
    print()
    print(f"## {PHASE_LABELS[phase]}")
    print(f"Run: {run_id} ({state['run_date']})")
    print()
    if phase == PHASE_0:
        print(f"Write literature/{run_id}_sources.md and framework/{run_id}_criteria.md from fresh GEO/AEO research.")
    elif phase == PHASE_1:
        print("Automated DB state is ready. Use selected DB URLs for the current context brief.")
    elif phase == PHASE_2:
        print(f"Audit selected DB URLs and write {run_dir}/metadata_snapshot.md plus {run_dir}/gap_analysis.md.")
    elif phase == PHASE_2_5:
        print(f"Research the gaps in {run_dir}/gap_analysis.md and write {run_dir}/gap_research.md.")
    elif phase == PHASE_3:
        print(f"Synthesize one proposal per gap and write {run_dir}/optimization_proposal.md.")
    elif phase == PHASE_3_5:
        print("Run python3 run.py --next to build jira_tickets rows and exports from the DB.")
    elif phase == PHASE_4:
        print(f"Write {run_dir}/log_reflection.md, refresh memory/master_summary.md, and append memory/run_index.md.")


def ensure_db() -> None:
    if not db.DB_PATH.exists():
        result = migrate(db.DB_PATH)
        if not result["valid"]:
            raise SystemExit(f"Migration validation failed: {result['mismatches']}")
    db.initialize_database(db.DB_PATH)
    with db.connection() as conn:
        counts = db.table_counts(conn)
    if counts.get("runs", 0) and counts.get("sources", 0) == 0:
        import_all_runs(db.DB_PATH)


def init_run() -> int:
    ensure_db()
    existing = load_state()
    if existing and existing.get("status") == "IN_PROGRESS":
        print(f"Active run already in progress: {existing['run_id']} ({existing['current_phase']}).")
        return 2
    with db.connection() as conn:
        next_number = detect_next_run_number(conn)
        run_id = f"run_{next_number:03d}"
        run_date = datetime.now().strftime("%Y-%m-%d")
        run_dir = ROOT / "runs" / f"{run_id}_{run_date}"
        run_dir.mkdir(parents=True, exist_ok=True)
        db.upsert_run(conn, run_id, next_number, run_date, "IN_PROGRESS", previous_run_id(conn))
        selected_count = db.snapshot_next_run_targets(conn, run_id)
    state = {
        "run_id": run_id,
        "run_number": next_number,
        "run_date": run_date,
        "run_dir": rel(run_dir),
        "status": "IN_PROGRESS",
        "current_phase": PHASE_0,
        "completed_phases": [],
        "selected_url_count": selected_count,
    }
    save_state(state)
    print(f"Initialized {run_id} with {selected_count} DB-selected URLs.")
    print_phase_prompt(state)
    return 0


def status() -> int:
    ensure_db()
    state = load_state()
    with db.connection() as conn:
        counts = db.table_counts(conn)
        selected_count = len(db.selected_urls(conn))
    if not state:
        print("No active run.")
    else:
        print(f"Active run: {state['run_id']} - {PHASE_LABELS.get(state['current_phase'], state['current_phase'])}")
        print(f"Run dir: {state['run_dir']}")
    print(f"Selected URLs in DB: {selected_count}")
    print("Table counts:")
    for table in db.TABLES:
        print(f"- {table}: {counts[table]}")
    return 0


def advance(skip_scrape: bool = False) -> int:
    ensure_db()
    state = load_state()
    if not state:
        print("No active run. Run python3 run.py --init first.")
        return 2
    phase = state["current_phase"]
    if phase != PHASE_3_5 and missing_required_files(state, phase) and not skip_scrape:
        missing = ", ".join(rel(path) for path in missing_required_files(state, phase))
        print(f"Cannot advance; missing required files for {phase}: {missing}")
        return 2
    if not skip_scrape or phase == PHASE_3_5:
        sync_phase_to_db(state, phase)
    if phase == PHASE_3_5:
        export_all(state["run_id"])
    completed = list(state.get("completed_phases", []))
    if phase not in completed:
        completed.append(phase)
    current_index = PHASE_ORDER.index(phase)
    if current_index == len(PHASE_ORDER) - 1:
        state["status"] = "COMPLETED"
        state["completed_phases"] = completed
        save_state(state)
        print(f"Completed {state['run_id']}.")
        return 0
    state["completed_phases"] = completed
    state["current_phase"] = PHASE_ORDER[current_index + 1]
    save_state(state)
    print(f"Advanced to {PHASE_LABELS[state['current_phase']]}.")
    print_phase_prompt(state)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Radisson GEO Optimizer DB-backed runner.")
    parser.add_argument("--init", action="store_true", help="Initialize the next run in SQLite.")
    parser.add_argument("--status", action="store_true", help="Show DB and active-run status.")
    parser.add_argument("--next", action="store_true", help="Advance the active run by one phase.")
    parser.add_argument("--skip-scrape", action="store_true", help="Smoke-pass a phase without requiring generated scrape files.")
    parser.add_argument("--run", action="store_true", help="Alias for --init when no active run exists.")
    parser.add_argument("--dry-run", action="store_true", help="Validate DB status without mutating run phase.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.init or args.run:
        return init_run()
    if args.status or args.dry_run:
        return status()
    if args.next:
        return advance(skip_scrape=args.skip_scrape)
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
