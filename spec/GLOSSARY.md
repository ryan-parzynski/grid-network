# Grid Network — Glossary

**Revision:** 2.2
**Protocol version:** v0.6.3

Terms are listed alphabetically. Each definition is one sentence or a
short paragraph. Where a term has a normative definition elsewhere, the
section is cited.

---

## A

**Application layer.** The layer above the protocol. Handles user
identity, roles, and resource policy. The protocol does not define
application-layer authorization.

**Authorization Key.** A key delegated by the Identity Root to sign
grants, leases, and lease revocations. Published in
`stream:authorization:{auth_key_id}`. Separate from the Identity Root
and from every device and service key.

**Authorization stream.** The sequence space for a single Authorization
Key. Contains grants, leases, and lease revocations. Sequence space:
`(auth_key_id, stream:authorization)`.

**Authority domain.** One of six partitions of responsibility: identity,
authorization, reachability, rendezvous, relay, application. No domain
may escalate into another.

## B

**Base state.** The initial chain state of a stream. Represented by
`initial_chain_hash`, computed per `OBJECTS.md §3.6`.

**Blast radius.** The set of capabilities affected by the compromise of
a specific key. Documented per key role.

## C

**Capability.** A scoped authorization target within a grant. Composed
of `namespace`, `action`, and `resource`, each a text string.

**Chain hash.** The cumulative hash of a stream's history up to and
including the current object. Computed per `OBJECTS.md §3.8`. An object
field.

**Commitment preimage.** The byte string hashed to produce
`object_commitment`. Computed per `OBJECTS.md §3.4`.

**Compromise model.** How damage from key compromise is bounded.
Implemented through key-role separation and `effective_sequence`.

**Conformance.** Agreement with the specification's stated requirements
and test vectors. Defined in Protocol §44.

**Credits.** An accounting unit in the commercial model. Not part of
the protocol. A credit represents one gigabyte of relay usage at the
standard tier, or an equivalent value at another tier.

## D

**Device.** A machine or process holding a device key. Authorized by
`device_bindings` in the identity document.

**Device key.** A key held by one device, used to sign reachability
records. Separate from every other key role.

**Domain separator.** A text string identifying an object's schema
family and version. Part of the signed payload. Registered in
`OBJECTS.md §5`.

## E

**`effective_sequence`.** The sequence number at or after which objects
signed by a revoked key are invalid. Part of a `KeyRevocation`.

**Envelope.** The common fields on every signed object:
`domain_separator`, `sequence`, `previous_hash`, `chain_hash`,
`signature`. Defined in `OBJECTS.md §4`.

## F

**Fail-closed.** The principle that missing information denies access.
Failure never grants authorization. See Protocol §39 (F1).

**Fork.** Two objects in the same stream with the same `sequence` and
different `chain_hash`. Requires explicit resolution.

## G

**Grant.** A signed authorization from one principal to another. Names
a relationship, a subject, a set of capabilities, and a lease policy.
Signed by an Authorization Key. Published in
`stream:authorization:{auth_key_id}`.

**GrantRevocation.** A signed terminal invalidation of a grant. Signed
by the Identity Root. Published in `stream:identity`.

**Grid agent.** Local software that holds keys, verifies objects, and
exposes an API to applications. Not part of the protocol; defined in
the Operator Guide.

**Grid URI.** A `grid://` URI referring to a principal, service, or
capability. Format defined in Protocol §22.

## H

**Hardware-backed key.** A key stored in a secure element or enclave.
Recommended for the Identity Root.

## I

**Identity.** Who controls a keypair. In Grid Network, identity is a
keypair bound to a Peer ID by a signed identity document.

**Identity Continuity.** An object that transitions the Identity Root
from one key to another. Signed by both roots. Defined in Protocol §40.

**Identity document.** The object that binds a Peer ID to an Identity
Root and lists the principal's authorized keys, devices, and services.
Published in `stream:identity`.

**Identity Root.** The highest cryptographic authority for a principal.
Signs identity documents, relationship assertions, revocations, and
identity continuity. Should normally remain offline or hardware-
protected.

**Identity stream.** The sequence space for a single principal's
identity objects. Sequence space: `(peer_id, stream:identity)`.

## K

**Key Binding.** A record within an identity document that names a
public key and its role. Part of `IdentityDocument`.

**Key revocation.** A signed terminal invalidation of a subordinate
key. Carries `effective_sequence`. Signed by the Identity Root.
Published in `stream:identity`.

