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

---

## Future Work

### What It Does Well

**Opaque peer IDs rather than self-certifying IDs.** Peer identity is a principal identifier bound to a signing key through an explicit authorization record, not derived from the key itself. This allows key rotation without identity change, and supports delegation without re-deriving IDs.

**Per-principal relationship assertions.** Authorization is expressed as assertions issued by principals about their own state (device posture, key bindings, revocation decisions), not as permissions granted by a central authority. Each relationship carries its own signed state.

**Effective_sequence on revocation.** Revocation carries an explicit sequence number that orders it relative to other state changes, enabling verifiers to reason about temporal precedence without relying on wall-clock time.

**Separation of lease validity from freshness.** A lease (rendezvous ticket, relay capability, key authorization) has a validity window; freshness is a separate property evaluated by the verifier based on observation recency. This avoids conflating expiration with staleness.

**Revocation as state, not just an event.** Revocation is recorded in the identity continuity chain as a signed object with `effective_sequence`, making it queryable and auditable. A revoked key leaves a verifiable trace rather than disappearing.

**Infrastructure never being authoritative.** Rendezvous, relay, and directory services are replaceable infrastructure. They carry signed state; they do not *become* the source of truth. Authority remains with the signing principals.

**Canonical CBOR with domain separation.** All signed objects use a deterministic CBOR profile (RFC 8949 §4.2.3 length-first map ordering, lexicographic set-element ordering, explicit null/absent semantics) with domain-separated tags per object type. This eliminates encoding ambiguity as a source of verification divergence.

---

### Unresolved Contradictions (Block Implementation)

These are structural inconsistencies where the specification gives implementers incompatible models. **Implementation cannot proceed on the affected subsystems until these are reconciled.**

| Area | Issue |
|------|-------|
| **Stream identity: §7 vs §45.1** | `spec/OBJECTS.md` §7 defines hash-derived `stream_id = H(principal_id \|\| signing_key_id \|\| stream_context \|\| epoch)` with opaque keys; `spec/PROTOCOL.md` §45.1 defines text-string streams (`stream:identity`, `stream:reachability:<device_id>`). Two incompatible models coexist in normative text. |
| **Verification authority: §5.3 vs §9** | §9 explicitly defers to §5.3 ("§5.3 takes precedence"), but both contain full 12-phase procedures. Normative text has two copies with a stated tiebreak — not a single source of truth. |
| **§5.3 step 6 ambiguity** | "sequence-1" reads as "the object at sequence number 1" rather than "the object at sequence N-1." §9 Phase 6 phrases it correctly ("the verifier's accepted `chain_hash` for `sequence-1`"), but §5.3 is authoritative. |
| **§54.5 completeness** | §54.5.1–§54.5.3 exist (model, schema, stream semantics). §54.5.4–§54.5.7 (verification rules, trust chain, effect of acceptance, recovery from root compromise) are absent in both this snapshot and the prior. Diagram truncates at "dual authorization" with no closing content. Source loss vs intentional removal unconfirmed. |
| **§7 dangling normative file references** | §7 ends with a "Missing schema bindings" block referencing six files that do not exist: `SCHEMA.md`, `CRYPTO.md`, `ENCODING.md`, `ROUTING.md`, `CONTINUITY.md`. These are missing normative material (KeyAuthorizationRecord, stream_context, epoch encoding, varint spec, hash function, signature bindings, routing key, continuity mechanism), not mere note-to-self. |
| **PAKE selection** | The pairing protocol requires SPAKE2 or CPace but does not mandate one. This blocks pairing, transcript binding, wire protocol, and test vector completion. |
| **Wire protocol missing** | No transport encoding, framing, or RPC definitions exist. Object delivery, rendezvous API endpoints, relay wire format, and ticket presentation flow are not specified. This is an interoperability blocker. |
| **Map-ordering citation error** | OBJECTS.md §2.7 cites RFC 8949 §4.2.1 for length-first core deterministic encoding; the correct section is §4.2.3. This affects canonical encoding. |

---

### Open Design Decisions (Deferred but Not Contradictory)

These are bounded design choices where the architecture anticipates a decision but does not yet prescribe one. **Implementation can proceed on other subsystems while these are open.**

| Area | Open Work |
|------|-----------|
| **Identity sequence across root rotation** | Defining how `identity_sequence` advances and is verified when a principal rotates its root key; handling competing successor roots; migration path for existing implementations |
| **Reboot / suspend / restore behavior** | Specifying how a peer reconstructs its continuity chain and lease state after process restart; handling clock-skew and monotonicity gaps; defining what state must be durably persisted |
| **Transport-to-identity binding** | Binding rendezvous/relay connections to the identity continuity chain; preventing connection hijacking when transport changes; defining the wire-level binding mechanism |
| **Revocation ordering** | Resolving concurrent revocations of the same key; defining the fork-resolution rule when two revocation objects claim the same `effective_sequence` |
| **Delayed observation / freshness rules** | Formalizing how verifiers handle objects received significantly after their validity window; defining freshness thresholds and grace periods without central time authority |
| **Delegated resolver roles** | Defining resolver authority, challenge semantics, and dispute resolution for delegated identity resolution |
| **Relay profile / ticket stream semantics** | Independent artifact vs stream-bound; rotation transition table; capability advertisement format |
| **Conformance scenarios and test vectors** | Producing the 50+ normative test vectors blocked on OBJECTS.md §§6–10 schema completion and PAKE selection |

---

### Open Investigation

| Item | Question |
|------|----------|
| **§54.5.4–§54.5.7 absence** | Confirm whether content was intentionally removed or accidentally lost in the merge pipeline. If lost, restore from source. If never authored, write the missing verification rules, trust chain requirements, and recovery semantics. |

---

### Minor Hygiene

| Item | Status |
|------|--------|
| `CHANGELOG.md` missing | Optional follow-up — add if project adopts changelog convention |

---

### Why This Matters

The unresolved items do not negate the core design; they define the boundary between **review-ready** and **implementation-ready**. The protocol's central commitments — identity as a verifiable property, coordination as a service provided by signed state, infrastructure as replaceable substrate — are internally consistent and documented.

The open work falls into two categories:
1. **Unresolved contradictions** (above) — where the spec gives incompatible answers and implementation is blocked.
2. **Open design decisions** (above) — where the spec correctly identifies a boundary and implementation can proceed elsewhere.

Each item is a bounded design decision or reconciliation task, not a fundamental gap.

---

### Summary

Grid Network provides a coordination model where **identity is a property proved by signed state**, **infrastructure is a replaceable service**, and **authorization flows from principals to peers without a central authority**. The review-stage specification establishes the cryptographic and structural foundations; the remaining work closes the boundary between design intent and interoperable implementation.

---

*Triage report based on commit `70154b7` (cleanup: fix frozen labels, dated timelines, remove artifact files). Cleanup changes: README wording, 7 files' frozen labels, dated timelines in ROADMAP.md and implementations/README.md, removal of 4 artifact files (.bak, .json). No new specs or mechanisms introduced.*
