# Gap Analysis — run_002 | 2026-03-20

**Pages audited:** 5 Priority 1 + 1 Priority 2 rotation (Meeting/Conference)
**Total gaps this run:** 39 (25 persistent from run_001 + 14 newly identified)
**New gaps:** 14 | **Persistent gaps:** 25 (0 resolved since run_001 — same-day run, no implementation expected)

---

## Persistent Gaps from run_001 (Summary)

All 25 gaps from run_001 remain unresolved. They are listed below for tracking purposes with updated severity notes where applicable.

| Gap ID | Page | Criterion | Type | Severity | Status |
|--------|------|-----------|------|----------|--------|
| GAP-001 | Homepage | C01 — Hotel schema | MISSING | 3 | PERSISTENT |
| GAP-002 | Homepage | C02 — FAQPage schema | MISSING | 3 | PERSISTENT |
| GAP-003 | Homepage | C03 — Meta description register | MISALIGNED | 2 | PERSISTENT |
| GAP-004 | Homepage | C04 — Title tag alignment | MISALIGNED | 2 | PERSISTENT |
| GAP-005 | Homepage | C07 — Entity signals | WEAK | 2 | PERSISTENT |
| GAP-006 | Homepage | C08 — Traveler type signals | MISSING | 2 | PERSISTENT |
| GAP-007 | Radisson Blu | C01 — Hotel schema | MISSING | 3 | PERSISTENT |
| GAP-008 | Radisson Blu | C02 — FAQPage schema | MISSING | 3 | PERSISTENT |
| GAP-009 | Radisson Blu | C03 — Meta description register | MISALIGNED | 3 | PERSISTENT |
| GAP-010 | Radisson Blu | C09 — Content register | MISALIGNED | 3 | PERSISTENT |
| GAP-011 | Radisson Blu | C05 — FAQ/Q&A blocks | MISSING | 3 | PERSISTENT |
| GAP-012 | Radisson Blu | C08 — Traveler type signals | MISSING | 3 | PERSISTENT |
| GAP-013 | Radisson Blu | C04 — Title tag alignment | WEAK | 1 | PERSISTENT |
| GAP-014 | Radisson (brand) | C01 — Hotel schema | MISSING | 3 | PERSISTENT |
| GAP-015 | Radisson (brand) | C04 — Title tag alignment | MISALIGNED | 3 | PERSISTENT |
| GAP-016 | Park Plaza | C01 — Hotel schema | MISSING | 3 | PERSISTENT → now formally confirmed |
| GAP-017 | Park Plaza | C02 — FAQPage schema | MISSING | 2 | PERSISTENT → now formally confirmed |
| GAP-018 | London | C04 — Title tag alignment | MISALIGNED | 3 | PERSISTENT (from run_001) |
| GAP-019 | London | C08 — Traveler type / bleisure | MISSING | 3 | PERSISTENT (from run_001) |
| GAP-020 | London | C02 — FAQPage schema | MISSING | 3 | PERSISTENT (from run_001) |
| GAP-021 | London | C01 — Hotel schema | MISSING | 3 | PERSISTENT (from run_001) |
| GAP-022 | London | C09 — Content register (tourism-first) | MISALIGNED | 3 | PERSISTENT (from run_001) |
| GAP-023 | Site-wide | C01 — Hotel/LodgingBusiness schema | MISSING | 3 | PERSISTENT — all brand/overview pages |
| GAP-024 | Site-wide | C02 — FAQPage schema | MISSING | 3 | PERSISTENT — all brand/overview pages |
| GAP-025 | Site-wide | C11 — AI crawler access | MISSING | 3 | PERSISTENT (was PROP-016 in run_001; now formal criterion C11) |

**Severity note on GAP-025 (AI crawler access):** Re-evaluated in run_002 with new literature data. Perplexity documented to bypass robots.txt via headless browsers — meaning Radisson's 403 blocking may not fully prevent Perplexity crawling but does block GPT-User, Claude-Web, and other compliant AI retrieval crawlers. This gap is more nuanced than run_001 characterized. Still Severity 3 but root cause is more complex.

---

## New Gaps Identified in run_002

---

### GAP-026
**Gap ID:** GAP-026
**Page URL:** https://www.radissonhotels.com/en-us/brand/park-plaza
**Criterion:** C04 — Title Tag Alignment
**Current metadata state:** Title is "City Centre Hotels | Park Plaza Hotels & Resorts"
**Gap type:** MISALIGNED
**Gap description:** "City Centre Hotels" is a functional category descriptor, not a query-answering title. It does not include geographic specificity, traveler type, or brand value proposition. An AI engine parsing this title cannot distinguish between a generic "city centre hotels" category page and a specific brand offering. Compare: Booking.com titles use "[Brand] Hotels — [Location] | Official Site" format. The bleisure traveler query "Park Plaza hotels in Europe for business travelers" cannot be answered by this title.
**Severity:** 2
**New or recurring:** NEW (page was unassessable in run_001)

