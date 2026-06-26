# Literature Findings — run_004 | 2026-06-24

## Research Questions Addressed
1. Which AI engines are currently dominant for travel and hotel discovery?
2. What signals do the currently dominant engines use to surface hotel results in conversational queries?
3. What current GEO/AEO practices are best evidenced for hospitality?
4. What metadata and content structures are hospitality leaders and OTAs using?
5. What content patterns and query types matter for American bleisure travelers aged 25-55 traveling from the US to Europe?

## Dated Findings and Synthesis

### 2026-06-24 — Dominant travel AI surfaces
Current hotel discovery is split across search AI, assistant apps/connectors, OTA-owned AI, and metasearch AI. The relevant current set for this run is Google AI Overviews/AI Mode/Gemini, ChatGPT Search and ChatGPT apps, Claude travel connectors, Perplexity, KAYAK Ask AI, Booking.com, and Expedia. OpenAI's app ecosystem now includes Booking.com and Expedia; Expedia has a Claude travel-planning connector in the US; KAYAK Ask AI supports natural-language travel planning; 5W and Meltwater both identify Marriott/Hilton and Booking.com/Expedia as high-visibility competitors in AI travel answers.

**What changed since run_003:** AI travel discovery is more transactional. Run_003 already saw Accor/Hyatt/Perplexity as strategic threats; run_004 adds more mature app/connector distribution through ChatGPT apps, Claude/Expedia, KAYAK Ask AI, and AI Mode query fan-out.

### 2026-06-24 — Retrieval and crawlability are still first-order signals
Google's AI features guidance keeps the ranking/control model rooted in normal Search infrastructure: pages must be crawlable, indexable, useful, and technically coherent. ChatGPT Search also requires permitted retrieval access. This run's partial robots recovery matters, but page-level 403 blocks still prevent AI systems from reading the actual Country Inn English/US and hotel pages.

**Interpretation:** Root `/robots.txt` HTTP 200 is not a pass. The decisive criterion is whether representative public brand/hotel URLs return 200 HTML to search and AI retrieval agents.

### 2026-06-24 — Hospitality structured data and local hotel facts
Google structured data, LocalBusiness guidance, Schema.org Hotel markup, and lodging/vacation-rental documentation all converge on the same stable signals: hotel/place identity, address, geo, telephone, images, amenities, check-in/check-out, ratings/reviews where valid, and booking or offer paths. Accessible run_004 Country Inn pages expose `Organization` and `BreadcrumbList`, but not `Hotel` or `LodgingBusiness`, so they remain shallow for AI hotel comparison.

**Interpretation:** Organization schema is not enough for hotel discovery. Hotel-level data must be present on property pages and visible content must support it.

### 2026-06-24 — OTA and competitor page structures
Booking.com's accessible London city page exposes query-aligned title/meta, OG fields, city/country/price framing, accommodation count, reviews, and a task-oriented H1. Expedia, Marriott, Hilton, and Hyatt were access-limited from this environment, so they are not used as page-source proof here. Third-party AI visibility studies still identify Marriott/Hilton and Booking.com/Expedia as leaders.

**Interpretation:** Radisson should compete with direct, crawlable hotel facts rather than leaving AI systems to rely on OTAs for availability, reviews, location, and booking confidence.

### 2026-06-24 — American bleisure traveler behavior
Expedia's 2026 AI Trust Gap research shows travelers use AI for planning and price/itinerary support but still prefer trusted travel brands for booking. Booking.com's 2026 predictions emphasize individualized trips. Adobe/TechRadar reporting shows US travel AI referral traffic rising sharply, with AI-referred users spending more time and bouncing less. The target query pattern is compound: US traveler + Europe destination + business need + leisure need + amenity + booking/trust constraint.

**Representative queries for scoring:**
- "Country Inn hotels in Europe for American business travelers with breakfast and reliable Wi-Fi"
- "Hotels near business districts in London or Amsterdam that also work for sightseeing"
- "Best midscale Radisson alternatives to Marriott or Hilton for a work trip in Europe"
- "Hotels with meeting rooms, breakfast, parking, and train access for a US traveler"

## Source Links and Imported DB Source Inventory

## developers.google.com
- Type: literature
- URL: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Claim: Literature source consulted: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Theme: literature_source

## developers.google.com
- Type: literature
- URL: https://developers.google.com/search/docs/appearance/ai-features
- Claim: Literature source consulted: https://developers.google.com/search/docs/appearance/ai-features
- Theme: literature_source

