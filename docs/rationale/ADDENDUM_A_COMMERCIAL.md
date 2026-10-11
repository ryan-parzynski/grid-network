261004-Rationale Addendum A

# RATIONALE.md

**Document:** `RATIONALE.md`
**Version:** 2.0
**Status:** Draft
**Purpose:** Companion to the protocol specification. Explains *why* the design is the way it is, *who* it serves, and *how* participation works across scales — without descending into byte-level specification.

---

## Purpose of this document

`PROTOCOL.md` defines what the protocol is. `OBJECTS.md` defines how it is encoded. This document defines **why** — the reasoning behind the design decisions, the problems being solved, the audiences being served, and the shape of the ecosystem that results.

It is written for:

- Reviewers evaluating whether the design makes sense.
- Implementers deciding whether to build on it.
- Operators deciding whether to contribute infrastructure.
- Applications deciding whether to integrate.
- Skeptics who think the problem is already solved.
- Anyone trying to understand the *intent* behind the technical choices.

It does not contain normative requirements. Where it describes behavior that is normatively specified elsewhere, it does so for explanation, not for authority.

---

## The one-paragraph version

Today, the ability to reach your own devices from anywhere is rented from companies. Tailscale, Cloudflare, ZeroTier, and every commercial mesh product own your identity and your relationships. If they change their terms, you migrate or lose access. Grid Network is a protocol that makes identity and authorization portable. Your devices, your relationships, your authorizations belong to you, not to a vendor. Anyone can operate infrastructure, anyone can switch providers, and no company decides whether your network exists. It's the same model as email — anyone can run a server, anyone can switch providers, nobody needs permission.

---

## Part I — The problem

### 1. The core problem

Every self-hosted service, every personal server, every home automation system, every private application eventually hits the same wall:

> *"How do I reach this from somewhere else?"*

This seems like a small problem. It isn't. It forces every project that encounters it into one of three bad choices.

### 2. The three bad choices

**Choice 1: Expose it to the internet.**

Open a port, forward it on the router, hope nothing scans you. This works until it doesn't — until a firmware vulnerability is discovered, until a service is running with default credentials, until someone's home camera feed is on Shodan. The result is a growing pile of "I accidentally published my home network to the world" incidents.

**Choice 2: Use a proprietary tunnel or mesh VPN.**

Tailscale, Cloudflare Tunnel, ZeroTier, ngrok, and their many competitors. These work well. But they require:

- An account with a company.
- Authentication through Google, GitHub, or a proprietary identity provider.
- Acceptance that the company owns the device graph, the access policies, and the identity of every machine.
- Dependency on the vendor's continued operation, pricing, and business decisions.

The vendor is not the *transport* — it's the *authority*. If the vendor disappears, your network doesn't just lose connectivity; it loses its definition of who is allowed to talk to whom.

**Choice 3: Build it yourself.**

Run your own VPN, manage your own certificates, deal with dynamic DNS, deal with CGNAT, deal with NAT traversal, deal with relay infrastructure, deal with revocation, deal with offline state. This works, but only for someone who is already an expert. Normal people cannot do this.

Every self-hosted project, every commercial product, and every enterprise deployment eventually picks one of these three. All three are bad for different reasons.

### 3. Why this matters more than it sounds

The obvious framing is "this is annoying." The real framing is: **the ability to reach your own devices has become a subscription.**

A decade ago, if you wanted to reach your home server, you opened a port or ran a VPN. Both were awkward, but they were *yours*. Today, the easy path is to sign up for a service. The service works beautifully. But you don't own your network anymore. You're renting the ability to reach your own stuff.

This is the same story as email, and the same story as social media, and the same story as every other layer of the internet where convenience has slowly become dependence. It's not a conspiracy; it's just how products work. But it means the current state of the world has a specific cost that's rarely named: **you don't own your digital relationships.**

### 4. Why the alternatives don't fully solve it

Three common responses to the problem turn out to be incomplete.

**"Just use Tailscale."**

