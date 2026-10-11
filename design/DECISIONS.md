# Design Decisions

Significant design choices, their alternatives, and rationale.

---

## 1. Scope Refinements

### 1.1 Removed: Global DHT for Coordinator Discovery
**Decision:** Do not include a global DHT for coordinator discovery in V1.
**Alternatives considered:** Kademlia-based DHT, Mainline DHT, custom DHT.
**Rationale:** DHTs introduce complexity, Sybil vulnerability, and operational burden. V1 relies on signed coordinator manifests with explicit federation. DHT can be added as a V2 extension without changing the core object model.

### 1.2 Removed: Mandatory Homeserver/Coordinator Model
**Decision:** No single coordinator is required. Coordinators are replaceable infrastructure.
**Alternatives considered:** Matrix-style homeserver model, mandatory coordinator per identity.
**Rationale:** Single coordinator creates availability dependency and concentration of power. Replaceable coordinators enable graceful degradation.

### 1.3 Removed: XOR Obfuscation for Reachability Records
**Decision:** Use authenticated encryption (COSE/HPKE) instead of XOR with shared key.
**Alternatives considered:** XOR with QR-shared key, plaintext records.
**Rationale:** XOR provides no meaningful confidentiality (key shared with all QR recipients), cannot provide independent revocation, and is not standard cryptographic practice.

### 1.4 Removed: Unrestricted Global Gossip
**Decision:** Bounded anti-entropy only. No recursive uncontrolled fan-out.
**Alternatives considered:** Full gossip protocol, epidemic broadcast.
**Rationale:** Unrestricted gossip scales poorly and creates unbounded resource consumption. Bounded replication with explicit quotas achieves resilience without resource exhaustion.

### 1.5 Narrowed: Identity Continuity to V1
**Decision:** IdentityContinuity requires dual signatures from both roots.
**Alternatives considered:** Single-root rotation, threshold-based rotation, social recovery only.
**Rationale:** Dual signatures provide cryptographic proof of both parties' consent. Threshold and social recovery deferred to V2.

---

## 2. License Choice: GPL v3

**Decision:** Use GPL v3 (not v2, not AGPL, not Apache/MIT).
**Rationale:**
- Patent clarity: GPL v3 makes patent grant explicit (critical for cryptographic protocols).
- Anti-tivoization: Prevents hardware lockdown of modified software (important for decentralized identity).
One core rule: if code from this project is used, modifications must be shared.
- Not AGPL: Complexity of "running a service" definition, Linus's principle (simple licenses are clearer), pragmatic (spec implementations not covered anyway).
- Not Apache: "Anyone can do anything" vs GPL "community benefits from improvements."

---

## 3. Failure Mode Treatments (from FAILURE_MODES.md analysis)

### 3.1 Revocation Effect on Active Sessions
**Decision:** Revocation does NOT terminate active sessions immediately. Sessions continue until next authorization check.
**Rationale:** Immediate termination requires in-band signaling that adds complexity and state. Leases already bound access to short windows. Revocation prevents future leases.
**Documented in:** PROTOCOL.md authorization semantics.

### 3.2 Identity Root Compromise — No In-Band Recovery
**Decision:** V1 has no in-band recovery for Identity Root compromise.
**Rationale:** Any in-band recovery mechanism would be an authority the protocol cannot trust. Recovery is out-of-band through trusted channels.
**Documented in:** SECURITY.md §5, THREAT-MODEL.md.

### 3.3 Published_At Timestamp on Reachability Records
**Decision:** Reachability records carry a `published_at` timestamp (not just expiry).
**Rationale:** Enables gossip/federation to order records correctly. Required for V2 federation.
**Documented in:** PROTOCOL.md reachability record schema, OBJECTS.md.

### 3.4 Explicit IdentityContinuity Bootstrap Rules
**Decision:** Verifiers MAY bootstrap trust from any IdentityContinuity object whose `previous_root` is already trusted, without full chain download.
**Rationale:** Enables history compression. New verifiers don't need full identity chain.
**Documented in:** PROTOCOL.md identity continuity section.

---

## 4. Pairing Model Decisions

### 4.1 Three-Phase Pairing (Human Coord → Auth → Tunnel)
**Decision:** Decouple human coordination window (5-10 min) from tunnel establishment (open-ended).
**Rationale:** Prevents slow NAT traversal from breaking pairing. Code consumed in Phase 2; tunnel retries in Phase 3.
**Source:** PAKE_DISCUSSION.md, FAILURE_MODES.md §1.

### 4.2 Server-Side Confirmation (Allow/Deny Prompt)
**Decision:** Receiving side displays confirmation prompt with peer identity label.
**Rationale:** Human verification step complements PAKE. Prevents silent pairing by attacker who observed code.
**Source:** PAKE_DISCUSSION.md, FAILURE_MODES.md §1.3.

### 4.3 QR Code Contains Ephemeral Secret Only
**Decision:** QR code contains temporary pairing secret, not long-lived credential.
**Rationale:** Prevents QR code reuse, photography, logging. Secret consumed on first successful pairing.
**Source:** PAKE_DISCUSSION.md, FAILURE_MODES.md §1.4.

---

## 5. Relay Architecture Decisions

### 5.1 Relay Forwards Encrypted Traffic Only
**Decision:** Relay never terminates end-to-end encryption. Sees only ciphertext.
**Rationale:** Keeps relay untrusted. Malicious relay can drop/delay but not read/modify content.
**Source:** RELAY_DISCUSSION.md, RELAY_OPTIMIZATION.md, THREAT-MODEL.md.

### 5.2 Capability Advertisement, Not Hardware Classification
**Decision:** Relays advertise capabilities (bandwidth, sessions, latency), not hardware type.
**Rationale:** Hardware-independent protocol. Raspberry Pi and bare-metal server implement same protocol.
**Source:** RELAY_OPTIMIZATION.md, ROUTER_CONTRIBUTION.md.

### 5.3 Direct-First Connectivity Preference
**Decision:** Preference order: LAN → Direct IPv6 → Direct IPv4 → NAT traversal → Relay.
**Rationale:** Relay is fallback, not default. Minimizes relay bandwidth costs.
**Source:** CONNECTIVITY.md, COMMERCIAL.md.

---

## 6. Commercial Model Decisions

### 6.1 Commercial Layer Sells Guarantees, Not Access
**Decision:** Free tier always works (best-effort). Paid tier gets priority/predictability.
**Rationale:** Free users are the network's foundation (reachability publication, P2P connections). Commercial layer expands network rather than partitioning it.
**Source:** COMMERCIAL.md, ../commercial/MODEL.md.

### 6.2 Credit System: Contribution Earns Priority
**Decision:** Users running relays earn credits for capacity contributed. Credits spendable on priority.
**Rationale:** Creates contribution economy. Family pool model for shared resources. Operator-agnostic credits via exchange rates.
**Source:** COMMERCIAL.md, RELAY_ECONOMICS.md.

### 6.3 Geographic Scarcity Multiplier
**Decision:** Relays in underserved regions earn more credits per byte.
**Rationale:** Encourages infrastructure where it's most needed. Market incentive for geographic diversity.
**Source:** COMMERCIAL.md, RELAY_ECONOMICS.md.

---

## 7. Naming Decisions

**Decision:** Final name is Grid Network. Domain separators use `grid/`. URIs use `grid://`.
The name "Grid Network" was chosen because "Mesh" collides with existing libraries and "NotDNS" is defined by negation.
**Source:** Project history in README.md.

---

*End of Design Decisions*
