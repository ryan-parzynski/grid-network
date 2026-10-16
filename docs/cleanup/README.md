# Grid Network — Cleanup Audit Archive

**Repository path:** `docs/cleanup/README.md`

`docs/cleanup/` is a historical audit archive. It preserves the review
and decision record for the revision 2.2 to 2.4 cleanup. It is
non-normative and adds no requirements.

**Do not treat these files as current documentation.** They may contain
retired version numbers, stale cross-references, historical document
names, and terminology that no longer matches the current
specifications. They must not be treated as current normative
documentation. The current specification source of truth remains the
files outside `docs/cleanup/`. Where an archived file and a current file
disagree, the current file governs.

- `MERGE-PLAN.md` is the merge plan for revision 2.2. It is historical.
  It is preserved verbatim, so it may refer to scratchpad paths and
  states that no longer exist. Read it as a record of what was decided,
  not as instructions.
- `SECURITY-REVIEW.md` records the independent traceability review of
  `spec/SECURITY.md` and what was done with each finding.
- `EXECUTION-RECORD.md` summarizes what was applied and pushed, from the
  base commit through revision 2.4.

The durable validator is `tools/validate.py`. It treats this directory as
a historical archive: it skips the checks that compare documents with the
current specification, and it still checks which files may change here,
for credentials and local paths, and for file size. The durable
follow-up register is `docs/FOLLOW-UPS.md`. Items still open are
recorded there, not here.
