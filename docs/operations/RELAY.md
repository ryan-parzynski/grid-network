# Grid Network — Relay & Rendezvous Operations

**Status:** Complete draft  
**Version:** 1.0

---

## Core Architecture: Direct-First Preference Order

When connecting to a peer, the verifier tries these approaches in order:

1. **Local network (mDNS)** — Broadcast mDNS query for peer. If found: try direct connection on LAN. Latency: <10ms typical.
2. **Direct connection (public IP)** — Obtain peer's public IP from reachability record. Try direct P2P connection. Latency: 50-500ms depending on geography.
3. **NAT traversal (STUN/ICE)** — Peer is behind NAT, has no public IP. Use STUN to detect NAT characteristics. Attempt hole-punching. Latency: 200-1000ms. Success rate: 70-85% depending on NAT type.
4. **Relay (fallback)** — Direct connection failed. Use a relay to forward traffic. Latency: 100-500ms. Cost: Consumes relay bandwidth/credits.
5. **Alternative relay** — Primary relay failed or overloaded. Try secondary relay.

**Design principle:** Always try cheaper/faster options first.

---

## Relay Capability Model

A relay is NOT a proxy. It is a pair-bound packet forwarder.

### What a relay does:

```
Device A (203.0.113.1:51820)
    │
    │ Encrypted packet
    │ From Device A to Device B
    ▼
Relay Server
    │ Sees: packet_size, timestamp, device_a_id, device_b_id
    │ Does NOT see: packet content (encrypted)
    │ Does NOT see: which application
    │
    ▼ Forwards packet
Device B (192.0.2.50:51820)
```

Relay bandwidth is metered by relay ticket (bytes/duration).

### Relay priority classes (from commercial model):

- **Free ticket:** Best-effort bandwidth
- **Standard ticket:** 10 Mbps minimum
- **Priority ticket:** 50 Mbps minimum
- **Dedicated ticket:** Reserved capacity

### Relay CANNOT:
- Decrypt content
- Modify packets
- Forge signatures
- Impersonate either party
- Create new relationships
- Issue grants

### Relay CAN:
- See packet counts
- Observe traffic patterns
- Enforce byte limits
- Apply priority queuing

---

## Path Abstraction & Diversity

A "path" is a route from source to destination. Verifier maintains path state: reachability hints, success rates, latencies.

### Why multiple relays?
Single relay = single point of failure. If relay goes offline/overloaded/censors, peer becomes unreachable.

### Diversity types:

**Geographic diversity** — Relays in different regions (NYC, Virginia, NJ) provide redundant paths.

**Provider diversity** — Home Pi relay + AWS + Linode + DigitalOcean. If AWS fails, others continue.

**Autonomous System (AS) diversity** — Relays in different BGP ASes (Cogent, Telia, Level3, Global Crossing). Failure at any one AS → other paths continue.

**Network redundancy** — Primary: direct; Secondary: relay 1; Tertiary: relay 2 (different ISP); Quaternary: relay 3 (different country).

Verifier tries all automatically. User never explicitly chooses.

---

## Relay Load Distribution (Commercial)

Commercial relay operators provision N Gbps capacity.

```
Total: 100 Gbps

Free users: 20 Gbps (first-come-first-served)
Standard users: 40 Gbps (reserved)
Priority users: 30 Gbps (reserved)
Dedicated: 10 Gbps (reserved per customer)

Idle capacity from Standard/Priority/Dedicated users flows to Free pool.

Result: Free users get opportunistic access to 60 Gbps when Standard/Priority don't use it fully.
```

This model:
- Ensures free users always have capacity
- Rewards paid users with guaranteed bandwidth
- Doesn't penalize paid users for overbooking
- Encourages overprovisioning (more capacity = more free benefit)

---

## Geographic Diversity & Scarcity Multipliers

Latency depends on geography:
- Same city: 5-20ms
- Same region: 20-100ms
- Continent: 100-300ms
- Intercontinental: 200-500ms

Scarce regions (rural, less-developed) have fewer relays.

Solution: Geographic credit multiplier.

```
Relay in NYC (abundant): 1 credit per GB
Relay in rural Nebraska: 3 credits per GB
Relay in remote region: 5+ credits per GB
```

Incentivizes relay operators to deploy in underserved areas.

---

## Home Relays (Raspberry Pi 3B Analysis)

### Why Raspberry Pi?

