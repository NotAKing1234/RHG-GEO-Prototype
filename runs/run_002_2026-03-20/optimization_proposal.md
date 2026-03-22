# Optimization Proposal — run_002 | 2026-03-20

**Sources synthesized from:**
- `/framework/run_002_criteria.md`
- `/runs/run_002_2026-03-20/gap_research.md`
- `/runs/run_002_2026-03-20/context_brief.md`

---

## Executive Summary

This run identified **39 gaps** across 6 audited pages (5 Priority 1 + Meeting/Conference Priority 2 rotation). Of these, **25 are persistent** from run_001 with zero implementation observed (expected: same-day run), and **14 are new** gaps arising from newly audited pages (Radisson Collection, Park Plaza confirmed, Meeting/Conference page) and new criteria (C11–C15: AI crawler access, OTA completeness, llms.txt, geographic specificity, structured amenity data).

**Top 3 Priority Changes:**

1. **Unblock AI retrieval crawlers (Cloudflare/WAF configuration)** — radissonhotels.com returns HTTP 403 for all direct fetches including /robots.txt and /llms.txt. Websites blocking AI crawlers are cited 73% less in ChatGPT responses. This is the foundational prerequisite: every other fix is irrelevant if AI retrieval systems cannot access the pages. Estimated implementation time: 1–2 hours (Cloudflare configuration change).

2. **Deploy Hotel/LodgingBusiness JSON-LD schema with amenityFeature and potentialAction across all brand and overview pages** — confirmed absent from all audited pages in SERP rich results. Only 10.6% of hotel websites have good schema; implementing it creates immediate competitive differentiation. Pages with schema are cited 2–3x more by AI engines. Booking.com and Marriott schema implementations are the primary reason they dominate AI hotel recommendations.

3. **Rewrite Radisson Blu brand page meta description and opening body copy to factual register** — current confirmed copy ("unparalleled service, comfort, and style… unforgettable experiences") contains zero extractable facts. A 2-sentence rewrite ("Radisson Blu: 300+ upscale hotels across Europe, Africa, and Asia Pacific. Properties feature meeting and conference facilities, premium dining, and fitness centers for business and leisure travelers.") is the highest-ROI content change available. Zero technical effort, pure copywriting.

---

## Proposal Entries

---

### PROP-001 — Unblock AI Retrieval Crawlers (GAP-036, GAP-025)

**1. Proposed change**
Audit Cloudflare/WAF configuration to identify the rule triggering HTTP 403 for all fetches (likely the "Block AI Scrapers and Crawlers" managed rule enabled by default since July 2025). Disable blanket AI block. Deploy a robots.txt at /robots.txt (currently also 403) with explicit Allow directives for AI retrieval crawlers:
```
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: Claude-User
Allow: /
User-agent: GPTBot
Disallow: /
User-agent: ClaudeBot
Disallow: /
```
Strategy: allow retrieval crawlers (real-time citation), block training crawlers (IP protection). Verify with crawl test from each bot user-agent post-deployment.

**2. Source citation**
C11 — AI Crawler Access. Research: sites blocking GPTBot cited 73% less in ChatGPT responses (2026 study). Distinction between training crawlers (block) vs. retrieval crawlers (allow) is 2026 best practice standard. Source: Cloudflare AI Search Visibility Guide 2026 (nytroseo.com); PhocusWire "Making the case for hotels to enable AI crawlability"; ChatRank.ai "The Hidden Cost of Cloudflare's AI Scraper Crackdown."

**3. Current state**
HTTP 403 blocks all direct fetches. /robots.txt returns 403 (cannot be assessed). /llms.txt returns 403 (absent). AI retrieval crawlers (ChatGPT-User, Claude-Web) almost certainly blocked. Perplexity documented to sometimes bypass via headless browser — unreliable, not structured retrieval access.

**4. Inferred implementation status**
N/A — first non-same-day comparison will assess. This was PROP-016 in run_001 and remains unimplemented.

