Execute the full GEO optimization pipeline for Radisson Hotel Group as defined in CLAUDE.md.

Before Phase 0, initialize the next run through the DB-backed runner:

```bash
python3 run.py --init
```

This snapshots the dashboard's pending "Research Next" URL selection from SQLite into `run_url_targets` for the new run. Treat that run-scoped DB target set as authoritative. The generated `sources/website/run_targets/next_geo_run.csv` and `sources/website/target_urls.md` files are compatibility views only.

Then proceed through all phases in order: Phase 0 → Phase 1 (if run 002+) → Phase 2 → Phase 2.5 (sub-agent) → Phase 3 → Phase 4.

Use the run ID and run folder printed by `python3 run.py --init`.
Do not skip any phase. Do not ask for confirmation between phases — run the full pipeline to completion.
Report progress at the start of each phase with a one-line status message.
When complete, print a summary: run number, total gaps found, top 3 priority recommendations, and path to the optimization proposal.
