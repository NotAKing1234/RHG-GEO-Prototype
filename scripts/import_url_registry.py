#!/usr/bin/env python3
"""Import a Radisson URL registry CSV into the SQLite URL table.

Data flow: generated crawl registry CSV -> urls. Pitfalls: imported registry rows should not
clear pending dashboard "Research Next" selections unless explicitly requested.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any, TextIO


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import db  # noqa: E402


DEFAULT_REGISTRY = ROOT / "sources" / "website" / "radisson_url_registry.csv"
HISTORICAL_REGISTRY_OBJECT = "b3852f3:sources/website/radisson_url_registry.csv"


class GitCsvStream:
    def __init__(self, object_name: str):
        self.object_name = object_name
        self.proc: subprocess.Popen[str] | None = None

    def __enter__(self) -> TextIO:
        self.proc = subprocess.Popen(
            ["git", "show", self.object_name],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if self.proc.stdout is None:
            raise RuntimeError(f"Unable to read git object {self.object_name}")
        return self.proc.stdout

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        if self.proc is None:
            return
        _, stderr = self.proc.communicate()
        if self.proc.returncode and exc is None:
            raise RuntimeError(f"git show {self.object_name} failed: {stderr.strip()}")


def clean(value: Any) -> str | None:
    text = str(value or "").strip()
    return text or None


def truthy(value: Any) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "y", "selected"}


def registry_url(row: dict[str, Any]) -> str | None:
    return clean(row.get("normalized_url")) or clean(row.get("canonical_url")) or clean(row.get("url"))


def iter_csv_rows(handle: TextIO) -> Iterator[dict[str, str]]:
    reader = csv.DictReader(handle)
    for row in reader:
        yield dict(row)


def import_registry_rows(
    conn,
    rows: Iterable[dict[str, Any]],
    *,
    sync_selection: bool = False,
) -> dict[str, Any]:
    processed = 0
    skipped = 0
    selected_rows = 0
    metadata_counts: dict[str, set[str]] = {
        "brand": set(),
        "region": set(),
        "country": set(),
        "locale": set(),
        "page_type": set(),
        "content_group": set(),
        "location_confidence": set(),
    }

    for row in rows:
        url = registry_url(row)
        if not url:
            skipped += 1
            continue
        selected = truthy(row.get("selected_for_next_run"))
        if selected:
            selected_rows += 1
        db.upsert_url(
            conn,
            url,
            brand=clean(row.get("brand")),
            region=clean(row.get("region")) or clean(row.get("locale_region")),
            country=clean(row.get("country")) or clean(row.get("locale_country")),
            locale=clean(row.get("locale")),
            page_type=clean(row.get("page_type")),
            content_group=clean(row.get("content_group")),
            location_confidence=clean(row.get("location_confidence")),
            location_source=clean(row.get("location_source")),
            source_sitemap=clean(row.get("source_sitemap")),
            selected_for_next_run=selected if sync_selection else None,
        )
        for field in metadata_counts:
            value = clean(row.get(field))
            if not value and field == "region":
                value = clean(row.get("locale_region"))
            if not value and field == "country":
                value = clean(row.get("locale_country"))
            if value:
                metadata_counts[field].add(value)
        processed += 1

    return {
        "processed": processed,
        "skipped": skipped,
        "selected_rows_in_source": selected_rows,
        "metadata_cardinality": {field: len(values) for field, values in metadata_counts.items()},
    }


def open_source(args: argparse.Namespace):
    if args.git_object:
        return GitCsvStream(args.git_object)
    if args.path == "-":
        return _stdin_context()
    path = Path(args.path or DEFAULT_REGISTRY)
    if not path.is_absolute():
        path = ROOT / path
    return path.open(encoding="utf-8", newline="")


class _stdin_context:
    def __enter__(self) -> TextIO:
        return sys.stdin

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        return None


def import_registry(
    *,
    db_path: Path = db.DB_PATH,
    path: str | None = None,
    git_object: str | None = None,
    sync_selection: bool = False,
) -> dict[str, Any]:
    args = argparse.Namespace(path=path, git_object=git_object)
    db.initialize_database(db_path)
    source_label = f"git:{git_object}" if git_object else str(path or DEFAULT_REGISTRY)
    with db.connection(db_path) as conn:
        before_count = db.table_counts(conn).get("urls", 0)
        with open_source(args) as handle:
            result = import_registry_rows(conn, iter_csv_rows(handle), sync_selection=sync_selection)
        after_count = db.table_counts(conn).get("urls", 0)
        selected_count = len(db.selected_urls(conn))
    result.update(
        {
            "source": source_label,
            "db_path": str(db_path),
            "before_count": before_count,
            "after_count": after_count,
            "added_count": after_count - before_count,
            "pending_selected_count": selected_count,
            "sync_selection": sync_selection,
        }
    )
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import Radisson URL registry rows into SQLite.")
    parser.add_argument(
        "path",
        nargs="?",
        default=str(DEFAULT_REGISTRY),
        help="Registry CSV path, or '-' for stdin. Defaults to sources/website/radisson_url_registry.csv.",
    )
    parser.add_argument("--db", type=Path, default=db.DB_PATH, help="SQLite DB path.")
    parser.add_argument(
        "--git-object",
        help=f"Read CSV from a git object such as {HISTORICAL_REGISTRY_OBJECT}.",
    )
    parser.add_argument(
        "--historical",
        action="store_true",
        help=f"Import the historical validated registry object {HISTORICAL_REGISTRY_OBJECT}.",
    )
    parser.add_argument(
        "--sync-selection",
        action="store_true",
        help="Also copy selected_for_next_run values from the registry CSV. Defaults to preserving dashboard selections.",
    )
    parser.add_argument("--json", action="store_true", help="Print a JSON summary.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    git_object = HISTORICAL_REGISTRY_OBJECT if args.historical else args.git_object
    result = import_registry(db_path=args.db, path=args.path, git_object=git_object, sync_selection=args.sync_selection)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            "Imported {processed} registry rows into {db_path}; URLs {before_count} -> {after_count} "
            "({added_count} added). Pending selections: {pending_selected_count}.".format(**result)
        )


if __name__ == "__main__":
    main()
