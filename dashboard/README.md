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

Editable or generated operator inputs:

- `sources/website/target_urls.md` via the target editor.
- `sources/website/radisson_url_registry.csv` via the URL Registry view.
- `sources/website/run_targets/next_geo_run.csv` when a URL Registry selection is saved for the next run. The runner uses this selection only when it has rows and is newer than `target_urls.md`.

The backend also exposes:

- `GET /api/url-registry` for registry filtering, cost estimates, and current next-run selection state.
- `POST /api/url-registry/selection` for saving explicit checked URLs or a bounded filtered subset.