---

### GAP-027
**Gap ID:** GAP-027
**Page URL:** https://www.radissonhotels.com/en-us/brand/park-plaza
**Criterion:** C08 — Traveler Type Signals (Business / Bleisure / American)
**Current metadata state:** Body copy confirmed: "Park Plaza is an upscale hotel brand for business and leisure travelers" — this is the ONLY brand page in the portfolio with any bleisure signal. However: (a) this is body copy, not title or meta description; (b) no American traveler specificity; (c) no European destination specificity.
**Gap type:** WEAK
**Gap description:** Park Plaza has the closest thing to a bleisure signal in the portfolio ("business and leisure travelers") but it is buried in body copy and does not appear in title or meta description. AI engines prioritizing above-the-fold content (ALM Corp 44% rule) will not reliably extract this signal for query routing. No American traveler context confirmed anywhere on this page.
**Severity:** 2
**New or recurring:** NEW (newly confirmed)

---

### GAP-028
**Gap ID:** GAP-028
**Page URL:** https://www.radissonhotels.com/en-us/brand/park-plaza
**Criterion:** C05 — FAQ/Q&A Content Blocks
**Current metadata state:** No FAQ content detected in SERP or confirmed body copy
**Gap type:** MISSING
**Gap description:** Park Plaza has sub-pages for family travel (/family-program) and digital services (/go-digital) and London destinations (/destinations/united-kingdom/london) — suggesting content infrastructure exists. Yet no FAQ content is accessible from SERP for the main brand page. Questions an AI engine would route to this page: "Is Park Plaza good for business travelers?", "Where are Park Plaza hotels in London?", "Does Park Plaza have meeting rooms?" — none of these are answerable from confirmed on-page content.
**Severity:** 2
**New or recurring:** NEW

---

### GAP-029
**Gap ID:** GAP-029
**Page URL:** https://www.radissonhotels.com/en-us/brand/radisson-collection
**Criterion:** C01 — Hotel / LodgingBusiness Schema
**Current metadata state:** NOT CONFIRMABLE (403 blocked). No rich result appearances in SERP.
**Gap type:** MISSING
**Gap description:** Radisson Collection is the luxury flagship brand. No Hotel or LodgingBusiness schema detected in SERP. Individual property pages (Lake Como, Paris Banke Opera) being added in 2026 — if schema is not implemented at launch, these new high-prestige properties miss their opening window for AI recommendation visibility.
**Severity:** 2
**New or recurring:** NEW (page newly audited)

---

### GAP-030
**Gap ID:** GAP-030
**Page URL:** https://www.radissonhotels.com/en-us/brand/radisson-collection
**Criterion:** C09 — Content Register
**Current metadata state:** "premium style collection of luxury hotels offering quality services, dining, wellness and much more" — generic luxury marketing copy.
**Gap type:** MISALIGNED
**Gap description:** Radisson Collection's 2026 expansion news (Paris Banke Opera in a 1907 building with Eiffel-designed staircase, Lake Como in a 30-year-dormant historic building) is highly specific, factual, and differentiated content that would rank in AI recommendations for luxury travelers. This content appears in press releases but is not confirmed on the brand page. The brand page instead uses generic luxury marketing copy ("quality services, dining, wellness"). For high-intent luxury and business travelers using AI discovery, this is a significant missed opportunity.
**Severity:** 2
**New or recurring:** NEW

---

### GAP-031
**Gap ID:** GAP-031
**Page URL:** https://www.radissonhotels.com/en-us/brand/radisson-collection
**Criterion:** C05 — FAQ/Q&A Content Blocks
**Current metadata state:** No FAQ content detected in SERP
**Gap type:** MISSING
**Gap description:** Luxury travelers and corporate executives using AI to research accommodation ask specific questions: "What makes Radisson Collection different from Radisson Blu?", "Which Radisson Collection hotels are opening in Europe in 2026?", "Is Radisson Collection comparable to Marriott Autograph Collection?" No FAQ content available to answer these on the brand page.
**Severity:** 2
**New or recurring:** NEW

---

