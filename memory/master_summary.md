# GEO Optimizer — Master Summary
Last updated: 2026-04-15
Run count: 3 | Last run: run_003 (2026-04-15)

## Implementation Patterns
**26-day non-implementation confirmed (run_003).** First meaningful implementation window elapsed with zero observable changes. Pattern: proposals are not reaching decision-makers or there is an organizational barrier (WAF rules require security sign-off; content changes require marketing team approval). Future proposals must quantify revenue cost of delay and frame AI crawler fix as a business decision, not a technical adjustment.
- Marketing register is deliberate — all brand pages stable across 3 runs. Frame factual content as additive to brand voice.
- HTTP 403 WAF block is infrastructure-level (Cloudflare) — organizational decision, not content decision.
- Sub-page infrastructure exists (Radisson Blu /business-travel-offer — good title, thin bleisure content). Gap is brand page discovery exposure.
- OTA footprint for London is STRONG (Bloomsbury: 4,423 TripAdvisor reviews, 5,693 Booking.com reviews) — a confirmed strength. Individual property OTA data is being cited by AI engines; Radisson's own domain is not.

## Persistent Gaps (Highest Severity — 3 Consecutive Runs)
- **CRITICAL-01:** HTTP 403 site-wide blocks all AI crawlers. 73% citation reduction for blocking GPTBot. Cloudflare WAF "Block AI Scrapers" managed rule. Fix: 2–4 hours one engineer. 3 unaddressed runs.
- **CRITICAL-02:** Zero Hotel/LodgingBusiness schema across all brand/overview pages. 3.2× citation multiplier for pages with schema (65–71% of AI-cited pages have structured data). 3 unaddressed runs.
- **CRITICAL-03:** Zero FAQPage schema across all audited pages. 3.2× AI Overview appearance rate for pages with FAQPage markup. AI engine Q&A extraction blocked. 3 unaddressed runs.
- **CRITICAL-04:** Radisson Blu brand page opening copy is pure marketing register — zero facts in first 80 words. Factual content cited 62% more. 3 unaddressed runs.
- **CRITICAL-05:** Zero implementations after 26 days — first meaningful window. All proposals unacted.

## New Gap Categories (run_003)
- **C17 — Direct AI Distribution gap (GAP-030, CRITICAL):** Accor live Jan 29 2026 (ChatGPT), Hyatt live Feb 2026, Perplexity/Selfbook bookable for 140,000 hotels. Radisson has no AI distribution channel. Fastest fix: Selfbook partnership (Perplexity bookability, weeks not quarters). ChatGPT app: Q2–Q3 2026 via Accor/Hyatt model.
- **C16 — Loyalty discoverability (GAP-026, HIGH):** Radisson Rewards not surfacing in AI loyalty comparison responses. Marriott Bonvoy/Hilton Honors dominate. Fix: MemberProgram schema (Google-officially-supported, displayable in SERP), comparison-ready copy, FAQPage schema on /rewards/faq.
- **Radisson Collection freshness ESCALATED (GAP-013, CRITICAL):** Lake Como property open Q1 2026 — absent from brand page. Pure content gap, zero tech work, high AI citation value (heritage facts: 1926 palazzo, panoramic rooftop, Via Cairoli 2, Como). Paris Banke Opéra on track H2 2026 (Belle Époque bank, Eiffel staircase, 90 rooms).
- **Destination page (GAP-023/024, MEDIUM-HIGH):** Title "Destinations | Radisson Hotels" purely navigational. No geographic entities. ItemList schema + geo-specific opening paragraph needed.
- **Rewards page (GAP-026/028, HIGH):** First audit. MemberProgram schema (Google-supported, SERP-displayable) absent. Comparison-ready loyalty facts absent.

## Competitive Intelligence (as of 2026-04-15)
- **Marriott:** 224 AI citations / 40 queries. Google API direct booking pipeline live. `potentialAction: ReserveAction` schema in use. One of 3 brands in sponsored ChatGPT hotel search results.
- **Accor:** ChatGPT app live Jan 29, 2026 (first major hotel group). Multi-language. ALL Accor booking platform.
- **Hyatt:** ChatGPT app live Feb 2026. +20% group sales productivity. Longer average stays. CEO cited AI search lift.
- **Hilton:** AI Planner live on Hilton.com March 2026 (8,000+ properties, no external partnership needed).
- **Perplexity/Selfbook:** 140,000 hotels bookable end-to-end. TripAdvisor integration confirmed. Primary Perplexity discovery mechanism for AI-referred hotel bookings.
- **OTAs:** Booking.com 54% ChatGPT citation share, 63% Gemini. Expedia AI Trip Planner in 40+ languages.
- **Radisson:** Zero confirmed AI citations from own domain. Zero AI distribution channel. Zero schema. All 403-blocked.

## Gap Detection Logic — current version
v3 (run_003): (a) Add standard Radisson brand page (/en-us/brand/radisson) to Priority 1 audit — currently missing from audit target list. (b) Add Booking.com amenity attribute completeness to OTA spot-check (not just review count). (c) Add GBP Q&A section check to property audit protocol. (d) Introduce implementation velocity tracking metric in context brief. (e) Track AI distribution gap separately in run index with per-path notation. (f) Weight TripAdvisor review *recency* (not just count) for Perplexity citation correlation.

## Run Index Summary
run_001 | 2026-03-20 | 25 gaps (baseline) | 0 implemented | key theme: schema + FAQ absence; marketing register systemic gap
run_002 | 2026-03-20 | 39 gaps (+14 new) | 0 implemented (same-day) | key theme: AI crawler blocking prerequisite; Park Plaza bleisure; Collection factual gap
run_003 | 2026-04-15 | 34 gaps (12 new, 22 recurring) | 0 implemented (26 days) | key theme: AI distribution gap (transactional era); Lake Como freshness escalation; Rewards loyalty discoverability

Top 3 current proposals:
1. Unblock AI retrieval crawlers (Cloudflare fix) — prerequisite for all else, 2–4 hours
2. Deploy Hotel/LodgingBusiness schema + FAQPage + MemberProgram schema site-wide — 3.2× citation multiplier, one engineering sprint
3. Update Radisson Collection brand page with Lake Como (open) + Paris Banke Opéra facts — zero tech, pure content gap, high citability
