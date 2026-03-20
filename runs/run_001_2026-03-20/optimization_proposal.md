# Optimization Proposal — run_001 | 2026-03-20

**Sources synthesized from:**
- `/framework/run_001_criteria.md`
- `/runs/run_001_2026-03-20/gap_research.md`
- Context brief: N/A (first run, no prior implementation history)

---

## Executive Summary

This run identified **25 gaps** across 6 audited pages (5 Priority 1 + London, Priority 2). All 25 gaps are **new** — this is the baseline run with no prior implementation history. The audit was conducted via SERP metadata analysis after radissonhotels.com returned HTTP 403 for all direct fetches; structured data, OG tags, heading structure, and FAQ presence are assessed as absent from rich results and SERP signals.

**Top 3 Priority Changes:**

1. **Deploy FAQPage JSON-LD site-wide** (all brand pages + homepage + London overview) — the single highest-ROI action documented across 2025–2026 GEO literature, with up to 3.2x AI Overview citation multiplier; requires no design changes and is implementable in days.
2. **Rewrite Radisson Blu brand page content from marketing register to factual register** — Radisson Blu is the flagship European brand for the bleisure audience; its confirmed copy ("unparalleled service," "unforgettable experiences") is completely uncitable by AI engines. A 200-word factual rewrite is the fastest content-only fix available.
3. **Deploy Hotel/LodgingBusiness JSON-LD schema across all brand and overview pages** — the structural prerequisite for AI engine entity recognition; currently absent across the entire audited portfolio.

---

## Proposal Entries

---

### PROP-001 — FAQPage Schema: Radisson Blu Brand Page (GAP-011 + GAP-024)

**1. Proposed change**
Add a visible "Radisson Blu: Frequently Asked Questions" section to the Radisson Blu brand page with 5 question-answer pairs, each answer 50–80 words in factual language. Wrap the entire block in FAQPage JSON-LD in the page `<head>`. Suggested questions:
- "What kind of hotels are Radisson Blu?"
- "Where are Radisson Blu hotels located in Europe?"
- "What business facilities do Radisson Blu hotels offer?"
- "What leisure amenities are available at Radisson Blu?"
- "Is Radisson Blu suitable for American travelers on business trips to Europe?"

**2. Source citation**
C02 — FAQPage Schema with Conversational Query Coverage. Research: FAQPage markup pages are 3.2x more likely to appear in Google AI Overviews (Frase.io, 2025). AI-referred sessions grew 527% YoY to May 2025 (Geneo, 2025). GEO for hospitality: LSEO.com, 2025.

**3. Current state**
No FAQPage schema detected in SERP rich results for this URL. No FAQ or Q&A content visible in search snippets. The page's confirmed copy is entirely in marketing register with zero factual Q&A content.

**4. Inferred implementation status**
N/A — first run.

**5. Directional impact estimate**
HIGH. Radisson Blu is the brand most queried by American bleisure travelers in Europe. A FAQPage on this page becomes the citation source for ChatGPT, Google AI Overviews, and Perplexity when answering "Is Radisson Blu good for business travel in Europe?" — currently ceded entirely to OTA pages and Wikipedia.

**6. Priority tier**
P1

---

### PROP-002 — FAQPage Schema: Homepage (GAP-002 + GAP-024)

**1. Proposed change**
Add a visible FAQ section to the Radisson homepage with 4–6 questions answering bleisure traveler queries. Wrap in FAQPage JSON-LD. Suggested questions:
- "Does Radisson have hotels with meeting rooms in Europe?"
- "Which Radisson brands are designed for business travelers?"
- "Do Radisson hotels in Europe have spas and fitness facilities?"
- "What is the best Radisson brand for a work trip with leisure time in London?"
- "Does Radisson offer loyalty programs for frequent US business travelers to Europe?"

**2. Source citation**
C02 — FAQPage Schema. Research: FAQ schema is the single most impactful structured data type for AI citations in 2026; pages with 5–8 Q&A pairs cited up to 3x more (run_001 literature findings). Booking.com and Expedia FAQ architecture is the primary reason OTAs dominate AI recommendations over brand.com pages (Kismet Travel, 2025).

**3. Current state**
No FAQPage schema detected. No FAQ section visible in SERP snippets. Meta description is booking-CTA format with no Q&A content.

**4. Inferred implementation status**
N/A — first run.