**5. Directional impact estimate**
CRITICAL. Without crawler access, all downstream fixes (schema, FAQ content, factual copy) deliver zero AI visibility improvement. Unblocking retrieval crawlers is the prerequisite for every other proposal.

**6. Priority tier**
P1

---

### PROP-002 — Deploy Hotel/LodgingBusiness JSON-LD Schema Site-Wide (GAP-001, GAP-023)

**1. Proposed change**
Add JSON-LD `<script type="application/ld+json">` block to every brand page (Homepage, Radisson Blu, Radisson Collection, Radisson RED, Park Plaza), every city/destination page, and the Meeting/Conference page. Minimum viable fields:
```json
{
  "@context": "https://schema.org",
  "@type": ["LodgingBusiness", "Hotel"],
  "name": "Radisson Blu Hotels & Resorts",
  "description": "Radisson Blu is an upper-upscale hotel brand operating 300+ properties across Europe, Africa, the Middle East, and Asia Pacific, offering meeting facilities, premium dining, and flexible workspaces.",
  "url": "https://www.radissonhotels.com/en-us/brand/radisson-blu",
  "amenityFeature": [
    {"@type": "LocationFeatureSpecification", "name": "Meeting rooms", "value": true},
    {"@type": "LocationFeatureSpecification", "name": "Business center", "value": true},
    {"@type": "LocationFeatureSpecification", "name": "High-speed WiFi", "value": true},
    {"@type": "LocationFeatureSpecification", "name": "Fitness center", "value": true},
    {"@type": "LocationFeatureSpecification", "name": "Restaurant", "value": true}
  ],
  "potentialAction": {
    "@type": "ReserveAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://www.radissonhotels.com/en-us/booking/room-display?..."
    }
  }
}
```
For brand overview pages, add `"numberOfRooms"` (total portfolio rooms) and `"hasOfferCatalog"` pointing to the hotel search page.

**2. Source citation**
C01 — Hotel/LodgingBusiness Schema. Research: only 10.6% of hotel websites have good schema implementation; pages with schema cited 2–3x more by AI engines; critical underutilized fields: aggregateRating (12.5% adoption), amenityFeature (7.7%), geo (18.8%); potentialAction enables agentic AI booking. Source: HotelRank.ai Hotel Schema Adoption Study 2026; Travel Tractions Schema Markup for Hotels.

**3. Current state**
No Hotel, LodgingBusiness, or any structured data schema detected in SERP rich results for any audited page. No rich results of any kind. Status UNCHANGED from run_001.

**4. Inferred implementation status**
Not implemented — confirmed unchanged from run_001. This was PROP-006, PROP-013, PROP-014, PROP-015 in run_001.

**5. Directional impact estimate**
HIGH. Hotel/LodgingBusiness schema is the machine-readable entity declaration that AI booking agents and recommendation engines require. Without it, Radisson properties cannot be distinguished from generic hotel results by AI systems. Booking.com and Expedia's schema pipelines are why they dominate AI citations for Radisson's own properties.

**6. Priority tier**
P1

---

### PROP-003 — Deploy FAQPage JSON-LD + Visible FAQ Sections Site-Wide (GAP-002, GAP-024)

**1. Proposed change**
Add a visible FAQ section (H3 questions + paragraph answers) plus FAQPage JSON-LD to each brand page and the Meeting/Conference page. Questions must be in natural language query format. Minimum 5 questions per page. Example for Radisson Blu:
- "What amenities does Radisson Blu offer for business travelers in Europe?" → factual answer naming meeting rooms, WiFi, business center, flexible workspace
- "Do Radisson Blu hotels have meeting and conference facilities?" → answer: yes, with capacity range
- "Which Radisson Blu hotels are best for American travelers visiting Europe?" → answer: name 3–4 flagship European properties with US flight connections
- "Are Radisson Blu hotels suitable for bleisure travelers combining business and leisure?" → answer: yes, with specific amenity examples
- "What is Radisson Blu's loyalty program and does it work for US-based travelers?" → answer: Radisson Rewards, points, partner airlines

