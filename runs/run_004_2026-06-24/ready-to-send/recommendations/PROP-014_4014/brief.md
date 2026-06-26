# PROP-014 - Unblock selected hotel review pages and add visible review summaries plus valid aggregateRating/Review markup where Radisson owns or can law

- Run proposal ID: 4014
- Status: ready-to-send
- Priority: P2
- Surface: Metadata / Structured Data
- Component: Commerce
- Pages: https://www.radissonhotels.com/en-us/brand/country-inn

## Proposed Change
Unblock selected hotel review pages and add visible review summaries plus valid aggregateRating/Review markup where Radisson owns or can lawfully display the review data. Include review count, rating, review source, and recency in visible copy, and keep claims consistent across official hotel pages, Google Business Profile, and OTAs.

## Current State
AI hotel assistants lean on reviews and consensus. Country Inn brand pages expose amenities but not review/rating evidence, and selected review/property pages are inaccessible.

## Rationale
C09

## Impact
Medium to high. Reviews and consensus help AI systems compare trust and quality, especially for international travelers choosing between brands and OTAs.

## Jira Summary
Unblock selected hotel review pages and add visible review summaries plus valid aggregateRating/Review markup where Radisson owns or can law

## Jira Description
Dev change specs: Unblock selected hotel review pages and add visible review summaries plus valid aggregateRating/Review markup where Radisson owns or can lawfully display the review data. Include review count, rating, review source, and recency in visible copy, and keep claims consistent across official hotel pages, Google Business Profile, and OTAs.

SEO/GEO rationale: Review/rating and third-party trust signals are exposed and current: Page or linked booking/listing ecosystem exposes recent reviews, aggregate rating, review count, trusted awards/editorial mentions, and consistent claims across Booking.com, Expedia, Tripadvisor, Google, and brand pages.

GEO visibility score: P2 / severity-informed.

Validation steps: Confirm the change is present on https://www.radissonhotels.com/en-us/brand/country-inn and rerun GEO audit.

## Acceptance Criteria
- Proposed change is implemented for https://www.radissonhotels.com/en-us/brand/country-inn.
- Validation confirms the run_004_GAP-014 gap is closed or explicitly downgraded.
- Existing visible behavior remains unchanged unless specified in the ticket.

## Evidence Sources
- S1242: schema.org
  https://schema.org/docs/hotels.html
- S1243: developers.google.com
  https://developers.google.com/search/docs/appearance/structured-data/review-snippet
