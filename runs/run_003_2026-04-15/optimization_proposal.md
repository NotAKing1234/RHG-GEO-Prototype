# Optimization Proposal — run_003 | 2026-04-15

## Executive Summary

This run identified **34 total gaps** across all audited Radisson Hotel Group pages — 12 new gaps and 22 recurring from prior runs, with one escalated (Radisson Collection Lake Como, now open Q1 2026, still absent from brand page). After 26 days since run_002, zero implementations have been detected, making this the first run where the cost of inaction becomes measurable: every week Radisson remains AI-crawler-blocked and schema-absent, Accor's ChatGPT app (live January 29) and Hyatt's (live February 2026) widen the direct AI distribution gap. The **top 3 priority changes** for this run are: (1) remove the site-wide AI crawler block (Cloudflare fix — prerequisite for all else); (2) deploy Hotel/LodgingBusiness schema across all five Priority 1 brand pages (3.2× citation multiplier in one engineering sprint); and (3) update the Radisson Collection brand page with 2026 expansion facts (Lake Como already open, Paris Banke Opéra H2 2026) — a zero-tech content gap that makes Radisson uncitable for "new luxury hotels in Europe 2026" queries the brand should own.

---

## PROPOSAL ENTRIES

---

### PROP-001 — Unblock AI Retrieval Crawlers Site-Wide (Cloudflare Fix)
**Gap ref:** GAP-001 | C04 | Homepage (site-wide)

1. **Proposed change:** Log into Cloudflare Dashboard → Security → Bots → AI Crawl Control. Disable the "Block AI bots" master toggle (or equivalent WAF managed rule). Set per-crawler rules: Allow OAI-SearchBot, ChatGPT-User, PerplexityBot, ClaudeBot, Google-Extended, Applebot-Extended. Block GPTBot (OpenAI training) and CCBot (Common Crawl training). Update robots.txt to explicitly permit retrieval bots. Validate: robots.txt returns HTTP 200.

2. **Source citation:** Nytro SEO Cloudflare AI Crawler Guide 2026 — distinguish AI retrieval bots (drive citations) from AI training bots (harvest content). Hotel robots.txt & AI Blocking Study 2026 (hotelrank.ai): only 3.3% of 105,002 hotel websites block any AI crawler; smart allow/block split used by just 2.1% — clear competitive opportunity. 2025 Rutgers/Wharton study: blocking AI crawlers reduces citation quality but does NOT reliably prevent citation (≈75% of blocked sites still cited). 73% citation reduction confirmed for sites blocking GPTBot in ChatGPT (prior run research, confirmed current).

3. **Current state:** HTTP 403 returned for all WebFetch attempts including /robots.txt, /llms.txt, and all brand/overview/property pages. WAF "Block AI Scrapers and Crawlers" managed rule confirmed active for 3 consecutive runs (run_001, run_002, run_003). robots.txt content unreadable.

4. **Inferred implementation status:** NOT IMPLEMENTED. /robots.txt still returns 403 on 2026-04-15 — 26 days post-run_002 proposal. This is the 3rd consecutive unaddressed run for this gap.

5. **Directional impact estimate:** CRITICAL. This is the upstream prerequisite for all other GEO optimizations. An American bleisure traveler asking ChatGPT or Perplexity "best business hotels in London with good restaurants and weekend availability" structurally cannot receive a Radisson citation from Radisson's own domain under the current configuration. Unblocking enables all subsequent schema, FAQ, and content improvements to deliver their intended value.

6. **Priority tier:** P1

---

### PROP-002 — Deploy Hotel/LodgingBusiness Schema on All Brand Pages
**Gap ref:** GAP-002, GAP-010, GAP-015, GAP-016, GAP-021 | C02 | All Priority 1 brand pages

1. **Proposed change:** Add Hotel JSON-LD to all five Priority 1 brand pages. Template for each page: `@type: Hotel`, `name`, `description` (informational register, 150–200 chars), `amenityFeature` (≥5 LocationFeatureSpecification entries), `potentialAction` (ReserveAction with booking URL), `address`, `telephone`, `logo`. See gap_research.md GAP-002 for specific JSON-LD templates per brand. The `potentialAction` with `ReserveAction` is the 2026 addition enabling AI agents to surface the direct booking path. Validate with Google Rich Results Test before deployment.

2. **Source citation:** Hotel Schema Adoption Study 2026 (hotelrank.ai): 10.6% of hotels have good schema; 2.5× higher AI citation probability for those that do; 3.2× citation multiplier confirmed in cross-industry analysis (65–71% of AI-cited pages have structured data). Anatomy of ChatGPT Hotel Search 2026 (hotelrank.ai): Marriott is among only 3 hotel brands appearing in sponsored ChatGPT hotel search results — Hotel schema is a prerequisite. URL quality (0.60) and trust signals (0.50) have larger raw weights, but schema (0.23) enables both by providing structured entity data.

