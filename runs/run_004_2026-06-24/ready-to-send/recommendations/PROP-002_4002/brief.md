# PROP-002 - Restore crawlable /en-us/ Country Inn brand, about, business-travel, breakfast, renovated-hotels, featured-hotels, sitemap, hotel overview,

- Run proposal ID: 4002
- Status: ready-to-send
- Priority: P1
- Surface: Strategic / Infrastructure
- Component: Meetings & Events
- Pages: https://www.radissonhotels.com/en-us/brand/country-inn

## Proposed Change
Restore crawlable /en-us/ Country Inn brand, about, business-travel, breakfast, renovated-hotels, featured-hotels, sitemap, hotel overview, and hotel subpages. Add reciprocal hreflang links and x-default from accessible localized pages to the English/US equivalents, and confirm that the English/US pages return their own title/meta/canonical instead of the access-restricted template.

## Current State
The locale most relevant to American travelers is blocked, while several localized non-US pages are accessible. This prevents US-origin AI prompts from landing on the intended English/US content path.

## Rationale
C13

## Impact
Very high. The target audience is American travelers; blocking the US-English path prevents AI systems from routing US-origin prompts to the most relevant official Radisson content.

## Jira Summary
Restore crawlable /en-us/ Country Inn brand, about, business-travel, breakfast, renovated-hotels, featured-hotels, sitemap, hotel overview,

## Jira Description
Dev change specs: Restore crawlable /en-us/ Country Inn brand, about, business-travel, breakfast, renovated-hotels, featured-hotels, sitemap, hotel overview, and hotel subpages. Add reciprocal hreflang links and x-default from accessible localized pages to the English/US equivalents, and confirm that the English/US pages return their own title/meta/canonical instead of the access-restricted template.

SEO/GEO rationale: Multilingual pages identify the correct locale and canonical relationship: Page declares appropriate lang, locale-aware title/meta, canonical URL, and hreflang alternates; localized pages are not thin duplicates with mismatched country/region signals.

GEO visibility score: P1 / severity-informed.

Validation steps: Confirm the change is present on https://www.radissonhotels.com/en-us/brand/country-inn and rerun GEO audit.

## Acceptance Criteria
- Proposed change is implemented for https://www.radissonhotels.com/en-us/brand/country-inn.
- Validation confirms the run_004_GAP-002 gap is closed or explicitly downgraded.
- Existing visible behavior remains unchanged unless specified in the ticket.

## Evidence Sources
- S1212: developers.google.com
  https://developers.google.com/search/docs/specialty/international/localized-versions
- S1213: wyndhamhotels.com
  https://www.wyndhamhotels.com/ramada/london-united-kingdom/ramada-london-north-m1/overview
