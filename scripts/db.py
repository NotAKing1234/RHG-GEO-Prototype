#!/usr/bin/env python3
"""Thin SQLite access layer for the GEO Optimizer.

Data flow: migration and pipeline phases write normalized rows here; exports and dashboard reads
come back through these helpers. Pitfalls: no ORM, no generated-file authority, and all connections
enable foreign keys so bad cross-run references fail early.
"""

from __future__ import annotations

import csv
import json
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator, Sequence


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "db" / "geo_optimizer.db"
SCHEMA_PATH = ROOT / "db" / "schema.sql"

JIRA_FIELDS = [
    "Issue Type",
    "Epic Name",
    "Summary",
    "Description",
    "Priority",
    "Labels",
    "Component",
    "Acceptance Criteria",
]

TABLES = [
    "runs",
    "urls",
    "run_artifacts",
    "sources",
    "source_insights",
    "criteria",
    "gaps",
    "gap_insights",
    "proposals",
    "metadata_snapshots",
    "proposal_changes",
    "proposal_sources",
    "dashboard_overrides",
    "jira_tickets",
    "jira_exports",
    "run_url_targets",
    "url_selection_events",
]

PRIORITY_MAP = {"P1": "Highest", "P2": "High", "P3": "Medium"}

COMPONENT_KEYWORDS = [
    ("Meetings & Events", ("meeting", "mice", "conference", "venue", "event")),
    ("Commerce", ("pricing", "availability", "booking", "distribution", "commerce", "rate")),
    ("Guest Experience", ("loyalty", "reward", "guest journey", "member")),
    ("Platform", ("schema", "crawler", "technical", "json-ld", "structured data", "access")),
    ("Discovery", ("content", "destination", "seo", "copy", "discovery", "faq", "entity")),
]


@dataclass(frozen=True)
class UrlSelectionResult:
    selected_count: int
    selection_mode: str
    selected_urls: list[str]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def connect(db_path: Path | str = DB_PATH) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def connection(db_path: Path | str = DB_PATH) -> Iterator[sqlite3.Connection]:
    conn = connect(db_path)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def initialize_database(db_path: Path | str = DB_PATH, schema_path: Path | str = SCHEMA_PATH) -> None:
    with connection(db_path) as conn:
        conn.executescript(Path(schema_path).read_text(encoding="utf-8"))
        apply_compat_migrations(conn)


def table_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    return {str(item["name"]) for item in conn.execute(f"PRAGMA table_info({table})").fetchall()}


def add_column_if_missing(conn: sqlite3.Connection, table: str, column: str, ddl_type: str) -> None:
    if column not in table_columns(conn, table):
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {ddl_type}")


def apply_compat_migrations(conn: sqlite3.Connection) -> None:
    """Upgrade already-created local DB files without requiring a reset."""
    for column in ("country", "locale", "content_group", "location_source", "source_sitemap"):
        add_column_if_missing(conn, "urls", column, "TEXT")
    for column in (
        "source_key",
        "headline",
        "finding_group",
        "full_excerpt",
        "ai_assessment_prose",
        "scorecard_json",
        "related_criteria_json",
        "related_gaps_json",
        "related_recommendations_json",
    ):
        add_column_if_missing(conn, "sources", column, "TEXT")
    for column in ("evidence_url", "excerpt"):
        add_column_if_missing(conn, "source_insights", column, "TEXT")
    for column in ("source_proposal_id", "source_citation", "current_state", "implementation_status"):
        add_column_if_missing(conn, "proposals", column, "TEXT")


def rows(conn: sqlite3.Connection, query: str, params: Sequence[Any] = ()) -> list[dict[str, Any]]:
    return [dict(row) for row in conn.execute(query, params).fetchall()]


def row(conn: sqlite3.Connection, query: str, params: Sequence[Any] = ()) -> dict[str, Any] | None:
    value = conn.execute(query, params).fetchone()
    return dict(value) if value else None


def table_names(conn: sqlite3.Connection) -> list[str]:
    found = rows(conn, "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    return [item["name"] for item in found]


def table_counts(conn: sqlite3.Connection) -> dict[str, int]:
    return {table: int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]) for table in TABLES}


