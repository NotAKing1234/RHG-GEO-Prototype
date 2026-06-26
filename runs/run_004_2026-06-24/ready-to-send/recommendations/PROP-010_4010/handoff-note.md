# PROP-010 Handoff Note

Subject: Move banner-tests URLs behind authentication or return noindex via meta robots or X-Robots-Tag; remove them from XML sitemaps, registry sele

Status: ready-to-send

Recommended change:
Move banner-tests URLs behind authentication or return noindex via meta robots or X-Robots-Tag; remove them from XML sitemaps, registry selection, and future run targets. Add a pre-run selection check that rejects public URLs with empty title, meta description, canonical, OG fields, and structured data unless explicitly marked as test-only.

Why this matters:
Medium. This is a fast cleanup that prevents AI/search systems and future audits from sampling broken test pages.

Requested next action:
Review the attached Jira CSV row, confirm ownership/component, and import or paste the ticket into the delivery tracker.
