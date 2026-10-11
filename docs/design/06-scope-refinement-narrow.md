# NotDNS Resolver  
## Executive Summary — Updated v0.1 Design

**Status:** Architecture and product-design proposal  
**Version:** v0.1  
**Date:** September 21, 2026

## Overview

**NotDNS is an open, self-hostable dynamic rendezvous system for stable cryptographic identities operating on changing networks.**

It allows devices, servers, and self-hosted services to find one another again after changes in:

- Public IP address.
- UDP port.
- NAT mapping.
- Internet provider.
- Router.
- Wi-Fi or cellular network.
- IPv4/IPv6 availability.
- Temporary offline periods.
- Relay or transport path.

The central design principle is:

> **Identity and authorization are durable. Reachability and connection paths are temporary.**

NotDNS does not replace WireGuard, DNS, or application authentication. Instead, it provides the missing coordination layer between durable peer identity and changing network location.

WireGuard is the first supported data-plane transport. NotDNS automates the discovery, authorization, endpoint refresh, and reconnection work required to keep existing WireGuard relationships usable over time.

## The core problem

Self-hosted services commonly depend on manually maintained network information:

```text
Public IP address
Dynamic DNS hostname
UDP port
Port forwarding
WireGuard peer configuration
NAT keepalive settings
Relay or VPS fallback
```

That information is fragile. A device may retain the correct cryptographic keys and authorization while losing the ability to find its peer because:

- The ISP changed the public address.
- The router assigned a new external port.
- The phone changed from Wi-Fi to cellular.
- A NAT mapping expired.
- The server was offline for several weeks.
- The home network moved behind CGNAT.
- A previous relay or VPS path changed.

Traditional DDNS updates a name-to-address record. It generally does not manage:

- Authorized peer lookup.
- Multiple endpoint candidates.
- Dynamic UDP port discovery.
- Peer identity association.
- Endpoint lease expiration.
- NAT signaling.
- Transport selection.
- Relay fallback.
- Revocation.
- Decentralized record hosting.

NotDNS addresses this broader problem.

## Product statement

> **NotDNS is decentralized, identity-aware dynamic rendezvous infrastructure for private networks and self-hosted services. It resolves a durable, authorized peer identity into current connectivity candidates and helps the peers establish the best available private path.**

The practical v0.1 experience is:

```text
Pair once
  ↓
Store durable peer identities
  ↓
Refresh current reachability automatically
  ↓
Reconnect after network and endpoint changes
```

A user can configure a phone and home server once, leave the phone offline for 90 days, change the home network’s public IP and UDP port, and reconnect without creating new WireGuard keys or repeating enrollment.

## What NotDNS resolves

Traditional DNS resolves:

```text
hostname → address
```

NotDNS resolves:

```text
authorized node identity
  → current signed endpoint candidates
  → available transport paths
  → permitted private connection
```

A lookup may return:

```text
- Current IPv4 candidates.
- Current IPv6 candidates.
- Current UDP port.
- Transport type.
- Endpoint generation.
- NAT/reachability hints.
- Owner-approved relay path.
- Expiration time.
- Capability-specific connection information.
```

The returned information is signed by the publishing node or owner authority and validated by the receiving device. Coordinators store and distribute records but do not own the underlying identity relationship.

## What persists and what refreshes

### Durable state

```text
- Owner authority key
- Node/device identity
- WireGuard private/public keypairs
- Peer public keys
- Tunnel addresses
- Allowed routes
- Capability grants
- Firewall and service policy
- Trusted coordinator information
```

### Short-lived state

```text
- Public IP candidates
- UDP source and destination ports
- NAT mappings
- Endpoint leases
- Candidate rankings
- Relay tickets
- Current handshake state
- Current path status
```

The most important operational rule is:

> **NotDNS refreshes endpoint discovery, not WireGuard credentials.**

A returning phone normally needs only:

```text
Fresh endpoint lookup
+ updated WireGuard peer endpoint
+ a new handshake
```

It does not need:

```text
- New WireGuard keys.
- New peer identity.
- New enrollment.
- New QR code.
- New service authorization.
```

## Example return-after-90-days flow

```text
1. The phone comes online through Wi-Fi or cellular.

2. It contacts a known NotDNS coordinator over HTTPS or QUIC.

3. It authenticates using its existing device identity.

4. The coordinator returns the latest signed endpoint lease
   for the home server.

5. The phone updates only the dynamic WireGuard endpoint:
   current IP address and UDP port.

6. The phone sends a WireGuard handshake using its existing keys.

7. The home server authenticates the packet and learns the phone’s
   current NAT-mapped source address and port.

8. The private connection resumes.
```

