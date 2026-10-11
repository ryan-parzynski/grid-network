# Yes. This changes the design priority. Let me explain why, and what to do about it.

You've identified something the design was treating as a V2 concern that is actually a V1 concern, because **the short-lived record windows make the discovery problem sharper, not softer**. I want to walk through why, because I think it's a real shift in how you should think about the design.

## Why the short windows make this a V1 problem

The design has short reachability record TTLs. A record is valid for an hour, then it expires. This is good for security — a stale record doesn't linger. But it creates a real problem for discovery:

If a peer publishes a new record every hour, and there are three rendezvous servers in its manifest, then every hour the peer must publish to all three. If one of those servers is down, the peer has to detect that and publish to a replacement. If the peer doesn't notice for a few hours, other peers asking for the peer's record on the down server get nothing (or a stale record), and have to try another server.

Now scale this up. If the network has thousands of peers, each publishing every hour, then each rendezvous server is receiving thousands of publications per hour. If a rendezvous server goes down, thousands of peers lose one of their publication targets simultaneously. They must all detect the failure, find a replacement, and republish. This is a **thundering herd** problem: hundreds or thousands of peers all trying to react to the same event at the same time.

The short TTL doesn't create the problem — the problem exists with any TTL — but it makes it worse. A short TTL means more frequent publications, more frequent opportunities for a server to be down, and more frequent need for peers to find a replacement.

**The V1 answer — "peers publish to a small set of servers, and if one is down, they try another" — works for small deployments.** For a family or small community, it's fine. For a network of hundreds of peers publishing every hour, it becomes a coordination problem that V1 doesn't solve.

So yes, this is a V1 concern if you care about adoption beyond the very small scale.

## Why the design was treating it as V2

The design treated this as V2 because:

1. The early adoption phase is small. A handful of peers, a handful of rendezvous servers. No thundering herd.
2. Decentralized discovery mechanisms (DHT, gossip) are complex, and V1 was trying to be simple.
3. The design's position was "solve V1's problem first, add DHT when V1 is deployed."

This was a reasonable call for a *first deployment*. It is not a reasonable call if the design's actual goal is "an open protocol that any community can use at any scale." The design needs to acknowledge this and choose: either accept the small-scale limitation explicitly, or design for federation/gossip from the start.

## The key property you identified: the data is tiny

You said "since the actual data transferred and stored is so small, it can be reasonably robust." This is correct, and it's the observation that makes the problem tractable.

A reachability record is a few hundred bytes. A rendezvous server's total state for 10,000 peers is a few megabytes. The entire network's reachability state, at any moment, is trivially small.

This matters because **you can afford to be generous with replication**. You can afford to publish to more servers, or to gossip more aggressively, or to cache more, because the cost of doing so is negligible.

Compare this to, say, IPFS, where content discovery must handle terabytes of data. Or Bitcoin, where the ledger is hundreds of gigabytes. The Grid Network's discovery problem is much smaller than either of those, which means the design has more freedom in how to solve it.

## What the design should actually do

There are three mechanisms to consider, and I'd argue for adding all three to the roadmap in a specific order:

### Mechanism 1 — Federation (V2)

Rendezvous servers replicate their records to a small set of peer servers. When Peer A publishes to Rendezvous 1, Rendezvous 1 immediately replicates to Rendezvous 2 and 3. When Peer B asks Rendezvous 1, it gets the record. If Rendezvous 1 is down, Peer B asks Rendezvous 2, which already has the record because it was replicated.

**Cost:** Each rendezvous server needs to maintain a list of peers to replicate to. The replication is a continuous background process. If Peer A publishes to 100 servers, that's 100 servers each replicating to each other, which is 10,000 replication events per publication. Too many.

**Solution:** Peers don't publish to 100 servers. They publish to 2-3 servers, and those servers federate with each other. So Peer A publishes to Rendezvous 1, 2, 3. Rendezvous 1 federates with Rendezvous 4, 5, 6. When Peer B asks Rendezvous 4, it doesn't have the record yet, but it knows to ask Rendezvous 1 or 2 or 3, and gets the record within a few hundred milliseconds.

**This is what Matrix does with homeserver federation.** It's the smallest change to the design that solves the "rendezvous server disappeared" problem, because the record survives on other servers that have replicated it.

### Mechanism 2 — Gossip (V3)

Rendezvous servers gossip with each other periodically. Each server sends "here are the newest records I have" to a random subset of other servers, and receives their newest records in return. Over time, every server converges on the same set of current records.

**Cost:** Gossip is O(N log N) traffic per round, where N is the number of servers. For a small network (tens of servers), this is trivial. For a large network (thousands of servers), it's significant. But the data being gossiped is tiny, so even thousands of servers gossiping is manageable.

**Benefit:** More robust than federation. If a peer publishes to one server and that server goes down before federating, the record is lost. With gossip, the record propagates to many servers quickly, and the loss of any one server doesn't lose the record.

**This is what BitTorrent does with trackerless torrents.** The DHT is a specific form of gossip that's optimized for lookup, but the underlying idea is the same: continuous propagation of small state across many nodes.

### Mechanism 3 — DHT (V5)

A distributed hash table stores reachability records at specific nodes determined by hashing the peer ID. A lookup for peer A's record routes through the DHT to the node responsible for peer A's hash.

**Cost:** Every peer must either participate in DHT routing (expensive) or use a client that does. Lookups take seconds, not milliseconds. The DHT introduces its own trust assumptions (the peers storing your record may be adversarial).

