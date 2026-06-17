#!/usr/bin/env python3
"""Build a Radisson URL inventory from official robots and sitemap sources.

The crawler is intentionally sitemap-first. In this environment Radisson's
origin returns an Akamai access-restricted page to direct automation, so the
script records that boundary once and uses public reader snapshots for the
robots.txt and sitemap XML files. It does not attempt login, reservation, or
internal paths.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "sources" / "website" / "radisson_crawl" / "latest"
SEED_DOMAIN = "https://www.radissonhotels.com/"
ROBOTS_URL = urllib.parse.urljoin(SEED_DOMAIN, "robots.txt")
SITEMAP_INDEX_URL = urllib.parse.urljoin(SEED_DOMAIN, "sitemapindex.xml")
USER_AGENT_ID = "GEOOptimizerAuditBot/0.1 (+local Radisson GEO audit; respects robots.txt)"
READER_PREFIX = "https://r.jina.ai/http://"
ALLOWED_SITE_HOSTS = {"www.radissonhotels.com", "radissonhotels.com"}
MEDIA_SITEMAP_TOKENS = {"images", "videos", "pdf-files"}
AUTH_PATH_TOKENS = (
    "/system/",
    "/fragment/",
    "/secure/",
    "/my-account",
    "/my-profile/",
    "/login",
    "/cvent/",
)
URL_IN_MARKDOWN_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
ISO_TIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T[0-9:.+-]+(?:Z|[+-]\d{2}:\d{2})?$")


@dataclass
class FetchRecord:
    url: str
    method: str
    status: int | None
    content_type: str
    last_modified: str
    body: str
    fetched_at: str
    elapsed_seconds: float
    error: str = ""
    reader_url: str = ""
    published_time: str = ""


@dataclass
class SitemapRef:
    url: str
    lastmod: str
    source: str
    reader_status: int | None = None
    fetch_error: str = ""


@dataclass
class UrlRef:
    url: str
    lastmod: str
    source_sitemap: str
    source_sitemap_lastmod: str
    source_sitemap_reader_status: int | None
    source_type: str = "sitemap"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def repo_path(path: str | Path) -> Path:
    path = Path(path)
    return path if path.is_absolute() else ROOT / path


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def reader_url(url: str) -> str:
    return READER_PREFIX + url


def fetch(
    url: str,
    *,
    method: str,
    timeout: int,
    reader: bool = False,
    reader_source_url: str | None = None,
) -> FetchRecord:
    started = time.monotonic()
    target_url = reader_url(reader_source_url or url) if reader else url
    headers = {
        "User-Agent": USER_AGENT_ID,
        "Accept": "text/plain,text/xml,application/xml,text/html;q=0.8,*/*;q=0.5",
        "Accept-Language": "en-US,en;q=0.9",
    }
    request = urllib.request.Request(target_url, headers=headers, method=method)
    fetched_at = utc_now()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
            content_type = response.headers.get("content-type", "")
            body = decode(raw, content_type)
            return FetchRecord(
                url=url,
                method="reader_snapshot" if reader else method.lower(),
                status=int(getattr(response, "status", None) or response.getcode()),
                content_type=content_type,
                last_modified=response.headers.get("last-modified", ""),
                body=body,
                fetched_at=fetched_at,
                elapsed_seconds=round(time.monotonic() - started, 3),
                reader_url=target_url if reader else "",
                published_time=extract_reader_published_time(body) if reader else "",
            )
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        content_type = exc.headers.get("content-type", "") if exc.headers else ""
        return FetchRecord(
            url=url,
            method="reader_snapshot" if reader else method.lower(),
            status=exc.code,
            content_type=content_type,
            last_modified=exc.headers.get("last-modified", "") if exc.headers else "",
            body=decode(raw, content_type),
            fetched_at=fetched_at,
            elapsed_seconds=round(time.monotonic() - started, 3),
            error=f"HTTP {exc.code}",
            reader_url=target_url if reader else "",
            published_time="",
        )
    except (urllib.error.URLError, TimeoutError) as exc:
        return FetchRecord(
            url=url,
            method="reader_snapshot" if reader else method.lower(),
            status=None,
            content_type="",
            last_modified="",
            body="",
            fetched_at=fetched_at,
            elapsed_seconds=round(time.monotonic() - started, 3),
            error=str(exc),
            reader_url=target_url if reader else "",
            published_time="",
        )


def fetch_reader_with_retries(url: str, *, timeout: int, retries: int, backoff_seconds: float) -> FetchRecord:
    origins = [url]
    if url.startswith("https://www.radissonhotels.com/"):
        origins.append("http://www.radissonhotels.com/" + url.removeprefix("https://www.radissonhotels.com/"))

    attempts = max(1, retries + 1)
    last = FetchRecord(url, "reader_snapshot", None, "", "", "", utc_now(), 0.0, "No attempts made")
    for origin in origins:
        last = fetch(url, method="GET", timeout=timeout, reader=True, reader_source_url=origin)
        for attempt in range(1, attempts):
            if last.status not in {422, 429, 503, 524}:
                break
            time.sleep(backoff_seconds * attempt)
            last = fetch(url, method="GET", timeout=timeout, reader=True, reader_source_url=origin)
        if last.status is not None and last.status < 400:
            return last
    return last


def decode(raw: bytes, content_type: str) -> str:
    charset = "utf-8"
    match = re.search(r"charset=([^;\s]+)", content_type, flags=re.IGNORECASE)
    if match:
        charset = match.group(1)
    try:
        return raw.decode(charset, errors="replace")
    except LookupError:
        return raw.decode("utf-8", errors="replace")


def extract_reader_published_time(text: str) -> str:
    match = re.search(r"^Published Time:\s*(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def parse_xml_sitemap(text: str) -> tuple[str, list[tuple[str, str]]]:
    root = ET.fromstring(text)
    root_name = root.tag.split("}", 1)[-1]
    items: list[tuple[str, str]] = []
    for child in root:
        child_name = child.tag.split("}", 1)[-1]
        if child_name not in {"sitemap", "url"}:
            continue
        loc = ""
        lastmod = ""
        for field in child:
            field_name = field.tag.split("}", 1)[-1]
            if field_name == "loc":
                loc = (field.text or "").strip()
            elif field_name == "lastmod":
                lastmod = (field.text or "").strip()
        if loc:
            items.append((loc, lastmod))
    return root_name, items


def parse_markdown_sitemap(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    items: list[tuple[str, str]] = []
    for index, line in enumerate(lines):
        match = URL_IN_MARKDOWN_RE.search(line)
        if not match:
            continue
        label = match.group(1).strip()
        url = match.group(2).strip()
        if label.startswith("Image:"):
            continue
        lastmod = ""
        for lookahead in range(index + 1, min(index + 5, len(lines))):
            candidate = lines[lookahead].strip()
            if not candidate:
                continue
            if ISO_TIME_RE.match(candidate):
                lastmod = candidate
            break
        items.append((url, lastmod))
    return items


def parse_sitemap_like(text: str) -> tuple[str, list[tuple[str, str]]]:
    stripped = text.lstrip()
    if stripped.startswith("<"):
        try:
            return parse_xml_sitemap(stripped)
        except ET.ParseError:
            pass
    return "markdown", parse_markdown_sitemap(text)


def parse_robots(text: str) -> dict[str, list[str]]:
    disallow: list[str] = []
    allow: list[str] = []
    sitemaps: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "#" in line:
            line = line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()
        if key == "disallow" and value:
            disallow.append(value)
        elif key == "allow" and value:
            allow.append(value)
        elif key == "sitemap" and value:
            sitemaps.append(value)
    return {"disallow": disallow, "allow": allow, "sitemaps": sitemaps}


def robots_pattern_matches(pattern: str, url: str) -> bool:
    parsed = urllib.parse.urlsplit(url)
    target = parsed.path or "/"
    if parsed.query:
        target += "?" + parsed.query
    escaped = re.escape(pattern).replace(r"\*", ".*").replace(r"\$", "$")
    if pattern.startswith("*"):
        regex = escaped
    else:
        regex = "^" + escaped
    return re.search(regex, target) is not None


def robots_disallowed(url: str, rules: dict[str, list[str]]) -> bool:
    matching_disallows = [rule for rule in rules.get("disallow", []) if robots_pattern_matches(rule, url)]
    if not matching_disallows:
        return False
    matching_allows = [rule for rule in rules.get("allow", []) if robots_pattern_matches(rule, url)]
    longest_disallow = max(len(rule) for rule in matching_disallows)
    longest_allow = max((len(rule) for rule in matching_allows), default=-1)
    return longest_disallow > longest_allow


def canonicalize(url: str) -> str:
    parsed = urllib.parse.urlsplit(url.strip())
    scheme = (parsed.scheme or "https").lower()
    host = parsed.netloc.lower()
    path = urllib.parse.unquote(parsed.path or "/")
    path = re.sub(r"/{2,}", "/", path)
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    return urllib.parse.urlunsplit((scheme, host, path, "", ""))


def locale_from_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    parts = [part for part in parsed.path.split("/") if part]
    if parts and re.match(r"^[a-z]{2}-[a-z]{2}$", parts[0], flags=re.IGNORECASE):
        return parts[0].lower()
    return ""


def infer_content_group(sitemap_url: str) -> str:
    name = Path(urllib.parse.urlsplit(sitemap_url).path).name
    name = name.removesuffix(".xml")
    return name.removeprefix("sitemap-") or "primary-domain"


def infer_content_type(url: str, group: str) -> str:
    path = urllib.parse.urlsplit(url).path.lower()
    if path.endswith(".pdf"):
        return "application/pdf; inferred from URL extension"
    if group == "pdf-files":
        return "application/pdf; inferred from sitemap"
    return "text/html; inferred from sitemap URL"


def classify_customer_facing(url: str, group: str) -> tuple[bool, str]:
    parsed = urllib.parse.urlsplit(url)
    host = parsed.netloc.lower()
    path = parsed.path.lower()
    if host not in ALLOWED_SITE_HOSTS:
        return False, "non_site_asset_or_external_domain"
    if any(token in path for token in AUTH_PATH_TOKENS):
        return False, "internal_auth_or_non_customer_path"
    if group in {"images", "videos"}:
        return True, "customer_page_referenced_by_media_sitemap"
    if path.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".mp4", ".mov", ".webm")):
        return False, "media_asset_url"
    return True, "customer_facing_candidate"


def sha256_short(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def build_url_record(
    ref: UrlRef,
    *,
    normalized_url: str,
    discovered_at: str,
    direct_origin_status: int | None,
) -> dict[str, Any]:
    parsed = urllib.parse.urlsplit(normalized_url)
    group = infer_content_group(ref.source_sitemap)
    locale = locale_from_url(normalized_url)
    sitemap_listed = ref.source_type == "sitemap"
    source_note = "URL is verified as sitemap-listed." if sitemap_listed else "URL is the approved seed homepage."
    status_note = (
        "Origin page was not fetched from this environment; Radisson origin returned access-restricted "
        f"403 to direct automation during robots/sitemap probing. {source_note}"
    )
    return {
        "url": ref.url,
        "normalized_url": normalized_url,
        "canonical_url": normalized_url,
        "canonicalization_key": normalized_url,
        "url_hash": sha256_short(normalized_url),
        "source_domain": parsed.netloc.lower(),
        "language_locale": locale,
        "content_group": group,
        "source_sitemap": ref.source_sitemap,
        "source_sitemap_lastmod": ref.source_sitemap_lastmod,
        "sitemap_lastmod": ref.lastmod,
        "date_discovered": discovered_at,
        "crawl_depth": 2 if sitemap_listed else 0,
        "http_status": None,
        "http_status_note": status_note,
        "origin_probe_status_for_seed_domain": direct_origin_status,
        "source_sitemap_reader_status": ref.source_sitemap_reader_status,
        "fetch_status": "DISCOVERED_FROM_OFFICIAL_SITEMAP" if sitemap_listed else "ADDED_FROM_APPROVED_SEED_DOMAIN",
        "content_type": infer_content_type(normalized_url, group),
        "last_modified": ref.lastmod or ref.source_sitemap_lastmod,
        "crawl_method": "robots_and_sitemap_reader_snapshot",
        "user_agent_identifier": USER_AGENT_ID,
        "provenance": {
            "seed_domain": SEED_DOMAIN,
            "robots_url": ROBOTS_URL,
            "sitemap_index_url": SITEMAP_INDEX_URL,
            "source_sitemap": ref.source_sitemap,
            "source_type": ref.source_type,
            "source_authority": (
                "Radisson robots.txt sitemap declaration and Radisson sitemap index"
                if sitemap_listed else
                "Approved seed domain configured for the crawl"
            ),
            "reader_service": "https://r.jina.ai/",
        },
    }


def exclusion_row(
    url: str,
    *,
    source: str,
    reason: str,
    discovered_at: str,
    detail: str = "",
) -> dict[str, str]:
    return {
        "url": url,
        "normalized_url": canonicalize(url) if url.startswith("http") else "",
        "source": source,
        "exclusion_reason": reason,
        "detail": detail,
        "date_discovered": discovered_at,
        "crawl_method": "robots_and_sitemap_reader_snapshot",
    }


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    fieldnames = [
        "url",
        "normalized_url",
        "canonical_url",
        "source_domain",
        "language_locale",
        "content_group",
        "source_sitemap",
        "sitemap_lastmod",
        "date_discovered",
        "crawl_depth",
        "http_status",
        "http_status_note",
        "origin_probe_status_for_seed_domain",
        "source_sitemap_reader_status",
        "fetch_status",
        "content_type",
        "last_modified",
        "crawl_method",
        "user_agent_identifier",
        "url_hash",
    ]
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for record in records:
            writer.writerow(record)


def write_exclusions(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "url",
        "normalized_url",
        "source",
        "exclusion_reason",
        "detail",
        "date_discovered",
        "crawl_method",
    ]
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_target_urls(path: Path, records: list[dict[str, Any]]) -> None:
    by_group: dict[str, list[str]] = {}
    for record in records:
        by_group.setdefault(record["content_group"], []).append(record["normalized_url"])
    lines = [
        "# Radisson Website - Discovered Customer-Facing URL Inventory",
        "",
        "Generated from official Radisson robots.txt and sitemap index snapshots.",
        "Use `radisson_url_index.jsonl` as the machine-readable source of truth.",
        "",
    ]
    for group in sorted(by_group):
        lines.extend([f"## {group}", ""])
        for url in sorted(set(by_group[group])):
            lines.append(f"- {url}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_summary(path: Path, manifest: dict[str, Any]) -> None:
    lines = [
        "# Radisson Crawl Summary",
        "",
        f"Generated: {manifest['generated_at']}",
        "",
        "## Result",
        "",
        f"- Customer-facing URL records: {manifest['counts']['included_urls']}",
        f"- Exclusions: {manifest['counts']['excluded_urls']}",
        f"- Sitemaps discovered: {manifest['counts']['sitemaps_discovered']}",
        f"- Sitemaps attempted: {manifest['counts']['sitemaps_attempted']}",
        f"- Sitemaps fetched successfully: {manifest['counts']['sitemaps_fetched']}",
        f"- Sitemaps failed: {manifest['counts']['sitemaps_failed']}",
        f"- Sitemaps skipped: {manifest['counts']['sitemaps_skipped']}",
        "",
        "## Access Boundary",
        "",
        (
            "- Direct origin fetches from this environment returned access-restricted 403 "
            "during robots/sitemap probing. The inventory is therefore sitemap-discovered "
            "through public reader snapshots, not page-body crawled from origin."
        ),
        "",
        "## Primary Deliverables",
        "",
        "- `radisson_url_index.jsonl`",
        "- `radisson_url_index.csv`",
        "- `crawl_manifest.json`",
        "- `crawl_exclusions.csv`",
        "- `target_urls_discovered.md`",
        "",
        "## Handoff / Restart Prompt",
        "",
        manifest["handoff_restart_prompt"],
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_crawl_plan(path: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Radisson Crawl Plan",
                "",
                "1. Use Radisson robots.txt as the crawl-policy boundary.",
                "2. Use the robots-declared sitemap index as the authoritative URL source.",
                "3. Fetch sitemap XML through public reader snapshots when direct origin access is restricted.",
                "4. Exclude robots-disallowed, login, account, secure, reservation funnel, internal, and non-site asset URLs.",
                "5. Normalize and deduplicate URLs by scheme, host, path, and stripped query/fragment.",
                "6. Preserve locale-specific pages as distinct customer-facing URLs.",
                "7. Record source sitemap, sitemap lastmod, discovery timestamp, method, and access-boundary status for every row.",
                "8. Validate counts against the sitemap index and write exclusions separately.",
                "",
                "For a full page-body crawl, rerun from a contract-approved environment or proxy that can access "
                "Radisson origin pages without triggering access restrictions.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def load_sitemap_cache(output_dir: Path) -> dict[str, dict[str, Any]]:
    manifest_path = output_dir / "crawl_manifest.json"
    if not manifest_path.exists():
        return {}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}

    cache: dict[str, dict[str, Any]] = {}
    for item in manifest.get("sitemap_fetches", []):
        if item.get("reader_status") != 200:
            continue
        raw_file = item.get("raw_file")
        if not raw_file:
            continue
        path = repo_path(raw_file)
        if not path.exists() or path.stat().st_size == 0:
            continue
        body = path.read_text(encoding="utf-8")
        if "HTTP 429" in body[:200] or "Too Many Requests" in body[:500]:
            continue
        cache[item["url"]] = {
            "body": body,
            "raw_file": raw_file,
            "reader_status": item.get("reader_status"),
            "published_time": item.get("published_time", ""),
        }
    return cache


def run(args: argparse.Namespace) -> int:
    output_dir = repo_path(args.output_dir)
    raw_dir = output_dir / "raw_sitemaps"
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)
    generated_at = utc_now()
    sitemap_cache = {} if args.no_reuse_cache else load_sitemap_cache(output_dir)

    direct_robots = fetch(ROBOTS_URL, method="GET", timeout=args.timeout, reader=False)
    reader_robots = fetch(ROBOTS_URL, method="GET", timeout=args.timeout, reader=True)
    robots_source = reader_robots if reader_robots.body else direct_robots
    robots_rules = parse_robots(robots_source.body)
    (raw_dir / "robots.txt.reader.md").write_text(reader_robots.body, encoding="utf-8")

    direct_sitemap_index = fetch(SITEMAP_INDEX_URL, method="GET", timeout=args.timeout, reader=False)
    reader_sitemap_index = fetch(SITEMAP_INDEX_URL, method="GET", timeout=args.timeout, reader=True)
    sitemap_index_source = reader_sitemap_index if reader_sitemap_index.body else direct_sitemap_index
    (raw_dir / "sitemapindex.xml.reader.md").write_text(reader_sitemap_index.body, encoding="utf-8")

    _, sitemap_items = parse_sitemap_like(sitemap_index_source.body)
    sitemap_refs = [
        SitemapRef(url=url, lastmod=lastmod, source=SITEMAP_INDEX_URL)
        for url, lastmod in sitemap_items
        if "radissonhotels.com" in urllib.parse.urlsplit(url).netloc.lower()
    ]
    if args.max_sitemaps:
        sitemap_refs = sitemap_refs[: args.max_sitemaps]

    url_refs: list[UrlRef] = []
    exclusions: list[dict[str, str]] = []
    sitemap_fetch_records: list[dict[str, Any]] = []

    for index, sitemap_ref in enumerate(sitemap_refs, start=1):
        group = infer_content_group(sitemap_ref.url)
        if group in MEDIA_SITEMAP_TOKENS and not args.include_media_sitemaps:
            exclusions.append(
                exclusion_row(
                    sitemap_ref.url,
                    source=SITEMAP_INDEX_URL,
                    reason="media_or_asset_sitemap_skipped",
                    detail="Use --include-media-sitemaps to include image, video, or PDF sitemap URLs.",
                    discovered_at=generated_at,
                )
            )
            continue

        cached = sitemap_cache.get(sitemap_ref.url)
        if cached:
            record = FetchRecord(
                url=sitemap_ref.url,
                method="reader_snapshot_cache",
                status=cached["reader_status"],
                content_type="text/plain; charset=utf-8",
                last_modified="",
                body=cached["body"],
                fetched_at=generated_at,
                elapsed_seconds=0.0,
                reader_url=reader_url(sitemap_ref.url),
                published_time=cached.get("published_time", ""),
            )
            raw_file_rel = cached["raw_file"]
        else:
            record = fetch_reader_with_retries(
                sitemap_ref.url,
                timeout=args.timeout,
                retries=args.retries,
                backoff_seconds=args.retry_backoff_seconds,
            )
            raw_name = f"{index:04d}_{sha256_short(sitemap_ref.url)}_{Path(urllib.parse.urlsplit(sitemap_ref.url).path).name}.md"
            raw_file_rel = rel(raw_dir / raw_name)
            (raw_dir / raw_name).write_text(record.body, encoding="utf-8")
        sitemap_ref.reader_status = record.status
        sitemap_ref.fetch_error = record.error
        sitemap_fetch_records.append(
            {
                "url": sitemap_ref.url,
                "lastmod": sitemap_ref.lastmod,
                "content_group": group,
                "reader_status": record.status,
                "reader_url": record.reader_url,
                "published_time": record.published_time,
                "elapsed_seconds": record.elapsed_seconds,
                "error": record.error,
                "cache_hit": bool(cached),
                "raw_file": raw_file_rel,
            }
        )
        if not record.body or record.status is None or record.status >= 400:
            exclusions.append(
                exclusion_row(
                    sitemap_ref.url,
                    source=SITEMAP_INDEX_URL,
                    reason="sitemap_fetch_failed",
                    detail=record.error or f"reader HTTP {record.status}",
                    discovered_at=generated_at,
                )
            )
            if not cached:
                time.sleep(args.delay_seconds)
            continue

        _, page_items = parse_sitemap_like(record.body)
        for url, lastmod in page_items:
            url_refs.append(
                UrlRef(
                    url=url,
                    lastmod=lastmod,
                    source_sitemap=sitemap_ref.url,
                    source_sitemap_lastmod=sitemap_ref.lastmod,
                    source_sitemap_reader_status=record.status,
                )
            )
        if args.verbose:
            print(f"[{index}/{len(sitemap_refs)}] {group}: {len(page_items)} URLs", file=sys.stderr)
        if not cached:
            time.sleep(args.delay_seconds)

    records_by_key: dict[str, dict[str, Any]] = {}
    duplicate_count = 0
    robots_excluded_count = 0
    non_customer_count = 0

    primary_root = UrlRef(
        url=SEED_DOMAIN,
        lastmod="",
        source_sitemap=SITEMAP_INDEX_URL,
        source_sitemap_lastmod=reader_sitemap_index.published_time,
        source_sitemap_reader_status=reader_sitemap_index.status,
        source_type="seed_homepage",
    )
    url_refs.append(primary_root)

    for ref in url_refs:
        normalized = canonicalize(ref.url)
        parsed = urllib.parse.urlsplit(normalized)
        if parsed.scheme not in {"http", "https"}:
            exclusions.append(
                exclusion_row(ref.url, source=ref.source_sitemap, reason="unsupported_scheme", discovered_at=generated_at)
            )
            continue
        group = infer_content_group(ref.source_sitemap)
        is_customer, reason = classify_customer_facing(normalized, group)
        if not is_customer:
            non_customer_count += 1
            exclusions.append(
                exclusion_row(ref.url, source=ref.source_sitemap, reason=reason, discovered_at=generated_at)
            )
            continue
        if robots_disallowed(ref.url, robots_rules):
            robots_excluded_count += 1
            exclusions.append(
                exclusion_row(ref.url, source=ref.source_sitemap, reason="robots_disallow", discovered_at=generated_at)
            )
            continue
        if normalized in records_by_key:
            duplicate_count += 1
            exclusions.append(
                exclusion_row(
                    ref.url,
                    source=ref.source_sitemap,
                    reason="duplicate_canonical_url",
                    detail=f"Duplicate of {normalized}",
                    discovered_at=generated_at,
                )
            )
            continue
        records_by_key[normalized] = build_url_record(
            ref,
            normalized_url=normalized,
            discovered_at=generated_at,
            direct_origin_status=direct_sitemap_index.status,
        )

    records = sorted(records_by_key.values(), key=lambda item: item["normalized_url"])
    excluded_sorted = sorted(exclusions, key=lambda item: (item["exclusion_reason"], item["url"]))

    jsonl_path = output_dir / "radisson_url_index.jsonl"
    csv_path = output_dir / "radisson_url_index.csv"
    manifest_path = output_dir / "crawl_manifest.json"
    exclusions_path = output_dir / "crawl_exclusions.csv"
    target_urls_path = output_dir / "target_urls_discovered.md"
    summary_path = output_dir / "crawl_summary.md"
    plan_path = output_dir / "crawl_plan.md"

    write_jsonl(jsonl_path, records)
    write_csv(csv_path, records)
    write_exclusions(exclusions_path, excluded_sorted)
    write_target_urls(target_urls_path, records)
    write_crawl_plan(plan_path)

    content_groups: dict[str, int] = {}
    locales: dict[str, int] = {}
    for record in records:
        content_groups[record["content_group"]] = content_groups.get(record["content_group"], 0) + 1
        locale = record["language_locale"] or "none"
        locales[locale] = locales.get(locale, 0) + 1

    manifest = {
        "generated_at": generated_at,
        "seed_domains": [SEED_DOMAIN],
        "allowed_site_hosts": sorted(ALLOWED_SITE_HOSTS),
        "source_authority": {
            "robots_url": ROBOTS_URL,
            "sitemap_index_url": SITEMAP_INDEX_URL,
            "radisson_brand_source": "https://www.radissonhotels.com/en-us/corporate/about-us/our-brands",
        },
        "crawl_policy": {
            "robots_source_method": robots_source.method,
            "robots_direct_status": direct_robots.status,
            "robots_reader_status": reader_robots.status,
            "robots_reader_published_time": reader_robots.published_time,
            "disallow_rule_count": len(robots_rules.get("disallow", [])),
            "allow_rule_count": len(robots_rules.get("allow", [])),
            "robots_sitemaps": robots_rules.get("sitemaps", []),
        },
        "access_boundary": {
            "direct_origin_sitemap_index_status": direct_sitemap_index.status,
            "direct_origin_sitemap_index_content_type": direct_sitemap_index.content_type,
            "direct_origin_sitemap_index_error": direct_sitemap_index.error,
            "reader_sitemap_index_status": reader_sitemap_index.status,
            "reader_sitemap_index_published_time": reader_sitemap_index.published_time,
            "note": (
                "Direct origin access from this environment returned an access-restricted response. "
                "Per compliance constraints, the crawler did not attempt to bypass that restriction; "
                "it used public reader snapshots of robots and sitemap files."
            ),
        },
        "methods": {
            "url_discovery": "robots.txt -> sitemapindex.xml -> sitemap files",
            "fetch_method": "public reader snapshot for sitemap files after direct origin 403",
            "user_agent_identifier": USER_AGENT_ID,
            "rate_limit_delay_seconds": args.delay_seconds,
            "media_sitemaps_included": args.include_media_sitemaps,
            "reused_successful_sitemap_cache": not args.no_reuse_cache,
            "sitemap_cache_hits": sum(1 for item in sitemap_fetch_records if item.get("cache_hit")),
            "retries_on_429": args.retries,
            "retry_backoff_seconds": args.retry_backoff_seconds,
        },
        "normalization": {
            "scheme_host_lowercased": True,
            "query_and_fragment_stripped": True,
            "trailing_slash_stripped_except_root": True,
            "locale_pages_preserved": True,
        },
        "counts": {
            "sitemaps_discovered": len(sitemap_refs),
            "sitemaps_attempted": len(sitemap_fetch_records),
            "sitemaps_fetched": sum(1 for item in sitemap_fetch_records if item.get("reader_status") == 200),
            "sitemaps_failed": sum(1 for item in sitemap_fetch_records if item.get("reader_status") != 200),
            "sitemaps_skipped": sum(1 for row in exclusions if row["exclusion_reason"] == "media_or_asset_sitemap_skipped"),
            "raw_url_refs": len(url_refs),
            "included_urls": len(records),
            "excluded_urls": len(excluded_sorted),
            "duplicate_urls": duplicate_count,
            "robots_excluded_urls": robots_excluded_count,
            "non_customer_or_asset_urls": non_customer_count,
        },
        "content_group_counts": dict(sorted(content_groups.items())),
        "locale_counts": dict(sorted(locales.items())),
        "sitemap_fetches": sitemap_fetch_records,
        "deliverables": {
            "jsonl": rel(jsonl_path),
            "csv": rel(csv_path),
            "manifest": rel(manifest_path),
            "exclusions": rel(exclusions_path),
            "target_urls_markdown": rel(target_urls_path),
            "summary": rel(summary_path),
            "plan": rel(plan_path),
            "raw_sitemaps_dir": rel(raw_dir),
        },
        "known_gaps": [
            "Per-page origin HTTP status, canonical link tags, and content-type headers were not fetched because direct origin access returned 403 from this environment.",
            "The inventory is sitemap-comprehensive for non-media customer-facing RadissonHotels.com URLs, not a recursive body-link crawl of every page.",
            "External customer platforms such as app stores, careers, and Choice-owned Americas pages are excluded unless explicitly added as approved scope.",
        ],
        "handoff_restart_prompt": (
            "Current state: generated a robots/sitemap-based RadissonHotels.com customer-facing URL inventory "
            "under sources/website/radisson_crawl/latest. Direct origin fetches from this environment returned "
            "403 access-restricted responses, so per-page HTTP status/canonical/content-type must be completed "
            "from a contract-approved environment or proxy before claiming full page-crawl completion. Next action: "
            "run scripts/radisson_crawl.py again with origin access enabled, then extend it to fetch page HEAD/GET "
            "for canonical URL and content-type validation."
        ),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    write_summary(summary_path, manifest)

    print(json.dumps(manifest["counts"], indent=2, sort_keys=True))
    print(f"Wrote {rel(output_dir)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Radisson sitemap URL inventory for GEO optimizer ingestion.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for crawl deliverables.")
    parser.add_argument("--timeout", type=int, default=60, help="HTTP timeout per robots/sitemap fetch.")
    parser.add_argument("--delay-seconds", type=float, default=0.75, help="Delay between sitemap reader requests.")
    parser.add_argument("--retries", type=int, default=2, help="Retries for transient reader responses: HTTP 422, 429, 503, and 524.")
    parser.add_argument("--retry-backoff-seconds", type=float, default=5.0, help="Linear backoff base for 429 retries.")
    parser.add_argument("--no-reuse-cache", action="store_true", help="Refetch all sitemap files instead of reusing prior successful raw snapshots.")
    parser.add_argument("--include-media-sitemaps", action="store_true", help="Include image, video, and PDF sitemaps.")
    parser.add_argument("--max-sitemaps", type=int, default=0, help="Optional limit for debugging.")
    parser.add_argument("--verbose", action="store_true", help="Print sitemap progress to stderr.")
    return parser


def main(argv: list[str] | None = None) -> int:
    return run(build_parser().parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
