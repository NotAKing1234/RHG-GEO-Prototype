# PROP-005 - Unblock Park Plaza offer pages and add a structured offer module to each selected offer URL, beginning with https://www.radissonhotels.com/e

- Run proposal ID: 5005
- Status: ready-to-send
- Priority: P2
- Surface: Metadata / Structured Data
- Component: Commerce
- Pages: https://www.radissonhotels.com/en-us/hotel-deals/park-plaza-family

## Proposed Change
Unblock Park Plaza offer pages and add a structured offer module to each selected offer URL, beginning with https://www.radissonhotels.com/en-us/hotel-deals/park-plaza-family. Include offer name, discount/value proposition, eligible hotels, book-by date, stay window, cancellation/refund terms, Radisson Rewards hook, support URL, official booking CTA, and Offer JSON-LD with validity fields such as validThrough where dates are present. Expire or redirect offers automatically after the end date.

## Current State
All 7 selected Park Plaza offer URLs were blocked. Offer and direct-booking pages cannot provide assistants with official booking routes, offer terms, cancellation/support cues, or loyalty hooks.

## Rationale
C10; Phase 2.5 GAP-005 research cites Schema.org Offer and Google hotel price structured data: https://schema.org/Offer, https://schema.org/validThrough, https://developers.google.com/hotels/hotel-prices/structured-data/hotel-price-structured-data.

## Impact
Medium to high. AI assistants can recommend official direct-booking paths only when offer terms and booking routes are explicit and crawlable.

## Jira Summary
Unblock Park Plaza offer pages and add a structured offer module to each selected offer URL, beginning with https://www.radissonhotels.com/e

## Jira Description
Dev change specs: Unblock Park Plaza offer pages and add a structured offer module to each selected offer URL, beginning with https://www.radissonhotels.com/en-us/hotel-deals/park-plaza-family. Include offer name, discount/value proposition, eligible hotels, book-by date, stay window, cancellation/refund terms, Radisson Rewards hook, support URL, official booking CTA, and Offer JSON-LD with validity fields such as validThrough where dates are present. Expire or redirect offers automatically after the end date.

SEO/GEO rationale: Official booking next steps are clear and machine-readable enough for assistant handoff: Page exposes official booking CTA, rate/availability path, policy/support cues, loyalty hooks, and no ambiguity about ownership.

GEO visibility score: P2 / severity-informed.

Validation steps: Confirm the change is present on https://www.radissonhotels.com/en-us/hotel-deals/park-plaza-family and rerun GEO audit.

## Acceptance Criteria
- Proposed change is implemented for https://www.radissonhotels.com/en-us/hotel-deals/park-plaza-family.
- Validation confirms the run_005_GAP-005 gap is closed or explicitly downgraded.
- Existing visible behavior remains unchanged unless specified in the ticket.

## Evidence Sources
- S1282: schema.org
  https://schema.org/Offer
- S1283: schema.org
  https://schema.org/validThrough
- S1284: developers.google.com
  https://developers.google.com/hotels/hotel-prices/structured-data/hotel-price-structured-data
- S1285: hilton.com
  https://www.hilton.com/en/offers/the-hilton-sale-europe-and-africa-2000001516/
