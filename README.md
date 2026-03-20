# Radisson GEO Optimizer

Radisson GEO Optimizer is a local-first Claude Code project for auditing and improving Radisson Hotel Group's website discoverability inside AI-driven discovery engines. On each run it refreshes current GEO and AEO best practices, audits live Radisson metadata, analyzes gaps, researches each gap in more depth, and produces a prioritized optimization proposal tailored to American bleisure travelers traveling from the US to Europe.

## Why it exists

GEO is replacing traditional SEO for high-intent discovery workflows inside ChatGPT, Gemini, Perplexity, and similar interfaces. If Radisson's metadata, entity signals, and content structure are not legible to those engines, brand and hotel discovery shifts to better-structured competitors and OTAs. This repository exists to make that gap measurable and actionable.

## Setup

- Requires Claude Code.
- No API keys are needed for v1 (the current version).
- No dependencies need to be installed.
- The pipeline is orchestrated by `CLAUDE.md`; `run.py` is only a future automation stub.

## How to run

Open this repository in Claude Code and type `/geo-run`.

Claude Code should execute the full pipeline defined in `CLAUDE.md`: literature refresh, audit, gap analysis, targeted sub-agent research, optimization proposal, and memory updates.


**IMPORTANT**
`sources/website/target_urls.md` contains all of the links that are researched. Please update this with all relevant links to ensure the suggestions are targeted for the appropriate sites! Current links are placeholders!

## Folder structure

- `CLAUDE.md` - primary operating manual for the full GEO optimization pipeline.
- `README.md` - project overview, setup, and run instructions.
- `run.py` - future CLI entrypoint for API-based automation; currently a stub.
- `.claude/commands/geo-run.md` - slash command that triggers the end-to-end workflow in Claude Code.
- `memory/master_summary.md` - rolling compressed memory updated after each run.
- `memory/run_index.md` - append-only ledger of completed runs.
- `framework/` - stores run-specific GEO criteria documents generated from fresh literature research.
- `literature/` - stores run-specific source and synthesis notes gathered during literature refresh.
- `sources/website/target_urls.md` - canonical list of Radisson pages to audit.
- `sources/app/README.md` - placeholder for future mobile app metadata auditing.
- `runs/` - stores timestamped per-run artifacts such as snapshots, analyses, proposals, and reflections.
- `inferred/implementation_log.md` - cumulative record of what Radisson appears to have implemented between runs.

## Upgrade path

### Stage 1: Claude Code workflow
The current version is intentionally local and instruction-driven. Claude Code performs the research, auditing, reasoning, and file writing directly from `CLAUDE.md`, which keeps the system fast to start and easy to iterate.

### Stage 2: `run.py` plus API automation
The next step is to move the orchestration logic into `run.py` using API calls for web retrieval, page parsing, and structured proposal generation. At that point the repository can preserve the same folder conventions while making runs repeatable outside the Claude Code UI.

### Stage 3: MCP server
The longer-term path is an MCP-backed service that exposes run orchestration, memory access, auditing tools, and reporting as callable capabilities. That would make the optimizer easier to schedule, integrate, and operate as a shared system rather than a local-only workflow.

## Future app audit scope

The `/sources/app/` folder is a placeholder for future Radisson app metadata auditing. When activated, it will expand this workflow beyond the website to cover app store listings, deep-link structure, and app-specific discoverability signals.
