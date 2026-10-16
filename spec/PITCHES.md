# Grid Network — Pitches

**Revision:** 2.4
**Protocol version:** v0.6.3

**Repository path:** `spec/PITCHES.md`

This document is non-normative. It provides canonical descriptions of
the protocol at several lengths, for use in documentation, talks,
proposals, and introductions. Each pitch states the same thing at a
different scale.

A pitch is not a specification. Where a pitch and the Protocol
Specification conflict, the specification governs.

---

## Ten-second pitch

Grid Network makes private connectivity portable. Your devices, your
identities, your relationships — owned by you, not rented from a
company.

---

## Thirty-second pitch

Every time you want to reach your own devices from outside your home,
you choose between exposing them to the internet or renting a
company's account to coordinate them. Grid Network is a cryptographic
protocol that makes the coordination layer portable. Your identity and
your relationships belong to you, not to a vendor. The result is
private connectivity that behaves like email: anyone can run the
infrastructure, anyone can switch providers, and no company decides
whether your network exists.

---

## One-paragraph pitch

Today, the ability to reach your own devices from anywhere is rented
from companies. Commercial mesh VPNs, tunnels, and coordination
services own your identity and your relationships. If they change
their terms, you migrate or lose access. Grid Network is a protocol
that makes identity and authorization portable. Your devices, your
relationships, your authorizations belong to you, not to a vendor.
Anyone can operate infrastructure, anyone can switch providers, and no
company decides whether your network exists. The model is the same as
email: anyone can run a server, anyone can switch providers, nobody
needs permission.

---

## Developer pitch

You offloaded authentication. Offload this too.

Grid Network is not a replacement for WireGuard, DNS, or anything else
you are already using. It is the layer above them that handles
identity, pairing, discovery, relay fallback, and revocation — the
parts you have been solving badly on your own. Your application calls
a local agent, receives an authorized connection, and stops thinking
about connectivity.

That is the same calculation you made when you decided not to build
your own login system.

---

## User pitch

Your devices, your identity, your relationships. Not rented. Not
revocable by a vendor. Not dependent on any single provider.

It works like email: anyone can run infrastructure, anyone can switch
providers, nobody needs permission. And it is simple enough that you
do not have to think about any of it.

---

## Commercial pitch

Buy priority relay capacity for your users. When they are not using
it, your capacity helps hobbyists and small communities connect. A
share of your subscription funds the protocol itself.

You get SLA-backed connectivity. The ecosystem gets funded. Nobody
owns the network.

---

## Positioning statements

**What this is.** A cryptographic identity and authorization layer
above existing transports.

**What this is not.** Not a VPN, not a DNS replacement, not an
anonymity network, not a blockchain, not a company.

**What makes it different.** Relationships survive infrastructure
changes. Identity is portable. No single entity controls the network.

**Who it is for.** Developers who need remote access in their
applications; self-hosters who want connectivity without a vendor;
operators who want to run infrastructure without a central
coordinator.

**What it costs.** The protocol is free. The specification is free.
Implementations are free to build. Commercial operators sell
guarantees, not access.

---

## Pitches by audience

| Audience | Use |
|---|---|
| Developer evaluating a dependency | Developer pitch |
| End user deciding whether to install | User pitch |
| Operator considering infrastructure | Commercial pitch |
| Executive reviewing a proposal | One-paragraph pitch |
| Conference talk introduction | Thirty-second pitch |
| Slide title or project tagline | Ten-second pitch |