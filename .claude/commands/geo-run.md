Execute the full GEO optimization pipeline for Radisson Hotel Group as defined in CLAUDE.md.

Start with `python3 run.py --init`, then proceed through all phases in order with `python3 run.py --next`: Phase 0 → Phase 1 (if run 002+) → Phase 2 → Phase 2.5 (sub-agent) → Phase 3 → Phase 4.

Use the run number and run folder created by `run.py`; it infers the next run from `/memory/run_index.md`.
Do not skip any phase. Do not ask for confirmation between phases — run the full pipeline to completion.
Report progress at the start of each phase with a one-line status message.
When complete, print a summary: run number, total gaps found, top 3 priority recommendations, and path to the optimization proposal.
