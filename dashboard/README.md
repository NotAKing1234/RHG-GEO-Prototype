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

- `python run.py --init`
- `python run.py --status`
- `python run.py --next`
- `python run.py --next --skip-scrape`

It reads existing artifacts from `runs/`, `memory/`, `framework/`, and `literature/`. The only editable source in v1 is `sources/website/target_urls.md`.