NOTE: Google no longer shows FAQ rich results for hotel brands (policy change 2023, still active 2026). FAQPage schema value in 2026 is entirely AI engine parsability — ChatGPT, Perplexity, and Google AI Overviews all extract FAQ structured data for answer generation. The implementation is still warranted; the success metric is AI citation rate, not SERP rich result display.

**2. Source citation**
C02 — FAQPage Schema. Research: FAQ structured data has highest citation rate in AI-generated answers; FAQPage schema increases AI citability up to 2x vs. unstructured content; AI engines pattern-match FAQ Q&A pairs directly against user conversational queries. Source: Frase.io "Are FAQ Schemas Important for AI Search, GEO & AEO?" 2026; GenOptima AEO Techniques 2026; Zumeirah.com FAQ Schema for AI Overviews.

**3. Current state**
No FAQPage schema or visible FAQ content detected in SERP for any Priority 1 page. /en-us/faq and /en-us/rewards/faq exist but are not brand/destination pages and are not generating AI citations for bleisure travel queries.

**4. Inferred implementation status**
Not implemented — unchanged from run_001 (PROP-001, PROP-002, PROP-003).

**5. Directional impact estimate**
HIGH. FAQPage schema is the most direct technical bridge between a page's content and an AI conversational answer. Without it, bleisure travelers asking natural language hotel questions receive answers sourced from Booking.com and TripAdvisor (which carry FAQ-structured content), not from Radisson's brand pages.

**6. Priority tier**
P1

---

### PROP-004 — Rewrite Radisson Blu Meta Description and Opening Copy (GAP-009, GAP-010)

**1. Proposed change**
Rewrite the Radisson Blu brand page meta description and first 50–80 words of body copy to factual register:

**Current meta description (confirmed):** "We provide unparalleled service, comfort, and style while creating meaningful and memorable experiences."

**Proposed meta description (155 characters):** "Radisson Blu: 300+ upscale hotels across Europe, Africa & Asia. Meeting rooms, business centers & premium dining for business and leisure travelers."

**Proposed opening body copy:** "Radisson Blu operates more than 300 upper-upscale hotels across Europe, Africa, the Middle East, and Asia Pacific — making it the largest upper-upscale brand in Europe for over a decade. Properties feature full-service meeting and conference facilities, on-site restaurants, fitness centers, and flexible room configurations for business and extended stays. Radisson Blu is a flagship brand of Radisson Hotel Group, present in over 70 countries."

Brand voice ("Style, form, beauty and function. That's what you'll find at Radisson Blu.") should be retained as a secondary statement below the factual opening, not lead with it.

**2. Source citation**
C09 — Content Register; C03 — Meta Description Quality. Research: AI engines cite factual content at 62% higher rate than marketing copy (Search Engine Land 8,000-citation study). Factual meta descriptions are the primary text AI engines extract for entity identification and citation. Source: Lodging Magazine "From SEO to GEO"; asksuite.com "LLM-Ready Hotel Website Optimization."

**3. Current state**
Confirmed meta description: "We provide unparalleled service, comfort, and style…" — pure marketing register, zero extractable facts. UNCHANGED from run_001.

**4. Inferred implementation status**
Not implemented — unchanged from run_001 (PROP-007, PROP-008).

**5. Directional impact estimate**
HIGH. Zero technical effort required — pure copywriting change. Factual meta description and opening copy are the first text AI engines extract for citation. A bleisure traveler asking "Which hotel brand is best for business travel in Europe?" will receive a Radisson Blu citation only if the page carries extractable factual content.

**6. Priority tier**
P1

---

### PROP-005 — Rewrite Radisson (Brand) Page Title (GAP-015)

**1. Proposed change**
Rewrite the Radisson brand page title tag:

**Current:** "Radisson | Hotel Deals | Yes I Can! Attitude"

**Proposed:** "Radisson Hotels | Upscale Hotels in Europe, Americas & Asia Pacific"

Alternative: "Radisson Hotels | Upscale Hotel Brand | 100+ Countries"

