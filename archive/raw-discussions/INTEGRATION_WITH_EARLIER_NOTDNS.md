Mesh Identity & Reachability Protocol

Design Document — v0.5

Status: Draft
Version: 0.5
Supersedes: v0.4.2
Scope: Identity, relationships, authorization, revocation, reachability, transport integration, deployment model, failure semantics, and reconciliation

---

Change Log from v0.4.2

1. §20 and §45 rewritten. Authorization Keys own exactly one authorization stream. Key revocation is an identity-authority operation signed by the Identity Root.
2. §40 rewritten. Relative validity, absolute validity, monotonic time, and max_offline_tolerance defined separately.
3. §45.2 rewritten. chain_hash defined non-circularly via object_commitment.
4. §47 completed. Verifier local state, processing order, atomicity, fork/gap handling, and identity-fork continuity.
5. §48–§52 added and refined. State machines, authority domains, threat model, compromise model, service identity.
6. §53 added and refined. Failure semantics and recovery.
7. §54 added. Reconciliation and conflict resolution.
8. §55–§62 added. Application integration, V1 scope, deferred features, signing-authority matrix, implementation requirements, test vectors, conformance scenarios, future extensions.
9. Authority Precedence Table normative in §58.5.

---

1. Abstract

The Mesh Identity & Reachability Protocol is an open protocol for establishing persistent, mutually authenticated relationships between machines and services without requiring permanent accounts, centralized identity providers, or fixed network locations.

The protocol provides a control plane above existing networking technologies. It does not replace WireGuard, IPv6, NAT traversal, relays, DNS, or application-level authorization. It establishes:

· who a peer is;
· which devices and services belong to that peer;
· which peers recognize one another;
· what one peer is authorized to do;
· whether that authorization remains valid;
· whether authorization has been revoked;
· how a peer can currently be reached.

Network location is deliberately treated as ephemeral. A machine may change its IP address, move between networks, disappear for months, change NAT mappings, or use a relay without changing its cryptographic identity or relationships.

---

2. Core Security Invariant

Given a set of locally trusted anchors, authenticated protocol objects, known revocations, accepted chain state, and recorded observation history, a verifier must be able to deterministically establish the identity, authorization, validity, and freshness state of a peer as of the verifier's most recent observation of each object's issuer chain, without contacting an authority.

Network access may improve freshness, discover new reachability information, or obtain newer objects. It must not be required to establish authenticity.

This means:

· rendezvous infrastructure cannot define identity;
· relays cannot define authorization;
· DNS cannot define identity;
· IP addresses cannot define identity;
· WireGuard keys cannot by themselves define application authorization;
· temporary pairing codes cannot become permanent credentials.

The phrase as of the verifier's most recent observation is deliberate. A verifier cannot know about revocations it has not received. Its security state is always relative to the last point at which its local object graph was synchronized.

---

3. Design Goals

3.1 Primary goals

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

3.2 Secondary goals

· Multiple devices per principal.
· Multiple services per device.
· Service-specific authorization.
· Temporary guests.
· Delegated administration.
· Groups.
· Multiple rendezvous providers.
· Direct peer-to-peer connections.
· Relay fallback.
· Local-first operation.
· Identity portability.
· Hardware-backed keys.

These features should not complicate the V1 security kernel unless required.

---

4. Non-Goals

· A replacement for WireGuard.
· A general-purpose VPN.
· A global DNS replacement.
· A universal application authorization framework.
· A blockchain.
· A global identity registry.
· A mandatory centralized account system.
· A mandatory DHT.
· A permanent network locator.
· A substitute for application-level authentication.
· An anonymity network.
· A public endpoint directory.
· A global event log.
· A guarantee that direct connectivity always succeeds.

Applications may continue to implement their own authorization.

---

5. Conceptual Architecture

```
┌──────────────────────────────────────────────┐
│                  Application                 │
├──────────────────────────────────────────────┤
│          Mesh Identity & Authorization       │
│ Principal / Device / Service / Grant / Lease │
├──────────────────────────────────────────────┤
│               Reachability                   │
├──────────────────────────────────────────────┤
│                  Transport                   │
└──────────────────────────────────────────────┘
```

Identity and authorization are independent of transport.

---

6. Peer Principal

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

7. Peer Principal ID

```
peer:v1:7f3a9c2e5d91b0a4c7e8126fa31d449b
```

Opaque, randomly generated, not self-certifying. The identity document binds the ID to the principal's identity root.

```
Identity = Peer ID + signed identity document + trusted root
Identifier = opaque reference
```

Advantages:

· Identity-root rotation does not change the Peer ID.
· Provisioning can occur before key generation.
· Cryptographic constructions can change in future versions.
· Identifiers do not expose the construction.
· Relationships remain stable through root-key replacement.

---

8. Identity Root

The Identity Root is the highest cryptographic authority for a principal. It is used to:

· Establish the identity document.
· Authorize device keys.
· Authorize service keys.
· Delegate authorization authority.
· Rotate subordinate keys.
· Revoke subordinate keys (including Authorization Keys).
· Recover from subordinate-key compromise.

The root should not normally participate in routine network sessions. Ideally it remains offline or hardware-protected.

---

9. Key Roles and Separation

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

9.1 Role definitions

Role Owner Purpose
Identity Root Principal Defines the principal; signs identity documents and key delegations; revokes subordinate keys
Device Key One device Authenticates a device; signs reachability records
Service Key One service Authenticates a service; signs service records
Authorization Key Principal or delegated authority Signs grants, leases, and revocations in its stream
Recovery Key Principal Future: threshold or offline recovery
Rendezvous Identity Key Rendezvous operator Signs rendezvous manifests and federation messages
Relay Authority Key Relay coordinator Signs relay tickets (if centralized)
Relay Node Key Relay operator Authenticates a relay endpoint

9.2 Non-reuse rule

A single private key MUST NOT be used for more than one role.

Implementations that cannot enforce separate keys MUST at minimum enforce:

· Identity Root separate from Device Key.
· Identity Root separate from Authorization Key.
· Device Key separate from Service Key.
· Any role separate from Recovery Key.

9.3 Delegation

Delegation of authority from the Identity Root to a subordinate key is expressed inside the identity document. A verifier MUST NOT infer authority from key possession alone.

---

10. Identity Documents

```
IdentityDocument {
    version
    peer_id
    sequence
    chain_hash
    previous_hash
    identity_root
    authorized_keys : set<KeyBinding>
    device_bindings : set<DeviceBinding>
    service_bindings : set<ServiceBinding>
    issued_at
    not_before
    expires_at
    signature
}
```

The exact encoding is defined by OBJECTS.md.

10.1 Ordering semantics

All key collections are canonical sets:

· Ordered by key identifier (lexicographic byte comparison).
· Duplicates forbidden.
· Reordering does not change the set.

10.2 Linear signed history

```
Document 0 → Document 1 → Document 2 → ...
```

10.3 Fork detection

Two documents with the same peer_id and sequence but different chain_hash values constitute a fork. A verifier MUST treat this as a security event. Resolution follows §54.

---

11. Identity Document History

Identity state is append-only. A verifier MUST advance only by walking forward from its accepted state (§45). Intermediate documents remain useful for audit and diagnosis.

---

12. Relationship

A Relationship expresses mutual recognition between two principals.

```
Ryan ↔ Dad
```

A relationship does not automatically grant access. Recognition and authorization are separate.

---

13. Grant

A Grant is directional.

```
Dad → Ryan: jellyfin.stream
```

A grant contains: relationship ID, issuer, subject, device scope (optional), capabilities, resources, constraints, lease policy, issuance info, and signature.

Grants are immutable single-object streams. Any change produces a new grant with a new grant_id.

---

14. Lease

A Lease proves that a grant is currently valid.

```
Relationship  "We recognize each other."
Grant         "You are authorized for X."
Lease         "That authorization is currently valid."
```

Capability Typical lease
Jellyfin streaming 30 days
File access 7 days
SSH 1 hour
Admin SSH 15 minutes

14.1 Lease expiration is a state transition

When a lease expires, the peer is unauthorized until a new lease is issued. A peer returning from a long offline period does NOT inherit the expired lease.

---

15. Capabilities

```
Capability {
    namespace : string    // org.jellyfin
    action    : string    // stream, admin, read
    resource  : string    // library:movies
}
```

The protocol validates well-formedness but does not interpret capability semantics.

15.1 Namespace rules

Lowercase ASCII, dot-separated, at least one dot, first component reverse-DNS.

15.2 Unknown namespaces

A verifier that encounters an unknown namespace:

