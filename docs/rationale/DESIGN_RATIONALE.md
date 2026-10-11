# Mesh Identity & Reachability Protocol

## Relay, Low-Power Nodes, Path Diversity & Residential Connectivity Design Record

**Status:** Design record / architectural rationale
**Related protocol:** Mesh Identity & Reachability Protocol v0.6 / planned v0.6.1
**Purpose:** Preserve the reasoning, alternatives, conclusions, and unresolved questions surrounding relay infrastructure, Raspberry Pi/community nodes, residential connectivity, bandwidth behavior, and future multipath/path-selection capabilities.

---

## 1. Purpose of This Document

This document records a substantial design discussion about the role of relays and low-power devices in the Mesh Identity & Reachability Protocol.

The discussion began with a practical question:

> Can inexpensive devices such as Raspberry Pis provide useful relay infrastructure?

It expanded into several related questions:

* Does a relay need to terminate WireGuard or other encryption?
* How capable can a Raspberry Pi 3B be as a relay?
* What persistent storage does a relay need?
* Can thousands of inexpensive community nodes create meaningful aggregate infrastructure?
* Is relay infrastructure still important as NAT traversal and direct connectivity improve?
* Why do residential peer-to-peer connections sometimes achieve much less than advertised bandwidth?
* Can multiple independent paths improve this?
* Is the behavior analogous to torrent swarms?
* Can burst tolerance or flow fairness be leveraged?
* What existing technologies already solve parts of this problem?
* Should multipath be part of the Mesh kernel?
* What should be standardized now versus deferred?

The resulting architectural position is:

> **Relays should be treated as replaceable, untrusted connectivity resources rather than authorities or mandatory intermediaries. Direct connectivity should be preferred whenever practical. A future path-selection/multipath layer can exploit multiple independent paths when doing so improves throughput, resilience, latency, or availability. Low-power devices can contribute useful capacity because the value of the network comes from distributed resources and path diversity, not merely from individual node performance.**

This document is deliberately outside the normative protocol kernel. It records design rationale and future direction rather than adding requirements to v0.6.1.

---

# 2. Core Architectural Context

The Mesh protocol is fundamentally a **control plane above existing transports**.

Its primary responsibilities are:

1. cryptographic identity
2. relationships
3. authorization
4. leases
5. revocation
6. freshness
7. service/device identity
8. reachability information
9. discovery/rendezvous
10. selection of an appropriate connectivity path

It is deliberately not:

* a replacement for IP
* inherently a VPN
* inherently a relay network
* a blockchain
* a global identity registry
* an anonymity network
* a mandatory cloud service
* an application authorization replacement

The architectural abstraction is approximately:

```text
Application
     │
     ▼
Mesh Agent
     │
     ├── Identity
     ├── Relationship
     ├── Authorization
     ├── Service identity
     ├── Reachability
     ├── Discovery
     └── Path selection
              │
       ┌──────┼────────┐
       ▼      ▼        ▼
    Direct  Relay    Future
   transport          paths
       │      │        │
       └──────┼────────┘
              ▼
        Existing network
```

The application should ideally ask:

> “Connect me to this service identity.”

It should not need to know whether the eventual path uses:

* IPv6
* direct IPv4
* NAT traversal
* QUIC
* WireGuard
* another supported transport
* a single relay
* multiple relays
* future multipath mechanisms

---

# 3. Relay as a Connectivity Resource

## 3.1 Fundamental role

A Mesh relay is best understood as a **forwarding resource**.

It is not:

* an identity authority
* an authorization authority
* a service owner
* a relationship authority
* a rendezvous authority
* an application proxy

Its job is to help packets get from one endpoint to another when direct connectivity is unavailable, undesirable, or insufficient.

The preferred conceptual model is:

```text
Endpoint A
    │
    │ encrypted traffic
    ▼
Relay
    │
    │ encrypted traffic
    ▼
Endpoint B
```

The relay should preferably never need to see plaintext application traffic.

---

# 4. Relay Does Not Need to Terminate WireGuard

An important clarification emerged during the discussion.

A conventional WireGuard hub might terminate WireGuard at the hub:

```text
A ── WireGuard ──> Hub
                    │
                 decrypt
                    │
                 re-encrypt
                    │
                    B
```

That is **not the preferred Mesh relay model**.

Instead:

```text
A ── encrypted packet ──> Pi Relay ── encrypted packet ──> B
```

