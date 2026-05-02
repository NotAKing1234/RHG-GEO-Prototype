# Context Brief — run_003 | 2026-04-15

## Previous Run Used for Comparison
run_002 | 2026-03-20 | /runs/run_002_2026-03-20/metadata_snapshot.md
Gap between runs: **26 days** (first meaningful implementation window — unlike run_001→run_002 same-day gap)

---

## Summary of Detected Metadata Changes

**Fetch method:** HTTP 403 blocks all direct WebFetch attempts on radissonhotels.com, including /robots.txt, /llms.txt, and all brand/property pages. SERP snippets and WebSearch remain primary observation window.

**UNCHANGED (all 26 days post-run_002):**
| Page | Field | run_002 value | run_003 value | Status |
|------|-------|--------------|--------------|--------|
| Homepage | Title | "Radisson Hotels Official Site | Book Rooms Worldwide" | Same | NO CHANGE |
| Homepage | Meta description | "Explore over 1100 hotels worldwide..." | Same | NO CHANGE |
| Radisson Blu brand | Title | "Radisson Blu Hotels & Resorts | Radisson Hotels" | Same | NO CHANGE |
| Radisson Blu brand | Meta/copy | "unparalleled service, comfort, and style...meaningful and memorable experiences" | Same | NO CHANGE |
| Radisson Collection brand | Title | "Radisson Collection Luxury Hotels | Radisson Hotels" | Same | NO CHANGE |
| Radisson RED brand | Title | "Radisson RED - Stylish & Boutique Hotels | Radisson Hotels" | Same | NO CHANGE |
| Park Plaza brand | Title | "City Centre Hotels | Park Plaza Hotels & Resorts" | Same | NO CHANGE |
| Park Plaza brand | Meta | "stylish guest rooms in city centre locations, meeting facilities..." | Same | NO CHANGE |
| Meeting/Conference | Title | "Book Your Meeting Rooms and Conferences Now | Radisson Hotels" | Same | NO CHANGE |
| /robots.txt | HTTP | 403 | 403 | NO CHANGE — WAF still blocking |
| /llms.txt | HTTP | 403 | 403 | NO CHANGE — still absent |
| Schema (all pages) | Rich results | NONE | NONE | NO CHANGE |

**NEW CONFIRMED (run_003):**
| Item | Finding |
|------|---------|
| Radisson Rewards page | First audit: title "Radisson Hotel Rewards Program | Radisson Rewards" (Priority 3, skipped runs 001–002) |
| Radisson Collection 2026 news | Lake Como confirmed open Q1 2026; Paris Banke Opera on track for H2 2026 — in trade press but NOT confirmed in brand page content |
| Radisson Blu "About" sub-page | /en-us/brand/radisson-blu/about confirmed: "elegant, sophisticated structures and spaces for business and leisure" — bleisure signal at sub-page level |
| Radisson brand page | Title "Radisson | Hotel Deals | Yes I Can! Attitude" — tagline-dominated, confirmed first time for this page specifically |
| London OTA presence | Radisson Blu London Bloomsbury: 4,423 TripAdvisor reviews (above 500 threshold); 5,693 Booking.com reviews — positive OTA footprint |
| GBP signals | Radisson Blu London properties appear in Google Travel with amenity data (fitness center, business center, meeting rooms noted) |

---

## Implemented Recommendations Inferred from Diff

**NONE CONFIRMED.**

After 26 days, zero observable changes to any Priority 1 page metadata, AI crawler access, schema implementation, or /llms.txt. All run_002 gaps remain open.

Inferences:
- PROP-001 (Cloudflare AI crawler unblock): NOT IMPLEMENTED. /robots.txt still returns 403.
- PROP-002 (Hotel/LodgingBusiness schema): NOT IMPLEMENTED. No rich results detected.
- PROP-003 (FAQPage schema): NOT IMPLEMENTED. No FAQ rich results detected.
- PROP-004 (Radisson Blu meta/title rewrite): NOT IMPLEMENTED. Titles unchanged.
- PROP-011 (llms.txt): NOT IMPLEMENTED. Still returns 403.
- PROP-014 (Radisson Collection 2026 expansion content): NOT IMPLEMENTED on brand page (news confirmed in trade press, not in brand page metadata).

---

## Unchanged Recommendations from run_002

All top-priority proposals remain unimplemented after 26 days:
1. Unblock AI retrieval crawlers — Cloudflare fix (CRITICAL prerequisite)
2. Deploy Hotel/LodgingBusiness schema site-wide
3. Rewrite Radisson Blu meta/opening copy to factual register
4. Add Park Plaza American traveler signals
5. Add Radisson Collection 2026 expansion facts to brand page
6. Deploy llms.txt
7. Add FAQPage schema across brand pages

---

## Persistent Gaps (2+ Consecutive Runs)

| Gap | Description | Runs | Severity |
|-----|-------------|------|---------|
| CRITICAL-01 | HTTP 403 blocks all AI crawlers site-wide | run_001, run_002, run_003 | 3 (max) |
| CRITICAL-02 | Zero Hotel/LodgingBusiness schema across all brand/overview pages | run_001, run_002, run_003 | 3 (max) |
| CRITICAL-03 | Zero FAQPage schema across all audited pages | run_001, run_002, run_003 | 3 (max) |
| CRITICAL-04 | Radisson Blu brand page in pure marketing register | run_001, run_002, run_003 | 3 (max) |
| CRITICAL-05 | Homepage title/meta not query-answering | run_001, run_002, run_003 | 3 (max) |
| HIGH-01 | No American/bleisure traveler signals in any brand page title or meta | run_001, run_002, run_003 | 2 |
| HIGH-02 | llms.txt absent | run_002, run_003 | 2 |
| HIGH-03 | Radisson Collection 2026 expansion facts absent from brand page | run_002, run_003 | 2 |

---

## Implications for Scoring and Prioritization

1. **26-day non-implementation = escalation signal.** The first meaningful implementation window has passed with zero observable changes. Proposals in run_003 should note this explicitly and frame the cost of each additional delay in measurable terms (AI citations lost per week, competitor advantage widening).

2. **Radisson Collection brand page freshness gap is now more urgent.** Lake Como is already open as of Q1 2026. The brand page still shows no reference to it. A major new European luxury property (highly citeable, US travel media coverage) is generating zero discovery benefit from the Radisson website.

3. **Loyalty program gap newly confirmed.** Radisson Rewards page title is present but sub-optimal. Marriott Bonvoy and Hilton Honors are prominently surfaced in AI responses for loyalty comparison queries. Radisson Rewards is not.

4. **OTA footprint is actually positive for London.** Radisson Blu London Bloomsbury's TripAdvisor volume (4,423 reviews) and Booking.com volume (5,693 reviews) exceed the AI citation threshold. This is a STRENGTH to build on — not a gap.

5. **New gap categories for run_003:** C11 (individual property schema), C16 (loyalty AI discoverability), C17 (direct AI distribution channel).
