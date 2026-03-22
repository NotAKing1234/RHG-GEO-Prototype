# Literature Findings — run_002 | 2026-03-20

## Research Method
Live web search conducted on 2026-03-20. Five research questions queried via WebSearch. Direct page fetches of radissonhotels.com continue to return HTTP 403; literature sourced from web search results, industry reports, and secondary research platforms.

---

## Q1: Which AI Engines Are Currently Dominant for Travel and Hotel Discovery?

**Findings (March 2026):**

Based on HotelRank.ai analysis of 245,046 unique sources across 19,579 AI runs on 2,500 unique prompts (25 cities, 8 personas, 9 hotel types):

- **ChatGPT (GPT-5.x):** Dominant engine. GPT 5.2 doubled web search depth vs 5.1, now cites direct hotel sources more than any other model except Perplexity. Booking.com leads in GPT 5.2 citation share (54%). Less Wikipedia reliance (75%→30%) and less Reddit (14.6%→2.3%). Google powers ~94% of ChatGPT hotel data via SerpAPI (web search) and Google Places (entity data). Yelp integrated January 2026 for US cities + Berlin. 800M+ weekly active users.
- **Gemini:** Booking.com leads Gemini citations (63%). YouTube heavily preferred for social/media content citations (Google ecosystem integration).
- **Perplexity:** TripAdvisor dominant at 95.5% citation share. Real-time web search + Tripadvisor data partnership. PerplexityBot known to have circumvented robots.txt via headless browser in some cases (Cloudflare documented).
- **Grok:** Social platforms and UGC dominate. Expedia + Hotels.com + Travelocity combined reach 99%+ in Grok responses. Twitter/X data integration prominent.
- **Emerging:** Amex AI concierge, Chase AI travel agent — autonomous booking agents that bypass traditional search entirely.

**Key change vs run_001:** GPT-5.2 is confirmed as updated model with significantly deeper web search (double the depth). Yelp added as live data source for hotel data in ChatGPT. Perplexity's robots.txt evasion is now documented via Cloudflare.

**Sources:**
- https://hotelrank.ai/research/ai-hotel-landscape-2026
- https://hotelrank.ai/research/anatomy-chatgpt-hotel-search-2026
- https://vertu.com/lifestyle/ai-chatbot-market-share-2026-chatgpt-drops-to-68-as-google-gemini-surges-to-18-2/
- https://docs.perplexity.ai/docs/resources/perplexity-crawlers
- https://blog.cloudflare.com/perplexity-is-using-stealth-undeclared-crawlers-to-evade-website-no-crawl-directives/

---

## Q2: What Signals Do Dominant Engines Use to Surface Hotel Results?

**Findings:**

1. **OTA citation dominance:** All AI models scan an OTA/Meta 50%+ of the time. Booking.com is #1 in ChatGPT/Gemini. TripAdvisor is #1 in Perplexity/Grok. Hotels not appearing on these OTAs are algorithmically invisible.

2. **Review scores and volume:** AI systems use review scores from Google, Booking.com, and Expedia. High review scores = higher recommendation probability.

3. **Data consistency across sources:** GPT-5.2's doubled search depth means consistency across 10+ sources matters more than ever. Hotels cited on only 2-3 sites lose to competitors on 10+.

4. **Google Business Profile:** Google Places provides entity data to ChatGPT (~94% of ChatGPT hotel data routes through Google). Fully completed GBP is prerequisite for ChatGPT hotel recommendations.

5. **Structured data machine-readability:** "Unified Digital Shelf" — if hotel assets (rooms, dining, spa, experiences) aren't digitized into structured data or machine-readable APIs, they are invisible to AI booking agents.

6. **Content structure on website:** Headings, FAQ blocks, bulleted lists, tables — parseable by AI scrapers. FAQPage schema, Hotel/LodgingBusiness schema.

7. **Brand presence in AI model training data:** Top-cited brands in AI recs — Marriott leads all models (GPT 5.1 at 39%); Perplexity prefers Four Seasons (21%), Ritz-Carlton (18%).

**What changed vs run_001:** GPT-5.2 confirmed with doubled depth. Google Places/SerpAPI pipeline to ChatGPT now documented. Yelp added as data source. Autonomous AI agents (Amex, Chase) confirmed as new channel that bypasses both SEO and GEO entirely — requiring direct API integrations.

