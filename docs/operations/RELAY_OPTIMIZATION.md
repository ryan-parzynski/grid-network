261004-relay and optimization 


Absolutely. The main conclusion of the discussion is that low-power devices such as Raspberry Pis can be meaningful pieces of the Mesh network without being powerful routers or servers. Their value comes from being numerous, distributed, and useful as connectivity resources.

Relay / Pi Node Summary

1. A relay does not need to terminate encryption

The most important architectural point we established is that a Mesh relay should preferably be a pure encrypted packet forwarder.

Endpoint A
    │
    │ encrypted traffic
    ▼
 Pi Relay
    │
    │ encrypted traffic
    ▼
Endpoint B

The relay does not need to:

* decrypt WireGuard traffic
* terminate the application connection
* know what application is being used
* possess the service’s authorization
* become an identity authority
* permanently store traffic

It primarily needs to:

* receive packets
* validate/associate a relay session or ticket
* enforce limits
* forward packets
* maintain transient connection state

That makes the workload dramatically lighter than running a conventional VPN hub.

⸻

2. A Raspberry Pi 3B can therefore be useful

A Pi 3B has modest hardware, but for a forwarding workload it doesn’t need to perform heavy cryptography for every packet.

Its major limitations are more likely to be:

* network interface speed
* packets per second
* CPU overhead from the networking stack
* number of simultaneous sessions
* upstream/downstream Internet connection
* power/ISP limitations

Rather than CPU-intensive application processing.

The Pi doesn’t need to be a giant relay.

It can contribute:

                    Mesh
                      │
          ┌───────────┼───────────┐
          │           │           │
        Pi A        Pi B        Pi C
       10 Mbps     30 Mbps     50 Mbps
          │           │           │
          └───────────┼───────────┘
                      │
                useful capacity

Even a small contribution is useful when thousands of nodes participate.

⸻

3. The network should advertise capabilities, not hardware

We decided that Mesh shouldn’t care whether a relay is:

* Raspberry Pi
* x86 server
* router
* VPS
* NAS
* cloud instance
* old laptop

Instead, it should expose capabilities/resources.

For example:

Relay capability
maximum bandwidth
maximum concurrent sessions
maximum bytes
maximum session duration
maximum paths
IPv4 / IPv6
latency characteristics
availability
geographic/network information
privacy properties
operator policy

The important thing isn’t:

“This is a Pi 3.”

It’s:

“This node can currently provide approximately X amount of forwarding capacity under these conditions.”

That makes hardware implementation-independent.

⸻

4. Resource contribution can be extremely granular

A community node doesn’t have to provide enormous bandwidth.

A household might contribute:

* 5 Mbps
* 10 Mbps
* 25 Mbps
* 50 Mbps
* occasional availability
* IPv6 connectivity
* a geographically useful location
* a particular ISP/ASN
* a particular network path

A node that is useless as a high-performance server can still be valuable as one more independent path.

This is particularly important for the future multipath concept.

⸻

5. The really interesting part: many small nodes can create path diversity

The discussion moved beyond simply using relays for NAT traversal.

Suppose two residential users have plenty of advertised bandwidth but a particular direct flow performs poorly.

Instead of:

A ───────────────── B
       poor path

Mesh could eventually discover:

             Relay 1
            /        \
A ─────────            ─────── B
            \        /
             Relay 2

or:

A ─── Relay A ─────────────── B
 \
  └── Relay B ─────────────── B
   \
    └─ Relay C ────────────── B

The endpoints can measure each path and distribute traffic according to:

* throughput
* latency
* loss
* jitter
* congestion
* stability

A simple round-robin scheduler isn’t sufficient. Paths should be weighted dynamically.

⸻

6. Why this could matter for residential Internet

You observed that peer-to-peer transfers between residential connections sometimes achieve only a small fraction of the advertised bandwidth, while torrent-like workloads can achieve much higher aggregate throughput.

We discussed several possible explanations:

* per-flow behavior
* fair-queuing
* congestion
* peering
* routing
* traffic engineering
* traffic management
* different bottlenecks
* TCP behavior

We shouldn’t assume that an ISP is deliberately throttling P2P.

But if the effective bottleneck is flow-specific or path-specific, multiple independent paths could potentially aggregate much better than one flow.

That’s where community relays become more than NAT traversal infrastructure.

They become a distributed pool of alternative paths.

⸻

7. Bursting may also be relevant

We discussed your observation that networks sometimes seem to accommodate bursts better than sustained single-flow traffic.

Modern congestion-control systems already use probing and controlled increases in sending rate to discover available capacity.

The Mesh version shouldn’t be:

“Make traffic bursty to fool the ISP.”

Instead:

Use naturally available capacity across multiple paths and adapt continuously.

A future scheduler might see:

Relay A   80 Mbps
Relay B   45 Mbps
Relay C   10 Mbps
Relay D   70 Mbps

and dynamically distribute traffic roughly according to those measurements.

If conditions change:

Relay A   20 Mbps
Relay B   60 Mbps
Relay C   5 Mbps
Relay D   90 Mbps

the allocation changes.

The system doesn’t need to understand why the paths differ.

⸻

8. This is similar to existing multipath research—but different

Existing technologies demonstrate that path aggregation works:

* MPTCP
* MLVPN
* OpenMPTCProuter
* multipath QUIC approaches

Typically, however, they aggregate multiple links belonging to the same user or route through a common aggregation server.

