# GEO Criteria Framework — run_003 | 2026-04-15

Synthesized from: /literature/run_003_sources.md
Previous criteria: /framework/run_002_criteria.md (inherited and updated)

---

## C01 — Google Business Profile Completeness
**Signal name:** GBP completeness for key European properties
**Why it matters:** GBP accounts for 32% of Local Pack rankings and directly feeds Google AI Overviews (triggering on 40%+ of local queries). Google Places powers ~94% of ChatGPT hotel data. Incomplete GBP = incomplete AI data.
**Passing:** GBP listing for each audited property has: business description with amenity keywords, 20+ photos, review count (ideally 100+), Q&A section populated, service attributes (Wi-Fi, parking, meeting rooms), correct category (Hotel), and address NAP consistent with website.
**How to check:** Search "[Property Name] [City]" in Google; inspect the Knowledge Panel. Spot-check 2–3 flagship European Radisson properties.
**Bleisure relevance:** American bleisure travelers frequently trigger Google Local Pack queries; GBP is the primary data source for AI-generated hotel summaries. HIGH.

---

## C02 — Hotel/LodgingBusiness Schema Presence
**Signal name:** JSON-LD Hotel or LodgingBusiness schema on all hotel pages
**Why it matters:** 10.6% of hotels have good schema; those that do receive 2.5x higher AI citation probability. Radisson confirmed schema-absent on all brand and overview pages through run_002.
**Passing:** Each page (brand, overview, individual property) has valid JSON-LD with type Hotel or LodgingBusiness, including: name, address, geo, telephone, starRating, priceRange, amenityFeature (≥5 items), aggregateRating, checkInTime, checkOutTime, url.
**How to check:** Google Rich Results Test; view-source JSON-LD search; SERP rich result observation.
**Bleisure relevance:** Amenity fields (meeting rooms, Wi-Fi, gym, workspace) are directly parseable by AI when in amenityFeature. HIGH.

---

## C03 — FAQPage Schema for AI Q&A Parsing
**Signal name:** FAQPage JSON-LD on brand and destination pages
**Why it matters:** Google does not show FAQ rich results for hotel brands (2023 policy), but FAQPage schema remains a strong AI engine Q&A extraction signal. AI engines use FAQ blocks to generate direct answers to traveler questions.
**Passing:** FAQ section with ≥5 Q&A pairs present in page copy; FAQPage JSON-LD present in page source; questions mirror real traveler queries ("Does Radisson Blu have meeting rooms?", "Is Radisson Blu good for business travelers in London?").
**How to check:** View page source for FAQPage JSON-LD; check for visible FAQ sections; attempt WebFetch for body content.
**Bleisure relevance:** FAQs that address business amenities, location-to-business-district proximity, and leisure activities directly serve bleisure discovery queries. HIGH.

---

## C04 — AI Crawler Access (robots.txt + Cloudflare)
**Signal name:** GPTBot, PerplexityBot, ClaudeBot, Google-Extended, Applebot-Extended access permitted
**Why it matters:** Sites blocking GPTBot cited 73% less in ChatGPT. Radisson's WAF returns HTTP 403 for all fetch attempts, including /robots.txt itself — confirmed Cloudflare WAF "Block AI Scrapers and Crawlers" managed rule (or equivalent) is active.
**Passing:** /robots.txt accessible (HTTP 200); key AI crawlers either explicitly Allowed or not Disallowed; Cloudflare WAF rule updated to permit AI search crawlers. /llms.txt present (bonus criterion).
**How to check:** Attempt WebFetch of /robots.txt and /sitemap.xml. HTTP 403 = fail. HTTP 200 + review of Disallow rules = assess per crawler.
**Bleisure relevance:** Prerequisite for all other GEO signals to function. No AI citation possible from direct Radisson domain if crawlers are blocked. CRITICAL.

---

## C05 — Title Tag Query Compatibility
**Signal name:** Title tags answer real traveler queries rather than taglines or brand slogans
**Why it matters:** Title tags are the primary signal AI engines use for page categorization. Tagline-dominated titles ("Yes I Can!") are not parseable for hotel-type, location, or use-case queries.
**Passing:** Title contains: brand name + hotel type keyword + location (or use case). Example: "Radisson Blu Hotels | Business & Luxury Hotels in Europe | Radisson Hotel Group"
**How to check:** Extract from SERP snippet or WebFetch page title.
**Bleisure relevance:** Title must contain bleisure-compatible keywords (business, luxury, meetings, leisure) to surface for bleisure queries. MEDIUM-HIGH.

---

## C06 — Meta Description Informational Register
**Signal name:** Meta description in informational/factual register (not marketing copy)
**Why it matters:** Marketing register meta descriptions ("Yes I Can!" ethos) are not extracted by AI engines for factual query responses. Factual content is cited 62% more.
**Passing:** Meta description contains ≥2 specific facts (property count, room count, location cities, amenity types) and references American/international traveler value proposition.
**How to check:** Extract from SERP snippet.
**Bleisure relevance:** Meta descriptions referencing meeting facilities, business services, and leisure experiences directly serve bleisure intent. HIGH.

