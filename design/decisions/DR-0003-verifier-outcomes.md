---
title: "Grid Network — Verifier outcomes and classification"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-03
severity: High
blocks: V1
linked_finding: C3
opened: 2026-10-11
deciders: (pending acceptance)
---
---
title: "Grid Network — Verifier outcomes and classification"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-03
severity: High
blocks: V1
linked_finding: C3
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-03 — Verifier outcomes and classification

> **Status:** PROPOSED — NOT ACCEPTED. Change only on merged PR with spec updates and CHANGELOG entry.

## Metadata

- ID: D-03
- Title: Verifier outcomes and classification
- Severity: High
- Blocks: V1
- Linked finding: [REVIEW-2026-10-11 C3](../REVIEW-2026-10-11.md) (see section C3 or search tag)
- Date opened: 2026-10-11
- Status: PROPOSED

D-03: VERIFICATION OUTCOMES AND CLASSIFICATION
[BLOCKING, CRITICAL PRIORITY]

Problem:
v0.6.2 §14 has two outcomes (ACCEPT, REJECT) but the procedure describes
cases that need more fine-grained handling: gaps (sequence N+5 arrives before
N+1), forks (conflicting sequence N with same predecessor), and overlapping
rejection criteria (e.g., INVALID_SEQUENCE and INVALID_PREVIOUS_HASH both
apply to the same object). C3 identifies the problem; §14 proposed replacement
has four outcomes.

Option A: Four outcomes, one check per class [PROPOSED in §14]

  ACCEPT           Valid object extends accepted head.
  REJECT(class)    One of 11 reject classes, exactly one per object.
  DEFER(GAP)       Authentic but predecessor not held; store deferred,
                   enter SYNCING.
  FORK_EVIDENCE    Authentic, correctly chained to accepted predecessor,
                   but conflicts with accepted object at same sequence.
                   Record evidence; stream enters FORKED.

  Verification steps: parse → identify schema → validate envelope/schema →
  verify signature → check signer → place in stream → validate chain/temporal
  → check revocation → semantic checks.

  One check per step; one step per rejection class.

  Pros:
    - Clear semantics for each outcome; no ambiguity on what to do next.
    - Forks are explicitly tracked and can be audited/resolved.
    - Deferred objects are not authority; SYNCING is a clear state.
    - Matches the "fail closed on gaps and forks" principle.

  Cons:
    - Implementers must handle three deferred/fork cases; slightly more code.
    - "Deferred" and "fork evidence" state must be persisted and bounded
      (§13.6).

Option B: Two outcomes, implicit handling [v0.6.2 model]

  ACCEPT / REJECT only. Gaps and forks are treated as REJECT with different
  error messages, or as state-dependent logic outside the verifier.

  Pros:
    - Simpler API surface.
    - Fewer state types.

  Cons:
    - Implementers add ad-hoc gap/fork logic outside the core verifier.
    - Verifiers diverge on how to handle missing predecessors (retry vs
      fail).
    - Fork handling is ambiguous: should a second valid sequence-N cause
      rollback, or is it an error?
    - Tested behavior is hard to specify without explicit outcomes.

Recommendation:
Accept Option A (four outcomes, one class per check). Implement the §14
procedure as proposed. This is the single highest-value decision for
unambiguous interoperable verification.

Consequences:
  - OBJECTS.md §5.3: becomes the §14 text verbatim.
  - Test vectors: at least one vector per outcome; one per rejection class.
  - Implementer docs: state-machine diagrams for SYNCING, FORKED, recovery.
  - D-14 (StreamResolution) depends on this; forks become explicit.
  - D-15 (fork-proof object) depends on this.

================================================================================
