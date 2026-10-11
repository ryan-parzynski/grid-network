# Grid Network — Complete Project Handoff

**Document:** `HANDOFF.md`
**Purpose:** Full context transfer. Everything another agent needs to understand where the project came from, what decisions were made and why, what exists today, and what to work on next.
**Audience:** An AI agent or human maintainer taking over the project without access to the original conversation.

---

# Table of Contents

1. The project in one page
2. Origin and evolution of the idea
3. Key decisions made and why
4. Rejected approaches and why
5. What exists today (artifact inventory)
6. Repository structure and file contents
7. Open questions and known gaps
8. Recommended next steps in priority order
9. Things not to do
10. Glossary of project-specific terms
11. Appendix A — the review that shaped the handoff
12. Appendix B — the conversation's argumentative arc

---

# 1. The project in one page

**Name:** Grid Network

**What it is:** A cryptographic identity and authorization layer that sits above whatever networking already exists. It answers three questions — "who is this?", "what are they allowed to do?", and "where can I find them?" — using signed objects that participants hold and verify locally.

**What it is not:** A VPN, a DNS replacement, an anonymity network, a blockchain, or a platform.

**The problem it solves:** Today, the ability to reach your own devices from anywhere is rented from companies. Tailscale, Cloudflare, ZeroTier, and every commercial mesh product own your identity and your relationships. If they change their terms, you migrate or lose access.

**The key property:** Identity is portable. Your devices, your relationships, your authorizations belong to you, not to a vendor. Anyone can operate infrastructure, anyone can switch providers, and no company decides whether your network exists.

**The developer pitch:** You already offloaded user authentication to Auth0, Okta, or Google Sign-In. You should do the same for device connectivity. Grid Network is a shared protocol that handles identity, pairing, discovery, NAT traversal, relay fallback, and revocation. Your app calls a local grid agent, gets an authorized connection, and never thinks about keys, relays, or pairing again.

**Current state:** Protocol frozen at v0.6.2. Documentation set at draft 0.1. Phase: documentation. No code yet.

**Design principle:** Every participant — free user, contributor, commercial operator, enterprise — makes the network more valuable to every other participant. The commercial model exists to fund the protocol's maintenance and development, not to extract value from users.

---

# 2. Origin and evolution of the idea

The project began as an attempt to solve a specific, practical problem: how do you make a self-hosted server reachable from a phone that moves between networks, behind NATs and CGNAT, when the server's public IP changes unpredictably?

The conversation proceeded through several distinct phases. Understanding them matters because the decisions in the current spec came from specific critiques at specific moments.

### Phase 1 — Initial architecture sketches

The first drafts proposed a mesh VPN with a coordinator that stored endpoint information. Names used included "Mesh Coordinator," "NotDNS," and "Mesh Identity & Reachability Protocol." The framing was "a lightweight distributed DNS for peer-to-peer connections."

**Key early insights that survived:**

- **The "two blobs" separation.** Identity (long-lived, signed, reputation-carrying) is distinct from endpoint (short-lived, ephemeral, current location only). This became the fundamental architectural split.
- **Rendezvous does not own traffic.** The coordinator helps peers find each other; it does not carry their traffic. This became the "untrusted infrastructure" principle.
- **Six-digit pairing codes are temporary.** A short human-readable code is a coordination mechanism, not a credential. The underlying cryptographic exchange provides the security.

**Early ideas that did not survive:**

- **XOR obfuscation for endpoint records.** Rejected because it provides no confidentiality against any party holding the key, cannot support revocation, and cannot be upgraded without a wire-format change.
- **Heartbeat-driven reputation as a protocol concept.** Rejected as protocol-level. Reputation belongs in deployment-layer policy, not in the identity document.
- **DNS-like hierarchical naming.** Rejected. The protocol's identifiers are flat and controlled by the participant, not by a hierarchy.

### Phase 2 — Architectural separation

A major review round established the four concepts that the protocol must keep separate:

1. **Identity** — who controls this key?
2. **Authorization** — what is this peer allowed to do?
3. **Reachability** — where is the peer currently?
4. **Transport** — how do bytes actually travel?

