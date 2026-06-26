Execute the full GEO optimization pipeline for Radisson Hotel Group as defined in CLAUDE.md.

Before Phase 0, initialize the next run through the DB-backed runner:

```bash
python3 run.py --init
```

This snapshots the dashboard's pending "Research Next" URL selection from SQLite into `run_url_targets` for the new run. Treat that run-scoped DB target set as authoritative. The generated `sources/website/run_targets/next_geo_run.csv` and `sources/website/target_urls.md` files are compatibility views only.

Then proceed through all phases in order: Phase 0 → Phase 1 (if run 002+) → Phase 2 → Phase 2.5 (sub-agent) → Phase 3 → Phase 4.

Use the run ID and run folder printed by `python3 run.py --init`.
Load `memory/execution_log.md` when it exists, and append a new entry before completion for material repo/tool decisions, fixes, failures, verification results, and follow-ups. This is automatic local learning; do not ask for confirmation before logging.
Audit every URL snapshotted into SQLite `run_url_targets`; do not sample selected links or stop after representative/grouped coverage.
Before Phase 2 is considered complete, verify `metadata_snapshot.md` contains every selected URL, including blocked or unavailable pages with exact fetch status.
`gap_analysis.md` must either contain URL-specific gaps or a per-URL coverage matrix mapping every selected URL to status and applicable gap IDs.
Exports must use the active/current run ID and must not default to any older run.
Every completed run must generate a `ready-to-send/` bundle inside the active run folder, including the full Jira CSV, stakeholder email draft, QA checklist, source/page/change CSVs, `jira-validation-report.md`, and per-recommendation briefs, validated `jira-ticket.csv` files, handoff notes, acceptance checklists, and source evidence.
Before reporting completion, run `python3 run.py --smoke --run-id <active_run_id>` and fix any failure. This smoke gate captures the known failure modes Daniel has raised: incomplete selected-link coverage, stale run exports, broken dashboard coverage counts, missing ready-to-send assets, malformed per-item Jira CSVs, missing evidence links, and missing execution-log coverage.
Do not skip any phase. Do not ask for confirmation between phases — run the full pipeline to completion.
Report progress at the start of each phase with a one-line status message.
When complete, print a summary: run number, total gaps found, top 3 priority recommendations, and path to the optimization proposal.
