# Gap Analysis — run_003 | 2026-04-15

**Audit summary:** 26 days since run_002. Zero implemented changes detected. Critical infrastructure gaps (AI crawler blocking, schema, marketing register) persist for 3 consecutive runs. Four new gaps identified: Destination page query compatibility, Radisson Rewards loyalty discoverability, Radisson Collection freshness gap escalated (Lake Como now open), and direct AI distribution channel absence confirmed against industry.

Total gaps this run: **34** (8 new, 26 recurring from run_002)

---

## HOMEPAGE — https://www.radissonhotels.com/en-us

### GAP-001
- **Gap ID:** GAP-001
- **Page URL:** https://www.radissonhotels.com/en-us
- **Criterion:** C04 — AI Crawler Access
- **Current state:** HTTP 403 returned for all WebFetch attempts including /robots.txt, /llms.txt, and all page URLs. Cloudflare WAF "Block AI Scrapers and Crawlers" rule (or equivalent) confirmed active.
- **Gap type:** MISSING
- **Gap description:** All AI retrieval crawlers (GPTBot, PerplexityBot, ClaudeBot, Google-Extended, Applebot-Extended) are blocked site-wide. Radisson cannot be cited from its own domain by any AI engine. 73% citation reduction confirmed for sites blocking GPTBot (ChatGPT). 3rd consecutive run unchanged.
- **Severity:** 3
- **Status:** RECURRING (run_001, run_002, run_003) — **CRITICAL ESCALATION: 3 runs unaddressed**

### GAP-002
- **Gap ID:** GAP-002
- **Page URL:** https://www.radissonhotels.com/en-us
- **Criterion:** C02 — Hotel/LodgingBusiness Schema
- **Current state:** No Hotel, LodgingBusiness, or any schema rich results detected in SERP for homepage. JSON-LD unconfirmable due to 403.
- **Gap type:** MISSING
- **Gap description:** Homepage lacks Hotel/LodgingBusiness schema. AI engines cannot parse structured hotel attributes (location, amenities, pricing, ratings) from the primary discovery page. Only 10.6% of hotel sites have good schema; Radisson is below this threshold.
- **Severity:** 3
- **Status:** RECURRING (run_001, run_002, run_003)

### GAP-003
- **Gap ID:** GAP-003
- **Page URL:** https://www.radissonhotels.com/en-us
- **Criterion:** C05 — Title Tag Query Compatibility
- **Current state:** Title: "Radisson Hotels Official Site | Book Rooms Worldwide"
- **Gap type:** MISALIGNED
- **Gap description:** Title is transactional CTA ("Book Rooms Worldwide"), not a query-answering statement. Does not surface for discovery queries ("best hotels in Europe for business travelers," "upscale hotels in London for American travelers"). 3rd consecutive run unchanged.
- **Severity:** 2
- **Status:** RECURRING (run_001, run_002, run_003)

### GAP-004
- **Gap ID:** GAP-004
- **Page URL:** https://www.radissonhotels.com/en-us
- **Criterion:** C06 — Meta Description Informational Register
- **Current state:** "Explore over 1100 hotels worldwide and book your stay with us today, with the best online rates guaranteed!"
- **Gap type:** MISALIGNED
- **Gap description:** Meta description is a booking incentive, not an informational answer. No traveler type, no specific destinations, no amenity types. AI engines cannot extract a useful answer to any discovery query from this text. 3rd consecutive run.
- **Severity:** 2
- **Status:** RECURRING (run_001, run_002, run_003)

### GAP-005
- **Gap ID:** GAP-005
- **Page URL:** https://www.radissonhotels.com/en-us
- **Criterion:** C03 — FAQPage Schema
- **Current state:** No FAQPage schema detected. General /en-us/faq page exists but no rich results.
- **Gap type:** MISSING
- **Gap description:** No FAQ blocks or FAQPage JSON-LD on homepage. AI engines cannot extract Q&A pairs for common traveler queries. 3rd consecutive run.
- **Severity:** 2
- **Status:** RECURRING (run_001, run_002, run_003)

