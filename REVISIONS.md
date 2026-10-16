# Grid Network — Revision History

This file records every revision of the specification. Each entry
states the revision number, the protocol version, what changed, what
remains open, and the stability markers after the revision.

Entries are never edited after publication. A correction produces a new
entry.

---

## Revision 2.5

**Protocol version:** v0.6.3 (unchanged)

**Applied changes.**

*Documentation.*
- `docs/cleanup/` added as a historical audit archive for the revision
  2.2 to 2.4 cleanup. It holds the merge plan for revision 2.2
  (`docs/cleanup/MERGE-PLAN.md`, preserved verbatim), the independent
  traceability review of `spec/SECURITY.md`
  (`docs/cleanup/SECURITY-REVIEW.md`), a summary of what was applied and
  pushed (`docs/cleanup/EXECUTION-RECORD.md`), and a guide
  (`docs/cleanup/README.md`). The files may contain retired version
  numbers, stale cross-references, and historical document names. They
  are not current documentation.
- The repository layout list in `README.md` includes `docs/cleanup/`.
- `docs/FOLLOW-UPS.md` carries an audit record note that points to
  `docs/cleanup/`.

*Tooling.*
- `tools/validate.py` treats `docs/cleanup/` as a historical archive. It
  skips the checks that compare a document with the current
  specification for those files. It still applies the scope, content-pin,
  credential, local-path, and file-size checks to them. The credential,
  local-path, private-URL, and file-size checks are new and apply to every
  tracked file.
- `tools/selftest.py` added. It applies deliberate defects in temporary
  clones and checks that `tools/validate.py` fails as it should, and that
  historical references in `docs/cleanup/` do not fail.
- `tools/README.md` describes the archive exemption and the self-test.

*Structure.*
- Revision strings advanced across all documents. The protocol version
  is unchanged.

**Normative changes.** None. No protocol rule, object, schema,
parameter, or stability marker changed.

**Open questions.** Same as revision 2.4. The open items are itemized in
`docs/FOLLOW-UPS.md`.

**Stability markers after this revision.** Unchanged from revision 2.2.

Stable:
- Protocol §23, §25, §39

Under review:
- Protocol §21, §27

`OBJECTS.md` carries no stability markers.

---

## Revision 2.4

**Protocol version:** v0.6.3 (unchanged)

**Applied changes.**

*Corrections.*
- `spec/SECURITY.md` sourcing corrected after an independent traceability
  review of every claim against `PROTOCOL.md`, `OBJECTS.md`,
  `PARAMETERS.md`, and the other documents it cites. Statements that no
  cited section supports were removed or recast to what the sections say:
  the pairing attempt limit, the F1–F6 summary, the lost-or-stolen device
  row, the clock-skew and replay rows, the eavesdropper row, the
  surveillance and endpoint-compromise bullets, the Application and
  Network observer rows of the blast-radius table, the polling-interval
  sentence, the device-revocation citations, and several guidance and
  out-of-scope bullets. The opening statement now says that each statement
  cites its source rather than that every statement traces to
  `PROTOCOL.md` or `OBJECTS.md`.

*Tooling.*
- `tools/validate.py` added. It is the validation gate used for
  revisions 2.2 and 2.3, moved into the repository and extended with
  checks for prose references to documents that do not exist, quoted
  section titles, and `spec/SECURITY.md` citations. `tools/README.md`
  explains how to run it.
- `.github/workflows/ci.yml` added. It runs `tools/validate.py` on pushes
  to `main` and on pull requests.

*Documentation.*
- `docs/FOLLOW-UPS.md` records newly identified follow-ups: parameters
  whose "Defined in" cell does not state them (item 3b), the
  non-exhaustive evidence review (item 6b), the missing statement about
  whether v0.6.3 differs normatively from v0.6.2 (item 9), and four
  inconsistencies in the specification found by the review (item 10).

*Structure.*
- Revision strings advanced across all documents. The protocol version
  is unchanged.

