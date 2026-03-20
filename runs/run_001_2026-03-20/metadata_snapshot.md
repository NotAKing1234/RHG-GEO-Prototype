# Metadata Snapshot — run_001 | 2026-03-20

**Fetch method:** WebFetch + WebSearch (all direct page fetches returned HTTP 403; data gathered from Google SERP snippets, cached search descriptions, and secondary source analysis)
**Fetch timestamp:** 2026-03-20
**Pages audited:** 5 Priority 1 pages + 1 Priority 2 page (London, first rotation)
**Note on data quality:** All direct HTTP fetches of radissonhotels.com return 403. Metadata extracted from Google SERP titles/descriptions, search snippet text, and secondary source references. JSON-LD, OG tags, heading structure, alt text, and FAQ presence for most pages cannot be confirmed without direct fetch. These fields are marked accordingly. This is a known limitation for run_001; future runs should attempt alternative access methods.

---

## Page 1: https://www.radissonhotels.com/en-us (Homepage)

**URL:** https://www.radissonhotels.com/en-us
**Fetch status:** 403 Blocked
**Fetch timestamp:** 2026-03-20

**Extracted title:** "Radisson Hotels Official Site | Book Rooms Worldwide"
**Source:** Google SERP snippet (confirmed)

**Extracted meta description:** "Explore over 1100 hotels worldwide and book your stay with us today, with the best online rates guaranteed!"
**Source:** Google SERP snippet (confirmed)

**Structured data blocks:** NOT CONFIRMABLE (fetch blocked). No rich result appearances (FAQPage, Hotel schema) detected in SERP for this URL. Assumed absent or unverifiable.

**Open Graph tags:** NOT CONFIRMABLE (fetch blocked)

**Heading outline:** NOT CONFIRMABLE (fetch blocked). Based on known Radisson homepage structure, likely contains H1 brand tagline, H2 destination sections, H2 brand sections. Cannot confirm exact text.

**FAQ / Q&A presence:** NOT DETECTED. No FAQ rich snippets in SERP for this URL. Not visible in search snippets.

**Alt text observations:** NOT CONFIRMABLE (fetch blocked)

**Query compatibility notes:**
- Title is transaction-focused ("Book Rooms Worldwide"), not discovery-focused
- Meta description is booking-incentive format ("best online rates guaranteed"), not answer format
- No traveler type (business, bleisure) mentioned in confirmed metadata
- No geographic specificity for European destinations in confirmed metadata
- "over 1100 hotels worldwide" signals scale but not relevance to specific traveler query

**Entity signal notes:**
- Brand name "Radisson Hotels" present in title (strong)
- Service category "Hotels" present (adequate)
- Geographic scope "Worldwide" (too broad — weak for European bleisure queries)
- No traveler type entity signal confirmed

---

## Page 2: https://www.radissonhotels.com/en-us/brands (Brands Overview)

**URL:** https://www.radissonhotels.com/en-us/brands
**Fetch status:** 403 Blocked
**Fetch timestamp:** 2026-03-20
**Note:** Search results show content accessible at /corporate/about-us/our-brands; direct /brands URL may redirect. Data sourced from search snippet of brands/corporate page.

**Extracted title:** "Discover our hotel brands | Radisson Hotel Group"
**Source:** Google SERP snippet for /corporate/about-us/our-brands (most likely redirect target)

**Extracted meta description:** "Radisson Hotel Group provides a dynamic set of hotel brands for a wide range of travelers and budgets. We have 9 hotel brands, each of these with own identity."
**Source:** Google SERP snippet

**Structured data blocks:** NOT CONFIRMABLE

**Open Graph tags:** NOT CONFIRMABLE

**Heading outline:** NOT CONFIRMABLE. Likely H1 "Discover our hotel brands" or similar; H2s for each brand name.

**FAQ / Q&A presence:** NOT DETECTED in SERP

**Alt text observations:** NOT CONFIRMABLE

**Query compatibility notes:**
- "wide range of travelers and budgets" is generic, not bleisure-specific
- No mention of American travelers, European destinations, or business travel
- Title "Discover our hotel brands" is navigation-oriented, not query-answering

