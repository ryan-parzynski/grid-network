---
title: "Grid Network — Chain base derivation"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-02
severity: High
blocks: V1
linked_finding: C4
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-02

> **Status:** PROPOSED — NOT ACCEPTED.



## Context / Problem

v0.6.2 computes initial_chain_hash using domain_separator as an input (C2).
But a stream may hold multiple object types (identity stream holds
IdentityDocument, KeyRevocation, RelationshipAssertion, IdentityContinuity).
Which separator determines the chain base? The spec says the type of the
*first* object, which is ambiguous and fragile.

## Options considered

Option A: Stream class as the base input

  initial_chain_hash = SHA-256(canonical_cbor(
      ["grid/chain-base/v1", stream_class, stream_id]))

  stream_class ∈ { "identity", "relationship", "authorization",
                   "reachability", "service" }   (fixed, small registry)

  Pros:
    - Deterministic: independent of which object arrives first.
    - Simple: one chain base per stream, always.
    - No fork ambiguity from "which separator did the first object have?"

  Cons:
    - Object schema must declare which stream_class(es) it belongs to.
    - Slightly more bytes in the derivation label (adds stream_class string).

Option B: Per-object-type derivation; chain base is always the first object's
separator

  Each object type declared as belonging to one stream_class. The separator of
  the first accepted object in that stream determines initial_chain_hash. If
  the first object has separator S, use S in the derivation.

  Pros:
    - Preserves the v0.6.2 design: everything flows from the first object.

  Cons:
    - Verifiers that haven't yet received the first object cannot construct
      the chain base and cannot validate a sequence-2 object. They must
      defer sequence 2 until sequence 1 arrives.
    - If two conflicting sequence-1 objects exist with different separators
      (both valid signatures), they implicitly define different chain bases
      and no fork is detected at the stream level—only at the object level.
      This obscures fork evidence.
    - "First object matters" reasoning is fragile and hard to reason about.

## Recommendation (PROPOSED — NOT DECIDED)

> **PROPOSED:**

Accept Option A (stream class in base derivation). Simpler, deterministic,
removes order dependence. Update §13.2 with the formula above. Each object
schema includes a required stream_class field or the schema spec names it.

## Consequences

- OBJECTS.md: every object schema declares stream_class ∈ {...}.
  - Chain base vectors: one for each stream_class.
  - Verifiers: compute initial_chain_hash once per stream, on first reference.

================================================================================
