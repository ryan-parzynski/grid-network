# Threat Model

Security properties and non-properties of Grid Network v0.6.2.

---

## 1. Adversary Model

### 1.1 Adversaries We Protect Against

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

### 1.2 What We Do NOT Protect Against

- **Anonymity** — Grid Network is not an anonymity network. Peers are identified. Rendezvous can observe who is talking to whom.
- **Global surveillance** — Network observer can see all reachability hints. Content is protected by transport encryption.
- **Quantum computers** — Ed25519 is vulnerable to quantum attacks. Migration to post-quantum crypto when needed.
- **Root compromise** — If device OS is compromised, all security is lost. Grid Network cannot protect against that.
- **Timezone bugs** — Verifier with wrong clock may incorrectly verify time-based proofs. Out-of-band clock sync is operator's responsibility.

---

## 2. Blast Radius

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

## 3. Failure Semantics (F1–F6 Taxonomy)

### F1: Authorization Failure → Deny
Missing grant, expired lease, revocation applied → Connection denied. System is fail-closed. Missing information never grants access.

### F2: Reachability Failure → Try Alternatives
Rendezvous unreachable, endpoint stale, direct connection fails → Try relay. System is availability-preserving. One infrastructure failure doesn't break existing relationships.

### F3: Clock Skew → Relative Validity Survives
Verifier's clock 1 hour behind issuer's → Relative lease still works. Absolute timestamps would fail. Grid Network uses relative by default.

### F4: Communication Interruption → Cache and Continue
Verifier offline, receives revocation later → Revocation cached, applied when object arrives. No silent state change.

### F5: Fork Detection → Require Resolution
Stream has two objects at same sequence → Fork detected. Requires explicit StreamResolution object. No silent choice.

### F6: Key Compromise → Effective_Sequence Limits Damage
Key compromised, retroactive revocation issued → Objects before effective_sequence remain valid. Damage is limited to forward time.

---

## 4. Security Principles

1. **No authority creates identity** — Identity is self-attested. Peer publishes identity document signed by their own Identity Root. Rendezvous is not authority.
2. **All authorization is local** — Verifier evaluates grants/leases using locally held state. No "call home" required. Offline operation works.
3. **Revocation is terminal** — Once revoked, object cannot become valid again. Prevents subtle bugs from temporary revocation semantics.
4. **Reachability is untrusted** — Reachability records are hints, not ground truth. Any can be stale or malicious. Verifier tries multiple endpoints.
5. **Infrastructure is replaceable** — Every infrastructure component (rendezvous, relay) can be swapped. Peer ID, relationships, and authorizations survive the change.
6. **Layering is strict** — Network authorization (Grid Network) and application authorization (app) are separate. Neither can violate the other.

---

## 5. Compromise Response Procedures

### If Authorization Key is Compromised:
1. Principal publishes key revocation in identity stream
2. Specifies effective_sequence (marks which objects are affected)
3. All future objects signed by that key are invalid
4. Existing leases remain valid until expiry
5. New Authorization Key provisioned
6. New leases issued by new key
**Time to recovery:** Minutes (revocation must propagate via rendezvous)