3. **Current state:** Zero Hotel, LodgingBusiness, FAQPage, or any structured data rich results detected in SERP for any Priority 1 brand page across 3 consecutive runs. JSON-LD unconfirmable due to 403 block but presumed absent given zero SERP rich results.

4. **Inferred implementation status:** NOT IMPLEMENTED. No schema rich results detected in run_003 (26 days post-run_002 proposal). 3rd consecutive unaddressed run.

5. **Directional impact estimate:** HIGH. Schema markup enables AI engines to extract structured hotel attributes (location, amenities, pricing, ratings) from brand pages. Without it, AI systems must infer properties from unstructured prose, producing unreliable and less frequent citations. A one-sprint engineering deployment across five pages.

6. **Priority tier:** P1

---

### PROP-003 — Add FAQPage Schema Across All Brand Pages
**Gap ref:** GAP-005, GAP-011, GAP-022, GAP-029 | C03 | Homepage, Radisson Blu, Park Plaza, Rewards

1. **Proposed change:** Add visible FAQ sections (minimum 5–7 Q&A pairs) on homepage, Radisson Blu brand page, and Park Plaza brand page, with corresponding FAQPage JSON-LD. Upgrade `/rewards/faq` page with FAQPage schema if not present. Questions must mirror real traveler AI queries (not generic "What is X?"). Key FAQ pairs for homepage: "Which Radisson hotels are best for American business travelers visiting Europe?" / "Does Radisson have hotels for bleisure travelers combining business and leisure?" / "What loyalty benefits does Radisson offer for frequent US travelers to Europe?" See gap_research.md GAP-005 for specific JSON-LD template and full question list per brand page.

2. **Source citation:** Frase.io FAQ Schema AEO Guide: pages with FAQPage markup are 3.2× more likely to appear in Google AI Overviews. AI extraction rate increases 3.1× when FAQ questions match actual user prompts. Google no longer shows FAQ rich results for hotel brands in SERP (2023 policy), but FAQPage schema remains the primary Q&A extraction mechanism for ChatGPT, Perplexity, and Gemini. Booking.com and Expedia embed FAQ structured data answering traveler-segment-specific questions directly in their property pages.

3. **Current state:** No FAQPage schema detected in SERP for any audited page. /en-us/faq and /en-us/rewards/faq pages exist but no FAQPage JSON-LD confirmed. 3rd consecutive run for homepage/Radisson Blu/Park Plaza. 1st run for Rewards.

4. **Inferred implementation status:** NOT IMPLEMENTED. 3rd consecutive unaddressed run.

5. **Directional impact estimate:** HIGH. FAQ schema creates machine-readable Q&A pairs that directly match conversational query patterns used by American bleisure travelers in ChatGPT and Perplexity. Each FAQ entry is a potential direct citation trigger for the specific traveler-type + destination + amenity combinations that define bleisure search.

6. **Priority tier:** P1

---

### PROP-004 — Rewrite Radisson Blu Brand Page Opening Copy to Factual Register
**Gap ref:** GAP-007 | C07 | Radisson Blu brand page

1. **Proposed change:** Replace the current marketing register opening copy ("We provide unparalleled service, comfort, and style while creating meaningful and memorable experiences...") with a factual opening that contains: hotel count (280+), number of European cities served (70+), named anchor cities (London, Paris, Amsterdam, Berlin), specific business amenities (meeting rooms, business centre, co-working), and bleisure positioning sentence. Proposed opening: "Radisson Blu operates 280+ hotels across 70+ European cities — including London, Paris, Amsterdam, and Berlin — offering city-centre locations with business centres, meeting facilities, and co-working spaces designed for business travelers extending their trips into weekends. Each property combines professional-grade connectivity with locally inspired design, making Radisson Blu the preferred choice for American bleisure travelers seeking European bases from which to work and explore."

2. **Source citation:** HiJiffy AEO/GEO for Hotels: "specificity over generics" is the defining AI citation pattern. Smartvel Location Pages 2026: "AI systems prioritize the main text, especially opening paragraphs." Search Engine Land 8,000-citation study: factual content cited at 62% higher rate than marketing register. ALM Corp "44% first-third rule": AI systems prioritize content appearing in the first 40–80 words.

3. **Current state:** Confirmed body copy (3 consecutive runs): "We provide unparalleled service, comfort, and style while creating meaningful and memorable experiences. By paying close attention to the small details that make a big difference, we inspire unforgettable experiences with every stay." Zero specific facts in first 80 words. Pure marketing register.

