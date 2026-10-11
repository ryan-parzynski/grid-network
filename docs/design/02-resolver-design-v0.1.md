260921-NotDNS Resolver

# Executive Summary: Mesh Coordinator Project

## What We're Building

We're creating a lightweight, distributed DNS system for peer-to-peer connections. The basic idea is simple: devices publish their IP and port to a network of volunteer-run coordinators. Someone wanting to connect scans a QR code and gets directed to that device. It handles the fact that home internet IPs change, phones move between WiFi and cellular, and servers get reassigned new IPs. The encryption happens via WireGuard—that's already solved. This is just about keeping track of where things are.

Think of it like a phonebook that knows that Alice's home server moved from one IP to another, and it tells people trying to reach Alice's Immich server the new address automatically. But it's distributed across volunteers running their own coordinators, so there's no central authority and no single point of failure.

---

## The Two-Blob Insight

Early on we realized we were mixing two completely different things: what a *device* is, and where a *device is right now*. That led to a lot of unnecessary complexity. So we separated them into two distinct blobs.

The first blob is the device identity. It says "This is Alice's home Immich server. It's been running for 180 days. It's trustworthy." This blob lives for a year. It doesn't change when the IP changes. It carries reputation.

The second blob is the endpoint. It says "Right now, that Immich server is at IP 203.0.113.50, port 8096." This blob changes whenever the IP changes. It expires relatively quickly—maybe 7 days, maybe 182 days depending on how stable the device is. It's the current address, not the device's identity.

This separation solves a bunch of problems at once. A phone that only connects once a month doesn't need to be in the database constantly. Its endpoint blob expires, but its identity blob remembers it exists, so when it comes back online it doesn't need to rescan the QR code. An Immich server behind CGNAT that gets a new IP address every few days just publishes a new endpoint blob with a higher version number. The old one gets overwritten. No accumulation of stale data. The identity stays the same, reputation stays intact.

---

## Heartbeats: How Reputation Actually Works

Here's the part we got right: we don't want devices to declare a fixed TTL. That doesn't make sense. A home server knows it's going to be online for months. A phone knows it's intermittent. They should get different TTLs based on their actual behavior.

So instead of a device saying "I'm stable, give me a 90-day TTL," the device periodically sends a heartbeat. It's just a signature proving the device key is still alive. The coordinator verifies it. If it's valid, the coordinator extends the TTL by another week and increments a counter: "This device has successfully heartbeated 10 times."

Over time, the device builds a reputation. After one successful heartbeat, it can request a 14-day TTL. After eight heartbeats spread over two months, it can request a 56-day TTL. After six months of consistent heartbeats, it can request a 182-day TTL. Then it only needs to republish every six months instead of every week.

The key part is that this reputation is *proven*, not claimed. You can't fake liveness without the private key. And the reputation decays if the device stops sending heartbeats. Stop sending signals for a month, and you're back to seven-day TTLs.

For intermittent devices like phones, they just request a one-day TTL and stick with it. Doesn't cost anything. When they come back after being offline for a month, their identity blob still exists—it never expired—so they don't need to rescan the QR code. They just publish a new endpoint blob and go. The identity remembers they existed before.

---

## Handling the CGNAT Problem

One of the real-world issues we knew we had to solve: what happens when your IP changes unpredictably? CGNAT is getting more common, especially for residential connections. Your ISP might reassign your address daily or weekly.

The device monitors for IP changes. When it detects one (via network interface changes or STUN queries), it publishes a new endpoint blob with an incremented version number. So version 1 is the old IP, version 2 is the new IP. The old version just gets replaced in the coordinator's database. It doesn't accumulate. There's no bloat.

The heartbeat mechanism keeps working seamlessly. The device continues sending heartbeat signatures on the new endpoint, so it keeps building reputation even as the IP changes. From a user's perspective, their phone just works. They don't have to do anything. The coordinator notices the new version and tells their devices to use it next time they check.

