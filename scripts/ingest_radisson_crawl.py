#!/usr/bin/env python3
"""Validate and prepare the Radisson crawl inventory for GEO optimizer use."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CRAWL_DIR = ROOT / "sources" / "website" / "radisson_crawl" / "latest"
DEFAULT_ACTIVE_TARGETS = ROOT / "sources" / "website" / "target_urls.md"
DEFAULT_REGISTRY = ROOT / "sources" / "website" / "radisson_url_registry.csv"
DEFAULT_RUN_TARGETS = ROOT / "sources" / "website" / "run_targets" / "next_geo_run.csv"
REQUIRED_FIELDS = {
    "url",
    "normalized_url",
    "canonical_url",
    "date_discovered",
    "crawl_depth",
    "http_status",
    "http_status_note",
    "source_domain",
    "source_sitemap",
    "content_type",
    "last_modified",
    "crawl_method",
    "user_agent_identifier",
    "provenance",
}
INTERNAL_PATH_TOKENS = (
    "/system/",
    "/fragment/",
    "/secure/",
    "/my-account",
    "/my-profile/",
    "/login",
    "/cvent/",
)
BRAND_LABELS = {
    "artotel": "art'otel",
    "country-inn": "Country Inn & Suites",
    "golden-tulip-china": "Golden Tulip China",
    "j": "J Hotel",
    "jin-jiang": "Jin Jiang",
    "kunlun": "Kunlun",
    "park-inn": "Park Inn by Radisson",
    "park-plaza": "Park Plaza",
    "prize-by-radisson": "Prize by Radisson",
    "radisson": "Radisson",
    "radisson-blu": "Radisson Blu",
    "radisson-collection": "Radisson Collection",
    "radisson-individuals": "Radisson Individuals",
    "radisson-individuals-retreats": "Radisson Individuals Retreats",
    "radisson-red": "Radisson RED",
}
BRAND_SLUGS = sorted(BRAND_LABELS, key=len, reverse=True)
LOCALE_COUNTRIES = {
    "ar-ae": ("United Arab Emirates", "Middle East & Africa", "Asia"),
    "cs-cz": ("Czech Republic", "Europe", "Europe"),
    "da-dk": ("Denmark", "Europe", "Europe"),
    "de-de": ("Germany", "Europe", "Europe"),
    "el-gr": ("Greece", "Europe", "Europe"),
    "en-us": ("United States", "North America", "North America"),
    "es-es": ("Spain", "Europe", "Europe"),
    "fi-fi": ("Finland", "Europe", "Europe"),
    "fr-fr": ("France", "Europe", "Europe"),
    "hi-in": ("India", "Asia Pacific", "Asia"),
    "hu-hu": ("Hungary", "Europe", "Europe"),
    "it-it": ("Italy", "Europe", "Europe"),
    "ja-jp": ("Japan", "Asia Pacific", "Asia"),
    "ko-kr": ("South Korea", "Asia Pacific", "Asia"),
    "nl-nl": ("Netherlands", "Europe", "Europe"),
    "no-no": ("Norway", "Europe", "Europe"),
    "pl-pl": ("Poland", "Europe", "Europe"),
    "pt-br": ("Brazil", "South America", "South America"),
    "ru-ru": ("Russia", "Europe", "Europe"),
    "sv-se": ("Sweden", "Europe", "Europe"),
    "tr-tr": ("Turkey", "Europe", "Europe"),
    "zh-cn": ("China", "Asia Pacific", "Asia"),
    "zh-tw": ("Taiwan", "Asia Pacific", "Asia"),
}
COUNTRY_SLUGS = {
    "united-states": ("United States", "North America", "North America"),
    "usa": ("United States", "North America", "North America"),
    "canada": ("Canada", "North America", "North America"),
    "mexico": ("Mexico", "North America", "North America"),
    "germany": ("Germany", "Europe", "Europe"),
    "deutschland": ("Germany", "Europe", "Europe"),
    "france": ("France", "Europe", "Europe"),
    "italy": ("Italy", "Europe", "Europe"),
    "spain": ("Spain", "Europe", "Europe"),
    "united-kingdom": ("United Kingdom", "Europe", "Europe"),
    "england": ("United Kingdom", "Europe", "Europe"),
    "netherlands": ("Netherlands", "Europe", "Europe"),
    "norway": ("Norway", "Europe", "Europe"),
    "sweden": ("Sweden", "Europe", "Europe"),
    "denmark": ("Denmark", "Europe", "Europe"),
    "finland": ("Finland", "Europe", "Europe"),
    "poland": ("Poland", "Europe", "Europe"),
    "india": ("India", "Asia Pacific", "Asia"),
    "china": ("China", "Asia Pacific", "Asia"),
    "japan": ("Japan", "Asia Pacific", "Asia"),
    "australia": ("Australia", "Asia Pacific", "Oceania"),
    "united-arab-emirates": ("United Arab Emirates", "Middle East & Africa", "Asia"),
    "uae": ("United Arab Emirates", "Middle East & Africa", "Asia"),
    "saudi-arabia": ("Saudi Arabia", "Middle East & Africa", "Asia"),
    "south-africa": ("South Africa", "Middle East & Africa", "Africa"),
    "morocco": ("Morocco", "Middle East & Africa", "Africa"),
    "egypt": ("Egypt", "Middle East & Africa", "Africa"),
    "brazil": ("Brazil", "South America", "South America"),
}
REGISTRY_FIELDS = [
    "url",
    "canonical_url",
    "normalized_url",
    "brand",
    "brand_slug",
    "locale",
    "locale_country",
    "locale_region",
    "country",
    "region",
    "continent",
    "location_source",
    "location_confidence",
    "content_group",
    "page_type",
    "hotel_name",
    "hotel_slug",
    "source_domain",
    "source_sitemap",
    "source_sitemap_reader_status",
    "sitemap_lastmod",
    "date_discovered",
    "crawl_depth",
    "http_status",
    "http_status_note",
    "content_type",
    "last_modified",
    "crawl_method",
    "user_agent_identifier",
    "provenance",
    "selected_for_next_run",
    "priority",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def repo_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as fh:
        for line_number, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSONL at {rel(path)}:{line_number}: {exc}") from exc
    return records


def validate_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    keys: set[str] = set()
    duplicates = 0
    missing_required: dict[str, int] = {}
    hosts: dict[str, int] = {}
    query_or_fragment_rows = 0
    internal_path_rows = 0

    for record in records:
        for field in REQUIRED_FIELDS:
            if field not in record:
                missing_required[field] = missing_required.get(field, 0) + 1

        key = record.get("canonicalization_key") or record.get("canonical_url") or record.get("normalized_url")
        if key in keys:
            duplicates += 1
        keys.add(str(key))

        normalized = str(record.get("normalized_url") or "")
        parsed = urllib.parse.urlsplit(normalized)
        if parsed.netloc:
            hosts[parsed.netloc] = hosts.get(parsed.netloc, 0) + 1
        if parsed.query or parsed.fragment:
            query_or_fragment_rows += 1
        lowered_path = parsed.path.lower()
        if any(token in lowered_path for token in INTERNAL_PATH_TOKENS):
            internal_path_rows += 1

    return {
        "record_count": len(records),
        "unique_canonicalization_keys": len(keys),
        "duplicate_canonicalization_keys": duplicates,
        "missing_required_fields": missing_required,
        "hosts": dict(sorted(hosts.items())),
        "query_or_fragment_rows": query_or_fragment_rows,
        "internal_path_rows": internal_path_rows,
        "valid_for_ingestion": not missing_required
        and duplicates == 0
        and query_or_fragment_rows == 0
        and internal_path_rows == 0,
    }


def activate_targets(source: Path, destination: Path, *, backup: bool) -> str | None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    backup_path: Path | None = None
    if backup and destination.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup_path = destination.with_name(f"{destination.stem}.backup_{stamp}{destination.suffix}")
        shutil.copy2(destination, backup_path)
    shutil.copy2(source, destination)
    return rel(backup_path) if backup_path else None


def url_parts(url: str) -> list[str]:
    return [part for part in urllib.parse.urlsplit(url).path.split("/") if part]


def strip_locale(parts: list[str]) -> tuple[str, list[str]]:
    if parts and re.match(r"^[a-z]{2}-[a-z]{2}$", parts[0], flags=re.IGNORECASE):
        return parts[0].lower(), parts[1:]
    return "", parts


def infer_brand(record: dict[str, Any], parts: list[str]) -> tuple[str, str]:
    group = str(record.get("content_group") or "")
    if group in BRAND_LABELS:
        return BRAND_LABELS[group], group
    path_slug = "/".join(parts).lower()
    for slug in BRAND_SLUGS:
        if f"/{slug}" in f"/{path_slug}" or path_slug.startswith(slug):
            return BRAND_LABELS[slug], slug
    if "hotels" in parts:
        index = parts.index("hotels")
        if len(parts) > index + 1:
            hotel_slug = parts[index + 1].lower()
            for slug in BRAND_SLUGS:
                if hotel_slug == slug or hotel_slug.startswith(f"{slug}-"):
                    return BRAND_LABELS[slug], slug
    return "Unclassified", "unclassified"


def infer_page_type(record: dict[str, Any], parts: list[str]) -> str:
    group = str(record.get("content_group") or "")
    path = "/".join(parts).lower()
    if not parts:
        return "homepage"
    if group in BRAND_LABELS or any(part in {"brand", "marke", "marca"} for part in parts):
        return "brand"
    if "hotels" in parts:
        index = parts.index("hotels")
        return "hotel_overview" if len(parts) == index + 2 else "hotel_subpage"
    if group == "hotel-overview-pages":
        return "hotel_overview"
    if group == "remaining-hotel-pages":
        return "hotel_subpage"
    if group == "destinations" or any(token in path for token in ["destination", "destino", "reiseziel", "bestemming", "kohde"]):
        return "destination"
    if group == "offers" or any(token in path for token in ["offer", "deal", "tilbud", "angebote", "oferta"]):
        return "offer"
    if any(token in path for token in ["meeting", "conference", "moede", "tagungen", "reuniones", "seminaires", "kokous"]):
        return "meetings"
    if "rewards" in parts:
        return "loyalty"
    if any(token in path for token in ["terms", "privacy", "cookie", "legal"]):
        return "legal"
    return "general"


def hotel_slug_and_name(parts: list[str]) -> tuple[str, str]:
    if "hotels" not in parts:
        return "", ""
    index = parts.index("hotels")
    if len(parts) <= index + 1:
        return "", ""
    slug = parts[index + 1]
    return slug, slug.replace("-", " ").title()


def infer_location(locale: str, parts: list[str]) -> tuple[str, str, str, str, str]:
    locale_country, locale_region, locale_continent = LOCALE_COUNTRIES.get(locale, ("", "", ""))
    lowered_parts = [part.lower() for part in parts]
    for part in lowered_parts:
        if part in COUNTRY_SLUGS:
            country, region, continent = COUNTRY_SLUGS[part]
            return country, region, continent, "url_country_slug", "high"
    path = "/".join(lowered_parts)
    for slug, (country, region, continent) in COUNTRY_SLUGS.items():
        if f"/{slug}/" in f"/{path}/":
            return country, region, continent, "url_country_slug", "medium"
    if locale_country:
        return locale_country, locale_region, locale_continent, "locale_fallback", "low"
    return "", "", "", "unknown", "unknown"


def registry_row(record: dict[str, Any]) -> dict[str, Any]:
    locale, path_parts = strip_locale(url_parts(str(record.get("normalized_url") or "")))
    brand, brand_slug = infer_brand(record, path_parts)
    hotel_slug, hotel_name = hotel_slug_and_name(path_parts)
    locale_country, locale_region, _ = LOCALE_COUNTRIES.get(locale, ("", "", ""))
    country, region, continent, location_source, location_confidence = infer_location(locale, path_parts)
    return {
        "url": record.get("url") or record.get("normalized_url") or "",
        "canonical_url": record.get("canonical_url") or record.get("normalized_url") or "",
        "normalized_url": record.get("normalized_url") or "",
        "brand": brand,
        "brand_slug": brand_slug,
        "locale": locale,
        "locale_country": locale_country,
        "locale_region": locale_region,
        "country": country,
        "region": region,
        "continent": continent,
        "location_source": location_source,
        "location_confidence": location_confidence,
        "content_group": record.get("content_group") or "",
        "page_type": infer_page_type(record, path_parts),
        "hotel_name": hotel_name,
        "hotel_slug": hotel_slug,
        "source_domain": record.get("source_domain") or "",
        "source_sitemap": record.get("source_sitemap") or "",
        "source_sitemap_reader_status": record.get("source_sitemap_reader_status") or "",
        "sitemap_lastmod": record.get("sitemap_lastmod") or "",
        "date_discovered": record.get("date_discovered") or "",
        "crawl_depth": record.get("crawl_depth") or "",
        "http_status": record.get("http_status") if record.get("http_status") is not None else "",
        "http_status_note": record.get("http_status_note") or "",
        "content_type": record.get("content_type") or "",
        "last_modified": record.get("last_modified") or "",
        "crawl_method": record.get("crawl_method") or "",
        "user_agent_identifier": record.get("user_agent_identifier") or "",
        "provenance": json.dumps(record.get("provenance") or {}, ensure_ascii=False, sort_keys=True),
        "selected_for_next_run": "false",
        "priority": "",
    }


def write_registry(records: list[dict[str, Any]], path: Path) -> list[dict[str, Any]]:
    rows = [registry_row(record) for record in records]
    rows.sort(key=lambda row: (row["brand"], row["region"], row["locale"], row["page_type"], row["normalized_url"]))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=REGISTRY_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return rows


def write_ingestion_manifest(
    path: Path,
    *,
    crawl_dir: Path,
    records: list[dict[str, Any]],
    registry_rows: list[dict[str, Any]],
    crawl_manifest: dict[str, Any],
    validation: dict[str, Any],
    active_targets_backup: str | None,
) -> dict[str, Any]:
    failed_sitemaps = [
        {
            "url": item.get("url"),
            "reader_status": item.get("reader_status"),
            "error": item.get("error"),
            "raw_file": item.get("raw_file"),
        }
        for item in crawl_manifest.get("sitemap_fetches", [])
        if item.get("reader_status") != 200
    ]
    origin_metadata_verified = bool(crawl_manifest.get("origin_metadata_verified"))
    known_gaps = {
        "failed_sitemaps": failed_sitemaps,
        "origin_metadata_gap": (
            "" if origin_metadata_verified else
            "Direct Radisson origin fetches returned access-restricted 403 from this environment; "
            "per-page origin HTTP status, canonical link tags, and content-type headers remain unverified."
        ),
    }
    payload = {
        "generated_at": utc_now(),
        "status": "ready" if not failed_sitemaps and origin_metadata_verified else "ready_with_known_gaps",
        "crawl_dir": rel(crawl_dir),
        "dataset": {
            "jsonl": rel(crawl_dir / "radisson_url_index.jsonl"),
            "csv": rel(crawl_dir / "radisson_url_index.csv"),
            "registry_csv": rel(DEFAULT_REGISTRY),
            "next_run_csv": rel(DEFAULT_RUN_TARGETS),
            "target_urls_markdown": rel(crawl_dir / "target_urls_discovered.md"),
            "exclusions": rel(crawl_dir / "crawl_exclusions.csv"),
            "crawl_manifest": rel(crawl_dir / "crawl_manifest.json"),
            "validation": rel(crawl_dir / "crawl_validation.md"),
        },
        "canonical_target_file": {
            "path": rel(DEFAULT_ACTIVE_TARGETS),
            "source": rel(crawl_dir / "target_urls_discovered.md"),
            "activation_command": "python3 scripts/ingest_radisson_crawl.py --activate-targets",
            "backup_created": active_targets_backup,
        },
        "run_selection": {
            "path": rel(DEFAULT_RUN_TARGETS),
            "format": "CSV subset of the canonical registry",
            "created_by": "Dashboard URL Registry filters or an explicit CSV export step",
        },
        "validation": validation,
        "crawl_counts": crawl_manifest.get("counts", {}),
        "known_gaps": known_gaps,
        "field_contract": sorted(REQUIRED_FIELDS),
        "record_count": len(records),
        "registry_record_count": len(registry_rows),
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate and prepare Radisson crawl output for GEO optimizer ingestion.")
    parser.add_argument("--crawl-dir", default=str(DEFAULT_CRAWL_DIR), help="Directory containing crawl deliverables.")
    parser.add_argument("--activate-targets", action="store_true", help="Copy target_urls_discovered.md to sources/website/target_urls.md.")
    parser.add_argument("--no-backup", action="store_true", help="Do not back up target_urls.md before --activate-targets.")
    parser.add_argument("--fail-on-gaps", action="store_true", help="Exit non-zero if known coverage gaps remain.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    crawl_dir = repo_path(args.crawl_dir)
    jsonl_path = crawl_dir / "radisson_url_index.jsonl"
    manifest_path = crawl_dir / "crawl_manifest.json"
    target_markdown = crawl_dir / "target_urls_discovered.md"
    ingestion_manifest_path = crawl_dir / "geo_optimizer_ingestion.json"

    for path in (jsonl_path, manifest_path, target_markdown):
        if not path.exists():
            raise SystemExit(f"Missing required crawl artifact: {rel(path)}")

    records = read_jsonl(jsonl_path)
    crawl_manifest = read_json(manifest_path)
    validation = validate_records(records)
    if not validation["valid_for_ingestion"]:
        raise SystemExit(json.dumps({"validation_failed": validation}, indent=2, sort_keys=True))
    registry_rows = write_registry(records, DEFAULT_REGISTRY)

    backup_path = None
    if args.activate_targets:
        backup_path = activate_targets(target_markdown, DEFAULT_ACTIVE_TARGETS, backup=not args.no_backup)

    ingestion_manifest = write_ingestion_manifest(
        ingestion_manifest_path,
        crawl_dir=crawl_dir,
        records=records,
        registry_rows=registry_rows,
        crawl_manifest=crawl_manifest,
        validation=validation,
        active_targets_backup=backup_path,
    )

    print(json.dumps({
        "ingestion_manifest": rel(ingestion_manifest_path),
        "status": ingestion_manifest["status"],
        "record_count": len(records),
        "registry_csv": rel(DEFAULT_REGISTRY),
        "valid_for_ingestion": validation["valid_for_ingestion"],
        "failed_sitemaps": len(ingestion_manifest["known_gaps"]["failed_sitemaps"]),
        "active_targets_backup": backup_path,
    }, indent=2, sort_keys=True))

    if args.fail_on_gaps and ingestion_manifest["status"] != "ready":
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
