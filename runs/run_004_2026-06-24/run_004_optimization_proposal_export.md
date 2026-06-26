# Optimization Proposal - run_004

## Proposal Entries

### PROP-4001 - run_004_GAP-001

**1. Proposed change**
Serve HTTP 200 HTML for all public Country Inn brand and hotel pages selected in run_004, especially /en-us/brand/country-inn, /en-us/brand/country-inn/business-travel-offer, and the selected /en-us/hotels/country-inn-* pages. Keep bot defense behavioral and rate-based rather than returning the Radisson/Akamai access-restricted template to normal search and AI retrieval crawlers. Validate with the same direct GET capture used in runs/run_004_2026-06-24/audit_capture.json.

**2. Source citation**
C01

**3. Current state**
Page-level retrieval remains blocked across the most important English/US Country Inn pages and multiple locale groups. AI systems cannot extract page-specific hotel facts from blocked URLs even though the root robots file is now reachable.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
Very high. Until the official pages return real HTML, AI travel assistants must rely on OTAs, stale snippets, or localized fallback pages rather than Radisson-owned Country Inn content.

**6. Priority tier**
P1

---

### PROP-4002 - run_004_GAP-002

**1. Proposed change**
Restore crawlable /en-us/ Country Inn brand, about, business-travel, breakfast, renovated-hotels, featured-hotels, sitemap, hotel overview, and hotel subpages. Add reciprocal hreflang links and x-default from accessible localized pages to the English/US equivalents, and confirm that the English/US pages return their own title/meta/canonical instead of the access-restricted template.

**2. Source citation**
C13

**3. Current state**
The locale most relevant to American travelers is blocked, while several localized non-US pages are accessible. This prevents US-origin AI prompts from landing on the intended English/US content path.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
Very high. The target audience is American travelers; blocking the US-English path prevents AI systems from routing US-origin prompts to the most relevant official Radisson content.

**6. Priority tier**
P1

---

### PROP-4003 - run_004_GAP-003

**1. Proposed change**
Serve https://www.radissonhotels.com/sitemap.xml or a sitemap-index URL as HTTP 200 XML. Include canonical public pages only, split by locale, brand, and hotel where needed, reference the sitemap in /robots.txt, and exclude banner-test or non-production URLs.

**2. Source citation**
C01

**3. Current state**
The root crawl rules are accessible, but the standard sitemap endpoint is not. This weakens discovery for assistants and search systems that rely on sitemap discovery or sitemap-index traversal.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
High. A fixed sitemap can be retested immediately and improves discovery, Search Console diagnostics, and canonical URL coverage for AI/search systems.

**6. Priority tier**
P1

---

### PROP-4004 - run_004_GAP-004

**1. Proposed change**
Add /llms.txt with a short official Radisson Hotel Group overview, supported domains, core brands, booking paths, canonical Country Inn brand/hotel URLs, US-to-Europe traveler guidance, and links to XML sitemaps. Keep it factual and update it from the same canonical source as sitemap/brand navigation.

**2. Source citation**
C01

**3. Current state**
No AI-oriented site summary file is present. This remains lower priority than page access and schema, but it is a cheap future-facing protocol gap.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
Low to medium. It will not compensate for blocked HTML, but it gives AI agents an official orientation file once the main crawl path is fixed.

**6. Priority tier**
P3

---

### PROP-4005 - run_004_GAP-005

**1. Proposed change**
Add validated Hotel or LodgingBusiness JSON-LD to every Country Inn hotel overview page with name, url, brand, description, address, geo, telephone, image, amenityFeature, checkInTime, checkOutTime, aggregateRating where valid, and a booking potentialAction or direct booking URL. Keep Organization schema for brand/corporate pages, but do not use it as a substitute for hotel entity markup.

**2. Source citation**
C03

**3. Current state**
Country Inn pages are machine-readable as organization/website pages, but not as hotel/lodging entities. AI hotel assistants cannot parse hotel amenities, place details, ratings, rooms, or booking facts from schema.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
Very high once pages are crawlable. Hotel schema gives AI systems machine-readable property, amenity, review, place, and booking facts instead of forcing inference from generic brand copy.

**6. Priority tier**
P1

---

### PROP-4006 - run_004_GAP-006

**1. Proposed change**
Return HTTP 200 for the 9 selected Country Inn hotel overview pages and 6 selected Bathinda hotel subpages. For each property, expose canonical URL, reciprocal hreflang, address, geo, telephone, room/amenity data, meeting/dining/local-attraction sections, review route, and direct booking deep links. Use the same fields in visible copy and Hotel JSON-LD.

**2. Source citation**
C04

**3. Current state**
Individual hotel pages cannot be evaluated or retrieved by AI systems from this environment. Property-level address, geo, review, meeting, dining, and local details are blocked.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
Very high. Property pages are the point where AI assistants can move from brand discovery to concrete hotel recommendation and booking.

**6. Priority tier**
P1

---

### PROP-4007 - run_004_GAP-007

**1. Proposed change**
Add a reusable Country Inn work-leisure module to brand and hotel pages: desk/workspace, Wi-Fi, breakfast, meeting room, parking, late checkout where offered, transit access, and nearby leisure. Map the same fields into amenityFeature on hotel pages. Prioritize making the English/US business-travel page and selected hotel meeting-events page crawlable first.

**2. Source citation**
C07

**3. Current state**
Business-travel suitability is inconsistently reachable and not expressed as structured amenity data. The accessible French page helps, but the English/US path and selected hotel meeting-events page are blocked.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
Medium to high. This directly improves matching for compound prompts such as "European hotel for work meetings with breakfast and weekend sightseeing."

**6. Priority tier**
P2

---

### PROP-4008 - run_004_GAP-008

