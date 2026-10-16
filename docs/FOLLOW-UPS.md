# Grid Network — Deferred Follow-ups

**Revision:** 2.2
**Protocol version:** v0.6.3

**Repository path:** `docs/FOLLOW-UPS.md`

This document is non-normative. It records work that was intentionally
deferred from the revision 2.2 / v0.6.3 cleanup merge. That merge
advanced the repository from commit `9898163` to commit `8527311`. Each
entry below states what remains unresolved, where the evidence is, and
whether the next step is a decision or an implementation.

Nothing in this document is a requirement, a schema, a parameter, or a
design decision. Where an entry proposes an approach, the approach is a
suggestion for whoever takes the work. Where an entry needs a human or
product decision, it says so, and the work should not be specified until
that decision is made.

---

## Reading this document

**Status.**

- **Needs decision.** A person must choose between outcomes before the
  work can be specified. A decision may be a product choice, a
  specification choice, or a choice of where content belongs.
- **Needs implementation.** The outcome is already determined by the
  current repository. Only the writing or checking remains.

**Priority.** Priority is a suggestion for ordering the work.

- **High.** Leaves an open question in the specification, or blocks a
  milestone listed in `ROADMAP.md`.
- **Medium.** Leaves a documentation inconsistency or a reference to
  something that does not exist.
- **Low.** Optional material, or a mechanical improvement.

**References.** The repository is authoritative. References to files in
this repository are checked mechanically. References to the Master
Archive, its appendices and addenda, to earlier commits, and to working
files that were never committed are historical: those sources are not in
this repository, and the earlier commits are not present in a shallow
clone. Each such reference is marked as historical or as an archive
source where it appears. Archive section numbers follow the first
uploaded Master Archive unless an appendix of the consolidated archive
is named. Historical material is evidence, not authority.

---

## Summary

| Item | Priority | Scope | Dependency or precondition | Suggested approach | Source and evidence |
|---|---|---|---|---|---|
| 1a. G6 multipath constraints | Low | `design/EXTENSIONS.md` | Decision on whether the Addendum's list adds anything to the existing paragraph | Compare the archive list with the existing paragraph; add only statements expressible in repository terms | Detailed Reference Addendum D.5; Master Archive §10.10 (historical archive) |
| 1b. G7 objections and reframings | Low | `design/RATIONALE.md` | Decision on scope and placement | Add a section after §7 with attributions removed; cross-reference D10 and D16 | Design Defense Addendum Parts 1, 3, 4 (historical archive) |
| 1c. G8 decision and rejection entries | Low | `design/DECISIONS.md`, `design/REJECTED.md` | Decision per objection: decision or rejection | Append entries with the next free numbers; never renumber | Design Defense Addendum §§2.7–2.9 (historical archive) |
| 1d. G9 reviewer questions | Low | `spec/PITCHES.md` | Decision on placement and audience | Add a section with three answers, attributions removed | Design Defense Addendum Part 5 (historical archive) |
| 1e. G10 application integration sketch | Low | Non-normative document | Decision on whether it is wanted at all | If wanted, add pseudo-code outside normative text | Master Archive §7.44 (historical archive) |
| 1f. G11 document dependency graph | Low | `README.md` | Decision on whether it is wanted | If wanted, add a short list or diagram to the layout section | Master Archive §18.3 (historical archive) |
| 1g. Level 6 cross-reference | Low | `spec/CONFORMANCE.md` | Decision on citing a non-normative document from the levels | Add one pointer line to `spec/SECURITY.md` in Level 6 | `CONFORMANCE.md §2`; cleanup plan (working file, unavailable) |
| 2. Appendix C audit | Medium | `design/RATIONALE.md` history | Full history available (shallow clone) | Read-only passage-by-passage comparison with verdicts | Appendix C of the consolidated archive (historical archive); commits `b5e8be7`, `21b91b9`, `bbc81b5` (historical) |
| 3. `DEFAULT_REACHABILITY_CREDIT_REWARD` | Medium | `spec/PARAMETERS.md` | Product decision: define or remove | Define in one document and update the cell, or remove the row | `spec/PARAMETERS.md`; `REVISIONS.md` Revision 2.2 |
| 4. `OBJECTS.md §10` pending work | High | `spec/OBJECTS.md`, `spec/CONFORMANCE.md` | Decisions on field sets; several earlier proposals were never accepted | Decide field sets first; then write schemas, vectors, suite | `OBJECTS.md §10`; `ROADMAP.md §4`; historical commits `d329409`, `ed627cb` |
| 5. Appendix B open decisions | High | `spec/PROTOCOL.md`, `design/DECISIONS.md`, `ROADMAP.md` | Four human decisions | Decide each; record in the decision log; update affected sections | `ROADMAP.md §5`; `REVISIONS.md`; Appendix B (historical archive) |
| 6. Security Addendum review | Low | `spec/SECURITY.md` | Decision per topic on whether to import | Review remaining sections against the repository; import only what traces to existing rules | Security Addendum (historical, `9f16353`); `spec/SECURITY.md` |
| 7a. "Operator Guide" and "Design Record" | Medium | `spec/PROTOCOL.md`, `spec/GLOSSARY.md`, others | Decision on defining the terms or replacing them | Define once, or replace with directory references | `REVISIONS.md` Revisions 2.0 and 2.1 |
| 7b. Cross-reference style in conventions | Low | `spec/PROTOCOL.md` | Decision on the canonical style | Choose one style and apply it to the conventions list | `PROTOCOL.md` conventions list; style used in `OBJECTS.md §2` |
| 8. README repository layout | Low | `README.md` | None | Add the missing documents using the existing style | `README.md`; tracked file list |

