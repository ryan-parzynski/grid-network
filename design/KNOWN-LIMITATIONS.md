# Known Limitations

This document identifies design limitations that are inherent to the Grid Network protocol's architecture and cannot be fixed by adding mechanisms. Each limitation is named, explained, and accompanied by its mitigation and boundary.

---

## 1. Stale Anchor / Identity State Distribution Gap

### The Limitation

Two peers who have not communicated in an extended period may not be able to verify each other's current identity state.

**The scenario:** Alice and Bob established a relationship six months ago. Since then, Alice has rotated her device keys (or her identity root). Bob has been offline or has not communicated with Alice. Bob's cached copy of Alice's identity document is stale. Bob has no way to obtain Alice's current identity document or the continuity chain from his anchor to her current state without communicating with Alice — which requires reaching her, which requires her current reachability record, which requires knowing her current authorized device keys.

This is a circular dependency:
- To reach Alice → Bob needs Alice's current reachability record
- To verify the record → Bob needs Alice's current authorized device keys
- To get those → Bob needs Alice's current identity document (or continuity chain)
- To get that → Bob needs to communicate with Alice
- To communicate → Bob needs to reach her

### Why No Protocol Mechanism Can Fix This

The protocol assumes identity state propagates through peer-to-peer contact. When two peers are disconnected, there is no communication path. A protocol mechanism cannot create a path where none exists.

Adding a global state distribution layer (DHT, gossip, blockchain) would:
- Change the trust model (introduce new authorities)
- Add enormous complexity
- Not solve the fundamental problem: if a peer is offline, no protocol can reach it

### Mitigation

1. **Rendezvous serves identity state** (adopted in PROTOCOL.md §30.6): Rendezvous servers accept and serve identity documents and `IdentityContinuity` objects. This provides a centralized but untrusted cache of identity state.

2. **Reachability freshness fields** (adopted in PROTOCOL.md §32.2): `published_at` and `identity_sequence` on reachability records allow a verifier to detect stale state and know when to refresh.

3. **Out-of-band contact**: If neither peer has been online and neither has out-of-band contact, the relationship cannot be revived. This is the boundary.

### Boundary

The protocol guarantees that **if a peer can reach the rendezvous, it can obtain current identity state**. It does **not** guarantee that a peer can reach the rendezvous. If both peers are offline, or neither can reach any rendezvous, the relationship is suspended until one party comes online or out-of-band contact is made.

---

## 2. Split-Brain Identity

### The Limitation

If an identity root is compromised and the attacker publishes a competing identity document, the protocol cannot distinguish the legitimate root transition from the attacker's transition without out-of-band information.

**Why no mechanism can fix this:** No cryptographic mechanism can distinguish "legitimate root rotation" from "attacker-driven root transition" based solely on the signed objects. Both are correctly signed by their respective roots.

### Mitigation

- `IdentityContinuity` dual-signature requirement makes orderly transitions verifiable
- Out-of-band recovery for unplanned transitions (PROTOCOL.md §54.10)
- The verifier's accepted state before the fork is preserved (PROTOCOL.md §54.5.7)

### Boundary

The protocol guarantees that **an orderly root transition is verifiable and auditable**. It does **not** guarantee that a disputed transition can be resolved in-band without prior trust anchor.

---

## 3. Metadata Leakage in Discovery

### The Limitation

Rendezvous servers observe which peers are looking for which other peers, and when. This is inherent to any rendezvous-based discovery system.

**Why no mechanism can fix this:** To discover a peer, you must ask a rendezvous server. The server learns the query pattern. Using multiple rendezvous servers distributes but does not eliminate the leakage. Private Information Retrieval (PIR) or DHT-based discovery would add enormous complexity and still leak metadata at some level.

### Mitigation

- Opaque Peer IDs prevent the rendezvous from linking queries to human identities
- Multiple rendezvous providers allow distribution of trust
- Future: DHT-based discovery (§31 V5) if required

### Boundary

The protocol guarantees that **the rendezvous cannot forge identity, authorization, or revocation**. It does **not** guarantee that the rendezvous cannot observe *who is looking for whom*.

---

## 4. No Availability Guarantee

### The Limitation

The protocol does not guarantee that peers can reach each other. It guarantees that **if** a connection is established, **then** it is authenticated and authorized.

**Why no mechanism can fix this:** Availability depends on network conditions (NAT, firewalls, CGNAT, relay capacity, rendezvous uptime, ISP blocking) that are outside the protocol's control. No cryptographic protocol can force the internet to deliver packets.

### Mitigation

- Relay fallback (§33)
- Multiple rendezvous providers (§31 V2+)
- Direct-first connectivity (§53.11: availability-preserving for connectivity)

### Boundary

The protocol guarantees **authorization correctness** (fail-closed). It does **not** guarantee **availability** (fail-open for connectivity).

---

## 5. PAKE Algorithm Unspecified in V1

### The Limitation

The pairing protocol requires an established PAKE (SPAKE2 or CPace) but does not mandate a single algorithm in V1.

**Why this matters:** Interoperability between implementations requires agreement on the exact PAKE, transcript construction, and identity binding.

### Mitigation

- Documented as a schema gap to be filled in OBJECTS.md §6
- PAKE must be specified before wire protocol (Offer 1)

### Boundary

This is a **schema gap** (fixable), not a design limitation. It will be resolved before V1 release.

---

## 6. Relay Key Rotation Requires OperatorManifest Update

### The Limitation

If the Relay Authority Key is rotated, all relay tickets issued under the old key become invalid unless the OperatorManifest is updated.

**Why this matters:** A coordinator who loses the Relay Authority Key cannot issue new tickets until the OperatorManifest is updated with the new key.

### Mitigation

- `current_relay_authority_key` field added to OperatorManifest (PROTOCOL.md §30.3)
- Relay Authority Key rotation is an operator-level operation

### Boundary

This is an operational consideration, not a protocol failure mode. It is documented and the mechanism exists.

---

## Summary Table

| Limitation | Type | Fixable? | Mitigation |
|------------|------|----------|------------|
| Stale Anchor / State Distribution | Design limitation | No | Rendezvous identity state + freshness fields + out-of-band |
| Split-Brain Identity | Design limitation | No | IdentityContinuity dual-sig + out-of-band recovery |
| Metadata Leakage | Design limitation | Partially | Opaque IDs, multiple rendezvous, future DHT |
| No Availability Guarantee | Design limitation | No | Relays, multiple rendezvous, availability-preserving connectivity |
| PAKE Algorithm | Schema gap | Yes | To be specified in OBJECTS.md |
| Relay Key Rotation | Operational | Yes | OperatorManifest `current_relay_authority_key` |

---

## How to Use This Document

When reviewing the Grid Network design, do not treat these limitations as bugs to be fixed. They are **acknowledged boundaries** of what the protocol can achieve. The design's strength is that it names these boundaries honestly, provides mitigations where possible, and does not pretend to solve problems that cannot be solved.

> "The design is not weakened by acknowledging these scenarios. It's strengthened, because it shows the author thought about them." — Deepseek stress-test review, 2026-10-10