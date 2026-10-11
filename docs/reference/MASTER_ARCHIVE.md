# Grid Network — Master Archive

**Version:** 1.0
**Status:** Consolidated archive of all project materials
**Purpose:** Preserve every artifact, decision, discussion, and detail produced over the course of the project. Organized so that nothing is lost. Read the index, then dive into whichever part you need.

---

# How to use this archive

This archive has **four levels**:

1. **Index** (this page) — points to every part
2. **Parts** — thematic groupings of documents
3. **Documents** — full-text files
4. **Appendices** — cross-cutting material (glossary, decisions, anti-patterns)

If you are handing off to another agent: point them at this file. They should read Parts 1–4 in order, then whichever Parts are relevant to their task.

If you are searching for a specific decision: start with Part 20 (Decision Log) — every significant choice is recorded there with its reasoning.

If you are searching for a specific document: Part 2 (Document Inventory) lists every file with its status and purpose.

---

# Part 1 — Master Index

## Part 1: Master Index (this section)

## Part 2: Document Inventory
Every document, its status, its purpose, and where its full text lives.

## Part 3: Executive Summary
The project in one page — problem, solution, audiences, current state.

## Part 4: The Problem
Full analysis of what's broken today.

## Part 5: The Solution
Full analysis of how Grid Network solves it.

## Part 6: Architecture and Layers
The four-layer project model, the authority chain, the stream model.

## Part 7: The Protocol
Full normative summary of PROTOCOL.md v0.6.2, section by section.

## Part 8: Object Encoding
Full normative summary of OBJECTS.md §1–§5, plus the pending structure of §6–§10.

## Part 9: Security Model
Threat model, blast radius, verifier rules, failure semantics.

## Part 10: Connectivity Architecture
Direct-first, relay model, path abstraction, future multipath.

## Part 11: Commercial Model
Free tier, relay priority, credit pools, geographic scarcity, developer funding.

## Part 12: The Developer Case
Why applications adopt Grid Network, what integration looks like.

## Part 13: Contribution Model
Three layers, contribution by capacity, economic shape.

## Part 14: Lineage and Composition
What Grid Network borrows from DNS, WireGuard, BitTorrent, Bitcoin, Tailscale, Headscale.

## Part 15: The Relay and Pi Node Design Record
Everything from the relay design discussion, including the Pi 3B analysis, bandwidth aggregation, path diversity.

## Part 16: Edge Cases and FAQ
Offline behavior, lost devices, malicious infrastructure, common questions.

## Part 17: Roadmap and Priorities
What to do next, in order, with completion criteria.

## Part 18: Project Structure
Repository layout, document responsibilities, dependency graph.

## Part 19: Naming and Positioning
Why "Grid Network," alternatives considered, pitch material.

## Part 20: Decision Log
Every significant decision made during the project, with reasoning.

## Part 21: Rejected Approaches
Everything considered and rejected, with reasoning.

## Part 22: Glossary
Every term, with cross-references.

## Part 23: Anti-Patterns and Design Rules
What not to do, and how to decide whether to add a mechanism.

## Part 24: The Complete Handoff Package
Ready-to-paste documentation set for another agent.

## Appendix A: The Relay Document (Full)
## Appendix B: Security Addendum (Full)
## Appendix C: Rationale Addendum A — Commercial Model (Full)
## Appendix D: Rationale Addendum B — Lineage (Full)

---

# Part 2 — Document Inventory

Every document that has been produced, drafted, or outlined during this project.

## 2.1 Documents with complete text available

| Document | Version | Status | Location in this archive |
|----------|---------|--------|--------------------------|
| `PROTOCOL.md` | v0.6.2 | Frozen | Part 7 (summary) + conversation history (full) |
| `OBJECTS.md` §1–§5 | v0.2 | Draft | Part 8 (summary) + conversation history (full) |
| `RATIONALE.md` | v2.0 | Draft | Parts 3–6, 11–16 (integrated) |
| `RATIONALE-ADDENDUM-A-COMMERCIAL.md` | v6.0 | Draft | Part 11 + Appendix C |
| `RATIONALE-ADDENDUM-B-LINEAGE.md` | v1.0 | Draft | Part 14 + Appendix D |
| `SECURITY.md` | — | Draft (as addendum) | Part 9 + Appendix B |
| Relay Design Record | — | Complete | Part 15 + Appendix A |
| Pitch Document | — | Complete | Part 19 |

## 2.2 Documents with partial content

| Document | Status |
|----------|--------|
| `OBJECTS.md` §6–§10 | To be drafted |
| `GLOSSARY.md` | Partial (Part 22) |
| `FAQ.md` | Partial (Part 16) |
| `VERSIONING.md` | Extracted (Part 18) |
| `ROADMAP.md` | Drafted (Part 17) |

## 2.3 Documents outlined but not drafted

| Document | Purpose | Priority |
|----------|---------|----------|
| `IMPLEMENTATION.md` | Grid Agent architecture, APIs, storage | Tier 2 |
| `CONNECTIVITY.md` | Connectivity layer specifics | Tier 2 |
| `VISION.md` | Product narrative | Tier 3 |
| `ECOSYSTEM.md` | Ecosystem map | Tier 4 |
| `TEST-VECTORS/` | Byte-exact test cases | Tier 1 |

## 2.4 Complete repository tree

```
grid-network/
├── README.md
├── LICENSE.md                    (Apache 2.0)
├── CONTRIBUTING.md
├── HANDOFF.md                    (this archive)
│
├── docs/
│   ├── README.md
│   ├── OUTLINE.md
│   │
│   ├── protocol/
│   │   ├── PROTOCOL.md           (v0.6.2 frozen; needs rename)
│   │   ├── OBJECTS.md            (§1–§5 done; §6–§10 pending)
│   │   └── VERSIONING.md         (extract from §64)
│   │
│   ├── security/
│   │   └── SECURITY.md           (to draft)
│   │
│   ├── implementation/
│   │   ├── IMPLEMENTATION.md     (to draft)
│   │   └── CONNECTIVITY.md       (to draft)
│   │
│   ├── rationale/
│   │   ├── RATIONALE.md          (v2.0)
│   │   ├── ADDENDUM-A-COMMERCIAL.md (v6.0)
│   │   └── ADDENDUM-B-LINEAGE.md    (v1.0)
│   │
│   ├── design/
│   │   └── RELAY-DESIGN-RECORD.md
│   │
│   └── reference/
│       ├── GLOSSARY.md
│       └── FAQ.md
│
├── spec/
│   └── test-vectors/
│       └── v1/
│           └── (no vectors yet)
│
├── implementations/
│   └── README.md
│
└── apps/
    └── README.md
```

---

# Part 3 — Executive Summary

**Project name:** Grid Network

**One-line:** A cryptographic identity and authorization layer that turns whatever network connectivity happens to exist into a usable, replaceable connectivity fabric.

**What it is:** A control plane above existing transports that answers three questions:

- **Who is this?** — Cryptographic identity (keypair)
- **What are they allowed to do?** — Signed authorization (grants, leases)
- **Where can I find them?** — Ephemeral reachability records

**The problem:** Today, the ability to reach your own devices from anywhere is rented from companies. Tailscale, Cloudflare, ZeroTier, and every commercial mesh product own your identity and your relationships. If they change their terms, you migrate or lose access.

**The key property:** Identity is portable. Your devices, relationships, and authorizations belong to you, not to a vendor.

**The design principle:**

> Every participant — free user, contributor, commercial operator, enterprise — makes the network more valuable to every other participant. The commercial model exists to fund the protocol's maintenance and development, not to extract value from users.

**Current state:**
- Protocol: v0.6.2 (frozen)
- Document set: 0.1 (early draft)
- Phase: Documentation
- Next: Complete OBJECTS.md §6–§10, produce first test vector

**What it is not:** A decentralized VPN, a DNS replacement, an anonymity network, a blockchain, or a platform.

**The evolution of the name:**
- Originally "Mesh Coordinator"
- Then "NotDNS"
- Then "Mesh Identity & Reachability Protocol"
- Now "Grid Network"

The name changed because:
- "NotDNS" defined the project by negation
- "Mesh" collided with an existing networking library
- "Lattice," "Signet," "Ravelin" had significant collisions in the networking and crypto space
- "Grid Network" was chosen for being descriptive (a grid of peers), scalable across audiences, and relatively uncollided

---

# Part 4 — The Problem

## 4.1 The core problem

Every self-hosted service, every personal server, every home automation system, every private application eventually hits the same wall:

> *"How do I reach this from somewhere else?"*

## 4.2 The three bad choices

**Choice 1: Expose it to the internet.**

Open a port, forward it on the router, hope nothing scans you. This works until it doesn't — until a firmware vulnerability is discovered, until a service is running with default credentials, until someone's home camera feed is on Shodan.

**Choice 2: Use a proprietary tunnel or mesh VPN.**

Tailscale, Cloudflare Tunnel, ZeroTier, ngrok, and their many competitors. These work well. But they require:

- An account with a company.
- Authentication through Google, GitHub, or a proprietary identity provider.
- Acceptance that the company owns the device graph, the access policies, and the identity of every machine.
- Dependency on the vendor's continued operation, pricing, and business decisions.

The vendor is not the *transport* — it's the *authority*. If the vendor disappears, your network doesn't just lose connectivity; it loses its definition of who is allowed to talk to whom.

**Choice 3: Build it yourself.**

Run your own VPN, manage your own certificates, deal with dynamic DNS, deal with CGNAT, deal with NAT traversal, deal with relay infrastructure, deal with revocation, deal with offline state. This works, but only for someone who is already an expert. Normal people cannot do this.

## 4.3 Why this matters more than it sounds

The obvious framing is "this is annoying." The real framing is: **the ability to reach your own devices has become a subscription.**

A decade ago, if you wanted to reach your home server, you opened a port or ran a VPN. Both were awkward, but they were *yours*. Today, the easy path is to sign up for a service. The service works beautifully. But you don't own your network anymore. You're renting the ability to reach your own stuff.

This is the same story as email, and the same story as social media, and the same story as every other layer of the internet where convenience has slowly become dependence. It's not a conspiracy; it's just how products work. But it means the current state of the world has a specific cost that's rarely named: **you don't own your digital relationships.**

## 4.4 Why alternatives don't fully solve it

**"Just use Tailscale."**

Tailscale is an excellent product. It also is a company. It runs a coordination server that is the source of truth for your device graph. If Tailscale changes its terms, or gets acquired, or shuts down a feature you depend on, or stops being able to operate in your jurisdiction, your network is affected. You can self-host Headscale, but then you're running infrastructure — you've swapped one problem for another.

Tailscale's identity model is account-based. That works for consumers. It's awkward for self-hosting, and it's problematic for applications that want to authorize based on *device identity* rather than *user identity*. And the underlying protocol is proprietary: third parties can't implement it, competitors can't speak it, and you can't switch providers without rebuilding your network.

**"Just use Cloudflare Tunnel."**

Cloudflare Tunnel lets a local machine connect outbound to Cloudflare, so you don't need a public IP. It works well. But it makes Cloudflare part of the access path. If Cloudflare changes its terms, filters the wrong traffic, has an outage, or exits the business, your access path goes with it.

**"Just build your own VPN."**

This works. It's also the reason self-hosted connectivity has remained a niche hobby rather than a mainstream capability. Running your own VPN requires expertise that most people don't have, and even for people who do have it, it means reimplementing NAT traversal, relay fallback, revocation, and offline state on your own.

None of these alternatives is wrong. Each is a good choice for some people. But none of them solves the underlying problem: **there is no portable, open, vendor-neutral way to establish and maintain identity and authorization between your devices.**

## 4.5 The insight

The insight behind Grid Network is that **connectivity is not a feature. It's infrastructure.** It should be a shared, audited, portable primitive that every project can consume — the same way they consume TLS for encryption, HTTP for requests, or DNS for resolution.

The reason this hasn't happened yet is that connectivity has three parts that are hard to standardize:

1. **Identity.** Who is this device?
2. **Authorization.** What is it allowed to do?
3. **Reachability.** Where is it right now?

Each of these is a distinct problem, and the current landscape tends to conflate them. When they are separated, each can be standardized independently.

## 4.6 Why this is hard

A reasonable skeptic might say: "This sounds like a solved problem. WireGuard exists. NAT traversal techniques exist. Relays exist. What's new?"

The answer is that all of these pieces exist, but none of them *coordinate*. Specifically:

- **Identity must survive location changes.** Today, everything online is identified by where it is. If the location changes, the identity breaks.
- **Authorization must work offline.** If your device is offline for six months, the network shouldn't forget you exist, but it also shouldn't keep granting you access forever.
- **Intermediaries must be untrusted.** A rendezvous server must not decide authorization. A relay must not grant access.
- **No single party must be the authority.** There must be no central server whose disappearance ends the network.
- **The result must be portable.** Your identity, relationships, and authorizations must survive any change of infrastructure provider.

Each of these constraints rules out a class of easy solutions. What remains is more complex than a naive design. But the complexity is in the protocol, not in the user experience.

---

# Part 5 — The Solution

## 5.1 What Grid Network is

Grid Network is a **control plane for identity, authorization, and reachability** that sits above whatever networking already exists.

It is not a VPN. It is not a tunnel. It is not a replacement for WireGuard, IPv6, or any transport protocol. It is a layer that answers questions *about* devices and their permissions, using signed objects that participants hold and verify themselves.

## 5.2 The three questions

- **Who is this?** — A cryptographic identity, controlled by the participant.
- **What is it allowed to do?** — A signed authorization, verified locally.
- **Where can I find it?** — An ephemeral reachability record, refreshed as networks change.

Every question is answered by signed objects. No answer requires contacting a central authority.

## 5.3 What Grid Network is not

- **Not a decentralized VPN.** A VPN is a transport. Grid Network is a control plane above transports.
- **Not a DNS replacement.** DNS maps names to addresses. Grid Network maps identities to reachability, with authorization.
- **Not an anonymity network.** Peers are identified. Metadata is visible to infrastructure operators. By design.
- **Not a blockchain.** No global consensus, no ledger, no mining, no token.
- **Not a peer-to-peer file system.** No distributed storage.
- **Not a company.** No operator, no owner, no central authority.
- **Not a Tor / I2P / Freenet replacement.** Those provide anonymity through routing.

## 5.4 Five key design properties

**Property 1 — Identity is portable.** A device's identity is a cryptographic keypair. It does not depend on any account, any server, any provider, or any vendor.

**Property 2 — Authorization is local.** A device verifies authorization itself, using state it holds locally. This means authorization works offline, works through network partitions, works when the infrastructure is unreachable.

**Property 3 — Reachability is ephemeral.** Where a device currently is, is not part of its identity. It's a hint, refreshed as networks change.

**Property 4 — Infrastructure is untrusted.** Rendezvous servers, relays, and any other infrastructure can be operated by anyone, including parties the user does not trust.

**Property 5 — The protocol is open.** No proprietary component. Any implementation can speak to any other.

## 5.5 The core security invariant

> Given a set of locally trusted anchors, authenticated protocol objects, known revocations, accepted chain state, and recorded observation history, a verifier must be able to deterministically establish the identity, authorization, validity, and freshness state of a peer **as of the verifier's most recent observation**, without contacting an authority.

This means:

- Rendezvous infrastructure cannot define identity
- Relays cannot define authorization
- DNS cannot define identity
- IP addresses cannot define identity
- WireGuard keys cannot by themselves define application authorization
- Temporary pairing codes cannot become permanent credentials

---

# Part 6 — Architecture and Layers

## 6.1 Conceptual architecture

```
┌──────────────────────────────────────────────┐
│                  Application                 │
├──────────────────────────────────────────────┤
│          Grid Protocol (Layer 1)             │
│  Identity / Authorization / Reachability     │
├──────────────────────────────────────────────┤
│          Connectivity (Layer 3)              │
│  Direct / NAT traversal / Relay / Multipath  │
├──────────────────────────────────────────────┤
│                  Transport                   │
│           WireGuard / QUIC / TCP             │
└──────────────────────────────────────────────┘
```

Identity and authorization are independent of transport.

## 6.2 The four-layer project model

```
┌──────────────────────────────────────────────────────────┐
│  LAYER 4 — STRATEGY                                       │
│  Vision, ecosystem, roadmap                              │
├──────────────────────────────────────────────────────────┤
│  LAYER 3 — CONNECTIVITY ARCHITECTURE                     │
│  Path abstraction, relay model, future multipath         │
├──────────────────────────────────────────────────────────┤
│  LAYER 2 — SECURITY & IMPLEMENTATION                     │
│  Threat model, verifier rules, parser requirements       │
├──────────────────────────────────────────────────────────┤
│  LAYER 1 — PROTOCOL KERNEL                               │
│  Identity, authorization, reachability, cryptographic    │
│  objects, and the verification model                     │
└──────────────────────────────────────────────────────────┘
```

