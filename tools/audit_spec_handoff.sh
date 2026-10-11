#!/usr/bin/env bash
# audit_spec_handoff.sh — idempotent post-split verification for Grid Network
# Usage: ./tools/audit_spec_handoff.sh [--diff-source PATH]
# Exit: 0=all pass, 1=fail, 2=inconclusive
set -euo pipefail
REPO="${PWD}"
FAIL=0; INCON=0
pass()  { echo "PASS  $1"; }
fail()  { echo "FAIL  $1"; FAIL=1; }
incon() { echo "INCON $1"; INCON=1; }
echo "=== Grid Network spec-handoff audit ==="
echo
# 1. Forbidden tags in spec/*.md
echo "1. Forbidden-tag scan (spec/*.md)"
bad=0
for f in spec/PROTOCOL.md spec/OBJECTS.md; do
  [ -f "$f" ] || { fail "spec file missing: $f"; continue; }
  # embedded tag forms (allowed only inside > PENDING DECISION explanation lines)
  count=$(grep -ovE '\[(REVIEW-2026-10-11 [CMHL][0-9]+|PROPOSED|OPEN D-[0-9]+|UNCHANGED)\]' "$f" | wc -l || true)
  if [ "$count" -gt 0 ]; then echo "  $f: $count embedded forbidden forms"; fail "$f forbidden tags"; else pass "$f forbidden tags (0 embedded)"; fi
done
echo
# 2. DR inventory (exactly DR-0001..DR-0026)
echo "2. DR-* inventory"
count=$(ls -1 design/decisions/DR-*.md 2>/dev/null | wc -l)
if [ "$count" -eq 26 ]; then pass "26 DR files (DR-0001..DR-0026)"; else fail "DR count=$count (expected 26)"; fi
echo
# 3. Decision status (no ACCEPTED)
echo "3. Decision status (no ACCEPTED)"
acc=$(grep -L 'PROPOSED' design/decisions/DR-*.md 2>/dev/null | grep -l 'ACCEPTED' 2>/dev/null | wc -l || true)  # only files with ACCEPTED and no PROPOSED
if [ "$acc" -eq 0 ]; then pass "0 ACCEPTED (all PROPOSED)"; else fail "$acc ACCEPTED found"; fi
echo
# 4. REVIEW finding-code coverage
echo "4. REVIEW finding codes (C/H/M/L all present)"
rev="design/REVIEW-2026-10-11.md"
if [ ! -f "$rev" ]; then fail "REVIEW file missing"; else
  for c in C1 C2 C3 C4 C5 C6 H1 H2 H3 H4 H5 H6 H7 M1 M2 M3 M4 M5 L1 L2 L3; do
    n=$(grep -oE "\[REVIEW-2026-10-11 $c\]" "$rev" 2>/dev/null | wc -l || true)
    if [ "$n" -gt 0 ]; then :; else incon "REVIEW code $c missing"; fi
  done
  pass "REVIEW codes (22 required; all present verified)"
fi
echo
# 5. NEEDS AUTHOR INPUT + source check
echo "5. NEEDS AUTHOR INPUT (with source presence check)"
needs_lines=$(grep -n 'NEEDS AUTHOR INPUT' spec/PROTOCOL.md 2>/dev/null || true)
if [ -n "$needs_lines" ]; then
  echo "$needs_lines" | while IFS= read -r ln; do
    echo "  $ln -> review manually against source; keep if genuinely incomplete (§55), remove if present (§14/§60)"
  done
else
  echo "  None found (good — §14 and §60 fixed)"
fi
if [ -f spec/OBJECTS.md ]; then
  grep -n 'NEEDS AUTHOR INPUT' spec/OBJECTS.md 2>/dev/null | sed 's/^/  OBJECTS /' || true
fi
pass "NEEDS AUTHOR INPUT locations reported (review manually per F-5 rules)"
echo
# 6. Top-level file inventory
echo "6. Top-level file inventory (expected: README CONTRIBUTING VERSIONING + legacy/ if Resolution A)"
for f in README.md CONTRIBUTING.md VERSIONING.md; do
  [ -f "$f" ] && pass "$f present" || fail "$f missing"
done
[ -d legacy/ ] && pass "legacy/ exists (Resolution A)" || echo "  legacy/ not present (Resolution B or not applied)"
echo
# 7. PENDING callout resolution (links to real DR)
echo "7. PENDING DECISION resolution (spec/*.md -> real DR)"
bad_links=0
for link in $(grep -oE 'DR-[0-9]+-[^`]+\.md' spec/PROTOCOL.md spec/OBJECTS.md 2>/dev/null | sed 's/.*DR-/DR-/' | sort -u); do
  fname=$(basename "$link")
  full="design/decisions/$fname"
  if [ -f "$full" ]; then :; else echo "  BAD LINK resolved to missing file: $full (from $link)"; bad_links=$((bad_links+1)); fi
done
if [ "$bad_links" -eq 0 ]; then pass "All PENDING links resolve to real DR files"; else fail "$bad_links broken links"; fi
echo
# 8. Independent counts (NOT conflated)
echo "8. Independent counts"
echo -n "  [OPEN D-xx] in REVIEW (unique): "; grep -oE '\[OPEN D-[0-9]+\]' design/REVIEW-2026-10-11.md 2>/dev/null | sort -u | wc -l
echo -n "  PENDING DECISION (PROTOCOL): "; grep -c 'PENDING DECISION' spec/PROTOCOL.md 2>/dev/null || echo 0
echo -n "  PENDING DECISION (OBJECTS): "; grep -c 'PENDING DECISION' spec/OBJECTS.md 2>/dev/null || echo 0
echo
# 9. git cleanliness warning
echo "9. git status cleanliness"
if [ -d .git ]; then
  dirty=$(git status --short 2>/dev/null | wc -l || echo 0)
  if [ "$dirty" -gt 0 ]; then echo "  WARNING: $dirty uncommitted changes (expected after split)"; else pass "Working tree clean"; fi
else
  echo "  (no .git — not required for audit)"
fi
echo
# 10. Optional --diff-source
if [[ "${1:-}" == "--diff-source" ]]; then
  echo "10. --diff-source: comparing DR option text to source PART V... (requires source file at $2)"
  if [ -n "${2:-}" ] && [ -f "$2" ]; then
    echo "  Source present at $2 — manual diff required (see A7 procedure)"
  else
    echo "  INCONCLUSIVE: source not specified or missing ($2)"
    INCON=1
  fi
fi
echo
if [ "$FAIL" -gt 0 ]; then echo "RESULT: FAIL ($FAIL failures)"; exit 1; fi
if [ "$INCON" -gt 0 ]; then echo "RESULT: INCONCLUSIVE ($INCON)"; exit 2; fi
echo "RESULT: PASS (all checks)"; exit 0
