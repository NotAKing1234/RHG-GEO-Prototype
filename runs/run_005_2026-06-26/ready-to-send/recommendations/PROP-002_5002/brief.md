# PROP-002 - After access is restored, run a locale QA pass for every selected en-us Park Plaza URL

- Run proposal ID: 5002
- Status: ready-to-send
- Priority: P1
- Surface: Strategic / Infrastructure
- Component: Platform
- Pages: https://www.radissonhotels.com/en-us/brand/park-plaza

## Proposed Change
After access is restored, run a locale QA pass for every selected en-us Park Plaza URL. Require each page to return US-English content, a self-referencing canonical, reciprocal hreflang alternates for equivalent language/region pages, and no canonical or hreflang reference to the access-restricted template. Start validation from https://www.radissonhotels.com/en-us/brand/park-plaza and extend it to all 478 selected URLs.

## Current State
All selected URLs are en-us, but the English/US Park Plaza path is not yielding retrievable page content from this environment. Locale, canonical, and hreflang quality cannot be validated because the access template replaces the underlying page.

## Rationale
C02; Phase 2.5 GAP-002 research cites Google localized versions and canonical guidance: https://developers.google.com/search/docs/specialty/international/localized-versions and https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls.

## Impact
Very high. American travelers asking AI tools for official Park Plaza hotels in Europe need assistants to select the US-English official page, not a blocked template or uncertain regional fallback.

## Jira Summary
After access is restored, run a locale QA pass for every selected en-us Park Plaza URL

## Jira Description
Dev change specs: After access is restored, run a locale QA pass for every selected en-us Park Plaza URL. Require each page to return US-English content, a self-referencing canonical, reciprocal hreflang alternates for equivalent language/region pages, and no canonical or hreflang reference to the access-restricted template. Start validation from https://www.radissonhotels.com/en-us/brand/park-plaza and extend it to all 478 selected URLs.

SEO/GEO rationale: English/US and European localized pages expose coherent language, canonical, and alternate signals: HTML lang, canonical, hreflang alternates, title/meta language, and URL locale are consistent with the selected page purpose.

GEO visibility score: P1 / severity-informed.

Validation steps: Confirm the change is present on https://www.radissonhotels.com/en-us/brand/park-plaza and rerun GEO audit.

## Acceptance Criteria
- Proposed change is implemented for https://www.radissonhotels.com/en-us/brand/park-plaza.
- Validation confirms the run_005_GAP-002 gap is closed or explicitly downgraded.
- Existing visible behavior remains unchanged unless specified in the ticket.

## Evidence Sources
- S1270: developers.google.com
  https://developers.google.com/search/docs/specialty/international/localized-versions
- S1271: developers.google.com
  https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- S1272: marriott.com
  https://www.marriott.com/en-us/hotels/parar-ac-hotel-paris-porte-maillot/overview/
