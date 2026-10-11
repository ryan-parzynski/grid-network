---
title: "Grid Network — KeyRevocation history pinning"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-04
severity: High
blocks: V1
linked_finding: C1/C4
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-04

> **Status:** PROPOSED — NOT ACCEPTED.



## Context / Problem

v0.6.2 KeyRevocation names effective_sequence but not what history is
legitimate below it. An attacker with a compromised Authorization Key can
construct an alternative branch at sequences below effective_sequence; a
verifier that never saw the genuine objects there accepts the fake branch.
C4 identifies the gap.

## Options considered

Option A: Pin predecessor chain hash [PROPOSED in §9]

  KeyRevocation gains: revoked_stream_id, effective_predecessor_chain_hash
  (the chain_hash of the object at effective_sequence - 1, or
  initial_chain_hash if effective_sequence = 1).

  Objects on any branch not leading to that pinned hash are REVOKED.

  Pros:
    - Unambiguous: the legitimate chain is pinned by the root.
    - Fails closed: an attacker building an alternative branch below the
      revocation point is detected when revocation is received.
    - Works with D-03 fork evidence: if the verifier's accepted state
      diverges, the divergent branch objects are marked REVOKED atomically.

  Cons:
    - KeyRevocation becomes 2–3 fields larger.
    - Verifiers must store more history (must keep the pinned object's state
      available for comparison).

Option B: No pinning; revoke only effective_sequence and above

  effective_sequence alone revokes sequence >= N. Anything before N is
  accepted as-is, no pinning.

  Pros:
    - Simpler: smaller KeyRevocation.
    - Assumes the verifier's accepted state is trustworthy.

  Cons:
    - Allows alternative history below the revocation point.
    - Does not fail closed if the verifier's earlier state was forked without
      it knowing.
    - Violates "no missing information grants authority."

## Recommendation (PROPOSED — NOT DECIDED)

> **PROPOSED:**

Accept Option A (pinned predecessor hash). Closes C4 directly and
deterministically. Update §9 with the amended fields.

## Consequences

- OBJECTS.md KeyRevocation schema: add revoked_stream_id,
    effective_predecessor_chain_hash.
  - Test vectors: KeyRevocation pinning scenarios (alternative branch rejected,
    rollback on divergence).
  - Verifier: check pinned hash against accepted predecessor when processing
    revocation.

================================================================================
