# Grid Network — Relay Operation Guide

**Revision:** 2.4
**Protocol version:** v0.6.3

This document is non-normative. It describes how to operate a relay for
the Grid Network. Where this document and the Protocol Specification
conflict, the Protocol Specification governs.

---

## 1. What a relay is

A relay is infrastructure that forwards encrypted traffic between two
peers when direct connection is not possible. It is a pair-bound packet
forwarder, not a proxy.

A relay does not decrypt content. It does not decide authorization. It
does not define identity. It accepts relay tickets, forwards packets
for the pair named in each ticket, and meters usage.

The pair bound to a ticket is (source device, destination device). The
ticket is signed by the relay's authority key. A relay that receives a
packet without a valid ticket rejects it.

---

## 2. Relay capability model

A relay advertises its capabilities through an `OperatorManifest`. The
manifest declares:

- supported transport families (UDP, TCP, QUIC)
- maximum bandwidth
- maximum concurrent sessions
- maximum bytes per session
- maximum session duration
- expected latency characteristics
- expected availability
- geographic region

The manifest is signed by the relay's identity root and published to a
well-known rendezvous server so that peers can obtain it before
connecting. How the manifest is discovered is a deployment choice;
typical deployments publish the manifest URL out-of-band, in
documentation, or through a directory service.

A relay's admission control rejects a ticket when capacity is
exhausted. Rejection is an availability failure, not an authorization
failure. The verifier responds by trying an alternative relay.

---

## 3. Relay ticket lifecycle

A ticket is issued by a relay's authority key in response to a request
from a device that wishes to use the relay. The ticket binds the source
device to a destination device, bounds the capacity, bounds the
duration, and assigns a priority class.

**Issuance.** The requesting device authenticates to the relay's
authority (using its identity root or a delegated key) and requests a
ticket. The relay issues the ticket if its policy permits.

**Use.** The device presents the ticket to the relay when it sends the
first packet. The relay validates the ticket and begins forwarding.
Subsequent packets in the same session use the ticket's session
identifier.

**Expiry.** The ticket expires when its `expires_at` passes or when its
`capacity` is exhausted. On expiry, the session terminates.

**Renewal.** A ticket is renewed by requesting a new ticket. The
protocol does not define a renewal mechanism within a ticket; a new
ticket is issued.

---

## 4. Capacity planning

A relay operator plans capacity in three dimensions: bandwidth,
concurrent sessions, and total throughput.

**Bandwidth.** Determined by the uplink to the internet. A relay's
maximum bandwidth is the lesser of its uplink and its own forwarding
capability. The forwarding capability of a relay is bounded by CPU,
memory, and network interface.

**Concurrent sessions.** Each active pair consumes state. On
commodity hardware, per-session state is a few hundred kilobytes. A
relay with 1 GB of memory available can handle roughly 1,000
concurrent sessions, subject to CPU.

**Total throughput.** The product of average session bandwidth and
session count, capped by the uplink.

An operator should provision for peak load rather than average. Idle
capacity during troughs is not wasted; in the current commercial model,
idle capacity from paid reservations flows to free users.

---

## 5. Home relay deployment

A low-cost single-board computer such as a Raspberry Pi 3B is adequate
for a home relay. The board's forwarding capability substantially
exceeds the typical residential uplink, so the uplink is the binding
constraint.

### 5.1 Hardware

An illustrative configuration:

| Component | Cost | Note |
|---|---|---|
| Single-board computer (Pi 3B class) | ~$35 | One-time |
| Ethernet cable | ~$5 | Cat5e sufficient |
| Power supply | ~$5 | 5V 2A |
| Storage card | ~$5 | 32 GB sufficient |
| Case | ~$5 | Optional |

Total hardware cost is roughly $55.

### 5.2 Software installation

1. Install the relay software on the board. A pre-built image or a
   package-manager installation is typical.
2. Connect the board to the home router with Ethernet.
3. Configure the relay with the operator's identity root (a fresh root
   for the relay, or a delegated key).
4. The relay discovers a rendezvous server and publishes its
   `OperatorManifest`.
5. The relay is now accepting tickets.

### 5.3 Operating cost

Power draw is roughly 5 W sustained. At typical residential electricity
rates this is under $1/month. The board has no moving parts and a
multi-year operating lifetime.

### 5.4 What the operator earns

A home relay earns credits for the bytes it forwards. The exchange rate
is defined by the operator's policy within the bounds of the credit
model. Typical earnings for a home relay with light usage are modest;
the break-even against electricity alone is measured in months, and
against hardware in years.

The primary benefit of running a home relay is not revenue. It is the
credits earned, which offset the operator's own relay usage, and the
contribution to network resilience.

---

## 6. Bandwidth aggregation

A single home relay's capacity is bounded by the residential uplink.
Users who need more bandwidth can aggregate multiple relays.