· MUST validate well-formedness.
· MUST NOT grant network-level authorization based on the unknown namespace alone.
· MAY pass through to an application that understands it.
· MUST NOT reject a grant solely for containing unknown namespaces.

15.3 Empty resource

Empty resource means "all resources in this namespace for this action" only when the grant sets a wildcard flag. Otherwise invalid.

15.4 Constraints

Canonical map string → string. Max 32 entries. Values max 1024 bytes. Well-formedness validated but not interpreted.

---

16. Authorization Policy

Policy belongs to grants.

```
Grant:
    capability = org.jellyfin.stream
    lease_duration = 30 days
    max_offline_tolerance = 30 days
```

Offline tolerance is defined per-grant and evaluated separately from lease validity (§40.6).

---

17. Network Authorization vs Application Authorization

Network authorization: May this peer connect?

Application authorization: Once connected, what may the application do?

The mesh layer does not replace application access control.

```
Mesh:     Ryan may connect to Jellyfin.
Jellyfin: Ryan may access Movies but not Admin.
```

---

18. Revocation

Revocation is terminal.

```
Grant A → revoked → Grant B (new authorization)
```

Never:

```
Grant A → revoked → unrevoked
```

---

19. Revocation Hierarchy

```
Lease → Grant → Device → Authorization Key → Principal
```

Revocation Invalidates
Revoke lease One authorization period
Revoke grant The grant and future leases derived from it
Revoke device Device-specific authorization and services
Revoke authorization key Objects signed at or after effective_sequence
Revoke principal The principal's entire identity

---

20. Key Revocation and Effective Sequence

Key IDs are immutable. Once revoked, a key ID can never be reused.

20.1 Revocation authorities

Two revocation authorities exist:

Authorization-state revocation is signed by an Authorization Key. It revokes grants, leases, or other authorization objects that the key itself issued. It occupies the Authorization Key's authorization stream.

Authorization-Key revocation is signed by the Identity Root. It revokes the Authorization Key itself. It occupies the Identity Root's identity stream.

20.2 KeyRevocation object

```
KeyRevocation {
    key_id
    effective_sequence
    revoked_at
    reason
    replacement_key_id?   // optional
    signature             // Identity Root signature
}
```

Semantics:

· Signed by the Identity Root, not by the key being revoked.
· Occupies the Identity Root's identity stream.
· effective_sequence refers to a position in the revoked Authorization Key's authorization stream.
· Objects signed by key_id at or after effective_sequence are invalid.
· Objects signed by key_id before effective_sequence remain subject to ordinary rules.

Example:

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

The root's seq 202 has no relationship to effective_sequence = 103. They refer to different streams. A verifier MUST NOT compare sequence numbers from different streams.

Consequence: G, L1, L2 remain valid. G2, L3 are invalid.

effective_sequence = 0 invalidates the entire authorization history signed by K, including G.

20.3 No key reuse

A revoked key ID can never be reauthorized. Replacement always creates a new key ID.

---

21. Authorization-Key Compromise

Recovery is an identity-authority operation.

```
Authorization Key compromised
          ↓
Identity Root signs KeyRevocation (effective_sequence = N)
          ↓
All objects signed by K at or after N become invalid
          ↓
Identity Root issues new Authorization Key
          ↓
Legitimate grants re-issued under new key
```

A compromised Authorization Key does not imply compromise of the principal identity, other devices, unrelated service keys, or the identity root.

---

22. Identity Root Compromise

V1 treats the root as the highest trust anchor.

Advanced recovery mechanisms are deferred to V2:

· offline recovery keys;
· hardware-backed roots;
· threshold recovery;
· multi-party approval;
· social recovery.

---

23. Key Rotation

Key rotation is a V1 requirement. Rotation preserves the Peer Principal ID. The identity history establishes the transition.

---

24. Pairing

```
Device A displays:  481729
Device B enters:    481729
```

The six-digit value is a temporary human coordination mechanism, not a credential. The cryptographic exchange provides the actual security.

---

25. Pairing Protocol

V1 pairing MUST use an established PAKE (SPAKE2 or CPace are candidates).

The final protocol must specify:

· Exact PAKE.
· Transcript construction.
· Identity binding.
· Protocol version and context binding.
· Replay protection.
· Code lifetime, retry limits, enumeration resistance.

25.1 Transcript binding

The pairing transcript MUST bind:

· Protocol version.
· Peer identities being introduced.
· PAKE identities.
· Capabilities being requested.
· Pairing context.
· Rendezvous session identifier (if any).

---

26. Pairing Code

~20 bits of entropy. MUST NOT be treated as sufficient cryptographic authentication.

Code should be: short-lived, single-use, rate-limited, invalidated after success, timeout, or excessive failures.

---

27. Human Verification

Devices may display a verification value derived from the pairing transcript:

```
8341 2910
```

---

28. Permanent Identity References

```
Identity Reference ≠ Pairing Invitation ≠ Authorization Grant ≠ Recovery Credential
```

· Identity reference: safely stored for years.
· Pairing invitation: temporary.
· Authorization lease: expires.

---

29. Mesh URI

```
mesh://v1/...
```

Grammar MUST be formally specified in ABNF. Parsing MUST be strict. Malformed forms rejected. Must distinguish identity references, temporary invitations, capability requests, and rendezvous hints. A permanent URI MUST NOT contain a mandatory fixed rendezvous dependency.

---

30. Rendezvous

Rendezvous provides discovery. It has no identity authority.

30.1 Rendezvous roles

Role Purpose
Publication Accepts authorized reachability publications
Replica Stores signed copies
Cache Fetches and caches on demand
Bootstrap Helps peers find manifests
Relay coordinator Issues relay tickets
Freshness source Attests to authorization state, only when explicitly authorized

A rendezvous server is not a freshness source merely because it stores objects.

30.2 Rendezvous manifest

```
RendezvousManifest {
    version
    peer_id
    sequence
    chain_hash
    previous_hash
    generation
    active_until
    recovery_until
    rendezvous_set : set<RendezvousEntry>
    issued_at
    signature
}

RendezvousEntry {
    id
    url
    public_key
    roles
    priority
    region_hint?
}
```

States:

· Active: normal operation.
· Recovery: constrained operation (obtain newer manifest only).
· Expired: not authoritative; requires offline recovery bundle.

30.3 Rendezvous trust model

A malicious rendezvous server may provide stale or false endpoints, suppress endpoint information, observe metadata, or attempt DoS. It MUST NOT be able to forge identity, authorization, or revocation; create a valid lease; or decrypt transport traffic.

---

31. Rendezvous Evolution

Version Capability
V1 HTTPS rendezvous
V2 Multiple interchangeable rendezvous servers
V3 Federation
V4 Peer-assisted gossip
V5 DHT, if required

---

32. Reachability

```
ReachabilityRecord {
    version
    peer_id
    device_id
    service_id?
    endpoint
    transport
    observed_at
    expires_at
    sequence
    chain_hash
    previous_hash
    signature
}
```

Reachability records do not establish identity.

32.1 Reachability record chain

Each device maintains a linear chain. Higher sequence supersedes lower.

32.2 Endpoint hints are not authoritative

A cached endpoint is a hint, not a destination. Cache hits reduce latency but do not substitute for NAT traversal.

---

33. Relays

Relays are transport infrastructure. Both direct and relayed paths represent the same identity relationship.

33.1 Relay tickets (optional)

```
RelayTicket {
    ticket_id
    source_device
    destination_device
    service_link_id
    requested_capability
    issued_at
    expires_at
    max_bytes
    max_rate_bps
    signature
}
```

---

34. Transport

WireGuard is the preferred initial transport. It establishes encrypted communication between cryptographic endpoints. The mesh control plane determines identity, recognition, authorization, lease validity, and permitted services.

---

35. Enforcement

```
Mesh daemon → WireGuard configuration → Firewall → Reverse proxy → Application
```

The protocol does not require WireGuard to understand mesh leases.

---

36. Service Discovery

```
ServiceRecord {
    version
    service_id
    peer_id
    device_id
    service_type
    endpoint
    supported_capabilities : set<CapabilityNamespace>
    metadata
    issued_at
    expires_at
    sequence
    chain_hash
    previous_hash
    signature
}
```

Service records do not grant access. Authorization is separate.

---

37. Offline Operation

A peer may remain offline for months. Others retain principal identity, relationship state, last known authorization, reachability, lease state, and revocation state. An offline peer is represented as:

```
KNOWN / TRUSTED / OFFLINE / LAST SEEN: ...
```

---

