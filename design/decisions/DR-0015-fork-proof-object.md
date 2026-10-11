---
title: "Grid Network — Transmissible fork-proof object"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-15
severity: Med
blocks: EXT
linked_finding: —
opened: 2026-10-11
deciders: (pending acceptance)
---
---
title: "Grid Network — Transmissible fork-proof object"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-15
severity: Med
blocks: EXT
linked_finding: —
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-15 — Transmissible fork-proof object

> **Status:** PROPOSED — NOT ACCEPTED.

## Metadata

- ID: D-15
- Title: Transmissible fork-proof object
- Severity: Med
- Blocks: EXT
- Linked finding: [REVIEW-2026-10-11 —](../REVIEW-2026-10-11.md)
- Date opened: 2026-10-11
- Status: PROPOSED

D-15: TRANSMISSIBLE FORK-PROOF OBJECT
[MEDIUM PRIORITY, DEPENDS ON D-03]

Problem:
§14 (D-03) generates FORK_EVIDENCE as a verifier outcome. But how does one
verifier communicate fork evidence to another? What is the authoritative
representation of a fork? D-15 considers whether to add a signed fork-proof
object that can be transmitted and acted upon.

Option A: Fork evidence is verifier-local; no transmissible object

  FORK_EVIDENCE is an outcome at one verifier; it records conflicting objects
  in its audit log. If another verifier queries, the first verifier can
  describe the fork informally (e.g., via a log export or a manual report).

  Pros:
    - Simpler: no new object or transmission protocol.
    - Verifiers are accountable: they hold fork evidence and cannot blame
      each other.

  Cons:
    - No standardized way to communicate forks.
    - Another verifier cannot automatically update based on fork evidence.

Option B: ForkProof object signed by a disputing party [NEW OBJECT]

  A new separator: grid/fork-proof/v1. Signed by one of the two conflicting
  stream authors. Contains: stream_id, conflicting_sequence,
  conflicting_commitments (array of object_commitment hashes), reason, issued_at.

  A verifier that receives a ForkProof can validate the signatures on both
  conflicting objects and mark the stream FORKED.

  Pros:
    - Transmissible: can be shared via rendezvous, relay, or email.
    - Standardized: every verifier knows how to parse and validate it.
    - Auditable: the ForkProof itself is signed.

  Cons:
    - Adds a new object type (1 more in the registry).
    - Proof generation and validation logic (small, but adds code).
    - Requires the disputing party to voluntarily generate a proof (could be
      kept secret).

Recommendation:
Defer to D-23 (vector planning). If testing reveals that fork communication
is valuable, add ForkProof in V1.1. For V1, fork evidence is verifier-local
(Option A).

Consequences:
  - If Option B is chosen later: add grid/fork-proof/v1 to EXTENSION registry;
    implement and vector it.
  - D-23: include fork scenarios and evidence-communication scenarios in the
    test plan.

================================================================================
