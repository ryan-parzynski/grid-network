---
title: "Grid Network — Same-sequence key revocations"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-16
severity: Med
blocks: V1.1
linked_finding: —
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-16

> **Status:** PROPOSED — NOT ACCEPTED.



## Context / Problem

If two KeyRevocations are accepted for the same Authorization Key with the
same effective_sequence but different effective_predecessor_chain_hash (D-04
introduces the predecessor hash), the root's stream is internally
inconsistent. Which revocation is correct? v0.6.2 does not address this.

## Options considered

Option A: First revocation stands; second is fork evidence

  The first accepted KeyRevocation for (key_id, effective_sequence) sets the
  pinned predecessor hash. A second KeyRevocation with a different hash is
  FORK_EVIDENCE.

  Pros:
    - Simple: deterministic rule.

  Cons:
    - Does not reveal which branch is legitimate (both could be valid
      signatures).

Option B: Both revocations are recorded; operator must investigate

  Mark both as valid but conflicting. Raise an operator alert: "root stream
  has conflicting revocations for key_id." Do not accept authority from either
  branch.

  Pros:
    - Explicit: operator is aware of the inconsistency.

  Cons:
    - No automatic resolution.
    - User-facing: users see an alert for a root-stream issue.

## Recommendation (PROPOSED — NOT DECIDED)

> **PROPOSED:**

Accept Option A (first revocation stands) unless operator experience testing
(D-23) shows otherwise. The scenario is rare (requires root to issue
conflicting revocations, i.e., root compromise or bug). If it happens,
re-pairing and explicit root recovery are likely needed anyway.

## Consequences

- §9 rule 6 (added by D-04): clarify that equal effective_sequence with
    different predecessor hashes is FORK_EVIDENCE at the root stream level.
  - Test vectors: competing revocations for the same key at the same
    effective_sequence.

================================================================================
