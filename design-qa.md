# GeoOptimizer Dashboard QA

current result: pending browser validation after URL Registry integration

## Scope

- Default home view: Minimal Executive Atlas / `Overview`.
- Operator view: Minimal Signal Console / `Signal Console`.
- URL selection view: `URL Registry`.
- Existing views preserved: Radisson Pages, Sources, Metadata, Copy Bank, Exports.
- Backend/API contracts include URL Registry endpoints and next-run selection persistence.

## Evidence

- Reference home mockup inspected: `/Users/daniel/.codex/generated_images/019ec65a-7321-7ad0-80a0-19f5f715a562/ig_01b652967487491f016a2ed6faafa48191a256e7f09696bd5b.png`.
- Reference Signal Console mockup inspected: `/Users/daniel/.codex/generated_images/019ec65a-7321-7ad0-80a0-19f5f715a562/ig_01b652967487491f016a2ed6a8daa48191b054157c30686cab.png`.
- Historical `/tmp` screenshots are not durable QA evidence for the current worktree.
- Current validation should use a fresh dashboard build plus browser smoke test for Overview, Signal Console, URL Registry, and Exports.

## Checks

- Build must pass with `npm --prefix dashboard run build`.
- Navigation must expose `Overview`, `Signal Console`, `URL Registry`, Radisson Pages, Sources, Metadata, Copy Bank, and Exports.
- URL Registry must load `/api/url-registry`, show filtered counts and cost estimate, support checked visible row saves, and reject accidental all-registry saves through the backend.
- `Exports` must preserve saved Jira ticket draft descriptions in Jira CSV output.
- Browser smoke screenshots should be regenerated before this file is marked passed.

## Notes

- The implementation intentionally keeps existing dashboard run/export data shapes while adding registry selection APIs.
- The visual direction is an adapted, original implementation of the selected mockups, not a copy of any competitor UI.