### GAP-032
**Gap ID:** GAP-032
**Page URL:** https://www.radissonhotels.com/en-us/meeting-conference-hotels
**Criterion:** C04 — Title Tag Alignment
**Current metadata state:** "Book Your Meeting Rooms and Conferences Now | Radisson Hotels"
**Gap type:** MISALIGNED
**Gap description:** The title is a CTA ("Book...Now"), not a query-answering descriptor. An American corporate traveler using AI to search "best conference hotels in London for a finance industry event" cannot be routed to this page by a title that leads with a booking imperative. Compare Marriott's meeting page: uses descriptive titles like "Meeting & Conference Hotels | Marriott Hotels" that match discovery queries. The CTA format may also reduce AI citation probability as engines prefer informational titles.
**Severity:** 2
**New or recurring:** NEW

---

### GAP-033
**Gap ID:** GAP-033
**Page URL:** https://www.radissonhotels.com/en-us/meeting-conference-hotels
**Criterion:** C05 — FAQ/Q&A Content Blocks
**Current metadata state:** No FAQ content detected in SERP for main meeting page
**Gap type:** MISSING
**Gap description:** Meeting and conference discovery queries are high-intent and frequently routed through AI: "Which hotel chains have the best conference facilities in European capitals?", "What are the best hotels near London Heathrow for a corporate event?", "Does Radisson offer hybrid meeting packages with video conferencing?". No FAQ content on the main meeting page to capture these queries. Industry-specific sub-pages (finance, associations) exist but are not linked from an FAQ discovery layer.
**Severity:** 2
**New or recurring:** NEW

---

### GAP-034
**Gap ID:** GAP-034
**Page URL:** https://www.radissonhotels.com/en-us/meeting-conference-hotels
**Criterion:** C13 — Structured Amenity Data (MeetingRoom/Event Schema)
**Current metadata state:** NOT CONFIRMABLE (fetch blocked). No rich results for meeting rooms, event spaces, or conference facilities visible in SERP.
**Gap type:** MISSING
**Gap description:** Schema.org includes MeetingRoom type (subtype of Accommodation) and EventVenue type. For corporate travel queries, AI booking agents (Amex, Chase) that perform autonomous booking will look for machine-readable meeting room capacity, AV equipment, catering options, and pricing. Without structured amenity data, Radisson's conference offerings are invisible to AI booking agents even if the content exists in prose form. Radisson Heathrow is confirmed to have 41 meeting rooms and 2,000+ sqm of meeting space — this data exists but is likely in prose, not schema.
**Severity:** 2
**New or recurring:** NEW

---

### GAP-035
**Gap ID:** GAP-035
**Page URL:** https://www.radissonhotels.com/en-us/meeting-conference-hotels
**Criterion:** C08 — Traveler Type Signals (American corporate traveler)
**Current metadata state:** No American corporate traveler signals in confirmed title or meta description
**Gap type:** MISSING
**Gap description:** Confirmed content mentions "global presence in business districts, capital cities, and airport gateways" but does not explicitly reference American corporate travelers, US-to-Europe travel, or transatlantic business travel context. An American executive using AI to plan a European conference tour will not find explicit relevance signals. Compare: Marriott Meetings pages have dedicated content for US corporate travel to Europe.
**Severity:** 1
**New or recurring:** NEW

---

### GAP-036
**Gap ID:** GAP-036
**Page URL:** https://www.radissonhotels.com (site-wide)
**Criterion:** C11 — AI Crawler Access (robots.txt + 403 behavior)
**Current metadata state:** /robots.txt returns 403. /llms.txt returns 403 (absent). All direct page fetches return 403.
**Gap type:** MISSING
**Gap description:** Site-wide HTTP 403 blocks all direct crawling. /robots.txt is itself blocked, preventing assessment of whether AI retrieval crawlers (ChatGPT-User, Claude-Web, PerplexityBot) are explicitly permitted or blocked. Best practice (2026): allow retrieval crawlers, block training crawlers. Radisson currently has no confirmed AI-specific crawler policy. Literature finding: Perplexity documented to bypass robots.txt via headless browsers — meaning Perplexity may be partially scraping Radisson content despite 403 blocking. ChatGPT-User and Claude-Web are more compliant and likely blocked by 403. This gap directly prevents AI-generated answers from citing Radisson's own website. /llms.txt is an emerging alternative — could explicitly declare AI accessibility without exposing full pages. Currently absent.
**Severity:** 3
**New or recurring:** PERSISTENT (was PROP-016 in run_001, now formalized as GAP-036 under C11)

---

### GAP-037
**Gap ID:** GAP-037
**Page URL:** https://www.radissonhotels.com/llms.txt (absent)
**Criterion:** C14 — llms.txt File
**Current metadata state:** /llms.txt returns 403 (file absent or blocked)
**Gap type:** MISSING
**Gap description:** llms.txt is an emerging 2026 protocol for explicitly declaring AI-accessible content at a domain. Unlike robots.txt, which tells crawlers what NOT to access, llms.txt positively declares what IS available for AI engines to use. Given Radisson's 403 blocking posture, an /llms.txt file could serve as an explicit accessibility declaration that allows specific AI retrieval agents to access curated content. This is a low-effort, high-signal fix. Fast-moving adoption among AI-forward brands in early 2026.
**Severity:** 2
**New or recurring:** NEW (criterion added in run_002)