38. Lease Expiration

```
Lease expires → No new lease → Access denied
```

Relationship may remain intact.

---

39. Revocation Propagation

V1 supports:

· Pull on reconnect: peers ask issuers for newer authorization state.
· Opportunistic synchronization: peers exchange newer signed objects when they communicate.

A verifier that has not yet received a revocation may temporarily continue honoring a valid lease, subject to max_offline_tolerance.

---

40. Time Semantics

40.1 Relative validity

```
valid_from  = verifier first-acceptance time
valid_until = valid_from + duration
```

Deterministic per verifier. Does not require synchronized wall clocks.

Relative validity MUST NOT be interpreted as extending authority beyond any independently applicable revocation, grant, or policy constraint.

40.2 Absolute validity

```
not_before = issuer-asserted wall-clock
expires_at = issuer-asserted wall-clock
```

Verifiers apply the protocol-defined clock-skew tolerance.

40.3 Validity by object class

Object Validity
Identity Document Absolute
Rendezvous Manifest Absolute
Grant Absolute for issuance; policy controls freshness
Lease Relative by default; absolute MAY be supported
Reachability Record Relative
Revocation Terminal; not expiry-based

40.4 Clock skew

```
MAX_CLOCK_SKEW = 5 minutes
```

40.5 Issued-at ordering

Within an issuer's stream:

```
issued_at(N+1) >= issued_at(N)
```

Sequence numbers establish ordering.

40.6 Authorization freshness and offline tolerance

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

If exceeded, the verifier MUST stop honoring authorization until refresh succeeds.

40.6.1 Definition of authorization refresh

A successful refresh requires an authenticated exchange with the grant issuer or an explicitly designated freshness source. Local re-evaluation does not count. A rendezvous server or relay MUST NOT constitute a freshness source merely because it stores or forwards signed objects.

40.7 Revocation interaction

When a verifier receives a valid revocation:

1. It is added to local state.
2. Affected grants, leases, keys, devices, principals are re-evaluated.
3. Invalidated authorization ceases to be honored.
4. A previously valid lease MUST NOT regain validity merely because its relative validity has not expired.

Revocation takes precedence over remaining lease lifetime.

40.8 Revocation as state, not event

A revocation is a state assertion. If received before its target, it MUST remain effective when the target is subsequently received.

---

41. Cryptographic Object Encoding

All signed objects use one canonical encoding (OBJECTS.md).

V1 uses deterministic CBOR. Rules MUST explicitly define:

· Integer encoding (shortest form).
· Map ordering (canonical CBOR map ordering).
· Byte string, text string, array rules.
· Prohibited values.
· Prohibited floating-point values.
· Null/default handling.
· Integer ranges.

Floating-point values are prohibited from signed V1 objects.

---

42. Domain Separation

Every object type has a unique domain separator:

```
mesh/identity-document/v1
mesh/device-binding/v1
mesh/service-record/v1
mesh/relationship-grant/v1
mesh/authorization-lease/v1
mesh/revocation/v1
mesh/reachability-record/v1
mesh/rendezvous-manifest/v1
mesh/relay-ticket/v1
mesh/stream-resolution/v1
mesh/identity-continuity/v1
mesh/rendezvous-update/v1
```

The domain separator is included in the signature input.

---

43. Cryptographic Baseline

· Ed25519 signatures.
· SHA-256 hashes.
· Deterministic CBOR.
· Cryptographically random identifiers.

43.1 Algorithm identifiers inside signed payloads

Every signed object includes a version field determining algorithm. The version field is part of the signed payload. Objects with unknown versions are rejected.

43.2 Agility

Cryptographic agility is possible at protocol-version boundaries. A version bump is required.

---

44. Object Identity

44.1 object_id

```
object_id = SHA-256(canonical_signed_object)
```

Identifies one signed artifact.

44.2 payload_id

```
payload_id = SHA-256(canonical_unsigned_payload)
```

Identifies semantic payload.

Revocations reference object_id. Semantic comparisons MAY use payload_id.

---

45. Sequence and History

45.1 Sequence spaces

```
sequence_space = (issuer, stream_id)
```

Stream identifiers:

```
stream:identity
stream:reachability:<device_id>
stream:service:<service_id>
stream:rendezvous
stream:authorization:<authorization_key_id>
```

An Authorization Key owns exactly one authorization stream:

```
(K, stream:authorization:<K>)
```

Grants, leases, and revocations issued by K occupy that stream and consume sequence numbers regardless of object type.

A KeyRevocation is different. It is an identity-authority object signed by the Identity Root and occupies the Identity Root's identity stream.

The effective_sequence field of a KeyRevocation refers to the sequence space of the revoked Authorization Key's stream, not to the Identity Root's stream.

A verifier MUST NOT compare sequence numbers from different streams.

45.2 Chain structure

```
unsigned_payload(N)      = object fields excluding chain_hash and signature
commitment_preimage(N)   = canonical_cbor([
                              "mesh/commitment/v1",
                              domain_separator,
                              unsigned_payload(N)
                           ])
object_commitment(N)     = SHA-256(commitment_preimage(N))
previous_hash(N)         = object_commitment(N-1)
chain_hash(N)            = SHA-256(chain_hash(N-1) || object_commitment(N))
signed_object(N)         = unsigned_payload(N) || chain_hash(N) || signature(N)
```

chain_hash(0) = SHA-256(domain_separator).

45.3 Single-object streams

Grants are immutable single-object streams within the authorization stream. Their sequence position is the position at which they were issued.

45.4 Fork detection

Two objects in the same sequence space with the same sequence but different chain_hash values constitute a fork. Resolution (§54) requires an explicit signed resolution object.

45.5 V1 does not support skip-ahead

When advancing a mutable object stream, a verifier MUST validate sequentially from its last accepted state. A verifier MUST NOT accept a current chain head merely because its signature is valid, its sequence is higher, its chain_hash appears plausible, or a rendezvous server supplied it.

45.6 Future chain-extension proofs

Future versions MAY introduce authenticated chain-extension proofs. A compact chain hash alone is not sufficient evidence for skip-ahead.

---

46. Trust Anchors

```
peer_id
trusted_identity_root
accepted_identity_state  (sequence + chain_hash)
acceptance_time
```

Trust anchors are established through explicit pairing, local administrative configuration, trusted provisioning, or future recovery mechanisms. A rendezvous server is never itself a trust anchor.

---

47. Verifier Local State

47.1 Principal state

```
PrincipalState {
    peer_id
    trusted_identity_root
    accepted_identity_sequence
    accepted_identity_chain_hash
    identity_acceptance_time
}
```

47.2 Key state

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

Status: ACTIVE, REVOKED, SUPERSEDED, UNKNOWN.

47.3 Relationship state

```
RelationshipState {
    relationship_id
    local_principal
    remote_principal
    state
    accepted_sequence
}
```

47.4 Grant state

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

47.5 Lease state

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

47.6 Chain state

```
ChainState {
    issuer
    stream_id
    accepted_sequence
    accepted_chain_hash
    sync_state
}
```

sync_state ∈ { IDLE, SYNCING, FORKED }.

47.7 Reachability state

Soft state. Loss MUST NOT invalidate identity, relationship, grant, or revocation state.

47.8 Rendezvous state

Infrastructure state. Loss MUST NOT invalidate identity or authorization state.

47.9 Observation history and monotonic time

For relative validity, the verifier MUST retain first_observed_at (monotonic).

Implementations MUST use a monotonic local clock for elapsed-duration calculations. Wall-clock changes MUST NOT extend or shorten a relative validity interval.

47.10 Processing order

1. Decode canonical object.
2. Validate version.
3. Validate domain separator.
4. Validate signature.
5. Validate issuer authority.
6. Validate object sequence.
7. Validate chain continuity.
8. Detect rollback, fork, extension, or gap.
9. Apply key transitions.
10. Apply revocations.
11. Apply relationship transitions.
12. Apply grants.
13. Apply leases.
14. Update authorization freshness.
15. Update reachability state if applicable.
16. Commit resulting local state.

An implementation MAY optimize internally, but its resulting security state MUST be equivalent to this ordering.

47.11 Atomic state updates

Security-significant object processing MUST be atomic. An implementation MUST NOT expose an intermediate state in which:

· a new grant is visible but its revocation is not;
· a replacement key is visible but its predecessor revocation is not;
· a new identity state is visible but its chain transition is not;
· a lease is visible without its corresponding grant state.

If processing fails, the verifier MUST retain the previous accepted state.

47.12 Fork handling

