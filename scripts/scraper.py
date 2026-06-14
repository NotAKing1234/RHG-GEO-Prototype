#!/usr/bin/env python3
"""Fetch target URLs and extract page metadata for a GEO audit snapshot."""

from __future__ import annotations

import argparse
import json
import logging
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:  # pragma: no cover - runtime fallback
    requests = None  # type: ignore[assignment]

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover - runtime fallback
    BeautifulSoup = None  # type: ignore[assignment]


ROOT = Path(__file__).resolve().parents[1]
URL_RE = re.compile(r"https?://[^\s)<>'\"]+")
IMPORTANT_SCHEMA_TYPES = {
    "Hotel",
    "LodgingBusiness",
    "FAQPage",
    "LocalBusiness",
    "Organization",
    "BreadcrumbList",
    "ItemList",
    "WebPage",
    "MemberProgram",
    "Offer",
    "Product",
}

HEADER_PROFILES = [
    {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
    },
    {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) "
            "Gecko/20100101 Firefox/126.0"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    },
    {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    },
]


@dataclass
class TargetURL:
    source_url: str
    canonical_url: str
    priority: str
    line_number: int


@dataclass
class FetchResult:
    ok: bool
    status_code: int | None
    method: str
    html: str
    error: str = ""
    final_url: str = ""
    elapsed_seconds: float = 0.0


@dataclass
class PageMetadata:
    url: str
    source_url: str
    priority: str
    fetch_status: str
    fetch_method: str
    fetch_timestamp: str
    final_url: str = ""
    title: str = "NONE"
    meta_description: str = "NONE"
    schema_types: list[str] = field(default_factory=list)
    json_ld_blocks: list[Any] = field(default_factory=list)
    invalid_json_ld_blocks: list[str] = field(default_factory=list)
    og_tags: dict[str, str] = field(default_factory=dict)
    headings: dict[str, list[str]] = field(default_factory=dict)
    faq_presence: str = "NOT DETECTED"
    image_alt_texts: list[str] = field(default_factory=list)
    image_alt_missing_count: int = 0
    query_compatibility_notes: str = "Requires agent review against current criteria."
    entity_signal_notes: str = "Requires agent review against current criteria."
    error: str = ""


def repo_path(path: str | Path) -> Path:
    path = Path(path)
    return path if path.is_absolute() else ROOT / path


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def canonicalize_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url.strip())
    path = parsed.path or "/"
    return urllib.parse.urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path.rstrip("/") or "/", "", ""))


def trim_url(url: str) -> str:
    return url.rstrip(".,;]")


def parse_target_urls(filepath: str | Path) -> list[TargetURL]:
    path = repo_path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Target URL file not found: {path}")

    targets: list[TargetURL] = []
    seen: set[str] = set()
    priority = "Uncategorized"
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        heading_match = re.match(r"^##\s+(.+)$", line.strip())
        if heading_match:
            priority = heading_match.group(1).strip()
        for raw in URL_RE.findall(line):
            source_url = trim_url(raw)
            canonical = canonicalize_url(source_url)
            if canonical in seen:
                logging.info("Skipping duplicate target URL at line %s: %s", line_number, canonical)
                continue
            seen.add(canonical)
            targets.append(
                TargetURL(
                    source_url=source_url,
                    canonical_url=canonical,
                    priority=priority,
                    line_number=line_number,
                )
            )
    return targets


def decode_response_body(raw: bytes, headers: Any) -> str:
    charset = None
    content_type = ""
    if hasattr(headers, "get"):
        content_type = headers.get("content-type") or headers.get("Content-Type") or ""
    charset_match = re.search(r"charset=([^;\s]+)", content_type, flags=re.IGNORECASE)
    if charset_match:
        charset = charset_match.group(1)
    for encoding in [charset, "utf-8", "latin-1"]:
        if not encoding:
            continue
        try:
            return raw.decode(encoding, errors="replace")
        except LookupError:
            continue
    return raw.decode("utf-8", errors="replace")


