# Grid Network

This specification was developed with AI assistance.

Grid Network is a cryptographic identity, authorization, and reachability protocol for portable, vendor-neutral device connectivity.

Every self-hosted application eventually needs remote access. Today that access either depends on a vendor (commercial mesh VPNs), requires an expert (self-hosted VPNs), or exposes the user to risk (port forwarding). The structural reason is that coordination has always required somebody to be the authority. Authorities cost money to operate, so somebody has to pay.

Grid Network presents a design that solves coordination without introducing an authority. Identity is a keypair, not an account. Authorization is local, not remote. Discovery is signed, not centralized. Infrastructure is replaceable, not mandatory.

The result is a protocol that costs nothing to operate, requires nobody's permission, and cannot be captured by any single entity. It is designed to be for private connectivity what Linux is for operating systems and TLS is for transport security.

---

## The Problem

Every self-hosted service, every personal server, every home automation system, every private application eventually hits the same wall:

> "How do I reach this from somewhere else?"

This forces every project into one of three bad choices:

1. **Expose to the internet** — Open a port, hope nothing scans you. Firmware vulnerabilities, default credentials, Shodan exposure.
2. **Use a proprietary tunnel/mesh VPN** — Tailscale, Cloudflare Tunnel, ZeroTier, ngrok. The company owns your device graph, access policies, identity. If the vendor disappears, your network loses its definition of who is allowed to talk to whom.
3. **Build it yourself** — Run your own VPN, manage certificates, deal with dynamic DNS, CGNAT, NAT traversal, relay infrastructure, revocation, offline state. Works, but requires sysadmin expertise most people don't have.

---

## The Solution

Grid Network is a **control plane** that sits above existing transports (WireGuard, QUIC, TCP) and answers three questions:

| Question | Answer |
|----------|--------|
| **Who is this?** | Persistent cryptographic identity — opaque Peer ID bound to Identity Root keypair |
| **What is it allowed to do?** | Signed Grants + short-lived Leases with relative validity |
| **Where can I find it?** | Ephemeral signed Reachability Records |

---

## Key Properties

- **Identity is portable** — Survives device replacement, network changes, provider changes
- **Authorization is local** — Offline verification, no central authority required
- **Reachability is ephemeral** — Hints, not ground truth; refreshed as networks change
- **Infrastructure is untrusted** — Rendezvous/relay operators cannot forge auth or identity
- **Protocol is open** — No proprietary components; any implementation can interoperate

---

## Where to Start

| Audience | Start Here |
|----------|------------|
| New reader | This README, then `spec/PROTOCOL.md` |
| Implementer | `spec/PROTOCOL.md`, then `spec/OBJECTS.md` |
| Reviewer | `design/THREAT-MODEL.md`, then `design/RATIONALE.md` |
| Operator | `operations/CONNECTIVITY.md`, then `operations/RELAYS.md` |

---

## Repository Structure

```
grid-network/
├── README.md                 # This file
├── LICENSE.md                # GPL v3
├── CONTRIBUTING.md           # Contribution guidelines
├── ROADMAP.md                # Project roadmap
├── VERSIONING.md             # Versioning policy
│
├── spec/                     # Normative specifications
│   ├── README.md
│   ├── PROTOCOL.md           # Protocol specification (v0.6.2, design-review)
│   ├── OBJECTS.md            # Byte-level encoding (partial)
│   └── TEST-VECTORS/         # Test vectors (to be created)
│
├── design/                   # Rationale and decisions
│   ├── README.md
│   ├── RATIONALE.md          # Design philosophy
│   ├── LINEAGE.md            # Prior art relationships
│   ├── DECISIONS.md          # Decision log
│   └── THREAT-MODEL.md       # Security properties
│
├── operations/               # Infrastructure operation
│   ├── README.md
│   ├── CONNECTIVITY.md       # Direct connectivity, NAT traversal
│   ├── RENDEZVOUS.md         # Rendezvous model
│   └── RELAYS.md             # Relay model
│
├── commercial/               # Economic model
│   ├── README.md
│   └── MODEL.md              # Commercial model
│
├── implementations/          # Reference implementations
├── apps/                     # Application integrations
└── examples/                 # Usage examples
```

---

## License

GPL v3 — see [`LICENSE.md`](LICENSE.md).
