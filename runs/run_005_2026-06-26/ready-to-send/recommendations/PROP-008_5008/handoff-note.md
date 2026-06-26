# PROP-008 Handoff Note

Subject: Remove utility, picklist, sitemap-like, and test-adjacent URL patterns from run_url_targets selection and from any generated public sitemaps

Status: ready-to-send

Recommended change:
Remove utility, picklist, sitemap-like, and test-adjacent URL patterns from run_url_targets selection and from any generated public sitemaps, starting with https://www.radissonhotels.com/en-us/brand/park-plaza/meeting-conference/picklist. If utility endpoints must remain public, return crawlable noindex headers or disallow them in robots rules. Replace them in GEO selections with canonical production landing pages for Park Plaza properties, city/destination pages, meeting pages, and offers.

Why this matters:
Medium. Cleaner target sets reduce crawl waste and AI confusion so assistants find useful Park Plaza meeting, property, city, and offer pages rather than internal utility pages.

Requested next action:
Review the attached Jira CSV row, confirm ownership/component, and import or paste the ticket into the delivery tracker.
