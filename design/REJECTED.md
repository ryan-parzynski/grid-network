# Grid Network — Rejected Approaches

**Revision:** 2.2
**Protocol version:** v0.6.3

This document records approaches that were considered and rejected, with
the reason for rejection. It is non-normative. Its purpose is to prevent
re-litigation of settled questions and to document what would need to
change for a rejected approach to be reconsidered.

---

## R1. XOR obfuscation for reachability endpoints

**Approach.** Obfuscate endpoint addresses with a shared XOR key.

**Rejected because.** XOR provides no confidentiality against an
attacker who knows the key, breaks revocation because revoked keys
cannot be tracked, and cannot be upgraded to a stronger scheme without
changing every published record.

**Reopening condition.** None. The approach is strictly weaker than the
current design.

---

## R2. Shared-key encryption for endpoints

**Approach.** Encrypt reachability endpoints under a key shared between
publisher and verifier.

**Rejected because.** A rendezvous server cannot serve encrypted
endpoints it cannot read. The lookup model requires the server to read
the record to dispatch it.

**Reopening condition.** A design in which rendezvous servers do not
need to read records, for example a fully encrypted query-response
scheme.

---

## R3. DNS-like hierarchical naming

**Approach.** Assign identities hierarchical names (like
`alice.example.peer`) and resolve them through a tree of authorities.

**Rejected because.** Hierarchy requires a root authority, which the
design forbids. It also enables censorship at any level and reintroduces
mutable names.

**Reopening condition.** None. The design's core property is the
absence of a root authority.

---

## R4. Timestamp-based fork resolution

**Approach.** When two objects are observed at the same sequence,
resolve the fork by accepting the object with the newer timestamp.

**Rejected because.** An attacker can forge a future timestamp.
Timestamp-based resolution grants the attacker the fork.

**Reopening condition.** None. Timestamps are attacker-controlled data.

---

## R5. Automatic recovery from Identity Root compromise

**Approach.** Provide an in-band mechanism to recover from root key
compromise.

**Rejected because.** No in-band mechanism can distinguish a legitimate
recovery from an attacker-driven one. Any such mechanism is a new
authority the protocol cannot trust.

**Reopening condition.** A threshold scheme in which multiple parties
must agree. Threshold recovery is a `planned` feature; the current
protocol version does not include it.

---

## R6. Dual-signature relationship objects in a single stream

**Approach.** Store mutual recognition as a single object signed by
both principals.

**Rejected because.** A bilateral object raises the question of which
stream owns it. Every candidate answer creates either a new stream
signed by two authorities, a co-signing convention, or an ordering
problem.

**Reopening condition.** A stream model that permits multi-signer
objects.

---

## R7. Global Sybil resistance in the protocol

**Approach.** Add a protocol-level mechanism to prevent Sybil attacks.

**Rejected because.** Sybil resistance is a policy problem. The
protocol does not prevent identity creation; rate limits and admission
control at the infrastructure layer are the appropriate mitigations.

**Reopening condition.** None at the protocol layer. A deployment may
add admission control as a policy.

---

## R8. Proof-of-work as a foundation

**Approach.** Require proof-of-work to create an identity or publish a
record.

**Rejected because.** Mobile devices cannot perform sustained
proof-of-work. The environmental cost is disproportionate to the
benefit.

**Reopening condition.** None. The cost falls on users, not attackers.

---

## R9. Blockchain for credit settlement

**Approach.** Use a blockchain for cross-operator credit settlement.

**Rejected because.** The number of operators is small. A blockchain
adds latency, cost, and complexity without solving a problem that
signed receipts and notarized records cannot solve.

**Reopening condition.** A scale of operators at which signed receipts
are insufficient. The design does not anticipate such a scale.

---

## R10. DHT-based discovery as the primary mechanism

**Approach.** Use a distributed hash table as the primary discovery
mechanism instead of rendezvous servers.

**Rejected because.** Lookup latency in a DHT is seconds, not
milliseconds. The protocol needs fast discovery for interactive
sessions.

**Reopening condition.** A DHT with sub-second lookup, or a use case
where discovery latency is not interactive. DHT-based discovery is a
`planned` feature as a fallback, not a primary mechanism.

---

## R11. Reputation and liveness scoring in identity

**Approach.** Include reputation and liveness scores in the identity
document, updated by peers.

**Rejected because.** Reputation is application-specific and can be
gamed. Including it in the protocol would require defining what
reputation means, who can update it, and how it is protected from
manipulation.

**Reopening condition.** None at the protocol layer. Applications may
maintain reputation data alongside the protocol.

---

## R12. Adaptive TTLs from heartbeats

**Approach.** Adjust reachability TTL based on observed heartbeats
from the peer.

**Rejected because.** Heartbeats are expensive and create an implicit
liveness protocol. Reachability TTL should be policy-driven, not
adaptive from behavior.

**Reopening condition.** None. The TTL is set by the publisher.

---

## R13. "Home relays form a decentralized network" as the primary pitch

**Approach.** Lead with the claim that a network of home relays
provides decentralized capacity comparable to commercial infrastructure.

**Rejected because.** It oversells the capability. Home relays are a
contribution to capacity, not the primary capacity. Commercial relays
remain the backbone.

**Reopening condition.** None. The pitch is misleading.

---

## R14. "The network bursts around ISP throttling" as a product feature

**Approach.** Market the protocol as a way to circumvent ISP
throttling.

**Rejected because.** It does not work as a general claim, it
overstates the design's capabilities, and it carries legal risk.

**Reopening condition.** None. The claim is not supported by the
design.

---

## R15. Push-based revocation

**Approach.** Revocations are pushed to all relevant parties.

**Rejected because.** Push-based revocation violates the design
principle that no authority pushes state changes. It requires the
protocol to define who pushes, to whom, and with what guarantees.
Pull-based revocation is the correct model.

**Reopening condition.** A push mechanism that is itself signed and
verifiable, and that does not require the recipient to trust the
pusher.

---

## R16. An `IdentitySnapshot` object

**Approach.** Add a snapshot object that captures the current identity
state.

**Rejected because.** It is redundant with `IdentityContinuity` and
with rendezvous serving identity documents. Adding it would duplicate
existing mechanisms.

**Reopening condition.** A use case where neither continuity nor
rendezvous-served documents is sufficient.

---

## R17. Decay fields in the protocol for relationship state

**Approach.** Include decay parameters in the protocol for how long
relationship state persists.

**Rejected because.** Decay is a property of the verifier's local
state, not a protocol object. The protocol does not define verifier
local state structure.

**Reopening condition.** A need to standardize decay behavior across
implementations. If such a need emerges, it is an operator policy, not
a protocol rule.