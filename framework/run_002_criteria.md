# GEO Criteria Framework — run_002 | 2026-03-20

Synthesized from live literature research conducted on 2026-03-20. Updated from run_001 criteria based on new findings: GPT-5.2 deeper web search, Yelp integration, Marriott-Google direct booking, llms.txt emergence, Perplexity robots.txt evasion documentation.

---

## C01 — Hotel / LodgingBusiness Schema
**Signal name:** Hotel or LodgingBusiness JSON-LD structured data
**Why it matters:** Google Places pipeline powers ~94% of ChatGPT hotel data. Schema enables rich result eligibility. Machine-readable amenity data is the foundation for AI booking agent recommendations. "If an asset isn't digitized, it remains invisible to AI search agents." (Marriott-Google AI direct booking analysis, 2026)
**What passing looks like:** JSON-LD block with @type Hotel or LodgingBusiness present in page source, with name, address, telephone, priceRange, amenityFeature, and starRating populated. Rich results visible in Google SERP (star ratings, price range).
**How to check:** Attempt page source fetch; if blocked, check Google SERP for rich result snippets (hotel card, star rating, amenity list). Use Google Rich Results Test URL inference.
**Bleisure relevance:** Hotel schema with amenityFeature including meeting rooms, WiFi, fitness center directly answers bleisure traveler queries routed through AI.

---

## C02 — FAQPage Schema
**Signal name:** FAQPage JSON-LD structured data
**Why it matters:** FAQPage schema generates rich result appearances in Google SERP. AI engines parse FAQ content as answer-ready text. 74.2% of AI citations come from structured "Top N" or Q&A content. ALM Corp: 44% first-third citation rule.
**What passing looks like:** FAQPage JSON-LD block with at least 5 traveler-intent Q&As. Questions match natural language queries ("Is Radisson Blu good for business travelers?", "Does Radisson have conference rooms in London?"). Rich result FAQ accordion visible in SERP.
**How to check:** Google SERP "People also ask" appearances for brand/destination pages; SERP snippet inspection for FAQ rich results.
**Bleisure relevance:** FAQ content that explicitly addresses bleisure queries ("Can I extend my business stay for a weekend?", "What leisure amenities are available at Radisson Blu?") directly surfaces in AI travel discovery answers.

---

## C03 — Meta Description Quality (Informational Register)
**Signal name:** Meta description in informational/answer register (not marketing CTA register)
**Why it matters:** AI engines extract meta descriptions as summary text. Marketing CTAs ("Book today!", "best rates guaranteed") are not citable by AI as answers to traveler queries. Informational register meta descriptions are directly usable as AI citation text.
**What passing looks like:** Meta description of 150-160 characters that answers a traveler query, states category (hotel brand / upscale), location coverage (European cities), and target traveler type. No CTAs, no superlatives without factual backing.
**How to check:** Google SERP snippet text for each URL. Compare register against Booking.com/Marriott equivalent pages.
**Bleisure relevance:** Meta descriptions that mention business amenities + leisure features match compound bleisure queries.

---

## C04 — Title Tag Optimization (Query Alignment)
**Signal name:** Page title tag aligned to AI discovery queries rather than brand taglines
**Why it matters:** Title tags are primary signals for topic identification by AI systems. Tagline-dominated titles ("Yes I Can! Attitude") are not parseable as answers to traveler questions. Query-aligned titles ("Radisson Blu Hotels in Europe | Business & Leisure Travel") are.
**What passing looks like:** Title includes brand name, geographic scope (if applicable), and functional descriptor matching traveler query vocabulary. Max 60 characters. No pure taglines.
**How to check:** Google SERP title for each URL.
**Bleisure relevance:** Titles with "business travel," "bleisure," or city + amenity terms align to AI query patterns.

---

## C05 — FAQ / Q&A Content Blocks (On-Page)
**Signal name:** Visible FAQ or Q&A content block on page (separate from FAQPage schema)
**Why it matters:** Even without schema, crawlable FAQ content can be cited by AI engines. Content in Q&A format is structurally preferred for AI citation. The first 40-80 words of each answer block are most likely to be cited (ALM Corp 44% rule).
**What passing looks like:** Visible FAQ section with 5+ questions, answers starting with a direct response in the first sentence, questions using natural traveler language.
**How to check:** SERP snippet inspection; search for the page + "FAQ" or "frequently asked questions".
**Bleisure relevance:** Q&As addressing compound traveler needs ("Do your London hotels have meeting rooms I can use for a business trip?") directly serve bleisure query patterns.

