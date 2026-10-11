Mesh Identity & Reachability Protocol

Design Document — v0.3

Status: Draft
Version: 0.3
Scope: Identity, relationships, authorization, revocation, reachability, and transport integration

⸻

1. Abstract

The Mesh Identity & Reachability Protocol is an open protocol for establishing persistent, mutually authenticated relationships between machines and services without requiring permanent accounts, centralized identity providers, or fixed network locations.

The protocol provides a control plane above existing networking technologies.

It does not attempt to replace WireGuard, IPv6, NAT traversal, relays, DNS, or application-level authorization. Instead, it establishes:

* who a peer is;
* which devices and services belong to that peer;
* which peers recognize one another;
* what one peer is authorized to do;
* whether that authorization remains valid;
* whether authorization has been revoked;
* how a peer can currently be reached.

Network location is deliberately treated as ephemeral.

A machine may change its IP address, move between networks, disappear for months, change NAT mappings, or use a relay without changing its cryptographic identity or relationships.

⸻

2. Core Security Invariant

The fundamental protocol invariant is:

Given a set of locally trusted anchors, authenticated protocol objects, known revocations, and a defined verifier time, a verifier must be able to deterministically establish the identity, authorization, validity, and freshness state of a peer without contacting an authority.

Network access may improve freshness, discover new reachability information, or obtain newer objects.

It must not be required to establish authenticity.

This means:

* rendezvous infrastructure cannot define identity;
* relays cannot define authorization;
* DNS cannot define identity;
* IP addresses cannot define identity;
* WireGuard keys cannot by themselves define application authorization;
* temporary pairing codes cannot become permanent credentials.

⸻

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

The protocol should support:

* multiple devices belonging to one principal;
* multiple services per device;
* service-specific authorization;
* temporary guests;
* delegated administration;
* groups;
* multiple rendezvous providers;
* direct peer-to-peer connections;
* relay fallback;
* local-first operation;
* identity portability;
* hardware-backed keys.

These features should not complicate the V1 security kernel unless required.

⸻

4. Non-Goals

The protocol is not intended to be:

* a replacement for WireGuard;
* a general-purpose VPN;
* a global DNS replacement;
* a universal application authorization framework;
* a blockchain;
* a global identity registry;
* a mandatory centralized account system;
* a mandatory DHT;
* a permanent network locator;
* a substitute for application-level authentication.

Applications may continue to implement their own authorization.

The mesh layer provides authenticated identity and scoped network/service authorization that applications may consume.

⸻

5. Conceptual Architecture

The system consists of four major layers.

┌──────────────────────────────────────────────┐
│                  Application                 │
│       Jellyfin / SSH / Files / APIs         │
├──────────────────────────────────────────────┤
│          Mesh Identity & Authorization       │
│ Principal / Device / Service / Grant / Lease│
├──────────────────────────────────────────────┤
│               Reachability                   │
│ Discovery / NAT Traversal / Relay / Paths  │
├──────────────────────────────────────────────┤
│                  Transport                   │
│       WireGuard / QUIC / TCP / IPv6        │
└──────────────────────────────────────────────┘

The identity and authorization layer is independent of the transport.

⸻

6. Peer Principal

A Peer Principal is the durable logical identity represented by the protocol.

It is not necessarily:

* one physical machine;
* one operating-system installation;
* one network interface;
* one device key;
* one service.

A principal may own multiple devices and services.

For example:

Principal: Dad
 ├── Home Server
 │    ├── Jellyfin
 │    └── File Service
 │
 ├── Laptop
 └── Phone

The principal survives replacement of individual devices.

⸻

7. Peer Principal ID

The Peer Principal ID is an opaque, randomly generated identifier.

Example:

peer:v1:7f3a9c2e5d91b0a4c7e8126fa31d449b

The ID is not self-certifying.

Instead, the identity document binds the ID to the principal’s identity root.

This deliberately separates:

Identity
    =
Peer ID + signed identity document + trusted root

from:

Identifier
    =
opaque reference

Advantages:

* identity-root rotation does not change the Peer ID;
* provisioning can occur before key generation;
* cryptographic constructions can change in future protocol versions;
* identifiers do not expose the construction used to derive them;
* relationships remain stable through root-key replacement.

⸻

8. Identity Root

Each principal has an Identity Root.

The root is the highest cryptographic authority for that principal.

It is used to:

