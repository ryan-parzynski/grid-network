# Grid Network — Decision Log

**Revision:** 2.3
**Protocol version:** v0.6.3

This document records every design decision made for the protocol, with
its rationale and consequences. It is non-normative. Where a decision
conflicts with the Protocol Specification, the specification governs.

Each entry has a stable title. Numbering is for reference only and does
not imply priority.

---

## D1. Peer IDs are opaque, not self-certifying

**Decision.** A Peer ID is a random opaque identifier, not a hash of
the identity root public key.

**Rationale.** A self-certifying ID cannot rotate the identity root
without changing the ID. Since root rotation is required for key
compromise recovery and algorithm migration, self-certifying IDs would
force either never rotating or accepting that rotation changes the
peer's identity. Neither is acceptable.

**Consequence.** An extra object — the identity document — is required
to bind the Peer ID to the identity root. The cost is one verification
step. The benefit is rotation without identity change.

---

## D2. Relationships are per-principal assertions, not bilateral objects

**Decision.** Recognition between two principals is expressed by a pair
of independently signed `RelationshipAssertion` objects, one published
by each principal in its own identity stream.

**Rationale.** A bilateral object raises the question of which stream
owns it. Every candidate answer creates either a new stream that is
signed by two authorities, or a convention that the object is
co-signed, or an ordering problem. Per-principal assertions keep every
object in exactly one stream, signed by exactly one authority.

**Consequence.** Recognition is verifier-derived state, not a stored
object. The verifier binds the two assertions by `relationship_id` and
requires mutual naming.

---

## D3. Relationship termination is unilateral

**Decision.** Either principal may terminate a relationship by
publishing a `RelationshipTermination`.

**Rationale.** Recognition cannot be coerced. A principal that wishes
to withdraw recognition must be able to do so without the other
principal's consent.

**Consequence.** A termination is terminal. Re-establishing requires a
new `relationship_id`.

---

## D4. Identity Continuity requires dual signatures

**Decision.** The object that transitions the identity root is signed
by both the old root and the new root.

**Rationale.** Neither root alone should be able to claim continuity.
If only the new root signs, an attacker who has generated a new key
can claim continuity. If only the old root signs, the new root has no
say. Requiring both signatures means only a transition both parties
agree to is accepted.

**Consequence.** Root rotation requires both keys to be available at
the time of transition. For deployments where the old root is offline,
this requires a planned handover.

---

## D5. Chain hash is cumulative

**Decision.** The `chain_hash` of an object commits to the entire
stream history, not just to the previous object.

**Rationale.** A chain hash that commits to the entire stream history
binds each object to the history that precedes it. Because the
signature covers `chain_hash`, an object cannot be moved onto a
different history without invalidating its signature. Two verifiers can
compare a single `chain_hash` value at a given sequence to determine
whether they hold the same history.

**Consequence.** Each object carries one additional hash value. The
per-object computation cost is constant, because it depends only on the
previous chain hash and the object's commitment. The chain hash does
not reveal a fork to a verifier that has seen only one branch. Fork
detection requires observing two conflicting objects at the same
sequence (`OBJECTS.md` §9.3).

---

## D6. Sequence spaces are disjoint

**Decision.** Each stream has its own sequence space. Sequence numbers
from different streams are never compared.

**Rationale.** Global sequence numbers would require global
coordination. Two issuers signing objects simultaneously would have to
agree on ordering, which requires consensus. The protocol does not have
consensus.

**Consequence.** A verifier must never compare sequence numbers across
streams. Each stream maintains its own order. This is a discipline
requirement and must be enforced by implementation.

---

## D7. Authorization Keys own one heterogeneous stream

**Decision.** Each Authorization Key signs grants, leases, and lease
revocations into a single stream `stream:authorization:{auth_key_id}`.

**Rationale.** Splitting grants, leases, and revocations into separate
streams would require either three keys per authority or a rule that a
single key signs into three streams. Both add complexity without
benefit. A single stream per key is simpler and correctly sequences the
objects the key is responsible for.

**Consequence.** A stream contains a mix of object types. The verifier
must dispatch by `domain_separator`.

---

## D8. KeyRevocation is signed by the Identity Root

**Decision.** A `KeyRevocation` for a subordinate key is signed by the
Identity Root and published in `stream:identity`.

**Rationale.** A compromised key cannot be trusted to sign its own
revocation. The Identity Root is the only authority above the
compromised key.

