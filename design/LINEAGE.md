# Grid Network — Lineage

**Revision:** 2.1
**Protocol version:** v0.6.2

This document records what the protocol learned from prior systems. It
is non-normative. Its purpose is to credit prior work, to explain which
mechanisms were borrowed and why, and to identify where the design
departs from its predecessors.

The protocol is not novel in its parts. Its novelty is in the
composition.

---

## DNS

DNS solves the problem of finding services by name through untrusted
resolvers.

**Borrowed.** The resolver model, in which queries are answered by
servers the requester does not necessarily trust. Cache semantics that
do not require trust in the source. The TTL concept for ephemeral data.

**Departed.** DNS names are mutable; a name can be pointed at a new
address. Grid Peer IDs are immutable. DNS authority is hierarchical,
with a root; Grid authority is flat. DNS names are human-readable;
Grid identifiers are opaque.

**Why.** Mutable names enable hijacking. Hierarchical authority enables
censorship. The design chose immutability and flat authority to prevent
both.

**Contribution.** Mutable location with immutable identity.

---

## WireGuard

WireGuard solves tunnel encryption and authentication with a small,
auditable implementation.

**Borrowed.** Cryptographic simplicity. The choice of Ed25519 rather
than RSA or ECDSA. Key-based identity rather than certificate-based
identity. Stateless verification.

**Departed.** WireGuard is a transport. Grid is a control plane above
transports. WireGuard's identity has no lifecycle; Grid's identity has
relationships, authorization, and rotation.

**Why.** A transport does not need relationship management. A control
plane does.

**Contribution.** Identity above transport.

---

## Bitcoin

Bitcoin solves decentralized ownership without a central authority.

**Borrowed.** Cryptographic signatures as proof of ownership.
Hash-chain verification that detects tampering. Decentralized
verification without a central server. Offline verification.

**Departed.** Bitcoin uses consensus; Grid uses local verification.
Bitcoin has a global ledger; Grid has local caches. Bitcoin requires
proof-of-work; Grid uses signatures.

**Why.** Consensus is expensive and unnecessary for Grid's use case.
A global ledger creates privacy problems. Proof-of-work has an
environmental cost that is disproportionate.

**Contribution.** Offline verification without consensus.

---

## Tailscale

Tailscale (a commercial mesh VPN) solves the user-experience problem
of VPN setup.

**Borrowed.** QR code pairing. Automatic NAT traversal. Relays as
fallback. Per-peer authorization. Cross-platform support.

**Departed.** Tailscale is account-based. Grid is identity-based.
Tailscale has a central coordination server. Grid treats rendezvous as
replaceable infrastructure. Tailscale's protocol is proprietary; Grid's
is open.

**Why.** Accounts are easier to operate but create lock-in. Central
coordination is simpler but creates a single point of failure.
Proprietary protocols are easier to monetize but limit adoption.

**Contribution.** The same user experience with portability.

---

## Headscale

Headscale solves the problem of self-hosting a Tailscale-compatible
coordination server.

**Borrowed.** The self-hosting model. A community implementation.
Privacy-first design.

**Departed.** Headscale is Tailscale-compatible, which means it
implements Tailscale's protocol and inherits its account model. Grid
is open from the start, with no compatibility requirements.

**Why.** Compatibility with a proprietary protocol limits design
freedom. The design chose freedom over compatibility.

**Contribution.** Self-hosting and portability from the start.

---

## Matrix

Matrix solves federated communication between independent homeservers.

**Borrowed.** The federation model, in which any server can
interoperate with any other. Portable identity that carries across
servers. Event signing that makes objects self-authenticating.

**Departed.** Matrix is for messaging and requires eventual
consistency. Grid is for connectivity and requires only local
verification. Matrix synchronizes state across servers; Grid does not.

**Why.** Messaging needs convergence so that all parties see the same
history. Connectivity needs only verification.

**Contribution.** Federation for the infrastructure layer.

---

## SSH

SSH solves secure remote shell access.

**Borrowed.** Trust-on-first-use pairing. Key-based identity rather
than passwords. Host key verification. Session certificates.

**Departed.** SSH is for terminal access. Grid is application-agnostic.
SSH requires manual key verification; Grid automates pairing with a
PAKE.

**Why.** Terminal access requires strong manual verification because a
single wrong command is catastrophic. Connectivity can use automation.
Manual verification scales to hundreds of servers, not to thousands of
peers.

**Contribution.** Automated PAKE with application-agnostic
authorization.

---

## Kerberos

Kerberos solves enterprise authentication.

**Borrowed.** Time-limited tickets. A trusted key server. Offline
operation using cached tickets. Terminal revocation.

**Departed.** Kerberos is enterprise-only and admin-controlled. Grid is
peer-to-peer and user-controlled. Kerberos requires wall-clock
synchronization; Grid uses relative validity.

**Why.** An enterprise has a central authority. A decentralized system
does not. An enterprise can enforce clock synchronization. A
distributed system cannot.

**Contribution.** Decentralized leases with relative validity.

---

## IPFS

IPFS solves distributed content storage and lookup.

**Borrowed.** Content addressing. Peer discovery. Multi-path routing.

**Departed.** IPFS is for immutable content. Grid is for mutable
identity. IPFS requires a DHT; Grid uses rendezvous. IPFS stores
content on arbitrary peers; Grid stores identity on the owner's chosen
rendezvous servers.

**Why.** Content addressing requires immutability. Identity requires
mutability because keys rotate and relationships change.

**Contribution.** Hash-like identification with mutability.

---

## What is new

Each borrowed mechanism is well-proven. The composition is what is new.

The composition provides:

- Offline-verifiable leases. Kerberos assumes online operation.
- Federated identity without synchronization. Matrix requires eventual
  consistency.
- Portable credentials for mutable identity. IPFS addresses immutable
  content.
- Replaceable infrastructure. Tailscale's coordination server is not
  replaceable without leaving the ecosystem.

A system that is proven in its parts, novel in its composition, and
pragmatic in its scope.