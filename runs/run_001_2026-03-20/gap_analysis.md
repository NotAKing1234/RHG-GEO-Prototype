# Gap Analysis — run_001 | 2026-03-20

**Criteria source:** /framework/run_001_criteria.md
**Snapshot source:** /runs/run_001_2026-03-20/metadata_snapshot.md
**Pages audited:** 6 (5 Priority 1 + 1 Priority 2)
**Fetch limitation note:** All direct page fetches returned HTTP 403. Gaps derived from SERP metadata, search snippets, and secondary source analysis. Schema-level gaps (C01, C02, C05, C09, C10) are assessed as MISSING/UNCONFIRMED; they may be partially implemented on-page but are not surfacing in SERP rich results, which means AI engine citation value is negligible regardless.

---

## HOMEPAGE — https://www.radissonhotels.com/en-us

### GAP-001
**Gap ID:** GAP-001
**Page URL:** https://www.radissonhotels.com/en-us
**Criterion:** C01 — LodgingBusiness / Hotel Schema Presence
**Current metadata state:** No Hotel or LodgingBusiness schema detected in SERP rich results. No rich snippets (star ratings, check-in/out, amenityFeature) appear in Google search for this URL.
**Gap type:** MISSING
**Gap description:** The homepage shows no evidence of Hotel or LodgingBusiness JSON-LD schema appearing in search results. A brand homepage is a primary entity page; AI engines rely on schema to understand what Radisson is (hotel brand), where it operates, and what it offers. Without schema, AI engines must infer entity attributes from unstructured text, reducing confidence and citation probability.
**Severity:** 3 (Critical)
**New or recurring:** New (baseline run)

---

### GAP-002
**Gap ID:** GAP-002
**Page URL:** https://www.radissonhotels.com/en-us
**Criterion:** C02 — FAQPage Schema with Conversational Query Coverage
**Current metadata state:** No FAQPage schema detected in SERP. No FAQ rich snippets appear for this URL. No FAQ or Q&A section visible in search snippet text.
**Gap type:** MISSING
**Gap description:** The homepage has no FAQPage schema or visible FAQ content targeting bleisure traveler queries. This means the page cannot compete for AI citation in response to common traveler questions ("What kind of hotels does Radisson have in Europe?" / "Is Radisson good for business travelers?"). FAQ schema produces up to 3x citation advantage; absence represents a significant forfeited opportunity.
**Severity:** 3 (Critical)
**New or recurring:** New

---

### GAP-003
**Gap ID:** GAP-003
**Page URL:** https://www.radissonhotels.com/en-us
**Criterion:** C04 — Meta Description: Natural Language Answer Preview
**Current metadata state:** "Explore over 1100 hotels worldwide and book your stay with us today, with the best online rates guaranteed!"
**Gap type:** WEAK
**Gap description:** The meta description is written as a booking CTA with a discount incentive ("best online rates guaranteed"), not as an answer to a traveler discovery query. It provides no geographic context (no "Europe"), no traveler type, no amenity signal. AI engines parsing this description as an answer to "What is Radisson Hotels?" receive: scale (1100 hotels), booking incentive, worldwide scope. Missing: who these hotels serve, where the most relevant destinations are, what distinguishes Radisson for bleisure travelers.
**Severity:** 2 (Moderate)
**New or recurring:** New

---

### GAP-004
**Gap ID:** GAP-004
**Page URL:** https://www.radissonhotels.com/en-us
**Criterion:** C03 — Title Tag: Conversational Query Alignment
**Current metadata state:** "Radisson Hotels Official Site | Book Rooms Worldwide"
**Gap type:** WEAK
**Gap description:** Title is brand + transactional ("Book Rooms"), not brand + traveler-intent. "Book Rooms Worldwide" signals the page's purpose (booking) but not its relevance to any specific traveler query type. For AI engines matching "best European hotels for American business travelers," this title provides minimal query alignment. Missing: geographic specificity (Europe/global), traveler type (business/bleisure).
**Severity:** 2 (Moderate)
**New or recurring:** New

---

### GAP-005
**Gap ID:** GAP-005
**Page URL:** https://www.radissonhotels.com/en-us
**Criterion:** C08 — Natural Language Query Compatibility
**Current metadata state:** Confirmed content signals: "Explore over 1100 hotels worldwide"; brand name only. No body text passages visible that directly answer bleisure traveler queries.
**Gap type:** MISSING
**Gap description:** No content visible in confirmed metadata that answers compound bleisure queries. The homepage appears to be booking-interface-first rather than information-first. AI engines cannot extract a direct answer to "What does Radisson offer for American business travelers in Europe?" from the confirmed content. This makes the homepage a poor citation candidate for discovery-phase AI queries.
**Severity:** 3 (Critical)
**New or recurring:** New