def upsert_run(
    conn: sqlite3.Connection,
    run_id: str,
    run_number: int,
    run_date: str,
    status: str = "COMPLETED",
    previous_run_id: str | None = None,
) -> None:
    conn.execute(
        """
        INSERT INTO runs(run_id, run_number, run_date, status, previous_run_id)
        VALUES(?, ?, ?, ?, ?)
        ON CONFLICT(run_id) DO UPDATE SET
            run_number=excluded.run_number,
            run_date=excluded.run_date,
            status=excluded.status,
            previous_run_id=excluded.previous_run_id
        """,
        (run_id, run_number, run_date, status, previous_run_id),
    )


def upsert_url(
    conn: sqlite3.Connection,
    url: str,
    *,
    brand: str | None = None,
    region: str | None = None,
    country: str | None = None,
    locale: str | None = None,
    page_type: str | None = None,
    content_group: str | None = None,
    location_confidence: str | None = None,
    location_source: str | None = None,
    source_sitemap: str | None = None,
    selected_for_next_run: int | bool | None = None,
    selected_at: str | None = None,
    last_audited_run: str | None = None,
) -> int:
    conn.execute(
        """
        INSERT INTO urls(
            url, brand, region, country, locale, page_type, content_group, location_confidence,
            location_source, source_sitemap, selected_for_next_run, selected_at, last_audited_run
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, COALESCE(?, 0), ?, ?)
        ON CONFLICT(url) DO UPDATE SET
            brand=COALESCE(excluded.brand, urls.brand),
            region=COALESCE(excluded.region, urls.region),
            country=COALESCE(excluded.country, urls.country),
            locale=COALESCE(excluded.locale, urls.locale),
            page_type=COALESCE(excluded.page_type, urls.page_type),
            content_group=COALESCE(excluded.content_group, urls.content_group),
            location_confidence=COALESCE(excluded.location_confidence, urls.location_confidence),
            location_source=COALESCE(excluded.location_source, urls.location_source),
            source_sitemap=COALESCE(excluded.source_sitemap, urls.source_sitemap),
            selected_for_next_run=CASE
                WHEN ? IS NULL THEN urls.selected_for_next_run ELSE excluded.selected_for_next_run
            END,
            selected_at=COALESCE(excluded.selected_at, urls.selected_at),
            last_audited_run=COALESCE(excluded.last_audited_run, urls.last_audited_run)
        """,
        (
            url,
            brand,
            region,
            country,
            locale,
            page_type,
            content_group,
            location_confidence,
            location_source,
            source_sitemap,
            int(bool(selected_for_next_run)) if selected_for_next_run is not None else None,
            selected_at,
            last_audited_run,
            selected_for_next_run,
        ),
    )
    return int(conn.execute("SELECT url_id FROM urls WHERE url = ?", (url,)).fetchone()[0])


def upsert_criterion(conn: sqlite3.Connection, run_id: str, code: str | None, description: str) -> int:
    existing = conn.execute(
        "SELECT criterion_id FROM criteria WHERE run_id = ? AND COALESCE(code, '') = COALESCE(?, '')",
        (run_id, code),
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE criteria SET description = ? WHERE criterion_id = ?",
            (description, existing["criterion_id"]),
        )
        return int(existing["criterion_id"])
    cur = conn.execute(
        "INSERT INTO criteria(run_id, code, description) VALUES(?, ?, ?)",
        (run_id, code, description),
    )
    return int(cur.lastrowid)


def criterion_id_for_code(conn: sqlite3.Connection, run_id: str, code: str | None) -> int | None:
    if not code:
        return None
    found = conn.execute(
        "SELECT criterion_id FROM criteria WHERE run_id = ? AND code = ?",
        (run_id, code),
    ).fetchone()
    return int(found["criterion_id"]) if found else None


