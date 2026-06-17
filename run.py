#!/usr/bin/env python3
"""Stateful CLI orchestrator for the Radisson GEO Optimizer."""

from __future__ import annotations

import argparse
import json
import logging
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
STATE_FILE = ROOT / "runs" / "active_run.json"
RUN_INDEX = ROOT / "memory" / "run_index.md"
IMPLEMENTATION_LOG = ROOT / "inferred" / "implementation_log.md"
TARGET_URLS = ROOT / "sources" / "website" / "target_urls.md"
RUN_TARGETS_CSV = ROOT / "sources" / "website" / "run_targets" / "next_geo_run.csv"

PHASE_0 = "PHASE_0_LITERATURE_REFRESH"
PHASE_1 = "PHASE_1_CONTEXT_BRIEF"
PHASE_2 = "PHASE_2_AUDIT_GAP_ANALYSIS"
PHASE_2_5 = "PHASE_2_5_TARGETED_GAP_RESEARCH"
PHASE_3 = "PHASE_3_OPTIMIZATION_PROPOSAL"
PHASE_4 = "PHASE_4_LOG_AND_LEARN"

PHASE_ORDER = [PHASE_0, PHASE_1, PHASE_2, PHASE_2_5, PHASE_3, PHASE_4]

PHASE_LABELS = {
    PHASE_0: "Phase 0 - Literature Refresh",
    PHASE_1: "Phase 1 - Context Brief",
    PHASE_2: "Phase 2 - Audit and Gap Analysis",
    PHASE_2_5: "Phase 2.5 - Targeted Gap Research",
    PHASE_3: "Phase 3 - Optimization Proposal",
    PHASE_4: "Phase 4 - Log and Learn",
}


def rel(path: Path) -> str:
    """Return a repo-relative POSIX path for state files and logs."""
    return path.relative_to(ROOT).as_posix()


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


def run_id_number(run_id: str) -> int:
    match = re.search(r"run_(\d+)", run_id)
    if not match:
        raise ValueError(f"Invalid run id: {run_id}")
    return int(match.group(1))


def detect_next_run_number() -> int:
    """Detect the next run number from memory/run_index.md, with folder fallback."""
    numbers: list[int] = []
    if RUN_INDEX.exists():
        for match in re.finditer(r"\brun_(\d{3,})\s*\|", RUN_INDEX.read_text(encoding="utf-8")):
            numbers.append(int(match.group(1)))

    if not numbers:
        for path in (ROOT / "runs").glob("run_[0-9][0-9][0-9]_*"):
            match = re.match(r"run_(\d{3,})_", path.name)
            if match:
                numbers.append(int(match.group(1)))

    return (max(numbers) + 1) if numbers else 1


def find_run_dir(run_id: str) -> Path | None:
    matches = sorted((ROOT / "runs").glob(f"{run_id}_*"))
    return matches[-1] if matches else None


def expected_files(state: dict[str, Any], phase: str | None = None) -> list[Path]:
    phase = phase or state["current_phase"]
    run_id = state["run_id"]
    run_dir = ROOT / state["run_dir"]
    if phase == PHASE_0:
        return [
            ROOT / "literature" / f"{run_id}_sources.md",
            ROOT / "framework" / f"{run_id}_criteria.md",
        ]
    if phase == PHASE_2:
        return [run_dir / "gap_analysis.md"]
    if phase == PHASE_2_5:
        return [run_dir / "gap_research.md"]
    if phase == PHASE_3:
        return [run_dir / "optimization_proposal.md"]
    if phase == PHASE_4:
        return [run_dir / "log_reflection.md", ROOT / "memory" / "master_summary.md"]
    return []


def missing_required_files(state: dict[str, Any], phase: str | None = None) -> list[Path]:
    missing: list[Path] = []
    for path in expected_files(state, phase):
        if not path.exists() or path.stat().st_size == 0:
            missing.append(path)
    return missing


def append_completed(state: dict[str, Any], *phases: str) -> None:
    completed = list(state.get("completed_phases", []))
    for phase in phases:
        if phase not in completed:
            completed.append(phase)
    state["completed_phases"] = completed


