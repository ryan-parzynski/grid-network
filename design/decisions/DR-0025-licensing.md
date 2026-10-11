---
title: "Grid Network — Licensing"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-25
severity: Low
blocks: —
linked_finding: L3
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-25

> **Status:** PROPOSED — NOT ACCEPTED.



## Context / Problem

The repository is licensed GPLv3. The stated goal is to embed the agent/SDK
in commercial and App Store applications (iOS, Android, Immich, Jellyfill,
Home Assistant, etc.). GPLv3 license compatibility with applications using
Apache 2.0, MIT, or proprietary licenses is a known problem. M5 flags this
(REVIEW-2026-10-11).

## Options considered

Option A: Split licensing [LEGAL REVIEW REQUIRED]

  Specification (spec/ directory): license under CC-BY-4.0 or CC0 (public
  domain). Permissive, non-viral.

  Test vectors (spec/TEST-VECTORS/): CC0 (examples are uncopyrighted).

  Reference implementation (reference/ and reference/): dual-license
  Apache-2.0 + GPLv3. Permissive Apache-2.0 allows embedding; GPLv3 is
  available for community projects.

  Agent library (the "common agent" meant for embedding): Apache-2.0 or MIT.
  Permissive, embed-friendly.

  Contributing and community: GPLv3 for community-contributed code; authors
  can elect to dual-license contributions.

  Pros:
    - Specification is free and unrestricted.
    - Agent library can be embedded in apps without conflict.
    - Community code can remain GPLv3 if authors prefer.

  Cons:
    - Multiple licenses are confusing; requires careful labeling.
    - Legal review is required before adoption.

Option B: Keep GPLv3 for everything; separate agent over IPC [NO LICENSE
CHANGE]

  The spec, reference implementation, and test vectors all remain GPLv3.
  Linking GPLv3 code into proprietary apps violates the license. But if the
  agent is a separate process communicating over IPC (Unix socket, named pipe,
  REST API), linking does not apply; the proprietary app just calls the
  service. The app can be proprietary; the agent is GPLv3 and separate.

  Pros:
    - No license change; GPLv3 is the choice.
    - IPC separation is architecturally sound.
    - Apps embedding the agent as a library must still comply with GPLv3, but
      calling a separate agent process is allowed.

  Cons:
    - IPC overhead (latency, security complexity).
    - Mobile platforms (iOS, Android) have limited background-process support;
      embedding in-process is often required.
    - The app and agent must coordinate carefully (socket creation, lifecycle).

Option C: Switch to Apache-2.0 or MIT; fork point for GPL community

  The whole project switches to Apache-2.0. Community members who want GPLv3
  can fork and re-license (permissible under Apache-2.0).

  Pros:
    - Embedding-friendly.
    - Simplest.

  Cons:
    - Breaks the GPL-community intention.
    - Re-licensing a fork adds friction.

## Recommendation (PROPOSED — NOT DECIDED)

> **PROPOSED:**

Defer to counsel. Before v0.8.0, obtain legal advice on Option A (split
licensing) and Option B (IPC separation as a GPL-compliance strategy). Make
the decision and document it in CONTRIBUTING.md. Do not ship an implementation
without clarity.

## Consequences

- Legal review required (not a technical decision).
  - If Option A: apply licenses to each directory; update LICENSE.md and
    CONTRIBUTING.md.
  - If Option B: enforce IPC architecture in design docs and implementer
    guide.
  - D-25 should be resolved before v0.8.0; otherwise, App Store and embedded
    deployment will face licensing barriers.

================================================================================
