# Optimization Proposal - run_005 | 2026-06-26

## Executive Summary

This run identified **8 total gaps** across 478 DB-selected Park Plaza URLs: **1 newly explicit gap** and **7 recurring or persistent themes**. The dominant finding is not subtle metadata drift; it is page-level retrieval failure. 476 selected URLs returned the Radisson access-restricted template and 2 timed out, so AI systems cannot inspect the official Park Plaza hotel, meeting, offer, destination, or brand content. The **top 3 priority changes** are: (1) restore HTTP 200 page-specific HTML for public Park Plaza `en-us` pages and verified search/AI crawlers; (2) make `/sitemap.xml` public and use it to accelerate recrawl after the access fix; and (3) add server-rendered Hotel/LodgingBusiness and MeetingRoom structured data once the property and meeting pages are reachable.

## Proposal Entries

### PROP-001 - GAP-001 - run_005_GAP-001

**1. Proposed change**
Restore HTTP 200 page-specific HTML for all public Park Plaza `en-us` brand, destination, hotel, meeting-event, and offer URLs selected in run_005, starting with https://www.radissonhotels.com/en-us/brand/park-plaza. Add CDN/WAF allow rules for verified Googlebot, Bingbot, OAI-SearchBot, ChatGPT-User, and PerplexityBot where policy permits, and use rate limits or 429 responses for abuse instead of the access-restricted template. Validate with a 478-URL recrawl that confirms unique page titles, body fingerprints, and schema/content extraction per URL.

**2. Source citation**
C01; Phase 2.5 GAP-001 research cites Google HTTP status and AI features guidance, OpenAI bot documentation, and Perplexity crawler documentation: https://developers.google.com/crawling/docs/troubleshooting/http-status-codes, https://developers.google.com/search/docs/appearance/ai-features, https://developers.openai.com/api/docs/bots, https://docs.perplexity.ai/docs/resources/perplexity-crawlers.

**3. Current state**
476 of 478 selected Park Plaza URLs returned HTTP 403 or an access-restricted template, and 2 timed out. AI systems cannot extract page-specific Park Plaza hotel, meeting, offer, destination, or booking facts from the selected official URLs.

**4. Inferred implementation status**
Not implemented for the Park Plaza target set. Run_004 showed only partial root `robots.txt` recovery; the current run shows page-level access remains blocked for a different brand family.

**5. Directional impact estimate**
Very high. This is the dependency for every other GEO fix; without retrievable official pages, assistants will ground answers in OTAs, maps, reviews, or competitors instead of Park Plaza-owned content.

**6. Priority tier**
P1

---

### PROP-002 - GAP-002 - run_005_GAP-002

**1. Proposed change**
After access is restored, run a locale QA pass for every selected `en-us` Park Plaza URL. Require each page to return US-English content, a self-referencing canonical, reciprocal hreflang alternates for equivalent language/region pages, and no canonical or hreflang reference to the access-restricted template. Start validation from https://www.radissonhotels.com/en-us/brand/park-plaza and extend it to all 478 selected URLs.

**2. Source citation**
C02; Phase 2.5 GAP-002 research cites Google localized versions and canonical guidance: https://developers.google.com/search/docs/specialty/international/localized-versions and https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls.

**3. Current state**
All selected URLs are `en-us`, but the English/US Park Plaza path is not yielding retrievable page content from this environment. Locale, canonical, and hreflang quality cannot be validated because the access template replaces the underlying page.

**4. Inferred implementation status**
Not implemented. The current Park Plaza `en-us` selection repeats the run_004 pattern where the audience-critical English/US path is the least useful path for AI retrieval.

**5. Directional impact estimate**
Very high. American travelers asking AI tools for official Park Plaza hotels in Europe need assistants to select the US-English official page, not a blocked template or uncertain regional fallback.

**6. Priority tier**
P1

---

### PROP-003 - GAP-003 - run_005_GAP-003

