# Relays

Relay model, capability advertisement, deployment, and economics for Grid Network.

---

## 1. Relay Model

A relay is infrastructure for forwarding traffic when a direct path is unavailable or undesirable. It is not an identity authority, authorization authority, or ownership authority.

### 1.1 Core Properties

- **End-to-end encryption:** Relays forward ciphertext only. They cannot decrypt application payloads.
- **No authorization authority:** Relays enforce ticket validity, expiration, byte limits, bandwidth limits, session lifetime, and connection limits. They MUST NOT create identities, grant capabilities, establish relationships, or modify authorization.
- **Replaceable:** Any relay can be swapped without changing identity, authorization, or relationships.
- **Untrusted by design:** A malicious relay can drop traffic, delay traffic, refuse service, observe metadata, and consume its own resources. It cannot impersonate services, grant authorization, read content, change identity, create relationships, forge leases, or become an authority.

### 1.2 Connectivity Preference Order

1. **Local LAN** — Direct. No relay.
2. **Direct IPv6** — Direct. No relay.
3. **Direct IPv4** — Direct. No relay.
4. **NAT traversal** — Direct once established. No relay.
5. **Relay** — Direct failed. Fallback.

In mature deployments with widespread IPv6 and working NAT traversal, most traffic never reaches step 5.

---

## 2. Capability Advertisement

Relays advertise capabilities rather than hardware identity.

### 2.1 Advertised Properties

- Maximum concurrent sessions
- Aggregate bandwidth
- Maximum per-session bandwidth
- Maximum bytes per session
- Maximum aggregate or periodic transfer
- Maximum connection lifetime
- Supported transports
- IPv4/IPv6 availability
- Current or estimated utilization
- Geographic/region metadata
- Latency characteristics
- Availability characteristics
- Supported relay modes
- Privacy-related capabilities
- Operator access policy

### 2.2 Capability Profiles

| Profile | Description |
|---------|-------------|
| BASIC | Ordinary encrypted forwarding with resource limits |
| HIGH_CAPACITY | Optimized for high aggregate bandwidth and large concurrent sessions |
| LOW_LATENCY | Optimized for path latency rather than maximum throughput |
| LONG_LIVED | Supports long-duration forwarding sessions |
| COMMUNITY | Operator-volunteered with explicitly declared access/resource policies |
| PRIVACY | Supports additional privacy-oriented forwarding capabilities |

Profiles are descriptive capability groupings, not separate protocol architectures.


### 2.3 Relay Capability Advertisement (Future Extension)

The relay capability advertisement mechanism allows relays to publish their current operational capabilities and capacity for client path selection.

### RelayNodeRecord

A RelayNodeRecord is a signed object published by a relay node to advertise its capabilities and current operational state.

Fields:
- `relay_node_id` — unique identifier for the relay node
- `operator_id` — identity of the relay operator
- `endpoint` — network endpoint (address, port, transport)
- `capabilities` — set of capability profile identifiers (BASIC, HIGH_CAPACITY, LOW_LATENCY, LONG_LIVED, COMMUNITY, PRIVACY)
- `capacity` — current capacity declaration:
  - `max_concurrent_sessions` — maximum concurrent sessions
  - `aggregate_bandwidth_bps` — aggregate bandwidth in bits per second
  - `max_per_session_bandwidth_bps` — maximum per-session bandwidth
  - `max_bytes_per_session` — maximum bytes per session
  - `max_session_duration_seconds` — maximum session duration
- `availability` — availability declaration:
  - `hours_per_day` — hours per day the relay is available
  - `days_per_week` — days per week the relay is available
  - `uptime_percentage` — expected uptime percentage
- `supported_transports` — set of supported transport protocols (WireGuard, QUIC, TCP, etc.)
- `privacy_capabilities` — privacy-oriented capabilities (e.g., onion forwarding, multi-hop support)
- `operator_policy` — operator access and contribution policy:
  - `access` — public, relationship-required, or operator-approved
  - `contribution` — free, paid, or reciprocal
  - `price` — pricing information if applicable
- `geographic_metadata` — geographic and network metadata:
  - `region` — geographic region
  - `country` — country code
  - `network_asn` — autonomous system number
  - `latitude` — optional latitude
  - `longitude` — optional longitude
- `issued_at` — timestamp of record creation
- `expires_at` — optional expiration timestamp