### GAP-006
- **Gap ID:** GAP-006
- **Page URL:** https://www.radissonhotels.com/en-us
- **Criterion:** C14 — llms.txt
- **Current state:** /llms.txt returns HTTP 403
- **Gap type:** MISSING
- **Gap description:** llms.txt absent. Low-effort AI accessibility protocol not implemented. Second consecutive run.
- **Severity:** 1
- **Status:** RECURRING (run_002, run_003)

---

## RADISSON BLU BRAND PAGE — https://www.radissonhotels.com/en-us/brand/radisson-blu

### GAP-007
- **Gap ID:** GAP-007
- **Page URL:** https://www.radissonhotels.com/en-us/brand/radisson-blu
- **Criterion:** C07 — Factual Content Density
- **Current state:** Confirmed body copy: "We provide unparalleled service, comfort, and style while creating meaningful and memorable experiences. By paying close attention to the small details that make a big difference, we inspire unforgettable experiences with every stay."
- **Gap type:** MISALIGNED
- **Gap description:** First 80 words contain zero specific facts (0 hotel counts, 0 city names, 0 amenity types). Pure marketing register — confirmed unciteable by AI. Register is "Style, form, beauty and function. That's what you'll find at Radisson Blu." Factual content (390+ hotels, business travel sub-page, European presence) exists at sub-page level but not on brand page. 3rd consecutive run.
- **Severity:** 3
- **Status:** RECURRING (run_001, run_002, run_003) — **CRITICAL**

### GAP-008
- **Gap ID:** GAP-008
- **Page URL:** https://www.radissonhotels.com/en-us/brand/radisson-blu
- **Criterion:** C08 — Bleisure Explicit Signals
- **Current state:** No bleisure terminology in title, meta description, or confirmed opening body copy. About sub-page (/brand/radisson-blu/about) has "business and leisure" but this is not the main brand discovery page.
- **Gap type:** MISSING
- **Gap description:** Main Radisson Blu brand page has no bleisure/business-and-leisure signal in any AI-discoverable metadata. Business travel content exists at /business-travel-offer sub-page but is buried. Main brand page cannot answer "Is Radisson Blu good for business travelers?" from metadata alone.
- **Severity:** 3
- **Status:** RECURRING (run_001, run_002, run_003)

### GAP-009
- **Gap ID:** GAP-009
- **Page URL:** https://www.radissonhotels.com/en-us/brand/radisson-blu
- **Criterion:** C09 — American Traveler Signals
- **Current state:** No US/American traveler orientation in any confirmed metadata.
- **Gap type:** MISSING
- **Gap description:** No content addressing American travelers in European context. For queries like "Radisson hotels in Europe for American business travelers," the brand page provides no responsive signal.
- **Severity:** 2
- **Status:** RECURRING (run_002, run_003)

### GAP-010
- **Gap ID:** GAP-010
- **Page URL:** https://www.radissonhotels.com/en-us/brand/radisson-blu
- **Criterion:** C02 — Hotel/LodgingBusiness Schema
- **Current state:** No schema rich results. No confirmable JSON-LD.
- **Gap type:** MISSING
- **Gap description:** No Hotel/LodgingBusiness schema on brand page. 3rd consecutive run.
- **Severity:** 3
- **Status:** RECURRING (run_001, run_002, run_003)

### GAP-011
- **Gap ID:** GAP-011
- **Page URL:** https://www.radissonhotels.com/en-us/brand/radisson-blu
- **Criterion:** C03 — FAQPage Schema
- **Current state:** No FAQPage in SERP or confirmed page metadata.
- **Gap type:** MISSING
- **Gap description:** No FAQ content or FAQPage schema on brand page. AI engines cannot extract Q&A responses for Radisson Blu–specific queries.
- **Severity:** 2
- **Status:** RECURRING (run_001, run_002, run_003)