---

### GAP-006
**Gap ID:** GAP-006
**Page URL:** https://www.radissonhotels.com/en-us
**Criterion:** C11 — Amenity Coverage: Bleisure-Specific Features
**Current metadata state:** No amenities confirmed in metadata or visible body text snippets.
**Gap type:** MISSING
**Gap description:** Confirmed homepage metadata contains no mention of specific amenities (business center, meeting rooms, WiFi, spa, gym, restaurant). AI engines cannot assess Radisson's amenity proposition from this page. For bleisure traveler queries requiring both business and leisure amenity confirmation, this page offers zero signal.
**Severity:** 3 (Critical)
**New or recurring:** New

---

## BRANDS PAGE — https://www.radissonhotels.com/en-us/brands

### GAP-007
**Gap ID:** GAP-007
**Page URL:** https://www.radissonhotels.com/en-us/brands
**Criterion:** C04 — Meta Description: Natural Language Answer Preview
**Current metadata state:** "Radisson Hotel Group provides a dynamic set of hotel brands for a wide range of travelers and budgets. We have 9 hotel brands, each of these with own identity."
**Gap type:** WEAK
**Gap description:** The meta description mentions "wide range of travelers and budgets" but gives no bleisure-relevant specificity. It does not explain which brand serves which traveler type (e.g., "Radisson Blu is our upscale brand for business travelers in Europe"). AI engines parsing this description receive: 9 brands exist, serve diverse travelers — but no actionable answer to "which Radisson brand is best for American business travelers in Europe?"
**Severity:** 2 (Moderate)
**New or recurring:** New

---

### GAP-008
**Gap ID:** GAP-008
**Page URL:** https://www.radissonhotels.com/en-us/brands
**Criterion:** C02 — FAQPage Schema with Conversational Query Coverage
**Current metadata state:** No FAQPage schema detected. No FAQ content visible in SERP.
**Gap type:** MISSING
**Gap description:** The brands overview page is the ideal location for FAQ schema answering common brand discovery questions: "What is Radisson Blu vs. Radisson Red?" / "Which Radisson brand has the most European hotels?" / "Which Radisson brand is best for business travel?" Absence of FAQ schema here forfeits a high-value opportunity for AI engine citation at the brand comparison stage of the traveler's decision journey.
**Severity:** 3 (Critical)
**New or recurring:** New

---

### GAP-009
**Gap ID:** GAP-009
**Page URL:** https://www.radissonhotels.com/en-us/brands
**Criterion:** C07 — Entity Signals: Brand + Location + Category Clarity
**Current metadata state:** Description mentions "Radisson Hotel Group" and "9 hotel brands" but no geographic scope or traveler type.
**Gap type:** WEAK
**Gap description:** The brands page fails to establish geographic entity context — no mention of Europe, European cities, or US→Europe travel corridor. AI engines building entity graphs for "Radisson brands in Europe" cannot confirm geographic scope from this page's confirmed metadata.
**Severity:** 2 (Moderate)
**New or recurring:** New

---

## RADISSON BLU BRAND PAGE — https://www.radissonhotels.com/en-us/brands/radisson-blu

### GAP-010
**Gap ID:** GAP-010
**Page URL:** https://www.radissonhotels.com/en-us/brands/radisson-blu
**Criterion:** C04 — Meta Description: Natural Language Answer Preview
**Current metadata state:** Confirmed copy: "We provide unparalleled service, comfort, and style while creating meaningful and memorable experiences. By paying close attention to the small details that make a big difference, we inspire unforgettable experiences with every stay."
**Gap type:** WEAK
**Gap description:** The Radisson Blu brand page description is entirely in marketing/brand voice register. It contains zero factual information that AI engines can cite as an answer to any traveler query. "Unparalleled service, comfort, and style" and "unforgettable experiences" are superlatives, not facts. An AI engine asked "What is Radisson Blu?" cannot cite this description as a useful answer. Competitors (Marriott, Hilton) whose pages contain factual brand descriptions (number of properties, locations, star rating, target traveler, amenities) will be preferred as citation sources.
**Severity:** 3 (Critical)
**New or recurring:** New

---