def phase_index(phase: str) -> int:
    return PHASE_ORDER.index(phase)


def print_phase_prompt(state: dict[str, Any], phase: str | None = None) -> None:
    phase = phase or state["current_phase"]
    run_id = state["run_id"]
    run_dir = state["run_dir"]

    print()
    print(f"## {PHASE_LABELS.get(phase, phase)}")
    print(f"Run: {run_id} ({state['run_date']})")
    print()

    if phase == PHASE_0:
        print("Prompt for the active agent:")
        print(
            f"""Research the current GEO/AEO environment for hotel discovery using live web sources. Write:
- literature/{run_id}_sources.md
- framework/{run_id}_criteria.md

Cover dominant AI travel engines, hotel discovery signals, hospitality GEO/AEO best practices, competitor/OTA metadata patterns, and American bleisure traveler query behavior. Make every criterion auditable against live pages.

When both files exist, run:
python run.py --next

If live Radisson scraping is blocked during the automated step, run:
python run.py --next --skip-scrape"""
        )
        return

    if phase == PHASE_2:
        print("Automated context files are ready:")
        print(f"- {run_dir}/metadata_snapshot.md")
        print(f"- {run_dir}/context_brief.md")
        print()
        print("Prompt for the active agent:")
        print(
            f"""Review the current criteria, metadata snapshot, and context brief. Score every audited page for missing, weak, or misaligned GEO/AEO signals. Write:
- {run_dir}/gap_analysis.md

Include a clear audit summary, every gap ID, page URL, criterion/signal, current state, gap type, severity 1-3, and whether it appears new or recurring.

When gap_analysis.md exists, run:
python run.py --next"""
        )
        return

    if phase == PHASE_2_5:
        print("Prompt for the active agent:")
        print(
            f"""Use a fresh web-capable research pass focused only on the gaps in:
- {run_dir}/gap_analysis.md

For each gap, find the current best practice, a competitor or OTA example, a concrete fix, and the likely impact for American bleisure traveler discovery. Write the full research output with citations to:
- {run_dir}/gap_research.md

When gap_research.md exists, run:
python run.py --next"""
        )
        return

    if phase == PHASE_3:
        print("Prompt for the active agent:")
        print(
            f"""Synthesize the current proposal from:
- framework/{run_id}_criteria.md
- {run_dir}/gap_research.md
- {run_dir}/context_brief.md

Write:
- {run_dir}/optimization_proposal.md

Open with an executive summary and then write exactly one concrete proposal entry per gap: proposed change, source citation, current state, inferred implementation status, directional impact estimate, and priority tier.

For every proposal entry, include a "Jira ticket fields" subsection that is ready to convert to the dashboard's Jira CSV. Use these Jira import fields exactly:
- Issue Type
- Epic Name
- Summary
- Description
- Priority
- Labels
- Component
- Acceptance Criteria

Treat Summary as the ticket name/title for Jira import.

Group the Description content under:
- Dev change specs
- SEO/GEO rationale
- GEO visibility score
- Validation steps

Acceptance Criteria must be concrete, testable, and implementation-facing. If a value cannot be determined from the run evidence, include a [NEEDED: ...] placeholder instead of guessing. This Jira ticket subsection is mandatory for every proposal every time the GEO optimizer is run.

When optimization_proposal.md exists, run:
python run.py --next"""
        )
        return

    if phase == PHASE_4:
        print("Prompt for the active agent:")
        print(
            f"""Write the run reflection and refresh cross-run memory:
- {run_dir}/log_reflection.md
- memory/master_summary.md

The reflection should cover correct/missed gaps, how research sharpened proposals, diff findings, future weighting changes, and detection-logic changes. Keep memory/master_summary.md under 800 tokens.

When both files exist, run:
python run.py --next

The final --next call will append memory/run_index.md, update inferred/implementation_log.md, save completed run state, and clear runs/active_run.json."""
        )
        return

    print("This phase is automated. Run python run.py --next to continue.")


