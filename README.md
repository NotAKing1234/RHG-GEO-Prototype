# Radisson GEO Optimizer

Radisson GEO Optimizer is a local dashboard and workflow for auditing Radisson Hotel Group pages for GEO/AEO readiness. It helps review how well selected Radisson URLs expose the metadata, structured data, crawlability, and content signals that AI discovery engines can parse.

The project is prepared for both Claude Code and Codex. The same `/geo-run` workflow is available through Claude Code instructions and repo-local Codex command files.

## What This Includes

- A local dashboard for reviewing GEO recommendations, page coverage, sources, URL registry selections, and ready-to-send exports.
- A SQLite-backed run database at `db/geo_optimizer.db`.
- Completed run artifacts under `runs/`, including the latest handoff run `run_005`.
- Ready-to-send Jira CSVs, QA checklists, stakeholder notes, source evidence, and per-recommendation handoff folders.
- Codex and Claude Code workflow instructions for running future GEO audits.

## Requirements

- Python 3 with the standard library.
- Node.js and npm for the dashboard.
- The supplied GEO Optimizer database file, placed at `db/geo_optimizer.db`.
- Claude Code or Codex only if you want to run a new `/geo-run`; they are not required just to open the dashboard.

No API keys are required for reviewing the included dashboard and completed runs.

## Add The Supplied Database

The dashboard expects the SQLite database at this exact path:

```text
db/geo_optimizer.db
```

From the repository root:

```bash
mkdir -p db
cp /path/to/supplied/geo_optimizer.db db/geo_optimizer.db
```

If the database is supplied as a zip file:

```bash
mkdir -p db
unzip -p /path/to/geo_optimizer.db.zip > db/geo_optimizer.db
```

Replace any existing `db/geo_optimizer.db` with the supplied handoff database before starting the dashboard. The database file is intentionally not tracked by Git because it is runtime state.

At the time of handoff, the supplied database contains 58,094 URL rows, 5 runs, 595 run targets, 595 metadata snapshots, and 388 proposal-source links.

## Start The Dashboard

Run these commands from the repository root.

1. Install dashboard dependencies:

```bash
npm --prefix dashboard install
```

2. Verify the database and latest completed run:

```bash
python3 run.py --status
python3 run.py --smoke --run-id run_005
```

The smoke gate should report:

- 478 selected URLs represented in `run_005`
- 33 proposal-source links
- 8 ready-to-send Jira CSVs
- 51 ready-to-send manifest assets

3. Start the dashboard API in terminal 1:

```bash
npm --prefix dashboard run backend
```

4. Start the dashboard frontend in terminal 2:

```bash
npm --prefix dashboard run dev -- --host 127.0.0.1
```

5. Open the dashboard:

```text
http://127.0.0.1:5173/
```

Select `run_005 - 2026-06-26` from the run picker to review the latest completed handoff.

## If The Database Is Missing

If the supplied database file is not available, build a reduced read model from committed artifacts:

```bash
python3 scripts/import_run_artifacts.py --json
python3 run.py --smoke --run-id run_005
```

This fallback is enough to review completed runs and exports. It does not fully replace the supplied database for saved URL Registry state and dashboard selections.

## Running A New GEO Audit

Open this repository in Claude Code or Codex and type:

```text
/geo-run
```

In Codex, this explicit path is also available:

```text
/geo/run
```

The workflow starts with:

```bash
python3 run.py --init
```

This snapshots the dashboard's saved "Research Next" URL selection from SQLite into `run_url_targets` for the new run. That run-scoped SQLite target set is the source of truth for Phase 2 auditing.

Important run rule: every URL in SQLite `run_url_targets` must be processed as fully as the site allows. Do not sample, stop after representative pages, or group pages before every selected URL has a page-level audit outcome. Blocked, redirected, timed-out, empty, rate-limited, or otherwise unavailable pages still need an exact fetch status in `metadata_snapshot.md` and page coverage in `gap_analysis.md`.

Before reporting a run complete, run:

```bash
python3 run.py --smoke --run-id run_NNN
```

Fix any smoke failure before treating the run as send-ready.

## Claude Code And Codex Entrypoints

- `CLAUDE.md` - full workflow authority for Claude Code and the product pipeline.
- `.claude/commands/geo-run.md` - Claude Code slash command.
- `.codex/commands/geo-run.md` - Codex `/geo-run` alias.
- `.codex/commands/geo/run.md` - Codex `/geo/run` command.
- `AGENTS.md` - Codex repo-level instructions and `/geo-run` alias.

The Codex command files point back to the same workflow as Claude Code. They are included so GitHub checkouts retain the Codex-readable command surface.

## Key Project Paths

- `dashboard/` - local React dashboard and Python API server.
- `db/schema.sql` - SQLite schema.
- `db/geo_optimizer.db` - supplied runtime database path; not tracked by Git.
- `runs/` - timestamped run artifacts.
- `runs/run_005_2026-06-26/ready-to-send/` - latest handoff bundle.
- `framework/` - run-specific GEO criteria.
- `literature/` - run-specific research sources.
- `memory/execution_log.md` - local execution and verification log.
- `scripts/import_run_artifacts.py` - rebuilds dashboard read-model rows from committed artifacts.
- `scripts/geo_run_smoke.py` - completed-run smoke gate.
- `sources/website/target_urls.md` - generated compatibility view of known Radisson URLs.

Compatibility note: `sources/website/target_urls.md` and `sources/website/run_targets/next_geo_run.csv` are flat-file views for inspection and legacy tooling. When SQLite is available, `run_url_targets` is the authoritative per-run target list.
