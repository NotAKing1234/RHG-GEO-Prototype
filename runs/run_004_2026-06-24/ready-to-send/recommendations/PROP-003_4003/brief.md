# PROP-003 - Serve https://www.radissonhotels.com/sitemap.xml or a sitemap-index URL as HTTP 200 XML

- Run proposal ID: 4003
- Status: ready-to-send
- Priority: P1
- Surface: Strategic / Infrastructure
- Component: Platform
- Pages: https://www.radissonhotels.com/sitemap.xml

## Proposed Change
Serve https://www.radissonhotels.com/sitemap.xml or a sitemap-index URL as HTTP 200 XML. Include canonical public pages only, split by locale, brand, and hotel where needed, reference the sitemap in /robots.txt, and exclude banner-test or non-production URLs.

## Current State
The root crawl rules are accessible, but the standard sitemap endpoint is not. This weakens discovery for assistants and search systems that rely on sitemap discovery or sitemap-index traversal.

## Rationale
C01

## Impact
High. A fixed sitemap can be retested immediately and improves discovery, Search Console diagnostics, and canonical URL coverage for AI/search systems.

## Jira Summary
Serve https://www.radissonhotels.com/sitemap.xml or a sitemap-index URL as HTTP 200 XML

## Jira Description
Dev change specs: Serve https://www.radissonhotels.com/sitemap.xml or a sitemap-index URL as HTTP 200 XML. Include canonical public pages only, split by locale, brand, and hotel where needed, reference the sitemap in /robots.txt, and exclude banner-test or non-production URLs.

SEO/GEO rationale: Public AI/search crawler access for audited pages: The audited URL and domain root return HTTP 200 or indexable redirects for normal browser requests and major retrieval crawlers; /robots.txt is reachable; no WAF/access template blocks the page; pages are eligible for snippets/indexing.

GEO visibility score: P1 / severity-informed.

Validation steps: Confirm the change is present on https://www.radissonhotels.com/sitemap.xml and rerun GEO audit.

## Acceptance Criteria
- Proposed change is implemented for https://www.radissonhotels.com/sitemap.xml.
- Validation confirms the run_004_GAP-003 gap is closed or explicitly downgraded.
- Existing visible behavior remains unchanged unless specified in the ticket.

## Evidence Sources
- S1214: developers.google.com
  https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- S1215: wyndhamhotels.com
  https://www.wyndhamhotels.com/sitemap.xml
- S1216: hilton.com
  https://www.hilton.com/sitemap.xml
- S1217: kayak.com
  https://www.kayak.com/sitemap.xml