The endpoints establish their end-to-end protected session.

The relay forwards the resulting encrypted traffic.

This has several advantages:

* less CPU work at the relay
* no application plaintext at the relay
* smaller security boundary
* compromise of the relay does not reveal application content
* relay operators do not need application credentials
* inexpensive hardware becomes more viable
* relays remain interchangeable

A relay may still need to perform limited control-plane checks, such as:

* identifying the relay session
* validating a RelayTicket or equivalent forwarding authorization
* enforcing expiration
* enforcing byte limits
* enforcing rate limits
* enforcing session limits
* applying local admission policy

But these checks should not turn the relay into an application or identity authority.

---

# 5. Security Boundary of Relays

The central security principle is:

> **Relays are untrusted transport infrastructure. Compromise or malicious operation of a relay MUST NOT by itself grant application authorization, identity authority, or access to end-to-end protected payloads.**

A malicious relay should primarily be able to cause:

* packet loss
* delay
* disconnection
* reduced availability
* traffic analysis
* metadata observation
* resource consumption against the relay itself

It should not be able to:

* forge a service identity
* create a relationship
* issue a grant
* issue a lease
* revoke another principal's authorization
* impersonate a service
* decrypt end-to-end protected content

This separation is one of the strongest architectural properties of the protocol.

---

# 6. Direct Connectivity Comes First

An important refinement during the discussion was that the protocol should **not assume relays are required for NAT traversal**.

Networking technology continues to improve.

Potential direct mechanisms include:

* IPv6
* direct IPv4
* NAT traversal
* UDP hole punching
* PCP
* QUIC
* WireGuard
* other standardized or implementation-specific mechanisms
* future transport technologies

Therefore the preferred progression is conceptually:

```text
1. Direct IPv6
        ↓
2. Direct IPv4 / NAT traversal
        ↓
3. Other suitable direct transport
        ↓
4. Relay fallback
        ↓
5. Multiple relays / multipath when useful
```

This makes Mesh transport-neutral and future-proof.

The protocol should not become obsolete if NAT traversal gets significantly better.

Instead, improved networking automatically becomes another tool available to the Mesh path-selection layer.

---

# 7. Why Relays Still Matter

Better NAT traversal does not eliminate all difficult environments.

Examples include:

* symmetric or restrictive NAT
* carrier-grade NAT
* corporate firewalls
* hotel/public Wi-Fi
* restrictive carrier networks
* IPv4-only networks
* networks where inbound UDP is unavailable
* networks where port mapping cannot be established
* local policy prohibiting direct connectivity
* cases where direct connectivity exists but has undesirable performance
* cases where an alternative path has better latency, reliability, or bandwidth

Therefore the relay is best viewed as an **escape hatch**.

The argument for relays is no longer:

> “NAT is impossible without them.”

It is:

> “There should always be a replaceable path resource available when the best direct path is unavailable or inadequate.”

That is a stronger and more future-proof position.

---

# 8. Why Low-Power Devices Can Matter

The discussion initially considered whether Raspberry Pi-class hardware was sufficiently powerful.

The conclusion was that the answer depends heavily on what the relay is actually doing.

If the relay is terminating encryption and acting as a full VPN hub, CPU and cryptographic processing become more significant.

If it is primarily forwarding already-encrypted traffic, the workload becomes much lighter.

A low-power node can therefore contribute:

* a small amount of bandwidth
* a geographic location
* a particular ISP/ASN
* IPv4 or IPv6 reachability
* an additional independent path
* temporary capacity
* redundancy
* local/community infrastructure

The value does not have to come from a single powerful machine.

---

# 9. Raspberry Pi 3B as an Example

A Raspberry Pi 3B has modest resources and a 100-Mbit Ethernet interface.

It should not be assigned a normative performance guarantee by the protocol.

However, as a planning concept, a Pi 3B can be useful as a modest relay because:

* forwarding is much cheaper than application processing
* the relay need not persist packet data
* end-to-end encryption remains at the endpoints
* the 100-Mbit Ethernet interface is itself a meaningful ceiling
* actual capacity depends on packet size, packets per second, concurrent sessions, OS/network stack, Internet uplink, and implementation

The correct engineering approach is therefore:

> **Benchmark actual implementations rather than encode hardware performance assumptions into the protocol.**

A Pi 3B should be viewed as a possible community node, not as a prescribed relay class.

---

# 10. Advertise Capabilities, Not Hardware Classes

