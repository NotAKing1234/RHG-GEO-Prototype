# PROP-003 - Generate server-rendered Hotel or LodgingBusiness JSON-LD for each Park Plaza property URL, beginning with https://www.radissonhotels.com/en

- Run proposal ID: 5003
- Status: ready-to-send
- Priority: P1
- Surface: Metadata / Structured Data
- Component: Meetings & Events
- Pages: https://www.radissonhotels.com/en-us/hotels/park-plaza-amsterdam-airport/meeting-events

## Proposed Change
Generate server-rendered Hotel or LodgingBusiness JSON-LD for each Park Plaza property URL, beginning with https://www.radissonhotels.com/en-us/hotels/park-plaza-amsterdam-airport/meeting-events and the related hotel overview pages. Use CMS fields for Hotel, PostalAddress, GeoCoordinates, amenityFeature, check-in/check-out, phone, official URL, image, star rating where official, aggregate rating only where visibly supported, and direct booking or offer URL where current. Add schema validation and visible-content parity checks to the run smoke process after access is fixed.

## Current State
457 selected hotel/property URLs were in scope, but 455 were blocked and 2 timed out. Property-level Hotel/LodgingBusiness schema, address, geo, amenity, rating, and booking facts are unavailable to AI systems for the selected Park Plaza hotel URLs.

## Rationale
C03; Phase 2.5 GAP-003 research cites Schema.org Hotel/hotel vocabulary, Google local business structured data, and Google hotel price structured data: https://schema.org/Hotel, https://schema.org/docs/hotels.html, https://developers.google.com/search/docs/appearance/structured-data/local-business, https://developers.google.com/hotels/hotel-prices/structured-data/hotel-price-structured-data.

## Impact
High after page access is restored. Complete hotel facts let AI assistants answer property-comparison queries such as Park Plaza hotels with meeting rooms, Wi-Fi, transit access, and weekend attractions from official data.

## Jira Summary
Generate server-rendered Hotel or LodgingBusiness JSON-LD for each Park Plaza property URL, beginning with https://www.radissonhotels.com/en

## Jira Description
Dev change specs: Generate server-rendered Hotel or LodgingBusiness JSON-LD for each Park Plaza property URL, beginning with https://www.radissonhotels.com/en-us/hotels/park-plaza-amsterdam-airport/meeting-events and the related hotel overview pages. Use CMS fields for Hotel, PostalAddress, GeoCoordinates, amenityFeature, check-in/check-out, phone, official URL, image, star rating where official, aggregate rating only where visibly supported, and direct booking or offer URL where current. Add schema validation and visible-content parity checks to the run smoke process after access is fixed.

SEO/GEO rationale: Valid hotel-specific JSON-LD exists on property pages: Hotel, LodgingBusiness, or relevant subtype JSON-LD includes name, URL, address, geo, telephone, image, description, amenityFeature, rating/review where valid, and booking/offer route where applicable.

GEO visibility score: P1 / severity-informed.

Validation steps: Confirm the change is present on https://www.radissonhotels.com/en-us/hotels/park-plaza-amsterdam-airport/meeting-events and rerun GEO audit.

## Acceptance Criteria
- Proposed change is implemented for https://www.radissonhotels.com/en-us/hotels/park-plaza-amsterdam-airport/meeting-events.
- Validation confirms the run_005_GAP-003 gap is closed or explicitly downgraded.
- Existing visible behavior remains unchanged unless specified in the ticket.

## Evidence Sources
- S1273: schema.org
  https://schema.org/Hotel
- S1274: schema.org
  https://schema.org/docs/hotels.html
- S1275: developers.google.com
  https://developers.google.com/search/docs/appearance/structured-data/local-business
- S1276: developers.google.com
  https://developers.google.com/hotels/hotel-prices/structured-data/hotel-price-structured-data
- S1277: marriott.com
  https://www.marriott.com/en-us/hotels/parar-ac-hotel-paris-porte-maillot/overview/