The critique that drove this: mixing these concepts made the protocol fragile and hard to reason about. Separating them made each small enough to specify and made the resulting system robust.

**Key architectural decisions from this phase:**

- **Opaque Peer IDs, not self-certifying.** A self-certifying ID (hash of public key) is convenient but prevents root-key rotation without changing the ID. An opaque random ID bound by a signed identity document is more flexible.
- **Identity Root, Device Key, Service Key, Authorization Key as distinct roles.** Compromise of one should not compromise the others.
- **Revocation is terminal.** A revoked object cannot become valid again. Reauthorization creates a new object.
- **Key rotation is a V1 requirement.** Without it, the protocol bakes in an assumption that the key hierarchy never changes.

### Phase 3 — The verifier model

A second major review established the "verifier must be able to determine state without contacting an authority" invariant. This drove:

- **Offline verification.** The verifier holds signed objects and evaluates them locally.
- **Relative validity for leases.** Duration measured from the verifier's first observation, not from wall-clock time.
- **`max_offline_tolerance`.** A per-grant bound on how long authorization may continue without a freshness refresh.
- **Revocation as state, not event.** A revocation received before its target is cached and applied when the target arrives.

### Phase 4 — Failure semantics

A third major review established the failure semantics section. The key principle:

> **Failure of communication, discovery, synchronization, or transport MUST NOT silently become a change in identity or authorization state.**

This drove the distinction between fail-closed (authorization) and availability-preserving (connectivity), and the taxonomy of failure conditions.

### Phase 5 — Reconciliation and conflict resolution

A fourth review established the reconciliation model. Forks are resolved only by explicit signed `StreamResolution` objects, signed by pre-fork authorities. Identity continuity is handled by `IdentityContinuity` objects signed by both old and new roots.

**Key insight:** Reconciliation mechanisms may only select among already-authenticated branches. They must not introduce new state.

### Phase 6 — Stream ownership and sequence spaces

A fifth review tightened the sequence space model. The final architecture:

- **One identity stream per principal** containing identity documents, key revocations, relationship assertions, relationship terminations, and rendezvous manifests.
- **One authorization stream per Authorization Key** containing grants, leases, and revocations, all sharing a single heterogeneous sequence.
- **One reachability stream per device** containing reachability records.
- **One service stream per service** containing service records.

The invariant: **A verifier MUST NOT compare sequence numbers from different streams.**

### Phase 7 — The commercial model

A separate thread developed the commercial model. The key insight:

> **Free users are the network's foundation, not a loss leader.** They contribute reachability, peer-to-peer efficiency, local relays, and ecosystem gravity. The paid tier is built on top of the free tier.

The commercial model has these components:

- **Relay priority classes** (free, standard, priority, dedicated).
- **Idle capacity donation** (commercial overprovisioning serves the free pool).
- **Credit pools** (families and groups share credits).
- **Geographic scarcity adjustment** (scarce regions earn more credit per byte).
- **Developer funding** (structural revenue share from commercial operators).

### Phase 8 — The developer case

A separate thread developed the argument that **application developers are the primary adoption path**. The analogy to authentication offloading (Auth0, Okta, Google Sign-In) is central. Applications adopt Grid Network the way they adopted authentication providers, because connectivity is not the application's actual job.

### Phase 9 — Naming and handoff

The project was named "Grid Network" after rejecting "NotDNS" (defined by negation), "Mesh" (heavily used), "Lattice" (multiple collisions in the networking space), "Signet" (Bitcoin and Ethereum collisions), and "Ravelin" (fraud detection company).

The handoff documents were produced with a review that identified six issues, all of which were addressed.

---

# 3. Key decisions made and why

This section lists every significant decision reached during the conversation, with the reasoning.

## Protocol architecture

**Decision:** Peer IDs are opaque, not self-certifying.
**Reason:** Self-certifying IDs prevent root-key rotation without changing the ID. Opaque IDs bound by signed identity documents allow root-key rotation while preserving the identity.

**Decision:** Relationships are per-principal assertions, not a single dual-signed object.
**Reason:** A bilateral object raises the question "which principal's stream does it live in?" Per-principal assertions sidestep this. Recognition is verifier-derived.

