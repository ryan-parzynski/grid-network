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

## Maintaining it

The script compares against three commits named at the top of
`validate.py`. The revision-specific checks in V16 apply to the newest
revision entry. When a new revision is published, update the commit
anchors and any release-specific check in the same commit, and list new
files in `ALLOWED_CHANGES`.