**5. Directional impact estimate**
HIGH. The homepage FAQ creates brand-level citation surfaces for the most common brand-discovery queries. Without it, AI engines cannot authoritatively answer "What is Radisson Hotels?" from Radisson's own domain, defaulting instead to Wikipedia or OTA descriptions.

**6. Priority tier**
P1

---

### PROP-003 — FAQPage Schema: London Hotels Page (GAP-020 + GAP-024)

**1. Proposed change**
Add a "London Hotel FAQ" section to the London overview page with 5 questions and FAQPage JSON-LD:
- "Where are Radisson Blu hotels located in London?"
- "Do Radisson hotels in London have meeting rooms and business facilities?"
- "Are Radisson hotels in London near Heathrow Airport?"
- "Which Radisson hotel is closest to Canary Wharf or the City of London?"
- "Do Radisson hotels in London allow extended stays for business travelers?"

**2. Source citation**
C02 — FAQPage Schema. C12 — Geographic Entity Signals. Research: London is the top European bleisure destination for American travelers; FAQ schema on city pages is the fastest path to AI citation for destination-specific queries (PCMA Trends Report 2025; HiJiffy AEO/GEO guide).

**3. Current state**
No FAQPage schema detected. London overview page confirmed body content is tourism-framed with no business travel FAQ content visible.

**4. Inferred implementation status**
N/A — first run.

**5. Directional impact estimate**
HIGH. London-specific FAQs match the highest-volume AI query type for US→Europe bleisure travelers. This FAQ block directly intercepts queries like "Radisson hotels London near financial district" — currently answered by Booking.com, Tripadvisor, or IHG rather than Radisson's own domain.

**6. Priority tier**
P1

---

### PROP-004 — FAQPage Schema: Brands Page (GAP-008)

**1. Proposed change**
Add a visible "Brand Comparison FAQ" section to the brands overview page with 4–5 questions:
- "What is the difference between Radisson Blu and Radisson?"
- "Which Radisson brand is designed for upscale business travel in Europe?"
- "Does Radisson have a luxury hotel brand?"
- "Which Radisson brands are available in the United Kingdom?"
Wrap in FAQPage JSON-LD.

**2. Source citation**
C02 — FAQPage Schema. C07 — Entity Signals. Research: Brand comparison is a high-frequency AI query type; FAQPage schema on the brands page converts it into a structured answer source for brand-selection queries at the decision stage of the traveler journey (Frase.io; GenOptima AEO guide 2026).

**3. Current state**
No FAQPage schema detected. Meta description mentions "9 hotel brands" but gives no brand-specific or bleisure-relevant differentiation.

**4. Inferred implementation status**
N/A — first run.

**5. Directional impact estimate**
MEDIUM-HIGH. Brand comparison FAQ captures traveler decision-stage queries — the exact moment AI-assisted research is replacing traditional search. Establishes tier clarity between Radisson and Radisson Blu, reducing conflation in AI-generated recommendations.

**6. Priority tier**
P1

---

### PROP-005 — Rewrite Radisson Blu Brand Page: Factual Register (GAP-010 + GAP-012)

**1. Proposed change**
Rewrite the Radisson Blu brand page hero and about section to lead with factual statements, replacing or layering over current marketing copy ("unparalleled service," "unforgettable experiences"):
- "Radisson Blu is Radisson Hotel Group's flagship upscale brand, operating over 380 hotels across more than 60 countries, with the majority of its portfolio in Europe."
- "Radisson Blu hotels are located in major European business cities including London, Brussels, Amsterdam, Frankfurt, Copenhagen, and Stockholm."
- "Each Radisson Blu property includes high-speed WiFi, business center facilities, meeting and conference rooms, spa and wellness amenities, and on-site dining."
- "Radisson Blu holds a 4-star or higher classification at the majority of its European properties."
Opening paragraph must answer the query "Why choose Radisson Blu for European business travel?" in the first 80 words.

**2. Source citation**
C08 — Natural Language Query Compatibility. C04 — Meta Description Answer Format. Research: AI-cited content contains 62% more facts than non-cited content (Search Engine Land 8,000-citation study). 44% of ChatGPT citations come from the first third of cited content (ALM Corp). Marketing register is positively counterproductive to AI citation (Shiji Group, 2025).

**3. Current state**
Confirmed copy: "We provide unparalleled service, comfort, and style while creating meaningful and memorable experiences." / "By paying close attention to the small details that make a big difference, we inspire unforgettable experiences with every stay." Zero factual content in confirmed metadata.