**Consequence.** Revoking an Authorization Key requires the Identity
Root to be available. For deployments where the root is offline, a
break-glass procedure is required.

---

## D9. GrantRevocation is signed by the Identity Root

**Decision.** A `GrantRevocation` is signed by the Identity Root and
published in `stream:identity`.

**Rationale.** A compromised Authorization Key must not be able to
prevent its own revocation. If the AuthKey that issued a grant also
signs the revocation of that grant, a compromised AuthKey could refuse
to revoke. The Identity Root is the correct authority.

**Consequence.** This decision supersedes the earlier signing matrix
that placed `GrantRevocation` in the Authorization Key's stream. The
signing matrix in the Protocol Specification reflects this decision.

---

## D10. Failure never grants authorization

**Decision.** Missing information never grants access. Every check
that fails denies access.

**Rationale.** A system that grants access on ambiguous state is
unpredictable under attack. Fail-closed is the safe default.

**Consequence.** A verifier that cannot reach a rendezvous server for
a freshness check does not grant access. It does, however, continue to
use cached authorization for peers whose state it already holds. The
distinction is between unknown state (deny) and stale state (allow
within `max_offline_tolerance`).

---

## D11. Revocation is terminal

**Decision.** Once revoked, an object cannot be un-revoked.
Re-establishing requires a new object.

**Rationale.** Reversible revocation creates a class of subtle bugs.
An un-revocation must be signed, distributed, and trusted; it
reintroduces the state that revocation removed. Races between
revocation and un-revocation are exploitable.

**Consequence.** Temporary revocation is expressed with short leases.
Permanent revocation is expressed with a terminal object. An
accidental revocation requires issuing a new grant.

---

## D12. StreamResolution requires pre-fork authority

**Decision.** A `StreamResolution` must be signed by an authority
that appears in the forked stream's history at the forked sequence.

**Rationale.** A key whose own stream is disputed cannot be trusted to
resolve the dispute unilaterally. The resolution must come from the
authority that signed the disputed history.

**Consequence.** If the required signing key is lost, the fork is
unrecoverable. This is a design limit, not a bug.

---

## D13. Service Link is referential only

**Decision.** A `ServiceLink` is a reference from one service to
another. It is not an authorization object.

**Rationale.** Adding a second authorization primitive would duplicate
the grant model and introduce ambiguity about which primitive governs.
A link is a reference; authorization is by grant.

**Consequence.** A service that depends on another service does not
gain authorization through the link. The subject that needs access
must hold a grant.

---

## D14. Service ownership transfer is not in the current protocol version

**Decision.** There is no mechanism for transferring a service from
one principal to another.

**Rationale.** A transfer requires an authenticated object signed by
both parties, a definition of what happens to outstanding grants, and
a resolution for in-flight leases. None of these are defined.

**Consequence.** A service that needs to move to a different principal
must be decommissioned and re-registered under the new principal.
Service ownership transfer is a `planned` feature.

---

## D15. Grant validity is absolute; lease validity is relative

**Decision.** A grant's validity is expressed as an absolute time
window. A lease's validity is expressed as a duration measured from
the verifier's observation.

**Rationale.** A grant is an issuance event. Its validity is a property
of the issuance, decided by the issuer, independent of when any
verifier sees it. A lease is an ongoing state. Its validity is a
property of the verifier's observation.

**Consequence.** Clock skew affects grants but not leases. A verifier
whose clock is wrong may reject a valid grant by comparing times
incorrectly. A verifier's clock does not affect lease validity.

---

## D16. `max_offline_tolerance` bounds freshness, not lease validity

**Decision.** `max_offline_tolerance` is a separate bound from the
lease duration. It is measured from the verifier's last successful
contact with the subject.

**Rationale.** Keeping the two bounds separate keeps the layers clean.
The lease duration is a property of the lease. The offline tolerance is
a property of the verifier's relationship with the subject.

**Consequence.** A subject may have a valid lease and still be
unauthorized because it has exceeded `max_offline_tolerance`.

---

## D17. Revocation is state, not event

**Decision.** A revocation received before its target is cached and
applied when the target arrives.

**Rationale.** An event-based model requires that revocation and its
target arrive in a specific order. State-based models are order-
independent.

**Consequence.** A verifier's local state includes a set of revoked
object identifiers, which grows over time. Implementations should
manage this set with appropriate pruning.

---

## D18. Ed25519 and SHA-256

