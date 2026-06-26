# PROP-008 - Add city, neighborhood, airport/train distance, business district, landmark, parking/shuttle, and public-transit fields to each Country Inn

- Run proposal ID: 4008
- Status: ready-to-send
- Priority: P2
- Surface: Metadata
- Component: Commerce
- Pages: https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn

## Proposed Change
Add city, neighborhood, airport/train distance, business district, landmark, parking/shuttle, and public-transit fields to each Country Inn hotel page and selected brand/destination modules. Where a page is brand-level, link to city/property pages with named examples instead of leaving metadata generic.

## Current State
The accessible metadata helps with brand and amenity discovery, but not city, district, airport, station, or nearby-business queries that AI travel assistants generate.

## Rationale
C08

## Impact
Medium to high. AI systems need location facts to answer "near airport," "near client office," and "near sightseeing" prompts.

## Jira Summary
Add city, neighborhood, airport/train distance, business district, landmark, parking/shuttle, and public-transit fields to each Country Inn

## Jira Description
Dev change specs: Add city, neighborhood, airport/train distance, business district, landmark, parking/shuttle, and public-transit fields to each Country Inn hotel page and selected brand/destination modules. Where a page is brand-level, link to city/property pages with named examples instead of leaving metadata generic.

SEO/GEO rationale: Page names actionable places, districts, transit, airports, and attractions: Page names city, country, neighborhood or district, nearby train/airport/metro access, and at least two business or leisure landmarks where relevant.

GEO visibility score: P2 / severity-informed.

Validation steps: Confirm the change is present on https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn and rerun GEO audit.

## Acceptance Criteria
- Proposed change is implemented for https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn.
- Validation confirms the run_004_GAP-008 gap is closed or explicitly downgraded.
- Existing visible behavior remains unchanged unless specified in the ticket.

## Evidence Sources
- S1229: support.google.com
  https://support.google.com/hotelprices/answer/9218458
- S1230: developers.google.com
  https://developers.google.com/my-business/reference/lodging/rest/v1/Lodging
