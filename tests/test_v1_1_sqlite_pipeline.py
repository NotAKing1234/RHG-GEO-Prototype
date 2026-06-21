import csv
import io
import tempfile
import unittest
from pathlib import Path

from scripts import db
from scripts.export import jira_csv_content
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


if __name__ == "__main__":
    unittest.main()
