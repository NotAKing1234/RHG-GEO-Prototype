# Optimization Proposal - run_005

## Proposal Entries

### PROP-5001 - run_005_GAP-001

**1. Proposed change**
Restore HTTP 200 page-specific HTML for all public Park Plaza en-us brand, destination, hotel, meeting-event, and offer URLs selected in run_005, starting with https://www.radissonhotels.com/en-us/brand/park-plaza. Add CDN/WAF allow rules for verified Googlebot, Bingbot, OAI-SearchBot, ChatGPT-User, and PerplexityBot where policy permits, and use rate limits or 429 responses for abuse instead of the access-restricted template. Validate with a 478-URL recrawl that confirms unique page titles, body fingerprints, and schema/content extraction per URL.

**2. Source citation**
C01

**3. Current state**
Page-level retrieval is blocked across the selected Park Plaza set. AI systems cannot extract page-specific hotel, meeting, offer, destination, or booking facts from blocked URLs.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
Very high. This is the dependency for every other GEO fix; without retrievable official pages, assistants will ground answers in OTAs, maps, reviews, or competitors instead of Park Plaza-owned content.

**6. Priority tier**
P1

---

### PROP-5002 - run_005_GAP-002

**1. Proposed change**
After access is restored, run a locale QA pass for every selected en-us Park Plaza URL. Require each page to return US-English content, a self-referencing canonical, reciprocal hreflang alternates for equivalent language/region pages, and no canonical or hreflang reference to the access-restricted template. Start validation from https://www.radissonhotels.com/en-us/brand/park-plaza and extend it to all 478 selected URLs.

**2. Source citation**
C02

**3. Current state**
The locale most relevant to American travelers is not yielding retrievable page content. Locale/canonical quality cannot be validated because the access template replaces the underlying English/US page.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
Very high. American travelers asking AI tools for official Park Plaza hotels in Europe need assistants to select the US-English official page, not a blocked template or uncertain regional fallback.

**6. Priority tier**
P1

---

### PROP-5003 - run_005_GAP-003

**1. Proposed change**
Generate server-rendered Hotel or LodgingBusiness JSON-LD for each Park Plaza property URL, beginning with https://www.radissonhotels.com/en-us/hotels/park-plaza-amsterdam-airport/meeting-events and the related hotel overview pages. Use CMS fields for Hotel, PostalAddress, GeoCoordinates, amenityFeature, check-in/check-out, phone, official URL, image, star rating where official, aggregate rating only where visibly supported, and direct booking or offer URL where current. Add schema validation and visible-content parity checks to the run smoke process after access is fixed.

**2. Source citation**
C03

**3. Current state**
Property-level Hotel/LodgingBusiness schema, address, geo, amenity, rating, and booking facts are unavailable to AI systems for the selected Park Plaza hotel URLs.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
High after page access is restored. Complete hotel facts let AI assistants answer property-comparison queries such as Park Plaza hotels with meeting rooms, Wi-Fi, transit access, and weekend attractions from official data.

**6. Priority tier**
P1

---

### PROP-5004 - run_005_GAP-004

**1. Proposed change**
Publish crawlable Park Plaza meeting-event pages with property-specific capacity matrices, room names, floor area, layouts, AV/Wi-Fi/catering availability, accessibility, RFP/contact path, group-room booking path, and nearby leisure context. Add MeetingRoom/Place JSON-LD, including maximumAttendeeCapacity, floorSize, and amenityFeature, on pages such as https://www.radissonhotels.com/en-us/brand/park-plaza/meeting-conference and the 76 selected property meeting URLs.

**2. Source citation**
C04

**3. Current state**
Meeting-room capacity, RFP/contact paths, event services, Wi-Fi/AV/catering, and work-travel suitability are not retrievable from the selected meeting-event pages.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
High. American planners asking assistants for European hotels that can host meetings and weekend stays need official capacity and RFP facts to shortlist Park Plaza.

**6. Priority tier**
P1

---

### PROP-5005 - run_005_GAP-005

**1. Proposed change**
Unblock Park Plaza offer pages and add a structured offer module to each selected offer URL, beginning with https://www.radissonhotels.com/en-us/hotel-deals/park-plaza-family. Include offer name, discount/value proposition, eligible hotels, book-by date, stay window, cancellation/refund terms, Radisson Rewards hook, support URL, official booking CTA, and Offer JSON-LD with validity fields such as validThrough where dates are present. Expire or redirect offers automatically after the end date.

**2. Source citation**
C10

**3. Current state**
Offer and direct-booking pages cannot provide assistants with official booking routes, offer terms, cancellation/support cues, or loyalty hooks.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
Medium to high. AI assistants can recommend official direct-booking paths only when offer terms and booking routes are explicit and crawlable.

**6. Priority tier**
P2

---

### PROP-5006 - run_005_GAP-006

**1. Proposed change**
Serve https://www.radissonhotels.com/sitemap.xml as public HTTP 200 XML or a sitemap index before WAF/challenge rules. Segment Park Plaza sitemap coverage by brand, hotel/property, meetings, offers, and locale alternates; include only canonical 200 URLs with accurate lastmod; reference the sitemap in /robots.txt; and submit the sitemap index in Google Search Console and Bing Webmaster Tools.

**2. Source citation**
C01

**3. Current state**
The standard sitemap endpoint remains unavailable from this environment, weakening discovery even though individual sitemap-derived URLs are selected in SQLite.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
High and fast to measure. A public sitemap accelerates recrawl and gives search/AI systems a canonical URL map for long-tail Park Plaza property and meeting pages.

**6. Priority tier**
P1

---

### PROP-5007 - run_005_GAP-007

**1. Proposed change**
Publish https://www.radissonhotels.com/llms.txt as a concise official Markdown orientation file with sections for Radisson Hotel Group, Park Plaza, hotel discovery, meetings/events, offers, booking/support, loyalty, accessibility, and sitemap references. Generate it from approved CMS/source-of-truth data, include Last-Updated, and exclude internal/test/picklist URLs.

**2. Source citation**
C16

**3. Current state**
No AI-oriented site summary file is available. This is lower priority than restoring page access, but remains a cheap future-facing discoverability gap.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
Low to medium. It will not compensate for blocked pages, but it can give AI agents an official map once page access and sitemaps are fixed.

**6. Priority tier**
P3

---

### PROP-5008 - run_005_GAP-008

**1. Proposed change**
Remove utility, picklist, sitemap-like, and test-adjacent URL patterns from run_url_targets selection and from any generated public sitemaps, starting with https://www.radissonhotels.com/en-us/brand/park-plaza/meeting-conference/picklist. If utility endpoints must remain public, return crawlable noindex headers or disallow them in robots rules. Replace them in GEO selections with canonical production landing pages for Park Plaza properties, city/destination pages, meeting pages, and offers.

**2. Source citation**
C15

**3. Current state**
The run target set includes URLs that may not be production landing pages for AI travel discovery. They should be reviewed or excluded before stakeholder handoff unless they have a clear public purpose.

**4. Inferred implementation status**
N/A

**5. Directional impact estimate**
Medium. Cleaner target sets reduce crawl waste and AI confusion so assistants find useful Park Plaza meeting, property, city, and offer pages rather than internal utility pages.

**6. Priority tier**
P2

---
