# Grid Network

> **NOTICE** — Heavy AI agent usage in the creation of this project

## What is Grid Network?

Grid Network is a cryptographic identity, authorization, and reachability protocol for portable,
vendor-neutral device connectivity.

Every self-hosted application eventually needs remote access. Today that access either depends on a
vendor (commercial mesh VPNs), requires an expert (self-hosted VPNs), or exposes the user to risk
(port forwarding). The structural reason is that coordination has always required somebody to be the
authority. Authorities cost money to operate, so somebody has to pay.

Grid Network is the first design that solves coordination without introducing an authority.
Identity is a keypair, not an account. Authorization is local, not remote. Discovery is signed, not
centralized. Infrastructure is replaceable, not mandatory.

The result is a protocol that costs nothing to operate, requires nobody's permission, and cannot be
captured by any single entity. It is designed to be for private connectivity what Linux is for
operating systems and TLS is for transport security.

**Current version:** v0.6.2 (frozen)
**Status:** Documentation & Design Phase — reference implementation not yet started

---

## Core Architecture

Grid Network is a **control plane** that sits above existing transports (WireGuard, QUIC, TCP) and
answers three questions:

| Question | Answer |
|----------|--------|
| **Who is this?** | Persistent cryptographic identity — opaque Peer ID bound to Identity Root keypair |
| **What is it allowed to do?** | Signed Grants + short-lived Leases with relative validity |
| **Where can I find it?** | Ephemeral signed Reachability Records |

### Key Properties

- **Identity is portable** — Survives device replacement, network changes, provider changes
- **Authorization is local** — Offline verification, no central authority required
- **Reachability is ephemeral** — Hints, not ground truth; refreshed as networks change
- **Infrastructure is untrusted** — Rendezvous/relay operators cannot forge auth or identity
- **Protocol is open** — No proprietary components; any implementation can interoperate

---

## Quick Start by Audience

| If you are... | Start here |
|---------------|------------|
| Application developer | [`docs/rationale/`](docs/rationale/) — Developer case, integration path |
| Self-hoster | This README — key properties above |
| Skeptic | [`docs/design/SECURITY.md`](docs/design/SECURITY.md) — threat model, blast radius, failure semantics |
| Protocol implementer | [`docs/protocol/PROTOCOL-v0.6.2.md`](docs/protocol/PROTOCOL-v0.6.2.md) — normative spec |

---

## Repository Structure

```
docs/
├── protocol/           # Normative specifications (frozen)
│   ├── PROTOCOL-v0.6.1.md
│   ├── PROTOCOL-v0.6.2.md      ← Current frozen spec
│   └── OBJECTS.md              # Byte-level encoding (§1–§5 done, §6–§10 pending)
├── rationale/          # Design philosophy & decisions
│   ├── DESIGN_RATIONALE.md     # Complete: problem, solution, properties, invariants, pitches
│   ├── ADDENDUM_A_COMMERCIAL.md
│   ├── ADDENDUM_B_LINEAGE.md
│   └── PITCHES.md
├── design/             # Technical design documents
│   ├── SECURITY.md             # Threat model, blast radius, failure semantics
│   ├── FAILURE_MODES.md
│   ├── PAKE_DISCUSSION.md
│   ├── PROTOTYPE.md
│   ├── SCOPE_REFINEMENT.md     # What was removed & why
│   └── HISTORY/                # Original design iterations
├── commercial/         # Business model & economics
│   ├── COMMERCIAL.md           # Complete: tiers, credits, pools, funding, disruption
│   └── RELAY_ECONOMICS.md      # Pi relay analysis, bandwidth aggregation, deployment
├── operations/         # Operational guides
│   ├── CONNECTIVITY.md         # Direct-first, path abstraction, multipath future
│   └── RELAY.md                # Relay model, rendezvous, Pi deployment, economics
├── implementation/     # IMPLEMENTATION.md (placeholder)
└── reference/          # Reference materials
    ├── OVERVIEW.md
    ├── MASTER_ARCHIVE.md       # 24-part complete archive
    ├── PITCHES.md
    └── GPL_REASONING.md

spec/
└── test-vectors/
    └── v0.6.2/         # Test vectors (to be created)

implementations/        # Reference implementations (placeholder)
apps/                   # Application integrations (placeholder)
examples/               # Usage examples (placeholder)
archive/
└── raw-discussions/    # Historical discussion logs
```

---

## Project History

Grid Network evolved through several naming and scope iterations:

| Iteration | Name | Why Changed |
|-----------|------|-------------|
| 1 | Mesh Coordinator | Too technical, didn't communicate value |
| 2 | NotDNS | Defined by negation |
| 3 | Mesh Identity & Reachability Protocol | Acronym awkward, "Mesh" collided with existing library |
| 4 | **Grid Network** (final) | Descriptive, scalable, uncollided |

The design was refined from a fully decentralized global DHT model to a **federated,
capability-based** architecture with explicit trust relationships — preserving self-hosting and
community operation while avoiding privacy, abuse, and operator-burnout problems.

---

## License

GPL v3 — see [`LICENSE.md`](LICENSE.md)

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Current phase: complete OBJECTS.md §6–§10 and produce
first test vectors.
