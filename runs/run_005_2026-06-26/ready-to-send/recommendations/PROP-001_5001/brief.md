# PROP-001 - Restore HTTP 200 page-specific HTML for all public Park Plaza en-us brand, destination, hotel, meeting-event, and offer URLs selected in run

- Run proposal ID: 5001
- Status: ready-to-send
- Priority: P1
- Surface: Metadata / Structured Data
- Component: Meetings & Events
- Pages: https://www.radissonhotels.com/en-us/brand/park-plaza

## Proposed Change
Restore HTTP 200 page-specific HTML for all public Park Plaza en-us brand, destination, hotel, meeting-event, and offer URLs selected in run_005, starting with https://www.radissonhotels.com/en-us/brand/park-plaza. Add CDN/WAF allow rules for verified Googlebot, Bingbot, OAI-SearchBot, ChatGPT-User, and PerplexityBot where policy permits, and use rate limits or 429 responses for abuse instead of the access-restricted template. Validate with a 478-URL recrawl that confirms unique page titles, body fingerprints, and schema/content extraction per URL.

## Current State
476 of 478 selected Park Plaza URLs returned HTTP 403 or an access-restricted template, and 2 timed out. AI systems cannot extract page-specific Park Plaza hotel, meeting, offer, destination, or booking facts from the selected official URLs.

## Rationale
C01; Phase 2.5 GAP-001 research cites Google HTTP status and AI features guidance, OpenAI bot documentation, and Perplexity crawler documentation: https://developers.google.com/crawling/docs/troubleshooting/http-status-codes, https://developers.google.com/search/docs/appearance/ai-features, https://developers.openai.com/api/docs/bots, https://docs.perplexity.ai/docs/resources/perplexity-crawlers.

## Impact
Very high. This is the dependency for every other GEO fix; without retrievable official pages, assistants will ground answers in OTAs, maps, reviews, or competitors instead of Park Plaza-owned content.

## Jira Summary
Restore HTTP 200 page-specific HTML for all public Park Plaza en-us brand, destination, hotel, meeting-event, and offer URLs selected in run

## Jira Description
Dev change specs: Restore HTTP 200 page-specific HTML for all public Park Plaza en-us brand, destination, hotel, meeting-event, and offer URLs selected in run_005, starting with https://www.radissonhotels.com/en-us/brand/park-plaza. Add CDN/WAF allow rules for verified Googlebot, Bingbot, OAI-SearchBot, ChatGPT-User, and PerplexityBot where policy permits, and use rate limits or 429 responses for abuse instead of the access-restricted template. Validate with a 478-URL recrawl that confirms unique page titles, body fingerprints, and schema/content extraction per URL.

SEO/GEO rationale: Public AI/search crawler access for every selected page: The audited URL returns HTTP 200 useful HTML or an indexable redirect; failures such as 403, AccessDenied, timeout, empty HTML, or blocked templates are recorded precisely.

GEO visibility score: P1 / severity-informed.

Validation steps: Confirm the change is present on https://www.radissonhotels.com/en-us/brand/park-plaza and rerun GEO audit.

## Acceptance Criteria
- Proposed change is implemented for https://www.radissonhotels.com/en-us/brand/park-plaza.
- Validation confirms the run_005_GAP-001 gap is closed or explicitly downgraded.
- Existing visible behavior remains unchanged unless specified in the ticket.

## Evidence Sources
- S1265: developers.google.com
  https://developers.google.com/crawling/docs/troubleshooting/http-status-codes
- S1266: developers.google.com
  https://developers.google.com/search/docs/appearance/ai-features
- S1267: developers.openai.com
  https://developers.openai.com/api/docs/bots
- S1268: docs.perplexity.ai
  https://docs.perplexity.ai/docs/resources/perplexity-crawlers
- S1269: hilton.com
  https://www.hilton.com/en/hotels/orygigi-hilton-garden-inn-paris-la-villette/
