# GEO Optimizer — Master Summary
Last updated: 2026-03-20
Run count: 2 | Last run: run_002 (2026-03-20)

## Implementation Patterns
No implementations confirmed across two runs (run_001 and run_002 are same-calendar-day). Baseline patterns confirmed stable:
- **Marketing register is deliberate.** All brand pages maintain marketing copy across both SERP checks. GEO proposals must frame factual content as additive to brand voice, not a replacement.
- **HTTP 403 is WAF/Cloudflare-level.** /robots.txt itself returns 403 — a configuration decision. A single Cloudflare rule change (disable "Block AI Scrapers and Crawlers" managed rule) is the likely fix. /llms.txt also absent.
- **Sub-page content infrastructure exists.** Radisson Blu has /business-travel-offer sub-page; the meeting section has 7+ sub-pages with factual content. The gap is brand page discovery exposure, not content non-existence.

## Persistent Gaps (Highest Severity — 2 Consecutive Runs)
- **GAP-023/001 (CRITICAL):** Zero Hotel/LodgingBusiness schema across all audited brand and overview pages. Only 10.6% of hotel sites have good schema; 2–3x AI citation multiplier for those that do.
- **GAP-024/002 (CRITICAL):** Zero FAQPage schema across all audited pages. Note (run_002): FAQPage rich results no longer shown in SERP for hotel brands (Google 2023 policy). Schema value is now AI engine parsability only — justification unchanged.
- **GAP-010/009 (CRITICAL):** Radisson Blu brand page copy is pure marketing register — confirmed unciteable by AI. Factual content cited at 62% higher rate.
- **GAP-036/025 (CRITICAL):** Site-wide 403 blocking includes AI retrieval crawlers. Sites blocking GPTBot cited 73% less in ChatGPT. Perplexity documented bypassing via headless browser — but structured retrieval still blocked.
- **GAP-015 (CRITICAL):** Radisson brand page title tagline-dominated ("Yes I Can!") — not query-parseable.

## New Gap Categories (run_002)
- **C14 — llms.txt absent:** Emerging 2026 AI accessibility protocol. Low effort, worth implementing alongside crawler fix.
- **C12 — OTA/Yelp completeness:** Yelp added to ChatGPT Jan 2026. European Radisson Yelp coverage likely weak. Currently US cities + Berlin only — demoted to P3.
- **C15 — US-origination context:** No American traveler signals in any confirmed title or meta description.
- **Park Plaza bleisure signal confirmed:** Only brand page with "business and leisure travelers" in body copy. Not in title/meta — gap to fix.
- **Radisson Collection 2026 news:** Paris Banke Opera (1907 Beaux-Arts, Eiffel staircase, Q3 2026), Lake Como (Q1 2026, 72 rooms). High-citability facts absent from brand page.

## Competitive Intelligence (as of 2026-03-20)
- **Marriott:** AI Assistant launched Q1 2026. Marriott-Google direct booking integration active. $1B+ tech investment. Leads all AI models at 39%+ citation share.
- **Hilton:** AI Planner live March 2026. AI-driven direct booking channels.
- **Accor:** ChatGPT MCP integration live (Jan 2026).
- **IHG:** AI-compatible hotel data platform Feb 2026.
- **Booking.com/Expedia:** Full FAQ + schema pipelines; primary AI citation winners. Booking.com: 54% ChatGPT, 63% Gemini.
- **Perplexity:** TripAdvisor 95.5% citation share. Perplexity bypasses robots.txt via headless browser (Cloudflare documented).
- **ChatGPT (GPT-5.2):** Doubled search depth vs. 5.1. Yelp added Jan 2026. Google Places powers ~94% of hotel data.
- **Radisson:** No confirmed AI integration. No schema in SERP. 403 blanket blocking. Zero AI citations from own domain.

## Gap Detection Logic — current version
v2 (run_002): (a) FAQPage schema test is AI-parsability, not SERP rich result display (Google policy change 2023). (b) Add individual property page tier to audit protocol (run_003). (c) Add GBP completeness check to Phase 2. (d) Add OTA listing spot-check to Phase 2. (e) Refine register scoring: ≥3 specific facts in first 80 words = pass C09. (f) /business-travel-offer sub-page discovered — audit in run_003.

## Run Index Summary
run_001 | 2026-03-20 | 25 gaps (baseline) | 0 implemented | key theme: schema + FAQ absence; marketing register systemic gap
run_002 | 2026-03-20 | 39 gaps (+14 new) | 0 implemented (same-day) | key theme: AI crawler blocking as prerequisite; Park Plaza bleisure signal; Collection factual gap

Top 3 current proposals:
1. Unblock AI retrieval crawlers (Cloudflare fix) — prerequisite for all else
2. Deploy Hotel/LodgingBusiness schema site-wide — 2–3x AI citation multiplier
3. Rewrite Radisson Blu meta/opening copy to factual register — zero tech effort, highest-ROI content fix