Tailscale is an excellent product. It also is a company. It runs a coordination server that is the source of truth for your device graph. If Tailscale changes its terms, or gets acquired, or shuts down a feature you depend on, or stops being able to operate in your jurisdiction, your network is affected. You can self-host Headscale, but then you're running infrastructure — you've swapped one problem for another.

Tailscale's identity model is account-based. That works for consumers. It's awkward for self-hosting, and it's problematic for applications that want to authorize based on *device identity* rather than *user identity*. And the underlying protocol is proprietary: third parties can't implement it, competitors can't speak it, and you can't switch providers without rebuilding your network.

**"Just use Cloudflare Tunnel."**

Cloudflare Tunnel lets a local machine connect outbound to Cloudflare, so you don't need a public IP. It works well. But it makes Cloudflare part of the access path. If Cloudflare changes its terms, filters the wrong traffic, has an outage, or exits the business, your access path goes with it. The convenience is real; the dependence is real.

**"Just build your own VPN."**

This works. It's also the reason self-hosted connectivity has remained a niche hobby rather than a mainstream capability. Running your own VPN requires expertise that most people don't have, and even for people who do have it, it means reimplementing NAT traversal, relay fallback, revocation, and offline state on your own.

None of these alternatives is wrong. Each is a good choice for some people. But none of them solves the underlying problem: **there is no portable, open, vendor-neutral way to establish and maintain identity and authorization between your devices.**

### 5. The insight

The insight behind Grid Network is that **connectivity is not a feature. It's infrastructure.** It should be a shared, audited, portable primitive that every project can consume — the same way they consume TLS for encryption, HTTP for requests, or DNS for resolution.

The reason this hasn't happened yet is that connectivity has three parts that are hard to standardize:

1. **Identity.** Who is this device?
2. **Authorization.** What is it allowed to do?
3. **Reachability.** Where is it right now?

Each of these is a distinct problem, and the current landscape tends to conflate them. When they are conflated, standardization becomes hard — because different projects want to make different trade-offs. When they are separated, each can be standardized independently.

Grid Network separates them cleanly:

- **Identity** is a cryptographic keypair, controlled by the user.
- **Authorization** is a signed grant, verified locally.
- **Reachability** is an ephemeral hint, replaceable and untrusted.

Once separated, each becomes small enough to specify, and the whole system becomes small enough to be portable.

### 6. Why this is hard

A reasonable skeptic might say: "This sounds like a solved problem. WireGuard exists. NAT traversal techniques exist. Relays exist. What's new?"

The answer is that all of these pieces exist, but none of them *coordinate*. Specifically:

- **Identity must survive location changes.** Today, everything online is identified by where it is: an IP address, a DNS name, an account tied to a specific server. If the location changes, the identity breaks. Grid Network separates the two completely.
- **Authorization must work offline.** If your device is offline for six months, the network shouldn't forget you exist. But it also shouldn't keep granting you access forever. This requires separating long-lived relationships from short-lived authorizations.
- **Intermediaries must be untrusted.** A rendezvous server that helps two peers find each other must not get to decide they're authorized to talk. A relay that forwards their packets must not get to grant access. Enforcing this requires careful design.
- **No single party must be the authority.** There must be no central server whose disappearance ends the network. This rules out the easy solutions.
- **The result must be portable.** Your identity, relationships, and authorizations must survive any change of infrastructure provider.

Each of these constraints rules out a class of easy solutions. What remains is more complex than a naive design. But the complexity is in the protocol, not in the user experience — the user sees a QR code, a name, and a working connection.

---

## Part II — The solution

### 7. What Grid Network is

Grid Network is a **control plane for identity, authorization, and reachability** that sits above whatever networking already exists.

It is not a VPN. It is not a tunnel. It is not a replacement for WireGuard, IPv6, or any transport protocol. It is a layer that answers questions *about* devices and their permissions, using signed objects that participants hold and verify themselves.

The three questions Grid Network answers are:

- **Who is this?** — A cryptographic identity, controlled by the participant.
- **What is it allowed to do?** — A signed authorization, verified locally.
- **Where can I find it?** — An ephemeral reachability record, refreshed as networks change.

