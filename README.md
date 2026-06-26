# Radisson GEO Optimizer

Radisson GEO Optimizer is a local-first Claude Code and Codex project for auditing and improving Radisson Hotel Group's website discoverability inside AI-driven discovery engines. On each run it refreshes current GEO and AEO best practices, audits live Radisson metadata, analyzes gaps, researches each gap in more depth, and produces a prioritized optimization proposal tailored to American bleisure travelers traveling from the US to Europe.

## Why it exists

GEO is replacing traditional SEO for high-intent discovery workflows inside ChatGPT, Gemini, Perplexity, and similar interfaces. If Radisson's metadata, entity signals, and content structure are not legible to those engines, brand and hotel discovery shifts to better-structured competitors and OTAs. This repository exists to make that gap measurable and actionable.

## Setup

- Supports Claude Code and Codex.
- No API keys are needed for v1.
- Python stdlib is enough for the local runner and dashboard API.
- Node.js/npm are needed for the dashboard frontend.
- The pipeline is orchestrated by `CLAUDE.md` and initialized by `python3 run.py --init`.
- Codex entrypoints live at `.codex/commands/geo-run.md`, `.codex/commands/geo/run.md`, and `AGENTS.md`.
- SQLite is the system of record. Markdown and CSV files are generated or imported views.

## Client quickstart

Use this path when you receive the repository plus the separate GEO Optimizer SQLite database file.

1. Clone or unzip the repository.

2. Place the supplied database file at the repo root path below. The file name must be exactly `geo_optimizer.db`.

```bash
mkdir -p db
cp /path/to/supplied/geo_optimizer.db db/geo_optimizer.db
```

If a file already exists at `db/geo_optimizer.db`, replace it with the supplied handoff database before starting the dashboard. The database is intentionally ignored by Git because it is runtime state.

3. Install dashboard dependencies from the repository root.

```bash
npm --prefix dashboard install
```

4. Verify the database and latest completed run.

```bash
python3 run.py --status
python3 run.py --smoke --run-id run_005
```

The smoke gate should report 478 selected URLs, 33 proposal-source links, 8 ready-to-send Jira CSVs, and 51 manifest assets for `run_005`.

5. Start the dashboard. Use two terminals from the repository root.

Terminal 1:

```bash
npm --prefix dashboard run backend
```

Terminal 2:

```bash
npm --prefix dashboard run dev -- --host 127.0.0.1
```

6. Open the dashboard at `http://127.0.0.1:5173/` and select `run_005 - 2026-06-26` from the run picker.

If the supplied database file is not available, build a reduced local read model from committed artifacts instead:

```bash
python3 scripts/import_run_artifacts.py --json
python3 run.py --smoke --run-id run_005
```

This fallback is enough to review completed runs and exports. It does not replace the supplied database for the full saved URL Registry state.

The supplied SQLite database belongs at `db/geo_optimizer.db`. At the time of handoff it contains the full URL Registry and run state used during development: 58,094 URL rows, 5 runs, 595 run targets, 595 metadata snapshots, and 388 proposal-source links.

## How to run

Open this repository in Claude Code or Codex and type `/geo-run`. In Codex, `/geo/run` is also available as the explicit slash-command path.

Claude Code and Codex should execute the same workflow defined in `CLAUDE.md`, `.claude/commands/geo-run.md`, and the Codex command shims under `.codex/commands/`: literature refresh, audit, gap analysis, targeted sub-agent research, optimization proposal, exports, smoke checks, and memory updates.

The dashboard's Radisson Links / URL Registry view controls the next run target set. When you save links as "Research Next", the selection is stored in SQLite. The next `/geo-run` calls `python3 run.py --init`, snapshots those pending links into `run_url_targets`, and uses that run-scoped snapshot for the audit.

For both Claude Code and Codex, the selected target snapshot is a complete workload. Every URL in SQLite `run_url_targets` must be processed as fully as the site allows. Do not sample, stop after representative pages, or group pages before every selected URL has a page-level audit outcome. If a page is blocked, unavailable, redirected, empty, rate-limited, timed out, or otherwise uninspectable, it still must appear in `metadata_snapshot.md` with the exact fetch status and notes, and `gap_analysis.md` must include URL-specific gaps or a per-URL coverage matrix.

If the local SQLite database is rebuilt and the URL Registry shows only the small seed set, import the validated sitemap crawl registry before using Radisson Links:

```bash
python3 scripts/import_url_registry.py --historical --json
```

The importer preserves any pending "Research Next" selections by default and loads crawl metadata used by dashboard filters: brand, region, country, locale, page type, content group, location confidence, location source, and sitemap provenance.

Before treating a completed run as send-ready, run the repo smoke gate:

```bash
python3 run.py --smoke --run-id run_NNN
```

The smoke gate checks the known historical failure modes: every selected URL has a metadata snapshot, exports use the requested run ID, dashboard coverage totals are coherent, `ready-to-send/` has the required assets, each ready recommendation has a valid `jira-ticket.csv`, Phase 2.5 evidence links exist, and `memory/execution_log.md` mentions the run.

**Compatibility note**
`sources/website/target_urls.md` and `sources/website/run_targets/next_geo_run.csv` are flat-file views for inspection and legacy tooling. Do not treat them as authority when SQLite is available.

## Folder structure

- `CLAUDE.md` - primary operating manual for the full GEO optimization pipeline.
- `README.md` - project overview, setup, and run instructions.
- `run.py` - DB-backed CLI entrypoint for initializing and advancing runs.
- `scripts/geo_run_smoke.py` - completed-run smoke gate for known `/geo-run` failure modes.
- `.claude/commands/geo-run.md` - slash command that triggers the end-to-end workflow in Claude Code.
- `.codex/commands/geo-run.md` and `.codex/commands/geo/run.md` - Codex slash-command entrypoints for the same workflow.
- `AGENTS.md` - Codex repo-level operating instructions and `/geo-run` alias.
- `memory/master_summary.md` - rolling compressed memory updated after each run.
- `memory/execution_log.md` - local automatic log of repo/tool decisions, fixes, failures, verification, and follow-ups.
- `memory/run_index.md` - append-only ledger of completed runs.
- `framework/` - stores run-specific GEO criteria documents generated from fresh literature research.
- `literature/` - stores run-specific source and synthesis notes gathered during literature refresh.
- `sources/website/target_urls.md` - generated compatibility view of known Radisson pages.
- `db/geo_optimizer.db` - local SQLite system of record for run data, source insights, dashboard overrides, Jira exports, and next-run URL selections.
- `sources/app/README.md` - placeholder for future mobile app metadata auditing.
- `runs/` - stores timestamped per-run artifacts such as snapshots, analyses, proposals, and reflections.
- `runs/run_NNN_YYYY-MM-DD/ready-to-send/` - generated handoff bundle for each completed run, including Jira import assets, stakeholder notes, QA checklist, Jira validation report, source/page/change CSVs, and per-recommendation files.
- `inferred/implementation_log.md` - cumulative record of what Radisson appears to have implemented between runs.



<!-- CHECKPOINT id="ckpt_mmywgfoh_5xc9a1" time="2026-03-20T12:53:06.017Z" note="auto" fixes=0 questions=0 highlights=0 sections="" -->