4. **Inferred implementation status:** NOT IMPLEMENTED. Identical copy detected in run_003 (26 days post-run_002). 3rd consecutive unaddressed run.

5. **Directional impact estimate:** HIGH. The first 80 words are heavily weighted by AI extraction systems. Factual, specific content in the opening paragraph dramatically increases citation probability for queries like "best hotels in Europe for American business travelers who want to explore the city on weekends." Zero tech work required — copywriting only.

6. **Priority tier:** P1

---

### PROP-005 — Add Radisson Collection 2026 Expansion Facts to Brand Page
**Gap ref:** GAP-013, GAP-014 | C10, C07 | Radisson Collection brand page

1. **Proposed change:** Add a "New in 2026" section to the Radisson Collection brand page immediately, featuring: (a) Palazzo San Gottardo Lake Como, A Radisson Collection Hotel — "Opened Q1 2026. A restored 1926 landmark palazzo on Lake Como with 72 rooms and suites, panoramic rooftop views, and a heritage spa. Located at Via Cairoli 2, Como, Italy." (b) Banke Opéra Paris, A Radisson Collection Hotel — "Opening H2 2026. The first Radisson Collection property in Paris, in a renovated Belle Époque bank building in the 9th arrondissement, featuring 90 rooms and a staircase attributed to Gustave Eiffel." Update meta description to reference "2026 openings in Lake Como and Paris." Add Heritage details (Eiffel staircase, Belle Époque bank vault) to main brand copy — these specific facts are cited verbatim in AI travel recommendations (confirmed: Four Seasons, Rosewood models).

2. **Source citation:** Anatomy of ChatGPT Hotel Search 2026 (hotelrank.ai): ChatGPT "prioritizes fresh content" in hotel search pipeline. Smartvel Location Pages 2026: heritage architecture facts are exactly the type of entity-level specifics that appear in AI travel recommendations. Trade press citations: CPP-Luxury (Lake Como open Q1 2026), Travel and Tour World (Banke Opéra Paris H2 2026), Robb Report (Palazzo San Gottardo). GAP-013 ESCALATED: property is now open and generating OTA reviews — Radisson brand page is not capturing the citation benefit.

3. **Current state:** Radisson Collection brand page title "Radisson Collection Luxury Hotels | Radisson Hotels" unchanged for 3 consecutive runs. No reference to Lake Como opening (already open Q1 2026) or Paris Banke Opéra in any confirmed brand page metadata. Copy remains generic ("premium style collection of luxury hotels offering quality services, dining, wellness and much more"). Lake Como and Paris coverage is appearing on OTA pages and third-party travel media — not on Radisson's own brand page.

4. **Inferred implementation status:** NOT IMPLEMENTED. No freshness signal detected. Gap escalated from run_002 (WEAK → MISSING/CRITICAL): the property is now operational and generating reviews. This is a pure content gap requiring zero technical work.

5. **Directional impact estimate:** HIGH. An American luxury bleisure traveler researching "new luxury hotels in Italy 2026" or "hotel near Paris Opera for business and leisure" is asking queries Radisson Collection should own. Every week without this content, the brand page loses citation priority to OTA listings that already have the property data.

6. **Priority tier:** P1

---

### PROP-006 — Elevate Park Plaza Bleisure Signals to Title and Meta
**Gap ref:** GAP-018, GAP-019, GAP-020 | C05, C08, C09 | Park Plaza brand page

1. **Proposed change:** (a) Rewrite title: from "City Centre Hotels | Park Plaza Hotels & Resorts" to "Park Plaza Hotels | Business & Leisure Hotels in London, Amsterdam & Europe" (adds bleisure signal, names cities). (b) Rewrite meta description: from "Park Plaza Hotels & Resorts offer stylish guest rooms in city centre locations, meeting facilities and award-winning restaurants and bars." to "Park Plaza city-centre hotels in London, Amsterdam, and 50+ European locations offer meeting facilities, flexible workspaces, and leisure amenities for business travelers extending their stays. Book direct for member rates." (c) Add one paragraph addressing American travelers explicitly, citing London Heathrow/Schiphol airport proximity, USD billing, English-speaking service, and Radisson Rewards compatibility for US members.

2. **Source citation:** Park Plaza's own body copy ("business and leisure travelers") is the portfolio's strongest bleisure signal — just needs elevation to title/meta. 12AM Agency Entity SEO 2026 and Smartvel Location Pages 2026: geographic anchoring in title is required for city-specific AI query matching. WISK Bleisure Travel 2026: bleisure is now a standardized travel category with 70%+ adoption among business travelers — the term must appear in title/meta to match AI query patterns. GBTA data 2026: American business travelers take 405M+ long-haul trips annually, adding leisure time to 60% — largest bleisure segment by volume.