---

## C06 — Open Graph Tags
**Signal name:** Open Graph metadata (og:title, og:description, og:image, og:type)
**Why it matters:** OG tags are read by social platforms and increasingly by AI scraping pipelines. og:type="website" or "place" gives entity classification signals. Incomplete OG reduces social shareability and can affect how AI summarizers describe the page.
**What passing looks like:** og:title, og:description, og:image, og:type all populated. og:description in informational register. og:image relevant to hotel/brand.
**How to check:** Source fetch (if available); indirect: Facebook debugger, LinkedIn post inspector, or OG tag validators with cached data.
**Bleisure relevance:** OG description contributing to AI summary of the brand/page.

---

## C07 — Named Entity Clarity (Brand + Location + Category)
**Signal name:** Named entity signals establishing Radisson brand, location, and category
**Why it matters:** AI engines rely on named entity recognition to associate a hotel brand with specific cities, traveler types, and service categories. Weak entity signals = lower recall probability in AI responses. GPT-5.2 doubled search depth, so entity consistency across sources is critical.
**What passing looks like:** Brand name, specific geographic entities (city names, landmarks, districts), hotel category (upscale, business hotel, resort), and service type (conference facilities, loyalty program) all named explicitly in page content.
**How to check:** SERP snippet text; search for "[brand] [city]" queries and inspect how the AI/SERP presents Radisson vs competitors.
**Bleisure relevance:** Entity associations that include both "business travel" and "leisure" or "weekend" signals enable AI to route bleisure queries to Radisson.

---

## C08 — Traveler Type Signals (Business / Bleisure / American)
**Signal name:** Explicit traveler type signals for business travelers, bleisure travelers, and/or American travelers
**Why it matters:** AI engines parse query intent to match traveler type with hotel recommendations. Pages that don't explicitly name target traveler types are not recalled for traveler-type queries. American-specific signals (US flight connections, USD pricing, English staff) improve relevance for US-origin queries.
**What passing looks like:** Explicit mention of business travelers, bleisure, American guests, US-to-Europe travelers, or corporate travel in page content or metadata.
**How to check:** SERP snippet text; site search for "business travelers", "bleisure", "American".
**Bleisure relevance:** Direct signal for the target audience.

---

## C09 — Content Register (Informational vs Marketing)
**Signal name:** Body content uses informational register, not pure marketing register
**Why it matters:** AI engines cite factual content at 62% higher rate than marketing copy (Search Engine Land 8,000-citation study — first reported run_001, still current). Superlatives without factual backing ("unparalleled service") are not citable. Specific facts ("9 brands, 1,100+ hotels across 95 countries") are.
**What passing looks like:** Page body contains factual statements about hotel attributes, amenities, locations, and guest experiences. Marketing voice can co-exist but must be layered on factual foundation.
**How to check:** SERP snippet body text; compare against competitor brand pages.
**Bleisure relevance:** Factual content about business amenities (meeting rooms, fast WiFi, executive floors) and leisure amenities (restaurants, spas, city location) enables AI to construct compound bleisure recommendations.

---

## C10 — Content Freshness Signals
**Signal name:** Content publication/update date signals visible to AI crawlers
**Why it matters:** AI models deprioritize stale content. Version history, publication dates, and "last reviewed" dates are freshness signals. GenOptima 2026: mandatory freshness elements include verification windows.
**What passing looks like:** Article/page has visible publication or update date. Structured data includes dateModified or datePublished. Content is refreshed at least quarterly.
**How to check:** SERP snippet for date display; page source dateModified in structured data; compare SERP snippet dates across pages.
**Bleisure relevance:** Fresh content signals that hotel information (availability, amenities, pricing) is current.

---