---

## 1. Archive gap merges and the Level 6 cross-reference

These items were identified when the archive and addenda were compared
with the repository. They were not merged because their wording was not
fully specified. Each is optional. None blocks the specification.

**1a. Multipath non-preclusion constraints (G6).** `design/EXTENSIONS.md`
already has a paragraph under "Multipath connectivity" titled
"Constraints on the current protocol that preserve multipath". It makes
four statements about relay tickets, reachability records, and relay
selection. The Detailed Reference Addendum (D.5) and Master Archive
§10.10 list five constraints, both historical. Unresolved:
whether any of the five adds a constraint the existing paragraph lacks,
and whether it can be stated using terms the repository defines. Some
archive wording uses terms the repository does not define.

- Needs decision: which, if any, of the five to add.
- Needs implementation: the edit, after the decision.

**1b. Objections and reframings (G7).** The Design Defense Addendum
(Parts 1, 3, 4; historical archive) answers objections such as "it is
just a VPN", "it is too complex", "nobody cares about portability", and
"the commercial model is a hypothesis". `design/RATIONALE.md` §7.9
(FAQ) covers some of the same ground. Unresolved: whether the design
record should carry this material, where it belongs, and how to avoid
restating D10 and D16. Any attributions to reviewers must be removed, as
revision 2.1 did elsewhere.

- Needs decision: scope and placement.
- Needs implementation: the section, after the decision.

**1c. Decision and rejection entries (G8).** The Design Defense Addendum
(§§2.7–2.9; historical archive) records objections about using DNS for
discovery, a four-layer project model, and multipath in the first
protocol version. Unresolved: for each, whether it is a decision in
`design/DECISIONS.md` (next free number is D39) or a rejection in
`design/REJECTED.md` (next free number is R18). `design/REJECTED.md` R3
and R10 already cover hierarchical naming and DHT discovery, so overlap
must be checked. The archive's own decision numbers 38 and 39
(rendezvous serves identity state; freshness fields) are already D36 and
D37 in the repository and must not be imported again.

- Needs decision: classification of each objection.
- Needs implementation: the entries, after the decision.

**1d. Reviewer questions (G9).** The Design Defense Addendum Part 5
(historical archive) gives three scripted answers to skeptical
reviewers. `spec/PITCHES.md` has no reviewer section. Unresolved:
whether pitches should carry them, and the audience row that would
reference them.

