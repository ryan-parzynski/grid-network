---
title: "Grid Network — Fork resolution and dispute handling"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-14
severity: High
blocks: EXT
linked_finding: —
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-14

> **Status:** PROPOSED — NOT ACCEPTED.



## Context / Problem

v0.6.2 includes a heavy StreamResolution mechanism for resolving forks at the
stream level. It assumes a resolver is trusted, a conflict is recorded, and
votes/timestamps select a winner. However, forks in authorization streams can
already be resolved by the root using KeyRevocation with pinning (D-04). For
identity streams, root compromise has no in-band recovery anyway. D-03
(explicit fork evidence) changes the landscape: forks are now first-class
verifier outcomes, not errors to be resolved.

## Options considered

Option A: Defer StreamResolution to extension (V1.1)

  V1 fork policy: authorization-stream fork → root issues KeyRevocation
  pinned to the last good chain hash (D-04 already handles this).
  Identity-stream fork → principal is marked FORKED for that verifier; no
  authority beyond the last common accepted point; out-of-band re-pairing.

  StreamResolution, voting, resolver delegation, and dispute mechanics are
  designed in design/EXTENSIONS.md for later versions.

  Pros:
    - Simplifies V1: no resolver machinery in the kernel.
    - D-04 (KeyRevocation pinning) is the primary resolution mechanism.
    - Fork evidence (§14, D-03) is sufficient for auditing.
    - V1.1 can add StreamResolution if real deployments need it.

  Cons:
    - Identity-stream forks require out-of-band coordination (inconvenient
      for users).
    - No automatic dispute resolution; users must notice and act.

Option B: Include StreamResolution in V1 [ORIGINAL v0.6.2]

  Implement the full mechanism: resolver eligibility, vote counting,
  timestamp-based selection, rollback semantics.

  Pros:
    - Automated fork resolution (better UX).
    - Can delegate to higher-level keys without involving the root.

  Cons:
    - Adds 200+ lines of spec to the kernel.
    - Introduces voting and availability dependence ("which resolver is
      online?").
    - Verifiers disagree if a resolver is unavailable or sends conflicting
      evidence.
    - Not proven necessary (KeyRevocation pinning solves authorization
      streams; identity forks are rare in well-managed systems).
    - Violates "fail closed on unresolved conflicts."

## Recommendation (PROPOSED — NOT DECIDED)

> **PROPOSED:**

Accept Option A (defer to V1.1). Focus V1 on proving the kernel works
(identity, relationships, grants, leases, revocation, reachability). Add
StreamResolution as a V1.1 extension if real deployments show a need.

## Consequences

- §16.1: moved to design/EXTENSIONS.md (marked EXTENSION in separator
    registry).
  - §14: fork evidence is an outcome; no automatic resolution machinery in V1.
  - design/EXTENSIONS.md: StreamResolution will be specified there.
  - Test vectors: fork evidence scenarios; out-of-band re-pairing recovery.
  - D-14 simplifies the V1 spec significantly; focus shifts to D-06 and D-20
    (pairing and wire protocol).

================================================================================