* establish the identity document;
* authorize device keys;
* authorize service keys where appropriate;
* delegate authorization authority;
* rotate subordinate keys;
* recover from subordinate-key compromise.

The identity root should not normally participate in routine network sessions.

Ideally it may remain offline or hardware-protected.

⸻

9. Key Hierarchy

The protocol distinguishes several key roles.

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

9.1 Identity Root

Highest authority.

9.2 Device Key

Identifies an authorized device belonging to the principal.

9.3 Service Key

Identifies a service exposed by a device.

9.4 Authorization Key

Authorizes grants and leases within a delegated scope.

9.5 Recovery Authority

Recovery mechanisms are intentionally separated from ordinary V1 operation.

V1 supports root-authorized key replacement.

More sophisticated recovery mechanisms, including threshold recovery, are future work.

⸻

10. Identity Documents

The identity document establishes the cryptographic structure of a principal.

Conceptually:

IdentityDocument {
    version
    peer_id
    sequence
    previous_hash
    identity_root
    authorized_keys
    device_bindings
    service_bindings
    validity
    signature
}

The exact encoding is defined by OBJECTS.md.

Identity documents form a linear signed history.

Document 0
    ↓
Document 1
    ↓
Document 2
    ↓
Document 3

⸻

11. Identity Document History

Identity state is append-only.

Each document references its immediate predecessor.

A verifier may accept a current document without downloading every historical document if the document is otherwise valid and chains to a trusted state.

Intermediate documents remain useful for:

* auditing;
* forensic investigation;
* debugging;
* historical reconstruction.

Conflicting documents with the same issuer and sequence number constitute an identity-state conflict.

Implementations MUST NOT resolve such conflicts by simply selecting the newest timestamp.

⸻

12. Relationship

A Relationship expresses mutual recognition between two principals.

It answers:

“Do these principals recognize one another?”

Relationships are conceptually symmetrical.

Example:

Ryan ↔ Dad

A relationship does not automatically grant access.

Recognition and authorization are separate.

⸻

13. Grant

A Grant is directional.

It answers:

“What is Principal A authorizing Principal B to do?”

Example:

Dad
  │
  │ grants
  ▼
Ryan
  │
  └── jellyfin.stream

A grant may contain:

* relationship ID;
* issuer;
* subject;
* device scope;
* capabilities;
* resources;
* constraints;
* lease policy;
* issuance information;
* sequence information;
* signature.

⸻

14. Lease

A Lease proves that a grant is currently valid for a defined period.

The distinction is:

Relationship
    "We recognize each other."
Grant
    "You are authorized for X."
Lease
    "That authorization is currently valid."

Leases should normally be short-lived relative to relationships.

Examples:

Jellyfin streaming: 30 days
File access:        7 days
SSH:                 1 hour
Administrative SSH: 15 minutes

Exact durations are policy decisions.

⸻

15. Capabilities

Capabilities describe what a peer may do.

Capabilities are structured rather than arbitrary strings.

Conceptually:

Capability {
    namespace
    action
    resource
    constraints
}

Example:

namespace: jellyfin
action:    stream
resource:  library:movies

Another:

namespace: ssh
action:    connect
resource:  host:home-server

Capabilities describe authorization semantics.

They do not determine lease duration or offline tolerance.

⸻

16. Authorization Policy

Policy belongs to grants and relationships rather than the capability vocabulary.

For example:

Grant:
    capability = jellyfin.stream
    lease_duration = 30 days
    offline_tolerance = 30 days

Another grant may contain:

Grant:
    capability = ssh.admin
    lease_duration = 15 minutes
    offline_tolerance = 0

This allows the same capability vocabulary to be used under different trust policies.

⸻

17. Network Authorization vs Application Authorization

The mesh protocol should distinguish:

Network authorization

May this peer establish a connection to this service/device?

Application authorization

Once connected, what may the application itself do?

The mesh layer should not attempt to replace application-level access control.

For example:

Mesh:
    Ryan may connect to Jellyfin.
Jellyfin:
    Ryan may access Movies but not Admin.

Applications may use mesh identity information as an authentication input.

⸻

18. Revocation

Revocation is terminal.

An object that has been revoked MUST NOT become valid again.

If authorization needs to be restored, a new object is issued.

For example:

Grant A
    ↓
revoked
Grant B
    ↓
new authorization

Never:

Grant A
    ↓
revoked
    ↓
unrevoked

⸻

19. Revocation Hierarchy