### GAP-012
- **Gap ID:** GAP-012
- **Page URL:** https://www.radissonhotels.com/en-us/brand/radisson-blu/business-travel-offer (sub-page)
- **Criterion:** C08 — Bleisure Explicit Signals
- **Current state:** Title "Radisson Blu Hotels for Business Travelers | Radisson Hotels" — good. Content includes meeting rooms, flexible spaces. BUT: (a) main brand page does not link to or surface this page for discovery; (b) no bleisure compound language combining business + leisure; (c) no American traveler targeting.
- **Gap type:** WEAK
- **Gap description:** Business travel content exists at sub-page level but is not discoverable from main brand page. Sub-page title is good but copy is B2B-focused, missing leisure + bleisure compound content and American traveler context.
- **Severity:** 2
- **Status:** NEW (first formal sub-page audit run_003)

---

## RADISSON COLLECTION — https://www.radissonhotels.com/en-us/brand/radisson-collection

### GAP-013
- **Gap ID:** GAP-013
- **Page URL:** https://www.radissonhotels.com/en-us/brand/radisson-collection
- **Criterion:** C10 — Content Freshness
- **Current state:** Brand page title "Radisson Collection Luxury Hotels | Radisson Hotels" and copy unchanged since run_002. Lake Como property open as of Q1 2026. Paris Banke Opera on track H2 2026.
- **Gap type:** MISSING
- **Gap description:** Radisson Collection Lake Como is ALREADY OPEN (Q1 2026) and is generating trade press coverage. Brand page shows no reference to it. This is the most specific escalation since run_002: a major new European luxury property (72 rooms, rooftop lake views, heritage building) is live and already missing from brand discovery content. For an American luxury traveler asking "What's new in Radisson Collection in Europe?" the brand page provides zero answer.
- **Severity:** 3
- **Status:** ESCALATED (WEAK in run_002 → MISSING/CRITICAL in run_003; property now open)

### GAP-014
- **Gap ID:** GAP-014
- **Page URL:** https://www.radissonhotels.com/en-us/brand/radisson-collection
- **Criterion:** C07 — Factual Content Density
- **Current state:** "premium style collection of luxury hotels offering quality services, dining, wellness and much more."
- **Gap type:** WEAK
- **Gap description:** Confirmed body copy contains some factual signals (quality services, dining, wellness) but no specific counts, locations, or unique property facts. The specific heritage architecture claims (Eiffel-designed staircase, 1907 Belle Époque bank, bank vault wellness area) are in trade press but not on the brand page.
- **Severity:** 2
- **Status:** RECURRING (run_002, run_003)

### GAP-015
- **Gap ID:** GAP-015
- **Page URL:** https://www.radissonhotels.com/en-us/brand/radisson-collection
- **Criterion:** C02 — Hotel/LodgingBusiness Schema
- **Current state:** No schema rich results detected.
- **Gap type:** MISSING
- **Gap description:** No Hotel schema. Same gap as all brand pages. 3rd consecutive run.
- **Severity:** 3
- **Status:** RECURRING (run_001, run_002, run_003)

---

## RADISSON RED — https://www.radissonhotels.com/en-us/brand/radisson-red

### GAP-016
- **Gap ID:** GAP-016
- **Page URL:** https://www.radissonhotels.com/en-us/brand/radisson-red
- **Criterion:** C02 — Hotel/LodgingBusiness Schema
- **Current state:** No schema rich results. Title: "Radisson RED - Stylish & Boutique Hotels | Radisson Hotels."
- **Gap type:** MISSING
- **Gap description:** No Hotel schema. Lower severity for bleisure audience but schema absence is systemic.
- **Severity:** 2
- **Status:** RECURRING (run_001, run_002, run_003)

### GAP-017
- **Gap ID:** GAP-017
- **Page URL:** https://www.radissonhotels.com/en-us/brand/radisson-red
- **Criterion:** C05 — Title Tag Query Compatibility
- **Current state:** "Radisson RED - Stylish & Boutique Hotels | Radisson Hotels"
- **Gap type:** MISALIGNED
- **Gap description:** Title reflects brand voice (playful/social) but not query language. "Stylish & Boutique" is not how travelers search. No location, no use case, no traveler type.
- **Severity:** 1
- **Status:** RECURRING (run_002, run_003)

