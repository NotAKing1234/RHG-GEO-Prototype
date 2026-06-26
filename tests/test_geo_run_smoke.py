import csv
import json
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path

import run as runner
from scripts import db
from scripts import geo_run_smoke
from scripts.export import export_ready_to_send_bundle, jira_csv_content


@contextmanager
def patched_smoke_root(root: Path, db_path: Path):
    original_root = geo_run_smoke.ROOT
    original_state = geo_run_smoke.STATE_FILE
    original_db_path = db.DB_PATH
    geo_run_smoke.ROOT = root
    geo_run_smoke.STATE_FILE = root / "runs" / "active_run.json"
    db.DB_PATH = db_path
    try:
        yield
    finally:
        geo_run_smoke.ROOT = original_root
        geo_run_smoke.STATE_FILE = original_state
        db.DB_PATH = original_db_path


def seed_complete_run(root: Path, db_path: Path, *, include_all_metadata: bool = True, source_proposal_id: str = "PROP-001") -> Path:
    run_id = "run_999"
    run_dir = root / "runs" / "run_999_2026-06-24"
    run_dir.mkdir(parents=True)
    (root / "memory").mkdir(parents=True)
    (root / "runs" / "active_run.json").write_text(
        json.dumps(
            {
                "run_id": run_id,
                "run_number": 999,
                "run_date": "2026-06-24",
                "run_dir": "runs/run_999_2026-06-24",
                "status": "IN_PROGRESS",
                "current_phase": "PHASE_4_LOG_AND_LEARN",
            }
        ),
        encoding="utf-8",
    )
    (root / "memory" / "execution_log.md").write_text(f"# Execution Log\n\n## {run_id}\n\nSmoke fixture.\n", encoding="utf-8")
    urls = ["https://example.com/a", "https://example.com/b"]
    db.initialize_database(db_path)
    with db.connection(db_path) as conn:
        db.upsert_run(conn, run_id, 999, "2026-06-24", "COMPLETED")
        for url in urls:
            db.upsert_url(conn, url, brand="Radisson", page_type="hotel")
        for url in urls:
            url_id = conn.execute("SELECT url_id FROM urls WHERE url = ?", (url,)).fetchone()["url_id"]
            conn.execute(
                """
                INSERT INTO run_url_targets(run_id, url_id, selection_source, selected_at, audit_profile, model)
                VALUES(?, ?, 'test_fixture', '2026-06-24T00:00:00Z', 'metadata_light', 'gpt-5.4-mini')
                """,
                (run_id, url_id),
            )
        metadata_urls = urls if include_all_metadata else urls[:1]
        for index, url in enumerate(metadata_urls, start=1):
            url_id = db.upsert_url(conn, url, brand="Radisson", page_type="hotel")
            conn.execute(
                """
                INSERT INTO metadata_snapshots(run_id, url_id, page_label, title, meta_description, fetch_status, captured_at)
                VALUES(?, ?, ?, ?, ?, ?, ?)
                """,
                (run_id, url_id, f"Page {index}", f"Title {index}", "Description", "http_200", "2026-06-24T00:00:00Z"),
            )
        criterion_id = db.upsert_criterion(conn, run_id, "C01", "Pages must be crawlable and structured.")
        db.upsert_gap(
            conn,
            "GAP-999",
            run_id,
            url_id=db.upsert_url(conn, urls[0]),
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
            run_id,
            source_proposal_id=source_proposal_id,
            proposed_change="Add Hotel JSON-LD with address, geo, amenities, and booking URL.",
            source_citation="C01",
            current_state="No Hotel schema is present.",
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
            VALUES('run_999:999:primary', 999, 'run_999', 'schema_update', ?, 'Structured data / JSON-LD', '', ?, '')
            """,
            (urls[0], "Add Hotel JSON-LD with address, geo, amenities, and booking URL."),
        )
        source_id = db.upsert_source(
            conn,
            run_id=run_id,
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
            (999, source_id, run_id, "evidence"),
        )
        db.build_jira_tickets(conn, run_id)
        (run_dir / "run_999_jira_import.csv").write_text(jira_csv_content(conn, run_id), encoding="utf-8")
        export_ready_to_send_bundle(conn, run_id, run_dir)
    (run_dir / "metadata_snapshot.md").write_text(metadata_snapshot_fixture(urls if include_all_metadata else urls[:1]), encoding="utf-8")
    (run_dir / "gap_analysis.md").write_text(
        "GAP-999\nhttps://example.com/a\n\nCoverage matrix\n- https://example.com/a: GAP-999\n- https://example.com/b: no gaps found\n",
        encoding="utf-8",
    )
    (run_dir / "gap_research.md").write_text("**GAP-999 - Hotel schema missing**\nhttps://schema.org/Hotel\n", encoding="utf-8")
    (run_dir / "run_999_optimization_proposal_export.md").write_text("# Optimization Proposal - run_999\n", encoding="utf-8")
    return run_dir


def metadata_snapshot_fixture(urls: list[str]) -> str:
    lines = ["# Metadata Snapshot - run_999", ""]
    for index, url in enumerate(urls, start=1):
        lines.extend(
            [
                f"## Page {index}: {url}",
                "",
                f"**URL:** {url}",
                "**Fetch status:** http_200",
                "**Fetch timestamp:** 2026-06-24T00:00:00Z",
                "",
            ]
        )
    return "\n".join(lines)


class GeoRunSmokeTests(unittest.TestCase):
    def test_geo_run_smoke_passes_complete_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            db_path = root / "geo.db"
            with patched_smoke_root(root, db_path):
                seed_complete_run(root, db_path)
                messages = geo_run_smoke.run_smoke("run_999")
        self.assertTrue(any("target coverage" in message for message in messages))
        self.assertTrue(any("ready-to-send" in message for message in messages))

    def test_geo_run_smoke_fails_when_selected_url_missing_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            db_path = root / "geo.db"
            with patched_smoke_root(root, db_path):
                seed_complete_run(root, db_path, include_all_metadata=False)
                with self.assertRaisesRegex(geo_run_smoke.SmokeFailure, "missing 1 selected URL"):
                    geo_run_smoke.run_smoke("run_999")

    def test_geo_run_smoke_fails_when_artifact_missing_selected_url_even_if_db_has_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            db_path = root / "geo.db"
            with patched_smoke_root(root, db_path):
                run_dir = seed_complete_run(root, db_path)
                (run_dir / "metadata_snapshot.md").write_text("nonempty stale artifact without page records\n", encoding="utf-8")
                with self.assertRaisesRegex(geo_run_smoke.SmokeFailure, "metadata_snapshot.md is missing 2 selected URL"):
                    geo_run_smoke.run_smoke("run_999")

    def test_geo_run_smoke_fails_when_gap_analysis_omits_selected_url(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            db_path = root / "geo.db"
            with patched_smoke_root(root, db_path):
                run_dir = seed_complete_run(root, db_path)
                (run_dir / "gap_analysis.md").write_text("GAP-999\nhttps://example.com/a\n", encoding="utf-8")
                with self.assertRaisesRegex(geo_run_smoke.SmokeFailure, "gap_analysis.md is missing 1 selected URL"):
                    geo_run_smoke.run_smoke("run_999")

    def test_geo_run_smoke_fails_when_ready_item_jira_csv_is_malformed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            db_path = root / "geo.db"
            with patched_smoke_root(root, db_path):
                run_dir = seed_complete_run(root, db_path)
                item_csv = run_dir / "ready-to-send" / "recommendations" / "PROP-001_999" / "jira-ticket.csv"
                with item_csv.open("w", encoding="utf-8", newline="") as fh:
                    writer = csv.writer(fh)
                    writer.writerow(["Summary", "Issue Type"])
                    writer.writerow(["Broken", "Story"])
                with self.assertRaisesRegex(geo_run_smoke.SmokeFailure, "failed validation"):
                    geo_run_smoke.run_smoke("run_999")

    def test_geo_run_smoke_accepts_slugged_recommendation_folder_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            db_path = root / "geo.db"
            with patched_smoke_root(root, db_path):
                run_dir = seed_complete_run(root, db_path, source_proposal_id="PROP 001 / Hotel Schema")
                self.assertTrue((run_dir / "ready-to-send" / "recommendations" / "PROP-001-Hotel-Schema_999").exists())
                messages = geo_run_smoke.run_smoke("run_999")
        self.assertTrue(any("ready-to-send" in message for message in messages))

    def test_geo_run_smoke_defaults_to_active_run_state_not_latest_run_number(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            db_path = root / "geo.db"
            with patched_smoke_root(root, db_path):
                seed_complete_run(root, db_path)
                with db.connection(db_path) as conn:
                    db.upsert_run(conn, "run_1000", 1000, "2026-06-25", "IN_PROGRESS")
                messages = geo_run_smoke.run_smoke()
        self.assertIn("run: run_999", messages)

    def test_phase4_smoke_failure_does_not_mark_sqlite_run_completed(self):
        original_root = runner.ROOT
        original_state = runner.STATE_FILE
        original_smoke = runner.smoke
        original_db_path = db.DB_PATH
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            db_path = root / "geo.db"
            runner.ROOT = root
            runner.STATE_FILE = root / "runs" / "active_run.json"
            runner.smoke = lambda run_id: 2
            db.DB_PATH = db_path
            try:
                run_dir = root / "runs" / "run_999_2026-06-24"
                run_dir.mkdir(parents=True)
                (root / "memory").mkdir(parents=True)
                (run_dir / "log_reflection.md").write_text("reflection\n", encoding="utf-8")
                (root / "memory" / "master_summary.md").write_text("summary\n", encoding="utf-8")
                (root / "memory" / "execution_log.md").write_text("execution\n", encoding="utf-8")
                runner.STATE_FILE.write_text(
                    json.dumps(
                        {
                            "run_id": "run_999",
                            "run_number": 999,
                            "run_date": "2026-06-24",
                            "run_dir": "runs/run_999_2026-06-24",
                            "status": "IN_PROGRESS",
                            "current_phase": runner.PHASE_4,
                            "completed_phases": runner.PHASE_ORDER[:-1],
                        }
                    ),
                    encoding="utf-8",
                )
                db.initialize_database(db_path)
                with db.connection(db_path) as conn:
                    db.upsert_run(conn, "run_999", 999, "2026-06-24", "IN_PROGRESS")
                    url_id = db.upsert_url(conn, "https://example.com/a")
                    conn.execute(
                        """
                        INSERT INTO run_url_targets(run_id, url_id, selection_source, selected_at, audit_profile, model)
                        VALUES('run_999', ?, 'test', '2026-06-24T00:00:00Z', 'metadata_light', 'gpt-5.4-mini')
                        """,
                        (url_id,),
                    )
                self.assertEqual(runner.advance(), 2)
                with db.connection(db_path) as conn:
                    run_status = conn.execute("SELECT status FROM runs WHERE run_id = 'run_999'").fetchone()[0]
                    last_audited = conn.execute("SELECT last_audited_run FROM urls WHERE url = 'https://example.com/a'").fetchone()[0]
                state = json.loads(runner.STATE_FILE.read_text(encoding="utf-8"))
                self.assertEqual(run_status, "IN_PROGRESS")
                self.assertIsNone(last_audited)
                self.assertEqual(state["status"], "IN_PROGRESS")
            finally:
                runner.ROOT = original_root
                runner.STATE_FILE = original_state
                runner.smoke = original_smoke
                db.DB_PATH = original_db_path

    def test_phase2_advance_blocks_when_selected_url_has_no_fetch_status(self):
        original_root = runner.ROOT
        original_state = runner.STATE_FILE
        original_db_path = db.DB_PATH
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            db_path = root / "geo.db"
            runner.ROOT = root
            runner.STATE_FILE = root / "runs" / "active_run.json"
            db.DB_PATH = db_path
            try:
                run_dir = root / "runs" / "run_999_2026-06-24"
                run_dir.mkdir(parents=True)
                (root / "runs").mkdir(exist_ok=True)
                runner.STATE_FILE.write_text(
                    json.dumps(
                        {
                            "run_id": "run_999",
                            "run_number": 999,
                            "run_date": "2026-06-24",
                            "run_dir": "runs/run_999_2026-06-24",
                            "status": "IN_PROGRESS",
                            "current_phase": runner.PHASE_2,
                            "completed_phases": [],
                        }
                    ),
                    encoding="utf-8",
                )
                db.initialize_database(db_path)
                with db.connection(db_path) as conn:
                    db.upsert_run(conn, "run_999", 999, "2026-06-24", "IN_PROGRESS")
                    url_id = db.upsert_url(conn, "https://example.com/a")
                    conn.execute(
                        """
                        INSERT INTO run_url_targets(run_id, url_id, selection_source, selected_at, audit_profile, model)
                        VALUES('run_999', ?, 'test', '2026-06-24T00:00:00Z', 'metadata_light', 'gpt-5.4-mini')
                        """,
                        (url_id,),
                    )
                (run_dir / "metadata_snapshot.md").write_text(
                    "# Metadata Snapshot\n\n## Page 1: https://example.com/a\n\n**URL:** https://example.com/a\n\n",
                    encoding="utf-8",
                )
                (run_dir / "gap_analysis.md").write_text("https://example.com/a\n", encoding="utf-8")
                self.assertEqual(runner.advance(), 2)
                state = json.loads(runner.STATE_FILE.read_text(encoding="utf-8"))
                self.assertEqual(state["current_phase"], runner.PHASE_2)
            finally:
                runner.ROOT = original_root
                runner.STATE_FILE = original_state
                db.DB_PATH = original_db_path

    def test_phase2_skip_scrape_is_blocked(self):
        original_root = runner.ROOT
        original_state = runner.STATE_FILE
        original_db_path = db.DB_PATH
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            db_path = root / "geo.db"
            runner.ROOT = root
            runner.STATE_FILE = root / "runs" / "active_run.json"
            db.DB_PATH = db_path
            try:
                (root / "runs").mkdir(parents=True)
                runner.STATE_FILE.write_text(
                    json.dumps(
                        {
                            "run_id": "run_999",
                            "run_number": 999,
                            "run_date": "2026-06-24",
                            "run_dir": "runs/run_999_2026-06-24",
                            "status": "IN_PROGRESS",
                            "current_phase": runner.PHASE_2,
                            "completed_phases": [],
                        }
                    ),
                    encoding="utf-8",
                )
                db.initialize_database(db_path)
                self.assertEqual(runner.advance(skip_scrape=True), 2)
                state = json.loads(runner.STATE_FILE.read_text(encoding="utf-8"))
                self.assertEqual(state["current_phase"], runner.PHASE_2)
            finally:
                runner.ROOT = original_root
                runner.STATE_FILE = original_state
                db.DB_PATH = original_db_path


if __name__ == "__main__":
    unittest.main()