Revocations have different blast radii.

Conceptually:

Lease
  ↓
Grant
  ↓
Device
  ↓
Authorization Key
  ↓
Principal

A revocation MUST explicitly define which subordinate authorization state it invalidates.

For example:

Revoke lease

Invalidates one current authorization period.

Revoke grant

Invalidates future leases derived from that grant.

Revoke device

Invalidates device-specific authorization and services.

Revoke authorization key

Invalidates authorization objects issued by that key.

Revoke principal

Invalidates the principal’s entire identity.

⸻

20. Key Revocation

Key IDs are immutable.

Once a key is revoked, that key ID can never be reused.

Replacement always creates a new key ID.

auth-key-A
    ↓
REVOKED
auth-key-B
    ↓
NEW

This prevents un-revocation and rollback attacks.

⸻

21. Authorization-Key Compromise

Authorization-key compromise is a first-class threat.

The normal recovery sequence is:

Authorization Key compromised
          ↓
Identity Root revokes key
          ↓
All affected authorization state becomes invalid
          ↓
Identity Root creates new Authorization Key
          ↓
New authorization state is issued

The principal identity remains unchanged.

A compromised authorization key does not automatically imply compromise of:

* the principal identity;
* other devices;
* unrelated service keys;
* the identity root.

⸻

22. Identity Root Compromise

Identity-root compromise is substantially more severe.

A compromised root can potentially:

* replace subordinate keys;
* revoke legitimate keys;
* issue contradictory identity state;
* create fraudulent authorization.

V1 therefore treats the root as the highest trust anchor.

Advanced recovery mechanisms are deferred to V2.

Possible future mechanisms include:

* offline recovery keys;
* hardware-backed roots;
* threshold recovery;
* multi-party approval;
* social recovery.

⸻

23. Key Rotation

Key rotation is a V1 requirement.

Rotation must preserve the Peer Principal ID.

Example:

Peer ID: P
Root Key A
    ↓
Root Key B
    ↓
Root Key C

The identity history establishes the transition.

Subordinate keys may likewise be replaced without changing the principal.

⸻

24. Pairing

Pairing creates the initial trusted relationship.

The human interaction should be simple:

Device A displays:
    481729
Device B enters:
    481729

The six-digit value is not a credential.

It is a temporary human coordination mechanism.

The underlying cryptographic exchange provides the actual security.

⸻

25. Pairing Protocol

V1 pairing MUST use an established PAKE or authenticated key-establishment protocol rather than a custom challenge-response construction.

A candidate construction is SPAKE2 or CPace.

The final protocol must specify:

* exact PAKE;
* transcript construction;
* identity binding;
* protocol version;
* context binding;
* replay protection;
* code lifetime;
* retry limits;
* enumeration resistance.

The pairing transcript MUST bind the identities being introduced.

This prevents unknown-key-share attacks.

⸻

26. Pairing Code

The six-digit code has approximately 20 bits of entropy.

It MUST therefore never be treated as sufficient cryptographic authentication by itself.

The code should be:

* short-lived;
* single-use;
* rate-limited;
* invalidated after successful pairing;
* invalidated after timeout;
* invalidated after excessive failed attempts.

The durable credential is the resulting cryptographic relationship.

⸻

27. Human Verification

Where stronger assurance is required, devices may display a verification value derived from the pairing transcript.

Example:

8341 2910

or a word sequence.

Both users can compare the value over an independent channel.

This protects against a compromised rendezvous infrastructure attempting active interception.

⸻

28. Permanent Identity References

A permanent identity reference identifies a principal.

It does not authorize access.

This distinction is critical.

Identity Reference
    ≠
Pairing Invitation
    ≠
Authorization Grant
    ≠
Recovery Credential

A permanent identity reference may safely be stored for years.

A pairing invitation should be temporary.

An authorization lease should expire.

⸻

29. Mesh URI

The protocol may define a human- and machine-readable URI:

mesh://v1/...

The URI grammar MUST be formally specified.

Parsing must be strict.

Implementations MUST reject malformed or ambiguous forms.

The URI must clearly distinguish:

* identity references;
* temporary invitations;
* capability requests;
* rendezvous hints.

A permanent URI MUST NOT contain a mandatory fixed rendezvous dependency.

⸻

30. Rendezvous

Rendezvous infrastructure provides discovery.

It does not provide identity authority.

It may answer:

“Where has Peer P recently announced itself?”

