# Gap Analysis — run_004 | 2026-06-24

**Audit summary:** 100 DB-selected Country Inn URLs were audited from SQLite `run_url_targets`. 58 returned HTTP 403 access-restricted templates and 42 returned HTTP 200. The root `robots.txt` probe improved to HTTP 200, but page-level blocking persists for all English/US selected pages and every selected hotel page. Accessible localized pages expose Organization/Breadcrumb schema but not Hotel/LodgingBusiness schema.

Total gaps this run: **15** (4 new or newly explicit, 11 recurring or persistent themes)

## Per-Page Coverage Statement
Every selected page is represented in `metadata_snapshot.md`. No selected page is omitted from the audit. Each page maps to at least one grouped gap below: blocked pages map primarily to GAP-001/GAP-002/GAP-006; accessible brand pages map primarily to GAP-005/GAP-008/GAP-011/GAP-014; banner-test pages map to GAP-010.

### GAP-001
- **Gap ID:** GAP-001
- **Page URL:** https://www.radissonhotels.com/en-us/brand/country-inn
- **Criterion:** C01 — AI Crawler and Index Access
- **Current metadata state:** 58 of 100 selected URLs returned HTTP 403 access-restricted templates; representative English/US brand page blocked. `/robots.txt` is now HTTP 200, but `/sitemap.xml` is still HTTP 403.
- **Gap type:** MISSING
- **Gap description:** Page-level retrieval remains blocked across the most important English/US Country Inn pages and multiple locale groups. AI systems cannot extract page-specific hotel facts from blocked URLs even though the root robots file is now reachable.
- **Severity:** 3
- **New or recurring:** RECURRING from run_001-run_004; partial robots improvement only
- **Status:** RECURRING from run_001-run_004; partial robots improvement only
- **Affected URLs:**
  - https://www.radissonhotels.com/hr-hr/brand/country-inn (hr-hr brand)
  - https://www.radissonhotels.com/hr-hr/brand/country-inn/featured-hotels (hr-hr brand)
  - https://www.radissonhotels.com/hr-hr/brand/country-inn/mapa-stranice (hr-hr brand)
  - https://www.radissonhotels.com/zh-cn/brand/country-inn (zh-cn China brand)
  - https://www.radissonhotels.com/zh-cn/brand/country-inn/about (zh-cn China brand)
  - https://www.radissonhotels.com/zh-cn/brand/country-inn/featured-hotels (zh-cn China brand)
  - https://www.radissonhotels.com/zh-cn/brand/country-inn/sitemap (zh-cn China brand)
  - https://www.radissonhotels.com/da-dk/brand/country-inn (da-dk Denmark brand)
  - https://www.radissonhotels.com/da-dk/brand/country-inn/banner-tests (da-dk Denmark brand)
  - https://www.radissonhotels.com/da-dk/brand/country-inn/forretningsrejse-tilbud (da-dk Denmark brand)
  - https://www.radissonhotels.com/da-dk/brand/country-inn/fremhaevede-hoteller (da-dk Denmark brand)
  - https://www.radissonhotels.com/da-dk/brand/country-inn/gratis-hotelmorgenmad (da-dk Denmark brand)
  - https://www.radissonhotels.com/da-dk/brand/country-inn/hotel-lending-library (da-dk Denmark brand)
  - https://www.radissonhotels.com/da-dk/brand/country-inn/istandsatte-hoteller (da-dk Denmark brand)
  - https://www.radissonhotels.com/da-dk/brand/country-inn/om (da-dk Denmark brand)
  - https://www.radissonhotels.com/da-dk/brand/country-inn/sitemap (da-dk Denmark brand)
  - https://www.radissonhotels.com/nl-nl/brand/country-inn (nl-nl Netherlands brand)
  - https://www.radissonhotels.com/nl-nl/brand/country-inn/nieuwe-hotels-opening (nl-nl Netherlands brand)
  - ... 40 additional URLs listed in metadata_snapshot.md and audit_capture.json

### GAP-002
- **Gap ID:** GAP-002
- **Page URL:** https://www.radissonhotels.com/en-us/brand/country-inn
- **Criterion:** C13 — Locale, Hreflang, and Canonical Clarity
- **Current metadata state:** All 23 selected `en-us` Country Inn URLs returned HTTP 403 while 42 localized European pages returned HTTP 200.
- **Gap type:** MISALIGNED
- **Gap description:** The locale most relevant to American travelers is blocked, while several localized non-US pages are accessible. This prevents US-origin AI prompts from landing on the intended English/US content path.
- **Severity:** 3
- **New or recurring:** NEW in current selected target family; related to recurring access gap
- **Status:** NEW in current selected target family; related to recurring access gap
- **Affected URLs:**
  - https://www.radissonhotels.com/en-us/brand/country-inn (en-us United States brand)
  - https://www.radissonhotels.com/en-us/brand/country-inn/about (en-us United States brand)
  - https://www.radissonhotels.com/en-us/brand/country-inn/business-travel-offer (en-us United States brand)
  - https://www.radissonhotels.com/en-us/brand/country-inn/featured-hotels (en-us United States brand)
  - https://www.radissonhotels.com/en-us/brand/country-inn/free-hotel-breakfast (en-us United States brand)
  - https://www.radissonhotels.com/en-us/brand/country-inn/hotel-lending-library (en-us United States brand)
  - https://www.radissonhotels.com/en-us/brand/country-inn/renovated-hotels (en-us United States brand)
  - https://www.radissonhotels.com/en-us/brand/country-inn/sitemap (en-us United States brand)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-bathinda (en-us United States hotel_overview)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-bengaluru (en-us United States hotel_overview)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-gurgaon-sector-12 (en-us United States hotel_overview)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-jammu (en-us United States hotel_overview)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-kota (en-us United States hotel_overview)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-manipal (en-us United States hotel_overview)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-sahibabad (en-us United States hotel_overview)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-sonamarg (en-us United States hotel_overview)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-zirakpur (en-us United States hotel_overview)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-bathinda/attractions (en-us United States hotel_subpage)
  - ... 5 additional URLs listed in metadata_snapshot.md and audit_capture.json