**Normative changes.** None. No protocol rule, object, schema,
parameter, or stability marker changed. `spec/SECURITY.md` is
non-normative.

**Open questions.** Same as revision 2.2, plus the follow-ups itemized in
`docs/FOLLOW-UPS.md`.

**Stability markers after this revision.** Unchanged from revision 2.2.

Stable:
- Protocol §23, §25, §39

Under review:
- Protocol §21, §27

`OBJECTS.md` carries no stability markers.

---

## Revision 2.3

**Protocol version:** v0.6.3 (unchanged)

**Applied changes.**

*Documentation.*
- `docs/FOLLOW-UPS.md` added. It records the work deferred from the
  revision 2.2 cleanup, with the unresolved question, the relevant files
  and historical sources, and whether each item needs a decision or an
  implementation. It is non-normative.
- The repository layout list in `README.md` includes
  `docs/FOLLOW-UPS.md`.

*Structure.*
- Revision strings advanced across all documents. The protocol version
  is unchanged.

**Normative changes.** None. No protocol rule, object, schema,
parameter, or stability marker changed.

**Open questions.** Same as revision 2.2. The deferred work is itemized
in `docs/FOLLOW-UPS.md`.

**Stability markers after this revision.** Unchanged from revision 2.2.

Stable:
- Protocol §23, §25, §39

Under review:
- Protocol §21, §27

`OBJECTS.md` carries no stability markers.

---

## Revision 2.2

**Protocol version:** v0.6.3

**Applied changes.**

*Corrections.*
- The chain hash rationale in `OBJECTS.md §3.8` and `DECISIONS.md` D5
  corrected. The signature covers `chain_hash`, which binds an object to
  its history. A chain hash does not reveal a fork to a verifier that
  has observed only one branch. The per-object cost stated in D5
  corrected to constant.
- Dangling cross-references repaired: `PROTOCOL.md §14` (revocation
  propagation is §31), `PROTOCOL.md §43` (verification is
  `OBJECTS.md §8`, constructions are `OBJECTS.md §3`), and the example
  references in the conventions list.
- `PARAMETERS.md` "Defined in" entries for relay and commercial
  parameters redirected from a nonexistent document to
  `commercial/MODEL.md` and `operations/RELAYS.md`.
  `DEFAULT_REACHABILITY_CREDIT_REWARD` is defined in no document and is
  marked open.
- `OBJECTS.md §7.9` and `§9.4` state that the remaining schemas are
  planned and not yet specified.

*Security documentation.*
- `SECURITY.md` added: security model, threats addressed and not
  addressed, blast radius, compromise response, and implementation
  guidance. It is non-normative and restates rules from `PROTOCOL.md`
  and `OBJECTS.md`.
- `PROTOCOL.md §44` and `RATIONALE.md §9` refer to `SECURITY.md`.

*Structure.*
- Revision and protocol version advanced across all documents.

**Correction to the revision 2.1 stability record.** The stability
list in revision 2.1 is historical. It named sections that carry no
marker in the files and `OBJECTS.md §11`, which does not exist. The
markers present in the files are listed below and are authoritative.

**Open questions.**

- The four open questions recorded in revision 2.1 remain open.
- Schemas, test vectors, and a conformance suite for the objects listed
  in `OBJECTS.md §10` are not yet specified.
- `DEFAULT_REACHABILITY_CREDIT_REWARD` has no defining document.

**Stability markers after this revision.**

Stable:
- Protocol §23, §25, §39

Under review:
- Protocol §21, §27

`OBJECTS.md` carries no stability markers.

---

## Revision 2.1

**Protocol version:** v0.6.2 (unchanged)

**Applied changes.**

*Byte-level constructions.*
- Domain separators in `PROTOCOL.md` aligned with the registry in
  `OBJECTS.md §5`.
- The verification procedure was consolidated into `OBJECTS.md §8` and
  the prior conflicting procedure was retired.
- Map key ordering rule in `OBJECTS.md §2.7` corrected to RFC 8949
  §4.2.1 bytewise lexicographic ordering.