Every one of these questions is answered by cryptographically signed objects. No answer requires contacting a central authority. No answer requires a company to be in the loop.

### 8. What Grid Network is not

- **Not a decentralized VPN.** A VPN is a transport. Grid Network is a control plane above transports.
- **Not a DNS replacement.** DNS maps names to addresses. Grid Network maps identities to reachability, and adds authorization on top.
- **Not an anonymity network.** Peers are identified. Metadata is visible to infrastructure operators. This is by design.
- **Not a blockchain.** There is no global consensus, no ledger, no mining, no token.
- **Not a peer-to-peer file system.** Peers connect directly or through relays, but there is no distributed storage.
- **Not a company.** There is no operator, no owner, no central authority.
- **Not a Tor / I2P / Freenet replacement.** Those systems provide anonymity through routing. Grid Network provides authenticated identity with explicit non-anonymity.

These distinctions matter because Grid Network is often compared to systems that occupy adjacent but distinct parts of the design space.

### 9. The key design properties

Five properties distinguish Grid Network from other approaches.

**Property 1 — Identity is portable.**

A device's identity is a cryptographic keypair. It does not depend on any account, any server, any provider, or any vendor. It can be used across multiple rendezvous providers, multiple relays, multiple networks, and multiple applications.

**Property 2 — Authorization is local.**

A device verifies authorization itself, using state it holds locally. It does not ask a server "am I allowed to do this?" It asks itself, using signed objects it already has. This means authorization works offline, works through network partitions, works when the infrastructure is unreachable.

**Property 3 — Reachability is ephemeral.**

Where a device currently is, is not part of its identity. It's a hint, refreshed as networks change. If a device moves, the hint changes; the identity doesn't. If a rendezvous server is unreachable, cached hints still work until they expire.

**Property 4 — Infrastructure is untrusted.**

Rendezvous servers, relays, and any other infrastructure can be operated by anyone, including parties the user does not trust. They help peers find each other and forward encrypted traffic, but they cannot forge identity, cannot grant authorization, cannot decrypt content, cannot alter signed objects without detection.

**Property 5 — The protocol is open.**

There is no proprietary component. Any implementation can speak to any other. Any operator can run infrastructure. Any user can switch providers without losing their identity, their relationships, or their authorizations.

These five properties, taken together, produce a system where **the network can help you reach someone without becoming an authority over who you are or what you're allowed to do.**

---

## Part III — Who it serves

### 10. The four audiences

Grid Network serves four distinct audiences, each with different needs.

**Audience 1 — Self-hosters and hobbyists.**

People who run their own servers, home automation, media libraries, file storage, photo management. They want to reach their services from anywhere, without depending on a company. They contribute to the network by running a grid agent, sometimes a rendezvous server, sometimes a light relay.

**Audience 2 — Small communities.**

Families, friends, small clubs, small businesses. They share a few services and want those services reachable to their members, without a central vendor. A rendezvous server on a Raspberry Pi or a small VPS is enough to keep the group connected.

**Audience 3 — Application developers.**

Self-hosted applications (Immich, Jellyfin, Nextcloud, Home Assistant) and commercial products that want to offer connectivity without building it themselves. They integrate with a grid agent on the user's device and get identity, pairing, NAT traversal, revocation, and cross-platform support for free.

**Audience 4 — Enterprises.**

Organizations that need device trust, BYOD support, remote access, and edge connectivity. They adopt Grid Network as a portable layer that works across vendors, integrates with their existing identity infrastructure, and doesn't lock them into any single provider.

These four audiences share a common problem. They differ in scale, resources, and risk tolerance, but the protocol serves all of them with the same primitives.

### 11. What each audience gains

**Self-hosters gain:**

- Remote access that works from anywhere, without accounts.
- Control over who can reach what, without a company in the loop.
- Portability across infrastructure providers.
- A working private network that's theirs, not rented.

**Small communities gain:**

- A shared rendezvous they can host on cheap hardware.
- Simple pairing for members.
- No dependency on commercial services.
- A graceful degradation model when infrastructure fails.

**Application developers gain:**

