---
title: "Decision Record Template"
status: TEMPLATE (no content from input — skeleton only)
date: 2026-10-11
---

# Decision Record Template — DR-00xx

| Field | Value |
|---|---|
| ID | D-xx |
| Status | PROPOSED (change to ACCEPTED / REJECTED / SUPERSEDED only on merge) |
| Severity | High / Medium / Low |
| Blocks | V1 / V1.1 / EXTENSION / — |
| Opened | 2026-10-11 |
| Deciders | (names when accepted) |

## Context

Which finding (C/H/M/L code from `design/REVIEW-2026-10-11.md`)? Which spec sections affected (`spec/PROTOCOL.md` / `spec/OBJECTS.md` sections)? Related decisions (links to `DR-*.md`).

## Options considered

- **Option A:** (description) — pros: / cons:
- **Option B:** (description) — pros: / cons:
- **Option C:** (description) — pros: / cons: (if any)

## Decision (leave empty until accepted)

> **Status:** PROPOSED — not ACCEPTED. Fill only when decision is accepted.

## Consequences

Files to change: `spec/PROTOCOL.md` (§), `spec/OBJECTS.md` (§), `spec/CHANGELOG.md`. Vectors to add/update: `spec/OBJECTS.md` §3.5 / §6 / §7 / §9 / §13.2. Migration notes: (if any).

## Security review answers (§19 rule)

- Authority protected? (yes/no + how)
- Attack prevented? (which attack, which failure mode)
- Failure behavior if absent? (availability / confidentiality / integrity impact)
- Complexity added? (new fields / new verification paths / new key roles)
