# PROP-005 - Add validated Hotel or LodgingBusiness JSON-LD to every Country Inn hotel overview page with name, url, brand, description, address, geo, te

- Run proposal ID: 4005
- Status: ready-to-send
- Priority: P1
- Surface: Metadata / Structured Data
- Component: Commerce
- Pages: https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn

## Proposed Change
Add validated Hotel or LodgingBusiness JSON-LD to every Country Inn hotel overview page with name, url, brand, description, address, geo, telephone, image, amenityFeature, checkInTime, checkOutTime, aggregateRating where valid, and a booking potentialAction or direct booking URL. Keep Organization schema for brand/corporate pages, but do not use it as a substitute for hotel entity markup.

## Current State
Country Inn pages are machine-readable as organization/website pages, but not as hotel/lodging entities. AI hotel assistants cannot parse hotel amenities, place details, ratings, rooms, or booking facts from schema.

## Rationale
C03

## Impact
Very high once pages are crawlable. Hotel schema gives AI systems machine-readable property, amenity, review, place, and booking facts instead of forcing inference from generic brand copy.

## Jira Summary
Add validated Hotel or LodgingBusiness JSON-LD to every Country Inn hotel overview page with name, url, brand, description, address, geo, te

## Jira Description
Dev change specs: Add validated Hotel or LodgingBusiness JSON-LD to every Country Inn hotel overview page with name, url, brand, description, address, geo, telephone, image, amenityFeature, checkInTime, checkOutTime, aggregateRating where valid, and a booking potentialAction or direct booking URL. Keep Organization schema for brand/corporate pages, but do not use it as a substitute for hotel entity markup.

SEO/GEO rationale: Valid Hotel or LodgingBusiness JSON-LD with useful hotel facts: Page contains valid JSON-LD using Hotel, LodgingBusiness, or a relevant subtype with visible-page-aligned fields: name, URL, address, geo, telephone, image, description, amenityFeature, aggregateRating/reviews where available, checkInTime/checkOutTime, starRating, and priceRange or offer data when applicable.

GEO visibility score: P1 / severity-informed.

Validation steps: Confirm the change is present on https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn and rerun GEO audit.

## Acceptance Criteria
- Proposed change is implemented for https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn.
- Validation confirms the run_004_GAP-005 gap is closed or explicitly downgraded.
- Existing visible behavior remains unchanged unless specified in the ticket.

## Evidence Sources
- S1222: schema.org
  https://schema.org/docs/hotels.html
- S1223: developers.google.com
  https://developers.google.com/search/docs/appearance/structured-data/local-business
- S1224: all.accor.com
  https://all.accor.com/hotel/0929/index.en.shtml
