---
title: "Grid Network — Relationship privacy"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-07
severity: High
blocks: V1
linked_finding: H1/M1
opened: 2026-10-11
deciders: (pending acceptance)
---
---
title: "Grid Network — Relationship privacy"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-07
severity: High
blocks: V1
linked_finding: H1/M1
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-07 — Relationship privacy

> **Status:** PROPOSED — NOT ACCEPTED. Change only on merged PR with spec updates and CHANGELOG entry.

## Metadata

- ID: D-07
- Title: Relationship privacy
- Severity: High
- Blocks: V1
- Linked finding: [REVIEW-2026-10-11 H1/M1](../REVIEW-2026-10-11.md) (see section H1/M1 or search tag)
- Date opened: 2026-10-11
- Status: PROPOSED

D-07: RELATIONSHIP PRIVACY — ASSERTION STREAM LOCATION
[HIGH PRIORITY, IMPACTS D-01 AND DEPLOYMENT]

Problem:
v0.6.2 places RelationshipAssertion and RelationshipTermination in the
principal's identity stream. Rendezvous servers are expected to serve identity
streams. Anyone querying the rendezvous learns the principal's entire contact
list (H1). The spec acknowledges anonymity is not a property, but this is a
larger exposure than intended.

Option A: Per-relationship stream, shared only with counterpart [PROPOSED]

  A new stream type: stream:relationship:<relationship_id>, created during
  pairing by both parties. It contains assertions and terminations for that
  specific relationship only. It is not published to rendezvous; it is
  exchanged directly between the two parties (via relay or direct path).

  relationship_id is derived from the pairing transcript (D-06/M1).

  Pros:
    - Social graph is not exposed.
    - Scalable: each relationship has its own stream; no per-device
      relationship accounting in the identity stream.
    - Simpler identity stream: only identity/key/binding/revocation/continuity
      data, not relationships.
    - Relationship state is symmetric by design: each party holds the same
      stream with the same objects.

  Cons:
    - One more stream type / object type.
    - Relationship discovery requires direct communication; a third party
      cannot verify relationships between peers A and B by querying
      rendezvous. (Depends on use case; not always a con.)
    - Adds streaming state management (per-relationship).

Option B: Identity stream + optional encryption, rendezvous does not serve
relationship objects

  Assertions and terminations remain in the identity stream (per v0.6.2), but
  the rendezvous API is restricted: GET /v1/identity/{peer_id} returns only
  IdentityDocument, KeyRevocation, and IdentityContinuity, never
  RelationshipAssertion/Termination.

  Pros:
    - Keeps all peer state in one stream.
    - Existing logic unchanged.
    - Third-party verifiers can still see the peer's identity.

  Cons:
    - Identity stream still grows with relationships (though they're not
      served).
    - Rendezvous must filter served objects; adds a filtering rule.
    - Clients must use out-of-band channels (relay or direct) to discover
      relationships anyway.

Option C: No change; live with the exposure

  Relationships are public. Users who care about anonymity do not use the
  service.

  Pros:
    - No design change.
    - Simpler.

  Cons:
    - Violates the design's spirit ("no infrastructure authority, but also
      no incidental mega-leaks").
    - Creates a user-visible privacy cliff.

Recommendation:
Accept Option A (per-relationship streams). Closes H1. Simplifies identity
and relationship state management. Adds clarity to the wire protocol.

Consequences:
  - D-01: add stream:relationship:<relationship_id> to the text-name model.
  - OBJECTS.md: move RelationshipAssertion and RelationshipTermination to
    relationship streams; remove them from identity stream.
  - §7: update the relationship state machine; note that RECOGNIZED requires
    holding both sides' assertion streams.
  - Rendezvous API (D-20): specifies how relationship streams are exchanged
    (direct endpoint, relay, encrypted channel).
  - Test vectors: pairing produces relationship stream; assertions and
    terminations in that stream only.
  - Wire protocol (D-21): specifies transport for relationship-stream objects
    between peers.

================================================================================
