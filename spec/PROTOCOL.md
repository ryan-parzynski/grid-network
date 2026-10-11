# Grid Network Protocol

**Design Document — v0.6.2 (design-review)**


Scope: Identity, relationships, authorization, revocation, reachability, transport integration, deployment model, failure semantics, reconciliation


## 1. Abstract

The Grid Network Protocol is an open protocol for establishing persistent, mutually authenticated relationships between machines and services without requiring permanent accounts, centralized identity providers, or fixed network locations.

The protocol provides a control plane above existing networking technologies. It does not replace WireGuard, IPv6, NAT traversal, relays, DNS, or application-level authorization. It establishes:

- who a peer is;
- which devices and services belong to that peer;
- which peers recognize one another;
- what one peer is authorized to do;
- whether that authorization remains valid;
- whether authorization has been revoked;
- how a peer can currently be reached.

Network location is deliberately treated as ephemeral. A machine may change its IP address, move between networks, disappear for months, change NAT mappings, or use a relay without changing its cryptographic identity or relationships.

---

## 2. Core Security Invariant

> Given a set of locally trusted anchors, authenticated protocol objects, known revocations, accepted chain state, and recorded observation history, a verifier must be able to deterministically establish the identity, authorization, validity, and freshness state of a peer **as of the verifier's most recent observation of each object's issuer chain**, without contacting an authority.

Network access may improve freshness, discover new reachability information, or obtain newer objects. It must not be required to establish authenticity.

This means:

- rendezvous infrastructure cannot define identity;
- relays cannot define authorization;
- DNS cannot define identity;
- IP addresses cannot define identity;
- WireGuard keys cannot by themselves define application authorization;
- temporary pairing codes cannot become permanent credentials.

The phrase *as of the verifier's most recent observation* is deliberate. A verifier cannot know about revocations it has not received. Its security state is always relative to the last point at which its local object graph was synchronized.

---

## 3. Design Goals

### 3.1 Primary goals

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

### 3.2 Secondary goals

- Multiple devices per principal.
- Multiple services per device.
- Service-specific authorization.
- Temporary guests.
- Delegated administration.
- Groups.
- Multiple rendezvous providers.
- Direct peer-to-peer connections.
- Relay fallback.
- Local-first operation.
- Identity portability.
- Hardware-backed keys.

These features should not complicate the V1 security kernel unless required.

---

## 4. Non-Goals

- A replacement for WireGuard.
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

Applications may continue to implement their own authorization.

---

## 5. Conceptual Architecture

### 5.1 Protocol-layer architecture

```
┌──────────────────────────────────────────────┐
│                  Application                 │
├──────────────────────────────────────────────┤
│          Grid Network Identity & Authorization       │
│ Principal / Device / Service / Grant / Lease │
├──────────────────────────────────────────────┤
│               Reachability                   │
├──────────────────────────────────────────────┤
│                  Transport                   │
└──────────────────────────────────────────────┘
```

Identity and authorization are independent of transport.

### 5.2 Full-stack architecture (informative)

The protocol layer is consumed by a **Connectivity layer** that is not part of the protocol. This layer is where path selection, path measurement, and (in future versions) multipath scheduling live.

```
┌──────────────────────────────────────────────┐
│                  Application                 │
├──────────────────────────────────────────────┤
│          Grid Network Protocol (Layer 1)             │
│  Identity / Authorization / Reachability     │
├──────────────────────────────────────────────┤
│          Connectivity (Layer 3)              │
│  Direct / NAT traversal / Relay / Multipath  │
├──────────────────────────────────────────────┤
│                  Transport                   │
│           WireGuard / QUIC / TCP             │
└──────────────────────────────────────────────┘
```

The protocol does not standardize the connectivity algorithm. It establishes the information and authority boundaries that allow an implementation to make connectivity decisions.

---

## 6. Peer Principal

A Peer Principal is the durable logical identity represented by the protocol. It is not necessarily one physical machine, one OS installation, one network interface, one device key, or one service.

```
Principal: Dad
 ├── Home Server
 │    ├── Jellyfin
 │    └── File Service
 ├── Laptop
 └── Phone
```

The principal survives replacement of individual devices.

---

## 7. Peer Principal ID

```
peer:v1:7f3a9c2e5d91b0a4c7e8126fa31d449b
```

Opaque, randomly generated, not self-certifying. The identity document binds the ID to the principal's identity root.

```
Identity = Peer ID + signed identity document + trusted root
Identifier = opaque reference
```

Advantages:

- Identity-root rotation does not change the Peer ID.
- Provisioning can occur before key generation.
- Cryptographic constructions can change in future versions.
- Identifiers do not expose the construction.
- Relationships remain stable through root-key replacement.

---

## 8. Identity Root

The Identity Root is the highest cryptographic authority for a principal. It is used to:

- Establish the identity document.
- Authorize device keys.
- Authorize service keys.
- Delegate authorization authority.
- Rotate subordinate keys.
- Revoke subordinate keys (including Authorization Keys).
- Recover from subordinate-key compromise.

The root should not normally participate in routine network sessions. Ideally it remains offline or hardware-protected.

---

## 9. Key Roles and Separation

```
                    Identity Root
                         │
             ┌───────────┼────────────┐
             │           │            │
         Device Key   Auth Key    Recovery
             │           │
        ┌────┴────┐      │
        │         │      │
   Service Key  ...    Grants
                         │
                       Leases
```

### 9.1 Role definitions

| Role | Owner | Purpose |
|------|-------|---------|
| Identity Root | Principal | Defines the principal; signs identity documents, relationship assertions, key delegations; revokes subordinate keys; signs the principal's rendezvous manifest |
| Device Key | One device | Authenticates a device; signs reachability records |
| Service Key | One service | Authenticates a service; signs service records |
| Authorization Key | Principal or delegated authority | Signs grants, leases, and revocations in its stream |
| Recovery Key | Principal | Future: threshold or offline recovery |
| Relay Authority Key | Relay coordinator | Signs relay tickets (if centralized) |
| Relay Node Key | Relay operator | Authenticates a relay endpoint |

A rendezvous operator's signing key is simply that operator's own Identity Root, used to sign its own OperatorManifest (§30).

### 9.2 Non-reuse rule

**A single private key MUST NOT be used for more than one role.**

Implementations that cannot enforce separate keys MUST at minimum enforce:

- Identity Root separate from Device Key.
- Identity Root separate from Authorization Key.
- Device Key separate from Service Key.
- Any role separate from Recovery Key.

### 9.3 Delegation

Delegation of authority from the Identity Root to a subordinate key is expressed inside the identity document. A verifier MUST NOT infer authority from key possession alone.

---

## 10. Identity Documents

```
IdentityDocument {
    domain_separator   = "grid/identity-document/v1"
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
    expires_at
}
```

The exact encoding is defined by OBJECTS.md.

### 10.1 Ordering semantics

All key collections are **canonical sets**:

- Ordered by key identifier (lexicographic byte comparison).
- Duplicates forbidden.
- Reordering does not change the set.

### 10.2 Linear signed history

```
Document 1 → Document 2 → Document 3 → ...
```

Identity documents occupy `stream:identity`.

### 10.3 Fork detection

Two documents with the same `peer_id` and `sequence` but different `chain_hash` values constitute a fork. Resolution follows §54.

---

## 11. Identity Document History

Identity state is append-only. A verifier MUST advance only by walking forward from its accepted state (§45). Intermediate documents remain useful for audit and diagnosis.

---

## 12. Relationship

### 12.1 Model

Recognition between two principals is expressed by a pair of independently signed `RelationshipAssertion` objects, one published by each principal.

Each principal publishes its own assertion in its own `stream:identity`. No object spans both streams. Bilateral recognition is a **verifier-derived state**, not a property of any single object.

### 12.2 RelationshipAssertion

```
RelationshipAssertion {
    domain_separator   = "grid/relationship-assertion/v1"
    sequence
    previous_hash?
    chain_hash
    signature

    relationship_id
    subject_principal
    issued_at
    not_before
    expires_at?
}
```

- Signed by the **issuer's** Identity Root.
- Published in the **issuer's** `stream:identity`.
- `subject_principal` is the other principal whose recognition this assertion names.

**Semantics:** A `RelationshipAssertion` states: "The issuer recognizes `subject_principal` under `relationship_id`." It is unilateral. It does not itself establish `RECOGNIZED`.

### 12.3 RelationshipTermination

```
RelationshipTermination {
    domain_separator   = "grid/relationship-termination/v1"
    sequence
    previous_hash?
    chain_hash
    signature

    relationship_id
    reason
    terminated_at
}
```

- Signed by the **terminating principal's** Identity Root.
- Published in the **terminating principal's** `stream:identity`.
- Unilateral. Either principal may terminate.
- On acceptance, the relationship for `relationship_id` transitions to `TERMINATED`.

### 12.4 Verifier-derived relationship state

```
PENDING     iff exactly one assertion is accepted:
                either assertion_a by A with subject B,
                or assertion_b by B with subject A.

RECOGNIZED  iff both assertions are accepted:
                assertion_a by A with subject B, AND
                assertion_b by B with subject A,
            AND neither assertion is expired,
            AND no accepted RelationshipTermination for R.

TERMINATED  iff an accepted RelationshipTermination for R exists.

UNKNOWN     otherwise.
```

- `PENDING` does not contribute to authorization.
- `RECOGNIZED` is required for authorization.
- `TERMINATED` is terminal. A new relationship requires a new `relationship_id`.

**Normative:** `PENDING` and `RECOGNIZED` are states of the verifier's belief, not states encoded by any single object.

### 12.5 Compatibility

The v0.6 single-object dual-signature `Relationship` is superseded. Implementations MUST NOT accept a `Relationship` object with a dual-signature field.

### 12.6 Rationale

- **Stream purity.** Every object lives in exactly one stream.
- **Unilateral assertion.** Either principal may publish independently.
- **Unilateral termination.** Either may terminate unilaterally.
- **No invented stream.** No new sequence space required.
- **Recognition without coercion.**

---

## 13. Grant

A Grant is directional.

```
Dad → Ryan: jellyfin.stream
```

A grant contains: relationship ID, issuer, subject, device scope (optional), capabilities, resources, constraints, lease policy, issuance info, and signature.

**Known issue:** Grant acceptance may be conflated with authorization in implementation logic. PROTOCOL.md §12.4 distinguishes PENDING/RECOGNIZED/TERMINATED as verifier-derived states, and §12.4 explicitly states "`PENDING` does not contribute to authorization" and "`RECOGNIZED` is required for authorization." However, the verification procedure (OBJECTS.md §5.3 Step 11 / §9 Phase 11) for authorization objects (Grant, Lease) requires "relationship is `RECOGNIZED`, grant is `GRANTED`" — the grant's own state (`GRANTED` vs `EXPIRED`/`REVOKED`) is separate from the relationship state. Implementations must not treat grant receipt as authorization without checking relationship state and lease validity. (open blocker)

Grants are immutable objects within the Authorization Key's authorization stream. Any change produces a new grant with a new `grant_id`.

---

## 14. Lease

A Lease proves that a grant is currently valid.

```
Relationship  "We recognize each other."
Grant         "You are authorized for X."
Lease         "That authorization is currently valid."
```

| Capability | Typical lease |
|------------|---------------|
| Jellyfin streaming | 30 days |
| File access | 7 days |
| SSH | 1 hour |
| Admin SSH | 15 minutes |

### 14.1 Lease expiration is a state transition

When a lease expires, the peer is unauthorized until a new lease is issued. A peer returning from a long offline period does NOT inherit the expired lease.

---

## 15. Capabilities

```
Capability {
    namespace : string    // org.jellyfin
    action    : string    // stream, admin, read
    resource  : string    // library:movies
}
```

The protocol validates well-formedness but does not interpret capability semantics.

