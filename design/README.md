# Design

Design rationale, decisions, threat model, and lineage for Grid Network.

## Files

- `RATIONALE.md` — Why the design is the way it is: the problem, the solution, who it serves, the contribution model, what it enables for applications, the ecosystem that results, edge cases, and frequently raised concerns.
- `LINEAGE.md` — What Grid Network borrows from prior art (DNS, WireGuard, BitTorrent, Bitcoin, Tailscale, Headscale, Matrix, SSH, IPFS, Kerberos), what it does differently, and why the composition produces properties none of them has alone.
- `DECISIONS.md` — Decision log: significant design choices, their alternatives, and why they were made. Includes scope refinements, license choice (GPL v3), and failure mode treatments.
- `THREAT-MODEL.md` — Security properties and non-properties: adversary model, blast radius, failure semantics (F1–F6), security principles, compromise procedures, attack scenarios, implementation requirements, and parser hardening.

## Reading Order

1. `RATIONALE.md` — Start here for the design philosophy.
2. `THREAT-MODEL.md` — For security review.
3. `LINEAGE.md` — For context on prior art.
4. `DECISIONS.md` — For specific design choices.
