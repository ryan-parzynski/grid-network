---
title: "Grid Network — previous_hash redundancy"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-17
severity: Med
blocks: V1.1
linked_finding: —
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-17

> **Status:** PROPOSED — NOT ACCEPTED.



## Context / Problem

v0.6.2 transmits both previous_hash and chain_hash in every object. §13.2
defines previous_hash(N) = object_commitment(N-1) and chain_hash(N) =
SHA256(...previous_chain_hash(N), object_commitment(N)). The verifier can
compute previous_hash from committed state, so sending it is redundant and
increases object size. Should it be removed?

## Options considered

Option A: Remove previous_hash from the wire; derive it during verification

  Objects omit previous_hash. The verifier computes the expected previous_hash
  from its accepted head at sequence N-1 and compares it to the incoming
  object's commitment. If they match, proceed; if not, CHAIN_MISMATCH.

  Pros:
    - Smaller objects (~64 bytes saved per object).
    - Clearer semantics: chain_hash is the only linking value.
    - Still deterministic: verifier computes the expected previous from
      accepted state.

  Cons:
    - Implementers must remember to derive and check previous_hash.
    - Streaming/progressive verification is slightly more complex (must have
      accepted N-1 before verifying N).

Option B: Keep both on the wire [v0.6.2 behavior]

  No change. Objects carry both values.

  Pros:
    - Explicit: every linkage is named.
    - Easier for naive implementations to check both.

  Cons:
    - Redundant: one of the two is computable.
    - Larger object size.
    - More test vectors needed (both fields must match).

## Recommendation (PROPOSED — NOT DECIDED)

> **PROPOSED:**

Accept Option A (remove previous_hash, derive it). Saves space and improves
clarity. Update §13.2 and the verifier procedure (§14) to derive and check it.

## Consequences

- OBJECTS.md: remove previous_hash field from all object schemas.
  - §13.2: describe the derivation during verification.
  - §14 step 9: modified to derive and check previous_hash.
  - Test vectors: re-encode all objects without previous_hash; update
    verification scenarios.
  - Implementer guide: pseudocode for previous_hash derivation.

================================================================================