def init_run() -> int:
    existing = load_state()
    if existing and existing.get("status") == "IN_PROGRESS":
        print(
            f"Active run already in progress: {existing['run_id']} "
            f"({PHASE_LABELS.get(existing['current_phase'], existing['current_phase'])})."
        )
        print("Run python run.py --status, or finish it before initializing a new run.")
        return 2

    next_number = detect_next_run_number()
    run_id = f"run_{next_number:03d}"
    run_date = datetime.now().strftime("%Y-%m-%d")
    run_dir = ROOT / "runs" / f"{run_id}_{run_date}"
    if run_dir.exists():
        logging.warning("%s already exists; reusing it for this active run.", rel(run_dir))
    else:
        run_dir.mkdir(parents=True, exist_ok=False)
        logging.info("Created %s", rel(run_dir))

    previous_id = f"run_{next_number - 1:03d}" if next_number > 1 else None
    previous_dir = find_run_dir(previous_id) if previous_id else None

    state = {
        "run_id": run_id,
        "run_number": next_number,
        "run_date": run_date,
        "run_dir": rel(run_dir),
        "previous_run_id": previous_id,
        "previous_run_dir": rel(previous_dir) if previous_dir else None,
        "current_phase": PHASE_0,
        "status": "IN_PROGRESS",
        "completed_phases": [],
        "metadata": {
            "target_urls_count": 0,
            "scraped_count": 0,
            "blocked_count": 0,
            "gaps_found": 0,
            "implemented_count": 0,
        },
    }
    save_state(state)
    logging.info("Wrote %s", rel(STATE_FILE))
    print_phase_prompt(state, PHASE_0)
    return 0


def print_status() -> int:
    state = load_state()
    if not state:
        print("No active run. Start one with: python run.py --init")
        return 0

    phase = state["current_phase"]
    print(f"Active run: {state['run_id']} ({state['run_date']})")
    print(f"Status: {state.get('status', 'UNKNOWN')}")
    print(f"Run directory: {state['run_dir']}")
    print(f"Current phase: {PHASE_LABELS.get(phase, phase)}")
    if state.get("previous_run_id"):
        print(f"Previous run: {state['previous_run_id']} ({state.get('previous_run_dir') or 'not found'})")
    print()

    expected = expected_files(state)
    if expected:
        print("Expected files for current phase:")
        for path in expected:
            marker = "OK" if path.exists() and path.stat().st_size > 0 else "MISSING"
            print(f"- [{marker}] {rel(path)}")
        print()

    current_idx = phase_index(phase)
    remaining = [PHASE_LABELS[p] for p in PHASE_ORDER[current_idx:]]
    print("Remaining steps:")
    for item in remaining:
        print(f"- {item}")
    print()
    print("Next command: python run.py --next")
    return 0