**Sources:**
- https://hotelrank.ai/research/anatomy-chatgpt-hotel-search-2026
- https://hotelrank.ai/research/ai-hotel-landscape-2026
- https://www.customer-alliance.com/en/articles/ai-hotel-recommendations-visibility-chatgpt-search/
- https://www.hospitalitynet.org/whitepaper/4131059/ai-is-now-how-travellers-find-hotels-hotelworld-ai-launches-worlds-best-at-ai-index

---

## Q3: Current Best-Evidenced GEO/AEO Practices for Hospitality

**Findings:**

1. **Triple JSON-LD schema stacking:** Best practice for hotel ranking pages is Article + ItemList + FAQPage stacked. Hotel/LodgingBusiness schema at property level. Required for rich result eligibility.

2. **74.2% of AI citations from structured "Top N" content:** Build listicle-format content (e.g., "Top 5 hotels in London for business travelers") on website and partner sites. ItemList schema on all list pages.

3. **Quick answer blocks above the fold:** Answer the key traveler question in the first 40-80 words. ALM Corp study (run_001): 44% first-third citation rule. Still confirmed in 2026.

4. **FAQ content on every page:** FAQPage schema implementation. Questions must match natural language queries travelers use with AI engines.

5. **Content freshness:** AI models deprioritize stale content. Version history and verification windows recommended. Publishing 1-2 new listicles per week maintains citation frequency. (GenOptima, 2026)

6. **Question-focused content development:** Content should answer real traveler questions using internal data, expert insights, and local knowledge — not marketing copy.

7. **Google Business Profile completeness:** Required for ChatGPT hotel data pipeline.

8. **OTA listing optimization:** Both Booking.com and TripAdvisor must have complete, keyword-rich listings. These are primary citation sources for 3 of 4 dominant AI engines.

9. **llms.txt emerging:** New protocol being adopted — structured file at /llms.txt that explicitly tells AI engines what content is available. Analogous to robots.txt but for AI accessibility.

10. **robots.txt AI crawler strategy:** Distinction between training crawlers (GPTBot, Google-Extended, CCBot — block for training) vs retrieval crawlers (ChatGPT-User, Claude-Web, PerplexityBot — allow for real-time citation). Perplexity known to evade robots.txt via headless browsers.

**Sources:**
- https://www.gen-optima.com/blog/generative-engine-optimization-best-practices-complete-2026-playbook/
- https://tryxlr8.ai/blogs/geo-generative-engine-optimization-for-travel-hospitality
- https://lseo.com/generative-engine-optimization/generative-engine-optimization-geo-for-hospitality-travel/
- https://www.becurious.com/generative-engine-optimization-for-hotels-download-checklist
- https://www.travelboommarketing.com/blog/generative-engine-optimization-for-hotels
- https://higoodie.com/blog/llms-txt-robots-txt-ai-optimization
- https://witscode.com/blogs/robots-txt-strategy-2026-managing-ai-crawlers/
- https://dev.to/william_geo/the-complete-guide-to-ai-crawler-management-in-2026-6ai

---

## Q4: Metadata and Content Structures Used by Hospitality Leaders and OTAs

**Findings:**

**Marriott (leading AI visibility):**
- AI Assistant launched Q1 2026. $1B+ technology investment in 2026 including cloud-native platform migration.
- Marriott-Google AI direct booking integration launched — bypasses OTAs via natural language search.
- AI-compatible hotel data platform — all room categories, dining, spa, experiences digitized into machine-readable APIs.
- Leads AI recommendations: 39% in GPT 5.1, consistent across all models.

**Hilton:**
- AI Planner launched March 2026 — personalized itinerary builder.
- Uses AI to drive travelers back to direct booking channels.
- Structured data and schema implementation mature.

**Accor:**
- ChatGPT MCP integration confirmed (Jan 2026) — direct AI-to-booking capability.

**IHG:**
- AI-compatible hotel data platform launched Feb 2026.

**Booking.com:**
- Full FAQ and schema architecture. Primary AI citation winner for ChatGPT and Gemini.
- AI Trip Planner with visual itineraries using real-time reviews.
- Schema markup for listings + structured content understanding signals.

**Expedia:**
- Consistent OTA presence. Machine-readable listing data.

**TripAdvisor:**
- Primary data source for Perplexity (95.5%). Extensive user review data, structured listing format.