**Decision:** Relationship termination is unilateral.
**Reason:** Recognition cannot be coerced. Either principal may withdraw it.

**Decision:** Identity continuity requires dual signatures.
**Reason:** Neither old nor new root alone should be able to claim continuity. Both must agree.

**Decision:** Chain hash construction uses cumulative commitment.
**Reason:** A bare `previous_hash` link cannot detect forks. A cumulative chain hash detects them even when a verifier has seen only one branch.

**Decision:** Sequence spaces are disjoint.
**Reason:** Prevents cross-stream comparison bugs.

**Decision:** Authorization Keys own one heterogeneous stream.
**Reason:** Grants, leases, and revocations all sequence together, making `effective_sequence` unambiguous.

**Decision:** Key revocation is signed by the Identity Root, not the revoked key.
**Reason:** A compromised key cannot be trusted to sign its own revocation.

**Decision:** Failure never grants authorization.
**Reason:** Missing information must not become authority.

**Decision:** Revocation is terminal.
**Reason:** Un-revocation is a source of subtle bugs. New authorization requires a new object.

**Decision:** `StreamResolution` requires pre-fork authority.
**Reason:** A key whose own stream is disputed cannot be trusted to resolve the fork.

**Decision:** Identity Continuity cannot bootstrap from an untrusted root.
**Reason:** A chain of dual-signed transitions must ultimately terminate at a root that was trusted before the first transition.

**Decision:** Service Link is referential only.
**Reason:** Eliminates a second authorization primitive. Authorization comes exclusively from Grant and Lease.

**Decision:** Service ownership transfer is not supported in V1.
**Reason:** Requires an authenticated transfer mechanism that V1 does not define.

**Decision:** Grant validity is absolute; lease validity is relative by default.
**Reason:** Grants are issuance events; leases are ongoing state.

**Decision:** `max_offline_tolerance` bounds authorization freshness, not lease validity.
**Reason:** Keeps the two layers clean. Lease validity is cryptographic; freshness is policy.

**Decision:** Revocation is state, not event.
**Reason:** A revocation received before its target must remain effective when the target arrives.

**Decision:** The protocol uses Ed25519 signatures and SHA-256 hashes.
**Reason:** Widely deployed, well-understood, efficient, and small.

**Decision:** Encoding is deterministic CBOR with strict canonicalization.
**Reason:** JSON has ordering ambiguity. Protobuf has multiple valid encodings. CBOR with canonical rules is unambiguous and efficient.

**Decision:** No `version` field in the signed object.
**Reason:** The `domain_separator` already carries the schema version. A separate field would create a possibility for disagreement.

**Decision:** Domain separators are part of the signed payload.
**Reason:** Prevents signature transplant between object types.

**Decision:** Object IDs and payload IDs use distinct domain-separated framing.
**Reason:** Every cryptographic construction has a unique tag; no two hashes can collide by construction.

## Commercial model

**Decision:** The protocol is free; the development is funded.
**Reason:** Free to use, free to implement, free to modify. Not free to maintain. Maintenance is funded by the commercial layer.

**Decision:** Commercial layer sells guarantees, not access.
**Reason:** Free users get best-effort service; paid users get priority. Access is never gated.

**Decision:** Free users are the network's foundation, not a loss leader.
**Reason:** They contribute reachability, P2P efficiency, local relays, and ecosystem gravity.

**Decision:** Idle commercial capacity flows to the free pool.
**Reason:** Efficient use of overprovisioning. Paid users' priority is preserved.

**Decision:** Priority is a property of the ticket, not the user's identity.
**Reason:** Enables privacy, portability, and composability.

**Decision:** Credits are bound to a pool and not freely transferable.
**Reason:** Prevents credit laundering and speculative markets.

**Decision:** Operator-agnostic credits are the design goal.
**Reason:** A user's contribution should be valuable anywhere.

**Decision:** Geographic scarcity multiplies credit value.
**Reason:** Relays in underserved regions should earn more per byte, encouraging geographic diversity.