The protocol should not fundamentally advertise:

> “This is a Raspberry Pi 3B.”

Instead it should expose useful capabilities.

A future `RelayCapability` concept might include:

```text
roles
transport capabilities
maximum bandwidth
maximum concurrent sessions
maximum bytes
maximum session duration
maximum concurrent paths
network-family support
latency characteristics
availability expectations
geographic metadata
privacy capabilities
operator policy
```

The meaningful property is:

> “This resource can provide these connectivity characteristics.”

not:

> “This resource contains this CPU.”

The same protocol can therefore operate across:

* Raspberry Pis
* routers
* NAS systems
* laptops
* x86 servers
* VPS instances
* cloud infrastructure
* dedicated relay hardware

---

# 11. Stable Capability vs Dynamic State

An important distinction is required between **capability** and **current utilization**.

Stable or relatively stable information might include:

* maximum supported bandwidth
* supported transports
* IPv4/IPv6
* maximum sessions
* policy
* geographic/ASN metadata
* expected availability

Dynamic state includes:

* current bandwidth
* current session count
* congestion
* current path quality
* temporary reachability
* current resource consumption

Dynamic state should generally remain ephemeral.

The protocol should not require a relay to persist every utilization change.

For example:

```text
Relay:
    configured capacity = 50 Mbps

Current:
    37 Mbps in use
    13 Mbps estimated available
```

The latter can be local operational state.

---

# 12. Persistent Storage Requirements

A relay does not need large persistent storage merely to forward traffic.

Persistent state can include:

* identity keys
* configuration
* accepted protocol state
* signed objects
* revocation state
* checkpoints
* bounded logs
* administrative metadata

It should not need to perform:

```text
packet → disk
packet → disk
packet → disk
...
```

for normal forwarding.

A useful design invariant is:

> **Forwarding traffic, connection statistics, and transient reachability observations MUST NOT require persistent storage writes.**

This reduces:

* SD-card wear
* storage requirements
* I/O overhead
* power consumption
* complexity

It also makes inexpensive hardware substantially more practical.

---

# 13. Community Infrastructure Model

A particularly important conclusion was that the value of low-power nodes can come from **scale and distribution**.

Imagine:

```text
Home A → Pi relay → 10 Mbps
Home B → Pi relay → 20 Mbps
Home C → Pi relay → 30 Mbps
Home D → Pi relay → 50 Mbps
NAS E  → relay    → 100 Mbps
VPS F  → relay    → 1 Gbps
```

No individual household needs to operate a major data center.

Instead, the network gains:

* many alternative paths
* geographic diversity
* ISP diversity
* ASN diversity
* redundancy
* aggregate resources

A node that contributes only 10 Mbps can still be useful.

This suggests a general principle:

> **Community connectivity infrastructure can be valuable through distributed small contributions, not only through high-capacity centralized nodes.**

---

# 14. Network Self-Healing

Because relays are replaceable resources, the network can adapt to resource scarcity.

If:

```text
Relay A → overloaded
```

the path selector can choose:

```text
Relay B → available
Relay C → available
Relay D → available
```

If:

```text
Relay B → disappears
```

the system can establish another path.

If one ISP path becomes congested, another path may be preferable.

If a geographic region lacks resources, additional nodes can increase its available capacity.

The design principle is:

> **Optimize around scarce resources rather than pretending scarcity does not exist.**

Potential scarce resources include:

* bandwidth
* latency
* relay capacity
* uptime
* geographic availability
* IPv4
* IPv6
* connection slots
* CPU
* battery
* storage

---

# 15. Residential Bandwidth Problem

A major part of the discussion concerned an observed practical phenomenon:

> Residential-to-residential peer-to-peer transfers can sometimes achieve a surprisingly small fraction of the advertised access bandwidth.

The important conclusion is **not** that all residential ISPs deliberately throttle peer-to-peer traffic.

There are many possible causes:

* ordinary congestion
* peering constraints
* routing
* traffic engineering
* fair queuing
* per-flow scheduling
* TCP congestion behavior
* traffic management
* access-network architecture
* CGNAT
* asymmetric links
* bottlenecks elsewhere in the path

An advertised 500-Mbit/s service does not necessarily mean that an arbitrary end-to-end flow to another residential subscriber will obtain 500 Mbps.

---

# 16. Fair Sharing and Multiple Flows

The discussion examined ISP/network fairness behavior.