It must not answer:

“Is this really Peer P?”

The verifier determines that using cryptographic identity documents.

⸻

31. Rendezvous Trust Model

Rendezvous infrastructure is untrusted.

A malicious rendezvous server may:

* provide stale endpoints;
* provide false endpoints;
* suppress endpoint information;
* observe metadata;
* attempt denial of service.

It must not be able to:

* forge a peer identity;
* forge authorization;
* create a valid lease;
* revoke authorization;
* decrypt transport traffic.

⸻

32. Rendezvous Evolution

V1 should use one simple self-hostable rendezvous protocol.

Future versions may add:

V1  HTTPS rendezvous
V2  Multiple interchangeable rendezvous servers
V3  Federation
V4  Peer-assisted gossip
V5  DHT, if required

DHT infrastructure should not be introduced merely because decentralized discovery sounds attractive.

⸻

33. Reachability

Reachability information is ephemeral.

A peer may publish:

ReachabilityRecord {
    peer_id
    device_id
    endpoint
    transport
    observed_at
    expiration
    signature
}

Examples:

IPv6 address
IPv4 + UDP port
NAT mapping
Relay endpoint
Local LAN endpoint

Reachability records do not establish identity.

⸻

34. Relays

Relays are transport infrastructure.

They may forward encrypted traffic when direct connectivity fails.

Relays should not receive authorization authority.

The desired architecture is:

Peer A
   │
   ├──── direct ──── Peer B
   │
   └──── relay ───── Peer B

Both paths represent the same identity relationship.

⸻

35. Transport

WireGuard is the preferred initial transport.

However:

WireGuard is a transport security mechanism, not the mesh authorization system.

WireGuard establishes encrypted communication between cryptographic endpoints.

The mesh control plane determines:

* which peer that endpoint belongs to;
* whether the relationship is recognized;
* whether the peer is authorized;
* whether its lease is valid;
* which service it may access.

Other transports may be supported later.

⸻

36. Enforcement

Mesh authorization may be enforced at several layers:

Mesh daemon
    ↓
WireGuard configuration
    ↓
Firewall / nftables / eBPF
    ↓
Reverse proxy / gateway
    ↓
Application

The protocol does not require WireGuard itself to understand mesh leases.

A host implementation may translate authorization state into transport or firewall configuration.

⸻

37. Service Discovery

Services publish signed service records.

Example:

ServiceRecord {
    service_id
    peer_id
    device_id
    service_type
    endpoint
    capabilities
    metadata
    expiration
    signature
}

Service records are signed by the service-authorized key defined in the authority matrix.

Example:

service:jellyfin
service:ssh
service:smb

A service record does not grant access.

Authorization remains separate.

⸻

38. Offline Operation

Offline operation is a first-class property.

A peer may remain offline for months.

Other peers should retain:

* principal identity;
* relationship state;
* last known authorization;
* last known reachability;
* lease state;
* revocation state.

An offline peer should be represented as:

KNOWN
TRUSTED
OFFLINE
LAST SEEN: ...

rather than as an unknown identity.

⸻

39. Lease Expiration

A lease can expire without active revocation.

This is the primary mechanism limiting the consequences of offline authorization.

For example:

Lease expires
    ↓
No new lease
    ↓
Access denied

The relationship itself may remain intact.

The peer can reconnect and obtain a new lease if policy permits.

⸻

40. Revocation Propagation

Revocation propagation is separate from revocation validity.

A revocation becomes authoritative because it is correctly signed.

Its propagation determines how quickly other peers learn about it.

V1 should support:

Pull on reconnect

A peer asks the issuer for newer authorization state.

Opportunistic synchronization

Peers exchange newer signed objects whenever they communicate.

Future versions may add:

* push;
* gossip;
* federated revocation distribution.

A verifier that has not yet received a revocation may temporarily continue honoring a valid lease until its defined expiration.

This is an unavoidable consequence of offline operation.

Security policy therefore controls the maximum exposure window through lease duration.

⸻

41. Time Semantics

Signed objects may contain:

issued_at
not_before
expires_at

issued_at records the issuer’s asserted creation time.

It is not by itself proof of validity.

Absolute validity intervals are used because authorization state must be deterministic between different verifiers.

Implementations MUST define an acceptable clock-skew tolerance.

For example:

MAX_CLOCK_SKEW = 5 minutes

The exact value is protocol policy.

Implementations MUST NOT silently invent their own semantics.

