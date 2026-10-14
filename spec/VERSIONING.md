# Grid Network — Versioning

**Revision:** 2.1
**Protocol version:** v0.6.2

This document defines how the protocol and its specification evolve.

---

## Two version concepts

**Document revision.** The version of the specification itself. Format:
`MAJOR.MINOR`. Advances whenever the document changes. The current
revision is 2.1.

**Protocol version.** The feature set the specification defines.
Format: `vMAJOR.MINOR.PATCH`. The current protocol version is v0.6.2.
Implementations conform to a protocol version, not to a document
revision.

A document revision may advance without changing the protocol version.
A protocol-version change always produces a document revision.

---

## Document revisions

Revisions advance for any change, including editorial changes,
clarifications, restructuring, and corrections.

**MAJOR** — restructuring. Sections move, documents split, numbering
changes. Implementations are unaffected.

**MINOR** — content changes. Patches applied, sections rewritten, new
material added. The document's substance changes; the structure does
not.

**Example.** Revision 2.0 was the consolidation. Revision 2.1 applies
the review-cycle corrections described in `REVISIONS.md`.

A revision is never edited after it is published. Corrections produce a
new revision.

---

## Protocol versions

Format: `vMAJOR.MINOR.PATCH`.

**PATCH** — bug fixes only. No new features. No new fields. Backward
compatible. An implementation of the previous patch version remains
conformant.

**MINOR** — new features, new object types, new optional fields. New
implementations understand old objects; old implementations reject
objects they do not understand. Backward compatible in the sense that
old objects remain valid.

**MAJOR** — breaking changes. Old implementations cannot read new
objects. Migration requires a documented path.

---

## Stability markers

A section of the specification may carry a stability marker:

- **`stable`** — normative and conformance-grade. The section does not
  change without a protocol-version bump in the same revision.
- **`under-review`** — a rule exists but has a known defect or open
  question. Implementations must not build against this section yet.
- **Unmarked** — the default. Not a conformance claim.

### Build rule

A diff that changes a `stable` section must include a protocol-version
bump in the same revision. A diff that changes an `under-review`
section may be applied without a protocol-version bump, but the
section cannot be marked `stable` without a review closure recorded in
`REVISIONS.md`.

### Marked sections in the current revision

**Stable:**

- Protocol §1 (core invariant)
- Protocol §23 (rendezvous)
- Protocol §25 (relays)
- Protocol §36 (streams and sequence spaces)
- Protocol §37 (authority domains)
- Protocol §39 (failure semantics)
- Protocol §41 (cryptographic object encoding)
- Protocol §42 (signing-authority matrix)
- `OBJECTS.md §2` (canonical CBOR)
- `OBJECTS.md §3` (serialization)
- `OBJECTS.md §4` (envelope)
- `OBJECTS.md §8` (verification procedure)

**Under review:**

- Protocol §21 (pairing)
- Protocol §27 (verifier rules)
- Protocol §40 (reconciliation and conflict resolution)

---

## Support timeline

A protocol version is maintained for a minimum of five years after the
next major version ships. Maintenance covers security patches and
clarifications only.

End of support does not mean the protocol stops working. It means no
new security patches are issued. Implementations may continue running
older versions indefinitely.

---

## Feature status

A feature that is not in the current protocol version carries a feature
name and one status word.

- **`planned`** — the design is defined, the implementation is
  scheduled.
- **`deferred`** — the design is defined, the implementation is
  unscheduled. The feature is not in the roadmap.
- **`unscheduled`** — the design is not defined. The feature is a
  direction, not a plan.

A feature label without a status word is a documentation defect.

### Current status of features outside v0.6.2

| Feature | Status |
|---|---|
| Multipath connectivity | planned |
| Metadata minimization | planned |
| Chain-extension proofs | planned |
| Service ownership transfer | planned |
| Rendezvous federation | planned |
| Rendezvous gossip | planned |
| DHT-based discovery | planned |
| Post-quantum signature suite | planned |
| Threshold recovery | planned |
| Hardware-backed root keys | unscheduled |
| Delegated authorization trees | unscheduled |
| Anonymity transport | unscheduled |

---

## Migration

A protocol-version change requires a documented migration path. The path
must state:

- Which objects are added.
- Which objects are removed.
- Which objects change shape.
- Which fields are added or removed.
- The order in which a deployment should upgrade.
- What an old implementation sees when it encounters new objects.
- What a new implementation does when it encounters old objects.

A migration path is recorded in `REVISIONS.md` alongside the
protocol-version bump.

---

## Changelog

Every revision appends an entry to `REVISIONS.md`. An entry states:

- The revision number.
- The protocol version.
- A list of applied changes, grouped by tier.
- A list of open questions not yet resolved.
- The sections marked `stable` after the revision.
- The sections marked `under-review` after the revision.

An entry is never edited after publish. Corrections produce a new
entry.