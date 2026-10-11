# Extensions

This document describes future extensions to the Grid Network protocol that are not part of the v1 kernel but are architecturally anticipated.

---

## 1. Multi-hop Relay and Onion Anonymity

### 1.1 Multi-hop Relay

Basic multi-hop forwarding is straightforward:

```
A → R1 → R2 → R3 → B
```

Each relay in the path forwards encrypted traffic without terminating the end-to-end encryption. The kernel supports multi-hop relay by chaining RelayTicket objects and RelayNodeRecord advertisements.

### 1.2 Onion Anonymity

Tor-grade anonymity is not simply “three relays.” A genuinely strong anonymity system requires:

- Circuit construction with layered encryption
- Relay compromise resistance
- Guard relay selection
- Timing correlation resistance
- Packet-size correlation resistance
- Traffic volume correlation resistance
- Circuit rotation mechanisms
- Congestion management
- Malicious relay resistance
- Sybil attack resistance
- Relay discovery without metadata leakage
- Exit behavior controls
- Metadata leakage prevention
- Active attack resistance

For example, even if a path `A → R1 → R2 → R3 → B` is encrypted, an observer who can watch both ends might correlate traffic timing and volume.

The kernel can support anonymity without being redesigned around anonymity, but a genuinely strong anonymity system is a major subsystem in its own right.

Another reason not to include it in v1 is that a genuinely strong anonymity system is a major subsystem in its own right.

### 1.2 Anonymity Extension Architecture

Future anonymity extensions would introduce:

- **OnionRouting** object type for multi-hop circuit construction
- **LayeredEncryption** for per-hop encryption
- **CircuitRotation** mechanism for periodic path rotation
- **GuardRelay** designation for entry guard selection
- **ExitPolicy** for exit relay behavior control
- **TrafficPadding** for volume/timing correlation resistance

These extensions would operate as layers above the kernel, composing the existing RelayNodeRecord and RelayTicket primitives.

---

## 2. Advanced Extensions (Future)

### 2.1 Multi-path Connectivity

Future versions may support concurrent use of multiple paths for increased bandwidth, redundancy, and latency optimization. This requires:

- PathSet abstraction for managing multiple concurrent paths
- Adaptive scheduling algorithms
- Congestion control across paths
- Redundancy/FEC for reliability

### 2.2 Dynamic Relay Markets

Future relay markets could enable:

- Automated credit exchange between operators
- Geographic scarcity pricing
- Quality-of-service guarantees
- Reputation systems

### 2.3 Metadata Protection

Future extensions may provide:

- Rotating pseudonyms for rendezvous lookups
- Traffic padding for volume/timing correlation resistance
- Mix network integration for stronger anonymity
