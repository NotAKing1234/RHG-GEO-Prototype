import csv
import io
import tempfile
import unittest
from pathlib import Path

from scripts import db
from scripts.dashboard_read_model import dashboard_payload
from scripts.export import jira_csv_content, write_next_geo_run
from scripts.import_run_artifacts import import_all_runs
from scripts.import_url_registry import import_registry_rows
from scripts.migrate_to_sqlite import migrate


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

    def test_dashboard_payload_preserves_frontend_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "geo.db"
            import_all_runs(db_path)
            with db.connection(db_path) as conn:
                payload = dashboard_payload(conn, "run_003")
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


if __name__ == "__main__":
    unittest.main()
