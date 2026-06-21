# Radisson GEO Optimizer — V1.1 Data Model Spec

**Status:** Draft for build · **Principle:** local-first, single operator, agent-supported → SQLite, not a server DB.

> Doc convention (from the Execution Log): every table opens with a one-line gloss — *what it is · what flows in · the pitfall it prevents*. The DB is the one source of truth; files are generated views.

## TL;DR

- **SQLite is the system of record** (`db/geo_optimizer.db`). CSV/Markdown are generated exports, not authority.
- **One linear pipeline:** `sources → source_insights → criteria → gaps → gap_insights → proposals → jira_tickets`.
- **9 tables.** The final `jira_tickets` step prepares each proposal as a Jira-import row matching `RHG JIRA EXPORT.csv` exactly.
- **Selection is a DB flag**, not a CSV race. Dashboard checks a box → `selected_for_next_run = 1` → agents query it.

---

## 1. The model in one sentence

Grab the **sources**, pull the **insights** out of each, distil those into **criteria**, audit pages against the criteria to find **gaps**, cite the insights that justify each gap (**gap_insights**), turn gaps into **proposals**, then prepare each proposal as a Jira-ready **jira_ticket** for export.

```
sources ─▶ source_insights ─▶ criteria ─▶ gaps ─▶ proposals ─▶ jira_tickets ─▶ Jira CSV
                    └────────── gap_insights ──────┘
```

---

## 2. Tables (9)

