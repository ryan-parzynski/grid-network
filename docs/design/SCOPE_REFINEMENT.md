# Grid Network — Scope Refinement History

**Status:** Historical record of design evolution  
**Purpose:** Document what was deliberately removed or narrowed from the original ambitious vision to make the project tractable

---

## Original Ambition vs. Refined Scope

The project started with a fully decentralized, global DHT-based architecture. Through iterative refinement, we deliberately removed or deferred several ambitious features. This document records those decisions.

---

## What Was Removed (and Why)

| Feature | Status | Why |
|---------|--------|-----|
| Universal global DHT for endpoint lookup | Deferred / optional later | Leaks presence/lookup metadata; vulnerable to Sybil/eclipse/poisoning attacks; poor fit for sleeping phones |
| Every endpoint as a routing/discovery participant | Not required | Phones, CGNAT hosts, and low-power devices should not maintain an Internet-scale P2P routing table |
| Global automatic gossip between all coordinators | Removed | Creates unbounded replication, bandwidth, and volunteer burnout |
| Anonymous participation | Not a core goal | Makes abuse control, relay economics, revocation, and private service authorization much harder |
| Fully hidden metadata from coordinators | Not in v1 | A directly contacted coordinator naturally sees source IP and timing; stronger privacy needs optional proxying |
| Permanent free global relays | Explicitly avoided | Becomes a costly encrypted proxy/media-transit network |
| "No central authority anywhere" | Relaxed | Each service owner needs a root of trust to approve/revoke devices and sign policy |
| Global public service search/directory | Excluded | A private home-service directory should not be enumerable |
| Every app shipping its own transport | Avoided | NotDNS agent/client owns the difficult WireGuard/NAT lifecycle |

None of these are essential for "scan QR, use Immich/Jellyfin remotely." In fact, deferring them is what makes the project tractable.

---

## What "Distributed" Means Here

There are three different types of distribution. Grid Network preserves the first two immediately and adds the third selectively.

| Type | Meaning | Grid Network Status |
|------|---------|---------------------|
| **Distributed data plane** | Phone and home server exchange WireGuard traffic directly | Core design |
| **Distributed control availability** | Several independent coordinators/replicas can answer lookup requests | Core design |
| **Distributed operation** | Different people/community groups run coordinators and relays | Core design, with explicit agreements |
| **Fully decentralized global routing** | Every node participates in a DHT/gossip overlay with no chosen authority | Optional future research, not required |

The ordinary successful path is already decentralized in the most important sense:

```
Phone ───────── encrypted WireGuard packets ───────── Home server
             direct peer-to-peer connection

Coordinator:
  only helps the two find one another and obtain current configuration
```

Tailscale uses the same broad split: direct connections send packets directly between devices using UDP, while DERP relays carry packets only when a direct connection cannot be established.

---

## Community Hosting Model

A community member could run one or more NotDNS roles independently.

```
Community operator
  ├── Coordinator
  │    ├── enrollment / policy service for opted-in owners
  │    ├── short-lived endpoint-leases
  │    └── signed replica/cache records
  │
  ├── Replica
  │    ├── stores encrypted/signed lease copies
  │    └── provides failover reads
  │
  ├── STUN / signaling node
  │    └── helps peers discover and test paths
  │
  ├── Relay
  │    └── forwards only ticket-authorized encrypted traffic
  │
  └── Bootstrap mirror
       └── hosts signed manifests and software metadata
```

The operator declares:
```
I host:
  directory replica + signal

I accept:
  up to 10,000 active encrypted leases
  selected service namespaces
  10 MiB/minute replication traffic
  no public enrollment

I do not host:
  shared relay
  private endpoint plaintext
  global federation
```

Another operator might volunteer a small Chicago-area relay pool but cap it at, for example, 10 Mbps total and 250 GB/month. A separate operator could host only public bootstrap mirrors. No individual volunteer needs to take every role.

That is the useful Fediverse-style principle: **autonomous operators publish capacity and choose their obligations**. The difference is that a NotDNS coordinator never needs to carry a global social graph, permanent post archive, or public timeline.

---

## Service Owner Choice

The service owner — not the NotDNS project — chooses who operates their control plane.

```
Alice's Immich installation
  ├── Primary coordinator: Alice's $5 VPS
  ├── Replica: community coordinator in North America
  ├── Replica: friend's homelab coordinator
  ├── User-owned relay: Alice's VPS
  └── Optional shared relay: only when quota allows
```

Or:
```
Alice's Immich installation
  ├── Primary/replica: one all-in-one local VPS deployment
  ├── Public coordinator: disabled
  └── Relay: own VPS only
```

