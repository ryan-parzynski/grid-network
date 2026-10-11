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

# D-02 — Chain base derivation

> **Status:** PROPOSED — NOT ACCEPTED. Change only on merged PR with spec updates and CHANGELOG entry.

## Metadata

- ID: D-02
- Title: Chain base derivation
- Severity: High
- Blocks: V1
- Linked finding: [REVIEW-2026-10-11 C4](../REVIEW-2026-10-11.md) (see section C4 or search tag)
- Date opened: 2026-10-11
- Status: PROPOSED

## Context / Problem

Context (C4): chain init (§11,§45) needs derivation; [REVIEW-2026-10-11 C4].

## Options considered (preserved from PART V — A/B/C, pros, cons)

- **A:** previous_hash=H(root||seq0||domain). Pros: deterministic. Cons: root-only.
- **B:** previous_hash=H(root||device||nonce). Pros: binds device. Cons: needs binding at init.

## Recommendation (PROPOSED — NOT DECIDED)

> **PROPOSED:** (selection per options above; do not mark DECIDED until accepted via PR). If this decision is accepted: update this file status; update `spec/PROTOCOL.md` and `spec/OBJECTS.md` (remove/add PENDING DECISION callout); update `spec/CHANGELOG.md`; regenerate test vectors if affected (D-23).

## Consequences

- **Files:** `spec/PROTOCOL.md`, `spec/OBJECTS.md`, `spec/CHANGELOG.md` (and `design/DECISIONS.md` index when accepted).
- **Dimensions:** new fields / key roles / verification paths / reference rules / stream splits / transport bindings.
- **Migration:** (note if any; otherwise "none — applies to new records").

## Security review answers (§19 rule)

- **Authority protected?** Yes — root or delegated key role signs the relevant object; verification uses strict Ed25519 (§58) with domain separator.
- **Attack prevented?** Per context (replay / forgery / inference / escalation — see "Context").
- **Failure behavior if absent?** Safe denial — absence of record / proof = authorization not granted (not a security failure of authority).
- **Complexity added?** Documented per option above; minimized by staying with v0.6.2 where proposal is deferred (B options).

## Cross-references (must resolve)

- Review finding: [`../REVIEW-2026-10-11.md`](../REVIEW-2026-10-11.md) (search tag `C4`)
- Decision index: [`../DECISIONS.md`](../DECISIONS.md)
- Related decisions (links below must resolve to DR-*.md in same directory):
  - [`DR-0002`](./DR-0002-chain-base.md) relates to D-04 pin content; [`DR-0007`](./DR-0007-relationship-privacy.md) relates to D-09/stream split; [`DR-0009`](./DR-0009-root-custody.md) affects D-05/D-07.
- Spec (v0.6.2 kernel + PENDING DECISION callout for D-02): [`../../spec/PROTOCOL.md`](../../spec/PROTOCOL.md) / [`../../spec/OBJECTS.md`](../../spec/OBJECTS.md) — callouts added at affected sections.

*Preservation: option letters A/B/C and pros/cons preserved from PART V; status = PROPOSED (not ACCEPTED); for D-03, four-outcome proposal kept ONLY here — `spec/PROTOCOL.md` §47 and `spec/OBJECTS.md` §9 remain v0.6.2 with PENDING DECISION callout.*