Upon detecting a fork, the stream enters FORKED state. Behavior is governed by §53.7. Recovery is governed by §54.

47.13 Gap handling

A gap occurs when an incoming object has sequence greater than accepted_sequence + 1. A gap is not a fork.

Behavior:

· Stream enters SYNCING.
· Verifier MUST obtain missing intermediates or decline to advance.
· Authorization decisions dependent on the stream use the last accepted state.
· If SYNCING persists beyond a policy timeout, authorization MAY be treated as non-fresh.
· Stream MUST NOT become FORKED absent an actual conflicting object.

47.14 Case summary

Incoming object Condition Result
Rollback sequence < accepted Reject
Fork sequence == accepted, chain differs Enter FORKED
Extension sequence == accepted + 1, predecessor matches Accept
Gap sequence > accepted + 1 Enter SYNCING

47.15 Local verification invariant

Given locally trusted anchors, authenticated objects, known revocations, accepted chain state, and recorded observation history, the verifier can deterministically establish principal, authorization, revocation, and freshness state without contacting an authority.

Network communication may improve state; it MUST NOT be required to establish whether the state already known is authentic.

---

48. Security State Machines

48.1 Relationship

```
UNKNOWN → INTRODUCED → RECOGNIZED → TERMINATED (terminal)
```

New relationship requires new relationship ID.

48.2 Grant

```
UNKNOWN → GRANTED → { EXPIRED (terminal), REVOKED (terminal) }
```

V1 grant validity is absolute.

48.3 Lease

Two independent predicates: lease validity and authorization freshness.

```
UNKNOWN → VALID
VALID → { EXPIRED (terminal), REVOKED (terminal), STALE }
STALE → VALID (on successful refresh)
```

STALE is not terminal. Authorization requires: lease VALID, grant GRANTED, relationship RECOGNIZED, key ACTIVE or SUPERSEDED, no applicable revocation.

48.4 Authorization Key

```
UNKNOWN → ACTIVE → { SUPERSEDED → REVOKED (terminal), REVOKED (terminal) }
```

· ACTIVE → SUPERSEDED is established only by an accepted identity document.
· ACTIVE → REVOKED and SUPERSEDED → REVOKED are established by accepted KeyRevocation signed by Identity Root.
· REVOKED: no longer trusted for objects at or after effective_sequence. Objects before it remain subject to ordinary rules.

48.5 Device Key

```
UNKNOWN → ACTIVE → { REVOKED (terminal), RETIRED (terminal) }
```

48.6 Service Record

```
UNKNOWN → CURRENT → { SUPERSEDED (terminal), EXPIRED (terminal) }
```

48.7 Reachability Record

```
UNKNOWN → CURRENT → { SUPERSEDED (terminal), EXPIRED (terminal) }
```

48.8 Cross-object constraints

· A grant whose relationship is TERMINATED MUST NOT contribute to effective authorization.
· A lease whose grant is not GRANTED MUST NOT contribute.
· A lease whose Authorization Key is REVOKED with effective_sequence ≤ lease sequence MUST NOT contribute.
· A reachability record signed by a REVOKED Device Key MUST NOT be accepted as current.
· A service record signed by a REVOKED Service Key MUST NOT be accepted as current.

These constraints derive from §58.5.

---

49. Authority Domains

The protocol partitions authority into five domains. Authority ≠ trust. Rendezvous is explicitly untrusted.

49.1 Identity authority

Source: Identity Root.

Scope: identity document, subordinate keys, device bindings, service bindings.

Boundary: does not extend to authorization. The root establishes who the principal is and which keys speak for it.

The root retains authority to revoke subordinate keys, including Authorization Keys.

49.2 Authorization authority

Source: Authorization Key delegated by Identity Root.

Scope: grants, leases, and revocations in its stream.

Boundary: does not extend to identity. An Authorization Key cannot revoke itself.

49.3 Service authority

Source: Service Key bound by Identity Root (or by a device key if the identity document permits).

Scope: service records describing endpoints and metadata.

Boundary: does not extend to authorization.

49.4 Reachability authority

Source: Device Key.

Scope: reachability records.

Boundary: does not extend to identity, authorization, or service description.

49.5 Rendezvous authority

Source: none. Rendezvous has no signing authority.

Scope: discovery and storage.

Boundary: cannot create, modify, or invalidate signed objects.

49.6 Cross-domain rules

1. No domain may exercise authority belonging to another.
2. Delegation is explicit.
3. Possession is not authority.
4. Boundaries are enforced at verification time.
5. Revocation authority does not depend on the revoked key.

---

50. Threat Model

50.1 Threat taxonomy

T1 Identity forgery. T2 Authorization forgery. T3 Revocation exposure. T4 Rollback. T5 Fork. T6 Replay. T7 MITM during pairing. T8 Endpoint poisoning. T9 Rendezvous observation. T10 Relay observation. T11 Subordinate key compromise. T12 Identity Root compromise. T13 DoS. T14 Abuse of shared infrastructure.

50.2 Threat-to-property mapping

Threat Property Mechanism
T1 Identity authenticity Signed identity documents
T2 Authorization authenticity Signed grants and leases
T3 Bounded revocation exposure max_offline_tolerance limits exposure; cannot eliminate it
T4 Monotonic state Sequence numbers; rollback rejection
T5 Chain uniqueness chain_hash cumulative commitment
T6 Object application control Stream sequence state; object identity; context binding; validity intervals; state-machine rules
T7 Pairing integrity PAKE with transcript binding; human verification
T8 Endpoint authenticity Reachability records signed by Device Key; service records signed by Service Key
T9 Metadata minimization Opaque peer IDs; limited rendezvous state
T10 Traffic confidentiality End-to-end encryption
T11 Blast radius containment Key role separation
T12 (partial) Recovery V1 treats root as anchor; V2 adds recovery
T13 (not addressed) Deployment property
T14 (not addressed) Deployment policy

50.3 Explicit non-properties

· Anonymity.
· Availability.
· Metadata confidentiality against global observer.
· Protection against compromised endpoints.
· Protection against authorized-but-malicious peers.
· Protection against compromised Identity Root beyond V1 trust-anchor model.

---

51. Compromise Model and Blast Radius

51.1 Service Key compromise

Attacker can: point discovery metadata toward attacker-controlled endpoints for one service.

Attacker cannot: authorize any endpoint; grant access; modify identity document; affect other services or devices; forge authorization.

Blast radius: one service's discovery metadata.

Recovery: revoke Service Key via identity document; issue new key; re-sign record.

51.2 Device Key compromise

Attacker can: point discovery metadata toward attacker-controlled endpoints for one device.

Attacker cannot: authorize endpoints; grant access; sign identity documents; affect other devices.

Recovery: revoke Device Key; issue new key; re-publish records.

51.3 Authorization Key compromise

Attacker can: issue grants, leases, revocations in the key's stream.

Attacker cannot: modify identity document; revoke the compromised key itself.

Blast radius: all authorization state under the key, from compromise forward.

Recovery is an identity-authority operation:

1. Identity Root signs KeyRevocation with effective_sequence.
2. Objects signed by the compromised key at or after effective_sequence are invalid.
3. Principal issues new Authorization Key.
4. Legitimate grants re-issued.

Normative:

A revocation of an Authorization Key is an identity-authority operation and MUST NOT require the compromised key to sign its own revocation. The effective_sequence field identifies the first sequence position in the revoked key's authorization stream that is no longer trusted.

effective_sequence = 0 invalidates the entire key history, including grants.

51.4 Identity Root compromise

Attacker gains: all authority over the principal.

Recovery: V1 has no in-band recovery. Principal must be re-established with a new Peer ID. Peers informed out-of-band.

Detectability: none from within the protocol.

51.5 Device compromise

Blast radius: union of compromised keys' blast radii.

Design implication: devices hold only the keys they need.

51.6 Rendezvous compromise

Blast radius: discovery only. Cannot forge identity, authorization, revocation; cannot decrypt.

51.7 Relay compromise

Blast radius: transport for peers using the relay. Cannot decrypt or forge.

51.8 Compromise summary

Asset Blast radius Detectable Recovery
Service Key One service's discovery No Rotate via identity document
Device Key One device's discovery No Rotate via identity document
Authorization Key All authorization under it No Root revokes with effective_sequence; new key
Identity Root Entire principal No None in V1; new Peer ID
Device (hardware) Union of held keys No Depends on keys held
Rendezvous Discovery only Yes (via redundancy) Rotate rendezvous
Relay Transport only No Use another relay or direct

51.9 Invariants