### GAP-011
**Gap ID:** GAP-011
**Page URL:** https://www.radissonhotels.com/en-us/brands/radisson-blu
**Criterion:** C02 — FAQPage Schema with Conversational Query Coverage
**Current metadata state:** No FAQPage schema detected. No FAQ content visible.
**Gap type:** MISSING
**Gap description:** The Radisson Blu brand page is the highest-value brand page in the Radisson portfolio for American bleisure travelers traveling to Europe. Radisson Blu is the flagship upscale brand with the strongest European presence. An FAQ section and schema answering questions like "Is Radisson Blu good for business travel?", "Where are Radisson Blu hotels in Europe?", "What amenities do Radisson Blu hotels offer?" would directly serve bleisure discovery queries. Absence is a critical missed opportunity.
**Severity:** 3 (Critical)
**New or recurring:** New

---

### GAP-012
**Gap ID:** GAP-012
**Page URL:** https://www.radissonhotels.com/en-us/brands/radisson-blu
**Criterion:** C08 — Natural Language Query Compatibility
**Current metadata state:** Confirmed copy is brand voice only ("unparalleled service," "unforgettable experiences"). No factual content answering traveler queries confirmed.
**Gap type:** MISSING
**Gap description:** The Radisson Blu brand page cannot answer the AI query "Why choose Radisson Blu for a European business trip?" with factual content. The confirmed metadata contains no: location count, European city coverage, business amenity confirmation, traveler type targeting, or comparison to competitive brands. This is the most important brand page for the bleisure audience, and it scores 0 on natural language query compatibility.
**Severity:** 3 (Critical)
**New or recurring:** New

---

### GAP-013
**Gap ID:** GAP-013
**Page URL:** https://www.radissonhotels.com/en-us/brands/radisson-blu
**Criterion:** C11 — Amenity Coverage: Bleisure-Specific Features
**Current metadata state:** No amenities mentioned in confirmed metadata.
**Gap type:** MISSING
**Gap description:** External industry sources confirm Radisson Blu as "business-meets-leisure guest mix" with "extensive meeting facilities" and "strong connectivity" — but these attributes are NOT reflected in the confirmed brand page metadata. The page does not communicate the bleisure amenity proposition. AI engines cannot confirm these attributes from the brand page.
**Severity:** 3 (Critical)
**New or recurring:** New

---

### GAP-014
**Gap ID:** GAP-014
**Page URL:** https://www.radissonhotels.com/en-us/brands/radisson-blu
**Criterion:** C12 — Geographic Entity Signals for European Destinations
**Current metadata state:** No geographic specificity in confirmed title or description.
**Gap type:** MISSING
**Gap description:** Title "Radisson Blu Hotels & Resorts | Radisson Hotels" contains no geographic entity. The description mentions no locations. Radisson Blu's primary competitive advantage is its European footprint, yet this is absent from confirmed page metadata. AI engines asked "Which hotel brand has the most European locations?" cannot cite this page as evidence for Radisson Blu.
**Severity:** 2 (Moderate)
**New or recurring:** New

---

## RADISSON BRAND PAGE — https://www.radissonhotels.com/en-us/brands/radisson

### GAP-015
**Gap ID:** GAP-015
**Page URL:** https://www.radissonhotels.com/en-us/brands/radisson
**Criterion:** C03 — Title Tag: Conversational Query Alignment
**Current metadata state:** "Radisson | Hotel Deals | Yes I Can! Attitude"
**Gap type:** MISALIGNED
**Gap description:** The title is tagline-dominated ("Yes I Can! Attitude") and transactional ("Hotel Deals"). Both signals are misaligned with AI engine query matching. A bleisure traveler asking "What is the Radisson brand?" receives a title that reads as a deals page with a brand slogan, not an information page about a hotel brand. "Hotel Deals" competes with OTA pages; "Yes I Can! Attitude" is brand-internal jargon that has zero query match value.
**Severity:** 2 (Moderate)
**New or recurring:** New

---

### GAP-016
**Gap ID:** GAP-016
**Page URL:** https://www.radissonhotels.com/en-us/brands/radisson
**Criterion:** C02 — FAQPage Schema with Conversational Query Coverage
**Current metadata state:** No FAQPage schema detected.
**Gap type:** MISSING
**Gap description:** No FAQ schema or content detected. Same structural gap as other brand pages.
**Severity:** 2 (Moderate)
**New or recurring:** New

---

## PARK PLAZA BRAND PAGE — https://www.radissonhotels.com/en-us/brands/park-plaza

