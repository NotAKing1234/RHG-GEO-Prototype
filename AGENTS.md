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
- Do not skip Phase 2.5 gap research.
- Keep current-run outputs inside the active timestamped run folder unless the workflow explicitly names another destination.