## help.openai.com
- Type: literature
- URL: https://help.openai.com/en/articles/9237897-chatgpt-search
- Claim: Literature source consulted: https://help.openai.com/en/articles/9237897-chatgpt-search
- Theme: literature_source

## openai.com
- Type: literature
- URL: https://openai.com/index/introducing-apps-in-chatgpt/
- Claim: Literature source consulted: https://openai.com/index/introducing-apps-in-chatgpt/
- Theme: literature_source

## expedia.com
- Type: literature
- URL: https://www.expedia.com/newsroom/plan-your-next-trip-with-expedia-in-claude/
- Claim: Literature source consulted: https://www.expedia.com/newsroom/plan-your-next-trip-with-expedia-in-claude/
- Theme: literature_source

## kayak.com
- Type: literature
- URL: https://www.kayak.com/news/ai-mode/
- Claim: Literature source consulted: https://www.kayak.com/news/ai-mode/
- Theme: literature_source

## 5wpr.com
- Type: literature
- URL: https://www.5wpr.com/ai-visibility-index/airlines-hotels-ai-visibility-index-2026/
- Claim: Literature source consulted: https://www.5wpr.com/ai-visibility-index/airlines-hotels-ai-visibility-index-2026/
- Theme: literature_source

## meltwater.com
- Type: literature
- URL: https://www.meltwater.com/en/blog/online-travel-platform-ai-visibility-index
- Claim: Literature source consulted: https://www.meltwater.com/en/blog/online-travel-platform-ai-visibility-index
- Theme: literature_source

## developers.google.com
- Type: literature
- URL: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- Claim: Literature source consulted: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- Theme: literature_source

## developers.google.com
- Type: literature
- URL: https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
- Claim: Literature source consulted: https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
- Theme: literature_source

## developers.google.com
- Type: literature
- URL: https://developers.google.com/search/docs/appearance/structured-data/local-business
- Claim: Literature source consulted: https://developers.google.com/search/docs/appearance/structured-data/local-business
- Theme: literature_source

## schema.org
- Type: literature
- URL: https://schema.org/docs/hotels.html
- Claim: Literature source consulted: https://schema.org/docs/hotels.html
- Theme: literature_source

## schema.org
- Type: literature
- URL: https://schema.org/LodgingBusiness
- Claim: Literature source consulted: https://schema.org/LodgingBusiness
- Theme: literature_source

## developers.google.com
- Type: literature
- URL: https://developers.google.com/search/docs/appearance/structured-data/vacation-rental
- Claim: Literature source consulted: https://developers.google.com/search/docs/appearance/structured-data/vacation-rental
- Theme: literature_source

## booking.com
- Type: literature
- URL: https://www.booking.com/city/gb/london.en-gb.html
- Claim: Literature source consulted: https://www.booking.com/city/gb/london.en-gb.html
- Theme: literature_source

## expedia.com
- Type: literature
- URL: https://www.expedia.com/London-Hotels.d178279.Travel-Guide-Hotels
- Claim: Literature source consulted: https://www.expedia.com/London-Hotels.d178279.Travel-Guide-Hotels
- Theme: literature_source

## ir.expediagroup.com
- Type: literature
- URL: https://ir.expediagroup.com/news-and-events/news/news-details/2026/Expedia-Group-Reveals-The-AI-Trust-Gap-Travelers-Embrace-AI-for-Planning-but-Rely-on-Trusted-Brands-to-Book/default.aspx
- Claim: Literature source consulted: https://ir.expediagroup.com/news-and-events/news/news-details/2026/Expedia-Group-Reveals-The-AI-Trust-Gap-Travelers-Embrace-AI-for-Planning-but-Rely-on-Trusted-Brands-to-Book/default.aspx
- Theme: literature_source

## news.booking.com
- Type: literature
- URL: https://news.booking.com/the-era-of-you-bookingcom-predicts-the-top-trends-defining-travel-in-2026-with-individuality-taking-center-stage/
- Claim: Literature source consulted: https://news.booking.com/the-era-of-you-bookingcom-predicts-the-top-trends-defining-travel-in-2026-with-individuality-taking-center-stage/
- Theme: literature_source

## techradar.com
- Type: literature
- URL: https://www.techradar.com/pro/ai-traffic-to-travel-sites-is-booming-as-shoppers-look-for-the-best-holiday-deal-without-doing-any-research
- Claim: Literature source consulted: https://www.techradar.com/pro/ai-traffic-to-travel-sites-is-booming-as-shoppers-look-for-the-best-holiday-deal-without-doing-any-research
- Theme: literature_source
