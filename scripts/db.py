#!/usr/bin/env python3
"""Thin SQLite access layer for the GEO Optimizer.

Data flow: migration and pipeline phases write normalized rows here; exports and dashboard reads
come back through these helpers. Pitfalls: no ORM, no generated-file authority, and all connections
enable foreign keys so bad cross-run references fail early.
"""

from __future__ import annotations

import csv
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
    "sources",
    "source_insights",
    "criteria",
    "gaps",
    "gap_insights",
    "proposals",
    "jira_tickets",
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
    page_type: str | None = None,
    location_confidence: str | None = None,
    selected_for_next_run: int | bool | None = None,
    selected_at: str | None = None,
    last_audited_run: str | None = None,
) -> int:
    conn.execute(
        """
        INSERT INTO urls(url, brand, region, page_type, location_confidence, selected_for_next_run, selected_at, last_audited_run)
        VALUES(?, ?, ?, ?, ?, COALESCE(?, 0), ?, ?)
        ON CONFLICT(url) DO UPDATE SET
            brand=COALESCE(excluded.brand, urls.brand),
            region=COALESCE(excluded.region, urls.region),
            page_type=COALESCE(excluded.page_type, urls.page_type),
            location_confidence=COALESCE(excluded.location_confidence, urls.location_confidence),
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
            page_type,
            location_confidence,
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
    proposed_change: str,
    priority_tier: str,
    impact_estimate: str | None,
    handoff_status: str = "draft",
) -> int:
    conn.execute(
        """
        INSERT INTO proposals(proposal_id, gap_id, run_id, proposed_change, priority_tier, impact_estimate, handoff_status)
        VALUES(?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(proposal_id) DO UPDATE SET
            gap_id=excluded.gap_id,
            run_id=excluded.run_id,
            proposed_change=excluded.proposed_change,
            priority_tier=excluded.priority_tier,
            impact_estimate=excluded.impact_estimate,
            handoff_status=excluded.handoff_status
        """,
        (proposal_id, gap_id, run_id, proposed_change, priority_tier, impact_estimate, handoff_status),
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
        SELECT url_id, url, brand, region, page_type, location_confidence,
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
        SELECT url_id, url, brand, region, page_type, location_confidence, selected_at, last_audited_run
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


def build_jira_tickets(conn: sqlite3.Connection, run_id: str) -> int:
    conn.execute("DELETE FROM jira_tickets WHERE run_id = ?", (run_id,))
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
        conn.execute(
            """
            INSERT INTO jira_tickets(proposal_id, run_id, issue_type, epic_name, summary, description, priority, labels, component, acceptance_criteria)
            VALUES(?, ?, 'Story', ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                proposal["proposal_id"],
                run_id,
                epic_name,
                summarize_change(proposal.get("proposed_change") or ""),
                description,
                priority,
                labels_for(component, proposal.get("gap_description") or "", proposal.get("proposed_change") or ""),
                component,
                acceptance,
            ),
        )
    return len(proposal_rows) + 1


def jira_export_rows(conn: sqlite3.Connection, run_id: str) -> list[dict[str, str]]:
    values = rows(
        conn,
        """
        SELECT issue_type, epic_name, summary, description, priority, labels, component, acceptance_criteria
        FROM jira_tickets
        WHERE run_id = ?
        ORDER BY CASE issue_type WHEN 'Epic' THEN 0 ELSE 1 END, jira_ticket_id
        """,
        (run_id,),
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
