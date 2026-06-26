# Implementation Log — Cumulative Diff Record

Tracks what Radisson has implemented (or not) from each run's optimization proposal.
Updated automatically at the end of every run via diff between metadata snapshots.

## Format
run_NNN → run_NNN+1 | YYYY-MM-DD | [implemented: list] | [unchanged: list] | [new gaps: list]

## Log

### run_001 | 2026-03-20 (baseline initialization)

**Implemented:** N/A — first run, no prior recommendations

**Unchanged:** N/A — first run

**New gaps identified (25 total):**

Structural (portfolio-wide):
- GAP-023: Zero Hotel/LodgingBusiness schema in SERP rich results
- GAP-024: Zero FAQPage schema across all audited pages
- GAP-025: Systemic marketing register in all page meta descriptions

Homepage: GAP-001 (no schema), GAP-002 (no FAQ), GAP-003 (CTA meta description), GAP-004 (transactional title), GAP-005 (no bleisure body content), GAP-006 (no amenity content)

Brands page: GAP-007 (generic description), GAP-008 (no FAQ), GAP-009 (no geographic signals)

Radisson Blu brand page: GAP-010 (zero factual content), GAP-011 (no FAQ), GAP-012 (no NL query compatibility), GAP-013 (no amenity content), GAP-014 (no geographic entity signals)

Radisson brand page: GAP-015 (misaligned title), GAP-016 (no FAQ)

Park Plaza: GAP-017 (unassessable — fetch blocked)

London hotels overview: GAP-018 (tourism-first title), GAP-019 (tourism-framed body), GAP-020 (no FAQ), GAP-021 (amenity content at property level only), GAP-022 (district geography at property level only)

**Fetch note:** radissonhotels.com returns HTTP 403 for all direct fetches. All metadata sourced from SERP snippets. Run_002 must check robots.txt and attempt alternative fetch methods.

---

### run_001 → run_002 | 2026-03-20 (same-day diff — baseline verification only)

**Implemented:** ZERO — same-day run, no implementation expected or possible.

**Unchanged (all 16 run_001 proposals):** PROP-001 through PROP-016 all unimplemented. Metadata for all pages verified identical to run_001 SERP snapshots. Baseline confirmed stable.

**What changed (non-implementation):**
- Park Plaza brand page NOW CONFIRMED: title "City Centre Hotels | Park Plaza Hotels & Resorts", meta description with "meeting facilities" and "award-winning restaurants" — previously unassessable. Body copy confirmed: "business and leisure travelers" — the portfolio's best bleisure signal, not in title/meta.
- Radisson Collection page added to audit: title "Radisson Collection Luxury Hotels | Radisson Hotels". 2026 expansion news (Paris Banke Opera, Lake Como) confirmed via press releases but not on brand page.
- Meeting/Conference page added as Priority 2 rotation: title CTA-format, OG confirmed, 7+ sub-pages.
- /robots.txt confirmed 403 (cannot assess AI crawler policy). /llms.txt confirmed 403 (absent).
- Google FAQPage rich result policy (2023): hotel brands ineligible. FAQPage schema value reframed as AI parsability only, not SERP display.
- GPT-5.2 confirmed with doubled search depth. Yelp added to ChatGPT Jan 2026 (US cities + Berlin only).

**New gaps identified (14 new, total 39):**
GAP-026: Park Plaza title misaligned (MISALIGNED, Sev 2)
GAP-027: Park Plaza bleisure signals in body only, not metadata (WEAK, Sev 2)
GAP-028: Park Plaza no FAQ content (MISSING, Sev 2)
GAP-029: Radisson Collection no Hotel schema (MISSING, Sev 2)
GAP-030: Radisson Collection marketing register — 2026 expansion facts absent from brand page (MISALIGNED, Sev 2)
GAP-031: Radisson Collection no FAQ content (MISSING, Sev 2)
GAP-032: Meeting/Conference page CTA title (MISALIGNED, Sev 2)
GAP-033: Meeting/Conference no FAQ content (MISSING, Sev 2)
GAP-034: Meeting/Conference no MeetingRoom/EventVenue schema (MISSING, Sev 2)
GAP-035: Meeting/Conference no American corporate traveler signals (MISSING, Sev 1)
GAP-036: Site-wide AI crawler access formally assessed as MISSING against C11 (Sev 3)
GAP-037: llms.txt absent (MISSING, Sev 2)
GAP-038: Yelp OTA listing completeness for European properties unverified (WEAK, Sev 2)
GAP-039: All brand pages missing US-origination geographic context (MISSING, Sev 2)