### 15.1 Namespace rules

Lowercase ASCII, dot-separated, at least one dot, first component reverse-DNS.

### 15.2 Unknown namespaces

A verifier that encounters an unknown namespace:

- MUST validate well-formedness.
- MUST NOT grant network-level authorization based on the unknown namespace alone.
- MAY pass through to an application that understands it.
- MUST NOT reject a grant solely for containing unknown namespaces.

### 15.3 Empty resource

Empty resource means "all resources in this namespace for this action" only when the grant sets a wildcard flag.

### 15.4 Constraints

Canonical map string → string. Max 32 entries. Values max 1024 bytes.

---

## 16. Authorization Policy

```
Grant:
    capability = org.jellyfin.stream
    lease_duration = 30 days
    max_offline_tolerance = 30 days
```

Offline tolerance is defined per-grant and evaluated separately from lease validity (§40.6).

---

## 17. Network Authorization vs Application Authorization

**Network authorization:** May this peer connect?

**Application authorization:** Once connected, what may the application do?

The Grid Network layer does not replace application access control.

---

## 18. Revocation

Revocation is terminal.

```
Grant A → revoked → Grant B (new authorization)
```

Never:

```
Grant A → revoked → unrevoked
```

---

## 19. Revocation Hierarchy

```
Lease → Grant → Device → Authorization Key → Principal
```

| Revocation | Invalidates |
|-----------|-------------|
| Revoke lease | One authorization period |
| Revoke grant | The grant and future leases derived from it |
| Revoke device | Device-specific authorization and services |
| Revoke authorization key | Objects signed at or after `effective_sequence` |
| Revoke principal | The principal's entire identity |

---

## 20. Key Revocation and Effective Sequence

Key IDs are immutable. Once revoked, a key ID can never be reused.

### 20.1 Revocation authorities

**Authorization-state revocation** is signed by an Authorization Key. It revokes grants, leases, or other authorization objects that the key itself issued. It occupies the Authorization Key's authorization stream.

**Authorization-Key revocation** is signed by the Identity Root. It revokes the Authorization Key itself. It occupies the Identity Root's identity stream.

### 20.2 KeyRevocation object

```
KeyRevocation {
    domain_separator   = "grid/key-revocation/v1"
    sequence
    previous_hash?
    chain_hash
    signature

    key_id
    effective_sequence
    revoked_at
    reason
    replacement_key_id?
}
```

Semantics:

- Signed by the Identity Root.
- Occupies the Identity Root's identity stream.
- `effective_sequence` refers to a position in the **revoked Authorization Key's authorization stream**.
- Objects signed by `key_id` at or after `effective_sequence` are invalid.

**Example:**

```
Identity Root stream
seq 201  IdentityDocument
seq 202  KeyRevocation { key_id=K, effective_sequence=103 }
seq 203  IdentityDocument

Authorization Key K stream
seq 100  Grant G
seq 101  Lease L1
seq 102  Lease L2
seq 103  Grant G2
seq 104  Lease L3
```

The root's seq 202 has no relationship to `effective_sequence = 103`. They refer to different streams.

**`effective_sequence = 0`** invalidates the entire authorization history signed by K.

### 20.3 No key reuse

A revoked key ID can never be reauthorized.

---

## 21. Authorization-Key Compromise

```
Authorization Key compromised
          ↓
Identity Root signs KeyRevocation (effective_sequence = N)
          ↓
Objects signed by K at or after N become invalid
          ↓
Identity Root issues new Authorization Key
          ↓
Legitimate grants re-issued under new key
```

A compromised Authorization Key does not imply compromise of the principal identity, other devices, unrelated service keys, or the identity root.

---

## 22. Identity Root Compromise

V1 treats the root as the highest trust anchor.

Advanced recovery mechanisms are deferred to V2:

- Offline recovery keys.
- Hardware-backed roots.
- Threshold recovery.
- Multi-party approval.
- Social recovery.

---

## 23. Key Rotation

Key rotation is a V1 requirement. Rotation preserves the Peer Principal ID. The identity history establishes the transition. `IdentityContinuity` (§54.5) is used for orderly root transition.

---

## 24. Pairing

```
Device A displays:  481729
Device B enters:    481729
```

The six-digit value is a temporary human coordination mechanism, not a credential.

---

## 25. Pairing Protocol

V1 pairing MUST use an established PAKE (SPAKE2 or CPace).

**Open blocker:** PAKE selection remains unresolved (SPAKE2 vs CPace). This blocks pairing, transcript binding, and test vectors. The exact PAKE, transcript construction, identity binding, protocol version and context binding, replay protection, code lifetime, retry limits, and enumeration resistance must be specified before wire protocol and test vector completion. (see design/KNOWN-LIMITATIONS.md §Unresolved Contradictions)

The final protocol must specify:

- Exact PAKE.
- Transcript construction.
- Identity binding.
- Protocol version and context binding.
- Replay protection.
- Code lifetime, retry limits, enumeration resistance.

### 25.1 Transcript binding

The pairing transcript MUST bind: protocol version, peer identities, PAKE identities, capabilities being requested, pairing context, and rendezvous session identifier.

---

## 26. Pairing Code

~20 bits of entropy. MUST NOT be treated as sufficient cryptographic authentication.

Short-lived, single-use, rate-limited, invalidated after success, timeout, or excessive failures.

---

## 27. Human Verification

Devices may display a verification value derived from the pairing transcript.

```
8341 2910
```

---

## 28. Permanent Identity References

```
Identity Reference ≠ Pairing Invitation ≠ Authorization Grant ≠ Recovery Credential
```

---

## 29. Grid Network URI

```
grid://v1/...
```

Grammar MUST be formally specified in ABNF. Parsing MUST be strict. Must distinguish identity references, temporary invitations, capability requests, and rendezvous hints. A permanent URI MUST NOT contain a mandatory fixed rendezvous dependency.

---

## 30. Rendezvous

### 30.1 Rendezvous roles

| Role | Purpose |
|------|---------|
| Publication | Accepts authorized reachability publications |
| Replica | Stores signed copies |
| Cache | Fetches and caches on demand |
| Bootstrap | Helps peers find manifests |
| Relay coordinator | Issues relay tickets |
| Freshness source | Attests to authorization state, only when explicitly authorized |

A rendezvous server is not a freshness source merely because it stores objects.

### 30.2 Principal Rendezvous Manifest

```
RendezvousManifest {
    domain_separator   = "grid/rendezvous-manifest/v1"
    sequence
    previous_hash?
    chain_hash
    signature

    peer_id
    generation
    active_until
    recovery_until
    rendezvous_set : set<RendezvousEntry>
    issued_at
}
```

- Signed by the principal's Identity Root.
- Occupies the principal's `stream:identity`.
- States: Active, Recovery, Expired.

### 30.3 Operator Manifest

```
OperatorManifest {
    domain_separator   = "grid/operator-manifest/v1"
    sequence
    previous_hash?
    chain_hash
    signature

    operator_id
    operator_root
    nodes
    federation_peers
    current_relay_authority_key
    issued_at
    expires_at
}
```

- Signed by the operator's Identity Root.
- Occupies the operator's `stream:identity`.
- Not an assertion about any principal, service, or authorization stream.
- `current_relay_authority_key` — the currently active Relay Authority Key for validating relay tickets.

### 30.4 Rendezvous invariant

**Normative:**

> Neither a Principal Rendezvous Manifest nor an OperatorManifest grants authority over any principal, service, authorization stream, or reachability state. The operator's Peer ID is simply the operator's identity; operating rendezvous infrastructure does not create protocol authority.

### 30.5 Rendezvous trust model

A malicious rendezvous server may provide stale or false endpoints, suppress endpoint information, observe metadata, or attempt DoS. It MUST NOT be able to forge identity, authorization, or revocation; create a valid lease; or decrypt transport traffic.

### 30.6 Rendezvous identity state distribution

**Normative:** Rendezvous servers MUST accept and serve identity documents and `IdentityContinuity` objects in addition to reachability records.

**Rationale:** The protocol assumes identity state propagates through peer-to-peer contact, but this fails when peers are disconnected — which is exactly when synchronization matters most. Without this change, a peer who hasn't communicated with another peer in months cannot verify that peer's current state, because the peer's anchor may be stale and there is no way to obtain current state.

**Scope:** The rendezvous layer's scope is extended, not the object model. The endpoints for publication and query are extended; the objects themselves are unchanged.

**Trust model:** Rendezvous remains untrusted. Identity documents are still signed by their issuers; the rendezvous cannot forge them.