- Remote access without building connectivity infrastructure.
- Cross-platform support without writing per-platform code.
- A trust-portability story for their users.
- An enterprise sales narrative about not owning the customer's device graph.

**Enterprises gain:**

- Device trust portability across vendors and clouds.
- A unified model for BYOD, IoT, edge, partner, and employee devices.
- Integration with existing identity providers (Okta, Entra, MDM).
- Independence from any single grid vendor.

The important property is that **none of these gains require the others to exist.** A self-hoster gets value from a single grid agent. A community gets value from a rendezvous server on a Pi. A commercial project gets value from integration. An enterprise gets value from a self-hosted deployment. Each scales independently.

### 12. Who actually wants this

A common critique is: "Nobody actually cares about portability. Everyone uses Tailscale, and it works fine."

This is not true. Specific communities care about portability, and they care about it enough to make different choices:

- **Self-hosters** who have watched services shut down, change pricing, or restrict features.
- **Open-source applications** that don't want to run a cloud service or tell users to install third-party software.
- **Enterprises** that have been burned by vendor lock-in and are actively looking for portable solutions.
- **Regulators** who increasingly care about digital sovereignty and infrastructure resilience.
- **Communities** — small towns, hobbyist groups, cooperative ISPs — that want private infrastructure that isn't dependent on a vendor.

Each of these groups has a concrete example of what breaks under the current alternatives. The self-hoster whose NAS maker restricted the built-in remote access. The enterprise whose VPN vendor was acquired and changed its pricing. The open-source project that shut down its cloud service because it couldn't sustain the operational cost.

Grid Network is not for everyone. But it's for people who have already been burned by the alternatives.

---

## Part IV — The developer case

### 13. Developer adoption is the primary path

The most likely path to Grid Network becoming widely used is not end users adopting it directly. It's *application developers adopting it as a shared layer.*

The historical analogy is authentication. Fifteen years ago, every app built its own login system. Today, almost no app does — they delegate to Auth0, Okta, Firebase Auth, Cognito, Clerk, Supabase Auth, or "Sign in with Google." The reasons were practical: authentication is expensive to build correctly, risky to get wrong, and orthogonal to what makes an app valuable.

Every developer who has built an app in the last decade has made this exact decision: *"I'm not going to build auth. I'll use [provider]."*

The same argument applies to device identity and connectivity. The pitch to a developer is:

> You already offloaded user authentication to Auth0, Okta, or Google Sign-In. You should do the same for device connectivity. Grid Network is a shared protocol that handles identity, pairing, discovery, NAT traversal, relay fallback, and revocation. Your app calls a local grid agent, gets an authorized connection, and never thinks about keys, relays, or pairing again.

That's a shorter, sharper, and more immediately compelling pitch than anything about user ownership.

### 14. The problem every application faces

Every application that has a self-hosted, on-premises, or local-device component eventually hits the same wall: *"How does the user's phone reach this thing when they're not on the same network?"*

Today, every application answers this independently. Immich, Jellyfin, Home Assistant, Nextcloud, Syncthing, Paperless, PhotoPrism, Vaultwarden, Gitea, and dozens of others each have a partial solution. Each is a different implementation of the same concepts: identity, pairing, NAT traversal, relay, revocation, offline state, cross-platform support.

None of this is the app's actual job. None of it is a competitive advantage. All of it costs engineering time, support burden, and security review.

### 15. Three bad patterns

**Pattern 1 — Build a cloud service.**

"Sign up for our cloud, and we'll handle connectivity." Now the project is running a cloud service: uptime, support, compliance, abuse handling. It has stopped being a photo app and become an infrastructure company.

**Pattern 2 — Require an external tool.**

"Just install Tailscale and point the app at the local IP." This works technically, but it burdens the user, fragments the documentation, and makes the app depend on a third party the app doesn't control.

**Pattern 3 — Roll your own.**

"We'll build a custom tunnel." The project ends up reimplementing identity, authorization, discovery, NAT traversal, relays, revocation, and every edge case, badly, with a small team, and shipping security bugs because connectivity isn't the team's expertise.

Every self-hosted application eventually picks one of these three. All three are bad for different reasons.

