---
title: "Grid Network — Relay economy and extension scope"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-24
severity: Low
blocks: EXT
linked_finding: —
opened: 2026-10-11
deciders: (pending acceptance)
---
---
title: "Grid Network — Relay economy and extension scope"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-24
severity: Low
blocks: EXT
linked_finding: —
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-24 — Relay economy and extension scope

> **Status:** PROPOSED — NOT ACCEPTED.

## Metadata

- ID: D-24
- Title: Relay economy and extension scope
- Severity: Low
- Blocks: EXT
- Linked finding: [REVIEW-2026-10-11 —](../REVIEW-2026-10-11.md)
- Date opened: 2026-10-11
- Status: PROPOSED

D-24: RELAY ECONOMY AND EXTENSION SCOPE
[MEDIUM PRIORITY, AFFECTS V1.1 ROADMAP]

Problem:
v0.6.2 describes RelayTicket, RelayNodeRecord, relay operator manifests,
capability profiles, capacity pooling, and credits. These are important to
community and commercial relay deployment, but they are not kernel
functionality. They depend on a completed wire protocol (D-20 / D-21) and
operator experience. Should they be in V1 or deferred?

Option A: Minimal relay in V1; economy extension in V1.1

  V1 relay: simple pair-bound packet forwarding. RelayTicket carries
  endpoints, expiry, and rate limits; no operator manifests, credits, or
  capacity pools.
  V1.1 extension: OperatorManifest, capability profiles, credit system,
  federation.

  Pros:
    - V1 is focused: proof that relaying works at all.
    - Economy design is deferred until operators have real feedback.
    - Does not block core deployment.

  Cons:
    - Community and commercial operators cannot use V1's relay for
      incentivized deployment.
    - V1.1 work is large; roadmap extends.

Option B: Full relay economy in V1

  Include RelayTicket, OperatorManifest, Relay Authority Key, capability
  profiles, credits, capacity accounting.

  Pros:
    - Complete relay story in V1.
    - Community can build incentive models immediately.

  Cons:
    - Scope explosion: relay economy alone is 500+ lines of schema and rules.
    - Unproven: no operator experience yet; design will change.
    - Delays v0.8.0 by months.

Recommendation:
Accept Option A (minimal relay in V1, economy in V1.1). Kernel first, then
relays, then incentives. Update the roadmap (stage 6).

Consequences:
  - OBJECTS.md: RelayTicket is a minimal V1 object with endpoints, expiry,
    rate limits, and source/destination principals.
  - design/EXTENSIONS.md: OperatorManifest, Relay Authority Key, capability
    profiles, credits, gossip, federation.
  - Commercial model doc: economy design deferred to post-v0.8.0.
  - D-24 simplifies the V1 spec and stages the relay deployment timeline.

================================================================================
