# PROP-007 - Publish https://www.radissonhotels.com/llms.txt as a concise official Markdown orientation file with sections for Radisson Hotel Group, Park

- Run proposal ID: 5007
- Status: ready-to-send
- Priority: P3
- Surface: Strategic / Infrastructure
- Component: Meetings & Events
- Pages: https://www.radissonhotels.com/llms.txt

## Proposed Change
Publish https://www.radissonhotels.com/llms.txt as a concise official Markdown orientation file with sections for Radisson Hotel Group, Park Plaza, hotel discovery, meetings/events, offers, booking/support, loyalty, accessibility, and sitemap references. Generate it from approved CMS/source-of-truth data, include Last-Updated, and exclude internal/test/picklist URLs.

## Current State
/llms.txt returned HTTP 404. No AI-oriented site summary file is available.

## Rationale
C16; Phase 2.5 GAP-007 research cites Chrome/Lighthouse agentic browsing documentation and the llms.txt convention: https://developer.chrome.com/docs/lighthouse/agentic-browsing/llms-txt and https://llmstxt.org/.

## Impact
Low to medium. It will not compensate for blocked pages, but it can give AI agents an official map once page access and sitemaps are fixed.

## Jira Summary
Publish https://www.radissonhotels.com/llms.txt as a concise official Markdown orientation file with sections for Radisson Hotel Group, Park

## Jira Description
Dev change specs: Publish https://www.radissonhotels.com/llms.txt as a concise official Markdown orientation file with sections for Radisson Hotel Group, Park Plaza, hotel discovery, meetings/events, offers, booking/support, loyalty, accessibility, and sitemap references. Generate it from approved CMS/source-of-truth data, include Last-Updated, and exclude internal/test/picklist URLs.

SEO/GEO rationale: Brand can participate in assistant, connector, OTA, and metasearch travel flows: Brand pages expose availability/rate/deep-link/booking facts and there is a visible strategy for assistant surfaces or feed/API participation.

GEO visibility score: P3 / severity-informed.

Validation steps: Confirm the change is present on https://www.radissonhotels.com/llms.txt and rerun GEO audit.

## Acceptance Criteria
- Proposed change is implemented for https://www.radissonhotels.com/llms.txt.
- Validation confirms the run_005_GAP-007 gap is closed or explicitly downgraded.
- Existing visible behavior remains unchanged unless specified in the ticket.

## Evidence Sources
- S1290: developer.chrome.com
  https://developer.chrome.com/docs/lighthouse/agentic-browsing/llms-txt
- S1291: llmstxt.org
  https://llmstxt.org/
- S1292: skyscanner.com
  https://www.skyscanner.com/llms.txt
- S1293: radissonhotels.com
  https://www.radissonhotels.com/llms.txt`