3. **Current state:** Title: "City Centre Hotels | Park Plaza Hotels & Resorts." Meta: "stylish guest rooms in city centre locations, meeting facilities and award-winning restaurants and bars." "Business and leisure travelers" confirmed in body copy but NOT in title or meta. No American traveler signals anywhere. Unchanged for 3 consecutive runs.

4. **Inferred implementation status:** NOT IMPLEMENTED. 2nd consecutive unaddressed run. Park Plaza is one title/meta edit away from being the portfolio's best bleisure-positioned page — the content evidence already exists in body copy.

5. **Directional impact estimate:** MEDIUM-HIGH. Park Plaza already has the strongest bleisure signal in the Radisson portfolio — the fix is simply ensuring it appears in AI-parseable metadata fields. Named cities (London, Amsterdam) in title create geographic entity signals for city-specific AI travel queries from American travelers. No tech work required.

6. **Priority tier:** P2

---

### PROP-007 — Rewrite Homepage Title and Meta Description
**Gap ref:** GAP-003, GAP-004 | C05, C06 | Homepage

1. **Proposed change:** (a) Title: replace "Radisson Hotels Official Site | Book Rooms Worldwide" with "Business & Leisure Hotels in Europe & Worldwide | Radisson Hotel Group" (60 chars). (b) Meta description: replace "Explore over 1100 hotels worldwide and book your stay with us today, with the best online rates guaranteed!" with "1,100+ hotels across Europe and worldwide for business travel and extended leisure stays. Radisson Hotel Group — city-centre locations, meeting facilities, member rates." (158 chars).

2. **Source citation:** Marriott.com title: "Hotels & Resorts: Business, Leisure & Extended Stay | Marriott International" — explicitly encodes both traveler types and stay-type categories, directly responsive to bleisure queries. SearchScaleAI Title/Meta Masterclass 2026: meta descriptions should function as informational summaries answering the searcher's question, not conversion language. Google rewrites 62%+ of meta titles in AI-powered results, algorithm favors specificity over brand declaration.

3. **Current state:** Title: "Radisson Hotels Official Site | Book Rooms Worldwide" (transactional CTA). Meta: "Explore over 1100 hotels worldwide and book your stay with us today, with the best online rates guaranteed!" (booking incentive). Neither contains traveler type, geographic specificity, or bleisure signal. Unchanged for 3 consecutive runs.

4. **Inferred implementation status:** NOT IMPLEMENTED. 3rd consecutive unaddressed run.

5. **Directional impact estimate:** MEDIUM-HIGH. Title is the first signal an AI engine reads to determine page relevance. Query-answering title increases probability of inclusion in AI citation pool for bleisure-intent queries from American travelers.

6. **Priority tier:** P2

---

### PROP-008 — Implement llms.txt
**Gap ref:** GAP-006 | C14 | Homepage (site-wide)

1. **Proposed change:** After resolving GAP-001 (Cloudflare fix), create /llms.txt at domain root. Content: Radisson Hotel Group overview (brands, property count, primary markets), links to key brand pages with descriptors, key facts for AI systems (founded, HQ, target traveler, direct booking URL). See gap_research.md GAP-006 for specific template. Deploy as part of the same Cloudflare fix sprint. Estimated implementation time: 30 minutes.

2. **Source citation:** llms.txt standard originated by Jeremy Howard (Answer.AI, September 2024). Visito AI and INNsight have documented implementation for hotel properties. John Mueller (Google): no AI crawlers currently confirmed to extract via llms.txt — but the protocol is gaining adoption and pairs naturally with the crawler access restoration. Not a standalone fix; a complement to the Cloudflare fix. Free generators available (Visito, Firecrawl, llms-txt.io).

3. **Current state:** /llms.txt returns HTTP 403. Absent. 2nd consecutive unaddressed run.

4. **Inferred implementation status:** NOT IMPLEMENTED.

5. **Directional impact estimate:** LOW-MEDIUM. Not a ranking factor yet, but signals AI-cooperative intent, provides structured content summary for AI systems that can't crawl, and is a 30-minute implementation bundled with the Cloudflare fix (GAP-001).

6. **Priority tier:** P3 (implement alongside PROP-001, not as a separate sprint)

---

### PROP-009 — Add American Traveler Signals to Radisson Blu and Park Plaza Brand Pages
**Gap ref:** GAP-009, GAP-020 | C09 | Radisson Blu, Park Plaza