| Spec | Value |
|------|-------|
| CPU | Quad-core 1.2 GHz ARM |
| RAM | 1 GB |
| Network | 1 Gbps Ethernet |
| Power | 5W USB |
| Cost | $35 (one-time) |
| Ongoing | ~$2/month electricity |
| MTBF | 5-10 years (no moving parts) |

### Relay performance on Pi 3B:
- Throughput: 100-200 Mbps (WireGuard encrypted)
- Concurrent connections: 50-200 depending on packet size
- Bandwidth consumption: Residential home upload (typical 5-20 Mbps)
- Operational reliability: 99.5% uptime with proper setup

### Why this works:
Most home internet has asymmetric bandwidth:
- Download: 100-500 Mbps
- Upload: 5-50 Mbps

A Raspberry Pi relay maximizes upload utilization:
- Idle time: relay receives other peers' traffic
- Peak time: relay relays other peers' traffic
- User's own traffic: uses direct connection (doesn't need relay)

### Economic model:
- Pi operator gets credit for relayed bytes
- Earns credits at ~$1/month (for typical usage)
- Breaks even in 35 months
- Then provides free relay for their peers

### Community effect:
- 10,000 Pi relays = 1-2 Tbps potential capacity
- Deployed globally by hobbyists
- No capital expenditure from Grid operators

---

## Bandwidth Aggregation

Problem: Single relay handles ~100 Mbps. Some users need 1 Gbps+.

Solution: Aggregate across multiple relays.

```
User has:
  Pi relay at home: 100 Mbps
  VPS relay 1: 200 Mbps
  VPS relay 2: 200 Mbps
  VPS relay 3: 200 Mbps

Total aggregated capacity: 700 Mbps
```

Verifier connects to first relay, gets some bandwidth. If more needed, opens second relay connection. Load distribution across multiple relays. Cost scales with usage.

---

## Relay & Rendezvous Interaction

Relay and rendezvous are separate services.

| Rendezvous | Relay |
|------------|-------|
| Stores reachability hints (IP:port) | Forwards encrypted packets |
| Serves hints on query | Pair-bound (specific source → destination) |
| Size: Tiny (URLs) | Size: Large (packets) |
| Bandwidth: Low (lookups only) | Bandwidth: High (data forwarding) |

### Use cases:

| Case | Rendezvous | Relay |
|------|------------|-------|
| Both peers have public IP | Not needed | Not needed |
| One peer is NAT'd | Needed | Maybe (if NAT punch fails) |
| Both peers are NAT'd | Needed | Probably needed |
| Peer is offline | Serves stale hint if cached | No point |

---

## Multipath (Future)

Not in v0.6.2. Planned for v1.5 or v2.0.

**Benefits:** Redundancy, load balancing, congestion avoidance, resilience.

**Design constraints (from v0.6.2):**
- Every relay ticket must specify throughput
- Every relay ticket must be pair-bound
- Every relay must accept admission control
- Reachability records must support multiple endpoints
- Verifier must be free to choose which relay to use
- No relay architecture decision precludes multipath

---

## Rendezvous Model

Rendezvous provides discovery. It has **no identity authority**.

### Roles:
- **Publication** — Accepts authorized reachability publications
- **Replica** — Stores signed copies
- **Cache** — Fetches and caches on demand
- **Bootstrap** — Helps peers find manifests
- **Relay coordinator** — Issues relay tickets
- **Freshness source** — Attests to authorization state (only when explicitly authorized)

### Rendezvous invariant (normative):
> Neither a Principal Rendezvous Manifest nor an OperatorManifest grants authority over any principal, service, authorization stream, or reachability state.

### Trust model:
A malicious rendezvous may provide stale/false endpoints, suppress info, observe metadata, or attempt DoS. It MUST NOT forge identity, authorization, or revocation; create a valid lease; or decrypt transport traffic.

---

## Relay Deployment Guide (Home Pi)

### Hardware:
- Raspberry Pi 3B: $35
- Ethernet cable (Cat5e): $5
- Power supply (5V 2A): $5
- MicroSD card (32 GB): $5
- Case: $5
- **Total: $55**

### Software:
1. Download Grid relay software
2. Install on Pi (via SD card image or package manager)
3. Point to home router
4. Software auto-discovers rendezvous
5. Software auto-publishes capacity
6. Done (user contributes relay capacity)

### Operating:
- Electricity cost: $2/month
- Maintenance: None (set and forget)
- Monitoring: Web dashboard (optional)
- Earnings: ~$1/month (100 GB average usage)
- Break-even: 35 months

---

*End of Relay & Rendezvous Operations*
