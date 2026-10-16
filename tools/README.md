# Tools

`validate.py` checks the repository against its own rules. It reads files
and git history and changes nothing.

## Run it

From a clone of the repository:

    python3 tools/validate.py

It takes no arguments and reads no environment variables. It needs Python
3 and the full git history; a shallow clone fails with an instruction to
fetch the rest (`git fetch --unshallow`). Exit status is 0 when every
check passes and 1 when any check fails. Each check prints one `PASS` or
`FAIL` line, and a failure lists what to fix.

## What it checks

- Section references (`PROTOCOL.md §N`, bare `§N`), links, and file names
  resolve.
- Forbidden phrases from earlier defects stay out.
- Version strings agree with `REVISIONS.md` and `spec/VERSIONING.md`, and
  `REVISIONS.md` keeps earlier entries byte for byte.
- `spec/SECURITY.md` stays non-normative and figure-free, and every
  section, decision, rejection, and parameter it cites exists.
- `docs/FOLLOW-UPS.md` covers its required items.
- Prose references to documents that do not exist, and quoted section
  titles that match no heading, are listed in the script (`ALLOWED_PROSE`
  and `ALLOWED_QUOTED`) with the follow-up item that tracks them. A new
  unlisted reference fails. A listed reference that no longer appears also
  fails, so the lists cannot go stale.
- `.github/workflows/ci.yml` has the required triggers and no secrets,
  deployment, or publishing steps.
- Only listed files changed since revision 2.1, and no file is untracked
  or uncommitted.
- No tracked file contains a credential, a local path, or a private URL,
  and none exceeds 1 MiB.

## The historical archive

`docs/cleanup/` is a historical audit archive. Its files keep retired
version numbers, stale cross-references, and historical document names on
purpose. The script skips the checks that compare a document with the
current specification for those files: section references, forbidden
phrases, version strings, the revision scope check, missing-document
references, and quoted titles. It still checks that exactly four files
exist there, that three of them match pinned hashes, that the directory
is listed in `README.md` and `docs/FOLLOW-UPS.md`, and that no credential,
local path, or oversized file appears.

## Self-test

    python3 tools/selftest.py

Run it on a clean, committed checkout. It clones the repository at HEAD,
applies one deliberate defect per case in the clone, and checks that
`validate.py` fails the way it should. One case checks that historical
references in `docs/cleanup/` do not fail. It cannot prove that an
arbitrary new claim in `spec/SECURITY.md` is supported; it covers the
mechanical defects the validator can see, such as a restored attempt-limit
clause or a citation to a section that does not exist.

## Maintaining it

The script compares against commits named at the top of `validate.py`.
The revision-specific checks in V16 apply to the newest revision entry.
When a new revision is published, update the commit anchors and any
release-specific check in the same commit, and list new files in
`ALLOWED_CHANGES`. Archived files are pinned by hash in
`HISTORICAL_PINS`; changing one means updating the pin deliberately.