**Key role.** The purpose a key serves. One of: identity root, device,
service, authorization, recovery. A single key MUST NOT serve more
than one role.

## L

**Lease.** A signed proof that a grant is currently valid. Carries
either `valid_until_absolute` or `valid_for_duration`. Signed by the
Authorization Key that issued the grant.

**Lease revocation.** A signed terminal invalidation of a lease.
Signed by the Authorization Key. Published in
`stream:authorization:{auth_key_id}`.

## M

**`MAX_LEASE_AGE`.** A configurable bound on the age of a lease,
measured from its `issued_at`. Default: twice the lease's nominal
duration. See `PARAMETERS.md`.

**`max_offline_tolerance`.** A per-grant bound on how long a subject
may be offline before the verifier denies access. Measured from the
verifier's last successful contact with the subject.

## O

**Object commitment.** The hash of the commitment preimage. Appears in
the next object's `previous_hash`.

**Object ID.** The hash of the signed object's canonical bytes.
Distinct from `payload_id`.

**Observation time.** The verifier's monotonic clock reading when it
first accepts an object. Used to measure relative lease validity.

**Operator Manifest.** A signed declaration of a relay or rendezvous
operator's capabilities. Includes `serves_identity_state` and
`current_relay_authority_key`.

## P

**Payload ID.** The hash of the semantic content of an object's
unsigned payload. Not unique per stream position.

**Peer.** A principal or a device participating in the protocol.

**Peer Principal.** A durable logical identity that may span multiple
devices, services, and locations.

**Peer Principal ID.** An opaque random identifier. Format:
`peer:v1:<base32>`.

**Priority class.** A property of a relay ticket. One of `free`,
`standard`, `priority`, `dedicated`.

## R

**Reachability.** The ephemeral signed hint about where a device can be
reached. Not part of identity.

**Reachability record.** A signed object naming a device's current
endpoints. Signed by the device key. Published to rendezvous servers.

**Recognition.** The bilateral relationship state between two
principals. Derived by the verifier from two signed assertions.

**Relationship.** An explicit pairing between two principals. Expressed
by a pair of `RelationshipAssertion` objects.

**Relationship assertion.** A unilateral signed statement by one
principal that it recognizes another. Published in `stream:identity`.

**Relationship termination.** A unilateral signed statement by one
principal that it terminates a relationship. Terminal.

**Relative validity.** Lease validity measured from the verifier's
observation, not from wall-clock time. Survives clock skew up to the
duration.

**Relay.** Infrastructure that forwards encrypted traffic between two
peers when direct connection fails. Pair-bound and untrusted.

**Relay ticket.** A signed authorization to use a relay for a specific
pair of devices, with a byte capacity and a duration.

**Rendezvous server.** Infrastructure that stores ephemeral protocol
state (reachability records, identity documents) on behalf of peers.
Untrusted.

**Rendezvous Manifest.** A signed list of the rendezvous servers a
principal currently publishes to. Published in `stream:identity`.

## S

**Service.** A named endpoint within a principal. Holds a service key.

**Service binding.** A record within an identity document that names a
service. Part of `IdentityDocument`.

**Service key.** A key held by one service, used to sign service
records.

**Service record.** A signed object naming a service's type, endpoint,
and metadata. Published in `stream:service:{service_id}`.

**Service stream.** The sequence space for a single service. Sequence
space: `(service_id, stream:service)`.

**Signature input.** The exact byte string that is signed. Computed per
`OBJECTS.md §3.12`.

**Stability marker.** A per-section label: `stable` or `under-review`.
`stable` sections do not change without a protocol-version bump.

**Stream.** An ordered sequence of cryptographically linked objects
sharing one sequence space and one signing authority.

**Stream ID.** The canonical CBOR encoding of a stream's sequence-space
identifier. Format defined in `OBJECTS.md §3.6`.

**StreamResolution.** A signed object that resolves a fork in a stream.
Signed by the authorities that appear in the forked history.

## T

**Terminal.** A state that cannot be un-reached. Revocation and
relationship termination are terminal.

**Test vector.** A byte-exact example used to define conformance.

**Trust anchor.** A key a verifier starts with. Types: self,
relationship, credential (deferred).

## V

**Verifier.** A device or process that decides whether to grant access
to a peer.

**Verifier local state.** The cached knowledge a verifier maintains for
decision-making. Includes identity state, relationship state, grant and
lease state, revocations, and observation records.

## W

**WireGuard.** A transport protocol used by Grid Network implementations.
Grid does not define WireGuard; it uses it.