### 16. What Grid Network changes for applications

Grid Network lets an application say: *"I don't need to solve this. Somebody else already did."*

Instead of building connectivity, the application talks to a **local grid agent** running on the user's device. The agent handles identity, pairing, discovery, NAT traversal, relay fallback, authorization, revocation, and freshness. The application asks the agent for a connection, and the agent returns a local URL. The application treats that URL like any other local service.

This means the application does not have to:

- Implement NAT traversal.
- Implement relay fallback.
- Implement device pairing.
- Implement certificate handling.
- Implement revocation.
- Implement offline-state handling.
- Implement cross-platform connectivity.
- Manage a user account system for connectivity.

The application retains its own *application-level* authorization — who can see which photos, who can admin the media server, who can access which files. That is the application's job. Grid Network only handles *network-level* identity and authorization.

The two layers are cleanly separated. The grid agent says "this connection is from a cryptographically authenticated device belonging to Alice." The application decides "Alice can see the Kids albums but not the Work albums." Both are necessary; neither substitutes for the other.

### 17. The analogy to authentication, in detail

This is the same story that happened with user authentication.

**Phase 1 — Roll your own.** Every app built its own username/password system: custom hashing, custom password reset, custom session management, custom MFA. This was a support nightmare, a security nightmare, and duplicated across every product in the industry.

**Phase 2 — Use a framework.** Apps started using Django's auth, Rails' Devise, Spring Security, passport.js. This was better — you still had your own user database, but at least the crypto was handled by people who knew what they were doing. But you still owned the account, the passwords, the resets, the policy, the compliance.

**Phase 3 — Offload to an identity provider.** Auth0, Okta, Firebase Auth, Cognito, Clerk, Supabase Auth. The app no longer stores passwords, doesn't handle resets, doesn't manage MFA, doesn't worry about compliance. The app calls an IdP, gets a token, and treats "who is this user" as a solved problem.

**Phase 4 — Federate to third parties.** "Sign in with Google," "Sign in with GitHub," "Sign in with Apple." Now the app doesn't even manage the identity provider — it delegates to a provider the user probably already has an account with.

The overall trend is unmistakable: **every modern app has decided that user identity is not their problem.**

Grid Network extends this reasoning from *user* authentication to *device* authentication and *network* authorization. It's the same insight: some problems are better solved once and shared than solved many times and fragmented.

### 18. What integration looks like

A project integrating with Grid Network does roughly this:

1. Bundles or recommends a grid agent for the user's platform.
2. Uses the grid agent's local API to establish connections.
3. Optionally receives grid identity information for use in application-level decisions.

That's the extent of the integration. Everything else — pairing, NAT traversal, relay, revocation — is handled by the agent.

The API is small:

```
grid.connect(service_link_id, capability) → local connection handle
grid.resolve(peer_id)                     → peer state
grid.discover()                            → list of known peers
grid.revoke(object_id)                     → issue revocation
grid.status()                              → daemon state
```

The application calls `grid.connect` with the service it wants to reach and the capability it wants to exercise. The agent returns a local URL. The application uses that URL like any other local service.

### 19. The commercial economics for applications

Building connectivity from scratch costs millions of dollars and years of engineering. Adopting Grid Network costs a small integration effort and delivers the same functionality — often better, because it's protocol-level rather than product-level.

**For a self-hosted open-source project:**

- No cloud service to run.
- No relay infrastructure.
- No cross-platform code.
- A much smaller surface for security review.

**For a commercial SaaS product:**

- Fewer engineers needed for connectivity.
- No relay infrastructure to run.
- A trust-portability story to sell to users.
- A compliance story to sell to enterprises.
- No vendor lock-in exposure for their customers.

### 20. Why this matters more than the end-user pitch

The end-user pitch is philosophical: "You should own your own network." It's true, but it's abstract, and it doesn't have a specific person with a specific pain.

The developer pitch is practical: "You can stop building connectivity infrastructure. Here's how." It has a specific person with a specific pain — the engineer who has written NAT traversal code, deployed a relay, or debugged a pairing failure — and it offers a specific solution.

