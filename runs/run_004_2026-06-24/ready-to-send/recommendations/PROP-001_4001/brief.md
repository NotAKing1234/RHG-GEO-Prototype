# PROP-001 - Serve HTTP 200 HTML for all public Country Inn brand and hotel pages selected in run_004, especially /en-us/brand/country-inn, /en-us/brand/

- Run proposal ID: 4001
- Status: ready-to-send
- Priority: P1
- Surface: Strategic / Infrastructure
- Component: Commerce
- Pages: https://www.radissonhotels.com/en-us/brand/country-inn

## Proposed Change
Serve HTTP 200 HTML for all public Country Inn brand and hotel pages selected in run_004, especially /en-us/brand/country-inn, /en-us/brand/country-inn/business-travel-offer, and the selected /en-us/hotels/country-inn-* pages. Keep bot defense behavioral and rate-based rather than returning the Radisson/Akamai access-restricted template to normal search and AI retrieval crawlers. Validate with the same direct GET capture used in runs/run_004_2026-06-24/audit_capture.json.

## Current State
Page-level retrieval remains blocked across the most important English/US Country Inn pages and multiple locale groups. AI systems cannot extract page-specific hotel facts from blocked URLs even though the root robots file is now reachable.

## Rationale
C01

## Impact
Very high. Until the official pages return real HTML, AI travel assistants must rely on OTAs, stale snippets, or localized fallback pages rather than Radisson-owned Country Inn content.

## Jira Summary
Serve HTTP 200 HTML for all public Country Inn brand and hotel pages selected in run_004, especially /en-us/brand/country-inn, /en-us/brand/

## Jira Description
Dev change specs: Serve HTTP 200 HTML for all public Country Inn brand and hotel pages selected in run_004, especially /en-us/brand/country-inn, /en-us/brand/country-inn/business-travel-offer, and the selected /en-us/hotels/country-inn-* pages. Keep bot defense behavioral and rate-based rather than returning the Radisson/Akamai access-restricted template to normal search and AI retrieval crawlers. Validate with the same direct GET capture used in runs/run_004_2026-06-24/audit_capture.json.

SEO/GEO rationale: Public AI/search crawler access for audited pages: The audited URL and domain root return HTTP 200 or indexable redirects for normal browser requests and major retrieval crawlers; /robots.txt is reachable; no WAF/access template blocks the page; pages are eligible for snippets/indexing.

GEO visibility score: P1 / severity-informed.

Validation steps: Confirm the change is present on https://www.radissonhotels.com/en-us/brand/country-inn and rerun GEO audit.

## Acceptance Criteria
- Proposed change is implemented for https://www.radissonhotels.com/en-us/brand/country-inn.
- Validation confirms the run_004_GAP-001 gap is closed or explicitly downgraded.
- Existing visible behavior remains unchanged unless specified in the ticket.

## Evidence Sources
- S1209: developers.google.com
  https://developers.google.com/crawling/docs/troubleshooting/http-status-codes
- S1210: developers.google.com
  https://developers.google.com/search/docs/appearance/ai-features
- S1211: premierinn.com
  https://www.premierinn.com/gb/en/hotels/england/greater-london/london/london-county-hall.html