**Run_003 tracking targets:**
- Will run_001/run_002 proposals appear implemented? Target indicators: schema rich results in SERP, updated meta descriptions in SERP, robots.txt accessible, llms.txt accessible.
- Sub-page /business-travel-offer to be audited.
- Individual London property pages (2–3) to be audited for schema tier assessment.
- Google Business Profile completeness for key European properties to be checked.
- Radisson Rewards (Priority 3) due for inclusion.

---

### run_002 → run_003 | 2026-04-15 (26-day diff — first meaningful implementation window)

**Implemented:** ZERO — 26 days post-run_002, zero observable changes. All homepage/brand page titles, meta descriptions, and body copy identical to run_002 snapshots. HTTP 403 blocking unchanged. /robots.txt still 403. /llms.txt still 403. No schema rich results detected.

**What changed (non-implementation):**
- Radisson Collection Lake Como now OPEN (Q1 2026) — was "planned" in run_002, now operational. Brand page still shows no reference. GAP escalated from WEAK to MISSING/CRITICAL.
- Accor ChatGPT app launched Jan 29, 2026; Hyatt ChatGPT app Feb 2026; Hilton AI Planner Mar 2026. BCG "ask and book era" report March 30, 2026 confirmed transactional AI phase is live. AI distribution gap widened since run_002.
- Radisson Blu London Bloomsbury OTA status: 4,423 TripAdvisor reviews; 5,693 Booking.com reviews — strong OTA footprint confirmed (positive). Q&A section (569 insider tips) on TripAdvisor.
- Perplexity/Selfbook hotel booking integration confirmed live (140,000 hotels bookable end-to-end).
- GBP (March 2026 core update): GBP now accounts for 32% of Local Pack ranking; feeds Google AI Overviews (40%+ of local queries).

**Unchanged (all 17 run_003 proposals unchanged from run_002 targets):**
- PROP-001 (Cloudflare fix): NOT IMPLEMENTED — 3rd consecutive unaddressed
- PROP-002 (Hotel schema): NOT IMPLEMENTED — 3rd consecutive unaddressed
- PROP-003 (FAQPage schema): NOT IMPLEMENTED — 3rd consecutive unaddressed
- PROP-004 (Radisson Blu copy rewrite): NOT IMPLEMENTED — 3rd consecutive unaddressed
- PROP-005 (Collection freshness content): NOT IMPLEMENTED — ESCALATED to CRITICAL
- PROP-006 (Park Plaza bleisure title/meta): NOT IMPLEMENTED — 2nd consecutive
- PROP-007 (Homepage title/meta): NOT IMPLEMENTED — 3rd consecutive
- PROP-008 (llms.txt): NOT IMPLEMENTED — 2nd consecutive

**New gaps identified (12 new, total 34 in run_003):**
GAP-012: Radisson Blu /business-travel-offer — WEAK bleisure compound language (WEAK, Sev 2)
GAP-023: Destination page — title purely navigational (MISSING, Sev 2) — first audit
GAP-024: Destination page — no geographic entities (MISSING, Sev 2) — first audit
GAP-025: Destination page — no bleisure signals (MISSING, Sev 1) — first audit
GAP-026: Radisson Rewards — not surfacing in loyalty comparison AI responses (WEAK, Sev 2) — first audit
GAP-027: Radisson Rewards — no American traveler signals (WEAK, Sev 2) — first audit
GAP-028: Radisson Rewards — no MemberProgram/Organization schema (MISSING, Sev 1) — first audit
GAP-029: Radisson Rewards — FAQ page exists but no FAQPage schema (WEAK, Sev 1) — first audit
GAP-030: Portfolio — no direct AI distribution channel vs. Accor/Hyatt (MISSING, Sev 3) — CRITICAL
GAP-031: Portfolio — individual property schema unconfirmable (MISSING, Sev 2)
GAP-032: Portfolio — GBP completeness unconfirmed (WEAK, Sev 2) — first formal assessment
GAP-034: Destination page — no ItemList schema (MISSING, Sev 2) — first audit

**Run_004 tracking targets:**
- Implementation indicators: robots.txt HTTP 200, any schema rich results in SERP, Rewards/Collection page copy changes, Selfbook/ChatGPT app announcement, Radisson Collection Lake Como reference on brand page.
- Add standard Radisson brand page (/en-us/brand/radisson) to Priority 1 audit.
- OTA spot-check: add Booking.com amenity attribute completeness check (not just review count).
- GBP: check Q&A sections for flagship London/Amsterdam properties.
- Property proxy: expand to 3 properties (London, Amsterdam, Paris).
- Review recency check: TripAdvisor Radisson Blu London — are most recent reviews within 3 months?

---

### run_003 → run_004 | 2026-06-24 (Country Inn DB-selected target set)