**1. Proposed change**
Generate server-rendered Hotel or LodgingBusiness JSON-LD for each Park Plaza property URL, beginning with https://www.radissonhotels.com/en-us/hotels/park-plaza-amsterdam-airport/meeting-events and the related hotel overview pages. Use CMS fields for `Hotel`, `PostalAddress`, `GeoCoordinates`, `amenityFeature`, check-in/check-out, phone, official URL, image, star rating where official, aggregate rating only where visibly supported, and direct booking or offer URL where current. Add schema validation and visible-content parity checks to the run smoke process after access is fixed.

**2. Source citation**
C03; Phase 2.5 GAP-003 research cites Schema.org Hotel/hotel vocabulary, Google local business structured data, and Google hotel price structured data: https://schema.org/Hotel, https://schema.org/docs/hotels.html, https://developers.google.com/search/docs/appearance/structured-data/local-business, https://developers.google.com/hotels/hotel-prices/structured-data/hotel-price-structured-data.

**3. Current state**
457 selected hotel/property URLs were in scope, but 455 were blocked and 2 timed out. Property-level Hotel/LodgingBusiness schema, address, geo, amenity, rating, and booking facts are unavailable to AI systems for the selected Park Plaza hotel URLs.

**4. Inferred implementation status**
Not implemented or not verifiable because property pages are blocked. The hotel-schema depth issue is recurring from run_001 through run_005.

**5. Directional impact estimate**
High after page access is restored. Complete hotel facts let AI assistants answer property-comparison queries such as Park Plaza hotels with meeting rooms, Wi-Fi, transit access, and weekend attractions from official data.

**6. Priority tier**
P1

---

### PROP-004 - GAP-004 - run_005_GAP-004

**1. Proposed change**
Publish crawlable Park Plaza meeting-event pages with property-specific capacity matrices, room names, floor area, layouts, AV/Wi-Fi/catering availability, accessibility, RFP/contact path, group-room booking path, and nearby leisure context. Add MeetingRoom/Place JSON-LD, including `maximumAttendeeCapacity`, `floorSize`, and `amenityFeature`, on pages such as https://www.radissonhotels.com/en-us/brand/park-plaza/meeting-conference and the 76 selected property meeting URLs.

**2. Source citation**
C04; Phase 2.5 GAP-004 research cites Schema.org MeetingRoom and Event structured data guidance: https://schema.org/MeetingRoom, https://schema.org/maximumAttendeeCapacity, https://developers.google.com/search/docs/appearance/structured-data/event.

**3. Current state**
All 78 selected meeting-related URLs were blocked. Meeting-room capacity, RFP/contact paths, event services, Wi-Fi/AV/catering, and work-travel suitability are not retrievable from the selected Park Plaza meeting-event pages.

**4. Inferred implementation status**
Newly explicit for this Park Plaza run. Related work-travel/bleisure gaps existed in earlier runs, but run_005 is the first large meeting-event slice.

**5. Directional impact estimate**
High. American planners asking assistants for European hotels that can host meetings and weekend stays need official capacity and RFP facts to shortlist Park Plaza.

**6. Priority tier**
P1

---

### PROP-005 - GAP-005 - run_005_GAP-005

**1. Proposed change**
Unblock Park Plaza offer pages and add a structured offer module to each selected offer URL, beginning with https://www.radissonhotels.com/en-us/hotel-deals/park-plaza-family. Include offer name, discount/value proposition, eligible hotels, book-by date, stay window, cancellation/refund terms, Radisson Rewards hook, support URL, official booking CTA, and Offer JSON-LD with validity fields such as `validThrough` where dates are present. Expire or redirect offers automatically after the end date.

**2. Source citation**
C10; Phase 2.5 GAP-005 research cites Schema.org Offer and Google hotel price structured data: https://schema.org/Offer, https://schema.org/validThrough, https://developers.google.com/hotels/hotel-prices/structured-data/hotel-price-structured-data.

**3. Current state**
All 7 selected Park Plaza offer URLs were blocked. Offer and direct-booking pages cannot provide assistants with official booking routes, offer terms, cancellation/support cues, or loyalty hooks.

