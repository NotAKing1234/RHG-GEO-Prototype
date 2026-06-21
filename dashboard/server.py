#!/usr/bin/env python3
"""Local API server for the DB-backed Radisson GEO Optimizer dashboard.

Data flow: dashboard reads URL registry state from SQLite and writes selection back to
urls.selected_for_next_run. Pitfalls: next_geo_run.csv and Jira CSV are generated exports,
not dashboard-owned source files.
"""

from __future__ import annotations

import json
import mimetypes
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


DASHBOARD_ROOT = Path(__file__).resolve().parent
REPO_ROOT = DASHBOARD_ROOT.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts import db  # noqa: E402
from scripts.export import export_all, jira_csv_content  # noqa: E402
from scripts.migrate_to_sqlite import migrate  # noqa: E402


GEO_DB_PATH = db.DB_PATH
JIRA_CSV_FIELDS = db.JIRA_FIELDS
MAX_ACTIVE_TARGETS_FOR_RUN_SCOPE = 500

MODEL_PRICES_PER_MILLION = {
    "gpt-5.4-mini": {"input": 0.75, "output": 4.50},
    "gpt-5.4": {"input": 2.50, "output": 15.00},
    "gpt-5.5": {"input": 5.00, "output": 30.00},
    "gpt-5.3-codex": {"input": 1.75, "output": 14.00},
}
AUDIT_PROFILES = {
    "metadata_light": {
        "label": "Metadata light",
        "input_tokens_per_url": 1500,
        "output_tokens_per_url": 300,
        "description": "Metadata, sitemap fields, and focused GEO checks.",
    },
    "page_summary": {
        "label": "Page summary",
        "input_tokens_per_url": 3000,
        "output_tokens_per_url": 500,
        "description": "Rendered/page excerpt summary plus metadata check.",
    },
    "full_page_medium": {
        "label": "Full page medium",
        "input_tokens_per_url": 10000,
        "output_tokens_per_url": 750,
        "description": "Medium full-page text pass for deeper content auditing.",
    },
}


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def ensure_db() -> None:
    if not GEO_DB_PATH.exists():
        result = migrate(GEO_DB_PATH)
        if not result["valid"]:
            raise RuntimeError(f"Migration validation failed: {result['mismatches']}")


def estimate_registry_cost(row_count: int, profile_id: str, model_id: str) -> dict[str, Any]:
    profile = AUDIT_PROFILES.get(profile_id) or AUDIT_PROFILES["metadata_light"]
    model = MODEL_PRICES_PER_MILLION.get(model_id) or MODEL_PRICES_PER_MILLION["gpt-5.4-mini"]
    input_tokens = row_count * int(profile["input_tokens_per_url"])
    output_tokens = row_count * int(profile["output_tokens_per_url"])
    input_cost = (input_tokens / 1_000_000) * model["input"]
    output_cost = (output_tokens / 1_000_000) * model["output"]
    return {
        "row_count": row_count,
        "profile_id": profile_id if profile_id in AUDIT_PROFILES else "metadata_light",
        "profile": profile,
        "model_id": model_id if model_id in MODEL_PRICES_PER_MILLION else "gpt-5.4-mini",
        "model_prices_per_million": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "input_cost_usd": round(input_cost, 2),
        "output_cost_usd": round(output_cost, 2),
        "total_cost_usd": round(input_cost + output_cost, 2),
        "batch_total_cost_usd_estimate": round((input_cost + output_cost) * 0.5, 2),
    }


def registry_filter_from_query(query: dict[str, list[str]]) -> dict[str, str]:
    return {
        "query": query.get("query", [""])[0].strip(),
        "brand": query.get("brand", ["all"])[0] or "all",
        "region": query.get("region", ["all"])[0] or "all",
        "page_type": query.get("page_type", ["all"])[0] or "all",
        "location_confidence": query.get("location_confidence", ["all"])[0] or "all",
        "audit_profile": query.get("audit_profile", ["metadata_light"])[0] or "metadata_light",
        "model": query.get("model", ["gpt-5.4-mini"])[0] or "gpt-5.4-mini",
    }


def registry_filter_from_payload(payload: dict[str, Any]) -> dict[str, str]:
    values = payload.get("filters") if isinstance(payload.get("filters"), dict) else payload
    return {
        "query": str(values.get("query") or "").strip(),
        "brand": str(values.get("brand") or "all"),
        "region": str(values.get("region") or "all"),
        "page_type": str(values.get("page_type") or "all"),
        "location_confidence": str(values.get("location_confidence") or "all"),
        "audit_profile": str(values.get("audit_profile") or "metadata_light"),
        "model": str(values.get("model") or "gpt-5.4-mini"),
    }


def has_active_registry_filter(filters: dict[str, str]) -> bool:
    exact_fields = ["brand", "region", "page_type", "location_confidence"]
    return bool(filters.get("query")) or any(filters.get(field, "all") != "all" for field in exact_fields)


