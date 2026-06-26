# Radisson GEO Dashboard

Local dashboard for operating and reviewing the Radisson GEO Optimizer.

## Run locally

Terminal 1:

```bash
npm --prefix dashboard install
npm --prefix dashboard run backend
```

Terminal 2:

```bash
npm --prefix dashboard run dev -- --host 127.0.0.1
```

Open `http://127.0.0.1:5173`.

For a clean checkout, first build or provide the SQLite runtime database from the repository root:

```bash
python3 scripts/import_run_artifacts.py --json
python3 run.py --smoke --run-id run_005
```

The full local URL Registry database is `db/geo_optimizer.db`; it is ignored by Git and should be supplied separately when a client needs the exact saved link registry and run state.

## What it wraps

The dashboard calls the existing runner from the repository root:

- `python3 run.py --init`
- `python3 run.py --status`
- `python3 run.py --next`
- `python3 run.py --next --skip-scrape` for non-Phase 2 local dry-runs only

It reads existing artifacts from `runs/`, `memory/`, `framework/`, and `literature/`.
On import, those artifacts are normalized into SQLite so dashboard reads come from the DB.

Editable or generated operator inputs:

- SQLite `urls.selected_for_next_run` via the URL Registry / Radisson Links view.
- SQLite `dashboard_overrides` via proposal ticket drafting and team adjustments.
- SQLite `run_url_targets` when `python3 run.py --init` snapshots pending "Research Next" links for a run.
- `sources/website/run_targets/next_geo_run.csv` and `sources/website/target_urls.md` as generated compatibility views only.

The backend also exposes:

- `GET /api/dashboard/runs` for available run records.
- `GET /api/dashboard/data?run_id=...` for the DB-backed dashboard read model.
- `POST /api/dashboard/import` for re-importing historical run artifacts into SQLite.
- `PUT /api/dashboard/overrides` for saved proposal adjustments and Jira field edits.
- `GET /api/dashboard/export` for Jira CSV, clipboard, CSV, JSON, and full audit exports.
- `GET /api/url-registry` for registry filtering, cost estimates, and current next-run selection state.
- `POST /api/url-registry/selection` for saving explicit checked URLs or a bounded filtered subset.
