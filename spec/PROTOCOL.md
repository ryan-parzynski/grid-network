# Grid Network Protocol Specification

**Revision:** 2.1
**Protocol version:** v0.6.2
**Status:** Sections marked `stable` are normative and will not change
without a protocol-version bump. Sections marked `under-review` carry a
known defect or open question and must not be built against yet.
Unmarked sections are the default state.

---

## Abstract

Grid Network is an open protocol for establishing persistent, mutually
authenticated relationships between machines and services without
requiring permanent accounts, centralized identity providers, fixed
network locations, a single source of truth, or continuous presence of
a coordinator.

Participants establish identity, authorization, and reachability
independently, using cryptographic signatures and locally verifiable
state.

---

## Normative order

The Protocol Specification is normative. The Design Record, Roadmap,
and Operator Guide are informative. Where an informative document
conflicts with this specification, this specification governs. Where a
section carries the `under-review` marker, its rule is subject to
change and the section's current text governs only until the next
revision.

---

## Conventions

- MUST, MUST NOT, SHOULD, SHOULD NOT, MAY are used per RFC 2119.
- **Document revision** is the version of this specification (e.g.,
  2.1). It advances whenever the document changes.
- **Protocol version** is the feature set this specification defines
  (e.g., v0.6.2). Implementations conform to a protocol version, not a
  document revision.
- **Feature status.** Every feature that is not in the current protocol
  version is labeled with a feature name and one status word:
  `planned`, `deferred`, or `unscheduled`.
- **Examples.** Example principals are named Alice, Bob, and Charlie.
  Example devices are named by role (Alice's laptop, Bob's phone) or
  by symbol (Device A, Device B).
- **Cross-references.** References within this document use `§N.M`.
  Cross-document references use the document name: `[RECORD §3.2]`,
  `[ROADMAP §2]`, `[GUIDE §4.1]`.
- **Parameters.** Every tunable value in a rule is a symbol defined in
  `PARAMETERS.md`. Literal values do not appear in normative text.
- **Stability markers.** `stable` and `under-review`, per the status
  line above.

---

## 1. The core security invariant

> Given a set of locally trusted anchors, authenticated protocol
> objects, known revocations, accepted chain state, and recorded
> observation history, a verifier must be able to deterministically
> establish the identity, authorization, validity, and freshness state
> of a peer as of the verifier's most recent observation, without
> contacting an authority.

This invariant means:

1. Rendezvous infrastructure cannot define identity.
2. Relays cannot define authorization.
3. DNS cannot define identity.
4. IP addresses cannot define identity.
5. WireGuard keys cannot by themselves define application-level
   authorization.
6. Temporary pairing codes cannot become permanent credentials.
7. Heartbeat activity cannot establish freshness; only an explicit
   lease can.
8. Infrastructure disappearing must not invalidate existing
   authorization.
9. Contacting an authority must not be required to verify
   authorization.

Corollaries:

- A system that requires calling home to verify has failed the
  invariant.
- A system where a relay can grant access has failed it.
- A system where a rendezvous server is the source of truth has failed
  it.
- A system where a device loses its identity when offline has failed
  it.

---

## 2. Design goals

**Primary goals**

1. Persistent cryptographic identity.
2. Replaceable physical devices.
3. Explicit peer relationships.
4. Scoped authorization.
5. Short-lived authorization leases.
6. Terminal revocation.
7. Key rotation.
8. Offline verification.
9. Replaceable rendezvous infrastructure.
10. Transport independence.
11. Human-friendly initial pairing.
12. Self-hostable infrastructure.
13. No mandatory central account provider.
14. Deterministic security state.
15. Interoperable implementations.

**Secondary goals**

1. Multiple devices per principal.
2. Multiple services per device.
3. Service-specific authorization.
4. Temporary guest access.
5. Delegated administration.
6. Groups and team management.
7. Multiple rendezvous providers.
8. Direct peer-to-peer connectivity.
9. Relay fallback.
10. Local-first operation.
11. Identity portability.
12. Hardware-backed keys.
13. Key sharding and threshold recovery (feature: `threshold-recovery`;
    status: `deferred`).
14. Graceful degradation.
15. Continuous availability during update.
16. Minimal metadata leakage.

**Non-goals**

- A replacement for WireGuard. Grid uses it as transport.
- A general-purpose VPN.
- A global DNS replacement.
- A universal application authorization framework.
- A blockchain.
- A global identity registry.
- A mandatory centralized account system.
- A mandatory DHT.
- A permanent network locator.
- A substitute for application-level authentication.
- An anonymity network.
- A public endpoint directory.
- A global event log.
- A guarantee that direct connectivity always succeeds.

---

## 3. Peer Principal

A durable logical identity. The "who" that controls a set of devices
and services.

A peer principal is not one machine, one operating system, one device
key, one service, or one person. It is a logical entity that may span
multiple devices, multiple services, or an organization, and that may
change devices, replace keys, and change locations without changing
identity.

Example principal and its devices:

    Peer Principal: "Alice's home network"
    ├── Home server
    │   ├── Media service
    │   ├── File service
    │   └── Backup service
    ├── Laptop
    │   └── Shell service
    ├── Phone
    └── Home automation controller

The Peer Principal ID ties these together.

---

## 4. Peer Principal ID

A random, opaque identifier. Example:

    peer:v1:7f3a9c2e5d91b0a4c7e8126fa31d449b

The identifier is not self-certifying (not a hash of the public key).
This is deliberate.

Why opaque, not self-certifying:

A self-certifying ID, such as a hash of the identity root public key,
cannot rotate the identity root without changing the ID. Because root
rotation is a core requirement — for key compromise recovery, for
algorithm migration, for any change of cryptographic construction —
self-certifying IDs would force either never rotating or accepting
that rotation changes the peer's identity. Neither is acceptable.

Grid Network binds the Peer ID to an identity root through a signed
identity document. When the root rotates, a new identity document is
published, signed by both the old and new roots. The Peer ID is
unchanged.

Advantages:

- Identity root rotation without ID change.
- Provisioning before key generation.
- Cryptographic constructions can change in future versions.
- Identifiers do not expose the construction.
- Relationships remain stable through root rotation.

---

## 5. Identity Root

