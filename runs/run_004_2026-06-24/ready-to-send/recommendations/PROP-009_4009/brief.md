# PROP-009 - Add visible FAQ blocks and matching FAQPage JSON-LD where the Q&A appears on page

- Run proposal ID: 4009
- Status: ready-to-send
- Priority: P2
- Surface: Metadata / Structured Data
- Component: Meetings & Events
- Pages: https://www.radissonhotels.com/fr-fr/marque/country-inn

## Proposed Change
Add visible FAQ blocks and matching FAQPage JSON-LD where the Q&A appears on page. Start with questions about check-in/out, breakfast, Wi-Fi, parking, accessibility, business amenities, meeting rooms, transit, local attractions, and weekend leisure add-ons. Do not add hidden or unsupported FAQ schema.

## Current State
Useful Q&A content is not consistently exposed as visible, structured, page-aligned FAQ data, and the target English/US pages are blocked. This limits direct answers to breakfast, Wi-Fi, meeting, parking, and business-travel questions.

## Rationale
C05

## Impact
Medium. It improves assistant follow-up answers, but it depends on crawlable pages and should not be prioritized above access and hotel schema.

## Jira Summary
Add visible FAQ blocks and matching FAQPage JSON-LD where the Q&A appears on page

## Jira Description
Dev change specs: Add visible FAQ blocks and matching FAQPage JSON-LD where the Q&A appears on page. Start with questions about check-in/out, breakfast, Wi-Fi, parking, accessibility, business amenities, meeting rooms, transit, local attractions, and weekend leisure add-ons. Do not add hidden or unsupported FAQ schema.

SEO/GEO rationale: Real traveler questions answered visibly, with FAQPage only when accurate: Page includes visible Q&A for real traveler decisions and, where schema is used, FAQPage/Question/Answer JSON-LD exactly matches visible questions and answers without promotional stuffing.

GEO visibility score: P2 / severity-informed.

Validation steps: Confirm the change is present on https://www.radissonhotels.com/fr-fr/marque/country-inn and rerun GEO audit.

## Acceptance Criteria
- Proposed change is implemented for https://www.radissonhotels.com/fr-fr/marque/country-inn.
- Validation confirms the run_004_GAP-009 gap is closed or explicitly downgraded.
- Existing visible behavior remains unchanged unless specified in the ticket.

## Evidence Sources
- S1231: developers.google.com
  https://developers.google.com/search/docs/appearance/structured-data/faqpage
- S1232: schema.org
  https://schema.org/FAQPage