**4. Inferred implementation status**
N/A — first run.

**5. Directional impact estimate**
HIGH. This is the single highest-impact content change available. Radisson Blu is the brand most relevant to the bleisure audience. Every AI query about upscale European business hotels is a potential citation opportunity currently squandered because the page contains no citable facts. Implementing factual content costs one hour of a content editor's time.

**6. Priority tier**
P1

---

### PROP-006 — Deploy Hotel/LodgingBusiness JSON-LD Schema: All Brand and Overview Pages (GAP-001 + GAP-023)

**1. Proposed change**
Deploy Hotel or LodgingBusiness JSON-LD schema via CMS template or tag manager across all brand and overview pages. Priority order: (1) Radisson Blu brand page, (2) Homepage, (3) London overview page, (4) All other brand pages. At minimum for each page, include: `@type: "Hotel"`, `name`, `url`, `logo`, `description` (factual), `address`, `starRating`, `amenityFeature` array (Business Center, Meeting Rooms, Free WiFi, Spa, Fitness Center), `sameAs` (Wikipedia, Wikidata, social profiles). For the homepage, additionally include `numberOfRooms` (portfolio total) and `areaServed` listing European countries and key cities.

**2. Source citation**
C01 — LodgingBusiness / Hotel Schema Presence. Research: GPT-4 accuracy on hotel queries improved from 16% to 54% when underlying content used structured data (Digidop, 2025). Schema is the machine interface for AI entity recognition; without it, pages are invisible to structured AI parsing (Google, Microsoft official statements, 2025). AI sessions in hospitality up 527% in 12 months to May 2025 (Geneo).

**3. Current state**
Zero Hotel or LodgingBusiness schema rich results detected across any audited brand or overview page. No star rating, check-in/out, or amenityFeature rich snippets visible in SERP for any Priority 1 URL.

**4. Inferred implementation status**
N/A — first run.

**5. Directional impact estimate**
HIGH (structural). Schema is the precondition for all other GEO improvements. Without it, content improvements and FAQ schema operate without the machine-readable entity foundation AI engines use to categorize and cite hotel brands. IHG and Accor have already moved to AI-native data architectures; every week without schema is competitive ground ceded.

**6. Priority tier**
P1

---

### PROP-007 — Add Amenity Content (Business + Leisure) to Radisson Blu Brand Page (GAP-013)

**1. Proposed change**
Add an "Amenities at Radisson Blu" section to the brand page with two explicit sub-sections:
- **For Business:** Business center, dedicated meeting and conference rooms, high-speed WiFi, secretarial services, executive floors
- **For Leisure:** Spa and wellness center, fitness facilities, swimming pool at select properties, on-site bar and restaurant, concierge services

Back with schema: add `amenityFeature` array in LodgingBusiness JSON-LD covering both business and leisure categories.

**2. Source citation**
C11 — Amenity Coverage: Bleisure-Specific Features. Research: The dual business-and-leisure amenity profile is the defining signal for bleisure traveler queries; AI engines processing compound amenity queries look for sources confirming both types (Dan Taylor SEO; Hotel Growth Agency, 2025). Industry sources confirm Radisson Blu as "business-meets-leisure guest mix" but this is absent from on-page metadata.

**3. Current state**
No amenities mentioned in confirmed Radisson Blu brand page metadata. Confirmed copy mentions "service, comfort, and style" without specific amenity categories.

**4. Inferred implementation status**
N/A — first run.

**5. Directional impact estimate**
HIGH for bleisure segment. The compound amenity signal ("meeting rooms AND spa") is the most common query pattern for US bleisure travelers. Absence means the Radisson Blu brand page is invisible to this query type entirely, even though the physical amenities exist at almost every property.

**6. Priority tier**
P1

---

### PROP-008 — Add Geographic Entity Signals to Radisson Blu Brand Page (GAP-014)

**1. Proposed change**
Add a "Radisson Blu in Europe" section naming 10–15 flagship European cities with Radisson Blu presence: "Radisson Blu operates in over 200 European locations including London, Brussels, Amsterdam, Paris, Frankfurt, Stockholm, Copenhagen, Oslo, Dublin, Zurich, Vienna, Rome, Milan, Barcelona, and Warsaw." Add `areaServed` to brand-level schema: `"areaServed": ["Europe", "United Kingdom", "Germany", "France", "Netherlands", "Belgium", "Sweden", "Denmark", "Ireland", "Switzerland", "Italy", "Spain", "Poland"]`.