- Needs decision: placement and audience.
- Needs implementation: the section, after the decision.

**1e. Application integration sketch (G10).** Master Archive §7.44
(historical archive) contains a code sketch of an application calling
the local agent. The concept is related to `PROTOCOL.md §13`. Unresolved:
whether a sketch is wanted. Pseudo-code must not enter normative text.

- Needs decision: whether to include it, and in which non-normative
  document.

**1f. Document dependency graph (G11).** Master Archive §18.3
(historical archive) contains a graph of how the documents depend on one
another. `README.md` has a repository layout list but no dependency
information. Unresolved: whether the graph is wanted.

- Needs decision: whether to include it.
- Needs implementation: the graph, if wanted.

**1g. Level 6 cross-reference.** `CONFORMANCE.md §2` Level 6 ("Security")
lists forgery-and-bypass tests. `spec/SECURITY.md` is non-normative.
Unresolved: whether a conformance level may point at it. A pointer would
not add any requirement.

- Needs decision: whether the pointer is appropriate.
- Needs implementation: one line, after the decision.

---

## 2. Appendix C "Future Proofs" audit

**Unresolved.** Whether commit `21b91b9` (historical) removed substantive
design content from `design/RATIONALE.md` beyond the "Future-Proofing"
section, and whether the restoration in commit `bbc81b5` (historical)
recovered that section. Follow-up commits `b3263da` and `ae38fd6`
(historical) removed residue from the restored text.

**What the archive reports.** Appendix C of the consolidated archive
(historical archive) reports that `21b91b9` deleted 594 lines from
`design/RATIONALE.md`; that the "Future-Proofing" block was about 320
lines; and that the restored text is about 243 lines. It reports that
the 77-line difference was never proven to be residue. The archive
itself marks these numbers as unverified. This document does not
verify them either.

**Layout caveat.** Appendix C of the consolidated archive (historical)
names the restore locations as section 8 of `design/DECISIONS.md`,
`design/EXTENSIONS.md`, and section 2.3 of `operations/RELAYS.md`. Those
names come from the layout before revision 2.1. In the current
repository `design/DECISIONS.md` is a numbered log (D1–D38) with no
section 8, and `operations/RELAYS.md` has a §2 ("Relay capability model")
with no section 2.3. The audit must first map each
old location to its current equivalent.

**Residue check done.** The two residue phrases quoted in Appendix C of
the consolidated archive (historical) do not appear in the current
repository.

**Method required by the archive.**

- Read only. Use the "Future-Proofing" section of `design/RATIONALE.md`
  at commit `b5e8be7` (historical) as the source of truth. Do not use
  session notes.
- Compare passage by passage. Quote both texts verbatim.
- Give each passage a verdict: MAPPED, CONDENSED, or MISSING.
- Account for the line arithmetic, with the difference itemized.
- If a command's output contradicts an earlier output, stop and report
  the contradiction.

**Precondition.** The commits above are not present in this clone, which
is shallow. The full history must be fetched before the audit can run.

- Needs implementation: the audit.
- Needs decision: whether to restore any passage the audit finds MISSING.

---

## 3. `DEFAULT_REACHABILITY_CREDIT_REWARD`

**Unresolved.** `spec/PARAMETERS.md` lists
`DEFAULT_REACHABILITY_CREDIT_REWARD` in the commercial parameters with
the meaning "Credit earned per day of reachability published". Its
"Defined in" cell carries a TODO because no document in the repository
defines it or uses the symbol. Credit accounting is described in
`operations/RELAYS.md` §12 and `commercial/MODEL.md`, and neither
describes a per-day reachability credit. `REVISIONS.md` (Revision 2.2)
records the parameter as open.

The existing literal default in the row is retained unchanged, by an
earlier decision. This document does not propose a value.

**Options.**

- Define the behavior in one document, then point the "Defined in" cell
  at it.
- Remove the row, if the behavior is not wanted.