**Decision.** Ed25519 for signatures, SHA-256 for hashes.

**Rationale.** Ed25519 has formal security proofs, is widely deployed,
is fast, and produces small signatures. SHA-256 is well understood with
no known collisions.

**Consequence.** Both are vulnerable to quantum attacks. A post-quantum
signature suite is a `planned` feature.

---

## D19. Deterministic CBOR with strict canonicalization

**Decision.** All protocol objects are encoded in deterministic CBOR
with the canonical rules defined in `OBJECTS.md §2`.

**Rationale.** JSON has map-ordering ambiguity that prevents canonical
encoding. Protobuf has multiple valid encodings for the same value.
CBOR with strict rules produces one canonical form for each semantic
value.

**Consequence.** Every object has exactly one valid byte
representation. Test vectors are byte-exact.

---

## D20. No version field in signed objects

**Decision.** The schema version is carried by the `domain_separator`
field. There is no separate version field.

**Rationale.** A separate version field would duplicate the version
information and create a possibility of disagreement between the two.

**Consequence.** Any schema change requires a new domain separator. A
future version of the same object family uses a distinct separator.

---

## D21. Domain separators are part of the signed payload

**Decision.** The `domain_separator` is included in
`commitment_preimage`, `payload_id`, and `signature_input`.

**Rationale.** If the separator were external to the signature, an
attacker could take a signature over an object of one type and reuse
it on an object of another type. Including the separator in the
signature input prevents this.

**Consequence.** Every cryptographic construction is domain-separated.
The tags are registered in `OBJECTS.md §3.13`.

---

## D22. Payload ID and Object ID use distinct framing

**Decision.** `payload_id` and `object_id` are distinct values with
distinct domain tags.

**Rationale.** `payload_id` identifies semantic content. `object_id`
identifies a specific signed artifact. A revocation must reference the
specific artifact it revokes; a deduplication check may reference
semantic content. Both relationships are expressible when both
identifiers exist.

**Consequence.** An implementation must compute both. Neither is a
substitute for the other.

---

## D23. The protocol is free; development is funded by commercial revenue

**Decision.** The protocol specification is free to use, implement,
and modify. Development of the specification is funded by a revenue
share from commercial operators.

**Rationale.** Free use and free maintenance are distinct. A protocol
that is free to use but unfunded cannot sustain maintenance,
audits, and evolution.

**Consequence.** The commercial model exists to fund the specification
and ecosystem, not to extract value from users.

---

## D24. The commercial layer sells guarantees, not access

**Decision.** Free users get full functionality with best-effort
bandwidth. Paid users get guaranteed bandwidth and priority.

**Rationale.** Selling access would create a captive market.
Selling guarantees lets free users use the network and lets paid users
buy predictability.

**Consequence.** Free users make the network valuable by contributing
reachability, peer-to-peer efficiency, and ecosystem gravity. Paid
users fund the infrastructure that all users benefit from.

---

## D25. Idle commercial capacity flows to the free pool

**Decision.** When paid users do not use their reserved capacity, the
idle capacity is available to free users.

**Rationale.** Overprovisioning benefits everyone. The operator
provisions for peak paid load; the trough is free.

**Consequence.** Free users get better service during off-peak hours.
Paid users are unaffected because their reservations are guaranteed.

---

## D26. Priority is a ticket property, not a user identity

**Decision.** Relay tickets carry a `priority_class`. The relay
enforces priority by ticket, not by identifying the requester.

**Rationale.** Making priority a property of the ticket preserves
privacy, portability, and composability. A user can hold tickets of
different classes; the class travels with the ticket.

**Consequence.** A relay cannot prefer a specific user; it prefers
tickets of a specific class. This is the correct privacy property.

---

## D27. Credits are bound to a pool, not freely transferable

**Decision.** Credits earned by running a relay accrue to an
account. They may be allocated to a pool. They may not be transferred
arbitrarily between accounts.

**Rationale.** Free transferability would create a market for credits
and introduce laundering, regulatory, and tax complexity. Binding to a
pool preserves the sharing benefit without those complications.

**Consequence.** A user who wants to share credits with another user
does so through a shared pool, not a peer-to-peer transfer.

---

## D28. Operator-agnostic credits are a design goal

**Decision.** The credit system is designed so that a contribution to
one operator is valuable at another operator.

**Rationale.** A credit system that locks contributions to a single
operator recreates the vendor lock-in the protocol is designed to
prevent.

