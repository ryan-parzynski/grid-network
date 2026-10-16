#!/usr/bin/env python3
"""Repository validation for the Grid Network specification.

Usage:
    python3 tools/validate.py

Run it from any directory inside a clone. It takes no arguments and reads
no environment variables. It needs only the Python 3 standard library and
the full git history of the repository (a normal clone; in CI use
fetch-depth: 0). Exit status is 0 only if every check passes.

Checks V1-V16 descend from the validation gate used for revisions 2.2 and
2.3. V17-V21 are added in revision 2.4. Nothing here changes the
specification; the script only reads the repository.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Commits this tool compares against. They are part of the repository history.
BASE_2_1 = "9898163"   # revision 2.1: the base of the revision 2.2 cleanup
REV_2_2 = "8527311"    # published revision 2.2 / protocol v0.6.3
REV_2_3 = "3d9cd36"    # published revision 2.3 (last revision before this tool)
REV_2_4 = "ccb0b1b"    # published revision 2.4 (this tool and its CI workflow)

# Files that may differ from BASE_2_1. Anything else is a scope violation.
ALLOWED_CHANGES = {
    "README.md", "REVISIONS.md", "ROADMAP.md", "LICENSE.md", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md",
    "commercial/MODEL.md", "design/DECISIONS.md", "design/EXTENSIONS.md", "design/LINEAGE.md",
    "design/RATIONALE.md", "design/REJECTED.md", "design/RULES.md", "operations/DEPLOYMENT.md",
    "operations/RELAYS.md", "operations/RENDEZVOUS.md", "spec/CONFORMANCE.md", "spec/GLOSSARY.md",
    "spec/OBJECTS.md", "spec/PARAMETERS.md", "spec/PITCHES.md", "spec/PROTOCOL.md", "spec/SECURITY.md",
    "spec/VERSIONING.md", "docs/FOLLOW-UPS.md",
    "tools/validate.py", "tools/README.md", ".github/workflows/ci.yml",
    # revision 2.5: historical audit archive and its self-test
    "docs/cleanup/MERGE-PLAN.md", "docs/cleanup/SECURITY-REVIEW.md",
    "docs/cleanup/EXECUTION-RECORD.md", "docs/cleanup/README.md", "tools/selftest.py",
}

# Historical audit archive. Files here keep retired version numbers, stale references and
# historical document names on purpose, so the checks that compare a document with the
# current specification skip them (V1, V3, V6, V16, V17, V18). The scope, content-pin,
# secret, local-path and file-size checks (V11, V21, V22, V23) still apply to them.
HISTORICAL_DIRS = ("docs/cleanup/",)


def historical(path):
    return path.startswith(HISTORICAL_DIRS)

# SHA-256 of archived files whose content must not change. A change to one of them is
# deliberate and needs this table updated in the same commit.
HISTORICAL_PINS = {
    "docs/cleanup/MERGE-PLAN.md": "5a4dacb3a7071158caa60b239fe5416a2719bd93d4001f66a68e23ca17b684fe",
    "docs/cleanup/SECURITY-REVIEW.md": "3551e14db6c1eb9b2b96c9473105e9f19bb4da59670ca44fea5e994d7040f21a",
    "docs/cleanup/EXECUTION-RECORD.md": "6bdec8419d2f54936a8f5a520ced18eb861eabeb2956cabf5ce7316a2bf80513",
}


# Prose names for documents that do not exist in this repository. Each use must
# be listed in ALLOWED_PROSE with the follow-up item that tracks it. The list is
# checked in both directions: an unlisted use fails, and a listed use that no
# longer occurs also fails, so the allowlist cannot go stale.
MISSING_DOCUMENTS = [
    r"Operator Guide", r"operator guide", r"Design Record", r"design record",
    r"THREAT-MODEL", r"Threat Model", r"Security Addendum", r"Master Archive",
    r"Detailed Reference Addendum", r"Design Defense Addendum",
]
# (file, phrase as written in the file, follow-up item that tracks it)
ALLOWED_PROSE = [
    ("spec/PROTOCOL.md", "Design Record", "7a"),
    ("spec/PROTOCOL.md", "Operator Guide", "7a"),
    ("spec/GLOSSARY.md", "Operator Guide", "7a"),
    ("design/RATIONALE.md", "Operator Guide", "7a"),
    ("design/RATIONALE.md", "operator guide", "7a"),
    ("design/RULES.md", "design record", "7a"),
    ("design/RULES.md", "operator guide", "7a"),
    ("LICENSE.md", "design record", "7a"),
    ("LICENSE.md", "operator guide", "7a"),
    ("CONTRIBUTING.md", "design record", "7a"),
    ("CONTRIBUTING.md", "operator guide", "7a"),
]
# Files that discuss missing or historical material on purpose.
PROSE_EXEMPT_FILES = {"REVISIONS.md", "docs/FOLLOW-UPS.md"}

# Quoted section titles that name no heading in the repository. Same two-way rule.
# (file, quoted title, follow-up item that tracks it)
ALLOWED_QUOTED = [
    ("ROADMAP.md", "Open decisions", "5"),
]


def git(*args, check=True):
    p = subprocess.run(["git", "-C", str(ROOT)] + list(args), capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), p.stderr.strip()))
    return p.stdout


def have(commit):
    return subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", commit + "^{commit}"],
                          capture_output=True).returncode == 0


def show(ref, path):
    return git("show", "%s:%s" % (ref, path))


for c in (BASE_2_1, REV_2_2, REV_2_3, REV_2_4):
    if not have(c):
        print("ERROR: commit %s is not in this clone. Fetch the full history "
              "(git fetch --unshallow, or fetch-depth: 0 in CI) and run again." % c)
        sys.exit(2)

tracked = set(git("ls-files").split("\n")) - {""}
files = sorted(f for f in tracked if f.endswith(".md"))
text = {f: (ROOT / f).read_text(encoding="utf-8") for f in files}
lines = {f: text[f].split("\n") for f in files}
fails = []
results = []
current_files = [f for f in files if not historical(f)]


def check(name, bad):
    results.append((name, not bad))
    if bad:
        fails.append(name)
        print("FAIL  %s" % name)
        for b in bad[:25]:
            print("        " + b)
        if len(bad) > 25:
            print("        ... %d more" % (len(bad) - 25))
    else:
        print("PASS  %s" % name)


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", re.sub(r"\s+", " ", s.lower())).strip()


# ---- headings index ----------------------------------------------------------------
def heads(f):
    s = set()
    for l in lines[f]:
        m = re.match(r"^#{1,4}\s+§?(\d+(?:\.\d+)*)\.?\s", l)
        if m:
            s.add(m.group(1))
    return s


H = {f: heads(f) for f in files}
DOCS = {
    "PROTOCOL": "spec/PROTOCOL.md", "Protocol": "spec/PROTOCOL.md", "OBJECTS": "spec/OBJECTS.md",
    "CONFORMANCE": "spec/CONFORMANCE.md", "DEPLOYMENT": "operations/DEPLOYMENT.md",
    "RELAYS": "operations/RELAYS.md", "RENDEZVOUS": "operations/RENDEZVOUS.md",
    "RATIONALE": "design/RATIONALE.md", "DECISIONS": "design/DECISIONS.md",
    "VERSIONING": "spec/VERSIONING.md", "PARAMETERS": "spec/PARAMETERS.md",
    "GLOSSARY": "spec/GLOSSARY.md", "MODEL": "commercial/MODEL.md",
    "EXTENSIONS": "design/EXTENSIONS.md", "ROADMAP": "ROADMAP.md", "SECURITY": "spec/SECURITY.md",
}
named = re.compile(r"(?:`?\[?(PROTOCOL|OBJECTS|CONFORMANCE|DEPLOYMENT|RELAYS|RENDEZVOUS|RATIONALE|DECISIONS|"
                   r"VERSIONING|PARAMETERS|GLOSSARY|MODEL|EXTENSIONS|ROADMAP|SECURITY)(?:\.md)?`?\]?|\bProtocol)"
                   r"\s+§\s?(\d+(?:\.\d+)*)")

# V1 ----------------------------------------------------------------------------------
bad = []
for f in current_files:
    for i, l in enumerate(lines[f], 1):
        for m in named.finditer(l):
            d = m.group(1) or "Protocol"
            sec = m.group(2)
            if f == "REVISIONS.md":
                continue  # append-only history; historical section numbers are not rewritten
            if sec not in H[DOCS[d]]:
                bad.append("%s:%d %s §%s has no heading in %s" % (f, i, d, sec, DOCS[d]))
        if f in ("spec/PROTOCOL.md", "spec/OBJECTS.md"):
            for m in re.finditer(r"(?<![\w`])§\s?(\d+(?:\.\d+)*)", l):
                pre = l[: m.start()]
                if re.search(r"(PROTOCOL|OBJECTS|Protocol|CONFORMANCE|DEPLOYMENT|RELAYS|RFC \d+|RFC)\S*\s*$", pre):
                    continue
                if "RFC" in l or (i > 1 and "RFC" in lines[f][i - 2]):
                    continue
                if m.group(1) not in H[f]:
                    bad.append("%s:%d bare §%s has no heading in %s" % (f, i, m.group(1), f))
check("V1  section references resolve (named, bracketed, and bare)", sorted(set(bad)))

# V2 ----------------------------------------------------------------------------------
bad = []
linkre = re.compile(r"\]\(([^)#\s]+)?(#[^)]*)?\)")
for f in files:
    for i, l in enumerate(lines[f], 1):
        for m in linkre.finditer(l):
            target = m.group(1)
            if target and not re.match(r"[a-z]+://", target):
                p = os.path.normpath(os.path.join(os.path.dirname(f), target))
                if not (ROOT / p).exists():
                    bad.append("%s:%d link to missing file %s" % (f, i, target))
for f in ("spec/SECURITY.md",):
    for i, l in enumerate(lines[f], 1):
        for m in re.finditer(r"`((?:spec|design|operations|commercial)/[A-Za-z_./-]+\.md)`", l):
            if m.group(1) not in tracked:
                bad.append("%s:%d names missing file %s" % (f, i, m.group(1)))
check("V2  markdown links and file references resolve", bad)

# V3 ----------------------------------------------------------------------------------
forb = ["stated threat model", "from a single branch", "See §33", "§8.5.3", "[RECORD", "[GUIDE"]
bad = []
for f in current_files:
    if f == "REVISIONS.md":
        continue
    for phrase in forb:
        if phrase in text[f]:
            bad.append("%s contains %r" % (f, phrase))
    if "grows linearly" in " ".join(text[f].split()):
        bad.append("%s contains 'grows linearly'" % f)
if "later sections" in text["spec/OBJECTS.md"]:
    bad.append("spec/OBJECTS.md still defers to 'later sections'")
if "Operator Guide" in text["spec/PARAMETERS.md"]:
    bad.append("spec/PARAMETERS.md still cites 'Operator Guide'")
check("V3  forbidden phrases absent", bad)

# V4 ----------------------------------------------------------------------------------
bad = []
for i, l in enumerate(lines["spec/PARAMETERS.md"], 1):
    m = re.match(r"\| `([A-Z_]+)` \|.*\| (`[a-z/]+\.md`|TODO[^|]*) \|$", l)
    if m and m.group(2).startswith("`"):
        path = m.group(2).strip("`")
        if path in ("commercial/MODEL.md", "operations/RELAYS.md"):
            if not re.search(r"\b%s\b" % m.group(1), text[path]):
                bad.append("PARAMETERS:%d %s not found in %s" % (i, m.group(1), path))
rows = [l for l in lines["spec/PARAMETERS.md"] if "TODO: no document defines this parameter" in l]
if len(rows) != 1 or "DEFAULT_REACHABILITY_CREDIT_REWARD" not in rows[0]:
    bad.append("expected exactly one TODO row for DEFAULT_REACHABILITY_CREDIT_REWARD")
check("V4  PARAMETERS redirects point at files that use each symbol", bad)

# V5 ----------------------------------------------------------------------------------
orig = show(BASE_2_1, "spec/PARAMETERS.md").split("\n")
now = lines["spec/PARAMETERS.md"]


def strip_defined(rows_):
    out = []
    for r in rows_:
        c = [x.strip() for x in r.split("|")]
        out.append(tuple(c[1:4]) if (r.startswith("| `") and len(c) >= 6) else None)
    return [x for x in out if x]


check("V5  PARAMETERS symbol, default, and meaning columns unchanged since revision 2.1",
      [] if strip_defined(orig) == strip_defined(now) else ["a Symbol, Default, or Meaning cell changed"])

# V6 ----------------------------------------------------------------------------------
rev = text["REVISIONS.md"]
entries = re.findall(r"^## Revision (\S+)", rev, re.M)
latest = entries[0] if entries else None
pv_m = re.search(r"current protocol version is (v\d+\.\d+\.\d+)", text["spec/VERSIONING.md"])
pv = pv_m.group(1) if pv_m else None
bad = []
if not latest or not pv:
    bad.append("cannot determine the current revision or protocol version")
else:
    hdr_re = re.compile(r"^\*\*(Document revision|Revision):\*\* (\S+)$", re.M)
    pv_re = re.compile(r"^\*\*Protocol version:\*\* (v\d+\.\d+\.\d+)", re.M)
    for f in current_files:
        if f == "REVISIONS.md":
            continue
        for m in hdr_re.finditer(text[f]):
            if m.group(2) != latest:
                bad.append("%s: revision header %s, expected %s" % (f, m.group(2), latest))
        for m in pv_re.finditer(text[f]):
            if m.group(1) != pv:
                bad.append("%s: protocol version %s, expected %s" % (f, m.group(1), pv))
        if f != "docs/FOLLOW-UPS.md" and re.search(r"v0\.6\.[0-2]\b", text[f]):
            bad.append("%s mentions a retired protocol version" % f)
        for i, l in enumerate(lines[f], 1):
            m = re.search(r"(?:current (?:document is )?revision is|current document is revision) (\d+\.\d+)", l)
            if m and m.group(1) != latest:
                bad.append("%s:%d stale current-revision statement %s" % (f, i, m.group(1)))
    if not re.search(r"current revision is %s\b" % re.escape(latest), " ".join(text["spec/VERSIONING.md"].split())):
        bad.append("spec/VERSIONING.md does not state that the current revision is %s" % latest)
    if "revision %s" % latest not in " ".join(text["spec/PROTOCOL.md"].split()):
        bad.append("spec/PROTOCOL.md section 45 does not state revision %s" % latest)
check("V6  version strings consistent (revision %s, protocol %s, taken from REVISIONS.md and VERSIONING.md)"
      % (latest, pv), bad)

# V7 ----------------------------------------------------------------------------------
bad = []
if entries[:4] != ["2.4", "2.3", "2.2", "2.1"] and entries[1:5] != ["2.4", "2.3", "2.2", "2.1"]:
    bad.append("entries are not ordered newest first with 2.4, 2.3, 2.2, 2.1 contiguous: %s" % entries[:6])
if "historical" not in rev.split("## Revision 2.1")[0].split("## Revision 2.2")[1]:
    bad.append("the 2.2 entry does not mark the 2.1 stability list historical")
actual = []
cur = None
for l in lines["spec/PROTOCOL.md"]:
    m = re.match(r"^## (\d+)\.", l)
    if m:
        cur = m.group(1)
    m2 = re.match(r"<!-- stability: (stable|under-review) -->", l)
    if m2:
        actual.append((m2.group(1), cur))
stable = sorted(int(c) for s, c in actual if s == "stable")
review = sorted(int(c) for s, c in actual if s == "under-review")
newest_entry = rev.split("\n## Revision ")[1] if "\n## Revision " in rev else ""


def listed(label):
    m = re.search(label + r":\n- Protocol ([^\n]+)\n", newest_entry)
    return sorted(int(x) for x in re.findall(r"§(\d+)", m.group(1))) if m else None


if listed("Stable") != stable:
    bad.append("newest entry Stable list %s != markers %s" % (listed("Stable"), stable))
if listed("Under review") != review:
    bad.append("newest entry Under review list %s != markers %s" % (listed("Under review"), review))
if len(actual) != 5:
    bad.append("expected 5 stability markers in PROTOCOL.md, found %d" % len(actual))
for f in files:
    if f != "spec/PROTOCOL.md" and "<!-- stability:" in text[f]:
        bad.append("%s unexpectedly carries a stability marker" % f)
old_rev = show(REV_2_4, "REVISIONS.md")
_head, _tail = old_rev.split("## Revision 2.4\n", 1)
if not (rev.startswith(_head) and rev.endswith("## Revision 2.4\n" + _tail)):
    bad.append("entries for revision 2.4 and earlier, or the introduction, were altered (append-only rule)")
check("V7  REVISIONS: newest first, history byte-preserved, markers match files, 2.1 list marked historical", bad)

# V8 ----------------------------------------------------------------------------------
bad = []
o = " ".join(text["spec/OBJECTS.md"].split())
d = " ".join(text["design/DECISIONS.md"].split())
for needle in ("the signature binds an object to the specific history that precedes it",
               "does not by itself reveal a fork"):
    if needle not in o:
        bad.append("OBJECTS §3.8 missing: " + needle)
for needle in ("an object cannot be moved onto a different history without invalidating its signature",
               "per-object computation cost is constant",
               "does not reveal a fork to a verifier that has seen only one branch"):
    if needle not in d:
        bad.append("DECISIONS D5 missing: " + needle)
check("V8  chain-hash wording corrected in OBJECTS §3.8 and DECISIONS D5", bad)

# V9 ----------------------------------------------------------------------------------
bad = []
sec = text["spec/SECURITY.md"]
sl = lines["spec/SECURITY.md"]
if sl[0] != "# Grid Network — Security Model":
    bad.append("title line")
if sl[2:4] != ["**Revision:** %s" % latest, "**Protocol version:** %s" % pv]:
    bad.append("header lines")
if "**Repository path:** `spec/SECURITY.md`" not in sec:
    bad.append("repository path line")
if "This document is non-normative." not in sec:
    bad.append("non-normative statement")
for m in re.finditer(r"\b(MUST|MUST NOT|SHALL|SHOULD|SHOULD NOT|MAY|REQUIRED)\b", sec):
    bad.append("normative keyword %r" % m.group(1))
for pat, why in ((r"\bMesh\b|mesh/", "old project name"), (r"v0\.6\.[0-2]\b", "old version"),
                 (r"\$\s?\d", "dollar figure"),
                 (r"\b\d+\s?(ms|seconds?|minutes?|hours?|days?|Mbps|Gbps|MB|GB|%)\b", "literal figure"),
                 (r"Time to recovery|social recovery|timezone|time zone", "excluded content"),
                 (r"[Bb]itcoin|proof-of-work admission|relay hardware", "excluded content")):
    for m in re.finditer(pat, sec):
        bad.append("%s: %r" % (why, m.group(0)))
params = set(re.findall(r"^\| `([A-Z][A-Z0-9_]+)` \|", text["spec/PARAMETERS.md"], re.M))
for sym in set(re.findall(r"`((?:MAX|MIN|DEFAULT|PAIRING|CREDIT|GEOGRAPHIC)_[A-Z0-9_]+)`", sec)):
    if sym not in params:
        bad.append("symbol %s not in PARAMETERS.md" % sym)
if "provides no in-band" not in " ".join(sec.split()):
    bad.append("Identity Root section must state no in-band recovery (PROTOCOL §18)")
for want in ("`PROTOCOL.md §18`", "`design/REJECTED.md` R5", "`PROTOCOL.md §43`", "`OBJECTS.md §3.8`"):
    if want not in sec:
        bad.append("missing citation " + want)
check("V9  SECURITY.md: header, non-normative, no figures or keywords, symbols exist, consistent with §18 and R5", bad)

# V10 ---------------------------------------------------------------------------------
bad = []
if "SECURITY.md" not in text["README.md"]:
    bad.append("README layout does not list SECURITY.md")
if "`SECURITY.md`" not in text["spec/PROTOCOL.md"] or "`SECURITY.md`" not in text["design/RATIONALE.md"]:
    bad.append("PROTOCOL §44 or RATIONALE §9 does not cite SECURITY.md")
check("V10 SECURITY.md is wired into README, PROTOCOL §44, RATIONALE §9", bad)

# V11 ---------------------------------------------------------------------------------
changed = set(git("diff", "--name-only", BASE_2_1, "HEAD").split())
extra = sorted(changed - ALLOWED_CHANGES)
untracked = git("ls-files", "--others", "--exclude-standard").split()
dirty = [l for l in git("status", "--porcelain").split("\n") if l and not l.startswith("??")]
check("V11 only allowed files changed since revision 2.1; no untracked or uncommitted changes",
      ["unexpected: " + e for e in extra] + ["untracked: " + u for u in untracked]
      + ["uncommitted: " + x for x in dirty])

# V12 ---------------------------------------------------------------------------------
check("V12 decision and rejection counts unchanged (38 and 17)",
      [] if (len(re.findall(r"^## D\d+\.", text["design/DECISIONS.md"], re.M)) == 38 and
             len(re.findall(r"^## R\d+\.", text["design/REJECTED.md"], re.M)) == 17)
      else ["decision/rejection count changed"])

# V13 ---------------------------------------------------------------------------------
bad = []
rat = text["design/RATIONALE.md"]
guide = rat.split("## 1. Purpose and reading guide")[1].split("\n## 2. ")[0]
flat = " ".join(guide.split())
for want in ("Sections 2 through 4 address that.", "Sections 5 and 6 address that.",
             "edge cases in Section 7 and a question index in Section 7.9."):
    if want not in flat:
        bad.append("reading guide missing: " + want)
for stale in ("Sections 2 through 5", "Sections 6 and 7", "Section 8", "Section 9"):
    if stale in flat:
        bad.append("stale reference remains: " + stale)
titles = {}
for l in lines["design/RATIONALE.md"]:
    m = re.match(r"^#{2,3}\s+(\d+(?:\.\d+)*)\.?\s+(.*)$", l)
    if m:
        titles[m.group(1)] = m.group(2)
for sec_no, kw in (("2", "problem"), ("3", "solution"), ("4", "matters"), ("5", "developer"),
                   ("6", "contribution"), ("7", "Edge cases"), ("7.9", "FAQ")):
    if sec_no not in titles or kw.lower() not in titles[sec_no].lower():
        bad.append("RATIONALE section %s is %r, expected title containing %r" % (sec_no, titles.get(sec_no), kw))
for ref in re.findall(r"Sections? (\d+(?:\.\d+)?)", flat):
    if ref not in titles:
        bad.append("reading guide cites section %s which does not exist" % ref)
check("V13 RATIONALE section 1 reading guide cites real, correctly titled sections", bad)

# V14 ---------------------------------------------------------------------------------
bad = []
pro = text["spec/PROTOCOL.md"]
if "Continued from Part 1" in pro:
    bad.append("stray 'Continued from Part 1' line still present")
if len(re.findall(r"^\*\*Revision:\*\*", pro, re.M)) != 1 or len(re.findall(r"^\*\*Protocol version:\*\*", pro, re.M)) != 1:
    bad.append("PROTOCOL.md must carry exactly one Revision and one Protocol version header line")
if pro.count("the relationship assertion is.\n\n---\n\n## 21. Pairing") != 1:
    bad.append("transition from section 20 to section 21 is not the standard separator")
base_pro = show(BASE_2_1, "spec/PROTOCOL.md")


def body(t, a, b):
    return t.split(a)[1].split(b)[0]


for a, b in (("## 21. Pairing", "\n## 22. "), ("## 22. Grid URI", "\n## 23. ")):
    if body(base_pro, a, b) != body(pro, a, b):
        bad.append("content of %r changed" % a)
if [l for l in base_pro.split("\n") if re.match(r"^## \d+\.", l)] != [l for l in pro.split("\n") if re.match(r"^## \d+\.", l)]:
    bad.append("section heading list of PROTOCOL.md changed")
check("V14 stray revision block removed; PROTOCOL section 21 and surroundings intact", bad)

# V15 ---------------------------------------------------------------------------------
# Coverage data that earlier revisions took from a working file is embedded here.
# Each entry: item id in the FOLLOW-UPS summary table -> tokens its text must contain.
COVERAGE = {
    "1a": ["G6", "design/EXTENSIONS.md"],
    "1b": ["G7", "design/RATIONALE.md"],
    "1c": ["G8", "design/DECISIONS.md", "design/REJECTED.md"],
    "1d": ["G9", "spec/PITCHES.md"],
    "1e": ["G10"],
    "1f": ["G11"],
    "1g": ["Level 6", "spec/SECURITY.md"],
    "2": ["Appendix C", "b5e8be7", "MAPPED", "CONDENSED", "MISSING"],
    "3": ["DEFAULT_REACHABILITY_CREDIT_REWARD", "spec/PARAMETERS.md"],
    "3b": ["PAIRING_MAX_ATTEMPTS", "spec/PARAMETERS.md", "spec/PROTOCOL.md"],
    "4": ["OBJECTS.md §10", "test vectors", "conformance"],
    "5": ["Appendix B", "active session", "lease renewal", "relationship decay"],
    "6": ["Security Addendum", "spec/SECURITY.md"],
    "6b": ["evidence", "consolidated archive", "Security Addendum"],
    "7a": ["Operator Guide", "Design Record", "PROTOCOL.md", "GLOSSARY.md", "RATIONALE.md", "RULES.md", "LICENSE.md"],
    "7b": ["conventions list", "PROTOCOL.md"],
    "8": ["README.md", "CONFORMANCE.md", "PITCHES.md", "RULES.md", "RENDEZVOUS.md",
          "ROADMAP.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "LICENSE.md"],
    "9": ["v0.6.3", "v0.6.2", "normative", "Revision 2.2", "REVISIONS.md"],
    "10": ["PROTOCOL.md §6", "PROTOCOL.md §16", "OBJECTS.md §8.2", "PARAMETERS.md", "FORKED"],
}
bad = []
FU = "docs/FOLLOW-UPS.md"
if FU not in files:
    bad.append("%s does not exist" % FU)
else:
    fu = text[FU]
    fl = fu.lower()
    lay = text["README.md"].split("## Repository layout")[1].split("\n---")[0]
    if "FOLLOW-UPS.md" not in lay or "docs/" not in lay:
        bad.append("README layout list does not include docs/ and FOLLOW-UPS.md")
    if lines[FU][2:4] != ["**Revision:** %s" % latest, "**Protocol version:** %s" % pv]:
        bad.append("header lines")
    if "This document is non-normative." not in fu:
        bad.append("missing non-normative statement")
    expect = [("1.", "Archive gap merges"), ("2.", "Appendix C"), ("3.", "DEFAULT_REACHABILITY_CREDIT_REWARD"),
              ("4.", "OBJECTS.md"), ("5.", "Appendix B"), ("6.", "Security Addendum"),
              ("7.", "document names"), ("8.", "README"), ("9.", "v0.6.3"),
              ("10.", "inconsistenc")]
    secs = {}
    cur = None
    for l in lines[FU]:
        m = re.match(r"^## (\d+)\. (.*)$", l)
        if m:
            cur = m.group(1) + "."
            secs[cur] = [m.group(2), ""]
        elif l.startswith("## "):
            cur = None
        elif cur:
            secs[cur][1] += l + "\n"
    for num, kw in expect:
        if num not in secs or kw.lower() not in secs[num][0].lower():
            bad.append("section %s missing or mis-titled (want %r)" % (num, kw))
        elif "Needs decision" not in secs[num][1] and "Needs implementation" not in secs[num][1]:
            bad.append("section %s has no Needs decision / Needs implementation status" % num)
    hdr = [l for l in lines[FU] if l.startswith("| Item |")]
    if not hdr or [c.strip() for c in hdr[0].strip("|").split("|")] != [
            "Item", "Priority", "Scope", "Dependency or precondition", "Suggested approach", "Source and evidence"]:
        bad.append("summary table columns are not exactly: item, priority, scope, dependency/precondition, "
                   "suggested approach, source/evidence")
    rows = [l for l in lines[FU] if re.match(r"^\| \d+[a-g]?\. ", l)]
    ids = []
    for r in rows:
        cells = [c.strip() for c in r.strip("|").split("|")]
        ids.append(cells[0].split(".")[0])
        if len(cells) != 6 or any(not c for c in cells) or cells[1] not in ("High", "Medium", "Low"):
            bad.append("malformed summary row: " + r[:60])
    if sorted(ids) != sorted(COVERAGE):
        bad.append("summary table items %s differ from the required coverage list %s" % (sorted(ids), sorted(COVERAGE)))
    # every required item's tokens appear somewhere in the document
    for item, toks in COVERAGE.items():
        for tok in toks:
            if tok.lower() not in fl:
                bad.append("item %s: token %r not in FOLLOW-UPS.md" % (item, tok))
    # every reference resolves, or is marked historical or unavailable
    marker = re.compile(r"historical|unavailable|not in this repository|archive", re.I)
    blocks = []
    cur_b = []
    for l in lines[FU]:
        if l.startswith("|"):
            if cur_b:
                blocks.append("\n".join(cur_b))
                cur_b = []
            blocks.append(l)
        elif l.strip() == "":
            if cur_b:
                blocks.append("\n".join(cur_b))
                cur_b = []
        else:
            cur_b.append(l)
    if cur_b:
        blocks.append("\n".join(cur_b))
    by_base = {}
    for t in tracked:
        by_base.setdefault(os.path.basename(t), []).append(t)
    for blk in blocks:
        flat_b = " ".join(blk.split())
        marked = bool(marker.search(flat_b))
        for tok in re.findall(r"`([^`]+)`", blk):
            t = tok.strip()
            m = re.match(r"^([A-Za-z0-9_./*-]+\.(?:md|json))(?:\s+§(\d+(?:\.\d+)*))?$", t)
            if m:
                path, secn = m.group(1), m.group(2)
                cand = [path] if path in tracked else by_base.get(path, [])
                if "*" in path:
                    continue
                if len(cand) == 1:
                    if secn and secn not in H.get(cand[0], set()):
                        bad.append("%s §%s has no heading" % (cand[0], secn))
                elif not marked:
                    bad.append("unresolved file reference %r without historical/unavailable marker" % t)
                continue
            if re.match(r"^[0-9a-f]{7,40}$", t):
                if not have(t) and not marked:
                    bad.append("commit %s does not resolve and is not marked historical" % t)
                continue
            if re.match(r"^[A-Z][A-Z0-9_]{5,}$", t):
                if t not in text["spec/PARAMETERS.md"]:
                    bad.append("symbol %s not in PARAMETERS.md" % t)
                continue
            m = re.match(r"^(spec|design|operations|commercial|docs)/[A-Za-z0-9_./-]+$", t)
            if m and t not in tracked and not marked:
                bad.append("unresolved path %r without marker" % t)
        for ident in re.findall(r"\b(D\d+|R\d+)\b", flat_b):
            f2 = "design/DECISIONS.md" if ident[0] == "D" else "design/REJECTED.md"
            if not re.search(r"^## %s\." % ident, text[f2], re.M):
                if ident in ("D39", "R18"):
                    continue  # next free numbers, stated as such
                bad.append("%s is not a heading in %s" % (ident, f2))
        if re.search(r"Appendix [A-Z]|Addendum|Master Archive", flat_b) and not marked and not flat_b.startswith("#"):
            bad.append("archive reference without a historical/archive marker: " + flat_b[:70])
    intro = fu.split("## Summary")[0]
    if "historical" not in intro or "not in this repository" not in " ".join(intro.split()):
        bad.append("introduction must state that historical sources are not in this repository")
check("V15 docs/FOLLOW-UPS.md covers the required items, references resolve or are marked historical", bad)

# V16 ---------------------------------------------------------------------------------
bad = []
m_new = re.search(r"^## Revision %s\n.*?(?=^## Revision )" % re.escape(latest or "?"), rev, re.M | re.S)
if not m_new:
    bad.append("no entry for revision %s" % latest)
else:
    e = m_new.group(0)
    fe = " ".join(e.split())
    for want in ("**Protocol version:** %s" % pv, "**Normative changes.**", "Stable:", "Under review:",
                 "**Open questions.**", "**Applied changes.**"):
        if want not in fe:
            bad.append("entry %s is missing %r (VERSIONING.md, Changelog)" % (latest, want))
    for nm in re.findall(r"`([^`]+\.(?:md|py|yml))`", e):
        if "/" in nm and nm not in tracked:
            bad.append("entry %s names a path that does not exist: %s" % (latest, nm))
    if latest == "2.4":
        for want in ("(unchanged)", "**Normative changes.** None.", "`tools/validate.py`",
                     "`.github/workflows/ci.yml`", "`spec/SECURITY.md`", "`docs/FOLLOW-UPS.md`"):
            if want not in fe:
                bad.append("2.4 entry missing: " + want)
    if latest == "2.5":
        for want in ("(unchanged)", "**Normative changes.** None.", "`docs/cleanup/`", "`tools/validate.py`",
                     "`tools/selftest.py`", "`README.md`", "`docs/FOLLOW-UPS.md`", "historical"):
            if want not in fe:
                bad.append("2.5 entry missing: " + want)
ch = [c.split("\t") for c in git("diff", "--name-status", REV_2_3, "HEAD").split("\n") if c]
if latest == "2.4":
    added = sorted(p for s_, p in ch if s_ == "A")
    if added != [".github/workflows/ci.yml", "tools/README.md", "tools/validate.py"]:
        bad.append("files added since 2.3 are %s; the 2.4 entry describes tools/validate.py, tools/README.md, "
                   ".github/workflows/ci.yml" % added)
    revre = re.compile(r"^(\*\*(Document revision|Revision):\*\* \d\.\d|  \d\.\d\)\. It advances whenever the document changes\.|"
                       r"`2\.0`, `2\.1`, `2\.2`, and so on\. The current document is revision \d\.\d\.|revision is \d\.\d\.)$")
    allowed_substance = {"REVISIONS.md", "spec/SECURITY.md", "docs/FOLLOW-UPS.md", "README.md"}
    for s_, p in ch:
        if s_ != "M" or p in allowed_substance:
            continue
        d_ = git("diff", "-U0", REV_2_3, "HEAD", "--", p).split("\n")
        b_ = [l[1:] for l in d_ if l and l[0] in "+-" and not l.startswith(("+++", "---"))]
        non_hdr = [l for l in b_ if l and not revre.match(l)]
        if non_hdr:
            bad.append("%s changed beyond revision strings: %r" % (p, non_hdr[0][:60]))
    d_ = git("diff", "-U0", REV_2_3, "HEAD", "--", "README.md").split("\n")
    b_ = [l[1:] for l in d_ if l and l[0] in "+-" and not l.startswith(("+++", "---"))]
    if [l for l in b_ if l and not revre.match(l)]:
        bad.append("README.md changed beyond revision strings")
    pv_diff = git("diff", "-U0", REV_2_3, "HEAD")
    if re.search(r"^-\*\*Protocol version:\*\*", pv_diff, re.M):
        bad.append("a protocol-version line changed; revision 2.4 states it is unchanged")
    if listed("Stable") != [23, 25, 39] or listed("Under review") != [21, 27]:
        bad.append("2.4 stability lists differ from the five markers")
if latest == "2.5":
    ch5 = [c.split("\t") for c in git("diff", "--name-status", REV_2_4, "HEAD").split("\n") if c]
    added5 = sorted(p for s_, p in ch5 if s_ == "A")
    want_added = sorted(["docs/cleanup/EXECUTION-RECORD.md", "docs/cleanup/MERGE-PLAN.md", "docs/cleanup/README.md",
                         "docs/cleanup/SECURITY-REVIEW.md", "tools/selftest.py"])
    if added5 != want_added:
        bad.append("files added since 2.4 are %s; the 2.5 entry describes %s" % (added5, want_added))
    if [p for s_, p in ch5 if s_ not in ("A", "M")]:
        bad.append("files were deleted or renamed since 2.4")
    revre5 = re.compile(r"^(\*\*(Document revision|Revision):\*\* \d\.\d|  \d\.\d\)\. It advances whenever the document changes\.|"
                        r"`2\.0`, `2\.1`, `2\.2`, and so on\. The current document is revision \d\.\d\.|revision is \d\.\d\.)$")

    def changed_lines(path):
        d_ = git("diff", "-U0", REV_2_4, "HEAD", "--", path).split("\n")
        return [l for l in d_ if l and l[0] in "+-" and not l.startswith(("+++", "---"))]

    tooling5 = {"REVISIONS.md", "tools/validate.py", "tools/README.md"}
    for s_, p in ch5:
        if s_ != "M" or p in tooling5 or p in ("README.md", "docs/FOLLOW-UPS.md"):
            continue
        extra5 = [l for l in changed_lines(p) if not revre5.match(l[1:])]
        if extra5:
            bad.append("%s changed beyond revision strings: %r" % (p, extra5[0][:60]))
    readme_new = {"", "    docs/cleanup/   Audit record for the revision 2.2 to 2.4 cleanup",
                  "      README.md           Guide to the audit record",
                  "      MERGE-PLAN.md       Historical merge plan for revision 2.2",
                  "      SECURITY-REVIEW.md  Traceability review of SECURITY.md",
                  "      EXECUTION-RECORD.md Summary of what was applied and pushed"}
    fu_new = {"", "**Audit record.** The cleanup review, merge plan, and execution summary",
              "are preserved under `docs/cleanup/`. The merge plan is historical and may",
              "refer to scratchpad paths and states that no longer exist. This register",
              "remains the list of open items."}
    for path_, allowed_ in (("README.md", readme_new), ("docs/FOLLOW-UPS.md", fu_new)):
        for l in changed_lines(path_):
            if revre5.match(l[1:]):
                continue
            if l[0] == "-" or l[1:] not in allowed_:
                bad.append("%s: unexpected change %r" % (path_, l[:70]))
    if re.search(r"^-\*\*Protocol version:\*\*", git("diff", "-U0", REV_2_4, "HEAD"), re.M):
        bad.append("a protocol-version line changed; revision 2.5 states it is unchanged")
    if listed("Stable") != [23, 25, 39] or listed("Under review") != [21, 27]:
        bad.append("2.5 stability lists differ from the five markers")
check("V16 newest revision entry is complete and matches the actual changes; protocol version unchanged", bad)

# V17 ---------------------------------------------------------------------------------
bad = []
seen = set()
for f in current_files:
    if f in PROSE_EXEMPT_FILES:
        continue
    flat_f = " ".join(text[f].split())
    for pat in MISSING_DOCUMENTS:
        for m in re.finditer(pat, flat_f):
            phrase = m.group(0)
            key = (f, phrase)
            seen.add(key)
            if not any(a == f and b == phrase for a, b, _ in ALLOWED_PROSE):
                bad.append("%s: prose reference to a document that does not exist: %r" % (f, phrase))
for f, phrase, item in ALLOWED_PROSE:
    if (f, phrase) not in seen:
        bad.append("allowlist entry is stale (no longer in %s): %r (follow-up %s)" % (f, phrase, item))
    elif not re.search(r"^\| %s[a-g]?\. " % re.escape(item), text["docs/FOLLOW-UPS.md"], re.M):
        bad.append("allowlist entry for %s %r names follow-up %s, which is not in docs/FOLLOW-UPS.md" % (f, phrase, item))
check("V17 prose references to documents that do not exist are tracked in docs/FOLLOW-UPS.md", bad)

# V18 ---------------------------------------------------------------------------------
bad = []
heading_titles = set()
for f in files:
    for l in lines[f]:
        m = re.match(r"^#{1,6}\s+(?:§?\d+(?:\.\d+)*\.?\s+)?(.*)$", l)
        if m:
            heading_titles.add(norm(m.group(1)))
cue = re.compile(r"\b(?:under|section|sections|heading|titled|called|named|see|in)\s+(?:the\s+)?[\"“]([A-Z][^\"”]{2,60})[\"”]")
seen_q = set()
for f in current_files:
    if f in PROSE_EXEMPT_FILES:
        continue
    for para in re.split(r"\n\s*\n", text[f]):
        flat_p = " ".join(para.split())
        for m in cue.finditer(flat_p):
            title = m.group(1).rstrip(".,;:")
            if norm(title) in heading_titles:
                continue
            seen_q.add((f, title))
            if not any(a == f and norm(b) == norm(title) for a, b, _ in ALLOWED_QUOTED):
                bad.append("%s: quoted section title %r matches no heading in the repository" % (f, title))
for f, title, item in ALLOWED_QUOTED:
    if not any(a == f and norm(b) == norm(title) for a, b in seen_q):
        bad.append("quoted-title allowlist entry is stale: %s %r (follow-up %s)" % (f, title, item))
    elif not re.search(r"^\| %s[a-g]?\. " % re.escape(item), text["docs/FOLLOW-UPS.md"], re.M):
        bad.append("quoted-title allowlist entry %s %r names follow-up %s, which is not in docs/FOLLOW-UPS.md"
                   % (f, title, item))
check("V18 quoted section-title references resolve to a heading, or are tracked in docs/FOLLOW-UPS.md", bad)

# V19 ---------------------------------------------------------------------------------
# SECURITY.md traceability: every citation resolves, every parameter is defined, and the
# claims corrected in revision 2.4 stay corrected.
bad = []
sec = text["spec/SECURITY.md"]
for m in re.finditer(r"`design/REJECTED\.md` (R\d+)", sec):
    if not re.search(r"^## %s\." % m.group(1), text["design/REJECTED.md"], re.M):
        bad.append("SECURITY.md cites %s, which is not a heading in design/REJECTED.md" % m.group(1))
for m in re.finditer(r"`([A-Za-z/]+\.md) §(\d+(?:\.\d+)*)`", sec):
    doc = m.group(1)
    cand = [t for t in tracked if t == doc or t.endswith("/" + doc)]
    if len(cand) != 1:
        bad.append("SECURITY.md cites %s, which does not resolve to one file" % doc)
    elif m.group(2) not in H[cand[0]]:
        bad.append("SECURITY.md cites %s §%s, which has no heading" % (doc, m.group(2)))
_pp = re.split(r"(?m)^(#{2,4}) (\d+(?:\.\d+)*)\.? .*$", text["spec/PROTOCOL.md"])
_secbody = {_pp[i + 1]: _pp[i + 2] for i in range(1, len(_pp), 3)}


def protocol_section(n):
    """Text of PROTOCOL section n, including its subsections."""
    return "".join(b for k, b in _secbody.items() if k == n or k.startswith(n + "."))


for sym in sorted(set(re.findall(r"`([A-Z][A-Z0-9_]{5,})`", sec))):
    if sym == "FORK_DETECTED":
        continue  # a stream state defined in OBJECTS.md §9.3, not a parameter
    rowm = re.search(r"^\| `%s` \|.*$" % re.escape(sym), text["spec/PARAMETERS.md"], re.M)
    if not rowm:
        bad.append("SECURITY.md names %s, which PARAMETERS.md does not define" % sym)
        continue
    cell = [c.strip() for c in rowm.group(0).strip("|").split("|")][-1]
    cm = re.match(r"Protocol §(\d+(?:\.\d+)*)", cell)
    if cm and sym not in protocol_section(cm.group(1)):
        bad.append("SECURITY.md cites %s, but its PARAMETERS.md 'Defined in' cell (Protocol §%s) does not state it"
                   % (sym, cm.group(1)))
flat_s = " ".join(sec.split())
if "attempts are limited (`PROTOCOL.md §20`, `PROTOCOL.md §21`)" in flat_s:
    bad.append("SECURITY.md still attributes a pairing attempt limit to PROTOCOL §20/§21")
check("V19 SECURITY.md citations resolve, cited parameters are defined, and corrected claims stay corrected", bad)

# V20 ---------------------------------------------------------------------------------
bad = []
wf = ROOT / ".github" / "workflows" / "ci.yml"
if not wf.is_file():
    bad.append(".github/workflows/ci.yml is missing")
else:
    y = wf.read_text(encoding="utf-8")
    if "\t" in y:
        bad.append("workflow contains a tab character")
    for want, why in ((r"^name: CI\s*$", "name: CI"), (r"^on:\s*$", "on: block"),
                      (r"^\s+push:\s*$", "push trigger"), (r"^\s+branches: \[main\]\s*$", "push to main only"),
                      (r"^\s+pull_request:\s*$", "pull_request trigger"),
                      (r"run: python3 tools/validate\.py\s*$", "run: python3 tools/validate.py")):
        if not re.search(want, y, re.M):
            bad.append("workflow missing " + why)
    for forbidden in ("secrets.", "deploy", "publish", "upload-artifact", "pip install"):
        if forbidden in y:
            bad.append("workflow must not contain %r" % forbidden)
    try:
        import yaml  # optional; used only when installed
        doc = yaml.safe_load(y)
        trig = doc.get(True, doc.get("on"))
        if doc.get("name") != "CI" or "pull_request" not in trig or trig["push"]["branches"] != ["main"]:
            bad.append("workflow YAML parsed but does not match the required triggers")
    except ImportError:
        pass
    except Exception as ex:  # noqa: BLE001
        bad.append("workflow YAML does not parse: %s" % ex)
rd = ROOT / "tools" / "README.md"
if not rd.is_file() or "python3 tools/validate.py" not in rd.read_text(encoding="utf-8"):
    bad.append("tools/README.md must show: python3 tools/validate.py")
check("V20 CI workflow and tools/README.md are present and valid", bad)

# V21 ---------------------------------------------------------------------------------
# The historical archive: exactly its four files, content pinned, wired into README and FOLLOW-UPS.
import hashlib
bad = []
need = ["docs/cleanup/README.md", "docs/cleanup/MERGE-PLAN.md", "docs/cleanup/SECURITY-REVIEW.md",
        "docs/cleanup/EXECUTION-RECORD.md"]
under = sorted(f for f in tracked if historical(f))
if under != sorted(need):
    bad.append("files under docs/cleanup/ are %s; expected exactly %s" % (under, sorted(need)))
for f, want in HISTORICAL_PINS.items():
    if f in tracked and hashlib.sha256((ROOT / f).read_bytes()).hexdigest() != want:
        bad.append("%s differs from its pinned content; archived files are not edited" % f)
if "docs/cleanup/README.md" in text:
    flat_c = " ".join(text["docs/cleanup/README.md"].split())
    for want in ("is a historical audit archive", "must not be treated as current normative documentation",
                 "source of truth remains the files outside `docs/cleanup/`", "`tools/validate.py`",
                 "`docs/FOLLOW-UPS.md`"):
        if want not in flat_c:
            bad.append("docs/cleanup/README.md must state: " + want)
if "docs/cleanup/" not in text["README.md"].split("## Repository layout")[1].split("\n---")[0]:
    bad.append("README.md layout list does not include docs/cleanup/")
if "**Audit record.**" not in text["docs/FOLLOW-UPS.md"] or "`docs/cleanup/`" not in text["docs/FOLLOW-UPS.md"]:
    bad.append("docs/FOLLOW-UPS.md does not carry the audit record note")
check("V21 docs/cleanup/ holds exactly its four archived files, content pinned, and is wired into README and FOLLOW-UPS", bad)

# V22 ---------------------------------------------------------------------------------
# Credentials, local paths and private URLs. Applies to every tracked file, including
# docs/cleanup/. Only this script is skipped, because it contains the patterns.
SECRET_PATTERNS = [
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key block"),
    (r"\bAKIA[0-9A-Z]{16}\b", "AWS access key id"),
    (r"\bgh[pousr]_[A-Za-z0-9]{30,}\b", "GitHub token"),
    (r"\bgithub_pat_[A-Za-z0-9_]{20,}\b", "GitHub token"),
    (r"\bxox[abprs]-[A-Za-z0-9-]{10,}", "Slack token"),
    (r"\bsk-[A-Za-z0-9_-]{20,}\b", "API key"),
    (r"(?i)\b(?:api[_-]?key|secret|token|passwd|password)\b\s*[:=]\s*['\"]?[A-Za-z0-9+/_\-]{16,}", "credential assignment"),
    (r"://[^/\s:@]+:[^/\s@]+@", "credentials in a URL"),
    (r"(?i)\bbearer\s+[A-Za-z0-9._\-]{20,}", "bearer token"),
    (r"(?<![\w.])/(?:home|Users|root)/[A-Za-z0-9._-]+", "local home path"),
    (r"/tmp/claude", "local scratch path"),
    (r"[A-Za-z]:\\Users\\", "local Windows path"),
    (r"/var/folders/", "local temp path"),
    (r"https?://claude\.ai/(?:code|chat|artifact|project)/", "private claude.ai URL"),
    (r"https?://(?:localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+)", "private network URL"),
]
bad = []
for f in sorted(tracked):
    if f == "tools/validate.py":
        continue
    try:
        body_ = (ROOT / f).read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        bad.append("%s is not readable as UTF-8 text" % f)
        continue
    for pat, why in SECRET_PATTERNS:
        for m in re.finditer(pat, body_):
            bad.append("%s:%d %s: %r" % (f, body_.count("\n", 0, m.start()) + 1, why, m.group(0)[:20] + "..."))
check("V22 no credentials, local paths or private URLs in any tracked file (docs/cleanup/ included)", bad)

# V23 ---------------------------------------------------------------------------------
LIMIT = 1024 * 1024
bad = ["%s is %d bytes; the limit is %d" % (f, (ROOT / f).stat().st_size, LIMIT)
       for f in sorted(tracked) if (ROOT / f).is_file() and (ROOT / f).stat().st_size > LIMIT]
check("V23 no tracked file exceeds 1 MiB (docs/cleanup/ included)", bad)

# ---- summary -----------------------------------------------------------------------
print()
print("%d of %d checks passed" % (sum(1 for _, ok in results if ok), len(results)))
if fails:
    print("VALIDATION FAILED: %s" % "; ".join(n.split(" ")[0] for n in fails))
    sys.exit(1)
print("VALIDATION PASSED")
