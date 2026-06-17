# Radisson GEO Optimizer

Radisson GEO Optimizer is a local-first Claude Code project for auditing and improving Radisson Hotel Group's website discoverability inside AI-driven discovery engines. On each run it refreshes current GEO and AEO best practices, audits live Radisson metadata, analyzes gaps, researches each gap in more depth, and produces a prioritized optimization proposal tailored to American bleisure travelers traveling from the US to Europe.

## Why it exists

GEO is replacing traditional SEO for high-intent discovery workflows inside ChatGPT, Gemini, Perplexity, and similar interfaces. If Radisson's metadata, entity signals, and content structure are not legible to those engines, brand and hotel discovery shifts to better-structured competitors and OTAs. This repository exists to make that gap measurable and actionable.

## Setup

- Requires Claude Code.
- Python 3 is required for the runner and crawl scripts.
- Install Python scraper dependencies with `python3 -m pip install -r requirements.txt`.
- Install dashboard dependencies with `npm --prefix dashboard install`.
- No API keys are required for the default local flow. Optional live scraping providers use `ZENROWS_API_KEY` or `SCRAPINGBEE_API_KEY`.
- `run.py` is the stateful local runner; `CLAUDE.md` defines the operating procedure and phase prompts.

## How to run

Open this repository in Claude Code and type `/geo-run`.

Claude Code should execute the full pipeline defined in `CLAUDE.md`: literature refresh, audit, gap analysis, targeted sub-agent research, optimization proposal, and memory updates.

The same pipeline state can be operated directly:

```bash
python3 run.py --init
python3 run.py --status
python3 run.py --next
```

## Local dashboard

A local operator dashboard is available in `dashboard/`. It wraps the existing `run.py` workflow, displays run status and artifacts, summarizes historical gaps/proposals, exposes the URL registry, and lets you edit `sources/website/target_urls.md` or save a filtered next-run subset to `sources/website/run_targets/next_geo_run.csv`.

### Option 1: Running from the repository root (Recommended)

You can run the dashboard directly from the root of the repository without changing directories.

1. **Install frontend dependencies** (first time only):
   ```bash
   npm --prefix dashboard install
   ```

2. **Start the API backend**:
   ```bash
   python3 dashboard/server.py
   ```
   *(Alternatively: `npm --prefix dashboard run backend`)*

3. **Start the frontend** in a second terminal:
   ```bash
   npm --prefix dashboard run dev
   ```

4. **Access the dashboard**:
   Open [http://127.0.0.1:5173](http://127.0.0.1:5173) in your browser.

### Option 2: Running from the `dashboard/` directory

1. **Navigate and install dependencies** (first time only):
   ```bash
   cd dashboard
   npm install
   ```

2. **Start the API backend**:
   ```bash
   npm run backend
   ```

3. **Start the frontend** in a second terminal:
   ```bash
   npm run dev
   ```

4. **Access the dashboard**:
   Open [http://127.0.0.1:5173](http://127.0.0.1:5173) in your browser.



**IMPORTANT**
`sources/website/target_urls.md` contains the canonical Radisson URL inventory researched by the optimizer. Refresh it from the crawl output when Radisson sitemap coverage changes.

If `sources/website/run_targets/next_geo_run.csv` contains at least one data row, `run.py --next` uses that CSV as the active scrape target subset. If it is missing or header-only, the runner falls back to `sources/website/target_urls.md`.

## Radisson crawl inventory

A sitemap-derived Radisson URL inventory can be generated and validated with:

```bash
python3 scripts/radisson_crawl.py
python3 scripts/ingest_radisson_crawl.py
```

The latest machine-readable crawl deliverables are written to `sources/website/radisson_crawl/latest/`, including `radisson_url_index.jsonl`, `radisson_url_index.csv`, `crawl_manifest.json`, `crawl_exclusions.csv`, and `geo_optimizer_ingestion.json`.

To make the generated inventory the canonical optimizer target file, run:

```bash
python3 scripts/ingest_radisson_crawl.py --activate-targets
```

That command backs up the existing `sources/website/target_urls.md` before replacing it with all discovered Radisson target URLs.

The current crawl inventory is sitemap-derived and may be `ready_with_known_gaps` until all customer-facing sitemaps are fetched and origin page metadata is verified from an approved environment.

## Folder structure

- `CLAUDE.md` - primary operating manual for the full GEO optimization pipeline.
- `README.md` - project overview, setup, and run instructions.
- `run.py` - stateful CLI entrypoint for local GEO optimizer runs.
- `.claude/commands/geo-run.md` - slash command that triggers the end-to-end workflow in Claude Code.
- `memory/master_summary.md` - rolling compressed memory updated after each run.
- `memory/run_index.md` - append-only ledger of completed runs.
- `framework/` - stores run-specific GEO criteria documents generated from fresh literature research.
- `literature/` - stores run-specific source and synthesis notes gathered during literature refresh.
- `sources/website/target_urls.md` - canonical list of Radisson pages to audit.
- `sources/website/radisson_url_registry.csv` - machine-readable registry derived from the Radisson crawl.
- `sources/website/run_targets/next_geo_run.csv` - optional selected subset used by `run.py --next` when it has data rows.
- `sources/app/README.md` - placeholder for future mobile app metadata auditing.
- `runs/` - stores timestamped per-run artifacts such as snapshots, analyses, proposals, and reflections.
- `inferred/implementation_log.md` - cumulative record of what Radisson appears to have implemented between runs.



<!-- CHECKPOINT id="ckpt_mmywgfoh_5xc9a1" time="2026-03-20T12:53:06.017Z" note="auto" fixes=0 questions=0 highlights=0 sections="" -->