A network can apply fairness at different levels:

```text
subscriber
household
access link
destination
flow
TCP connection
```

This matters enormously.

If a bottleneck effectively gives each flow a share:

```text
One flow:
    50 Mbps

Several flows:
    50 + 50 + 50 + ...
```

then applications using many flows can achieve greater aggregate throughput.

Torrent swarms are an intuitive example because they typically involve many simultaneous peer connections.

However, if the ISP enforces an aggregate subscriber limit:

```text
Subscriber:
    500 Mbps maximum

Flow 1: 100
Flow 2: 100
Flow 3: 100
Flow 4: 100
Flow 5: 100
```

then adding more flows cannot exceed the aggregate access capacity.

Therefore:

> **Multipath cannot defeat an aggregate physical/access-link bottleneck.**

Its value appears when bottlenecks are sufficiently independent.

---

# 17. The Key Distinction: Multiple Flows vs Multiple Paths

Opening many connections does not necessarily create independent network paths.

For example:

```text
Flow 1 ─┐
Flow 2 ─┤
Flow 3 ─┼── same bottleneck ── destination
Flow 4 ─┘
```

may simply divide the same bottleneck differently.

The more interesting situation is:

```text
Path A ── bottleneck A ──┐
Path B ── bottleneck B ──┤
Path C ── bottleneck C ──┼── destination
Path D ── bottleneck D ──┘
```

If the paths have sufficiently independent constraints, aggregate throughput can potentially increase.

That is the fundamental motivation for future Mesh path diversity.

---

# 18. Multipath Relay Concept

A future Mesh implementation could discover:

```text
             Relay A
            /       \
           /         \
Endpoint A             Endpoint B
           \         /
            \       /
             Relay B
```

or:

```text
Endpoint A
    │
    ├──── direct ──────────────── Endpoint B
    │
    ├──── Relay A ─────────────── Endpoint B
    │
    ├──── Relay B ─────────────── Endpoint B
    │
    └──── Relay C ─────────────── Endpoint B
```

The endpoint could maintain several simultaneously usable paths.

Traffic could then be distributed according to measured conditions.

The relays do not need to know that they are part of a larger multipath system.

Each relay simply forwards opaque traffic.

---

# 19. Existing Multipath Technologies

The discussion examined existing technologies to avoid reinventing solved problems.

Important examples include:

### MPTCP

Multipath TCP allows one logical connection to use multiple subflows.

Relevant lessons:

* path managers
* packet schedulers
* congestion control
* path measurement
* failover
* packet reinjection
* dynamic path selection

MPTCP demonstrates that multipath aggregation is a practical engineering problem, not merely a theoretical concept.

### MLVPN

Multi-Link VPN systems demonstrate:

* multiple-link aggregation
* heterogeneous links
* failover
* packet reordering
* practical bandwidth aggregation

### OpenMPTCProuter

Demonstrates practical residential multi-link aggregation using technologies such as MPTCP and multipath QUIC approaches.

It generally uses a VPS/aggregation point and multiple Internet connections belonging to the same user.

### Important distinction

These systems typically solve:

> “How do I combine multiple links that I control?”

The Mesh concept potentially extends the idea to:

> **“How can I select and combine useful paths supplied by independently operated community nodes?”**

That is the potentially novel architectural aspect.

---

# 20. Torrent Analogy

Torrent swarms provide a useful analogy but should not be copied directly.

A torrent can obtain high aggregate throughput because it communicates with many peers.

Conceptually:

```text
Peer 1 ─┐
Peer 2 ─┤
Peer 3 ─┤
Peer 4 ─┼── local endpoint
Peer 5 ─┤
Peer 6 ─┘
```

Different connections may encounter:

* different congestion
* different routes
* different bottlenecks
* different peers
* different access networks

Mesh could use a similar principle deliberately, while still maintaining one logical service connection.

The important difference is that Mesh would ideally preserve:

* service identity
* authorization
* end-to-end encryption
* explicit path policy
* controlled resource use

rather than simply creating many application-level transfers.

---

# 21. Burst Behavior

The discussion also considered whether networks may tolerate short bursts differently from sustained traffic.

Modern congestion-control systems already probe available capacity and adjust their sending rate.

This suggests a possible future interaction between:

* transport-level congestion control
* path-level scheduling
* relay selection

However, the design should **not** make “trick the ISP into allowing bursts” a protocol goal.

