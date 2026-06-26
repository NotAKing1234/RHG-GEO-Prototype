# PROP-006 - Serve https://www.radissonhotels.com/sitemap.xml as public HTTP 200 XML or a sitemap index before WAF/challenge rules

- Run proposal ID: 5006
- Status: ready-to-send
- Priority: P1
- Surface: Strategic / Infrastructure
- Component: Meetings & Events
- Pages: https://www.radissonhotels.com/sitemap.xml

## Proposed Change
Serve https://www.radissonhotels.com/sitemap.xml as public HTTP 200 XML or a sitemap index before WAF/challenge rules. Segment Park Plaza sitemap coverage by brand, hotel/property, meetings, offers, and locale alternates; include only canonical 200 URLs with accurate lastmod; reference the sitemap in /robots.txt; and submit the sitemap index in Google Search Console and Bing Webmaster Tools.

## Current State
The standard /sitemap.xml endpoint returned HTTP 403 while /robots.txt returned HTTP 200. This weakens discovery even after the page-level access fix.

## Rationale
C01; Phase 2.5 GAP-006 research cites Google sitemap guidance and the Sitemaps protocol: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap and https://www.sitemaps.org/protocol.html.

## Impact
High and fast to measure. A public sitemap accelerates recrawl and gives search/AI systems a canonical URL map for long-tail Park Plaza property and meeting pages.

## Jira Summary
Serve https://www.radissonhotels.com/sitemap.xml as public HTTP 200 XML or a sitemap index before WAF/challenge rules

## Jira Description
Dev change specs: Serve https://www.radissonhotels.com/sitemap.xml as public HTTP 200 XML or a sitemap index before WAF/challenge rules. Segment Park Plaza sitemap coverage by brand, hotel/property, meetings, offers, and locale alternates; include only canonical 200 URLs with accurate lastmod; reference the sitemap in /robots.txt; and submit the sitemap index in Google Search Console and Bing Webmaster Tools.

SEO/GEO rationale: Public AI/search crawler access for every selected page: The audited URL returns HTTP 200 useful HTML or an indexable redirect; failures such as 403, AccessDenied, timeout, empty HTML, or blocked templates are recorded precisely.

GEO visibility score: P1 / severity-informed.

Validation steps: Confirm the change is present on https://www.radissonhotels.com/sitemap.xml and rerun GEO audit.

## Acceptance Criteria
- Proposed change is implemented for https://www.radissonhotels.com/sitemap.xml.
- Validation confirms the run_005_GAP-006 gap is closed or explicitly downgraded.
- Existing visible behavior remains unchanged unless specified in the ticket.

## Evidence Sources
- S1286: developers.google.com
  https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- S1287: sitemaps.org
  https://www.sitemaps.org/protocol.html
- S1288: hyatt.com
  https://www.hyatt.com/robots.txt
- S1289: radissonhotels.com
  https://www.radissonhotels.com/sitemap.xml`
