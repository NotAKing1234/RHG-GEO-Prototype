# Section 1 - Project Overview
This repository runs a local-first GEO/AEO optimization workflow for Radisson Hotel Group. Its purpose is to improve discoverability inside AI-driven travel discovery engines by researching current hotel discovery signals, auditing Radisson web metadata, identifying structured gaps, researching those gaps, and producing prioritized optimization proposals for American bleisure travelers aged 25-55 traveling from the United States to Europe.

# Section 2 - Agent-Agnostic Run Commands
The pipeline is orchestrated by `run.py`. It does not depend on Claude Code slash commands.

Start a new run:

```bash
python run.py --init
```

Check progress:

```bash
python run.py --status
```

Advance after completing the current phase output files:

```bash
python run.py --next
```

If Radisson live fetching is blocked and the run should continue with placeholder snapshot outlines:

```bash
python run.py --next --skip-scrape
```

`run.py --init` detects the next zero-padded run number from `memory/run_index.md`, creates `runs/run_NNN_YYYY-MM-DD/`, writes `runs/active_run.json`, and prints the Phase 0 prompt. Each later `--next` validates the expected files, runs the automated helper scripts when needed, updates state, and prints the next agent prompt.

# Section 3 - State and Outputs
Active state is stored in `runs/active_run.json` and is intentionally gitignored. A completed copy is saved to the run directory as `run_state_completed.json` when Phase 4 finalizes.

Run outputs are stored in:

- `literature/run_NNN_sources.md`
- `framework/run_NNN_criteria.md`
- `runs/run_NNN_YYYY-MM-DD/metadata_snapshot.md`
- `runs/run_NNN_YYYY-MM-DD/context_brief.md`
- `runs/run_NNN_YYYY-MM-DD/gap_analysis.md`
- `runs/run_NNN_YYYY-MM-DD/gap_research.md`
- `runs/run_NNN_YYYY-MM-DD/optimization_proposal.md`
- `runs/run_NNN_YYYY-MM-DD/log_reflection.md`

Cross-run memory is stored in:

- `memory/master_summary.md`
- `memory/run_index.md`
- `inferred/implementation_log.md`

# Section 4 - Phase Workflow
## Phase 0 - Literature Refresh
Run command:

```bash
python run.py --init
```

The active agent must use live web research, not cached assumptions, to answer:

1. Which AI engines are currently dominant for travel and hotel discovery?
2. What signals do dominant engines use to surface hotel results?
3. What are current best-evidenced GEO/AEO practices for hospitality?
4. What metadata and content structures do hospitality leaders and OTAs use?
5. What content patterns and query types does the target American bleisure traveler use?

Write:

- `literature/run_NNN_sources.md`
- `framework/run_NNN_criteria.md`

Then run:

```bash
python run.py --next
```

Phase 0 `--next` automatically runs:

- `scripts/scraper.py` to create `metadata_snapshot.md`
- `scripts/differ.py` to create `context_brief.md`

Use `python run.py --next --skip-scrape` if direct fetching and configured proxies are blocked.

## Phase 1 - Context Brief
This phase is automated by `run.py` after Phase 0 validation. It compares the current metadata snapshot against the previous run's `metadata_snapshot.md` and writes:

- `runs/run_NNN_YYYY-MM-DD/context_brief.md`

The context brief includes a prefilled comparison table, inferred implemented changes, unchanged fields, new pages, missing pages, and scoring implications.

## Phase 2 - Audit and Gap Analysis
Use:

- `framework/run_NNN_criteria.md`
- `runs/run_NNN_YYYY-MM-DD/metadata_snapshot.md`
- `runs/run_NNN_YYYY-MM-DD/context_brief.md`

Audit every target page in the snapshot. Label each gap as:

- `MISSING` when the signal is absent
- `WEAK` when the signal exists but is underoptimized
- `MISALIGNED` when the signal exists but is framed incorrectly for American bleisure traveler queries

Write:

- `runs/run_NNN_YYYY-MM-DD/gap_analysis.md`

Every gap must include gap ID, page URL, criterion or signal, current metadata state, gap type, description, severity 1-3, and new/recurring status. If no gaps are found for a page, state that explicitly.

Then run:

```bash
python run.py --next
```

## Phase 2.5 - Targeted Gap Research
Use a fresh web-capable research pass focused on the actual gap list from `gap_analysis.md`.

