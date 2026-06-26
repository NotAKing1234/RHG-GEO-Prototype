# PROP-004 - Add /llms.txt with a short official Radisson Hotel Group overview, supported domains, core brands, booking paths, canonical Country Inn bran

- Run proposal ID: 4004
- Status: ready-to-send
- Priority: P3
- Surface: Metadata / Structured Data
- Component: Commerce
- Pages: https://www.radissonhotels.com/llms.txt

## Proposed Change
Add /llms.txt with a short official Radisson Hotel Group overview, supported domains, core brands, booking paths, canonical Country Inn brand/hotel URLs, US-to-Europe traveler guidance, and links to XML sitemaps. Keep it factual and update it from the same canonical source as sitemap/brand navigation.

## Current State
No AI-oriented site summary file is present. This remains lower priority than page access and schema, but it is a cheap future-facing protocol gap.

## Rationale
C01

## Impact
Low to medium. It will not compensate for blocked HTML, but it gives AI agents an official orientation file once the main crawl path is fixed.

## Jira Summary
Add /llms.txt with a short official Radisson Hotel Group overview, supported domains, core brands, booking paths, canonical Country Inn bran

## Jira Description
Dev change specs: Add /llms.txt with a short official Radisson Hotel Group overview, supported domains, core brands, booking paths, canonical Country Inn brand/hotel URLs, US-to-Europe traveler guidance, and links to XML sitemaps. Keep it factual and update it from the same canonical source as sitemap/brand navigation.

SEO/GEO rationale: Public AI/search crawler access for audited pages: The audited URL and domain root return HTTP 200 or indexable redirects for normal browser requests and major retrieval crawlers; /robots.txt is reachable; no WAF/access template blocks the page; pages are eligible for snippets/indexing.

GEO visibility score: P3 / severity-informed.

Validation steps: Confirm the change is present on https://www.radissonhotels.com/llms.txt and rerun GEO audit.

## Acceptance Criteria
- Proposed change is implemented for https://www.radissonhotels.com/llms.txt.
- Validation confirms the run_004_GAP-004 gap is closed or explicitly downgraded.
- Existing visible behavior remains unchanged unless specified in the ticket.

## Evidence Sources
- S1218: llmstxt.org
  https://llmstxt.org/
- S1219: web.dev
  https://web.dev/articles/ai-agent-site-ux
- S1220: expedia.com
  https://www.expedia.com/llms.txt
- S1221: wyndhamhotels.com
  https://www.wyndhamhotels.com/llms.txt