def registry_options(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    options: dict[str, list[dict[str, Any]]] = {}
    for field in ["brand", "region", "page_type", "location_confidence"]:
        counts: dict[str, int] = {}
        for row in rows:
            value = str(row.get(field) or "Unspecified")
            counts[value] = counts.get(value, 0) + 1
        options[field] = [
            {"value": value, "label": value, "count": count}
            for value, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        ]
    return options


def read_url_registry(filters: dict[str, str] | None = None) -> list[dict[str, Any]]:
    ensure_db()
    with db.connection(GEO_DB_PATH) as conn:
        values = db.list_urls(conn, filters)
    for value in values:
        value["selected_for_next_run"] = bool(value.get("selected_for_next_run"))
    return values


def registry_payload(filters: dict[str, str], *, limit: int = 250, offset: int = 0) -> dict[str, Any]:
    rows = read_url_registry(filters)
    all_rows = read_url_registry({})
    selected_count = sum(1 for row in all_rows if row.get("selected_for_next_run"))
    return {
        "registry_path": "db/geo_optimizer.db:urls",
        "registry_source": "sqlite",
        "registry_source_label": "SQLite URL registry",
        "registry_missing": False,
        "next_run_path": "sources/website/run_targets/next_geo_run.csv",
        "total_records": len(all_rows),
        "filtered_count": len(rows),
        "selected_count": selected_count,
        "filters": filters,
        "options": registry_options(all_rows),
        "audit_profiles": AUDIT_PROFILES,
        "model_prices_per_million": MODEL_PRICES_PER_MILLION,
        "cost_estimate": estimate_registry_cost(len(rows), filters.get("audit_profile", "metadata_light"), filters.get("model", "gpt-5.4-mini")),
        "rows": rows[offset : offset + limit],
        "limit": limit,
        "offset": offset,
    }


def save_registry_selection(payload: dict[str, Any]) -> dict[str, Any]:
    ensure_db()
    filters = registry_filter_from_payload(payload)
    has_explicit_selection = "selected_urls" in payload
    explicit_urls = [str(url) for url in payload.get("selected_urls", []) if url]
    with db.connection(GEO_DB_PATH) as conn:
        if has_explicit_selection:
            result = db.set_selected_urls(conn, explicit_urls)
        else:
            if not has_active_registry_filter(filters):
                raise ValueError("Refusing to save the entire registry as the next run. Choose filters or selected URLs first.")
            candidate_count = len(db.list_urls(conn, filters))
            if candidate_count > MAX_ACTIVE_TARGETS_FOR_RUN_SCOPE and not payload.get("confirm_large_selection"):
                raise ValueError(
                    f"Selection contains {candidate_count} URLs. Refusing to write more than "
                    f"{MAX_ACTIVE_TARGETS_FOR_RUN_SCOPE} without confirm_large_selection=true."
                )
            result = db.set_selected_by_filters(conn, filters)
    return {
        "next_run_path": "sources/website/run_targets/next_geo_run.csv",
        "selected_count": result.selected_count,
        "selection_mode": result.selection_mode,
        "filters": filters,
        "cost_estimate": estimate_registry_cost(result.selected_count, filters.get("audit_profile", "metadata_light"), filters.get("model", "gpt-5.4-mini")),
    }


def export_jira_csv(run_id: str, data: dict[str, Any] | None = None, proposal_id: str | None = None) -> dict[str, Any]:
    ensure_db()
    with db.connection(GEO_DB_PATH) as conn:
        content = jira_csv_content(conn, run_id)
    return {"type": "jira_csv", "filename": f"{run_id}_jira_import.csv", "content": content, "fields": JIRA_CSV_FIELDS}


def export_dashboard(run_id: str, export_type: str, proposal_id: str | None = None) -> dict[str, Any]:
    ensure_db()
    if export_type == "jira_csv":
        return export_jira_csv(run_id, proposal_id=proposal_id)
    if export_type == "json":
        with db.connection(GEO_DB_PATH) as conn:
            payload = {"tables": db.table_counts(conn), "urls": db.list_urls(conn)}
        return {"type": "json", "filename": f"{run_id}_dashboard.json", "content": json.dumps(payload, indent=2)}
    export_all(run_id, GEO_DB_PATH)
    return {"type": export_type, "filename": f"{run_id}_{export_type}.txt", "content": f"Exports regenerated for {run_id}."}


class DashboardHandler(BaseHTTPRequestHandler):
    def send_json(self, payload: Any, status: int = 200) -> None:
        body = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_error_json(self, message: str, status: int = 400) -> None:
        self.send_json({"error": message}, status=status)

    def serve_static(self, path: str) -> None:
        target = (DASHBOARD_ROOT / (path.lstrip("/") or "index.html")).resolve()
        if target.is_dir():
            target = target / "index.html"
        if DASHBOARD_ROOT.resolve() not in target.parents and target != DASHBOARD_ROOT.resolve():
            self.send_error_json("Path escapes dashboard root", 403)
            return
        if not target.exists():
            self.send_error_json("Not found", 404)
            return
        body = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(str(target))[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if not length:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        try:
            if parsed.path == "/api/status":
                ensure_db()
                with db.connection(GEO_DB_PATH) as conn:
                    self.send_json({"status": "ok", "db_path": rel(GEO_DB_PATH), "tables": db.table_counts(conn)})
            elif parsed.path == "/api/url-registry":
                limit = int(query.get("limit", ["250"])[0])
                offset = int(query.get("offset", ["0"])[0])
                self.send_json(registry_payload(registry_filter_from_query(query), limit=limit, offset=offset))
            elif parsed.path == "/api/dashboard/export":
                run_id = query.get("run_id", query.get("runId", ["run_003"]))[0]
                export_type = query.get("type", ["json"])[0]
                proposal_id = query.get("proposal_id", query.get("proposalId", [None]))[0]
                self.send_json(export_dashboard(run_id, export_type, proposal_id=proposal_id))
            else:
                self.serve_static(parsed.path)
        except Exception as exc:
            self.send_error_json(str(exc), 500)

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        try:
            if parsed.path == "/api/url-registry/selection":
                self.send_json(save_registry_selection(self.read_body()))
            else:
                self.send_error_json("Not found", 404)
        except Exception as exc:
            self.send_error_json(str(exc), 400)

    def log_message(self, format: str, *args: Any) -> None:
        return


def main() -> int:
    ensure_db()
    server = ThreadingHTTPServer(("127.0.0.1", 8787), DashboardHandler)
    print("Dashboard API server listening on http://127.0.0.1:8787")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