Or:
```
Alice's Immich installation
  ├── Public default coordinator
  ├── Public default replicas
  └── Community fallback relay
```

The same protocol works in all cases. That is what makes it self-hostable rather than merely "a centralized hosted service with source code."

---

## What a Basic Self-Hosted Deployment Needs

A minimal single-owner stack could initially be modest:

```
NotDNS coordinator
  ├── HTTPS API
  ├── SQLite/Postgres storage
  ├── owner/device enrollment
  ├── short-lived signed/encrypted endpoint records
  ├── WireGuard peer-configuration delivery
  ├── STUN endpoint observation
  └── optional local relay endpoint
```

For a user like you, this could plausibly live as a Docker Compose stack or Proxmox LXC on a small VPS, with the RB5009/home server acting as the stable WireGuard-capable endpoint. You would get direct connectivity where NAT permits it, while the VPS gives you a reliable fallback place for coordination and possibly your own relay.

As capacity grows, split it:

```
Coordinator/API         → separate small VPS/container
Signal/STUN             → public UDP-capable host
Relay                   → bandwidth-accounted VPS or volunteer node
Replica/cache           → inexpensive object/database host
Bootstrap manifests     → static site/CDN/Git repository
```

---

## What Community Federation Would Look Like

The project can retain federation without global forced synchronization.

```
Alice-owned coordinator A
  ↔ replicates Alice's authorized encrypted lease records to
Community coordinator B
  ↔ optionally caches selected records at
Friend-operated coordinator C
```

Replication is:
- Explicitly allowed by the owner's signed coordinator manifest
- Bounded by object count, byte rate, and TTL
- Restricted by namespace/service identity
- Signed and versioned
- Recipient-encrypted where endpoint confidentiality is needed
- Terminable by either operator
- Optional; it is not automatic global gossip

A coordinator cannot simply decide: "I see Alice's service; I will replicate it to everyone." It needs a valid replication relationship and the service owner's authorization.

---

## The Tradeoff: Less "Magical," More Dependable

A worldwide DHT/gossip system sounds more decentralized, but it creates difficult questions:

```
Who can publish a record?
Who can query it?
Who sees lookup patterns?
How do phones participate?
How do you prevent fake nodes surrounding a lookup key?
How do you revoke records?
How do you stop global replication?
Who pays for relay bandwidth?
```

The revised NotDNS model answers those with explicit ownership and controlled replication:

```
Who publishes?
  Authorized device identity.

Who can read?
  Authorized service-link recipient.

Who validates?
  Endpoint agent using owner-signed policy and device signatures.

Who hosts?
  Owner, community, volunteer, friend, or public operator.

Who pays for heavy relay traffic?
  Preferably the owner via a VPS; shared relay only under caps.

What happens if a host disappears?
  Use replicas, cached manifests, local discovery, or owner recovery.
```

That is still distributed. It is simply **federated and capability-based**, rather than permissionless and globally replicated.

---

## What Remains as an Optional "More Decentralized" Mode

Later versions could add optional features for users who prioritize minimizing coordinator dependence:

- Encrypted/signed coordinator-manifest pointers in a DHT
- Multiple independent community bootstrap mirrors
- Friend-to-friend cache replication
- User-selected regional coordinator pools
- Peer relay contributions with strict policy and quotas
- Content-addressed manifest distribution
- Tor/I2P/proxy access to coordinators for metadata-sensitive users
- Threshold owner/recovery keys
- Peer-assisted relay selection
- Offline export/import and migration tools

The critical rule remains:

```
DHT / peer discovery can help find coordinators.
It should not be the default public store for current home IPs,
phone endpoints, service ports, or private membership data.
```

---

## Bottom Line

Grid Network still supports community hosting and distributed operation. It loses **permissionless global decentralization as a v1 requirement**, not self-hosting or federation.

The project becomes:

```
Open protocol
+ self-hostable coordinator
+ several independent coordinator operators
+ owner-selected replicas
+ direct WireGuard peer-to-peer paths
+ optional community relay capacity
+ signed migration and recovery
```

rather than:

```
One worldwide DHT
+ mandatory gossip
+ anonymous public endpoint publication
+ every device participates
+ unbounded volunteer relay bandwidth
```

That trade is favorable. It preserves the practical benefits you want — low-friction remote access, failure tolerance, community participation, and user sovereignty — while avoiding the privacy, abuse, mobile-device, and operator-burnout problems that usually kill "fully decentralized" connectivity systems.

---

*End of Scope Refinement History*
