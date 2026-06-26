# PROP-012 - After unblocking the English/US pages, add page-specific OG images and gallery alt text for rooms, desks, meeting rooms, breakfast, exterior

- Run proposal ID: 4012
- Status: ready-to-send
- Priority: P3
- Surface: Metadata / Structured Data
- Component: Meetings & Events
- Pages: https://www.radissonhotels.com/en-us/brand/country-inn

## Proposed Change
After unblocking the English/US pages, add page-specific OG images and gallery alt text for rooms, desks, meeting rooms, breakfast, exterior, transit, and nearby attractions. Tie image fields into Hotel JSON-LD where valid and avoid keyword-stuffed alt text.

## Current State
AI and visual search surfaces cannot reliably understand rooms, breakfast, meetings, exterior/location, or amenity visuals for the most relevant US path.

## Rationale
C15

## Impact
Low to medium. Helpful for visual search and AI confidence, but secondary to retrieval, schema, and content specificity.

## Jira Summary
After unblocking the English/US pages, add page-specific OG images and gallery alt text for rooms, desks, meeting rooms, breakfast, exterior

## Jira Description
Dev change specs: After unblocking the English/US pages, add page-specific OG images and gallery alt text for rooms, desks, meeting rooms, breakfast, exterior, transit, and nearby attractions. Tie image fields into Hotel JSON-LD where valid and avoid keyword-stuffed alt text.

SEO/GEO rationale: Meaningful hotel imagery has descriptive alt text and relevant structured image URLs: Meaningful images have descriptive alt text; structured data image fields are crawlable; hero/room/amenity images are not all unlabeled or generic.

GEO visibility score: P3 / severity-informed.

Validation steps: Confirm the change is present on https://www.radissonhotels.com/en-us/brand/country-inn and rerun GEO audit.

## Acceptance Criteria
- Proposed change is implemented for https://www.radissonhotels.com/en-us/brand/country-inn.
- Validation confirms the run_004_GAP-012 gap is closed or explicitly downgraded.
- Existing visible behavior remains unchanged unless specified in the ticket.

## Evidence Sources
- S1238: developers.google.com
  https://developers.google.com/search/docs/appearance/google-images
