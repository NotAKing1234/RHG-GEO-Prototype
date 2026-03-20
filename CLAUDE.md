# Section 1 — Project Overview
This repository runs a local-first GEO optimization workflow for Radisson Hotel Group. Its purpose is to help Radisson improve discoverability inside AI-driven travel discovery engines by researching fresh GEO and AEO best practices on every run, auditing Radisson's live web metadata, identifying structured gaps, researching each gap in depth, and producing prioritized optimization proposals for American bleisure travelers aged 25–55 traveling from the United States to Europe and increasingly using conversational AI systems as their primary hotel discovery interface.

# Section 2 — How to Run
Open this repository in Claude Code and either type `/geo-run` or say "run the pipeline". Claude Code should handle the workflow end to end by following the instructions in this file, including web research, website audit, gap analysis, sub-agent research, proposal generation, and memory updates.

# Section 3 — Pipeline Instructions
Use the following execution rules on every run:

- Always infer the current run number before doing any work.
- Always read `/memory/master_summary.md` and `/memory/run_index.md` at the start of every run.
- Compute `NNN` from the last line of `/memory/run_index.md` using zero-padded numbering. If no run lines exist, use `run_001`.
- Compute `RUN_DATE` using the local current date in `YYYY-MM-DD` format.
- Create the active run directory as `/runs/run_NNN_YYYY-MM-DD/` before writing outputs.
- When older instructions refer to `/runs/run_NNN/...`, interpret that as the active timestamped run directory `/runs/run_NNN_YYYY-MM-DD/...` for the current run.
- Write all current-run outputs into the active run directory and do not write current-run artifacts anywhere else unless a phase explicitly names another destination such as `/framework/`, `/literature/`, `/memory/`, or `/inferred/`.
- Report progress at the start of each phase with a one-line status update.
- Do not skip phases. Do not stop for confirmation between phases.

## PHASE 0 — LITERATURE REFRESH (every run, no exceptions)
This phase is mandatory on every run. Use Claude Code's web search tool to research the current GEO and AEO environment fresh. Do not rely on cached knowledge, prior run assumptions, or static engine lists. Always search the live web on each run before drafting criteria.

Research all of the following questions:

1. Which AI engines are currently dominant for travel and hotel discovery? Include any models or interfaces that have emerged recently. Do not hardcode a list; discover it fresh each run.
2. What signals do the currently dominant engines use to surface hotel results in conversational queries?
3. What are the current best-evidenced GEO and AEO practices specifically for the hospitality sector?
4. What metadata and content structures are hospitality leaders and OTAs such as Booking.com, Expedia, Marriott, and Hilton using to perform well in AI engine results?
5. What content patterns and query types does an American bleisure traveler aged 25–55, traveling from the US to Europe, use when searching via AI engines?

Output requirements:

- Write the literature findings to `/literature/run_NNN_sources.md`.
- Structure the literature file with dated findings, source links, synthesis notes, and a concise interpretation of what changed since the last run if such change is detectable.
- From the literature findings, synthesize a structured criteria framework and write it to `/framework/run_NNN_criteria.md`.
- The criteria file must list every specific, checkable GEO signal discovered in this run.
- Each criterion must include:
  - Criterion ID
  - Signal name
  - Why the signal matters for AI hotel discovery
  - What "passing" looks like on a hotel brand page
  - How the signal should be checked during the audit
  - Relevance to American bleisure traveler queries
- Do not leave the criteria abstract. Every criterion must be auditable against live pages.

## PHASE 1 — LOG REVIEW AND IMPLEMENTATION INFERENCE (skip on run_001, required for all subsequent runs)
If the current run is `run_001`, skip this phase and note `first run: no prior implementation history` in the later proposal fields that depend on historical inference.

If the current run is `run_002` or later:

1. Load these files:
   - `/memory/master_summary.md`
   - `/memory/run_index.md`
   - The two most recent `log_reflection.md` files from `/runs/`
2. Do not load full historical run folders automatically. Load only the reflection logs.
3. Identify the immediately previous run directory by run number and use its `metadata_snapshot.md` as the historical comparison baseline.
4. Fetch the current live metadata from the Radisson website for the pages being audited in the current run.
5. Diff the live metadata against the previous run's `metadata_snapshot.md`.

From the metadata diff alone, infer:

- Which recommendations from the last optimization proposal appear to have been implemented
- Which recommendations appear ignored or unchanged
- Which gaps have persisted across two or more consecutive runs

Write the output to `/runs/run_NNN_YYYY-MM-DD/context_brief.md`.

The context brief must include:

- Previous run used for comparison
- Summary of detected metadata changes
- Implemented recommendations inferred from the diff
- Unchanged recommendations inferred from the diff
- Persistent gaps now recurring for 2 or more runs
- Implications for scoring and prioritization in the current run

## PHASE 2 — AUDIT AND GAP ANALYSIS
Load the target pages from `/sources/website/target_urls.md`.

Audit rules:

- Audit every Priority 1 page on every run.
- Rotate one or two Priority 2 city pages across runs unless the user explicitly asks for all of them in the current run.
- Audit Priority 3 every other run unless the user explicitly asks for it in the current run.
- If a page is unavailable, note the fetch issue and continue with the rest of the audit.

For each audited page, fetch the live page and extract:

- Title tag
- Meta description
- Structured data and schema.org markup, including Hotel, LodgingBusiness, FAQPage, and related types
- Open Graph tags
- FAQ or Q&A blocks
- Heading structure across H1, H2, and H3
- Alt text on meaningful images
- Natural language query compatibility, especially whether the page can answer queries such as "hotels in London for American business travelers with meeting rooms"
- Entity signals establishing Radisson as a named brand with location, category, and service type

Score every page against:

- `/framework/run_NNN_criteria.md`
- `/runs/run_NNN_YYYY-MM-DD/context_brief.md` when it exists

Gap rules:

- Label a gap as `MISSING` when the signal is absent.
- Label a gap as `WEAK` when the signal exists but is underoptimized for AI engine parsing or retrieval.
- Label a gap as `MISALIGNED` when the signal exists but is framed incorrectly for American bleisure traveler queries.

Write `/runs/run_NNN_YYYY-MM-DD/metadata_snapshot.md` as the raw audit record for future diffing.

The metadata snapshot must capture, page by page:

- Page URL
- Fetch timestamp
- Extracted title
- Extracted meta description
- Structured data blocks or normalized summaries
- Open Graph fields
- Heading outline
- FAQ and Q&A presence
- Alt text observations
- Query compatibility notes
- Entity signal notes

Write `/runs/run_NNN_YYYY-MM-DD/gap_analysis.md`.

For every identified gap, include:

- Gap ID
- Page URL
- Criterion ID or signal name being evaluated
- Current metadata state
- Gap type: `MISSING`, `WEAK`, or `MISALIGNED`
- Gap description
- Severity score from 1 to 3
- Whether the gap appears new or recurring

If no gaps are found for a page, state that explicitly rather than omitting the page.

## PHASE 2.5 — TARGETED GAP RESEARCH (sub-agent)
After completing `gap_analysis.md`, spawn a focused sub-agent using the Task tool.

Sub-agent execution rules:

- The sub-agent must have web search access.
- The sub-agent must start with a fresh context window.
- The sub-agent must not inherit the main session context beyond the prompt text you generate.
- Generate the prompt dynamically using the actual audit findings from the current run.
- Include the real gap list and one-paragraph audit summary from the current run.

Use this prompt template and inject the live run data before sending:

```text
[WHO]
You are a specialist GEO/AEO researcher optimizing metadata for a major international hotel brand (Radisson Hotel Group). The target audience is American bleisure travelers aged 25–55 who are traveling from the US to Europe and increasingly use AI engines as their primary hotel discovery interface.

[WHAT]
Radisson's current website metadata has the following state:
{INJECT: one-paragraph summary from Phase 2 audit}

[GAP]
The following specific gaps were identified in this audit run:
{INJECT: numbered list of all gaps from gap_analysis.md, with page URL and gap type}

[GOAL]
For each gap listed above, find:
→ The current best practice for addressing this specific gap in travel/hospitality GEO
→ A concrete example of a competing brand or OTA that does this well (with evidence)
→ The specific metadata or content change that would close this gap
→ The directional impact this change would have for an American bleisure traveler using AI-assisted travel search

[FORMAT]
For each gap, structure your output as:
— Gap ID and description (from the list above)
— Best practice for closing it (with source citation)
— Competitor or OTA example doing this well
— Specific proposed fix (implementable, not vague)
— Directional impact for bleisure traveler discovery

[ASSESS]
→ Which gap is most urgent for AI engine visibility right now?
→ Which gap would deliver the fastest measurable improvement?
→ Are there any gaps where best practice is still actively contested or changing rapidly?
```