**Decision:** Blockchain is not used for the credit system.
**Reason:** The operator count is small. Notarized receipts solve the same problem at lower cost.

**Decision:** Developer funding comes from a structural revenue share.
**Reason:** Donations and grants are volatile. Revenue share scales with adoption.

**Decision:** The stewardship entity is independent of any commercial operator.
**Reason:** Prevents commercial capture of the protocol.

## Positioning and naming

**Decision:** Name is "Grid Network."
**Reason:** "NotDNS" is defined by negation; "Mesh" is heavily used; "Lattice," "Signet," and "Ravelin" have significant collisions.

**Decision:** Applications are the primary adoption path, not end users.
**Reason:** Applications adopt Grid Network the way they adopted authentication providers. Users get it automatically.

**Decision:** Grid Network stands on the shoulders of DNS, WireGuard, BitTorrent, Bitcoin, Tailscale, and Headscale.
**Reason:** The composition is the contribution, not any individual piece.

---

# 4. Rejected approaches and why

**XOR obfuscation for endpoints.** Provides no confidentiality against parties holding the key. Cannot support revocation. Cannot be upgraded without a wire-format change.

**Shared-key encryption for endpoint records.** Same issues as XOR with a shared key.

**DNS-like hierarchical naming.** Protocol identifiers are flat and controlled by the participant, not by a hierarchy.

**Timestamp-based fork resolution.** Wall-clock time is not a resolution mechanism.

**Automatic recovery from Identity Root compromise.** No in-band mechanism exists or is proposed.

**Dual-signature objects in a single stream.** The adopted model uses per-principal assertions in per-principal streams.

**Global Sybil resistance in the protocol.** Identity quantity does not grant authority. Sybil resistance belongs at the admission policy layer of specific services.

**Proof-of-work as a foundational mechanism.** Optional admission control at the margins, not a protocol primitive.

**Blockchain for credit settlement.** Number of operators is small; notarized receipts suffice.

**DHT-based discovery in V1.** Deferred. Available rendezvous servers suffice for V1.

**Reputation and liveness scoring in identity.** Belongs in deployment-layer policy.

**Adaptive TTLs based on heartbeats.** Belongs in deployment-layer policy.

**Heartbeat as a protocol concept.** Same as above.

**"Raspberry Pis form a decentralized relay network" as product pitch.** Demoted to example. Capability abstraction is what matters.

**"Mesh can burst around ISP throttling" as feature framing.** Underlying observation retained as research note. Not a product feature.

**Cascading multiple documents into one.** The reviewer of an earlier draft recommended keeping documents separate. Each document serves a distinct audience and change rate.

---

# 5. What exists today (artifact inventory)

## Complete and frozen

**`PROTOCOL.md` v0.6.2** — The normative protocol specification. Contains 65 sections plus the Final Protocol Statement. This document is what defines the protocol. It is frozen; changes require a version bump.

**Rename needed:** The document still says "Mesh" instead of "Grid Network" in the title. Domain separators still use `mesh/*`. These need a find-and-replace to `grid/*`.

## Complete drafts

**`RATIONALE.md` v2.0** — Design rationale. Covers the problem, the solution, the audiences, the developer case, the contribution model, the commercial layer, and edge cases.

**`RATIONALE-ADDENDUM-A-COMMERCIAL.md` v6.0** — Commercial model. Covers what the commercial layer sells, free users as foundation, relay priority, credit pools, blockchain question, geographic scarcity, self-hosted priority, database synchronization, commercial products, developer funding.

**`RATIONALE-ADDENDUM-B-LINEAGE.md` v1.0** — Relationship to other systems. Covers what Grid Network borrows from DNS, WireGuard, BitTorrent, Bitcoin, Tailscale, and Headscale. Explains the composition argument and the developer angle.

## Partial drafts

**`OBJECTS.md` v0.2** — Byte-level encoding. §1–§5 complete:
- §1 Scope and normative terminology
- §2 Canonical CBOR profile
- §3 Object serialization (cryptographic constructions)
- §4 Common stream envelope
- §5 Signature semantics