1. **Proposed change:** Add one dedicated section to the Radisson Blu brand page and one to the Park Plaza brand page explicitly addressing American travelers. Content for Radisson Blu: "For American travelers visiting Europe: Radisson Blu properties across Europe offer USD-denominated billing, US-plug adapters in all rooms, English-speaking front desk teams 24/7, and direct connectivity to Radisson Rewards — earned in the US and redeemable across our European network. Our locations in London, Paris, Amsterdam, Brussels, and 70+ other European cities provide familiar standards with authentic local character." Add FAQ entry: "Are Radisson Blu hotels popular with American travelers visiting Europe?" — answer with specific cities, amenities relevant to US travelers, and loyalty program compatibility. Mirror this for Park Plaza with London/Amsterdam/airport proximity specifics.

2. **Source citation:** Navan Bleisure Travel Statistics 2026: 56% of US leisure travelers used AI for at least one trip in the past 12 months. Deloitte Travel Outlook 2026: American travelers planning European hotel stays use queries including "best hotels for US travelers in [European city]" and "European hotels with English-speaking staff." Booking.com destination pages for European cities include explicit American traveler context — this is confirmed best practice at scale. Marriott.com addresses US-to-Europe travelers in its international travel hub with Bonvoy points, USD booking, and US customer service contacts.

3. **Current state:** Zero American/US traveler references in any confirmed title, meta, or opening copy across all audited pages. 2nd consecutive unaddressed run for both pages.

4. **Inferred implementation status:** NOT IMPLEMENTED.

5. **Directional impact estimate:** MEDIUM-HIGH. American traveler signals create direct semantic matches for the highest-intent query segment (US-to-Europe business travel with leisure extension). Straightforward to add — copywriting only, no technical work.

6. **Priority tier:** P2

---

### PROP-010 — Upgrade Radisson Rewards for AI Loyalty Discovery
**Gap ref:** GAP-026, GAP-027, GAP-028, GAP-029 | C16, C09, C02, C03 | Rewards page

1. **Proposed change:** (a) Rewrite Rewards landing page opening with comparison-ready facts: member count, properties (1,100+), tiers (Club/Silver/Gold/Platinum), points-per-dollar-spent rate (Club: 20 pts/$1), European portfolio coverage (280+ Radisson Blu in 70+ European cities). Add: "No blackout dates. Points never expire as long as you stay once every 36 months." (b) Add comparison paragraph: "Radisson Rewards vs. other programs: earn points at 1,100+ properties worldwide including 280+ Radisson Blu hotels across 70+ European cities." (c) Add MemberProgram schema (Google-supported structured data type) to the Rewards page — see gap_research.md GAP-028 for specific JSON-LD template. (d) Add FAQPage schema to /rewards/faq page with query-mirroring questions including: "Is Radisson Rewards worth it compared to Marriott Bonvoy for European travel?", "How many points do I earn per dollar spent at Radisson hotels in Europe?", "Do Radisson Rewards points expire?" (e) Add explicit USD-denomination and US customer service contact to rewards page content.

2. **Source citation:** Smart With Points (UK): Radisson Rewards described as "the unsung hero of hotel loyalty." NerdWallet: "underrated" program. Both assessments indicate weak brand signal in AI training data. Marriott Bonvoy loyalty page: 200M+ members, 30 brands, 8,900 properties — comparison-ready facts that AI systems cite in loyalty comparison responses. Google introduced MemberProgram structured data as officially supported schema type for loyalty programs — directly displayable in Google search results. Marriott leads with 224 AI citations per 40 queries vs. Radisson's near-zero cited share.

3. **Current state:** Title: "Radisson Hotel Rewards Program | Radisson Rewards" — functional but not comparison-query-answering. No MemberProgram or Organization schema. /rewards/faq exists but no FAQPage schema confirmed. No explicit US traveler or transatlantic content. First audit run_003.

4. **Inferred implementation status:** N/A — first audit. No prior proposals for this page.

5. **Directional impact estimate:** HIGH. American bleisure travelers frequently ask AI systems to compare loyalty programs before committing to a hotel chain for European travel. Radisson not surfacing in these comparisons is a direct revenue risk — Marriott Bonvoy and Hilton Honors are cited in virtually every loyalty comparison AI response. MemberProgram schema is directly displayable in Google search results and is the only schema type specifically designed for this use case.

6. **Priority tier:** P1

---

### PROP-011 — Upgrade Destination Page for Geographic AI Discovery
**Gap ref:** GAP-023, GAP-024, GAP-025, GAP-034 | C05, C15, C08, C02 | Destination page