Demote "Yes I Can!" tagline to an H2 brand statement in page body — not in the title tag. "Hotel Deals" should be removed from the primary title (if deals are promoted, use meta description or a dedicated /hotel-deals page title).

**2. Source citation**
C04 — Title Tag Optimization. Research: title tags are primary entity identification signals for AI systems; tagline-dominated titles are uninterpretable as entity descriptors; format best practice: [Brand Name] | [Entity type + key differentiator] | [Geography or audience signal]. Source: discoveredlabs.com Metadata Optimization for AI Search; dhihospitality.com 5-Step GEO Framework.

**3. Current state**
"Radisson | Hotel Deals | Yes I Can! Attitude" — tagline ("Yes I Can!") and promotional phrase ("Hotel Deals") dominate the title. No geographic scope. No entity type clarity. UNCHANGED from run_001.

**4. Inferred implementation status**
Not implemented — unchanged from run_001 (PROP-009).

**5. Directional impact estimate**
MEDIUM-HIGH. Title tag edit is a CMS change — zero technical effort. Query-parseable title immediately increases AI engine probability of correctly routing "Radisson hotels" entity queries to this page. The tagline in the title actively harms entity disambiguation for AI systems.

**6. Priority tier**
P1

---

### PROP-006 — Add Bleisure Content Layer to London (and Major European City) Pages (GAP-019, GAP-022)

**1. Proposed change**
Add a "For Business and Bleisure Travelers from the US" section to the London destination page and all major European city pages:

1. H2: "London Hotels for Business and Bleisure Travelers"
2. Opening paragraph (factual, 3–4 sentences): "Radisson operates [N] hotels across London's key business and leisure neighborhoods — including the City, Canary Wharf, Bloomsbury, and Heathrow. Properties offer meeting rooms (capacity: 10–700 guests), business centers, and high-speed WiFi. Heathrow is [X] minutes by direct rail; City Airport is [Y] minutes. Radisson Blu London Heathrow features 41 meeting rooms and 2,000+ sqm of flexible conference space."
3. Bullet list: meeting room capacity, WiFi speed, concierge services for US travelers, flexible check-in/check-out, leisure amenities (restaurants, spa, fitness)
4. FAQPage JSON-LD with questions: "Which London Radisson hotels are best for American business travelers?", "Do Radisson hotels in London have meeting rooms?", "Which Radisson London hotels are close to Heathrow?"

**2. Source citation**
C08 — Traveler Type Signals; C15 — Geographic Specificity; C05 — FAQ blocks. Research: 83% of business travelers take bleisure trips; American business travelers take 405M+ long-haul trips/year, ~60% add leisure time; bleisure-framed hotel pages receive significantly higher AI citation for combined business+leisure queries. Source: WISK Bleisure Travel Trends 2026; Engine.com 2026 Bleisure Travel Trends; hoteliers.guru AI Travel Planning Visibility Strategies.

**3. Current state**
London page title: "Beloved secret spots and best hotels in London" — tourism-first, no business traveler content. Confirmed body copy references Big Ben, Buckingham Palace — leisure tourist framing. No American traveler content confirmed. UNCHANGED from run_001.

**4. Inferred implementation status**
Not implemented — unchanged from run_001 (PROP-003, PROP-010, PROP-011).

**5. Directional impact estimate**
HIGH for target audience. Highest-impact content change for the primary audience. IHG and Hilton's London pages carry explicit "For Business Travelers" sections — Radisson is ceding bleisure discovery queries to competitors.

**6. Priority tier**
P1

---

### PROP-007 — Add Factual Content to Radisson Collection Brand Page (GAP-030, GAP-031)

**1. Proposed change**
Add a "2026 Portfolio Highlights" section to the Radisson Collection brand page featuring specific, citable facts:

- H2: "Radisson Collection: Landmark Properties in Europe's Most Storied Destinations"
- Banke Opéra Paris: "Opening Q3 2026 in a landmark 1907 Beaux-Arts bank headquarters near Galeries Lafayette and Opéra Garnier. Features a staircase designed by Gustave Eiffel, 90 redesigned rooms, and the original Belle Époque atrium."
- Palazzo San Gottardo Lake Como: "Opened Q1 2026 in a historic palazzo with 72 rooms and suites, panoramic Lake Como views, and restored 19th-century architecture."