def request_get(url: str, *, headers: dict[str, str] | None = None, params: dict[str, str] | None = None, timeout: int) -> FetchResult:
    started = time.monotonic()
    if requests is not None:
        try:
            response = requests.get(url, headers=headers, params=params, timeout=timeout)
            elapsed = time.monotonic() - started
            return FetchResult(
                ok=response.ok,
                status_code=response.status_code,
                method="requests",
                html=response.text or "",
                error="" if response.ok else f"HTTP {response.status_code}",
                final_url=response.url,
                elapsed_seconds=elapsed,
            )
        except requests.RequestException as exc:  # type: ignore[union-attr]
            return FetchResult(False, None, "requests", "", str(exc), "", time.monotonic() - started)

    full_url = url
    if params:
        full_url = f"{url}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(full_url, headers=headers or {})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
            elapsed = time.monotonic() - started
            status = getattr(response, "status", None) or response.getcode()
            return FetchResult(
                ok=200 <= int(status) < 400,
                status_code=int(status),
                method="urllib",
                html=decode_response_body(raw, response.headers),
                final_url=response.geturl(),
                elapsed_seconds=elapsed,
            )
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        return FetchResult(
            ok=False,
            status_code=exc.code,
            method="urllib",
            html=decode_response_body(raw, exc.headers),
            error=f"HTTP {exc.code}",
            final_url=full_url,
            elapsed_seconds=time.monotonic() - started,
        )
    except urllib.error.URLError as exc:
        return FetchResult(False, None, "urllib", "", str(exc), full_url, time.monotonic() - started)


def fetch_via_zenrows(url: str, timeout: int) -> FetchResult | None:
    api_key = os.getenv("ZENROWS_API_KEY")
    if not api_key:
        return None
    params = {
        "apikey": api_key,
        "url": url,
        "js_render": "true",
        "premium_proxy": "true",
    }
    result = request_get("https://api.zenrows.com/v1/", params=params, timeout=timeout)
    result.method = "ZenRows"
    return result


def fetch_via_scrapingbee(url: str, timeout: int) -> FetchResult | None:
    api_key = os.getenv("SCRAPINGBEE_API_KEY")
    if not api_key:
        return None
    params = {
        "api_key": api_key,
        "url": url,
        "render_js": "true",
        "block_ads": "true",
    }
    result = request_get("https://app.scrapingbee.com/api/v1/", params=params, timeout=timeout)
    result.method = "ScrapingBee"
    return result


def fetch_direct(url: str, timeout: int) -> FetchResult:
    profiles = HEADER_PROFILES[:]
    random.shuffle(profiles)
    last_result = FetchResult(False, None, "direct", "", "No attempts made")
    for index, headers in enumerate(profiles, start=1):
        result = request_get(url, headers=headers, timeout=timeout)
        result.method = f"Direct header profile {index}"
        if result.ok and result.html:
            return result
        last_result = result
        if result.status_code not in {403, 429, 500, 502, 503, 504, None}:
            return result
        time.sleep(0.4)
    return last_result


def scrape_page(url: str, timeout: int) -> FetchResult:
    attempts: list[tuple[str, FetchResult | None]] = [
        ("ZenRows", fetch_via_zenrows(url, timeout)),
        ("ScrapingBee", fetch_via_scrapingbee(url, timeout)),
    ]

    for label, result in attempts:
        if result is None:
            continue
        logging.info("%s fetch returned %s for %s", label, result.status_code or result.error, url)
        if result.ok and result.html:
            return result

    result = fetch_direct(url, timeout)
    logging.info("Direct fetch returned %s for %s", result.status_code or result.error, url)
    return result


def compact_text(value: str | None, default: str = "NONE") -> str:
    if not value:
        return default
    value = re.sub(r"\s+", " ", value).strip()
    return value or default


