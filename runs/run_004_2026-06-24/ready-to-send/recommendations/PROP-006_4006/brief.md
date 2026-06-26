# PROP-006 - Return HTTP 200 for the 9 selected Country Inn hotel overview pages and 6 selected Bathinda hotel subpages

- Run proposal ID: 4006
- Status: ready-to-send
- Priority: P1
- Surface: Metadata / Structured Data
- Component: Meetings & Events
- Pages: https://www.radissonhotels.com/en-us/hotels/country-inn-bathinda

## Proposed Change
Return HTTP 200 for the 9 selected Country Inn hotel overview pages and 6 selected Bathinda hotel subpages. For each property, expose canonical URL, reciprocal hreflang, address, geo, telephone, room/amenity data, meeting/dining/local-attraction sections, review route, and direct booking deep links. Use the same fields in visible copy and Hotel JSON-LD.

## Current State
Individual hotel pages cannot be evaluated or retrieved by AI systems from this environment. Property-level address, geo, review, meeting, dining, and local details are blocked.

## Rationale
C04

## Impact
Very high. Property pages are the point where AI assistants can move from brand discovery to concrete hotel recommendation and booking.

## Jira Summary
Return HTTP 200 for the 9 selected Country Inn hotel overview pages and 6 selected Bathinda hotel subpages

## Jira Description
Dev change specs: Return HTTP 200 for the 9 selected Country Inn hotel overview pages and 6 selected Bathinda hotel subpages. For each property, expose canonical URL, reciprocal hreflang, address, geo, telephone, room/amenity data, meeting/dining/local-attraction sections, review route, and direct booking deep links. Use the same fields in visible copy and Hotel JSON-LD.

SEO/GEO rationale: Machine-readable local/place details for individual hotel pages: Individual hotel pages expose address, locality, country, geo coordinates, telephone, opening/check-in details, reviews, business category, and reservation/booking route; details are consistent with Google Business Profile and major OTAs.

GEO visibility score: P1 / severity-informed.

Validation steps: Confirm the change is present on https://www.radissonhotels.com/en-us/hotels/country-inn-bathinda and rerun GEO audit.

## Acceptance Criteria
- Proposed change is implemented for https://www.radissonhotels.com/en-us/hotels/country-inn-bathinda.
- Validation confirms the run_004_GAP-006 gap is closed or explicitly downgraded.
- Existing visible behavior remains unchanged unless specified in the ticket.

## Evidence Sources
- S1225: support.google.com
  https://support.google.com/hotelprices/answer/9218458
- S1226: wyndhamhotels.com
  https://www.wyndhamhotels.com/ramada/london-united-kingdom/ramada-london-north-m1/overview
