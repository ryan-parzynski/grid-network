---
title: "Grid Network — Resource limits"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-11
severity: High
blocks: V1
linked_finding: —
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-11

> **Status:** PROPOSED — NOT ACCEPTED.



## Context / Problem

v0.6.2 states that limits are "deferred to the applicable completed schema."
Hostile CBOR input must be rejected before allocation; without normative
limits, every parser is left guessing (H5).

## Options considered

Option A: Normative table in §13.6 [PROPOSED]

  Encode starting limits in the specification as a normative table:
    Max encoded object size .................. 16 KiB
    Max CBOR nesting depth ................... 8
    Max text string length (free text) ....... 1024 bytes
    Max identifier length .................... 128 bytes
    Max byte string length ................... 1024 bytes
    Max elements in any set/array ............ 256
    Max authorized_keys / bindings ........... 64 each
    Max capabilities per Grant ............... 64
    Max constraint map entries ............... 32
    Max endpoints per ReachabilityRecord ..... 16
    Max deferred (gap) objects per stream .... 64
    Max objects per sync response ............ 256
    Max fork-evidence records per stream ..... 16

  Exceptions: IdentityDocument may be 64 KiB to accommodate large authorized_keys
  and bindings.

  Pros:
    - Implementations know exactly where to check.
    - Prevents DOS by allocation (parser rejects oversized input before heap
      allocation).
    - Unambiguous interoperability.

  Cons:
    - Limits may need adjustment after measurement; if so, new version of
      protocol.
    - Specifying limits is a commitment; if too tight, real deployments fail.

Option B: Guidelines only; defer to implementation

  §13.6 is advisory. Implementations choose their own limits.

  Pros:
    - Flexibility: each implementation can optimize for its environment.

  Cons:
    - Verifiers diverge: one rejects an object as oversized; another accepts
      it.
    - Interoperability breaks.
    - No protection against DOS by allocation.

## Recommendation (PROPOSED — NOT DECIDED)

> **PROPOSED:**

Accept Option A (normative table in §13.6). Test against the limits before
release (D-23). If measurement shows a limit is wrong, revise and re-tag the
spec.

## Consequences

- §13.6: finalize the table with measurements (D-23 responsibility).
  - Implementer guide: pseudocode for size checks before CBOR parsing.
  - Test vectors: object at limit, object 1 byte over limit (rejection).
  - Conformance: every conformance test must enforce the same limits.
  - IdentityDocument exception: document the reason (large key sets) and keep
    it in reviews.

================================================================================