**Consequence.** Cross-operator settlement is a `planned` feature. In
the current protocol version, credits are operator-local.

---

## D29. Geographic scarcity multiplies credit value

**Decision.** Credits earned in scarce regions are multiplied by a
factor greater than one.

**Rationale.** Scarce regions have fewer relays and higher demand.
Operators who deploy in scarce regions earn more, which draws
infrastructure to where it is needed.

**Consequence.** The multiplier is set by the operator's policy, not
by the protocol. The protocol defines the credit model; it does not
define the multiplier.

---

## D30. No blockchain for credit settlement

**Decision.** The protocol does not use a blockchain for credit
settlement.

**Rationale.** The number of operators is small. A blockchain would
add latency, cost, and complexity without solving a problem. Signed
receipts and notarized records suffice.

**Consequence.** Cross-operator settlement requires trust in the
receipts. This is a `planned` feature; the protocol does not yet define
it.

---

## D31. Developer funding is structural

**Decision.** Commercial operators contribute a fixed fraction of
revenue to developer funding.

**Rationale.** Donations and grants are volatile. A structural revenue
share scales with adoption and provides predictable funding.

**Consequence.** The share is a policy parameter. The default is
`DEFAULT_DEVELOPER_FUND_SHARE`.

---

## D32. The stewardship entity is independent of operators

**Decision.** A stewardship entity, separate from any operator,
maintains the specification.

**Rationale.** Operator control of the specification would create a
commercial capture. An independent entity represents all operators and
users.

**Consequence.** The stewardship entity is a `planned` institution.
The protocol does not define its composition, funding, or authority.
Its decisions are external to the specification.

---

## D33. The name is Grid Network

**Decision.** The protocol and its ecosystem are named Grid Network.

**Rationale.** The name is descriptive, uncollided, memorable,
scalable across audiences, and aligned with the design's distributed
topology.

**Consequence.** Earlier working names are retired.

---

## D34. Applications are the primary adoption path

**Decision.** Applications integrate the protocol on behalf of users.
Users receive connectivity through applications.

**Rationale.** Users do not adopt protocols. They adopt products. The
protocol's path to broad adoption is through applications that
integrate it the way they integrate authentication.

**Consequence.** The design prioritizes developer ergonomics over
end-user operations.

---

## D35. Composition over invention

**Decision.** The protocol composes mechanisms from prior systems
rather than inventing new ones.

**Rationale.** Each borrowed mechanism is well-proven. The novelty is
in the composition.

**Consequence.** The design's contribution is the way the pieces are
combined, not the pieces themselves. The lineage document records what
was borrowed from which system.

---

## D36. Rendezvous serves identity state

**Decision.** Rendezvous servers accept and serve identity documents
and `IdentityContinuity` objects, in addition to reachability records.

**Rationale.** The protocol assumes identity state propagates through
peer-to-peer contact. This fails when peers are disconnected, which is
exactly when synchronization matters most. Without rendezvous serving
identity state, a peer that has not communicated with another peer in
months cannot verify that peer's current state.

**Consequence.** Rendezvous infrastructure holds slightly more state
than originally described. The state is signed, so the rendezvous
remains untrusted. Peers that cannot reach any rendezvous server still
cannot refresh state; that limitation remains.

---

## D37. Reachability records carry freshness fields

**Decision.** `ReachabilityRecord` carries `published_at` and
`identity_sequence`.

**Rationale.** A verifier that fetches a reachability record has no
way to know whether its cached copy of the publisher's identity
document is current. With `identity_sequence`, the verifier can
compare: if the cached sequence is lower than the record's claimed
sequence, the verifier knows to refresh before using the record.

**Consequence.** The verifier detects mismatch and refreshes. The field
is a hint for cache invalidation, not a proof of freshness. Detection
of stale identity state requires either multi-rendezvous comparison or
the continuity chain.

---

## D38. "Frozen" is retired; stability markers replace it

**Decision.** The specification is not "frozen". Sections carry a
stability marker: `stable`, `under-review`, or unmarked.

**Rationale.** The specification is a living document. It changes as
the review cycle produces corrections and as the protocol evolves.
Calling it frozen while patching it created a class of contradictory
findings.

**Consequence.** A `stable` section requires a protocol-version bump
to change. An `under-review` section may change freely. Unmarked
sections are unconstrained. The revision model is described in
`VERSIONING.md`.