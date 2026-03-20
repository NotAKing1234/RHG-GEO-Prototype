# GEO/AEO Criteria Framework — run_001 | 2026-03-20

Synthesized from fresh web research conducted 2026-03-20. All criteria are specific, checkable signals discovered this run.
Target audience: American bleisure travelers (ages 25–55, US→Europe, AI-first discovery).
Target engines: ChatGPT, Google AI Overviews, Perplexity AI, Microsoft Copilot.

---

## C01 — LodgingBusiness / Hotel Schema Presence

**Signal name:** Schema.org LodgingBusiness or Hotel structured data
**Why it matters for AI hotel discovery:** Google and Microsoft explicitly use Schema.org structured data for generative AI features. ChatGPT confirmed it uses structured data to determine which products appear in results. AI systems parse schema at scale and prioritize machine-readable context over unstructured text. Without it, the page is effectively invisible to AI parsing layers.
**What "passing" looks like:** Page contains valid JSON-LD block with `@type: "Hotel"` or `@type: "LodgingBusiness"` including at minimum: name, address (PostalAddress), telephone, image, description, checkinTime, checkoutTime, amenityFeature, starRating, and url.
**How to check during audit:** View page source or use browser DevTools → inspect `<script type="application/ld+json">` blocks. Validate against schema.org/Hotel. Check for nested amenityFeature, starRating, geo coordinates, and priceRange fields.
**Relevance to American bleisure traveler queries:** When a bleisure traveler asks ChatGPT "best Radisson in London with meeting rooms," structured data is how Radisson's meeting room amenity is surfaced as a parseable feature rather than buried in paragraph text.

---

## C02 — FAQPage Schema with Conversational Query Coverage

**Signal name:** FAQPage structured data aligned to natural language traveler queries
**Why it matters for AI hotel discovery:** FAQ schema is the single most impactful structured data type for AI citations in 2026. Pages with 5–8 well-implemented Q&A pairs get cited up to 3x more than equivalent pages without FAQ schema. AI engines treat FAQ blocks as pre-extracted answers ready for citation.
**What "passing" looks like:** Page contains JSON-LD `@type: "FAQPage"` with 5–8 Q&A pairs. Questions must use natural language matching real traveler queries (not internal marketing language). At least 2–3 questions must address the bleisure traveler profile (e.g., "Do Radisson Blu hotels have business centers?", "Which Radisson hotels in London are near the financial district?").
**How to check during audit:** Inspect JSON-LD blocks for FAQPage type. Also check visible FAQ or Q&A sections on page rendered HTML. Evaluate question phrasing for conversational vs. marketing register.
**Relevance to American bleisure traveler queries:** Bleisure travelers use highly specific, conversational AI queries. FAQ schema ensures Radisson pages contain pre-formatted answers that AI engines extract and cite directly, rather than paraphrasing competitor content.

---

## C03 — Title Tag: Conversational Query Alignment

**Signal name:** Title tag containing traveler-intent keywords and brand entity
**Why it matters for AI hotel discovery:** Title tags remain a primary entity signal for both traditional search and AI citation selection. AI engines use titles to understand page scope and match it against query intent. Generic titles ("Radisson Hotels") fail to match specific conversational queries.
**What "passing" looks like:** Title includes brand name (Radisson / Radisson Blu / Park Plaza), city or region, and one traveler-intent modifier (e.g., "luxury," "business travelers," "Europe hotels"). Format: `[Brand] [City] Hotels | [Intent Modifier]`. Character length 50–65.
**How to check during audit:** Extract `<title>` tag from page source. Evaluate brand presence, geographic specificity, and intent alignment. Check character count.
**Relevance to American bleisure traveler queries:** American travelers searching for "Radisson hotels London business" need the title to match their query scope. Misaligned titles reduce citation probability.

---

## C04 — Meta Description: Natural Language Answer Preview

**Signal name:** Meta description structured as a natural language answer to traveler queries
**Why it matters for AI hotel discovery:** Meta descriptions function as answer previews. AI engines scan meta descriptions to assess whether the page likely contains the answer to a user query. A description written as a statement ("Discover luxury Radisson hotels…") scores lower than one written as an answer ("Radisson hotels in London offer business-class amenities, central locations near Canary Wharf, and flexible stay options for American business travelers.").
**What "passing" looks like:** Meta description 140–160 characters, structured as a declarative sentence answering "what does this hotel offer and to whom." Includes brand, city, at least one amenity, and one traveler-type signal. No marketing fluff verbs ("Discover," "Experience," "Explore").
**How to check during audit:** Extract `<meta name="description">` from page source. Parse for query-answer format vs. marketing CTA format. Check length.
**Relevance to American bleisure traveler queries:** Bleisure travelers use natural language AI queries. Meta descriptions that read as answers increase the probability of AI engines selecting this page as the citation source.

---

## C05 — Open Graph Tags: Social and AI Preview Accuracy