**2. Source citation**
C12 — Geographic Entity Signals. C07 — Entity Signals: Brand + Location + Category Clarity. Research: Geographic entity consistency (schema + copy + third-party naming same cities) is a primary AI citation predictor (WebProNews, 2025). AI engines cannot confidently associate Radisson Blu with European destinations without explicit geographic entity signals in page content.

**3. Current state**
No geographic specificity in confirmed Radisson Blu title or description. Title "Radisson Blu Hotels & Resorts | Radisson Hotels" contains no geographic entity. Description mentions no locations.

**4. Inferred implementation status**
N/A — first run.

**5. Directional impact estimate**
MEDIUM-HIGH. Geographic entity signals are how AI engines resolve "which Radisson hotel is in [European city]" — without them, the brand page cannot answer city-specific discovery queries. This is a single sentence addition to body content and a one-line schema field.

**6. Priority tier**
P2

---

### PROP-009 — Rewrite Homepage Meta Description: Factual Answer Format (GAP-003)

**1. Proposed change**
Replace current meta description ("Explore over 1100 hotels worldwide and book your stay with us today, with the best online rates guaranteed!") with:

*"Radisson Hotel Group operates over 1,100 hotels across more than 95 countries, with a strong concentration in European business destinations. Brands include Radisson Blu, designed for upscale business and leisure travel, with meeting facilities, spas, and loyalty benefits for frequent travelers."*

**2. Source citation**
C04 — Meta Description: Natural Language Answer Preview. Research: AI-cited content contains 62% more facts than non-cited content. Factual meta descriptions increase AI engine citation probability and organic click rate simultaneously. "Best rates guaranteed" is a booking incentive, not an information signal (Search Engine Land; MyLighthouse hotel AI guide, 2025).

**3. Current state**
"Explore over 1100 hotels worldwide and book your stay with us today, with the best online rates guaranteed!" — booking-CTA format, no traveler type, no geographic specificity, no amenity signal.

**4. Inferred implementation status**
N/A — first run.

**5. Directional impact estimate**
MEDIUM. A factual meta description increases the probability that AI engines pull Radisson's own language rather than OTA language when responding to brand-level traveler queries. Impact is portfolio-wide since the homepage is the primary entity page.

**6. Priority tier**
P1

---

### PROP-010 — Rewrite Homepage Title: Geographic and Category Alignment (GAP-004)

**1. Proposed change**
Change homepage title from "Radisson Hotels Official Site | Book Rooms Worldwide" to:
*"Radisson Hotel Group | Upscale Hotels in Europe & Worldwide"*

Or with bleisure framing:
*"Radisson Hotel Group | Business & Leisure Hotels Across Europe"*

**2. Source citation**
C03 — Title Tag: Conversational Query Alignment. Research: AI engines process titles as semantic summaries for LLM embedding; "Book Rooms Worldwide" is transactional with no entity, audience, or geographic signal. Hilton: "Hotels & Resorts Worldwide | Hilton"; Marriott: "Hotel Rooms & Suites | Marriott Hotels" — both use category + scope, no conversion verbs (DefiniteSEO title tag optimization; DHI Hospitality GEO framework).

**3. Current state**
"Radisson Hotels Official Site | Book Rooms Worldwide" — transactional ("Book Rooms"), no geographic specificity, no traveler type.

**4. Inferred implementation status**
N/A — first run.

**5. Directional impact estimate**
MEDIUM. "Europe" in the homepage title creates the geographic association currently missing from Radisson's primary entity page. Directly improves AI entity categorization for US-to-Europe bleisure queries.

**6. Priority tier**
P2

---

### PROP-011 — Add Factual Body Content to Homepage: Bleisure-Answering Section (GAP-005 + GAP-006)

**1. Proposed change**
Add a "Who We Are" / "About Our Hotels" body section to the homepage with 150–250 words of factual, structured content:
- H2: "Radisson Hotel Group: Upscale Hotels for Business and Leisure Travel in Europe and Beyond"
- Bullet points: portfolio size (1,100+ hotels, 95+ countries), brand count (9 brands), featured European cities (London, Amsterdam, Paris, Brussels, Frankfurt), flagship amenities (business centers, meeting rooms, high-speed WiFi, spa, fitness centers, on-site dining)
- One sentence explicitly addressing the bleisure audience: "Radisson and Radisson Blu hotels across Europe are designed for travelers combining business trips with leisure time, offering both professional facilities and leisure amenities at the same property."

