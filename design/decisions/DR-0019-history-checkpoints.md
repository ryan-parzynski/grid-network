---
title: "Grid Network — History checkpoints"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-19
severity: Med
blocks: EXT
linked_finding: —
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-19

> **Status:** PROPOSED — NOT ACCEPTED.



## Context / Problem

Append-only streams grow forever. A new verifier downloading a principal's
entire authorization stream from a rendezvous would fetch every object ever
issued, which could be thousands of lease/grant/revocation objects over
years. M4 flags this; it is not a correctness problem but a deployment
concern.

## Options considered

Option A: Checkpoint objects with prior pruning [V1.1 EXTENSION]

  New object: grid/stream-checkpoint/v1. Issued periodically (e.g., annually)
  by the stream issuer. Contains: stream_id, checkpoint_sequence,
  checkpoint_chain_hash, summarized_state (revoked_grants, revoked_leases,
  active_leases_count), issued_at.

  Rendezvous: may prune objects with sequence < checkpoint_sequence, retaining
  only the checkpoint and later objects. A new verifier can validate from the
  checkpoint forward.

  Pros:
    - Bounded download: new verifiers sync only from the latest checkpoint.
    - Issuer controls checkpointing; rendezvous cannot arbitrarily drop data.
    - Summarized state can be spot-checked by verifiers.

  Cons:
    - Adds a new object type.
    - Issuer must generate checkpoints.
    - Summarized state must be precisely defined (more schema work).

Option B: No checkpoints; accept unbounded growth [V1]

  V1 streams have no checkpoint mechanism. Verifiers download the whole
  history. Rendezvous must store everything.

  Pros:
    - Simpler V1.

  Cons:
    - Operational pain: rendezvous storage grows unboundedly.
    - Long bootstrap time for new verifiers.
    - Incentivizes key rotation to "reset" history (unintended consequence).

Option C: Truncation allowed; older objects discarded [V1, SIMPLE]

  Rendezvous may discard objects older than a retention window (e.g., 2
  years). Verifiers accept that they cannot verify the full history.

  Pros:
    - Operational simplicity.

  Cons:
    - Verifiers cannot prove what was valid historically.
    - Revocation of very old grants becomes hard to trace.
    - Contradicts the "verifier retains history for audit" principle.

## Recommendation (PROPOSED — NOT DECIDED)

> **PROPOSED:**

Accept Option B for V1 (unbounded growth; no checkpoints). Checkpoints are
designed in D-19 for V1.1 after real deployments reveal true growth rates. If
measurement (D-23) shows growth is problematic before v0.8.0, add a simple
checkpoint mechanism to V1.

## Consequences

- V1 spec: no checkpoint mechanism.
  - Rendezvous operators: must plan for multi-year storage (rough estimate:
    100 bytes per object × 10 grants/leases/revocations per principal ×
    1000 principals = ~1 GB for a 1000-peer rendezvous; varies wildly).
  - D-19 (checkpoint design) deferred to V1.1.
  - D-23: measure real growth under pilot deployments.

================================================================================
