---
title: "Grid Network — Identity continuity termination"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-05
severity: High
blocks: V1
linked_finding: C5
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-05

> **Status:** PROPOSED — NOT ACCEPTED.



## Context / Problem

v0.6.2 has no mechanism to end the predecessor identity stream. If the old
root signs a document after a continuity that references an earlier sequence,
verifiers that saw the new document reject the transition, and verifiers that
didn't accept it. Different verifiers reach different conclusions. C5
identifies the view-dependence problem.

## Options considered

Option A: IdentityTerminal object, signed by old root [PROPOSED in §16.2]

  New object: grid/identity-terminal/v1, signed by previous_root, as the
  final sequence of the predecessor stream.

  Fields: peer_id, new_root, successor_stream_id [from D-01],
  continuity_reason, issued_at.

  After IdentityTerminal is accepted, any further object in the predecessor
  stream is SEMANTIC_VIOLATION. Predecessor stream is deterministically closed.

  Competing terminals or competing continuities are FORK_EVIDENCE (not
  "first-wins").

  Pros:
    - Deterministic: every verifier with the terminal has a committed end to
      the old stream.
    - Explicit: the terminal is a signed artifact, auditable.
    - Detects forks: two different terminals or two competing
      successor-stream references are fork evidence, not silent divergence.

  Cons:
    - Adds a new object type (1 more in the V1 registry).
    - Root must sign both the terminal and the continuity (2 signatures
      required).
    - Verifier must receive the terminal before accepting the continuity
      (§14 step 8 allows DEFER).

Option B: Continuity object alone; treat old-root document after continuity
as simply a late arrival

  No terminal. The continuity references a predecessor sequence N. If a
  sequence N+1 arrives after the continuity, it's treated as late and either
  deferred or treated as a fork relative to the continuity.

  Pros:
    - One fewer object type.
    - Root signs only the continuity, not a separate terminal.

  Cons:
    - View-dependent: verifiers that see the N+1 document reject the
      transition; those that don't accept it.
    - Not deterministic per the core invariant (§4).
    - Doesn't actually work: N+1 arrived first in some verifier's view, so
      before the continuity it was accepted as ordinary identity state. You
      can't retroactively call it a fork.

## Recommendation (PROPOSED — NOT DECIDED)

> **PROPOSED:**

Accept Option A (IdentityTerminal object). Mandatory for deterministic
IdentityContinuity. Update §13.4 (separator registry) and §16.2 (continuity
rules).

## Consequences

- Add grid/identity-terminal/v1 to the separator registry.
  - OBJECTS.md: IdentityTerminal schema.
  - Verifier: step 8 of §14 defers continuity until terminal is held.
  - Test vectors: competing terminals, late N+1 documents, fork evidence.

================================================================================