**Entity signal notes:**
- "Radisson Hotel Group" as named entity (strong)
- "9 hotel brands" — portfolio breadth signal (present)
- Traveler type: generic ("wide range of travelers and budgets") — weak
- Geographic scope: not mentioned in snippet

---

## Page 3: https://www.radissonhotels.com/en-us/brands/radisson-blu (Radisson Blu Brand Page)

**URL:** https://www.radissonhotels.com/en-us/brands/radisson-blu
**Fetch status:** 403 Blocked
**Fetch timestamp:** 2026-03-20
**Note:** Search shows canonical content at /en-us/brand/radisson-blu (singular); the /brands/ URL may redirect.

**Extracted title:** "Radisson Blu Hotels & Resorts | Radisson Hotels"
**Source:** Google SERP snippet

**Extracted meta description / brand copy:** "We provide unparalleled service, comfort, and style while creating meaningful and memorable experiences. By paying close attention to the small details that make a big difference, we inspire unforgettable experiences with every stay."
**Source:** Search snippet body text

**Additional confirmed copy:** "Style, form, beauty and function. That's what you'll find at Radisson Blu."

**Structured data blocks:** NOT CONFIRMABLE. Radisson Blu is known (from industry sources) to be upper upscale; schema implementation at brand level pages is unclear.

**Open Graph tags:** NOT CONFIRMABLE

**Heading outline:** NOT CONFIRMABLE. Likely H1 "Radisson Blu Hotels & Resorts"; H2s for key messaging sections.

**FAQ / Q&A presence:** NOT DETECTED in SERP

**Alt text observations:** NOT CONFIRMABLE

**Query compatibility notes:**
- "unparalleled service, comfort, and style" is brand voice, not query-answering copy
- No explicit answer to "Is Radisson Blu good for American business travelers in Europe?"
- "unforgettable experiences" and "small details" are marketing register, not information register
- Brand described as "upper upscale with business-meets-leisure guest mix" in external sources but this is NOT reflected in confirmed page metadata

**Entity signal notes:**
- "Radisson Blu Hotels & Resorts" as brand entity (strong in title)
- Service category "Hotels & Resorts" (present)
- Geographic scope: NOT mentioned in title or confirmed description
- Target traveler: NOT explicitly mentioned in confirmed metadata
- Business/leisure dimension: NOT in confirmed copy (present in external brand descriptions but not on-page)

---

## Page 4: https://www.radissonhotels.com/en-us/brands/radisson (Radisson Brand Page)

**URL:** https://www.radissonhotels.com/en-us/brands/radisson
**Fetch status:** 403 Blocked
**Fetch timestamp:** 2026-03-20
**Note:** Canonical at /en-us/brand/radisson

**Extracted title:** "Radisson | Hotel Deals | Yes I Can! Attitude"
**Source:** Google SERP snippet

**Extracted meta description:** NOT INDEPENDENTLY CONFIRMED. Brand copy from search snippets: "Our hotels reflect the communities and cultures they're in." Tagline: "Yes I Can!"

**Structured data blocks:** NOT CONFIRMABLE

**Open Graph tags:** NOT CONFIRMABLE

**Heading outline:** NOT CONFIRMABLE

**FAQ / Q&A presence:** NOT DETECTED

**Alt text observations:** NOT CONFIRMABLE

**Query compatibility notes:**
- Title is tagline-dominated ("Yes I Can! Attitude") — misaligned for AI query matching
- "Hotel Deals" signals transactional intent, not discovery/information intent favored by AI engines
- No geographic specificity, no traveler type in title
- Brand philosophy ("Yes I Can!") is not parseable as an answer to any bleisure traveler query

**Entity signal notes:**
- "Radisson" as named brand entity (present)
- Service: "Hotel" (present, singular, weak)
- Geographic: absent in confirmed metadata
- Traveler type: absent in confirmed metadata

---

## Page 5: https://www.radissonhotels.com/en-us/brands/park-plaza (Park Plaza Brand Page)

