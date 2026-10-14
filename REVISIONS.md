# Grid Network — Revision History

This file records every revision of the specification. Each entry
states the revision number, the protocol version, what changed, what
remains open, and the stability markers after the revision.

Entries are never edited after publication. A correction produces a new
entry.

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