The highest cryptographic authority for a principal. The Identity Root
establishes the identity document, authorizes device and service keys,
delegates authorization authority, rotates and revokes subordinate
keys, recovers from subordinate key compromise, and establishes
relationships with other principals.

The Identity Root should normally remain offline or hardware-protected.
It should not participate in routine network sessions. It appears only
in identity documents, key revocations, relationship assertions, key
delegation certificates, and identity continuity objects.

For deployments where the root must remain online (for example, a solo
user's single-device deployment), the risk is that root compromise
gives an attacker the entire principal. The deployment guidance
recommends hardware-backed keys for such cases.

---

## 6. Key roles

A single private key must not be used for more than one role.

                    Identity Root (offline)
                          │
                          │ signs
             ┌────────────┼────────────┐
             │            │            │
         Device Key   Authorization   Recovery Key
             │           Key              │
        ┌────┴────┐      │            (offline)
        │         │      │
   Service Key  ...    Grants
                       │
                     Leases
                       │
                    Revocations

Role definitions:

| Role | Owner | Usage | Separation |
|------|-------|-------|-----------|
| Identity Root | Principal | Signs identity docs, relationships, revocations | Separate from Device and Auth |
| Device Key | One device | Authenticates device, signs reachability | Separate from Service |
| Service Key | One service | Authenticates service, signs service records | Separate from Device |
| Authorization Key | Delegated | Signs grants, leases, revocations | Own stream |
| Recovery Key | Principal | Threshold recovery (deferred) | Offline |

Minimum required separations:

1. Identity Root ≠ Device Key.
2. Identity Root ≠ Authorization Key.
3. Device Key ≠ Service Key.
4. Any role ≠ Recovery Key.

Why non-reuse matters:

If one key serves multiple roles, compromise of that key compromises
every role. Device key compromise lets an attacker forge reachability,
which is untrusted anyway; authorization and service identity are
unaffected. Authorization key compromise lets an attacker forge grants
and leases, bounded by `effective_sequence`; identity and reachability
are unaffected.

---

## 7. Identity Documents

The object that binds a Peer ID to an Identity Root and its subordinate
keys.

    IdentityDocument {
        domain_separator = "grid/identity-document/v1"

        sequence
        previous_hash?
        chain_hash
        signature

        peer_id
        identity_root
        authorized_keys : set<KeyBinding>
        device_bindings : set<DeviceBinding>
        service_bindings : set<ServiceBinding>
        issued_at
        not_before
        expires_at?
    }

    KeyBinding {
        key_role : enum(identity_root, device, service, auth, recovery)
        public_key
        effective_sequence : sequence number
    }

    DeviceBinding {
        device_id
        device_key
        device_name?
    }

    ServiceBinding {
        service_id
        service_key
        service_name
        service_url?
    }

Key collections are canonical sets: ordered by bytewise lexicographic
comparison of their canonical CBOR encodings, with no duplicates.

Identity documents occupy `stream:identity`. The stream is a linear
signed history: Document 1 → Document 2 → Document 3.

Two documents with the same `peer_id` and `sequence` but different
`chain_hash` constitute a fork. Resolution is defined by
`StreamResolution` (§42).

---

## 8. Relationship model

Recognition between two principals is expressed by a pair of
independently signed `RelationshipAssertion` objects, one published by
each principal.

Each principal publishes its own assertion in its own `stream:identity`.
There is no bilateral object. Recognition is verifier-derived state.

    RelationshipAssertion {
        domain_separator = "grid/relationship-assertion/v1"

        sequence
        previous_hash?
        chain_hash
        signature

        relationship_id : uuid
        subject_principal : peer_id
        issued_at
        not_before
        expires_at?
    }

Signed by the issuer's Identity Root. Published in the issuer's
`stream:identity`. `subject_principal` is the other principal being
recognized.

Semantics: the issuer recognizes `subject_principal` under
`relationship_id`. Unilateral. Does not establish RECOGNIZED by itself.

    RelationshipTermination {
        domain_separator = "grid/relationship-termination/v1"

        sequence
        previous_hash?
        chain_hash
        signature

        relationship_id : uuid
        reason : text string
        terminated_at
    }

Signed by the terminating principal's Identity Root. Published in the
terminating principal's `stream:identity`. Unilateral. Either principal
may terminate.

**Verifier-derived relationship state.**

    PENDING     ← exactly one assertion accepted
    RECOGNIZED  ← both assertions accepted, neither expired, no termination
    TERMINATED  ← accepted RelationshipTermination exists
    UNKNOWN     ← otherwise

Only RECOGNIZED contributes to authorization. PENDING does not.
TERMINATED is terminal; re-establishing requires a new
`relationship_id`.

**Binding requirements.** A verifier MUST bind the two assertions to a
single `relationship_id` and require that the two principals are
mutually named: A's `subject_principal` is B, and B's
`subject_principal` is A. Assertions that do not satisfy this binding
MUST NOT transition the state to RECOGNIZED.

**Termination-first.** If a `RelationshipTermination` is accepted
before both assertions are present, the state transitions directly to
TERMINATED, bypassing PENDING.

---

## 9. Grant

A directional signed authorization. Grants are immutable; any change
produces a new grant with a new `grant_id`.

    Grant {
        domain_separator = "grid/relationship-grant/v1"

        grant_id : uuid
        relationship_id : uuid
        issuer : peer_id
        subject : peer_id

        device_scope? : set<device_id>
        capabilities : set<Capability>
        resources : set<Resource>
        constraints : map<text string, text string>

        lease_policy {
            default_duration : duration
            max_duration : duration
            max_offline_tolerance : duration
        }

        issued_at
        not_before
        expires_at?
        note?

        sequence
        previous_hash?
        chain_hash
        signature
    }

Signed by the issuer's Authorization Key. Published in that key's
`stream:authorization`.

`expires_at`, when present, bounds the grant's own validity. When
absent, the grant does not expire by time; lease renewal is the only
freshness mechanism.

`device_scope`, when present, restricts the grant to specific devices
of the subject principal. When absent, the grant applies to any device
of the subject principal.

---

## 10. Lease

A short-lived proof that a grant is currently valid.

    Lease {
        domain_separator = "grid/authorization-lease/v1"

        grant_id : uuid

        valid_until_absolute? : timestamp
        valid_for_duration?   : duration

        issued_at
        issuer : peer_id

        sequence
        previous_hash?
        chain_hash
        signature
    }

Signed by the Authorization Key that issued the grant. Published in
that key's `stream:authorization`.

Exactly one of `valid_until_absolute` or `valid_for_duration` MUST be
present.

Typical durations (illustrative; the actual values are policy):

- Media streaming: 30 days
- File access: 7 days
- Shell access: 1 hour
- Administrative shell: 15 minutes

Freshness model:

- Grant validity is absolute; the issuer decides the grant lifetime.
- Lease validity is relative by default, measured from the verifier's
  observation.
- Relative validity survives clock skew up to the lease duration.
- `max_offline_tolerance` is a per-grant bound on offline
  authorization.

When a lease expires, the peer is unauthorized until a new lease is
issued. A peer returning from an offline period does not inherit an
expired lease.

**Observation, persistence, and clock source.** A verifier that uses
relative lease validity MUST:

1. Persist observation records to durable storage.
2. Measure elapsed time on a clock that advances during system
   suspend.
3. Treat elapsed time as maximum if elapsed cannot be established —
   for example, if the system boot identifier has changed or the
   observation record was lost — and fail closed.
4. Reject any lease whose `issued_at` is older than `MAX_LEASE_AGE`,
   a configurable bound whose default is twice the lease's nominal
   duration.
5. Preserve the original observation start if the same lease is
   re-observed.

A persisted wall-clock high-water mark may be used as a lower bound on
elapsed time. A verifier without durable storage must not use relative
lease validity.

---

## 11. Capabilities

Authorization is scoped by capability.

    Capability {
        namespace : text string
        action    : text string
        resource  : text string
    }

Namespace rules:

- Lowercase ASCII, dot-separated.
- At least one dot (namespace minimum is `org.X`).
- First component preferably reverse-DNS.
- Unknown namespaces: the verifier MUST validate well-formedness, MUST
  NOT grant access based on an unknown namespace alone, and MAY pass
  the namespace to an application that understands it.

Constraints are a map of text to text, at most `MAX_CAPABILITY_
CONSTRAINTS` entries, each value at most `MAX_CONSTRAINT_VALUE_BYTES`
bytes. Constraints are application-specific and are not interpreted by
the protocol.

---

## 12. Authorization policy

Per-grant policy:

    lease_policy {
        default_duration     : duration
        max_duration         : duration
        max_offline_tolerance : duration
    }

`default_duration` is how long a lease is valid without renewal.
`max_duration` bounds the longest possible lease.
`max_offline_tolerance` bounds how long the subject may be offline
before the verifier denies access.

`max_offline_tolerance` is measured from the verifier's last successful
contact with the subject, on the same clock used for observation time.
Successful contact resets the clock.

---

## 13. Network versus application authorization

The protocol handles the network layer. Applications handle the
application layer.

**Network layer.** May this peer connect?
Grid verifies that a RECOGNIZED relationship exists, that a grant
covers the requested capability, and that a lease is fresh. Result:
connection allowed or denied.

**Application layer.** Once connected, what may the user do?
The application verifies user identity, role, and resource policy.
Result: operation allowed or denied.

Example:

    Network layer (Grid):
      Device verified as Bob's phone.
      Grant permits media.stream.
      Result: connection allowed.

    Application layer (media server):
      User authenticated as "bob".
      Role: viewer.
      Resource: public library permitted, private library not.
      Result: public library served, private library denied.

The protocol does not replace application authorization. Application
authorization does not replace the protocol.

---

## 14. Revocation hierarchy

Revocation is terminal. Once revoked, an object cannot be un-revoked.
Re-establishing requires a new object.

    GrantRevocation {
        grant_id : uuid
        revoked_at : timestamp
    }

    KeyRevocation {
        key_id : uuid
        revoked_at : timestamp
        reason : enum(compromise, rotation, decommission)
        effective_sequence : sequence number
    }

    RelationshipTermination {
        relationship_id : uuid
        terminated_at : timestamp
        reason : text string
    }

All three are signed by the authority that created the original
object, with the exception of `GrantRevocation` (§15).

Why terminal: reversible revocation is a source of subtle bugs.
Temporary revocation is expressed with short leases; permanent
revocation is expressed with a terminal object.

**Propagation.** Revocations are not broadcast. They are pulled. An
issuer publishes a revocation in the appropriate stream. A verifier
polls rendezvous servers, caches what it receives, and applies the
revocation to local state.

There is no guarantee of immediate propagation. The protocol does not
define a bound. See §33.

**Revocation before target.** A revocation received before its target
object is cached. When the target arrives, the cached revocation is
applied. Revocation is state, not event.

---

## 15. GrantRevocation signer and stream

A `GrantRevocation` is signed by the Identity Root and published in
`stream:identity`.

The signer is the Identity Root, not the Authorization Key that issued
the original grant. The reason is that a compromised Authorization Key
must not be able to prevent its own revocation. Publishing in
`stream:identity` preserves the stream-owns-one-authority rule of
§36.

---

## 16. Key revocation and `effective_sequence`

When a key is revoked, objects signed by that key are invalidated
according to the following rule.

An object signed by a revoked key is **invalid** if its sequence is
greater than or equal to `effective_sequence`, **and** the verifier
has an accepted predecessor chain that reaches the object's chain
hash.

An object with sequence below `effective_sequence` is **valid** only
if the verifier had accepted the object's chain hash, or an ancestor of
it, before observing the revocation.

An object with sequence below `effective_sequence` that does not
satisfy the predecessor-chain requirement is **unverifiable** and MUST
be treated as unaccepted.

The predecessor-chain requirement closes a forgery vector: an attacker
holding a compromised key can produce objects at any sequence, but the
verifier will reject any object for which no accepted predecessor chain
exists.

Example:

    Sequence 1: Grant signed by Auth Key (valid)
    Sequence 2: Lease signed by Auth Key (valid)
    Sequence 3: KeyRevocation (effective_sequence = 2)

    Result:
      Grant at sequence 1: valid if the verifier accepted its chain
      hash before observing the revocation.
      Lease at sequence 2: invalid, because sequence ≥ effective_sequence.
      Any object at sequence 3 or later: invalid.

---

## 17. Authorization key compromise recovery

When an Authorization Key is compromised, the Identity Root publishes a
`KeyRevocation` targeting the compromised key with an
`effective_sequence`.

Objects signed by that key at or after `effective_sequence` become
invalid. Objects signed before, whose chain hashes were accepted before
the revocation was observed, remain valid until the grant expires or
the lease expires.

The issuer provisions a new Authorization Key and re-issues grants
under it. There is no in-band recovery for the compromised key itself.

---

## 18. Identity Root compromise

If the Identity Root is compromised, the attacker can forge identity
documents, relationship assertions, key revocations, and grants. The
entire principal is compromised.

The protocol provides no in-band recovery mechanism. Any in-band
recovery mechanism would be an authority the protocol cannot trust.

Recovery is external and out-of-band: the principal contacts peers who
recognized the old identity, proves ownership by a mechanism agreed
outside the protocol, and re-establishes relationships under a new
principal. The protocol defines no recovery authorities, no
proof-of-ownership criteria, and no recovery adjudication procedure.

Threshold recovery is a planned feature. It is not in the current
protocol version.

---

## 19. Key rotation

The Identity Root can rotate subordinate keys without changing the Peer
ID.

1. The existing key continues signing (for example, Device Key A).
2. A new key is authorized (Device Key B) and added to the identity
   document.
3. Both keys are listed during the overlap period.
4. The old key is revoked (a `KeyRevocation` in `stream:identity`).
5. The new key becomes the only active key.

Each key has an `effective_sequence` in the identity document. A
verifier accepts objects from the active key at the effective time.

---

## 20. Pairing

Pairing establishes a cryptographic relationship between two principals
that have no prior knowledge of each other's keys.

Two mechanisms are defined.

**Mechanism 1 — PAKE.** The initiating device generates a
high-entropy random secret and transmits it to the other party through
an out-of-band channel. Both sides run an authenticated key exchange
using the secret as input. The selected PAKE is SPAKE2. The exchange
binds the session to the secret and to a transcript that includes both
principals' identity roots.

**Mechanism 2 — Out-of-band verification.** One side publishes its
public key. The other side verifies the fingerprint through a trusted
channel and issues a relationship assertion. This mechanism is used
for unattended enrollment (§21.4) and for enterprise scenarios where a
provisioning step can pin the peer's fingerprint.

The result of pairing is a set of signed relationship assertions, one
published by each principal in its own `stream:identity`. A session
key is not the durable output; the relationship assertion is.


**Revision:** 2.1
**Protocol version:** v0.6.2

*(Continued from Part 1 of this document. Section numbers continue.)*

---

## 21. Pairing — operational detail

<!-- stability: under-review -->

### 21.1 Three phases

Pairing has three phases with different time bounds.

**Phase 1 — human coordination.** One side displays a code or QR
payload. The other side receives it through an out-of-band channel.
Window: `PAIRING_CODE_VALIDITY`, ten minutes by default.

**Phase 2 — authentication.** Both sides run the PAKE. The exchange
completes in a small number of round-trips once the two sides can
communicate. If they cannot communicate directly, the exchange is
routed through a rendezvous server. The secret is consumed on first
successful use.

**Phase 3 — tunnel establishment.** With authentication complete, the
two sides establish a transport tunnel. This phase has no time bound
imposed by pairing. Direct connection, relay, or waiting for
connectivity all proceed without further user interaction.

Phase 2 and Phase 3 are decoupled. The pairing code's lifetime applies
only to Phase 1 and Phase 2.

### 21.2 Human verification codes

The verification code is derived from the PAKE transcript and displayed
on both devices. Both parties compare the codes through the out-of-band
channel. If the codes do not match, the pairing aborts and both sides
discard the session key.

    PAIRING_VERIFICATION_CODE_DIGITS = 6
    PAIRING_CODE_VALIDITY            = 10 minutes
    PAIRING_PAKE_SECRET_BITS         = 128

A six-digit verification code is a short authentication string. It is
not the PAKE secret. The PAKE secret is a 128-bit random value
generated by the initiating device and transmitted out-of-band.

### 21.3 Confirmation on the receiving side

On receipt of a pairing attempt, the receiving device displays a
confirmation prompt. The prompt shows the pairing session identifier
and, if the initiating device has previously been observed, its
human-readable label. The receiving user confirms or rejects.

Confirmation is a human check that complements the PAKE. It does not
substitute for the PAKE; without the PAKE, an attacker who observes
the out-of-band channel could MITM the exchange.

### 21.4 Unattended enrollment

For headless devices and fleet provisioning, Mechanism 2 (§20) is used
in place of interactive pairing.

A provisioning step pins the peer's fingerprint, or issues a one-time
token with a use count. The token is consumed on first successful use.
Unattended enrollment weakens the confirmation property described in
§21.3; deployments that require the confirmation property must use
interactive pairing.

### 21.5 QR payload

The QR payload contains the pairing session identifier, the PAKE
secret (or a value that derives it), and a rendezvous hint. The secret
is temporary. It is consumed when the pairing succeeds. A QR payload
must not contain a long-lived shared secret.

### 21.6 Security properties and limits

The properties: the code is ephemeral, the exchange is authenticated,
confirmation is required on the receiving side, establishment is
decoupled, and the output is a durable relationship assertion.

The limits: the protocol does not protect against a compromised
device, a coerced user, a malicious rendezvous combined with an
intercepted code, or a sophisticated attack on the out-of-band
channel. These are limits of any pairing mechanism that relies on a
human channel.

---

## 22. Grid URI format

URIs for Grid Network resources.

    grid://peer:v1:7f3a9c2e5d91b0a4c7e8126fa31d449b
    grid://peer:v1:7f3a9c2e5d91b0a4c7e8126fa31d449b/media
    grid://peer:v1:7f3a9c2e5d91b0a4c7e8126fa31d449b/media/library:movies

Format: scheme `grid://`, a type (`peer`, `service`, or `capability`),
an identifier, and an optional path.

URIs are the human-readable form of Grid identities. They are not
required for protocol operation.

---

## 23. Rendezvous

<!-- stability: stable -->

Rendezvous servers store ephemeral protocol state on behalf of peers.
They do not define identity, grant authorization, make policy
decisions, or persist relationships.

**What rendezvous servers do.**

- Accept reachability records from peers.
- Accept identity documents and `IdentityContinuity` objects from
  peers.
- Serve records and documents on request.
- Discard reachability records after their TTL.
- Rate-limit lookups.
- Handle DNS-like queries.

**What rendezvous servers do not do.**

- Define identity.
- Grant authorization.
- Decide policy.
- Persist relationships beyond the reachability TTL.

**Serving identity state.** A rendezvous server may accept and serve
the current identity document for a peer, and the continuity chain
from a peer's previous anchor. The documents are signed by their
issuers; the rendezvous server cannot forge them. A verifier that
obtains an identity document from a rendezvous server validates it in
the same way it validates a document obtained from the peer.

**Trust model.**

- A peer may use any rendezvous provider, multiple providers, or none.
- A peer may switch providers without changing identity.
- A rendezvous server cannot MITM signed objects; it can only serve or
  withhold.
- Withholding is a denial of service; a verifier treats missing data
  as unknown, not as a negative assertion.
- A rendezvous server that serves stale identity documents does not
  cause a verifier to accept stale state; the verifier detects
  mismatch via `identity_sequence` (§24) and refreshes before relying
  on a record.

**OperatorManifest.** A rendezvous provider publishes an
`OperatorManifest` in `stream:identity`. The manifest declares
`serves_identity_state` and the provider's `current_relay_authority_key`.
The manifest is signed by the provider's Identity Root. Peers that
wish to use the provider first obtain the manifest.

    RendezvousManifest {
        domain_separator = "grid/rendezvous-manifest/v1"

        sequence
        previous_hash?
        chain_hash
        signature

        rendezvous_servers : set<RendezvousEntry>
        ttl : duration
        issued_at
        expires_at
    }

    RendezvousEntry {
        url : text string
        transport : enum(https, http)
    }

A principal publishes its RendezvousManifest in `stream:identity`. The
manifest names the servers the principal currently publishes to.

**Limitations.** Rendezvous availability is not guaranteed. A
rendezvous server may be unavailable, may withhold records, or may be
selectively unavailable to specific requesters. A peer that becomes
undiscoverable because all its rendezvous servers are offline is
recoverable only by out-of-band contact or by re-publishing to an
available server. The rendezvous availability roadmap is documented in
the Roadmap.

---

## 24. Reachability records

A reachability record is an ephemeral signed hint about where a device
can be reached.

    ReachabilityRecord {
        domain_separator = "grid/reachability-record/v1"

        device_id
        device_key

        endpoints : set<Endpoint>

        issued_at
        expires_at
        published_at
        identity_sequence

        sequence
        previous_hash?
        chain_hash
        signature
    }

    Endpoint {
        protocol : enum(direct, relay)
        address  : text string
        priority : integer
        transport : enum(udp, tcp, quic)
    }

Signed by the device key. Published to rendezvous servers. Not
published to `stream:identity`.

`identity_sequence` is the sequence number of the publisher's latest
accepted identity document. A verifier whose cached identity state is
at a lower sequence MUST refresh before relying on the record. The
field is a hint for cache invalidation, not a proof of freshness.

`published_at` is the wall-clock time at which the record was signed.
It is used by rendezvous servers for their own bookkeeping and by
verifiers to detect obviously stale records.

Endpoints are sorted by canonical CBOR encoding. Priority is a
preference hint. A verifier is not required to try endpoints in
priority order; it is required to treat every endpoint as untrusted.

**Trust.** A verifier treats reachability as a hint. The endpoint's
identity is bound to the device key, not to the address. A malicious
rendezvous cannot redirect to a different peer because the peer's
authentication is by signature, not by address.

---

## 25. Relays and relay tickets

<!-- stability: stable -->

A relay forwards encrypted traffic when direct connection is not
possible. A relay is not a proxy; it is a pair-bound packet forwarder.

    RelayTicket {
        domain_separator = "grid/relay-ticket/v1"

        relay_id
        relay_key

        subject_peer        : peer_id
        subject_device      : device_id
        destination_peer    : peer_id
        destination_device  : device_id

        capacity     : bytes
        duration     : duration

        issued_at
        expires_at

        priority_class : enum(free, standard, priority, dedicated)

        sequence
        previous_hash?
        chain_hash
        signature
    }

A relay ticket is signed by the relay's authority key, bound to a
specific source and destination pair, bounded in bytes and duration,
and assigned a priority class.

**What a relay can observe.** Packet size, timing, source and
destination identifiers. Nothing else.

**What a relay cannot do.** Decrypt content, modify packets without
detection, forge signatures, impersonate either party, grant
authorization, or create relationships.

**Admission control.** A relay MAY reject a ticket when its capacity
is exhausted. A rejected ticket is not an authorization failure; it is
an availability failure. A verifier treats rejection as a signal to
try an alternative relay.

**Priority is a ticket property.** Priority classes do not depend on
the identity of the requester. A requester may hold multiple tickets
of different classes. The relay enforces class by queue policy, not by
authentication.

---

## 26. Transport

The protocol is transport-independent. It uses WireGuard, QUIC, or
TLS as transport, chosen by the implementation.

Transport requirements:

- Mutual authentication. The Grid layer provides this.
- Confidentiality. The transport provides this.
- Integrity. The transport provides this.
- Forward secrecy. The transport provides this.

The protocol ensures that peers know who they are talking to. The
transport ensures that nobody can eavesdrop or modify.

A conformant implementation MUST support at least one transport that
survives networks that block UDP. The recommended default is TLS over
TCP port 443. Implementations may support additional transports.

---

## 27. Verifier rules

<!-- stability: under-review -->

A verifier that decides whether to grant access follows these rules.

1. Verify all signatures against known public keys.
2. Verify that all signing keys are current and not revoked.
3. Verify that all objects are in their correct streams.
4. Verify chain hashes.
5. Detect forks and apply `StreamResolution` if present.
6. Verify that the relationship state is RECOGNIZED. PENDING and
   TERMINATED do not authorize.
7. Verify that a grant exists, covers the requested capability, and is
   in the correct stream.
8. Verify that a lease is present, unexpired, and within
   `max_offline_tolerance`.
9. Verify that no revocation invalidates any part of the authorization
   chain.
10. Verify that the signing key role is authorized for the object type
    and stream.

If any check fails, access is denied. Missing information never grants
access.

---

## 28. Service discovery

A service is discovered by:

1. Obtaining the peer's identity document.
2. Reading `service_bindings`.
3. Retrieving each service's `ServiceRecord`, signed by the service
   key.
4. Reading the record's metadata.

Service discovery is not DNS, mDNS, or LDAP. It is part of the identity
document and the service stream. It is signed and authenticated.

---

## 29. Offline operation

Peers may operate offline. Authorization state remains valid as long as
leases have not expired and `max_offline_tolerance` has not been
exceeded.

**Offline peer.** Cannot publish new reachability (the record will be
stale when the peer returns). Can verify incoming grants and leases
using local state. Cannot issue new leases; a lease issued offline has
a stale `issued_at`. Can receive and cache revocations.

**Returning online.** Republish reachability, request new leases,
synchronize revocations, and resume normal operation.

---

## 30. Lease expiration and renewal

A lease that expires leaves the peer unauthorized until a new lease is
issued.

**Renewal.** Renewal produces a new lease object. It is not a mutation
of the existing lease. The new lease has a new `issued_at` and a new
validity window.

**Auto-renewal.** An issuer may auto-renew leases according to its own
policy. The protocol does not require auto-renewal.

**Manual renewal.** A subject may request a new lease. The issuer
issues one if its policy allows.

**Concurrent attempts.** How an issuer resolves concurrent renewal
attempts is issuer policy. A verifier MUST accept any lease the issuer
has signed and that satisfies the validity rules, regardless of
whether an earlier lease is still in its validity window. The
verifier's observation of a lease is independent from the issuer's
renewal bookkeeping.

---

## 31. Revocation propagation

Revocations are pull-based. An issuer publishes a revocation in the
appropriate stream. A verifier polls rendezvous servers and applies
what it receives.

There is no guarantee of immediate propagation. The protocol does not
define a normative propagation bound. A deployment may choose to
operate with short leases so that stale revocation knowledge has a
bounded effect.

**Offline revocation.** A revocation received before its target is
cached. When the target is later received, the cached revocation is
applied.

---

## 32. Time semantics

Two validity models.

**Absolute validity.** Uses wall-clock time. Requires time
synchronization. Vulnerable to clock skew.

**Relative validity.** Uses a duration measured from the verifier's
observation. Survives clock skew up to the duration.

The protocol uses relative validity by default for leases. Absolute
validity may be used for grants, subject to the issuer's policy.

Every rule that involves time must name which clock class it uses:

- **Issuer-asserted** — the timestamp in the object, set by the
  issuer.
- **Verifier-monotonic** — elapsed time measured on a clock that
  advances during system suspend.
- **Verifier-wall-clock** — local wall-clock time, used only for
  logging and for a lower bound on elapsed time.

Wall-clock time must not extend authorization validity.

---

## 33. Trust anchors

A trust anchor is a key a verifier starts with before evaluating any
objects.

Types:

- **Self.** The verifier's own Identity Root.
- **Relationship.** The Identity Roots of recognized peers, established
  through pairing and cached locally.
- **Credential.** Delegated identity roots (a planned feature; not in
  the current protocol version).

Every cryptographic verification traces back to at least one trust
anchor. Objects signed by unknown keys are rejected unless a delegation
path leads to a known anchor.

---

## 34. Verifier local state

A verifier maintains local state for decision-making.

    VerifierState {
        known_peers      : map<peer_id, IdentityState>
        relationships    : map<relationship_id, RelationshipState>
        grants           : map<grant_id, GrantState>
        leases           : map<grant_id, LeaseState>
        revocations      : set<revoked_object_id>
        reachability     : map<device_id, ReachabilityRecord>
        stream_cache     : map<stream_id, StreamState>
        chain_hash_cache : map<stream_id, chain_hash>
        observations     : map<object_id, observation_time>
        observation_clock : verifier-monotonic time
    }

`IdentityState`, `RelationshipState`, and `GrantState` are the derived
state structures the verifier maintains. Their exact representation is
implementation-defined.

Observation records MUST be persisted. State corruption requires
re-establishing trust from scratch; implementations should use atomic
writes and checksums to minimize the risk.

---

## 35. Security state machines

A verifier maintains these state machines.

**Identity.**

    UNKNOWN         ← no document seen
    RECOGNIZED      ← document valid, chain hash correct
    FORK_DETECTED   ← two documents at the same sequence with different hashes
    QUARANTINED     ← authorization suspended pending resolution

Transitions: UNKNOWN → RECOGNIZED on a valid document. RECOGNIZED →
FORK_DETECTED on a fork. FORK_DETECTED → QUARANTINED when an
authorization decision is required before resolution. FORK_DETECTED →
RECOGNIZED on accepted `StreamResolution`.

**Relationship.**

    UNKNOWN     ← no assertions accepted
    PENDING     ← exactly one assertion accepted
    RECOGNIZED  ← both accepted, bound to the same relationship_id
    TERMINATED  ← accepted RelationshipTermination

Transitions: UNKNOWN → PENDING on the first accepted assertion.
PENDING → RECOGNIZED when the second assertion is accepted and the two
are mutually bound. PENDING → TERMINATED or RECOGNIZED → TERMINATED on
an accepted termination. TERMINATED is terminal.

**Authorization.**

    UNAUTHORIZED  ← no valid grant or lease
    AUTHORIZED    ← grant and lease valid, no revocation, within tolerance

Transitions: UNAUTHORIZED → AUTHORIZED on grant + lease. AUTHORIZED →
UNAUTHORIZED on lease expiry, grant revocation, key revocation, or
`max_offline_tolerance` exceeded.

---

## 36. Streams and sequence spaces

All objects are organized in streams. A stream is an ordered sequence
of cryptographically linked objects sharing one sequence space.

    stream:identity                     → signed by the principal's Identity Root
    stream:authorization:{auth_key_id}  → signed by that Authorization Key
    stream:reachability:{device_id}     → signed by that Device Key
    stream:service:{service_id}         → signed by that Service Key

Each stream is signed by exactly one authority. Objects from different
authorities never share a stream.

**Sequence-space invariant.** A sequence number has meaning only within
its `(issuer, stream_id)` sequence space. Sequence numbers from
different sequence spaces must not be compared.

**Base state.** Every stream has an `initial_chain_hash` computed per
§41. The first object in a stream has `sequence = 1`. The value 0 is
reserved.

---

## 37. Authority domains

The protocol partitions authority into domains.

| Domain | Decides | Cannot decide |
|---|---|---|
| Identity | Who a peer is, what keys it holds, what it recognizes, where it can be reached | What anyone is allowed to do, where a peer currently is |
| Authorization | Whether a peer is allowed to perform a capability | Who a peer is, how to reach it |
| Reachability | Where a device can be reached | Who is authorized, who the peer is |
| Rendezvous | Which records and documents to serve | Who is authorized, whether an endpoint is correct |
| Relay | Whether to forward a ticket | Who is authorized, whether traffic is allowed |
| Application | What a user may do with a resource | Who a device is, whether a device may connect |

No domain may escalate into another. A relay that grants authorization
has violated this partition. A rendezvous server that defines identity
has violated it. An application that decides device identity has
violated it.

---

## 38. Service identity, binding, and linking

A service is a named endpoint within a principal.

    ServiceRecord {
        domain_separator = "grid/service-record/v1"

        service_id
        service_key

        service_type : text string
        endpoint     : text string
        metadata     : map<text string, text string>

        issued_at
        expires_at

        sequence
        previous_hash?
        chain_hash
        signature
    }

Signed by the service key. Published in `stream:service:{service_id}`.

Service identity survives root key rotation because the service is
bound to the peer's Peer ID, not to the root key. Rotation changes the
identity document; the service binding is re-signed by the new root in
the new document, and the service's own stream is unaffected.

A `ServiceLink` is a referential connection from one service to
another. It is not an authorization object. Authorization is by grant.

---

## 39. Failure semantics (F1–F6)

<!-- stability: stable -->

The behavior of the protocol under failure is defined by six rules.

**F1 — Authorization failure denies access.** When any authorization
check fails — missing grant, expired lease, revocation applied, offline
tolerance exceeded — access is denied. The system is fail-closed.
Missing information never grants access.

**F2 — Reachability failure tries alternatives.** When a reachability
endpoint fails, the verifier tries the next endpoint, then the next
relay. When all alternatives fail, the connection is UNREACHABLE. This
is distinct from DENIED and does not change authorization state.

**F3 — Clock skew is tolerated for relative validity.** A lease
measured from the verifier's observation survives skew up to the lease
duration. Absolute timestamps are vulnerable; relative durations are
not. The recommended mitigation is `MAX_CLOCK_SKEW`, a configured
bound on the acceptable difference between the verifier's clock and
the issuer's.

**F4 — Revocation is state.** A revocation received before its target
is cached and applied when the target arrives. The verifier does not
require the target to be present at the moment the revocation is
received.

**F5 — Forks require explicit resolution.** When two objects with the
same sequence and different chain hashes are observed, the stream is
in FORK_DETECTED state. The verifier refuses to advance authorization
for that stream until a `StreamResolution` (§40) is accepted.

**F6 — Communication interruption caches and continues.** A verifier
that goes offline continues to use cached state. When connectivity
returns, cached revocations are applied to future decisions.

---

## 40. Reconciliation and conflict resolution

Two objects address stream conflicts.

**StreamResolution.** Resolves a fork.

    StreamResolution {
        domain_separator = "grid/stream-resolution/v1"

        stream            : stream_id
        forked_sequence   : sequence number
        accepted_chain_hash : hash

        reason
        resolved_at

        signatures : map<authority, signature>

        sequence
        previous_hash?
        chain_hash
        signature
    }

The `signatures` map contains a signature from each authority that
appears in the forked stream's history at the forked sequence. The
resolution is accepted only if all required signatures are present and
valid. The resolution is published in `stream:identity`.

A verifier that is in FORK_DETECTED state transitions to
QUARANTINED. In QUARANTINED state, authorization for that stream is
refused. A verifier that does not accept a resolution remains in
QUARANTINED. Quarantine is not a permanent condition, but the protocol
does not define a timeout.

If a resolution cannot be produced — for example, because a signing
key is lost — the stream is unrecoverable within the protocol. This is
a design limit, not a bug.

**IdentityContinuity.** Transitions the Identity Root.

    IdentityContinuity {
        domain_separator = "grid/identity-continuity/v1"

        peer_id          : unchanged
        old_identity_root : public_key
        new_identity_root : public_key

        signatures : {
            old_root : signature,
            new_root : signature
        }

        reason       : enum(rotation)
        effective_at : timestamp

        sequence
        previous_hash?
        chain_hash
        signature
    }

Both old and new roots sign the same signature input. The `reason`
enum is `rotation`. `recovery` and `delegation` are not in the current
protocol version.

A verifier accepts an `IdentityContinuity` only if the `old_identity_
root` is already accepted. This prevents bootstrap from an untrusted
root.

---

## 41. Cryptographic object encoding

All objects are encoded in deterministic CBOR with strict canonical
rules. The canonical form is defined in `OBJECTS.md`. The chain
construction, signature input, and domain separation are defined in
`OBJECTS.md`.

A summary of the constructions:

- `initial_chain_hash` — `SHA-256(canonical_cbor(["grid/chain-base/v1", domain_separator, stream_id]))`
- `object_commitment` — `SHA-256(canonical_cbor(["grid/commitment/v1", domain_separator, unsigned_payload]))`
- `chain_hash(N)` — `SHA-256(canonical_cbor(["grid/chain/v1", previous_chain_hash(N), object_commitment(N)]))`
- `payload_id` — `SHA-256(canonical_cbor(["grid/payload-id/v1", unsigned_payload]))`
- `signature_input(N)` — `canonical_cbor(["grid/signature/v1", domain_separator, unsigned_payload, chain_hash(N)])`

Every cryptographic construction has a unique domain tag. The tags are
registered in `OBJECTS.md`.

---

## 42. Signing-authority matrix

| Object | Signer | Stream |
|---|---|---|
| IdentityDocument | Identity Root | stream:identity |
| KeyBinding | Identity Root | stream:identity |
| DeviceBinding | Identity Root (or delegated device authority) | stream:identity |
| ServiceBinding | Identity Root (or delegated service authority) | stream:identity |
| KeyRevocation | Identity Root | stream:identity |
| RelationshipAssertion | Identity Root | stream:identity |
| RelationshipTermination | Identity Root | stream:identity |
| IdentityContinuity | Previous + New Identity Root | stream:identity |
| StreamResolution | Pre-fork authorities | stream:identity |
| RendezvousManifest | Identity Root | stream:identity |
| OperatorManifest | Identity Root | stream:identity |
| Grant | Authorization Key | stream:authorization:{auth_key_id} |
| Lease | Authorization Key | stream:authorization:{auth_key_id} |
| GrantRevocation | Identity Root | stream:identity |
| LeaseRevocation | Authorization Key | stream:authorization:{auth_key_id} |
| ReachabilityRecord | Device Key | stream:reachability:{device_id} |
| ServiceRecord | Service Key | stream:service:{service_id} |
| RelayTicket | Relay Authority Key | not streamed |
| RelayNodeRecord | Relay Node Key | not streamed |
| CreditReceipt | Operator | stream:credit:{operator_id} |

---

## 43. Implementation requirements

**Implementations MUST:**

1. Use Ed25519 for signatures and SHA-256 for hashes.
2. Use deterministic CBOR with canonical encoding.
3. Reject malformed CBOR before semantic processing.
4. Implement the verification procedure defined in `OBJECTS.md` §8.5.3
   and §8.3.
5. Support all object types in the current protocol version.
6. Implement the F1–F6 failure semantics.
7. Maintain the identity, relationship, and authorization state
   machines.
8. Fail closed on missing information.
9. Persist observation records for relative lease validity.
10. Use a monotonic clock that advances during suspend, or fail
    closed.

**Implementations SHOULD:**

1. Use constant-time cryptographic operations.
2. Clear sensitive data from memory after use.
3. Rate-limit rendezvous queries and relay admissions.
4. Support multiple rendezvous providers.
5. Cache reachability with TTL.
6. Support hardware-backed keys.
7. Log security events without key material.

**Implementations MUST NOT:**

1. Add new object types without a protocol-version bump.
2. Allow unknown capabilities to authorize access.
3. Cache authorization indefinitely.
4. Skip signature verification.
5. Use non-canonical encodings.
6. Implement cryptographic primitives directly.
7. Transmit private keys.
8. Log credentials, grants, or leases.
9. Allow wall-clock time to extend authorization validity.
10. Auto-resolve forks without explicit `StreamResolution`.

---

## 44. Conformance

Conformance is defined by test vectors and by the requirements of §43.

**Levels.**

1. **Basic crypto** — canonical CBOR, Ed25519, SHA-256, domain
   separators.
2. **Object structure** — validation of each object type.
3. **Stream processing** — chain correctness, sequence monotonicity,
   fork detection, fork resolution.
4. **Authorization logic** — grant + lease combinations, expiry,
   revocation.
5. **Edge cases** — clock skew, offline tolerance, rendezvous
   unavailability.
6. **Security** — signature forgery resistance, revocation bypass
   resistance, identity continuity validation.

An implementation conforms to protocol version v0.6.2 if it passes all
levels for the object types and behaviors it claims to support.

Conformance demonstrates agreement with this specification's defined
requirements and test vectors. It does not constitute a security
certification, interoperability certification, operational audit, or
assurance against threats outside the stated threat model.

The terms "Grid-compatible" and "Grid-inspired" have no defined
conformance meaning in this specification.

---

## 45. Versioning

**Document revision.** Advances whenever the specification changes.
`2.0`, `2.1`, `2.2`, and so on. The current document is revision 2.1.

**Protocol version.** `vMAJOR.MINOR.PATCH`. The current protocol
version is `v0.6.2`.

Semantics:

- **PATCH** — bug fixes only. No new features. No new fields. Backward
  compatible.
- **MINOR** — new features, new object types, new optional fields.
  Backward compatible with older objects.
- **MAJOR** — breaking changes. Old implementations cannot read new
  objects.

Any change to a `stable` section requires a protocol-version bump in
the same revision. Any change to an `under-review` section does not
require a protocol-version bump, but the section cannot be marked
`stable` without a review closure.

**Support.** A protocol version is maintained for a minimum of five
years after the next major version ships. Maintenance covers security
patches and clarifications only. Implementations may continue running
older versions indefinitely.

**Feature status words.** `planned`, `deferred`, `unscheduled`. A
feature label without a status word is a documentation defect.

---

## 46. Deferred features

The following features are not in protocol version v0.6.2. Each is
listed with its status word.

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

## 47. Scope

The specification defines the protocol. It does not define:

- **Governance.** Who arbitrates disputes, how decisions are made, or
  how revenue is allocated. Any governance structure is external.
- **Compatibility.** "Grid-compatible" and "Grid-inspired" have no
  conformance meaning.
- **Certification.** Conformance is not a security certification.
- **Affiliation.** The specification does not identify any operator,
  provider, or organization as authoritative.
- **Standardization.** The specification is a project document; it is
  not issued by a standards body.
- **Legal.** The specification does not grant licenses, patent rights,
  or terms of use. Those instruments are published separately.
- **Deployment.** Deployments may use zero, one, or many rendezvous
  servers; relay availability, transport availability, and direct
  connectivity depend on the deployment.
- **Identity-provider functions.** The protocol defines self-controlled
  cryptographic principals. It does not define user accounts, account
  recovery services, or a global identity registry.
- **Anonymity.** Peers are identified. Metadata is visible to
  infrastructure operators.
- **Availability.** Identity and authorization semantics survive
  infrastructure changes. Reachability does not.
- **Application authorization.** Grid authorizes connectivity. It does
  not define application roles, resource policy, or session management.
- **Identity recovery.** Recovery from Identity Root compromise is an
  external process. The protocol defines no recovery authority.

---

## 48. The core security invariant — restated

The invariant from §1 is the anchor of the specification. Every rule in
this document traces to it.

> Given a set of locally trusted anchors, authenticated protocol
> objects, known revocations, accepted chain state, and recorded
> observation history, a verifier must be able to deterministically
> establish the identity, authorization, validity, and freshness state
> of a peer as of the verifier's most recent observation, without
> contacting an authority.

The spec is complete when every normative rule either enforces this
invariant or serves a goal that supports it.