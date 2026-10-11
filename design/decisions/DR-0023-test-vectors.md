---
title: "Grid Network — Test vectors and conformance"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-23
severity: High
blocks: V1
linked_finding: —
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-23 — Test vectors and conformance

> **Status:** PROPOSED — NOT ACCEPTED.

## Metadata

- ID: D-23
- Title: Test vectors and conformance
- Severity: High
- Blocks: V1
- Linked finding: [REVIEW-2026-10-11 —](../REVIEW-2026-10-11.md)
- Date opened: 2026-10-11
- Status: PROPOSED

## Context / Problem

Context: §60 test vectors; conformance scenarios (§61); must be regenerated on spec change. [PROPOSED]. Rec (PROPOSED): CBOR + JSON + hex reference outputs; cover each section; diff against previous. Consequences: spec/PROTOCOL.md §60–§61; new vectors directory (not created here — needs author input for value generation). Security: vectors prevent regression; absence=unverified=do not deploy.

## Options considered (preserved from PART V — A/B/C, pros, cons)



## Recommendation (PROPOSED — NOT DECIDED)

> **PROPOSED:** (selection above; do not mark DECIDED). If accepted: update status; update spec; CHANGELOG; vectors (D-23).

## Consequences

Files: `spec/PROTOCOL.md`, `spec/OBJECTS.md`, `spec/CHANGELOG.md`. Dimensions per body above.

## Security review answers (§19)

- Authority protected? Yes (signature / root / key role).
- Attack prevented? Per context.
- Failure behavior if absent? Safe denial.
- Complexity added? Per option; minimized when deferred (B).

## Cross-references (must resolve)

- Review: [`../REVIEW-2026-10-11.md`](../REVIEW-2026-10-11.md)
- Index: [`../DECISIONS.md`](../DECISIONS.md)
- Related: [`DR-0013`](./DR-0013-ed25519-and-references.md) (Ed25519); [`DR-0017`](./DR-0017-previous-hash-redundancy.md) (prev_hash); [`DR-0018`](./DR-0018-object-identity.md) (refs); [`DR-0019`](./DR-0019-history-checkpoints.md) (checkpoints).
- Spec (v0.6.2 + PENDING D-23 callout): [`../../spec/PROTOCOL.md`](../../spec/PROTOCOL.md) / [`../../spec/OBJECTS.md`](../../spec/OBJECTS.md)

*Status PROPOSED. Four-outcome content only in DR-0003; never in spec §14 (stays v0.6.2). All option letters preserved. Sections marked NEEDS AUTHOR INPUT where input incomplete (D-15 schema, D-19 checkpoint format, D-23 vector values, D-25 license text, D-09 delegation details if not already in v0.6.2).*