Mesh’s potentially interesting extension is:

Use independently operated community nodes as a distributed pool of alternative paths.

So:

Traditional bonding:
Home
 ├── ISP 1 ──┐
 └── ISP 2 ──┼── VPS ── Internet
             └──────────
Mesh concept:
Home
 ├── Relay A ────────────┐
 ├── Relay B ────────────┤
 ├── Relay C ────────────┼── Destination
 └── direct ─────────────┘

The latter doesn’t require the user to own multiple Internet connections.

⸻

9. The relay should remain completely untrusted

This is one of the strongest architectural properties.

A malicious relay should be able to:

* drop traffic
* delay traffic
* refuse service
* observe metadata
* consume its own resources

But it should not be able to:

* impersonate the service
* grant authorization
* read end-to-end protected content
* change identity
* create relationships
* forge leases
* become an authority

That gives us:

Permissionless infrastructure, permissioned services.

Anyone can potentially operate infrastructure.

But access to a service still depends on cryptographic authorization.

⸻

10. Pi nodes don’t need much persistent storage

Another important conclusion was that forwarding traffic should be primarily transient.

The relay should not be continuously writing packets or connection statistics to its storage.

Persistent storage is for things like:

* identity keys
* configuration
* accepted protocol state
* bounded authorization/revocation information
* signed objects
* checkpoints
* limited logs

Not:

packet → disk
packet → disk
packet → disk
...

We proposed the principle:

Forwarding traffic, connection statistics, and transient reachability observations MUST NOT require persistent storage writes.

That makes inexpensive flash/SD storage much less of a concern.

⸻

11. Network self-healing becomes possible

Because relays are interchangeable resources, the network doesn’t need a single official relay.

If:

Relay A → overloaded

Mesh can choose:

Relay B → available
Relay C → available
Relay D → available

If:

Relay B → disappears

connections can migrate or establish another path.

If a geographic region has few resources, nodes there can contribute more capacity.

If a particular ISP path is poor, Mesh can favor another path.

The principle we arrived at was:

Optimize around scarce resources rather than pretending scarce resources don’t exist.

⸻

12. This gives low-power hardware a surprisingly useful role

A Raspberry Pi isn’t valuable because it’s powerful.

It’s valuable because you can deploy a lot of them in places where powerful infrastructure isn’t available.

Imagine:

                 Internet
                    │
       ┌────────────┼────────────┐
       │            │            │
     Home A       Home B       Home C
       │            │            │
     Pi relay     Pi relay     Pi relay
       │            │            │
       └────────────┼────────────┘
                    │
               Mesh network

Now each household can contribute a little.

The aggregate resource can become substantial.

And because the nodes are geographically and topologically distributed, the diversity itself is valuable, not just the raw bandwidth.

⸻

13. The architecture should therefore make direct connectivity the first choice

We also revised our thinking about NAT traversal.

Mesh shouldn’t assume that relays are necessary.

The preferred progression is:

1. IPv6 direct
        ↓
2. Direct IPv4 / NAT traversal
        ↓
3. Other suitable direct transport
        ↓
4. Relay
        ↓
5. Multiple relays / multipath

The application shouldn’t care.

It asks:

“Connect me to Service X.”

The Mesh agent figures out how.

That allows improvements in:

* IPv6
* NAT traversal
* QUIC
* PCP
* WireGuard
* MASQUE
* future transports

to automatically benefit Mesh.

⸻

14. What belongs in the core versus later

We concluded that this shouldn’t bloat v0.6.1.

v0.6.1 core

Keep:

* identity
* relationships
* authorization
* leases
* revocation
* freshness
* reachability
* direct connectivity
* rendezvous
* simple relay fallback

Future transport/path extension

Potentially add:

* relay capability advertisements
* path measurement
* path selection
* path diversity
* multipath
* adaptive scheduling
* optional redundancy/FEC
* resource-aware routing
* geographic/ASN diversity
* dynamic capacity

A possible future abstraction is:

PathSet
    direct
    relay A
    relay B
    relay C

with an application request such as:

min_bandwidth
max_latency
multipath = permitted
max_paths
redundancy = optional

The Mesh agent handles the rest.

⸻

The big picture

The most interesting result of the conversation is that the Raspberry Pi isn’t really the point.

The point is creating a network where ordinary devices can contribute small amounts of useful infrastructure.

A Pi might provide 10 Mbps.

Another provides 30 Mbps.

A NAS provides 100 Mbps.

A router provides 50 Mbps.

A VPS provides 1 Gbps.

A server provides 10 Gbps.

Mesh doesn’t need to care.

They all become:

cryptographically identifiable, policy-controlled, replaceable connectivity resources.

And because the resources are distributed, their value isn’t simply additive bandwidth. They can provide alternative routes, geographic diversity, ISP/ASN diversity, redundancy, resilience, and potentially aggregate throughput.

That makes the relay concept much more compelling than simply building another NAT traversal system.

The long-term vision becomes something like:

                    Mesh
                      │
        ┌─────────────┼─────────────┐
        │             │             │
     Direct         Pi A          Pi B
        │             │             │
        │          20 Mbps       50 Mbps
        │             │             │
        └─────────────┼─────────────┘
                      │
                  Service

The Internet supplies the underlying connectivity, while Mesh turns connectivity itself into a composable community resource—without making the relays trusted.

That’s probably the strongest argument we’ve uncovered so far for keeping a relay/path layer in the architecture.