For each gap, find:

- Current best practice for addressing it in hospitality GEO/AEO
- A concrete competitor or OTA example
- The specific metadata or content change that would close the gap
- Directional impact for American bleisure traveler discovery

Write:

- `runs/run_NNN_YYYY-MM-DD/gap_research.md`

Then run:

```bash
python run.py --next
```

## Phase 3 - Optimization Proposal
Synthesize the proposal from:

- `framework/run_NNN_criteria.md`
- `runs/run_NNN_YYYY-MM-DD/gap_research.md`
- `runs/run_NNN_YYYY-MM-DD/context_brief.md`

Write:

- `runs/run_NNN_YYYY-MM-DD/optimization_proposal.md`

Open with one executive-summary paragraph stating total gaps found, new versus recurring gaps, and the top three priority changes.

For every gap, write exactly one proposal entry in this order:

1. **Proposed change** - specific rewrite, tag, structured data addition, or content addition
2. **Source citation** - criterion or research finding
3. **Current state** - what is present now
4. **Inferred implementation status** - whether Radisson acted on a similar prior recommendation, or `N/A` on the first run
5. **Directional impact estimate** - qualitative discovery effect
6. **Priority tier** - `P1`, `P2`, or `P3`
7. **Jira ticket fields** - a Jira-ready subsection that can convert to CSV

The **Jira ticket fields** subsection is mandatory for every proposal on every GEO optimizer run. Use these Jira import fields exactly:

- `Issue Type`
- `Epic Name`
- `Summary`
- `Description`
- `Priority`
- `Labels`
- `Component`
- `Acceptance Criteria`

Treat `Summary` as the ticket name/title for Jira import.

Group the `Description` content under:

- `Dev change specs`
- `SEO/GEO rationale`
- `GEO visibility score`
- `Validation steps`

Acceptance Criteria must be concrete, testable, and implementation-facing. If a value cannot be determined from run evidence, write a `[NEEDED: ...]` placeholder instead of guessing.

Then run:

```bash
python run.py --next
```

## Phase 4 - Log and Learn
Write:

- `runs/run_NNN_YYYY-MM-DD/log_reflection.md`
- Updated `memory/master_summary.md` under 800 tokens

The reflection should answer:

- What gaps were identified correctly versus missed compared to the last run?
- Did targeted gap research change or sharpen proposals?
- What did the diff reveal about implementation behavior?
- What should be weighted differently in gap detection next run?
- What detection logic should change?

Then run:

```bash
python run.py --next
```

The final `--next` call automatically:

- Appends `memory/run_index.md` in the ledger format
- Updates `inferred/implementation_log.md` from the diff and current gap analysis
- Saves `run_state_completed.json`
- Removes `runs/active_run.json`

# Section 5 - Helper Scripts
Scraper:

```bash
python3 scripts/scraper.py --run-dir runs/run_NNN_YYYY-MM-DD --run-id run_NNN --run-date YYYY-MM-DD
```

The runner passes the active target file to the scraper. If `sources/website/run_targets/next_geo_run.csv` has data rows, `run.py --next` uses that selected subset; otherwise it uses `sources/website/target_urls.md`. The scraper supports ZenRows via `ZENROWS_API_KEY`, supports ScrapingBee via `SCRAPINGBEE_API_KEY`, falls back to direct HTTP with rotating headers, delays between live target fetches, extracts page metadata with BeautifulSoup when available, and writes `metadata_snapshot.md`.

Differ:

```bash
python3 scripts/differ.py --current-run-dir runs/run_NNN_YYYY-MM-DD --run-id run_NNN --run-date YYYY-MM-DD
```

The differ compares the current snapshot with the previous numbered run and writes `context_brief.md`.

# Section 6 - Memory Rules
- Always start with `python run.py --init` unless resuming an active run.
- Use `python run.py --status` before continuing an unfamiliar active run.
- Do not overwrite historical run folders.
- Do not overwrite `memory/run_index.md`; finalization appends only.
- Do not load full historical run folders automatically. Use the current run, `memory/master_summary.md`, `memory/run_index.md`, and the two most recent `log_reflection.md` files unless a specific older run is requested.
- When older notes refer to `/runs/run_NNN/...`, interpret that as the timestamped directory `/runs/run_NNN_YYYY-MM-DD/...`.