The verifier uses its local time for validity checks.

Monotonic local time should be used for measuring elapsed intervals where the operating system provides it.

⸻

42. Issued-at Ordering

Within an issuer’s object chain, implementations should enforce monotonicity constraints on timestamps where the object semantics require them.

A later sequence number MUST NOT normally contain an earlier issued_at than an already accepted predecessor.

Backdating should be treated as suspicious or invalid according to the object type.

Sequence numbers, rather than wall-clock time, remain the authoritative ordering mechanism.

⸻

43. Cryptographic Object Encoding

All signed protocol objects use one canonical encoding defined by OBJECTS.md.

V1 is expected to use deterministic CBOR.

The canonicalization rules MUST explicitly define:

* integer encoding;
* map ordering;
* byte strings;
* text strings;
* arrays;
* prohibited values;
* prohibited floating-point values;
* null/default handling;
* integer ranges.

Floating-point values should be prohibited from signed V1 objects.

The protocol must include canonical binary test vectors.

⸻

44. Domain Separation

Every signed object type has a unique domain separator.

Examples:

mesh/identity-document/v1
mesh/device-binding/v1
mesh/service-record/v1
mesh/relationship-grant/v1
mesh/authorization-lease/v1
mesh/revocation/v1
mesh/reachability/v1

The domain separator is included in the signature input.

This prevents a valid signature over one object type from being reused as a signature over another object type.

⸻

45. Cryptographic Baseline

V1 targets:

* Ed25519 signatures;
* SHA-256 hashes;
* deterministic CBOR;
* cryptographically random identifiers.

The exact wire representation of signatures, hashes, and keys is defined by OBJECTS.md.

Cryptographic agility should be possible at protocol-version boundaries without creating ambiguous algorithm negotiation.

⸻

46. Object Identity

Each signed object has a deterministic object identifier derived from its canonical representation.

Conceptually:

object_id = SHA-256(canonical_signed_object)

This allows other objects to refer to an exact historical object.

Revocation should therefore reference the exact object ID rather than vaguely referring to “the current grant.”

⸻

47. Sequence and History

Mutable object streams use:

sequence
previous_hash

The combination establishes ordered history.

Example:

Object 1
sequence = 1
previous_hash = null
Object 2
sequence = 2
previous_hash = H(Object 1)
Object 3
sequence = 3
previous_hash = H(Object 2)

Two objects with:

issuer = X
sequence = 3

but different content represent a fork.

Implementations MUST NOT arbitrarily choose one.

Fork handling and higher-order historical proofs may be extended in future versions.

⸻

48. Trust Anchors

A verifier maintains explicit local trust anchors.

A trust anchor typically contains:

peer_id
trusted_identity_root
accepted_identity_state
acceptance_time

Trust anchors are established through:

* explicit pairing;
* local administrative configuration;
* trusted provisioning;
* future recovery mechanisms.

A rendezvous server is never itself a trust anchor.

⸻

49. Verification

A verifier should conceptually execute:

1. Identify Peer Principal.
2. Validate identity document.
3. Validate key chain.
4. Validate device/service binding.
5. Validate relationship.
6. Validate grant.
7. Validate lease.
8. Apply revocations.
9. Check validity interval.
10. Check local policy.
11. Determine authorization.

The result should be deterministic.

⸻

50. Security State Machine

The fundamental peer state machine is:

UNKNOWN
   │
   │ successful pairing
   ▼
INTRODUCED
   │
   │ valid relationship + grant + lease
   ▼
AUTHORIZED
   │
   ├───────────────┐
   │               │
   ▼               ▼
EXPIRED          REVOKED
   │               │
   │ new lease     │ new relationship/grant
   │ if permitted  │
   └──────► AUTHORIZED

REVOKED is terminal for the affected authorization object.

A new authorization requires a new object.

⸻

51. Trust Domains

The protocol defines distinct trust domains.

Identity authority

Controls the principal’s identity and subordinate keys.

Relationship authority

Controls recognition and relationship state.

Service authority

Controls service identity and service records.

Rendezvous infrastructure

Provides discovery only.

Transport

Provides encrypted communication.

No layer should silently acquire authority belonging to another.

⸻

52. Threat Model

The protocol assumes attackers may control:

* IP routing;
* DNS;
* rendezvous servers;
* relay servers;
* network traffic;
* endpoint discovery;
* individual subordinate keys.

Attackers may attempt:

* MITM;
* replay;
* identity substitution;
* authorization forgery;
* stale-state replay;
* rollback;
* fork creation;
* revocation suppression;
* endpoint poisoning;
* key compromise;
* unknown-key-share attacks;
* denial of service.

The protocol does not guarantee availability.

Its primary security goal is authenticity and authorization correctness.

⸻

53. Compromise Model

The system distinguishes compromise levels.

Service Key
    ↓
Device Key
    ↓
Authorization Key
    ↓
Identity Root

Compromise of a lower-level key should not automatically compromise higher-level keys.

The protocol should minimize blast radius.

Each key class therefore has explicit authority.

⸻

54. Privacy Considerations

Peer IDs should not encode:

* IP addresses;
* usernames;
* email addresses;
* hardware identifiers;
* geographic information.

Rendezvous metadata may nevertheless reveal:

* approximate online times;
* endpoint information;
* relationship activity;
* service availability.

Future versions may add privacy-preserving rendezvous mechanisms.

Privacy is not assumed merely because identity is cryptographically decentralized.

⸻

55. Application API

A local mesh daemon may expose APIs such as:

mesh.discover()
mesh.resolve(peer)
mesh.connect(peer, service)
mesh.authorize(peer, capability)
mesh.revoke(object)
mesh.status(peer)

Applications should not need to understand:

* NAT traversal;
* rendezvous protocols;
* WireGuard configuration;
* key rotation;
* lease renewal.

The daemon acts as the local control-plane implementation.

⸻

56. V1 Scope

V1 should remain deliberately narrow.

Required:

1. Peer Principal identity.
2. Opaque Peer IDs.
3. Identity Root.
4. Device keys.
5. Signed identity documents.
6. Key rotation.
7. Human-mediated QR/copy-paste pairing.
8. Established PAKE.
9. Relationships.
10. Scoped grants.
11. Expiring leases.
12. Terminal revocation.
13. Authorization-key revocation.
14. One self-hostable rendezvous service.
15. Direct connectivity.
16. WireGuard integration.
17. Offline verification.
18. Canonical object encoding.
19. Positive and negative test vectors.

Features such as:

* DHT;
* federation;
* gossip;
* sophisticated recovery;
* threshold roots;
* advanced privacy-preserving discovery;
* automatic multi-hop routing

should wait until the core protocol is interoperable.

⸻

57. Implementation Order

Implementation should proceed in this order:

Phase 1 — Object model

Implement:

* canonical encoding;
* hashing;
* signatures;
* object IDs;
* identity documents;
* key hierarchy.

No networking required.

Phase 2 — Verification engine

Implement:

* object validation;
* chain validation;
* fork detection;
* time validation;
* revocation;
* authorization evaluation.

Phase 3 — Pairing

Implement:

* six-digit pairing UX;
* PAKE;
* transcript binding;
* identity exchange;
* relationship creation.

Phase 4 — Authorization

Implement:

* grants;
* leases;
* renewal;
* expiration;
* revocation.

Phase 5 — Local daemon

Expose the control-plane API.

Phase 6 — Rendezvous

Implement basic HTTPS discovery.

Phase 7 — Transport

Integrate WireGuard.

Phase 8 — NAT traversal and relay

Add direct-path optimization and relay fallback.

This order deliberately proves the security state machine before networking complexity is introduced.

⸻

58. Required Specifications

The protocol should eventually consist of:

ARCHITECTURE.md
IDENTITY.md
OBJECTS.md
PAIRING.md
AUTHORIZATION.md
REVOCATION.md
RENDEZVOUS.md
TRANSPORT.md
SERVICE-INTEGRATION.md
THREAT-MODEL.md
TEST-VECTORS.md

OBJECTS.md is the normative foundation for the remaining documents.

⸻

59. OBJECTS.md Requirements

OBJECTS.md MUST define:

1. Canonical encoding.
2. Hash algorithm.
3. Signature algorithm.
4. Domain separators.
5. Key identifiers.
6. Common object envelope.
7. Signing authority matrix.
8. Identity documents.
9. Device bindings.
10. Service records.
11. Relationships.
12. Grants.
13. Leases.
14. Revocations.
15. Key rotations.
16. Reachability records.
17. Sequence semantics.
18. Previous-hash semantics.
19. Fork handling.
20. Timestamp semantics.
21. Clock-skew rules.
22. Validity rules.
23. Object IDs.
24. Positive test vectors.
25. Negative/adversarial test vectors.