§6–§10 pending:
- §6 Object schemas (one per object type)
- §7 Stream rules
- §8 Positive test vectors
- §9 Negative test vectors
- §10 Conformance requirements

**`README.md`** — Entry point.

**`OUTLINE.md`** — Project map.

**`VERSIONING.md`** — Extracted from `PROTOCOL.md` §64.

**`GLOSSARY.md`** — Partial term list.

**`FAQ.md`** — Question list, answers pending.

## Stubs

**`SECURITY.md`** — Structure defined (11 parts). Content to be drafted from `PROTOCOL.md` §50–§53.

**`IMPLEMENTATION.md`** — Structure defined (8 parts). Content to be drafted.

**`CONNECTIVITY.md`** — Structure defined (11 parts). Content to be drafted.

**`ROADMAP.md`** — Structure defined. Phases 0–5.

**`CONTRIBUTING.md`** — Ready.

**`LICENSE.md`** — Apache 2.0.

## Empty

**`TEST-VECTORS/`** — Structure defined. No vectors exist.

**`implementations/`** — Placeholder. No implementations.

**`apps/`** — Placeholder. No applications.

---

# 6. Repository structure and file contents

## Directory tree

```
grid-network/
├── README.md
├── LICENSE.md
├── CONTRIBUTING.md
├── HANDOFF.md (this file)
│
├── docs/
│   ├── README.md
│   ├── OUTLINE.md
│   │
│   ├── protocol/
│   │   ├── PROTOCOL.md
│   │   ├── OBJECTS.md
│   │   └── VERSIONING.md
│   │
│   ├── security/
│   │   └── SECURITY.md
│   │
│   ├── implementation/
│   │   ├── IMPLEMENTATION.md
│   │   └── CONNECTIVITY.md
│   │
│   ├── rationale/
│   │   ├── RATIONALE.md
│   │   ├── ADDENDUM-A-COMMERCIAL.md
│   │   └── ADDENDUM-B-LINEAGE.md
│   │
│   └── reference/
│       ├── GLOSSARY.md
│       └── FAQ.md
│
├── spec/
│   └── test-vectors/
│       └── v1/
│           (no vectors yet)
│
├── implementations/
│   └── README.md
│
└── apps/
    └── README.md
```

## Relationship between documents

- `PROTOCOL.md` defines the protocol. It is the source of truth.
- `OBJECTS.md` defines byte-level encoding. It must not contradict `PROTOCOL.md`.
- `SECURITY.md` elaborates on the security properties stated in `PROTOCOL.md` §50–§53. It does not introduce new protocol requirements.
- `IMPLEMENTATION.md` describes how to build a Grid Agent. It does not introduce new protocol requirements.
- `CONNECTIVITY.md` describes the connectivity layer above the protocol. It consumes `PROTOCOL.md` and does not modify it.
- `RATIONALE.md` and its addenda explain why. They do not introduce normative requirements.
- `VERSIONING.md` is extracted from `PROTOCOL.md` §64.

## The four layers

1. **Protocol Kernel** — identity, authorization, reachability, cryptographic objects, and the verification model.
2. **Security & Implementation** — threat model, verifier rules, parser requirements.
3. **Connectivity Architecture** — path abstraction, relay model, future multipath.
4. **Strategy** — vision, ecosystem, roadmap.

Layers must not cross. No Layer 1 document should contain Layer 2 content, and so on.

---

# 7. Open questions and known gaps

## Documentation gaps

**OBJECTS.md §6 — Object schemas.** Every object type needs its full field schema. Approximately 18 object types.

**OBJECTS.md §7 — Stream rules.** Sequence spaces, initial chain state, monotonicity, gap detection, fork detection, resolution.

**OBJECTS.md §8–§10.** Positive test vectors, negative test vectors, conformance requirements.

**SECURITY.md.** Content from `PROTOCOL.md` §50–§53 plus operational security material.

**IMPLEMENTATION.md.** Grid Agent architecture, API, storage, cross-platform notes.

**CONNECTIVITY.md.** Direct-first preference, NAT traversal, relay architecture, PathSet abstraction.

**GLOSSARY.md.** Complete term definitions. Partial list exists.