**2. Source citation**
C08 — Natural Language Query Compatibility. C11 — Amenity Coverage. Research: 82.5% of AI citations link to deeply nested pages, but brand homepages need minimum viable factual content for brand-level queries (Search Engine Land answer-first content guide). IHG's AI content platform restructures content into modular, machine-readable answers — the recognized standard (Hospitality.today; IHG Skift Feb 2026).

**3. Current state**
Confirmed homepage content: "Explore over 1100 hotels worldwide" — scale signal only. No amenity content, no traveler type, no geographic specificity, no bleisure content visible.

**4. Inferred implementation status**
N/A — first run.

**5. Directional impact estimate**
HIGH when combined with FAQ schema (PROP-002). The homepage factual layer creates citation-ready content for brand-level AI queries — "Tell me about Radisson hotels" — currently answered from OTA descriptions or Wikipedia rather than Radisson's own domain.

**6. Priority tier**
P1

---

### PROP-012 — Rewrite London Page Title and Add Business Travel Content Layer (GAP-018 + GAP-019)

**1. Proposed change**
Part A — Title change: Replace "Beloved secret spots and best hotels in London | Radisson Hotels" with "Hotels in London | Radisson Blu & Radisson Hotels | Business & Leisure Stays"

Part B — Add "London for Business and Bleisure Travel" content section: "Radisson and Radisson Blu hotels in London are located near key business districts including Canary Wharf, Heathrow Airport, and the City of London. All London properties offer high-speed WiFi, business centers, and meeting facilities. Extended weekend rates are available for business travelers combining work and leisure." Use H2 for this section.

**2. Source citation**
C03 — Title Tag Alignment. C08 — Natural Language Query Compatibility. C11 — Amenity Coverage. Research: London is the top European bleisure destination for American travelers (PCMA, 2025). Title misalignment makes the page invisible to business travel query types (eHotelier bleisure strategy guide, 2025). Hilton's and Marriott's London pages both use neutral, query-aligned titles (confirmed in SERP, March 2026).

**3. Current state**
Title: "Beloved secret spots and best hotels in London | Radisson Hotels" — tourism-first framing with no business travel signal. Body content focuses on Thames, Big Ben, Buckingham Palace — leisure traveler register.

**4. Inferred implementation status**
N/A — first run.

**5. Directional impact estimate**
HIGH for the London destination segment. Title realignment immediately broadens the page's query surface area to include business travel and bleisure queries — the dominant AI query type for US→London travel in the 25–55 age group.

**6. Priority tier**
P1

---

### PROP-013 — Add Amenity Aggregation and District-Level Geographic Signals to London Page (GAP-021 + GAP-022)

**1. Proposed change**
Add "Amenities at Radisson London Hotels" section to London overview page: "All Radisson and Radisson Blu hotels in London provide complimentary high-speed WiFi, on-site business centers, meeting room facilities, and fitness centers. Select properties offer spa services. Airport transfer arrangements are available at Heathrow-area properties."

Add district-level geographic callouts: "Radisson Blu Edwardian properties are located in the West End and Bloomsbury. Our Canary Wharf-area property serves London's financial district. Heathrow-adjacent properties provide convenient access for connecting travelers."

Map to schema-level `location` properties in LodgingBusiness or ItemList schema on the overview page.

**2. Source citation**
C11 — Amenity Coverage. C12 — Geographic Entity Signals. Research: Overview-level amenity aggregation is what OTAs do natively and what AI engines look for when answering portfolio-level queries (Kismet Travel, 2025). IHG names key London districts at overview level to enable district-level entity associations (confirmed SERP, March 2026).

**3. Current state**
Bleisure amenity content exists only at individual property level. Geographic district signals (Canary Wharf, Heathrow, Bloomsbury) only visible inside individual property listings.

**4. Inferred implementation status**
N/A — first run.

**5. Directional impact estimate**
MEDIUM-HIGH. Enables the London overview page to answer "Radisson hotels near Canary Wharf" and "hotels in London with business center" at the page level — queries that currently bounce travelers to individual property pages, ceding the overview citation to Booking.com or IHG.

**6. Priority tier**
P2

---

### PROP-014 — Fix Radisson Brand Page Title (GAP-015)