---

### GAP-038
**Gap ID:** GAP-038
**Page URL:** OTA listings (off-site: Booking.com, TripAdvisor, Expedia, Yelp)
**Criterion:** C12 — OTA Listing Completeness
**Current metadata state:** Yelp listings for European Radisson properties: UNVERIFIED. Booking.com and TripAdvisor listings: PRESENT for individual properties but completeness/review volume UNVERIFIED for brand-level discoverability. Yelp added to ChatGPT January 2026 — European property coverage on Yelp is typically weak for non-US-city brands.
**Gap type:** WEAK (inferred)
**Gap description:** ChatGPT now uses Yelp data for hotel queries in addition to SerpAPI/Google Places. Radisson is a European-heavy brand. Yelp's European coverage is spotty — many European Radisson properties may have minimal or no Yelp presence, creating a specific ChatGPT citation gap. Additionally, with GPT-5.2 doubled search depth, consistency across 10+ citation sources matters more than ever. Radisson's OTA presence needs audit for completeness and review quality.
**Severity:** 2
**New or recurring:** NEW (criterion added in run_002)

---

### GAP-039
**Gap ID:** GAP-039
**Page URL:** All Priority 1 brand pages + meeting page
**Criterion:** C15 — Geographic Specificity (European Destinations + US Origination)
**Current metadata state:** No US-origination context confirmed in any audited page title or meta description. "Europe" mentioned in sub-page URLs but not in main brand page titles/descriptions.
**Gap type:** MISSING
**Gap description:** The target audience is American bleisure travelers from the US to Europe. None of the confirmed titles or meta descriptions contain: (a) specific European city names, (b) reference to American travelers, US flights, or US origination context, or (c) transatlantic travel framing. AI engines routing "hotels in Europe for American business travelers" have zero explicit signals from Radisson's own metadata to match this query. Compare: Marriott brand pages include "hotels in Europe for American travelers" as explicit content target. Park Plaza's London sub-page (/destinations/united-kingdom/london) is a partial exception but the main brand discovery pages are silent on this.
**Severity:** 2
**New or recurring:** NEW (criterion formalized in run_002)

---

## Gap Summary Table

| ID | Page | Criterion | Type | Severity | New/Persistent |
|----|------|-----------|------|----------|----------------|
| GAP-001 through GAP-025 | Multiple | Multiple | Mixed | 1-3 | PERSISTENT (from run_001) |
| GAP-026 | Park Plaza | C04 Title | MISALIGNED | 2 | NEW |
| GAP-027 | Park Plaza | C08 Traveler signals | WEAK | 2 | NEW |
| GAP-028 | Park Plaza | C05 FAQ blocks | MISSING | 2 | NEW |
| GAP-029 | Radisson Collection | C01 Schema | MISSING | 2 | NEW |
| GAP-030 | Radisson Collection | C09 Content register | MISALIGNED | 2 | NEW |
| GAP-031 | Radisson Collection | C05 FAQ blocks | MISSING | 2 | NEW |
| GAP-032 | Meeting/Conference | C04 Title | MISALIGNED | 2 | NEW |
| GAP-033 | Meeting/Conference | C05 FAQ blocks | MISSING | 2 | NEW |
| GAP-034 | Meeting/Conference | C13 Amenity schema | MISSING | 2 | NEW |
| GAP-035 | Meeting/Conference | C08 Traveler signals | MISSING | 1 | NEW |
| GAP-036 | Site-wide | C11 AI crawler access | MISSING | 3 | PERSISTENT (formalized) |
| GAP-037 | Site-wide | C14 llms.txt | MISSING | 2 | NEW |
| GAP-038 | OTA listings | C12 OTA completeness | WEAK | 2 | NEW |
| GAP-039 | All brand pages | C15 Geographic specificity | MISSING | 2 | NEW |

**Total gaps: 39**
**Severity 3:** GAP-001, 002, 007, 008, 009, 010, 011, 012, 014, 015, 018, 019, 020, 021, 022, 023, 024, 025, 036 (19 gaps)
**Severity 2:** GAP-003, 004, 005, 006, 013, 016, 017, 026, 027, 028, 029, 030, 031, 032, 033, 034, 037, 038, 039 (19 gaps)
**Severity 1:** GAP-035 (1 gap)