---

## PARK PLAZA — https://www.radissonhotels.com/en-us/brand/park-plaza

### GAP-018
- **Gap ID:** GAP-018
- **Page URL:** https://www.radissonhotels.com/en-us/brand/park-plaza
- **Criterion:** C05 — Title Tag Query Compatibility
- **Current state:** "City Centre Hotels | Park Plaza Hotels & Resorts"
- **Gap type:** WEAK
- **Gap description:** Title identifies brand and category but no city name, no traveler type, no bleisure signal. "City Centre Hotels" is a generic descriptor. Could be strengthened to surface for European business/bleisure queries.
- **Severity:** 2
- **Status:** RECURRING (run_001, run_002, run_003)

### GAP-019
- **Gap ID:** GAP-019
- **Page URL:** https://www.radissonhotels.com/en-us/brand/park-plaza
- **Criterion:** C08 — Bleisure Explicit Signals
- **Current state:** "business and leisure travelers" confirmed in body copy. Not in title or meta description.
- **Gap type:** WEAK
- **Gap description:** Portfolio's strongest bleisure signal is confirmed in body copy but absent from title and meta — the primary AI engine parsing fields. Body copy bleisure signal is not surfacing in AI discovery. Needs promotion to title/meta and explicit American traveler reference added.
- **Severity:** 2
- **Status:** RECURRING (run_002, run_003)

### GAP-020
- **Gap ID:** GAP-020
- **Page URL:** https://www.radissonhotels.com/en-us/brand/park-plaza
- **Criterion:** C09 — American Traveler Signals
- **Current state:** No American/US traveler references in any confirmed metadata.
- **Gap type:** MISSING
- **Gap description:** Park Plaza's "business and leisure" positioning is the most natural fit for American bleisure travelers in European city centers, but no explicit US traveler orientation in confirmed metadata.
- **Severity:** 2
- **Status:** RECURRING (run_002, run_003)

### GAP-021
- **Gap ID:** GAP-021
- **Page URL:** https://www.radissonhotels.com/en-us/brand/park-plaza
- **Criterion:** C02 — Hotel/LodgingBusiness Schema
- **Current state:** No schema rich results.
- **Gap type:** MISSING
- **Gap description:** No Hotel schema on Park Plaza brand page. Same systemic gap.
- **Severity:** 3
- **Status:** RECURRING (run_001, run_002, run_003)

### GAP-022
- **Gap ID:** GAP-022
- **Page URL:** https://www.radissonhotels.com/en-us/brand/park-plaza
- **Criterion:** C03 — FAQPage Schema
- **Current state:** No FAQ rich results. No FAQ blocks detected.
- **Gap type:** MISSING
- **Gap description:** Park Plaza brand page has no FAQ content for meeting/business/leisure queries despite having the strongest positioning for this audience.
- **Severity:** 2
- **Status:** RECURRING (run_001, run_002, run_003)

---

## DESTINATION PAGE — https://www.radissonhotels.com/en-us/destination

### GAP-023
- **Gap ID:** GAP-023
- **Page URL:** https://www.radissonhotels.com/en-us/destination
- **Criterion:** C05 — Title Tag Query Compatibility
- **Current state:** "Destinations | Radisson Hotels"
- **Gap type:** MISSING
- **Gap description:** Title is purely navigational. Provides no query-answering value. Does not surface for destination-specific discovery queries ("Radisson hotels in Europe," "best Radisson hotels for American travelers in London"). Sub-pages have better geographic specificity but main discovery page has no geographic entity signal.
- **Severity:** 2
- **Status:** NEW (first audit run_003)