RelayNodeRecord is signed by the Relay Node Key and published to rendezvous servers. Clients use this information for path selection without centralized load balancers.



---

## 3. Operational State

Static capacity is insufficient. Relays expose current operational state:

```json
{
  "load": {
    "active_sessions": 97,
    "utilization": 0.97,
    "available_bandwidth_bps": 3000000
  }
}
```

Clients use this for path selection without centralized load balancers.

---

## 4. Path Requirements

Applications express connectivity requirements rather than selecting specific relays:

```json
{
  "direct": "preferred",
  "relay": "permitted",
  "min_bandwidth_bps": 20000000,
  "max_latency_ms": 100,
  "max_hops": 3,
  "ipv6": "preferred",
  "privacy_level": 0,
  "minimum_path_lifetime": "2h"
}
```

The local agent evaluates available paths and selects one satisfying the requirements.

---

## 5. Low-Power Node Deployment

### 5.1 Raspberry Pi Class Hardware

A relay does not need to terminate encryption. The workload is packet forwarding with validation/association of relay sessions, limit enforcement, and transient state maintenance — not heavy cryptography per packet.

A Raspberry Pi 3B can contribute meaningfully:
- Network interface speed and packets/second are the limiting factors
- 10-50 Mbps forwarding is achievable
- Even small contributions are valuable when thousands of nodes participate

### 5.2 Resource Contribution Granularity

Community nodes don't need enormous bandwidth:
- 5-50 Mbps
- Occasional availability
- IPv6 connectivity
- Geographically useful location
- Particular ISP/ASN

A node useless as a high-performance server can still be valuable as one more independent path.

### 5.3 Path Diversity Value

Many small nodes create path diversity. When direct flow performs poorly, the network can discover alternative paths through multiple relays and distribute traffic dynamically based on throughput, latency, loss, jitter, congestion, and stability.

This addresses the residential internet problem where single flows achieve only a fraction of advertised bandwidth while aggregate multipath throughput can be much higher.

---

## 6. Relay Untrusted Property

This is the strongest architectural property. A malicious relay can:
- Drop traffic
- Delay traffic
- Refuse service
- Observe metadata
- Consume its own resources

But it cannot:
- Impersonate the service
- Grant authorization
- Read end-to-end protected content
- Change identity
- Create relationships
- Forge leases
- Become an authority

**Permissionless infrastructure, permissioned services.**

---

## 7. Storage Principles

Forwarding traffic, connection statistics, and transient reachability observations MUST NOT require persistent storage writes.

Persistent storage is for:
- Identity keys
- Configuration
- Accepted protocol state
- Bounded authorization/revocation information
- Signed objects
- Checkpoints
- Limited logs

This makes inexpensive flash/SD storage viable for relay operators.

---

## 8. Network Self-Healing

Because relays are interchangeable resources, the network doesn't need a single official relay. If Relay A is overloaded, the network chooses Relay B. If Relay B disappears, connections migrate or establish another path.

Optimize around scarce resources rather than pretending scarce resources don't exist.

---

## 9. Direct Connectivity First

The preferred progression is:
1. IPv6 direct
2. Direct IPv4 / NAT traversal
3. Other suitable direct transport
4. Relay
5. Multiple relays / multipath

The application shouldn't care. It asks "Connect me to Service X." The agent figures out how.

---

## 10. Core vs Future

### V1 Core (Current)
- Identity
- Relationships
- Authorization
- Leases
- Revocation
- Freshness
- Reachability
- Direct connectivity
- Rendezvous
- Simple relay fallback

### Future Transport/Path Extension (V2+)
- Relay capability advertisements
- Path measurement
- Path selection
- Path diversity
- Multipath
- Adaptive scheduling
- Optional redundancy/FEC
- Resource-aware routing
- Geographic/ASN diversity
- Dynamic capacity

Future abstraction: `PathSet` with application requests for `min_bandwidth`, `max_latency`, `multipath`, `max_paths`, `redundancy`.

---

## 11. Economic Model (Summary)

The relay layer enables a spectrum from free/self-hosted to global high-capacity networks:

- Free/self-hosted (Pi, home NAS)
- Community relay (shared VPS)
- Small paid operator
- Regional provider
- Enterprise managed service
- Global high-capacity network

The protocol does not decide which model wins. It makes them interoperable.

See `../commercial/MODEL.md` for full commercial model including credit system, priority classes, geographic scarcity, and developer funding.