## C11 — AI Crawler Access (robots.txt + 403 behavior)
**Signal name:** AI retrieval crawlers are permitted to access the site
**Why it matters:** Documented in run_001 as critical gap. Blocking bots = zero AI citability. In 2026, best practice is to distinguish training crawlers (block) from retrieval crawlers (allow): allow ChatGPT-User, Claude-Web, PerplexityBot for real-time citation; block GPTBot, CCBot, Google-Extended for training. Perplexity documented bypassing robots.txt via headless browser (Cloudflare, 2025).
**What passing looks like:** robots.txt explicitly allows retrieval crawlers. 403 behavior does not trigger for AI-identified user agents. Or: /llms.txt file exists that explicitly lists accessible content for AI engines.
**How to check:** Fetch /robots.txt (if accessible); infer from 403 behavior whether blanket blocking is in effect; check /llms.txt.
**Bleisure relevance:** Without crawler access, zero visibility in any AI engine — affects all traveler types equally.

---

## C12 — OTA Listing Completeness (Booking.com, TripAdvisor, Expedia, Yelp)
**Signal name:** Complete, schema-rich, review-heavy OTA listings across primary AI citation sources
**Why it matters:** Booking.com dominates ChatGPT/Gemini citations (54%/63%). TripAdvisor dominates Perplexity/Grok (95.5%). Yelp added to ChatGPT January 2026. Hotels not present or incomplete on these OTAs are algorithmically invisible to most AI engines regardless of their own website quality.
**What passing looks like:** Booking.com, TripAdvisor, Expedia, and Yelp listings for Radisson properties have complete descriptions, amenity lists, high review volume (200+), and recent reviews (within 90 days).
**How to check:** Search each OTA for Radisson brand listings; check completeness of listings for key European properties.
**Bleisure relevance:** OTA listings with business amenities mentioned and bleisure-relevant reviews increase AI recommendation probability.

---

## C13 — Structured Amenity Data
**Signal name:** Machine-readable amenity data (not prose only)
**Why it matters:** Marriott-Google AI integration analysis: "if an asset isn't digitized into machine-readable APIs, it remains invisible to AI booking agents." Amenity data in prose paragraphs is not reliably parsed; structured data (schema amenityFeature, OTA listing checkboxes, API-accessible data) is.
**What passing looks like:** Hotel/LodgingBusiness schema includes amenityFeature array with specific amenities named as LocationFeatureSpecification. Meeting rooms, WiFi, gym, restaurant, spa individually named.
**How to check:** Schema fetch (if available); OTA listing amenity checkboxes; Google rich results hotel card amenity display.
**Bleisure relevance:** Meeting rooms, business center, high-speed WiFi, fitness center, spa, restaurant are the core bleisure amenity set.

---

## C14 — llms.txt File
**Signal name:** /llms.txt file at domain root explicitly listing AI-accessible content
**Why it matters:** Emerging standard (2026) — analogous to robots.txt but for AI engines. Explicitly tells AI systems what content is available, its structure, and how to access it. Fast-moving adoption in 2026 among AI-forward brands.
**What passing looks like:** /llms.txt file exists at https://www.radissonhotels.com/llms.txt with structured content index for AI systems.
**How to check:** Attempt fetch of /llms.txt.
**Bleisure relevance:** Explicit AI accessibility declaration could significantly improve AI engine crawlability given Radisson's 403 blocking behavior.

---

## C15 — Geographic Specificity (European Destinations + US Origination)
**Signal name:** Explicit European destination content with American traveler origination context
**Why it matters:** American bleisure travelers are the target audience. AI query routing depends on geographic entity matching. "Hotels in London for American business travelers" requires both entities (London AND American travelers) to be present.
**What passing looks like:** Destination pages name specific European cities, districts, transport links (airport names, train stations), and explicitly mention American traveler needs (direct flights from US hubs, USD pricing, transatlantic travel context).
**How to check:** SERP snippet text for London/destination pages; check title/description for US-relevant geographic entities.
**Bleisure relevance:** Core to the primary target audience query pattern.

---

## New Criteria Added in run_002 (Not in run_001 Framework)
- **C12** (OTA Listing Completeness) — previously noted as gap in research; now formalized
- **C13** (Structured Amenity Data) — Marriott-Google integration findings elevated this
- **C14** (llms.txt) — New protocol identified in run_002 literature
- **C15** (Geographic Specificity with US context) — formalized from run_001 gap observations
