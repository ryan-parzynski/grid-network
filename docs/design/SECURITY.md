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