```sql
-- runs: the run envelope. In: one row per run. Pitfall: stops cross-run data bleed.
CREATE TABLE runs (
    run_id          TEXT PRIMARY KEY,          -- 'run_004'
    run_number      INTEGER NOT NULL,
    run_date        TEXT NOT NULL,
    status          TEXT NOT NULL,             -- IN_PROGRESS | COMPLETED
    previous_run_id TEXT REFERENCES runs(run_id)
);

-- urls: the managed Radisson registry (moved off CSV). In: crawl + dashboard edits.
-- Pitfall: selection is a column here, not a separate file that goes stale.
CREATE TABLE urls (
    url_id                INTEGER PRIMARY KEY,
    url                   TEXT NOT NULL UNIQUE,
    brand                 TEXT,
    region                TEXT,
    page_type             TEXT,
    location_confidence   TEXT,
    selected_for_next_run INTEGER NOT NULL DEFAULT 0,  -- the selection flag
    selected_at           TEXT,
    last_audited_run      TEXT REFERENCES runs(run_id)
);

-- sources: the artifact you consulted (~100/run). In: URL / competitor / OTA / literature refs.
-- Pitfall: keeps "where it came from" separate from "what it said".
CREATE TABLE sources (
    source_id   INTEGER PRIMARY KEY,
    run_id      TEXT NOT NULL REFERENCES runs(run_id),
    url         TEXT,
    domain      TEXT,
    title       TEXT,
    source_type TEXT NOT NULL,                 -- literature | competitor | ota | radisson_own | other
    credibility REAL NOT NULL DEFAULT 1.0,     -- 0..2, used in ranking
    fetched_at  TEXT
);

-- source_insights: ONE insight pulled from ONE source (many per source).
-- In: agent extraction. Pitfall: a source yields many findings, so insights can't be a column on sources.
CREATE TABLE source_insights (
    insight_id   INTEGER PRIMARY KEY,
    source_id    INTEGER NOT NULL REFERENCES sources(source_id),
    run_id       TEXT NOT NULL REFERENCES runs(run_id),
    claim        TEXT NOT NULL,                -- the finding, in plain language
    theme        TEXT,                         -- group label; consensus = COUNT per theme
    weight       REAL NOT NULL DEFAULT 1.0,    -- agent confidence × source.credibility
    criterion_id INTEGER REFERENCES criteria(criterion_id)  -- which criterion this informed (nullable)
);

-- criteria: the auditable GEO/AEO rules, distilled from source_insights. In: Phase 0.
-- Pitfall: justification is the insights that point here (source_insights.criterion_id) — no junction table.
CREATE TABLE criteria (
    criterion_id INTEGER PRIMARY KEY,
    run_id       TEXT NOT NULL REFERENCES runs(run_id),
    code         TEXT,                          -- e.g. C11
    description  TEXT NOT NULL
);

-- gaps: a scored finding on a page. In: Phase 2 audit. Pitfall: severity-ranked, dedup'd by id.
CREATE TABLE gaps (
    gap_id        TEXT PRIMARY KEY,             -- 'GAP-030'
    run_id        TEXT NOT NULL REFERENCES runs(run_id),
    url_id        INTEGER REFERENCES urls(url_id),
    criterion_id  INTEGER REFERENCES criteria(criterion_id),
    gap_type      TEXT NOT NULL,                -- MISSING | WEAK | MISALIGNED
    severity      INTEGER NOT NULL,             -- 1..3
    status        TEXT NOT NULL,                -- NEW | RECURRING
    description   TEXT
);

-- gap_insights: the one bridge — which insights justify a gap (a gap cites several).
-- Pitfall: enforces "gaps are researched from insights, not asserted".
CREATE TABLE gap_insights (
    gap_id     TEXT NOT NULL REFERENCES gaps(gap_id),
    insight_id INTEGER NOT NULL REFERENCES source_insights(insight_id),
    role       TEXT,                            -- best_practice | competitor_example | impact
    PRIMARY KEY (gap_id, insight_id)
);

-- proposals: the recommended change + handoff state. In: Phase 3.
-- Pitfall: stays clean — Jira-specific fields live in jira_tickets, not here.
CREATE TABLE proposals (
    proposal_id     INTEGER PRIMARY KEY,
    gap_id          TEXT NOT NULL REFERENCES gaps(gap_id),
    run_id          TEXT NOT NULL REFERENCES runs(run_id),
    proposed_change TEXT NOT NULL,
    priority_tier   TEXT NOT NULL,              -- P1 | P2 | P3
    impact_estimate TEXT,
    handoff_status  TEXT NOT NULL DEFAULT 'draft'  -- draft | sent | accepted | implemented | rejected
);

-- jira_tickets: each proposal prepared as a Jira-import row (the export-prep step).
-- Columns mirror RHG JIRA EXPORT.csv exactly so the CSV is a 1:1 dump. In: Phase 3.5.
-- Pitfall: this is the handoff contract — wrong columns/values break the Jira import.
CREATE TABLE jira_tickets (
    jira_ticket_id      INTEGER PRIMARY KEY,
    proposal_id         INTEGER REFERENCES proposals(proposal_id),  -- NULL on the per-run Epic header row
    run_id              TEXT NOT NULL REFERENCES runs(run_id),
    issue_type          TEXT NOT NULL,          -- Epic | Story
    epic_name           TEXT NOT NULL,          -- groups stories, e.g. 'Radisson GEO Optimization - run_004'
    summary             TEXT NOT NULL,          -- ticket title
    description         TEXT,                   -- Dev specs / SEO-GEO rationale / GEO score / Validation
    priority            TEXT NOT NULL,          -- Highest | High | Medium | Low
    labels              TEXT,                   -- semicolon-separated, e.g. 'GEO;Schema;Discovery'
    component           TEXT,                   -- Platform | Discovery | Commerce | Guest Experience | Meetings & Events
    acceptance_criteria TEXT                    -- dash-bulleted, concrete and testable
);
```

---

## 3. Jira export step (proposal → jira_ticket)

The reference file `RHG JIRA EXPORT.csv` defines the exact import contract. `jira_tickets` carries those 8 columns verbatim, so the Jira CSV is a straight dump (`SELECT issue_type, epic_name, summary, description, priority, labels, component, acceptance_criteria`).

**Mapping each proposal to a Story row:**

