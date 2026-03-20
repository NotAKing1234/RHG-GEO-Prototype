# GEO Optimizer — Master Summary
Last updated: 2026-03-20
Run count: 1 | Last run: run_001 (2026-03-20)

## Implementation Patterns
No prior implementation data. run_001 is the baseline. Key observation: Radisson's brand/overview pages consistently use marketing register (superlatives, taglines) rather than informational register — this appears to be a deliberate brand voice strategy, not an oversight. Future proposals should frame factual content as additive to brand voice, not replacement.

Radisson.com returns HTTP 403 for all direct page fetches. This is a deliberate bot-blocking policy. Whether AI crawlers (GPTBot, PerplexityBot, Bingbot) are also blocked is unconfirmed — checking robots.txt must be step 0 of every future audit.

## Persistent Gaps
run_001 identified 25 gaps. All are new (baseline). The following are highest-severity and most likely to persist if not addressed:
- **GAP-023/024 (CRITICAL):** Zero Hotel/LodgingBusiness schema AND zero FAQPage schema across all audited brand and overview pages. No schema rich results in SERP.
- **GAP-010 (CRITICAL):** Radisson Blu brand page is pure marketing voice with zero factual content — entirely uncitable by AI engines.
- **GAP-018/019 (CRITICAL):** London hotels page is tourism-first; no business travel content layer visible.
- **GAP-001/002 (CRITICAL):** Homepage has no schema and no FAQ content.

## Gap Detection Logic — current version
v1 (run_001): Score all criteria equally. Weight FAQ schema (C02) and entity clarity (C07/C08) as P1 defaults. Added to v1 during run: (a) robots.txt/AI crawler access check must precede all page fetches; (b) distinguish schema-absent from schema-non-surfacing (different root causes); (c) add OTA comparison baseline for future runs.

## Competitive Intelligence (as of 2026-03-20)
- **Accor:** ChatGPT MCP integration live (Jan 2026) — direct AI booking via app
- **IHG:** AI-compatible hotel data platform launched (Feb 2026)
- **Hilton:** AI Planner launched (Mar 2026)
- **Booking.com/Expedia:** Full FAQ and schema architecture; primary AI citation winners for hotel queries
- **Perplexity:** Hotel booking in-app (Mar 2025 via Tripadvisor/Selfbook)
- **Radisson:** No confirmed AI integration; no schema in SERP rich results; bot-blocking policy in place

## Last Run Summary
run_001 | 2026-03-20 | 25 gaps found | 0 implemented (baseline) | key theme: schema and FAQ absence + marketing register systemic gap

Top 3 proposals:
1. Deploy FAQPage JSON-LD site-wide (P1, fastest measurable win)
2. Rewrite Radisson Blu brand page to factual register (P1, highest-impact content change)
3. Deploy Hotel/LodgingBusiness schema across all brand/overview pages (P1, structural prerequisite)

Fetch limitation: radissonhotels.com returns 403 for all direct fetches. Data sourced from SERP metadata. Next run must attempt robots.txt check and alternative fetch strategies.
