#!/usr/bin/env python3
"""Negative tests for tools/validate.py.

Usage:
    python3 tools/selftest.py

Run it on a clean, committed checkout. For each case it clones the repository
at HEAD into a temporary directory, applies one deliberate defect, commits it
there, runs tools/validate.py in the clone, and checks which checks fail. The
repository you run it in is never modified. It needs git and Python 3 only.

Each case states the checks that must fail. One case states that nothing may
fail: historical references inside docs/cleanup/ are allowed. The cases added
in revision 2.6 cover operations/IMPLEMENTATION-NOTES.md (a broken reference, a
normative keyword, an uncited statement, a dangling document name, a named
language), a new unsupported claim in spec/SECURITY.md, a stale revision
string, an unexpected new file, a dollar figure, a superiority claim in a
LINEAGE entry, an edited LINEAGE entry, and a threshold-recovery status that
disagrees with the rest of the repository.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GIT = ["git", "-c", "user.name=selftest", "-c", "user.email=selftest@example.invalid"]


def append(path, text):
    def mutate(work):
        p = work / path
        p.write_text(p.read_text(encoding="utf-8") + text, encoding="utf-8")
    return mutate


def replace(path, old, new):
    def mutate(work):
        p = work / path
        s = p.read_text(encoding="utf-8")
        if s.count(old) != 1:
            raise SystemExit("selftest setup error: %r is not unique in %s" % (old[:50], path))
        p.write_text(s.replace(old, new), encoding="utf-8")
    return mutate


def create(path, text):
    def mutate(work):
        (work / path).write_text(text, encoding="utf-8")
    return mutate


# Credentials are built at run time so that this file does not contain one.
FAKE_TOKEN = "gh" + "p_" + "A1b2C3d4E5" * 4
LOCAL_PATH = "/" + "home" + "/someone/project"
NOTES = "operations/IMPLEMENTATION-NOTES.md"
HISTORICAL = ("\nHistorical note: see the Operator Guide, protocol v0.6.2, PROTOCOL.md §99,\n"
              "the section \"Nonexistent Chapter\", and the stated threat model.\n")

CASES = [
    ("baseline: the checked-out state passes", lambda w: None, set()),
    ("unsupported claim restored in SECURITY.md",
     replace("spec/SECURITY.md", "Residual limits are stated",
             "and attempts are limited (`PROTOCOL.md §20`, `PROTOCOL.md §21`). Residual limits are stated"),
     {"V19"}),
    ("new citation to a section that does not exist in SECURITY.md",
     replace("spec/SECURITY.md", "(`PROTOCOL.md §47`, Section 3)", "(`PROTOCOL.md §99`, Section 3)"),
     {"V1", "V19"}),
    ("dangling prose reference in a current spec document",
     append("spec/OBJECTS.md", "\nSee the Operator Guide for details.\n"), {"V17"}),
    ("retired version in a current spec document",
     append("spec/GLOSSARY.md", "\nWritten for v0.6.2.\n"), {"V6"}),
    ("current specification document changed substantively",
     append("spec/PROTOCOL.md", "\nAn added sentence that is not a revision string.\n"), {"V16"}),
    ("secret added under docs/cleanup/",
     append("docs/cleanup/README.md", "\nExample: %s\n" % FAKE_TOKEN), {"V22"}),
    ("local path added under docs/cleanup/",
     append("docs/cleanup/README.md", "\nBuilt in %s\n" % LOCAL_PATH), {"V22"}),
    ("unexpected file added under docs/cleanup/",
     create("docs/cleanup/EXTRA.md", "Extra file.\n"), {"V11", "V21"}),
    ("file over 1 MiB under docs/cleanup/",
     append("docs/cleanup/README.md", "\n" + ("padding " * 140000) + "\n"), {"V23"}),
    ("archived MERGE-PLAN.md edited",
     append("docs/cleanup/MERGE-PLAN.md", "\nA later edit.\n"), {"V21"}),
    ("historical references inside docs/cleanup/ do not fail",
     append("docs/cleanup/README.md", HISTORICAL), set()),
    ("broken section reference in IMPLEMENTATION-NOTES.md",
     replace(NOTES, "(`OBJECTS.md §2.9`)", "(`OBJECTS.md §99`)"), {"V1"}),
    ("normative keyword in IMPLEMENTATION-NOTES.md",
     append(NOTES, "\n- An implementation MUST do something (`PROTOCOL.md §43`).\n"), {"V24"}),
    ("uncited statement in IMPLEMENTATION-NOTES.md",
     append(NOTES, "\n- A statement with no citation.\n"), {"V24"}),
    ("language named in IMPLEMENTATION-NOTES.md",
     append(NOTES, "\n- The core is written in Rust (`PROTOCOL.md §43`).\n"), {"V24"}),
    ("dangling document name in IMPLEMENTATION-NOTES.md",
     append(NOTES, "\n- See the Operator Guide (`PROTOCOL.md §43`).\n"), {"V17"}),
    ("new unsupported claim in spec/SECURITY.md",
     append("spec/SECURITY.md", "\nA new rate limit applies to pairing (`PAIRING_RATE_LIMIT`).\n"),
     {"V9", "V16", "V19"}),
    ("stale revision string",
     replace("spec/GLOSSARY.md", "**Revision:** 2.6", "**Revision:** 2.5"), {"V6"}),
    ("unexpected new file outside the manifest",
     create("operations/EXTRA-NOTES.md", "Extra file.\n"), {"V11"}),
    ("dollar figure added to a current document",
     append("design/LINEAGE.md", "\nAbout $5 a month.\n"), {"V27"}),
    ("superiority claim in a LINEAGE entry",
     replace("design/LINEAGE.md", "Grid has no certificate authority.",
             "Grid has no certificate authority and is better for it."), {"V25"}),
    ("existing LINEAGE entry edited",
     replace("design/LINEAGE.md", "The protocol is not novel in its parts.",
             "The protocol is novel in its parts."), {"V16"}),
    ("threshold recovery relabeled deferred",
     replace("spec/PROTOCOL.md", "Threshold recovery (planned) | Offline",
             "Threshold recovery (deferred) | Offline"), {"V26"}),
]


def run_case(name, mutate, must_fail):
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "work"
        subprocess.run(["git", "clone", "-q", str(ROOT), str(work)], check=True)
        mutate(work)
        subprocess.run(GIT + ["add", "-A"], cwd=work, check=True)
        if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=work).returncode != 0:
            subprocess.run(GIT + ["commit", "-q", "-m", "selftest"], cwd=work, check=True)
        p = subprocess.run([sys.executable, "tools/validate.py"], cwd=work, capture_output=True, text=True)
        failed = set(re.findall(r"^FAIL\s+(V\d+)", p.stdout, re.M))
    if must_fail:
        ok = must_fail <= failed and p.returncode == 1
        want = "must fail %s" % sorted(must_fail)
    else:
        ok = not failed and p.returncode == 0
        want = "must pass"
    print("%s  %s (%s; failed: %s)" % ("PASS" if ok else "FAIL", name, want, sorted(failed) or "none"))
    return ok


def main():
    status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True).stdout
    if status.strip():
        print("ERROR: the working tree is not clean. Commit or stash changes; the self-test uses HEAD.")
        return 2
    results = [run_case(*c) for c in CASES]
    print()
    print("%d of %d self-tests passed" % (sum(results), len(results)))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