def truncate(value: str, limit: int = 500) -> str:
    value = compact_text(value, "")
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def schema_type_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value if item]
    return []


def collect_schema_types(obj: Any) -> list[str]:
    found: list[str] = []
    if isinstance(obj, dict):
        found.extend(schema_type_values(obj.get("@type")))
        for key in ("@graph", "mainEntity", "itemListElement", "hasPart"):
            if key in obj:
                found.extend(collect_schema_types(obj[key]))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(collect_schema_types(item))
    ordered: list[str] = []
    for item in found:
        if item not in ordered:
            ordered.append(item)
    return ordered


def parse_json_ld_block(raw: str) -> tuple[Any | None, str | None]:
    raw = raw.strip()
    if not raw:
        return None, None
    try:
        return json.loads(raw), None
    except json.JSONDecodeError as exc:
        return None, f"{exc}: {truncate(raw, 300)}"


def extract_metadata_with_bs4(html: str) -> dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")  # type: ignore[operator]

    title = compact_text(soup.title.string if soup.title else None)
    description_tag = soup.find("meta", attrs={"name": re.compile(r"^description$", re.IGNORECASE)})
    meta_description = compact_text(description_tag.get("content") if description_tag else None)

    json_ld_blocks: list[Any] = []
    invalid_json_ld_blocks: list[str] = []
    schema_types: list[str] = []
    for script in soup.find_all("script"):
        script_type = compact_text(script.get("type"), "")
        if "ld+json" not in script_type.lower():
            continue
        parsed, error = parse_json_ld_block(script.string or script.get_text(" ", strip=True))
        if parsed is not None:
            json_ld_blocks.append(parsed)
            schema_types.extend(collect_schema_types(parsed))
        elif error:
            invalid_json_ld_blocks.append(error)

    og_tags: dict[str, str] = {}
    for meta in soup.find_all("meta"):
        prop = meta.get("property") or meta.get("name")
        if not prop:
            continue
        prop = str(prop)
        if prop.lower().startswith("og:"):
            og_tags[prop] = truncate(str(meta.get("content") or ""), 500)

    headings: dict[str, list[str]] = {"h1": [], "h2": [], "h3": []}
    for level in headings:
        for tag in soup.find_all(level):
            text = compact_text(tag.get_text(" ", strip=True), "")
            if text:
                headings[level].append(text)
        headings[level] = headings[level][:20]

    image_alt_texts: list[str] = []
    missing_alt = 0
    for image in soup.find_all("img"):
        alt = compact_text(image.get("alt"), "")
        if alt:
            image_alt_texts.append(alt)
        else:
            missing_alt += 1

    all_text = soup.get_text(" ", strip=True).lower()
    faq_presence = "NOT DETECTED"
    if "FAQPage" in schema_types:
        faq_presence = "FAQPage JSON-LD detected"
    elif re.search(r"\b(frequently asked questions|faq|q&a)\b", all_text):
        faq_presence = "Visible FAQ/Q&A text detected; schema not confirmed"

    ordered_schema_types: list[str] = []
    for item in schema_types:
        if item not in ordered_schema_types:
            ordered_schema_types.append(item)

    return {
        "title": title,
        "meta_description": meta_description,
        "schema_types": ordered_schema_types,
        "json_ld_blocks": json_ld_blocks,
        "invalid_json_ld_blocks": invalid_json_ld_blocks,
        "og_tags": og_tags,
        "headings": headings,
        "faq_presence": faq_presence,
        "image_alt_texts": image_alt_texts[:30],
        "image_alt_missing_count": missing_alt,
    }