**FAQ.md.** Answers to all comparison and design questions.

**ROADMAP.md.** Phases and completion criteria.

## Technical open questions

**Chain-extension proofs.** V1 does not support skip-ahead. V2 may introduce authenticated chain-extension proofs. The exact form is undecided.

**Governance model.** V1 has no governance mechanism. The choice among reference-implementation-driven, benevolent-dictator, and standards-body models is deferred.

**Threshold recovery.** V1 has no in-band recovery from Identity Root compromise. V2 may introduce threshold or social recovery. The design is open.

**Metadata minimization.** The protocol provides confidentiality of content and authorization, not anonymity of participation. Future versions may add rotating pseudonyms for rendezvous lookups.

**Credit system calibration.** Scarcity multipliers, exchange rates, and the specific formula for credit earning are deployment policy, not protocol. Best practices are open.

**Local state storage.** Best practices for durable storage of trust anchors, stream state, and observation history are not yet specified.

## Design questions

**Why doesn't the protocol handle user authentication?** Because user authentication and device authentication are different problems. The application keeps its own user model.

**Why is relay a fallback and not the default?** Because direct connections are preferable. Relay exists for cases where direct connectivity fails.

**Why is identity portable?** Because that's the property that prevents vendor lock-in.

**How does the protocol handle a peer offline for six months?** Identity is unchanged, relationships are unchanged, reachability expires, authorization is bounded by leases. On return, the peer republishes reachability and renews leases.

---

# 8. Recommended next steps in priority order

## Tier 1 — Blocks everything else

**Task 1.** Rename Mesh → Grid Network throughout `PROTOCOL.md`. Atomic commit. 19 domain separators, 6 cryptographic tags, the URI scheme, the local API prefix, and the protocol name itself. Must complete before tasks 2–4.

**Task 2.** Complete `OBJECTS.md` §6 — Object schemas. One schema per object type with field names, types, constraints, stream membership, signing key role, and domain separator.

**Task 3.** Complete `OBJECTS.md` §7 — Stream rules. Sequence spaces, initial chain state, monotonicity, gap detection, fork detection, resolution procedures, cross-stream prohibition.

**Task 4.** Produce the first test vector. A minimal sequence-1 signed object exercising §2 and §3 of `OBJECTS.md`. Then sequence-2. Then IdentityDocument at sequence 1 and 2. Then RelationshipAssertion. Then IdentityContinuity (dual-signature). Then StreamResolution. Then the remaining object types.

### Definition of a test vector

A **test vector** is a byte-exact normative case consisting of:

1. **Input** — a fully-specified set of parameters that determine the object.
2. **Expected canonical bytes** — the exact `canonical_signed_object_bytes`.
3. **Expected derived values** — `object_commitment`, `chain_hash`, `payload_id`, `object_id`.
4. **Expected signature** — the Ed25519 signature over `signature_input`.
5. **Specification reference** — the section that the vector tests.

A **positive test vector** has expected behavior "validates." A **negative test vector** has expected behavior "rejected with class X."

### Sequence of vector production

1. Minimal sequence-1 generic object
2. Sequence-2 generic object
3. IdentityDocument at sequence 1
4. IdentityDocument at sequence 2
5. RelationshipAssertion (single-signature)
6. IdentityContinuity (dual-signature)
7. StreamResolution (resolver/disputed stream distinction)
8. Remaining object types (one positive vector each)

### Negative vectors

At minimum, three negative vectors accompany the first positive vector:

1. Tampered field
2. Non-canonical encoding (longer-than-necessary integer)
3. Wrong domain separator

Each specifies the expected rejection class.

### Vector format

Each vector is JSON with: description, object (base64), domain_separator, expected (object_id, payload_id, chain_hash, signature_valid), specification reference. Negative vectors include expected_rejection_class. Alongside each JSON file is a `.bytes` file with the raw canonical bytes.

### Vector ownership

The receiving agent produces the vectors. An implementation "passes" when it produces the same canonical bytes and derived values (positive) or rejects with the correct class (negative).

## Tier 2 — Enables adoption

