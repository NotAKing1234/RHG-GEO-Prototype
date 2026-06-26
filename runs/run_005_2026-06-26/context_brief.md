# Context Brief - run_005 | 2026-06-26

## Previous Run Used for Comparison
- Baseline run: `run_004` (`runs/run_004_2026-06-24/metadata_snapshot.md` and `log_reflection.md`).
- Current run: `run_005`, 478 SQLite-selected Park Plaza URLs from `run_url_targets`.
- Direct URL overlap with run_004: 0 URLs. The current run therefore cannot support page-by-page implementation claims against run_004. It can only compare recurring infrastructure, selection, and metadata-pattern behavior across brand families.

## Current Target Set
- Brand: Park Plaza only.
- Locale: 478 `en-us` URLs.
- Page-type mix: 381 generic/page URLs, 76 meeting-event URLs, 14 brand URLs, 7 offers URLs.
- Source sitemap mix: 419 from `sitemap-remaining-hotel-pages.xml`, 38 from `sitemap-hotel-overview-pages.xml`, 14 from `sitemap-park-plaza.xml`, 7 from `sitemap-offers.xml`.

## Current Live Metadata Probe
A representative Phase 1 probe of Park Plaza brand, destination, hotel overview, meeting-event, and offer URLs returned HTTP 403 access-restricted templates with the title `Access Restricted | Radisson Hotel Group`:
- `https://www.radissonhotels.com/en-us/brand/park-plaza`
- `https://www.radissonhotels.com/en-us/brand/park-plaza/destinations`
- `https://www.radissonhotels.com/en-us/hotels/park-plaza-amsterdam-airport`
- `https://www.radissonhotels.com/en-us/hotels/park-plaza-amsterdam-airport/meeting-events`
- `https://www.radissonhotels.com/en-us/hotel-deals/park-plaza-family`

This is only a context probe. Phase 2 must still audit all 478 selected URLs individually and record exact fetch status for each URL.

## Summary of Detected Metadata Changes
- `run_004` already showed partial root-level infrastructure recovery: `/robots.txt` was HTTP 200, but `/sitemap.xml` remained HTTP 403 and selected English/US Country Inn pages were blocked.
- `run_005` starts with a different brand family but the same representative access symptom on Park Plaza `en-us` pages: HTTP 403 access-restricted template instead of page-specific metadata.
- Because there is no URL overlap, no exact title/meta/schema field can be marked changed, improved, or regressed from the previous run for the current selected URLs.

## Implemented Recommendations Inferred from the Diff
- No fully implemented recommendation can be inferred for `run_005` before Phase 2.
- The only prior partial improvement remains the `run_004` root `/robots.txt` recovery. It does not count as current-run Park Plaza page-level implementation.

## Unchanged Recommendations Inferred from the Diff
- Page-level retrieval/access remains the likely upstream blocker.
- English/US locale access remains especially important because every selected Park Plaza URL in this run is `en-us`.
- Hotel/LodgingBusiness schema, meeting-event details, reviews, amenities, and direct booking data remain unconfirmed until pages return useful HTML; blocked pages should be scored as missing retrieval and unevaluable metadata.

## Persistent Gaps Recurring for 2+ Runs
- AI crawler/page access: recurring from earlier runs and now representative Park Plaza probe.
- Sitemap and discovery infrastructure: recurring until `/sitemap.xml` and selected sitemap-derived pages are publicly retrievable.
- Hotel/LodgingBusiness schema depth: recurring as an unresolved pattern because blocked property pages prevent validation and previously accessible pages exposed only shallow schema.
- Locale alignment for American travelers: recurring because the current run is entirely `en-us`, and representative `en-us` pages are blocked.
- Selection hygiene: recurring as a watch-out because this run includes many non-overview hotel subpages and meeting-event pages that must be individually classified rather than assumed production-ready.

## Implications for Current Scoring and Prioritization
- Prioritize `C01` access and `C02` locale/canonical clarity before deeper content recommendations when URLs return the access-restricted template.
- Treat meeting-event pages as a distinct business-travel opportunity only when underlying page content is reachable; otherwise score them as blocked evidence with lost meeting-data visibility.
- Avoid claiming Park Plaza schema/content gaps from unreachable pages beyond what the fetch result supports. The correct current-state wording is `blocked/uninspectable`, not `schema absent`, until Phase 2 captures a useful document.
- Require `gap_analysis.md` to include a per-URL coverage matrix for all 478 selected URLs because grouped gaps alone will be too easy to misread as sampled coverage.