The most likely path to Grid Network being widely adopted is applications adopting it. Once applications adopt it, users get it automatically. The user-facing portability story is downstream of the developer-facing adoption story.

---

## Part V — The contribution model

### 21. Three contribution layers

Participants contribute to the network in three distinct layers, each with different resource requirements.

**Layer 1 — Reachability publication.**

Every participant publishes its own reachability records. This is the minimum contribution, and it's automatic — a grid agent publishes its own reachability by default. The cost is negligible: a few hundred bytes of data, a few times per hour.

**Layer 2 — Rendezvous.**

Some participants run rendezvous servers. These are lightweight services that store reachability records for a bounded duration and serve them to peers on request. The resource requirements are modest:

- **CPU:** a Raspberry Pi 3 or comparable is sufficient for hundreds of peers.
- **RAM:** tens of megabytes.
- **Storage:** hundreds of megabytes, most of which expires quickly.
- **Bandwidth:** proportional to lookup queries, which are small and infrequent.

**Layer 3 — Relay.**

Some participants run relays. Relays forward encrypted traffic when direct connectivity fails. They are the layer where bandwidth and cost actually matter.

### 22. Contribution by capacity

The contribution model is proportionate to capacity. A participant contributes what it can and consumes what it needs.

| Contributor | What they contribute |
|-------------|----------------------|
| Phone, laptop, small device | Reachability publication |
| Raspberry Pi, home NAS | Rendezvous for a small group; light relay |
| Home server, small VPS | Rendezvous for a community; relay for a group |
| Enterprise server, cloud instance | Large rendezvous; high-capacity relay |
| Datacenter | Backbone relay for a region |

No one is required to contribute more than they can. A phone that only publishes its own reachability is a full participant. A Raspberry Pi that runs a small rendezvous contributes meaningfully. A datacenter contributes at a different scale but in the same direction.

### 23. Why contribution is safe

A common concern with contribution models is: *"What if a contributor is malicious?"*

Grid Network handles this by making infrastructure **untrusted by design**.

- A **rendezvous server** can only store and forward signed objects. It cannot forge them. A malicious rendezvous server can provide stale or false endpoints, but peers verify reachability records against signatures, so false endpoints are rejected.
- A **relay** can only forward encrypted traffic. It cannot decrypt. A malicious relay can drop or delay traffic, but it cannot read it, cannot modify it undetected, and cannot grant authorization.

This means **a contribution from an untrusted party is still useful.** A hobbyist's Raspberry Pi relay and a community VPS relay are equally valid, and a peer can use both without trusting either.

### 24. The economic shape

The network has a particular economic shape:

**Bottom of the stack: free.** Reachability publication is free. Every participant does it.

**Middle of the stack: volunteer.** Rendezvous and light relay are volunteer-contributed.

**Top of the stack: commercial.** High-bandwidth, low-latency, guaranteed-uptime relay is a service worth paying for.

The key property is that **no layer depends on the layer above it.** A community that never pays for commercial relay still has a functional network. An enterprise that never uses volunteer infrastructure still has a functional network. Both can coexist, and a peer can move between them without friction.

---

## Part VI — The commercial layer

### 25. What the commercial layer sells

The commercial layer sells **guarantees**, not access.

Free users can always connect. They get relay on a best-effort basis. Paid users get the same relay with a predictable quality level — higher priority, guaranteed capacity, consistent latency, SLA backing for enterprises.

The difference between free and paid is **predictability**, not availability.

### 26. Relay is a fallback, not a default

The connectivity preference order is:

1. **Local LAN.** Direct. No relay.
2. **Direct IPv6.** Direct. No relay.
3. **Direct IPv4.** Direct. No relay.
4. **NAT traversal.** Direct once established. No relay.
5. **Relay.** Direct failed. Fallback.

In a mature deployment with widespread IPv6 and working NAT traversal, most traffic never reaches step 5. Relay exists for the cases that steps 1–4 can't handle.

This matters because **relay bandwidth costs are much lower than they would be if relay were the default.** A network where 90% of traffic goes direct has very different economics than a network where 50% goes through relay.

