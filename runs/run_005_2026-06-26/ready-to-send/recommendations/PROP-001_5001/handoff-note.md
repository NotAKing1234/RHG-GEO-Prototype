# PROP-001 Handoff Note

Subject: Restore HTTP 200 page-specific HTML for all public Park Plaza en-us brand, destination, hotel, meeting-event, and offer URLs selected in run

Status: ready-to-send

Recommended change:
Restore HTTP 200 page-specific HTML for all public Park Plaza en-us brand, destination, hotel, meeting-event, and offer URLs selected in run_005, starting with https://www.radissonhotels.com/en-us/brand/park-plaza. Add CDN/WAF allow rules for verified Googlebot, Bingbot, OAI-SearchBot, ChatGPT-User, and PerplexityBot where policy permits, and use rate limits or 429 responses for abuse instead of the access-restricted template. Validate with a 478-URL recrawl that confirms unique page titles, body fingerprints, and schema/content extraction per URL.

Why this matters:
Very high. This is the dependency for every other GEO fix; without retrievable official pages, assistants will ground answers in OTAs, maps, reviews, or competitors instead of Park Plaza-owned content.

Requested next action:
Review the attached Jira CSV row, confirm ownership/component, and import or paste the ticket into the delivery tracker.