**Signal name:** Open Graph metadata (og:title, og:description, og:image, og:type)
**Why it matters for AI hotel discovery:** Open Graph tags are used by AI engines and social platforms to understand page identity when fetching content for citation. Missing or mismatched OG tags reduce confidence in page identity, especially for brand pages. Perplexity and other engines fetch OG data as part of citation evaluation.
**What "passing" looks like:** Page contains `og:title`, `og:description`, `og:image` (with hotel photography, not generic placeholders), `og:type: "website"` or `og:type: "place"`, and `og:url` matching canonical URL. og:description should match or complement the meta description in natural language format.
**How to check during audit:** Inspect page source for `<meta property="og:*">` tags. Check image URL resolves to real hotel photography. Confirm og:url matches page URL.
**Relevance to American bleisure traveler queries:** When Perplexity or ChatGPT fetch a Radisson page to evaluate it as a citation, Open Graph data is part of the content fingerprint. Accurate OG data increases citation confidence.

---

## C06 — Heading Structure: Scannable and Query-Aligned

**Signal name:** H1/H2/H3 hierarchy aligned to traveler query vocabulary
**Why it matters for AI hotel discovery:** AI engines parse heading structures to understand page information architecture. Headings act as semantic anchors: an H2 reading "Hotels in London for Business Travelers" signals content relevance to bleisure queries far more effectively than "Our Properties."
**What "passing" looks like:** Page has exactly one H1 containing brand + location or brand + category. H2s cover distinct traveler-relevant topics (e.g., "Business Amenities," "Location and Transport," "Meeting Facilities," "Leisure After Work"). H3s add specificity within each topic. No duplicate heading levels. Headings use traveler vocabulary, not internal brand jargon.
**How to check during audit:** Extract full heading outline (H1→H3) from rendered page. Evaluate alignment to bleisure traveler query vocabulary. Check for duplicate H1s and missing H2 structure.
**Relevance to American bleisure traveler queries:** Headings that match query patterns ("London hotels near financial district," "business meeting facilities") increase AI engine confidence that the page directly addresses the traveler's question.

---

## C07 — Entity Signals: Brand + Location + Category Clarity

**Signal name:** Named entity clarity — Radisson as a brand with location, category, and service type
**Why it matters for AI hotel discovery:** AI engines build knowledge graphs of entities. For Radisson to appear in ChatGPT or Perplexity responses to "best European hotel brands for business travelers," the page must consistently and unambiguously signal: brand name, property category (luxury/upscale), geographic footprint (Europe), and service type (hotel/lodging/business travel).
**What "passing" looks like:** Page mentions "Radisson" as a named brand (not just implied) at least 3× in body text. Mentions at least one geographic scope (city, country, or "Europe"). Mentions at least one service category ("hotel," "business hotel," "luxury hotel"). Mentions at least one traveler type ("business travelers," "bleisure travelers," "American guests").
**How to check during audit:** Read page body content and count explicit brand, location, category, and traveler-type mentions. Check if structured data reinforces these entity signals.
**Relevance to American bleisure traveler queries:** Named entity recognition is how AI engines resolve "which Radisson hotel is best for an American in London" — the brand must be confidently recognized as an entity with known attributes.

---

## C08 — Natural Language Query Compatibility

**Signal name:** Page content can directly answer a conversational AI travel query
**Why it matters for AI hotel discovery:** AI engines match user queries to content by assessing whether the page would plausibly answer the question. A page that only contains marketing copy ("Experience the Radisson Difference") cannot answer "Is Radisson Blu good for American business travelers in London?" A page that explicitly addresses this query type becomes a citation candidate.
**What "passing" looks like:** Page body text contains at least one paragraph directly addressing a realistic bleisure traveler query: traveler type (business, bleisure, American), purpose (meeting, conference, leisure extension), amenity need (WiFi, business center, gym, bar), and location context. Ideally structured as a clear statement that could be extracted as a direct answer.
**How to check during audit:** Read page body text. Identify if any passage directly answers a query like "hotels in [city] for American business travelers with meeting rooms." Note the query coverage score: 0 = no match, 1 = partial match, 2 = direct match.
**Relevance to American bleisure traveler queries:** This is the core signal. Pages that can answer the traveler's actual question will be cited; pages that cannot will be skipped, even with perfect technical schema.

---

## C09 — Alt Text on Meaningful Images

