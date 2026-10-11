

# How small self-hosters and enterprises contribute to the network

The Mesh protocol is designed so that *every* participant contributes what they have and consumes what they need. There's no distinction between "small user" and "big infrastructure provider." A Pi 3 and a datacenter can participate in the same protocol, at very different capacities, without either being privileged or disadvantaged.

This is important because it's the property that makes the network grow organically. You don't need a critical mass of large operators for the protocol to be useful. You need a handful of small participants who each contribute a little.

## The three contribution layers

Not every participant contributes in the same way. There are three distinct layers, and a given machine might participate in one, two, or all three.

### Layer 1 — Reachability publication

Every peer that runs a mesh agent is a **publisher**. It periodically publishes:

- Its current endpoints (IPv4 address, IPv6 address, UDP port).
- Its NAT behavior hints (for hole punching).
- Its relay preferences.

This costs almost nothing. A reachability record is a few hundred bytes. Publishing one every few minutes uses negligible bandwidth, negligible CPU, and no persistent storage beyond the record itself.

**A Pi 3 contributes here automatically.** It has to publish its own reachability to be reachable, and doing so makes it a full participant in the reachability layer. There's no separate "contribute" action — participation is the default.

The collective effect is that every peer in the network is discoverable to every other peer, using only the aggregate storage and bandwidth of the network's own participants. There's no separate "publisher tier" and no party that has to do this on behalf of anyone else.

### Layer 2 — Rendezvous

Some participants choose to run a **rendezvous server**. This is a small service that:

- Accepts reachability publications from peers.
- Serves those publications to other peers on request.
- Stores the records for a bounded duration.
- Does not need to persist anything long-term.

A rendezvous server for a few hundred peers fits comfortably in:

- **CPU:** a Raspberry Pi 3, low-power VPS, or an old laptop.
- **RAM:** tens of megabytes.
- **Storage:** a few hundred megabytes for records, most of which expires within hours.
- **Bandwidth:** proportional to lookup queries, which are small and infrequent.

For a small community — a family, a hobbyist group, a small business — a single rendezvous server on a Pi 3 at home is enough to keep the whole group connected. It doesn't need to be online 100% of the time; peers cache reachability records and use them until they expire.

**A Pi 3 running rendezvous contributes meaningfully to the network.** It provides a fixed, reliable discovery point that peers can rely on. If it goes down, the network degrades gracefully — peers use cached records and try other rendezvous servers if any are configured. When it comes back, it's immediately useful again.

The requirement for a rendezvous server is not power. It's *availability*. A Pi 3 with a stable power supply and a stable internet connection is a perfectly good rendezvous server, even if it's running on someone's desk at home.

### Layer 3 — Relay

Some participants choose to run a **relay**. This is the layer that requires more consideration, because relay is where bandwidth and cost actually matter.

A relay:

- Accepts encrypted traffic from a peer.
- Forwards it to the destination peer.
- Sees only ciphertext — it never sees plaintext.
- Enforces resource limits (bytes, rate, sessions) per the relay ticket.

The relay's cost is proportional to traffic. This is fundamentally different from rendezvous, where the cost is proportional to the number of peers and their lookup frequency — both of which are small.

**A Pi 3 can run a relay, but its capacity is limited.** On a home connection with, say, 20 Mbps upload, a Pi 3 relay can carry a few video streams or many small connections, but it cannot carry much aggregate traffic. For a family or a small group of friends who mostly use it as a fallback when direct connection fails, this is sufficient.

**A VPS relay can carry more.** A $5/month VPS with a gigabit connection can carry substantial traffic. This is a small but real commercial opportunity for hobbyists and small operators — running a relay for a community in exchange for cost recovery.

**An enterprise relay can carry enormous traffic.** A datacenter-grade relay with high bandwidth, low latency, and multiple network paths can be the backbone for an organization. It's what commercial mesh products sell today, and it's a legitimate business.

The point is that **all three of these can coexist in the same network.** A Pi 3 relay and a datacenter relay speak the same protocol. Peers choose which relay to use based on policy — "use my own Pi if it's reachable, fall back to the community relay, escalate to the commercial relay if needed." The protocol doesn't care about capacity; it cares about availability and correctness.

## The contribution model

The important insight is that **contribution is proportionate to capacity**.

| Contributor | What they can contribute |
|-------------|--------------------------|
| Phone, laptop, Pi Zero | Publish own reachability; participate in the network |
| Pi 3, old laptop, home NAS | Rendezvous for a small group; light relay for a family |
| Home server, dedicated VPS | Rendezvous for a community; relay for a group |
| Enterprise server, cloud instance | Large rendezvous; high-capacity relay for an organization |
| Datacenter with anycast | Backbone relay for a whole region |

No one is required to contribute more than they can. A Pi 3 contributes what it can, and the network is better for it. An enterprise server contributes more, and the network is better for that. There's no "minimum contribution" required to participate, and there's no "maximum contribution" that makes someone privileged.

