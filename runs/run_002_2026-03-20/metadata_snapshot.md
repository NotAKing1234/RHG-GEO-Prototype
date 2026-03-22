# Metadata Snapshot — run_002 | 2026-03-20

**Fetch method:** WebFetch + WebSearch (radissonhotels.com continues to return HTTP 403 for all direct page fetches, including /robots.txt and /llms.txt; data gathered from Google SERP snippets, social metadata, and secondary source analysis)
**Fetch timestamp:** 2026-03-20
**Pages audited:** 5 Priority 1 pages + 1 Priority 2 rotation (Meeting/Conference page)
**Priority 3:** Skipped per rotation rules (run_001 also skipped; run_003 should include)
**Note on data quality:** Same limitation as run_001. HTTP 403 blocks direct source inspection. JSON-LD, OG tags, heading structure, alt text cannot be confirmed without direct fetch. SERP snippets remain the primary observation window. Key delta from run_001: Park Plaza now confirmed; Radisson Collection added; Meeting/Conference page added as Priority 2 rotation.

---

## Page 1: https://www.radissonhotels.com/en-us (Homepage)

**URL:** https://www.radissonhotels.com/en-us
**Fetch status:** 403 Blocked
**Fetch timestamp:** 2026-03-20

**Extracted title:** "Radisson Hotels Official Site | Book Rooms Worldwide"
**Source:** Google SERP snippet (confirmed)
**Change vs run_001:** NO CHANGE

**Extracted meta description:** "Explore over 1100 hotels worldwide and book your stay with us today, with the best online rates guaranteed!"
**Source:** Google SERP snippet (confirmed)
**Change vs run_001:** NO CHANGE

**Structured data blocks:** NOT CONFIRMABLE (fetch blocked). No Hotel schema, LodgingBusiness schema, FAQPage schema, or any rich result appearances detected in SERP. UNCHANGED from run_001.

**Open Graph tags:** NOT CONFIRMABLE (fetch blocked)

**Heading outline:** NOT CONFIRMABLE (fetch blocked)

**FAQ / Q&A presence:** NOT DETECTED. Radisson FAQ page exists at /en-us/faq (general booking FAQs) and /en-us/rewards/faq (loyalty FAQs) — neither surfacing rich results. Note from literature: Google no longer shows FAQ rich results for non-government/health sites (policy change 2023, still current 2026). FAQPage schema still valuable for AI engine parsability even without SERP rich result display.

**Alt text observations:** NOT CONFIRMABLE (fetch blocked)

**Query compatibility notes:**
- Title: transaction-focused ("Book Rooms Worldwide") — not discovery-oriented
- Meta description: booking incentive ("best online rates guaranteed") — not answer-format
- No traveler type, no European destination, no bleisure signals in confirmed metadata
- UNCHANGED since run_001

**Entity signal notes:**
- "Radisson Hotels" brand entity present (strong)
- "Worldwide" scope (too broad for European bleisure queries)
- No traveler type entity confirmed

---

## Page 2: https://www.radissonhotels.com/en-us/brand/radisson-blu (Radisson Blu Brand Page)

**URL:** https://www.radissonhotels.com/en-us/brand/radisson-blu
**Fetch status:** 403 Blocked
**Fetch timestamp:** 2026-03-20

**Extracted title:** "Radisson Blu Hotels & Resorts | Radisson Hotels"
**Source:** Google SERP snippet (confirmed)
**Change vs run_001:** NO CHANGE

**Extracted meta description / brand copy:** "We provide unparalleled service, comfort, and style while creating meaningful and memorable experiences. By paying close attention to the small details that make a big difference, we inspire unforgettable experiences with every stay."
**Source:** Search snippet body text (confirmed)
**Change vs run_001:** NO CHANGE

**Additional confirmed copy:** "Style, form, beauty and function. That's what you'll find at Radisson Blu." (confirmed, UNCHANGED)

**NEW discovery (run_002):** Sub-page /en-us/brand/radisson-blu/business-travel-offer now confirmed to exist in SERP ("Radisson Blu Hotels for Business Travelers | Radisson Hotels"). This is a dedicated business travel page. It was NOT in the run_001 audit. Indicates some existing business content infrastructure at sub-page level, but main brand page remains in marketing register.