---

## XOR Obfuscation: A Practical Middle Ground

We debated whether endpoints should be encrypted or public. Full encryption seemed like overkill. It doubles the storage per device, adds encryption overhead, and requires managing shared keys. On the other hand, having all IPs and ports sitting in plaintext on a coordinator database makes the coordinator an attractive target.

We landed on XOR obfuscation. When a device publishes its endpoint, it encodes the IP and port using a random 32-bit key. That key gets included in the QR code that Alice shares with Bob. The coordinator stores the obfuscated values—which look like random numbers. If someone steals the coordinator database, they get useless obfuscated IPs. If someone tries to scan the network for services, they don't have a readable IP list to enumerate.

It's not encryption—it's obfuscation. It prevents casual attacks and makes the coordinator less of an attractive target. If privacy becomes critical later, you can upgrade to real AES encryption with zero changes to the structure. The client would just detect which encoding was used and decode accordingly.

The beauty of it is that it costs nothing. XOR is a single operation. It takes microseconds. Storage is actually smaller than storing IP addresses as strings.

---

## Gossip Replication: Simple and Resilient

Coordinators talk to each other, but not in any fancy way. Every five minutes, each coordinator sends a message to a few random peers: "Here are my ten newest blobs." The peers receive them, verify the signatures to make sure they're authentic, check if they're newer than what they already have, and store them if they are.

Data spreads organically. After thirty minutes, most coordinators have the data. After an hour, all of them do (unless one is permanently down). If a coordinator goes offline, the others continue working. When it comes back up, it catches up by receiving gossip from its neighbors. No central sync, no coordination.

It's the same approach BitTorrent uses. It's proven to work at massive scale.

---

## Real Lifecycle: From Setup to Months Later

Let's walk through what actually happens.

Alice sets up her Immich server and generates a QR code. She shares it with Bob. Bob scans it and his phone knows: "This is Alice's Immich, the coordinator is at middle-eu.mesh.local, and I need to use this transform key to decode the IP when I fetch it."

Bob's phone queries the coordinator, gets back an obfuscated endpoint, decodes it, verifies the signature, and establishes a WireGuard tunnel. He syncs photos.

Meanwhile, Alice's Immich server sends a heartbeat signature to the coordinator every few days. The coordinator extends the TTL and increments a counter. After the first heartbeat, it can request a 14-day TTL. After two weeks of consistent signals, it can request 21 days. After two months, it can request 60 days.

One day Alice's ISP reassigns her IP. Her Immich server detects it (the network interface changed), publishes a new endpoint blob with the new IP and version 2. The old version gets overwritten. Gossip spreads this to other coordinators. Bob's phone pulls the new endpoint next time it checks. Everything just works.

A month later Bob hasn't used Immich. He opens the app. His phone still has the QR code. It queries the coordinator for Alice's endpoint. Gets the current version. Connects. No re-scan needed.

Two weeks after that, Alice's connection drops for three days (power outage). Her endpoint blob expires because she hasn't sent a heartbeat. But her identity blob is still there—it lives for a year. When the server comes back up, it publishes a fresh endpoint blob with a new IP (ISP reassigned it while she was down) and version 3. The heartbeats resume. Reputation doesn't reset because the identity blob kept the history.

---

## What We Decided Against (And Why)

We talked about a lot of complicated features. Almost all of them got rejected.

Revocation systems with recovery keys and multi-signature authority—that's good when you're running DNS at global scale and need to be extremely careful about who can change the root keys. For Phase 1, we don't need it. TTL expiry handles device cleanup automatically. If something's compromised, a kill switch (one optional field) lets you delete that specific version. The device republishes a new version. Done.

Full encryption with shared group keys—we ran the math. A million devices, each storing an extra half-kilobyte of encrypted data, just so the coordinator doesn't know which services exist. Meanwhile, XOR obfuscation costs zero extra storage and prevents the same casual enumeration attack. We chose simplicity.