In deployments where direct connectivity always works — a home LAN, an enterprise with well-connected infrastructure, a community with IPv6 throughout — the commercial layer is unused. The protocol works. No subscription, no account, no cost.

### 27. The commercial layer is not a platform

A platform owns the customer's identity, data, or relationships. Grid Network commercial operators own none of these. They sell services on top of the protocol. They do not own the protocol, the identity, or the relationship.

This is what forces them to compete on quality rather than on lock-in. A user can leave any operator at any time, taking their identity, relationships, and grants with them. The only reason to stay is that the operator is genuinely better.

The entire commercial model rests on one property: **identity is portable.** If identity were not portable, the commercial layer would inevitably become extractive. Because it is portable, the commercial layer is forced to be additive.

### 28. Free users as the network's foundation

The free tier is not a loss leader. It is the network's foundation.

Free users contribute:

- **Reachability publication.** Without this, there is no network.
- **Peer-to-peer connections.** Every free user who can establish a direct connection reduces relay load.
- **Hairpinning and traversal.** Free users on networks that support traversal contribute to the network's ability to avoid relay.
- **Local relays.** Some free users run their own relays, contributing to the volunteer pool.
- **Reduced infrastructure cost.** The aggregate of the above means the network's infrastructure cost is significantly lower than it would be if all users needed relay.
- **Ecosystem gravity.** A large free user base makes the network attractive to applications, contributors, and commercial operators.

A network with one million free users and ten thousand paid users is more valuable than a network with ten thousand paid users and no free users.

### 29. The relay priority model

Four properties:

**Property 1 — Free tier is real.** Free users can always connect. Relay is best-effort.

**Property 2 — Paid tier is priority.** Paid users get guaranteed relay capacity and consistent performance.

**Property 3 — Idle paid capacity flows to the public pool.** When paid capacity isn't in use, it serves the free tier.

**Property 4 — Contribution earns credit.** Users who run their own relays earn credits for the capacity they contribute.

Relay tickets carry a priority class:

- **Free class.** Served best-effort. May be preempted under contention.
- **Standard class.** Served with modest guaranteed share.
- **Priority class.** Served with higher guaranteed share.
- **Dedicated class.** Served with reserved capacity. Never preempted.

The protocol provides the mechanism for tickets to carry priority information. A relay's policy determines how many classes exist and what guarantees each provides.

### 30. Priority is a claim, not an identity

Priority is a property of the ticket, not of the user's identity. A free-tier user with a priority ticket gets priority service. A priority-tier user with a free ticket gets best-effort service.

