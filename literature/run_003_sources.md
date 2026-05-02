# Literature Findings — run_003 | 2026-04-15

## Research Questions Addressed
1. Which AI engines are currently dominant for travel and hotel discovery?
2. What signals do dominant engines use to surface hotel results?
3. Current best-evidenced GEO/AEO practices for hospitality?
4. What metadata/content structures do hospitality leaders and OTAs use?
5. What content patterns and query types does an American bleisure traveler use via AI engines?

---

## FINDING 1 — Dominant AI Engines for Travel & Hotel Discovery (April 2026)

**Sources:**
- https://www.mylighthouse.com/resources/blog/chatgpt-is-the-new-front-door-for-hotel-discovery
- https://www.phocuswire.com/hotels-push-live-chatgpt-integrations-ai-search-goes-bookable
- https://www.triptease.com/resources/perplexity-ai-hotel-search-agent
- https://www.hospitality.today/article/what-direct-ai-hotel-distribution-looks-like
- https://www.biztechreports.com/news-archive/2026/3/19/hotels-enter-the-ask-and-book-era-as-ai-reshapes-discovery-distribution-and-operations-bcg-march-19-2026

**Key platforms (April 2026, in order of travel discovery relevance):**
1. **ChatGPT (OpenAI)** — 900M users; dominant AI discovery platform; Accor launched native ChatGPT app Jan 29 2026; Hyatt launched branded ChatGPT app Feb 2026; GPT-5 significantly expanded web search depth; bookable via OTA integrations
2. **Google AI Overviews / Gemini** — triggers for 40%+ of local queries; Marriott-Google direct integration live; Google Places powers ~94% of hotel data surfaced in AI responses; March 2026 core update deepened local GBP signals
3. **Perplexity** — launched hotel search agent with Selfbook + TripAdvisor integration; 140,000 bookable hotels in-platform; agentic travel planning; accesses Tripadvisor data (95.5% citation share on Perplexity)
4. **Claude (Anthropic)** — ClaudeBot active crawler; growing for complex travel planning queries
5. **Grok (xAI)** — emerging; lower travel domain share but growing with X/Twitter data integration
6. **Apple Intelligence / Siri** — Applebot-Extended crawler active; increasingly relevant for mobile-first US travelers

**What changed since run_002 (2026-03-20):**
- BCG March 30, 2026 report confirms "ask and book era" has arrived — AI discovery is now transactional, not just informational
- Marriott-Google AI direct booking pipeline confirmed as live — most significant competitive threat to independent hotel chains without such partnerships
- Perplexity hotel booking fully live (was "developing" in prior runs); TripAdvisor integration confirmed
- AI adoption among travelers: ~50% in 2025, projected 70%+ in 2026

---

## FINDING 2 — AI Engine Signals for Hotel Surface Results

**Sources:**
- https://hotelrank.ai/research/hotel-schema-adoption-study-2026
- https://www.nokumo.net/en/blog/how-does-ai-recommend-hotels-we-tested-450-queries-across-4-models-to-find-out
- https://metricusapp.com/blog/travel-ai-visibility/
- https://wellows.com/blog/ai-search-visibility-for-hospitality-brands/
- https://kismet.travel/blog/how-to-beat-the-otas-booking-com-expedia-at-ai-search

**Measured signal weights for AI hotel recommendations (Nokumo 450-query study):**
- URL quality / domain authority: 0.60 (largest factor)
- Trust signals (reviews, ratings, backlinks from authoritative travel publications): 0.50
- Content quality (factual, informational, answer-ready copy): 0.36
- Schema markup: 0.23 (smallest measured direct effect, but enables the above)

