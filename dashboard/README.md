# Radisson GEO Dashboard

Local dashboard for operating and reviewing the Radisson GEO Optimizer.

## Run locally

Terminal 1:

```bash
cd dashboard
npm install
npm run backend
```

Terminal 2:

```bash
cd dashboard
npm run dev
```

Open `http://127.0.0.1:5173`.

## What it wraps

The dashboard calls the existing runner from the repository root:

- `python3 run.py --init`
- `python3 run.py --status`
- `python3 run.py --next`
- `python3 run.py --next --skip-scrape`

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