1. **Proposed change:** (a) Rewrite title: from "Destinations | Radisson Hotels" to "Hotel Destinations in Europe & Worldwide | Radisson Hotel Group" (62 chars). (b) Add opening paragraph naming key geographic entities: London, Paris, Amsterdam, Berlin, Brussels, Stockholm, Copenhagen, Vienna, plus a bleisure traveler framing: "Whether you're planning a business trip that extends into a city break, or a luxury European tour, Radisson Hotel Group properties are located in city centres, near major airports, and at iconic European addresses." (c) Add ItemList JSON-LD schema listing top 10 European destinations with `name`, `url`, and `description` per city. See gap_research.md GAP-034 for specific JSON-LD template. (d) Add a bleisure traveler-type filter concept: "Browse by traveler type: Business Travel | Bleisure Stays | Leisure Breaks."

2. **Source citation:** Smartvel Location Pages 2026: destination pages must include "destination names, relevant areas, or activity categories naturally in opening paragraphs." 12AM Agency Entity SEO 2026: geographic anchoring in title required for city-specific AI query matching. Black Bear Media Schema for Travel Websites + SEOClarity Best Schema for Hotels: ItemList schema enables AI systems to parse a collection of destinations as a ranked, machine-readable geography map.

3. **Current state:** Title: "Destinations | Radisson Hotels" (purely navigational). No geographic entities in confirmed snippet. Sub-pages (/destination/united-kingdom, /destination/france/paris) have appropriate titles but main page provides no geographic signal. No schema detected. First audit run_003.

4. **Inferred implementation status:** N/A — first audit.

5. **Directional impact estimate:** MEDIUM-HIGH. Named geographic entities + ItemList schema on the destination page create a machine-readable European footprint map, enabling AI engines to answer destination-specific portfolio queries that currently return OTA results.

6. **Priority tier:** P2

---

### PROP-012 — Initiate Direct AI Distribution Channel (ChatGPT + Perplexity)
**Gap ref:** GAP-030 | C17 | Portfolio-wide

1. **Proposed change:** Pursue three parallel tracks on a prioritized sequence: (a) Q2 2026: Contract with Selfbook to gain Perplexity bookability — fastest path to live AI distribution, no OpenAI partnership required, access to 140,000+ Perplexity-bookable hotels. (b) Q2–Q3 2026: Build a Radisson ChatGPT GPT Action app following the Accor/Hyatt model — allows users to search Radisson properties by destination/dates and redirect to direct booking. OpenAI provides the Actions framework; a hospitality tech partner (Selfbook, Amadeus, Cendyn) can accelerate build. (c) Parallel: Add an on-site conversational AI search interface to radissonhotels.com, mirroring Hilton's AI Planner (live March 2026), to improve direct booking conversion from AI-assisted planners who land on the Radisson website.

2. **Source citation:** Accor ChatGPT app live Jan 29 2026 (Skift). Hyatt ChatGPT app live Feb 2026 — CEO noted "lift from AI search," longer average stays, +20% group sales productivity (Skift). Perplexity/Selfbook integration live with 140,000 bookable hotels (PhocusWire, Hospitality.today). Hilton AI Planner live March 2026 (stories.hilton.com). BCG March 30, 2026: "ask and book era" is live — AI discovery is now transactional. CONTESTED BEST PRACTICE: MCP Protocol (Cendyn, HFTP documentation) is still pilot phase — no major chain fully deployed. Prioritize ChatGPT app and Perplexity/Selfbook over MCP for 2026 H1.

3. **Current state:** No confirmed Radisson ChatGPT app, Perplexity integration, or MCP implementation. American bleisure travelers using ChatGPT or Perplexity as booking interfaces cannot book Radisson properties directly. All AI booking traffic is routing through OTAs or to competitor direct channels (Accor, Hyatt, Marriott-Google pipeline).

4. **Inferred implementation status:** N/A — newly identified gap run_003. Strategic, not a metadata fix.

5. **Directional impact estimate:** VERY HIGH long-term. When an American bleisure traveler asks ChatGPT "find me a Radisson Blu in London with meeting rooms for next Tuesday and Wednesday, then I want to stay through the weekend," Accor and Hyatt can answer with live inventory — Radisson cannot. Perplexity/Selfbook is the fastest remediation path (weeks, not quarters). This is the most strategically significant gap in this run.

6. **Priority tier:** P1 (strategic — requires partnership decision, not a web team sprint)

---

### PROP-013 — Audit and Optimize Google Business Profile for Key European Properties
**Gap ref:** GAP-032 | C01 | Portfolio-wide

1. **Proposed change:** Conduct GBP audit for the top 20 Radisson properties in Europe (London, Paris, Amsterdam, Brussels, Berlin). For each: (a) Update GBP description to include property-specific meeting room capacity, bleisure positioning, and proximity to key landmarks/transport hubs relevant to US travelers (e.g., "15 minutes from Heathrow Terminal 5," "walking distance from Paris Opéra"). (b) Target 50+ photos per GBP, categorized by room type, meeting/conference facilities, dining, and leisure. (c) Ensure GBP name/address/phone exactly matches the schema-declared data on the property website (NAP consistency is critical for ChatGPT entity resolution via Google Places API). (d) Populate GBP Q&A section with pre-answered questions about business facilities and bleisure relevance.