**NEW discovery (run_002):** Regional sub-pages confirmed:
- /en-us/brand/radisson-blu/hotels-resorts/central-eastern-southern-europe — "Radisson Blu welcomes guests to stylish properties from Nice to Barcelona"
- /en-us/brand/radisson-blu/hotels-resorts/western-europe-nordics — "stylish and contemporary hotels and resorts in Western and Northern Europe and the United Kingdom"

**Structured data blocks:** NOT CONFIRMABLE. No rich result appearances in SERP. UNCHANGED.

**Open Graph tags:** NOT CONFIRMABLE

**Heading outline:** NOT CONFIRMABLE

**FAQ / Q&A presence:** NOT DETECTED in SERP for brand overview page

**Alt text observations:** NOT CONFIRMABLE

**Query compatibility notes:**
- Brand page: pure marketing register, zero factual content in confirmed metadata (UNCHANGED from run_001)
- Sub-page /business-travel-offer exists — suggests some business travel content is available at sub-page level, but the main brand discovery page does not surface this
- "Largest upper-upscale brand in Europe for over a decade" — confirmed in press release search result (factual claim exists in corporate media but not on brand page)
- No American traveler targeting in any confirmed metadata

**Entity signal notes:**
- "Radisson Blu Hotels & Resorts" strong brand entity
- European context detectable via sub-pages but not main brand page
- Business travel entity present at sub-page level (/business-travel-offer) but absent from main brand page

---

## Page 3: https://www.radissonhotels.com/en-us/brand/radisson-collection (Radisson Collection Brand Page)

**URL:** https://www.radissonhotels.com/en-us/brand/radisson-collection
**Fetch status:** 403 Blocked
**Fetch timestamp:** 2026-03-20
**Note:** This page was in run_001 target URLs but not individually audited. Adding to run_002 audit.

**Extracted title:** "Radisson Collection Luxury Hotels | Radisson Hotels"
**Source:** Google SERP snippet (confirmed)
**Change vs run_001:** NEWLY CONFIRMED (not individually audited in run_001)

**Extracted meta description / brand copy:** "premium style collection of luxury hotels offering quality services, dining, wellness and much more. At the top of the ladder sits Radisson Collection, with marquee addresses in historic buildings, prominent city landmarks or prime resort locations, featuring elevated design, polished service and more individualized experiences."
**Source:** SERP snippet and secondary sources

**Notable 2026 news:** 4 new Radisson Collection properties opening in 2026: Lake Como (early 2026), Paris Banke Opera (H2 2026), Casablanca Lincoln Hotel (late 2026), plus additional MENA/Asia expansion. This is highly citable factual content that could feed AI recommendations but is not confirmed to be on the brand page itself.

**Structured data blocks:** NOT CONFIRMABLE. No rich result appearances in SERP.

**Open Graph tags:** NOT CONFIRMABLE

**Heading outline:** NOT CONFIRMABLE

**FAQ / Q&A presence:** NOT DETECTED in SERP

**Alt text observations:** NOT CONFIRMABLE

**Query compatibility notes:**
- "premium style collection of luxury hotels" — partially informational but still generic
- No mention of American travelers, business travel, bleisure
- "individualized experiences" — marketing register, not factual
- Notable missed opportunity: 2026 expansion news (Paris, Lake Como) is highly discoverable factual content that is not surfacing in AI recommendations from this brand page

**Entity signal notes:**
- "Radisson Collection" brand entity (adequate)
- "Luxury Hotels" category (adequate for luxury audience)
- Geographic: absent from confirmed main brand page metadata (sub-pages show specific destinations)
- Traveler type: absent from confirmed metadata

---

## Page 4: https://www.radissonhotels.com/en-us/brand/radisson-red (Radisson RED Brand Page)

**URL:** https://www.radissonhotels.com/en-us/brand/radisson-red
**Fetch status:** 403 Blocked
**Fetch timestamp:** 2026-03-20
**Note:** This page was in run_001 target URLs via the Radisson RED URL. Adding to run_002 audit.

