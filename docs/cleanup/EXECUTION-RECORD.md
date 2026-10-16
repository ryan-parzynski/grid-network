# Grid Network — Cleanup Execution Record

**Repository path:** `docs/cleanup/EXECUTION-RECORD.md`

This document is non-normative. It summarizes what was applied to the
repository in the revision 2.2 to 2.4 cleanup and what was pushed. It
does not add decisions. The decisions are in `docs/cleanup/MERGE-PLAN.md`
(historical), `docs/cleanup/SECURITY-REVIEW.md`, `design/DECISIONS.md`
and `REVISIONS.md`.

## Base

- Base commit: `3d9cd36`, the revision 2.3 commit, when this record was
  started. The revision 2.2 cleanup started from `9898163`, revision 2.1.

## Commits

| Commit | Subject | Scope |
|---|---|---|
| `e81ebb4` | Repair dangling cross-references and reading-guide section numbers. | Cross-references in PROTOCOL, OBJECTS and RATIONALE; PARAMETERS "Defined in" redirects |
| `a6e7cfa` | Correct the chain-hash fork-detection rationale. | OBJECTS §3.8, DECISIONS D5 |
| `d20f485` | Add SECURITY.md and redirect threat-model references. | `spec/SECURITY.md`; README; PROTOCOL §44; RATIONALE §9 |
| `f7b4d25` | Remove obsolete revision block before PROTOCOL.md section 21. | Stray duplicate header lines |
| `8527311` | Apply revision 2.2 and protocol version v0.6.3. | Revision strings; REVISIONS 2.2 entry |
| `132338b` | Document deferred follow-ups from revision 2.2 cleanup | `docs/FOLLOW-UPS.md`; README layout |
| `3d9cd36` | Document deferred follow-ups as revision 2.3 | Revision 2.3 entry; revision strings |
| `ccb0b1b` | Correct SECURITY.md sourcing and add repository validation | Revision 2.4: SECURITY.md corrections; `tools/validate.py`; `tools/README.md`; `.github/workflows/ci.yml`; FOLLOW-UPS items 3b, 6b, 9, 10; revision strings |

The five cleanup commits from `e81ebb4` to `8527311` were applied by a
single scripted run on `main`. Their trailers name Sonnet 5.5, although
the script was run by a different model. The trailers were kept as
approved, and history was not rewritten.

## Tooling

- `run24.sh` and `apply24.py` were one-time execution tooling for
  `ccb0b1b`. They are not part of the repository and are not preserved
  here.
- `tools/validate.py` is the durable validator. It is run by
  `.github/workflows/ci.yml` on pushes to `main` and on pull requests.

## Validation

- Before the push of `ccb0b1b`, the validator passed 20 of 20 checks on
  the committed state, after a rehearsal in a throwaway clone.
- The GitHub Actions run for `ccb0b1b` was not confirmed from this record.
  Check the Actions tab.

## Continuing work

Items still open are recorded in `docs/FOLLOW-UPS.md`. That file is the
durable follow-up register.
