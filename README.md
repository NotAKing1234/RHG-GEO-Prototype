# Radisson GEO Optimizer

Radisson GEO Optimizer is a local-first Claude Code project for auditing and improving Radisson Hotel Group's website discoverability inside AI-driven discovery engines. On each run it refreshes current GEO and AEO best practices, audits live Radisson metadata, analyzes gaps, researches each gap in more depth, and produces a prioritized optimization proposal tailored to American bleisure travelers traveling from the US to Europe.

## Why it exists

GEO is replacing traditional SEO for high-intent discovery workflows inside ChatGPT, Gemini, Perplexity, and similar interfaces. If Radisson's metadata, entity signals, and content structure are not legible to those engines, brand and hotel discovery shifts to better-structured competitors and OTAs. This repository exists to make that gap measurable and actionable.

## Setup

- Requires Claude Code.
- No API keys are needed for v1.
- Python stdlib is enough for the local runner and dashboard API.
- The pipeline is orchestrated by `CLAUDE.md` and initialized by `python3 run.py --init`.
- SQLite is the system of record. Markdown and CSV files are generated or imported views.

## How to run

Open this repository in Claude Code and type `/geo-run`.

Claude Code should execute the full pipeline defined in `CLAUDE.md`: literature refresh, audit, gap analysis, targeted sub-agent research, optimization proposal, and memory updates.

The dashboard's Radisson Links / URL Registry view controls the next run target set. When you save links as "Research Next", the selection is stored in SQLite. The next `/geo-run` calls `python3 run.py --init`, snapshots those pending links into `run_url_targets`, and uses that run-scoped snapshot for the audit.

**Compatibility note**
`sources/website/target_urls.md` and `sources/website/run_targets/next_geo_run.csv` are flat-file views for inspection and legacy tooling. Do not treat them as authority when SQLite is available.

## Folder structure

- `CLAUDE.md` - primary operating manual for the full GEO optimization pipeline.
- `README.md` - project overview, setup, and run instructions.
- `run.py` - DB-backed CLI entrypoint for initializing and advancing runs.
- `.claude/commands/geo-run.md` - slash command that triggers the end-to-end workflow in Claude Code.
- `memory/master_summary.md` - rolling compressed memory updated after each run.
- `memory/run_index.md` - append-only ledger of completed runs.
- `framework/` - stores run-specific GEO criteria documents generated from fresh literature research.
- `literature/` - stores run-specific source and synthesis notes gathered during literature refresh.
- `sources/website/target_urls.md` - generated compatibility view of known Radisson pages.
- `db/geo_optimizer.db` - local SQLite system of record for run data, source insights, dashboard overrides, Jira exports, and next-run URL selections.
- `sources/app/README.md` - placeholder for future mobile app metadata auditing.
- `runs/` - stores timestamped per-run artifacts such as snapshots, analyses, proposals, and reflections.
- `inferred/implementation_log.md` - cumulative record of what Radisson appears to have implemented between runs.



<!-- CHECKPOINT id="ckpt_mmywgfoh_5xc9a1" time="2026-03-20T12:53:06.017Z" note="auto" fixes=0 questions=0 highlights=0 sections="" -->