**URL:** https://www.radissonhotels.com/en-us/brands/park-plaza
**Fetch status:** 403 Blocked
**Fetch timestamp:** 2026-03-20

**Extracted title:** NOT CONFIRMED from search results in this run. Likely follows pattern "Park Plaza Hotels & Resorts | Radisson Hotels"

**Extracted meta description:** NOT CONFIRMED

**Structured data blocks:** NOT CONFIRMABLE

**Open Graph tags:** NOT CONFIRMABLE

**Heading outline:** NOT CONFIRMABLE

**FAQ / Q&A presence:** NOT DETECTED

**Alt text observations:** NOT CONFIRMABLE

**Query compatibility notes:** CANNOT ASSESS (no confirmed metadata)

**Entity signal notes:** CANNOT ASSESS (no confirmed metadata)

---

## Page 6: https://www.radissonhotels.com/en-us/hotels/london (London Hotels Page — Priority 2 Rotation)

**URL:** https://www.radissonhotels.com/en-us/hotels/london
**Fetch status:** 403 Blocked
**Fetch timestamp:** 2026-03-20
**Note:** Search results show content at /en-us/destination/united-kingdom/london (title: "Beloved secret spots and best hotels in London | Radisson Hotels"). The /hotels/london URL may redirect to this destination page.

**Extracted title (inferred):** "Beloved secret spots and best hotels in London | Radisson Hotels"
**Source:** Google SERP snippet for inferred redirect target

**Extracted meta description:** NOT INDEPENDENTLY CONFIRMED. Confirmed body copy: "London is centered along the iconic banks of the River Thames and is a bustling capital that is a kaleidoscope of culture, cuisine, and endless adventures waiting to be discovered. Iconic landmarks like Big Ben and Buckingham Palace stand supreme, proudly showcasing centuries of rich heritage."

**Structured data blocks:** NOT CONFIRMABLE. Individual London hotel pages (Canary Wharf, Bloomsbury, South Kensington, Euston Square, Tottenham Court Road, Marble Arch, Heathrow) confirmed to exist. Brand-level London page schema unknown.

**Open Graph tags:** NOT CONFIRMABLE

**Heading outline:** NOT CONFIRMABLE. Likely H1: "Hotels in London" or destination-focused; H2s for individual property listings or area descriptions.

**FAQ / Q&A presence:** NOT DETECTED in SERP for London overview page

**Alt text observations:** NOT CONFIRMABLE

**Query compatibility notes:**
- Title "Beloved secret spots and best hotels in London" — misaligned for American bleisure business traveler (no mention of business amenities, "secret spots" is tourism-oriented)
- Body copy describes tourist landmarks (Big Ben, Buckingham Palace) — leisure-first framing
- Individual property pages do mention business amenities (Canary Wharf "event spaces," Euston "meeting spaces", Heathrow "conference centre")
- No explicit American traveler targeting visible in confirmed metadata
- No compound bleisure query coverage visible ("hotel in London with meeting rooms and good WiFi for business travelers")

**Entity signal notes:**
- "Radisson Hotels" present (strong)
- "London" geographic entity present (strong)
- Individual property districts mentioned (Canary Wharf, Bloomsbury, South Kensington, Euston, Marble Arch, Heathrow) — geographic specificity adequate at individual level, weak at overview page level
- Business traveler type: absent from overview page title; present in individual pages
- American traveler: not detected anywhere in confirmed metadata

---

## Cross-Page Patterns

**Consistent across confirmed pages:**
- No FAQPage schema detected in SERP rich results for any audited URL
- No Hotel or LodgingBusiness schema detected in rich results for brand/overview pages
- Meta descriptions consistently use marketing register (CTAs, adjectives) rather than answer format
- No explicit American traveler targeting detected in any confirmed metadata
- No explicit bleisure compound content (business + leisure) visible at brand or overview level

**Notable absences:**
- No FAQ rich snippets for any Priority 1 page
- No star rating rich results for brand pages
- No "People also ask" appearances confirmed for main brand pages
- Schema visibility is essentially zero at the overview/brand page level based on SERP observation