Each layer is independent. Layer 1 does not depend on Layer 3; Layer 3 consumes Layer 1. Layer 4 does not constrain Layer 1.

**Rule: layers must not cross.** No Layer 1 document should contain Layer 2 content.

## 6.3 The authority chain

```
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
```

Rendezvous and relay infrastructure operate **outside** the authority chain.

## 6.4 Stream model

All objects are organized in streams — ordered sequences of cryptographically linked objects.

- **One identity stream per principal** — identity documents, key revocations, relationships, rendezvous manifests
- **One authorization stream per Authorization Key** — grants, leases, revocations, all sequencing together
- **One reachability stream per device** — reachability records
- **One service stream per service** — service records

**Critical invariant:** A verifier MUST NOT compare sequence numbers from different streams.

## 6.5 Cryptography

- Ed25519 signatures
- SHA-256 hashes
- Deterministic CBOR encoding with strict canonicalization
- Domain separators prevent signature transplant
- Object IDs and payload IDs use distinct framing

## 6.6 The verifier model

A verifier must be able to determine all state without contacting an authority. This drives:

- Offline verification (signed objects held locally)
- Relative validity for leases (duration from verifier's observation)
- `max_offline_tolerance` (per-grant bound on offline freshness)
- Revocation as state, not event

## 6.7 Failure semantics core

**Core principle:** Failure of communication, discovery, synchronization, or transport MUST NOT silently become a change in identity or authorization state.

- Authorization failures are **fail-closed**
- Connectivity failures are **availability-preserving**

---

# Part 7 — The Protocol

Full normative text is `PROTOCOL.md` v0.6.2. This part summarizes every section.

## 7.1 Abstract (§1)

Grid Network is an open protocol for establishing persistent, mutually authenticated relationships between machines and services without requiring permanent accounts, centralized identity providers, or fixed network locations.

## 7.2 Core Security Invariant (§2)

See Part 5.5.

## 7.3 Design Goals (§3)

**Primary:**
1. Persistent cryptographic identity
2. Replaceable physical devices
3. Explicit peer relationships
4. Scoped authorization
5. Short-lived authorization leases
6. Terminal revocation
7. Key rotation
8. Offline verification
9. Replaceable rendezvous infrastructure
10. Transport independence
11. Human-friendly initial pairing
12. Self-hostable infrastructure
13. No mandatory central account provider
14. Deterministic security state
15. Interoperable implementations

**Secondary:** Multiple devices per principal, multiple services per device, service-specific authorization, temporary guests, delegated administration, groups, multiple rendezvous providers, direct P2P, relay fallback, local-first operation, identity portability, hardware-backed keys.

## 7.4 Non-Goals (§4)

Not a replacement for WireGuard, not a general-purpose VPN, not a global DNS replacement, not a universal application authorization framework, not a blockchain, not a global identity registry, not a mandatory centralized account system, not a mandatory DHT, not a permanent network locator, not a substitute for application-level authentication, not an anonymity network, not a public endpoint directory, not a global event log, not a guarantee that direct connectivity always succeeds.

## 7.5 Peer Principal (§6)

A durable logical identity. Not one machine, one OS, one device key, or one service. Survives replacement of individual devices.

```
Principal: Dad
 ├── Home Server
 │    ├── Jellyfin
 │    └── File Service
 ├── Laptop
 └── Phone
```

## 7.6 Peer Principal ID (§7)

```
peer:v1:7f3a9c2e5d91b0a4c7e8126fa31d449b
```

Opaque, randomly generated, not self-certifying. The identity document binds the ID to the principal's identity root.

**Advantages:**
- Identity-root rotation does not change the Peer ID
- Provisioning can occur before key generation
- Cryptographic constructions can change in future versions
- Identifiers do not expose the construction
- Relationships remain stable through root-key replacement

## 7.7 Identity Root (§8)

Highest cryptographic authority for a principal. Used to establish the identity document, authorize device/service keys, delegate authorization authority, rotate subordinate keys, revoke subordinate keys, recover from subordinate-key compromise.

Should not normally participate in routine network sessions. Ideally remains offline or hardware-protected.

## 7.8 Key Roles (§9)

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

| Role | Owner | Purpose |
|------|-------|---------|
| Identity Root | Principal | Signs identity documents, relationship assertions, key delegations; revokes subordinate keys |
| Device Key | One device | Authenticates a device; signs reachability records |
| Service Key | One service | Authenticates a service; signs service records |
| Authorization Key | Principal or delegated authority | Signs grants, leases, revocations in its stream |
| Recovery Key | Principal | Future: threshold or offline recovery |
| Relay Authority Key | Relay coordinator | Signs relay tickets |
| Relay Node Key | Relay operator | Authenticates a relay endpoint |

**Non-reuse rule:** A single private key MUST NOT be used for more than one role.

Minimum required separations:
- Identity Root separate from Device Key
- Identity Root separate from Authorization Key
- Device Key separate from Service Key
- Any role separate from Recovery Key

## 7.9 Identity Documents (§10)

```
IdentityDocument {
    domain_separator   = "grid/identity-document/v1"
    sequence
    previous_hash?
    chain_hash
    signature

    peer_id
    identity_root
    authorized_keys : set<KeyBinding>
    device_bindings : set<DeviceBinding>
    service_bindings : set<ServiceBinding>
    issued_at
    not_before
    expires_at
}
```

Key collections are canonical sets: ordered by key identifier (lexicographic byte comparison), duplicates forbidden.

Identity documents occupy `stream:identity`. Linear signed history: Document 1 → Document 2 → Document 3.

Two documents with the same `peer_id` and `sequence` but different `chain_hash` values constitute a fork. Resolution follows §54.

## 7.10 Relationship (§12)

Recognition between two principals is expressed by a pair of independently signed `RelationshipAssertion` objects, one published by each principal.

Each principal publishes its own assertion in its own `stream:identity`. No object spans both streams. Bilateral recognition is a **verifier-derived state**, not a property of any single object.

### RelationshipAssertion

```
RelationshipAssertion {
    domain_separator   = "grid/relationship-assertion/v1"
    sequence
    previous_hash?
    chain_hash
    signature

    relationship_id
    subject_principal
    issued_at
    not_before
    expires_at?
}
```

- Signed by the issuer's Identity Root
- Published in the issuer's `stream:identity`
- `subject_principal` is the other principal whose recognition this assertion names

**Semantics:** States "The issuer recognizes `subject_principal` under `relationship_id`." Unilateral. Does not itself establish `RECOGNIZED`.

### RelationshipTermination

```
RelationshipTermination {
    domain_separator   = "grid/relationship-termination/v1"
    sequence
    previous_hash?
    chain_hash
    signature

    relationship_id
    reason
    terminated_at
}
```

- Signed by the terminating principal's Identity Root
- Published in the terminating principal's `stream:identity`
- Unilateral. Either principal may terminate.
- On acceptance, the relationship for `relationship_id` transitions to `TERMINATED`.

### Verifier-derived relationship state

```
PENDING     iff exactly one assertion is accepted

RECOGNIZED  iff both assertions are accepted,
            AND neither assertion is expired,
            AND no accepted RelationshipTermination for R

TERMINATED  iff an accepted RelationshipTermination for R exists

UNKNOWN     otherwise
```

- `PENDING` does not contribute to authorization
- `RECOGNIZED` is required for authorization
- `TERMINATED` is terminal; new relationship requires new `relationship_id`

**Rationale for per-principal assertions:**
- Stream purity. Every object lives in exactly one stream.
- Unilateral assertion. Either principal may publish independently.
- Unilateral termination. Either may terminate unilaterally.
- No invented stream. No new sequence space required.
- Recognition without coercion.

## 7.11 Grant (§13)

Directional.

```
Dad → Ryan: jellyfin.stream
```

Contains: relationship ID, issuer, subject, device scope (optional), capabilities, resources, constraints, lease policy, issuance info, signature.

Grants are immutable objects within the Authorization Key's authorization stream. Any change produces a new grant with a new `grant_id`.

## 7.12 Lease (§14)

A Lease proves that a grant is currently valid.

```
Relationship  "We recognize each other."
Grant         "You are authorized for X."
Lease         "That authorization is currently valid."
```

Typical durations:

| Capability | Typical lease |
|------------|---------------|
| Jellyfin streaming | 30 days |
| File access | 7 days |
| SSH | 1 hour |
| Admin SSH | 15 minutes |

When a lease expires, the peer is unauthorized until a new lease is issued. A peer returning from a long offline period does NOT inherit the expired lease.

## 7.13 Capabilities (§15)

```
Capability {
    namespace : string    // org.jellyfin
    action    : string    // stream, admin, read
    resource  : string    // library:movies
}
```

Namespace rules: lowercase ASCII, dot-separated, at least one dot, first component reverse-DNS.

Unknown namespace handling:
- MUST validate well-formedness
- MUST NOT grant network-level authorization based on unknown namespace alone
- MAY pass through to an application that understands it
- MUST NOT reject a grant solely for containing unknown namespaces

Constraints: canonical map string → string, max 32 entries, values max 1024 bytes.

## 7.14 Authorization Policy (§16)

```
Grant:
    capability = org.jellyfin.stream
    lease_duration = 30 days
    max_offline_tolerance = 30 days
```

Offline tolerance is per-grant, evaluated separately from lease validity.

## 7.15 Network vs Application Authorization (§17)

- **Network authorization:** May this peer connect?
- **Application authorization:** Once connected, what may the application do?

The grid layer does not replace application access control.

## 7.16 Revocation (§18–§20)

**Revocation is terminal.** A revoked object cannot become valid again. Reauthorization creates a new object.

### Revocation hierarchy

```
Lease → Grant → Device → Authorization Key → Principal
```

| Revocation | Invalidates |
|-----------|-------------|
| Revoke lease | One authorization period |
| Revoke grant | The grant and future leases derived from it |
| Revoke device | Device-specific authorization and services |
| Revoke authorization key | Objects signed at or after `effective_sequence` |
| Revoke principal | The principal's entire identity |

### KeyRevocation

```
KeyRevocation {
    domain_separator   = "grid/key-revocation/v1"
    sequence
    previous_hash?
    chain_hash
    signature

    key_id
    effective_sequence
    revoked_at
    reason
    replacement_key_id?
}
```

**Semantics:**
- Signed by the Identity Root (not the revoked key)
- Occupies the Identity Root's identity stream
- `effective_sequence` refers to a position in the revoked Authorization Key's authorization stream
- Objects signed by `key_id` at or after `effective_sequence` are invalid

**Example:**
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

The root's seq 202 has no relationship to `effective_sequence = 103`. They refer to different streams.

`effective_sequence = 0` invalidates the entire authorization history signed by K.

## 7.17 Authorization-Key Compromise (§21)

Recovery:
1. Identity Root signs `KeyRevocation` with `effective_sequence`
2. Objects signed by the compromised key at or after `effective_sequence` are invalid
3. Principal issues new Authorization Key
4. Legitimate grants re-issued under new key

**Normative:** A revocation of an Authorization Key is an identity-authority operation and MUST NOT require the compromised key to sign its own revocation.

## 7.18 Identity Root Compromise (§22)

V1 treats the root as the highest trust anchor. Advanced recovery mechanisms deferred to V2:
- Offline recovery keys
- Hardware-backed roots
- Threshold recovery
- Multi-party approval
- Social recovery

## 7.19 Key Rotation (§23)

V1 requirement. Rotation preserves the Peer Principal ID. The identity history establishes the transition. `IdentityContinuity` (§54.5) is used for orderly root transition.

## 7.20 Pairing (§24–§26)

```
Device A displays:  481729
Device B enters:    481729
```

The six-digit value is a temporary human coordination mechanism, not a credential.

**V1 pairing MUST use an established PAKE (SPAKE2 or CPace).**

Final protocol must specify: exact PAKE, transcript construction, identity binding, protocol version and context binding, replay protection, code lifetime, retry limits, enumeration resistance.

**Transcript binding:** protocol version, peer identities, PAKE identities, capabilities being requested, pairing context, rendezvous session identifier.

Pairing code has ~20 bits of entropy. MUST NOT be treated as sufficient cryptographic authentication. Short-lived, single-use, rate-limited, invalidated after success, timeout, or excessive failures.

## 7.21 Human Verification (§27)

Devices may display a verification value derived from the pairing transcript:

```
8341 2910
```

## 7.22 Permanent Identity References (§28)

```
Identity Reference ≠ Pairing Invitation ≠ Authorization Grant ≠ Recovery Credential
```

## 7.23 Grid URI (§29)

```
grid://v1/...
```

Grammar MUST be formally specified in ABNF. Parsing MUST be strict. Must distinguish identity references, temporary invitations, capability requests, and rendezvous hints. A permanent URI MUST NOT contain a mandatory fixed rendezvous dependency.

## 7.24 Rendezvous (§30–§31)

Rendezvous provides discovery. It has **no identity authority**.

### Rendezvous roles

| Role | Purpose |
|------|---------|
| Publication | Accepts authorized reachability publications |
| Replica | Stores signed copies |
| Cache | Fetches and caches on demand |
| Bootstrap | Helps peers find manifests |
| Relay coordinator | Issues relay tickets |
| Freshness source | Attests to authorization state, only when explicitly authorized |

A rendezvous server is not a freshness source merely because it stores objects.

### Principal Rendezvous Manifest

```
RendezvousManifest {
    domain_separator   = "grid/rendezvous-manifest/v1"
    sequence
    previous_hash?
    chain_hash
    signature

    peer_id
    generation
    active_until
    recovery_until
    rendezvous_set : set<RendezvousEntry>
    issued_at
}
```

- Signed by the principal's Identity Root
- Occupies the principal's `stream:identity`
- States: Active, Recovery, Expired

### Operator Manifest

```
OperatorManifest {
    domain_separator   = "grid/operator-manifest/v1"
    sequence
    previous_hash?
    chain_hash
    signature

    operator_id
    operator_root
    nodes
    federation_peers
    issued_at
    expires_at
}
```

- Signed by the operator's Identity Root
- Occupies the operator's `stream:identity`
- Not an assertion about any principal, service, or authorization stream

### Rendezvous invariant (normative)

> Neither a Principal Rendezvous Manifest nor an OperatorManifest grants authority over any principal, service, authorization stream, or reachability state. The operator's Peer ID is simply the operator's identity; operating rendezvous infrastructure does not create protocol authority.

### Rendezvous trust model

A malicious rendezvous server may provide stale or false endpoints, suppress endpoint information, observe metadata, or attempt DoS. It MUST NOT be able to forge identity, authorization, or revocation; create a valid lease; or decrypt transport traffic.

### Rendezvous evolution

| Version | Capability |
|---------|-----------|
| V1 | HTTPS rendezvous |
| V2 | Multiple interchangeable rendezvous servers |
| V3 | Federation |
| V4 | Peer-assisted gossip |
| V5 | DHT, if required |

## 7.25 Reachability (§32)

```
ReachabilityRecord {
    domain_separator   = "grid/reachability-record/v1"
    sequence
    previous_hash?
    chain_hash
    signature

    peer_id
    device_id
    service_id?
    endpoint
    transport
    observed_at
    expires_at
}
```

Each device maintains a linear chain. Higher `sequence` supersedes lower. A cached endpoint is a hint, not a destination.

## 7.26 Relays (§33)

Relays are transport infrastructure.

```
RelayTicket {
    domain_separator   = "grid/relay-ticket/v1"
    sequence
    previous_hash?
    chain_hash
    signature

    ticket_id
    source_device
    destination_device
    service_link_id
    requested_capability
    issued_at
    expires_at
    max_bytes
    max_rate_bps
}
```

A RelayTicket authorizes transport use only. It cannot create authorization.

## 7.27 Transport (§34)

WireGuard is the preferred initial transport.

## 7.28 Enforcement (§35)

```
Grid daemon → WireGuard configuration → Firewall → Reverse proxy → Application
```

## 7.29 Service Discovery (§36)

```
ServiceRecord {
    domain_separator   = "grid/service-record/v1"
    sequence
    previous_hash?
    chain_hash
    signature

    service_id
    peer_id
    device_id
    service_type
    endpoint
    supported_capabilities : set<CapabilityNamespace>
    metadata
    issued_at
    expires_at
}
```

Service records do not grant access.

## 7.30 Offline Operation (§37)

```
KNOWN / TRUSTED / OFFLINE / LAST SEEN: ...
```

## 7.31 Lease Expiration (§38)

```
Lease expires → No new lease → Access denied
```

## 7.32 Revocation Propagation (§39)

V1 supports:
- **Pull on reconnect**
- **Opportunistic synchronization**

A verifier that has not received a revocation may temporarily continue honoring a valid lease, subject to `max_offline_tolerance`.

## 7.33 Time Semantics (§40)

### Relative validity

```
valid_from  = verifier first-acceptance time
valid_until = valid_from + duration
```

Deterministic per verifier. Does not require synchronized wall clocks.

### Absolute validity

Verifiers apply the protocol-defined clock-skew tolerance.

### Validity by object class

| Object | Validity |
|--------|----------|
| Identity Document | Absolute |
| Rendezvous Manifest | Absolute |
| Grant | Absolute for issuance; policy controls freshness |
| Lease | Relative by default; absolute MAY be supported |
| Reachability Record | Relative |
| Revocation | Terminal |

### Clock skew

```
MAX_CLOCK_SKEW = 5 minutes
```

### Issued-at ordering

```
issued_at(N+1) >= issued_at(N)
```

### Authorization freshness

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

### Definition of authorization refresh

A successful refresh requires an authenticated exchange with the grant issuer or an explicitly designated freshness source. Local re-evaluation does not count. A rendezvous server or relay MUST NOT constitute a freshness source merely because it stores or forwards signed objects.

### Revocation interaction

When a verifier receives a valid revocation:
1. It is added to local state
2. Affected objects are re-evaluated
3. Invalidated authorization ceases to be honored
4. A previously valid lease MUST NOT regain validity

### Revocation as state, not event

A revocation is a state assertion. If received before its target, it MUST remain effective when the target is subsequently received.

## 7.34 Cryptographic Object Encoding (§41–§45)

See Part 8.

## 7.35 Trust Anchors (§46)

```
peer_id
trusted_identity_root
accepted_identity_state  (sequence + chain_hash)
acceptance_time
```

## 7.36 Verifier Local State (§47)

### Principal state

```
PrincipalState {
    peer_id
    trusted_identity_root
    accepted_identity_sequence
    accepted_identity_chain_hash
    identity_acceptance_time
}
```

### Key state

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


### Relationship state

```
RelationshipState {
    relationship_id
    local_principal
    remote_principal
    state          // UNKNOWN | PENDING | RECOGNIZED | TERMINATED
    assertion_local?
    assertion_remote?
    termination?
}
```

### Grant state

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

### Lease state

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

### Chain state

```
ChainState {
    issuer
    stream_id
    accepted_sequence
    accepted_chain_hash
    sync_state
}
```

`sync_state` ∈ { `IDLE`, `SYNCING`, `FORKED` }.

### Reachability state

Soft state. Loss MUST NOT invalidate identity, relationship, grant, or revocation state.

### Rendezvous state

Infrastructure state.

### Observation history and monotonic time

For relative validity, the verifier MUST retain `first_observed_at` (monotonic).

Implementations MUST use a monotonic local clock for elapsed-duration calculations.

### Processing order

1. Decode canonical object
2. Validate domain separator
3. Validate signature
4. Validate issuer authority
5. Validate object sequence
6. Validate chain continuity
7. Detect rollback, fork, extension, or gap
8. Apply key transitions
9. Apply revocations
10. Apply relationship transitions
11. Apply grants
12. Apply leases
13. Update authorization freshness
14. Update reachability state if applicable
15. Commit resulting local state

**Note:** Steps 1–9 are logically ordered validation phases, not necessarily separate persistence operations. Verification MUST NOT mutate accepted state; commitment is the only mutation.

### Atomic state updates

Security-significant object processing MUST be atomic. Validation is pure with respect to accepted state; commitment is the only mutation.

### Fork handling

Upon detecting a fork, the stream enters `FORKED` state.

### Gap handling

A gap occurs when an incoming object has sequence greater than `accepted_sequence + 1`. A gap is **not** a fork.

### Case summary

| Incoming object | Condition | Result |
|-----------------|-----------|--------|
| Rollback | sequence < accepted | Reject |
| Fork | sequence == accepted, chain differs | Enter `FORKED` |
| Extension | sequence == accepted + 1, predecessor matches | Accept |
| Gap | sequence > accepted + 1 | Enter `SYNCING` |

### Local verification invariant

> Given locally trusted anchors, authenticated objects, known revocations, accepted chain state, and recorded observation history, the verifier can deterministically establish principal, authorization, revocation, and freshness state without contacting an authority.

## 7.37 Security State Machines (§48)

### Relationship

```
UNKNOWN → CURRENT → { SUPERSEDED (terminal), EXPIRED (terminal) }
```

Verifier-derived relationship state:
```
UNKNOWN → PENDING → RECOGNIZED → TERMINATED (terminal)
```

### Grant

```
UNKNOWN → GRANTED → { EXPIRED (terminal), REVOKED (terminal) }
```

V1 grant validity is absolute.

### Lease

Two independent predicates: lease validity and authorization freshness.

```
UNKNOWN → VALID
VALID → { EXPIRED (terminal), REVOKED (terminal), STALE }
STALE → VALID (on successful refresh)
```

Authorization requires: lease `VALID`, grant `GRANTED`, relationship `RECOGNIZED`, key `ACTIVE` or `SUPERSEDED`, no applicable revocation.

### Authorization Key

```
UNKNOWN → ACTIVE → { SUPERSEDED → REVOKED (terminal), REVOKED (terminal) }
```

- `ACTIVE → SUPERSEDED` is established only by an accepted identity document
- `REVOKED`: no longer trusted for objects at or after `effective_sequence`. Objects before it remain subject to ordinary rules.

### Device Key

```
UNKNOWN → ACTIVE → { REVOKED (terminal), RETIRED (terminal) }
```

### Service Record

```
UNKNOWN → CURRENT → { SUPERSEDED (terminal), EXPIRED (terminal) }
```

### Reachability Record

```
UNKNOWN → CURRENT → { SUPERSEDED (terminal), EXPIRED (terminal) }
```

### Cross-object constraints

- A grant whose relationship is not `RECOGNIZED` MUST NOT contribute to effective authorization
- A lease whose grant is not `GRANTED` MUST NOT contribute
- A lease whose Authorization Key is `REVOKED` with `effective_sequence` ≤ lease sequence MUST NOT contribute
- A reachability record signed by a `REVOKED` Device Key MUST NOT be accepted as current
- A service record signed by a `REVOKED` Service Key MUST NOT be accepted as current

## 7.38 Authority Domains (§49)

### Identity authority
**Source:** Identity Root
**Scope:** Identity document, subordinate keys, device bindings, service bindings, relationship assertions and terminations, rendezvous manifest
**Boundary:** Does not extend to authorization

### Authorization authority
**Source:** Authorization Key delegated by Identity Root
**Scope:** Grants, leases, and revocations in its stream
**Boundary:** Does not extend to identity. Cannot revoke itself.

### Service authority
**Source:** Service Key
**Scope:** Service records

### Reachability authority
**Source:** Device Key
**Scope:** Reachability records

### Rendezvous authority
**Source:** None. Rendezvous has no signing authority.

### Cross-domain rules

1. No domain may exercise authority belonging to another
2. Delegation is explicit
3. Possession is not authority
4. Boundaries are enforced at verification time
5. Revocation authority does not depend on the revoked key

## 7.39 Threat Model (§50)

See Part 9.

## 7.40 Compromise Model (§51)

See Part 9.

## 7.41 Service Identity (§52)

### Service Identity

```
service_id  = opaque identifier
service_key = Ed25519 key pair
```

Stable across device replacement and network changes.

### Service Binding

```
ServiceBinding {
    service_id
    service_public_key
    bound_to     : principal_id | device_id
    issued_at
    expires_at?
}
```

Signed as part of the identity document. Establishes which principal or device speaks for the service.

### Service Link

```
service_link_id = opaque identifier
```

**Referential only.** Not an independently signed object.

Normative:
- N1. A Service Link is not an authorization object
- N2. MUST NOT contain capabilities, authorization constraints, lease validity
- N3. Presence, validity, or recognition MUST NOT authorize access
- N4. Authorization established exclusively through Grant and Lease state
- N5. Referential identifier; not signed, mutable, or independently authoritative
- N6. If two objects reference the same ID but disagree, the objects are the source of truth
- N7. An attacker who invents a `service_link_id` gains nothing

### Service host migration

Service moves from one device to another **within the same principal**.

Effect on authorization:
- Grants and leases whose scope does not constrain the hosting device remain valid
- Grants and leases whose scope constrains the hosting device are evaluated against their scope
- Migration MUST NOT widen authorization

### Service ownership transfer

**V1 does not support service ownership transfer.**

### Service lifecycle summary

| Object | Signed by | Purpose |
|--------|-----------|---------|
| Service Identity | (n/a) | Service identity |
| Service Binding | Identity Root (or delegated) | Binds identity to principal/device |
| Service Link | (n/a) | Referential identifier |
| Grant | Authorization Key | Authorizes subject |
| Lease | Authorization Key | Proves current validity |
| Service Record | Service Key | Current endpoint and metadata |
| Reachability Record | Device Key | Current device endpoints |

### Service Record and Reachability Record

- Service Record describes how the service can be reached
- Reachability Record describes where the hosting device can be reached
- Neither overrides the other. Both are used. Neither grants authorization.

## 7.42 Failure Semantics (§53)

### General invariants

- **F1** No failure silently grants authorization
- **F2** No failure silently extends authorization
- **F3** No failure silently changes identity state
- **F4** Availability is preserved where possible
- **F5** Security-relevant failure conditions are represented in local state
- **F6** Failures are recoverable where specified; terminal where specified

### Taxonomy

Discovery (§53.3), synchronization (§53.4), integrity (§53.5), validity (§53.6), fork (§53.7), freshness (§53.8), local (§53.9), pairing (§53.14).

### Discovery failures

- **53.3.1 Rendezvous unreachable.** Retry; rotate to next. State unchanged.
- **53.3.2 Endpoint unreachable.** Failed connection is not evidence the peer is offline, compromised, or unauthorized. Record's protocol state unchanged. Local observation is soft.
- **53.3.3 Conflicting reachability records.** Fork in reachability stream. Neither branch used. Resolution per §54.
- **53.3.4 Malicious rendezvous.** Reject object; do not alter state.

### Synchronization failures

- **53.4.1 Stream gap.** `SYNCING` state. Use last accepted state. Gap MUST NOT become `FORKED`.
- **53.4.2 Partial synchronization.** Use locally known objects for decisions determinable from them. Absent objects not assumed.
- **53.4.3 Network partition.** Cached objects evaluated against normal rules. Leases may become `STALE`.

### Integrity failures

- **53.5.1 Malformed object.** Reject. State unchanged.
- **53.5.2 Invalid signature.** Reject.
- **53.5.3 Unknown object type.** Reject.
- **53.5.4 Unknown issuer.** Reject as untrusted.

### Validity failures

- **53.6.1 Expired.** Excluded. State `EXPIRED`.
- **53.6.2 Revoked.** Excluded. State `REVOKED`.
- **53.6.3 Superseded.** Excluded. State `SUPERSEDED`.
- **53.6.4 Unknown revocation.** Cache as state assertion. MUST remain effective when target is subsequently received.

### Fork failures

- **53.7.1 Conflicting stream states.** Stream `FORKED`. Use last accepted state.
- **53.7.2 Conflicting identity documents.** Identity stream `FORKED`. Use last accepted identity state.
- **53.7.3 Authorization continuity during identity fork.**
  - Authorization state derived from last accepted identity state remains locally recognized
  - MUST NOT incorporate assertions from either disputed branch
  - Existing grants and leases continue to be evaluated against last accepted identity state
  - No new authorization state dependent on disputed branch may be accepted

Invariant: **accepted state remains accepted; disputed state contributes nothing.**

### Freshness failures

- **53.8.1 Authorization refresh failure.** `last_successful_authorization_refresh` not updated. Leases may become `STALE`.
- **53.8.2 Freshness source unavailable.** MUST NOT substitute undesignated sources.

### Local failures

- **53.9.1 Local storage loss.** All state lost; return to `UNKNOWN`.
- **53.9.2 Clock forward jump.** Relative validity unaffected. Absolute validity may misclassify.
- **53.9.3 Clock backward jump.** `issued_at` monotonicity violations rejected as temporal-policy violations, NOT malformed.
- **53.9.4 Monotonic clock unavailable.** MUST NOT substitute wall clock.

### Summary table

| Failure | Authorization impact | State impact | Recovery |
|---------|---------------------|--------------|----------|
| Rendezvous unreachable | None | None | Retry; rotate |
| Endpoint unreachable | None | Local observation only | Refresh; alternates |
| Conflicting reachability | None | Stream `FORKED` | External resolution |
| Malicious rendezvous | None | None | Deprioritize |
| Stream gap | Use last accepted state | `SYNCING` | Obtain intermediates |
| Partial sync | Use local state | None | Continue sync |
| Network partition | Leases may become `STALE` | None | Refresh |
| Malformed object | None | None | Discard |
| Invalid signature | None | None | Discard |
| Unknown object type | None | None | Discard |
| Unknown issuer | None | None | Discard |
| Expired object | Excluded | `EXPIRED` | New object |
| Revoked object | Excluded | `REVOKED` | Issue new |
| Superseded object | Excluded | `SUPERSEDED` | Use newer |
| Unknown revocation | None | Revocation cached | Apply on receipt |
| Fork | Use last accepted state | `FORKED` | §54 |
| Identity fork | Accepted state effective | Identity stream `FORKED` | §54 |
| Refresh failure | None until tolerance elapses | `STALE` | Successful refresh |
| Freshness source unavailable | As above | As above | Retry designated source |
| Local storage loss | All authorization lost | Return to `UNKNOWN` | Re-pair |
| Clock forward jump | Possible absolute misclassification | History unchanged | Restore clock |
| Clock backward jump | Possible absolute misclassification | History unchanged | Restore clock |
| Monotonic clock unavailable | Relative validity cannot be evaluated | None | Environmental |
| Pairing failure | None | None | Discard; retry |

### Fail-closed vs. availability-preserving

**Fail-closed (authorization):** missing information MUST NOT grant authorization; failed refresh ≠ refresh; forked streams contribute nothing; expired/revoked/superseded excluded; gaps not filled by inference; local state loss not reconstructed from untrusted sources; persistent gaps not reinterpreted as forks.

**Availability-preserving (connectivity and discovery):** discovery retries permitted; relay use permitted; reconnections do not require re-validation; cached reachability MAY be used subject to signed validity; alternate rendezvous and endpoints MAY be tried.

### Conformance

1. MUST preserve local state under all failures unless failure is explicitly local
2. MUST NOT interpret any failure as authorization
3. MUST NOT extend validity or freshness based on failed operations
4. MUST represent security-relevant failure conditions in local state
5. MUST apply specified recovery paths
6. MUST NOT invent recovery paths for authorization-relevant decisions
7. MUST NOT conflate distinct failure conditions

### Pairing failures

Failed pairing: attempt discarded; no state created; ephemeral state destroyed; MAY retry with fresh session.

**Invariant:** An incomplete pairing has no partially committed security state.

## 7.43 Reconciliation (§54)

### Scope

Defines reconciliation of conflicting objects in the same stream, synchronization of persistent gaps, conflicting identity documents, conflicting reachability or service records, conflicting rendezvous manifests.

### Principles

- **R1** No new authority
- **R2** Issuer-scoped resolution
- **R3** Explicit resolution
- **R4** Preservation of accepted state until resolution
- **R5** Fail-closed if unresolved
- **R6** Resolution is a stream transition, not an override
- **R7** Resolutions are auditable

### Object classes

1. **StreamResolution** — resolves a fork in a single stream
2. **IdentityContinuity** — establishes continuity across an orderly transition

### StreamResolution

```
StreamResolution {
    domain_separator   = "grid/stream-resolution/v1"
    sequence           // in the resolver's stream
    previous_hash?
    chain_hash
    signature

    issuer
    stream_id          // the disputed stream
    disputed_sequence
    disputed_hashes
    accepted_hash
    resolution_reason
    issued_at
    not_before
    expires_at
}
```

**Resolution authority:**

| Disputed stream | Resolution authority |
|-----------------|----------------------|
| `stream:identity` | Identity Root trusted before the fork |
| `stream:authorization:<K>` | Identity Root, or a resolution-authority key delegated before the fork |
| `stream:reachability:<D>` | Identity Root, or the device-authority key delegated before the fork |
| `stream:service:<S>` | Identity Root, or the service-authority key delegated before the fork |

**Normative:**
- A `StreamResolution` MUST be signed by an authority above the disputed stream in the authority hierarchy, trusted by the verifier from state accepted **before** the fork was observed
- A key whose own stream is disputed MUST NOT sign the resolution for that stream
- Trust for the resolution authority is evaluated against the verifier's accepted authority state **at the time the fork was first observed**
- A `StreamResolution` MAY select among already-authenticated disputed branches. It MUST NOT introduce new object contents, authority, capabilities, bindings, or authorization state
- The `sequence` field of a `StreamResolution` refers to the **resolver's** stream. It MUST NOT be numerically compared with `disputed_sequence`

### IdentityContinuity

```
IdentityContinuity {
    domain_separator   = "grid/identity-continuity/v1"
    sequence           = 1
    // previous_hash omitted
    chain_hash                                   // initial_chain_hash of successor stream

    peer_id
    previous_root
    previous_chain_hash                          // terminal chain hash of predecessor stream
    new_root
    continuity_reason
    issued_at
    expires_at

    signature                                    // two-element array [sig_prev, sig_new]
}
```

- `sequence` MUST be exactly 1
- `previous_hash` is omitted
- `chain_hash` is the `initial_chain_hash` of the **successor** identity stream
- `previous_chain_hash` is the terminal `chain_hash` of the **predecessor** identity stream
- `signature` is a two-element array `[sig_prev, sig_new]`, both over the same `signature_input`

**Trust chain requirement:** A chain of `IdentityContinuity` transitions MUST ultimately terminate at an Identity Root that the verifier accepted as trusted **before** the first transition in the chain.

**Recovery from root compromise:** `IdentityContinuity` handles orderly transitions. It does NOT handle root compromise. Recovery is out-of-band.

### RendezvousUpdate

Rendezvous manifests are normal streams. Forks resolved by `StreamResolution` signed by the principal's Identity Root.

### Persistent gaps

Persistent gaps are not forks. Resolved by obtaining missing objects, not by issuing resolution objects.

### Non-stream conflicts

**Ambiguity rule:** If two independently valid signed objects assert incompatible authorization predicates for the same `(subject, service, capability)` and no rule in the Authority Precedence Table resolves the conflict, the verifier MUST NOT authorize the capability.

### Explicit non-mechanisms

- Voting
- Timestamps as resolution
- Availability as resolution
- Preference order among sources
- Peer voting on disputed state
- Automatic resolution
- Transfer of authority between principals without dual signature

### Resolution availability

For orderly transitions: Identity Root available.
For unplanned events: out-of-band recovery, administrative re-acceptance, or terminal abandonment of old Peer ID.

### Conformance

1. MUST NOT resolve `FORKED` by mechanisms other than valid `StreamResolution` or `IdentityContinuity`
2. MUST NOT resolve `SYNCING` by mechanisms other than obtaining intermediates
3. MUST preserve last accepted state until resolution
4. MUST retain disputed artifacts and resolution
5. MUST NOT authorize ambiguous conflicts
6. MUST NOT treat time, availability, source preference, or voting as resolution
7. MUST accept `IdentityContinuity` only with dual signature

## 7.44 Application Integration (§55)

### Principle

Applications consume authenticated identity and authorized connections. They do not receive raw endpoints, relay credentials, or rendezvous URLs.

### Local interface

```
grid.discover()                     → list of known peers
grid.resolve(peer_id)               → peer state
grid.connect(service_link_id, cap)  → local connection handle
grid.authorize(peer_id, capability) → authorization decision
grid.revoke(object_id)              → issue revocation
grid.status()                       → daemon and peer state
```

### Connection handles

```
{
    "connection_id": "random-id",
    "local_url": "http://127.0.0.1:41873",
    "expires_at": "2026-10-04T21:00:00Z"
}
```

The application uses the local URL. It does not receive the underlying endpoint, relay credentials, or peer ID.

### Authorization inputs

When an application requests a connection, the daemon evaluates `authorized` (§40.6). If authorized, a local connection is established. If not, the daemon returns an error.

### Application identity

Applications MAY receive an authenticated Peer Principal ID for the peer on the other end of a connection.

### Enforcement boundary

Enforcement may occur through transport configuration, firewall rules, proxying, or a combination.

### Integration with existing applications

```
Application → grid.connect() → daemon → overlay → peer
```

## 7.45 V1 Scope (§56)

V1 MUST include:

1. Peer Principal identity
2. Opaque Peer IDs
3. Identity Root
4. Device keys
5. Service keys
6. Signed identity documents
7. Key rotation
8. Authorization Keys
9. Grants (immutable)
10. Leases with relative validity
11. Authorization freshness
12. Terminal revocation
13. Key revocation with `effective_sequence`
14. Relationship assertions and terminations
15. Human-mediated QR/copy-paste pairing
16. Established PAKE
17. Canonical object encoding
18. One self-hostable rendezvous service
19. Reachability records
20. Direct connectivity
21. WireGuard integration
22. Offline verification
23. Positive and negative test vectors

Deferrable to V1.1: multi-server rendezvous, relay fallback, service host migration tooling, comprehensive failure test coverage.

## 7.46 Explicitly Deferred Features (§57)

- DHT-based discovery
- Federation between rendezvous servers
- Peer-assisted gossip
- Groups
- Sophisticated recovery (threshold, social, hardware-backed)
- Multipath routing
- Automatic service migration
- Service ownership transfer
- Reputation and liveness scoring
- Advanced metadata protection
- Delegated administration
- Temporary guests

## 7.47 Signing-Authority Matrix (§58)

See Part 8.6.

## 7.48 Implementation Requirements (§59)

### Required components

1. Object encoding and decoding (canonical CBOR)
2. Signature and verification
3. Hash computation
4. Object type dispatch (domain separators)
5. Identity document validation
6. Stream tracking
7. Authority validation
8. Authorization evaluation
9. Failure handling per §53
10. Reconciliation per §54
11. Local trust anchor storage
12. Rendezvous client

### Recommended components

1. Local API server
2. WireGuard integration
3. Reachability publication
4. NAT traversal
5. Relay client

### Interoperability requirements

Two independent implementations MUST interoperate on: canonical encoding, signature verification, identity document validation, stream state management, authorization decisions, failure handling.

### State durability

Trust anchors and accepted stream state MUST be durable. Local observation history for relative validity MUST be durable.

### Cryptographic requirements

Ed25519, SHA-256, deterministic CBOR.

## 7.49 Test Vectors and Conformance (§60)

### Required test vectors

For each object type: canonical encoding, hash, payload hash, signature, verification, tampered field, wrong domain separator, wrong schema version.

### Negative test vectors

Required negative vectors: non-minimal integer encoding, incorrectly ordered map keys, floating-point field, duplicate set entry, set entries out of canonical order, missing required field, extra unknown field, oversized field, replayed object, expired object, revoked object, invalid `previous_hash`, invalid `chain_hash`, wrong issuer for object type, signature from wrong key role, fork at same sequence, gap in stream, non-canonical CBOR encoding.

### Conformance levels

- Level 1: Encoding
- Level 2: Verification
- Level 3: Authorization
- Level 4: Failure handling
- Level 5: Reconciliation

### Vector normative invariant

Where prose and a normative test vector appear to conflict, the specification must be corrected so that prose and vector agree. Test vectors are not an alternative interpretation of ambiguous prose.

### Rejection classes

A conforming implementation MUST reject every negative test vector with the specified rejection class.

## 7.50 Verifier Conformance Scenarios (§61)

### 61.1 Fresh peer

**Initial:** No local state.
**Incoming:** Pairing completes; relationship assertions exchanged; grant and lease received.
**Expected:** Peer `KNOWN`; relationship `RECOGNIZED`; grant `GRANTED`; lease `VALID`. Authorization succeeds.

### 61.2 Offline peer returns

**Initial:** Peer `KNOWN`, `RECOGNIZED`, valid grant and lease.
**Incoming:** Reachability record with new endpoint.
**Expected:** Peer reachable at new endpoint. Identity and authorization unchanged.

### 61.3 Lease expires while offline

**Initial:** Valid lease. Verifier offline past expiry.
**Incoming:** Reachability record. No new lease.
**Expected:** Lease `EXPIRED`. Authorization fails.

### 61.4 Revocation occurs while offline

**Initial:** Valid lease.
**Incoming:** Revocation for the lease.
**Expected:** Lease `REVOKED`. Authorization fails.

### 61.4b Revocation arrives before its target

**Initial:** No knowledge of grant G.
**Incoming:** Revocation for G, then G.
**Expected:** Revocation cached. G rejected on first observation.

### 61.5 Authorization-key compromise

**Initial:** Active Authorization Key K with:
```
seq 100  Grant G1
seq 101  Lease L1 (for G1)
seq 102  Lease L2 (for G1)
seq 103  GrantRevocation (revokes G1)
seq 104  Grant G2
seq 105  Lease L3 (for G2)
seq 106  LeaseRevocation (revokes L3)
```

**Incoming:**
```
Identity Root stream:
seq 201  IdentityDocument
seq 202  KeyRevocation { key_id=K, effective_sequence=103 }
```

**Expected applicability:**

| Seq | Object | Applicable | Reason |
|-----|--------|------------|--------|
| 100 | Grant G1 | yes | before `effective_sequence` |
| 101 | Lease L1 | yes | before |
| 102 | Lease L2 | yes | before |
| 103 | GrantRevocation | no | at `effective_sequence` |
| 104 | Grant G2 | no | after |
| 105 | Lease L3 | no | after |
| 106 | LeaseRevocation | no | after |

**Further state:**
- G1 `GRANTED`
- L1, L2 remain `VALID`
- G2 not applicable; not `REVOKED` — outside trusted window
- L3 not applicable

### 61.6 Key rotation mid-chain

**Initial:** Peer P with trusted root R1, accepted identity stream at sequence N, chain hash `H_old`.
**Incoming:** `IdentityContinuity` object with `previous_root = R1`, `previous_chain_hash = H_old`, `new_root = R2`, `sequence = 1`, dual signature.
**Expected:** Trusted root updated to R2. Successor stream begins at sequence 1. Predecessor stream retained for audit.

### 61.7 Identity fork

**Initial:** Accepted identity state at sequence 10, hash H.
**Incoming:** Identity document at sequence 10, hash H'.
**Expected:** Identity stream `FORKED`. Accepted state (H) remains effective.

### 61.8 Gap in received chain

**Initial:** Accepted sequence 10.
**Incoming:** Object at sequence 15.
**Expected:** Stream `SYNCING`. Authorization uses last accepted state (sequence 10). Verifier attempts to obtain 11–14. Stream does NOT become `FORKED`.

### 61.9 Conflicting rendezvous data

**Initial:** Cached reachability record R1 at endpoint E1.
**Incoming:** Reachability record R2 at same sequence, different chain hash.
**Expected:** Reachability stream `FORKED`. Neither endpoint used.

### 61.10 Stale reachability record

**Initial:** Cached reachability record within validity.
**Incoming:** Attempted connection fails.
**Expected:** Record's protocol state unchanged. Local observation is soft.

### 61.11 Direct path fails, relay succeeds

**Initial:** Peer authorized, reachability record with candidates.
**Incoming:** Direct connection fails; relay path established.
**Expected:** Connection established via relay. Authorization unchanged.

### 61.12 Relay disappears during session

**Initial:** Active session via relay.
**Incoming:** Relay unreachable.
**Expected:** Session disrupted. Verifier attempts direct path.

### 61.13 Grant reissued after terminal revocation

**Initial:** Grant G1 revoked.
**Incoming:** New grant G2 with new `grant_id`, same subject, same capability.
**Expected:** G1 remains `REVOKED`. G2 is `GRANTED`. No state inherited from G1.

### 61.14 Freshness elapses without revocation

**Initial:** Valid lease, relative validity 30 days, `max_offline_tolerance` 7 days.
**After 7 days offline:** authorization_fresh = false. Lease `STALE`. Authorization fails.
**Successful refresh on day 10:** `authorization_fresh` restored. Lease `VALID`.
**After 30 days offline without refresh:** Lease `EXPIRED`. Refresh on day 31 does NOT restore.

### 61.15 Local storage loss

**Initial:** Peer P `KNOWN`, `RECOGNIZED`, authorized.
**Incoming:** Local storage lost.
**Expected:** Verifier returns to `UNKNOWN`. Trust anchor must be re-established via pairing.

### 61.16 Relationship assertion pair

**Initial:** No local state for peer P.
**Incoming:** `RelationshipAssertion` A from peer P naming local principal as subject.
**Expected:** Relationship state `PENDING`. Does not contribute to authorization.
**Incoming:** Local assertion naming peer P as subject.
**Expected:** Relationship state `RECOGNIZED`. Contributes to authorization.

### 61.17 Relationship termination

**Initial:** Relationship `RECOGNIZED`.
**Incoming:** `RelationshipTermination` from remote principal.
**Expected:** Relationship state `TERMINATED`. Terminal. Subsequent assertions do not reactivate; new `relationship_id` required.

## 7.51 Future Extensions (§62)

- Chain-extension proofs
- Sophisticated recovery (threshold, social, hardware-backed)
- Delegated administration
- Groups
- Service ownership transfer
- Rendezvous federation and gossip
- DHT-based discovery
- Metadata protection
- Reputation and liveness scoring

### Documented anti-patterns (§62.10)

- XOR-based endpoint obfuscation
- Shared-key encryption for endpoint records
- DNS-like hierarchical naming
- Timestamp-based fork resolution
- Automatic recovery from Identity Root compromise
- Dual-signature objects in a single stream
- Global Sybil resistance in the protocol
- PoW as a foundational mechanism

## 7.52 Project Structure (§63)

See Part 18.

## 7.53 Versioning and Evolution (§64)

### Versioning model

Each protocol object type carries its schema version in `domain_separator`:
```
grid/identity-document/v1
grid/relationship-assertion/v1
grid/stream-resolution/v1
```

A new schema version uses a new domain separator:
```
grid/identity-document/v2
```

Domain separators are never reused. A `v1` schema is frozen once declared stable.

### Adding new object types

New object types are added by registering a new `domain_separator` value. The registry is normative and lives in `OBJECTS.md`.

### Implementation version signaling

Implementations signal supported domain separators through the objects they produce. No separate "capabilities" negotiation.

A verifier that receives an unknown `domain_separator` rejects the object.

### Protocol version bumps

Triggered by:
- A new object type is registered
- An existing object type's semantics change
- An authority boundary changes

Editorial clarifications do not trigger a version bump.

### Compatibility guarantees

Within a major protocol version (`v0.x`):
- No existing object type's schema changes
- No existing authority boundary changes
- No existing rejection class changes meaning
- New object types may be added without invalidating existing ones

Across major protocol versions, no compatibility is guaranteed.

### Governance

V1 governance is not defined. Options:
- Single reference implementation (early SSH model)
- Benevolent dictatorship (Python, Linux kernel model)
- Standards-body-like governance (TLS, DNS model)

The choice is deferred.

### DeprecationObject types are deprecated by:
1. Removing the `domain_separator` from the recommended registry
2. Documenting the removal and the reason
3. Retaining the old schema for reference

## 7.54 Triage Decisions (§65)

### Keep as fundamental (Protocol Kernel)

Identity, relationships, authorization, leases, revocation, key hierarchy, freshness, reachability, service identity/binding/link, direct-first connectivity, untrusted relay, relay tickets, capability-based relay resources, provider replaceability, deterministic local verification, atomic state transitions, failure-does-not-grant-authority, canonical encoding, domain separation, sequence/chain rules, verifier local state

### Keep, but as architecture rather than V1 protocol

- `PathSet` as abstraction
- Path measurement
- Path selection
- Path diversity
- Multipath
- Adaptive scheduling
- Geographic/ASN diversity
- Dynamic capacity

### Keep as implementation/security guidance

- Resource limits
- Anti-amplification
- Parser hardening
- Crash/restart behavior
- Persistent-state integrity
- Fuzzing requirements
- Concurrency/race-condition testing
- Power-loss testing
- Key-compromise/recovery testing
- Normative security test vectors
- Maximum object/message sizes
- Connection/session rate limiting
- Metadata/privacy threat model
- Threat model for malicious relay/coordinator

### Keep as strategic vision

- Community relay infrastructure
- Commercial relay providers
- Open connectivity substrate
- Vendor-neutral device connectivity
- NAS/home-server/IoT integration
- Commercial managed services
- Enterprise layer
- Replacement of proprietary remote-access clouds
- Reduced dependence on DDNS
- Reduced dependence on proprietary tunnel services

### Defer hard

- FEC
- Relay marketplace
- Relay payments
- Reputation and liveness scoring
- Global relay economics
- Global Sybil resistance
- Proof-of-work as a protocol primitive
- Distributed routing consensus
- DHT
- Anonymous routing
- Global capacity allocation
- Complicated path optimization
- Blockchain
- Global ledger
- Mining
- Global consensus
- Token economics
- Global transaction ordering

### Discard from main architecture

- XOR-based endpoint obfuscation
- Shared-key encryption for endpoint records
- DNS-like hierarchical naming
- Timestamp-based fork resolution
- Automatic recovery from Identity Root compromise
- Dual-signature objects in a single stream
- Global Sybil resistance in the protocol kernel
- PoW as a foundational mechanism
- "Raspberry Pis form a decentralized relay network" as product pitch
- "Mesh can burst around ISP throttling" as feature framing

### Deferral principle

> Do not introduce a security mechanism merely because an attack is theoretically possible. Introduce it when there is a concrete authority, resource, or trust boundary that needs protecting.

Before adding a mechanism:
1. What authority or resource does it protect?
2. What specific attack does it prevent?
3. What happens if it is removed?
4. What new complexity does it introduce?

## 7.55 Final Protocol Statement

A Peer Principal is a durable cryptographic identity.

Devices, services, and infrastructure are subordinate to it and replaceable.

Relationships between principals are explicit and derived from paired per-principal assertions.

Authorization is directional, scoped, and temporary.

Leases provide bounded proof of current authorization.

Revocation is terminal.

Keys can rotate without changing principal identity.

Reachability is ephemeral and untrusted.

Rendezvous infrastructure provides discovery but no authority.

Transport is pluggable.

The resulting security question:

> Can the verifier, using its trusted anchors and locally available signed state, deterministically establish who the peer is, what it is authorized to do, whether that authorization is currently valid, and whether it has been revoked?

If the answer is yes, the peer can be trusted regardless of its current IP address, NAT mapping, rendezvous provider, relay, physical network, or whether it has been offline for months.

That is the fundamental purpose of the Grid Network protocol.

---

# Part 8 — Object Encoding

Full normative text is `OBJECTS.md` §1–§5. This part summarizes.

## 8.1 Two top-level invariants

**I1 — Sequence-space invariant.** A sequence number has meaning only within its `(issuer, stream_id)` sequence space. Sequence numbers from different sequence spaces MUST NOT be compared.

**I2 — Vector normative invariant.** Normative test vectors define exact byte-level behavior. If prose and a vector disagree, the specification MUST be corrected; implementations MUST NOT choose their preferred interpretation.

## 8.2 Canonical CBOR profile

| Major type | Allowed | Notes |
|------------|---------|-------|
| 0 — unsigned integer | Yes | Shortest form only |
| 1 — negative integer | No | Protocol values are non-negative |
| 2 — byte string | Yes | Definite-length only |
| 3 — text string | Yes | Definite-length, valid UTF-8, NFC |
| 4 — array | Yes | Definite-length |
| 5 — map | Yes | Definite-length, unique keys, canonical ordering |
| 6 — tag | No | Protocol uses no CBOR tags |
| 7 — simple/float | Partial | Only null (0xf6) and booleans |

**Prohibited:**
- Non-shortest integer encodings
- Indefinite-length byte strings, text strings, arrays, maps
- Duplicate map keys
- Floating-point values
- CBOR tags
- Non-NFC text strings
- Byte-order marks

## 8.3 Set semantics

A protocol `set<T>` is encoded as a definite-length CBOR array whose elements are:
1. **Unique** — no two elements have identical canonical CBOR encodings
2. **Sorted** — elements ordered by bytewise lexicographic comparison of their canonical CBOR encodings

An empty set is encoded as an empty definite-length array.

## 8.4 Map key ordering

Map keys MUST be ordered according to CBOR deterministic encoding (RFC 8949 §4.2.1):
1. First by the length of the encoded key (shorter first)
2. Then by bytewise lexicographic comparison of the encoded key bytes

This is **not** alphabetical ordering.

## 8.5 Cryptographic constructions

```
initial_chain_hash =
    SHA-256(canonical_cbor([
        "grid/chain-base/v1",
        domain_separator,
        stream_id
    ]))

commitment_preimage(N) =
    canonical_cbor([
        "grid/commitment/v1",
        domain_separator,
        unsigned_payload(N)
    ])

object_commitment(N) =
    SHA-256(commitment_preimage(N))

previous_hash(N) = object_commitment(N-1)     for N > 1
                   omitted                     for N = 1

previous_chain_hash(N) = initial_chain_hash    for N = 1
                         chain_hash(N-1)        for N > 1

chain_hash(N) =
    SHA-256(canonical_cbor([
        "grid/chain/v1",
        previous_chain_hash(N),
        object_commitment(N)
    ]))

signature_input(N) =
    canonical_cbor([
        "grid/signature/v1",
        domain_separator,
        unsigned_payload(N),
        chain_hash(N)
    ])

signature(N) = Ed25519_sign(signing_private_key, signature_input(N))

payload_id(N) =
    SHA-256(canonical_cbor([
        "grid/payload-id/v1",
        unsigned_payload(N)
    ]))

object_id(N) =
    SHA-256(canonical_cbor([
        "grid/object-id/v1",
        canonical_signed_object_bytes(N)
    ]))
```

**Important:** `previous_hash` is a **field** in the unsigned payload. `previous_chain_hash` is a **derived input** to the chain construction, not a field.

The first object in every stream has `sequence = 1`. `0` is reserved for uninitialized.

## 8.6 Envelope fields

Every signed object shares:
- `domain_separator` — text string, carries schema family and version
- `sequence` — integer ≥ 1
- `previous_hash` — byte string (32 bytes); omitted at sequence 1
- `chain_hash` — byte string (32 bytes)
- `signature` — 64-byte string, or 2-element array for dual-signature schemas
- Schema-specific fields

**Envelope invariants:**
- E1. `domain_separator` MUST be present
- E2. `sequence` MUST be present and ≥ 1
- E3. `previous_hash` MUST be omitted at sequence 1 and present otherwise
- E4. `chain_hash` MUST be present
- E5. `signature` MUST be present
- E6. `unsigned_payload` MUST NOT contain `chain_hash` or `signature`
- E7. No fields outside the envelope plus schema-specific fields

## 8.7 Registered domain separators

```
grid/identity-document/v1
grid/device-binding/v1
grid/service-binding/v1
grid/key-binding/v1
grid/key-revocation/v1
grid/relationship-assertion/v1
grid/relationship-termination/v1
grid/rendezvous-manifest/v1
grid/operator-manifest/v1
grid/relationship-grant/v1
grid/authorization-lease/v1
grid/grant-revocation/v1
grid/lease-revocation/v1
grid/service-record/v1
grid/reachability-record/v1
grid/stream-resolution/v1
grid/identity-continuity/v1
grid/relay-ticket/v1
grid/relay-node-record/v1
```

## 8.8 Cryptographic tags

```
grid/commitment/v1
grid/chain-base/v1
grid/chain/v1
grid/signature/v1
grid/payload-id/v1
grid/object-id/v1
```

## 8.9 Signing-authority matrix

| Object | Authorized signer |
|--------|-------------------|
| IdentityDocument | Identity Root |
| DeviceBinding | Identity Root (or delegated device-authority key) |
| ServiceBinding | Identity Root (or delegated service-authority key) |
| KeyBinding | Identity Root |
| KeyRevocation | Identity Root |
| RelationshipAssertion | One principal's Identity Root (the issuer) |
| RelationshipTermination | One principal's Identity Root (the terminating principal) |
| Principal RendezvousManifest | Principal's Identity Root |
| OperatorManifest | Operator's Identity Root |
| Grant | Authorization Key |
| Lease | Authorization Key |
| GrantRevocation | Authorization Key |
| LeaseRevocation | Authorization Key |
| ServiceRecord | Service Key |
| ReachabilityRecord | Device Key |
| StreamResolution | Pre-fork authority above the disputed stream |
| IdentityContinuity | Both previous and new Identity Roots (dual signature) |
| RelayTicket | Relay Authority Key |
| RelayNodeRecord | Relay Node Key |

## 8.10 Verification procedure

1. **Decode.** Decode canonical CBOR. Reject as `MALFORMED_ENCODING` if invalid.
2. **Envelope validation.** Verify required envelope fields. Reject as `MALFORMED_ENVELOPE`.
3. **Domain separator validation.** Verify `domain_separator` is registered. Reject as `UNKNOWN_SCHEMA`.
4. **Schema validation.** Validate schema-specific fields. Reject as `MALFORMED_SCHEMA`.
5. **Sequence validation.** Verify `sequence >= 1` and `previous_hash` presence. Reject as `INVALID_SEQUENCE` or `INVALID_PREVIOUS_HASH`.
6. **Chain validation.** Compute `object_commitment`, verify `previous_hash`, compute and verify `chain_hash`. Reject as `CHAIN_MISMATCH`.
7. **Signature input construction.** Compute `signature_input`.
8. **Signature verification.** Verify signature(s). Reject as `INVALID_SIGNATURE`.
9. **Authority validation.** Verify signing key role and current authorization. Reject as `UNAUTHORIZED_SIGNER`.
10. **Semantic validation.** Apply the object's semantic rules.

**Atomicity:** A verifier MUST NOT advance or mutate its accepted stream state while performing steps 1–9. Validation is pure with respect to accepted state; commitment is the only mutation.

## 8.11 Rejection classes

| Class | Meaning |
|-------|---------|
| `MALFORMED_ENCODING` | Not valid canonical CBOR |
| `MALFORMED_ENVELOPE` | Envelope fields missing, mistyped, or unknown fields present |
| `UNKNOWN_SCHEMA` | `domain_separator` not registered |
| `MALFORMED_SCHEMA` | Schema-specific fields fail validation |
| `INVALID_SEQUENCE` | `sequence` is 0 or otherwise invalid |
| `INVALID_PREVIOUS_HASH` | `previous_hash` presence does not match `sequence` |
| `CHAIN_MISMATCH` | `previous_hash` or `chain_hash` does not match stream state |
| `INVALID_SIGNATURE` | Signature does not verify |
| `UNAUTHORIZED_SIGNER` | Signing key role is not authorized |

## 8.12 Pending sections

**§6 — Object Schemas.** To be drafted. One schema per object type with field names, types, constraints, stream membership, signing key role, domain separator.

**§7 — Stream Rules.** To be drafted. Sequence spaces, initial chain state, monotonicity, gap detection, fork detection, resolution, cross-stream prohibition.

**§8 — Positive Test Vectors.** To be drafted.

**§9 — Negative Test Vectors.** To be drafted.

**§10 — Conformance Requirements.** To be drafted.

---

# Part 9 — Security Model

Full text is `SECURITY.md` (draft). This part summarizes.

## 9.1 Security model

```
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
```

Rendezvous and relay infrastructure operate **outside** the authority chain.

## 9.2 Primary security invariant

> **No intermediary MUST become an authority merely by observing, storing, forwarding, or relaying grid traffic.**

In particular:
- A rendezvous operator MUST NOT be able to create identity authority
- A relay operator MUST NOT be able to create authorization
- A reachability record MUST NOT grant access
- Knowledge of an endpoint MUST NOT imply identity
- Possession of a signed object MUST NOT by itself override the verifier's trusted state
- Transport success MUST NOT imply application authorization

## 9.3 Blast-radius model

| Compromised component | Potential effect | Authority it MUST NOT gain |
|----------------------|------------------|---------------------------|
| Rendezvous service | Discovery manipulation, suppression, metadata, availability disruption | Identity or authorization authority |
| Relay | Traffic disruption, timing/volume observation, metadata | Identity or application authorization |
| Reachability state | Stale or misleading endpoint info | Identity authority |
| Service record | Service discovery disruption | General authorization |
| Authorization key | Authority within its defined scope | Identity Root authority |
| Device key | Device impersonation within its authority | Principal Root authority |
| Service key | Service-level signing authority | Principal Root authority |
| Identity Root | Control of that principal's identity authority | Authority over unrelated principals |
| Application | Use of capabilities granted to it | Arbitrary grid authority |

## 9.4 Threat taxonomy

- **T1** Identity forgery
- **T2** Authorization forgery
- **T3** Revocation exposure
- **T4** Rollback
- **T5** Fork
- **T6** Replay
- **T7** MITM during pairing
- **T8** Endpoint poisoning
- **T9** Rendezvous observation
- **T10** Relay observation
- **T11** Subordinate key compromise
- **T12** Identity Root compromise
- **T13** Denial of service
- **T14** Abuse of shared infrastructure

## 9.5 Threat-to-property mapping

| Threat | Property | Mechanism |
|--------|----------|-----------|
| T1 | Identity authenticity | Signed identity documents |
| T2 | Authorization authenticity | Signed grants and leases |
| T3 | Bounded revocation exposure | `max_offline_tolerance` |
| T4 | Monotonic state | Sequence numbers |
| T5 | Chain uniqueness | `chain_hash` |
| T6 | Object application control | Stream sequence state; object identity; validity intervals |
| T7 | Pairing integrity | PAKE with transcript binding |
| T8 | Endpoint authenticity | Signed reachability and service records |
| T9 | Metadata minimization | Opaque peer IDs |
| T10 | Traffic confidentiality | End-to-end encryption |
| T11 | Blast radius containment | Key role separation |
| T12 | (partial) Recovery | V1 treats root as anchor |
| T13 | (not addressed) | Deployment |
| T14 | (not addressed) | Deployment policy |

## 9.6 Explicit non-properties

- Anonymity
- Availability
- Metadata confidentiality against global observer
- Protection against compromised endpoints
- Protection against authorized-but-malicious peers
- Protection against compromised Identity Root beyond V1 trust-anchor model

## 9.7 Compromise and recovery

### Service Key compromise
- **Blast radius:** one service's discovery metadata
- **Recovery:** revoke Service Key via identity document; issue new key

### Device Key compromise
- **Blast radius:** one device's discovery metadata
- **Recovery:** revoke Device Key; issue new key

### Authorization Key compromise
- **Blast radius:** all authorization state under the key
- **Recovery:**
  1. Identity Root signs `KeyRevocation` with `effective_sequence`
  2. Objects signed by the compromised key at or after `effective_sequence` are invalid
  3. Principal issues new Authorization Key

**Normative:** A revocation of an Authorization Key is an identity-authority operation and MUST NOT require the compromised key to sign its own revocation.

`effective_sequence = 0` invalidates the entire key history.

### Identity Root compromise
- **Blast radius:** the entire principal
- **Recovery:** V1 has no in-band recovery

### Device compromise
- **Blast radius:** union of compromised keys' blast radii

### Rendezvous compromise
- **Blast radius:** discovery only

### Relay compromise
- **Blast radius:** transport for peers using the relay

### Compromise summary

| Asset | Blast radius | Recovery |
|-------|--------------|----------|
| Service Key | One service's discovery | Rotate via identity document |
| Device Key | One device's discovery | Rotate via identity document |
| Authorization Key | Authorization under it | Root revokes with `effective_sequence`; new key |
| Identity Root | Entire principal | None in V1 |
| Device | Union of held keys | Depends on keys held |
| Rendezvous | Discovery | Rotate rendezvous |
| Relay | Transport | Another relay or direct |

### Compromise invariants

1. Subordinate key compromise MUST NOT require replacing the Identity Root
2. Subordinate key compromise MUST NOT affect unrelated keys
3. Signing key compromise MUST NOT extend blast radius
4. Infrastructure compromise MUST NOT affect identity or authorization state
5. Revocation of a compromised key is authorized by a higher-authority key

## 9.8 Key security principles

- **Every security mechanism needs a specific boundary it protects.** Before adding a mechanism, answer all four:
  1. What authority or resource does it protect?
  2. What specific attack does it prevent?
  3. What happens if it is removed?
  4. What new complexity does it introduce?
  If any answer is unsatisfactory, the mechanism is premature.

- **Failure never grants authority.** Examples: rendezvous failure doesn't alter identity; relay failure doesn't alter authorization; network failure doesn't extend a lease; clock failure doesn't create authority; reconciliation failure doesn't create capabilities; identity forks don't automatically create authority.

- **Local state loss is a security-relevant event.** If a verifier loses state necessary to establish that a previously trusted stream is the accepted continuation, the safe behavior is to return to an unknown/untrusted state.

- **Metadata privacy is different from anonymity.** The protocol provides confidentiality of content and authorization, not anonymity of participation.

- **Operational security is out of scope.** The protocol does not attempt to protect against:
  - Key storage compromise on the local machine
  - Agent supply-chain attacks
  - Recovery-flow social engineering
  - Update-mechanism compromise

## 9.9 Security test program

### Cryptographic tests
- Canonical encoding vectors
- Signature vectors
- Commitment vectors
- Chain vectors
- Object-ID vectors
- Dual-signature vectors
- Invalid signature tests

### State-machine tests
- Sequence advancement
- Rollback
- Forks
- Termination
- Revocation
- Key rotation
- Identity continuity
- Local state loss
- Crash during commit

### Adversarial parsing
- Malformed CBOR
- Duplicate fields
- Oversized fields
- Invalid types
- Truncation
- Deeply nested data

### Authorization tests
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

### Infrastructure tests
- Malicious rendezvous
- Stale rendezvous
- Malicious relay
- Relay disappearance
- Direct-path failure
- Relay fallback
- Replayed reachability
- Coordinator flooding
- Relay resource exhaustion

### Persistence tests
- Restart
- Power loss
- Interrupted commit
- Corrupted local state
- Restored backup
- Missing state
- Recovery

## 9.10 Security roadmap priorities

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

# Part 10 — Connectivity Architecture

## 10.1 Direct-first preference order

1. **Local LAN.** Direct. No relay.
2. **Direct IPv6.** Direct. No relay.
3. **Direct IPv4.** Direct. No relay.
4. **NAT traversal (hairpinning, hole punching).** Direct once established.
5. **Relay.** Direct failed. Fallback.

In a mature deployment with widespread IPv6 and working NAT traversal, most traffic never reaches step 5.

## 10.2 Relay is untrusted

A relay can:
- Accept encrypted traffic and forward it
- See only ciphertext
- Enforce resource limits per ticket (expiration, session limits, maximum bytes, maximum rate, permitted source/destination, connection lifetime)

A relay cannot:
- Decrypt content
- Grant authorization
- Impersonate peers
- Create relationships
- Forge leases
- Become an authority

## 10.3 Relay capability model

Relays advertise **capabilities**, not hardware classes:

```
Relay capability
    maximum bandwidth
    maximum concurrent sessions
    maximum bytes
    maximum session duration
    maximum paths
    IPv4 / IPv6
    latency characteristics
    availability
    geographic/network information
    privacy properties
    operator policy
```

The meaningful property: **"This resource can provide these connectivity characteristics"** — not "This resource contains this CPU."

## 10.4 Low-power nodes

A Pi 3B can be a meaningful relay because forwarding is much cheaper than terminating encryption. The workload is:
- Receive packets
- Validate relay session/ticket
- Enforce limits
- Forward packets
- Maintain transient connection state

**Persistent storage principle:**
> Forwarding traffic, connection statistics, and transient reachability observations MUST NOT require persistent storage writes.

This reduces SD-card wear, storage requirements, I/O overhead, power consumption, and complexity.

## 10.5 Community infrastructure model

No individual household needs to operate a major data center. The network gains:
- Many alternative paths
- Geographic diversity
- ISP diversity
- ASN diversity
- Redundancy
- Aggregate resources

A node that contributes only 10 Mbps can still be useful.

## 10.6 Network self-healing

If Relay A is overloaded, the path selector can choose Relay B, C, D. If B disappears, connections migrate or establish another path. If a region has few resources, nodes there can contribute more capacity.

**Principle:** Optimize around scarce resources rather than pretending scarcity doesn't exist.

## 10.7 Residential bandwidth

Peer-to-peer transfers between residential connections sometimes achieve only a small fraction of advertised bandwidth. Possible causes:
- Ordinary congestion
- Peering constraints
- Routing
- Traffic engineering
- Fair queuing
- Per-flow scheduling
- TCP congestion behavior
- Traffic management
- Access-network architecture
- CGNAT
- Asymmetric links
- Bottlenecks elsewhere in the path

## 10.8 Multiple flows vs multiple paths

Opening many connections doesn't necessarily create independent network paths. If all flows share a bottleneck, aggregate throughput doesn't increase.

The interesting case: paths with sufficiently independent bottlenecks. Aggregate throughput can potentially increase.

**Multipath cannot defeat an aggregate access-link bottleneck.**

## 10.9 Multipath relay concept

A future implementation could discover:
- Direct path
- Multiple relay paths

The endpoint maintains several simultaneously usable paths. Traffic distributed according to measured conditions. Relays don't need to know they're part of a larger multipath system.

## 10.10 Existing multipath technologies

- **MPTCP** — multipath TCP with subflows
- **MLVPN** — multi-link VPN
- **OpenMPTCProuter** — practical residential multi-link aggregation
- **Multipath QUIC** — QUIC with multiple paths

Typically these aggregate multiple links belonging to the same user. Grid Network's extension: **use independently operated community nodes as a distributed pool of alternative paths.**

## 10.11 Torrent analogy

A torrent can obtain high aggregate throughput because it communicates with many peers. Different connections encounter different congestion, routes, bottlenecks.

Grid Network could use a similar principle deliberately while maintaining one logical service connection.

## 10.12 Burst behavior

Modern congestion-control systems already use probing and controlled increases in sending rate to discover available capacity.

**The grid version should NOT be:** "Make traffic bursty to fool the ISP."

**Instead:** Use naturally available capacity across multiple paths and adapt continuously.

## 10.13 Adaptive path scheduling

Naive round-robin striping is undesirable when paths differ substantially (creates packet reordering). Instead, the scheduler measures:
- Throughput
- RTT
- Loss
- Jitter
- Congestion
- Reordering
- Stability

and dynamically weights paths.

Example:
```
Path A: 55%
Path B: 25%
Path C: 15%
Path D: 5%
```

Weights change as conditions change.

## 10.14 Endpoint-owned multipath state

The endpoints own the multipath state. Relays remain independent forwarding resources. They do not need to coordinate, understand application semantics, know the PathSet, decrypt traffic, or maintain application state.

## 10.15 PathSet abstraction

Future:
```
PathSet
    direct
    relay A
    relay B
    relay C
```

Application might request:
- `min_bandwidth`
- `max_latency`
- `multipath = permitted`
- `max_paths`
- `redundancy = optional`

## 10.16 Path diversity

Ten relays behind the same ISP may not provide ten truly independent paths. Useful diversity:
- Different ASNs
- Different upstream providers
- Different geographic locations
- Different access networks
- IPv4 vs IPv6
- Different congestion domains

## 10.17 Non-preclusion constraints

V1 objects and state MUST NOT preclude future connectivity capabilities:
- Reachability records MAY carry multiple endpoint candidates
- Path identity is distinct from connection identity
- Authorization is path-agnostic
- Relay selection is not baked into signed objects

---

# Part 11 — Commercial Model

Full text is `RATIONALE-ADDENDUM-A-COMMERCIAL.md` v6.0.

## 11.1 The design principle

> Every participant — free user, contributor, commercial operator, enterprise — makes the network more valuable to every other participant. The commercial model exists to fund the protocol's maintenance and development, not to extract value from users.

## 11.2 What the commercial layer sells

**Guarantees**, not access. Free users always connect (best-effort). Paid users get the same relay with predictable quality — higher priority, guaranteed capacity, consistent latency.

The difference is **predictability**, not availability.

## 11.3 Relay is a fallback, not a default

The commercial layer exists for one purpose: relay. And relay is a fallback.

In deployments where direct connectivity always works, the commercial layer is unused. No subscription, no account, no cost.

## 11.4 The commercial layer is not a platform

A platform owns the customer's identity, data, or relationships. Grid Network commercial operators own none of these.

The entire commercial model rests on one property: **identity is portable.**

## 11.5 Free users as the foundation

Free users contribute:
- Reachability publication
- Peer-to-peer efficiency
- Hairpinning and traversal
- Local relays
- Reduced infrastructure cost
- Bug discovery
- Ecosystem gravity

A network with one million free users and ten thousand paid users is more valuable than one with ten thousand paid users and no free users.

## 11.6 The relay priority model

Four properties:
1. Free tier is real
2. Paid tier is priority
3. Idle paid capacity flows to the public pool
4. Contribution earns credit

Priority classes:
- **Free class** — best-effort, fair-share, may be preempted
- **Standard class** — modest guaranteed share
- **Priority class** — higher guaranteed share
- **Dedicated class** — reserved capacity, never preempted

**Priority is a property of the ticket, not the user's identity.**

## 11.7 Idle capacity donation

Commercial operators overprovision. The idle surplus serves the free pool, with priority classes allowing instant reclaim when paying customers need capacity back.

Three effects:
- Public pool expands
- Operators have a better story
- Overprovisioning becomes a public good

## 11.8 Credit pools

Family and group pools:
- A group identity
- A membership list
- A credit balance
- Policies
- Administration

Credits are earned by running infrastructure and consumed by using relay capacity. Cross-operator credit exchange at negotiated rates.

## 11.9 Preventing abuse

| Vector | Mitigation |
|--------|-----------|
| Fake contribution | Credits only for served traffic; anomaly detection |
| Circular traffic | Circuit detection; path length limits |
| Credit laundering | Credits bound to a pool; cross-operator exchanges mediated |
| Free-riding | Limited to free-tier capacity |
| Fake identity | Credits per-pool, not per-identity |
| Consumption fraud | Consumption recorded by relay, not consumer |
| Bonding | Relay operators may post a bond |

**Design principle:** The easiest way to earn credits is to actually contribute, and the easiest way to consume them is to actually need them.

## 11.10 Geographic scarcity

A VPS in Hawaii provides scarcer capacity than one in Frankfurt. **Scarcity multipliers** make contribution in scarce regions more attractive.

A relay's credit value depends on:
- Base value (bytes relayed)
- Scarcity multiplier
- Latency value
- Availability value
- Priority class value

## 11.11 Self-hosted priority

A user with their own VPS runs a relay on it. When their traffic needs relay, the agent prefers their own relay.

Enterprise self-hosted priority: enterprises run their own infrastructure, get priority, contribute idle capacity.

## 11.12 Six commercial products

1. Managed rendezvous
2. Priority relay capacity
3. Credit exchange
4. Enterprise integration
5. Support and SLAs
6. Managed deployment

Every product has a public-good component.

## 11.13 The urgency buyer

Traveler on hotel Wi-Fi, person whose connection is failing, small business owner whose meeting depends on reaching a file. Reliability-sensitive, not price-sensitive.

## 11.14 "No account" is a commercial feature

No user database, no signup flow, no password reset, no data breach risk, no GDPR exposure from user database.

## 11.15 Developer funding

Commercial operators contribute a percentage of revenue to protocol development as a structural line item. A nonprofit stewardship entity manages funds and maintains the protocol.

Distribution:
- Maintainer stipends
- Sponsored features
- Bug bounties and security work
- Ecosystem work
- Fellowships

Sources:
- Commercial operator revenue share
- Individual donations
- Grants
- Enterprise contributions
- Foundation endowments

**Success:** A developer can work on Grid Network full-time and be paid fairly.

---

# Part 12 — The Developer Case

## 12.1 Developer adoption is the primary path

The most likely path to Grid Network becoming widely used is application developers adopting it as a shared layer. The analogy is authentication offloading (Auth0, Okta, Google Sign-In).

## 12.2 The problem every application faces

Every app with a self-hosted, on-premises, or local-device component hits the same wall.

## 12.3 Three bad patterns

1. Build a cloud service
2. Require an external tool
3. Roll your own

## 12.4 What Grid Network changes

The application talks to a local grid agent. The agent handles identity, pairing, discovery, NAT traversal, relay fallback, authorization, revocation, freshness.

The app keeps its own application-level authorization.

## 12.5 The authentication analogy

- Phase 1 — Roll your own
- Phase 2 — Use a framework
- Phase 3 — Offload to an identity provider
- Phase 4 — Federate to third parties

Grid Network extends this from user authentication to device authentication and network authorization.

## 12.6 Integration

```
grid.connect(service_link_id, capability) → local connection handle
grid.resolve(peer_id)                     → peer state
grid.discover()                            → list of known peers
grid.revoke(object_id)                     → issue revocation
grid.status()                              → daemon state
```

Connection handle:
```
{
    "connection_id": "random-id",
    "local_url": "http://127.0.0.1:41873",
    "expires_at": "2026-10-04T21:00:00Z"
}
```

## 12.7 The developer pitch

> You already offloaded user authentication to Auth0, Okta, or Google Sign-In. You should do the same for device connectivity. Grid Network is a shared protocol that handles identity, pairing, discovery, NAT traversal, relay fallback, and revocation. Your app calls a local grid agent, gets an authorized connection, and never thinks about keys, relays, or pairing again.

## 12.8 Commercial economics for applications

**Self-hosted open-source project:** No cloud service, no relay infrastructure, no cross-platform code, smaller security review surface.

**Commercial SaaS product:** Fewer engineers, no relay infrastructure, trust-portability story, compliance story, no vendor lock-in exposure.

---

# Part 13 — Contribution Model

## 13.1 Three contribution layers

**Layer 1 — Reachability publication.** Automatic; every participant does it. Negligible cost.

**Layer 2 — Rendezvous.** Lightweight; a Raspberry Pi 3 is sufficient for hundreds of peers.

**Layer 3 — Relay.** Where bandwidth and cost actually matter.

## 13.2 Contribution by capacity

| Contributor | What they contribute |
|-------------|----------------------|
| Phone, laptop, small device | Reachability publication |
| Raspberry Pi, home NAS | Rendezvous for a small group; light relay |
| Home server, small VPS | Rendezvous for a community; relay for a group |
| Enterprise server, cloud instance | Large rendezvous; high-capacity relay |
| Datacenter | Backbone relay for a region |

## 13.3 Why contribution is safe

- A **rendezvous server** can only store and forward signed objects
- A **relay** can only forward encrypted traffic

A contribution from an untrusted party is still useful.

## 13.4 The economic shape

- **Bottom:** free (reachability publication)
- **Middle:** volunteer (rendezvous, light relay)
- **Top:** commercial (high-bandwidth, low-latency, guaranteed relay)

No layer depends on the layer above it.

---

# Part 14 — Lineage and Composition

Full text is `RATIONALE-ADDENDUM-B-LINEAGE.md` v1.0.

## 14.1 What Grid Network borrows

**From DNS:** Resolver model without hierarchy. Names resolve to current locations; the resolver is not the authority.

**From WireGuard:** Small, auditable transport. Used directly. Grid Network layers identity/authorization above it.

**From BitTorrent:** Peer coordination without a central server. Tracker model with signatures added.

**From Bitcoin:** Cryptographic proofs replace institutional trust — locally, not globally. No consensus overhead.

**From Tailscale:** Product polish, NAT traversal, seamless relay fallback. But identity is portable and the protocol is open.

**From Headscale:** Community self-hosting is possible and valuable.

**From Matrix:** Public-key identity and signed events; avoid mandatory homeservers.

**From SSH:** Trust-on-first-use is a valid model for some contexts; Grid Network provides explicit identity binding.

**From IPFS:** "Decentralized" is not automatically useful.

**From Kerberos:** Short-lived tickets; without the central authority.

## 14.2 The composition is the point

None of the individual ideas is new. The composition produces a system with properties none of them has:

1. **Portable identity** — no company owns it
2. **Local verification** — works offline, works under partition
3. **Untrusted infrastructure** — rendezvous and relays can be malicious
4. **Polished UX** — ordinary people can use it
5. **Developer integration** — applications consume it via API
6. **Sustainable funding** — the commercial layer funds the protocol

## 14.3 Not a competitor

Grid Network is not a replacement for Tailscale, WireGuard, DNS, or BitTorrent. It's a layer above them that solves portable identity and authorization.

## 14.4 What gets disrupted

Vendors whose business depends on being the **coordination authority**:
- Managed mesh VPNs (only "makes it easy" survives)
- Tunnel services (relay becomes a competitive market)
- Cloud identity providers
- DDNS services

## 14.5 What survives

Vendors whose value is not lock-in:
- Reliable relays
- Enterprise integration
- Managed infrastructure
- Support and SLAs
- Hardware appliances
- Developer tooling

**Vendors that compete on quality survive; vendors that compete on lock-in do not.**

---

# Part 15 — The Relay and Pi Node Design Record

Full text is the Relay Design Record.

## 15.1 The relay summary

A relay does not need to terminate encryption. It's a pure encrypted packet forwarder.

```
Endpoint A → encrypted traffic → Pi Relay → encrypted traffic → Endpoint B
```

A relay needs to:
- Receive packets
- Validate/associate a relay session or ticket
- Enforce limits
- Forward packets
- Maintain transient connection state

The workload is dramatically lighter than running a conventional VPN hub.

## 15.2 Pi 3B as an example

A Pi 3B has modest hardware, but for a forwarding workload it doesn't need to perform heavy cryptography for every packet. Limitations:
- Network interface speed
- Packets per second
- CPU overhead from networking stack
- Number of simultaneous sessions
- Upstream/downstream Internet connection
- Power/ISP limitations

The Pi doesn't need to be a giant relay. Even a small contribution is useful when thousands of nodes participate.

## 15.3 Advertise capabilities, not hardware

The protocol shouldn't care whether a relay is:
- Raspberry Pi
- x86 server
- Router
- VPS
- NAS
- Cloud instance
- Old laptop

It should expose capabilities/resources.

## 15.4 Resource contribution is granular

A household might contribute:
- 5 Mbps, 10 Mbps, 25 Mbps, 50 Mbps
- Occasional availability
- IPv6 connectivity
- Geographically useful location
- Particular ISP/ASN

A node that is useless as a high-performance server can still be valuable as one more independent path.

## 15.5 Path diversity

Suppose two residential users have plenty of advertised bandwidth but a particular direct flow performs poorly. Mesh could discover:
- Relay 1
- Relay 2
- Relay 3

The endpoints measure each path and distribute traffic according to throughput, latency, loss, jitter, congestion, stability.

A simple round-robin scheduler isn't sufficient. Paths should be weighted dynamically.

## 15.6 Why this matters for residential Internet

Peer-to-peer transfers between residential connections sometimes achieve only a small fraction of advertised bandwidth, while torrent-like workloads can achieve much higher aggregate throughput.

Possible causes:
- Per-flow behavior
- Fair-queuing
- Congestion
- Peering
- Routing
- Traffic engineering
- Traffic management
- Different bottlenecks
- TCP behavior

We shouldn't assume ISPs deliberately throttle P2P. But if the effective bottleneck is flow-specific or path-specific, multiple independent paths could potentially aggregate much better than one flow.

## 15.7 Bursting

Networks sometimes seem to accommodate bursts better than sustained single-flow traffic. Modern congestion-control systems already use probing and controlled increases in sending rate.

The Mesh version shouldn't be: "Make traffic bursty to fool the ISP."

Instead: **Use naturally available capacity across multiple paths and adapt continuously.**

## 15.8 Similar to existing multipath research

Existing technologies demonstrate that path aggregation works:
- MPTCP
- MLVPN
- OpenMPTCProuter
- Multipath QUIC approaches

Typically they aggregate multiple links belonging to the same user or route through a common aggregation server.

Grid Network's potentially interesting extension: **Use independently operated community nodes as a distributed pool of alternative paths.**

## 15.9 The relay should remain completely untrusted

A malicious relay should be able to:
- Drop traffic
- Delay traffic
- Refuse service
- Observe metadata
- Consume its own resources

But it should NOT be able to:
- Impersonate the service
- Grant authorization
- Read end-to-end protected content
- Change identity
- Create relationships
- Forge leases
- Become an authority

That gives us: **Permissionless infrastructure, permissioned services.**

## 15.10 Pi nodes don't need much persistent storage

Forwarding traffic should be primarily transient. Persistent storage is for:
- Identity keys
- Configuration
- Accepted protocol state
- Bounded authorization/revocation information
- Signed objects
- Checkpoints
- Limited logs

Not: `packet → disk → packet → disk`

**Principle:**
> Forwarding traffic, connection statistics, and transient reachability observations MUST NOT require persistent storage writes.

## 15.11 Network self-healing

Because relays are interchangeable resources, the network doesn't need a single official relay.

If a relay is overloaded, the network can choose another. If a relay disappears, connections migrate or establish another path.

**Principle:** Optimize around scarce resources rather than pretending scarce resources don't exist.

## 15.12 Low-power hardware has a useful role

A Raspberry Pi isn't valuable because it's powerful. It's valuable because you can deploy a lot of them in places where powerful infrastructure isn't available.

Each household can contribute a little. The aggregate resource can become substantial. And because the nodes are geographically and topologically distributed, the diversity itself is valuable.

## 15.13 Direct connectivity is first choice

Preferred progression:
1. IPv6 direct
2. Direct IPv4 / NAT traversal
3. Other suitable direct transport
4. Relay
5. Multiple relays / multipath

The application shouldn't care. It asks: "Connect me to Service X." The Grid agent figures out how.

This allows improvements in IPv6, NAT traversal, QUIC, PCP, WireGuard, MASQUE, and future transports to automatically benefit Grid Network.

## 15.14 What belongs in core vs later

**v0.6.1 core (keep):**
- Identity
- Relationships
- Authorization
- Leases
- Revocation
- Freshness
- Reachability
- Direct connectivity
- Rendezvous
- Simple relay fallback

**Future transport/path extension (potentially add):**
- Relay capability advertisements
- Path measurement
- Path selection
- Path diversity
- Multipath
- Adaptive scheduling
- Optional redundancy/FEC
- Resource-aware routing
- Geographic/ASN diversity
- Dynamic capacity

A possible future abstraction:
```
PathSet
    direct
    relay A
    relay B
    relay C
```

## 15.15 The big picture

The Raspberry Pi isn't really the point. The point is creating a network where ordinary devices can contribute small amounts of useful infrastructure.

A Pi might provide 10 Mbps. Another provides 30 Mbps. A NAS provides 100 Mbps. A router provides 50 Mbps. A VPS provides 1 Gbps. A server provides 10 Gbps.

They all become **cryptographically identifiable, policy-controlled, replaceable connectivity resources.**

The Internet supplies the underlying connectivity, while Grid Network turns connectivity itself into a composable community resource — without making the relays trusted.

---

# Part 16 — Edge Cases and FAQ

## 16.1 Offline for extended periods

A peer may be offline for weeks or months. What does the protocol do?

The peer's **identity** is unchanged. Its **relationships** are unchanged. Its **reachability** records expire and are forgotten. When the peer comes back online, it republishes reachability and everything resumes.

Authorization, however, is bounded. Leases expire. When the peer returns, it must renew its leases before accessing services.

The user experience: "your server is online again, but your phone needs to renew its access."

## 16.2 Device replacement

A user replaces their phone. What happens?

The new phone has a **new device key**, but it belongs to the **same principal**. The relationship with the user's server is preserved. The new device key is added to the identity document; the old one is revoked or retired.

The user experience: "your new phone is now your phone."

## 16.3 Lost device

A user loses their phone. What happens?

The user (from another device or from a recovery flow) revokes the lost device's key. The revocation propagates to peers who care. Services the lost device was authorized for stop accepting its connections.

Because revocation is a signed object, it works even if the lost device is offline. And because leases have maximum offline tolerance, even without an explicit revocation, a lost device eventually stops being able to access services.

The user experience: "I revoked my old phone; it can't access my stuff anymore."

## 16.4 Rendezvous server disappears

A community's rendezvous server goes down. What happens?

Peers that have cached reachability records continue using them until they expire. Peers that haven't cached can try other rendezvous servers, if any are configured. If no rendezvous is reachable, peers may be unable to discover each other's current endpoints — but their existing sessions, their identities, and their authorizations are unaffected.

The user experience: "discovery was temporarily slow, but nothing was lost."

## 16.5 Relay operator is malicious

A user's traffic is being relayed by an operator who tries to attack. What can they do?

A relay sees: source and destination endpoints, volume and timing of traffic, the fact that two peers are communicating.

A relay does **not** see: plaintext content (traffic is end-to-end encrypted), authorization state (relays have no authority), identity (relays see endpoint identifiers, not cryptographic identities).

A malicious relay can drop traffic, delay it, or attempt to inject traffic. The first two are availability problems; the third is detected by transport-layer encryption.

The user experience: "I switched to a different relay; the malicious one accomplished nothing."

## 16.6 Identity key is compromised

A user's Identity Root is stolen. This is the worst-case scenario.

A compromised Identity Root can produce valid signatures, so it can impersonate the user to peers. There is no in-band recovery mechanism for this.

Recovery is out-of-band: the user contacts their peers through a trusted channel, explains the compromise, and establishes a new identity.

This is why the Identity Root should be stored with the highest possible protection — offline, hardware-backed, or in a secure enclave.

## 16.7 Service moves between devices

A user moves their Jellyfin service from one server to another. What happens?

The service **identity** is preserved. Grants and leases remain valid because they reference the service identity, not the device. Only the reachability changes.

The user experience: "I moved Jellyfin to a new machine; my phone doesn't have to re-pair."

## 16.8 Peer on a network with no direct connectivity

A user is on a network that blocks direct peer-to-peer traffic (hotel Wi-Fi, corporate network, restrictive CGNAT). What happens?

The grid agent detects that direct connection fails. It requests a relay path from an available relay. The relay forwards encrypted traffic, and the connection is established.

The user experience: "It was slightly slower, but it worked."

## 16.9 Application uses grid identity for its own authorization

A user has two devices — a personal laptop and a work laptop. Both are paired to the same Jellyfin server. The user wants their personal laptop to access all libraries, and their work laptop to access only the Music library.

The grid agent provides identity: "this connection is from device X." The application's own authorization (in Jellyfin) decides: "device X can access Music only."

This separation is important. The grid agent handles *who the device is*. The application handles *what the device can do within the application*.

## 16.10 Frequently raised concerns

### "Isn't this just a blockchain?"
No. Grid Network has no global consensus, no ledger, no mining, no tokens, no global ordering. It uses cryptographic signatures and local verification.

### "Isn't this just Tor / I2P / Freenet?"
No. Those systems provide anonymity through routing. Grid Network provides authenticated identity with explicit non-anonymity.

### "Isn't this just Tailscale / Cloudflare Tunnel?"
Similar in some ways, fundamentally different in others. Tailscale and Cloudflare Tunnel are products built around a specific company's infrastructure. Grid Network is a protocol that any company can implement, and identity is portable across implementations.

The key difference: if Tailscale disappears, your network is gone. If a Grid Network infrastructure provider disappears, you point your peer at a different one — your identity, relationships, and authorizations are unaffected.

### "Why not just use a VPN?"
VPNs solve a different problem. A VPN gives you access to a network. Grid Network gives you access to a *service* with *identity* and *authorization* attached. VPNs are typically all-or-nothing; Grid Network is per-service and per-relationship.

### "What about performance?"
For direct connections, Grid Network performs comparably to any other overlay network. For relayed connections, performance depends on the relay.

### "What about metadata privacy?"
Grid Network provides confidentiality of content and authorization, not anonymity of participation. Rendezvous servers see which peers query for which other peers. Relays see endpoints and traffic volume.

### "What about governance?"
V1 has no governance mechanism. The protocol is a specification, not an organization.

### "What if the Identity Root is compromised?"
V1 has no in-band recovery. This is intentional — any in-band recovery mechanism would be an authority the protocol cannot trust. Recovery is out-of-band.

---

# Part 17 — Roadmap and Priorities

## 17.1 Tier 1 — Blocks everything else

1. **Rename Mesh → Grid Network** in PROTOCOL.md (atomic commit; 19 domain separators, 6 cryptographic tags, URI scheme, local API prefix, protocol name)
2. **Complete OBJECTS.md §6** — Object schemas (~18 types)
3. **Complete OBJECTS.md §7** — Stream rules
4. **Produce first test vector** — minimal sequence-1 signed object

## 17.2 Tier 2 — Enables adoption

5. Complete OBJECTS.md §8–§10 (test vectors, conformance)
6. Draft SECURITY.md
7. Draft IMPLEMENTATION.md
8. Draft CONNECTIVITY.md

## 17.3 Tier 3 — Enables funding

9. Complete GLOSSARY.md
10. Complete FAQ.md
11. Extract VERSIONING.md

## 17.4 Tier 4 — Long-term

12. Reference implementation
13. Independent implementation
14. Applications and integrations
15. Commercial infrastructure

## 17.5 Project phases

**Phase 0 — Documentation (current)**

**Phase 1 — Reference implementation**
- Core agent (Go or Python)
- Test vectors (crypto test suite)
- Two-agent system demo
- Local discovery (mDNS)
- Simple relay
- WireGuard integration

**Phase 2 — Local connectivity**
- LAN discovery
- Hairpinning
- Local NAT traversal
- Cross-platform (Linux, macOS, Windows)

**Phase 3 — Remote reachability**
- NAT traversal (STUN/ICE)
- Candidate gathering
- Direct connection establishment

**Phase 4 — Coordinator resilience**
- Multiple coordinator support
- Replica behavior
- Cache semantics
- Recovery manifests

**Phase 5 — Relay fallback**
- Relay protocol
- Pair-bound tickets
- Bandwidth quotas
- At Phase 5 completion: PROTOCOL.md freezes as v1.0
- v0.x gets 5-year support

**Phase 6 — Mobile integration**
- iOS agent
- Android agent
- Background execution

**Phase 7 — Community infrastructure**
- Operator tooling
- Capacity declarations
- Federation support

**Phase 8 — Advanced features**
- Multi-hop relay
- Privacy transport
- DHT (if needed)

## 17.6 What is not on the roadmap

- Global consensus
- Blockchain
- Global Sybil resistance
- Anonymity networks
- Reputation systems (belongs in deployment policy)
- Adaptive TTLs (belongs in deployment policy)
- Proof-of-work as a foundational mechanism

## 17.7 What not to do

- Do not redesign the protocol. v0.6.2 is frozen.
- Do not add new object types or authority domains without justification.
- Do not add security mechanisms unless they protect a specific boundary.
- Do not conflate the four layers.
- Do not introduce vendor lock-in.
- Do not skip the rename.
- Do not produce test vectors before §6–§7 stable.
- Do not omit negative test vectors.
- Do not silently extend the protocol.

## 17.8 Test vector definition

A **test vector** is a byte-exact normative case consisting of:

1. **Input** — a fully-specified set of parameters that determine the object
2. **Expected canonical bytes** — the exact `canonical_signed_object_bytes`
3. **Expected derived values** — `object_commitment`, `chain_hash`, `payload_id`, `object_id`
4. **Expected signature** — the Ed25519 signature over `signature_input`
5. **Specification reference** — the section that the vector tests

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

### Vector format

Each vector is JSON with: description, object (base64), domain_separator, expected (object_id, payload_id, chain_hash, signature_valid), specification reference. Negative vectors include expected_rejection_class. Alongside each JSON file is a `.bytes` file with the raw canonical bytes.

---

# Part 18 — Project Structure

## 18.1 Complete repository tree

```
grid-network/
├── README.md
├── LICENSE.md                    (Apache 2.0)
├── CONTRIBUTING.md
├── HANDOFF.md                    (this archive)
│
├── docs/
│   ├── README.md
│   ├── OUTLINE.md
│   │
│   ├── protocol/
│   │   ├── PROTOCOL.md           (v0.6.2 frozen; needs rename)
│   │   ├── OBJECTS.md            (§1–§5 done; §6–§10 pending)
│   │   └── VERSIONING.md         (extract from §64)
│   │
│   ├── security/
│   │   └── SECURITY.md           (to draft)
│   │
│   ├── implementation/
│   │   ├── IMPLEMENTATION.md     (to draft)
│   │   └── CONNECTIVITY.md       (to draft)
│   │
│   ├── rationale/
│   │   ├── RATIONALE.md          (v2.0)
│   │   ├── ADDENDUM-A-COMMERCIAL.md (v6.0)
│   │   └── ADDENDUM-B-LINEAGE.md    (v1.0)
│   │
│   ├── design/
│   │   └── RELAY-DESIGN-RECORD.md
│   │
│   └── reference/
│       ├── GLOSSARY.md
│       └── FAQ.md
│
├── spec/
│   └── test-vectors/
│       └── v1/
│           └── (no vectors yet)
│
├── implementations/
│   └── README.md
│
└── apps/
    └── README.md
```

## 18.2 Document responsibilities

| Document | Layer | Audience | Change rate |
|----------|-------|----------|-------------|
| README.md | Entry | Everyone | Rare |
| OUTLINE.md | Cross | Everyone | Rare |
| PROTOCOL.md | 1 | Implementers | Slow |
| OBJECTS.md | 1 | Implementers | Slow |
| VERSIONING.md | Cross | Implementers | Slow |
| test-vectors/ | 1 | Testers | Additive |
| SECURITY.md | 2 | Implementers, reviewers | Moderate |
| IMPLEMENTATION.md | 2 | Builders | Moderate |
| CONNECTIVITY.md | 3 | Connectivity builders | Moderate |
| RATIONALE.md | 4 | Stakeholders | Slow |
| ADDENDUM-A-COMMERCIAL.md | 4 | Operators, investors | Moderate |
| ADDENDUM-B-LINEAGE.md | 4 | Skeptics, reviewers | Slow |
| GLOSSARY.md | Reference | Everyone | Additive |
| FAQ.md | Reference | Everyone | Additive |
| ROADMAP.md | 4 | Everyone | Moderate |

## 18.3 Document dependency graph

```
                        README.md
                            │
                        OUTLINE.md
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
         PROTOCOL.md    RATIONALE.md    (other)
              │             │
              │             ├─── ADDENDUM-A-COMMERCIAL.md
              │             │
              │             └─── ADDENDUM-B-LINEAGE.md
              │
              ▼
        OBJECTS.md  ───►  test-vectors/
              │
              ▼
        SECURITY.md
              │
              ▼
       IMPLEMENTATION.md
              │
              ▼
       CONNECTIVITY.md
```

## 18.4 Rules

- `PROTOCOL.md` and `OBJECTS.md` must not contradict each other
- `SECURITY.md` and `IMPLEMENTATION.md` are derived from `PROTOCOL.md`; they do not introduce new protocol requirements
- `CONNECTIVITY.md` consumes `PROTOCOL.md`; it does not modify the protocol
- `RATIONALE.md` and its addenda are descriptive; they do not introduce normative requirements

## 18.5 Versioning

Two version numbers, not to be conflated:

- **Protocol version** (e.g., v0.6.2) — version of `PROTOCOL.md`
- **Document set version** (e.g., 0.1) — snapshot of all documents together

**Current state:**
- Protocol: v0.6.2 (frozen)
- Document set: 0.1 (early draft)

---

# Part 19 — Naming and Positioning

## 19.1 Why "Grid Network"

The name changed several times:
- Originally "Mesh Coordinator"
- Then "NotDNS"
- Then "Mesh Identity & Reachability Protocol"
- Now "Grid Network"

**Why not "NotDNS":** Defined by negation. Implies DNS is the reference point. Undersells scope. Reads as a joke.

**Why not "Mesh":** Heavily used by existing networking libraries.

**Why not "Lattice":** Multiple collisions in the networking and crypto space (LatticeNet, Lattice P2P protocol, Lattice the Ethereum infrastructure company).

**Why not "Signet":** Collides with a Bitcoin test network (BIP 325), a proof-of-possession authentication protocol, and an Ethereum rollup.

**Why not "Ravelin":** Collides with a funded fraud detection company.

**Why "Grid Network":**
- Describes a grid of peers
- Scalable across audiences (family, community, enterprise, global)
- Relatively uncollided in the networking space
- One syllable, spellable
- Old Norse *grið* connection (security guarantee, truce)

## 19.2 The pitches

**The 3-minute pitch (full text):** See the Pitch Document appendix.

**The 30-second pitch:**
Every time you want to reach your own devices from outside your home, you have to choose between exposing them to the internet or renting a company's account to coordinate them. Grid Network is a cryptographic protocol that makes the coordination layer portable. Your identity and your relationships belong to you, not to a vendor. The result is private connectivity that behaves like email: anyone can run the infrastructure, anyone can switch providers, and no company gets to decide whether your network exists.

**The 10-second pitch:**
Grid Network makes private connectivity portable. Your devices, your identities, your relationships — owned by you, not rented from a company.

**The one-paragraph pitch:**
Today, the ability to reach your own devices from anywhere is rented from companies. Tailscale, Cloudflare, ZeroTier, and every commercial mesh product own your identity and your relationships. If they change their terms, you migrate or lose access. Grid Network is a protocol that makes identity and authorization portable. Your devices, your relationships, your authorizations belong to you, not to a vendor. Anyone can operate infrastructure, anyone can switch providers, and no company decides whether your network exists. It's the same model as email — anyone can run a server, anyone can switch providers, nobody needs permission.

**The developer pitch:**
You offloaded authentication. Offload this too. Grid Network isn't a replacement for WireGuard, DNS, or anything else you're using. It's the layer above them that handles identity, pairing, discovery, relay fallback, and revocation — the parts you've been solving badly on your own. Your app calls a local agent, gets an authorized connection, and stops thinking about connectivity. That's the same calculation you made when you decided not to build your own login system.

**The user pitch:**
Your devices, your identity, your relationships. Not rented. Not revocable by a vendor. Not dependent on any single provider. Works like email: anyone can run infrastructure, anyone can switch providers, nobody needs permission. And it's simple enough that you don't have to think about any of it.

**The commercial pitch:**
Buy priority relay capacity for your users. When they're not using it, your capacity helps hobbyists and small communities connect. A share of your subscription funds the protocol itself. You get SLA-backed connectivity; the ecosystem gets funded; nobody owns the network.

---

# Part 20 — Decision Log

Every significant decision made during the project, with reasoning.

## 20.1 Protocol architecture decisions

**Decision:** Peer IDs are opaque, not self-certifying.
**Reason:** Self-certifying IDs prevent root-key rotation without ID change. Opaque IDs bound by signed identity docs allow rotation while preserving identity.

**Decision:** Relationships are per-principal assertions (not dual-signed).
**Reason:** Bilateral object raises "which stream does it live in?" question. Per-principal assertions sidestep this. Recognition is verifier-derived.

**Decision:** Relationship termination is unilateral.
**Reason:** Recognition cannot be coerced. Either principal may withdraw it.

**Decision:** Identity continuity requires dual signatures (old + new roots).
**Reason:** Neither old nor new root alone should claim continuity. Both must agree.

**Decision:** Chain hash uses cumulative commitment (not just previous link).
**Reason:** Bare `previous_hash` can't detect forks. Cumulative hash detects forks even when verifier has seen only one branch.

**Decision:** Sequence spaces are disjoint.
**Reason:** Prevents cross-stream comparison bugs.

**Decision:** Authorization Keys own one heterogeneous stream.
**Reason:** Grants, leases, revocations all sequence together. Makes `effective_sequence` unambiguous.

**Decision:** Key revocation signed by Identity Root (not revoked key).
**Reason:** Compromised key can't be trusted to sign its own revocation.

**Decision:** Failure never grants authorization.
**Reason:** Missing information must not become authority.

**Decision:** Revocation is terminal.
**Reason:** Un-revocation is subtle bug source. New auth requires new object.

**Decision:** StreamResolution requires pre-fork authority.
**Reason:** Key whose own stream is disputed can't be trusted to resolve fork.

**Decision:** Identity Continuity can't bootstrap from untrusted root.
**Reason:** Dual-signed transitions must ultimately reach root trusted before first transition.

**Decision:** Service Link is referential only.
**Reason:** Eliminates second authorization primitive. All authorization from Grant/Lease.

**Decision:** Service ownership transfer not in V1.
**Reason:** Requires authenticated transfer mechanism V1 doesn't define.

**Decision:** Grant validity absolute, lease validity relative.
**Reason:** Grants are issuance events. Leases are ongoing state.

**Decision:** `max_offline_tolerance` bounds freshness, not lease validity.
**Reason:** Keeps layers clean. Lease validity is cryptographic. Freshness is policy.

**Decision:** Revocation is state, not event.
**Reason:** Revocation received before target must stay effective when target arrives.

**Decision:** Ed25519 signatures + SHA-256 hashes.
**Reason:** Widely deployed, well-understood, efficient, small.

**Decision:** Deterministic CBOR with strict canonicalization.
**Reason:** JSON has ordering ambiguity. Protobuf has multiple valid encodings. CBOR canonical rules: unambiguous, efficient.

**Decision:** No version field in signed object.
**Reason:** `domain_separator` carries schema version. Separate field creates disagreement possibility.

**Decision:** Domain separators part of signed payload.
**Reason:** Prevents signature transplant between object types.

**Decision:** Object IDs and payload IDs use distinct framing.
**Reason:** Every crypto construction gets unique tag. No collisions by construction.

## 20.2 Commercial model decisions

**Decision:** Protocol free, development funded.
**Reason:** Free to use/implement/modify. Not free to maintain. Funding from commercial layer.

**Decision:** Commercial layer sells guarantees, not access.
**Reason:** Free users get best-effort. Paid users get priority. Access never gated.

**Decision:** Free users are foundation, not loss leader.
**Reason:** They contribute reachability, P2P efficiency, local relays, ecosystem gravity.

**Decision:** Idle commercial capacity flows to free pool.
**Reason:** Efficient overprovisioning use. Paid users' priority preserved.

**Decision:** Priority is ticket property, not user identity.
**Reason:** Enables privacy, portability, composability.

**Decision:** Credits bound to pool, not freely transferable.
**Reason:** Prevents credit laundering, speculative markets.

**Decision:** Operator-agnostic credits are design goal.
**Reason:** User contribution should be valuable anywhere.

**Decision:** Geographic scarcity multiplies credit value.
**Reason:** Scarce-region relays should earn more per byte. Encourages geographic diversity.

**Decision:** No blockchain for credit system.
**Reason:** Operator count is small. Notarized receipts solve same problem at lower cost.

**Decision:** Developer funding from structural revenue share.
**Reason:** Donations/grants volatile. Revenue share scales with adoption.

**Decision:** Stewardship entity independent of operators.
**Reason:** Prevents commercial capture of protocol.

## 20.3 Positioning decisions

**Decision:** Name is "Grid Network."
**Reason:** NotDNS defined by negation. Mesh heavily used. Lattice/Signet/Ravelin have collisions.

**Decision:** Applications primary adoption path.
**Reason:** Apps adopt Grid like Auth0. Users get it automatically.

**Decision:** Standing on shoulders of DNS, WireGuard, BitTorrent, Bitcoin, Tailscale, Headscale.
**Reason:** Composition is contribution, not individual pieces.

## 20.4 Relay decisions

**Decision:** Relay does not need to terminate encryption.
**Reason:** Endpoints establish end-to-end protected session. Relay forwards encrypted traffic.

**Decision:** Relay is untrusted by design.
**Reason:** Anyone can operate. Cannot forge identity or grant authorization.

**Decision:** Advertise capabilities, not hardware classes.
**Reason:** Hardware implementation-independent.

**Decision:** Low-power nodes can be useful.
**Reason:** Forwarding is much cheaper than terminating encryption. Aggregate value from many small contributions.

**Decision:** Forwarding traffic should not require persistent storage writes.
**Reason:** Reduces SD-card wear, storage requirements, I/O overhead, power consumption.

**Decision:** Direct connectivity is always preferred.
**Reason:** Faster, cheaper, doesn't depend on infrastructure.

**Decision:** Multiple paths can potentially improve throughput when bottlenecks are independent.
**Reason:** Path diversity may provide aggregate capacity. Establishes the case for future multipath.

**Decision:** Multipath cannot defeat an aggregate access-link bottleneck.
**Reason:** If all paths share the same bottleneck, aggregate throughput doesn't increase.

**Decision:** Adaptive scheduling is preferable to naive round-robin striping.
**Reason:** Blind round-robin creates packet reordering when paths differ.

**Decision:** The endpoint owns the multipath state.
**Reason:** Relays remain simple. Endpoints measure and schedule.

**Decision:** Burst tolerance should be treated as a transport phenomenon, not an ISP-evasion objective.
**Reason:** Deliberate excessive bursting causes queues, packet loss, bufferbloat, unfairness, congestion collapse.

---

# Part 21 — Rejected Approaches

Everything considered and rejected, with reasoning.

**XOR obfuscation for endpoints**
No confidentiality against key holders, can't support revocation, can't upgrade without format change.

**Shared-key encryption for endpoints**
Same issues as XOR.

**DNS-like hierarchical naming**
Identifiers must be flat and user-controlled.

**Timestamp-based fork resolution**
Wall-clock time doesn't resolve disagreements.

**Automatic recovery from Identity Root compromise**
No in-band mechanism possible.

**Dual-signature objects in single stream**
Which stream does it live in? Per-principal assertions cleaner.

**Global Sybil resistance in protocol**
Identity count doesn't grant authority. Belongs in policy.

**Proof-of-work as foundation**
Optional at margins, not protocol primitive. Calibration issues, energy consumption, hardware inequity.

**Blockchain for credit settlement**
Operator count small. Notarized receipts sufficient.

**DHT-based discovery in V1**
Deferred. Rendezvous servers sufficient.

**Reputation/liveness scoring in identity**
Belongs in policy layer.

**Adaptive TTLs from heartbeats**
Belongs in policy layer.

**"Raspberry Pis form decentralized relay network" as pitch**
Demoted to example. Capability abstraction is what matters.

**"Mesh bursts around ISP throttling"**
Retained as observation. Not product feature.

**Anonymity in V1**
Kernel can support anonymity without being redesigned around it, but a genuinely strong anonymity system is a major subsystem. Deferred to future.

**Global consensus**
Not needed. Trust problem is local.

**Enterprise features in kernel**
Enterprise functionality is policy layered over the kernel. Not kernel concern.

---

# Part 22 — Glossary

**Peer Principal** — Durable logical identity. May span multiple devices/services.

**Peer Principal ID** — Opaque, randomly generated identifier bound to a principal's identity root by the identity document. Example: `peer:v1:7f3a9c2e5d91b0a4c7e8126fa31d449b`.

**Identity Root** — Highest cryptographic authority. Signs identity documents, relationship assertions, key delegations.

**Device Key** — Authenticates a device; signs reachability records.

**Service Key** — Authenticates a service; signs service records.

**Authorization Key** — Signs grants, leases, revocations in its stream.

**Identity Document** — Signed object binding a Peer ID to an identity root and subordinate keys. Occupies the principal's `stream:identity`.

**Device Binding** — Entry in an identity document that binds a device key to the principal.

**Service Binding** — Entry in an identity document that binds a service key to the principal or device.

**Key Binding** — Entry in an identity document that delegates authority to a subordinate key.

**Relationship Assertion** — Unilateral signed recognition. Two matching assertions = verifier-derived `RECOGNIZED`.

**Relationship Termination** — Unilateral signed withdrawal. Terminal.

**Grant** — Directional signed authorization. Contains capabilities, constraints, lease policy.

**Lease** — Short-lived proof grant currently valid. Bounded by relative validity and freshness.

**Revocation** — Terminal signed invalidation. Once revoked, cannot become valid again.

**Key Revocation** — Revocation of Authorization Key, signed by Identity Root. Contains `effective_sequence`.

**Reachability Record** — Ephemeral signed device endpoint assertion.

**Service Record** — Signed service endpoint + metadata assertion.

**Rendezvous** — Infrastructure storing/serving signed objects. Untrusted.

**Relay** — Infrastructure forwarding encrypted traffic. Untrusted.

**Relay Ticket** — Signed relay-use authorization. Pair-bound, capability-bound, short-lived.

**Service Link** — Referential ID. Not authorization object. Not independently signed.

**Stream** — Ordered sequence of objects sharing sequence space.

**Sequence Space** — Pair `(issuer, stream_id)`. Numbers meaningful only within space.

**Initial Chain Hash** — Base state for stream (`domain_separator` + `stream_id`).

**Chain Hash** — Cumulative stream-history hash.

**Object Commitment** — Hash of object's unsigned payload with domain-separated preimage.

**Signature Input** — Canonical CBOR structure that is signed.

**Object ID** — Hash of signed object's canonical bytes.

**Payload ID** — Hash of unsigned payload's semantic content.

**Authority Precedence Table** — Which object governs in conflicts.

**Signing-Authority Matrix** — Which key role signs each object type.

---

# Part 23 — Anti-Patterns and Design Rules

## 23.1 Anti-patterns

- **XOR-based endpoint obfuscation.** Provides no confidentiality against parties holding the key, cannot support revocation, cannot be upgraded without a format change.
- **Shared-key encryption for endpoint records.** Same issues.
- **DNS-like hierarchical naming.** Protocol identifiers are opaque and flat.
- **Timestamp-based fork resolution.** Wall-clock time is not a resolution mechanism.
- **Automatic recovery from Identity Root compromise.** No in-band mechanism exists or is proposed.
- **Dual-signature objects in a single stream.** Adopted model uses per-principal assertions in per-principal streams.
- **Global Sybil resistance in the protocol.** Identity quantity does not grant authority.
- **PoW as a foundational mechanism.** Optional admission control at the margins.
- **"Raspberry Pis form a decentralized relay network" as product pitch.** Capability abstraction is what matters.
- **"Mesh can burst around ISP throttling" as feature framing.** Underlying observation retained as research note.

## 23.2 The rule for adding mechanisms

Before adding any mechanism, answer all four:

1. What authority or resource does it protect?
2. What specific attack does it prevent?
3. What happens if it is removed?
4. What new complexity does it introduce?

If any answer is unsatisfactory, the mechanism is premature.

## 23.3 Design principles

- **Failure never grants, extends, or changes identity or authorization.**
- **Local state loss is a security-relevant event.**
- **Metadata privacy is different from anonymity.**
- **Every intermediary must be untrusted by design.**
- **Identity is portable. No vendor lock-in.**
- **Byte-level interoperability is non-negotiable.**
- **The protocol is free; the development is funded.**
- **Layers must not cross.**
- **Sequences numbers are meaningful only within their sequence space.**
- **Reconciliation may only select among authenticated branches, not introduce new state.**

---

# Part 24 — The Complete Handoff Package

The complete handoff package for another agent, ready to paste:

## 24.1 What to hand off

1. This document (Master Archive)
2. `PROTOCOL.md` v0.6.2 full text
3. `OBJECTS.md` §1–§5 full text
4. `RATIONALE.md` v2.0 full text
5. `RATIONALE-ADDENDUM-A-COMMERCIAL.md` v6.0 full text
6. `RATIONALE-ADDENDUM-B-LINEAGE.md` v1.0 full text
7. Relay Design Record full text
8. Security Addendum full text

## 24.2 Instructions to the receiving agent

Read this archive in order, starting with Part 1. Then read the full text documents. Your priorities are in Part 17. Do not redesign the protocol — v0.6.2 is frozen. Do not add new object types or authority domains without justification. Do not add security mechanisms unless they protect a specific boundary. Begin with Tier 1: rename Mesh → Grid Network, complete OBJECTS.md §6, complete OBJECTS.md §7, produce first test vector.

## 24.3 Handoff sequence

1. Create repository structure (Part 18.1)
2. Populate files with content from this archive
3. Rename Mesh → Grid Network in PROTOCOL.md
4. Begin Tier 1 work

---

# Appendix A — The Relay Document (Full)

[Full text of the "261004-relay and optimization" document — the complete relay and Pi node discussion, retained verbatim in the project history]

# Appendix B — Security Addendum (Full)

[Full text of the "261004-notdns security addendum" document — the complete security recap, retained verbatim in the project history]

# Appendix C — Rationale Addendum A (Full)

[Full text of RATIONALE-ADDENDUM-A-COMMERCIAL.md v6.0 — the complete commercial model, retained verbatim in the project history]

# Appendix D — Rationale Addendum B (Full)

[Full text of RATIONALE-ADDENDUM-B-LINEAGE.md v1.0 — the complete lineage analysis, retained verbatim in the project history]

---

# End of Archive

This document contains every substantive decision, rationale, design record, and artifact produced over the course of the project. It is organized into four levels (index → parts → documents → appendices) so that any reader can navigate to the material they need.

The archive is complete as of the current date. Future work should be added as additional parts or as separate documents referenced from Part 2.
