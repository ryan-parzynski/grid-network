---
title: "Grid Network Spec Change Log"
status: v0.6.2 design-review baseline + v0.7.0 placeholder
version: 2026-10-11
date: 2026-10-11
---

# Change Log

## v0.6.2 (2026-10-11) — Design-review baseline

- Protocol kernel (§1–§65) preserved from consolidated source.
- Design-review edits applied: PENDING DECISION callouts at affected sections; no promotion of [PROPOSED] items to normative; §14 / §47 verification stays v0.6.2 (two-class accept/reject) — four-output proposal kept in `design/decisions/DR-0003-verifier-outcomes.md` only.
- Sections with NEEDS AUTHOR INPUT marked: §14 (lease expiry mechanics), §6 (object schemas / CDDL), §55 (application integration profile), §60 (test vector values), §1 / §8 (canonical form / intro).
- Cross-references verified: all 26 `DR-0001..DR-0026-*.md` exist; links from spec to `../../design/decisions/DR-*.md` resolve; links from DR to `../REVIEW-2026-10-11.md` / `../DECISIONS.md` / related DR resolve.
- Review contradictions identified (see `../../design/REVIEW-2026-10-11.md`): C1–C6 (revocation / pairing / verification / authority), H1–H7 (stream privacy / root / revocation / freshness / refs / local API), M1–M5 (relationship / identifiers / authorization / rendezvous / revocation fields), L1–L3 (scope / reader-copy / licensing). All mapped to D-01..D-26 in `../../design/DECISIONS.md`.
- Preserved: all [REVIEW-2026-10-11 C/H/M/L] tags (in review); all [PROPOSED]/[UNCHANGED]/[OPEN D-xx] (in review/decisions); all option letters A/B/C and pros/cons (in DR); Ed25519 rules (DR-0013 + §58); resource-limit table entries (DR-0011 + §13.6 proposed); rejection classes (§10); cryptographic equations (§58 domain separators); threat model (§50); conformance (§61).
- Not promoted to normative: four-outcome verifier (D-03); new revocation fields (D-04 until accepted); stream split (D-01/D-07); PAKE choice (D-06); Relationship Key (D-09); V1 profile (D-22) — v0.6.2 text preserved with callouts.

## v0.7.0 (placeholder — to be written when D-01..D-13 accepted)

When decisions D-01 (stream identity), D-02 (chain base), D-03 (verifier — only if four-output accepted, else keep v0.6.2), D-04 (revocation pinning), D-05 (continuity), D-06 (PAKE), D-07 (privacy), D-08 (freshness), D-09 (root custody), D-10 (local API), D-11 (limits), D-12 (clock), D-13 (Ed25519) are ACCEPTED: update `spec/PROTOCOL.md` (§8–§11, §18–§20, §24–§29, §9, §12, §40, §13.6, §47); update `spec/OBJECTS.md` (§3.5, §7, §9, §13.2); generate `spec/OBJECTS.md` schemas (§6); regenerate test vectors (§60); update `CHANGELOG.md`; bump version to v0.7.0 per `VERSIONING.md`.

See `../../design/DECISIONS.md` for acceptance procedure (`status: ACCEPTED` in `DR-*.md` + same-PR spec update + CHANGELOG entry).