The cryptographic relationship remains unchanged. Only the delivery path is refreshed.

## Core architecture

```text
                    NotDNS control plane

 Phone agent ─────── HTTPS/QUIC ─────── Coordinator
     │                                      │
     │                                      ├── Endpoint leases
     │                                      ├── Identity lookup
     │                                      ├── Authorization
     │                                      ├── Candidate signaling
     │                                      └── Revocation state
     │
     │
     └────────────── WireGuard data plane ──────────────┐
                                                        │
                                             Home-server agent
```

### Control plane

The control plane handles:

- Device enrollment.
- Peer authorization.
- Endpoint publication.
- Endpoint lookup.
- Candidate exchange.
- NAT signaling.
- Coordinator selection.
- Revocation.
- Relay or fallback-path selection.
- Diagnostics.

It does not carry normal application traffic.

### Data plane

The data plane carries:

- Immich traffic.
- Jellyfin traffic.
- Home Assistant traffic.
- SSH.
- Backups.
- Private APIs.
- Other approved network traffic.

WireGuard is the initial data-plane transport. Future transports may include QUIC, TLS, WebSocket, SSH, or adapters for existing VPN systems.

## Identity model

NotDNS separates four concepts.

### Owner identity

The owner authority signs:

- Device approvals.
- Capability grants.
- Coordinator manifests.
- Revocations.
- Policy changes.

### Node identity

A node is an agent-bearing host or device.

Examples:

```text
Alice’s home server
Alice’s phone
Alice’s VPS
Bob’s laptop
Backup worker
```

A node has a durable identity key and publishes current reachability state.

### Transport identity

A transport identity belongs to the selected data-plane system.

For WireGuard, this is the WireGuard keypair:

```text
WireGuard private key
WireGuard public key
```

The transport identity remains stable while the network endpoint changes.

### Capability

A capability is an approved function exposed by a node:

```text
immich-api
jellyfin-stream
home-assistant-ui
ssh-admin
backup-repository
home-network
```

A capability maps to a local service, route, or policy-controlled destination.

## Authorization

Authorization is represented by an owner-signed link grant.

Conceptually:

```text
Bob’s phone
  → Alice’s home-server node
  → immich-api capability
```

A grant can specify:

```text
- Source device.
- Destination node.
- Capability.
- Transport.
- Allowed routes.
- Direction.
- Expiration.
- Revocation generation.
- Relay permission.
- Bandwidth or data limits.
```

A valid device identity does not automatically provide access to every service or route.

## WireGuard as the first transport

WireGuard is the initial transport because it provides:

- Strong peer authentication.
- Encrypted packet transport.
- Efficient roaming.
- Mature implementations.
- Good support for self-hosted infrastructure.
- Existing Linux, router, desktop, and mobile integrations.

NotDNS manages the surrounding lifecycle:

```text
- Persistent peer identity.
- Public-key association.
- Endpoint discovery.
- UDP port refresh.
- Candidate exchange.
- Keepalive selection.
- Peer configuration.
- Revocation.
- Direct-path and fallback selection.
```

WireGuard itself remains responsible for:

```text
- Packet encryption.
- Peer authentication.
- Tunnel transport.
- Cryptographic endpoint roaming.
```

## Direct connectivity and fallback

NotDNS prefers paths in this order:

```text
1. Local network path.
2. Direct IPv6.
3. Direct UDP/WireGuard.
4. UDP hole-punching attempt.
5. Owner-controlled VPS or relay.
6. Approved future shared relay.
7. Clear failure with diagnostics.
```

NotDNS does not promise universal direct connectivity. Some combinations of CGNAT, symmetric NAT, UDP filtering, or corporate firewalling require a relay or hub.

The important distinction is:

> **NotDNS automates endpoint discovery and path selection; it does not eliminate the physical limitations of NAT and firewalls.**

## Decentralized coordinator model

A coordinator is a replaceable rendezvous service.

It may:

- Accept signed endpoint publications.
- Return current endpoint records.
- Deliver authorized peer information.
- Provide candidate signaling.
- Store encrypted, expiring records.
- Publish coordinator metadata.

A coordinator does not need to hold:

- WireGuard private keys.
- Device private keys.
- Owner private keys.
- Decryption keys for unrelated records.
- Ownership of the peer relationship.

The protocol can support:

```text
- Self-hosted coordinators.
- Friend-operated coordinators.
- Community replicas.
- Public bootstrap services.
- Multiple coordinators.
- Selective federation.
- Owner-controlled relay infrastructure.
```

The first implementation may use one coordinator. The protocol should preserve the ability to add replicas, failover, and federation later.

