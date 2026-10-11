# Grid Network — Connectivity Architecture

---

## §1: DIRECT-FIRST PREFERENCE ORDER

When connecting to a peer, the verifier tries these approaches in order:

1. **Local network (mDNS)** — Broadcast mDNS query for peer. If found: try direct connection on LAN. Latency: <10ms typical.
2. **Direct connection (public IP)** — Obtain peer's public IP from reachability record. Try direct P2P connection. Latency: 50-500ms depending on geography.
3. **NAT traversal (STUN/ICE)** — Peer is behind NAT, has no public IP. Use STUN to detect NAT characteristics. Attempt hole-punching. Latency: 200-1000ms. Success rate: 70-85% depending on NAT type.
4. **Relay (fallback)** — Direct connection failed. Use a relay to forward traffic. Latency: 100-500ms. Cost: Consumes relay bandwidth/credits.
5. **Alternative relay** — Primary relay failed or overloaded. Try secondary relay.

**Design principle:** Always try cheaper/faster options first.

---

## §2: RELAY CAPABILITY MODEL

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

### Relay priority classes:

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

## §3: PATH ABSTRACTION

A "path" is a route from source to destination.

```
Path 1: Direct
  Source → [Internet] → Destination
  Cost: $0, Latency: low

Path 2: Relay A
  Source → Relay A → Destination
  Cost: $0.001/GB, Latency: medium

Path 3: Relay B
  Source → Relay B → Destination
  Cost: $0.001/GB, Latency: medium

Path 4: Relay A → Relay B (future multipath)
  Source → Relay A → Relay B → Destination
  Cost: $0.002/GB, Latency: high
```

Verifier maintains path state: reachability hints, success rates, latencies.

---

## §4: PATH DIVERSITY

**Why multiple relays?** Single relay is single point of failure.

**Solution:** Use multiple relays simultaneously (future multipath).

**Constraints:**
- Do not require multipath for v0.6.2 (too complex)
- Do allow multiple relays in reachability record
- Verifier is free to use any relay or combination

**Economic incentive:**
- Home relays (Raspberry Pi) provide diverse, abundant capacity
- Commercial relays provide reliable, high-capacity backbone
- Together: resilient, distributed infrastructure

---

## §5: RELAY LOAD DISTRIBUTION

Commercial relay operators provision N Gbps of capacity.

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

## §6: GEOGRAPHIC DIVERSITY

**Why geography matters:** Latency depends on geography.

```
Same city: 5-20ms
Same region: 20-100ms
Continent: 100-300ms
Intercontinental: 200-500ms
```

Scarce regions (rural, less-developed) have fewer relays.

**Solution:** Geographic credit multiplier.

```
Relay in NYC (abundant): 1 credit per GB
Relay in rural Nebraska: 2 credits per GB
Relay in remote region: 3+ credits per GB
```

This incentivizes relay operators to deploy in underserved areas.

---

## §7: HOME RELAYS (RASPBERRY PI 3B ANALYSIS)

### Why Raspberry Pi?

| Spec | Value |
|------|-------|
| CPU | Quad-core 1.2 GHz ARM |
| RAM | 1 GB |
| Network | 1 Gbps Ethernet |
| Power | 5W USB |
| Cost | $35 (one-time) |
| Ongoing | ~$2/month electricity |

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

## §8: RELAY AND RENDEZVOUS INTERACTION

Relay and rendezvous are separate services.

**Rendezvous:**
- Stores reachability hints (IP:port)
- Serves hints on query
- Size: Tiny (URLs)
- Bandwidth: Low (lookups only)

**Relay:**
- Forwards encrypted packets
- Pair-bound (specific source → destination)
- Size: Large (packets)
- Bandwidth: High (data forwarding)

### Use cases:

| Case | Rendezvous | Relay |
|------|------------|-------|
| Both peers have public IP | Not needed | Not needed |
| One peer is NAT'd | Needed | Maybe (if NAT punch fails) |
| Both peers are NAT'd | Needed | Probably needed |
| Peer is offline | Serves stale hint if cached | No point |

---

## §9: MULTIPATH (FUTURE)

**Not in v0.6.2.** Planned for v1.5 or v2.0.

### Benefits:
- Redundancy (one relay down, others work)
- Load balancing (spread traffic across relays)
- Congestion avoidance (pick path with lowest latency)
- Resilience (tolerate packet loss)

### Design considerations:
- PathSet abstraction (collection of paths)
- Preference ordering (direct > relay A > relay B)
- Cost model (cost of using multiple paths)
- Ordering semantics (which packets arrive first?)
- Retransmission (retransmit on all paths or just fastest?)

---

## §10: NON-PRECLUSION CONSTRAINTS

**Design rule:** No relay architecture decision should preclude future multipath.

**Constraints:**
- Every relay ticket must specify throughput (max bytes/duration)
- Every relay ticket must be pair-bound (source/dest specific)
- Every relay must accept admission control (reject if overloaded)
- Reachability records must support multiple endpoints
- Verifier must be free to choose which relay to use

These constraints allow:
- Single relay today (simple)
- Multiple relays tomorrow (complex)
- Multipath protocols to be added without breaking v0.6.2

---

*End of Connectivity Architecture draft*