Add FAQPage JSON-LD: "What makes Radisson Collection hotels different from other luxury hotel brands?", "Where are Radisson Collection hotels located in Europe?", "Which Radisson Collection hotels are opening in Europe in 2026?"

**2. Source citation**
C09 — Content Register; C05 — FAQ blocks. Research: brand pages surfacing property-level heritage facts appear in AI recommendations for "unique historic hotels" queries; press release content is lower-authority for AI citations than first-party brand page content. Source: ehotelier.com Radisson Collection Expansion 2026; Marriott Autograph Collection AI strategy analysis (klover.ai).

**3. Current state**
Radisson Collection brand page confirmed copy: "premium style collection of luxury hotels offering quality services, dining, wellness and much more" — generic luxury marketing copy. 2026 expansion facts (Paris, Lake Como) exist in press releases but not on brand page.

**4. Inferred implementation status**
N/A — page not audited in run_001.

**5. Directional impact estimate**
MEDIUM-HIGH. Luxury bleisure travelers and corporate executives using AI to research accommodation ask about specific properties and heritage narratives. Currently these queries route to press release pages and external media — not to Radisson's brand page. Factual content on the brand page captures these citations.

**6. Priority tier**
P2

---

### PROP-008 — Rewrite Meeting/Conference Page Title (GAP-032)

**1. Proposed change**
Rewrite the Meeting/Conference page title:

**Current:** "Book Your Meeting Rooms and Conferences Now | Radisson Hotels"

**Proposed:** "Meeting Rooms & Conference Venues | Radisson Hotels Europe & Worldwide"

Alternative: "Hotel Conference Facilities | Radisson Hotels | Business Meetings & Events"

The og:site_name "Radisson Meetings" is an appropriate sub-brand identity — retain this for social metadata but ensure the page title is query-parseable.

**2. Source citation**
C04 — Title Tag Optimization. Research: CTA-format titles ("Book...Now") are classified as ad-intent, not informational-intent by AI engines; query-answering titles match discovery queries from corporate travelers. Source: discoveredlabs.com; dhihospitality.com GEO Framework.

**3. Current state**
"Book Your Meeting Rooms and Conferences Now | Radisson Hotels" — imperative CTA, not query-matching descriptor.

**4. Inferred implementation status**
N/A — page not previously audited. This is a new proposal.

**5. Directional impact estimate**
MEDIUM. A query-parseable meeting page title allows AI engines to surface this page for corporate travel discovery queries. American executive asking "hotel chains with best conference facilities in Europe" will not receive this CTA-titled page in an AI recommendation.

**6. Priority tier**
P2

---

### PROP-009 — Add FAQ Content to Meeting/Conference Page (GAP-033)

**1. Proposed change**
Add a FAQ section to the Meeting/Conference main page with 5–6 questions:
- "Which Radisson hotels in Europe have the largest conference facilities?"
- "Does Radisson offer hybrid and video conferencing in its meeting rooms?"
- "What is the maximum capacity for a conference event at a Radisson hotel?"
- "Can I book meeting rooms at Radisson hotels for a single day without staying overnight?"
- "Does Radisson offer all-inclusive meeting packages with catering?"
- "Which Radisson hotels near London Heathrow have the best conference facilities for US corporate travelers?"

Each answer should contain specific facts (e.g., "Radisson Heathrow offers 41 meeting rooms with capacity up to 700 guests; Radisson Blu Heathrow offers 42 spaces accommodating up to 700 guests").

**2. Source citation**
C05 — FAQ/Q&A Content Blocks; C02 — FAQPage Schema. Research: meeting-planning queries are high-intent AI queries; FAQ content on meeting pages directly captures corporate travel discovery traffic.