### GAP-003
- **Gap ID:** GAP-003
- **Page URL:** https://www.radissonhotels.com/sitemap.xml
- **Criterion:** C01 — AI Crawler and Index Access
- **Current metadata state:** Domain `/sitemap.xml` returned HTTP 403 XML AccessDenied while `/robots.txt` returned HTTP 200.
- **Gap type:** WEAK
- **Gap description:** The root crawl rules are accessible, but the standard sitemap endpoint is not. This weakens discovery for assistants and search systems that rely on sitemap discovery or sitemap-index traversal.
- **Severity:** 2
- **New or recurring:** RECURRING technical access theme from run_001-run_004
- **Status:** RECURRING technical access theme from run_001-run_004

### GAP-004
- **Gap ID:** GAP-004
- **Page URL:** https://www.radissonhotels.com/llms.txt
- **Criterion:** C01 — AI Crawler and Index Access
- **Current metadata state:** `/llms.txt` returned HTTP 404 with a normal Radisson page-not-found document.
- **Gap type:** MISSING
- **Gap description:** No AI-oriented site summary file is present. This remains lower priority than page access and schema, but it is a cheap future-facing protocol gap.
- **Severity:** 1
- **New or recurring:** RECURRING from run_002-run_004
- **Status:** RECURRING from run_002-run_004