**Signal name:** Descriptive alt text on hotel photography
**Why it matters for AI hotel discovery:** Google AI Overviews favor multi-modal content (23.3% citation share from visual content). Alt text is the primary signal for image content understanding. Hotel room, amenity, and location images with descriptive alt text contribute to entity recognition and content relevance scoring.
**What "passing" looks like:** All meaningful hotel images (rooms, lobby, pool, business center, restaurant, cityscape) have descriptive alt text including property name and content description (e.g., "Radisson Blu London Executive Floor Business Room with city views"). No empty alt attributes on meaningful images. Decorative images may have empty alt.
**How to check during audit:** Inspect image `alt` attributes in rendered page source. Sample 5–10 meaningful images per page. Check for empty, generic ("image1.jpg"), or keyword-stuffed alt text.
**Relevance to American bleisure traveler queries:** Google AI Overviews with visual components increasingly appear for hotel discovery queries. Proper alt text ensures Radisson images are included in multi-modal AI responses.

---

## C10 — Content Freshness Signals

**Signal name:** Visible or schema-declared content freshness
**Why it matters for AI hotel discovery:** New content enters AI citation pools within 3–5 business days; content decays and loses citation priority without freshness updates. AI engines weight recently updated content higher in citation selection for time-sensitive topics like hotel availability, pricing, and amenities.
**What "passing" looks like:** Page contains a visible "Last updated" date, OR schema dateModified field in structured data, OR recent blog/news content linked from page. Content references current year (2025 or 2026). No outdated information visible (old promotions, past events, pre-2024 pricing ranges).
**How to check during audit:** Check for dateModified in JSON-LD. Check for visible date stamps on content. Check whether body text references current-year context. Note any obviously stale content.
**Relevance to American bleisure traveler queries:** Travelers using AI engines expect current information. Stale content reduces citation confidence and may cause AI engines to prefer fresher OTA pages for the same query.

---

## C11 — Amenity Coverage: Bleisure-Specific Features

**Signal name:** Explicit coverage of business AND leisure amenities for the bleisure profile
**Why it matters for AI hotel discovery:** Bleisure travelers issue compound queries combining business and leisure needs. Pages that only mention one dimension (business center OR spa, not both) fail to match the compound query. AI engines parse amenity mentions to assess relevance to multi-dimensional traveler needs.
**What "passing" looks like:** Page explicitly mentions both business amenities (meeting rooms, business center, high-speed WiFi, flexible check-in/out, airport transfer) AND leisure amenities (restaurant, bar, spa, gym, pool, city location for tourism). Ideally mentions "bleisure," "work and leisure," or equivalent phrasing.
**How to check during audit:** Scan body text and structured data amenityFeature list. Catalog all business amenities mentioned and all leisure amenities mentioned. Score: 0 = neither, 1 = one dimension, 2 = both dimensions.
**Relevance to American bleisure traveler queries:** This is the defining signal for bleisure discoverability. A page scoring 2 on amenity coverage can match queries like "hotel with conference room and great bar in Amsterdam" — a compound query that is increasingly common among AI-assisted bleisure planners.

---

## C12 — Geographic Entity Signals for European Destinations

**Signal name:** Geographic specificity for European cities relevant to US→Europe bleisure travel
**Why it matters for AI hotel discovery:** American bleisure travelers traveling to Europe use city-specific and region-specific queries. AI engines need to resolve "Radisson" to specific European geographic entities to answer "Which Radisson hotel is near Heathrow?" or "Radisson Amsterdam near the business district." Generic Europe-level content scores lower than city-specific content.
**What "passing" looks like:** Page (for city-specific pages) mentions the specific city by name ≥3×; mentions neighborhood or district context (e.g., "near Canary Wharf," "in the 8th arrondissement," "steps from Central Station"); mentions proximity to relevant US traveler reference points (airport, financial district, major attractions). Country mentioned at least once.
**How to check during audit:** For city-specific pages, count city name mentions. Check for district/neighborhood specificity. Check for proximity signals to US-traveler-known landmarks or transport hubs. For brand overview pages, check for country/region coverage breadth.
**Relevance to American bleisure traveler queries:** American travelers often navigate European cities by airport, financial district, and iconic landmark — not local neighborhood names. Pages that reference these entry-point geographies match the mental model of the target traveler.

---

## Summary Table

| ID  | Signal Name                          | Priority | Audit Method              |
|-----|--------------------------------------|----------|---------------------------|
| C01 | LodgingBusiness/Hotel Schema         | P1       | Source inspection / JSON-LD |
| C02 | FAQPage Schema (conversational)      | P1       | Source inspection / JSON-LD |
| C03 | Title Tag alignment                  | P1       | Source extraction          |
| C04 | Meta description (answer format)     | P1       | Source extraction          |
| C05 | Open Graph tags                      | P2       | Source inspection          |
| C06 | Heading structure                    | P2       | Rendered HTML extraction   |
| C07 | Entity signals (brand/location)      | P1       | Body text analysis         |
| C08 | Natural language query compatibility | P1       | Body text analysis         |
| C09 | Alt text on images                   | P2       | Source inspection          |
| C10 | Content freshness                    | P2       | JSON-LD + visible content  |
| C11 | Amenity coverage (bleisure)          | P1       | Body text + schema parse   |
| C12 | Geographic entity signals            | P2       | Body text analysis         |