**4. Inferred implementation status**
Not implemented for the current Park Plaza offer slice. Direct booking clarity remains a recurring conversion and trust theme from prior runs.

**5. Directional impact estimate**
Medium to high. AI assistants can recommend official direct-booking paths only when offer terms and booking routes are explicit and crawlable.

**6. Priority tier**
P2

---

### PROP-006 - GAP-006 - run_005_GAP-006

**1. Proposed change**
Serve https://www.radissonhotels.com/sitemap.xml as public HTTP 200 XML or a sitemap index before WAF/challenge rules. Segment Park Plaza sitemap coverage by brand, hotel/property, meetings, offers, and locale alternates; include only canonical 200 URLs with accurate `lastmod`; reference the sitemap in `/robots.txt`; and submit the sitemap index in Google Search Console and Bing Webmaster Tools.

**2. Source citation**
C01; Phase 2.5 GAP-006 research cites Google sitemap guidance and the Sitemaps protocol: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap and https://www.sitemaps.org/protocol.html.

**3. Current state**
The standard `/sitemap.xml` endpoint returned HTTP 403 while `/robots.txt` returned HTTP 200. This weakens discovery even after the page-level access fix.

**4. Inferred implementation status**
Not implemented. This is a recurring technical discovery gap from prior runs.

**5. Directional impact estimate**
High and fast to measure. A public sitemap accelerates recrawl and gives search/AI systems a canonical URL map for long-tail Park Plaza property and meeting pages.

**6. Priority tier**
P1

---

### PROP-007 - GAP-007 - run_005_GAP-007

**1. Proposed change**
Publish https://www.radissonhotels.com/llms.txt as a concise official Markdown orientation file with sections for Radisson Hotel Group, Park Plaza, hotel discovery, meetings/events, offers, booking/support, loyalty, accessibility, and sitemap references. Generate it from approved CMS/source-of-truth data, include `Last-Updated`, and exclude internal/test/picklist URLs.

**2. Source citation**
C16; Phase 2.5 GAP-007 research cites Chrome/Lighthouse agentic browsing documentation and the llms.txt convention: https://developer.chrome.com/docs/lighthouse/agentic-browsing/llms-txt and https://llmstxt.org/.

**3. Current state**
`/llms.txt` returned HTTP 404. No AI-oriented site summary file is available.

**4. Inferred implementation status**
Not implemented. This remains a recurring, lower-priority AI-discovery gap from run_002 through run_005.

**5. Directional impact estimate**
Low to medium. It will not compensate for blocked pages, but it can give AI agents an official map once page access and sitemaps are fixed.

**6. Priority tier**
P3

---

### PROP-008 - GAP-008 - run_005_GAP-008

**1. Proposed change**
Remove utility, picklist, sitemap-like, and test-adjacent URL patterns from `run_url_targets` selection and from any generated public sitemaps, starting with https://www.radissonhotels.com/en-us/brand/park-plaza/meeting-conference/picklist. If utility endpoints must remain public, return crawlable `noindex` headers or disallow them in robots rules. Replace them in GEO selections with canonical production landing pages for Park Plaza properties, city/destination pages, meeting pages, and offers.

**2. Source citation**
C15; Phase 2.5 GAP-008 research cites Google guidance on faceted navigation, blocking indexing, and URL structure: https://developers.google.com/crawling/docs/faceted-navigation, https://developers.google.com/search/docs/crawling-indexing/block-indexing, https://developers.google.com/search/docs/crawling-indexing/url-structure.

**3. Current state**
The run target set includes utility/test/picklist/sitemap-like URL patterns, especially `/meeting-conference/picklist`. These may not be production landing pages for AI travel discovery.

**4. Inferred implementation status**
Not implemented. Selection hygiene has been a recurring watch-out since run_004 banner-test findings.

**5. Directional impact estimate**
Medium. Cleaner target sets reduce crawl waste and AI confusion so assistants find useful Park Plaza meeting, property, city, and offer pages rather than internal utility pages.

**6. Priority tier**
P2