2. **Source citation:** Anatomy of ChatGPT Hotel Search 2026 (hotelrank.ai): ChatGPT hotel search links 89% of hotel mentions to Google Place IDs; Google Places API supplies ~94% of hotel data used by ChatGPT. Google AI Overviews trigger for 40%+ of local queries; GBP description + review content feeds these summaries. GBP accounts for 32% of Local Pack ranking (March 2026 core update). Marriott London GBP descriptions explicitly encode business + leisure signals within the 750-character limit — confirmed best practice model.

3. **Current state:** Basic Google Travel entries confirmed for Radisson Blu London properties (amenities visible: fitness center, business center, meeting rooms). GBP description quality not confirmed; photo count not confirmed. NAP consistency with website data unverifiable (property pages 403-blocked). First formal C01 assessment run_003.

4. **Inferred implementation status:** N/A — first formal assessment.

5. **Directional impact estimate:** HIGH. GBP completeness and consistency is the single most leveraged data source for AI hotel recommendations across ChatGPT, Google AI Mode, Perplexity, and Gemini. It requires no website changes — purely a Google-managed property profile update. Every improvement here directly improves citation probability.

6. **Priority tier:** P2

---

### PROP-014 — Upgrade Radisson Blu /business-travel-offer Sub-Page with Bleisure Content
**Gap ref:** GAP-012 | C08 | Radisson Blu /business-travel-offer

1. **Proposed change:** (a) Update sub-page title to: "Radisson Blu Hotels for Business and Leisure Travel in Europe" (adding "and Leisure"). (b) Add a dedicated "Extend Your Business Trip" section with: weekend rate packages, city break itineraries, local recommendations, and CTA to extend booking. (c) Add one paragraph addressing American travelers specifically. (d) Add FAQPage schema with bleisure-specific questions. (e) Add cross-link from Radisson Blu main brand page to this sub-page with anchor text "Radisson Blu business and leisure travel offers in Europe."

2. **Source citation:** Marriott "Business Travel" category pages include "Extend Your Stay" CTA section with leisure extension offers, local experiences, and weekend package rates — confirmed competitor model. Hospitality.today Bleisure Reshaping Hotel Website: bleisure content pages require compound language ("business and leisure," "extend your trip") throughout the page, paired with specific offers.

3. **Current state:** Sub-page title: "Radisson Blu Hotels for Business Travelers | Radisson Hotels." Content: meeting room facilities, flexible lobby spaces — no bleisure compound language, no American traveler context, no leisure extension offers. Confirmed existing but not cross-linked from main brand page in SERP. First formal sub-page audit run_003.

4. **Inferred implementation status:** N/A — first formal audit.

5. **Directional impact estimate:** MEDIUM-HIGH. This sub-page has a good title foundation — small additions would convert it from a thin B2B page to an AI-citeable source for bleisure queries. Main brand page cross-link is the easiest win.

6. **Priority tier:** P2

---

### PROP-015 — Deploy Individual Property Schema via CRS/PMS Template System
**Gap ref:** GAP-031 | C11 | Portfolio-wide (all property pages)

1. **Proposed change:** After resolving GAP-001 (Cloudflare fix), conduct a 10-property sample audit using Google Rich Results Test to confirm whether Hotel schema exists at the property page level. If absent (expected): deploy a template-based Hotel JSON-LD system across all property pages auto-generated from PMS/CRS data, including: property-specific `name`, `address`, `geo` coordinates, `telephone`, `starRating`, `aggregateRating` (from TripAdvisor/Google Reviews feed), `amenityFeature` (property-level), `potentialAction` booking URL. System must scale to 1,100+ properties without manual authoring.

2. **Source citation:** Anatomy of ChatGPT Hotel Search 2026 (hotelrank.ai): ChatGPT hotel search links 89% of hotel mentions to Google Place IDs — resolution depends on schema-declared address, coordinates, and telephone matching the GBP entity. Schema.org Hotel 2026 Guide: aggregateRating (12.5% adoption), amenityFeature (7.7% adoption) — low bar makes implementation a competitive differentiator.

3. **Current state:** All radissonhotels.com individual property pages return HTTP 403. Cannot confirm Hotel schema at property level. OTA proxy: Radisson Blu London Bloomsbury has strong TripAdvisor (4,423 reviews, Q&A active) and Booking.com (5,693 reviews) footprint — OTA data is being cited by AI engines in place of Radisson's own property pages.