**1. Proposed change**
Change title from "Radisson | Hotel Deals | Yes I Can! Attitude" to:
*"Radisson Hotels | Upper Midscale Stays for Business & Leisure"*
or
*"Radisson Hotels | Contemporary Hotels Worldwide | Radisson Hotel Group"*

Remove "Hotel Deals" (promotional term, not descriptive) and "Yes I Can! Attitude" (tagline with no AI-parseable meaning) from the title tag entirely.

**2. Source citation**
C03 — Title Tag Alignment. Research: Tagline-dominated titles perform poorly in AI engine embedding because non-semantic words dilute the signal (DefiniteSEO, 2025). Promotional terms in titles compete with OTA deal pages rather than positioning the brand as an informational entity (HotelMinder AI search optimization).

**3. Current state**
"Radisson | Hotel Deals | Yes I Can! Attitude" — tagline-first, promotional, no category or geographic signal.

**4. Inferred implementation status**
N/A — first run.

**5. Directional impact estimate**
MEDIUM. Removes the signal noise from the brand page title and enables correct AI entity categorization. "Hotel Deals" title competes against OTA deal pages rather than establishing Radisson as a hotel brand information page.

**6. Priority tier**
P2

---

### PROP-015 — Brands Page Meta Description: Name Specific Brands and Geographies (GAP-007 + GAP-009)

**1. Proposed change**
Replace brands page meta description ("Radisson Hotel Group provides a dynamic set of hotel brands for a wide range of travelers and budgets. We have 9 hotel brands, each of these with own identity.") with:

*"Radisson Hotel Group operates nine hotel brands including Radisson Collection, Radisson Blu, Radisson, Park Plaza, and Park Inn — spanning luxury, upscale, and midscale tiers across Europe, Middle East, Africa, and Asia-Pacific."*

Add body section: "Radisson Hotels in Europe" naming 8–10 key European cities with specific brand presence. Add `areaServed` to Organization schema.

**2. Source citation**
C04 — Meta Description. C07 — Entity Signals. C09/C12 — Geographic Signals. Research: Specific, brand-naming meta descriptions give AI engines extractable entity data for comparison queries. Geographic entities must be named explicitly to enable AI engine geographic association (Digidop, 2025; WebProNews entity optimization, 2025).

**3. Current state**
"Radisson Hotel Group provides a dynamic set of hotel brands for a wide range of travelers and budgets. We have 9 hotel brands, each of these with own identity." — generic, no brand names, no geographic scope.

**4. Inferred implementation status**
N/A — first run.

**5. Directional impact estimate**
MEDIUM. Enables the brands page to answer "What brands does Radisson have in Europe?" from Radisson's own domain. Currently AI engines must source this from Wikipedia or Skift because Radisson's own brands page doesn't contain the answer.

**6. Priority tier**
P2

---

### PROP-016 — Audit Radisson.com robots.txt for AI Crawler Blocking (GAP-017 + systemic)

**1. Proposed change**
Audit radissonhotels.com `robots.txt` and `meta robots` configurations to confirm that legitimate AI crawlers — GPTBot (ChatGPT), PerplexityBot, ClaudeBot, Bingbot/Copilot — are not blocked by blanket bot-blocking rules. If blocked: implement selective whitelisting for named AI crawlers while maintaining scraper/bad-bot protections. If JavaScript-only rendering is causing metadata to be inaccessible: implement server-side rendering (SSR) or static HTML export for all brand and overview pages. Confirm that `User-agent: GPTBot`, `User-agent: PerplexityBot`, and `User-agent: Bingbot` are permitted in `robots.txt` or not specifically blocked.

**2. Source citation**
C01 — Schema Presence (prerequisite). Research: Bot-blocked pages generate zero AI citations regardless of content quality. The 403 errors returned to this audit's direct fetch attempts suggest blanket blocking that may affect legitimate AI crawlers (GEO checklist, totheweb.com; assessment from gap_research.md Phase 2.5 sub-agent). Best practice for AI crawler access is actively contested — selective whitelisting is the recommended intermediate approach (Gap Research Assessment, run_001).

**3. Current state**
All direct HTTP fetches of radissonhotels.com returned 403. This may indicate user-agent-based blocking, IP-range blocking, or JavaScript rendering dependency. Whether AI crawler agents (GPTBot, PerplexityBot) are also blocked is unconfirmed.

**4. Inferred implementation status**
N/A — first run.