def upsert_gap(
    conn: sqlite3.Connection,
    gap_id: str,
    run_id: str,
    *,
    url_id: int | None,
    criterion_id: int | None,
    gap_type: str,
    severity: int,
    status: str,
    description: str | None,
) -> None:
    conn.execute(
        """
        INSERT INTO gaps(gap_id, run_id, url_id, criterion_id, gap_type, severity, status, description)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(gap_id) DO UPDATE SET
            run_id=excluded.run_id,
            url_id=excluded.url_id,
            criterion_id=excluded.criterion_id,
            gap_type=excluded.gap_type,
            severity=excluded.severity,
            status=excluded.status,
            description=excluded.description
        """,
        (gap_id, run_id, url_id, criterion_id, gap_type, severity, status, description),
    )


def upsert_proposal(
    conn: sqlite3.Connection,
    proposal_id: int,
    gap_id: str,
    run_id: str,
    *,
    source_proposal_id: str | None = None,
    proposed_change: str,
    source_citation: str | None = None,
    current_state: str | None = None,
    implementation_status: str | None = None,
    priority_tier: str,
    impact_estimate: str | None,
    handoff_status: str = "draft",
) -> int:
    conn.execute(
        """
        INSERT INTO proposals(
            proposal_id, gap_id, run_id, source_proposal_id, proposed_change, source_citation,
            current_state, implementation_status, priority_tier, impact_estimate, handoff_status
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(proposal_id) DO UPDATE SET
            gap_id=excluded.gap_id,
            run_id=excluded.run_id,
            source_proposal_id=COALESCE(excluded.source_proposal_id, proposals.source_proposal_id),
            proposed_change=excluded.proposed_change,
            source_citation=COALESCE(excluded.source_citation, proposals.source_citation),
            current_state=COALESCE(excluded.current_state, proposals.current_state),
            implementation_status=COALESCE(excluded.implementation_status, proposals.implementation_status),
            priority_tier=excluded.priority_tier,
            impact_estimate=excluded.impact_estimate,
            handoff_status=excluded.handoff_status
        """,
        (
            proposal_id,
            gap_id,
            run_id,
            source_proposal_id,
            proposed_change,
            source_citation,
            current_state,
            implementation_status,
            priority_tier,
            impact_estimate,
            handoff_status,
        ),
    )
    return proposal_id


def list_urls(conn: sqlite3.Connection, filters: dict[str, str] | None = None) -> list[dict[str, Any]]:
    filters = filters or {}
    clauses: list[str] = []
    params: list[Any] = []
    for field in ("brand", "region", "page_type", "location_confidence"):
        value = filters.get(field)
        if value and value != "all":
            if value == "Unspecified":
                clauses.append(f"(COALESCE({field}, '') = '')")
            else:
                clauses.append(f"{field} = ?")
                params.append(value)
    query_text = filters.get("query")
    if query_text:
        clauses.append("(url LIKE ? OR brand LIKE ? OR region LIKE ? OR page_type LIKE ?)")
        like = f"%{query_text}%"
        params.extend([like, like, like, like])
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    return rows(
        conn,
        f"""
        SELECT url_id, url, brand, region, country, locale, page_type, content_group,
               location_confidence, location_source, source_sitemap,
               selected_for_next_run, selected_at, last_audited_run
        FROM urls
        {where}
        ORDER BY COALESCE(brand, ''), COALESCE(region, ''), COALESCE(page_type, ''), url
        """,
        params,
    )


def set_selected_urls(
    conn: sqlite3.Connection,
    urls: Sequence[str],
    *,
    clear_existing: bool = True,
) -> UrlSelectionResult:
    if clear_existing:
        conn.execute("UPDATE urls SET selected_for_next_run = 0, selected_at = NULL")
    stamp = utc_now()
    selected: list[str] = []
    for value in urls:
        found = conn.execute("SELECT url FROM urls WHERE url = ?", (value,)).fetchone()
        if not found:
            continue
        conn.execute(
            "UPDATE urls SET selected_for_next_run = 1, selected_at = ? WHERE url = ?",
            (stamp, value),
        )
        selected.append(value)
    return UrlSelectionResult(len(selected), "explicit_urls", selected)