### GAP-017
**Gap ID:** GAP-017
**Page URL:** https://www.radissonhotels.com/en-us/brands/park-plaza
**Criterion:** ALL criteria
**Current metadata state:** No metadata confirmed for this page in this run. Direct fetch returned 403; no SERP snippet found.
**Gap type:** MISSING (data unavailable)
**Gap description:** Page metadata could not be assessed this run due to 403 blocking and no search snippet found. Gaps assumed to parallel other brand pages (no FAQ schema, marketing-register description, no geographic entity). Priority: audit directly in next run using alternative access method.
**Severity:** 2 (Moderate, pending confirmation)
**New or recurring:** New (unconfirmed)

---

## LONDON HOTELS PAGE — https://www.radissonhotels.com/en-us/hotels/london

### GAP-018
**Gap ID:** GAP-018
**Page URL:** https://www.radissonhotels.com/en-us/hotels/london (inferred redirect: /en-us/destination/united-kingdom/london)
**Criterion:** C03 — Title Tag: Conversational Query Alignment
**Current metadata state:** "Beloved secret spots and best hotels in London | Radisson Hotels"
**Gap type:** MISALIGNED
**Gap description:** The London page title is tourism/leisure-first ("Beloved secret spots") when the primary American bleisure traveler need is business-amenity confirmation + location optimization. An American business traveler asking "Radisson hotels London for business travel" receives a title about "secret spots" — completely misaligned with the query. The page title should lead with what the traveler needs to know: hotel count, business facilities, London coverage. Competitors like Marriott's London page uses "Marriott Hotels in London, England | Marriott Bonvoy" — brand + city + booking platform, clean entity signal.
**Severity:** 3 (Critical)
**New or recurring:** New

---

### GAP-019
**Gap ID:** GAP-019
**Page URL:** https://www.radissonhotels.com/en-us/hotels/london
**Criterion:** C08 — Natural Language Query Compatibility
**Current metadata state:** Confirmed body copy focuses on Thames, landmarks (Big Ben, Buckingham Palace), tourism framing.
**Gap type:** MISALIGNED
**Gap description:** The confirmed body content positions London as a tourist destination with no explicit business travel content visible at the overview page level. A bleisure traveler asking "Radisson London hotels with business center and good location" cannot be answered from the overview page content. Individual property pages do mention business amenities, but the overview/discovery page — where AI engines make citation decisions — is tourism-framed.
**Severity:** 3 (Critical)
**New or recurring:** New

---

### GAP-020
**Gap ID:** GAP-020
**Page URL:** https://www.radissonhotels.com/en-us/hotels/london
**Criterion:** C02 — FAQPage Schema with Conversational Query Coverage
**Current metadata state:** No FAQPage schema detected. No FAQ visible in search snippets.
**Gap type:** MISSING
**Gap description:** London is the highest-value European city for US→Europe bleisure travel. The London overview page has no FAQ schema answering: "How many Radisson hotels are in London?", "Which Radisson London hotels are near the financial district?", "Do Radisson London hotels have business centers?", "What neighborhoods are Radisson London hotels in?" These are direct AI query types for this audience. Absence means Tripadvisor, Booking.com, and Marriott pages with FAQ schema will consistently outperform this page in AI citation selection for London-specific queries.
**Severity:** 3 (Critical)
**New or recurring:** New

---

### GAP-021
**Gap ID:** GAP-021
**Page URL:** https://www.radissonhotels.com/en-us/hotels/london
**Criterion:** C11 — Amenity Coverage: Bleisure-Specific Features
**Current metadata state:** Overview page body copy mentions tourist attractions; individual property descriptions mention event spaces and meeting rooms at specific properties.
**Gap type:** WEAK
**Gap description:** Bleisure amenity content exists at individual hotel property level (Canary Wharf, Heathrow, Euston mention meeting/conference facilities) but is absent at the overview/discovery page level. AI engines making citation decisions at the London overview page level cannot confirm bleisure amenity coverage. The compound query "London hotels with both conference facilities and great dining" cannot be answered from confirmed overview page content.
**Severity:** 2 (Moderate)
**New or recurring:** New

---

### GAP-022
**Gap ID:** GAP-022
**Page URL:** https://www.radissonhotels.com/en-us/hotels/london
**Criterion:** C07 — Entity Signals: Brand + Location + Category Clarity
**Current metadata state:** London mentioned in title (strong). Brand "Radisson Hotels" present. Individual neighborhoods/districts mentioned at property level.
**Gap type:** WEAK
**Gap description:** Geographic entity signal is partially present (London in title) but missing district-level granularity at the overview page level. American bleisure travelers navigate by reference points: Canary Wharf (financial), Heathrow (arrival), West End (leisure). The overview page should surface these district associations in its confirmed metadata rather than relying on individual property pages.
**Severity:** 2 (Moderate)
**New or recurring:** New