1. Subordinate key compromise MUST NOT require replacing the Identity Root.
2. Subordinate key compromise MUST NOT affect unrelated keys.
3. Signing key compromise MUST NOT extend blast radius.
4. Infrastructure compromise MUST NOT affect identity or authorization state.
5. Revocation of a compromised key is authorized by a higher-authority key.

---

52. Service Identity, Service Binding, and Service Link

52.1 Service Identity

```
service_id  = opaque identifier
service_key = Ed25519 key pair
```

Stable across device replacement and network changes. Independent of any specific grant.

52.2 Service Binding

```
ServiceBinding {
    service_id
    service_public_key
    bound_to     : principal_id | device_id
    issued_at
    expires_at?
}
```

Signed as part of the identity document. Establishes which principal or device speaks for the service, not who may access it.

52.3 Service Link

```
service_link_id = opaque identifier
```

Referential only. Not an independently signed object. Carries no semantics beyond "this identifier names the relationship between a specific subject and a specific service." Semantics are established by the objects that reference it.

Normative:

N1. A Service Link is not an authorization object.

N2. A Service Link MUST NOT contain capabilities, authorization constraints, lease validity, or equivalent.

N3. Presence, validity, or recognition of a Service Link MUST NOT authorize access.

N4. Authorization to a service is established exclusively through Grant and Lease state.

N5. A Service Link is a referential identifier. It is not signed, mutable, or independently authoritative.

N6. If two objects reference the same service_link_id but disagree, the objects are the source of truth.

N7. An attacker who invents a service_link_id gains nothing.

52.4 Cross-object behavior

A service_link_id is meaningful only in the context of the objects referencing it. Created by the first object that references it; semantics defined by that object.

No Service Link object to compromise, revoke, or mis-sign. No possibility of conflicting Service Links. Cannot be un-authorized because it was never authorized.

52.5 Service host migration

Service moves from one device to another within the same principal.

```
Principal P
   └── Service S
          ├── old Device D1
          └── new Device D2
```

Mechanism: principal issues new identity document binding same Service Identity to new device.

After migration: Service Identity unchanged; Service Binding reflects new device; grants and leases remain valid because authorization is to the Service Identity.

52.6 Service ownership transfer

Service moves from one principal to another.

V1 does not support service ownership transfer.

Recovery is treated as: old principal retires the service binding; new principal establishes a new service with a new Service Identity; grants and leases re-issued; peers informed out-of-band.

Rationale: ownership transfer changes authority. Without an explicit authenticated transfer, allowing one principal to declare ownership of another's service would let it take over by issuing a competing identity document. V1 has no mechanism to arbitrate. V1 does not invent one.

52.7 Service lifecycle summary

Object Signed by Purpose Lifecycle
Service Identity (n/a) Service identity Long-lived
Service Binding Identity Root (or delegated) Binds identity to principal/device Identity document lifetime
Service Link (n/a) Referential identifier Referential
Grant Authorization Key Authorizes subject Until revocation or expiry
Lease Authorization Key Proves current validity Relative validity + freshness
Service Record Service Key Current endpoint and metadata Short-lived
Reachability Record Device Key Current device endpoints Short-lived

52.8 Service Record and Reachability Record

· Service Record describes how the service can be reached. Signed by Service Key.
· Reachability Record describes where the hosting device can be reached. Signed by Device Key.
· A Service Record MAY reference a Reachability Record for the hosting device.
· Neither overrides the other. Both are used. Neither grants authorization.

---

53. Failure Semantics and Recovery

53.1 General invariants

F1 No failure silently grants authorization.

F2 No failure silently extends authorization.

F3 No failure silently changes identity state.

F4 Availability is preserved where possible.

F5 Security-relevant failure conditions are represented in local state sufficiently to enforce failure semantics. Diagnostic logging is optional.

F6 Failures are recoverable where specified; terminal where specified.

53.2 Taxonomy

Discovery (§53.3), synchronization (§53.4), integrity (§53.5), validity (§53.6), fork (§53.7), freshness (§53.8), local (§53.9), pairing (§53.14).

53.3 Discovery failures

53.3.1 Rendezvous unreachable. Retry; rotate to next in manifest. Failure is not evidence of peer state. State unchanged.

53.3.2 Endpoint unreachable. Failed connection is not evidence the peer is offline, compromised, or unauthorized. Record's protocol state unchanged. Local "attempted and failed" annotation is soft, non-normative. Try alternate candidates; refresh reachability.

53.3.3 Conflicting reachability records. Fork in reachability stream. Stream enters FORKED. Neither branch used. Resolution per §54.

53.3.4 Malicious rendezvous. Reject object; do not alter state. Deprioritize server; log optionally.

53.4 Synchronization failures

53.4.1 Stream gap. SYNCING state. Use last accepted state for authorization. Persistent gap MAY be treated as non-fresh. Gap MUST NOT become FORKED.

53.4.2 Partial synchronization. Use locally known objects for decisions determinable from them, subject to all applicable rules. Absent objects not assumed revoked, expired, superseded, or existent. Partial sync does not authorize objects whose validity depends on missing state.

53.4.3 Network partition. Cached objects evaluated against normal rules. max_offline_tolerance evaluated on monotonic time. Leases may become STALE. Refresh on reconnect.

53.5 Integrity failures

53.5.1 Malformed object. Structurally invalid. Reject. State unchanged.

53.5.2 Invalid signature. Reject. MAY record diagnostically.

53.5.3 Unknown object type. Reject. Do not interpret.

53.5.4 Unknown issuer. Reject as untrusted.

53.6 Validity failures

53.6.1 Expired. Excluded. State EXPIRED.

53.6.2 Revoked. Excluded. State REVOKED.

53.6.3 Superseded. Excluded. State SUPERSEDED.

53.6.4 Unknown revocation. Cache as state assertion. MUST remain effective when target is subsequently received.

53.7 Fork failures

53.7.1 Conflicting stream states. Stream FORKED. Use last accepted state. No new information from stream. External resolution required.

53.7.2 Conflicting identity documents. Identity stream FORKED. Use last accepted identity state.

53.7.3 Authorization continuity during identity fork.

· Authorization state derived from last accepted identity state remains locally recognized.
· MUST NOT incorporate assertions from either disputed branch.
· Existing grants and leases continue to be evaluated against last accepted identity state.
· No new authorization state dependent on disputed branch may be accepted until fork is resolved.

Invariant: accepted state remains accepted; disputed state contributes nothing.

53.8 Freshness failures

53.8.1 Authorization refresh failure. last_successful_authorization_refresh not updated. Failed attempt is not a refresh. Leases may become STALE. Successful refresh transitions STALE → VALID only if grant remains GRANTED, no revocation applies, lease has not independently expired.

53.8.2 Freshness source unavailable. MUST NOT substitute undesignated sources. MUST NOT treat rendezvous or relay as freshness.

53.9 Local failures

53.9.1 Local storage loss. All state lost; return to UNKNOWN. MUST NOT reconstruct trust from received objects alone. Reachability MAY be reconstructed.

53.9.2 Clock forward jump. Relative validity unaffected. Absolute validity may misclassify. Apply clock-skew tolerance. Re-evaluation recomputes applicability; does NOT rewrite history.

53.9.3 Clock backward jump. As above. issued_at monotonicity violations rejected as temporal-policy violations, NOT malformed.

53.9.4 Monotonic clock unavailable. MUST NOT substitute wall clock. Refuse to evaluate relative validity, or use a source guaranteed not externally adjusted.

53.10 Summary table

Failure Authorization impact State impact Recovery
Rendezvous unreachable None None Retry; rotate
Endpoint unreachable None Local observation only Refresh; alternates
Conflicting reachability None Stream FORKED External resolution
Malicious rendezvous None None Deprioritize
Stream gap Use last accepted state SYNCING (not FORKED) Obtain intermediates
Partial sync Use local state with all rules None Continue sync
Network partition Leases may become STALE None Refresh
Malformed object None None Discard
Invalid signature None None Discard
Unknown object type None None Discard
Unknown issuer None None Discard
Expired object Excluded EXPIRED New object
Revoked object Excluded REVOKED Issue new
Superseded object Excluded SUPERSEDED Use newer
Unknown revocation None Revocation cached Apply on receipt
Fork Use last accepted state FORKED §54
Identity fork Accepted state effective; disputed contributes nothing Identity stream FORKED §54
Refresh failure None until tolerance elapses STALE Successful refresh
Freshness source unavailable As above As above Retry designated source
Local storage loss All authorization lost Return to UNKNOWN Re-pair
Clock forward jump Possible absolute misclassification History unchanged Restore clock
Clock backward jump Possible absolute misclassification; temporal violations rejected History unchanged Restore clock
Monotonic clock unavailable Relative validity cannot be evaluated None Environmental
Pairing failure None None Discard; retry