def set_selected_by_filters(conn: sqlite3.Connection, filters: dict[str, str]) -> UrlSelectionResult:
    selected_rows = list_urls(conn, filters)
    result = set_selected_urls(conn, [item["url"] for item in selected_rows])
    return UrlSelectionResult(result.selected_count, "filters", result.selected_urls)


def selected_urls(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    return rows(
        conn,
        """
        SELECT url_id, url, brand, region, country, locale, page_type, content_group,
               location_confidence, location_source, source_sitemap, selected_at, last_audited_run
        FROM urls
        WHERE selected_for_next_run = 1
        ORDER BY COALESCE(brand, ''), COALESCE(region, ''), COALESCE(page_type, ''), url
        """,
    )


def infer_component(*texts: str) -> str:
    haystack = " ".join(texts).lower()
    for component, keywords in COMPONENT_KEYWORDS:
        if any(keyword in haystack for keyword in keywords):
            return component
    return "Discovery"


def json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def json_loads(value: str | None, default: Any = None) -> Any:
    if not value:
        return default
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return default


def upsert_source(
    conn: sqlite3.Connection,
    *,
    run_id: str,
    source_key: str,
    url: str | None,
    domain: str | None,
    title: str | None,
    source_type: str,
    headline: str | None = None,
    finding_group: str | None = None,
    full_excerpt: str | None = None,
    ai_assessment_prose: str | None = None,
    scorecard: dict[str, Any] | None = None,
    related_criteria: list[str] | None = None,
    related_gaps: list[str] | None = None,
    related_recommendations: list[str] | None = None,
    credibility: float = 1.0,
    fetched_at: str | None = None,
) -> int:
    existing = conn.execute(
        "SELECT source_id FROM sources WHERE run_id = ? AND source_key = ?",
        (run_id, source_key),
    ).fetchone()
    values = (
        run_id,
        source_key,
        url,
        domain,
        title,
        source_type,
        headline,
        finding_group,
        full_excerpt,
        ai_assessment_prose,
        json_dumps(scorecard or {}),
        json_dumps(related_criteria or []),
        json_dumps(related_gaps or []),
        json_dumps(related_recommendations or []),
        credibility,
        fetched_at or utc_now(),
    )
    if existing:
        conn.execute(
            """
            UPDATE sources
            SET url = ?, domain = ?, title = ?, source_type = ?, headline = ?, finding_group = ?,
                full_excerpt = ?, ai_assessment_prose = ?, scorecard_json = ?,
                related_criteria_json = ?, related_gaps_json = ?, related_recommendations_json = ?,
                credibility = ?, fetched_at = ?
            WHERE source_id = ?
            """,
            values[2:] + (existing["source_id"],),
        )
        return int(existing["source_id"])
    cur = conn.execute(
        """
        INSERT INTO sources(
            run_id, source_key, url, domain, title, source_type, headline, finding_group,
            full_excerpt, ai_assessment_prose, scorecard_json, related_criteria_json,
            related_gaps_json, related_recommendations_json, credibility, fetched_at
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        values,
    )
    return int(cur.lastrowid)


def insert_source_insight(
    conn: sqlite3.Connection,
    *,
    source_id: int,
    run_id: str,
    claim: str,
    theme: str | None = None,
    evidence_url: str | None = None,
    excerpt: str | None = None,
    weight: float = 1.0,
    criterion_id: int | None = None,
) -> int:
    cur = conn.execute(
        """
        INSERT INTO source_insights(source_id, run_id, claim, theme, evidence_url, excerpt, weight, criterion_id)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (source_id, run_id, claim, theme, evidence_url, excerpt, weight, criterion_id),
    )
    return int(cur.lastrowid)


def upsert_run_artifact(
    conn: sqlite3.Connection,
    *,
    run_id: str,
    artifact_type: str,
    path: str,
    content_hash: str,
    raw_text: str,
) -> None:
    conn.execute(
        """
        INSERT INTO run_artifacts(run_id, artifact_type, path, content_hash, raw_text, imported_at)
        VALUES(?, ?, ?, ?, ?, ?)
        ON CONFLICT(run_id, artifact_type) DO UPDATE SET
            path=excluded.path,
            content_hash=excluded.content_hash,
            raw_text=excluded.raw_text,
            imported_at=excluded.imported_at
        """,
        (run_id, artifact_type, path, content_hash, raw_text, utc_now()),
    )


def save_dashboard_override(conn: sqlite3.Connection, run_id: str, proposal_id: str | int, override: dict[str, Any]) -> None:
    current = dashboard_override(conn, run_id, proposal_id) or {}
    merged = {**current, **override, "timestamp": utc_now()}
    conn.execute(
        """
        INSERT INTO dashboard_overrides(run_id, proposal_id, override_json, updated_at)
        VALUES(?, ?, ?, ?)
        ON CONFLICT(run_id, proposal_id) DO UPDATE SET
            override_json=excluded.override_json,
            updated_at=excluded.updated_at
        """,
        (run_id, str(proposal_id), json_dumps(merged), merged["timestamp"]),
    )


def dashboard_override(conn: sqlite3.Connection, run_id: str, proposal_id: str | int) -> dict[str, Any] | None:
    value = conn.execute(
        "SELECT override_json FROM dashboard_overrides WHERE run_id = ? AND proposal_id = ?",
        (run_id, str(proposal_id)),
    ).fetchone()
    return json_loads(value["override_json"], {}) if value else None


def dashboard_overrides_for_run(conn: sqlite3.Connection, run_id: str) -> dict[str, dict[str, Any]]:
    return {
        str(item["proposal_id"]): json_loads(item["override_json"], {})
        for item in rows(conn, "SELECT proposal_id, override_json FROM dashboard_overrides WHERE run_id = ?", (run_id,))
    }


def record_selection_event(
    conn: sqlite3.Connection,
    *,
    action: str,
    selection_mode: str,
    selected_count: int,
    filters: dict[str, Any] | None = None,
    selected_url_values: Sequence[str] = (),
) -> None:
    filters_json = json_dumps(filters or {})
    if selected_url_values:
        for value in selected_url_values:
            found = conn.execute("SELECT url_id FROM urls WHERE url = ?", (value,)).fetchone()
            conn.execute(
                """
                INSERT INTO url_selection_events(url_id, url, action, selection_mode, filters_json, selected_count, created_at)
                VALUES(?, ?, ?, ?, ?, ?, ?)
                """,
                (found["url_id"] if found else None, value, action, selection_mode, filters_json, selected_count, utc_now()),
            )
        return
    conn.execute(
        """
        INSERT INTO url_selection_events(url_id, url, action, selection_mode, filters_json, selected_count, created_at)
        VALUES(NULL, NULL, ?, ?, ?, ?, ?)
        """,
        (action, selection_mode, filters_json, selected_count, utc_now()),
    )


def latest_selection_context(conn: sqlite3.Connection) -> dict[str, Any]:
    found = conn.execute(
        """
        SELECT selection_mode, filters_json
        FROM url_selection_events
        WHERE action = 'save_next_run'
        ORDER BY event_id DESC
        LIMIT 1
        """
    ).fetchone()
    if not found:
        return {"selection_mode": "pending_selection", "filters": {}}
    return {"selection_mode": found["selection_mode"], "filters": json_loads(found["filters_json"], {}) or {}}


def snapshot_next_run_targets(conn: sqlite3.Connection, run_id: str) -> int:
    context = latest_selection_context(conn)
    filters = context.get("filters") or {}
    selected = selected_urls(conn)
    conn.execute("DELETE FROM run_url_targets WHERE run_id = ?", (run_id,))
    for item in selected:
        conn.execute(
            """
            INSERT INTO run_url_targets(run_id, url_id, selection_source, selected_at, audit_profile, model)
            VALUES(?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                item["url_id"],
                context.get("selection_mode") or "pending_selection",
                item.get("selected_at") or utc_now(),
                filters.get("audit_profile") or "metadata_light",
                filters.get("model") or "gpt-5.4-mini",
            ),
        )
    if selected:
        conn.execute("UPDATE urls SET selected_for_next_run = 0, selected_at = NULL WHERE selected_for_next_run = 1")
    return len(selected)


def run_target_urls(conn: sqlite3.Connection, run_id: str) -> list[dict[str, Any]]:
    return rows(
        conn,
        """
        SELECT u.url_id, u.url, u.brand, u.region, u.country, u.locale, u.page_type, u.content_group,
               u.location_confidence, u.location_source, u.source_sitemap, u.last_audited_run,
               t.selection_source, t.selected_at, t.audit_profile, t.model
        FROM run_url_targets t
        JOIN urls u ON u.url_id = t.url_id
        WHERE t.run_id = ?
        ORDER BY COALESCE(u.brand, ''), COALESCE(u.region, ''), COALESCE(u.page_type, ''), u.url
        """,
        (run_id,),
    )


def labels_for(component: str, *texts: str) -> str:
    labels = ["GEO"]
    compact = component.replace("&", "and").replace(" ", "")
    if compact and compact not in labels:
        labels.append(compact)
    haystack = " ".join(texts).lower()
    for label, keywords in (
        ("Schema", ("schema", "json-ld", "structured data")),
        ("FAQPage", ("faq", "question", "answer")),
        ("Content", ("copy", "content", "description")),
    ):
        if any(keyword in haystack for keyword in keywords) and label not in labels:
            labels.append(label)
    return ";".join(labels)


def summarize_change(value: str) -> str:
    clean = " ".join((value or "").replace("\n", " ").split())
    if not clean:
        return "[NEEDED: proposal summary]"
    sentence = clean.split(". ")[0].strip(".")
    return sentence[:140]


LEGACY_GENERATED_ACCEPTANCE_CRITERIA = {
    "required content or value is present in the delivered page output.",
    "target content is present in server-delivered html when javascript is disabled.",
    "updated structured data field or object is present in the rendered output.",
    "change applies to the listed target url or page set.",
    "existing visible behavior remains unchanged unless specified in the ticket.",
    "evidence is attached before the ticket moves to validation.",
}


def ticket_list_items(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value or "").strip()
    if not text:
        return []
    if text.startswith("- "):
        return [item.strip() for item in text.replace("- ", "", 1).split(" - ") if item.strip()]
    return [
        line.strip().lstrip("0123456789. ").strip()
        for line in text.splitlines()
        if line.strip()
    ]


def is_legacy_acceptance(value: Any) -> bool:
    items = [" ".join(item.lower().split()) for item in ticket_list_items(value)]
    return len(items) == 4 and all(item in LEGACY_GENERATED_ACCEPTANCE_CRITERIA for item in items)


def acceptance_text(value: Any, fallback: str) -> str:
    if value and not is_legacy_acceptance(value):
        items = ticket_list_items(value)
        return "\n".join(f"- {item}" for item in items) if items else str(value)
    return fallback


def build_jira_tickets(conn: sqlite3.Connection, run_id: str) -> int:
    conn.execute("DELETE FROM jira_tickets WHERE run_id = ?", (run_id,))
    overrides = dashboard_overrides_for_run(conn, run_id)
    epic_name = f"Radisson GEO Optimization - {run_id}"
    proposal_rows = rows(
        conn,
        """
        SELECT p.proposal_id, p.proposed_change, p.priority_tier, p.impact_estimate,
               g.gap_id, g.gap_type, g.description AS gap_description,
               u.url, u.brand, c.code AS criterion_code, c.description AS criterion_description
        FROM proposals p
        JOIN gaps g ON g.gap_id = p.gap_id
        LEFT JOIN urls u ON u.url_id = g.url_id
        LEFT JOIN criteria c ON c.criterion_id = g.criterion_id
        WHERE p.run_id = ?
        ORDER BY p.priority_tier, p.proposal_id
        """,
        (run_id,),
    )
    conn.execute(
        """
        INSERT INTO jira_tickets(proposal_id, run_id, issue_type, epic_name, summary, description, priority, labels, component, acceptance_criteria)
        VALUES(NULL, ?, 'Epic', ?, ?, ?, 'Highest', 'GEO', 'Platform', ?)
        """,
        (
            run_id,
            epic_name,
            epic_name,
            f"Epic container for {len(proposal_rows)} GEO optimization stories generated from {run_id}.",
            f"- Epic delivered when all {len(proposal_rows)} child stories are reviewed and ready for Jira import.",
        ),
    )
    for proposal in proposal_rows:
        override = overrides.get(str(proposal["proposal_id"]), {})
        ticket_draft = override.get("ticket_draft") if isinstance(override.get("ticket_draft"), dict) else {}
        ticket_fields = override.get("ticket_internal_fields") if isinstance(override.get("ticket_internal_fields"), dict) else {}
        component = infer_component(
            proposal.get("gap_description") or "",
            proposal.get("proposed_change") or "",
            proposal.get("criterion_description") or "",
        )
        priority = PRIORITY_MAP.get((proposal.get("priority_tier") or "").upper(), "Low")
        description = (
            f"Dev change specs: {proposal.get('proposed_change') or '[NEEDED: implementation detail]'}\n\n"
            f"SEO/GEO rationale: {proposal.get('criterion_description') or proposal.get('gap_description') or '[NEEDED: rationale]'}\n\n"
            f"GEO visibility score: {proposal.get('priority_tier') or '[NEEDED: priority]'} / severity-informed.\n\n"
            f"Validation steps: Confirm the change is present on {proposal.get('url') or '[NEEDED: target URL]'} and rerun GEO audit."
        )
        acceptance = (
            f"- Proposed change is implemented for {proposal.get('url') or '[NEEDED: target URL]'}.\n"
            f"- Validation confirms the {proposal.get('gap_id')} gap is closed or explicitly downgraded.\n"
            "- Existing visible behavior remains unchanged unless specified in the ticket."
        )
        labels = ticket_fields.get("labels")
        if isinstance(labels, list):
            labels = ";".join(str(item).strip() for item in labels if str(item).strip())
        labels = labels or labels_for(component, proposal.get("gap_description") or "", proposal.get("proposed_change") or "")
        issue_type = ticket_fields.get("issue_type") or "Story"
        summary = ticket_draft.get("summary") or summarize_change(proposal.get("proposed_change") or "")
        description = ticket_draft.get("description") or description
        component = ticket_fields.get("component") or component
        acceptance = acceptance_text(ticket_draft.get("acceptance_criteria"), acceptance)
        conn.execute(
            """
            INSERT INTO jira_tickets(proposal_id, run_id, issue_type, epic_name, summary, description, priority, labels, component, acceptance_criteria)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                proposal["proposal_id"],
                run_id,
                issue_type,
                epic_name,
                summary,
                description,
                priority,
                labels,
                component,
                acceptance,
            ),
        )
    return len(proposal_rows) + 1


