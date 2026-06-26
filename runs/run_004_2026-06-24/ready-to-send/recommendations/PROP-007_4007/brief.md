# PROP-007 - Add a reusable Country Inn work-leisure module to brand and hotel pages: desk/workspace, Wi-Fi, breakfast, meeting room, parking, late check

- Run proposal ID: 4007
- Status: ready-to-send
- Priority: P2
- Surface: Strategic / Infrastructure
- Component: Meetings & Events
- Pages: https://www.radissonhotels.com/fr-fr/marque/country-inn/offres-voyage-d-affaires

## Proposed Change
Add a reusable Country Inn work-leisure module to brand and hotel pages: desk/workspace, Wi-Fi, breakfast, meeting room, parking, late checkout where offered, transit access, and nearby leisure. Map the same fields into amenityFeature on hotel pages. Prioritize making the English/US business-travel page and selected hotel meeting-events page crawlable first.

## Current State
Business-travel suitability is inconsistently reachable and not expressed as structured amenity data. The accessible French page helps, but the English/US path and selected hotel meeting-events page are blocked.

## Rationale
C07

## Impact
Medium to high. This directly improves matching for compound prompts such as "European hotel for work meetings with breakfast and weekend sightseeing."

## Jira Summary
Add a reusable Country Inn work-leisure module to brand and hotel pages: desk/workspace, Wi-Fi, breakfast, meeting room, parking, late check

## Jira Description
Dev change specs: Add a reusable Country Inn work-leisure module to brand and hotel pages: desk/workspace, Wi-Fi, breakfast, meeting room, parking, late checkout where offered, transit access, and nearby leisure. Map the same fields into amenityFeature on hotel pages. Prioritize making the English/US business-travel page and selected hotel meeting-events page crawlable first.

SEO/GEO rationale: Meeting, workspace, breakfast, parking, Wi-Fi, wellness, and leisure amenities are scannable: Amenities appear in schema amenityFeature, tables, bullets, or clear sections; business amenities and leisure amenities are both present when relevant; meeting-room capacity and breakfast/parking/Wi-Fi are explicit if offered.

GEO visibility score: P2 / severity-informed.

Validation steps: Confirm the change is present on https://www.radissonhotels.com/fr-fr/marque/country-inn/offres-voyage-d-affaires and rerun GEO audit.

## Acceptance Criteria
- Proposed change is implemented for https://www.radissonhotels.com/fr-fr/marque/country-inn/offres-voyage-d-affaires.
- Validation confirms the run_004_GAP-007 gap is closed or explicitly downgraded.
- Existing visible behavior remains unchanged unless specified in the ticket.

## Evidence Sources
- S1227: support.google.com
  https://support.google.com/business/answer/9177958
- S1228: schema.org
  https://schema.org/amenityFeature
