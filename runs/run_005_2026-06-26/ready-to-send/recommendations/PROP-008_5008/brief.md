# PROP-008 - Remove utility, picklist, sitemap-like, and test-adjacent URL patterns from run_url_targets selection and from any generated public sitemaps

- Run proposal ID: 5008
- Status: ready-to-send
- Priority: P2
- Surface: Strategic / Infrastructure
- Component: Meetings & Events
- Pages: https://www.radissonhotels.com/en-us/brand/park-plaza/meeting-conference/picklist

## Proposed Change
Remove utility, picklist, sitemap-like, and test-adjacent URL patterns from run_url_targets selection and from any generated public sitemaps, starting with https://www.radissonhotels.com/en-us/brand/park-plaza/meeting-conference/picklist. If utility endpoints must remain public, return crawlable noindex headers or disallow them in robots rules. Replace them in GEO selections with canonical production landing pages for Park Plaza properties, city/destination pages, meeting pages, and offers.

## Current State
The run target set includes utility/test/picklist/sitemap-like URL patterns, especially /meeting-conference/picklist. These may not be production landing pages for AI travel discovery.

## Rationale
C15; Phase 2.5 GAP-008 research cites Google guidance on faceted navigation, blocking indexing, and URL structure: https://developers.google.com/crawling/docs/faceted-navigation, https://developers.google.com/search/docs/crawling-indexing/block-indexing, https://developers.google.com/search/docs/crawling-indexing/url-structure.

## Impact
Medium. Cleaner target sets reduce crawl waste and AI confusion so assistants find useful Park Plaza meeting, property, city, and offer pages rather than internal utility pages.

## Jira Summary
Remove utility, picklist, sitemap-like, and test-adjacent URL patterns from run_url_targets selection and from any generated public sitemaps

## Jira Description
Dev change specs: Remove utility, picklist, sitemap-like, and test-adjacent URL patterns from run_url_targets selection and from any generated public sitemaps, starting with https://www.radissonhotels.com/en-us/brand/park-plaza/meeting-conference/picklist. If utility endpoints must remain public, return crawlable noindex headers or disallow them in robots rules. Replace them in GEO selections with canonical production landing pages for Park Plaza properties, city/destination pages, meeting pages, and offers.

SEO/GEO rationale: Selected pages are production-grade, not tests, empty shells, or thin utility pages: Selected URLs are public production pages with meaningful title, meta, canonical, content, and page purpose.

GEO visibility score: P2 / severity-informed.

Validation steps: Confirm the change is present on https://www.radissonhotels.com/en-us/brand/park-plaza/meeting-conference/picklist and rerun GEO audit.

## Acceptance Criteria
- Proposed change is implemented for https://www.radissonhotels.com/en-us/brand/park-plaza/meeting-conference/picklist.
- Validation confirms the run_005_GAP-008 gap is closed or explicitly downgraded.
- Existing visible behavior remains unchanged unless specified in the ticket.

## Evidence Sources
- S1294: developers.google.com
  https://developers.google.com/crawling/docs/faceted-navigation
- S1295: developers.google.com
  https://developers.google.com/search/docs/crawling-indexing/block-indexing
- S1296: developers.google.com
  https://developers.google.com/search/docs/crawling-indexing/url-structure
- S1297: hyatt.com
  https://www.hyatt.com/robots.txt
