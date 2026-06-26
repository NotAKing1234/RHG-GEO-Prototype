# Dashboard Domain Contract

The dashboard follows one boundary: runs provide data; systems provide behavior.

Runs may supply normalized records such as pages, gaps, proposals, sources, proposal changes, and validation notes. Runs may not define dashboard categories, layouts, readiness rules, labels, handoff templates, smoke gates, or export eligibility.

## Stable Entities

- `run`: the run envelope and lifecycle state.
- `page`: an audited URL with page metadata and fetch/capture status.
- `gap`: a scored audit finding tied to a run and, when available, a page.
- `proposal`: a recommended change tied to a gap.
- `source`: evidence used by the run.
- `change`: the normalized implementation record for a proposal.
- `handoff_asset`: an exported file or Jira artifact generated from normalized records.
- `validation_warning`: a structured warning or error describing missing or malformed normalized data.

## Stable Rules

`scripts/dashboard_domain.py` owns product behavior:

- readiness and export eligibility
- coverage category labels and counts
- selector warning handling
- evidence requirements
- change surface labels
- generic stakeholder email priority copy
- validation warnings for missing or malformed normalized data

`scripts/dashboard_read_model.py` is an API adapter. It converts normalized DB rows into the current `/api/dashboard/data` payload shape and should not invent run-specific classifications.

`scripts/export.py` consumes the same domain readiness and copy rules as the dashboard. Ready-to-send tracker rows, bundle manifests, and dashboard `summary.ready_to_send` must agree.

`scripts/geo_run_smoke.py` verifies the generated artifacts against the same contract instead of reinterpreting run contents.

## Run Influence

Allowed run influence:

- record values such as URL, title, source excerpt, proposed change, current state, and imported Jira text
- normalized fields produced by import adapters, such as `change_type`, target page, and target field
- structured validation warnings for incomplete historical data

Disallowed run influence:

- dashboard tab layout, widget behavior, category labels, or visual grouping
- readiness rules or export eligibility
- stakeholder email template structure
- smoke-test pass/fail logic
- frontend parsing of proposal prose to infer behavior

## Adapter Placement

Historical Markdown and messy run formats are interpreted in `scripts/import_run_artifacts.py`. Current and future runs should normalize into SQLite fields before the dashboard, exports, or frontend see them.

If a future run introduces new wording, format quirks, or scenario-specific behavior, add or update an import adapter that maps that run data into the stable contract. Do not add that scenario logic to `dashboard/src/main.jsx`, `scripts/dashboard_read_model.py`, `scripts/export.py`, or smoke checks.