Deliberate excessive bursting can cause:

* queues
* packet loss
* bufferbloat
* unfairness
* congestion collapse

The useful goal is:

> **Exploit naturally available capacity while adapting responsibly to congestion.**

Bursting should be an emergent result of scheduling/transport behavior rather than a traffic-evasion mechanism.

---

# 22. Adaptive Path Scheduling

A naive multipath implementation might do:

```text
A B C D A B C D ...
```

This is undesirable when paths differ substantially.

Example:

```text
Path A: 10 ms RTT
Path B: 30 ms
Path C: 80 ms
Path D: 150 ms
```

Blind round-robin creates packet reordering.

Instead, the scheduler should measure:

* throughput
* RTT
* loss
* jitter
* congestion
* reordering
* stability

and dynamically weight paths.

Example:

```text
Path A: 55%
Path B: 25%
Path C: 15%
Path D: 5%
```

Those weights should be dynamic.

If conditions change, allocation changes.

---

# 23. Endpoint-Owned Multipath State

The preferred architecture is that **the endpoints own the multipath state**.

Relays remain independent forwarding resources.

They do not need to:

* coordinate with other relays
* understand application semantics
* know the overall PathSet
* decrypt traffic
* maintain application state

Conceptually:

```text
                 Mesh endpoint
                      │
                Path scheduler
                /    |    \
               /     |     \
          Relay A Relay B Relay C
```

This preserves the relay's simple role and limits the complexity of infrastructure nodes.

---

# 24. Potential Future PathSet Abstraction

A future extension could define something conceptually similar to:

```text
PathSet
    path_1
    path_2
    path_3
```

An application might request:

```text
min_bandwidth
max_latency
multipath = permitted
max_paths
redundancy = optional
```

The Mesh agent would translate that into actual paths.

The application would not need to understand:

* relay addresses
* WireGuard endpoints
* NAT mappings
* rendezvous servers
* path scheduling
* relay credentials

This reinforces the application-facing abstraction:

> **Connect to service identity, not endpoint address.**

---

# 25. Optional Redundancy and FEC

Multipath can also be used for resilience rather than only throughput.

Future mechanisms could include:

* redundant packet transmission
* forward error correction
* selective duplication
* packet reinjection
* fast failover

However:

> **FEC and redundancy add overhead. They do not create bandwidth from nothing.**

They should therefore remain optional capabilities.

---

# 26. Path Diversity Is More Important Than Raw Relay Count

Ten relays behind the same ISP may not provide ten truly independent paths.

For future path selection, useful diversity could include:

* different ASNs
* different upstream providers
* different geographic locations
* different access networks
* IPv4 vs IPv6
* different congestion domains

Therefore:

```text
10 relays
    ↓
same ISP
same upstream
same region
```

may provide less useful diversity than:

```text
3 relays
    ↓
3 different networks
3 different regions
```

The future scheduler should therefore consider **topological diversity**, not just node count.

---

# 27. Privacy Implications

Relays introduce metadata exposure even when payloads remain encrypted.

A relay can potentially observe:

* endpoint network addresses
* traffic volume
* timing
* session duration
* packet sizes
* connection patterns

It should not normally see:

* application plaintext
* application authorization credentials
* private service contents

Mesh v1 should therefore explicitly distinguish:

> **Confidentiality is not anonymity.**

The protocol does not provide anonymity of participation.

Future optional multi-hop/onion-style transports could provide stronger metadata privacy without changing the underlying identity and authorization model.

That should remain a separate extension rather than a requirement of the base relay.

---

# 28. Resource Controls

Community relays create potential abuse and resource-exhaustion problems.

Important controls include:

* connection limits
* per-session byte limits
* rate limits
* session expiration
* aggregate bandwidth limits
* admission policy
* storage quotas
* bounded state
* anti-amplification
* relay tickets
* expiration

A relay should not need to trust a remote party merely because that party can reach it.

---

# 29. Computational Admission Costs

The discussion considered proof-of-work or other computational costs.

The conclusion was that computational cost should **not** be foundational.

Potential uses include:

* mass rendezvous publication
* mass relay-session establishment
* mass pairing attempts
* other resource-specific abuse

But first-line defenses should remain:

* rate limiting
* quotas
* expiration
* connection limits
* storage limits
* policy

The principle is:

> **Attach computational cost to the scarce resource being protected, not to identity creation itself.**

A universal proof-of-work requirement would add:

* energy consumption
* calibration complexity
* hardware inequity
* unnecessary cost for legitimate users

without necessarily solving the actual attack.

---

# 30. Low-Power Nodes and Community Economics

The architecture naturally supports several participation levels.

Conceptually:

```text
Tiny node
    ↓
occasional / low-bandwidth relay

Home SBC
    ↓
community relay

NAS / router
    ↓
larger relay

x86 / VPS
    ↓
high-capacity relay

Professional infrastructure
    ↓
regional/global relay
```

This creates a possible community infrastructure market.

Operators could compete on:

* bandwidth
* latency
* geographic availability
* uptime
* privacy
* reliability
* price
* network diversity
* service guarantees

A relay provider can be replaced without changing the identity of the service being accessed.

That is important to the larger Mesh economic model:

> **Open the connectivity substrate; commercialize the layers above it.**

---

# 31. Commercial and Ecosystem Implications

The relay discussion fits the broader Mesh economic thesis.

Today, vendors frequently bundle:

* identity
* device enrollment
* discovery
* NAT traversal
* remote access
* relay infrastructure
* VPN-like connectivity
* application access
* cloud accounts

Mesh separates those functions.

Potentially affected categories include:

### Managed mesh VPNs

Most direct overlap.

Their value can shift toward:

* management
* enterprise policy
* SSO
* device posture
* audit
* support
* high-quality relay infrastructure
* administration

rather than owning the fundamental connectivity protocol.

### DDNS

Stable cryptographic service identity reduces dependence on changing public IP addresses.

### Reverse proxies/tunnels

Community relays can provide an open alternative to vendor-specific tunnels.

### Consumer remote-access clouds

NAS/camera/appliance vendors could potentially integrate Mesh rather than requiring proprietary remote-access clouds.

### Personal cloud/VPS

Users could expose services without needing to solve the complete combination of:

* public IP
* DNS
* TLS
* port forwarding
* VPN
* remote access
* identity

independently.

The intended result is not to eliminate commercial services.

It is to make the underlying connectivity interoperable.

---

# 32. Pros of the Community Relay Model

## 32.1 Low barrier to participation

Cheap hardware can contribute.

## 32.2 Distributed capacity

Capacity does not need to come from a few centralized providers.

## 32.3 Geographic diversity

Nodes can exist in many places.

## 32.4 ISP/ASN diversity

Different residential providers can create genuinely different network paths.

## 32.5 Resilience

A failed relay can be replaced.

## 32.6 End-to-end security

Relays do not need application plaintext.

## 32.7 Vendor neutrality

Users can change relay providers without changing service identity.

## 32.8 Better resource utilization

Unused residential capacity could potentially become useful community infrastructure.

## 32.9 Natural path experimentation

The architecture provides a foundation for future multipath research.

## 32.10 Compatibility with existing transports

The relay layer does not require inventing a new Internet transport.

---

# 33. Cons / Risks

## 33.1 Bandwidth may not actually aggregate

If all paths share the same bottleneck, multiple paths do not create additional capacity.

## 33.2 Relay traffic costs operators

Community nodes consume:

* bandwidth
* electricity
* router resources
* hardware lifespan

## 33.3 Abuse

Public relays can be abused for unwanted traffic.

## 33.4 Metadata exposure

Relays can observe traffic patterns even when payloads are encrypted.

## 33.5 Path correlation

Multiple relays do not automatically provide anonymity.

## 33.6 Scheduling complexity

Multipath introduces:

* packet reordering
* congestion-control interaction
* buffering
* path measurement
* failure recovery

## 33.7 Low-power hardware limits

Pi-class nodes have finite:

* bandwidth
* packet-processing capacity
* concurrent-session capacity
* storage
* uptime

## 33.8 Operational complexity

A large community relay network eventually needs:

* policy
* abuse handling
* monitoring
* admission control
* reputation or deployment-specific trust

## 33.9 No guarantee of ISP behavior

The protocol cannot assume that poor residential throughput is caused by per-flow shaping.

## 33.10 Potential dual-use

Open relay infrastructure can be abused.

The base protocol should therefore remain security-neutral while deployment policies address abuse.

---

# 34. What Should NOT Be Assumed

The design should avoid these unsupported assumptions:

### Do not assume:

> Every residential ISP throttles P2P.

### Do not assume:

> Multiple flows always increase throughput.

### Do not assume:

> Multiple relays always provide independent paths.

### Do not assume:

> A Pi can provide a particular guaranteed bandwidth.

### Do not assume:

> Relays are required for NAT traversal.

### Do not assume:

> Multipath defeats an aggregate subscriber bandwidth limit.

### Do not assume:

> Bursting is inherently beneficial.

### Do not assume:

> More relays automatically means more anonymity.

### Do not assume:

> Hardware class predicts network usefulness.

These should be treated as empirical questions or deployment-specific properties.

---

# 35. Recommended Future Benchmark Program

Before standardizing multipath behavior, implement experiments.

## Test A — Single flow

Measure:

```text
A → B
one TCP/QUIC flow
```

Record:

* Mbps
* RTT
* loss
* retransmissions

## Test B — Multiple flows

Measure:

```text
A → B
4 flows
8 flows
16 flows
```

This tests whether the bottleneck behaves differently with multiple flows.

## Test C — One relay

```text
A → Relay → B
```

Compare with direct.

## Test D — Multiple relays

```text
A → Relay A → B
A → Relay B → B
A → Relay C → B
```

Measure aggregate throughput.

## Test E — Diverse relays

Choose relays with:

* different ISPs
* different ASNs
* different geographic locations

Compare against relays sharing an upstream.

## Test F — Adaptive scheduler

Allow the endpoint to dynamically change path weights.

Measure:

* aggregate throughput
* stability
* reordering
* recovery after path failure

## Test G — Direct + relay

Compare:

```text
direct only
```

against:

```text
direct + relay
```

This determines whether the relay adds useful capacity even when direct connectivity exists.

---

# 36. Metrics That Matter

Future experiments should measure more than average throughput.

Useful metrics include:

* aggregate throughput
* per-path throughput
* RTT
* jitter
* packet loss
* packet reordering
* retransmissions
* congestion-window behavior
* path availability
* time to failover
* CPU utilization
* memory utilization
* packets per second
* concurrent sessions
* relay bandwidth utilization
* energy consumption
* storage writes

For community nodes, also measure:

* uptime
* network diversity
* geographic diversity
* ISP/ASN diversity

---

# 37. Architectural Placement

The resulting architecture should remain layered.

```text
Application
    │
    ▼
Mesh Agent
    │
    ├── Identity
    ├── Relationships
    ├── Authorization
    ├── Service Identity
    ├── Reachability
    └── Path Selection
             │
             ├── Direct
             ├── NAT traversal
             ├── Relay
             └── Future multipath
                    │
                    ▼
              Transport
                    │
                    ▼
             Internet / LAN
```

The relay is therefore below authorization but above raw packet routing only insofar as Mesh selects it as a resource.

---

# 38. What Belongs in v0.6.1

The following should remain in the current kernel:

* direct connectivity
* basic reachability
* rendezvous
* basic relay fallback
* RelayTicket
* end-to-end protected transport
* clear relay authority boundary
* relay resource limits
* failure semantics

The relay should remain simple.

No marketplace or sophisticated distributed path scheduler is necessary for the kernel.

---

# 39. What Should Be Deferred

The following should remain future extensions:

* relay capability advertisements
* dynamic capacity exchange
* path measurement protocol
* multi-relay PathSet
* adaptive path scheduling
* multipath striping
* redundant transmission
* FEC
* ASN-aware path diversity
* geography-aware path diversity
* sophisticated relay selection
* relay reputation
* relay economics
* privacy-preserving multi-hop
* onion routing
* large-scale community resource markets

These features should be built on the existing identity/reachability/transport architecture rather than changing the kernel's meaning of identity or authority.

---

# 40. Recommended Future Feature Name

The original concept was informally called:

> Multipath Relay Striping

A more general future abstraction may be:

> **Adaptive Path Aggregation**

This emphasizes that the objective is not simply striping packets.

It includes:

* path selection
* path diversity
* dynamic weighting
* aggregation
* failover
* resilience
* potentially redundancy

A future Mesh endpoint could conceptually expose:

```text
PathSet
    direct
    relay A
    relay B
    relay C
```

and choose among them dynamically.

---

# 41. Relationship to NAT Traversal

The architectural conclusion is especially important:

> **Mesh should not compete with NAT traversal. It should consume it.**

If future Internet infrastructure makes direct connectivity dramatically easier, Mesh becomes better automatically.

If direct connectivity fails, Mesh falls back to relay resources.