### GAP-005
- **Gap ID:** GAP-005
- **Page URL:** https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn
- **Criterion:** C03 — Hotel/LodgingBusiness Structured Data
- **Current metadata state:** Accessible pages expose `Organization` JSON-LD on 41 pages and `BreadcrumbList` on 30 pages; 0 accessible selected pages expose `Hotel` or `LodgingBusiness`.
- **Gap type:** MISSING
- **Gap description:** Country Inn pages are machine-readable as organization/website pages, but not as hotel/lodging entities. AI hotel assistants cannot parse hotel amenities, place details, ratings, rooms, or booking facts from schema.
- **Severity:** 3
- **New or recurring:** RECURRING from run_001-run_004; now confirmed on accessible localized Country Inn pages
- **Status:** RECURRING from run_001-run_004; now confirmed on accessible localized Country Inn pages
- **Affected URLs:**
  - https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn (fi-fi Finland brand)
  - https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn/sivustokartta (fi-fi Finland brand)
  - https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn/tietoja (fi-fi Finland brand)
  - https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn/uudet-avautuvat-hotellit (fi-fi Finland brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/a-propos (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/offres-voyage-d-affaires (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/ouverture-nouvel-hotel (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/petit-dejeuner-hotel-gratuit (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/plan-du-site (fr-fr France brand)
  - https://www.radissonhotels.com/de-de/marke/country-inn (de-de Germany brand)
  - https://www.radissonhotels.com/de-de/marke/country-inn/inhaltsuebersicht (de-de Germany brand)
  - https://www.radissonhotels.com/de-de/marke/country-inn/neue-hotels-oeffnungen (de-de Germany brand)
  - https://www.radissonhotels.com/de-de/marke/country-inn/ueber (de-de Germany brand)
  - https://www.radissonhotels.com/it-it/marca/country-inn (it-it Italy brand)
  - https://www.radissonhotels.com/it-it/marca/country-inn/informazioni (it-it Italy brand)
  - https://www.radissonhotels.com/it-it/marca/country-inn/mappa-del-sito (it-it Italy brand)
  - https://www.radissonhotels.com/it-it/marca/country-inn/nuova-apertura-hotel (it-it Italy brand)
  - ... 24 additional URLs listed in metadata_snapshot.md and audit_capture.json

### GAP-006
- **Gap ID:** GAP-006
- **Page URL:** https://www.radissonhotels.com/en-us/hotels/country-inn-bathinda
- **Criterion:** C04 — Local Business and Place Detail Completeness
- **Current metadata state:** All 9 selected hotel overview pages and all 6 selected Bathinda hotel subpages returned HTTP 403.
- **Gap type:** MISSING
- **Gap description:** Individual hotel pages cannot be evaluated or retrieved by AI systems from this environment. Property-level address, geo, review, meeting, dining, and local details are blocked.
- **Severity:** 3
- **New or recurring:** RECURRING from run_003 property-tier ambiguity; now confirmed for selected Country Inn hotel pages
- **Status:** RECURRING from run_003 property-tier ambiguity; now confirmed for selected Country Inn hotel pages
- **Affected URLs:**
  - https://www.radissonhotels.com/en-us/hotels/country-inn-bathinda (en-us United States hotel_overview)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-bengaluru (en-us United States hotel_overview)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-gurgaon-sector-12 (en-us United States hotel_overview)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-jammu (en-us United States hotel_overview)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-kota (en-us United States hotel_overview)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-manipal (en-us United States hotel_overview)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-sahibabad (en-us United States hotel_overview)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-sonamarg (en-us United States hotel_overview)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-zirakpur (en-us United States hotel_overview)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-bathinda/attractions (en-us United States hotel_subpage)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-bathinda/contact (en-us United States hotel_subpage)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-bathinda/deals (en-us United States hotel_subpage)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-bathinda/dining (en-us United States hotel_subpage)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-bathinda/meeting-events (en-us United States hotel_subpage)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-bathinda/reviews (en-us United States hotel_subpage)

### GAP-007
- **Gap ID:** GAP-007
- **Page URL:** https://www.radissonhotels.com/fr-fr/marque/country-inn/offres-voyage-d-affaires
- **Criterion:** C07 — Structured Amenity and Work-Leisure Data
- **Current metadata state:** French business-travel page is accessible and mentions business travelers; English/US, Danish, and Traditional Chinese business-travel equivalents are blocked. Accessible brand pages emphasize breakfast/Wi-Fi but not structured meeting/work-leisure data.
- **Gap type:** WEAK
- **Gap description:** Business-travel suitability is inconsistently reachable and not expressed as structured amenity data. The accessible French page helps, but the English/US path and selected hotel meeting-events page are blocked.
- **Severity:** 2
- **New or recurring:** RECURRING bleisure/work-travel exposure theme from run_002-run_004
- **Status:** RECURRING bleisure/work-travel exposure theme from run_002-run_004
- **Affected URLs:**
  - https://www.radissonhotels.com/da-dk/brand/country-inn/forretningsrejse-tilbud (da-dk Denmark brand)
  - https://www.radissonhotels.com/da-dk/brand/country-inn/hotel-lending-library (da-dk Denmark brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/offres-voyage-d-affaires (fr-fr France brand)
  - https://www.radissonhotels.com/zh-tw/brand/country-inn/business-travel-offer (zh-tw Taiwan brand)
  - https://www.radissonhotels.com/tr-tr/marka/country-inn/hotel-lending-library (tr-tr Turkey brand)
  - https://www.radissonhotels.com/en-us/brand/country-inn/business-travel-offer (en-us United States brand)
  - https://www.radissonhotels.com/en-us/brand/country-inn/hotel-lending-library (en-us United States brand)
  - https://www.radissonhotels.com/en-us/hotels/country-inn-bathinda/meeting-events (en-us United States hotel_subpage)

### GAP-008
- **Gap ID:** GAP-008
- **Page URL:** https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn
- **Criterion:** C08 — Geographic and Transport Specificity
- **Current metadata state:** Accessible Country Inn brand pages are mostly generic brand or feature pages; hotel/location pages are blocked. 42 accessible brand pages lacked clear city/neighborhood/transport/business-district wording in title/meta.
- **Gap type:** WEAK
- **Gap description:** The accessible metadata helps with brand and amenity discovery, but not city, district, airport, station, or nearby-business queries that AI travel assistants generate.
- **Severity:** 2
- **New or recurring:** RECURRING geographic specificity theme from run_002-run_004
- **Status:** RECURRING geographic specificity theme from run_002-run_004
- **Affected URLs:**
  - https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn (fi-fi Finland brand)
  - https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn/sivustokartta (fi-fi Finland brand)
  - https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn/tietoja (fi-fi Finland brand)
  - https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn/uudet-avautuvat-hotellit (fi-fi Finland brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/a-propos (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/offres-voyage-d-affaires (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/ouverture-nouvel-hotel (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/petit-dejeuner-hotel-gratuit (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/plan-du-site (fr-fr France brand)
  - https://www.radissonhotels.com/de-de/marke/country-inn (de-de Germany brand)
  - https://www.radissonhotels.com/de-de/marke/country-inn/inhaltsuebersicht (de-de Germany brand)
  - https://www.radissonhotels.com/de-de/marke/country-inn/neue-hotels-oeffnungen (de-de Germany brand)
  - https://www.radissonhotels.com/de-de/marke/country-inn/ueber (de-de Germany brand)
  - https://www.radissonhotels.com/it-it/marca/country-inn (it-it Italy brand)
  - https://www.radissonhotels.com/it-it/marca/country-inn/informazioni (it-it Italy brand)
  - https://www.radissonhotels.com/it-it/marca/country-inn/mappa-del-sito (it-it Italy brand)
  - https://www.radissonhotels.com/it-it/marca/country-inn/nuova-apertura-hotel (it-it Italy brand)
  - ... 24 additional URLs listed in metadata_snapshot.md and audit_capture.json

### GAP-009
- **Gap ID:** GAP-009
- **Page URL:** https://www.radissonhotels.com/fr-fr/marque/country-inn
- **Criterion:** C05 — Visible Q&A and FAQ Integrity
- **Current metadata state:** 19 accessible pages had textual FAQ/Q&A markers by regex, but no accessible selected page exposed `FAQPage` JSON-LD. Blocked English/US pages cannot be evaluated.
- **Gap type:** WEAK
- **Gap description:** Useful Q&A content is not consistently exposed as visible, structured, page-aligned FAQ data, and the target English/US pages are blocked. This limits direct answers to breakfast, Wi-Fi, meeting, parking, and business-travel questions.
- **Severity:** 2
- **New or recurring:** RECURRING from run_001-run_004, reframed after run_004 literature
- **Status:** RECURRING from run_001-run_004, reframed after run_004 literature
- **Affected URLs:**
  - https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn (fi-fi Finland brand)
  - https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn/sivustokartta (fi-fi Finland brand)
  - https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn/tietoja (fi-fi Finland brand)
  - https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn/uudet-avautuvat-hotellit (fi-fi Finland brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/a-propos (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/offres-voyage-d-affaires (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/ouverture-nouvel-hotel (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/petit-dejeuner-hotel-gratuit (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/plan-du-site (fr-fr France brand)
  - https://www.radissonhotels.com/de-de/marke/country-inn (de-de Germany brand)
  - https://www.radissonhotels.com/de-de/marke/country-inn/inhaltsuebersicht (de-de Germany brand)
  - https://www.radissonhotels.com/de-de/marke/country-inn/neue-hotels-oeffnungen (de-de Germany brand)
  - https://www.radissonhotels.com/de-de/marke/country-inn/ueber (de-de Germany brand)
  - https://www.radissonhotels.com/it-it/marca/country-inn (it-it Italy brand)
  - https://www.radissonhotels.com/it-it/marca/country-inn/informazioni (it-it Italy brand)
  - https://www.radissonhotels.com/it-it/marca/country-inn/mappa-del-sito (it-it Italy brand)
  - https://www.radissonhotels.com/it-it/marca/country-inn/nuova-apertura-hotel (it-it Italy brand)
  - ... 24 additional URLs listed in metadata_snapshot.md and audit_capture.json

### GAP-010
- **Gap ID:** GAP-010
- **Page URL:** https://www.radissonhotels.com/sv-se/marke/country-inn/banner-tests
- **Criterion:** C17 — Anti-Spam and Markup Honesty
- **Current metadata state:** Two selected `banner-tests` URLs returned HTTP 200 with empty title, meta description, canonical, OG fields, and structured data.
- **Gap type:** MISSING
- **Gap description:** Non-production or testing URLs appear in the run target set and are publicly fetchable without meaningful metadata. These pages should not be selected for GEO audit or indexation unless intentionally public.
- **Severity:** 2
- **New or recurring:** NEW in run_004 selected target set
- **Status:** NEW in run_004 selected target set
- **Affected URLs:**
  - https://www.radissonhotels.com/sv-se/marke/country-inn/banner-tests (sv-se Sweden brand)
  - https://www.radissonhotels.com/tr-tr/marka/country-inn/banner-tests (tr-tr Turkey brand)

### GAP-011
- **Gap ID:** GAP-011
- **Page URL:** https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn
- **Criterion:** C02 — Query Fan-Out Coverage
- **Current metadata state:** Accessible titles/meta generally cover brand and amenities such as breakfast, coffee maker, and Wi-Fi, but do not combine location, business need, leisure need, and traveler identity in one answer-ready surface.
- **Gap type:** WEAK
- **Gap description:** The current metadata is useful for broad brand/amenity queries but weak for AI fan-out prompts such as business district + breakfast + Wi-Fi + weekend leisure + US traveler.
- **Severity:** 2
- **New or recurring:** RECURRING query-compatibility theme from run_001-run_004
- **Status:** RECURRING query-compatibility theme from run_001-run_004
- **Affected URLs:**
  - https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn (fi-fi Finland brand)
  - https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn/sivustokartta (fi-fi Finland brand)
  - https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn/tietoja (fi-fi Finland brand)
  - https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn/uudet-avautuvat-hotellit (fi-fi Finland brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/a-propos (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/offres-voyage-d-affaires (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/ouverture-nouvel-hotel (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/petit-dejeuner-hotel-gratuit (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/plan-du-site (fr-fr France brand)
  - https://www.radissonhotels.com/de-de/marke/country-inn (de-de Germany brand)
  - https://www.radissonhotels.com/de-de/marke/country-inn/inhaltsuebersicht (de-de Germany brand)
  - https://www.radissonhotels.com/de-de/marke/country-inn/neue-hotels-oeffnungen (de-de Germany brand)
  - https://www.radissonhotels.com/de-de/marke/country-inn/ueber (de-de Germany brand)
  - https://www.radissonhotels.com/it-it/marca/country-inn (it-it Italy brand)
  - https://www.radissonhotels.com/it-it/marca/country-inn/informazioni (it-it Italy brand)
  - https://www.radissonhotels.com/it-it/marca/country-inn/mappa-del-sito (it-it Italy brand)
  - https://www.radissonhotels.com/it-it/marca/country-inn/nuova-apertura-hotel (it-it Italy brand)
  - ... 24 additional URLs listed in metadata_snapshot.md and audit_capture.json

### GAP-012
- **Gap ID:** GAP-012
- **Page URL:** https://www.radissonhotels.com/en-us/brand/country-inn
- **Criterion:** C15 — Image Accessibility and Visual Context
- **Current metadata state:** Blocked English/US pages expose no page-specific image/alt context; accessible localized pages expose OG images, but image alt samples are limited and not tied to rooms/meetings/local attractions in captured metadata.
- **Gap type:** WEAK
- **Gap description:** AI and visual search surfaces cannot reliably understand rooms, breakfast, meetings, exterior/location, or amenity visuals for the most relevant US path.
- **Severity:** 1
- **New or recurring:** NEW as explicit run_004 criterion; related accessibility gap existed implicitly
- **Status:** NEW as explicit run_004 criterion; related accessibility gap existed implicitly

### GAP-013
- **Gap ID:** GAP-013
- **Page URL:** https://www.radissonhotels.com/en-us/brand/country-inn
- **Criterion:** C15 — American Bleisure Traveler Queries / C11 — Booking Trust
- **Current metadata state:** English/US Country Inn brand, business-travel, free-breakfast, renovated-hotels, and hotel pages are blocked. Accessible localized pages do not address US-to-Europe or American traveler context.
- **Gap type:** MISSING
- **Gap description:** The current selected set cannot answer American bleisure prompts from the intended English/US pages, despite literature showing travelers use AI for planning and trusted brands for booking.
- **Severity:** 3
- **New or recurring:** RECURRING from run_002-run_004
- **Status:** RECURRING from run_002-run_004

### GAP-014
- **Gap ID:** GAP-014
- **Page URL:** https://www.radissonhotels.com/en-us/brand/country-inn
- **Criterion:** C09 — Trust, Reviews, and Consensus Footprint
- **Current metadata state:** 0 accessible selected pages exposed review or aggregateRating schema; selected hotel review pages are blocked.
- **Gap type:** MISSING
- **Gap description:** AI hotel assistants lean on reviews and consensus. Country Inn brand pages expose amenities but not review/rating evidence, and selected review/property pages are inaccessible.
- **Severity:** 2
- **New or recurring:** RECURRING OTA/review completeness theme from run_002-run_004
- **Status:** RECURRING OTA/review completeness theme from run_002-run_004
- **Affected URLs:**
  - https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn (fi-fi Finland brand)
  - https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn/sivustokartta (fi-fi Finland brand)
  - https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn/tietoja (fi-fi Finland brand)
  - https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn/uudet-avautuvat-hotellit (fi-fi Finland brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/a-propos (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/offres-voyage-d-affaires (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/ouverture-nouvel-hotel (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/petit-dejeuner-hotel-gratuit (fr-fr France brand)
  - https://www.radissonhotels.com/fr-fr/marque/country-inn/plan-du-site (fr-fr France brand)
  - https://www.radissonhotels.com/de-de/marke/country-inn (de-de Germany brand)
  - https://www.radissonhotels.com/de-de/marke/country-inn/inhaltsuebersicht (de-de Germany brand)
  - https://www.radissonhotels.com/de-de/marke/country-inn/neue-hotels-oeffnungen (de-de Germany brand)
  - https://www.radissonhotels.com/de-de/marke/country-inn/ueber (de-de Germany brand)
  - https://www.radissonhotels.com/it-it/marca/country-inn (it-it Italy brand)
  - https://www.radissonhotels.com/it-it/marca/country-inn/informazioni (it-it Italy brand)
  - https://www.radissonhotels.com/it-it/marca/country-inn/mappa-del-sito (it-it Italy brand)
  - https://www.radissonhotels.com/it-it/marca/country-inn/nuova-apertura-hotel (it-it Italy brand)
  - ... 24 additional URLs listed in metadata_snapshot.md and audit_capture.json

### GAP-015
- **Gap ID:** GAP-015
- **Page URL:** https://www.radissonhotels.com/en-us/brand/country-inn
- **Criterion:** C10 — Direct AI Travel Distribution Readiness
- **Current metadata state:** Current literature found Booking.com/Expedia in ChatGPT apps, Expedia in Claude, and KAYAK Ask AI; no Radisson AI app/connector/direct assistant distribution was detected.
- **Gap type:** MISSING
- **Gap description:** Radisson remains dependent on standard web/OTA surfaces while AI-native travel discovery becomes bookable through assistants and connectors.
- **Severity:** 3
- **New or recurring:** RECURRING from run_003-run_004
- **Status:** RECURRING from run_003-run_004

## Selected URL Coverage Matrix

Coverage check: **100 of 100 selected SQLite `run_url_targets` URLs are represented below and in `metadata_snapshot.md`. Technical probes such as `/robots.txt`, `/llms.txt`, and `/sitemap.xml` are excluded from this selected-link count.

| # | Selected URL | Fetch status | Locale | Page type | Applied gap IDs |
|---:|---|---|---|---|---|
| 1 | https://www.radissonhotels.com/hr-hr/brand/country-inn | http_403 | hr-hr | brand | GAP-001 |
| 2 | https://www.radissonhotels.com/hr-hr/brand/country-inn/featured-hotels | http_403 | hr-hr | brand | GAP-001 |
| 3 | https://www.radissonhotels.com/hr-hr/brand/country-inn/mapa-stranice | http_403 | hr-hr | brand | GAP-001 |
| 4 | https://www.radissonhotels.com/zh-cn/brand/country-inn | http_403 | zh-cn | brand | GAP-001 |
| 5 | https://www.radissonhotels.com/zh-cn/brand/country-inn/about | http_403 | zh-cn | brand | GAP-001 |
| 6 | https://www.radissonhotels.com/zh-cn/brand/country-inn/featured-hotels | http_403 | zh-cn | brand | GAP-001 |
| 7 | https://www.radissonhotels.com/zh-cn/brand/country-inn/sitemap | http_403 | zh-cn | brand | GAP-001 |
| 8 | https://www.radissonhotels.com/da-dk/brand/country-inn | http_403 | da-dk | brand | GAP-001 |
| 9 | https://www.radissonhotels.com/da-dk/brand/country-inn/banner-tests | http_403 | da-dk | brand | GAP-001 |
| 10 | https://www.radissonhotels.com/da-dk/brand/country-inn/forretningsrejse-tilbud | http_403 | da-dk | brand | GAP-001, GAP-007 |
| 11 | https://www.radissonhotels.com/da-dk/brand/country-inn/fremhaevede-hoteller | http_403 | da-dk | brand | GAP-001 |
| 12 | https://www.radissonhotels.com/da-dk/brand/country-inn/gratis-hotelmorgenmad | http_403 | da-dk | brand | GAP-001 |
| 13 | https://www.radissonhotels.com/da-dk/brand/country-inn/hotel-lending-library | http_403 | da-dk | brand | GAP-001, GAP-007 |
| 14 | https://www.radissonhotels.com/da-dk/brand/country-inn/istandsatte-hoteller | http_403 | da-dk | brand | GAP-001 |
| 15 | https://www.radissonhotels.com/da-dk/brand/country-inn/om | http_403 | da-dk | brand | GAP-001 |
| 16 | https://www.radissonhotels.com/da-dk/brand/country-inn/sitemap | http_403 | da-dk | brand | GAP-001 |
| 17 | https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn | http_200 | fi-fi | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 18 | https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn/sivustokartta | http_200 | fi-fi | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 19 | https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn/tietoja | http_200 | fi-fi | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 20 | https://www.radissonhotels.com/fi-fi/tuotemerkki/country-inn/uudet-avautuvat-hotellit | http_200 | fi-fi | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 21 | https://www.radissonhotels.com/fr-fr/marque/country-inn | http_200 | fr-fr | brand | GAP-005, GAP-008, GAP-011, GAP-014, GAP-009 |
| 22 | https://www.radissonhotels.com/fr-fr/marque/country-inn/a-propos | http_200 | fr-fr | brand | GAP-005, GAP-008, GAP-011, GAP-014, GAP-009 |
| 23 | https://www.radissonhotels.com/fr-fr/marque/country-inn/offres-voyage-d-affaires | http_200 | fr-fr | brand | GAP-007, GAP-005, GAP-008, GAP-011, GAP-014, GAP-009 |
| 24 | https://www.radissonhotels.com/fr-fr/marque/country-inn/ouverture-nouvel-hotel | http_200 | fr-fr | brand | GAP-005, GAP-008, GAP-011, GAP-014, GAP-009 |
| 25 | https://www.radissonhotels.com/fr-fr/marque/country-inn/petit-dejeuner-hotel-gratuit | http_200 | fr-fr | brand | GAP-005, GAP-008, GAP-011, GAP-014, GAP-009 |
| 26 | https://www.radissonhotels.com/fr-fr/marque/country-inn/plan-du-site | http_200 | fr-fr | brand | GAP-005, GAP-008, GAP-011, GAP-014, GAP-009 |
| 27 | https://www.radissonhotels.com/de-de/marke/country-inn | http_200 | de-de | brand | GAP-005, GAP-008, GAP-011, GAP-014, GAP-009 |
| 28 | https://www.radissonhotels.com/de-de/marke/country-inn/inhaltsuebersicht | http_200 | de-de | brand | GAP-005, GAP-008, GAP-011, GAP-014, GAP-009 |
| 29 | https://www.radissonhotels.com/de-de/marke/country-inn/neue-hotels-oeffnungen | http_200 | de-de | brand | GAP-005, GAP-008, GAP-011, GAP-014, GAP-009 |
| 30 | https://www.radissonhotels.com/de-de/marke/country-inn/ueber | http_200 | de-de | brand | GAP-005, GAP-008, GAP-011, GAP-014, GAP-009 |
| 31 | https://www.radissonhotels.com/it-it/marca/country-inn | http_200 | it-it | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 32 | https://www.radissonhotels.com/it-it/marca/country-inn/informazioni | http_200 | it-it | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 33 | https://www.radissonhotels.com/it-it/marca/country-inn/mappa-del-sito | http_200 | it-it | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 34 | https://www.radissonhotels.com/it-it/marca/country-inn/nuova-apertura-hotel | http_200 | it-it | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 35 | https://www.radissonhotels.com/nl-nl/brand/country-inn | http_403 | nl-nl | brand | GAP-001 |
| 36 | https://www.radissonhotels.com/nl-nl/brand/country-inn/nieuwe-hotels-opening | http_403 | nl-nl | brand | GAP-001 |
| 37 | https://www.radissonhotels.com/nl-nl/brand/country-inn/over | http_403 | nl-nl | brand | GAP-001 |
| 38 | https://www.radissonhotels.com/nl-nl/brand/country-inn/sitemap | http_403 | nl-nl | brand | GAP-001 |
| 39 | https://www.radissonhotels.com/no-no/varemerke/country-inn | http_200 | no-no | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 40 | https://www.radissonhotels.com/no-no/varemerke/country-inn/nye-hotellapninger | http_200 | no-no | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 41 | https://www.radissonhotels.com/no-no/varemerke/country-inn/om | http_200 | no-no | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 42 | https://www.radissonhotels.com/no-no/varemerke/country-inn/sidekart | http_200 | no-no | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 43 | https://www.radissonhotels.com/pl-pl/marka/country-inn | http_200 | pl-pl | brand | GAP-005, GAP-008, GAP-011, GAP-014, GAP-009 |
| 44 | https://www.radissonhotels.com/pl-pl/marka/country-inn/mapa-witryny | http_200 | pl-pl | brand | GAP-005, GAP-008, GAP-011, GAP-014, GAP-009 |
| 45 | https://www.radissonhotels.com/pl-pl/marka/country-inn/nowe-hotele | http_200 | pl-pl | brand | GAP-005, GAP-008, GAP-011, GAP-014, GAP-009 |
| 46 | https://www.radissonhotels.com/pl-pl/marka/country-inn/opis | http_200 | pl-pl | brand | GAP-005, GAP-008, GAP-011, GAP-014, GAP-009 |
| 47 | https://www.radissonhotels.com/ru-ru/brand/country-inn | http_403 | ru-ru | brand | GAP-001 |
| 48 | https://www.radissonhotels.com/ru-ru/brand/country-inn/about | http_403 | ru-ru | brand | GAP-001 |
| 49 | https://www.radissonhotels.com/ru-ru/brand/country-inn/featured-hotels | http_403 | ru-ru | brand | GAP-001 |
| 50 | https://www.radissonhotels.com/ru-ru/brand/country-inn/sitemap | http_403 | ru-ru | brand | GAP-001 |
| 51 | https://www.radissonhotels.com/es-es/marca/country-inn | http_200 | es-es | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 52 | https://www.radissonhotels.com/es-es/marca/country-inn/acerca-de | http_200 | es-es | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 53 | https://www.radissonhotels.com/es-es/marca/country-inn/apertura-nuevos-hoteles | http_200 | es-es | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 54 | https://www.radissonhotels.com/es-es/marca/country-inn/desayuno-gratuito-en-el-hotel | http_200 | es-es | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 55 | https://www.radissonhotels.com/es-es/marca/country-inn/mapa-del-sitio | http_200 | es-es | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 56 | https://www.radissonhotels.com/sv-se/marke/country-inn | http_200 | sv-se | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 57 | https://www.radissonhotels.com/sv-se/marke/country-inn/banner-tests | http_200 | sv-se | brand | GAP-005, GAP-008, GAP-011, GAP-014, GAP-010 |
| 58 | https://www.radissonhotels.com/sv-se/marke/country-inn/nya-hotell-oppningar | http_200 | sv-se | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 59 | https://www.radissonhotels.com/sv-se/marke/country-inn/om | http_200 | sv-se | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 60 | https://www.radissonhotels.com/sv-se/marke/country-inn/sidkarta | http_200 | sv-se | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 61 | https://www.radissonhotels.com/zh-tw/brand/country-inn | http_403 | zh-tw | brand | GAP-001 |
| 62 | https://www.radissonhotels.com/zh-tw/brand/country-inn/about | http_403 | zh-tw | brand | GAP-001 |
| 63 | https://www.radissonhotels.com/zh-tw/brand/country-inn/business-travel-offer | http_403 | zh-tw | brand | GAP-001, GAP-007 |
| 64 | https://www.radissonhotels.com/zh-tw/brand/country-inn/featured-hotels | http_403 | zh-tw | brand | GAP-001 |
| 65 | https://www.radissonhotels.com/zh-tw/brand/country-inn/free-hotel-breakfast | http_403 | zh-tw | brand | GAP-001 |
| 66 | https://www.radissonhotels.com/zh-tw/brand/country-inn/renovated-hotels | http_403 | zh-tw | brand | GAP-001 |
| 67 | https://www.radissonhotels.com/zh-tw/brand/country-inn/sitemap | http_403 | zh-tw | brand | GAP-001 |
| 68 | https://www.radissonhotels.com/tr-tr/marka/country-inn | http_200 | tr-tr | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 69 | https://www.radissonhotels.com/tr-tr/marka/country-inn/acilacak-yeni-oteller | http_200 | tr-tr | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 70 | https://www.radissonhotels.com/tr-tr/marka/country-inn/banner-tests | http_200 | tr-tr | brand | GAP-005, GAP-008, GAP-011, GAP-014, GAP-010 |
| 71 | https://www.radissonhotels.com/tr-tr/marka/country-inn/hakkimizda | http_200 | tr-tr | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 72 | https://www.radissonhotels.com/tr-tr/marka/country-inn/hotel-lending-library | http_200 | tr-tr | brand | GAP-007, GAP-005, GAP-008, GAP-011, GAP-014 |
| 73 | https://www.radissonhotels.com/tr-tr/marka/country-inn/site-haritasi | http_200 | tr-tr | brand | GAP-005, GAP-008, GAP-011, GAP-014 |
| 74 | https://www.radissonhotels.com/ar-ae/brand/country-inn | http_403 | ar-ae | brand | GAP-001 |
| 75 | https://www.radissonhotels.com/ar-ae/brand/country-inn/about | http_403 | ar-ae | brand | GAP-001 |
| 76 | https://www.radissonhotels.com/ar-ae/brand/country-inn/featured-hotels | http_403 | ar-ae | brand | GAP-001 |
| 77 | https://www.radissonhotels.com/ar-ae/brand/country-inn/sitemap | http_403 | ar-ae | brand | GAP-001 |
| 78 | https://www.radissonhotels.com/en-us/brand/country-inn | http_403 | en-us | brand | GAP-001, GAP-002, GAP-013 |
| 79 | https://www.radissonhotels.com/en-us/brand/country-inn/about | http_403 | en-us | brand | GAP-001, GAP-002, GAP-013 |
| 80 | https://www.radissonhotels.com/en-us/brand/country-inn/business-travel-offer | http_403 | en-us | brand | GAP-001, GAP-002, GAP-013, GAP-007 |
| 81 | https://www.radissonhotels.com/en-us/brand/country-inn/featured-hotels | http_403 | en-us | brand | GAP-001, GAP-002, GAP-013 |
| 82 | https://www.radissonhotels.com/en-us/brand/country-inn/free-hotel-breakfast | http_403 | en-us | brand | GAP-001, GAP-002, GAP-013 |
| 83 | https://www.radissonhotels.com/en-us/brand/country-inn/hotel-lending-library | http_403 | en-us | brand | GAP-001, GAP-002, GAP-013, GAP-007 |
| 84 | https://www.radissonhotels.com/en-us/brand/country-inn/renovated-hotels | http_403 | en-us | brand | GAP-001, GAP-002, GAP-013 |
| 85 | https://www.radissonhotels.com/en-us/brand/country-inn/sitemap | http_403 | en-us | brand | GAP-001, GAP-002, GAP-013 |
| 86 | https://www.radissonhotels.com/en-us/hotels/country-inn-bathinda | http_403 | en-us | hotel_overview | GAP-001, GAP-002, GAP-013, GAP-006 |
| 87 | https://www.radissonhotels.com/en-us/hotels/country-inn-bengaluru | http_403 | en-us | hotel_overview | GAP-001, GAP-002, GAP-013, GAP-006 |
| 88 | https://www.radissonhotels.com/en-us/hotels/country-inn-gurgaon-sector-12 | http_403 | en-us | hotel_overview | GAP-001, GAP-002, GAP-013, GAP-006 |
| 89 | https://www.radissonhotels.com/en-us/hotels/country-inn-jammu | http_403 | en-us | hotel_overview | GAP-001, GAP-002, GAP-013, GAP-006 |
| 90 | https://www.radissonhotels.com/en-us/hotels/country-inn-kota | http_403 | en-us | hotel_overview | GAP-001, GAP-002, GAP-013, GAP-006 |
| 91 | https://www.radissonhotels.com/en-us/hotels/country-inn-manipal | http_403 | en-us | hotel_overview | GAP-001, GAP-002, GAP-013, GAP-006 |
| 92 | https://www.radissonhotels.com/en-us/hotels/country-inn-sahibabad | http_403 | en-us | hotel_overview | GAP-001, GAP-002, GAP-013, GAP-006 |
| 93 | https://www.radissonhotels.com/en-us/hotels/country-inn-sonamarg | http_403 | en-us | hotel_overview | GAP-001, GAP-002, GAP-013, GAP-006 |
| 94 | https://www.radissonhotels.com/en-us/hotels/country-inn-zirakpur | http_403 | en-us | hotel_overview | GAP-001, GAP-002, GAP-013, GAP-006 |
| 95 | https://www.radissonhotels.com/en-us/hotels/country-inn-bathinda/attractions | http_403 | en-us | hotel_subpage | GAP-001, GAP-002, GAP-013, GAP-006 |
| 96 | https://www.radissonhotels.com/en-us/hotels/country-inn-bathinda/contact | http_403 | en-us | hotel_subpage | GAP-001, GAP-002, GAP-013, GAP-006 |
| 97 | https://www.radissonhotels.com/en-us/hotels/country-inn-bathinda/deals | http_403 | en-us | hotel_subpage | GAP-001, GAP-002, GAP-013, GAP-006 |
| 98 | https://www.radissonhotels.com/en-us/hotels/country-inn-bathinda/dining | http_403 | en-us | hotel_subpage | GAP-001, GAP-002, GAP-013, GAP-006 |
| 99 | https://www.radissonhotels.com/en-us/hotels/country-inn-bathinda/meeting-events | http_403 | en-us | hotel_subpage | GAP-001, GAP-002, GAP-013, GAP-006, GAP-007 |
| 100 | https://www.radissonhotels.com/en-us/hotels/country-inn-bathinda/reviews | http_403 | en-us | hotel_subpage | GAP-001, GAP-002, GAP-013, GAP-006 |