**Extracted title:** "Radisson RED - Stylish & Boutique Hotels | Radisson Hotels"
**Source:** Google SERP snippet (confirmed)

**Extracted meta description / brand copy:** "Radisson RED presents a playful twist on conventional hotel stays, injecting new life into hotels through informal services where anything goes, a social scene that's waiting to be shared and bold design."
**Source:** SERP snippet

**Target audience confirmed:** "style-savvy, connected and sociable travelers" — lifestyle/social audience, not primary business/bleisure audience.

**Structured data blocks:** NOT CONFIRMABLE. No rich result appearances in SERP.

**Open Graph tags:** NOT CONFIRMABLE

**Heading outline:** NOT CONFIRMABLE

**FAQ / Q&A presence:** NOT DETECTED

**Alt text observations:** NOT CONFIRMABLE

**Query compatibility notes:**
- Title: "Stylish & Boutique" — brand voice, not query-answering
- Brand explicitly positioned as lifestyle/social, not business/bleisure
- "Playful twist on conventional hotel stays" — misaligned for business travel queries
- Low relevance for primary American bleisure audience (aged 25-55, business-first)
- 100+ hotels in operation and under development — scale signal present but not prominent

**Entity signal notes:**
- "Radisson RED" brand entity (adequate)
- "Stylish & Boutique Hotels" category (lifestyle-oriented)
- No geographic specificity, no business travel, no bleisure signals

**Audit note:** Radisson RED is not the primary brand for bleisure/business traveler audience. Schema and FAQ gaps noted but lower severity than Radisson Blu and Collection pages for target audience use case.

---

## Page 5: https://www.radissonhotels.com/en-us/brand/park-plaza (Park Plaza Brand Page)

**URL:** https://www.radissonhotels.com/en-us/brand/park-plaza
**Fetch status:** 403 Blocked
**Fetch timestamp:** 2026-03-20
**Note:** Unassessable in run_001. NOW CONFIRMED from SERP.

**Extracted title:** "City Centre Hotels | Park Plaza Hotels & Resorts"
**Source:** Google SERP snippet (confirmed)
**Change vs run_001:** NEWLY CONFIRMED (was NOT CONFIRMED in run_001)

**Extracted meta description:** "Park Plaza Hotels & Resorts offer stylish guest rooms in city centre locations, meeting facilities and award-winning restaurants and bars."
**Source:** SERP snippet (confirmed)
**Register assessment:** Partially informational — mentions "meeting facilities" and specific amenity types ("award-winning restaurants and bars"). Better than other Radisson brand pages. Does not include bleisure, American traveler, or European specificity signals.

**Confirmed brand copy:** "Park Plaza is an upscale hotel brand for business and leisure travelers, offering stylish guest rooms, outstanding meeting spaces and dedicated staff who provide reliable service that is flawlessly delivered."
**Note:** "business and leisure travelers" phrasing is closer to bleisure positioning than any other confirmed brand copy in portfolio. However, not explicitly American-facing.

**Structured data blocks:** NOT CONFIRMABLE. No rich result appearances in SERP.

**Open Graph tags:** NOT CONFIRMABLE

**Heading outline:** NOT CONFIRMABLE

**FAQ / Q&A presence:** NOT DETECTED. Park Plaza sub-pages confirmed: /family-program, /park-plaza-moments, /go-digital, /destinations/united-kingdom/london, /hotel-deals.

**Alt text observations:** NOT CONFIRMABLE

**Query compatibility notes:**
- Title "City Centre Hotels" — navigation/category oriented, not query-answering
- Meta description partially informational (meeting facilities mentioned)
- "business and leisure travelers" in confirmed body copy — positive signal
- No American traveler specificity
- London sub-page confirmed (/destinations/united-kingdom/london) — relevant for bleisure queries

**Entity signal notes:**
- "Park Plaza Hotels & Resorts" brand entity (strong)
- "City Centre Hotels" — geographic category signal (weak — city not named)
- "meeting facilities" — business amenity signal (moderate)
- "business and leisure travelers" — closest to bleisure entity signal in portfolio
- No American traveler entity