**Task 5.** Complete `OBJECTS.md` §8–§10.

**Task 6.** Draft `SECURITY.md`. Derived from `PROTOCOL.md` §50–§53 plus operational security material.

**Task 7.** Draft `IMPLEMENTATION.md`. Grid Agent architecture, API, storage, cross-platform.

**Task 8.** Draft `CONNECTIVITY.md`. Direct-first, NAT traversal, relay architecture, PathSet.

## Tier 3 — Enables funding

**Task 9.** Complete `GLOSSARY.md`.

**Task 10.** Complete `FAQ.md`.

**Task 11.** Extract `VERSIONING.md` from `PROTOCOL.md` §64 if not already done.

## Tier 4 — Long-term

**Task 12.** Reference implementation.

**Task 13.** Independent implementation.

**Task 14.** Applications and integrations.

**Task 15.** Commercial infrastructure.

---

# 9. Things not to do

**Do not redesign the protocol.** v0.6.2 is frozen. Changes require a version bump.

**Do not add new object types, authority domains, or stream spaces** without explicit justification documented in a proposal.

**Do not add security mechanisms merely because an attack is theoretically possible.** Every mechanism needs a specific boundary it protects. Before adding a mechanism, answer:

1. What authority or resource does it protect?
2. What specific attack does it prevent?
3. What happens if it is removed?
4. What new complexity does it introduce?

If any answer is unsatisfactory, the mechanism is premature.

**Do not conflate the layers.** The protocol kernel is Layer 1. Security is Layer 2. Connectivity is Layer 3. Strategy is Layer 4. Keep them separate.

**Do not let the documentation set become a marketing document.** The rationale can make the case; the protocol must stay technical.

**Do not introduce vendor lock-in.** The whole point is portability.

**Do not skip the rename.** Tasks 2–4 depend on it.

**Do not produce test vectors before §6–§7 are stable.** Vectors against an unstable schema are wasted work.

**Do not omit negative test vectors.** A vector suite that only checks "valid objects validate" is incomplete. Rejection with specific classes is a protocol requirement.

**Do not silently extend the protocol.** If a schema needs a new field that isn't in the object type's current design, that's a protocol change, not a schema decision.

---

# 10. Glossary of project-specific terms

**Peer Principal** — The durable logical identity. May span multiple devices and services.

**Peer Principal ID** — Opaque identifier bound to the principal's identity root by the identity document.

**Identity Root** — Highest cryptographic authority for a principal. Signs identity documents, relationships, key delegations.

**Device Key** — Authenticates a device. Signs reachability records.

**Service Key** — Authenticates a service. Signs service records.

**Authorization Key** — Signs grants, leases, and revocations in its stream.

**Identity Document** — Signed object binding a Peer ID to an identity root and subordinate keys.

**Relationship Assertion** — Unilateral signed recognition statement. Two matching assertions establish verifier-derived `RECOGNIZED`.

**Relationship Termination** — Unilateral signed withdrawal of recognition. Terminal.

**Grant** — Directional signed authorization. Contains capabilities, constraints, lease policy.

**Lease** — Short-lived proof that a grant is currently valid.

**Revocation** — Terminal signed invalidation.

**Key Revocation** — Revocation of a specific Authorization Key, signed by the Identity Root. Contains `effective_sequence`.

**Reachability Record** — Signed assertion of a device's current endpoints. Ephemeral.

**Service Record** — Signed assertion of a service's current endpoint and metadata.

**Rendezvous** — Infrastructure that stores and serves signed objects. Untrusted.

**Relay** — Infrastructure that forwards encrypted traffic. Untrusted.

**Relay Ticket** — Signed authorization permitting relay use. Pair-bound, capability-bound, short-lived.

**Service Link** — Referential identifier. Not an authorization object.

**Sequence Space** — The pair `(issuer, stream_id)`. Sequence numbers are meaningful only within their space.

**Stream** — Ordered sequence of objects sharing one sequence space.

**Initial Chain Hash** — Base state for a stream, computed from the domain separator and stream ID.

**Chain Hash** — Cumulative stream-history hash.