DHT-based discovery—volunteers should be able to just point the QR code at a coordinator URL. They don't need a distributed hash table to find each other. If we get to a million devices and maintaining a coordinator list becomes impossible, we can add DHT. Not now.

Rate limiting, proof-of-work, abuse prevention—we decided to measure first. If spam actually becomes a problem, we'll add per-IP rate limits. We're not going to build complicated anti-abuse systems for attacks that haven't appeared yet.

Relay infrastructure in Phase 1—nice to have. But if someone's on CGNAT and can't reach a server directly, they just use the cached endpoint from last time it worked, or they wait. Phase 4 can add proper relay support if users ask for it.

---

## How It Actually Gets Deployed

The coordinator is simple. It's basically a REST API in front of SQLite (or RocksDB for scale). Two tables: one for identities, one for endpoints. A cleanup process runs every five minutes and deletes anything that's past its TTL. That's it.

A volunteer in Germany runs an instance. A homelabber in Australia runs another. They gossip with each other. Whenever someone publishes to the German coordinator, it spreads to Australia within an hour. If Australia goes down, the German one continues serving. Users in both regions just point their QR codes at the coordinator nearest them.

---

## The Two Database Tables

Device identities table holds: the device ID, its public keys, when it was created, its current reputation score, how many heartbeats it's sent, when the last one arrived, and when it expires (a year from last refresh).

Device endpoints table holds: the device ID, the obfuscated IP and port, the WireGuard public key, what version this is, when it was published, when it expires, and when the last heartbeat arrived.

That's ~1 KB per device total. Ten thousand devices is 10 MB. A hundred thousand devices is 100 MB. A million is a gigabyte per coordinator. Scales cleanly.

---

## What Each Layer Actually Does

The device (the Immich server, the phone app, whatever) generates an Ed25519 key pair once and stores it. Every few days it publishes its current IP and WireGuard key to a coordinator, signed with that key. If it's a stable device, it also sends heartbeat signatures to keep the TTL extended.

The coordinator stores what the device sends. It verifies signatures. When someone queries for a device, it returns what it has. It expires old blobs when their TTL hits. It gossips with other coordinators to spread new data. It tracks reputation (consecutive heartbeats, max allowed TTL) so stable devices earn longer lifetimes.

The client (the phone or app wanting to connect) scans a QR code to learn which coordinator to ask. It queries the coordinator for the endpoint. It decodes the obfuscated IP using the key from the QR code. It verifies the signature to make sure the endpoint is legit. It establishes a WireGuard tunnel. Done.

The coordinator doesn't know private keys. Doesn't authenticate users. Doesn't decide who can talk to whom. Doesn't route traffic. It's deliberately dumb. It just stores and returns obfuscated endpoint information.

---

## What Success Looks Like

Phase 1 is done when: a device can publish an endpoint, a client can scan a QR code and connect, and it still works when the IP changes. Two volunteers can run their own coordinators and data replicates between them. A phone can go offline for a month, come back, and connect without rescanning. A device can prove liveness with heartbeats and gradually earn longer TTLs.

If spam becomes a problem, we add a simple per-IP rate limit. If someone's behind CGNAT and can't do direct P2P, they use a fallback relay. If privacy becomes critical, we upgrade from XOR to AES. But Phase 1 proves the core idea works without any of those.

---

## Why This Survives Growing

The design doesn't have a central bottleneck. Add more coordinators, the load spreads via gossip. Each node gossips with a handful of neighbors, not everyone. Storage per device is tiny and expires naturally. Reputation is proven via heartbeats, not claimed. There's no voting, no consensus, no coordination overhead. Any node can fail and the others keep serving.

We're not trying to replace DNS. We're not trying to be a VPN. We're not trying to solve authentication. We're solving one problem: helping devices find each other when they're behind dynamic IPs, and keeping that working as the network grows.