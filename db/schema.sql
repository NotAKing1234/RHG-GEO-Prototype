-- Radisson GEO Optimizer V1.1 SQLite schema.
-- This file is the local system-of-record contract; markdown and CSV files are generated views.

PRAGMA foreign_keys = ON;

-- runs: the run envelope. In: one row per run. Pitfall: stops cross-run data bleed.
CREATE TABLE IF NOT EXISTS runs (
    run_id          TEXT PRIMARY KEY,
    run_number      INTEGER NOT NULL,
    run_date        TEXT NOT NULL,
    status          TEXT NOT NULL,
    previous_run_id TEXT REFERENCES runs(run_id)
);

-- urls: the managed Radisson registry. In: crawl + dashboard edits. Pitfall: selection is a column here.
CREATE TABLE IF NOT EXISTS urls (
    url_id                INTEGER PRIMARY KEY,
    url                   TEXT NOT NULL UNIQUE,
    brand                 TEXT,
    region                TEXT,
    country               TEXT,
    locale                TEXT,
    page_type             TEXT,
    content_group         TEXT,
    location_confidence   TEXT,
    location_source       TEXT,
    source_sitemap        TEXT,
    selected_for_next_run INTEGER NOT NULL DEFAULT 0,
    selected_at           TEXT,
    last_audited_run      TEXT REFERENCES runs(run_id)
);

-- sources: the artifact consulted. In: URL / competitor / OTA / literature refs.
-- Pitfall: keeps "where it came from" separate from "what it said".
CREATE TABLE IF NOT EXISTS sources (
    source_id   INTEGER PRIMARY KEY,
    run_id      TEXT NOT NULL REFERENCES runs(run_id),
    source_key  TEXT,
    url         TEXT,
    domain      TEXT,
    title       TEXT,
    source_type TEXT NOT NULL,
    headline    TEXT,
    finding_group TEXT,
    full_excerpt TEXT,
    ai_assessment_prose TEXT,
    scorecard_json TEXT,
    related_criteria_json TEXT,
    related_gaps_json TEXT,
    related_recommendations_json TEXT,
    credibility REAL NOT NULL DEFAULT 1.0,
    fetched_at  TEXT,
    UNIQUE(run_id, source_key)
);

-- source_insights: one insight pulled from one source.
-- Pitfall: a source yields many findings, so insights cannot be a column on sources.
CREATE TABLE IF NOT EXISTS source_insights (
    insight_id   INTEGER PRIMARY KEY,
    source_id    INTEGER NOT NULL REFERENCES sources(source_id),
    run_id       TEXT NOT NULL REFERENCES runs(run_id),
    claim        TEXT NOT NULL,
    theme        TEXT,
    evidence_url TEXT,
    excerpt      TEXT,
    weight       REAL NOT NULL DEFAULT 1.0,
    criterion_id INTEGER REFERENCES criteria(criterion_id)
);

-- criteria: the auditable GEO/AEO rules. In: Phase 0.
-- Pitfall: justification lives on source_insights.criterion_id, not an extra junction table.
CREATE TABLE IF NOT EXISTS criteria (
    criterion_id INTEGER PRIMARY KEY,
    run_id       TEXT NOT NULL REFERENCES runs(run_id),
    code         TEXT,
    description  TEXT NOT NULL
);

-- gaps: a scored finding on a page. In: Phase 2 audit.
-- Pitfall: severity-ranked, deduplicated by id.
CREATE TABLE IF NOT EXISTS gaps (
    gap_id        TEXT PRIMARY KEY,
    run_id        TEXT NOT NULL REFERENCES runs(run_id),
    url_id        INTEGER REFERENCES urls(url_id),
    criterion_id  INTEGER REFERENCES criteria(criterion_id),
    gap_type      TEXT NOT NULL,
    severity      INTEGER NOT NULL,
    status        TEXT NOT NULL,
    description   TEXT
);

-- gap_insights: the bridge between researched insights and gaps.
-- Pitfall: enforces that gaps cite insights instead of standing as assertions.
CREATE TABLE IF NOT EXISTS gap_insights (
    gap_id     TEXT NOT NULL REFERENCES gaps(gap_id),
    insight_id INTEGER NOT NULL REFERENCES source_insights(insight_id),
    role       TEXT,
    PRIMARY KEY (gap_id, insight_id)
);

-- proposals: recommended change plus handoff state. In: Phase 3.
-- Pitfall: Jira-specific fields live in jira_tickets, not here.
CREATE TABLE IF NOT EXISTS proposals (
    proposal_id     INTEGER PRIMARY KEY,
    gap_id          TEXT NOT NULL REFERENCES gaps(gap_id),
    run_id          TEXT NOT NULL REFERENCES runs(run_id),
    source_proposal_id TEXT,
    proposed_change TEXT NOT NULL,
    source_citation TEXT,
    current_state TEXT,
    implementation_status TEXT,
    priority_tier   TEXT NOT NULL,
    impact_estimate TEXT,
    handoff_status  TEXT NOT NULL DEFAULT 'draft'
);

