# Codex Project Instructions

## Slash Alias: `/geo-run`

When Daniel types `/geo-run`, `slash geo run`, or asks Codex to run the GEO pipeline in this repo, treat it as a request to execute the workflow defined in:

- `.claude/commands/geo-run.md`
- `CLAUDE.md`

This is a Codex repo-level alias for the existing Claude Code command. The authoritative workflow still starts with:

```bash
python3 run.py --init
```

`run.py --init` snapshots the dashboard's saved "Research Next" URL selection from SQLite into `run_url_targets` for the new run. Use that run-scoped DB target set for Phase 2 auditing and research.

Do not treat `sources/website/run_targets/next_geo_run.csv` or `sources/website/target_urls.md` as the source of truth when SQLite is available. Those files are generated compatibility views.

## Execution Notes

- Follow all phases listed in `.claude/commands/geo-run.md`.
- Use the run ID and run folder printed by `python3 run.py --init`.
- Audit every URL snapshotted into SQLite `run_url_targets` for the active run. Do not sample selected links or stop after grouped representative coverage.
- Keep Phase 2 running until `metadata_snapshot.md` contains every selected URL, including blocked/unavailable URLs with exact fetch status.
- `gap_analysis.md` must include either URL-specific gaps or a per-URL coverage matrix mapping each selected URL to status and gap IDs before advancing.
- Do not skip Phase 2.5 gap research.
- Exports must use the active/current run ID, never a stale default such as a prior run. Verify generated export filenames and contents show the current run ID.
- Each completed run must include a `ready-to-send/` bundle inside the active run folder. It should contain the Jira import CSV, recommendation tracker, stakeholder email draft, QA checklist, source/page/change CSVs, `jira-validation-report.md`, and per-recommendation handoff files. Every ready recommendation folder must include a validated `jira-ticket.csv` with the exact Jira import columns.
- Before reporting a `/geo-run` complete, run `python3 run.py --smoke --run-id <active_run_id>` and treat any failure as blocking. These smoke checks cover the repeated repo complaints: all selected URLs audited, active-run exports, dashboard coverage counts, ready-to-send assets, per-item Jira CSV format, Phase 2.5 evidence links, and execution-log coverage.
- Keep current-run outputs inside the active timestamped run folder unless the workflow explicitly names another destination.
- Automatically append meaningful repo/tool discussions, decisions, fixes, failures, verification notes, and follow-ups to the local Execution Log at `memory/execution_log.md`; do not ask Daniel first.