**OTA vs. brand advantage:**
- Properties with comprehensive OTA listings (Booking.com, Expedia) + TripAdvisor (500+ reviews) are cited far more frequently
- Booking.com: 54% ChatGPT citation share, 63% Gemini — unchanged from run_002 but confirmed fresh
- Marriott: 224 AI citations from 40 tracked queries (vs. Hilton 125, Hyatt 87, IHG 54) — Marriott's schema + Google integration driving outsized citation advantage
- Hotels blocking AI crawlers cited 73% less in ChatGPT — confirmed persistent

**New signals identified this run:**
- GBP (Google Business Profile) accounts for 32% of Local Pack ranking; combined with reviews (16%) = 48% of algorithm — **GBP completeness is now formally a Tier 1 signal**
- Editorial mentions in authoritative travel publications significantly boost AI citation probability
- Perplexity's TripAdvisor integration means TripAdvisor review volume/recency is now a direct Perplexity ranking input (not just indirect)

---

## FINDING 3 — GEO/AEO Best Practices for Hospitality (2026)

**Sources:**
- https://www.orourkehospitality.com/insights/what-is-generative-engine-optimization-for-hotels/
- https://tryxlr8.ai/blogs/geo-generative-engine-optimization-for-travel-hospitality
- https://apycue.com/blog/geo-for-hotels
- https://lseo.com/generative-engine-optimization/generative-engine-optimization-geo-for-hospitality-travel/
- https://www.sojern.com/blog/is-your-hotel-ai-ready-7-strategies-for-geo-success
- https://www.hospitality.today/article/bleisure-travel-is-reshaping-the-hotel-website

**Confirmed best practices:**
1. **Schema markup**: Hotel/LodgingBusiness with aggregateRating, amenityFeature, geo, checkinTime, checkoutTime — still only 10.6% of hotels have good schema; being in the top 7% requires these fields
2. **FAQPage schema**: Confirmed for AI parsability (not SERP display — Google 2023 policy unchanged). Q&A blocks in page copy + FAQPage JSON-LD = strong AI Q&A extraction signal
3. **Informational register in first 80 words**: Content cited at 62% higher rate when factual/informational vs. marketing register (Search Engine Land study — still current)
4. **Answer-ready content structure**: Heading + FAQ block + bulleted lists = higher AI parsability vs. flowing marketing prose
5. **AI crawler access**: Allowing GPTBot, PerplexityBot, ClaudeBot, Google-Extended, Applebot-Extended is prerequisite
6. **llms.txt**: Still early adoption (~limited measurable traffic impact per John Mueller), but growing as AI-protocol complement to robots.txt. Low-effort, good faith signal
7. **GBP completeness**: Now formally a Tier 1 signal — photos, description with amenity keywords, Q&A section, service attributes
8. **OTA listing quality**: TripAdvisor (500+ reviews), Booking.com (complete amenity attributes) now primary Perplexity + ChatGPT citation sources
9. **Bleisure content signals**: Pages with explicit "business and leisure," flexible workspace mentions, and meeting + leisure combination content outperform for bleisure queries
10. **Geographic specificity**: Content naming specific neighborhoods, proximity to business districts, transport links cited more reliably in AI hotel recommendations

---

## FINDING 4 — Competitor Metadata Strategies (Marriott, Hilton, OTAs)

**Sources:**
- https://otelciro.com/en/news/marriott-google-ai-direct-booking
- https://www.hospitality.today/article/hilton-uses-ai-to-bring-travelers-back-to-direct-booking-channels
- https://wellows.com/blog/ai-search-visibility-for-hospitality-brands/
- https://www.advicelocal.com/blog/2026-local-search-ranking-factors-maps-organic-ai/

**Marriott (leading AI citation share, 224 citations / 40 queries):**
- Real-time inventory + pricing pushed to Google via enhanced schema markup and direct API
- AI-native content formatted specifically for LLM consumption
- Inventory, pricing, room imagery, reviews, loyalty perks appear natively in Google AI search results
- Marriott Bonvoy loyalty program prominently surfaced in AI responses as a differentiator for US travelers

