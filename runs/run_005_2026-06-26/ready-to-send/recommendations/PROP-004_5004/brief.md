# PROP-004 - Publish crawlable Park Plaza meeting-event pages with property-specific capacity matrices, room names, floor area, layouts, AV/Wi-Fi/caterin

- Run proposal ID: 5004
- Status: ready-to-send
- Priority: P1
- Surface: Metadata / Structured Data
- Component: Meetings & Events
- Pages: https://www.radissonhotels.com/en-us/brand/park-plaza/meeting-conference

## Proposed Change
Publish crawlable Park Plaza meeting-event pages with property-specific capacity matrices, room names, floor area, layouts, AV/Wi-Fi/catering availability, accessibility, RFP/contact path, group-room booking path, and nearby leisure context. Add MeetingRoom/Place JSON-LD, including maximumAttendeeCapacity, floorSize, and amenityFeature, on pages such as https://www.radissonhotels.com/en-us/brand/park-plaza/meeting-conference and the 76 selected property meeting URLs.

## Current State
All 78 selected meeting-related URLs were blocked. Meeting-room capacity, RFP/contact paths, event services, Wi-Fi/AV/catering, and work-travel suitability are not retrievable from the selected Park Plaza meeting-event pages.

## Rationale
C04; Phase 2.5 GAP-004 research cites Schema.org MeetingRoom and Event structured data guidance: https://schema.org/MeetingRoom, https://schema.org/maximumAttendeeCapacity, https://developers.google.com/search/docs/appearance/structured-data/event.

## Impact
High. American planners asking assistants for European hotels that can host meetings and weekend stays need official capacity and RFP facts to shortlist Park Plaza.

## Jira Summary
Publish crawlable Park Plaza meeting-event pages with property-specific capacity matrices, room names, floor area, layouts, AV/Wi-Fi/caterin

## Jira Description
Dev change specs: Publish crawlable Park Plaza meeting-event pages with property-specific capacity matrices, room names, floor area, layouts, AV/Wi-Fi/catering availability, accessibility, RFP/contact path, group-room booking path, and nearby leisure context. Add MeetingRoom/Place JSON-LD, including maximumAttendeeCapacity, floorSize, and amenityFeature, on pages such as https://www.radissonhotels.com/en-us/brand/park-plaza/meeting-conference and the 76 selected property meeting URLs.

SEO/GEO rationale: Meeting-event pages expose capacity, room, service, and booking facts: Meeting pages include meeting-room names/capacities, event services, Wi-Fi/AV/catering, contact or RFP path, address/proximity, and schema or clearly structured tables where possible.

GEO visibility score: P1 / severity-informed.

Validation steps: Confirm the change is present on https://www.radissonhotels.com/en-us/brand/park-plaza/meeting-conference and rerun GEO audit.

## Acceptance Criteria
- Proposed change is implemented for https://www.radissonhotels.com/en-us/brand/park-plaza/meeting-conference.
- Validation confirms the run_005_GAP-004 gap is closed or explicitly downgraded.
- Existing visible behavior remains unchanged unless specified in the ticket.

## Evidence Sources
- S1278: schema.org
  https://schema.org/MeetingRoom
- S1279: schema.org
  https://schema.org/maximumAttendeeCapacity
- S1280: developers.google.com
  https://developers.google.com/search/docs/appearance/structured-data/event
- S1281: hilton.com
  https://www.hilton.com/en/hotels/brugrhi-hilton-brussels-grand-place/events/