| Jira column | Source | Convention |
|---|---|---|
| `Issue Type` | constant | `Story` per proposal; one `Epic` header row per run |
| `Epic Name` | run | `Radisson GEO Optimization - {run_id}` (every story shares it) |
| `Summary` | proposal | short imperative title of the change |
| `Description` | proposal | grouped: Dev change specs · SEO/GEO rationale · GEO visibility score · Validation steps |
| `Priority` | `proposals.priority_tier` | **P1→Highest, P2→High, P3→Medium** (Low for nice-to-haves) |
| `Labels` | gap category + brand | semicolon-separated, always lead with `GEO` (e.g. `GEO;Schema;FAQPage`) |
| `Component` | gap category → enum | Platform · Discovery · Commerce · Guest Experience · Meetings & Events (see map below) |
| `Acceptance Criteria` | proposal | dash-bulleted, concrete + testable; `[NEEDED: ...]` if unknown |

**Category → Component map:**

- schema / crawler access / technical → **Platform**
- content / destination / SEO copy / discovery → **Discovery**
- pricing / availability / booking / distribution → **Commerce**
- loyalty / rewards / guest journey → **Guest Experience**
- meetings / MICE / venues → **Meetings & Events**

One `Epic` row is emitted per run (`issue_type = Epic`, `proposal_id = NULL`) so the stories group cleanly on import, mirroring the reference file's Epic-plus-Stories structure.

---

## 4. Ranking & consensus (simple version)

```sql
SELECT claim, theme, weight FROM source_insights
WHERE run_id = :run_id ORDER BY weight DESC;          -- strongest insights

SELECT theme, COUNT(*) AS sources_backing, SUM(weight) AS total_weight
FROM source_insights WHERE run_id = :run_id
GROUP BY theme ORDER BY sources_backing DESC;         -- consensus by theme
```

`weight = agent_confidence × source.credibility`. No canonicalization step, no embeddings.

---

## 5. Exports (DB → files)

Generated on demand; the DB is authoritative.

| Export | From | Consumer |
|---|---|---|
| `target_urls.md` | all `urls` | human review / fallback |
| `next_geo_run.csv` | `urls WHERE selected_for_next_run = 1` | inspection only |
| `optimization_proposal.md` | `proposals ⨝ gaps` | run artifact |
| **Jira import CSV** | **`jira_tickets` (8 columns verbatim)** | **dashboard Exports → Jira** |
| `<run>_sources.md` | `sources ⨝ source_insights` | literature artifact |

The Jira CSV must match `RHG JIRA EXPORT.csv` header order exactly. One `scripts/export.py` renders all of these.

---

## 6. Selection flow (kills the CSV race)

1. Operator checks URLs in the dashboard.
2. `POST /api/url-registry/selection` → `selected_for_next_run = 1` + `selected_at`.
3. `run.py` scrapes `WHERE selected_for_next_run = 1`. One source of truth, deterministic.
4. On completion, stamp `last_audited_run` (auto-clear the flag is your call — see §9).

---

## 7. Migration (current files → SQLite)

One-time `scripts/migrate_to_sqlite.py`:

1. Create DB from `schema.sql`.
2. Backfill `runs` from `run_index.md` (run_001–003).
3. Backfill `urls` from `radisson_url_registry.csv`.
4. Backfill `gaps` / `proposals` from existing run `.md` files; sources/insights start fresh at run_004.
5. Keep flat files; switch reads to the DB incrementally, regenerating files via `export.py`.
6. Validate: row counts vs. parsed files; 3 proposals round-trip DB → Jira CSV identically to `RHG JIRA EXPORT.csv` format.

---

## 8. Phase map

| Phase | Reads | Writes |
|---|---|---|
| 0 Literature | runs | sources, source_insights, criteria |
| 1 Context brief | prior snapshot, urls | snapshot rows (optional) |
| 2 Audit/Gap | criteria, urls, source_insights | gaps, gap_insights |
| 2.5 Gap research | gaps | sources, source_insights, gap_insights |
| 3 Proposal | gaps, source_insights, criteria | proposals |
| 3.5 Jira prep | proposals, gaps | jira_tickets |
| 4 Log & learn | gaps, proposals diff | runs(status), proposals(handoff_status) |

---

## 9. Open questions before build

- Auto-clear `selected_for_next_run` after a run, or leave it sticky?
- One Epic per run, or one standing Epic across all GEO runs?
- Priority map P1→Highest / P2→High / P3→Medium — confirm, or should severity feed Priority instead?
- `.db` gitignored, with `schema.sql` + migrations checked in?