---

## Page 6: https://www.radissonhotels.com/en-us/meeting-conference-hotels (Meeting & Conference — Priority 2 Rotation)

**URL:** https://www.radissonhotels.com/en-us/meeting-conference-hotels
**Fetch status:** 403 Blocked
**Fetch timestamp:** 2026-03-20
**Note:** Priority 2 rotation for run_002 (London was Priority 2 rotation in run_001)

**Extracted title:** "Book Your Meeting Rooms and Conferences Now | Radisson Hotels"
**Source:** Google SERP snippet (confirmed)

**Extracted meta description:** "Discover the facilities available at our hotels for your meetings, conferences, and special events."
**Source:** SERP snippet (confirmed)

**OG metadata confirmed:**
- og:site_name: "Radisson Meetings"
- og:type: website
- og:title: same as page title
- og:description: same as meta description

**Sub-pages confirmed:**
- /destinations — "Meeting rooms and conference venues at Radisson Hotels"
- /types — "Hotel Events - Discover Our Solutions"
- /types/large-events — "Find Corporate Conference Venues"
- /industry-solutions — "Discover Our Industry Solutions for Corporate Events"
- /industry-solutions/finance — "Book Our Conference Rooms for Your Finance Events"
- /industry-solutions/association-signature-events
- /radisson-meetings-picklist
- /offers — promotions through Dec 2026

**Confirmed content:** Radisson Meetings — "clean, safe, office-quality set-ups with video conferencing"; "global presence in key destinations including business districts, capital cities, and airport gateways"; 2026 promo: 1-3 complimentary extras for meetings booked by Dec 31, 2026 for events held through March 2027.

**Structured data blocks:** NOT CONFIRMABLE. No rich result appearances in SERP for main meeting page.

**FAQ / Q&A presence:** NOT DETECTED for main meeting page

**Alt text observations:** NOT CONFIRMABLE

**Query compatibility notes:**
- Title: "Book Your Meeting Rooms and Conferences Now" — transactional CTA, not query-answering
- A bleisure traveler searching "hotels in London with good meeting rooms" will not find this page via AI — the page doesn't surface in AI discovery for individual traveler queries
- No FAQ content for compound meeting + leisure queries
- Industry-specific sub-pages are a positive signal (finance, associations) — shows content depth
- No explicit American corporate traveler content

**Entity signal notes:**
- "Radisson Meetings" as distinct entity (adequate for MICE market)
- Meeting rooms, conferences, corporate events — strong B2B signals
- No individual traveler / bleisure signal
- No geographic specificity in title or description

---

## Cross-Page Patterns (run_002)

**Consistent across all confirmed pages (all UNCHANGED from run_001):**
- No FAQPage schema rich results for any audited URL
- No Hotel or LodgingBusiness schema in SERP rich results for any brand/overview page
- No rich results of any type for any audited URL
- No explicit American traveler targeting in any confirmed title or meta description
- No explicit bleisure compound content at brand or overview level (exception: Park Plaza body copy partially)

**New cross-page observations (run_002):**
- Radisson Blu sub-page /business-travel-offer confirmed — partial infrastructure exists but not discoverable from main brand page
- Park Plaza is relatively strongest on C03 (informational register, meeting facilities mentioned)
- Meeting/Conference section has extensive sub-page architecture — good for MICE, not optimized for individual bleisure traveler queries
- Radisson Collection 2026 expansion news (Paris, Lake Como) is publicly available factual content not surfacing from brand page
- /llms.txt confirmed 403 (absent)
- /robots.txt confirmed 403 (cannot assess AI crawler policy)

**Schema status summary:**
- FAQPage schema: ABSENT across all audited pages (SERP proxy method)
- Hotel/LodgingBusiness schema: ABSENT across all audited pages (SERP proxy method)
- MeetingRoom/Event schema: ABSENT from meeting page (SERP proxy method)
- OG tags: UNCONFIRMABLE for all pages except Meeting/Conference (OG confirmed via social metadata)