This enables privacy (relays don't need to know who users are), portability (priority moves with the user across operators), and composability (users can hold tickets from different authorities).

### 31. Idle capacity donation

Commercial operators overprovision to handle surges. The surplus is idle most of the time. That surplus serves the free pool, with priority classes allowing instant reclaim when paying customers need capacity back.

The effect: money flowing into the commercial layer expands the network rather than extracting from it.

### 32. Credit pools and families

Real users come in groups: families, small businesses, hobbyist clubs. A family credit pool lets Dad add the family's devices, share contributions from the home server's relay, share consumption across devices, set per-member limits, and remove devices when they're lost.

Credits can be exchanged across operators at negotiated rates, like mobile roaming. A user of Operator A traveling to Operator B's region uses B's relays, and B accepts A's credits at an exchange rate.

This produces a system where capacity is used where it's most useful, not where it's owned. A user in Tokyo with a Frankfurt VPS uses their peer's Tokyo relay while in Japan, and their own Frankfurt relay when they travel to Europe. The credit balance balances out over time.

### 33. Preventing abuse

**Fake contribution.** Credits earned only for served traffic, verified by receiving peers. Statistical anomaly detection.

**Circular traffic.** Circuit detection, path length limits, time-based checks.

**Credit laundering.** Credits are bound to a pool. Cross-operator exchanges are operator-mediated.

**Free-riding.** Free riders limited to free-tier capacity.

**Fake identity multiplication.** Credits are per-pool, not per-identity.

**Consumption fraud.** Consumption recorded by the relay, not the consumer.

**Bonding.** Relay operators may post a bond, forfeited if abuse is proven.

The design principle: **the easiest way to earn credits is to actually contribute, and the easiest way to consume them is to actually need them.**

### 34. Geographic scarcity

A VPS in Hawaii provides scarcer capacity than a VPS in Frankfurt. The credit system should reflect this with a **scarcity multiplier**: relays in underserved regions earn more per byte. This makes contribution in scarce regions more attractive and encourages geographic diversity.

### 35. Self-hosted priority

A user with their own VPS or home server runs a grid relay on it. When their traffic needs relay, the grid agent prefers this relay. The user gets **self-priority**: their own relay serves their traffic at whatever priority they choose.

When the relay isn't reachable, the agent falls back to the free pool or commercial priority.

Enterprises do the same at larger scale: they run their own relay infrastructure, get priority on it, and contribute idle capacity to the public pool.

### 36. The six commercial products

**Managed rendezvous.** Low-cost, always-available rendezvous for users who don't want to run their own.

**Priority relay capacity.** High-bandwidth, low-latency, SLA-backed relay.

**Credit exchange.** Service that exchanges credits between operators.

**Enterprise integration.** Integration with Okta, Entra, MDM, SIEM, compliance systems.

**Support and SLAs.** Responsive support, published uptime, escalation paths.

**Managed deployment.** Turnkey grid deployments for organizations.

Every commercial product has a public-good component. Money flowing into the commercial layer expands the network rather than extracting from it.

### 37. The urgency buyer

The natural customer for the priority tier is the *urgency buyer*: the traveler on hotel Wi-Fi who needs to reach their server, the person whose connection is failing and just wants it to work *right now*, the small business owner whose meeting depends on reaching a file.

They aren't price-sensitive. They're reliability-sensitive. They'll happily pay for a moment of guaranteed reliability even if they use the network for free most of the time.

### 38. "No account" is a commercial feature

Grid Network has no account system. This is not just a technical property — it's a commercial benefit for operators:

- No user database to maintain.
- No signup flow to build.
- No password reset system to build.
- No account recovery to worry about.
- No data breach risk from a credential store.
- No GDPR exposure from a user database.

For operators, this is a real operational and legal simplification.

### 39. Developer funding

The commercial layer generates revenue that funds protocol maintenance. The model:

**Structural funding from commercial operators.** A percentage of revenue goes to protocol development, as a structural line item.

**The stewardship entity.** A nonprofit entity maintains the protocol, funds developers, and coordinates governance. Funded by commercial operators, enterprises, grants, and donations. Not owned by any single operator.

**Distribution mechanisms:**

- **Maintainer stipends.** Recurring payments for ongoing work.
- **Sponsored features.** A company or user funds a specific feature.
- **Bug bounties and security work.**
- **Ecosystem work.** Documentation, tooling, integration support.
- **Fellowships.** Time-limited funded positions.

**Funding sources:**

- Commercial operator revenue share.
- Individual donations.
- Grants (especially for security work).
- Enterprise contributions.
- Foundation endowments.

The goal: **a developer can work on Grid Network full-time and be paid fairly for it.** This sounds basic, but it is rare. Most open-source infrastructure is maintained by people who work on it in their spare time because they cannot afford to do otherwise.

If Grid Network reaches the point where core maintainers are paid, security work is funded, documentation and tooling are funded, and new contributors can be mentored and compensated, then the protocol will be sustainable.

---

## Part VII — Edge cases and unusual scenarios

### 40. Offline for extended periods

A peer may be offline for weeks or months. Identity is unchanged. Relationships are unchanged. Reachability records expire and are forgotten. When the peer comes back online, it republishes reachability. Authorization is bounded — leases expire, and when the peer returns, it must renew them.

The user experience: "your server is online again, but your phone needs to renew its access."

### 41. Device replacement

A user replaces their phone. The new phone has a new device key but belongs to the same principal. The relationship with the user's server is preserved. The new device key is added to the identity document; the old one is revoked or retired.

### 42. Lost device

A user loses their phone. They revoke the