def extract_metadata_fallback(html: str) -> dict[str, Any]:
    logging.warning("beautifulsoup4 is not installed; using reduced regex extraction.")
    title_match = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
    description_match = re.search(
        r"<meta[^>]+name=[\"']description[\"'][^>]+content=[\"']([^\"']+)[\"']",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    headings: dict[str, list[str]] = {"h1": [], "h2": [], "h3": []}
    for level in headings:
        pattern = rf"<{level}[^>]*>(.*?)</{level}>"
        headings[level] = [
            compact_text(re.sub(r"<[^>]+>", " ", match), "")
            for match in re.findall(pattern, html, flags=re.IGNORECASE | re.DOTALL)
        ][:20]
    return {
        "title": compact_text(title_match.group(1) if title_match else None),
        "meta_description": compact_text(description_match.group(1) if description_match else None),
        "schema_types": [],
        "json_ld_blocks": [],
        "invalid_json_ld_blocks": [],
        "og_tags": {},
        "headings": headings,
        "faq_presence": "NOT DETECTED",
        "image_alt_texts": [],
        "image_alt_missing_count": 0,
    }


def extract_metadata(html: str) -> dict[str, Any]:
    if BeautifulSoup is not None:
        return extract_metadata_with_bs4(html)
    return extract_metadata_fallback(html)


def parse_previous_snapshot(filepath: str | Path | None) -> dict[str, dict[str, str]]:
    if not filepath:
        return {}
    path = repo_path(filepath)
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    sections = re.split(r"(?=^##\s+Page\s+\d+)", text, flags=re.MULTILINE)
    previous: dict[str, dict[str, str]] = {}
    for section in sections:
        url_match = re.search(r"\*\*URL:\*\*\s*(\S+)", section)
        if not url_match:
            heading_url = URL_RE.search(section.splitlines()[0] if section.splitlines() else "")
            url_match = heading_url
        if not url_match:
            continue
        url = canonicalize_url(url_match.group(1))
        previous[url] = {
            "title": extract_bold_line(section, ["Extracted title", "Title"]),
            "meta_description": extract_bold_line(
                section,
                ["Extracted meta description", "Extracted meta/brand copy", "Meta Description"],
            ),
            "schema": extract_bold_line(section, ["JSON-LD Schema Types", "Structured data blocks", "Structured data"]),
            "fetch_status": extract_bold_line(section, ["Fetch status"]),
        }
    return previous


def extract_bold_line(text: str, labels: list[str]) -> str:
    for line in text.splitlines():
        match = re.match(r"\*\*([^*]+):\*\*\s*(.*)", line.strip())
        if not match:
            continue
        label = match.group(1).lower()
        for expected in labels:
            if label.startswith(expected.lower()):
                return compact_text(match.group(2), "NONE")
    return "NONE"


def build_mock_metadata(target: TargetURL, previous: dict[str, dict[str, str]]) -> PageMetadata:
    prior = previous.get(target.canonical_url, {})
    title = prior.get("title") or "PENDING MANUAL METADATA"
    meta = prior.get("meta_description") or "PENDING MANUAL METADATA"
    schema = prior.get("schema") or "NOT CONFIRMABLE"
    schema_types = [] if schema.upper() in {"NONE", "NOT CONFIRMABLE"} else [schema]
    return PageMetadata(
        url=target.canonical_url,
        source_url=target.source_url,
        priority=target.priority,
        fetch_status="SKIPPED_MOCK - live fetch not attempted",
        fetch_method="mock snapshot outline",
        fetch_timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        title=title,
        meta_description=meta,
        schema_types=schema_types,
        faq_presence="PENDING MANUAL REVIEW",
        query_compatibility_notes="Mock outline generated because --skip-scrape was used.",
        entity_signal_notes="Mock outline generated from previous snapshot when available.",
    )


def metadata_from_fetch(target: TargetURL, result: FetchResult) -> PageMetadata:
    status_text = "FETCH FAILED"
    if result.status_code is not None:
        status_text = f"{result.status_code} {'OK' if result.ok else 'Blocked/Error'}"
    if result.status_code == 403:
        status_text = "403 Blocked"
    elif result.status_code == 429:
        status_text = "429 Rate Limited"

    page = PageMetadata(
        url=target.canonical_url,
        source_url=target.source_url,
        priority=target.priority,
        fetch_status=status_text,
        fetch_method=result.method,
        fetch_timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        final_url=result.final_url,
        error=result.error,
    )

    if result.html:
        extracted = extract_metadata(result.html)
        for key, value in extracted.items():
            setattr(page, key, value)
    elif result.error:
        page.query_compatibility_notes = f"Fetch failed before content extraction: {result.error}"
        page.entity_signal_notes = "No page content available for entity extraction."

    if result.status_code in {403, 429, 503}:
        page.query_compatibility_notes = (
            "Fetch blocked or rate-limited. Use --skip-scrape for a mock outline or provide proxy credentials."
        )
        page.entity_signal_notes = "Entity signals not confirmable from blocked fetch."
    return page


def markdown_value(value: str, limit: int = 1200) -> str:
    return truncate(value or "NONE", limit)


def format_json_block(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True)


def write_snapshot(pages: list[PageMetadata], output_path: Path, run_id: str, run_date: str, skip_scrape: bool) -> None:
    lines: list[str] = [
        f"# Metadata Snapshot — {run_id} | {run_date}",
        "",
        f"**Fetch method:** {'Mock snapshot outlines generated with --skip-scrape.' if skip_scrape else 'Automated scraper with proxy hooks and rotating direct headers.'}",
        f"**Fetch timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Pages audited:** {len(pages)}",
        "",
        "---",
        "",
    ]

    for index, page in enumerate(pages, start=1):
        lines.extend(
            [
                f"## Page {index}: {page.url}",
                "",
                f"**URL:** {page.url}",
                f"**Source URL:** {page.source_url}",
                f"**Priority:** {page.priority}",
                f"**Fetch status:** {page.fetch_status}",
                f"**Fetch method:** {page.fetch_method}",
                f"**Fetch timestamp:** {page.fetch_timestamp}",
            ]
        )
        if page.final_url and page.final_url != page.source_url:
            lines.append(f"**Final URL:** {page.final_url}")
        if page.error:
            lines.append(f"**Fetch error:** {markdown_value(page.error)}")
        lines.extend(
            [
                "",
                f"**Extracted title:** {markdown_value(page.title)}",
                f"**Extracted meta description:** {markdown_value(page.meta_description)}",
                "",
                f"**JSON-LD Schema Types:** {', '.join(page.schema_types) if page.schema_types else 'NONE'}",
            ]
        )
        important = [item for item in page.schema_types if item in IMPORTANT_SCHEMA_TYPES]
        lines.append(
            f"**Priority Schema Matches:** {', '.join(important) if important else 'NONE'}"
        )

        if page.json_ld_blocks:
            lines.append("**Structured data blocks:**")
            for block_number, block in enumerate(page.json_ld_blocks[:5], start=1):
                lines.extend(["", f"```json", format_json_block(block)[:8000], "```"])
            if len(page.json_ld_blocks) > 5:
                lines.append(f"_Truncated: {len(page.json_ld_blocks) - 5} additional JSON-LD blocks._")
        else:
            lines.append("**Structured data blocks:** NONE")
        if page.invalid_json_ld_blocks:
            lines.append("**Invalid JSON-LD blocks:**")
            for block in page.invalid_json_ld_blocks[:3]:
                lines.append(f"- {markdown_value(block, 500)}")

        lines.extend(["", "**Open Graph tags:**"])
        if page.og_tags:
            for key in sorted(page.og_tags):
                lines.append(f"- `{key}`: {markdown_value(page.og_tags[key], 700)}")
        else:
            lines.append("- NONE")

        lines.extend(["", "**Heading outline:**"])
        any_heading = False
        for level in ("h1", "h2", "h3"):
            for heading in page.headings.get(level, []):
                any_heading = True
                lines.append(f"- {level.upper()}: {markdown_value(heading, 400)}")
        if not any_heading:
            lines.append("- NONE")

        lines.extend(
            [
                "",
                f"**FAQ / Q&A presence:** {markdown_value(page.faq_presence)}",
                "",
                "**Alt text observations:**",
            ]
        )
        if page.image_alt_texts:
            lines.append(f"- Images with alt text captured: {len(page.image_alt_texts)}")
            for alt in page.image_alt_texts[:12]:
                lines.append(f"- ALT: {markdown_value(alt, 300)}")
        else:
            lines.append("- No image alt text captured")
        lines.append(f"- Images missing alt text: {page.image_alt_missing_count}")

        lines.extend(
            [
                "",
                f"**Query compatibility notes:** {markdown_value(page.query_compatibility_notes)}",
                "",
                f"**Entity signal notes:** {markdown_value(page.entity_signal_notes)}",
                "",
                "---",
                "",
            ]
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def summarize_pages(pages: list[PageMetadata], output_path: Path) -> dict[str, Any]:
    scraped = sum(1 for page in pages if page.fetch_status.startswith("200"))
    blocked = sum(1 for page in pages if "Blocked" in page.fetch_status or page.fetch_status.startswith("403"))
    skipped = sum(1 for page in pages if page.fetch_status.startswith("SKIPPED_MOCK"))
    return {
        "target_urls_count": len(pages),
        "scraped_count": scraped,
        "blocked_count": blocked,
        "skipped_count": skipped,
        "output": display_path(output_path),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scrape target URLs into metadata_snapshot.md.")
    parser.add_argument("--targets", default="sources/website/target_urls.md", help="Markdown file containing target URLs.")
    parser.add_argument("--run-dir", required=True, help="Current run directory.")
    parser.add_argument("--run-id", required=True, help="Current run id, e.g. run_004.")
    parser.add_argument("--run-date", required=True, help="Current run date in YYYY-MM-DD format.")
    parser.add_argument("--output", help="Output metadata snapshot path. Defaults to RUN_DIR/metadata_snapshot.md.")
    parser.add_argument("--previous-snapshot", help="Previous run metadata snapshot for mock outlines.")
    parser.add_argument("--summary-json", help="Optional path for machine-readable scrape summary.")
    parser.add_argument("--timeout", type=int, default=25, help="HTTP timeout in seconds.")
    parser.add_argument("--skip-scrape", action="store_true", help="Generate mock snapshot outlines instead of fetching.")
    return parser


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    args = build_parser().parse_args(argv)

    run_dir = repo_path(args.run_dir)
    output_path = repo_path(args.output) if args.output else run_dir / "metadata_snapshot.md"
    targets = parse_target_urls(args.targets)
    if not targets:
        logging.error("No target URLs found in %s", args.targets)
        return 2

    logging.info("Loaded %s target URLs from %s", len(targets), args.targets)
    pages: list[PageMetadata] = []

    if args.skip_scrape:
        previous = parse_previous_snapshot(args.previous_snapshot)
        logging.info("Generating mock snapshot outlines for %s targets.", len(targets))
        for target in targets:
            pages.append(build_mock_metadata(target, previous))
    else:
        for index, target in enumerate(targets, start=1):
            logging.info("[%s/%s] Fetching %s", index, len(targets), target.source_url)
            result = scrape_page(target.source_url, args.timeout)
            pages.append(metadata_from_fetch(target, result))

    write_snapshot(pages, output_path, args.run_id, args.run_date, args.skip_scrape)
    summary = summarize_pages(pages, output_path)
    logging.info("Wrote %s", display_path(output_path))
    logging.info(
        "Scrape summary: %s scraped, %s blocked, %s skipped",
        summary["scraped_count"],
        summary["blocked_count"],
        summary["skipped_count"],
    )

    if args.summary_json:
        summary_path = repo_path(args.summary_json)
        summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        logging.info("Wrote %s", display_path(summary_path))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