53.11 Fail-closed vs. availability-preserving

Fail-closed (authorization): missing information MUST NOT grant authorization; failed refresh ≠ refresh; forked streams contribute nothing; expired/revoked/superseded excluded; gaps not filled by inference; local state loss not reconstructed from untrusted sources; persistent gaps not reinterpreted as forks.

Availability-preserving (connectivity and discovery): discovery retries permitted; relay use permitted; reconnections do not require re-validation; cached reachability MAY be used subject to signed validity; alternate rendezvous and endpoints MAY be tried.

53.12 Interaction with §50 and §51

§53 describes behavior under absence of information. §50 describes adversarial conditions. §51 describes compromise.

Where sections appear to overlap, the response is defined once and referenced.

53.13 Conformance

1. MUST preserve local state under all failures unless failure is explicitly local.
2. MUST NOT interpret any failure as authorization.
3. MUST NOT extend validity or freshness based on failed operations.
4. MUST represent security-relevant failure conditions in local state.
5. MUST apply specified recovery paths.
6. MUST NOT invent recovery paths for authorization-relevant decisions.
7. MUST NOT conflate distinct failure conditions.

53.14 Pairing failures

Failed, timed-out, or interrupted pairing:

· Attempt discarded.
· No relationship, grant, lease, delegation, or trust anchor created.
· Ephemeral PAKE state destroyed.
· Existing relationships and authorization unchanged.
· MAY retry with fresh session.
· Pairing code MUST NOT be reused.
· Previously successful pairing remains valid unless independently terminated.
· Failure does not imply remote principal is compromised or malicious.

Invariant: an incomplete pairing has no partially committed security state.

---

54. Reconciliation and Conflict Resolution

54.1 Scope

Defines reconciliation of:

· two conflicting objects in the same stream (FORKED);
· persistent stream gaps for which intermediates cannot be obtained;
· conflicting identity documents;
· conflicting reachability or service records;
· conflicting rendezvous manifests.

Does not define application-layer conflict resolution, policy decisions between equally authoritative peers, or adjudication of competing claims about the same identity or service.

54.2 Principles

R1 No new authority.

R2 Issuer-scoped resolution: resolution MUST be signed by a key whose authority covers the stream.

R3 Explicit resolution: no inference, timeout, or availability-based resolution.

R4 Preservation of accepted state until resolution.

R5 Fail-closed if unresolved: FORKED is a valid terminal condition.

R6 Resolution is a stream transition, not an override.

R7 Resolutions are auditable.

54.3 Object classes

1. StreamResolution — resolves a fork in a single stream.
2. IdentityContinuity — establishes continuity across an orderly transition.
3. RendezvousUpdate — controlled rendezvous manifest supersession.

54.4 StreamResolution

```
StreamResolution {
    version
    domain_separator      = "mesh/stream-resolution/v1"
    issuer
    stream_id
    disputed_sequence
    disputed_hashes
    accepted_hash
    resolution_reason
    issued_at
    not_before
    expires_at
    sequence
    chain_hash
    previous_hash
    signature
}
```

Acceptance rules:

1. Signature validates.
2. Issuer has authority over stream_id (per §49).
3. disputed_sequence matches locally observed fork.
4. accepted_hash ∈ locally observed disputed_hashes.
5. Resolution's sequence > disputed_sequence in resolver's stream.
6. Not expired.

On acceptance: accepted_chain_hash set to accepted_hash; stream transitions to IDLE.

54.5 IdentityContinuity

```
IdentityContinuity {
    version
    domain_separator      = "mesh/identity-continuity/v1"
    peer_id
    previous_root
    previous_chain_hash
    new_root
    new_sequence
    new_chain_hash
    continuity_reason
    signed_by_previous    // signature by previous_root
    signed_by_new         // signature by new_root
    issued_at
    expires_at
}
```

Dual-signature requirement. Signed by both previous and new root. Neither alone is sufficient.

Acceptance rules:

1. Both signatures validate.
2. previous_root matches trusted root OR chains through prior accepted IdentityContinuity objects.
3. previous_chain_hash matches last accepted chain hash.
4. new_sequence > previous sequence.
5. Not expired.
6. New identity document referenced by new_chain_hash validates under new_root.

On acceptance: trusted identity root updated to new_root; chain state updated; stream transitions to IDLE.

Recovery from root compromise is NOT handled by IdentityContinuity. Requires out-of-band notification and re-pairing, or peer administrators accepting a new identity root through external mechanisms.

54.6 RendezvousUpdate

Rendezvous manifests are normal streams. Forks resolved by StreamResolution signed by the principal's Identity Root.

54.7 Persistent gaps

Persistent gaps are not forks. Resolved by obtaining missing objects, not by issuing resolution objects.

54.8 Non-stream conflicts

Case 1: Conflicting signed objects from different authorities. Verifier evaluates both. If they conflict and no rule in §58.5 resolves, verifier MUST NOT authorize.

Ambiguity rule:

If two independently valid signed objects assert incompatible authorization for the same (subject, service, capability) and no rule in the Authority Precedence Table resolves the conflict, the verifier MUST NOT authorize the capability.

Case 2: Conflicting reachability records from different devices. Only the device bound to the service in the identity document is authoritative for that service.

54.9 Explicit non-mechanisms

· Voting.
· Timestamps as resolution.
· Availability as resolution.
· Preference order among sources.
· Peer voting on disputed state.
· Automatic resolution.
· Transfer of authority between principals without dual signature.

54.10 Resolution availability

For orderly transitions: Identity Root available to sign.

For unplanned events (root compromise, loss of root key material): out-of-band recovery, administrative re-acceptance, or terminal abandonment of old Peer ID.

54.11 Reconciliation state

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

FORKED remains until accepted resolution. SYNCING remains until intermediates obtained.

54.12 Interaction

· Fork detection: §45.4.
· Fork handling: §47.12.
· Gap handling: §47.13.
· State machines: §48.
· Authority domains: §49.
· Failure semantics: §53.
· Authority Precedence: §58.5.

54.13 Conformance

1. MUST NOT resolve FORKED by mechanisms other than valid StreamResolution or IdentityContinuity.
2. MUST NOT resolve SYNCING by mechanisms other than obtaining intermediates.
3. MUST preserve last accepted state until resolution.
4. MUST retain disputed artifacts and resolution.
5. MUST NOT authorize ambiguous conflicts.
6. MUST NOT treat time, availability, source preference, or voting as resolution.
7. MUST accept IdentityContinuity only with dual signature.

---

55. Application Integration and API

55.1 Principle

Applications consume authenticated identity and authorized connections. They do not receive raw endpoints, relay credentials, or rendezvous URLs. The mesh daemon is the boundary.

55.2 Local interface

The mesh daemon exposes a local API. Example operations:

```
mesh.discover()                     → list of known peers
mesh.resolve(peer_id)               → peer state
mesh.connect(service_link_id, cap)  → local connection handle
mesh.authorize(peer_id, capability) → authorization decision
mesh.revoke(object_id)              → issue revocation
mesh.status()                       → daemon and peer state
```

55.3 Connection handles

A connection handle is a local endpoint bound to one authorization decision.

```
{
    "connection_id": "random-id",
    "local_url": "http://127.0.0.1:41873",
    "expires_at": "2026-10-04T21:00:00Z"
}
```

The application uses the local URL. It does not receive the underlying endpoint, relay credentials, or peer ID.

path_type MAY be exposed diagnostically (LAN, direct, relay) but MUST NOT be used for authorization.

55.4 Authorization inputs

When an application requests a connection:

· The daemon evaluates authorized (§40.6).
· If authorized, a local connection is established.
· If not, the daemon returns an error without exposing internal state.

55.5 Application identity

Applications MAY receive an authenticated principal identifier for the peer on the other end of a connection, to integrate with their own authorization. The identifier is the Peer Principal ID, not a network address.

55.6 Enforcement boundary

The daemon MAY enforce authorization through:

· transport configuration (WireGuard peer configuration);
· firewall rules;
· proxying through the daemon;
· any combination.

The protocol does not require a specific enforcement mechanism.

55.7 Integration with existing applications

Applications that do not support mesh-aware APIs can be reached through a local proxy:

```
Application → mesh.connect() → daemon → overlay → peer
```

The application sees a normal local service.

---

56. V1 Scope and Kernel