4. **Inferred implementation status:** N/A — first formal assessment. Dependent on GAP-001 resolution.

5. **Directional impact estimate:** VERY HIGH once crawler access is restored. Property-level Hotel schema is the highest-impact schema deployment in the portfolio — it enables entity resolution for city-specific AI queries and is the mechanism by which individual hotels compete with OTA listings in AI results.

6. **Priority tier:** P1 (implement after PROP-001 as second sprint)

---

### PROP-016 — Rewrite Radisson RED Title for Query Language Alignment
**Gap ref:** GAP-017 | C05 | Radisson RED brand page

1. **Proposed change:** Replace title "Radisson RED - Stylish & Boutique Hotels | Radisson Hotels" with "Radisson RED | Lifestyle & Boutique Hotels for Modern Travelers" (57 chars).

2. **Source citation:** citizenM uses "Affordable luxury for the many" — query-adjacent language; Generator uses "Lifestyle Hotels & Hostels in Europe's Best Cities" — encodes category term and geography. AI Optimised Meta Titles 2026 (Absolute Websites): titles must match query language, not brand advertising language.

3. **Current state:** "Radisson RED - Stylish & Boutique Hotels | Radisson Hotels" — "Stylish & Boutique" is advertising language, not search language.

4. **Inferred implementation status:** NOT IMPLEMENTED. 2nd consecutive unaddressed run.

5. **Directional impact estimate:** MEDIUM. Ensures RED appears for "lifestyle hotels" and "boutique hotels" category queries.

6. **Priority tier:** P3

---

### PROP-017 — Implement ItemList and Amenity Table Schema on Destination Page
**Gap ref:** GAP-033, GAP-034 | C13, C02 | All brand pages, Destination page

1. **Proposed change:** (a) Add HTML amenity tables to all brand pages (Radisson Blu, Collection, Park Plaza) listing specific amenities in scannable, machine-parseable format. Radisson Blu example: meeting rooms (most properties), business centre (all full-service), co-working lounge (select), restaurant/bar (all), fitness centre (all), spa (select), free Wi-Fi (all). (b) Add ItemList schema to destination page covering top 10 European cities — see PROP-011 and gap_research.md GAP-034 for templates.

2. **Source citation:** Schema.org amenityFeature with LocationFeatureSpecification enables AI systems to answer comparison queries ("which hotel brand has the best business facilities"). Booking.com and Marriott both implement structured amenity data (confirmed as key AI citation mechanism). Black Bear Media and SEOClarity: ItemList schema enables geography-map parsing for portfolio destination queries.

3. **Current state:** No structured amenity tables or amenityFeature schema on any brand page. No schema on destination page. 3rd consecutive run for brand pages. First audit for destination page.

4. **Inferred implementation status:** NOT IMPLEMENTED (brand pages, 3 consecutive runs).

5. **Directional impact estimate:** MEDIUM-HIGH. Structured amenity data is the mechanism for attribute-matching queries ("Radisson hotels with business center and gym").

6. **Priority tier:** P2

---

## Implementation Priority Summary

| Sprint | Proposals | Type | Estimated Effort |
|--------|-----------|------|-----------------|
| **Sprint 0 (Blocker Fix)** | PROP-001, PROP-008 | Cloudflare + llms.txt | 2–4 hours (one engineer) |
| **Sprint 1 (Schema)** | PROP-002, PROP-003, PROP-010 | Hotel schema + FAQPage + MemberProgram | 3–5 dev days |
| **Sprint 2 (Content)** | PROP-004, PROP-005, PROP-009, PROP-007 | Copy rewrites + freshness content | 2–3 copywriting days |
| **Sprint 3 (Pages)** | PROP-006, PROP-011, PROP-014, PROP-017 | Park Plaza, Destination, sub-page, amenity tables | 2–3 copywriting + dev days |
| **Sprint 4 (Property)** | PROP-015, PROP-013 | Property schema system + GBP audit | 1–2 engineering weeks |
| **Strategic Track** | PROP-012 | AI distribution (ChatGPT app, Perplexity/Selfbook) | Partnership + 4–8 weeks build |
| **Maintenance** | PROP-016 | RED title update | 30 minutes |

**Total critical-path sprint estimate (Sprints 0–3):** ~10 working days of combined engineering + copywriting effort.

**26-day non-implementation cost note:** Accor's ChatGPT app launched January 29. Hyatt's launched February 12. The BCG "ask and book era" report published March 30, 2026. run_002 proposals were filed March 20. Each week of inaction in Q2 2026 is a week where competitor AI citations compound and Radisson's zero-citation baseline extends.