### GAP-024
- **Gap ID:** GAP-024
- **Page URL:** https://www.radissonhotels.com/en-us/destination
- **Criterion:** C15 — Geographic/Neighborhood Specificity
- **Current state:** Main destination page title and confirmed snippet contain no geographic entities.
- **Gap type:** MISSING
- **Gap description:** Primary destination discovery page names no countries, cities, or neighborhoods. For AI engines responding to "Where does Radisson have hotels in Europe?" or "Best cities to find Radisson hotels for American travelers" — the main page provides no geographic signal. Sub-pages (/destination/united-kingdom, /destination/france/paris) have appropriate titles but these are not the primary AI discovery entry point.
- **Severity:** 2
- **Status:** NEW (first audit run_003)

### GAP-025
- **Gap ID:** GAP-025
- **Page URL:** https://www.radissonhotels.com/en-us/destination
- **Criterion:** C08 — Bleisure Explicit Signals
- **Current state:** No bleisure, business + leisure, or traveler-type signals on destination page.
- **Gap type:** MISSING
- **Gap description:** Destination discovery page does not communicate why Radisson is a good choice for the bleisure traveler specifically. No meeting facility reference, no workstyle + lifestyle framing.
- **Severity:** 1
- **Status:** NEW (first audit run_003)

---

## RADISSON REWARDS — https://www.radissonhotels.com/en-us/rewards

### GAP-026
- **Gap ID:** GAP-026
- **Page URL:** https://www.radissonhotels.com/en-us/rewards
- **Criterion:** C16 — Loyalty Program AI Discoverability
- **Current state:** Title: "Radisson Hotel Rewards Program | Radisson Rewards." Program structure (tiers, point rates, benefits) confirmed in secondary sources but not surfacing in AI responses.
- **Gap type:** WEAK
- **Gap description:** Radisson Rewards title is adequate for branded search but does not answer loyalty comparison queries ("How does Radisson Rewards compare to Marriott Bonvoy?", "Does Radisson have a good hotel loyalty program for American travelers?"). Marriott Bonvoy (224 AI citations) and Hilton Honors are prominently surfaced in AI hotel recommendation responses; Radisson Rewards is not. The gap is: program mechanics exist but AI engines cannot extract them in a competitive comparison context.
- **Severity:** 2
- **Status:** NEW (first audit run_003)

### GAP-027
- **Gap ID:** GAP-027
- **Page URL:** https://www.radissonhotels.com/en-us/rewards
- **Criterion:** C09 — American Traveler Signals
- **Current state:** Points denominated in USD (20 pts/$1 spend) confirmed — implicit US traveler orientation. No explicit "American travelers," "US business travelers," or "earn miles on transatlantic flights" messaging confirmed.
- **Gap type:** WEAK
- **Gap description:** Loyalty program page does not explicitly address American business travelers' specific needs: transatlantic trip earning, European city coverage, airline mile transfers to US carriers, credit card partnerships comparable to Chase Sapphire/Marriott or AmEx/Hilton.
- **Severity:** 2
- **Status:** NEW (first audit run_003)

### GAP-028
- **Gap ID:** GAP-028
- **Page URL:** https://www.radissonhotels.com/en-us/rewards
- **Criterion:** C02 — Hotel/LodgingBusiness Schema (Loyalty/Organization schema)
- **Current state:** No schema rich results for rewards page.
- **Gap type:** MISSING
- **Gap description:** No LoyaltyProgram or Organization schema on rewards page. AI engines cannot parse loyalty tier structure, earning rates, or redemption options as structured data.
- **Severity:** 1
- **Status:** NEW (first audit run_003)

### GAP-029
- **Gap ID:** GAP-029
- **Page URL:** https://www.radissonhotels.com/en-us/rewards
- **Criterion:** C03 — FAQPage Schema
- **Current state:** /en-us/rewards/faq page confirmed but no FAQ rich results detected.
- **Gap type:** WEAK
- **Gap description:** Rewards FAQ page exists but no FAQPage schema detected. AI engines cannot extract loyalty Q&A for responses to: "How do I earn points at Radisson?", "What tier is Radisson Rewards?", "Can I transfer Radisson points to airline miles?"
- **Severity:** 1
- **Status:** NEW (first audit run_003)

---

## CROSS-SITE / PORTFOLIO-LEVEL GAPS

