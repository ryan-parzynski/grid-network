---
title: "Grid Network — V1 minimal profile"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-22
severity: High
blocks: V1
linked_finding: L1
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-22

> **Status:** PROPOSED — NOT ACCEPTED.



## Context / Problem

v0.6.2 defines 19 object types, but not all are needed to prove the kernel.
D-22 is the planning decision for what goes in V1 minimal (§13.5) vs V1.1 vs
EXTENSION.

## Options considered

Option A: Minimal V1 profile [PROPOSED in §13.5]

  9 core object types: IdentityDocument, KeyRevocation, RelationshipAssertion,
  RelationshipTermination, Grant, Lease, GrantRevocation, LeaseRevocation,
  ReachabilityRecord.
  + IdentityContinuity (if D-05 root rotation in V1).
  + IdentityTerminal (if D-05 accepted; required for continuity).
  + FreshnessAttestation (if D-08 Option A accepted; ephemeral).

  Streams: identity, relationship (if D-07 Option A), authorization,
  reachability.

  Removed from V1: Services as separate principals, StreamResolution,
  relays beyond minimal ticket model, operator manifests, recovery, multipath,
  federation.

  Exit criteria for v0.8.0: CDDL for every V1 object, reference verifier, 
  byte-exact vectors, two independent verifiers agree on all vectors.

  Pros:
    - Scoped: provable in reasonable time.
    - Kernel-focused: all authority decisions covered (identity,
      relationships, grants, leases, revocation, reachability).
    - Unblocks extensions: clear boundary between V1 and later work.

  Cons:
    - V1.1 work is deferred (services, federation, etc.).
    - Some use cases (e.g., service-specific keys) are not V1.

Option B: Kitchen sink: all 19 types in V1

  v0.6.2 as-is: all object types in V1.

  Pros:
    - Complete: every described feature is V1.

  Cons:
    - Unbounded scope: never ship.
    - Testing burden: 19 object types × 4 outcomes × edge cases = huge vector
      set.
    - Distraction: relay economy, federation, recovery are not kernel.

## Recommendation (PROPOSED — NOT DECIDED)

> **PROPOSED:**

Accept Option A (minimal profile). Draw a hard line around V1: identity,
relationships, grants, leases, reachability, revocation, pairing. Everything
else defers to V1.1 or extensions.

## Consequences

- §13.4 and §13.5: finalize the object registry with V1 / V1.1 / RESERVED /
    EXTENSION labels.
  - OBJECTS.md: write CDDL for the 9–11 V1 objects only initially.
  - design/EXTENSIONS.md: describe ServiceRecord, OperatorManifest,
    RelayTicket, RelayNodeRecord, StreamResolution, federation, multipath,
    recovery.
  - Roadmap: stages 2–3 are V1 (kernel); stages 4+ are V1.1 and extensions.

================================================================================
