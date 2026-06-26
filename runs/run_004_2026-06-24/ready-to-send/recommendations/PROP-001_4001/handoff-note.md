# PROP-001 Handoff Note

Subject: Serve HTTP 200 HTML for all public Country Inn brand and hotel pages selected in run_004, especially /en-us/brand/country-inn, /en-us/brand/

Status: ready-to-send

Recommended change:
Serve HTTP 200 HTML for all public Country Inn brand and hotel pages selected in run_004, especially /en-us/brand/country-inn, /en-us/brand/country-inn/business-travel-offer, and the selected /en-us/hotels/country-inn-* pages. Keep bot defense behavioral and rate-based rather than returning the Radisson/Akamai access-restricted template to normal search and AI retrieval crawlers. Validate with the same direct GET capture used in runs/run_004_2026-06-24/audit_capture.json.

Why this matters:
Very high. Until the official pages return real HTML, AI travel assistants must rely on OTAs, stale snippets, or localized fallback pages rather than Radisson-owned Country Inn content.

Requested next action:
Review the attached Jira CSV row, confirm ownership/component, and import or paste the ticket into the delivery tracker.
