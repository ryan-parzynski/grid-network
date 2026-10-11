# Grid Network

A cryptographic identity, authorization, and reachability protocol for portable, vendor-neutral device connectivity.

> **Formerly:** "NotDNS" / "Mesh Identity & Reachability Protocol"  
> **Current version:** v0.6.2 (frozen)  
> **Status:** Documentation & Design Phase

## What is Grid Network?

Grid Network is a **control plane** that sits above existing transports (WireGuard, QUIC, TCP) and answers three questions:

1. **Who is this?** — Persistent cryptographic identity (opaque Peer ID bound to Identity Root keypair)
2. **What is it allowed to do?** — Signed Grants + short-lived Leases with relative validity
3. **Where can I find it?** — Ephemeral signed Reachability Records

## Key Properties

- **Identity is portable** — Survives device replacement, network changes, provider changes
- **Authorization is local** — Offline verification, no central authority required
- **Reachability is ephemeral** — Hints, not ground truth; refreshed as networks change
- **Infrastructure is untrusted** — Rendezvous/relay operators cannot forge auth or identity
- **Protocol is open** — No proprietary components; any implementation can interoperate

## Repository Structure

```
docs/
├── protocol/           # Normative specifications (frozen)
│   ├── PROTOCOL-v0.6.1.md
│   ├── PROTOCOL-v0.6.2.md
│   └── OBJECTS.md      # Byte-level encoding (partial)
├── rationale/          # Design philosophy & decisions
│   ├── DESIGN_RATIONALE.md
│   ├── PROTOCOL_RATIONALE.md
│   ├── ADDENDUM_A_COMMERCIAL.md
│   ├── ADDENDUM_B_LINEAGE.md
│   ├── ENGLISH_EXPLANATION.md
│   ├── FUTURE_PROOFS.md
│   └── ELEVATOR_PITCH.md
├── design/             # Technical design documents
│   ├── 01-original-design-v0.1.md
│   ├── 02-resolver-design-v0.1.md
│   ├── 03-resolver-tuning.md
│   ├── 04-scope-refinement-removed.md
│   ├── 05-scope-refinement-massaging.md
│   ├── 06-scope-refinement-narrow.md
│   ├── SECURITY_ADDENDUM.md
│   ├── FAILURE_MODES.md
│   ├── PAKE_DISCUSSION.md
│   └── PROTOTYPE_OUTLINE.md
├── commercial/         # Business model & economics
│   ├── COMMERCIAL_MODEL.md
│   ├── COMMERCIAL_ANGLE.md
│   ├── DISRUPTION_ANALYSIS.md
│   └── RELAY_ECONOMICS.md
├── operations/         # Operational guides
│   ├── RELAY_OPTIMIZATION.md
│   ├── RENDEZVOUS_MODEL.md
│   ├── ROUTER_CONTRIBUTION.md
│   └── RELAY_DISCUSSION.md
└── reference/          # Reference materials
    ├── OVERVIEW.md
    ├── MASTER_ARCHIVE.md
    ├── MASTER_ARCHIVE_FULL.md
    └── GPL_REASONING.md

spec/
└── test-vectors/
    └── v0.6.2/         # Test vectors (to be created)

implementations/        # Reference implementations (placeholder)
apps/                   # Application integrations (placeholder)
examples/               # Usage examples (placeholder)
archive/
└── raw-discussions/    # Historical discussion logs