### If Device Key is Compromised:
1. Principal publishes key revocation
2. Device is now untrusted (can't sign reachability)
3. Remove device from device_bindings in identity document
4. Device is offline
5. User physically removes old device from network
**Time to recovery:** Hours (device physically removed)

### If Identity Root is Compromised:
**NO IN-BAND RECOVERY** (v0.6.2 limitation)

Out-of-band options:
1. Principal contacts other peers who know them
2. Provides proof of ownership (social recovery)
3. Other peers issue new relationship assertions
4. Principal re-establishes network relationships

This is a fundamental limitation of v0.6.2. V2 may add threshold recovery.

---

## 6. Implementation Requirements

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

## 7. Attack Scenarios and Mitigations

### Scenario 1: MITM on Pairing
- Attacker intercepts QR code
- Attacker follows pairing flow, claims to be Bob
- **Mitigation:** PAKE requires shared secret (QR code). Attacker doesn't have it.
- **Result:** Pairing fails, attacker cannot impersonate Bob

### Scenario 2: Replay Attack
- Attacker captures grant message
- Attacker replays it months later
- **Mitigation:** Grant has timestamp, lease has expiry. Replayed old lease is invalid.
- **Result:** Attacker cannot gain access with old lease

### Scenario 3: Sybil Attack
- Attacker creates 1000 fake peer IDs
- Attacker floods network with garbage
- **Mitigation:** Grid Network does not prevent Sybil. But relays enforce rate limits. Rendezvous enforces query limits. Cost scales with attack size.
- **Result:** Attacker can create fake peers but cannot flood infrastructure without paying for resources

### Scenario 4: Relay Intercepts Traffic
- Attacker runs a relay
- Attacker tries to decrypt forwarded traffic
- **Mitigation:** Content is encrypted by transport layer (WireGuard). Relay only sees ciphertext.
- **Result:** Attacker sees packet size and count, not content

### Scenario 5: Rendezvous Gives False Reachability
- Attacker runs a rendezvous
- Attacker claims peer is at 192.0.2.1
- **Mitigation:** Verifier treats reachability as untrusted. Tries endpoint. If connection fails, tries others.
- **Result:** Attacker can delay connections but cannot MITM (no key)

### Scenario 6: Grant Forgery
- Attacker tries to forge grant
- **Mitigation:** Grant is signed by issuer's Authorization Key. Attacker doesn't have the key.
- **Result:** Forged grant fails signature verification

---

## 8. Metadata and Privacy Properties

Grid Network provides strong confidentiality and authorization properties but does not provide anonymity of participation.

The following metadata may remain observable depending on transport and deployment:

**Stable identity:** Peer identifiers are intentionally stable and may be correlatable across contexts.

**Rendezvous queries:** A rendezvous operator may observe which participants query for which peers or services and when.

**Relay traffic:** A relay may observe participating network endpoints, session timing, session duration, traffic volume, packet-level metadata available to the transport. It does not necessarily learn protected application content.

**On-path observers:** Network observers may identify peers through transport-level information unless an additional privacy mechanism is used.

These properties are intentional consequences of stable identity and ordinary networking.

**The protocol claims:** Confidentiality of protected content and cryptographic authorization, not anonymity of participation.

Future multi-hop or onion-routed transports may provide stronger privacy without changing the underlying identity or authorization model.

---

## 9. Local Verifier Security State

A verifier's local state is a security-critical asset. It may include:
- Trusted anchors
- Accepted stream state (sequence, chain hash)
- Accepted objects
- Revocation state
- Freshness state
- Monotonic observation history

This state MUST be:
- Durable across normal restarts
- Atomically updated
- Attributable to signed protocol objects
- Protected from unauthorized modification
- Recoverable through safe procedures

The verifier MUST NOT reconstruct trusted state merely from arbitrary received objects after local security state has been lost.

---

## 10. Local State Loss

Local security-state loss is a security-relevant event, not merely an availability event.

If a verifier loses the state necessary to establish that a previously trusted stream is the accepted continuation of its history, the safe behavior is to return to an unknown/untrusted state for the affected authority.

The verifier MUST NOT silently reconstruct authority from untrusted observations.

Recovery should therefore result in one of:
- Restoration of trusted local state
- Explicit re-pairing
- Explicit re-establishment of trust
- Another protocol-defined trusted recovery mechanism

Failure to recover state MUST NOT grant or extend authority.

---

## 11. Failure Semantics (Foundational Invariant)

The following invariant is foundational:

**Failure MUST NOT grant, extend, or change identity or authorization.**

Examples:
- Rendezvous failure does not alter identity
- Relay failure does not alter authorization
- Network failure does not extend a lease
- Clock failure does not create authority
- Reconciliation failure does not create capabilities
- Identity forks do not automatically create authority
- Missing revocation information does not automatically prove that an authorization remains valid
- Local state loss does not justify reconstruction from arbitrary observations

Where current authority cannot be established, the safe result is denial or unknown state.

---

## 12. Endpoint and Key Compromise

The protocol cannot prevent compromise of a machine holding private keys.

If an attacker obtains an Identity Root key, the attacker may obtain the authority represented by that key until the key is revoked or otherwise superseded.

If a Device Key is compromised, the attacker may impersonate the affected device within that key's authority.

If an Authorization Key is compromised, the attacker may exercise that authorization authority within its defined scope.

Therefore implementations SHOULD:
- Minimize key scope
- Separate keys by authority
- Protect private keys at rest
- Support appropriate revocation
- Avoid unnecessary exposure of Identity Root keys
- Use hardware-backed or offline protection where appropriate for high-value deployments

---

## 13. Application and Agent Security

Applications should interact with Grid Network connectivity through the local agent/API rather than receiving unnecessary cryptographic authority.

Preferred model:
```
Application
     │
     │ request authorized connection
     ▼
Grid Network Agent
     │
     │ performs policy and connection work
     ▼
Grid Network transport
```

Applications SHOULD receive the minimum capability necessary to perform their requested operation.

The agent SHOULD NOT expose:
- Unnecessary private keys
- Unrestricted authorization capabilities
- Arbitrary relay credentials
- Unrestricted ability to create identities or grants

The application-facing abstraction is therefore both an API simplification and a security boundary.

---

## 14. Parser and Implementation Security

Protocol implementations MUST treat untrusted encoded objects as hostile input.

Security testing SHOULD include:
- Malformed CBOR
- Duplicate keys
- Noncanonical encoding
- Unsupported types
- Invalid UTF-8
- Invalid normalization
- Oversized arrays/maps
- Excessive nesting
- Oversized integers
- Truncated objects
- Invalid signatures
- Invalid chain hashes
- Invalid predecessor references
- Sequence rollback
- Fork conditions
- Expired objects
- Revoked objects
- Concurrent updates
- Crash/restart during state commit

Implementations SHOULD impose bounded resource usage before performing expensive processing. An object should not be able to cause unbounded memory allocation merely by declaring a large payload.

---

## 15. Anti-Amplification

Public protocol services should avoid turning small unauthenticated requests into disproportionately large responses.

Implementations SHOULD bound:
- Response size
- Lookup results
- Object retrieval
- Pagination
- Unauthenticated work
- Reflection behavior

This reduces the possibility that Grid Network infrastructure can be abused as a traffic amplifier.

---

## 16. Operational Security Boundary

Protocol security does not imply deployment security.

The protocol does not attempt to solve:
- Compromise of the host operating system
- Theft of private keys from compromised hosts
- Insecure key storage
- Malicious software installed on a legitimate device
- Compromised agent binaries
- Malicious package repositories
- Compromised build infrastructure
- Software supply-chain attacks
- Compromised update mechanisms
- Social engineering of recovery procedures
- Insecure administrative practices

These are deployment and operational security concerns.

Implementations and distributions SHOULD address them through appropriate measures such as:
- Signed releases
- Reproducible or independently verifiable builds
- Package provenance
- Secure update mechanisms
- Protected key storage
- Encrypted storage
- Hardware-backed keys where appropriate
- Carefully designed recovery procedures
- Administrative separation

These mechanisms should not redefine the protocol's identity or authority model.

---

## 17. Recovery

Recovery is intentionally separate from the core V1 identity model.

Implementations MUST NOT silently weaken cryptographic authority to make recovery convenient.

In particular, a recovery procedure MUST NOT effectively become:
"Contact the service operator and ask them to reset the identity."

unless that operator is explicitly part of the deployment's chosen trust model.

Recovery mechanisms should be treated as additional authority systems and evaluated separately.

---

## 18. Consensus and Bitcoin-Inspired Principles

The protocol may borrow useful principles from systems such as Bitcoin without adopting blockchain architecture.

Useful principles include:
- Independently verifiable state
- Cryptographic commitments
- Explicit deterministic rules
- Resistance to unilateral database rewriting
- Treating scarce resources as scarce
- Assuming adversarial participants
- Making certain classes of abuse economically costly where appropriate

The protocol does not require:
- A global blockchain
- Mining
- Global proof-of-work
- Global transaction ordering
- A global consensus protocol
- Tokens
- A global ledger

The Grid Network problem is primarily one of local cryptographic trust and authorization, not global agreement over a single universal history.

---

## 19. Threat Categories and Expected Outcome

| Threat Category | Expected Outcome |
|-----------------|------------------|
| Forgery | Cryptographic rejection |
| Replay | Expiration, sequence, freshness, or revocation rejection |
| Stream tampering | Predecessor/chain validation failure |
| Malicious rendezvous | Discovery failure or metadata exposure, not unauthorized access |
| Malicious relay | Availability degradation or metadata exposure, not unauthorized access or plaintext disclosure |
| Sybil identities | Little direct effect unless a higher-level system incorrectly treats identity quantity as authority |
| Resource exhaustion | Bounded by rate limits, quotas, expiration, admission controls, and deployment-level infrastructure protections |
| Endpoint compromise | Outside the cryptographic protocol's protection boundary |
| Local state loss | Unknown/untrusted state until trusted state is restored or trust is re-established |
| Implementation defect | Addressed through conformance tests, fuzzing, differential testing, crash/restart testing, and security review |

---

## 20. Security Review Rule

Before introducing a security mechanism, reviewers SHOULD be able to state all three:

1. What authority or resource does it protect?
2. What specific attack does it prevent or mitigate?
3. What is the failure mode if the mechanism is absent?

If any of these cannot be clearly identified, the mechanism should be considered premature.

This rule exists to prevent security-feature accumulation without a defined security boundary.

---

## 21. Recommended Security Test Program

Implementation should progress through increasingly realistic security tests.

**Cryptographic tests:**
- Canonical encoding vectors
- Signature vectors
- Commitment vectors
- Chain vectors
- Object-ID vectors
- Dual-signature vectors
- Invalid signature tests

**State-machine tests:**
- Sequence advancement
- Rollback
- Forks
- Termination
- Revocation
- Key rotation
- Identity continuity
- Local state loss
- Crash during commit

**Adversarial parsing:**
- Malformed CBOR
- Duplicate fields
- Oversized fields
- Invalid types
- Truncation
- Deeply nested data

**Authorization tests:**
- Missing grant
- Expired grant
- Missing lease
- Expired lease
- Revoked grant
- Stale freshness
- Wrong relationship
- Wrong device
- Wrong service
- Wrong stream

**Infrastructure tests:**
- Malicious rendezvous
- Stale rendezvous
- Malicious relay
- Relay disappearance
- Direct-path failure
- Relay fallback
- Replayed reachability
- Coordinator flooding
- Relay resource exhaustion

**Persistence tests:**
- Restart
- Power loss
- Interrupted commit
- Corrupted local state
- Restored backup
- Missing state
- Recovery

The first normative cryptographic test vector should remain the simple sequence-1 single-signature object already planned for the v0.6.2 implementation process.

---

## 22. Security Roadmap

The following items should be treated as implementation and review priorities rather than automatic additions to the protocol kernel:

1. Canonical encoding verification
2. Signature and commitment verification
3. Stream-state integrity
4. Atomic state transitions
5. Identity/key hierarchy
6. Relationship verification
7. Authorization evaluation
8. Freshness and revocation
9. Identity continuity
10. Direct transport security
11. Relay/rendezvous authority separation
12. Bounded resource consumption
13. Object and message size limits
14. Session and connection limits
15. Expiration and garbage collection
16. Anti-amplification controls
17. Optional computational admission mechanisms where justified
18. Key-compromise handling
19. Metadata/privacy analysis
20. Parser fuzzing
21. Concurrency and race testing
22. Crash/restart testing
23. Persistent-state security testing
24. Normative security test vectors
25. Normative requirements for local security-state durability and safe recovery
26. Explicit operational-security boundary and deployment guidance

---

## 23. Security Design Principle

The protocol should remain intentionally small.

Security mechanisms should be added when they protect a concrete:
- Authority boundary
- Resource
- Trust relationship
- State transition
- Confidentiality property
- Integrity property
- Availability boundary

The project should avoid adding mechanisms merely because an attack is theoretically conceivable.

The preferred question is not:

"Can we add another security mechanism?"

It is:

"What specific boundary are we protecting, what attack crosses that boundary, and what happens if the protection is absent?"

---

## 24. Final Security Position

Grid Network's security does not depend on any single component being universally trustworthy.

Instead:
- Identity establishes who controls a cryptographic authority
- Authorization establishes what that authority may do
- Local state establishes what the verifier currently accepts
- Freshness establishes whether that authority remains current
- Transport establishes how authorized parties communicate
- Rendezvous and relay infrastructure remain replaceable and untrusted

This produces a system in which compromise of an intermediary should normally affect availability or metadata, rather than automatically becoming a compromise of identity or authorization.

The principal security objective is therefore not to make every component trustworthy.

It is to make trust unnecessary outside the boundaries where it is explicitly established.

That is the security property that should be preserved as the implementation evolves beyond v0.6.2.
