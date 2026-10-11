# Grid Network — Security Model

**Status:** Draft (extracted from PROTOCOL.md §50–§53)
**Version:** 1.0

---

## §1: THREAT MODEL

### 1.1 Adversaries we protect against

1. **Malicious peers** — Peer tries to impersonate another peer or forge authorizations
2. **Malicious rendezvous** — Rendezvous operator tries to MITM or forge reachability
3. **Malicious relay** — Relay operator tries to decrypt traffic or forge authorizations
4. **Eavesdropper** — Third party tries to intercept traffic or observe grants
5. **Network observer** — ISP or state actor tries to observe metadata
6. **Lost device** — Stolen phone contains valid authorization keys
7. **Insider threat** — Authorized person tries to exceed their authorization
8. **Time-skewed verifier** — Device with incorrect clock verifies leases wrong
9. **Offline attacker** — No internet, but has local access
10. **Replay attacker** — Replays captured packets from old sessions
11. **Sybil attacker** — Creates many fake identities
12. **Denial of service** — Overwhelms infrastructure with requests

### 1.2 What we do NOT protect against

- **Anonymity** — Grid is not an anonymity network. Peers are identified. Rendezvous can observe who is talking to whom.
- **Global surveillance** — Network observer can see all reachability hints. But cannot see content (transport provides that).
- **Quantum computers** — Ed25519 is vulnerable to quantum attacks. Grid will need to migrate to post-quantum crypto when needed.
- **Root compromise** — If device OS is compromised, all security is lost. Grid cannot protect against that.
- **Timezone bugs** — Verifier with wrong clock may incorrectly verify time-based proofs. Out-of-band clock sync is operator's responsibility.

---

## §2: BLAST RADIUS TABLE

| Component Compromised | Identity | Relationship | Authorization | Reachability |
|----------------------|----------|--------------|---------------|--------------|
| Peer's Identity Root | TOTAL | TOTAL | TOTAL | TOTAL |
| Peer's Auth Key | No | No | TOTAL | No |
| Peer's Device Key | No | No | No | Reachability only |
| Rendezvous Server | No | No | No | Yes (stale hints) |
| Relay | No | No | No | Metadata only |
| Eavesdropper | No | No | No | No (content encrypted) |

**Key insight:** Separation of key roles limits blast radius.

---

## §3: FAILURE SEMANTICS (F1–F6 TAXONOMY)

### F1: Authorization failure → Deny
Missing grant, expired lease, revocation applied → Connection denied. System is fail-closed. Missing information never grants access.

### F2: Reachability failure → Try alternatives
Rendezvous unreachable, endpoint stale, direct connection fails → Try relay. System is availability-preserving. One infrastructure failure doesn't break existing relationships.

### F3: Clock skew → Relative validity survives
Verifier's clock 1 hour behind issuer's → Relative lease still works. Absolute timestamps would fail. Grid uses relative by default.

### F4: Communication interruption → Cache and continue
Verifier offline, receives revocation later → Revocation cached, applied when object arrives. No silent state change.

### F5: Fork detection → Require resolution
Stream has two objects at same sequence → Fork detected. Requires explicit StreamResolution object. No silent choice.

### F6: Key compromise → Effective_sequence limits damage
Key compromised, retroactive revocation issued → Objects before effective_sequence remain valid. Damage is limited to forward time.

---

## §4: SECURITY PRINCIPLES

1. **No authority creates identity** — Identity is self-attested. Peer publishes identity document signed by their own Identity Root. Rendezvous is not authority.
2. **All authorization is local** — Verifier evaluates grants/leases using locally held state. No "call home" required. Offline operation works.
3. **Revocation is terminal** — Once revoked, object cannot become valid again. Prevents subtle bugs from temporary revocation semantics.
4. **Reachability is untrusted** — Reachability records are hints, not ground truth. Any can be stale or malicious. Verifier tries multiple endpoints.
5. **Infrastructure is replaceable** — Every infrastructure component (rendezvous, relay) can be swapped. Peer ID, relationships, and authorizations survive the change.
6. **Layering is strict** — Network authorization (Grid) and application authorization (app) are separate. Neither can violate the other.