**Object Commitment** — Hash of an object's unsigned payload with domain-separated preimage.

**Signature Input** — Canonical CBOR structure that is signed.

**Object ID** — Hash of the signed object's canonical bytes.

**Payload ID** — Hash of the unsigned payload's semantic content.

**Authority Precedence Table** — Normative table specifying which object governs in conflicts.

**Signing-Authority Matrix** — Normative table specifying which key role signs each object type.

---

# 11. Appendix A — the review that shaped the handoff

A review of an earlier handoff draft identified six issues:

1. **Hidden dependency between rename and schema work.** The rename needed to be a prerequisite, not a parallel task.
2. **Test vector definition was underspecified.** The reviewer asked for a clear definition of what a "test vector" is and what "first test vector" means.
3. **CONNECTIVITY.md scope was unclear.** The reviewer asked for the split between `IMPLEMENTATION.md` and `CONNECTIVITY.md` to be documented.
4. **SECURITY.md had no structure.** The reviewer asked for a stub.
5. **GLOSSARY.md and FAQ.md had no seed content.** The reviewer asked for initial content.
6. **ROADMAP.md was missing.** The reviewer asked for a stub.

The reviewer also made technical observations:

- §3.7's object ID warning is easy to get wrong; test vectors should catch this.
- §2.8's set semantics require bytewise lexicographic ordering; this must be consistently applied in §6.
- The chain hash construction is novel; test under adversarial reordering.

All six issues and all three technical observations were addressed in the revised handoff.

---

# 12. Appendix B — the conversation's argumentative arc

The project went through a series of positions and critiques:

**Position 1.** "We need a decentralized DNS for peer-to-peer connections."

**Critique 1.** "This is defined by what it isn't. What is it, positively?"

**Position 2.** "It's a mesh VPN with a coordinator."

**Critique 2.** "How is this different from Tailscale?"

**Position 3.** "Identity is portable. The coordination layer is replaceable."

**Critique 3.** "But then who runs the infrastructure?"

**Position 4.** "Anyone can run it. The commercial layer funds the infrastructure and the development."

**Critique 4.** "How does the funding work?"

**Position 5.** "Commercial operators sell priority relay. Idle capacity flows to the free pool. Contributors earn credits."

**Critique 5.** "What about abuse?"

**Position 6.** "Abuse vectors are mitigated by design. Credits are bound to pools. Contributions verified by receiving peers."

**Critique 6.** "What about enterprises?"

**Position 7.** "Enterprises run their own infrastructure, get self-priority, contribute idle capacity, and integrate with their existing identity providers."

**Critique 7.** "What about the developer audience?"

**Position 8.** "Applications adopt Grid Network the way they adopted Auth0. The developer pitch is 'stop building connectivity.'"

**Critique 8.** "Why not just use Tailscale?"

**Position 9.** "Because Tailscale is a company, and identity is not portable across it. Grid Network's identity is portable."

**Critique 9.** "This seems overengineered."

**Position 10.** "The complexity is in the protocol, not the user experience. Every mechanism protects a specific boundary."

**Critique 10.** "What about governance?"

**Position 11.** "V1 has no governance mechanism. This is a deliberate deferral."

**Critique 11.** "What about the name?"

**Position 12.** "Grid Network. Rejected NotDNS, Mesh, Lattice, Signet, Ravelin."

**Critique 12.** "Give me a handoff."

**Position 13.** The handoff documents were produced.

**Critique 13.** The handoff was reviewed. Six issues were identified.

**Position 14.** The issues were addressed. This document is the response.

---

# End of handoff

The project is at documentation phase. The protocol is frozen at v0.6.2. The documentation set is at draft 0.1. The next priority is to complete `OBJECTS.md` §6–§10 and produce the first test vector.

The receiving agent should begin by reading this document, then `README.md`, then `docs/OUTLINE.md`, then `docs/protocol/PROTOCOL.md`. After that, the state of every document should be clear.

Any question that this document does not answer should be answerable by reference to `PROTOCOL.md` or `RATIONALE.md`. If a question is not answerable by either, it is either an open question (Section 7) or a signal that the documentation has a gap.