- Needs decision (product): whether a per-day reachability credit exists.
- Needs implementation: either edit, after the decision.

---

## 4. `OBJECTS.md` §10 schemas, test vectors, and conformance suite

**Unresolved.** `OBJECTS.md §10` lists what is not yet specified:

- Full schemas for `RendezvousManifest`, `OperatorManifest`,
  `KeyRevocation`, `RelationshipTermination`, `IdentityContinuity`,
  `StreamResolution`, `GrantRevocation`, `LeaseRevocation`,
  `RelayNodeRecord`, and `CreditReceipt`.
- Test vectors, positive and negative, for every object type.
- A conformance test suite.

Until these exist, `OBJECTS.md §6` is authoritative for which objects
exist and who signs them. `OBJECTS.md §7.9` and `OBJECTS.md §9.4` now state that
the schemas are planned.

**What the repository says.** `ROADMAP.md §4` lists "Object schemas for
the ten stubbed types" and "Test vector format and first vectors" as
not started, and "Conformance scenarios fully specified" as drafted.
`ROADMAP.md §3` assigns completed schemas and published test vectors to
the v0.7.0 release target. `CONFORMANCE.md §3` already defines a test
vector format, which the work queue entry appears not to reflect. Reconciling
the two is part of this item.

**Historical material, not authority.** Earlier drafts exist only in
history: `replacement_objects_sections.md` and `CHAIN_INIT_FIX.json` at
commit `d329409` (historical), and design records DR-0001 through DR-0026
at commit `ed627cb` (historical), whose status is "PROPOSED" and not
accepted. Appendix B.3 of the consolidated archive (historical archive)
lists the intended object set and five corrections to an earlier draft
plan. Some of those corrections are already reflected in revision 2.1
(`REVISIONS.md`). None of this material was imported. The current
repository governs any conflict.

- Needs decision: the field set and stream for each object, and any
  proposal that conflicts with the current repository.
- Needs implementation: the schemas in `OBJECTS.md §7`, the vectors, and
  the suite, after the decisions.

---

## 5. Appendix B open design decisions

**Unresolved.** Appendix B.5 of the consolidated archive (historical
archive) lists three open design decisions: the effect of revoking a
grant on an active session, lease renewal under concurrent attempts, and
relationship decay policy. `ROADMAP.md §5` lists the same three plus a
fourth, the revocation propagation bound, as questions Q1 to Q4.
`REVISIONS.md` carries all four forward. None is decided.

**Related rules already in the repository.**

- `PROTOCOL.md §14` and `PROTOCOL.md §31`: revocation is pulled, there is no
  immediacy guarantee, and no normative propagation bound is defined.
- `PROTOCOL.md §30`: lease expiration and renewal.
- `PROTOCOL.md §8`: the relationship model.
- `REJECTED.md` R15 rejects push-based revocation. R17 rejects decay
  fields in the protocol.

**Related defect found while writing this document.** `ROADMAP.md §5`
says each question is tracked in `design/DECISIONS.md` under "Open
decisions". `design/DECISIONS.md` has no such section. Resolving it means
either adding that section or repointing the sentence. That is a
decision about where open questions live.

**Already resolved.** Decisions 38 and 39 in Appendix B of the
consolidated archive (historical), on rendezvous serving identity state
and on freshness fields, are D36 and D37 in
`design/DECISIONS.md`. No action remains.

Any resulting change to a `stable` section requires a protocol-version
bump (D38).

- Needs decision (human): all four questions, and where open questions
  are tracked.
- Needs implementation: recording the decisions and updating the
  affected sections.

---

## 6. Remaining Security Addendum review

**Unresolved.** `spec/SECURITY.md` was written from the Security
Addendum recovered from history (historical, `9f16353`, path
`docs/design/SECURITY.md`). The Addendum has 32 numbered sections. Only
part of it was reviewed for this repository.