**Hilton (125 citations / 40 queries):**
- Conversational planning tool directly on Hilton.com — influencing travelers at discovery stage
- AI-driven direct booking to reduce OTA dependence
- Loyalty program (Hilton Honors) integrated into AI recommendations

**Booking.com (54% ChatGPT citation share):**
- AI Trip Planner in 40+ languages; first-mover ChatGPT app ecosystem integration
- Full FAQPage + LodgingBusiness schema pipeline
- Complete amenity attributes, review volume maintained at scale
- Expedia: acquired PredictHQ; Affirm partnership for AI-powered dynamic packaging

**What Radisson lacks vs. competitors:**
- No Marriott-style Google API integration
- No confirmed AI-native formatting of content
- No loyalty-program AI discoverability
- No direct AI booking channel (no ChatGPT/Perplexity native integration confirmed)

---

## FINDING 5 — American Bleisure Traveler AI Query Behavior (2026)

**Sources:**
- https://www.hospitality.today/article/bleisure-travel-is-reshaping-the-hotel-website
- https://www.thereputationlab.com/travel-search-trends/
- https://geneo.app/blog/geo-travel-hospitality-ai-visibility/
- https://www.biztechreports.com/news-archive/2026/3/19/hotels-enter-the-ask-and-book-era-as-ai-reshapes-discovery-distribution-and-operations-bcg-march-19-2026

**Behavioral profile (2026):**
- 37% of travelers use AI LLMs embedded in travel sites for planning/booking
- AI adoption projected to reach 70%+ among travelers in 2026 (from ~50% 2025)
- Bleisure is now "mainstream demand pattern" not niche — travelers expect seamless work+leisure blend from hotel website
- Micro-trips and bleisure are accelerating as AI reduces friction in planning

**Query types used by American bleisure travelers for European hotel search:**
- "Hotels in [city] good for remote work with meeting rooms" (complex multi-attribute)
- "Best hotels in London near financial district for business travelers" (location + use case)
- "Hotels in Amsterdam that work for both business meetings and sightseeing" (dual-purpose)
- "Upscale hotels in Europe for American business travelers with good Wi-Fi and gym" (attribute-led)
- Loyalty-driven: "What Marriott/Hilton alternatives have loyalty programs in European cities"

**Content signals that answer these queries:**
- Explicit "business and leisure" or "bleisure" terminology in page copy
- Meeting room availability + capacities listed on brand pages
- Proximity to business districts named explicitly
- Wi-Fi speed/type mentioned
- Loyalty program benefits described for American travelers specifically
- Flexible check-in/check-out referenced

---

## Synthesis: What Changed Since run_002

1. **AI booking is now transactional** — Perplexity (Selfbook/TripAdvisor), ChatGPT integrations, Marriott-Google pipeline all live. Not just discovery; actual bookings happening through AI. Hotels without direct AI distribution are losing bookings, not just citations.

2. **GBP is now Tier 1** — March 2026 Google core update deepened GBP signals. 32% of Local Pack ranking. Incomplete GBP for flagship Radisson properties is now a higher-severity gap than in prior runs.

3. **TripAdvisor is a Perplexity ranking input** — confirmed via Selfbook partnership. Review volume (500+ threshold) and recency directly affect Perplexity hotel search ranking. European Radisson properties with weak TripAdvisor footprint are at risk.

4. **Marriott's AI gap over Radisson is widening** — Marriott went from "leading AI citations" (run_002) to having a live Google API integration. The gap between Radisson and Marriott in AI visibility is likely larger in April 2026 than March 2026.

5. **llms.txt still early-stage** — John Mueller (Google) confirmed no AI crawlers currently extracting information via llms.txt. Still worth implementing (low effort, future-proofing) but should not be prioritized above schema and crawler access.

6. **Apple Intelligence confirmed as new crawler category** — Applebot-Extended now formally relevant. If Radisson's Cloudflare WAF blocks this too, another AI platform losing access.