---

## Cross-Page System Gaps (Portfolio-Level)

### GAP-023
**Gap ID:** GAP-023
**Page URL:** ALL Priority 1 pages
**Criterion:** C01 — LodgingBusiness / Hotel Schema Presence
**Current metadata state:** Zero Hotel or LodgingBusiness schema rich results detected across all Priority 1 pages.
**Gap type:** MISSING
**Gap description:** No brand-level or overview-level Hotel/LodgingBusiness schema is surfacing in SERP. This is a portfolio-level absence. Individual property pages may implement schema, but brand-level and destination-level pages — which are the primary AI citation targets for broad discovery queries — appear to lack schema or implement it in ways that don't surface in rich results. This is the single largest structural gap in Radisson's AI discoverability posture.
**Severity:** 3 (Critical)
**New or recurring:** New

---

### GAP-024
**Gap ID:** GAP-024
**Page URL:** ALL audited pages
**Criterion:** C02 — FAQPage Schema with Conversational Query Coverage
**Current metadata state:** Zero FAQPage schema detected across any audited page.
**Gap type:** MISSING
**Gap description:** No FAQ schema present on any audited page. This is the single highest-ROI action documented in GEO literature (up to 3x citation advantage). The absence across all pages represents a systemic gap, not a page-specific omission. Priority 1 action for all pages.
**Severity:** 3 (Critical)
**New or recurring:** New

---

### GAP-025
**Gap ID:** GAP-025
**Page URL:** ALL audited pages
**Criterion:** C07 + C08 — Entity signals and natural language query compatibility
**Current metadata state:** Confirmed metadata across all pages uses marketing register rather than information register.
**Gap type:** WEAK
**Gap description:** A systemic register problem exists across the Radisson portfolio at brand/overview page level. Meta descriptions and visible copy consistently use brand voice ("unforgettable experiences," "Yes I Can!," "beloved secret spots") rather than informational register aligned with AI engine citation patterns. This is a content strategy gap, not just a technical gap. All page descriptions need to be rewritten in answer-first, factual register.
**Severity:** 2 (Moderate)
**New or recurring:** New

---

## Gap Summary Table

| Gap ID  | Page        | Criterion | Type        | Severity |
|---------|-------------|-----------|-------------|----------|
| GAP-001 | Homepage    | C01       | MISSING     | 3        |
| GAP-002 | Homepage    | C02       | MISSING     | 3        |
| GAP-003 | Homepage    | C04       | WEAK        | 2        |
| GAP-004 | Homepage    | C03       | WEAK        | 2        |
| GAP-005 | Homepage    | C08       | MISSING     | 3        |
| GAP-006 | Homepage    | C11       | MISSING     | 3        |
| GAP-007 | Brands      | C04       | WEAK        | 2        |
| GAP-008 | Brands      | C02       | MISSING     | 3        |
| GAP-009 | Brands      | C07       | WEAK        | 2        |
| GAP-010 | Radisson Blu | C04     | WEAK        | 3        |
| GAP-011 | Radisson Blu | C02     | MISSING     | 3        |
| GAP-012 | Radisson Blu | C08     | MISSING     | 3        |
| GAP-013 | Radisson Blu | C11     | MISSING     | 3        |
| GAP-014 | Radisson Blu | C12     | MISSING     | 2        |
| GAP-015 | Radisson    | C03       | MISALIGNED  | 2        |
| GAP-016 | Radisson    | C02       | MISSING     | 2        |
| GAP-017 | Park Plaza  | ALL       | MISSING     | 2        |
| GAP-018 | London      | C03       | MISALIGNED  | 3        |
| GAP-019 | London      | C08       | MISALIGNED  | 3        |
| GAP-020 | London      | C02       | MISSING     | 3        |
| GAP-021 | London      | C11       | WEAK        | 2        |
| GAP-022 | London      | C07       | WEAK        | 2        |
| GAP-023 | ALL (P1)    | C01       | MISSING     | 3        |
| GAP-024 | ALL         | C02       | MISSING     | 3        |
| GAP-025 | ALL         | C07+C08   | WEAK        | 2        |

**Total gaps identified:** 25
**MISSING:** 15 | **WEAK:** 8 | **MISALIGNED:** 3 | **Severity 3:** 14 | **Severity 2:** 11
**New gaps:** 25 | **Recurring:** 0 (baseline run)