This is fundamentally different from systems like BitTorrent, where contribution is expected to be roughly proportional to consumption. In Mesh, contribution is optional and voluntary. A phone that only publishes its own reachability and never runs a rendezvous or relay is a full participant. A Pi 3 that runs a small rendezvous is contributing more. A datacenter is contributing at a different scale, but contributing in the same direction.

## The interesting emergent property: relay heterogeneity

Here's where it gets interesting. Because relays are untrusted — they forward ciphertext but cannot decrypt, cannot authorize, cannot impersonate — **a relay contributed by an untrusted party is still useful.**

This means:

- A hobbyist in Germany running a Pi 3 relay is useful to peers in Germany.
- A community in Brazil running a shared VPS is useful to peers in Brazil.
- An enterprise running a global relay network is useful to its own employees.
- A commercial operator selling relay capacity is useful to customers who want guaranteed bandwidth.

None of them have to trust each other. A peer that uses a German hobbyist's Pi relay and a Brazilian community VPS is using two independent relays with the same protocol. It doesn't matter that the operators don't know each other, don't trust each other, and have different capabilities. The protocol handles the difference.

This is why **relay providers are replaceable** — a property from the earlier design discussion. A peer can switch from one relay to another without changing identity, authorization, or relationships. The relay is a replaceable resource, not a permanent authority.

## The economic shape

This produces a network with a particular economic shape:

**Bottom of the stack: free.** Reachability publication is free. It's part of participating. Every peer does it.

**Middle of the stack: volunteer.** Rendezvous and light relay are volunteer-contributed. A hobbyist runs a Pi 3 because they want their own network to work; the fact that it also helps their community is a side effect. A community runs a shared VPS because the members want reliable rendezvous. A small business runs a server because they want their employees connected.

**Top of the stack: commercial.** High-bandwidth, low-latency, guaranteed-uptime relay is a service worth paying for. Enterprises pay for it because they need SLA-backed connectivity. Commercial operators sell it because there's demand. The protocol makes the service interchangeable, which means the market is competitive.

The interesting property is that **no layer depends on the layer above it**. A community that never pays for commercial relay still has a functional network. An enterprise that never uses volunteer infrastructure still has a functional network. Both can coexist, and both can use the same protocol, and a peer can move between them without friction.

## What each contributor actually gets

It's worth being specific about what each contributor actually receives, because the framing "contribute to the network" can sound abstract.

### A Pi 3 contributor gets:

- **A working private network** between their own devices, for free.
- **A working private network** between their devices and their friends' devices, for free.
- **Control over who they share with**, without a company in the loop.
- **The ability to switch infrastructure providers** without losing anything.
- **The satisfaction of contributing** to infrastructure that others can use, if they want.

The Pi 3 contributor isn't running rendezvous to "help the network" in an abstract sense. They're running it because it makes their own network more reliable, and the fact that it also helps their friends is a natural consequence.

### An enterprise contributor gets:

- **Portability of device trust** across vendors and clouds.
- **A unified model** for BYOD, IoT, edge, partner, and employee devices.
- **Independence from vendor lock-in**, which is a real strategic advantage.
- **The ability to audit and self-host** the coordination layer if they want.
- **The option to run their own relays** for cost and control.
- **The option to use commercial relays** when they need SLA-backed capacity.

The enterprise isn't contributing out of altruism. They're contributing because the network they contribute to is also the network they use, and the protocol's separations mean that their contributions benefit them directly and safely.

### A commercial relay operator gets:

- **A market for relay capacity** that's independent of identity lock-in.
- **A path to selling reliability, latency, and support** without having to own customers' trust graphs.
- **The ability to interoperate** with self-hosted and enterprise deployments, rather than competing against them.
- **A clear cost model** — bandwidth, sessions, bytes — that maps to pricing.

The commercial operator isn't contributing to a network they don't benefit from. They're participating in a market where their contribution has clear value.

## The key insight

The key insight is that **the protocol doesn't distinguish between small and large contributors.** A Pi 3 and a datacenter both speak the same protocol, both serve the same objects, and both are equally valid participants. The difference is capacity, not legitimacy.

This matters because it means:

- The network can grow from a single Pi 3 in someone's apartment.
- It can grow to a global mesh with commercial infrastructure at the edges.
- It can be used by a family, a community, a company, or an industry.
- It can never be captured by a single operator, because no operator has a privileged role.
- It can never be shut down by a single failure, because every layer has fallbacks.

This is what "democratic" or "permissionless" infrastructure actually means in practice. Not that everyone contributes equally, but that everyone's contribution is *recognized* as legitimate, and no contributor can be excluded by another, and no contributor can leverage their size into permanent control.

The Pi 3 contributor and the enterprise contributor are peers in the protocol. Their relationship to the network is the same. Their relationship to each other is neutral. They participate in the same ecosystem, on terms they each set for themselves, and neither can dictate to the other.

That's the shape of the network.