# Literature Findings - run_005 | 2026-06-26

## Research Questions Addressed
1. Which AI engines are currently dominant for travel and hotel discovery?
2. What signals do the currently dominant engines use to surface hotel results in conversational queries?
3. What current GEO/AEO practices are best evidenced for hospitality?
4. What metadata and content structures are hospitality leaders and OTAs using?
5. What content patterns and query types matter for American bleisure travelers aged 25-55 traveling from the US to Europe?

## Dated Findings and Synthesis

### 2026-06-26 - Dominant travel AI surfaces
Hotel discovery is now split across search AI, assistant app ecosystems, OTA-owned AI planning, and metasearch AI. The current surfaces to score against are Google AI features/AI Mode/Gemini, ChatGPT Search and ChatGPT apps, Claude with Expedia travel planning, Perplexity-style answer engines, KAYAK conversational AI, Booking.com, Expedia, and OTA/review ecosystems that assistants cite for hotel facts. For this Park Plaza run, the key implication is that brand pages, destination pages, meeting-event pages, and individual hotel pages must be retrievable and factual enough for both search crawlers and app/connector-style assistants.

**What changed since run_004:** The channel mix is still transactional and assistant-led, but this run's 478 selected Park Plaza URLs make page-level access, locale alignment, and repetitive template quality more important than a narrow brand-page sample.

### 2026-06-26 - Retrieval and indexability remain first-order signals
Google's AI-search guidance keeps eligibility grounded in normal Search infrastructure: useful content, crawlability, indexability, snippet controls, structured data that matches visible content, and technically coherent pages. ChatGPT Search and assistant retrieval also depend on permitted page access. A root technical file is not enough; every selected Park Plaza URL must return an auditable status and either useful HTML or a precise failure state.

**Interpretation:** Treat HTTP 403, AccessDenied, empty metadata, redirect-only pages, and unsupported test pages as first-order GEO blockers because they prevent assistants from validating hotel facts.

### 2026-06-26 - Hospitality structured data and local hotel facts
Google structured data guidance, Schema.org Hotel/LodgingBusiness definitions, and local business guidance converge on stable fields: name, URL, address, geo, telephone, images, opening/check-in details, amenities, reviews/ratings where valid, and booking or offer paths. Organization and BreadcrumbList markup can help entity context, but they do not replace Hotel or LodgingBusiness data on individual hotel pages.

**Interpretation:** Park Plaza property and meeting-event URLs should expose hotel/place identity plus amenities, meeting capacity, transit/location facts, and booking routes in visible text and structured data.

### 2026-06-26 - OTA and competitor page structures
Booking.com, Expedia, and large hotel brands generally orient hotel search pages around task completion: destination, accommodation type, price/availability path, review signals, amenity filters, and clear booking affordances. External AI visibility studies continue to show major hotel chains and OTAs outperforming fragmented brand pages when assistants need consensus and bookable facts.

**Interpretation:** Radisson/Park Plaza should reduce reliance on OTAs by making brand-owned pages equally explicit about location, amenities, meetings, family/leisure use, reviews, and direct booking confidence.

### 2026-06-26 - American bleisure traveler query behavior
Expedia's 2026 AI trust research reinforces a split behavior: travelers use AI for planning and comparison but still prefer trusted travel brands for booking. Booking.com's 2026 predictions emphasize individualized, preference-led trips. For American travelers to Europe, the query pattern is compound: destination plus work need plus leisure extension plus trust/booking constraint.

**Representative queries for scoring:**
- "Park Plaza hotels in London for a US business trip with weekend sightseeing"
- "Park Plaza Amsterdam hotels with meeting rooms, breakfast, train access, and reliable Wi-Fi"
- "European hotels near business districts that also work for families or couples"
- "Official Park Plaza booking with meeting rooms, reviews, parking, and cancellation details"

## Source Links and Notes

### Google Search Central - AI features and AI optimization
- URL: https://developers.google.com/search/docs/appearance/ai-features
- URL: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Use in this run: crawlability, indexability, helpful content, snippet control, and structured content remain the base for AI search eligibility.

### OpenAI - ChatGPT Search and apps in ChatGPT
- URL: https://help.openai.com/en/articles/9237897-chatgpt-search
- URL: https://openai.com/index/introducing-apps-in-chatgpt/
- Use in this run: assistant discovery now includes both retrieved web results and in-chat app surfaces such as travel/booking apps.

### Expedia - Claude travel planning and AI trust gap
- URL: https://www.expedia.com/newsroom/plan-your-next-trip-with-expedia-in-claude/
- URL: https://ir.expediagroup.com/news-and-events/news/news-details/2026/Expedia-Group-Reveals-The-AI-Trust-Gap-Travelers-Embrace-AI-for-Planning-but-Rely-on-Trusted-Brands-to-Book/default.aspx
- Use in this run: OTA app/connectors and traveler trust behavior make direct booking clarity a GEO conversion issue, not only an SEO issue.

### KAYAK - conversational AI travel search
- URL: https://www.kayak.com/news/ai-mode/
- Use in this run: metasearch assistants encourage natural-language trip constraints and comparison by amenities, dates, and location.

### Google structured data and local business guidance
- URL: https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
- URL: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- URL: https://developers.google.com/search/docs/appearance/structured-data/local-business
- Use in this run: structured data must be complete, relevant, and aligned with visible page content.

### Schema.org hotel vocabulary
- URL: https://schema.org/Hotel
- URL: https://schema.org/LodgingBusiness
- URL: https://schema.org/amenityFeature
- Use in this run: Hotel/LodgingBusiness, amenityFeature, aggregateRating/review where legitimate, and offer/booking properties are the hotel-specific vocabulary to check.

### Booking.com and Expedia public travel trend/OTA evidence
- URL: https://news.booking.com/the-era-of-you-bookingcom-predicts-the-top-trends-defining-travel-in-2026-with-individuality-taking-center-stage/
- URL: https://www.booking.com/city/gb/london.en-gb.html
- URL: https://www.expedia.com/London-Hotels.d178279.Travel-Guide-Hotels
- Use in this run: OTA pages expose destination, inventory, reviews, and booking decision structure that brand-owned Park Plaza pages should compete with.

### AI visibility studies for travel and hospitality
- URL: https://www.5wpr.com/ai-visibility-index/airlines-hotels-ai-visibility-index-2026/
- URL: https://www.meltwater.com/en/blog/online-travel-platform-ai-visibility-index
- Use in this run: third-party evidence that hotel and OTA answer visibility depends on brand authority, consensus, review footprint, and structured facts.
