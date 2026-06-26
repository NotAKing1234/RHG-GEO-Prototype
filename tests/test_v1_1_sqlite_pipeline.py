import csv
import io
import tempfile
import unittest
from pathlib import Path

import dashboard.server as dashboard_server
from scripts import db
from scripts.dashboard_domain import CHANGE_SUGGESTION_LABELS, READY_TO_SEND
from scripts.dashboard_read_model import capture_page, csv_export, dashboard_payload
from scripts.export import csv_content, export_all, export_ready_to_send_bundle, jira_csv_content, validate_jira_csv_file, write_next_geo_run
from scripts.import_run_artifacts import import_all_runs, import_proposal_change
from scripts.import_url_registry import import_registry_rows
from scripts.migrate_to_sqlite import migrate


def seed_contract_run(
    conn,
    *,
    run_id: str,
    run_number: int,
    url: str,
    brand: str,
    page_type: str,
    change_type: str,
    proposed_change: str,
    current_state: str = "Current normalized state is incomplete.",
    with_source: bool = True,
) -> int:
    proposal_id = run_number * 1000 + 1
    db.upsert_run(conn, run_id, run_number, "2026-06-24", "COMPLETED")
    url_id = db.upsert_url(conn, url, brand=brand, page_type=page_type)
    conn.execute(
        """
        INSERT INTO metadata_snapshots(run_id, url_id, page_label, title, meta_description, fetch_status, captured_at)
        VALUES(?, ?, ?, ?, ?, ?, ?)
        """,
        (run_id, url_id, brand, f"{brand} title", "Description", "http_200", "2026-06-24T00:00:00Z"),
    )
    criterion_id = db.upsert_criterion(conn, run_id, "C01", "Pages must expose normalized implementation details.")
    db.upsert_gap(
        conn,
        f"GAP-{run_number}",
        run_id,
        url_id=url_id,
        criterion_id=criterion_id,
        gap_type="MISSING",
        severity=3,
        status="NEW",
        description=current_state,
    )
    db.upsert_proposal(
        conn,
        proposal_id,
        f"GAP-{run_number}",
        run_id,
        source_proposal_id="PROP-001",
        proposed_change=proposed_change,
        source_citation="C01",
        current_state=current_state,
        implementation_status="N/A",
        priority_tier="P1",
        impact_estimate="High.",
    )
    conn.execute(
        """
        INSERT INTO proposal_changes(
            change_id, proposal_id, run_id, change_type, target_page,
            target_field_or_section, current_value, proposed_value, warning
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, '')
        """,
        (
            f"{run_id}:{proposal_id}:primary",
            proposal_id,
            run_id,
            change_type,
            url,
            "Normalized target field",
            current_state,
            proposed_change,
        ),
    )
    if with_source:
        source_id = db.upsert_source(
            conn,
            run_id=run_id,
            source_key=f"{run_id}:source:1",
            url="https://example.com/source",
            domain="example.com",
            title="Contract fixture source",
            source_type="gap_research",
            related_gaps=[f"GAP-{run_number}"],
            related_recommendations=[str(proposal_id)],
        )
        conn.execute(
            "INSERT INTO proposal_sources(proposal_id, source_id, run_id, role) VALUES(?, ?, ?, ?)",
            (proposal_id, source_id, run_id, "evidence"),
        )
    db.build_jira_tickets(conn, run_id)
    return proposal_id


