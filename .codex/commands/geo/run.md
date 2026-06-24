# /geo/run

Run the Radisson GEO Optimizer workflow in this repo.

Follow the global Codex skill `geo-run` and the repo workflow files:

- `.claude/commands/geo-run.md`
- `CLAUDE.md`

Start new runs with:

```bash
python3 run.py --init
```

Use SQLite `run_url_targets` for the active run as the authoritative target set. `sources/website/run_targets/next_geo_run.csv` is a generated compatibility view only.