**Aggregation.** A reachability record may list multiple relay
endpoints. A verifier opens sessions to multiple relays and distributes
traffic across them.

**Cost.** Each relay used incurs its own ticket and its own credit
cost. Aggregation is not free.

**Practical pattern.** A user with a home relay and a small number of
cloud relays can achieve bandwidth substantially above any single
relay's capacity. The home relay serves as the free base; cloud relays
add capacity when needed.

---

## 7. Path diversity

Relay operation should aim for diversity along four axes.

**Geographic.** Relays in different cities, regions, or continents.
Latency between source and destination varies by geography; a relay
near the destination is generally better than one near the source for
download-heavy traffic.

**Provider.** Relays operated by different operators. A single
operator's failure does not remove all paths.

**Autonomous system.** Relays in different ASes. A routing failure at
one AS does not remove all paths.

**Network.** Relays on different physical networks. A last-mile failure
at one site does not remove all paths.

A deployment that uses a single relay of a single operator in a single
AS is a deployment with a single point of failure. A deployment that
uses multiple relays across multiple axes can tolerate any single
relay's failure.

---

## 8. Relay economics

A relay operator earns revenue through two channels: paid tier
subscriptions and credit settlement with other operators. The economics
depend on the operator's scale, cost structure, and mix of users.

### 8.1 Cost structure

The dominant cost is bandwidth. For a cloud-hosted relay, bandwidth is
metered by the provider. For a home-hosted relay, bandwidth is the
residential uplink, and the cost is the electricity to run the board.

Secondary costs: hardware, monitoring, support, and the developer fund
contribution (a fraction of revenue).

### 8.2 Revenue structure

Revenue comes from subscriptions at the standard, priority, and
dedicated tiers. Free-tier users pay nothing; they are supported by the
idle capacity that paid users do not use.

### 8.3 Break-even

A relay breaks even when subscription revenue covers cost. The
relationship between capacity and revenue is roughly linear at scale;
larger operators have lower per-gigabit costs because of better peering
and amortized overhead.

An operator should model their own cost and revenue. The figures in the
Commercial Model are illustrative defaults, not promises.

---

## 9. Relay key rotation

A relay's authority key signs tickets. Rotating it does not invalidate
existing tickets until they expire, because tickets are validated
against the key that signed them.

To rotate:

1. Generate the new authority key.
2. Publish a new `OperatorManifest` under the relay's identity root,
   declaring the new key as `current_relay_authority_key`.
3. Existing tickets remain valid until they expire.
4. New tickets are signed by the new key.
5. After the transition period, revoke the old key.

A peer that has an old manifest and attempts to use an old ticket will
succeed until the ticket expires. A peer that requests a new ticket
uses the current manifest and receives a ticket signed by the current
key.

---

## 10. Relay failure modes and response

**Relay is unreachable.** Peers with active sessions lose connectivity
and retry via alternatives. New sessions are not admitted.

**Relay is overloaded.** New ticket requests are rejected. The
rejection is not an authorization failure. Peers try alternatives.

**Relay is compromised.** The attacker can observe metadata (packet
size, timing, source, destination), drop traffic, and inject traffic.
Injected traffic is rejected by transport-level authentication. The
attacker cannot decrypt content or change authorization.

**Relay is malicious.** A malicious relay can selectively deny service
to specific pairs. It cannot forge authorization or decrypt content.
The mitigation is the same as for any infrastructure: use multiple
providers.

**Relay's authority key is compromised.** The identity root publishes
a `KeyRevocation` for the compromised key. New tickets are not issued
under the compromised key. Existing tickets remain valid until they
expire.

---

## 11. Operational monitoring

An operator should monitor:

- Bandwidth utilization per minute and per hour.
- Session count and duration distribution.
- Ticket rejection rate (indicates overload).
- Peer satisfaction (through indirect signals; the protocol does not
  define a satisfaction metric).
- Reliability (uptime, latency percentiles).
- Geographic distribution of requests.

The data belongs to the operator. The protocol does not export it and
does not require it to be shared.

---

## 12. Credit accounting

An operator tracks credits earned and spent. Credits are earned when a
relay forwards bytes for another operator's user. Credits are spent
when an operator's user uses another operator's relay.

Credit accounting is an operator-local concern in the current protocol
version. Cross-operator settlement is a `planned` feature. In the
current protocol version, an operator's credit balance is internal.

The exchange rate between credits and bytes is defined by the
operator's policy. The default is `CREDIT_TO_GB_RATIO`. Geographic
multipliers for scarce regions are defined by the operator, with
defaults `GEOGRAPHIC_MULTIPLIER_ABUNDANT`, `GEOGRAPHIC_MULTIPLIER_SCARCE`,
and `GEOGRAPHIC_MULTIPLIER_VERY_SCARCE`.