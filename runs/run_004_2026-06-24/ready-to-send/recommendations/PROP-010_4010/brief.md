# PROP-010 - Move banner-tests URLs behind authentication or return noindex via meta robots or X-Robots-Tag; remove them from XML sitemaps, registry sele

- Run proposal ID: 4010
- Status: ready-to-send
- Priority: P2
- Surface: Metadata / Structured Data
- Component: Platform
- Pages: https://www.radissonhotels.com/sv-se/marke/country-inn/banner-tests

## Proposed Change
Move banner-tests URLs behind authentication or return noindex via meta robots or X-Robots-Tag; remove them from XML sitemaps, registry selection, and future run targets. Add a pre-run selection check that rejects public URLs with empty title, meta description, canonical, OG fields, and structured data unless explicitly marked as test-only.

## Current State
Non-production or testing URLs appear in the run target set and are publicly fetchable without meaningful metadata. These pages should not be selected for GEO audit or indexation unless intentionally public.

## Rationale
C17

## Impact
Medium. This is a fast cleanup that prevents AI/search systems and future audits from sampling broken test pages.

## Jira Summary
Move banner-tests URLs behind authentication or return noindex via meta robots or X-Robots-Tag; remove them from XML sitemaps, registry sele

## Jira Description
Dev change specs: Move banner-tests URLs behind authentication or return noindex via meta robots or X-Robots-Tag; remove them from XML sitemaps, registry selection, and future run targets. Add a pre-run selection check that rejects public URLs with empty title, meta description, canonical, OG fields, and structured data unless explicitly marked as test-only.

SEO/GEO rationale: GEO changes avoid manipulative markup and invisible claims: Structured data only describes visible page content; no fake reviews, hidden Q&A, irrelevant entity types, or unsupported claims; recommended properties are complete where used.

GEO visibility score: P2 / severity-informed.

Validation steps: Confirm the change is present on https://www.radissonhotels.com/sv-se/marke/country-inn/banner-tests and rerun GEO audit.

## Acceptance Criteria
- Proposed change is implemented for https://www.radissonhotels.com/sv-se/marke/country-inn/banner-tests.
- Validation confirms the run_004_GAP-010 gap is closed or explicitly downgraded.
- Existing visible behavior remains unchanged unless specified in the ticket.

## Evidence Sources
- S1233: developers.google.com
  https://developers.google.com/search/docs/crawling-indexing/block-indexing
- S1234: developers.google.com
  https://developers.google.com/search/docs/appearance/title-link
- S1235: developers.google.com
  https://developers.google.com/search/docs/appearance/snippet