**3. Current state**
No FAQ content detected in SERP for Meeting/Conference main page. Industry-specific sub-pages exist (/industry-solutions/finance, /industry-solutions/association-signature-events) but no discovery-oriented FAQ layer.

**4. Inferred implementation status**
N/A — page not previously audited.

**5. Directional impact estimate**
MEDIUM. American corporate travel planners and executive assistants increasingly use AI to identify meeting venues. FAQ content makes this page the citation source for meeting planning queries rather than ceding to MICE booking platforms and competitor sites.

**6. Priority tier**
P2

---

### PROP-010 — Deploy MeetingRoom/EventVenue Schema on Meeting/Conference Page (GAP-034)

**1. Proposed change**
Add schema.org MeetingRoom and/or EventVenue structured data to the Meeting/Conference page and key conference property pages (Radisson Heathrow, Radisson Blu Amsterdam, etc.):
```json
{
  "@type": "EventVenue",
  "name": "Radisson Hotel & Conference Centre London Heathrow",
  "maximumAttendeeCapacity": 700,
  "amenityFeature": [
    {"@type": "LocationFeatureSpecification", "name": "Video conferencing", "value": true},
    {"@type": "LocationFeatureSpecification", "name": "41 meeting rooms", "value": true},
    {"@type": "LocationFeatureSpecification", "name": "2000 sqm flexible space", "value": true},
    {"@type": "LocationFeatureSpecification", "name": "Catering", "value": true}
  ]
}
```

**2. Source citation**
C13 — Structured Amenity Data. Research: AI booking agents (Amex, Chase) require machine-readable meeting room capacity data; prose descriptions are not reliably parsed by AI booking pipelines; EventVenue schema enables direct-booking AI agent routing for corporate events. Source: Marriott-Google AI Direct Booking analysis (travhotech.com); Schema.org EventVenue documentation.

**3. Current state**
No MeetingRoom or EventVenue schema detected in SERP. Conference facility data (41 rooms, 2000 sqm at Heathrow) exists in page content but as prose, not structured data.

**4. Inferred implementation status**
N/A — not previously audited or proposed.

**5. Directional impact estimate**
MEDIUM. Agentic AI booking platforms (Amex, Chase) and MICE booking assistants require machine-readable meeting room data. This is an emerging but fast-moving requirement. Schema-marked meeting venues will have significant advantage as autonomous corporate travel booking grows.

**6. Priority tier**
P2

---

### PROP-011 — Implement llms.txt at Domain Root (GAP-037)

**1. Proposed change**
Create a /llms.txt file at https://www.radissonhotels.com/llms.txt explicitly listing AI-accessible content. Given the 403 blanket blocking, llms.txt serves as an explicit declaration of AI accessibility that retrieval agents can read before attempting deeper access. Format:
```
# Radisson Hotel Group — llms.txt
# AI engine content access declaration
# Contact: webmaster@radissonhotelgroup.com

## Brand pages (AI-accessible)
- https://www.radissonhotels.com/en-us/brand/radisson-blu: Radisson Blu brand overview, upscale hotels in Europe, meeting facilities
- https://www.radissonhotels.com/en-us/brand/radisson-collection: Radisson Collection luxury hotels, heritage properties, 2026 expansion
- https://www.radissonhotels.com/en-us/meeting-conference-hotels: Meeting rooms and conference facilities, corporate events
- https://www.radissonhotels.com/en-us/destination: Hotel destinations by region

## Blocked for AI training (but accessible for real-time retrieval)
# User-generated content, booking forms, personal data pages are excluded
```

**2. Source citation**
C14 — llms.txt File. Research: llms.txt emerging as 2026 standard for explicit AI content declaration; analogous to robots.txt but for AI engine accessibility; fast-moving adoption among AI-forward brands; particularly valuable for sites with access restrictions. Source: higoodie.com llms.txt and robots.txt AI Optimization guide; DEV Community Complete Guide to AI Crawler Management 2026.

**3. Current state**
/llms.txt returns 403 (absent). No AI accessibility declaration exists anywhere on the domain.