## Endpoint leases

An endpoint lease represents temporary reachability:

```text
Node identity
+ endpoint candidates
+ transport metadata
+ generation
+ expiry
+ publisher signature
```

A lease may include:

```text
203.0.113.42:51820
[2001:db8::42]:51820
```

The lease must:

- Expire automatically.
- Use monotonically increasing generations.
- Reject stale records.
- Be signed by the publishing node.
- Be optionally encrypted for authorized recipients.
- Be replaceable without changing peer identity.
- Be cached only until its signed expiration.

This makes NotDNS functionally similar to dynamic DNS while supporting a richer and more private model.

## Privacy model

NotDNS should make no claim that coordinators are invisible.

A coordinator may observe:

```text
- Source IP.
- Request time.
- Refresh frequency.
- Credential or identity reference.
- Object identifier.
- Ciphertext size.
- Publication activity.
```

Endpoint encryption can protect lease contents from unauthorized readers, replicas, storage operators, and database thieves. It does not automatically hide traffic metadata from the coordinator directly contacted by the device.

The design prioritizes:

```text
- Minimal necessary metadata.
- Signed records.
- Expiring state.
- Recipient-specific encryption where useful.
- Replaceable operators.
- No central ownership requirement.
```

## v0.1 product scope

### Required

```text
- Linux NotDNS agent.
- One coordinator implementation.
- Durable node and device identities.
- Durable WireGuard credentials.
- Signed endpoint leases.
- Authenticated endpoint lookup.
- Multiple endpoint candidates.
- Dynamic UDP-port discovery.
- Endpoint refresh after WAN or NAT changes.
- Existing-peer reconnection after long offline periods.
- Direct WireGuard connectivity attempts.
- Owner-controlled VPS or hub fallback.
- Device and grant revocation.
- Local status and diagnostics.
- Exportable configuration and recovery state.
```

### Demonstration scenario

The first compelling demonstration should be:

```text
1. Pair a phone and home server once.

2. Shut down the home server for several days or weeks.

3. Change the home network’s public IP and UDP port.

4. Move the phone from Wi-Fi to cellular.

5. Start both devices.

6. The phone obtains the server’s current endpoint.

7. Existing WireGuard keys remain unchanged.

8. The connection resumes without new enrollment or manual DDNS updates.
```

This demonstrates the actual product value rather than merely showing a QR-based WireGuard setup wizard.

## Deferred features

```text
- Multiple coordinator consensus.
- Community-wide federation.
- Global DHT discovery.
- Permissionless global routing.
- Shared public relays.
- Advanced recovery manifests.
- QUIC and TLS transport plugins.
- Full mobile platform parity.
- Plugin marketplace.
- Full-network VPN as the default experience.
- Complex application-specific policy enforcement.
```

## Non-goals

NotDNS is not:

```text
- Public DNS.
- A general Internet proxy.
- An anonymity network.
- An unrestricted VPN exit node.
- A public searchable directory of home services.
- A replacement for application authentication.
- A guarantee of direct connectivity through every NAT.
- A requirement that every coordinator store every record.
- A centralized account or identity provider.
- A replacement for every feature of existing mesh VPN products.
```

## Competitive distinction

NotDNS should not compete primarily as:

```text
“A simpler WireGuard setup tool.”
```

That positioning is too narrow and overlaps heavily with existing products.

Its stronger distinction is:

```text
A decentralized, identity-aware dynamic rendezvous layer
for private peers and self-hosted infrastructure.
```

The product combines:

```text
Dynamic DNS
+ authenticated peer lookup
+ endpoint leasing
+ dynamic UDP-port discovery
+ NAT signaling
+ durable WireGuard identity
+ revocation
+ decentralized hosting
```

The short product message is:

> **Pair once. Find each other again anywhere.**

## Final architecture statement

> **NotDNS is an open, self-hostable dynamic rendezvous layer that maps durable authorized identities to temporary network reachability. It allows devices and self-hosted nodes to reconnect after public IP changes, UDP-port changes, NAT churn, network migration, and long offline periods without replacing their cryptographic identities or repeating enrollment.**
>
> **WireGuard is the first data-plane transport. NotDNS manages the control plane: identity, authorization, endpoint leases, candidate discovery, signaling, path selection, revocation, and future federation.**
>
> **The initial release focuses on a reliable and demonstrable capability: pair peers once, allow their WireGuard credentials to persist, and automatically rediscover the current endpoint needed to reconnect later.**

# One-sentence summary

> **NotDNS is decentralized dynamic DNS for authenticated private peers—preserving durable identities while continuously resolving them to current, authorized connection paths.**