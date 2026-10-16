# Grid Network: Merge Plan (Archive + Addendum into the repo)

Base: `ryan-parzynski/grid-network` at `9898163` (Revision 2.1, protocol v0.6.2).
Sources: Master Archive (Parts 1-24), Detailed Reference Addendum, Design Defense Addendum.
Target revision: 2.2 (documentation only, protocol version unchanged).

## 1. Principle

The repo is the source of truth. The archive is an earlier, pre-sanitization form of most of it.
Nothing is pasted wholesale. Material goes in only where the repo has a real gap, in the
repo's own conventions:

- Symbols instead of literal values (`spec/PARAMETERS.md`).
- No personal names, dollar amounts, rates, or attributions to review material (Revision 2.1 sanitization).
- Stability markers instead of "frozen" (D38).
- `grid/*` domain separators, never `mesh/*`.
- `REVISIONS.md` is append-only.

## 2. Coverage matrix

### Already in the repo (drop from the merge)

| Archive / addendum material | Repo location |
|---|---|
| Parts 3-6 problem, solution, architecture, authority chain | `design/RATIONALE.md` §2-3, `spec/PROTOCOL.md` |
| Part 7 protocol (7.1-7.55) | `spec/PROTOCOL.md` (the repo version is newer) |
| Part 8 and addendum Parts A, B, E: constructions, 10-step verification, rejection classes | `spec/OBJECTS.md` §3, §8 (verified identical) |
| Signing-authority matrix (7.47) | `spec/OBJECTS.md`, `spec/PROTOCOL.md` |
| Failure semantics F1-F6 (7.42, 9.4) | `spec/PROTOCOL.md` §39, `design/DECISIONS.md` D10 |
| Conformance levels, 17 scenarios, vector format, production sequence, repo layout (7.49-7.50, 17.7-17.8) | `spec/CONFORMANCE.md` §2-6 (C1-C17 present) |
| Part 10/15 relay, Pi, aggregation, path diversity, economics, credits | `operations/RELAYS.md` §1-12, `commercial/MODEL.md` |
| Parts 11-13 commercial, developer case, contribution model | `commercial/MODEL.md`, `design/RATIONALE.md` §5-6 |
| Part 14 lineage | `design/LINEAGE.md` |
| Part 16 edge cases and FAQ | `design/RATIONALE.md` §7.1-7.9 |
| Parts 20-21 decision log, rejected approaches | `design/DECISIONS.md` (D1-D38), `design/REJECTED.md` (R1-R17) |
| Part 22 glossary | `spec/GLOSSARY.md` |
| Part 23 anti-patterns, new-mechanism checklist | `design/RULES.md` |
| 7.45-7.46, 7.51 scope, deferred features, future extensions | `spec/VERSIONING.md`, `design/EXTENSIONS.md` |
| Part 19 naming journey | `design/RATIONALE.md` §8, D33 (names removed on purpose) |
| Part 24 handoff package, Part 2 inventory | Superseded by `README.md` "Where to start" and `CONTRIBUTING.md` |
| Defense addendum objections 2.1-2.6 (self-certifying IDs, one stream per issuer, cumulative chain, PAKE, terminal revocation, offline tolerance) | D1, D5, D6, D11, D16, R-entries |

### Real gaps (these get merged)

| # | Gap | Source | Destination |
|---|---|---|---|
| G1 | **Consolidated threat model.** `PROTOCOL.md` ("conformance" section, near line 1609) and `RATIONALE.md` §9 both refer to "the stated threat model" in the Protocol Specification. No such section exists. Dangling reference. | Addendum C.1, C.2; Archive 7.39, 9.1, 9.2, 9.8 | New `spec/SECURITY.md` |
| G2 | Blast-radius table | Archive 9.3 + Addendum C.3 (merge into one table) | `spec/SECURITY.md` |
| G3 | Compromise response procedures with recovery-time framing | Archive 9.6, 7.40; Addendum C.4 | `spec/SECURITY.md` (link to `operations/DEPLOYMENT.md` §7 for key protection; do not duplicate) |
| G4 | Implementation MUST / SHOULD / MUST NOT list (constant-time, zeroization, no secret logging, rate limits, timestamp bounds, no custom crypto). Repo has only scattered mentions. | Archive 7.48, 9.7; Addendum C.5 | `spec/SECURITY.md` §Implementation requirements; add one cross-reference line in `spec/CONFORMANCE.md` Level 6 |
| G5 | Fork-detection worked example (single-branch detection) | Addendum A.3 | `spec/OBJECTS.md` §3.8 (about 12 lines) |
| G6 | Multipath non-preclusion constraints (five points) | Addendum D.5, Archive 10.10 | `design/EXTENSIONS.md` under "Multipath connectivity" |
| G7 | Defense-addendum framing not yet in repo: "just X" objection, "too complex", "nobody cares about portability", "commercial model is a hypothesis", reframings 3.1-3.8 | Defense addendum Parts 1, 3, 4 | `design/RATIONALE.md` new section "Objections and reframings"; strip attributions; merge reframings 3.2 and 3.3 with D10 and D16 rather than restating |
| G8 | Objections not yet recorded: DNS for discovery, four-layer model, multipath-in-V1 | Defense addendum 2.7-2.9 | `design/DECISIONS.md` (short entries, next free D numbers) and `design/REJECTED.md` where it was rejected |
| G9 | Skeptical-reviewer answers (three scripted answers) | Defense addendum Part 5 | `spec/PITCHES.md` as a "reviewer questions" section |
| G10 | Application integration example (code sketch) | Archive 7.44 | Optional. Concept exists at `PROTOCOL.md` §13; add a short pseudo-code block only if wanted |
| G11 | Document dependency graph | Archive 18.3 | Optional. One small diagram or list in `README.md` "Repository layout" |