**OTA Common Patterns:**
- Complete structured data on all listing pages (Hotel, LodgingBusiness, Review, AggregateRating schema)
- FAQ content on destination and property pages
- Machine-readable amenity data (not just prose descriptions)
- Content consistency across multiple platforms

**Key change vs run_001:** Marriott-Google direct AI booking confirmed as active (not future-tense). Hilton AI Planner live March 2026. MCP integrations (Accor, potentially others) are now a distinct AI distribution channel.

**Sources:**
- https://www.hospitalitynet.org/opinion/4130881/what-you-must-take-away-from-marriott-google-ai-direct-booking
- https://travhotech.com/marriott-google-ai-direct-booking-strategy/
- https://otelciro.com/en/news/hilton-ai-planner-yarisina-girdi
- https://www.klover.ai/hilton-ai-strategy-analysis-of-dominance-in-hospitality-hotel-ai/
- https://www.seoclarity.net/blog/the-best-schema-markup-for-hotels-and-travel-sites
- https://hoteltechnologynews.com/2026/02/marriott-advances-technology-migration-as-ai-strategy-moves-into-deployment/

---

## Q5: American Bleisure Traveler Query Patterns for AI-Assisted Hotel Discovery

**Findings:**

**Bleisure prevalence (2026):**
- 83% of business travelers have taken a bleisure trip in the past year.
- 89% of travelers want to add leisure time to their next business trip.
- American business travelers take 405M+ long-haul business trips per year; ~60% add leisure.
- Bleisure Travel Market valued at $445B (2024) → $764B projected by 2032.
- 55% of Millennials/Gen Z in Asia added leisure to business trips vs 29% in North America.

**AI-driven query transformation:**
- Travelers won't type hotel preferences into search forms — they'll describe requirements to an AI agent once.
- AI agent cross-references live pricing, sentiment, sustainability, loyalty preferences, then books.
- Amex/Chase AI concierges researching, comparing, booking without the traveler visiting a search engine.
- Query shift: from keyword fragments → to natural language compound requirements ("hotel in London with meeting rooms, fast WiFi, close to the City, good restaurant, fitness center, available Thursday-Sunday").

**European destination patterns:**
- London top business + bleisure destination for Americans.
- Strong business infrastructure + leisure appeal combination = highest AI recommendation scores.
- Key query types for American bleisure travelers:
  - "Best hotel in London for business meetings with weekend leisure options"
  - "Hotels near London financial district with spa and good restaurants"
  - "Radisson Blu London — is it good for American business travelers?"
  - "Hotels in London with conference rooms and easy airport access from JFK"
  - "Where to stay in London for a week mixing work and sightseeing"

**Content alignment needed:**
- Compound bleisure content (business + leisure on same page) performs best.
- American-specific signals: direct flights from US cities, US plug adapters, USD pricing visibility, English-speaking staff.
- Trust signals: Radisson Rewards loyalty parity with US expectations (compared to Marriott Bonvoy, Hilton Honors).

**Sources:**
- https://www.wisk.ai/blog/bleisure-travel-travel-trends-hotels-cant-ignore-in-2026
- https://hoteltechreport.com/news/bleisure-statistics
- https://www.hospitality.today/article/bleisure-travel-moves-into-the-mainstream-of-corporate-travel
- https://www.hospitalitymarketinginsight.com/p/how-ai-search-is-reshaping-hospitality

---

## Synthesis: What Changed Since run_001

1. **GPT-5.2 confirmed** with 2x search depth — source breadth matters more than ever. Radisson's minimal web presence across review sites is now a harder disadvantage.
2. **Yelp added to ChatGPT** (January 2026) — another data source Radisson must have a presence on.
3. **Marriott-Google direct booking integration confirmed active** — the competitive moat is widening. Radisson has no comparable direct AI integration.
4. **Perplexity's robots.txt evasion documented** — if Radisson's 403 blocking also blocks Perplexity's headless browser crawler, they may be partially visible to Perplexity despite blocking; if it doesn't, they may still be partially invisible. The 403 issue is more complex than run_001 characterized.
5. **llms.txt emerging as new AI accessibility protocol** — opportunity Radisson can implement cheaply and immediately.
6. **Autonomous AI travel agents (Amex, Chase)** — new channel requiring structured API data, not just web metadata. Radisson currently has no confirmed integration.
7. **Radisson FAQ page confirmed to exist** (https://www.radissonhotels.com/en-us/faq) — this page was not in the run_001 audit. Must audit in run_002.
