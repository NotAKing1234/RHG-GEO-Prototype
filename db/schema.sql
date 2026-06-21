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
    page_type             TEXT,
    location_confidence   TEXT,
    selected_for_next_run INTEGER NOT NULL DEFAULT 0,
    selected_at           TEXT,
    last_audited_run      TEXT REFERENCES runs(run_id)
);

-- sources: the artifact consulted. In: URL / competitor / OTA / literature refs.
-- Pitfall: keeps "where it came from" separate from "what it said".
CREATE TABLE IF NOT EXISTS sources (
    source_id   INTEGER PRIMARY KEY,
    run_id      TEXT NOT NULL REFERENCES runs(run_id),
    url         TEXT,
    domain      TEXT,
    title       TEXT,
    source_type TEXT NOT NULL,
    credibility REAL NOT NULL DEFAULT 1.0,
    fetched_at  TEXT
);

-- source_insights: one insight pulled from one source.
-- Pitfall: a source yields many findings, so insights cannot be a column on sources.
CREATE TABLE IF NOT EXISTS source_insights (
    insight_id   INTEGER PRIMARY KEY,
    source_id    INTEGER NOT NULL REFERENCES sources(source_id),
    run_id       TEXT NOT NULL REFERENCES runs(run_id),
    claim        TEXT NOT NULL,
    theme        TEXT,
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
    proposed_change TEXT NOT NULL,
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