- The Unicode version for NFC normalization fixed at Unicode 15.0.
- Example schemas in `OBJECTS.md §7` rewritten to satisfy the
  canonical CBOR rules they illustrate.
- Stream ID canonical encoding defined in `OBJECTS.md §3.6`.

*Security semantics.*
- `effective_sequence` boundary rule clarified to require an accepted
  predecessor chain, closing a forgery vector.
- `GrantRevocation` signer changed to Identity Root; stream changed to
  `stream:identity`.
- Pairing redesigned to use a high-entropy PAKE secret; the
  human-readable code is a verification code derived from the PAKE
  transcript.
- Observation records and clock-source rules added to lease validity.
- `MAX_LEASE_AGE` introduced as a bound on replayed leases.
- `max_offline_tolerance` clock defined.
- Verifier rule for relationship state corrected to require
  RECOGNIZED.

*Schema.*
- `Grant.expires_at` added.
- Lease validity expressed as two distinct fields.
- `ReachabilityRecord` freshness fields added.
- `OperatorManifest` extended with `serves_identity_state` and
  `current_relay_authority_key`.
- `CreditReceipt` stream defined.

*Sanitization.*
- Personal names, machine names, hostnames, and repository handles
  replaced with neutral forms or symbols.
- Product names retained where load-bearing, with a descriptive
  qualifier on first mention.
- Monetary, temporal, and rate values moved to `PARAMETERS.md` as
  symbols.
- Dated facts rewritten or qualified.
- Attributions to prior review material removed.
- First-person framing removed.
- Idiomatic phrasing replaced with declarative text.

*Structure.*
- Stability markers applied: `stable` on protocol §1, §23, §25, §36,
  §37, §39, §41, §42, and on `OBJECTS.md §2`, §3, §4, §8;
  `under-review` on protocol §21, §27, §40, and on `OBJECTS.md §11`
  (formerly the conflicting verification procedure).
- "Frozen" retired. Stability markers and `VERSIONING.md` replace it.
- Four-document structure adopted: specification, design record,
  roadmap (in a separate document), operator guide.
- Cross-document references use document names plus section numbers.
- Version vocabulary unified: `Vn` retired in favor of feature names
  and status words.

**Open questions.**

The following are recorded but not resolved in this revision. They are
carried forward in the decision log as open.

- Revocation effect on active sessions: immediate termination, or
  continue until the next authorization check.
- Lease renewal semantics under concurrent attempts.
- Relationship decay policy: whether idle state is pruned, and with
  what warning.
- Revocation propagation bound: whether a normative poll interval
  exists.

**Stability markers after this revision.**

Stable:
- Protocol §1, §23, §25, §36, §37, §39, §41, §42
- `OBJECTS.md §2`, §3, §4, §8

Under review:
- Protocol §21, §27, §40

---

## Revision 2.0

**Protocol version:** v0.6.2

**Applied changes.**

- Consolidated the specification and its companion documents into a
  single archive with four supporting volumes.
- Reorganized the protocol specification into sections 1 through 48.
- Extracted `OBJECTS.md` as a standalone encoding document.
- Merged security material into the protocol specification.
- Extracted the design rationale, decision log, rejected-approaches
  catalog, lineage, and extensions into the design record.
- Extracted relay operation and deployment into the operator guide.
- Extracted the commercial model into its own document.

**Open questions.** Same as revision 2.1; they were identified in 2.0
and carried forward.

**Stability markers after this revision.** None. The consolidation
introduced sections without a stability review.

---

## How to read this file

Each entry describes a complete revision of the specification. Between
revisions, patches are applied as described in the entry. The current
specification is at the revision listed at the top of `PROTOCOL.md`.

For a list of what is open, see the "Open questions" section of the
most recent entry. For a list of what is stable, see the "Stability
markers after this revision" section of the most recent entry.

For a list of features that are not in the current protocol version,
see `design/EXTENSIONS.md`. For a list of rejected approaches, see
`design/REJECTED.md`.