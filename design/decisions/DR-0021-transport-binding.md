---
title: "Grid Network — Transport binding"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-21
severity: Low
blocks: EXT
linked_finding: M4
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-21 — Transport binding

> **Status:** PROPOSED — NOT ACCEPTED.

## Metadata

- ID: D-21
- Title: Transport binding
- Severity: Low
- Blocks: EXT
- Linked finding: [REVIEW-2026-10-11 M4](../REVIEW-2026-10-11.md)
- Date opened: 2026-10-11
- Status: PROPOSED

## Context / Problem

Context (M4): rendezvous ingestion (§33); transport mapping (§34). [PROPOSED]. Rec (PROPOSED): HTTPS rendezvous V1; wire protocol deferred. Consequences: spec/PROTOCOL.md §34; spec/OBJECTS.md §4 envelope unchanged.

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
- Spec (v0.6.2 + PENDING D-21 callout): [`../../spec/PROTOCOL.md`](../../spec/PROTOCOL.md) / [`../../spec/OBJECTS.md`](../../spec/OBJECTS.md)

*Status PROPOSED. Four-outcome content only in DR-0003; never in spec §14 (stays v0.6.2). All option letters preserved. Sections marked NEEDS AUTHOR INPUT where input incomplete (D-15 schema, D-19 checkpoint format, D-23 vector values, D-25 license text, D-09 delegation details if not already in v0.6.2).*