**Wire-level implications (when wire protocol is specified):**
- `POST /v1/identity` — publish an identity document (and optionally the continuity chain to the publisher's previous anchor)
- `GET /v1/identity/{peer_id}` — fetch the current identity document for a peer

Peers still need to be able to reach the rendezvous. If they can't, this change doesn't help. That's a narrower limitation than having no state distribution at all.

---

## 31. Rendezvous Evolution

| Version | Capability |
|---------|-----------|
| V1 | HTTPS rendezvous |
| V2 | Multiple interchangeable rendezvous servers |
| V3 | Federation |
| V4 | Peer-assisted gossip |
| V5 | DHT, if required |

---

## 32. Reachability

```
ReachabilityRecord {
    domain_separator       = "grid/reachability-record/v1"
    sequence
    previous_hash?
    chain_hash
    signature

    peer_id
    device_id
    service_id?
    endpoint
    transport
    observed_at
    expires_at
    published_at
    identity_sequence
}
```

### 32.1 Reachability record chain

Each device maintains a linear chain. Higher `sequence` supersedes lower.

### 32.2 Reachability freshness fields

- `published_at` — wall-clock timestamp when the record was published to rendezvous (Unix epoch seconds).
- `identity_sequence` — the sequence number of the publisher's latest accepted identity document at the time of publication.

These fields allow a verifier to determine whether its cached identity state is current. A verifier that fetches a reachability record and finds `identity_sequence` greater than its accepted identity sequence for that peer MUST refresh identity state before using the record.

### 32.3 Endpoint hints are not authoritative

A cached endpoint is a hint, not a destination.

---

## 33. Relays

Relays are transport infrastructure.

### 33.1 Relay tickets (optional)

```
RelayTicket {
    domain_separator   = "grid/relay-ticket/v1"
    sequence
    previous_hash?
    chain_hash
    signature

    ticket_id
    source_device
    destination_device
    service_link_id
    requested_capability
    issued_at
    expires_at
    max_bytes
    max_rate_bps
}
```

A RelayTicket authorizes transport use only. It cannot create authorization.

---

## 34. Transport

WireGuard is the preferred initial transport.

**Open blocker:** Wire protocol is missing. No transport encoding, framing, or RPC definitions exist. Object delivery, rendezvous API endpoints, relay wire format, and ticket presentation flow are not specified. This is an interoperability blocker. (see design/KNOWN-LIMITATIONS.md §Unresolved Contradictions)

---

## 35. Enforcement

```
Grid Network daemon → WireGuard configuration → Firewall → Reverse proxy → Application
```

---

## 36. Service Discovery

```
ServiceRecord {
    domain_separator   = "grid/service-record/v1"
    sequence
    previous_hash?
    chain_hash
    signature

    service_id
    peer_id
    device_id
    service_type
    endpoint
    supported_capabilities : set<CapabilityNamespace>
    metadata
    issued_at
    expires_at
}
```

Service records do not grant access.

---

## 37. Offline Operation

```
KNOWN / TRUSTED / OFFLINE / LAST SEEN: ...
```

---

## 38. Lease Expiration

```
Lease expires → No new lease → Access denied
```

---

## 39. Revocation Propagation

V1 supports:

- **Pull on reconnect.**
- **Opportunistic synchronization.**

A verifier that has not received a revocation may temporarily continue honoring a valid lease, subject to `max_offline_tolerance`.

---

## 40. Time Semantics

### 40.1 Relative validity

```
valid_from  = verifier first-acceptance time
valid_until = valid_from + duration
```

Deterministic per verifier. Does not require synchronized wall clocks.

### 40.2 Absolute validity

Verifiers apply the protocol-defined clock-skew tolerance.

### 40.3 Validity by object class

| Object | Validity |
|--------|----------|
| Identity Document | Absolute |
| Rendezvous Manifest | Absolute |
| Grant | Absolute for issuance; policy controls freshness |
| Lease | Relative by default; absolute MAY be supported |
| Reachability Record | Relative |
| Revocation | Terminal |

### 40.4 Clock skew

```
MAX_CLOCK_SKEW = 5 minutes
```

**Known issue:** The verification procedure (OBJECTS.md §5.3 Step 10 / §9 Phase 10) assumes access to a wall clock with this skew tolerance and a monotonic clock for `acceptance_time`. The clock/time source interface is not specified in OBJECTS.md or PROTOCOL.md. (open blocker; see OBJECTS.md §Unresolved Dependencies item 6)

### 40.5 Issued-at ordering

```
issued_at(N+1) >= issued_at(N)
```

### 40.6 Authorization freshness and offline tolerance

```
authorized =
    valid_lease
    AND grant_valid
    AND not_revoked
    AND authorization_fresh

authorization_fresh =
    elapsed_since_last_successful_authorization_refresh
        <= max_offline_tolerance
```

### 40.6.1 Definition of authorization refresh

A successful refresh requires an **authenticated exchange** with the grant issuer or an explicitly designated freshness source. Local re-evaluation does not count. A rendezvous server or relay MUST NOT constitute a freshness source merely because it stores or forwards signed objects.

### 40.7 Revocation interaction

When a verifier receives a valid revocation:

1. It is added to local state.
2. Affected objects are re-evaluated.
3. Invalidated authorization ceases to be honored.
4. A previously valid lease MUST NOT regain validity.

### 40.8 Revocation as state, not event

A revocation is a state assertion. If received before its target, it MUST remain effective when the target is subsequently received.

---

## 41. Cryptographic Object Encoding

All signed objects use deterministic CBOR (OBJECTS.md).

---

## 42. Domain Separation

```
grid/identity-document/v1
grid/device-binding/v1
grid/service-binding/v1
grid/key-binding/v1
grid/key-revocation/v1
grid/relationship-assertion/v1
grid/relationship-termination/v1
grid/rendezvous-manifest/v1
grid/operator-manifest/v1
grid/relationship-grant/v1
grid/authorization-lease/v1
grid/grant-revocation/v1
grid/lease-revocation/v1
grid/service-record/v1
grid/reachability-record/v1
grid/stream-resolution/v1
grid/identity-continuity/v1
grid/relay-ticket/v1
grid/relay-node-record/v1
```

---

## 43. Cryptographic Baseline

- Ed25519 signatures.
- SHA-256 hashes.
- Deterministic CBOR.
- Cryptographically random identifiers.

The object's schema version is identified by its `domain_separator`. A signed object MUST NOT contain a separate `version` field unless a schema explicitly requires one.

---

## 44. Object Identity

### 44.1 object_id

```
object_id = SHA-256(canonical_cbor([
    "grid/object-id/v1",
    canonical_signed_object_bytes
]))
```

### 44.2 payload_id

```
payload_id = SHA-256(canonical_cbor([
    "grid/payload-id/v1",
    unsigned_payload
]))
```

---

## 45. Sequence and History

### 45.1 Sequence spaces

```
sequence_space = (issuer, stream_id)
```

Stream identifiers:

```
stream:identity
stream:reachability:<device_id>
stream:service:<service_id>
stream:authorization:<autho..._id>
```

**Known issue:** This section defines text-string stream identifiers (`stream:identity`, `stream:reachability:<device_id>`, etc.) that are incompatible with the hash-derived opaque `stream_id` model in OBJECTS.md §7 (`stream_id = H(principal_id || signing_key_id || stream_context || epoch)`). The two models coexist in normative text and must be reconciled before implementation. (open blocker; see design/KNOWN-LIMITATIONS.md §Unresolved Contradictions)

An Authorization Key owns exactly one authorization stream. Grants, leases, and revocations issued by K occupy that stream and consume sequence numbers regardless of object type.

A `KeyRevocation` is signed by the Identity Root and occupies the Identity Root's identity stream.

`effective_sequence` of a `KeyRevocation` refers to the sequence space of the revoked Authorization Key's stream.

**A verifier MUST NOT compare sequence numbers from different streams.**

### 45.2 Chain structure

```
unsigned_payload(N)      = object fields excluding chain_hash and signature
commitment_preimage(N)   = canonical_cbor([
                              "grid/commitment/v1",
                              domain_separator,
                              unsigned_payload(N)
                           ])
object_commitment(N)     = SHA-256(commitment_preimage(N))

previous_hash(N)         = object_commitment(N-1)     for N > 1
                           omitted                     for N = 1

previous_chain_hash(N)   = initial_chain_hash         for N = 1
                           chain_hash(N-1)             for N > 1

initial_chain_hash       = SHA-256(canonical_cbor([
                              "grid/chain-base/v1",
                              domain_separator,
                              stream_id
                           ]))

chain_hash(N)            = SHA-256(canonical_cbor([
                              "grid/chain/v1",
                              previous_chain_hash(N),
                              object_commitment(N)
                           ]))

signature_input(N)       = canonical_cbor([
                              "grid/signature/v1",
                              domain_separator,
                              unsigned_payload(N),
                              chain_hash(N)
                           ])
```

`unsigned_payload` contains all schema-defined fields plus the common envelope fields (`domain_separator`, `sequence`, `previous_hash?`). It excludes only `chain_hash` and `signature`.

`previous_hash` is a **field** in the unsigned payload carrying the previous object's `object_commitment`. `previous_chain_hash` is a **derived input** to the chain construction, not a field.

The first object in every stream has `sequence = 1`. `0` is reserved for uninitialized.

### 45.3 Immutable objects

Grants, leases, relationship assertions, and other immutable objects occupy a position in their issuer's stream. They are not streams of their own.

### 45.4 Fork detection

Two objects in the same sequence space with the same `sequence` but different `chain_hash` values constitute a fork. Resolution follows §54.

### 45.5 V1 does not support skip-ahead

A verifier MUST validate sequentially from its last accepted state.

### 45.6 Future chain-extension proofs

Future versions MAY introduce authenticated chain-extension proofs.

---

## 46. Trust Anchors

```
peer_id
trusted_identity_root
accepted_identity_state  (sequence + chain_hash)
acceptance_time
```

---

## 47. Verifier Local State

### 47.1 Principal state

```
PrincipalState {
    peer_id
    trusted_identity_root
    accepted_identity_sequence
    accepted_identity_chain_hash
    identity_acceptance_time
}
```

### 47.2 Key state

```
KeyState {
    key_id
    role
    owner_peer_id
    status
    first_seen_sequence
    revocation_state
    effective_sequence?
}
```

**Known issue:** The KeyState structure and the authority state representation (identity root, authorized keys, delegations, revocation state, key status) are defined here but the query interface (e.g., "is key K authorized for role R at sequence S?") is not formally specified in OBJECTS.md. Verification §5.3 Step 9 / §9 Phase 9 requires this interface. (open blocker; see OBJECTS.md §Unresolved Dependencies item 3)

### 47.3 Relationship state

Relationship state is **verifier-derived** from the pair of accepted `RelationshipAssertion` objects and any accepted `RelationshipTermination`:

```
RelationshipState {
    relationship_id
    local_principal
    remote_principal
    state          // UNKNOWN | PENDING | RECOGNIZED | TERMINATED
    assertion_local?
    assertion_remote?
    termination?
}
```

**Known issue:** The exact algorithm for deriving `RECOGNIZED` state from accepted `RelationshipAssertion` and `RelationshipTermination` objects is specified in PROTOCOL.md §12.4 but the verification procedure's dependency on it (OBJECTS.md §5.3 Step 11 / §9 Phase 11) should be acknowledged. The query interface for relationship state derivation is not formally specified. (open blocker; see OBJECTS.md §Unresolved Dependencies item 5)

### 47.4 Grant state

```
GrantState {
    grant_id
    relationship_id
    issuer
    subject
    capabilities
    constraints
    max_offline_tolerance
    state
}
```

### 47.5 Lease state

```
LeaseState {
    lease_id
    grant_id
    issued_sequence
    validity
    first_observed
    last_authorization_refresh
    state
}
```

### 47.6 Chain state

```
ChainState {
    issuer
    stream_id
    accepted_sequence
    accepted_chain_hash
    sync_state
}
```

`sync_state` ∈ { `IDLE`, `SYNCING`, `FORKED` }.

**Known issue:** The ChainState structure lacks the per-stream lookup interface needed by the verification procedure (OBJECTS.md §5.3 Step 6 / §9 Phase 6: "the verifier's accepted `chain_hash` for sequence-1 in the same `(issuer, stream_id)`"). The query interface for stream state access is not formally specified. (open blocker; see OBJECTS.md §Unresolved Dependencies item 2)

### 47.7 Reachability state

Soft state. Loss MUST NOT invalidate identity, relationship, grant, or revocation state.

### 47.8 Rendezvous state

Infrastructure state.

### 47.9 Observation history and monotonic time

For relative validity, the verifier MUST retain `first_observed_at` (monotonic).

Implementations MUST use a monotonic local clock for elapsed-duration calculations.

### 47.10 Processing order

1. Decode canonical object.
2. Validate domain separator.
3. Validate signature.
4. Validate issuer authority.
5. Validate object sequence.
6. Validate chain continuity.
7. Detect rollback, fork, extension, or gap.
8. Apply key transitions.
9. Apply revocations.

**Open blocker:** This processing order (signature before chain continuity, authority before sequence) differs from OBJECTS.md §5.3 / §9 verification order (CBOR → envelope → domain separator → schema → sequence → chain linkage → signature → authority). The two procedures conflict on validation ordering. This is part of the verification procedure duplication / authority conflict between OBJECTS.md and PROTOCOL.md. (open blocker; see design/KNOWN-LIMITATIONS.md §Unresolved Contradictions)
10. Apply relationship transitions.
11. Apply grants.
12. Apply leases.
13. Update authorization freshness.
14. Update reachability state if applicable.
15. Commit resulting local state.

**Note:** Steps 1–9 are logically ordered validation phases, not necessarily separate persistence operations. Verification MUST NOT mutate accepted state; commitment is the only mutation (§47.11).

### 47.11 Atomic state updates

Security-significant object processing MUST be atomic. Validation is pure with respect to accepted state; commitment is the only mutation. An implementation MUST NOT expose an intermediate state in which some validations have passed and others have not.

### 47.12 Fork handling

Upon detecting a fork, the stream enters `FORKED` state. Behavior is governed by §53.7. Recovery is governed by §54.

### 47.13 Gap handling

A gap occurs when an incoming object has sequence greater than `accepted_sequence + 1`. A gap is **not** a fork.

### 47.14 Case summary

| Incoming object | Condition | Result |
|-----------------|-----------|--------|
| Rollback | sequence < accepted | Reject |
| Fork | sequence == accepted, chain differs | Enter `FORKED` |
| Extension | sequence == accepted + 1, predecessor matches | Accept |
| Gap | sequence > accepted + 1 | Enter `SYNCING` |

### 47.15 Local verification invariant

> Given locally trusted anchors, authenticated objects, known revocations, accepted chain state, and recorded observation history, the verifier can deterministically establish principal, authorization, revocation, and freshness state without contacting an authority.

---

## 48. Security State Machines

### 48.1 Relationship

#### 48.1.1 RelationshipAssertion object state

```
UNKNOWN → CURRENT → { SUPERSEDED (terminal), EXPIRED (terminal) }
```

A `RelationshipAssertion` is a mutable stream object; it may be superseded by a newer assertion from the same issuer for the same `relationship_id`.

#### 48.1.2 Verifier-derived relationship state

```
UNKNOWN
   │
   │ first assertion accepted
   ▼
PENDING
   │
   │ second assertion accepted
   ▼
RECOGNIZED
   │
   │ termination accepted from either principal
   │ OR both assertions expired OR superseded
   ▼
TERMINATED (terminal)
```

`PENDING` does not contribute to authorization. `RECOGNIZED` is required for authorization. `TERMINATED` is terminal.

A new relationship with the same principals requires a new `relationship_id`.

### 48.2 Grant

```
UNKNOWN → GRANTED → { EXPIRED (terminal), REVOKED (terminal) }
```

V1 grant validity is absolute.

### 48.3 Lease

Two independent predicates: lease validity and authorization freshness.

```
UNKNOWN → VALID
VALID → { EXPIRED (terminal), REVOKED (terminal), STALE }
STALE → VALID (on successful refresh)
```

Authorization requires: lease `VALID`, grant `GRANTED`, relationship `RECOGNIZED`, key `ACTIVE` or `SUPERSEDED`, no applicable revocation.

A successful refresh transitions `STALE` → `VALID` only if the grant remains `GRANTED`, no revocation applies, and the lease has not independently expired.

### 48.4 Authorization Key

```
UNKNOWN → ACTIVE → { SUPERSEDED → REVOKED (terminal), REVOKED (terminal) }
```

- `ACTIVE → SUPERSEDED` is established only by an accepted identity document.
- `REVOKED`: no longer trusted for objects at or after `effective_sequence`. Objects before it remain subject to ordinary rules.

### 48.5 Device Key

```
UNKNOWN → ACTIVE → { REVOKED (terminal), RETIRED (terminal) }
```

### 48.6 Service Record

```
UNKNOWN → CURRENT → { SUPERSEDED (terminal), EXPIRED (terminal) }
```

### 48.7 Reachability Record

```
UNKNOWN → CURRENT → { SUPERSEDED (terminal), EXPIRED (terminal) }
```

### 48.8 Cross-object constraints

- A grant whose relationship is not `RECOGNIZED` MUST NOT contribute to effective authorization.
- A lease whose grant is not `GRANTED` MUST NOT contribute.
- A lease whose Authorization Key is `REVOKED` with `effective_sequence` ≤ lease sequence MUST NOT contribute.
- A reachability record signed by a `REVOKED` Device Key MUST NOT be accepted as current.
- A service record signed by a `REVOKED` Service Key MUST NOT be accepted as current.

---

## 49. Authority Domains

**Known issue:** Authority/revocation/relationship query interfaces are unspecified. §47 defines state structures (PrincipalState, KeyState, RelationshipState, GrantState, LeaseState, ChainState) but not the query API for "is key K authorized for role R at sequence S?", "does revocation X invalidate object Y at sequence Z?", or "what is the derived relationship state for relationship_id R?". (open blocker; see OBJECTS.md §Unresolved Dependencies items 2, 3, 4, 5)

### 49.1 Identity authority

**Source:** Identity Root.

**Scope:** identity document, subordinate keys, device bindings, service bindings, relationship assertions and terminations, rendezvous manifest.

**Boundary:** does not extend to authorization.

### 49.2 Authorization authority

**Source:** Authorization Key delegated by Identity Root.

**Scope:** grants, leases, and revocations in its stream.

**Boundary:** does not extend to identity. An Authorization Key cannot revoke itself.

### 49.3 Service authority

**Source:** Service Key.

**Scope:** service records.

### 49.4 Reachability authority

**Source:** Device Key.

**Scope:** reachability records.

### 49.5 Rendezvous authority

**Source:** none. Rendezvous has no signing authority.

### 49.6 Cross-domain rules

1. No domain may exercise authority belonging to another.
2. Delegation is explicit.
3. Possession is not authority.
4. Boundaries are enforced at verification time.
5. Revocation authority does not depend on the revoked key.

---

## 50. Threat Model

### 50.1 Threat taxonomy

T1 Identity forgery. T2 Authorization forgery. T3 Revocation exposure. T4 Rollback. T5 Fork. T6 Replay. T7 MITM during pairing. T8 Endpoint poisoning. T9 Rendezvous observation. T10 Relay observation. T11 Subordinate key compromise. T12 Identity Root compromise. T13 DoS. T14 Abuse of shared infrastructure.

### 50.2 Threat-to-property mapping

| Threat | Property | Mechanism |
|--------|----------|-----------|
| T1 | Identity authenticity | Signed identity documents |
| T2 | Authorization authenticity | Signed grants and leases |
| T3 | Bounded revocation exposure | `max_offline_tolerance` |
| T4 | Monotonic state | Sequence numbers |
| T5 | Chain uniqueness | `chain_hash` |
| T6 | Object application control | Stream sequence state; object identity; validity intervals |
| T7 | Pairing integrity | PAKE with transcript binding |
| T8 | Endpoint authenticity | Signed reachability and service records |
| T9 | Metadata minimization | Opaque peer IDs |
| T10 | Traffic confidentiality | End-to-end encryption |
| T11 | Blast radius containment | Key role separation |
| T12 | (partial) Recovery | V1 treats root as anchor |
| T13 | (not addressed) | Deployment |
| T14 | (not addressed) | Deployment policy |

### 50.3 Explicit non-properties

- Anonymity.
- Availability.
- Metadata confidentiality against global observer.
- Protection against compromised endpoints.
- Protection against authorized-but-malicious peers.
- Protection against compromised Identity Root beyond V1 trust-anchor model.

---

## 51. Compromise Model and Blast Radius

### 51.1 Service Key compromise

**Blast radius:** one service's discovery metadata.

**Recovery:** revoke Service Key via identity document; issue new key.

### 51.2 Device Key compromise

**Blast radius:** one device's discovery metadata.

**Recovery:** revoke Device Key; issue new key.

### 51.3 Authorization Key compromise

**Blast radius:** all authorization state under the key, from compromise forward.

**Recovery is an identity-authority operation:**

1. Identity Root signs `KeyRevocation` with `effective_sequence`.
2. Objects signed by the compromised key at or after `effective_sequence` are invalid.
3. Principal issues new Authorization Key.

**Normative:**

> A revocation of an Authorization Key is an identity-authority operation and MUST NOT require the compromised key to sign its own revocation.

`effective_sequence = 0` invalidates the entire key history.

### 51.4 Identity Root compromise

**Blast radius:** the entire principal.

**Recovery:** V1 has no in-band recovery.

### 51.5 Device compromise

**Blast radius:** union of compromised keys' blast radii.

### 51.6 Rendezvous compromise

**Blast radius:** discovery only.

### 51.7 Relay compromise

**Blast radius:** transport for peers using the relay.

### 51.8 Compromise summary

| Asset | Blast radius | Recovery |
|-------|--------------|----------|
| Service Key | One service's discovery | Rotate via identity document |
| Device Key | One device's discovery | Rotate via identity document |
| Authorization Key | Authorization under it | Root revokes with `effective_sequence`; new key |
| Identity Root | Entire principal | None in V1 |
| Device | Union of held keys | Depends on keys held |
| Rendezvous | Discovery | Rotate rendezvous |
| Relay | Transport | Another relay or direct |

### 51.9 Invariants

1. Subordinate key compromise MUST NOT require replacing the Identity Root.
2. Subordinate key compromise MUST NOT affect unrelated keys.
3. Signing key compromise MUST NOT extend blast radius.
4. Infrastructure compromise MUST NOT affect identity or authorization state.
5. Revocation of a compromised key is authorized by a higher-authority key.

---

## 52. Service Identity, Service Binding, and Service Link

### 52.1 Service Identity

```
service_id  = opaque identifier
service_key = Ed25519 key pair
```

Stable across device replacement and network changes.

### 52.2 Service Binding

```
ServiceBinding {
    service_id
    service_public_key
    bound_to     : principal_id | device_id
    issued_at
    expires_at?
}
```

Signed as part of the identity document. Establishes which principal or device speaks for the service.

### 52.3 Service Link

```
service_link_id = opaque identifier
```

**Referential only.** Not an independently signed object.

**Normative:**

**N1.** A Service Link is not an authorization object.

**N2.** A Service Link MUST NOT contain capabilities, authorization constraints, lease validity, or equivalent.

**N3.** Presence, validity, or recognition of a Service Link MUST NOT authorize access.

**N4.** Authorization to a service is established exclusively through Grant and Lease state.

**N5.** A Service Link is a referential identifier. It is not signed, mutable, or independently authoritative.

**N6.** If two objects reference the same `service_link_id` but disagree, the objects are the source of truth.

**N7.** An attacker who invents a `service_link_id` gains nothing.

### 52.4 Cross-object behavior

A `service_link_id` is meaningful only in the context of the objects referencing it.

### 52.5 Service host migration

Service moves from one device to another **within the same principal**.

**Effect on authorization:**

- Grants and leases whose scope does not constrain the hosting device remain valid.
- Grants and leases whose scope constrains the hosting device are evaluated against their scope.
- Migration MUST NOT widen authorization.

### 52.6 Service ownership transfer

**V1 does not support service ownership transfer.**

### 52.7 Service lifecycle summary

| Object | Signed by | Purpose |
|--------|-----------|---------|
| Service Identity | (n/a) | Service identity |
| Service Binding | Identity Root (or delegated) | Binds identity to principal/device |
| Service Link | (n/a) | Referential identifier |
| Grant | Authorization Key | Authorizes subject |
| Lease | Authorization Key | Proves current validity |
| Service Record | Service Key | Current endpoint and metadata |
| Reachability Record | Device Key | Current device endpoints |

### 52.8 Service Record and Reachability Record

- Service Record describes how the service can be reached.
- Reachability Record describes where the hosting device can be reached.
- Neither overrides the other. Both are used. Neither grants authorization.

---

## 53. Failure Semantics and Recovery

### 53.1 General invariants

**F1** No failure silently grants authorization.

**F2** No failure silently extends authorization.

**F3** No failure silently changes identity state.

**F4** Availability is preserved where possible.

**F5** Security-relevant failure conditions are represented in local state sufficiently to enforce failure semantics.

**F6** Failures are recoverable where specified; terminal where specified.

### 53.2 Taxonomy

Discovery (§53.3), synchronization (§53.4), integrity (§53.5), validity (§53.6), fork (§53.7), freshness (§53.8), local (§53.9), pairing (§53.14).

### 53.3 Discovery failures

**53.3.1 Rendezvous unreachable.** Retry; rotate to next. State unchanged.

**53.3.2 Endpoint unreachable.** Failed connection is not evidence the peer is offline, compromised, or unauthorized. Record's protocol state unchanged. Local observation is soft.

**53.3.3 Conflicting reachability records.** Fork in reachability stream. Neither branch used. Resolution per §54.

**53.3.4 Malicious rendezvous.** Reject object; do not alter state.

### 53.4 Synchronization failures

**53.4.1 Stream gap.** `SYNCING` state. Use last accepted state. Gap MUST NOT become `FORKED`.

**53.4.2 Partial synchronization.** Use locally known objects for decisions determinable from them. Absent objects not assumed.

**53.4.3 Network partition.** Cached objects evaluated against normal rules. Leases may become `STALE`.

### 53.5 Integrity failures

**53.5.1 Malformed object.** Reject. State unchanged.

**53.5.2 Invalid signature.** Reject.

**53.5.3 Unknown object type.** Reject.

**53.5.4 Unknown issuer.** Reject as untrusted.

### 53.6 Validity failures

**53.6.1 Expired.** Excluded. State `EXPIRED`.

**53.6.2 Revoked.** Excluded. State `REVOKED`.

**53.6.3 Superseded.** Excluded. State `SUPERSEDED`.

**53.6.4 Unknown revocation.** Cache as state assertion. MUST remain effective when target is subsequently received.

### 53.7 Fork failures

**53.7.1 Conflicting stream states.** Stream `FORKED`. Use last accepted state.

**53.7.2 Conflicting identity documents.** Identity stream `FORKED`. Use last accepted identity state.

**53.7.3 Authorization continuity during identity fork.**

- Authorization state derived from last accepted identity state remains locally recognized.
- MUST NOT incorporate assertions from either disputed branch.
- Existing grants and leases continue to be evaluated against last accepted identity state.
- No new authorization state dependent on disputed branch may be accepted.

Invariant: *accepted state remains accepted; disputed state contributes nothing.*

### 53.8 Freshness failures

**53.8.1 Authorization refresh failure.** `last_successful_authorization_refresh` not updated. Leases may become `STALE`. Successful refresh transitions `STALE` → `VALID` only if grant remains `GRANTED`, no revocation applies, lease has not independently expired.

**53.8.2 Freshness source unavailable.** MUST NOT substitute undesignated sources.

### 53.9 Local failures

**53.9.1 Local storage loss.** All state lost; return to `UNKNOWN`.

**53.9.2 Clock forward jump.** Relative validity unaffected. Absolute validity may misclassify. Re-evaluation recomputes applicability; does NOT rewrite history.

**53.9.3 Clock backward jump.** As above. `issued_at` monotonicity violations rejected as temporal-policy violations, NOT malformed.

**53.9.4 Monotonic clock unavailable.** MUST NOT substitute wall clock.

### 53.10 Summary table

| Failure | Authorization impact | State impact | Recovery |
|---------|---------------------|--------------|----------|
| Rendezvous unreachable | None | None | Retry; rotate |
| Endpoint unreachable | None | Local observation only | Refresh; alternates |
| Conflicting reachability | None | Stream `FORKED` | External resolution |
| Malicious rendezvous | None | None | Deprioritize |
| Stream gap | Use last accepted state | `SYNCING` | Obtain intermediates |
| Partial sync | Use local state | None | Continue sync |
| Network partition | Leases may become `STALE` | None | Refresh |
| Malformed object | None | None | Discard |
| Invalid signature | None | None | Discard |
| Unknown object type | None | None | Discard |
| Unknown issuer | None | None | Discard |
| Expired object | Excluded | `EXPIRED` | New object |
| Revoked object | Excluded | `REVOKED` | Issue new |
| Superseded object | Excluded | `SUPERSEDED` | Use newer |
| Unknown revocation | None | Revocation cached | Apply on receipt |
| Fork | Use last accepted state | `FORKED` | §54 |
| Identity fork | Accepted state effective | Identity stream `FORKED` | §54 |
| Refresh failure | None until tolerance elapses | `STALE` | Successful refresh |
| Freshness source unavailable | As above | As above | Retry designated source |
| Local storage loss | All authorization lost | Return to `UNKNOWN` | Re-pair |
| Clock forward jump | Possible absolute misclassification | History unchanged | Restore clock |
| Clock backward jump | Possible absolute misclassification | History unchanged | Restore clock |
| Monotonic clock unavailable | Relative validity cannot be evaluated | None | Environmental |
| Pairing failure | None | None | Discard; retry |

### 53.11 Fail-closed vs. availability-preserving

**Fail-closed (authorization):** missing information MUST NOT grant authorization; failed refresh ≠ refresh; forked streams contribute nothing; expired/revoked/superseded excluded; gaps not filled by inference; local state loss not reconstructed from untrusted sources; persistent gaps not reinterpreted as forks.

**Availability-preserving (connectivity and discovery):** discovery retries permitted; relay use permitted; reconnections do not require re-validation; cached reachability MAY be used subject to signed validity; alternate rendezvous and endpoints MAY be tried.

### 53.12 Interaction with §50 and §51

§53 describes behavior under absence of information. §50 describes adversarial conditions. §51 describes compromise.

### 53.13 Conformance

1. MUST preserve local state under all failures unless failure is explicitly local.
2. MUST NOT interpret any failure as authorization.
3. MUST NOT extend validity or freshness based on failed operations.
4. MUST represent security-relevant failure conditions in local state.
5. MUST apply specified recovery paths.
6. MUST NOT invent recovery paths for authorization-relevant decisions.
7. MUST NOT conflate distinct failure conditions.

### 53.14 Pairing failures

Failed pairing: attempt discarded; no state created; ephemeral state destroyed; MAY retry with fresh session.

**Invariant:** an incomplete pairing has no partially committed security state.

---

## 54. Reconciliation and Conflict Resolution

### 54.1 Scope

Defines reconciliation of conflicting objects in the same stream, synchronization of persistent gaps, conflicting identity documents, conflicting reachability or service records, conflicting rendezvous manifests.

### 54.2 Principles

**R1** No new authority.

**R2** Issuer-scoped resolution.

**R3** Explicit resolution.

**R4** Preservation of accepted state until resolution.

**R5** Fail-closed if unresolved.

**R6** Resolution is a stream transition, not an override.

**R7** Resolutions are auditable.

### 54.3 Object classes

1. **StreamResolution** — resolves a fork in a single stream.
2. **IdentityContinuity** — establishes continuity across an orderly transition.

### 54.4 StreamResolution

```
StreamResolution {
    domain_separator   = "grid/stream-resolution/v1"
    sequence           // in the resolver's stream
    previous_hash?
    chain_hash
    signature

    issuer
    stream_id          // the disputed stream
    disputed_sequence
    disputed_hashes
    accepted_hash
    resolution_reason
    issued_at
    not_before
    expires_at
}
```

**Resolution authority:**

| Disputed stream | Resolution authority |
|-----------------|----------------------|
| `stream:identity` | Identity Root trusted before the fork |
| `stream:authorization:<K>` | Identity Root, or a resolution-authority key delegated before the fork |
| `stream:reachability:<D>` | Identity Root, or the device-authority key delegated before the fork |
| `stream:service:<S>` | Identity Root, or the service-authority key delegated before the fork |

**Normative:**

> A `StreamResolution` MUST be signed by an authority that is (a) above the disputed stream in the authority hierarchy and (b) trusted by the verifier from state accepted **before** the fork was observed.

> A key whose own stream is disputed MUST NOT sign the resolution for that stream.

> Trust for the resolution authority is evaluated against the verifier's accepted authority state **at the time the fork was first observed**, not against the current identity document.

> A `StreamResolution` MAY select among already-authenticated disputed branches. It MUST NOT introduce new object contents, authority, capabilities, bindings, or authorization state not already established by the selected branch.

> The `sequence` field of a `StreamResolution` refers to the **resolver's** stream. It MUST NOT be numerically compared with `disputed_sequence`, which belongs to a different sequence space.

> The resolution's own `sequence` MUST be monotonic within the resolver's stream. It is not compared with `disputed_sequence`.

**Acceptance rules:**

1. Signature validates.
2. Issuer has authority over `stream_id` per the table above.
3. Issuer's authority is trusted from a state accepted before the fork was observed.
4. `disputed_sequence` matches locally observed fork position.
5. `accepted_hash` ∈ locally observed `disputed_hashes`.
6. Resolution's `sequence` is monotonic within the resolver's stream.
7. The resolution's `chain_hash` and `previous_hash` chain correctly to the resolver's accepted state.
8. Not expired.

### 54.5 IdentityContinuity

#### 54.5.1 Model

An `IdentityContinuity` object authorizes the transition from a predecessor identity root to a successor identity root. The object is **sequence 1 of the successor identity stream**.

The predecessor identity stream terminates at the point of transition. The successor identity stream begins with the `IdentityContinuity` object itself.

#### 54.5.2 Object schema

```
IdentityContinuity {
    domain_separator           = "grid/identity-continuity/v1"
    sequence                   = 1
    // previous_hash omitted (per §3.5, sequence 1 has no previous_hash)
    chain_hash                 // chain_hash(1) of successor stream, per standard sequence-1 construction
    
    peer_id
    previous_root
    predecessor_terminal_chain_hash   // terminal chain_hash of predecessor identity stream
    new_root
    continuity_reason
    issued_at
    expires_at

    signature                  // two-element array [sig_prev, sig_new]
}
```

- `sequence` MUST be exactly 1.
- `previous_hash` is omitted (standard sequence-1 rule).
- `chain_hash` is the chain_hash(1) of the **successor** identity stream, computed per the standard sequence-1 chain construction in §3.5 / §45.2:
  ```
  chain_hash = SHA-256(canonical_cbor([
      "grid/chain/v1",
      initial_chain_hash(successor_stream),
      object_commitment(this_object)
  ]))
  ```
  where `initial_chain_hash(successor_stream) = SHA-256(canonical_cbor(["grid/chain-base/v1", domain_separator, stream_id]))` with the successor stream's `domain_separator` ("grid/identity-document/v1") and `stream_id` ("stream:identity").

**Known issue:** IdentityContinuity chain-base inconsistency across OBJECTS.md §3.5 (uses object's `domain_separator` for `initial_chain_hash`), OBJECTS.md §4.5 (registers "grid/identity-document/v1" for IdentityDocument), and PROTOCOL.md §54.5.2 (explicitly uses "grid/identity-document/v1" and "stream:identity" for successor stream). For IdentityContinuity (domain_separator "grid/identity-continuity/v1"), the chain-base uses a different domain_separator than the object's own. The specification must clarify whether the chain-base domain_separator is the stream's canonical domain_separator or the object's domain_separator. (open blocker)
- `predecessor_terminal_chain_hash` is the terminal `chain_hash` of the **predecessor** identity stream. This is a semantic field in the unsigned payload; it is NOT the chain construction's `previous_chain_hash` input (which for sequence 1 is `initial_chain_hash` of the successor stream). The two values are from different sequence spaces and MUST NOT be conflated.
- `new_root` is the successor Identity Root.
- `signature` is a two-element array `[sig_prev, sig_new]`, both over the same `signature_input`.
- `new_sequence` and `new_chain_hash` from v0.6 are removed.

#### 54.5.3 Stream semantics

```
Predecessor identity stream             Successor identity stream
    (issuer = previous_root)                (issuer = new_root)
        ...                                     IdentityContinuity
        sequence N                              sequence 1
        chain_hash = H_old                      chain_hash = H_new (chain_hash(1) of successor)
             |                                       |
             |  dual authorization                   |
             +
**Open blocker:** §54.5.4–§54.5.7 (verification rules, trust chain requirements, effect of acceptance, recovery from root compromise) are missing from both this snapshot and the prior. The diagram truncates at "dual authorization" with no closing content. Source loss vs intentional removal unconfirmed. (see design/KNOWN-LIMITATIONS.md §Unresolved Contradictions and §Open Investigation)

### 54.6 RendezvousUpdate

Rendezvous manifests are normal streams. Forks resolved by `StreamResolution` signed by the principal's Identity Root.

### 54.7 Persistent gaps

Persistent gaps are not forks. Resolved by obtaining missing objects, not by issuing resolution objects.

### 54.8 Non-stream conflicts

**Ambiguity rule:**

> If two independently valid signed objects assert incompatible authorization predicates for the same `(subject, service, capability)` — that is, one asserts the capability is authorized and another asserts it is not — and no rule in the Authority Precedence Table resolves the conflict, the verifier MUST NOT authorize the capability.

Non-authorization differences between signed objects are governed by the corresponding objects' semantics, not by the ambiguity rule.

### 54.9 Explicit non-mechanisms

- Voting.
- Timestamps as resolution.
- Availability as resolution.
- Preference order among sources.
- Peer voting on disputed state.
- Automatic resolution.
- Transfer of authority between principals without dual signature.

### 54.10 Resolution availability

For orderly transitions: Identity Root available.

For unplanned events: out-of-band recovery, administrative re-acceptance, or terminal abandonment of old Peer ID.

### 54.11 Reconciliation state

```
ReconciliationState {
    stream_id
    state                 // IDLE | SYNCING | FORKED
    disputed_sequence
    disputed_hashes
    pending_resolution
    last_reconciliation
}
```

### 54.12 Interaction

- Fork detection: §45.4.
- Fork handling: §47.12.
- Gap handling: §47.13.
- State machines: §48.
- Authority domains: §49.
- Failure semantics: §53.
- Authority Precedence: §58.5.

### 54.13 Conformance

1. MUST NOT resolve `FORKED` by mechanisms other than valid `StreamResolution` or `IdentityContinuity`.
2. MUST NOT resolve `SYNCING` by mechanisms other than obtaining intermediates.
3. MUST preserve last accepted state until resolution.
4. MUST retain disputed artifacts and resolution.
5. MUST NOT authorize ambiguous conflicts.
6. MUST NOT treat time, availability, source preference, or voting as resolution.
7. MUST accept `IdentityContinuity` only with dual signature.

---

## 55. Application Integration and API

### 55.1 Principle

Applications consume authenticated identity and authorized connections. They do not receive raw endpoints, relay credentials, or rendezvous URLs.

### 55.2 Local interface

```
grid.discover()                     → list of known peers
grid.resolve(peer_id)               → peer state
grid.connect(service_link_id, cap)  → local connection handle
grid.authorize(peer_id, capability) → authorization decision
grid.revoke(object_id)              → issue revocation
grid.status()                       → daemon and peer state
```

### 55.3 Connection handles

```
{
    "connection_id": "random-id",
    "local_url": "http://127.0.0.1:41873",
    "expires_at": "2026-10-04T21:00:00Z"
}
```

The application uses the local URL. It does not receive the underlying endpoint, relay credentials, or peer ID.

### 55.4 Authorization inputs

When an application requests a connection, the daemon evaluates `authorized` (§40.6). If authorized, a local connection is established. If not, the daemon returns an error.

### 55.5 Application identity

Applications MAY receive an authenticated Peer Principal ID for the peer on the other end of a connection.

### 55.6 Enforcement boundary

Enforcement may occur through transport configuration, firewall rules, proxying, or a combination.

### 55.7 Integration with existing applications

```
Application → Grid Network.connect() → daemon → overlay → peer
```

---

## 56. V1 Scope and Kernel

V1 MUST include:

1. Peer Principal identity.
2. Opaque Peer IDs.
3. Identity Root.
4. Device keys.
5. Service keys.
6. Signed identity documents.
7. Key rotation.
8. Authorization Keys.
9. Grants (immutable).
10. Leases with relative validity.
11. Authorization freshness.
12. Terminal revocation.
13. Key revocation with `effective_sequence`.
14. Relationship assertions and terminations.
15. Human-mediated QR/copy-paste pairing.
16. Established PAKE.
17. Canonical object encoding.
18. One self-hostable rendezvous service.
19. Reachability records.
20. Direct connectivity.
21. WireGuard integration.
22. Offline verification.
23. Positive and negative test vectors.

**Known issue:** Test vectors have not been created. Their production is blocked on OBJECTS.md §§6–10 schema completion and PAKE selection (§25). (future work; see design/KNOWN-LIMITATIONS.md §Open Design Decisions)

Deferrable to V1.1: multi-server rendezvous, relay fallback, service host migration tooling, comprehensive failure test coverage.

---

## 57. Explicitly Deferred Features

Deferred to future versions:

- DHT-based discovery.
- Federation between rendezvous servers.
- Peer-assisted gossip.
- Groups.
- Sophisticated recovery (threshold, social, hardware-backed).
- Multipath routing.
- Automatic service migration.
- Service ownership transfer.
- Reputation and liveness scoring.
- Advanced metadata protection.
- Delegated administration.
- Temporary guests.

---

## 58. Normative Signing-Authority Matrix

### 58.1 Purpose

For each object type, the key role authorized to sign it.

### 58.2 Matrix

| Object | Authorized signer |
|--------|-------------------|
| IdentityDocument | Identity Root |
| DeviceBinding | Identity Root (or delegated device-authority key) |
| ServiceBinding | Identity Root (or delegated service-authority key) |
| KeyBinding | Identity Root |
| KeyRevocation | Identity Root |
| RelationshipAssertion | One principal's Identity Root (the issuer) |
| RelationshipTermination | One principal's Identity Root (the terminating principal) |
| Principal RendezvousManifest | Principal's Identity Root |
| OperatorManifest | Operator's Identity Root |
| Grant | Authorization Key |
| Lease | Authorization Key |
| GrantRevocation | Authorization Key |
| LeaseRevocation | Authorization Key |
| ServiceRecord | Service Key |
| ReachabilityRecord | Device Key |
| StreamResolution | Pre-fork authority above the disputed stream |
| IdentityContinuity | Both previous and new Identity Roots (dual signature) |
| RelayTicket | Relay Authority Key |
| RelayNodeRecord | Relay Node Key |

### 58.3 Delegation rules

- Delegation is expressed inside the identity document.
- A subordinate key's authority is exactly what the delegating key expressed.
- Revocation of a subordinate key does not affect keys not derived from it.

### 58.4 Cross-domain prohibition

An object signed by a key whose authority does not cover that object type MUST be rejected.

### 58.5 Authority Precedence Table

The Governing authority column has exactly four values:

- **A governs** — Object A's authority determines the outcome.
- **B governs** — Object B's authority determines the outcome.
- **No conflict** — Objects describe orthogonal properties.
- **Composed** — Objects contribute different predicates to the same decision.

**Where two objects contribute different predicates to a decision, the table MUST NOT be interpreted as establishing precedence between them.**

This table defines precedence for all protocol-defined pairs for which authority interaction or authorization ambiguity is possible. Pairs not listed are orthogonal unless another normative section explicitly defines their interaction.

#### Identity-domain pairs

| A | B | Governing authority | Notes |
|---|---|---------------------|-------|
| Identity Document | Service Binding | A governs | Contained in identity document |
| Identity Document | Device Binding | A governs | Contained in identity document |
| Identity Document | Key Revocation | Composed | Identity establishes trust; revocation removes it |
| Identity Document | RelationshipAssertion | No conflict | Identity is independent of recognition |
| Identity Document | Reachability Record | No conflict | Identity is independent of location |
| Identity Document | Service Record | No conflict | Identity is independent of service metadata |
| Identity Document | Rendezvous Manifest | No conflict | Identity is independent of discovery |

#### Relationship-domain pairs

| A | B | Governing authority | Notes |
|---|---|---------------------|-------|
| RelationshipAssertion | RelationshipAssertion (same `relationship_id`, different issuers) | No conflict | Both required for `RECOGNIZED` |
| RelationshipAssertion | RelationshipAssertion (same `relationship_id`, same issuer, differing sequence) | Higher sequence governs | Stream-order supersession |
| RelationshipAssertion | RelationshipTermination | B governs | Termination overrides |
| RelationshipTermination | RelationshipAssertion | A governs | Terminal; subsequent assertion does not reactivate |
| RelationshipAssertion | Grant | Composed | Assertion establishes recognition; Grant establishes authorization |
| RelationshipAssertion | RendezvousManifest | No conflict | Orthogonal |
| RelationshipTermination | Grant | B governs | Termination invalidates authorization derived from relationship |

#### Authorization-domain pairs

| A | B | Governing authority | Notes |
|---|---|---------------------|-------|
| Grant | Lease | Composed | Grant supplies scope; Lease establishes current validity |
| Grant | Grant Revocation | B governs | Revocation overrides grant |
| Grant | Relationship | Composed | Relationship establishes existence; Grant establishes scope |
| Grant | Key Revocation | A governs for key validity; B retains its own intrinsic semantics | Revocation invalidates at or after `effective_sequence` |
| Grant | Service Link | No conflict | Service Link referential only |
| Grant | Reachability Record | No conflict | Authorization and location orthogonal |
| Grant | Service Record | No conflict | Authorization and service description orthogonal |
| Grant | Rendezvous Manifest | No conflict | Authorization and discovery orthogonal |
| Grant | Relay Ticket | A governs | Authorization state governs |
| Lease | Lease Revocation | B governs | Revocation overrides lease |
| Lease | Relationship | Composed | Relationship establishes existence; Lease inherits grant scope |
| Lease | Key Revocation | A governs for key validity; B retains its own intrinsic semantics | Revocation invalidates at or after `effective_sequence` |
| Lease | Service Link | No conflict | Service Link referential only |
| Lease | Reachability Record | No conflict | Authorization and location orthogonal |
| Lease | Relay Ticket | A governs | Authorization state governs |
| Authorization Key State | Grant | A governs for key validity; B retains its own intrinsic semantics | Revoked key invalidates covered grants |
| Authorization Key State | Lease | A governs for key validity; B retains its own intrinsic semantics | Revoked key invalidates covered leases |
| Key Revocation | Grant | A governs for key validity; B retains its own intrinsic semantics | |
| Key Revocation | Lease | A governs for key validity; B retains its own intrinsic semantics | |

#### Service-domain pairs

| A | B | Governing authority | Notes |
|---|---|---------------------|-------|
| Service Binding | Service Record | A governs | Binding establishes authority |
| Service Binding | Grant | No conflict | Binding establishes ownership; Grant establishes authorization |
| Service Binding | Lease | No conflict | Binding establishes ownership |
| Service Binding | Revocation | No conflict | Orthogonal |
| Service Binding | Reachability Record | No conflict | Binding and location orthogonal |
| Service Record | Reachability Record | Composed | Service Record describes service endpoint; Reachability describes device path |
| Service Record | Grant | No conflict | Orthogonal |
| Service Record | Lease | No conflict | Orthogonal |
| Service Record | Revocation | No conflict | Orthogonal |
| Service Record | Relay Ticket | No conflict | Orthogonal |

#### Reachability-domain pairs

| A | B | Governing authority | Notes |
|---|---|---------------------|-------|
| Device Binding | Reachability Record | A governs | Binding establishes which device |
| Reachability Record | Relay Ticket | No conflict | Path description and permission orthogonal |
| Reachability Record | Rendezvous Manifest | No conflict | Orthogonal |
| Reachability Record | Grant | No conflict | Orthogonal |
| Reachability Record | Lease | No conflict | Orthogonal |

#### Infrastructure-domain pairs

| A | B | Governing authority | Notes |
|---|---|---------------------|-------|
| Rendezvous Manifest | Any signed object | B governs | Rendezvous has no signing authority |
| Relay Ticket | Grant | A governs | Authorization state governs |
| Relay Ticket | Lease | A governs | Authorization state governs |
| Relay Ticket | Reachability Record | No conflict | Orthogonal |

#### Chain and stream-state pairs

| A | B | Governing authority | Notes |
|---|---|---------------------|-------|
| New Identity Branch | Accepted Branch | B governs | Fork requires external resolution |
| Gap in Stream | Accepted Stream | B governs | Gap requires intermediate objects |
| New Valid Lease | Expired Lease | A governs | Provided grant remains valid |
| Identity Root State | Subordinate-Key Assertion | A governs | Root-authoritative |

#### Identity-continuity pairs

| A | B | Governing authority | Notes |
|---|---|---------------------|-------|
| IdentityContinuity | Predecessor IdentityDocument | A governs | Transition supersedes predecessor stream |
| IdentityContinuity | Successor IdentityDocument | Composed | Continuity establishes successor stream |
| IdentityContinuity | Prior Trust Anchor | Composed | New root trusted only if chain terminates at previously trusted root |

#### Cross-cutting

| A | B | Governing authority | Notes |
|---|---|---------------------|-------|
| Service Link | Any signed object referencing it | Referencing object governs | Service Link carries no semantics beyond use as shared identifier |

### 58.6 Vocabulary consistency

Where the governing authority is "A governs for key validity; B retains its own intrinsic semantics," this indicates the object's *intrinsic* state is unchanged; only its role in authorization decisions is affected.

---

## 59. Implementation Requirements

### 59.1 Required components

1. Object encoding and decoding (canonical CBOR).
2. Signature and verification.
3. Hash computation.
4. Object type dispatch (domain separators).
5. Identity document validation.
6. Stream tracking.
7. Authority validation.
8. Authorization evaluation.
9. Failure handling per §53.
10. Reconciliation per §54.
11. Local trust anchor storage.
12. Rendezvous client.

### 59.2 Recommended components

1. Local API server.
2. WireGuard integration.
3. Reachability publication.
4. NAT traversal.
5. Relay client.

### 59.3 Interoperability requirements

Two independent implementations MUST interoperate on: canonical encoding, signature verification, identity document validation, stream state management, authorization decisions, failure handling.

### 59.4 State durability

Trust anchors and accepted stream state MUST be durable. Local observation history for relative validity MUST be durable.

### 59.5 Cryptographic requirements

Ed25519, SHA-256, deterministic CBOR.

---

## 60. Test Vectors and Conformance

**Known issue:** Test vectors have not been created. Their production is blocked on OBJECTS.md §§6–10 schema completion and PAKE selection (§25). (future work; see design/KNOWN-LIMITATIONS.md §Open Design Decisions)

### 60.1 Purpose

Test vectors define exact byte sequences and their expected interpretations.

### 60.2 Required test vectors

For each object type: canonical encoding, hash, payload hash, signature, verification, tampered field, wrong domain separator, wrong schema version.

### 60.3 Negative test vectors

Required negative vectors: non-minimal integer encoding, incorrectly ordered map keys, floating-point field, duplicate set entry, set entries out of canonical order, missing required field, extra unknown field, oversized field, replayed object, expired object, revoked object, invalid `previous_hash`, invalid `chain_hash`, wrong issuer for object type, signature from wrong key role, fork at same sequence, gap in stream, non-canonical CBOR encoding.

### 60.4 Conformance levels

- **Level 1:** Encoding.
- **Level 2:** Verification.
- **Level 3:** Authorization.
- **Level 4:** Failure handling.
- **Level 5:** Reconciliation.

### 60.5 Vector normative invariant

Where prose and a normative test vector appear to conflict, the specification must be corrected so that prose and vector agree. Test vectors are not an alternative interpretation of ambiguous prose.

### 60.6 Rejection classes

A conforming implementation MUST reject every negative test vector with the specified rejection class (per OBJECTS.md §5.7).

**Known issue:** The rejection classes in OBJECTS.md §10.1 must align with the `expected_rejection` values in negative test vectors. Test vectors do not yet exist. (future work; see OBJECTS.md §Unresolved Dependencies item 8)

---

## 61. Verifier Conformance Scenarios

### 61.1 Fresh peer

**Initial:** No local state.

**Incoming:** Pairing completes; relationship assertions exchanged; grant and lease received.

**Expected:** Peer `KNOWN`; relationship `RECOGNIZED`; grant `GRANTED`; lease `VALID`. Authorization succeeds.

### 61.2 Offline peer returns

**Initial:** Peer `KNOWN`, `RECOGNIZED`, valid grant and lease.

**Incoming:** Reachability record with new endpoint.

**Expected:** Peer reachable at new endpoint. Identity and authorization unchanged.

### 61.3 Lease expires while offline

**Initial:** Valid lease. Verifier offline past expiry.

**Incoming:** Reachability record. No new lease.

**Expected:** Lease `EXPIRED`. Authorization fails.

### 61.4 Revocation occurs while offline

**Initial:** Valid lease.

**Incoming:** Revocation for the lease.

**Expected:** Lease `REVOKED`. Authorization fails.

### 61.4b Revocation arrives before its target

**Initial:** No knowledge of grant G.

**Incoming:** Revocation for G, then G.

**Expected:** Revocation cached. G rejected on first observation.

### 61.5 Authorization-key compromise

**Initial:** Active Authorization Key K with the following stream:

```
seq 100  Grant G1
seq 101  Lease L1 (for G1)
seq 102  Lease L2 (for G1)
seq 103  GrantRevocation (revokes G1)
seq 104  Grant G2
seq 105  Lease L3 (for G2)
seq 106  LeaseRevocation (revokes L3)
```

**Incoming:**

```
Identity Root stream:
seq 201  IdentityDocument
seq 202  KeyRevocation { key_id=K, effective_sequence=103 }
```

**Expected applicability:**

| Seq | Object | Applicable | Reason |
|-----|--------|------------|--------|
| 100 | Grant G1 | yes | before `effective_sequence` |
| 101 | Lease L1 | yes | before |
| 102 | Lease L2 | yes | before |
| 103 | GrantRevocation | no | at `effective_sequence` |
| 104 | Grant G2 | no | after |
| 105 | Lease L3 | no | after |
| 106 | LeaseRevocation | no | after |

**Further state:**

- G1 `GRANTED`.
- L1, L2 remain `VALID` (their revoking object at seq 103 is not applicable).
- G2 not applicable; not `REVOKED` — outside trusted window.
- L3 not applicable.

### 61.6 Key rotation mid-chain

**Initial:** Peer P with trusted root R1, accepted identity stream at sequence N, chain hash `H_old`.

**Incoming:** `IdentityContinuity` object with `previous_root = R1`, `previous_chain_hash = H_old`, `new_root = R2`, `sequence = 1`, dual signature.

**Expected:** Trusted root updated to R2. Successor stream begins at sequence 1. Predecessor stream retained for audit.

### 61.7 Identity fork

**Initial:** Accepted identity state at sequence 10, hash H.

**Incoming:** Identity document at sequence 10, hash H'.

**Expected:** Identity stream `FORKED`. Accepted state (H) remains effective.

### 61.8 Gap in received chain

**Initial:** Accepted sequence 10.

**Incoming:** Object at sequence 15.

**Expected:** Stream `SYNCING`. Authorization uses last accepted state (sequence 10). Verifier attempts to obtain 11–14. Stream does NOT become `FORKED`.

### 61.9 Conflicting rendezvous data

**Initial:** Cached reachability record R1 at endpoint E1.

**Incoming:** Reachability record R2 at same sequence, different chain hash.

**Expected:** Reachability stream `FORKED`. Neither endpoint used.

### 61.10 Stale reachability record

**Initial:** Cached reachability record within validity.

**Incoming:** Attempted connection fails.

**Expected:** Record's protocol state unchanged. Local observation is soft.

### 61.11 Direct path fails, relay succeeds

**Initial:** Peer authorized, reachability record with candidates.

**Incoming:** Direct connection fails; relay path established.

**Expected:** Connection established via relay. Authorization unchanged.

### 61.12 Relay disappears during session

**Initial:** Active session via relay.

**Incoming:** Relay unreachable.

**Expected:** Session disrupted. Verifier attempts direct path.

### 61.13 Grant reissued after terminal revocation

**Initial:** Grant G1 revoked.

**Incoming:** New grant G2 with new `grant_id`, same subject, same capability.

**Expected:** G1 remains `REVOKED`. G2 is `GRANTED`. No state inherited from G1.

### 61.14 Freshness elapses without revocation

**Initial:** Valid lease, relative validity 30 days, `max_offline_tolerance` 7 days.

**After 7 days offline:** authorization_fresh = false. Lease `STALE`. Authorization fails.

**Successful refresh on day 10:** `authorization_fresh` restored. Lease `VALID`.

**After 30 days offline without refresh:** Lease `EXPIRED`. Refresh on day 31 does NOT restore.

### 61.15 Local storage loss

**Initial:** Peer P `KNOWN`, `RECOGNIZED`, authorized.

**Incoming:** Local storage lost.

**Expected:** Verifier returns to `UNKNOWN`. Trust anchor must be re-established via pairing.

### 61.16 Relationship assertion pair

**Initial:** No local state for peer P.

**Incoming:** `RelationshipAssertion` A from peer P naming local principal as subject.

**Expected:** Relationship state `PENDING`. Does not contribute to authorization.

**Incoming:** Local assertion naming peer P as subject.

**Expected:** Relationship state `RECOGNIZED`. Contributes to authorization.

### 61.17 Relationship termination

**Initial:** Relationship `RECOGNIZED`.

**Incoming:** `RelationshipTermination` from remote principal.

**Expected:** Relationship state `TERMINATED`. Terminal. Subsequent assertions do not reactivate; new `relationship_id` required.

---

## 62. Future Extensions

### 62.1 Chain-extension proofs

Authenticated proofs permitting skip-ahead while preserving fork detection.

### 62.2 Sophisticated recovery

Threshold, social, hardware-backed. Must not introduce a new authority.

### 62.3 Delegated administration

Delegation of specific identity-document operations without exposing the Identity Root.

### 62.4 Groups

Multi-principal structures. Must not violate the "no new authority" principle.

### 62.5 Service ownership transfer

Authenticated transfer with dual signature. V1 does not support this.

### 62.6 Rendezvous federation and gossip

Bounded anti-entropy with explicit quotas.

### 62.7 DHT-based discovery

Only if the above prove insufficient. Must not become an authority.

### 62.8 Metadata protection

Rotating pseudonyms for rendezvous lookups.

### 62.9 Reputation and liveness scoring

Explicitly out of scope for identity. Belongs in deployment-layer policy.

### 62.10 Documented anti-patterns

- **XOR-based endpoint obfuscation.** Provides no confidentiality against parties holding the key, cannot support revocation.
- **Shared-key encryption for endpoint records.** Same issues.
- **DNS-like hierarchical naming.** Protocol identifiers are opaque and flat.
- **Timestamp-based fork resolution.** Wall-clock time is not a resolution mechanism.
- **Automatic recovery from Identity Root compromise.** No in-band mechanism exists or is proposed.
- **Dual-signature objects in a single stream.** Adopted model uses per-principal assertions in per-principal streams.
- **Global Sybil resistance in the protocol.** Identity quantity does not grant authority; Sybil resistance belongs at the admission policy layer of specific services, not in the identity kernel.
- **PoW as a foundational mechanism.** Optional admission control at the margins, not a protocol primitive.

---

## 63. Project Structure and Document Map

### 63.1 Purpose

This section defines how the project is organized: which layers exist, which documents hold which material, and how the layers relate.

This section is **informative** with respect to the protocol. It does not add normative requirements. It documents the intended structure of the specification as a whole.

### 63.2 Core insight

The entire project reduces to one sentence:

> **Grid Network is not a decentralized VPN. Grid Network is a cryptographic identity and authorization layer that turns whatever network connectivity happens to exist into a usable, replaceable connectivity fabric.**

Everything the protocol does, it does to answer one of these six questions:

| Question | Layer |
|----------|-------|
| Who is this? | Identity |
| Do we recognize each other? | Relationship |
| What may they access? | Authorization |
| Is that permission still valid? | Lease |
| Where can I currently find them? | Reachability |
| How should I get there? | Connectivity |

The protocol is responsible for the first five. The sixth is a separate layer that consumes the first five.

### 63.3 Four-layer model

```
┌──────────────────────────────────────────────────────────┐
│  LAYER 4 — STRATEGY                                       │
│  Vision, ecosystem, business model, roadmap               │
├──────────────────────────────────────────────────────────┤
│  LAYER 3 — CONNECTIVITY ARCHITECTURE                      │
│  Path abstraction, relay model, future multipath          │
├──────────────────────────────────────────────────────────┤
│  LAYER 2 — SECURITY & IMPLEMENTATION                      │
│  Threat model, verifier rules, parser requirements        │
├──────────────────────────────────────────────────────────┤
│  LAYER 1 — PROTOCOL KERNEL                                │
│  Identity, relationships, authorization, leases,          │
│  revocation, reachability, cryptographic objects          │
└──────────────────────────────────────────────────────────┘
```

Each layer is independent. Layer 1 does not depend on Layer 3; Layer 3 consumes Layer 1. Layer 4 does not constrain Layer 1; Layer 4 explains why Layer 1 matters.

### 63.4 Layer 1 — Protocol Kernel

**Contains:** the frozen cryptographic core. Peer Principal, identity documents, relationship assertions, grants, leases, revocation, key rotation, identity continuity, reachability records, rendezvous manifests, relay tickets, canonical CBOR, domain separation, sequence/chain rules, verifier local state, freshness, offline verification, authority boundaries, failure semantics, reconciliation.

**Corresponds to:** this document (§1–§62), plus `OBJECTS.md`.

**Change rate:** slow, near-frozen. Changes require a version bump (§64).

### 63.5 Layer 2 — Security & Implementation

**Contains:** the material that makes Layer 1 implementable safely. Threat model, blast-radius analysis, verifier processing rules, parser hardening, resource limits, rate limiting, anti-amplification, crash/restart behavior, persistent state integrity, concurrency constraints, fuzzing requirements, conformance levels.

**Corresponds to:** `design/THREAT-MODEL.md` and `design/DECISIONS.md` (existing).

**Change rate:** moderate, technical.

**Key principle:** every security mechanism needs a specific boundary it protects. Before adding a mechanism, answer: what authority or resource does it protect? What attack does it prevent? What happens if removed? What complexity does it introduce?

### 63.6 Layer 3 — Connectivity Architecture

**Contains:** the layer above the protocol kernel that turns "this connection is authorized" into "this connection is established." Path abstraction, direct-first preference, NAT traversal coordination, relay selection and fallback, relay capability model, path measurement, path selection, future multipath.

**Corresponds to:** `CONNECTIVITY.md` (to be drafted).

**Change rate:** moderate, engineering.

**V1 boundaries:** direct connectivity preferred; simple relay fallback; relay resources capability-bounded; relay untrusted. Path measurement, path selection, multipath, adaptive scheduling are deferred but must not be precluded.

**Non-preclusion constraint:** V1 objects and state MUST NOT preclude future Layer 3 capabilities. Reachability records MAY carry multiple candidates; path identity is distinct from connection identity; authorization is path-agnostic; relay selection is not baked into signed objects.

### 63.7 Layer 4 — Strategy

**Contains:** product positioning, disruption analysis, ecosystem model, commercial considerations, adoption paths, roadmap.

**Corresponds to:** `VISION.md`, `ECOSYSTEM.md`, and `ROADMAP.md` (to be drafted).

**Change rate:** slow, narrative.

**One strategy concept that belongs in the architecture:** relay providers are replaceable. This is a consequence of the authority separation, not a policy, and is already a Layer 1 property.

### 63.8 Document structure

```
grid/
│
├── PROTOCOL.md               ← this document (v0.6.2)
├── OBJECTS.md                ← canonical encoding, schemas, vectors
├── CONNECTIVITY.md           ← connectivity architecture (existing)
├── VERSIONING.md             ← §64 of this document (may split)
├── TEST-VECTORS/             ← byte-exact normative cases
├── VISION.md                 ← product positioning (to draft)
├── ECOSYSTEM.md              ← community + commercial (to draft)
└── ROADMAP.md                ← V1, V1.x, V2, research (existing)
```

### 63.9 Document responsibilities

|| Document | Layer | Audience | Change rate ||
|----------|-------|----------|-------------|
|| `PROTOCOL.md` | 1 | Protocol implementers | Slow ||
|| `OBJECTS.md` | 1 | Protocol implementers | Slow ||
|| `design/THREAT-MODEL.md` | 2 | Implementers, reviewers | Moderate ||
|| `design/DECISIONS.md` | 2 | Builders | Moderate ||
|| `operations/CONNECTIVITY.md` | 3 | Connectivity engine builders | Moderate ||
|| `VERSIONING.md` | cross | All | Slow ||
|| `TEST-VECTORS/` | 1 | Implementers, testers | Additive ||
|| `VISION.md` | 4 | Stakeholders, adopters | Slow ||
|| `ECOSYSTEM.md` | 4 | Operators, vendors | Slow ||
|| `ROADMAP.md` | 4 | Everyone | Moderate ||

---

## 64. Versioning and Evolution

### 64.1 Versioning model

Each protocol object type carries its schema version in its `domain_separator`:

```
grid/identity-document/v1
grid/relationship-assertion/v1
grid/stream-resolution/v1
```

A new schema version uses a new domain separator:

```
grid/identity-document/v2
```

Domain separators are never reused. A `v1` schema is frozen once the object type is declared stable in a released protocol version.

### 64.2 Adding new object types

New object types are added by registering a new `domain_separator` value. The registry is normative and lives in `OBJECTS.md`.

Adding a new object type does not change existing schemas. Existing implementations may continue to reject unknown domain separators (per `OBJECTS.md` §4.5) without affecting their operation on known types.

### 64.3 Implementation version signaling

Implementations signal supported domain separators through the objects they produce. There is no separate "capabilities" negotiation in V1.

A verifier that receives an unknown `domain_separator` rejects the object. It does not fall back to an older interpretation, and it does not attempt to interoperate with an unknown schema.

### 64.4 Protocol version bumps

A protocol version bump (v0.6.2 → v0.7) occurs when:

- A new object type is registered, OR
- An existing object type's semantics change in a way that would cause two conforming implementations to disagree, OR
- An authority boundary changes.

Editorial clarifications do not trigger a version bump.

### 64.5 Compatibility guarantees

Within a major protocol version (`v0.x`), the following are guaranteed:

- No existing object type's schema changes.
- No existing authority boundary changes.
- No existing rejection class changes meaning.
- New object types may be added without invalidating existing ones.

Across major protocol versions, no compatibility is guaranteed. Implementations may support multiple major versions if they choose.

### 64.6 Governance

V1 governance is **not defined**. This document acknowledges that:

- Future changes require a decision process.
- The decision process will matter more as independent implementers appear.
- The process should be chosen deliberately, not drifted into.

Options for future consideration:

- Single reference implementation (early SSH model).
- Benevolent dictatorship (Python, Linux kernel model).
- Standards-body-like governance (TLS, DNS model).

The choice is deferred. What matters now is acknowledging that the choice must be made before the protocol is deployed at scale.

### 64.7 Deprecation

Object types are deprecated by:

1. Removing the `domain_separator` from the recommended registry.
2. Documenting the removal and the reason.
3. Retaining the old schema for reference.

Deprecated schemas are not removed from the protocol. Implementations that already support them may continue to. New implementations should not add support for them.

---

## 65. Triage Decisions for V1 Scope

### 65.1 Purpose

This section records the triage decisions made about which concepts belong in the protocol kernel, which belong in adjacent documents, and which are deferred. It is **informative** with respect to the protocol but **normative** with respect to project scope.

### 65.2 Keep as fundamental (Protocol Kernel)

- Identity (Principal, Peer ID, Identity Root)
- Relationships (assertion pairs, termination)
- Authorization (grants)
- Leases
- Revocation (terminal)
- Key hierarchy (Device, Service, Authorization keys)
- Freshness
- Reachability
- Service identity, binding, link
- Direct-first connectivity
- Untrusted relay
- Relay tickets
- Capability-based relay resources
- Provider replaceability
- Deterministic local verification
- Atomic state transitions
- Failure-does-not-grant-authority
- Canonical encoding
- Domain separation
- Sequence/chain rules
- Verifier local state

### 65.3 Keep, but as architecture rather than V1 protocol

These concepts are preserved as architectural abstractions. They are **not** defined as V1 protocol objects, and V1 implementations are not required to produce or consume them. They are listed here so that V1 does not preclude their future introduction.

- `PathSet` as an abstraction (not a V1 wire object)
- Path measurement
- Path selection
- Path diversity
- Multipath
- Adaptive scheduling
- Geographic/ASN diversity
- Dynamic capacity

### 65.4 Keep as implementation/security guidance

These belong in `design/THREAT-MODEL.md` and `design/DECISIONS.md`, not in the protocol:

- Resource limits on externally supplied objects
- Anti-amplification rules
- Parser hardening
- Crash/restart behavior
- Persistent-state integrity
- Fuzzing requirements
- Concurrency/race-condition testing
- Power-loss testing
- Key-compromise/recovery testing
- Normative security test vectors
- Maximum object/message sizes
- Connection/session rate limiting
- Metadata/privacy threat model
- Threat model for malicious relay/coordinator

### 65.5 Keep as strategic vision

These belong in `VISION.md`, `ECOSYSTEM.md`, and `ROADMAP.md`:

- Community relay infrastructure
- Commercial relay providers
- Open connectivity substrate
- Vendor-neutral device connectivity
- NAS/home-server/IoT integration
- Commercial managed services
- Enterprise layer
- Replacement of proprietary remote-access clouds
- Reduced dependence on DDNS
- Reduced dependence on proprietary tunnel services

### 65.6 Defer hard

These are deferred to future versions or research. They are not in scope for V1 or V1.x:

- FEC
- Relay marketplace
- Relay payments
- Reputation and liveness scoring
- Global relay economics
- Global Sybil resistance
- Proof-of-work as a protocol primitive
- Distributed routing consensus
- DHT
- Anonymous routing
- Global capacity allocation
- Complicated path optimization
- Blockchain
- Global ledger
- Mining
- Global consensus
- Token economics
- Global transaction ordering

### 65.7 Discard from main architecture

These have been considered and rejected. They appear in §62.10 as documented anti-patterns. They are restated here for completeness:

- XOR-based endpoint obfuscation as a security mechanism
- Shared-key encryption for endpoint records
- DNS-like hierarchical naming
- Timestamp-based fork resolution
- Automatic recovery from Identity Root compromise
- Dual-signature objects in a single stream
- Global Sybil resistance in the protocol kernel
- PoW as a foundational mechanism
- "Grid Network can burst around ISP throttling" as a feature framing (underlying observation retained as research note)

### 65.8 Deferral principle

The following principle applies to every proposal to add a mechanism, object, or feature:

> Do not introduce a security mechanism merely because an attack is theoretically possible. Introduce it when there is a concrete authority, resource, or trust boundary that needs protecting.

Before adding a mechanism, answer:

1. What authority or resource does it protect?
2. What specific attack does it prevent?
3. What happens if it is removed?
4. What new complexity does it introduce?

If any answer is unsatisfactory, the mechanism is premature.

This principle is why the kernel has no proof-of-work, no DHT, no reputation system, no global Sybil resistance, and no anonymous routing. Each of those would introduce complexity without protecting a specific boundary that the protocol's existing separations do not already protect.

---

## Final Protocol Statement

A Peer Principal is a durable cryptographic identity.

Devices, services, and infrastructure are subordinate to it and replaceable.

Relationships between principals are explicit and derived from paired per-principal assertions.

Authorization is directional, scoped, and temporary.

Leases provide bounded proof of current authorization.

Revocation is terminal.

Keys can rotate without changing principal identity.

Reachability is ephemeral and untrusted.

Rendezvous infrastructure provides discovery but no authority.

Transport is pluggable.

The resulting security question:

> Can the verifier, using its trusted anchors and locally available signed state, deterministically establish who the peer is, what it is authorized to do, whether that authorization is currently valid, and whether it has been revoked?

If the answer is yes, the peer can be trusted regardless of its current IP address, NAT mapping, rendezvous provider, relay, physical network, or whether it has been offline for months.

That is the fundamental purpose of the Grid Network Protocol.
