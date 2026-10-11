---
title: "Grid Network — Identity Root custody"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-09
severity: High
blocks: V1
linked_finding: H2/H3
opened: 2026-10-11
deciders: (pending acceptance)
---
---
title: "Grid Network — Identity Root custody"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-09
severity: High
blocks: V1
linked_finding: H2/H3
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-09 — Identity Root custody

> **Status:** PROPOSED — NOT ACCEPTED. Change only on merged PR with spec updates and CHANGELOG entry.

## Metadata

- ID: D-09
- Title: Identity Root custody
- Severity: High
- Blocks: V1
- Linked finding: [REVIEW-2026-10-11 H2/H3](../REVIEW-2026-10-11.md) (see section H2/H3 or search tag)
- Date opened: 2026-10-11
- Status: PROPOSED

D-09: IDENTITY ROOT CUSTODY AND RELATIONSHIP KEY DELEGATION
[HIGH PRIORITY, IMPACTS DEPLOYMENT AND KEY MANAGEMENT]

Problem:
v0.6.2 intends the Identity Root to be offline, yet requires it to sign every
RelationshipAssertion and RelationshipTermination. In practice, users will
keep the root online to enable routine pairing, contradicting the design goal
(H3). A separate Relationship Key role could allow the root to stay offline.

Option A: Introduce Relationship Key, delegated by root [PROPOSED in §5.3]

  New role: Relationship Key, distinct from Identity Root.
  Root signs a delegation: "this Relationship Key is authorized to make
  assertions and terminations for this principal."
  RelationshipAssertion and RelationshipTermination are signed by the
  Relationship Key, not the root.
  Root is offline or hardware-backed; Relationship Key is on the device.

  Pros:
    - Separates authority: root is not routine; Relationship Key handles
      pairing.
    - Enables offline-root operation.
    - Smaller attack surface: Relationship Key compromise does not compromise
      the root or the principal's other keys.
    - Aligns with role separation principle (§5.3).

  Cons:
    - One more key type to manage and delegate.
    - Delegation object adds to the identity stream.
    - Initial pairing requires the root to delegate the Relationship Key
      (bootstrapping).

Option B: No Relationship Key; keep using Identity Root for assertions

  v0.6.2 behavior: root signs every assertion and termination.

  Pros:
    - Simpler: one fewer key role.
    - Existing logic.

  Cons:
    - Root must be online for routine pairing.
    - Root compromise is immediately catastrophic (every relationship is
      attacker-controlled).
    - Does not achieve offline root goal.
    - Verifier-derived relationship state depends on the root being responsive
      for pairing; if the root is offline/slow, pairing is blocked.

Option C: Relationship Key is optional; either root or delegated key can sign

  Relationship Key exists but is optional. Implementations can skip it if they
  accept root online.

  Pros:
    - Flexible: simple deployments skip it, complex deployments use it.

  Cons:
    - Two verification paths: verifier must check both (root signature OR
      delegated key signature). More complex; more testing.
    - Implementations diverge: some require it, some don't. Interoperability
      is unclear.
    - Does not actually solve H3 unless the implementation chooses to use it.

Recommendation:
Accept Option A (Relationship Key, mandatory, delegated by root). Enables
offline-root operation. Update §5.3 key-role table, §7 (RelationshipAssertion
signing), and identity document schema to include a relationship_key_ids
field.

Consequences:
  - OBJECTS.md: add relationship_key_ids to IdentityDocument; define
    delegation semantics.
  - §5.3: update key-role table; make Relationship Key V1.
  - §7 and §9 (if needed): update signer eligibility rules.
  - Pairing (D-06): must include delegating the Relationship Key after the
    root bootstraps the device key.
  - Test vectors: delegation, compromise of Relationship Key, root offline
    scenarios.
  - Operators: can now generate root offline, create device + relationship keys,
    import device-specific keys to the device, and operate with root in a
    vault.

================================================================================
PART V — OPEN DECISIONS D-10 THROUGH D-18
================================================================================
