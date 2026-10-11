---
title: "Grid Network — Multi-store publication"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-20
severity: Low
blocks: EXT
linked_finding: —
opened: 2026-10-11
deciders: (pending acceptance)
---
---
title: "Grid Network — Multi-store publication"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-20
severity: Low
blocks: EXT
linked_finding: —
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-20 — Multi-store publication

> **Status:** PROPOSED — NOT ACCEPTED.

## Metadata

- ID: D-20
- Title: Multi-store publication
- Severity: Low
- Blocks: EXT
- Linked finding: [REVIEW-2026-10-11 —](../REVIEW-2026-10-11.md)
- Date opened: 2026-10-11
- Status: PROPOSED

D-20: MULTI-STORE PUBLICATION AND RENDEZVOUS REPLICATION
[HIGH PRIORITY, AVAILABILITY IMPACT]

Problem:
v0.6.2 assumes a principal publishes to one rendezvous. But if that rendezvous
goes down, the peer becomes unreachable. Should principals publish to multiple
rendezvous for redundancy?

Option A: Multi-store publication in V1

  Principals are configured with a list of rendezvous servers (e.g., [A, B,
  C]). Every identity/reachability/manifest update is published to all three
  simultaneously. Clients are configured with the same list. On lookup,
  clients try servers in order, fall back, and merge results from multiple
  sources.

  Pros:
    - Redundancy: one server down does not affect availability.
    - Already compatible with the design (rendezvous is untrusted).

  Cons:
    - Coordination: must keep all three in sync.
    - Clients must handle reconciliation (which reachability record is newer?).
    - More complex wire protocol (sync, 3-way merge).
    - Configuration must be explicit (users must list multiple stores).

Option B: Single primary rendezvous in V1; replication in V1.1

  V1 assumes one configured rendezvous. V1.1 adds multi-store with federation
  (rendezvous replicate to each other).

  Pros:
    - Simpler V1: one rendezvous per principal.
    - Federation design deferred until rendezvous behavior is stable.

  Cons:
    - No redundancy in V1.
    - Later migration to multi-store may require schema changes.

Recommendation:
Accept Option B (single rendezvous in V1, multi-store deferred to V1.1 / D-20
decision). V1 focuses on proving the kernel. Rendezvous redundancy is a
deployment choice, not a protocol requirement.

Consequences:
  - §11.1 and wire protocol (D-20 decision in D-21): describe single
    rendezvous behavior.
  - Operator docs: note that multiple rendezvous are not supported in V1 (or
    require external caching/CDN).
  - V1.1 design: federation, conflict resolution, replica consistency.

================================================================================