---

## §5: COMPROMISE RESPONSE PROCEDURES

### If Authorization Key is compromised:

1. Principal publishes key revocation in identity stream
2. Specifies effective_sequence (marks which objects are affected)
3. All future objects signed by that key are invalid
4. Existing leases remain valid until expiry
5. New Authorization Key provisioned
6. New leases issued by new key
**Time to recovery:** Minutes (revocation must propagate via rendezvous)

### If Device Key is compromised:

1. Principal publishes key revocation
2. Device is now untrusted (can't sign reachability)
3. Remove device from device_bindings in identity document
4. Device is offline
5. User physically removes old device from network
**Time to recovery:** Hours (device physically removed)

### If Identity Root is compromised:

**NO IN-BAND RECOVERY** (v0.6.2 limitation)

Out-of-band options:
1. Principal contacts other peers who know them
2. Provides proof of ownership (social recovery)
3. Other peers issue new relationship assertions
4. Principal re-establishes network relationships

This is a fundamental limitation of v0.6.2. V2 may add threshold recovery.

---

## §6: IMPLEMENTATION REQUIREMENTS

### Implementations MUST:
- Use constant-time comparisons for cryptographic checks (prevent timing attacks)
- Validate all CBOR canonicalization before processing
- Implement signature verification with standard libraries (don't roll own crypto)
- Use OS-provided random number generation (don't seed with user input)
- Clear sensitive data from memory after use
- Not log private keys or authorization grants
- Implement rate limiting on rendezvous queries (prevent DoS)
- Validate all timestamps are within reasonable bounds (prevent wrapping)

### Implementations SHOULD:
- Use hardware-backed keys when available
- Support key sharding/threshold (future)
- Implement cache coherence for revocations
- Provide audit logs for sensitive operations
- Support multiple encryption transports (WireGuard, QUIC, TLS)

---

## §7: ATTACK SCENARIOS AND MITIGATIONS

### Scenario 1: MITM on pairing
- Attacker intercepts QR code
- Attacker follows pairing flow, claims to be Bob
- **Mitigation:** PAKE requires shared secret (QR code). Attacker doesn't have it.
- **Result:** Pairing fails, attacker cannot impersonate Bob

### Scenario 2: Replay attack
- Attacker captures grant message
- Attacker replays it months later
- **Mitigation:** Grant has timestamp, lease has expiry. Replayed old lease is invalid.
- **Result:** Attacker cannot gain access with old lease

### Scenario 3: Sybil attack
- Attacker creates 1000 fake peer IDs
- Attacker floods network with garbage
- **Mitigation:** Grid does not prevent Sybil. But relays enforce rate limits. Rendezvous enforces query limits. Cost scales with attack size.
- **Result:** Attacker can create fake peers but cannot flood infrastructure without paying for resources

### Scenario 4: Relay intercepts traffic
- Attacker runs a relay
- Attacker tries to decrypt forwarded traffic
- **Mitigation:** Content is encrypted by transport layer (WireGuard). Relay only sees ciphertext.
- **Result:** Attacker sees packet size and count, not content

### Scenario 5: Rendezvous gives false reachability
- Attacker runs a rendezvous
- Attacker claims peer is at 192.0.2.1
- **Mitigation:** Verifier treats reachability as untrusted. Tries endpoint. If connection fails, tries others.
- **Result:** Attacker can delay connections but cannot MITM (no key)

### Scenario 6: Grant forgery
- Attacker tries to forge grant
- **Mitigation:** Grant is signed by issuer's Authorization Key. Attacker doesn't have the key.
- **Result:** Forged grant fails signature verification

---

*End of Security Model draft — to be expanded with verifier rules, parser requirements, implementation guidance*

---

## Security Addendum (Detailed)

261004-notdns security addendum
Absolutely. I’d keep this parallel to v0.6.1, rather than putting all of the security material into the normative protocol amendment. It can serve as the security reference during implementation and review without expanding the kernel.

Mesh Identity & Reachability Protocol

Security Recap Addendum

Parallel to Protocol v0.6.1

Relationship: Companion document to Protocol v0.6.1
Normative scope: This document records security properties, threat boundaries, implementation requirements, and deployment considerations. It does not introduce new protocol authority, object types, or mandatory protocol mechanisms unless explicitly incorporated into the normative protocol specification.

⸻

1. Purpose

This document summarizes the security model of the Mesh Identity & Reachability Protocol as it exists alongside Protocol v0.6.1.

The protocol’s primary security property comes from separation of authority:

* identity establishes cryptographic control;
* relationships establish recognition;
* authorization establishes permission;
* leases establish current validity;
* reachability establishes current connectivity information;
* rendezvous provides discovery;
* relays provide transport;
* applications consume authorized connections.

No intermediary should become an authority merely by observing, storing, forwarding, or relaying mesh information.

This document exists to make that model explicit and to provide a reference for implementation, testing, security review, and deployment.

⸻

2. Security Model

The core security model is:

Identity
   │
   │ Who controls this cryptographic identity?
   ▼
Relationship
   │
   │ Who recognizes whom?
   ▼
Authorization
   │
   │ What is this identity allowed to do?
   ▼
Lease
   │
   │ Is that authorization currently valid?
   ▼
Connection
   │
   │ How can the authorized parties communicate?
   ▼
Direct transport ─────── Relay transport

Rendezvous and relay infrastructure operate outside the authority chain.

Rendezvous
    │
    └── discovery only
Relay
    │
    └── transport only
Identity / Authorization
    │
    └── cryptographic authority

A compromise of discovery or transport infrastructure should therefore result primarily in availability or metadata consequences rather than unauthorized access.

⸻

3. Primary Security Invariant

The following principle is foundational:

No intermediary MUST become an authority merely by observing, storing, forwarding, or relaying mesh traffic.

In particular:

* a rendezvous operator MUST NOT be able to create identity authority;
* a relay operator MUST NOT be able to create authorization;
* a reachability record MUST NOT grant access;
* knowledge of an endpoint MUST NOT imply identity;
* possession of a signed object MUST NOT by itself override the verifier’s trusted state;
* transport success MUST NOT imply application authorization.

⸻

4. Blast-Radius Model

The protocol should preserve a bounded blast radius for compromise.

Compromised component	Potential effect	Authority it MUST NOT gain
Rendezvous service	Discovery manipulation, suppression, metadata collection, availability disruption	Identity or authorization authority
Relay	Traffic disruption, timing/volume observation, metadata collection	Identity or application authorization
Reachability state	Stale or misleading endpoint information	Identity authority
Service record	Service discovery disruption	General authorization
Authorization key	Authority within its defined scope	Identity Root authority
Device key	Device impersonation within its authority	Principal Root authority
Service key	Service-level signing authority	Principal Root authority
Identity Root	Control of that principal’s identity authority	Authority over unrelated principals
Application	Use of capabilities granted to it	Arbitrary mesh authority

Implementations SHOULD preserve these boundaries even when individual components are compromised.

⸻

5. Cryptographic Object Security

Signed mesh objects provide the primary integrity mechanism.

Implementations MUST follow the canonical object-processing rules defined by the protocol and OBJECTS.md.

Security depends on:

* canonical CBOR;
* deterministic encoding;
* explicit domain separation;
* Ed25519 signatures;
* object commitments;
* payload identifiers;
* object identifiers;
* sequence numbers;
* stream-specific predecessor validation;
* chain hashes;
* explicit signing authority;
* schema validation.

The implementation MUST NOT substitute implementation-specific serialization, map ordering, parser behavior, or formatting for protocol-defined canonical encoding.

⸻

6. Sequence-Space Isolation

A sequence number has meaning only within its:

(issuer, stream_id)

sequence space.

Implementations MUST NOT compare sequence numbers from different sequence spaces.

In particular:

* an identity stream sequence MUST NOT be compared to an authorization stream sequence;
* a predecessor from another stream MUST NOT satisfy previous_hash;
* an authorization stream MUST NOT be advanced by an object from another authority’s stream;
* continuity references across identity generations MUST NOT be treated as ordinary same-stream sequence comparisons.

This prevents unrelated histories from being confused with one another.

⸻

7. Atomic Verification

Verification MUST be treated as a pure validation operation until all required checks succeed.

The verifier MUST NOT advance accepted stream state or otherwise mutate security state while performing validation steps.

The conceptual process is:

Receive
  ↓
Canonical decode
  ↓
Envelope validation
  ↓
Schema validation
  ↓
Sequence validation
  ↓
Predecessor validation
  ↓
Chain validation
  ↓
Signature validation
  ↓
Authority validation
  ↓
Semantic validation
  ↓
Commit accepted state

If any step fails, no security state transition occurs.

This protects against partial state advancement caused by malformed, forged, replayed, or semantically invalid objects.

⸻

8. Authorization Security

Authorization is valid only when all required conditions are satisfied.

Conceptually:

valid identity
AND
valid relationship/context
AND
valid grant
AND
valid lease
AND
no applicable revocation
AND
required freshness
=
ALLOW

Failure of any required condition results in denial or an explicitly non-authorized state.

In particular:

* identity alone does not authorize access;
* relationship alone does not authorize access;
* a grant without a valid lease does not authorize access;
* a stale lease does not authorize access;
* rendezvous discovery does not authorize access;
* relay possession does not authorize access.

⸻

9. Freshness and Replay Resistance

The protocol uses several mechanisms together to prevent stale authority from becoming current authority:

* sequence numbers;
* chained object state;
* leases;
* expiration;
* revocation;
* authenticated freshness;
* accepted local stream state.

A previously valid statement MUST NOT remain authoritative indefinitely merely because an attacker retained a copy.

Implementations SHOULD test at minimum:

* replay of expired leases;
* replay of revoked grants;
* replay of old reachability records;
* replay of superseded service records;
* replay after key rotation;
* rollback to an older stream sequence;
* insertion of an object into an unrelated stream;
* replay of previously terminated relationships.

⸻

10. Identity Continuity

Identity continuity is security-sensitive because a new cryptographic root cannot be trusted merely because it claims to replace an old one.

The v0.6.1 IdentityContinuity design requires evidence from both generations.

Acceptance requires, conceptually:

previous_root == trusted predecessor root
AND
previous_chain_hash == accepted predecessor terminal state
AND
new_root == successor stream authority
AND
previous signature valid
AND
new signature valid
AND
successor sequence == 1
AND
successor chain initialized correctly

The predecessor and successor streams remain separate sequence spaces.

A continuity statement MUST NOT allow an attacker to manufacture authority merely by presenting a validly signed but unrelated identity.

⸻

11. Relationship Security

Relationships are mutual recognition rather than unilateral global authority.

For a relationship to be recognized:

* each participating principal has an appropriate RelationshipAssertion;
* each assertion identifies the other principal;
* the shared relationship identifier matches;
* required validity conditions hold;
* no accepted termination applies.

One assertion alone represents a pending relationship rather than a fully recognized bilateral relationship.

Either participating principal can terminate the relationship according to the protocol’s termination rules.

⸻

12. Rendezvous Security

Rendezvous is deliberately non-authoritative infrastructure.

A malicious rendezvous operator may:

* return stale information;
* suppress legitimate information;
* return misleading reachability information;
* observe query patterns;
* correlate participants;
* refuse service;
* consume or discard stored state.

A rendezvous operator MUST NOT thereby gain the ability to:

* forge a principal;
* create a relationship;
* create an authorization;
* grant service access;
* redefine ownership;
* override accepted local security state.

Rendezvous data should be treated as discovery input, not as a trust anchor.

⸻

13. Relay Security

Relays are untrusted transport infrastructure.

The preferred security model is end-to-end protected communication:

A ───── encrypted traffic ───── Relay ───── encrypted traffic ───── B

The relay may enforce transport-resource constraints such as:

* RelayTicket validity;
* expiration;
* permitted source/destination;
* maximum bytes;
* maximum rate;
* session lifetime;
* concurrent-session limits.

A relay MUST NOT be able to manufacture application authorization.

A compromised relay should therefore primarily be capable of:

* dropping traffic;
* delaying traffic;
* refusing traffic;
* throttling traffic;
* observing permitted transport metadata.

It should not thereby obtain protected application contents or authorization authority.

⸻

14. Relay Capacity and Hardware

Relay capability should be treated separately from identity.

A Raspberry Pi, home server, VPS, bare-metal server, or large infrastructure provider can implement the same relay function at different capacities.

Relevant properties may include:

* maximum concurrent sessions;
* aggregate bandwidth;
* per-session bandwidth;
* maximum session duration;
* maximum bytes;
* IPv4/IPv6 capability;
* expected availability;
* latency;
* geographic/network characteristics.

Hardware identity is not itself a security property.

A relay should advertise or demonstrate capabilities, rather than requiring the protocol to classify hardware.

⸻

15. Resource Exhaustion and Admission Controls

The primary practical threat to public rendezvous and relay infrastructure is resource exhaustion.

Potential attacks include:

* excessive connection attempts;
* excessive object submission;
* excessive concurrent sessions;
* storage exhaustion;
* memory exhaustion;
* CPU exhaustion;
* bandwidth exhaustion;
* prolonged idle sessions;
* expensive handshake abuse;
* response amplification.

Preferred first-line defenses are:

* rate limits;
* connection limits;
* storage quotas;
* object-size limits;
* bounded response sizes;
* expiration;
* session timeouts;
* per-principal quotas;
* admission policy;
* resource accounting.

These mechanisms are generally preferable to introducing cryptographic cost where a simpler resource limit is sufficient.

⸻

16. Optional Computational Admission Cost

Computational cost may be used as an anti-abuse or admission mechanism where a concrete resource-exhaustion problem justifies it.

This is not an identity-authentication mechanism.

The purpose would be to make large-scale abuse consume a scarce resource:

Legitimate:
    create one identity/session
        ↓
    modest cost
Attacker:
    create millions of identities/sessions
        ↓
    millions of costs

However, computational admission cost MUST NOT be treated as the primary Sybil defense.

Before introducing such a mechanism, deployments should consider:

* rate limiting;
* connection caps;
* quotas;
* expiration;
* storage limits;
* authenticated admission;
* proof-of-possession;
* operator policy.

Computational cost has calibration and energy-consumption tradeoffs and may disproportionately affect low-power legitimate devices.

If used, its cost should be considered a deployment/admission parameter rather than an assumption that all mesh identities must satisfy.

⸻

17. Sybil Resistance

The core protocol does not require global Sybil resistance.

An identity is not inherently a vote, quota, reputation unit, or resource allocation.

Creating many identities therefore does not automatically provide:

* additional authorization;
* additional relationships;
* additional ownership;
* additional relay capacity;
* additional governance power.

This is intentional.

If a future system assigns scarce resources or authority based on identity count, that system MUST provide its own Sybil/admission mechanism.

The core mesh protocol SHOULD NOT introduce global consensus or identity scarcity merely to solve hypothetical higher-layer problems.

⸻

18. Metadata and Privacy Properties

The protocol provides strong confidentiality and authorization properties but does not provide anonymity of participation.

The following metadata may remain observable depending on transport and deployment:

Stable identity

Peer identifiers are intentionally stable and may be correlatable across contexts.

Rendezvous queries

A rendezvous operator may observe which participants query for which peers or services and when.

Relay traffic

A relay may observe:

* participating network endpoints;
* session timing;
* session duration;
* traffic volume;
* packet-level metadata available to the transport.

It does not necessarily learn protected application content.

On-path observers

Network observers may identify peers through transport-level information unless an additional privacy mechanism is used.

These properties are intentional consequences of stable identity and ordinary networking.

The protocol therefore claims:

Confidentiality of protected content and cryptographic authorization, not anonymity of participation.

Future multi-hop or onion-routed transports may provide stronger privacy without changing the underlying identity or authorization model.

⸻

19. Local Verifier Security State

A verifier’s local state is a security-critical asset.

It may include:

Verifier Security State
├── trusted anchors
├── accepted stream state
│   ├── sequence
│   └── chain hash
├── accepted objects
├── revocation state
├── freshness state
└── monotonic observation history

This state MUST be:

* durable across normal restarts;
* atomically updated;
* attributable to signed protocol objects;
* protected from unauthorized modification;
* recoverable through safe procedures.

The verifier MUST NOT reconstruct trusted state merely from arbitrary received objects after local security state has been lost.

⸻

20. Local State Loss

Local security-state loss is a security-relevant event, not merely an availability event.

If a verifier loses the state necessary to establish that a previously trusted stream is the accepted continuation of its history, the safe behavior is to return to an unknown/untrusted state for the affected authority.

The verifier MUST NOT silently reconstruct authority from untrusted observations.

Recovery should therefore result in one of:

* restoration of trusted local state;
* explicit re-pairing;
* explicit re-establishment of trust;
* another protocol-defined trusted recovery mechanism.

Failure to recover state MUST NOT grant or extend authority.

⸻

21. Failure Semantics

The following invariant is foundational:

Failure MUST NOT grant, extend, or change identity or authorization.

Examples:

* rendezvous failure does not alter identity;
* relay failure does not alter authorization;
* network failure does not extend a lease;
* clock failure does not create authority;
* reconciliation failure does not create capabilities;
* identity forks do not automatically create authority;
* missing revocation information does not automatically prove that an authorization remains valid;
* local state loss does not justify reconstruction from arbitrary observations.

Where current authority cannot be established, the safe result is denial or unknown state.

⸻

22. Endpoint and Key Compromise

The protocol cannot prevent compromise of a machine holding private keys.

If an attacker obtains an Identity Root key, the attacker may obtain the authority represented by that key until the key is revoked or otherwise superseded.

If a Device Key is compromised, the attacker may impersonate the affected device within that key’s authority.

If an Authorization Key is compromised, the attacker may exercise that authorization authority within its defined scope.

Therefore implementations SHOULD:

* minimize key scope;
* separate keys by authority;
* protect private keys at rest;
* support appropriate revocation;
* avoid unnecessary exposure of Identity Root keys;
* use hardware-backed or offline protection where appropriate for high-value deployments.

⸻

23. Application and Agent Security

Applications should interact with mesh connectivity through the local agent/API rather than receiving unnecessary cryptographic authority.

Preferred model:

Application
     │
     │ request authorized connection
     ▼
Mesh Agent
     │
     │ performs policy and connection work
     ▼
Mesh transport

Applications SHOULD receive the minimum capability necessary to perform their requested operation.

The agent SHOULD NOT expose:

* unnecessary private keys;
* unrestricted authorization capabilities;
* arbitrary relay credentials;
* unrestricted ability to create identities or grants.

The application-facing abstraction is therefore both an API simplification and a security boundary.

⸻

24. Parser and Implementation Security

Protocol implementations MUST treat untrusted encoded objects as hostile input.

Security testing SHOULD include:

* malformed CBOR;
* duplicate keys;
* noncanonical encoding;
* unsupported types;
* invalid UTF-8;
* invalid normalization;
* oversized arrays/maps;
* excessive nesting;
* oversized integers;
* truncated objects;
* invalid signatures;
* invalid chain hashes;
* invalid predecessor references;
* sequence rollback;
* fork conditions;
* expired objects;
* revoked objects;
* concurrent updates;
* crash/restart during state commit.

Implementations SHOULD impose bounded resource usage before performing expensive processing.

An object should not be able to cause unbounded memory allocation merely by declaring a large payload.

⸻

25. Anti-Amplification

Public protocol services should avoid turning small unauthenticated requests into disproportionately large responses.

Implementations SHOULD bound:

* response size;
* lookup results;
* object retrieval;
* pagination;
* unauthenticated work;
* reflection behavior.

This reduces the possibility that mesh infrastructure can be abused as a traffic amplifier.

⸻

26. Operational Security Boundary

Protocol security does not imply deployment security.

The protocol does not attempt to solve:

* compromise of the host operating system;
* theft of private keys from compromised hosts;
* insecure key storage;
* malicious software installed on a legitimate device;
* compromised agent binaries;
* malicious package repositories;
* compromised build infrastructure;
* software supply-chain attacks;
* compromised update mechanisms;
* social engineering of recovery procedures;
* insecure administrative practices.

These are deployment and operational security concerns.

Implementations and distributions SHOULD address them through appropriate measures such as:

* signed releases;
* reproducible or independently verifiable builds;
* package provenance;
* secure update mechanisms;
* protected key storage;
* encrypted storage;
* hardware-backed keys where appropriate;
* carefully designed recovery procedures;
* administrative separation.

These mechanisms should not redefine the protocol’s identity or authority model.

⸻

27. Recovery

Recovery is intentionally separate from the core V1 identity model.

Implementations MUST NOT silently weaken cryptographic authority to make recovery convenient.

In particular, a recovery procedure MUST NOT effectively become:

“Contact the service operator and ask them to reset the identity.”

unless that operator is explicitly part of the deployment’s chosen trust model.

Recovery mechanisms should be treated as additional authority systems and evaluated separately.

⸻

28. Consensus and Bitcoin-Inspired Principles

The protocol may borrow useful principles from systems such as Bitcoin without adopting blockchain architecture.

Useful principles include:

* independently verifiable state;
* cryptographic commitments;
* explicit deterministic rules;
* resistance to unilateral database rewriting;
* treating scarce resources as scarce;
* assuming adversarial participants;
* making certain classes of abuse economically costly where appropriate.

The protocol does not require:

* a global blockchain;
* mining;
* global proof-of-work;
* global transaction ordering;
* a global consensus protocol;
* tokens;
* a global ledger.

The mesh problem is primarily one of local cryptographic trust and authorization, not global agreement over a single universal history.

⸻

29. Threat Categories and Expected Outcome

The principal threat categories are:

Forgery

Expected result: cryptographic rejection.

Replay

Expected result: expiration, sequence, freshness, or revocation rejection.

Stream tampering

Expected result: predecessor/chain validation failure.

Malicious rendezvous

Expected result: discovery failure or metadata exposure, not unauthorized access.

Malicious relay

Expected result: availability degradation or metadata exposure, not unauthorized access or plaintext disclosure.

Sybil identities

Expected result: little direct effect unless a higher-level system incorrectly treats identity quantity as authority.

Resource exhaustion

Expected result: bounded by rate limits, quotas, expiration, admission controls, and deployment-level infrastructure protections.

Endpoint compromise

Expected result: outside the cryptographic protocol’s protection boundary.

Local state loss

Expected result: unknown/untrusted state until trusted state is restored or trust is re-established.

Implementation defect

Expected result: addressed through conformance tests, fuzzing, differential testing, crash/restart testing, and security review.

⸻

30. Security Review Rule

Before introducing a security mechanism, reviewers SHOULD be able to state all three:

1. What authority or resource does it protect?
2. What specific attack does it prevent or mitigate?
3. What is the failure mode if the mechanism is absent?

If any of these cannot be clearly identified, the mechanism should be considered premature.

This rule exists to prevent security-feature accumulation without a defined security boundary.

⸻

31. Recommended Security Test Program

Implementation should progress through increasingly realistic security tests.

Cryptographic tests

* canonical encoding vectors;
* signature vectors;
* commitment vectors;
* chain vectors;
* object-ID vectors;
* dual-signature vectors;
* invalid signature tests.

State-machine tests

* sequence advancement;
* rollback;
* forks;
* termination;
* revocation;
* key rotation;
* identity continuity;
* local state loss;
* crash during commit.

Adversarial parsing

* malformed CBOR;
* duplicate fields;
* oversized fields;
* invalid types;
* truncation;
* deeply nested data.

Authorization tests

* missing grant;
* expired grant;
* missing lease;
* expired lease;
* revoked grant;
* stale freshness;
* wrong relationship;
* wrong device;
* wrong service;
* wrong stream.

Infrastructure tests

* malicious rendezvous;
* stale rendezvous;
* malicious relay;
* relay disappearance;
* direct-path failure;
* relay fallback;
* replayed reachability;
* coordinator flooding;
* relay resource exhaustion.

Persistence tests

* restart;
* power loss;
* interrupted commit;
* corrupted local state;
* restored backup;
* missing state;
* recovery.

The first normative cryptographic test vector should remain the simple sequence-1 single-signature object already planned for the v0.6.1 implementation process.

⸻

32. Security Roadmap

The following items should be treated as implementation and review priorities rather than automatic additions to the protocol kernel:

1. Canonical encoding verification.
2. Signature and commitment verification.
3. Stream-state integrity.
4. Atomic state transitions.
5. Identity/key hierarchy.
6. Relationship verification.
7. Authorization evaluation.
8. Freshness and revocation.
9. Identity continuity.
10. Direct transport security.
11. Relay/rendezvous authority separation.
12. Bounded resource consumption.
13. Object and message size limits.
14. Session and connection limits.
15. Expiration and garbage collection.
16. Anti-amplification controls.
17. Optional computational admission mechanisms where justified.
18. Key-compromise handling.
19. Metadata/privacy analysis.
20. Parser fuzzing.
21. Concurrency and race testing.
22. Crash/restart testing.
23. Persistent-state security testing.
24. Normative security test vectors.
25. Normative requirements for local security-state durability and safe recovery.
26. Explicit operational-security boundary and deployment guidance.

⸻

33. Security Design Principle

The protocol should remain intentionally small.

Security mechanisms should be added when they protect a concrete:

* authority boundary;
* resource;
* trust relationship;
* state transition;
* confidentiality property;
* integrity property;
* availability boundary.

The project should avoid adding mechanisms merely because an attack is theoretically conceivable.

The preferred question is not:

“Can we add another security mechanism?”

It is:

“What specific boundary are we protecting, what attack crosses that boundary, and what happens if the protection is absent?”

⸻

34. Final Security Position

The Mesh protocol’s security does not depend on any single component being universally trustworthy.

Instead:

Identity establishes who controls a cryptographic authority. Authorization establishes what that authority may do. Local state establishes what the verifier currently accepts. Freshness establishes whether that authority remains current. Transport establishes how authorized parties communicate. Rendezvous and relay infrastructure remain replaceable and untrusted.

This produces a system in which compromise of an intermediary should normally affect availability or metadata, rather than automatically becoming a compromise of identity or authorization.

The principal security objective is therefore not to make every component trustworthy.

It is to make trust unnecessary outside the boundaries where it is explicitly established.

That is the security property that should be preserved as the implementation evolves beyond v0.6.1.
