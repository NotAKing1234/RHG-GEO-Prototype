#!/usr/bin/env python3
"""Stable dashboard domain rules for normalized GEO run data.

Runs provide records. This module provides behavior: readiness, coverage buckets,
warnings, and handoff copy rules that should stay stable across run contents.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


CHANGE_SUGGESTION_LABELS = {
    "html_visibility": "Access / crawlability",
    "metadata_update": "Metadata",
    "schema_update": "Schema",
    "content_update": "Content / copy",
    "trust_distribution": "Trust / distribution",
}
CHANGE_TYPE_ORDER = tuple(CHANGE_SUGGESTION_LABELS)

IMPLEMENTATION_READY = "Implementation-ready"
NEEDS_REVIEW = "Need review"
READY_TO_SEND = "ready-to-send"
NEEDS_REVIEW_STATUS = "needs-review"


@dataclass(frozen=True)
class DomainRun:
    run_id: str
    date: str = ""
    status: str = ""


@dataclass(frozen=True)
class DomainPage:
    canonical_url: str
    page_type: str = ""
    fetch_status: str = ""


@dataclass(frozen=True)
class DomainGap:
    gap_id: str
    severity: int = 0
    status: str = ""


@dataclass(frozen=True)
class DomainProposal:
    proposal_id: str
    proposed_change: str = ""
    priority_tier: str = ""
    evidence_source_ids: tuple[int, ...] = ()


@dataclass(frozen=True)
class DomainSource:
    source_id: int
    title_or_url: str = ""
    url: str = ""


@dataclass(frozen=True)
class DomainChange:
    change_id: str
    proposal_id: str
    change_type: str
    target_page: str = ""
    target_field_or_section: str = ""


@dataclass(frozen=True)
class HandoffAsset:
    asset: str
    status: str
    notes: str = ""


@dataclass(frozen=True)
class ValidationWarning:
    code: str
    message: str
    severity: str = "warning"
    entity_type: str = "run"
    entity_id: str = ""


@dataclass(frozen=True)
class ReadinessResult:
    status: str
    evidence_tier: str
    blockers: tuple[str, ...] = ()

    @property
    def ready(self) -> bool:
        return self.status == READY_TO_SEND


def warning_to_dict(warning: ValidationWarning) -> dict[str, str]:
    return asdict(warning)


def normalize_change_type(value: Any) -> str:
    change_type = str(value or "").strip()
    if change_type in CHANGE_SUGGESTION_LABELS:
        return change_type
    return "content_update"


def priority_score(priority_tier: str | None, severity: int | None, source_count: int) -> int:
    base = {"P1": 88, "P2": 72, "P3": 55}.get((priority_tier or "P3").upper(), 48)
    severity_boost = max(0, int(severity or 0) - 1) * 3
    evidence_boost = min(4, source_count)
    return min(99, base + severity_boost + evidence_boost)


def selector_status_for(change_type: str | None, target_page: str | None) -> str:
    normalized = normalize_change_type(change_type)
    if normalized in {"schema_update", "metadata_update"}:
        return "metadata field target"
    if target_page:
        return "team override selector"
    return "warning: selector not inferred"


def surface_for(change_type: str | None, fallback: str | None) -> str:
    normalized = normalize_change_type(change_type)
    if normalized == "schema_update":
        return "Metadata / Structured Data"
    if normalized == "metadata_update":
        return "Metadata"
    if normalized == "html_visibility":
        return "Strategic / Infrastructure"
    if normalized == "trust_distribution":
        return "Trust / Distribution"
    return fallback or "Front-end content"


def evidence_tier_for(evidence_source_ids: list[int] | tuple[int, ...] | None) -> str:
    return IMPLEMENTATION_READY if evidence_source_ids else NEEDS_REVIEW


def has_selector_warning(selector_status: Any) -> bool:
    return str(selector_status or "").lower().startswith("warning")


def handoff_readiness_for(rec: dict[str, Any]) -> ReadinessResult:
    blockers: list[str] = []
    ticket = rec.get("jira_ticket") or {}
    evidence_ids = rec.get("evidence_source_ids") or []
    selector_status = str(rec.get("selector_status") or "")
    if not str(rec.get("proposed_change") or "").strip():
        blockers.append("missing proposed change")
    if not ticket.get("summary") or not ticket.get("description"):
        blockers.append("missing Jira ticket fields")
    if not evidence_ids:
        blockers.append("missing linked evidence")
    if has_selector_warning(selector_status):
        blockers.append(selector_status)
    return ReadinessResult(
        status=READY_TO_SEND if not blockers else NEEDS_REVIEW_STATUS,
        evidence_tier=evidence_tier_for(evidence_ids),
        blockers=tuple(blockers),
    )


def change_suggestion_summary(recs: list[dict[str, Any]], changes: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {key: 0 for key in CHANGE_TYPE_ORDER}
    seen: set[str] = set()
    if changes:
        for item in changes:
            field_name = item.get("target_field_or_section") or item.get("field_name") or ""
            key = str(item.get("change_id") or item.get("metadata_change_id") or f"{item.get('proposal_id')}:{field_name}")
            if key in seen:
                continue
            seen.add(key)
            counts[normalize_change_type(item.get("change_type") or item.get("format_type"))] += 1
    else:
        for item in recs:
            key = str(item.get("proposal_id") or "")
            if key in seen:
                continue
            seen.add(key)
            counts[normalize_change_type(item.get("change_type"))] += 1
    return {
        "total": len(seen),
        "by_type": counts,
        "labels": dict(CHANGE_SUGGESTION_LABELS),
    }


def validation_warnings_for(
    run: dict[str, Any] | None,
    recs: list[dict[str, Any]],
    source_values: list[dict[str, Any]],
    page_values: list[dict[str, Any]],
    changes: list[dict[str, Any]],
) -> list[ValidationWarning]:
    run_id = str((run or {}).get("run_id") or "")
    warnings: list[ValidationWarning] = []
    if not run:
        warnings.append(ValidationWarning("missing_run", "Run metadata is missing.", "error", "run", run_id))
    if not source_values:
        warnings.append(ValidationWarning("missing_sources", "No sources imported for this run.", "error", "run", run_id))
    if not recs:
        warnings.append(ValidationWarning("missing_proposals", "No proposals imported for this run.", "error", "run", run_id))
    if recs and not changes:
        warnings.append(
            ValidationWarning(
                "missing_normalized_changes",
                "No normalized proposal changes were imported; coverage falls back to generic content changes.",
                "warning",
                "run",
                run_id,
            )
        )
    if recs and not page_values:
        warnings.append(ValidationWarning("missing_pages", "No audited pages are available for this run.", "warning", "run", run_id))
    for item in changes:
        change_type = str(item.get("raw_change_type") if "raw_change_type" in item else item.get("change_type") or "")
        change_id = str(item.get("metadata_change_id") or item.get("change_id") or "")
        if change_type not in CHANGE_SUGGESTION_LABELS:
            warnings.append(
                ValidationWarning(
                    "unknown_change_type",
                    f"Change {change_id or '[unknown]'} has unknown change_type {change_type or '[blank]'}; treated as content_update.",
                    "warning",
                    "change",
                    change_id,
                )
            )
    for rec in recs:
        readiness = handoff_readiness_for(rec)
        if readiness.blockers:
            warnings.append(
                ValidationWarning(
                    "proposal_needs_review",
                    f"Proposal {rec.get('proposal_id') or '[unknown]'} needs review: {'; '.join(readiness.blockers)}.",
                    "warning",
                    "proposal",
                    str(rec.get("proposal_id") or ""),
                )
            )
    return warnings


def validation_error_messages(warnings: list[ValidationWarning]) -> list[str]:
    return [item.message for item in warnings if item.severity == "error"]


def sorted_handoff_rows(recommendation_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    priority_rank = {"P1": 0, "Highest": 0, "P2": 1, "High": 1, "P3": 2, "Medium": 2}
    return sorted(
        recommendation_rows,
        key=lambda row: (
            row.get("status") != READY_TO_SEND,
            priority_rank.get(str(row.get("priority") or ""), 9),
            str(row.get("display_id") or row.get("proposal_id") or ""),
        ),
    )


def top_priority_sentence(recommendation_rows: list[dict[str, Any]]) -> str:
    sorted_rows = sorted_handoff_rows(recommendation_rows)
    if not sorted_rows:
        return "No recommendations are currently ready for handoff; review the validation warnings before sending."
    top = sorted_rows[0]
    title = str(top.get("title") or top.get("display_id") or "the highest-priority recommendation").strip()
    suffix = "" if top.get("status") == READY_TO_SEND else " once review blockers are resolved"
    return f"Top priority is {title}{suffix}."


def stakeholder_email_lines(run_id: str, ready_count: int, recommendation_rows: list[dict[str, Any]]) -> list[str]:
    return [
        f"# Stakeholder Email Draft - {run_id}",
        "",
        f"Subject: GEO optimization handoff for {run_id} - {ready_count} recommendations ready",
        "",
        "Hi team,",
        "",
        f"Attached is the GEO optimization handoff for {run_id}. It includes the Jira import CSV, a recommendation tracker, source evidence, page coverage, metadata/copy change exports, and per-recommendation briefs with acceptance checklists.",
        "",
        top_priority_sentence(recommendation_rows),
        "",
        "Please review ownership/component fields before importing the Jira CSV if your team uses a different routing model.",
    ]