class SqlitePipelineTests(unittest.TestCase):
    def test_schema_loads_all_spec_tables_with_foreign_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            db.initialize_database(db_path)
            with db.connection(db_path) as conn:
                self.assertEqual(set(db.TABLES), set(db.table_names(conn)) & set(db.TABLES))
                for table in db.TABLES:
                    conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
                self.assertIn("run_artifacts", db.table_names(conn))
                self.assertIn("metadata_snapshots", db.table_names(conn))
                self.assertIn("run_url_targets", db.table_names(conn))
                self.assertIn("source_key", db.table_columns(conn, "sources"))
                self.assertIn("country", db.table_columns(conn, "urls"))
                self.assertEqual(conn.execute("PRAGMA foreign_keys").fetchone()[0], 1)

    def test_migration_is_idempotent_and_matches_parsed_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            first = migrate(db_path)
            second = migrate(db_path)
            self.assertTrue(first["valid"], first)
            self.assertTrue(second["valid"], second)
            self.assertEqual(first["actual_counts"], second["actual_counts"])
            for table in ("runs", "urls", "criteria", "gaps", "proposals"):
                self.assertEqual(second["parsed_counts"][table], second["actual_counts"][table])

    def test_artifact_import_is_idempotent_and_populates_dashboard_tables(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            first = import_all_runs(db_path)
            second = import_all_runs(db_path)
            self.assertEqual(first["counts"], second["counts"])
            self.assertGreater(second["counts"]["run_artifacts"], 0)
            self.assertGreater(second["counts"]["sources"], 0)
            self.assertGreater(second["counts"]["source_insights"], 0)
            self.assertGreater(second["counts"]["gap_insights"], 0)
            self.assertGreater(second["counts"]["metadata_snapshots"], 0)
            self.assertGreater(second["counts"]["proposal_changes"], 0)
            self.assertGreater(second["counts"]["proposal_sources"], 0)
            with db.connection(db_path) as conn:
                run_004_links = conn.execute(
                    """
                    SELECT COUNT(*)
                    FROM proposal_sources ps
                    JOIN proposals p ON p.proposal_id = ps.proposal_id
                    WHERE p.run_id = 'run_004'
                    """
                ).fetchone()[0]
                run_004_payload = dashboard_payload(conn, "run_004")
                run_005_target_count = conn.execute(
                    "SELECT COUNT(*) FROM run_url_targets WHERE run_id = 'run_005'"
                ).fetchone()[0]
                run_005_snapshot_count = conn.execute(
                    "SELECT COUNT(*) FROM metadata_snapshots WHERE run_id = 'run_005'"
                ).fetchone()[0]
            self.assertGreater(run_004_links, 0)
            self.assertGreater(run_004_payload["summary"]["ready_to_send"], 0)
            self.assertEqual(run_004_payload["summary"]["evidence_sources"], run_004_payload["summary"]["sources"])
            self.assertEqual(
                run_004_payload["summary"]["reviewed_inputs"],
                run_004_payload["summary"]["pages"] + run_004_payload["summary"]["evidence_sources"],
            )
            self.assertGreater(run_004_payload["summary"]["reviewed_inputs"], run_004_payload["summary"]["sources"])
            self.assertGreater(run_005_target_count, 0)
            self.assertEqual(run_005_target_count, run_005_snapshot_count)

    def test_dashboard_payload_preserves_frontend_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            import_all_runs(db_path)
            with db.connection(db_path) as conn:
                payload = dashboard_payload(conn, "run_003")
                historical_payloads = {run_id: dashboard_payload(conn, run_id) for run_id in ("run_001", "run_002", "run_003", "run_004")}
            self.assertEqual(payload["run"]["run_id"], "run_003")
            self.assertGreater(len(payload["recommendations"]), 0)
            self.assertGreater(len(payload["sources"]), 0)
            self.assertGreater(len(payload["radisson_pages"]), 0)
            first = payload["recommendations"][0]
            for key in ("proposal_id", "title", "page_refs", "evidence_source_ids", "jira_ticket", "team_override"):
                self.assertIn(key, first)
            source = payload["sources"][0]
            for key in ("source_id", "title_or_url", "scorecard", "related_recommendations"):
                self.assertIn(key, source)
            for run_id, historical in historical_payloads.items():
                self.assertEqual(historical["run"]["run_id"], run_id)
                self.assertIn("validation_errors", historical["run"])
                self.assertIn("validation_warnings", historical["run"])
                self.assertEqual(historical["summary"]["change_suggestions"]["labels"], CHANGE_SUGGESTION_LABELS)
                self.assertIn("evidence_sources", historical["summary"])
                self.assertIn("reviewed_inputs", historical["summary"])
                self.assertEqual(historical["summary"]["evidence_sources"], historical["summary"]["sources"])
                self.assertEqual(
                    historical["summary"]["reviewed_inputs"],
                    historical["summary"]["pages"] + historical["summary"]["evidence_sources"],
                )
                for rec in historical["recommendations"]:
                    self.assertIn("handoff_status", rec)
                    self.assertIn("readiness_blockers", rec)

    def test_dashboard_payload_counts_change_suggestion_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            db.initialize_database(db_path)
            with db.connection(db_path) as conn:
                db.upsert_run(conn, "run_999", 999, "2026-06-24", "IN_PROGRESS")
                url_id = db.upsert_url(conn, "https://example.com/radisson", brand="Radisson", page_type="brand")
                db.upsert_gap(
                    conn,
                    "GAP-999",
                    "run_999",
                    url_id=url_id,
                    criterion_id=None,
                    gap_type="WEAK",
                    severity=3,
                    status="NEW",
                    description="The page needs metadata and structured data fixes.",
                )
                db.upsert_proposal(
                    conn,
                    999,
                    "GAP-999",
                    "run_999",
                    proposed_change="Restore HTTP 200 access, add title/meta copy, and add Hotel JSON-LD.",
                    priority_tier="P1",
                    impact_estimate="High.",
                )
                conn.execute(
                    """
                    INSERT INTO proposal_changes(
                        change_id, proposal_id, run_id, change_type, target_page,
                        target_field_or_section, current_value, proposed_value, warning
                    )
                    VALUES('run_999:999:primary', 999, 'run_999', 'html_visibility', ?, 'Crawler or rendered HTML access', '', ?, '')
                    """,
                    (
                        "https://example.com/radisson",
                        "Restore HTTP 200 access, add title/meta copy, and add Hotel JSON-LD.",
                    ),
                )
                conn.execute(
                    """
                    INSERT INTO proposal_changes(
                        change_id, proposal_id, run_id, change_type, target_page,
                        target_field_or_section, current_value, proposed_value, warning
                    )
                    VALUES('run_999:999:schema', 999, 'run_999', 'schema_update', ?, 'Structured data / JSON-LD', '', ?, '')
                    """,
                    (
                        "https://example.com/radisson",
                        "Add Hotel JSON-LD.",
                    ),
                )
                payload = dashboard_payload(conn, "run_999")
            suggestions = payload["summary"]["change_suggestions"]
            self.assertEqual(suggestions["total"], 2)
            self.assertEqual(suggestions["by_type"]["html_visibility"], 1)
            self.assertEqual(suggestions["by_type"]["metadata_update"], 0)
            self.assertEqual(suggestions["by_type"]["schema_update"], 1)
            self.assertEqual(suggestions["by_type"]["content_update"], 0)

    def test_dashboard_payload_uses_normalized_change_types_across_synthetic_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            db.initialize_database(db_path)
            with db.connection(db_path) as conn:
                seed_contract_run(
                    conn,
                    run_id="run_901",
                    run_number=901,
                    url="https://example.com/country-inn",
                    brand="Country Inn",
                    page_type="hotel",
                    change_type="html_visibility",
                    proposed_change="Restore blocked Country Inn crawlability, add schema, title copy, and review feed references.",
                )
                seed_contract_run(
                    conn,
                    run_id="run_902",
                    run_number=902,
                    url="https://example.com/park-plaza",
                    brand="Park Plaza",
                    page_type="brand",
                    change_type="trust_distribution",
                    proposed_change="Add Park Plaza review distribution handoff details.",
                )
                country_payload = dashboard_payload(conn, "run_901")
                park_payload = dashboard_payload(conn, "run_902")
            for payload in (country_payload, park_payload):
                self.assertEqual(payload["summary"]["change_suggestions"]["labels"], CHANGE_SUGGESTION_LABELS)
                self.assertEqual(payload["summary"]["ready_to_send"], 1)
                self.assertEqual(payload["summary"]["pages"], 1)
                self.assertEqual(payload["summary"]["evidence_sources"], 1)
                self.assertEqual(payload["summary"]["sources"], 1)
                self.assertEqual(payload["summary"]["reviewed_inputs"], 2)
                self.assertEqual(payload["recommendations"][0]["handoff_status"], READY_TO_SEND)
            country_counts = country_payload["summary"]["change_suggestions"]["by_type"]
            park_counts = park_payload["summary"]["change_suggestions"]["by_type"]
            self.assertEqual(country_counts["html_visibility"], 1)
            self.assertEqual(country_counts["schema_update"], 0)
            self.assertEqual(country_counts["metadata_update"], 0)
            self.assertEqual(country_counts["trust_distribution"], 0)
            self.assertEqual(park_counts["trust_distribution"], 1)
            self.assertEqual(park_counts["html_visibility"], 0)

    def test_import_proposal_change_falls_back_to_gap_url_for_target_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            db.initialize_database(db_path)
            with db.connection(db_path) as conn:
                db.upsert_run(conn, "run_999", 999, "2026-06-24", "IN_PROGRESS")
                url_id = db.upsert_url(conn, "https://example.com/radisson", brand="Radisson", page_type="brand")
                db.upsert_gap(
                    conn,
                    "GAP-999",
                    "run_999",
                    url_id=url_id,
                    criterion_id=None,
                    gap_type="WEAK",
                    severity=3,
                    status="NEW",
                    description="The page needs schema fixes.",
                )
                db.upsert_proposal(
                    conn,
                    999,
                    "GAP-999",
                    "run_999",
                    proposed_change="Add Hotel JSON-LD with address and booking URL.",
                    priority_tier="P1",
                    impact_estimate="High.",
                )
                import_proposal_change(
                    conn,
                    "run_999",
                    {
                        "proposal_id": 999,
                        "gap_id": "GAP-999",
                        "proposed_change": "Add Hotel JSON-LD with address and booking URL.",
                    },
                    {"current_state": "No Hotel schema is present."},
                )
                target_page = conn.execute(
                    "SELECT target_page FROM proposal_changes WHERE change_id = 'run_999:999:primary'"
                ).fetchone()[0]
            self.assertEqual(target_page, "https://example.com/radisson")

    def test_import_proposal_change_classifies_review_markup_as_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            db.initialize_database(db_path)
            with db.connection(db_path) as conn:
                db.upsert_run(conn, "run_906", 906, "2026-06-24", "IN_PROGRESS")
                db.upsert_gap(
                    conn,
                    "GAP-906",
                    "run_906",
                    url_id=None,
                    criterion_id=None,
                    gap_type="MISSING",
                    severity=3,
                    status="NEW",
                    description="Review markup is missing.",
                )
                db.upsert_proposal(
                    conn,
                    906001,
                    "GAP-906",
                    "run_906",
                    proposed_change="Add aggregateRating/Review JSON-LD markup with review count and rating.",
                    priority_tier="P1",
                    impact_estimate="High.",
                )
                import_proposal_change(
                    conn,
                    "run_906",
                    {
                        "proposal_id": 906001,
                        "gap_id": "GAP-906",
                        "proposed_change": "Add aggregateRating/Review JSON-LD markup with review count and rating.",
                    },
                    {"current_state": "Review pages exist but valid review markup is missing."},
                )
                change_type = conn.execute(
                    "SELECT change_type FROM proposal_changes WHERE change_id = 'run_906:906001:primary'"
                ).fetchone()[0]
            self.assertEqual(change_type, "schema_update")

    def test_incomplete_normalized_run_data_returns_structured_warnings(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            db.initialize_database(db_path)
            with db.connection(db_path) as conn:
                db.upsert_run(conn, "run_903", 903, "2026-06-24", "COMPLETED")
                db.upsert_gap(
                    conn,
                    "GAP-903",
                    "run_903",
                    url_id=None,
                    criterion_id=None,
                    gap_type="MISSING",
                    severity=2,
                    status="NEW",
                    description="Proposal exists without normalized supporting records.",
                )
                db.upsert_proposal(
                    conn,
                    903001,
                    "GAP-903",
                    "run_903",
                    proposed_change="Add missing content.",
                    priority_tier="P2",
                    impact_estimate="Medium.",
                )
                payload = dashboard_payload(conn, "run_903")
            warning_codes = {item["code"] for item in payload["run"]["validation_warnings"]}
            self.assertIn("missing_sources", warning_codes)
            self.assertIn("missing_normalized_changes", warning_codes)
            self.assertIn("missing_pages", warning_codes)
            self.assertIn("proposal_needs_review", warning_codes)
            self.assertIn("No sources imported for this run.", payload["run"]["validation_errors"])
            self.assertEqual(payload["summary"]["change_suggestions"]["by_type"]["content_update"], 1)

    def test_normalized_change_target_page_and_raw_type_warnings_survive_adapter(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            db.initialize_database(db_path)
            with db.connection(db_path) as conn:
                db.upsert_run(conn, "run_905", 905, "2026-06-24", "COMPLETED")
                db.upsert_gap(
                    conn,
                    "GAP-905",
                    "run_905",
                    url_id=None,
                    criterion_id=None,
                    gap_type="MISSING",
                    severity=3,
                    status="NEW",
                    description="Widget markup is missing.",
                )
                db.upsert_proposal(
                    conn,
                    905001,
                    "GAP-905",
                    "run_905",
                    source_proposal_id="PROP-001",
                    proposed_change="Add an AI widget handoff to https://example.com/normalized-target.",
                    priority_tier="P1",
                    impact_estimate="High.",
                )
                conn.execute(
                    """
                    INSERT INTO proposal_changes(
                        change_id, proposal_id, run_id, change_type, target_page,
                        target_field_or_section, current_value, proposed_value, warning
                    )
                    VALUES('run_905:905001:primary', 905001, 'run_905', 'ai_widget', ?, 'Widget mount', '', 'Add widget handoff.', '')
                    """,
                    ("https://example.com/normalized-target",),
                )
                source_id = db.upsert_source(
                    conn,
                    run_id="run_905",
                    source_key="source:1",
                    url="https://example.com/source",
                    domain="example.com",
                    title="Widget source",
                    source_type="gap_research",
                    related_gaps=["GAP-905"],
                    related_recommendations=["905001"],
                )
                conn.execute(
                    "INSERT INTO proposal_sources(proposal_id, source_id, run_id, role) VALUES(?, ?, ?, ?)",
                    (905001, source_id, "run_905", "evidence"),
                )
                db.build_jira_tickets(conn, "run_905")
                payload = dashboard_payload(conn, "run_905")
            self.assertEqual(payload["recommendations"][0]["page_refs"], ["https://example.com/normalized-target"])
            self.assertEqual(payload["recommendations"][0]["selector_status"], "team override selector")
            self.assertEqual(payload["metadata_changes"][0]["change_type"], "content_update")
            self.assertEqual(payload["metadata_changes"][0]["raw_change_type"], "ai_widget")
            warning_codes = {item["code"] for item in payload["run"]["validation_warnings"]}
            self.assertIn("unknown_change_type", warning_codes)
            self.assertEqual(payload["summary"]["change_suggestions"]["by_type"]["content_update"], 1)

    def test_jira_export_header_and_priority_mapping(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            db.initialize_database(db_path)
            with db.connection(db_path) as conn:
                db.upsert_run(conn, "run_999", 999, "2026-06-21", "IN_PROGRESS")
                url_id = db.upsert_url(conn, "https://example.com/radisson", brand="Radisson Blu", page_type="brand")
                criterion_id = db.upsert_criterion(conn, "run_999", "C02", "FAQPage schema with conversational coverage")
                db.upsert_gap(
                    conn,
                    "GAP-999",
                    "run_999",
                    url_id=url_id,
                    criterion_id=criterion_id,
                    gap_type="MISSING",
                    severity=3,
                    status="NEW",
                    description="FAQ schema is missing from the brand page.",
                )
                db.upsert_proposal(
                    conn,
                    999,
                    "GAP-999",
                    "run_999",
                    proposed_change="Add FAQPage JSON-LD to the Radisson Blu brand page.",
                    priority_tier="P1",
                    impact_estimate="High citation impact.",
                )
                db.build_jira_tickets(conn, "run_999")
                rows = list(csv.reader(io.StringIO(jira_csv_content(conn, "run_999"))))
            self.assertEqual(rows[0], db.JIRA_FIELDS)
            self.assertEqual(rows[1][0], "Epic")
            self.assertEqual(rows[2][0], "Story")
            self.assertEqual(rows[2][4], "Highest")
            self.assertTrue(rows[2][5].startswith("GEO;"))
            self.assertIn(rows[2][6], {"Platform", "Discovery"})

    def test_csv_exports_escape_formula_like_cells(self):
        content = csv_content(["value"], [{"value": "=HYPERLINK(\"https://example.com\")"}])
        rows = list(csv.DictReader(io.StringIO(content)))
        self.assertEqual(rows[0]["value"], "'=HYPERLINK(\"https://example.com\")")

        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            db.initialize_database(db_path)
            with db.connection(db_path) as conn:
                db.upsert_run(conn, "run_999", 999, "2026-06-21", "IN_PROGRESS")
                db.upsert_gap(
                    conn,
                    "GAP-999",
                    "run_999",
                    url_id=None,
                    criterion_id=None,
                    gap_type="MISSING",
                    severity=3,
                    status="NEW",
                    description="Crawler access is blocked.",
                )
                db.upsert_proposal(
                    conn,
                    999,
                    "GAP-999",
                    "run_999",
                    proposed_change="Allow approved AI retrieval crawlers.",
                    priority_tier="P1",
                    impact_estimate="High.",
                )
                db.save_dashboard_override(
                    conn,
                    "run_999",
                    "999",
                    {"ticket_draft": {"summary": "=HYPERLINK(\"https://example.com\")"}},
                )
                db.build_jira_tickets(conn, "run_999")
                jira_rows = list(csv.DictReader(io.StringIO(jira_csv_content(conn, "run_999", proposal_id=999))))
        self.assertEqual(jira_rows[1]["Summary"], "'=HYPERLINK(\"https://example.com\")")

    def test_dashboard_csv_export_escapes_formula_like_cells(self):
        content = csv_export(
            {
                "recommendations": [
                    {
                        "proposal_id": "1",
                        "title": "=HYPERLINK(\"https://example.com\")",
                        "combined_score": 90,
                        "priority_tier": "P1",
                        "surface": "Metadata",
                        "page_refs": ["https://example.com/a"],
                        "evidence_source_ids": [1],
                        "proposed_change": "+SUM(1,2)",
                    }
                ]
            }
        )
        rows = list(csv.DictReader(io.StringIO(content)))
        self.assertEqual(rows[0]["title"], "'=HYPERLINK(\"https://example.com\")")
        self.assertEqual(rows[0]["proposed_change"], "'+SUM(1,2)")

    def test_capture_page_rejects_loopback_urls(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            db.initialize_database(db_path)
            with db.connection(db_path) as conn:
                db.upsert_run(conn, "run_999", 999, "2026-06-24", "IN_PROGRESS")
                with self.assertRaisesRegex(ValueError, "not allowed"):
                    capture_page(conn, "run_999", "http://127.0.0.1:9/private")
                url_count = conn.execute("SELECT COUNT(*) FROM urls").fetchone()[0]
            self.assertEqual(url_count, 0)

    def test_export_paths_reject_unsafe_run_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            db.initialize_database(db_path)
            with self.assertRaisesRegex(ValueError, "Invalid run_id"):
                export_all("../../tmp/outside", db_path)

    def test_dashboard_export_rejects_unknown_type_without_regeneration(self):
        with self.assertRaisesRegex(ValueError, "Unsupported dashboard export type"):
            dashboard_server.export_dashboard("run_999", "refresh")

    def test_dashboard_override_wins_in_jira_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            db.initialize_database(db_path)
            with db.connection(db_path) as conn:
                db.upsert_run(conn, "run_999", 999, "2026-06-21", "IN_PROGRESS")
                db.upsert_gap(
                    conn,
                    "GAP-999",
                    "run_999",
                    url_id=None,
                    criterion_id=None,
                    gap_type="MISSING",
                    severity=3,
                    status="NEW",
                    description="Crawler access is blocked.",
                )
                db.upsert_proposal(
                    conn,
                    999,
                    "GAP-999",
                    "run_999",
                    proposed_change="Allow approved AI retrieval crawlers.",
                    priority_tier="P1",
                    impact_estimate="High.",
                )
                db.save_dashboard_override(
                    conn,
                    "run_999",
                    "999",
                    {
                        "ticket_draft": {
                            "summary": "Custom reviewer summary",
                            "description": "Custom reviewer description",
                            "acceptance_criteria": ["Custom criterion one", "Custom criterion two"],
                        },
                        "ticket_internal_fields": {
                            "issue_type": "Improve Story",
                            "labels": ["GEO", "CrawlerAccess"],
                            "component": "Platform",
                        },
                    },
                )
                db.build_jira_tickets(conn, "run_999")
                rows = list(csv.DictReader(io.StringIO(jira_csv_content(conn, "run_999", proposal_id=999))))
            self.assertEqual(rows[1]["Issue Type"], "Improve Story")
            self.assertEqual(rows[1]["Summary"], "Custom reviewer summary")
            self.assertEqual(rows[1]["Description"], "Custom reviewer description")
            self.assertEqual(rows[1]["Labels"], "GEO;CrawlerAccess")
            self.assertIn("Custom criterion one", rows[1]["Acceptance Criteria"])

    def test_selection_flag_is_db_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            db.initialize_database(db_path)
            with db.connection(db_path) as conn:
                db.upsert_url(conn, "https://example.com/a", brand="Radisson", region="Europe")
                db.upsert_url(conn, "https://example.com/b", brand="Radisson Blu", region="North America")
                result = db.set_selected_by_filters(conn, {"region": "North America"})
                selected = db.selected_urls(conn)
            self.assertEqual(result.selected_count, 1)
            self.assertEqual([row["url"] for row in selected], ["https://example.com/b"])

    def test_registry_import_preserves_selection_and_filters_full_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            db.initialize_database(db_path)
            rows = [
                {
                    "normalized_url": "https://www.radissonhotels.com/en-us/brand/radisson-blu",
                    "brand": "Radisson Blu",
                    "region": "North America",
                    "country": "United States",
                    "locale": "en-us",
                    "content_group": "radisson-blu",
                    "page_type": "brand",
                    "location_source": "locale_fallback",
                    "location_confidence": "low",
                    "source_sitemap": "https://www.radissonhotels.com/en-us/sitemap-radisson-blu.xml",
                    "selected_for_next_run": "false",
                },
                {
                    "normalized_url": "https://www.radissonhotels.com/de-de/destination/germany/berlin",
                    "brand": "Radisson",
                    "locale_region": "Europe",
                    "locale_country": "Germany",
                    "locale": "de-de",
                    "content_group": "destinations",
                    "page_type": "destination",
                    "location_source": "locale_fallback",
                    "location_confidence": "low",
                    "source_sitemap": "https://www.radissonhotels.com/de-de/sitemap-destinations.xml",
                    "selected_for_next_run": "true",
                },
            ]
            with db.connection(db_path) as conn:
                db.upsert_url(conn, rows[0]["normalized_url"])
                db.set_selected_urls(conn, [rows[0]["normalized_url"]])
                first = import_registry_rows(conn, rows)
                second = import_registry_rows(conn, rows)
                selected = db.selected_urls(conn)
                country_rows = db.list_urls(conn, {"country": "Germany"})
                group_rows = db.list_urls(conn, {"content_group": "radisson-blu"})
                query_rows = db.list_urls(conn, {"query": "sitemap-destinations"})
            self.assertEqual(first["processed"], 2)
            self.assertEqual(second["processed"], 2)
            self.assertEqual([row["url"] for row in selected], [rows[0]["normalized_url"]])
            self.assertEqual([row["url"] for row in country_rows], [rows[1]["normalized_url"]])
            self.assertEqual([row["url"] for row in group_rows], [rows[0]["normalized_url"]])
            self.assertEqual([row["url"] for row in query_rows], [rows[1]["normalized_url"]])

    def test_next_run_selection_snapshots_to_run_targets_and_csv_view(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            db.initialize_database(db_path)
            csv_path = Path(tmp) / "next_geo_run.csv"
            with db.connection(db_path) as conn:
                db.upsert_run(conn, "run_999", 999, "2026-06-21", "IN_PROGRESS")
                db.upsert_url(conn, "https://example.com/a", brand="Radisson", region="Europe")
                db.upsert_url(conn, "https://example.com/b", brand="Radisson Blu", region="North America")
                result = db.set_selected_urls(conn, ["https://example.com/b"])
                db.record_selection_event(
                    conn,
                    action="save_next_run",
                    selection_mode=result.selection_mode,
                    selected_count=result.selected_count,
                    filters={"audit_profile": "metadata_light", "model": "gpt-5.4-mini"},
                    selected_url_values=result.selected_urls,
                )
                self.assertEqual(db.snapshot_next_run_targets(conn, "run_999"), 1)
                self.assertEqual(db.selected_urls(conn), [])
                targets = db.run_target_urls(conn, "run_999")
                write_next_geo_run(conn, csv_path, run_id="run_999")
            self.assertEqual([row["url"] for row in targets], ["https://example.com/b"])
            with csv_path.open(encoding="utf-8", newline="") as fh:
                exported = list(csv.DictReader(fh))
            self.assertEqual([row["url"] for row in exported], ["https://example.com/b"])

    def test_ready_to_send_bundle_exports_handoff_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            run_dir = Path(tmp) / "runs" / "run_999_2026-06-24"
            db.initialize_database(db_path)
            with db.connection(db_path) as conn:
                db.upsert_run(conn, "run_999", 999, "2026-06-24", "COMPLETED")
                url_id = db.upsert_url(conn, "https://example.com/radisson", brand="Radisson", page_type="hotel")
                criterion_id = db.upsert_criterion(conn, "run_999", "C01", "Pages must be crawlable and structured.")
                db.upsert_gap(
                    conn,
                    "GAP-999",
                    "run_999",
                    url_id=url_id,
                    criterion_id=criterion_id,
                    gap_type="MISSING",
                    severity=3,
                    status="NEW",
                    description="Hotel schema is missing.",
                )
                db.upsert_proposal(
                    conn,
                    999,
                    "GAP-999",
                    "run_999",
                    source_proposal_id="PROP-001",
                    proposed_change="Add Hotel JSON-LD with address, geo, amenities, and booking URL.",
                    source_citation="C01",
                    current_state="No Hotel schema is present.",
                    implementation_status="N/A",
                    priority_tier="P1",
                    impact_estimate="High.",
                )
                source_id = db.upsert_source(
                    conn,
                    run_id="run_999",
                    source_key="source:1",
                    url="https://schema.org/Hotel",
                    domain="schema.org",
                    title="Schema.org Hotel",
                    source_type="gap_research",
                    related_gaps=["GAP-999"],
                    related_recommendations=["999"],
                )
                conn.execute(
                    "INSERT INTO proposal_sources(proposal_id, source_id, run_id, role) VALUES(?, ?, ?, ?)",
                    (999, source_id, "run_999", "evidence"),
                )
                db.build_jira_tickets(conn, "run_999")
                written = export_ready_to_send_bundle(conn, "run_999", run_dir)
            ready_dir = run_dir / "ready-to-send"
            self.assertTrue((ready_dir / "README.md").exists())
            self.assertTrue((ready_dir / "recommendation-tracker.csv").exists())
            self.assertTrue((ready_dir / "run_999-jira-import.csv").exists())
            self.assertTrue((ready_dir / "jira-validation-report.md").exists())
            self.assertTrue((ready_dir / "recommendations" / "PROP-001_999" / "brief.md").exists())
            item_jira = ready_dir / "recommendations" / "PROP-001_999" / "jira-ticket.csv"
            self.assertTrue(item_jira.exists())
            self.assertEqual(validate_jira_csv_file(item_jira, expected_story_count=1), [])
            with item_jira.open(encoding="utf-8", newline="") as fh:
                rows = list(csv.reader(fh))
            self.assertEqual(rows[0], db.JIRA_FIELDS)
            self.assertEqual([row[0] for row in rows[1:]], ["Epic", "Story"])
            self.assertIn("manifest", written)

    def test_ready_to_send_bundle_uses_domain_readiness_and_generic_email_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            run_dir = Path(tmp) / "runs" / "run_904_2026-06-24"
            db.initialize_database(db_path)
            with db.connection(db_path) as conn:
                seed_contract_run(
                    conn,
                    run_id="run_904",
                    run_number=904,
                    url="https://example.com/park-plaza",
                    brand="Park Plaza",
                    page_type="brand",
                    change_type="trust_distribution",
                    proposed_change="Add Park Plaza review distribution handoff details.",
                )
                payload = dashboard_payload(conn, "run_904")
                export_ready_to_send_bundle(conn, "run_904", run_dir)
            ready_dir = run_dir / "ready-to-send"
            with (ready_dir / "recommendation-tracker.csv").open(encoding="utf-8", newline="") as fh:
                tracker_rows = list(csv.DictReader(fh))
            ready_rows = [row for row in tracker_rows if row["status"] == READY_TO_SEND]
            self.assertEqual(payload["summary"]["ready_to_send"], len(ready_rows))
            email = (ready_dir / "stakeholder-email.md").read_text(encoding="utf-8")
            self.assertIn("Top priority is", email)
            self.assertIn("Park Plaza", email)
            self.assertNotIn("blocked Country Inn pages", email)
            self.assertNotIn("Country Inn", email)

    def test_ready_to_send_bundle_preserves_existing_bundle_on_late_failure(self):
        import scripts.export as export_module

        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            run_dir = Path(tmp) / "runs" / "run_999_2026-06-24"
            ready_dir = run_dir / "ready-to-send"
            ready_dir.mkdir(parents=True)
            (ready_dir / "manifest.json").write_text('{"old": true}\n', encoding="utf-8")
            db.initialize_database(db_path)
            with db.connection(db_path) as conn:
                db.upsert_run(conn, "run_999", 999, "2026-06-24", "COMPLETED")
                db.upsert_gap(
                    conn,
                    "GAP-999",
                    "run_999",
                    url_id=None,
                    criterion_id=None,
                    gap_type="MISSING",
                    severity=3,
                    status="NEW",
                    description="Hotel schema is missing.",
                )
                db.upsert_proposal(
                    conn,
                    999,
                    "GAP-999",
                    "run_999",
                    source_proposal_id="PROP-001",
                    proposed_change="Add Hotel JSON-LD.",
                    source_citation="C01",
                    priority_tier="P1",
                    impact_estimate="High.",
                )
                source_id = db.upsert_source(
                    conn,
                    run_id="run_999",
                    source_key="source:1",
                    url="https://schema.org/Hotel",
                    domain="schema.org",
                    title="Schema.org Hotel",
                    source_type="gap_research",
                    related_gaps=["GAP-999"],
                    related_recommendations=["999"],
                )
                conn.execute(
                    "INSERT INTO proposal_sources(proposal_id, source_id, run_id, role) VALUES(?, ?, ?, ?)",
                    (999, source_id, "run_999", "evidence"),
                )
                db.build_jira_tickets(conn, "run_999")
                original_writer = export_module.write_single_proposal_jira_csv
                export_module.write_single_proposal_jira_csv = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("late failure"))
                try:
                    with self.assertRaisesRegex(RuntimeError, "late failure"):
                        export_ready_to_send_bundle(conn, "run_999", run_dir)
                finally:
                    export_module.write_single_proposal_jira_csv = original_writer
            self.assertEqual((ready_dir / "manifest.json").read_text(encoding="utf-8"), '{"old": true}\n')


if __name__ == "__main__":
    unittest.main()