**Reviewed for `spec/SECURITY.md`.** Sections 1 to 4 of the Addendum
(historical; purpose, security model, primary invariant, blast-radius
model) and the short-form
sections that precede it (threat model, blast radius, failure
semantics, security principles, compromise procedures, implementation
requirements, attack scenarios).

**Excluded by decision.** §14 (relay capacity and hardware), §16
(optional computational admission cost), §28 (Bitcoin-inspired
principles), §31 (security test program), and §32 (security roadmap).

**Not yet reviewed for inclusion.** §§5–13 (cryptographic object
security, sequence-space isolation, atomic verification, authorization,
freshness and replay, identity continuity, relationship, rendezvous, and
relay security), §15 (resource exhaustion and admission controls), §17
(Sybil resistance), §18 (metadata and privacy), §§19–20 (local verifier
state and its loss), §21 (failure semantics), §22 (endpoint and key
compromise), §23 (application and agent security), §24 (parser and
implementation security), §25 (anti-amplification), §26–27 (operational
boundary and recovery), §29 (threat categories), and §30 (security
review rule).

**Also not fully reviewed.** The earlier `design/THREAT-MODEL.md` at
commit `eeb3983` (historical; 599 lines). Only its opening was read.

**Constraints for any import.** The material must stay non-normative,
must contain no literal figures, must trace to an existing rule in
`PROTOCOL.md` or `OBJECTS.md`, and must not contradict `PROTOCOL.md §18`
or `REJECTED.md` R5. `design/RULES.md` applies to any new mechanism.

- Needs implementation: the review of each remaining section.
- Needs decision: for each topic, whether it belongs in
  `spec/SECURITY.md`.

---

## 7. Undefined document names and conventions

**7a. "Operator Guide" and "Design Record".** Several documents use
these names as if they were files: `PROTOCOL.md` (the "Normative order"
paragraph), `GLOSSARY.md` (the Grid agent is "defined in the Operator
Guide"), `RATIONALE.md` §9, `RULES.md` (rule A2), `LICENSE.md`, and
`CONTRIBUTING.md`. No file has these names, and no document says which
directory each name refers to.

The evidence for the intended mapping is historical:
`REVISIONS.md` Revision 2.0 extracted relay operation and deployment
into "the operator guide" and the rationale, decisions, rejections,
lineage, and extensions into "the design record". Revision 2.1 adopted
a four-document structure: specification, design record, roadmap,
operator guide. That suggests the design record is `design/`, the
roadmap is `ROADMAP.md`, and the operator guide is `operations/`.
`LICENSE.md` lists the commercial model separately, so `commercial/` may
not be part of the operator guide. This mapping is an inference and is
not stated anywhere.

The `GLOSSARY.md` sentence is a separate case: it says the Grid agent is
defined in a document that does not exist, so the statement points at
nothing as written.

**Options.**

- Define each name once, for example in `GLOSSARY.md`, and keep the
  uses.
- Replace each use with the directory it means.

- Needs decision: which option, and the correct source for the Grid
  agent statement. `PROTOCOL.md` is normative, so wording there follows
  the stability rules in `VERSIONING.md`.
- Needs implementation: the edits, after the decision.

**7b. Cross-reference style in the conventions list.** The conventions
list in `PROTOCOL.md` shows cross-document references in bracket style,
such as `[OBJECTS §3]`. The rest of the repository writes them as
`OBJECTS.md §3` in backticks. Unresolved: which style is canonical.

- Needs decision: the canonical style.
- Needs implementation: apply it to the conventions list, or remove the
  examples.

---

## 8. README repository layout

**Unresolved.** The layout list in `README.md` omits documents that
exist in the repository: `spec/CONFORMANCE.md`, `spec/PITCHES.md`,
`design/RULES.md`, `operations/RENDEZVOUS.md`, `ROADMAP.md`,
`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `LICENSE.md`.
`spec/SECURITY.md` and `docs/FOLLOW-UPS.md` are listed.

No decision is needed about what to list. Each description should be
taken from the document's own opening statement, in the existing style:
a directory line followed by indented file names with a short
description.

- Needs implementation: the additions.