V1 is deliberately narrow. The following MUST be implemented:

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
11. Authorization freshness (max_offline_tolerance).
12. Terminal revocation.
13. Key revocation with effective_sequence.
14. Human-mediated QR/copy-paste pairing.
15. Established PAKE.
16. Relationships.
17. Canonical object encoding.
18. One self-hostable rendezvous service.
19. Reachability records.
20. Direct connectivity.
21. WireGuard integration.
22. Offline verification.
23. Positive and negative test vectors.

The following are deferrable to V1.1 without architectural change:

· Rendezvous manifest multi-server support.
· Relay fallback.
· Multiple rendezvous providers.
· Service host migration tooling.
· Comprehensive failure test coverage.

---

57. Explicitly Deferred Features

Deferred to future versions:

· DHT-based discovery.
· Federation between rendezvous servers.
· Peer-assisted gossip.
· Groups.
· Sophisticated recovery (threshold, social, hardware-backed).
· Multipath routing.
· Automatic service migration.
· Service ownership transfer.
· Reputation and liveness scoring.
· Advanced metadata protection.
· Delegated administration.
· Temporary guests.
· Rendezvous manifests with rotating pseudonyms.

These are deferred because they either introduce authorities the protocol does not define, or they depend on decisions not yet settled.

---

58. Normative Signing-Authority Matrix

58.1 Purpose

This matrix states, for each object type, the key role authorized to sign it. It is normative.

58.2 Matrix

Object Authorized signer
IdentityDocument Identity Root
DeviceBinding Identity Root (or delegated device-authority key)
ServiceBinding Identity Root (or delegated service-authority key)
KeyBinding (delegation) Identity Root
KeyRevocation Identity Root
Relationship Either participating principal's Authorization Key
RelationshipTermination Either participating principal's Authorization Key
Grant Authorization Key
Lease Authorization Key
GrantRevocation Authorization Key
LeaseRevocation Authorization Key
StreamResolution Key with authority over the stream
IdentityContinuity Both previous and new Identity Root
ServiceRecord Service Key
ReachabilityRecord Device Key
RendezvousManifest Identity Root
RendezvousUpdate Identity Root
RelayTicket Relay Authority Key
RelayNodeRecord Relay Node Key

58.3 Delegation rules

· Delegation is expressed inside the identity document.
· A subordinate key's authority is exactly what the delegating key has expressed, no more.
· Revocation of a subordinate key does not affect keys not derived from it.
· A subordinate key MUST NOT delegate authority beyond its own scope.

58.4 Cross-domain prohibition

An object signed by a key whose authority does not cover that object type MUST be rejected. There is no "fallback" authority.

58.5 Authority Precedence Table

The Governing authority column has exactly four values:

· A governs — Object A's authority determines the outcome.
· B governs — Object B's authority determines the outcome.
· No conflict — Objects A and B describe orthogonal properties.
· Composed — Objects A and B contribute different predicates to the same decision.

Where two objects contribute different predicates to a decision, the table MUST NOT be interpreted as establishing precedence between them.

Identity-domain pairs

A B Governing authority Notes
Identity Document Service Binding A governs Contained in identity document
Identity Document Device Binding A governs Contained in identity document
Identity Document Key Revocation Composed Identity establishes trust; revocation removes it at effective_sequence
Identity Document Relationship No conflict Identity is independent of recognition
Identity Document Reachability Record No conflict Identity is independent of location
Identity Document Service Record No conflict Identity is independent of service metadata
Identity Document Rendezvous Manifest No conflict Identity is independent of discovery

Authorization-domain pairs

A B Governing authority Notes
Grant Lease Composed Grant supplies scope; Lease establishes current validity
Grant Grant Revocation B governs Revocation overrides grant
Grant Relationship Composed Relationship establishes existence; Grant establishes scope
Grant Key Revocation A governs for key validity; B retains its own intrinsic semantics Revocation invalidates at or after effective_sequence
Grant Service Link No conflict Service Link referential only
Grant Reachability Record No conflict Authorization and location orthogonal
Grant Service Record No conflict Authorization and service description orthogonal
Grant Rendezvous Manifest No conflict Authorization and discovery orthogonal
Grant Relay Ticket A governs Authorization state governs
Lease Lease Revocation B governs Revocation overrides lease
Lease Relationship Composed Relationship establishes existence; Lease inherits grant scope
Lease Key Revocation A governs for key validity; B retains its own intrinsic semantics Revocation invalidates at or after effective_sequence
Lease Service Link No conflict Service Link referential only
Lease Reachability Record No conflict Authorization and location orthogonal
Lease Relay Ticket A governs Authorization state governs
Relationship Relationship Termination B governs Termination overrides relationship
Authorization Key State Grant A governs for key validity; B retains its own intrinsic semantics Revoked key invalidates covered grants
Authorization Key State Lease A governs for key validity; B retains its own intrinsic semantics Revoked key invalidates covered leases
Key Revocation Grant A governs for key validity; B retains its own intrinsic semantics 
Key Revocation Lease A governs for key validity; B retains its own intrinsic semantics 

Service-domain pairs

A B Governing authority Notes
Service Binding Service Record A governs Binding establishes authority; record describes endpoint
Service Binding Grant No conflict Binding establishes ownership; Grant establishes authorization
Service Binding Lease No conflict Binding establishes ownership
Service Binding Revocation No conflict Binding and authorization are orthogonal
Service Binding Reachability Record No conflict Binding and location orthogonal
Service Record Reachability Record Composed Service Record describes service endpoint; Reachability describes device path
Service Record Grant No conflict Orthogonal
Service Record Lease No conflict Orthogonal
Service Record Revocation No conflict Orthogonal
Service Record Relay Ticket No conflict Orthogonal

Reachability-domain pairs

A B Governing authority Notes
Device Binding Reachability Record A governs Binding establishes which device
Reachability Record Relay Ticket No conflict Path description and permission orthogonal
Reachability Record Rendezvous Manifest No conflict Orthogonal
Reachability Record Grant No conflict Orthogonal
Reachability Record Lease No conflict Orthogonal

Infrastructure-domain pairs

A B Governing authority Notes
Rendezvous Manifest Any signed object B governs Rendezvous has no signing authority
Relay Ticket Grant A governs Authorization state governs
Relay Ticket Lease A governs Authorization state governs
Relay Ticket Reachability Record No conflict Orthogonal

Chain and stream-state pairs

A B Governing authority Notes
New Identity Branch Accepted Branch B governs Fork requires external resolution
Gap in Stream Accepted Stream B governs Gap requires intermediate objects
New Valid Lease Expired Lease A governs Provided grant remains valid
Identity Root State Subordinate-Key Assertion A governs Root-authoritative

Cross-cutting

A B Governing authority Notes
Service Link Any signed object referencing it Referencing object governs Service Link carries no semantics beyond use as shared identifier

58.6 Vocabulary consistency

Where the governing authority is "A governs for key validity; B retains its own intrinsic semantics," this indicates the object's intrinsic state is unchanged; only its role in authorization decisions is affected.

---

59. Implementation Requirements

59.1 Required components

An implementation MUST provide:

1. Object encoding and decoding (canonical CBOR).
2. Signature and verification.
3. Hash computation.
4. Object type dispatch (domain separators).
5. Identity document validation.
6. Stream tracking (sequence, chain hash, sync state).
7. Authority validation.
8. Authorization evaluation.
9. Failure handling per §53.
10. Reconciliation per §54.
11. Local trust anchor storage.
12. Rendezvous client.

59.2 Recommended components

1. Local API server.
2. WireGuard integration.
3. Reachability publication.
4. NAT traversal.
5. Relay client.

59.3 Interoperability requirements

Two independent implementations MUST interoperate on:

1. Canonical encoding of all objects.
2. Signature verification.
3. Identity document validation.
4. Stream state management.
5. Authorization decisions.
6. Failure handling.

Test vectors (§60) and conformance scenarios (§61) define the minimum interop surface.

59.4 State durability

Trust anchors and accepted stream state MUST be durable across restarts. Local observation history for relative validity MUST be durable.

Reachability state MAY be ephemeral.

59.5 Cryptographic requirements

Implementations MUST use Ed25519, SHA-256, and deterministic CBOR. Implementations MUST NOT use non-deterministic signature schemes for signed objects.

---

60. Test Vectors and Conformance

60.1 Purpose

Test vectors define exact byte sequences and their expected interpretations. Two implementations that pass the same test vectors interoperate at the object level.

60.2 Required test vectors

For each object type:

· Canonical encoding (exact bytes).
· Hash (object_id).
· Payload hash (payload_id).
· Signature (exact bytes).
· Verification (accept).
· Tampered field (reject).
· Wrong domain separator (reject).
· Wrong version (reject).

60.3 Negative test vectors

Required negative vectors:

· Non-minimal integer encoding.
· Incorrectly ordered map keys.
· Floating-point field.
· Duplicate set entry.
· Set entries out of canonical order.
· Missing required field.
· Extra unknown field.
· Oversized field.
· Replayed object.
· Expired object.
· Revoked object.
· Invalid previous_hash.
· Invalid chain_hash.
· Wrong issuer for object type.
· Signature from wrong key role.
· Fork at same sequence.
· Gap in stream.
· Non-canonical CBOR encoding.

60.4 Conformance levels

· Level 1 — Encoding. Correct canonical encoding and decoding of all object types.
· Level 2 — Verification. Correct validation including signatures, authority, chains.
· Level 3 — Authorization. Correct authorization decisions per §40.6 and §48.8.
· Level 4 — Failure handling. Correct behavior under §53.
· Level 5 — Reconciliation. Correct behavior under §54.

---

61. Verifier Conformance Scenarios

Each scenario specifies: initial state, incoming objects, expected decisions, expected final state. Scenarios are executable tests.

61.1 Scenario: Fresh peer

Initial: No local state for peer P.

Incoming: Pairing completes; grant and lease received.

Expected: Peer P is KNOWN, relationship RECOGNIZED, grant GRANTED, lease VALID. Authorization succeeds.

61.2 Scenario: Offline peer returns

Initial: Peer P is KNOWN, RECOGNIZED, with valid grant and lease. Last observation was 3 months ago.

Incoming: Reachability record with new endpoint.

Expected: Peer P is reachable at new endpoint. Identity and authorization state unchanged. Authorization succeeds if lease is still valid.

61.3 Scenario: Lease expires while offline

Initial: Valid lease with relative validity. Verifier offline past expiry.

Incoming: Reachability record. No new lease.

Expected: Lease state EXPIRED. Authorization fails. Peer remains KNOWN and RECOGNIZED.

61.4 Scenario: Revocation occurs while offline

Initial: Valid lease. Verifier offline.

Incoming: Revocation for the lease, then a reachability record.

Expected: Lease REVOKED. Authorization fails. Revocation cached. Subsequent renewal attempt rejected.

61.4b Scenario: Revocation arrives before its target

Initial: No knowledge of grant G.

Incoming: Revocation for G, then G.

Expected: Revocation cached when received. G rejected on first observation. G is REVOKED.

61.5 Scenario: Authorization-key compromise

Initial: Active Authorization Key K.

Incoming: KeyRevocation { key_id=K, effective_sequence=N } signed by Identity Root. Objects signed by K at sequence ≥ N.

Expected: Objects at sequence ≥ N are invalid. Objects before N remain valid. New key K' becomes active.

61.6 Scenario: Key rotation mid-chain

Initial: Peer P with trusted root R1.

Incoming: IdentityContinuity signed by R1 and R2, followed by new identity document signed by R2.

Expected: Trusted root updated to R2. Stream advances. Historical state preserved.

61.7 Scenario: Identity fork

Initial: Peer P accepted identity state at sequence 10, hash H.

Incoming: Identity document at sequence 10, hash H' (different).

Expected: Identity stream FORKED. Accepted state (H) remains effective. Authorization based on pre-fork state continues. Disputed branch contributes nothing.

61.8 Scenario: Gap in received chain

Initial: Accepted sequence 10 for peer's stream.

Incoming: Object at sequence 15.

Expected: Stream enters SYNCING. Authorization uses last accepted state (sequence 10). Verifier attempts to obtain 11–14. Stream does NOT become FORKED.

61.9 Scenario: Conflicting rendezvous data

Initial: Cached reachability record R1 at endpoint E1.

Incoming: Reachability record R2 at same sequence, different chain hash.

Expected: Reachability stream FORKED. Neither endpoint used. Previous accepted endpoint (if any) remains in effect.

61.10 Scenario: Stale reachability record

Initial: Cached reachability record within validity.

Incoming: Attempted connection fails.

Expected: Record's protocol state unchanged. Local observation recorded as soft annotation. Verifier attempts refresh. Authorization state unaffected.

61.11 Scenario: Direct path fails, relay succeeds

Initial: Peer authorized, reachability record with candidates.

Incoming: Direct connection fails; relay ticket obtained; relay path established.

Expected: Connection established via relay. Authorization state unchanged. Both direct and relayed paths represent the same identity relationship.

61.12 Scenario: Relay disappears during session

Initial: Active session via relay.

Incoming: Relay unreachable.

Expected: Session disrupted. Verifier attempts direct path. If direct fails, retries relay or alternate. Authorization state unchanged.

61.13 Scenario: Grant reissued after terminal revocation

Initial: Grant G1 revoked.

Incoming: New grant G2 with new grant_id, same subject, same capability.

Expected: G1 remains REVOKED. G2 is GRANTED. Authorization uses G2. No state inherited from G1.

61.14 Scenario: Freshness elapses without revocation

Initial: Valid lease, max_offline_tolerance = 7 days. No network connectivity.

Incoming: Time elapses past 7 days.

Expected: Lease transitions to STALE. Authorization fails. On successful refresh within 30 days, lease returns to VALID. Authorization succeeds.

61.15 Scenario: Local storage loss

Initial: Peer P KNOWN, RECOGNIZED, authorized.

Incoming: Local storage lost.

Expected: Verifier returns to UNKNOWN for P. Authorization fails. Reachability may be reconstructed from received objects. Trust anchor must be re-established via pairing or provisioning.

---

62. Future Extensions

62.1 Chain-extension proofs

Authenticated proofs that permit skip-ahead while preserving fork detection. Must satisfy §45.6 requirements.

62.2 Sophisticated recovery

Threshold recovery, social recovery, hardware-backed roots. Must not introduce a new authority; recovery mechanisms MUST compose existing authority domains.

62.3 Delegated administration

Delegation of specific identity-document operations without exposing the Identity Root. Must be expressed as a new key role and added to §58.2.

62.4 Groups

Multi-principal structures. Must not violate the "no new authority" principle.

62.5 Service ownership transfer

Authenticated transfer with dual signature. V1 does not support this; a future extension MAY define it.

62.6 Rendezvous federation and gossip

Bounded anti-entropy with explicit quotas. Must not grant rendezvous any signing authority.

62.7 DHT-based discovery

Only if the above prove insufficient. Must not become an authority.

62.8 Metadata protection

Rotating pseudonyms for rendezvous lookups. Reduced correlation of peer activity.

62.9 Reputation and liveness scoring

Explicitly out of scope for identity. If implemented, reputation belongs in a deployment-layer policy engine that consumes authenticated identity, not in the identity document.

62.10 Documented anti-patterns

The following have been considered and rejected:

XOR-based endpoint obfuscation. XOR with a shared key provides no confidentiality against any party holding the key, cannot support revocation, and cannot be upgraded without a wire-format change. The protocol uses authenticated encryption with per-recipient key agreement, or no encryption at all when endpoints are intended to be public.

Shared-key encryption for endpoint records. Same issues as XOR with a shared key: no revocation, no per-recipient integrity, no upgrade path without new key distribution.

DNS-like hierarchical naming. The protocol's identifiers are opaque and flat. Introducing hierarchy would import DNS's authority model, which the protocol rejects.

Timestamp-based fork resolution. Wall-clock time is not a resolution mechanism (§54.9).

Automatic recovery from Identity Root compromise. No in-band mechanism exists or is proposed, because any such mechanism would be an authority the protocol cannot trust.

---

Final Protocol Statement

A Peer Principal is a durable cryptographic identity.

Devices, services, and infrastructure are subordinate to it and replaceable.

Relationships between principals are explicit.

Authorization is directional, scoped, and temporary.

Leases provide bounded proof of current authorization.

Revocation is terminal.

Keys can rotate without changing principal identity.

Reachability is ephemeral and untrusted.

Rendezvous infrastructure provides discovery but no authority.

Transport is pluggable.

The resulting security question:

Can the verifier, using its trusted anchors and locally available signed state, deterministically establish who the peer is, what it is authorized to do, whether that authorization is currently valid, and whether it has been revoked?

If the answer is yes, the peer can be trusted regardless of its current IP address, NAT mapping, rendezvous provider, relay, physical network, or whether it has been offline for months.

That is the fundamental purpose of the Mesh Identity & Reachability Protocol.