### Deliberately excluded (decision needed only if you disagree)

- Dollar figures, throughput figures, NAT/ISP percentages, operator margins (addendum D.3, D.4, D.6; archive 11.x, 15.x).
  Revision 2.1 moved these to symbols on purpose. If you want them back, put them in
  `spec/PARAMETERS.md` as `ILLUSTRATIVE_*` rows or in a clearly labeled non-normative
  appendix in `operations/RELAYS.md`.
- Naming journey candidates, personal names, reviewer attributions.
- Archive Parts 1-2 and 24 (inventory, handoff). They describe the old project state.

## 3. Conflicts: the repo wins

| Topic | Archive / addendum says | Repo says | Resolution |
|---|---|---|---|
| Pairing code | Code derived from device keypair and timestamp (7.21); also lists PAKE (7.20, 7.45) | PAKE secret; code is a verification code derived from the PAKE transcript | Repo. Archive is internally inconsistent here too |
| Relationship state in verifier rules | "RECOGNIZED or PENDING OK" (7.28) | RECOGNIZED required | Repo. Archive 7.9 itself says PENDING does not contribute |
| Wall-clock in authorization | "MUST NOT use wall-clock time for authorization (relative only)" (7.48) | Grant validity absolute, lease validity relative (D15) | Repo. Do not import that MUST NOT line |
| Revocation latency | "Immediate revocation, no propagation delay" (5.4) vs "within 30 minutes" (9.6, 7.50) | Pull-based, no immediacy guarantee (D17, R15) | Repo. Use a symbol for any target, never a literal |
| Revocation exposure on lost device | 30 minutes to 30 days (addendum T6) | Bounded by min(propagation, lease expiry) | State the formula only |
| Device key compromise scope | "Reachability only" (archive) vs "total" in the reachability column (addendum) | Device Keys sign only reachability | One table, reachability column only |
| Blast-radius table shape | Archive: 4 columns. Addendum: 3 columns plus Service Key and Application rows | n/a | Union of both: all rows, Identity, Relationship, Authorization, Reachability columns |
| "Frozen" status | Protocol "frozen, locked" | Stability markers (D38) | Repo |
| Domain separators | `mesh/*` called out as known issue | `grid/*` throughout | Already fixed |
| Precedence | Addendum Part E: "the Master Archive governs" | Repo is authoritative | Drop the clause; the two "drift" corrections are already the repo's only form |

## 4. Execution order

Each step is one commit. Steps are ordered so every later edit can link to something that exists.

1. **`spec/SECURITY.md` (G1-G4).** Sections: scope and assumptions; threats (T1-T14, one table: attacker goal, mechanism, defense, outcome); explicit non-properties; blast radius; compromise response; attack scenarios (only those adding something beyond the threat table); implementation requirements. Normative language limited to the requirements section; everything else non-normative. No literal times or rates; use `PARAMETERS.md` symbols and add any new ones there.
2. **Wire it in.** Fix the dangling "stated threat model" references in `spec/PROTOCOL.md` (conformance section) and `design/RATIONALE.md` §9 to point at `spec/SECURITY.md`. Add the cross-reference in `spec/CONFORMANCE.md` Level 6. Add `SECURITY.md` to the `README.md` layout list and `spec/GLOSSARY.md` entries for any new terms.
3. **`spec/OBJECTS.md` §3.8 (G5).** Add the single-branch fork-detection example after the chain-hash definition.
4. **`design/EXTENSIONS.md` (G6).** Add the non-preclusion constraint list under "Multipath connectivity".
5. **`design/RATIONALE.md` (G7).** Add "Objections and reframings" after the existing edge-cases section. Merge reframings with D10/D16 by cross-reference.
6. **`design/DECISIONS.md` and `design/REJECTED.md` (G8).** Append new entries after D38 and R17. Never renumber.
7. **`spec/PITCHES.md` (G9).** Add reviewer-question answers.
8. **Optional (G10, G11).** Application integration sketch; dependency graph.
9. **`REVISIONS.md`.** Append a Revision 2.2 entry: protocol version v0.6.2 (unchanged), applied changes, what remains open, stability markers. Update the revision header in every touched file and in `ROADMAP.md`. Update `spec/VERSIONING.md` changelog.