**Implemented:** ZERO fully implemented recommendations. One partial technical improvement detected: `/robots.txt` now returns HTTP 200, whereas run_003 recorded it as blocked.

**What changed:**
- Current run used SQLite `run_url_targets`: 100 selected Country Inn & Suites URLs.
- 42 selected localized pages returned HTTP 200 and exposed localized title/meta, canonical, hreflang, OG fields, `Organization` JSON-LD, and often `BreadcrumbList`.
- 58 selected URLs returned HTTP 403 access-restricted templates, including all 23 selected English/US Country Inn URLs and all selected hotel overview/subpage URLs.
- `/sitemap.xml` returned HTTP 403 XML AccessDenied.
- `/llms.txt` returned HTTP 404.
- Two public `banner-tests` URLs returned HTTP 200 with empty title/meta/canonical/OG/schema.

**Unchanged / still open:**
- Page-level public retrieval remains incomplete; English/US and hotel pages are blocked.
- Hotel/LodgingBusiness schema remains absent on accessible selected pages.
- FAQPage, review/aggregateRating, local/place schema depth, and direct AI distribution remain absent or unconfirmed.
- American bleisure traveler path remains missing because the target `/en-us/` pages are inaccessible.

**New gaps identified (15 total in run_004):**
- Country Inn page-level access blocking with partial root robots improvement.
- English/US path blocked while localized European Country Inn pages are accessible.
- Sitemap access denied despite accessible robots.txt.
- llms.txt missing.
- Accessible pages limited to Organization/Breadcrumb schema, no Hotel/LodgingBusiness.
- Individual hotel pages blocked.
- Work-leisure and amenity data inconsistent.
- Geographic/transport specificity weak.
- FAQ/Q&A integrity weak.
- Public banner-test URLs selected and metadata-empty.
- Query fan-out coverage weak.
- Image accessibility and visual context weak.
- American bleisure path missing.
- Trust/review footprint missing.
- Direct AI travel distribution readiness missing.

**Run_005 tracking targets:**
- Confirm whether page-level 403s are fixed for `/en-us/brand/country-inn` and selected `/en-us/hotels/country-inn-*`.
- Retest `/sitemap.xml` and `/llms.txt`.
- Verify whether banner-test URLs are removed/noindexed/excluded from run selection.
- Re-check schema depth on accessible pages: look specifically for `Hotel`, `LodgingBusiness`, `aggregateRating`, `Review`, and `FAQPage`.
- Add selection hygiene checks before run initialization.

---

### run_004 -> run_005 | 2026-06-26 (Park Plaza DB-selected target set)

**Implemented:** ZERO fully implemented recommendations. There is no direct URL overlap with run_004, so page-by-page implementation cannot be inferred. Cross-run infrastructure pattern remains unchanged: root `/robots.txt` is reachable, but selected public pages are still blocked.

**What changed:**
- Current run used SQLite `run_url_targets`: 478 selected Park Plaza URLs, all `en-us`.
- Target mix: 14 brand URLs, 457 hotel/property URLs, 78 meeting-related URLs, and 7 offer URLs.
- 476 selected URLs returned HTTP 403 access-restricted templates; 2 timed out.
- `/sitemap.xml` returned HTTP 403.
- `/llms.txt` returned HTTP 404.
- Full coverage succeeded: every selected URL is represented in `metadata_snapshot.md` and `gap_analysis.md`.

**Unchanged / still open:**
- Page-level public retrieval remains incomplete across another brand family.
- English/US audience path remains blocked.
- Hotel/LodgingBusiness schema, MeetingRoom data, offer terms, reviews, amenities, and direct booking facts remain unavailable or unconfirmed because pages are blocked.
- Target hygiene remains open because utility/picklist-like URLs entered the selected set.

**New gaps identified (8 total in run_005):**
- Park Plaza page-level access blocking across the selected set.
- English/US locale/canonical validation blocked.
- Property-level Hotel/LodgingBusiness schema unavailable.
- Meeting-event data unavailable for 78 meeting-related URLs.
- Offer/direct-booking facts unavailable for selected offer URLs.
- `/sitemap.xml` access denied.
- `/llms.txt` missing.
- Utility/picklist URL selection hygiene issue.

**Run_006 tracking targets:**
- Verify whether Park Plaza selected URLs return 200 page-specific HTML after WAF/access changes.
- Retest `/sitemap.xml` and `/llms.txt`.
- Re-check schema depth on unblocked Park Plaza property pages: `Hotel`, `LodgingBusiness`, `MeetingRoom`, `Offer`, `aggregateRating`, `Review`, and `FAQPage`.
- Confirm utility/picklist/test URLs are excluded from selected targets or marked noindex/disallowed.