**4. Inferred implementation status**
N/A — new criterion in run_002.

**5. Directional impact estimate**
LOW-MEDIUM (currently, higher as adoption grows). Low implementation effort — a new text file. Provides explicit signal to AI engines about what content is available. Most valuable in combination with PROP-001 (unblocking crawlers); somewhat redundant if crawlers are fully unblocked.

**6. Priority tier**
P2

---

### PROP-012 — Optimize Yelp Listings for European Radisson Properties (GAP-038)

**1. Proposed change**
Audit and complete Yelp business listings for all major European Radisson properties:
1. Verify Yelp profiles exist for flagship European properties (London Bloomsbury, London Heathrow, Amsterdam, Brussels, Paris, Berlin, Rome, Madrid)
2. Complete all Yelp business fields: category, hours, amenities, photos, price range, website URL
3. Actively solicit reviews from US-based guests (Yelp is heavily used by American travelers and is now a data source in ChatGPT)
4. Respond to all Yelp reviews (signals active property management to AI data pipelines)

**2. Source citation**
C12 — OTA Listing Completeness. Research: Yelp integrated into ChatGPT January 2026 for hotel data; European Radisson properties likely have weak Yelp presence (Yelp is US-centric); GPT-5.2 doubled search depth — source breadth across 10+ platforms matters. Source: HotelRank.ai Anatomy of ChatGPT Hotel Search 2026.

**3. Current state**
Yelp listing completeness for European Radisson properties: UNVERIFIED. Likely weak — Yelp historically has limited European hotel coverage. Booking.com and TripAdvisor likely more complete.

**4. Inferred implementation status**
N/A — new criterion in run_002.

**5. Directional impact estimate**
LOW-MEDIUM. Yelp's European coverage is improving post-ChatGPT integration but remains primarily US city-focused. Berlin is confirmed in the ChatGPT-Yelp integration. Impact for European Radisson properties is limited currently but will grow. Priority for Radisson properties in US-heavy tourist/business cities (London, Paris, Amsterdam, Berlin).

**6. Priority tier**
P3

---

### PROP-013 — Add US-Origination Geographic Context to All Brand Pages (GAP-039)

**1. Proposed change**
Add explicit American traveler context to all brand pages (Radisson Blu, Collection, Park Plaza) and major city destination pages:
1. In opening body copy: include at least one reference to "American travelers," "US-to-Europe business trips," or "transatlantic travel"
2. On city pages: name the relevant US gateway airports and direct flight routes ("Direct flights from JFK and Newark to London Heathrow, approximately 7 hours")
3. In FAQPage JSON-LD: include at least one Q&A pair explicitly addressing American travelers ("Is Radisson Blu a good choice for American business travelers visiting Europe?")
4. On brand pages: include loyalty program information relevant to US travelers (Radisson Rewards partnership with airlines popular for transatlantic routes)

**2. Source citation**
C15 — Geographic Specificity (European Destinations + US Origination); C08 — Traveler Type Signals. Research: AI engines route queries based on explicit traveler-type entity matching; "hotels in Europe for American business travelers" requires both entities present on the page; American bleisure travelers take 405M+ long-haul trips/year. Source: WISK 2026 Bleisure Statistics; hospitalitymarketinginsight.com AI Search Reshaping Hospitality Buyer Journey.

**3. Current state**
No American traveler context confirmed in any audited title or meta description. "Worldwide" scope signals on homepage are too generic. Sub-pages in /en-us/ (US English version) are implicitly US-targeted but carry no explicit American traveler content signals.

**4. Inferred implementation status**
N/A — formalized as new criterion in run_002.

**5. Directional impact estimate**
MEDIUM. Explicit American traveler signals enable AI engines to match queries from the primary target audience. Without these signals, Radisson brand pages do not compete for "US traveler in Europe" query types even if they have the right properties.

**6. Priority tier**
P2

---

### PROP-014 — Promote Park Plaza Bleisure Signals to Title and Meta Description (GAP-026, GAP-027)

