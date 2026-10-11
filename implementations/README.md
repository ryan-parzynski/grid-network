# Implementations

Reference implementations and implementation guides.

## Files

- `README.md` — This file.

## Reading Order

1. Implementation guide (to be created).
2. Platform-specific guides (to be created).

## Current Status

Phase 0 (Documentation) complete. Phase 1 (Reference Implementation) not yet started. See `../ROADMAP.md` for timeline.

## Phase Model (from ROADMAP.md)

The implementation follows the roadmap phases:

| Phase | Timeline | Focus |
|-------|----------|-------|
| **Phase 0** | Q4 2024 | Documentation (complete) |
| **Phase 1** | Q1–Q2 2025 | Reference Implementation — Core agent, local API, CLI tools, test suite, 2+ independent implementations |
| **Phase 2** | Q2 2025 | Local Connectivity — LAN discovery, local relay, device pairing UI, cross-platform support |
| **Phase 3** | Q2–Q3 2025 | Remote Reachability — NAT traversal, candidate gathering, 70%+ direct connection success |
| **Phase 4** | Q3 2025 | Coordinator Resilience — Multiple rendezvous, replica behavior, recovery manifests |
| **Phase 5** | Q3–Q4 2025 | Relay Fallback — Relay protocol, tickets, bandwidth quotas, priority classes, PROTOCOL.md freezes as v1.0 |
| **Phase 6** | Q4 2025 – Q1 2026 | Mobile Integration — iOS/Android agents, background execution, battery <5%/day |
| **Phase 7** | Q1–Q2 2026 | Community Infrastructure — Operator tooling, capacity declarations, federation, credit system |
| **Phase 8** | Q2+ 2026 | Advanced Features — Multi-hop relay, multipath, privacy transport, threshold recovery |

## Implementation Approach

Each phase should leave a working artifact. Don't implement the spec in document order — implement in dependency order:

1. Canonical CBOR + crypto (byte-level foundation)
2. Object/stream engine (state integrity)
3. Identity (cryptographic identity)
4. Relationships (mutual recognition)
5. Authorization (trust decisions)
6. Local agent (usable abstraction)
7. Reachability (endpoint discovery)
8. Direct transport (real connectivity)
9. Rendezvous (decentralized discovery)
10. Relay (connectivity fallback)
11. Application SDK (real application integration)
12. Pairing (human-friendly enrollment)
13. Production hardening (real deployment)
14. Enterprise/privacy/etc. (ecosystem expansion)

The vertical-slice approach is detailed in `../design/DECISIONS.md` and the phase model in `../ROADMAP.md`.