def jira_export_rows(conn: sqlite3.Connection, run_id: str, proposal_id: str | int | None = None) -> list[dict[str, str]]:
    params: list[Any] = [run_id]
    proposal_clause = ""
    if proposal_id not in (None, ""):
        proposal_value = int(str(proposal_id).replace("PROP-", "")) if str(proposal_id).startswith("PROP-") else int(proposal_id)
        proposal_clause = "AND (proposal_id = ? OR issue_type = 'Epic')"
        params.append(proposal_value)
    values = rows(
        conn,
        """
        SELECT issue_type, epic_name, summary, description, priority, labels, component, acceptance_criteria
        FROM jira_tickets
        WHERE run_id = ?
        {proposal_clause}
        ORDER BY CASE issue_type WHEN 'Epic' THEN 0 ELSE 1 END, jira_ticket_id
        """.format(proposal_clause=proposal_clause),
        params,
    )
    return [
        {
            "Issue Type": value["issue_type"],
            "Epic Name": value["epic_name"],
            "Summary": value["summary"],
            "Description": value.get("description") or "",
            "Priority": value["priority"],
            "Labels": value.get("labels") or "",
            "Component": value.get("component") or "",
            "Acceptance Criteria": value.get("acceptance_criteria") or "",
        }
        for value in values
    ]


def write_jira_csv(path: Path, rows_to_write: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=JIRA_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows_to_write)