---

## C07 — Brand Page Factual Content Density
**Signal name:** First 80 words of brand page body copy contain ≥3 specific facts
**Why it matters:** AI engines extract the first third of content most reliably (ALM Corp "44% first-third rule"). Marketing prose in the first 80 words means the page is uncitable.
**Passing:** Opening paragraph contains: at minimum hotel count, at least 2 city/country names, at least 1 specific amenity type (meeting rooms, spa, restaurant). Register is informational.
**How to check:** WebFetch page and extract first 100 words; apply register scoring.
**Bleisure relevance:** Facts about business facilities and leisure amenities in the lede paragraph make the page directly citeable for bleisure queries. HIGH.

---

## C08 — Bleisure Traveler Explicit Signals
**Signal name:** Explicit "business and leisure" or equivalent bleisure terminology in page copy and/or meta
**Why it matters:** AI engines matching "hotels for business and leisure travelers in London" queries need explicit signal in page text. Park Plaza is the only Radisson brand page confirmed to have this (body copy only, not title/meta).
**Passing:** At least one occurrence of "business and leisure," "bleisure," or equivalent phrasing in: title tag, meta description, or first 100 words of body copy, AND meeting/conference amenities named on the same page.
**How to check:** WebFetch page; search for bleisure terminology; check meeting room mentions.
**Bleisure relevance:** Direct signal for the primary target query type. CRITICAL.

---

## C09 — American Traveler Orientation Signals
**Signal name:** Content explicitly addresses American travelers, US-to-Europe travel, or US dollar pricing context
**Why it matters:** AI engines personalizing responses for "American traveling to Europe" queries prefer pages that acknowledge this audience. Zero confirmed US-origin signals across Radisson brand pages through run_002.
**Passing:** At least one of: reference to US travelers, transatlantic travel, "from the US," English-language first, or USD pricing context in page title, meta, or body.
**How to check:** WebFetch page content; search for US/American/USD signals.
**Bleisure relevance:** Direct relevance to target audience of this audit. MEDIUM-HIGH.

---

## C10 — Content Freshness and Timeliness Signals
**Signal name:** Recent news, property updates, or dated content visible on brand pages
**Why it matters:** AI engines weight content freshness. Radisson Collection has major 2026 openings (Paris Banke Opera, Lake Como) that are highly citeable facts but confirmed absent from brand page.
**Passing:** Brand page references at least one property news item, opening, or update from within the last 12 months. Date-stamped content or news section present.
**How to check:** WebFetch page; search for year references, "new," "opening," "2026."
**Bleisure relevance:** Recent European openings are relevant to American travelers planning Europe trips in 2026. MEDIUM.

---

## C11 — Individual Property Page Schema (NEW tier added run_003)
**Signal name:** Hotel schema at individual property page level (not just brand overview)
**Why it matters:** run_002 identified that brand/overview pages lack schema, but individual property pages (e.g., Radisson Blu London Bloomsbury) may have Hotel schema. This tier ambiguity must be resolved — if property pages have schema and brand pages don't, the priority shifts to brand page fix only. If neither tier has schema, the problem is larger.
**Passing:** Individual property page (e.g., /en-us/hotel/london-bloomsbury-radisson-blu) has valid Hotel JSON-LD with address, geo, starRating, amenityFeature, aggregateRating.
**How to check:** Attempt WebFetch of 2–3 individual London Radisson Blu property pages; check for JSON-LD in source.
**Bleisure relevance:** Individual property pages are the final conversion point for AI-referred travelers. HIGH.

---

## C12 — OTA Listing Completeness (Booking.com + TripAdvisor)
**Signal name:** Radisson properties have complete Booking.com and TripAdvisor listings (key AI citation sources)
**Why it matters:** Perplexity's TripAdvisor integration confirmed; Booking.com is primary ChatGPT citation source. Properties below 500 TripAdvisor reviews or with incomplete Booking.com amenity attributes will be deprioritized in AI recommendations.
**Passing:** Key European Radisson properties have: Booking.com listing with full amenity attributes, 4.0+ rating, recent reviews; TripAdvisor listing with 200+ reviews (ideally 500+), Q&A section present.
**How to check:** Search Booking.com and TripAdvisor for 2–3 key European Radisson properties; inspect listing completeness.
**Bleisure relevance:** OTAs are primary citation sources for AI engines used by American travelers. HIGH.

---