**Benefit:** Fully decentralized. No rendezvous servers at all. The network is the discovery mechanism.

**This is what IPFS uses.** It's the most scalable and most decentralized solution, but also the most complex and slowest.

## The order matters

The three mechanisms aren't alternatives — they're layers. A design that has all three is more robust than one with just one.

**Federation is the natural first step.** It's a small change (rendezvous servers replicate to each other) that solves the "one server is down" case without introducing DHT complexity. It also preserves the current model (peers publish to a small set of servers), which is what implementations of V1 already do.

**Gossip is the natural second step.** It's a bit more complex (servers exchange state continuously), but it solves the "peer published to one server that just went down" case that federation doesn't.

**DHT is the natural third step.** It's the most complex, and it's only needed at scale. If federation and gossip get you to hundreds of thousands of peers, DHT is for millions.

The design should describe this layering explicitly. V1 has no federation. V2 adds federation. V3 adds gossip. V5 adds DHT. Each version is a strictly more robust discovery layer built on the same object model.

## What this changes about the design

I want to be concrete about what changes:

**The rendezvous server's role expands.** In V1, a rendezvous server is a simple store. In V2, it's a store plus a federation peer. In V3, it's also a gossip participant. The interface (accept publications, serve queries) doesn't change, but the internal behavior does.

**The rendezvous manifest needs a section for "replication peers."** A rendezvous server declares which other servers it federates with. This is server configuration, not peer configuration, but it needs to be part of the protocol so that peers can understand what to expect.

**The reachability record needs a "published at" field.** Not to expire records sooner, but so that gossip knows which records are new. Without a timestamp, gossip can't tell whether a record has already been seen.

**The lookup process needs to handle multiple hops.** A peer asks Rendezvous 1, which doesn't have the record but federates with Rendezvous 2, which does. The response comes back through Rendezvous 1. This is a new kind of interaction — a discovery query that hops through multiple servers.

**Peer identity must remain the anchor.** None of these mechanisms change the fact that records are signed by the peer's device key. Whether the record comes from Rendezvous 1, Rendezvous 2, or a DHT lookup, the peer validates the signature. This is what keeps the design from needing to trust any of these mechanisms.

## What this means for V1's design

Should you add federation to V1? I don't think so, and here's why:

1. **Federation adds complexity that V1 doesn't need at small scale.** A family with two rendezvous servers doesn't need federation. Neither does a small community with one server.

2. **Federation is best designed after V1 is deployed.** The details of how servers find each other, how they replicate, and how they handle stale records are best informed by real usage. Designing them now means designing for hypothetical problems.

3. **The design can be changed later without a breaking change.** Adding federation to V2 doesn't require changing the reachability record format or the peer-to-server protocol. It only adds a new behavior to the server side. V1 peers and V2 servers can interoperate.

What you should do instead is:

1. **Add a "Limitations of V1 Rendezvous" section** to the archive, as I said before, but now with the specific note that "federation is not in V1, and this means a peer's records are lost if all rendezvous servers they publish to go down."

2. **Add a "Discovery Roadmap" section** that describes the three mechanisms (federation, gossip, DHT) and their order. Make clear that the object model supports all three without change.

3. **Add a "Federation-ready" design note** that lists the small changes V1 needs to make now to keep the door open for V2's federation. These are things like: the "published at" field on records, the ability to include multiple endpoints in a record, the ability for a server to indicate "I don't have this record, ask X." None of these require V1 to *implement* federation; they just prevent V1 from making decisions that would make federation impossible.

4. **Consider making reachability records larger.** A few hundred bytes is fine, but if you're going to federate later, having room for more endpoints (multiple relays, multiple direct addresses, priority hints) is useful. Designing the record with headroom means not having to change the record format when federation arrives.

## What I'd tell your skeptical reader

If someone asks "what happens when the rendezvous server goes away?", the answer becomes:

> V1 relies on rendezvous servers being available. If all of a peer's rendezvous servers go offline, that peer becomes unreachable until it republishes to a reachable server or until out-of-band contact re-establishes the connection.
>
> This is a known limitation of V1 and it's intentional. V2 adds federation between rendezvous servers, which means a record survives even if the server it was published to goes down. V3 adds gossip, which means a record propagates through the network continuously. V5 adds DHT, which means no rendezvous servers are needed at all.
>
> The object model is designed to support all three without change. The record format, the signature scheme, the identity model, and the authorization model are all unaffected. Only the discovery layer needs to be extended.
>
> V1's choice to defer this is a deliberate tradeoff: it keeps V1 small and implementable, and it defers the complexity of federation until there's a network large enough to need it.

That's a stronger answer than "we don't have a solution yet." It's "we have a roadmap, the roadmap is straightforward, and the design was written to accommodate it."

## The bottom line

You identified a real gap. The design treated rendezvous reliability as a V2 concern, but the short record windows and the potential for scale make it a V1 concern for any deployment beyond the very small.

The design doesn't need to *solve* this in V1. It needs to:

1. Acknowledge the limitation explicitly.
2. Document the roadmap for solving it.
3. Ensure that V1's decisions don't foreclose the solutions.

None of those are hard. All three should be in the published design. And you're right that the tiny size of the data is the property that makes the eventual solutions tractable — it's the reason federation and gossip are viable for Grid Network when they might not be for a system with larger state.

I'd add a "Discovery Roadmap and V1 Limitations" section to the archive before publishing. It's the honest answer to a question that will be asked, and it also makes clear that the design's author understood the problem and chose the sequencing deliberately.