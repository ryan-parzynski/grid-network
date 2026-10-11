---
title: "Migration — Top-Level Documentation Relocation"
status: RESOLUTION A APPLIED 2026-10-11
date: 2026-10-11
---

# Migration — Top-Level Documentation Relocation

Prior split (commit 34b16c3) wrote split-layout content over the original
README.md / CONTRIBUTING.md / VERSIONING.md (previous HEAD d329409).
This relocation resolves the conflict without deleting content.

- Pre-existing originals: preserved verbatim at `legacy/README.md`,
  `legacy/CONTRIBUTING.md`, `legacy/VERSIONING.md` (checked out from
  d329409).
- Split layout: remains at repo root (`README.md`, `CONTRIBUTING.md`,
  `VERSIONING.md`) per the split-layout specification.
- Nothing deleted; only relocated the originals into `legacy/`.
- The split-layout versions are the design-review versions (status,
  version, related_decisions blocks) and reference the 26 open
  decisions (`design/DECISIONS.md`).
- To restore original docs to root: move `legacy/*.md` to root and
  remove/update the split versions.

See `design/REVIEW-2026-10-11.md` and `spec/CHANGELOG.md` for context.