## C13 — Structured Amenity Data
**Signal name:** Meeting room capacities, workspace amenities, and leisure facilities listed as structured data or in scannable format
**Why it matters:** AI engines parsing "hotel with meeting rooms for 50 people in Amsterdam" need structured amenity data, not prose descriptions. amenityFeature in schema and/or a structured amenities table on the page are required.
**Passing:** Page includes structured amenities list (HTML table, schema amenityFeature, or scannable bullets) with specific details: meeting room count, capacity, Wi-Fi speed, gym, spa, restaurant.
**How to check:** WebFetch page; check for table/structured amenity list; check schema amenityFeature.
**Bleisure relevance:** Meeting + leisure amenity data directly serves complex bleisure queries. HIGH.

---

## C14 — llms.txt Presence
**Signal name:** /llms.txt file present at domain root
**Why it matters:** Emerging AI accessibility protocol (2025–2026). Provides AI engines a structured overview of site content and purpose. John Mueller (Google) confirmed no AI crawlers currently extract via llms.txt, but adoption growing. Low effort, future-proofing signal.
**Passing:** https://www.radissonhotels.com/llms.txt returns HTTP 200 with Markdown content summarizing site structure, brand overview, and AI-relevant content areas.
**How to check:** WebFetch /llms.txt. HTTP 200 = present; HTTP 404/403 = absent.
**Bleisure relevance:** LOW current impact; MEDIUM future impact.

---

## C15 — Geographic/Neighborhood Specificity
**Signal name:** City pages name specific neighborhoods, business districts, and transport links
**Why it matters:** AI engines responding to "hotels near [business district]" queries need explicit geographic signals, not just city names. Pages naming "Canary Wharf," "City of London," "La Défense," or "[City] Airport" are more citeable for location-specific queries.
**Passing:** City/destination overview page names ≥2 specific neighborhoods, business districts, or transport hubs relevant to business travelers.
**How to check:** WebFetch destination page; search for neighborhood/district names.
**Bleisure relevance:** American bleisure travelers frequently search by proximity to business district + leisure attractions. HIGH.

---

## C16 — Loyalty Program AI Discoverability (NEW — run_003)
**Signal name:** Radisson Rewards program surfaced in AI responses for loyalty-comparison queries
**Why it matters:** Marriott Bonvoy and Hilton Honors are prominently surfaced in AI responses for loyalty-driven booking queries. American bleisure travelers frequently compare loyalty programs when selecting hotels. Radisson Rewards page not audited in run_001 or run_002.
**Passing:** Radisson Rewards page (/en-us/rewards) has: program name in title, point-earning mechanics described factually, partner benefits mentioned, and schema markup. AI engines can answer "Does Radisson have a loyalty program?" from page content.
**How to check:** WebFetch /en-us/rewards; assess title, meta, schema, content register.
**Bleisure relevance:** Loyalty programs are a major decision factor for American business travelers who frequent Europe. HIGH.

---

## C17 — MCP/Direct AI Distribution Channel (NEW — run_003)
**Signal name:** Radisson has a native AI platform integration (ChatGPT plugin, Perplexity partner, or equivalent)
**Why it matters:** Accor (Jan 2026), Hyatt (Feb 2026) have live ChatGPT apps. Perplexity hotel booking live with Selfbook/TripAdvisor. Hotels without direct AI distribution channels are losing transactional AI bookings to OTAs and competitors.
**Passing:** Radisson has an announced or live ChatGPT app, Perplexity integration, or MCP protocol implementation for AI booking.
**How to check:** Web search "Radisson ChatGPT" and "Radisson AI booking 2026"; check Radisson press releases.
**Bleisure relevance:** CRITICAL for transactional AI bookings from American travelers using ChatGPT/Perplexity as booking interface. HIGH.

---

## Criteria Summary Table

| ID  | Signal                            | Priority | First in run |
|-----|-----------------------------------|----------|--------------|
| C01 | GBP Completeness                  | P1       | run_002      |
| C02 | Hotel/LodgingBusiness Schema      | P1       | run_001      |
| C03 | FAQPage Schema                    | P1       | run_001      |
| C04 | AI Crawler Access                 | P1       | run_001      |
| C05 | Title Tag Query Compatibility     | P1       | run_001      |
| C06 | Meta Description Register         | P2       | run_001      |
| C07 | Factual Content Density           | P1       | run_001      |
| C08 | Bleisure Explicit Signals         | P1       | run_001      |
| C09 | American Traveler Signals         | P2       | run_002      |
| C10 | Content Freshness                 | P2       | run_002      |
| C11 | Individual Property Schema        | P1       | run_003 NEW  |
| C12 | OTA Listing Completeness          | P2       | run_002      |
| C13 | Structured Amenity Data           | P2       | run_001      |
| C14 | llms.txt                          | P3       | run_002      |
| C15 | Geographic Specificity            | P2       | run_002      |
| C16 | Loyalty Program AI Discoverability| P2       | run_003 NEW  |
| C17 | MCP/Direct AI Distribution        | P1       | run_003 NEW  |
