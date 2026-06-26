# Targeted Gap Research — run_004 | 2026-06-24

**Research Report — 2026-06-24**

**GAP-001 — Page-level retrieval blocked**
- Best practice: AI/search visibility still starts with crawlable, indexable pages; Google warns against using `403` as a crawl-control mechanism and says AI features use normal Search controls. Sources: [Google HTTP status codes](https://developers.google.com/crawling/docs/troubleshooting/http-status-codes), [Google AI features](https://developers.google.com/search/docs/appearance/ai-features).
- Example: [Premier Inn London County Hall](https://www.premierinn.com/gb/en/hotels/england/greater-london/london/london-county-hall.html) returns a public hotel page with title, meta description, Hotel schema, and FAQ schema.
- Proposed fix: Serve `200` HTML for all public Country Inn brand/hotel pages to search and AI crawlers; keep abuse controls behavioral/rate-based, not blanket access templates.
- Impact: AI systems can retrieve Radisson's official content instead of relying on OTAs, stale snippets, or inaccessible localized fallbacks.

**GAP-002 — English/US path blocked while localized European pages are accessible**
- Best practice: Multiregional sites need crawlable localized variants with correct canonical and reciprocal `hreflang`. Source: [Google localized versions](https://developers.google.com/search/docs/specialty/international/localized-versions).
- Example: [Wyndham London North M1](https://www.wyndhamhotels.com/ramada/london-united-kingdom/ramada-london-north-m1/overview) exposes an English hotel page with title/meta and Hotel JSON-LD.
- Proposed fix: Restore crawlable `/en-us/` Country Inn brand, business travel, breakfast, renovated hotels, and hotel pages; add reciprocal `hreflang` and `x-default`.
- Impact: American travelers get US-English direct-booking content rather than AI systems routing them to non-US localized pages.

**GAP-003 — Sitemap access denied**
- Best practice: Submit canonical sitemap URLs and make the sitemap available to Google; include sitemap locations in `robots.txt`. Source: [Google sitemap guide](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).
- Example: [Wyndham sitemap](https://www.wyndhamhotels.com/sitemap.xml), [Hilton sitemap](https://www.hilton.com/sitemap.xml), and [KAYAK sitemap](https://www.kayak.com/sitemap.xml) are public sitemap endpoints.
- Proposed fix: Serve `sitemap.xml`/sitemap indexes as `200` XML; include only canonical `200` pages; split by locale, brand, and hotel; exclude test/banner URLs.
- Impact: Faster discovery, easier Search Console diagnostics, and better AI retrieval coverage.

**GAP-004 — llms.txt missing**
- Best practice: Treat `/llms.txt` as an emerging agent-usability map, not a replacement for crawlable HTML or XML sitemaps. Sources: [llms.txt proposal](https://llmstxt.org/), [web.dev agent-friendly websites](https://web.dev/articles/ai-agent-site-ux).
- Example: [Expedia llms.txt](https://www.expedia.com/llms.txt) and [Wyndham llms.txt](https://www.wyndhamhotels.com/llms.txt) publish AI-readable brand, scope, and key-link summaries.
- Proposed fix: Add `/llms.txt` with official Radisson identity, domains, brands, booking paths, US-to-Europe traveler guidance, and links to canonical brand/hotel/city pages.
- Impact: Helps AI agents orient to official Radisson sources; impact is directional but still experimental.

**GAP-005 — Hotel/LodgingBusiness schema absent**
- Best practice: Hotel pages should use `Hotel`/`LodgingBusiness` JSON-LD with address, geo, images, amenities, brand, ratings where valid, and booking actions. Sources: [Schema.org hotel markup](https://schema.org/docs/hotels.html), [Google LocalBusiness structured data](https://developers.google.com/search/docs/appearance/structured-data/local-business).
- Example: [Accor ibis Clermont-Ferrand Montferrand](https://all.accor.com/hotel/0929/index.en.shtml) exposes `Hotel` schema with address, aggregate rating, Wi-Fi, breakfast, and meeting-room amenities.
- Proposed fix: Add validated `Hotel` JSON-LD to every hotel overview page; use `Organization` only for corporate/brand pages.
- Impact: AI systems can identify Radisson pages as specific, bookable hotel entities with amenities.

**GAP-006 — Individual hotel pages blocked**
- Best practice: Property-level pages must be crawlable and consistent with hotel inventory feeds: name, address, geocode, phone, and website URL. Source: [Google hotel inventory setup](https://support.google.com/hotelprices/answer/9218458).
- Example: [Wyndham London North M1](https://www.wyndhamhotels.com/ramada/london-united-kingdom/ramada-london-north-m1/overview) exposes a property page with `Hotel`, `geo`, and `ReserveAction`.
- Proposed fix: Unblock hotel overview and subpages; add canonical, `hreflang`, Hotel schema, room/amenity data, and direct booking deep links.
- Impact: AI travel tools can recommend direct Radisson properties instead of only OTA copies.

**GAP-007 — Work-leisure and amenity data inconsistent**
- Best practice: Keep hotel amenities current in structured data, Google hotel details, and visible copy. Sources: [Google hotel details](https://support.google.com/business/answer/9177958), [Schema.org amenityFeature](https://schema.org/amenityFeature).
- Example: Accor's hotel schema includes Wi-Fi, breakfast, bar, parking, and meeting rooms on the same page.
- Proposed fix: Add a reusable bleisure module per hotel: desk/workspace, Wi-Fi, breakfast, meeting room, late checkout, transit, nearby leisure; map each to `amenityFeature`.
- Impact: Better matching for compound prompts like "European hotel for work meetings with weekend sightseeing."

**GAP-008 — Geographic and transport specificity weak**
- Best practice: Hotel discovery data should include physical location, geocode, phone, website, amenities, and location context. Sources: [Google hotel inventory](https://support.google.com/hotelprices/answer/9218458), [Google Lodging API transfer fields](https://developers.google.com/my-business/reference/lodging/rest/v1/Lodging).
- Example: Premier Inn's London County Hall page names South Bank, Big Ben, and London Eye; Wyndham's page includes address and `geo`.
- Proposed fix: Add city/neighborhood, airport/train distance, business districts, landmarks, parking/shuttle, and public transit metadata to each property page.
- Impact: AI can answer "near airport," "near client office," and "near sightseeing" queries with Radisson-owned evidence.

**GAP-009 — Visible Q&A and FAQ integrity weak**
- Best practice: Mark up visible FAQs with `FAQPage` only when the Q&A content is present for users; note Google has narrowed FAQ rich-result eligibility. Sources: [Google FAQ structured data](https://developers.google.com/search/docs/appearance/structured-data/faqpage), [Schema.org FAQPage](https://schema.org/FAQPage).
- Example: Premier Inn London County Hall exposes FAQPage JSON-LD for early check-in, accessibility, luggage storage, and local-distance questions.
- Proposed fix: Add visible FAQs and matching JSON-LD for check-in/out, breakfast, Wi-Fi, transit, business amenities, parking, accessibility, and local attractions.
- Impact: AI assistants can answer follow-up questions without guessing from generic brand copy.

**GAP-010 — Public banner-test URLs selected and metadata-empty**
- Best practice: Test pages should be excluded or `noindex`; production pages need descriptive titles and unique meta descriptions. Sources: [Google noindex](https://developers.google.com/search/docs/crawling-indexing/block-indexing), [Google title links](https://developers.google.com/search/docs/appearance/title-link), [Google snippets](https://developers.google.com/search/docs/appearance/snippet).
- Example: Wyndham and Premier Inn production hotel pages expose meaningful title/meta/schema rather than empty public test metadata.
- Proposed fix: Move banner-test URLs behind auth or add `X-Robots-Tag: noindex`; remove them from sitemaps and run selection; add CI checks for empty title/meta/canonical/OG.
- Impact: Removes low-quality signals and prevents AI engines from sampling broken test pages.

**GAP-011 — Query fan-out coverage weak**
- Best practice: Cover subtopics that AI systems decompose into related searches; Google says AI Mode/AI Overviews may use query fan-out. Source: [Google AI features](https://developers.google.com/search/docs/appearance/ai-features).
- Example: [KAYAK Ask AI](https://www.kayak.com/news/ask-ai/) lets travelers ask natural-language trip questions while hotel/flight/car results update live.
- Proposed fix: Build metadata/content clusters for "US traveler + Europe city + business need + leisure need + amenity + booking constraint."
- Impact: Higher chance Radisson appears in synthesized AI answers for complex bleisure prompts.

**GAP-012 — Image accessibility and visual context weak**
- Best practice: Use contextual, information-rich alt text and relevant page images; avoid keyword stuffing. Source: [Google image SEO](https://developers.google.com/search/docs/appearance/google-images).
- Example: Premier Inn's hotel schema includes multiple hotel images tied to the property page.
- Proposed fix: Add page-specific OG images and gallery alt text for rooms, desks, meeting rooms, breakfast, exterior, transit, and local attractions.
- Impact: Better visual-search and AI confidence for travelers comparing room/work/leisure suitability.

**GAP-013 — American bleisure traveler path missing**
- Best practice: Create crawlable, audience-specific pages that directly answer traveler intents; AI systems reward useful, unique content and may fan out across subtopics. Source: [Google AI features](https://developers.google.com/search/docs/appearance/ai-features).
- Example: [Expedia in ChatGPT](https://www.expedia.com/product/expedia-in-chatgpt/) and [Expedia in Claude](https://www.expedia.com/newsroom/plan-your-next-trip-with-expedia-in-claude/) target conversational hotel/flight planning for US users.
- Proposed fix: Add `/en-us/` bleisure hubs for US-to-Europe travelers by city/region, linking to relevant hotels with work amenities, weekend attractions, transit, loyalty, and direct booking.
- Impact: Radisson becomes eligible for prompts framed around American traveler identity, not just generic hotel search.

**GAP-014 — Trust, reviews, and consensus footprint missing**
- Best practice: Use visible, verifiable reviews and `aggregateRating` where eligible; validate review markup. Sources: [Schema.org hotel reviews](https://schema.org/docs/hotels.html), [Google review snippets](https://developers.google.com/search/docs/appearance/structured-data/review-snippet).
- Example: Accor's hotel page exposes aggregate rating and review count in Hotel JSON-LD.
- Proposed fix: Add visible review summaries and valid `aggregateRating`/`Review` to hotel pages where Radisson owns or can lawfully display the review data; unblock review pages.
- Impact: AI assistants can compare trust and consensus instead of treating Radisson as metadata-thin.

**GAP-015 — Direct AI travel distribution readiness missing**
- Best practice: Be present in AI planning surfaces with official tools/connectors and live inventory, not only passive SEO pages. Sources: [OpenAI Apps in ChatGPT](https://openai.com/index/introducing-apps-in-chatgpt/), [Claude Expedia connector](https://claude.com/connectors/expedia), [KAYAK Ask AI](https://www.kayak.com/news/ask-ai/).
- Example: OpenAI lists Booking.com and Expedia as ChatGPT app partners; Expedia also has Claude hotel/flight search.
- Proposed fix: Build a Radisson AI distribution roadmap: Apps SDK/MCP app, Claude connector, public hotel-search API, direct booking deep links, loyalty-aware but privacy-safe flows, and OTA data parity.
- Impact: Radisson can appear as an action-capable direct booking source inside AI-assisted travel planning.

**Assessment**
- Most urgent gap: GAP-001. If pages return `403`, AI engines cannot reliably retrieve the official Radisson content; schema, FAQs, reviews, and persona content cannot compensate.
- Fastest measurable improvement: GAP-003 if it is a server/config fix, because `sitemap.xml` can be retested immediately and monitored in Search Console. GAP-010 is the fastest content-quality cleanup.
- Contested or changing rapidly: GAP-004 `llms.txt`, GAP-009 FAQ rich-result value, GAP-011 query fan-out optimization tactics, and GAP-015 AI app/connector distribution. These should be treated as active-test areas, while crawlability, sitemaps, schema, images, and hotel inventory data are stable fundamentals.