## 5. Verification (last task before pushing)

- Every relative link resolves (script over all `.md` files).
- No literal dollar amounts, throughput numbers, personal names, or "TODO"/"pending" in new text.
- Every symbol used in `SECURITY.md` exists in `spec/PARAMETERS.md`.
- Every new decision/rejection ID is the next unused number and nothing was renumbered.
- Each claim in the threat table traces to an existing mechanism in `PROTOCOL.md` or `OBJECTS.md` (no new mechanisms introduced; `design/RULES.md` A1 checklist).
- Revision strings are consistent across all files.
- For the security document specifically, a second reader (separate agent) checks it against `PROTOCOL.md` and `OBJECTS.md` for contradictions, because it is the one new normative-adjacent document.

## 6. Open questions for you

1. Keep the numeric figures out (default), or restore them as labeled illustrative parameters?
2. Do you want the optional items G10 and G11?
3. Push directly to `main` as one commit per step, or open a branch and a pull request for review? (Default: branch + PR.)

## 7. Scope notes

- Everything above was checked against the repo at `9898163`.
- The archive appendices (A-D, verbatim) are referenced in the archive but not included in the upload; the repo already contains the material they summarize.

## 8. Final adjustments (supersede earlier sections where they differ)

- Target is revision 2.2 and protocol version v0.6.3 (the earlier "protocol unchanged" note is superseded).
- Superseded again: the user then authorized five commits applied directly on `main` and pushed with `git push origin main`; a protected-branch rejection stops the run. Earlier note: four commits on a feature branch.
- Applied: dangling-reference repairs, chain-hash correction (OBJECTS §3.8, D5), `spec/SECURITY.md`, README layout line, REVISIONS 2.2 entry, version bump.
- Not applied: G5 (fork example; replaced by the corrected wording), G6 to G9, G10, G11, and the D39/D40 imports.
- D39/D40 were not imported. The archive's rendezvous-serves-identity-state and freshness-field decisions already exist as D36 and D37, with the same fields in `OBJECTS.md` and `PROTOCOL.md`.
- Existing literal figures in `spec/PARAMETERS.md` are left untouched. No new figures were added.

## 9. Deferred follow-ups

Gap merges not fully specified:
- Application integration sketch (G10) and document dependency graph (G11), per the earlier decision.
- Multipath non-preclusion constraints in `design/EXTENSIONS.md` (G6).
- "Objections and reframings" in `design/RATIONALE.md` (G7).
- New decision and rejection entries from the defense addendum (G8).
- Reviewer-question answers in `spec/PITCHES.md` (G9).
- Optional cross-reference from `spec/CONFORMANCE.md` Level 6 to `spec/SECURITY.md`.

Provenance and consistency:
- Appendix C over-deletion audit: compare the "Future Proofs" block from commit `b5e8be7` (`design/RATIONALE.md`) with `design/DECISIONS.md` §8, `design/EXTENSIONS.md` and `operations/RELAYS.md` §2.3, passage by passage, with verbatim quotes and a MAPPED / CONDENSED / MISSING verdict.
- `DEFAULT_REACHABILITY_CREDIT_REWARD` has no defining document. It carries a TODO in `PARAMETERS.md`.
- Schemas, test vectors and a conformance suite for the objects listed in `OBJECTS.md` §10.
- Archive Appendix B open design decisions (revocation effect on active sessions, lease renewal concurrency, relationship decay).
- Remaining Security Addendum material not yet reviewed for `SECURITY.md`: relay and rendezvous security, local verifier state, metadata properties, parser security.

Pre-existing defects not fixed in this merge:
- "Operator Guide" and "Design Record" are used as document names in `PROTOCOL.md`, `GLOSSARY.md`, `RATIONALE.md`, `RULES.md` and `LICENSE.md` without a defined mapping to `operations/` and `design/`.
- `README.md` layout list omits several documents (CONFORMANCE, PITCHES, RULES, RENDEZVOUS, ROADMAP, CONTRIBUTING, CODE_OF_CONDUCT, LICENSE).
- `PROTOCOL.md` conventions list cross-document examples but the repository uses a different style elsewhere (`OBJECTS.md §2`).

Update: the RATIONALE §1 reading-guide numbers and the stray revision block before PROTOCOL §21 were moved into scope and are fixed by the script (commits 1 and 4).