**1. Proposed change**
Add city, neighborhood, airport/train distance, business district, landmark, parking/shuttle, and public-transit fields to each Country Inn hotel page and selected brand/destination modules. Where a page is brand-level, link to city/property pages with named examples instead of leaving metadata generic.

**2. Source citation**
C08

**3. Current state**
The accessible metadata helps with brand and amenity discovery, but not city, district, airport, station, or nearby-business queries that AI travel assistants generate.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
Medium to high. AI systems need location facts to answer "near airport," "near client office," and "near sightseeing" prompts.

**6. Priority tier**
P2

---

### PROP-4009 - run_004_GAP-009

**1. Proposed change**
Add visible FAQ blocks and matching FAQPage JSON-LD where the Q&A appears on page. Start with questions about check-in/out, breakfast, Wi-Fi, parking, accessibility, business amenities, meeting rooms, transit, local attractions, and weekend leisure add-ons. Do not add hidden or unsupported FAQ schema.

**2. Source citation**
C05

**3. Current state**
Useful Q&A content is not consistently exposed as visible, structured, page-aligned FAQ data, and the target English/US pages are blocked. This limits direct answers to breakfast, Wi-Fi, meeting, parking, and business-travel questions.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
Medium. It improves assistant follow-up answers, but it depends on crawlable pages and should not be prioritized above access and hotel schema.

**6. Priority tier**
P2

---

### PROP-4010 - run_004_GAP-010

**1. Proposed change**
Move banner-tests URLs behind authentication or return noindex via meta robots or X-Robots-Tag; remove them from XML sitemaps, registry selection, and future run targets. Add a pre-run selection check that rejects public URLs with empty title, meta description, canonical, OG fields, and structured data unless explicitly marked as test-only.

**2. Source citation**
C17

**3. Current state**
Non-production or testing URLs appear in the run target set and are publicly fetchable without meaningful metadata. These pages should not be selected for GEO audit or indexation unless intentionally public.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
Medium. This is a fast cleanup that prevents AI/search systems and future audits from sampling broken test pages.

**6. Priority tier**
P2

---

### PROP-4011 - run_004_GAP-011

**1. Proposed change**
Create Country Inn metadata/content clusters that combine "US traveler + Europe destination + business need + leisure need + amenity + booking constraint." For example: "Country Inn hotels for US business travelers in Europe with free breakfast, Wi-Fi, meeting access, and weekend sightseeing nearby." Apply this to title/meta where appropriate, first-screen copy, FAQ blocks, and hotel page modules.

**2. Source citation**
C02

**3. Current state**
The current metadata is useful for broad brand/amenity queries but weak for AI fan-out prompts such as business district + breakfast + Wi-Fi + weekend leisure + US traveler.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
Medium to high. This gives AI engines source text for synthesized bleisure answers rather than broad, disconnected brand and amenity snippets.

**6. Priority tier**
P2

---

### PROP-4012 - run_004_GAP-012

**1. Proposed change**
After unblocking the English/US pages, add page-specific OG images and gallery alt text for rooms, desks, meeting rooms, breakfast, exterior, transit, and nearby attractions. Tie image fields into Hotel JSON-LD where valid and avoid keyword-stuffed alt text.

**2. Source citation**
C15

**3. Current state**
AI and visual search surfaces cannot reliably understand rooms, breakfast, meetings, exterior/location, or amenity visuals for the most relevant US path.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
Low to medium. Helpful for visual search and AI confidence, but secondary to retrieval, schema, and content specificity.

**6. Priority tier**
P3

---

### PROP-4013 - run_004_GAP-013

**1. Proposed change**
Add a crawlable /en-us/brand/country-inn/business-leisure-europe or equivalent hub for American travelers planning Europe work trips with weekend stays. Link to relevant hotel/city pages and include work amenities, weekend attractions, transit, breakfast/Wi-Fi, loyalty benefits, direct booking support, and customer-service trust cues.

**2. Source citation**
C15

**3. Current state**
The current selected set cannot answer American bleisure prompts from the intended English/US pages, despite literature showing travelers use AI for planning and trusted brands for booking.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
High. It gives AI systems a direct Radisson-owned answer source for the target audience rather than relying on OTAs or generic localized pages.

**6. Priority tier**
P1

---

### PROP-4014 - run_004_GAP-014

**1. Proposed change**
Unblock selected hotel review pages and add visible review summaries plus valid aggregateRating/Review markup where Radisson owns or can lawfully display the review data. Include review count, rating, review source, and recency in visible copy, and keep claims consistent across official hotel pages, Google Business Profile, and OTAs.

**2. Source citation**
C09

**3. Current state**
AI hotel assistants lean on reviews and consensus. Country Inn brand pages expose amenities but not review/rating evidence, and selected review/property pages are inaccessible.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
Medium to high. Reviews and consensus help AI systems compare trust and quality, especially for international travelers choosing between brands and OTAs.

**6. Priority tier**
P2

---

### PROP-4015 - run_004_GAP-015

**1. Proposed change**
Start a three-track AI distribution roadmap: (a) evaluate an OpenAI Apps SDK / ChatGPT app that searches Radisson inventory and deep-links to direct booking; (b) evaluate Claude connector or MCP-style hotel-search endpoint with live availability, policies, loyalty-safe flows, and booking links; (c) expose a public hotel-search/feed layer that keeps OTA, sitemap, schema, and direct-booking data in parity.

**2. Source citation**
C10

**3. Current state**
Radisson remains dependent on standard web/OTA surfaces while AI-native travel discovery becomes bookable through assistants and connectors.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
Very high long-term. Radisson remains passive in AI planning surfaces while OTAs and competitors become action-capable sources inside assistant workflows.

**6. Priority tier**
P1

---
