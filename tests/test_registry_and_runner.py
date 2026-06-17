import csv
import tempfile
import unittest
from pathlib import Path

import run
import dashboard.server as server


class RegistrySelectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.tmp.name)
        self.old_registry = server.URL_REGISTRY_CSV
        self.old_next = server.NEXT_GEO_RUN_CSV
        self.old_max = server.MAX_ACTIVE_TARGETS_FOR_RUN_SCOPE
        server.URL_REGISTRY_CSV = self.tmp_path / "registry.csv"
        server.NEXT_GEO_RUN_CSV = self.tmp_path / "next_geo_run.csv"
        server.MAX_ACTIVE_TARGETS_FOR_RUN_SCOPE = 2
        with server.URL_REGISTRY_CSV.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(
                fh,
                fieldnames=["url", "canonical_url", "normalized_url", "brand", "region", "country", "locale", "page_type", "content_group", "location_confidence"],
            )
            writer.writeheader()
            writer.writerow({
                "url": "https://example.com/a",
                "canonical_url": "https://example.com/a",
                "normalized_url": "https://example.com/a",
                "brand": "Radisson",
                "region": "",
                "country": "",
                "locale": "en-us",
                "page_type": "brand",
                "content_group": "radisson",
                "location_confidence": "low",
            })
            writer.writerow({
                "url": "https://example.com/b",
                "canonical_url": "https://example.com/b",
                "normalized_url": "https://example.com/b",
                "brand": "Radisson Blu",
                "region": "North America",
                "country": "United States",
                "locale": "en-us",
                "page_type": "brand",
                "content_group": "radisson-blu",
                "location_confidence": "low",
            })

    def tearDown(self):
        server.URL_REGISTRY_CSV = self.old_registry
        server.NEXT_GEO_RUN_CSV = self.old_next
        server.MAX_ACTIVE_TARGETS_FOR_RUN_SCOPE = self.old_max
        self.tmp.cleanup()

    def test_default_selection_payload_refuses_entire_registry(self):
        with self.assertRaises(ValueError):
            server.save_registry_selection({})

    def test_explicit_empty_selection_writes_header_only(self):
        result = server.save_registry_selection({"selected_urls": []})
        self.assertEqual(result["selected_count"], 0)
        with server.NEXT_GEO_RUN_CSV.open(encoding="utf-8", newline="") as fh:
            rows = list(csv.reader(fh))
        self.assertEqual(len(rows), 1)
        self.assertIn("normalized_url", rows[0])

    def test_unspecified_filter_matches_blank_registry_values(self):
        rows = server.read_url_registry()
        filtered = server.filter_registry_rows(rows, {"region": "Unspecified"})
        self.assertEqual([row["normalized_url"] for row in filtered], ["https://example.com/a"])

    def test_jira_export_uses_saved_description(self):
        row = server.jira_story_row(
            "run_999",
            "Epic",
            {
                "proposal_id": "GEO-1",
                "title": "Original",
                "team_override": {"ticket_draft": {"description": "Saved reviewer description"}},
            },
            [],
            {"rating": 50},
        )
        self.assertEqual(row["Description"], "Saved reviewer description")


class RunnerTargetTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.tmp.name)
        self.old_targets = run.TARGET_URLS
        self.old_run_targets = run.RUN_TARGETS_CSV
        run.TARGET_URLS = self.tmp_path / "target_urls.md"
        run.RUN_TARGETS_CSV = self.tmp_path / "next_geo_run.csv"
        run.TARGET_URLS.write_text("- https://example.com/default\n", encoding="utf-8")

    def tearDown(self):
        run.TARGET_URLS = self.old_targets
        run.RUN_TARGETS_CSV = self.old_run_targets
        self.tmp.cleanup()

    def test_header_only_next_run_csv_falls_back_to_target_urls(self):
        run.RUN_TARGETS_CSV.write_text("url,normalized_url\n", encoding="utf-8")
        self.assertEqual(run.active_targets_path(), run.TARGET_URLS)

    def test_next_run_csv_with_data_is_active(self):
        run.RUN_TARGETS_CSV.write_text("url,normalized_url\nhttps://example.com/a,https://example.com/a\n", encoding="utf-8")
        self.assertEqual(run.active_targets_path(), run.RUN_TARGETS_CSV)


if __name__ == "__main__":
    unittest.main()