**1. Proposed change**
Park Plaza is the only Radisson brand with confirmed body copy using "business and leisure travelers" — this signal should be promoted from body copy to title and meta description:

**Current title:** "City Centre Hotels | Park Plaza Hotels & Resorts"
**Proposed title:** "Park Plaza Hotels | Business & Leisure in Europe's City Centres"

**Current meta description:** "Park Plaza Hotels & Resorts offer stylish guest rooms in city centre locations, meeting facilities and award-winning restaurants and bars."
**Proposed meta description:** "Park Plaza: upscale hotels for business and leisure travelers in European city centres. Meeting facilities, award-winning dining, and London locations near major business districts."

Also add specific European city names to meta description or schema: London, Amsterdam, Brussels, Rome.

**2. Source citation**
C04 — Title Tag Optimization; C08 — Traveler Type Signals; C03 — Meta Description. Research: Park Plaza confirmed "business and leisure travelers" in body copy — this is the portfolio's most natural bleisure alignment; promoting it to metadata makes it parseable by AI engines for bleisure query routing.

**3. Current state**
Title: "City Centre Hotels" — generic navigation category. Meta description: partially informational but bleisure signal in body only, not metadata. Run_002 formally confirmed both (was unassessable in run_001).

**4. Inferred implementation status**
N/A — page newly assessed in run_002.

**5. Directional impact estimate**
MEDIUM. Park Plaza has the most natural fit for bleisure positioning in the portfolio. Elevating its existing body copy signal into the title and meta is a quick, low-effort optimization with direct impact on AI routing for combined business-leisure queries.

**6. Priority tier**
P2

---

## Prioritized Summary

| Priority | Proposal | Effort | Gap ID(s) |
|----------|----------|--------|-----------|
| **P1** | PROP-001: Unblock AI retrieval crawlers (Cloudflare fix) | Low (1–2h config) | GAP-025, 036 |
| **P1** | PROP-002: Deploy Hotel/LodgingBusiness schema site-wide | Medium (dev sprint) | GAP-001, 023 |
| **P1** | PROP-003: Deploy FAQPage schema + visible FAQ blocks site-wide | Medium (content + dev) | GAP-002, 024 |
| **P1** | PROP-004: Rewrite Radisson Blu meta description + opening copy | Low (copywriting) | GAP-009, 010 |
| **P1** | PROP-005: Rewrite Radisson brand page title | Very low (CMS edit) | GAP-015 |
| **P1** | PROP-006: Add bleisure content layer to London page | Medium (content) | GAP-019, 022 |
| **P2** | PROP-007: Add factual content to Radisson Collection page | Low (content) | GAP-030, 031 |
| **P2** | PROP-008: Rewrite Meeting/Conference page title | Very low (CMS edit) | GAP-032 |
| **P2** | PROP-009: Add FAQ to Meeting/Conference page | Low (content) | GAP-033 |
| **P2** | PROP-010: Deploy EventVenue/MeetingRoom schema | Medium (dev) | GAP-034 |
| **P2** | PROP-011: Implement llms.txt | Very low (file creation) | GAP-037 |
| **P2** | PROP-013: Add US-origination context to brand pages | Low (content) | GAP-039 |
| **P2** | PROP-014: Promote Park Plaza bleisure signals to title/meta | Very low (CMS edit) | GAP-026, 027 |
| **P3** | PROP-012: Optimize Yelp listings for European properties | Low (OTA management) | GAP-038 |

**Implementation sequence recommendation:**
1. PROP-001 (unblock crawlers) — prerequisite for all else
2. PROP-004 + PROP-005 (copy rewrites, CMS edits) — zero dev effort, deploy in days
3. PROP-011 + PROP-014 (llms.txt + Park Plaza CMS edit) — very low effort
4. PROP-013 (US-origination copy) — low effort content additions
5. PROP-002 (Hotel/LodgingBusiness schema) — requires dev sprint
6. PROP-003 (FAQPage schema + content) — requires content + dev sprint
7. PROP-006 + PROP-007 (London bleisure + Collection factual content) — medium content effort
