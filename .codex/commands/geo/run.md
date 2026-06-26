# /geo/run

Run the Radisson GEO Optimizer workflow in this repo.

Follow the global Codex skill `geo-run` when it is installed and the repo workflow files:

- `.claude/commands/geo-run.md`
- `CLAUDE.md`
- `AGENTS.md`

Start new runs with:

```bash
python3 run.py --init
```

Use the run ID and run folder printed by `python3 run.py --init` for every later artifact.

## Authority

The Claude Code workflow in `.claude/commands/geo-run.md` and `CLAUDE.md` is the product workflow authority. This Codex command is the Codex-facing entrypoint for the same workflow, not a separate process.

Use SQLite `run_url_targets` for the active run as the authoritative target set. `sources/website/run_targets/next_geo_run.csv` and `sources/website/target_urls.md` are generated compatibility views only.

## Coverage Rules

- Audit every URL in the active run's SQLite `run_url_targets` snapshot.
- Do not sample selected links, stop after representative pages, or rely on grouped coverage before every selected URL has a page-level audit outcome.
- Process each selected link as fully as the site allows. If a page is blocked, unavailable, redirected, empty, rate-limited, timed out, or otherwise uninspectable, still record that URL in `metadata_snapshot.md` with the exact fetch status and notes.
- Before Phase 2 is complete, verify the selected DB target count equals the selected URLs represented in `metadata_snapshot.md`.
- `gap_analysis.md` must include URL-specific gaps or a per-URL coverage matrix mapping every selected URL to audit status and applicable gap IDs.
- Grouped recommendations are allowed only after every selected URL has a recorded audit outcome.

## Completion Rules

- Do not skip Phase 2.5 targeted gap research.
- Exports must use the active/current run ID, never a prior default.
- Every completed run must include a `ready-to-send/` bundle with Jira import CSVs, recommendation tracker, stakeholder draft, QA checklist, source/page/change CSVs, Jira validation report, and per-recommendation handoff files.
- Before reporting completion, run `python3 run.py --smoke --run-id <active_run_id>` and fix any failure.
- Append meaningful run/tool decisions, fixes, failures, verification notes, and follow-ups to `memory/execution_log.md`.