When the sub-agent returns:

- Write the complete sub-agent output to `/runs/run_NNN_YYYY-MM-DD/gap_research.md`.
- Preserve citations and examples from the sub-agent output.
- Do not summarize away the per-gap research detail; keep the full return intact.

## PHASE 3 — OPTIMIZATION PROPOSAL
Synthesize the proposal from these inputs:

1. `/framework/run_NNN_criteria.md`
2. `/runs/run_NNN_YYYY-MM-DD/gap_research.md`
3. `/runs/run_NNN_YYYY-MM-DD/context_brief.md` when available

Write `/runs/run_NNN_YYYY-MM-DD/optimization_proposal.md`.

Open the proposal with one executive-summary paragraph that states:

- Total number of gaps found
- How many gaps are new versus recurring
- The top 3 priority changes

For every gap, write exactly one proposal entry and keep the fields in this exact order:

1. **Proposed change** — the specific rewrite, new tag, structured data addition, or content addition
2. **Source citation** — the GEO criterion or research finding that justifies the change
3. **Current state** — what is present now
4. **Inferred implementation status** — whether Radisson acted on a similar recommendation in the prior run, or `N/A` on the first run
5. **Directional impact estimate** — the qualitative effect on discoverability for American bleisure travelers using AI-assisted travel search
6. **Priority tier** — `P1`, `P2`, or `P3`

Proposal rules:

- Put the proposed change first, before diagnosis.
- Make fixes implementable and concrete.
- Tie each recommendation back to current-run research or criteria.
- Prioritize speed to implementation and likely AI visibility impact.
- If best practice is contested, say so in the source citation or impact note rather than hiding uncertainty.

## PHASE 4 — LOG AND LEARN
Store all run outputs under the active timestamped run directory `/runs/run_NNN_YYYY-MM-DD/`.

Write `/runs/run_NNN_YYYY-MM-DD/log_reflection.md` answering:

- What gaps did I identify correctly versus miss compared to the last run?
- Did the targeted gap research in Phase 2.5 change or sharpen any proposals?
- What did the diff reveal about Radisson's implementation behavior?
- What should I weight differently in gap detection next run?
- What in my gap detection logic should change?

Then update cross-run memory:

1. Rewrite `/memory/master_summary.md`.
   - Read the current `master_summary.md`.
   - Read the just-completed `log_reflection.md`.
   - Merge them into an updated master summary.
   - Hard limit: 800 tokens maximum.
   - Compress older patterns when needed.
   - Recent signal wins when compressing.
2. Append one new line to `/memory/run_index.md` in this exact format:
   - `run_NNN | YYYY-MM-DD | N gaps found | N implemented since last run | key theme: [one phrase]`
3. Update `/inferred/implementation_log.md` with the Phase 1 diff summary:
   - What changed
   - What did not change
   - What new gaps appeared

Completion rules:

- Do not overwrite `run_index.md`; append only.
- Do not overwrite historical run folders.
- Do not load archive runs older than the two most recent reflections unless the user explicitly asks.
- End by reporting a compact run summary:
  - run number
  - total gaps found
  - top 3 priority recommendations
  - path to `optimization_proposal.md`

# Section 4 — Memory Rules
Memory loading rules are mandatory:

- Always load `/memory/master_summary.md` and `/memory/run_index.md` at the start of every run.
- Always load the two most recent `log_reflection.md` files from `/runs/`.
- Never load full run folders automatically.
- Never load archive runs older than two runs back unless the user explicitly requests a specific run ID.
- Keep the total context budget for memory loading to approximately 2,000 tokens maximum.

# Section 5 — Run Numbering
Infer the current run number from the last line of `/memory/run_index.md`.

- First run is `run_001`.
- Always zero-pad run numbers to three digits.
- If `run_index.md` has no run entries yet, use `run_001`.
- If the last recorded run is `run_00X`, increment it by one for the current run.
- Pair the run number with the local current date to form the active directory name `/runs/run_NNN_YYYY-MM-DD/`.