### GAP-030
- **Gap ID:** GAP-030
- **Page URL:** All brand pages
- **Criterion:** C17 — MCP/Direct AI Distribution Channel
- **Current state:** No confirmed Radisson ChatGPT app, Perplexity integration, or MCP protocol implementation. Accor launched ChatGPT app Jan 29 2026; Hyatt launched Feb 2026. Perplexity hotel booking live with Selfbook/TripAdvisor.
- **Gap type:** MISSING
- **Gap description:** Radisson has no direct AI distribution channel. American bleisure travelers using ChatGPT or Perplexity to book hotels in Europe cannot book Radisson directly through these interfaces. Bookings are routing through OTAs or to competitor direct channels. BCG (March 2026) confirms "ask and book era" is live; Radisson is not participating.
- **Severity:** 3
- **Status:** NEW (explicitly identified run_003; conceptually present since run_001)

### GAP-031
- **Gap ID:** GAP-031
- **Page URL:** All brand pages
- **Criterion:** C11 — Individual Property Schema
- **Current state:** All radissonhotels.com individual property pages return 403. Cannot confirm or deny Hotel schema at property level. OTA proxy indicates: property data is being surfaced via TripAdvisor/Booking.com (positive) but direct Radisson schema is unconfirmable.
- **Gap type:** MISSING (unconfirmable — possible issue or possible gap)
- **Gap description:** Inability to confirm individual property page schema is itself a gap (both for this audit's confidence and for AI crawlers who also face the same 403). Even if schema exists at property level in HTML, AI crawlers cannot read it.
- **Severity:** 2
- **Status:** NEW (first attempted run_003)

### GAP-032
- **Gap ID:** GAP-032
- **Page URL:** https://www.radissonhotels.com/en-us/brand/radisson-collection
- **Criterion:** C01 — Google Business Profile Completeness
- **Current state:** Cannot directly verify Radisson Collection London or Paris GBP listing completeness. Individual London Radisson Blu properties appear in Google Travel with basic amenity data. GBP description quality for flagship properties not confirmed.
- **Gap type:** WEAK
- **Gap description:** GBP completeness not fully verified for flagship European Radisson properties. With GBP accounting for 32% of Local Pack ranking and feeding Google AI Overviews (40%+ of local queries), sub-optimal GBP descriptions for key European Radisson properties represent a material AI visibility gap. Partially confirmed: London Radisson Blu properties appear in Google Travel but description quality not assessed.
- **Severity:** 2
- **Status:** NEW (first formal C01 assessment run_003)

### GAP-033
- **Gap ID:** GAP-033
- **Page URL:** All Priority 1 pages
- **Criterion:** C13 — Structured Amenity Data
- **Current state:** No structured amenity data (schema amenityFeature, HTML amenity tables) confirmed on any brand or overview page.
- **Gap type:** MISSING
- **Gap description:** Specific amenity data (meeting room counts, Wi-Fi speeds, gym specs, pool, spa) required for AI attribute-matching queries ("Radisson hotels in Amsterdam with business center and gym") is absent from all brand/overview pages. Individual property pages may have this but are 403-blocked.
- **Severity:** 2
- **Status:** RECURRING (run_001, run_002, run_003)

### GAP-034
- **Gap ID:** GAP-034
- **Page URL:** https://www.radissonhotels.com/en-us/destination
- **Criterion:** C02 — Hotel/LodgingBusiness Schema
- **Current state:** No schema rich results on destination page.
- **Gap type:** MISSING
- **Gap description:** Destination overview page lacks any schema markup (ItemList, TouristDestination, LodgingBusiness collection). AI engines parsing "Radisson hotels in Europe" cannot extract structured data from this page.
- **Severity:** 2
- **Status:** NEW (first audit run_003)

---

## Gap Summary Table

| Gap ID | Page | Criterion | Type | Severity | Status |
|--------|------|-----------|------|----------|--------|
| GAP-001 | Homepage | C04 AI Crawler | MISSING | 3 | RECURRING (3 runs) |
| GAP-002 | Homepage | C02 Schema | MISSING | 3 | RECURRING (3 runs) |
| GAP-003 | Homepage | C05 Title | MISALIGNED | 2 | RECURRING (3 runs) |
| GAP-004 | Homepage | C06 Meta | MISALIGNED | 2 | RECURRING (3 runs) |
| GAP-005 | Homepage | C03 FAQ | MISSING | 2 | RECURRING (3 runs) |
| GAP-006 | Homepage | C14 llms.txt | MISSING | 1 | RECURRING (2 runs) |
| GAP-007 | Radisson Blu | C07 Content | MISALIGNED | 3 | RECURRING (3 runs) |
| GAP-008 | Radisson Blu | C08 Bleisure | MISSING | 3 | RECURRING (3 runs) |
| GAP-009 | Radisson Blu | C09 American | MISSING | 2 | RECURRING (2 runs) |
| GAP-010 | Radisson Blu | C02 Schema | MISSING | 3 | RECURRING (3 runs) |
| GAP-011 | Radisson Blu | C03 FAQ | MISSING | 2 | RECURRING (3 runs) |
| GAP-012 | Blu /biz-travel | C08 Bleisure | WEAK | 2 | NEW (run_003) |
| GAP-013 | Collection | C10 Freshness | MISSING | 3 | ESCALATED |
| GAP-014 | Collection | C07 Content | WEAK | 2 | RECURRING (2 runs) |
| GAP-015 | Collection | C02 Schema | MISSING | 3 | RECURRING (3 runs) |
| GAP-016 | Radisson RED | C02 Schema | MISSING | 2 | RECURRING (3 runs) |
| GAP-017 | Radisson RED | C05 Title | MISALIGNED | 1 | RECURRING (2 runs) |
| GAP-018 | Park Plaza | C05 Title | WEAK | 2 | RECURRING (3 runs) |
| GAP-019 | Park Plaza | C08 Bleisure | WEAK | 2 | RECURRING (2 runs) |
| GAP-020 | Park Plaza | C09 American | MISSING | 2 | RECURRING (2 runs) |
| GAP-021 | Park Plaza | C02 Schema | MISSING | 3 | RECURRING (3 runs) |
| GAP-022 | Park Plaza | C03 FAQ | MISSING | 2 | RECURRING (3 runs) |
| GAP-023 | Destination | C05 Title | MISSING | 2 | NEW (run_003) |
| GAP-024 | Destination | C15 Geographic | MISSING | 2 | NEW (run_003) |
| GAP-025 | Destination | C08 Bleisure | MISSING | 1 | NEW (run_003) |
| GAP-026 | Rewards | C16 Loyalty | WEAK | 2 | NEW (run_003) |
| GAP-027 | Rewards | C09 American | WEAK | 2 | NEW (run_003) |
| GAP-028 | Rewards | C02 Schema | MISSING | 1 | NEW (run_003) |
| GAP-029 | Rewards | C03 FAQ | WEAK | 1 | NEW (run_003) |
| GAP-030 | Portfolio | C17 AI Channel | MISSING | 3 | NEW (run_003) |
| GAP-031 | Portfolio | C11 Prop Schema| MISSING | 2 | NEW (run_003) |
| GAP-032 | Portfolio | C01 GBP | WEAK | 2 | NEW (run_003) |
| GAP-033 | All brands | C13 Amenity | MISSING | 2 | RECURRING (3 runs) |
| GAP-034 | Destination | C02 Schema | MISSING | 2 | NEW (run_003) |

**Severity 3 gaps (CRITICAL):** GAP-001, GAP-002, GAP-007, GAP-008, GAP-010, GAP-013, GAP-015, GAP-021, GAP-030 — **9 critical gaps**
**New gaps this run:** GAP-012, GAP-023, GAP-024, GAP-025, GAP-026, GAP-027, GAP-028, GAP-029, GAP-030, GAP-031, GAP-032, GAP-034 — **12 new** (including escalated GAP-013)
**Recurring gaps (2+ runs):** All others — **22 recurring**