**5. Directional impact estimate**
CRITICAL PREREQUISITE. If AI crawlers are blocked, all other GEO improvements are ineffective. Schema, FAQ content, and factual rewrites only generate AI citations if the page can be crawled. This must be confirmed before any other optimization is deployed. Best practice is contested (privacy vs. visibility tradeoff), but the baseline position should be: AI crawlers are permitted.

**6. Priority tier**
P1 (prerequisite)

---

### PROP-017 — FAQPage Schema: Radisson Brand Page (GAP-016)

**1. Proposed change**
Add "Radisson Hotels FAQ" section to the Radisson brand page with 4 questions wrapped in FAQPage JSON-LD:
- "What type of hotels are Radisson?"
- "What is the difference between Radisson and Radisson Blu?"
- "Do Radisson hotels have business facilities?"
- "Where are Radisson hotels in Europe?"

**2. Source citation**
C02 — FAQPage Schema. Research: Brand tier differentiation content is critical since many travelers conflate "Radisson" and "Radisson Blu." FAQ schema on both tier pages establishes clear AI-readable distinctions (SeoTuners AEO/GEO schema guide, 2025).

**3. Current state**
No FAQPage schema detected. Title "Radisson | Hotel Deals | Yes I Can! Attitude" is misaligned; no FAQ or informational Q&A content visible.

**4. Inferred implementation status**
N/A — first run.

**5. Directional impact estimate**
MEDIUM. Establishes brand-tier clarity in AI-generated recommendations. Prevents AI engines from conflating Radisson and Radisson Blu when answering questions about specific service tiers.

**6. Priority tier**
P2

---

### PROP-018 — Homepage Amenity Schema: amenityFeature JSON-LD (GAP-006)

**1. Proposed change**
Add `amenityFeature` array to the homepage Hotel/LodgingBusiness JSON-LD:
```json
"amenityFeature": [
  {"@type": "LocationFeatureSpecification", "name": "Business Center", "value": true},
  {"@type": "LocationFeatureSpecification", "name": "Meeting Rooms", "value": true},
  {"@type": "LocationFeatureSpecification", "name": "Free WiFi", "value": true},
  {"@type": "LocationFeatureSpecification", "name": "Spa", "value": true},
  {"@type": "LocationFeatureSpecification", "name": "Fitness Center", "value": true},
  {"@type": "LocationFeatureSpecification", "name": "On-site Restaurant", "value": true}
]
```
This is additive to PROP-006 (Hotel schema deployment).

**2. Source citation**
C11 — Amenity Coverage. Research: Amenity data in schema is precisely what AI engines parse when answering compound amenity queries. Booking.com's granular amenity schema is a primary competitive advantage in AI recommendations (Hospitality.today; Core Optimisation schema guide).

**3. Current state**
No amenity content in confirmed homepage metadata. No amenityFeature schema visible in SERP.

**4. Inferred implementation status**
N/A — first run.

**5. Directional impact estimate**
HIGH when combined with PROP-006. Amenity schema is the machine-readable layer that enables Radisson to appear in amenity-filtered AI queries at the portfolio level.

**6. Priority tier**
P1 (bundled with PROP-006)

---

## Implementation Prioritization

### Immediate (Week 1–2): P1 Structural
1. PROP-016 — Audit AI crawler access / robots.txt (prerequisite for everything)
2. PROP-006 / PROP-018 — Deploy Hotel/LodgingBusiness + amenityFeature JSON-LD across all brand pages
3. PROP-001 — FAQPage schema: Radisson Blu brand page
4. PROP-002 — FAQPage schema: Homepage
5. PROP-003 — FAQPage schema: London overview page
6. PROP-004 — FAQPage schema: Brands page

### Short-term (Week 2–3): P1 Content
7. PROP-005 — Rewrite Radisson Blu brand page content (factual register)
8. PROP-009 — Rewrite homepage meta description
9. PROP-011 — Add factual body content to homepage (bleisure-answering section)
10. PROP-012 — London page title change + business travel content layer

### Medium-term (Week 3–6): P2
11. PROP-008 — Geographic entity signals: Radisson Blu brand page
12. PROP-010 — Homepage title change
13. PROP-013 — London amenity aggregation + district-level geographic signals
14. PROP-014 — Fix Radisson brand page title
15. PROP-015 — Brands page meta description + geographic signals
16. PROP-017 — FAQPage schema: Radisson brand page