def run_subprocess(command: list[str]) -> None:
    logging.info("Running: %s", " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def active_targets_path() -> Path:
    if RUN_TARGETS_CSV.exists() and RUN_TARGETS_CSV.stat().st_size > 0:
        return RUN_TARGETS_CSV
    return TARGET_URLS


def previous_snapshot_path(state: dict[str, Any]) -> Path | None:
    previous = state.get("previous_run_dir")
    if not previous:
        return None
    snapshot = ROOT / previous / "metadata_snapshot.md"
    return snapshot if snapshot.exists() else None


def run_scraper(state: dict[str, Any], skip_scrape: bool) -> dict[str, Any]:
    run_dir = ROOT / state["run_dir"]
    summary_path = run_dir / "scrape_summary.json"
    targets_path = active_targets_path()
    command = [
        sys.executable,
        "scripts/scraper.py",
        "--targets",
        rel(targets_path),
        "--run-dir",
        state["run_dir"],
        "--run-id",
        state["run_id"],
        "--run-date",
        state["run_date"],
        "--summary-json",
        rel(summary_path),
    ]
    previous_snapshot = previous_snapshot_path(state)
    if previous_snapshot:
        command.extend(["--previous-snapshot", rel(previous_snapshot)])
    if skip_scrape:
        command.append("--skip-scrape")

    run_subprocess(command)
    if summary_path.exists():
        return json.loads(summary_path.read_text(encoding="utf-8"))
    return {}


def run_differ(state: dict[str, Any]) -> dict[str, Any]:
    run_dir = ROOT / state["run_dir"]
    summary_path = run_dir / "context_diff.json"
    command = [
        sys.executable,
        "scripts/differ.py",
        "--current-run-dir",
        state["run_dir"],
        "--run-id",
        state["run_id"],
        "--run-date",
        state["run_date"],
        "--summary-json",
        rel(summary_path),
    ]
    if state.get("previous_run_dir"):
        command.extend(["--previous-run-dir", state["previous_run_dir"]])

    run_subprocess(command)
    if summary_path.exists():
        return json.loads(summary_path.read_text(encoding="utf-8"))
    return {}


def count_gaps(gap_analysis: Path) -> int:
    if not gap_analysis.exists():
        return 0
    text = gap_analysis.read_text(encoding="utf-8")
    total_match = re.search(r"Total gaps(?: this run)?:\s*\**(\d+)\**", text, re.IGNORECASE)
    if total_match:
        return int(total_match.group(1))
    ids = set(re.findall(r"\bGAP-\d+\b", text))
    return len(ids)


def extract_new_gaps(gap_analysis: Path) -> list[str]:
    if not gap_analysis.exists():
        return []
    text = gap_analysis.read_text(encoding="utf-8")
    sections = re.split(r"(?=^###\s+GAP-\d+)", text, flags=re.MULTILINE)
    gaps: list[str] = []
    for section in sections:
        heading = re.match(r"^###\s+(GAP-\d+)", section.strip())
        if not heading:
            continue
        status_match = re.search(r"\*\*Status:\*\*\s*([^\n]+)", section, re.IGNORECASE)
        if status_match and "NEW" in status_match.group(1).upper():
            description_match = re.search(r"\*\*Gap description:\*\*\s*([^\n]+)", section, re.IGNORECASE)
            description = clean_inline(description_match.group(1)) if description_match else "new gap"
            gaps.append(f"{heading.group(1)}: {description}")
    return gaps


def clean_inline(value: str) -> str:
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip(" -\n\t")


def extract_key_theme(state: dict[str, Any]) -> str:
    run_dir = ROOT / state["run_dir"]
    candidates = [
        run_dir / "gap_analysis.md",
        run_dir / "optimization_proposal.md",
        run_dir / "log_reflection.md",
    ]
    for path in candidates:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        audit_match = re.search(r"\*\*Audit summary:\*\*\s*([^\n]+)", text, re.IGNORECASE)
        if audit_match:
            return shorten_theme(clean_inline(audit_match.group(1)))
        for line in text.splitlines():
            line = clean_inline(line)
            if line and not line.startswith("#") and len(line) > 20:
                return shorten_theme(line)
    return "metadata and AI visibility audit"


def shorten_theme(value: str, max_chars: int = 96) -> str:
    value = value.strip().rstrip(".")
    if len(value) <= max_chars:
        return value
    cut = value[:max_chars].rsplit(" ", 1)[0]
    return cut.rstrip(" ,;:")


def load_context_diff(state: dict[str, Any]) -> dict[str, Any]:
    path = ROOT / state["run_dir"] / "context_diff.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        logging.warning("Could not parse %s", rel(path))
        return {}


def append_run_index(state: dict[str, Any], gaps_found: int, implemented_count: int, theme: str) -> bool:
    RUN_INDEX.parent.mkdir(parents=True, exist_ok=True)
    if RUN_INDEX.exists():
        text = RUN_INDEX.read_text(encoding="utf-8")
    else:
        text = (
            "# Run Index - append only, one line per run\n"
            "# Format: run_NNN | YYYY-MM-DD | N gaps found | N implemented since last run | key theme: [phrase]\n"
            "# ---\n"
        )

    if re.search(rf"^{re.escape(state['run_id'])}\s*\|", text, flags=re.MULTILINE):
        logging.info("%s already has an entry in %s; not appending a duplicate.", state["run_id"], rel(RUN_INDEX))
        return False

    line = (
        f"{state['run_id']} | {state['run_date']} | {gaps_found} gaps found | "
        f"{implemented_count} implemented since last run | key theme: {theme}"
    )
    if not text.endswith("\n"):
        text += "\n"
    RUN_INDEX.write_text(text + line + "\n", encoding="utf-8")
    logging.info("Appended %s", rel(RUN_INDEX))
    return True


def summarize_diff_item(item: dict[str, Any]) -> str:
    page = item.get("page") or item.get("url") or "unknown page"
    field = item.get("field") or "field"
    current = clean_inline(str(item.get("current_value") or item.get("current") or "updated"))
    return f"{page} - {field}: {shorten_theme(current, 120)}"


def update_implementation_log(state: dict[str, Any], diff: dict[str, Any], new_gaps: list[str]) -> bool:
    IMPLEMENTATION_LOG.parent.mkdir(parents=True, exist_ok=True)
    previous_id = state.get("previous_run_id") or "baseline"
    heading = f"### {previous_id} -> {state['run_id']} | {state['run_date']} (automated diff)"

    if IMPLEMENTATION_LOG.exists():
        text = IMPLEMENTATION_LOG.read_text(encoding="utf-8")
    else:
        text = (
            "# Implementation Log - Cumulative Diff Record\n\n"
            "Tracks what Radisson has implemented or left unchanged from each run's optimization proposal.\n\n"
            "## Log\n"
        )

    if heading in text:
        logging.info("%s already contains the automated diff heading; not appending a duplicate.", rel(IMPLEMENTATION_LOG))
        return False

    implemented = diff.get("implemented", [])
    unchanged = diff.get("unchanged", [])
    changed = diff.get("changed", [])
    missing_pages = diff.get("missing_pages", [])
    new_pages = diff.get("new_pages", [])

    lines = ["", heading, ""]
    if implemented:
        lines.append("**Implemented inferred from metadata diff:**")
        for item in implemented[:20]:
            lines.append(f"- {summarize_diff_item(item)}")
        if len(implemented) > 20:
            lines.append(f"- ... {len(implemented) - 20} additional implemented/changed fields")
    else:
        lines.append("**Implemented inferred from metadata diff:** ZERO confirmed.")

    lines.append("")
    if changed:
        lines.append("**Changed but not automatically classed as implemented:**")
        for item in changed[:20]:
            lines.append(f"- {summarize_diff_item(item)}")
        if len(changed) > 20:
            lines.append(f"- ... {len(changed) - 20} additional changed fields")
    else:
        lines.append("**Changed but not automatically classed as implemented:** None.")

    lines.append("")
    if unchanged:
        lines.append(f"**Unchanged:** {len(unchanged)} compared fields unchanged.")
        for item in unchanged[:12]:
            lines.append(f"- {summarize_diff_item(item)}")
        if len(unchanged) > 12:
            lines.append(f"- ... {len(unchanged) - 12} additional unchanged fields")
    else:
        lines.append("**Unchanged:** No comparable unchanged fields found.")

    if new_pages:
        lines.append("")
        lines.append("**New pages in current snapshot:**")
        for item in new_pages[:20]:
            lines.append(f"- {item}")

    if missing_pages:
        lines.append("")
        lines.append("**Pages missing from current snapshot:**")
        for item in missing_pages[:20]:
            lines.append(f"- {item}")

    lines.append("")
    if new_gaps:
        lines.append(f"**New gaps identified ({len(new_gaps)} detected from gap_analysis.md):**")
        for item in new_gaps[:30]:
            lines.append(f"- {item}")
        if len(new_gaps) > 30:
            lines.append(f"- ... {len(new_gaps) - 30} additional new gaps")
    else:
        lines.append("**New gaps identified:** None automatically detected from gap_analysis.md.")

    if not text.endswith("\n"):
        text += "\n"
    IMPLEMENTATION_LOG.write_text(text + "\n".join(lines) + "\n", encoding="utf-8")
    logging.info("Updated %s", rel(IMPLEMENTATION_LOG))
    return True


def finalize_run(state: dict[str, Any]) -> int:
    run_dir = ROOT / state["run_dir"]
    gap_analysis = run_dir / "gap_analysis.md"
    gaps_found = count_gaps(gap_analysis)
    diff = load_context_diff(state)
    implemented = diff.get("implemented", [])
    implemented_count = len(implemented)
    theme = extract_key_theme(state)
    new_gaps = extract_new_gaps(gap_analysis)

    append_run_index(state, gaps_found, implemented_count, theme)
    update_implementation_log(state, diff, new_gaps)

    state["metadata"]["gaps_found"] = gaps_found
    state["metadata"]["implemented_count"] = implemented_count
    append_completed(state, PHASE_4)
    state["status"] = "COMPLETED"
    state["completed_at"] = datetime.now().isoformat(timespec="seconds")
    completed_state_path = run_dir / "run_state_completed.json"
    completed_state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    if STATE_FILE.exists():
        STATE_FILE.unlink()
        logging.info("Cleared %s", rel(STATE_FILE))

    print()
    print("Run finalized.")
    print(f"- Run: {state['run_id']}")
    print(f"- Gaps found: {gaps_found}")
    print(f"- Implemented since last run: {implemented_count}")
    print(f"- Proposal: {state['run_dir']}/optimization_proposal.md")
    print(f"- Completed state: {rel(completed_state_path)}")
    return 0


def advance(args: argparse.Namespace) -> int:
    state = load_state()
    if not state:
        print("No active run. Start one with: python run.py --init")
        return 2
    if state.get("status") != "IN_PROGRESS":
        print(f"Active state is not in progress: {state.get('status')}")
        return 2

    phase = state["current_phase"]
    logging.info("Advancing %s from %s", state["run_id"], phase)

    missing = missing_required_files(state, phase)
    if missing:
        print("Cannot advance; required file outputs are missing or empty:")
        for path in missing:
            print(f"- {rel(path)}")
        print()
        print_phase_prompt(state, phase)
        return 2

    if phase == PHASE_0:
        scrape_summary = run_scraper(state, args.skip_scrape)
        diff_summary = run_differ(state)
        state["metadata"].update(
            {
                "target_urls_count": scrape_summary.get("target_urls_count", 0),
                "scraped_count": scrape_summary.get("scraped_count", 0),
                "blocked_count": scrape_summary.get("blocked_count", 0),
                "diff_rows": diff_summary.get("row_count", 0),
            }
        )
        append_completed(state, PHASE_0, PHASE_1)
        state["current_phase"] = PHASE_2
        save_state(state)
        print_phase_prompt(state, PHASE_2)
        return 0

    if phase == PHASE_2:
        state["metadata"]["gaps_found"] = count_gaps(ROOT / state["run_dir"] / "gap_analysis.md")
        append_completed(state, PHASE_2)
        state["current_phase"] = PHASE_2_5
        save_state(state)
        print_phase_prompt(state, PHASE_2_5)
        return 0

    if phase == PHASE_2_5:
        append_completed(state, PHASE_2_5)
        state["current_phase"] = PHASE_3
        save_state(state)
        print_phase_prompt(state, PHASE_3)
        return 0

    if phase == PHASE_3:
        append_completed(state, PHASE_3)
        state["current_phase"] = PHASE_4
        save_state(state)
        print_phase_prompt(state, PHASE_4)
        return 0

    if phase == PHASE_4:
        return finalize_run(state)

    print(f"Unknown current phase: {phase}")
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Radisson GEO Optimizer stateful runner.")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--init", action="store_true", help="Initialize the next run and print Phase 0 prompts.")
    action.add_argument("--status", action="store_true", help="Print active run state and remaining steps.")
    action.add_argument("--next", action="store_true", help="Validate the current phase and advance the run.")
    parser.add_argument(
        "--skip-scrape",
        action="store_true",
        help="With --next during Phase 0, generate mock snapshot outlines instead of live fetching.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.skip_scrape and not args.next:
        parser.error("--skip-scrape can only be used with --next")

    if args.init:
        return init_run()
    if args.status:
        return print_status()
    if args.next:
        return advance(args)
    parser.error("No action supplied")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