-- jira_tickets: each proposal prepared as a Jira-import row.
-- Pitfall: this is the handoff contract; wrong columns or values break Jira import.
CREATE TABLE IF NOT EXISTS jira_tickets (
    jira_ticket_id      INTEGER PRIMARY KEY,
    proposal_id         INTEGER REFERENCES proposals(proposal_id),
    run_id              TEXT NOT NULL REFERENCES runs(run_id),
    issue_type          TEXT NOT NULL,
    epic_name           TEXT NOT NULL,
    summary             TEXT NOT NULL,
    description         TEXT,
    priority            TEXT NOT NULL,
    labels              TEXT,
    component           TEXT,
    acceptance_criteria TEXT
);

-- run_artifacts: raw phase files imported into the DB.
-- Pitfall: normalized rows are queryable, raw markdown remains preserved for fallback/provenance.
CREATE TABLE IF NOT EXISTS run_artifacts (
    run_id       TEXT NOT NULL REFERENCES runs(run_id),
    artifact_type TEXT NOT NULL,
    path         TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    raw_text     TEXT NOT NULL,
    imported_at  TEXT NOT NULL,
    PRIMARY KEY (run_id, artifact_type)
);

-- metadata_snapshots: page-level audit state parsed from metadata_snapshot.md.
CREATE TABLE IF NOT EXISTS metadata_snapshots (
    snapshot_id      INTEGER PRIMARY KEY,
    run_id           TEXT NOT NULL REFERENCES runs(run_id),
    url_id           INTEGER REFERENCES urls(url_id),
    page_label       TEXT,
    title            TEXT,
    meta_description TEXT,
    fetch_status     TEXT,
    raw_excerpt      TEXT,
    source_path      TEXT,
    live_capture_json TEXT,
    captured_at      TEXT,
    UNIQUE(run_id, url_id)
);

-- proposal_changes: implementation fields extracted from proposals.
CREATE TABLE IF NOT EXISTS proposal_changes (
    change_id               TEXT PRIMARY KEY,
    proposal_id             INTEGER NOT NULL REFERENCES proposals(proposal_id),
    run_id                  TEXT NOT NULL REFERENCES runs(run_id),
    change_type             TEXT NOT NULL,
    target_page             TEXT,
    target_field_or_section TEXT,
    current_value           TEXT,
    proposed_value          TEXT,
    warning                 TEXT
);

-- proposal_sources: traceability from proposals back to cited sources.
CREATE TABLE IF NOT EXISTS proposal_sources (
    proposal_id INTEGER NOT NULL REFERENCES proposals(proposal_id),
    source_id   INTEGER NOT NULL REFERENCES sources(source_id),
    run_id      TEXT NOT NULL REFERENCES runs(run_id),
    role        TEXT,
    PRIMARY KEY (proposal_id, source_id)
);

-- dashboard_overrides: reviewer edits saved in the dashboard.
CREATE TABLE IF NOT EXISTS dashboard_overrides (
    run_id        TEXT NOT NULL REFERENCES runs(run_id),
    proposal_id   TEXT NOT NULL,
    override_json TEXT NOT NULL,
    updated_at    TEXT NOT NULL,
    PRIMARY KEY (run_id, proposal_id)
);

-- jira_exports: audit trail of generated Jira CSV exports.
CREATE TABLE IF NOT EXISTS jira_exports (
    export_id    INTEGER PRIMARY KEY,
    run_id       TEXT NOT NULL REFERENCES runs(run_id),
    proposal_id  TEXT,
    export_type  TEXT NOT NULL,
    csv_content  TEXT NOT NULL,
    created_at   TEXT NOT NULL
);

-- run_url_targets: immutable run-scoped URL target snapshot.
-- Pitfall: urls.selected_for_next_run is only a pending queue; this table records what a run actually uses.
CREATE TABLE IF NOT EXISTS run_url_targets (
    run_id           TEXT NOT NULL REFERENCES runs(run_id),
    url_id           INTEGER NOT NULL REFERENCES urls(url_id),
    selection_source TEXT NOT NULL,
    selected_at      TEXT,
    audit_profile    TEXT,
    model            TEXT,
    PRIMARY KEY (run_id, url_id)
);

-- url_selection_events: durable record of dashboard link-selection actions.
CREATE TABLE IF NOT EXISTS url_selection_events (
    event_id       INTEGER PRIMARY KEY,
    url_id         INTEGER REFERENCES urls(url_id),
    url            TEXT,
    action         TEXT NOT NULL,
    selection_mode TEXT NOT NULL,
    filters_json   TEXT,
    selected_count INTEGER NOT NULL DEFAULT 0,
    created_at     TEXT NOT NULL
);