If direct connectivity works but is slow, Mesh may eventually choose an alternative path.

Therefore:

```text
Networking technology improves
          ↓
More direct paths succeed
          ↓
Mesh uses fewer relays
          ↓
Relay remains fallback/resource option
```

This avoids making relay infrastructure a permanent architectural dependency.

---

# 42. Relationship to Bandwidth Shaping

The protocol should never define its objective as:

> “Defeat ISP throttling.”

That would be too specific and difficult to substantiate.

The technically defensible objective is:

> **Provide path diversity and adaptive connectivity so that endpoints can make better use of independently available network capacity and improve resilience when a particular path is constrained.**

If the cause happens to be:

* per-flow fairness
* traffic shaping
* peering
* routing
* congestion
* transport behavior

the mechanism can still work without knowing the cause.

---

# 43. The Most Important Open Research Question

The central empirical question is:

> **Can independently operated Mesh relay paths provide materially higher residential-to-residential throughput than a direct path when neither endpoint's aggregate access link is itself saturated?**

If the answer is consistently yes, then the relay network has a second major function beyond NAT fallback:

> **distributed path diversity and capacity aggregation.**

If the answer is generally no, relays remain valuable primarily for:

* reachability
* NAT/firewall traversal
* failover
* availability

Both outcomes are useful.

The experiment determines how important the future multipath feature should become.

---

# 44. Overall Architectural Judgment

The conversation ultimately moved through three different interpretations of the relay concept.

### Initial interpretation

> Relays are needed because NAT makes direct connectivity difficult.

### Refined interpretation

> Relays are fallback infrastructure when direct connectivity fails or is undesirable.

### Broader interpretation

> Relays are potentially distributed connectivity resources that can provide alternative paths, resilience, network diversity, and—under the right conditions—aggregate capacity.

The third interpretation is the most interesting, but it should remain a **future extension rather than an assumption baked into the v0.6.1 kernel**.

---

# 45. Final Design Position

The current recommended position is:

1. **Direct connectivity is preferred.**
2. **Mesh must remain transport-neutral.**
3. **Relays are fallback and path resources, not authorities.**
4. **Relays should preferably forward end-to-end encrypted traffic without terminating application encryption.**
5. **Low-power nodes such as Raspberry Pis can meaningfully contribute forwarding capacity.**
6. **The protocol should advertise capabilities rather than hardware classes.**
7. **Transient relay utilization should not require persistent storage.**
8. **Relay capacity should be treated as a replaceable community resource.**
9. **Network resilience should come from many interchangeable resources rather than a mandatory central relay.**
10. **Multiple paths can potentially improve throughput when their bottlenecks are sufficiently independent.**
11. **Multipath cannot overcome an aggregate access-link bottleneck.**
12. **Torrent behavior provides a useful analogy but is not proof that Mesh multipath will work.**
13. **MPTCP, MLVPN, OpenMPTCProuter, multipath QUIC, and related systems should be studied rather than reinvented.**
14. **Adaptive scheduling is preferable to naive round-robin striping.**
15. **Burst tolerance should be treated as a transport phenomenon, not an ISP-evasion objective.**
16. **The protocol should not claim that residential ISPs universally throttle P2P.**
17. **The usefulness of path aggregation should be established experimentally.**
18. **Privacy and anonymity remain distinct; relays do not automatically provide anonymity.**
19. **Multipath, FEC, sophisticated path selection, and community resource markets belong in future extensions.**
20. **v0.6.1 should keep the relay mechanism simple and stable.**

The resulting conceptual model is:

```text
                 ┌───────────────────────────┐
                 │       Mesh Agent          │
                 │                           │
Application ────►│ Identity / Authorization  │
                 │ Service / Reachability   │
                 │ Path Selection            │
                 └─────────────┬─────────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
             Direct         Relay A        Relay B
                │              │              │
                └──────────────┼──────────────┘
                               │
                         Service Endpoint
```

The deeper architectural idea is:

> **Connectivity becomes a composable resource rather than a property owned by a particular vendor, VPN provider, router, or cloud service.**

A Raspberry Pi does not have to be powerful to participate in that system.

It only needs to contribute **something useful**—a little bandwidth, a reachable location, a different ISP, a different ASN, another available path, or another point of resilience.

At scale, many small contributions can become meaningful infrastructure.

That is the strongest case for retaining a relay layer while keeping it deliberately outside the core trust model.