Every normative object should have a complete canonical example.

⸻

60. Signing Authority Matrix

The following authority model is normative at the architectural level.

Object	Signing authority
Identity Document	Identity Root
Device Binding	Identity-authorized authority
Service Binding	Identity/device-authorized service authority
Service Record	Service Key
Relationship Grant	Authorized Relationship/Authorization Key
Authorization Lease	Authorized Authorization Key
Revocation	Authority governing the revoked object
Reachability Record	Device Key
Key Rotation	Existing authority governing the rotated key

Where delegation is permitted, it MUST be explicitly represented in the identity state.

Implementations MUST NOT infer authority from object type alone.

The exact delegation rules belong in OBJECTS.md.

⸻

61. Negative Test Requirements

Interoperability testing must include invalid objects.

Examples:

* modified signed field;
* wrong signature;
* wrong domain separator;
* malformed canonical CBOR;
* non-minimal integer encoding;
* incorrectly ordered map keys;
* floating-point field;
* expired lease;
* lease not yet valid;
* revoked grant;
* revoked key;
* wrong issuer;
* wrong subject;
* invalid previous hash;
* duplicate sequence;
* conflicting sequence;
* replayed object;
* unauthorized signer;
* malformed URI;
* unknown capability;
* forged service record.

The implementation should return deterministic validation failures.

⸻

62. Operational Model

From the user’s perspective, the protocol should feel simple.

Example:

Install Mesh on Dad's server.
Install Mesh on Ryan's laptop.
Dad's server:
    "Pair device"
Server displays:
    QR + short code
Ryan scans QR / enters code.
Both devices verify pairing.
Relationship established.
Ryan sees:
    Dad
      └── Jellyfin
Ryan selects:
    Connect
Mesh:
    resolve identity
    discover endpoint
    establish WireGuard
    validate lease
    connect to Jellyfin

The user should not need to understand:

* keys;
* NAT;
* rendezvous;
* WireGuard;
* leases;
* revocation.

Those are implementation details of the control plane.

⸻

63. Example Security Scenario

Suppose Ryan is authorized to stream from Dad’s Jellyfin server.

The state is:

Relationship:
    Dad ↔ Ryan
Grant:
    Dad → Ryan
    capability = jellyfin.stream
Lease:
    valid for 30 days

Ryan’s IP address changes.

Nothing about identity changes.

The old endpoint expires.

A new reachability record is published.

Ryan reconnects.

The same principal and relationship are recognized.

⸻

64. Compromise Scenario

Suppose Ryan’s laptop authorization key is stolen.

Dad revokes that authorization key.

The revocation propagates when Ryan’s other devices or Dad’s services synchronize.

Existing short-lived leases eventually become invalid.

A new authorization key is issued.

Ryan’s Peer Principal remains unchanged.

His other authorized devices remain valid.

This demonstrates the intended property:

Compromise of one credential should not require destroying unrelated identity or trust state.

⸻

65. Long-Term Offline Scenario

A server is offline for six months.

Other peers retain:

Peer Principal
Relationship
Last known services
Last known authorization
Last seen time

When the server returns:

1. Identity is validated from cached state.
2. New reachability is discovered.
3. Current authorization state is synchronized.
4. Expired leases are renewed if policy allows.
5. Revocations are applied.
6. Transport is established.

The server’s physical location is irrelevant to its identity.

⸻

66. Fundamental Separation

The protocol deliberately separates:

WHO
    Peer Principal
WHAT DEVICE
    Device Identity
WHAT SERVICE
    Service Identity
WHO TRUSTS WHOM
    Relationship
WHAT MAY THEY DO
    Grant
IS IT CURRENTLY VALID
    Lease
HAS IT BEEN CANCELLED
    Revocation
WHERE ARE THEY
    Reachability
HOW DO WE CONNECT
    Transport

This separation is the core architectural property of the system.

⸻

67. Final Protocol Statement

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

The resulting security question is:

Can the verifier, using its trusted anchors and locally available signed state, deterministically establish who the peer is, what it is authorized to do, whether that authorization is currently valid, and whether it has been revoked?

If the answer is yes, the peer can be trusted regardless of:

* its current IP address;
* its NAT mapping;
* its rendezvous provider;
* its relay;
* its physical network;
* whether it has been offline for months.

That is the fundamental purpose of the Mesh Identity & Reachability Protocol.