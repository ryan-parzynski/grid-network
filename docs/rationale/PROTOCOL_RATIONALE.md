# Mesh Project — Design Rationale and Contribution Model

**Document:** `RATIONALE.md`
**Version:** 1.0
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
- Anyone trying to understand the *intent* behind the technical choices.

It does not contain normative requirements. Where it describes behavior that is normatively specified elsewhere, it does so for explanation, not for authority.

---

## Part I — The Problem

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

### 3. The deeper problem

The deeper problem is that **connectivity is treated as a feature, not as infrastructure.**

When a project needs connectivity, it builds connectivity. When a company needs connectivity, it buys connectivity. There is no shared layer that all of them can consume the way they consume TLS, or HTTP, or DNS.

This means:

- Every project reimplements the same concepts (identity, pairing, NAT traversal, relay, revocation).
- Every implementation has its own bugs, its own edge cases, its own security review burden.
- Every user has to learn a new connectivity story for every new app.
- Every ecosystem fragments along whatever connectivity choices individual products made.

The result is a lot of duplicated effort, a lot of fragmented user experience, and a lot of home networks that are subtly less secure than they could be.

### 4. The insight

The insight behind Mesh is that **connectivity is not a feature. It's infrastructure.** It should be a shared, audited, portable primitive that every project can consume — the same way they consume TLS for encryption, HTTP for requests, or DNS for resolution.

The reason this hasn't happened yet is that connectivity has three parts that are hard to standardize:

1. **Identity.** Who is this device?
2. **Authorization.** What is it allowed to do?
3. **Reachability.** Where is it right now?

Each of these is a distinct problem, and the current landscape tends to conflate them. When they are conflated, standardization becomes hard — because different projects want to make different trade-offs. When they are separated, each can be standardized independently.

Mesh separates them cleanly:

- **Identity** is a cryptographic keypair, controlled by the user.
- **Authorization** is a signed grant, verified locally.
- **Reachability** is an ephemeral hint, replaceable and untrusted.

Once separated, each becomes small enough to specify, and the whole system becomes small enough to be portable.

---

## Part II — The Solution

### 5. What Mesh is

Mesh is a **control plane for identity, authorization, and reachability** that sits above whatever networking already exists.

It is not a VPN. It is not a tunnel. It is not a replacement for WireGuard, IPv6, or any transport protocol. It is a layer that answers questions *about* devices and their permissions, using signed objects that participants hold and verify themselves.

The three questions Mesh answers are:

- **Who is this?** — A cryptographic identity, controlled by the participant.
- **What is it allowed to do?** — A signed authorization, verified locally.
- **Where can I find it?** — An ephemeral reachability record, refreshed as networks change.

Every one of these questions is answered by cryptographically signed objects. No answer requires contacting a central authority. No answer requires a company to be in the loop.

### 6. What Mesh is not

- **Not a decentralized VPN.** A VPN is a transport. Mesh is a control plane above transports.
- **Not a DNS replacement.** DNS maps names to addresses. Mesh maps identities to reachability, and adds authorization on top.
- **Not an anonymity network.** Peers are identified. Metadata is visible to infrastructure operators. This is by design.
- **Not a blockchain.** There is no global consensus, no ledger, no mining, no token.
- **Not a peer-to-peer file system.** Peers connect directly or through relays, but there is no distributed storage.
- **Not a company.** There is no operator, no owner, no central authority.

### 7. The key design properties

Four properties distinguish Mesh from other approaches.

**Property 1 — Identity is portable.**

A device's identity is a cryptographic keypair. It does not depend on any account, any server, any provider, or any vendor. It can be used across multiple rendezvous providers, multiple relays, multiple networks, and multiple applications.

**Property 2 — Authorization is local.**

A device verifies authorization itself, using state it holds locally. It does not ask a server "am I allowed to do this?" It asks itself, using signed objects it already has. This means authorization works offline, works through network partitions, works when the infrastructure is unreachable.

**Property 3 — Reachability is ephemeral.**

Where a device currently is, is not part of its identity. It's a hint, refreshed as networks change. If a device moves, the hint changes; the identity doesn't. If a rendezvous server is unreachable, cached hints still work until they expire.

**Property 4 — Infrastructure is untrusted.**

Rendezvous servers, relays, and any other infrastructure can be operated by anyone, including parties the user does not trust. They help peers find each other and forward encrypted traffic, but they cannot forge identity, cannot grant authorization, cannot decrypt content, cannot alter signed objects without detection.

These four properties, taken together, produce a system where **the network can help you reach someone without becoming an authority over who you are or what you're allowed to do.**

---

## Part III — Who it serves

### 8. The four audiences

Mesh serves four distinct audiences, each with different needs.

**Audience 1 — Self-hosters and hobbyists.**

People who run their own servers, home automation, media libraries, file storage, photo management. They want to reach their services from anywhere, without depending on a company. They contribute to the network by running a mesh agent, sometimes a rendezvous server, sometimes a light relay.

**Audience 2 — Small communities.**

Families, friends, small clubs, small businesses. They share a few services and want those services reachable to their members, without a central vendor. A rendezvous server on a Raspberry Pi or a small VPS is enough to keep the group connected.

**Audience 3 — Commercial projects.**

Self-hosted applications (Immich, Jellyfin, Nextcloud, Home Assistant) and commercial products (SaaS, consumer apps, enterprise tools) that want to offer connectivity without building it themselves. They integrate with a mesh agent on the user's device and get identity, pairing, NAT traversal, revocation, and cross-platform support for free.

**Audience 4 — Enterprises.**

Organizations that need device trust, BYOD support, remote access, and edge connectivity. They adopt Mesh as a portable layer that works across vendors, integrates with their existing identity infrastructure, and doesn't lock them into any single provider.

These four audiences share a common problem. They differ in scale, resources, and risk tolerance, but the protocol serves all of them with the same primitives.

### 9. What each audience gains

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

**Commercial projects gain:**

- Remote access without building connectivity infrastructure.
- Cross-platform support without writing per-platform code.
- A trust-portability story for their users.
- An enterprise sales narrative about not owning the customer's device graph.

**Enterprises gain:**

- Device trust portability across vendors and clouds.
- A unified model for BYOD, IoT, edge, partner, and employee devices.
- Integration with existing identity providers (Okta, Entra, MDM).
- Independence from any single mesh vendor.

The important property is that **none of these gains require the others to exist.** A self-hoster gets value from a single mesh agent. A community gets value from a rendezvous server on a Pi. A commercial project gets value from integration. An enterprise gets value from a self-hosted deployment. Each scales independently.

---

## Part IV — The contribution model

### 10. Three contribution layers

Participants contribute to the network in three distinct layers, and each layer has different resource requirements.

**Layer 1 — Reachability publication.**

Every participant publishes its own reachability records. This is the minimum contribution, and it's automatic — a mesh agent publishes its own reachability by default. The cost is negligible: a few hundred bytes of data, a few times per hour.

Any device that runs a mesh agent participates at this layer. A phone, a laptop, a Raspberry Pi, a server. There is no distinction between "contributors" and "users" at this layer — participation *is* the contribution.

**Layer 2 — Rendezvous.**

Some participants run rendezvous servers. These are lightweight services that store reachability records for a bounded duration and serve them to peers on request. Rendezvous servers do not need to persist state long-term, and they do not need to be highly available — peers cache records and use them until they expire.

The resource requirements for a rendezvous server are modest:

- **CPU:** a Raspberry Pi 3 or comparable is sufficient for hundreds of peers.
- **RAM:** tens of megabytes.
- **Storage:** hundreds of megabytes, most of which expires quickly.
- **Bandwidth:** proportional to lookup queries, which are small and infrequent.

A rendezvous server for a family, a hobbyist group, or a small business is well within reach of hobby-grade hardware.

**Layer 3 — Relay.**

Some participants run relays. Relays forward encrypted traffic when direct connectivity fails. They are the layer where bandwidth and cost actually matter.

A relay:

- Accepts encrypted traffic from a peer.
- Forwards it to the destination.
- Sees only ciphertext.
- Enforces resource limits (bytes, rate, sessions) per ticket.

The cost of a relay is proportional to traffic. This means a small relay can support a small community's fallback needs, while a large relay can support substantial traffic — but neither is privileged over the other.

### 11. Contribution by capacity

The contribution model is **proportionate to capacity**. A participant contributes what it can and consumes what it needs.

| Contributor | What they contribute |
|-------------|----------------------|
| Phone, laptop, small device | Reachability publication |
| Raspberry Pi, home NAS | Rendezvous for a small group; light relay |
| Home server, small VPS | Rendezvous for a community; relay for a group |
| Enterprise server, cloud instance | Large rendezvous; high-capacity relay |
| Datacenter | Backbone relay for a region |

No one is required to contribute more than they can. A phone that only publishes its own reachability is a full participant. A Raspberry Pi that runs a small rendezvous contributes meaningfully. A datacenter contributes at a different scale but in the same direction.

There is no "minimum contribution" required to participate, and there is no "maximum contribution" that makes someone privileged. Contribution is voluntary and proportionate.

### 12. Why contribution is safe

A common concern with contribution models is: *"What if a contributor is malicious?"*

Mesh handles this by making infrastructure **untrusted by design**.

- A **rendezvous server** can only store and forward signed objects. It cannot forge them. A malicious rendezvous server can provide stale or false endpoints, but peers verify reachability records against signatures, so false endpoints are rejected.
- A **relay** can only forward encrypted traffic. It cannot decrypt. A malicious relay can drop or delay traffic, but it cannot read it, cannot modify it undetected, and cannot grant authorization.

This means **a contribution from an untrusted party is still useful.** A hobbyist's Raspberry Pi relay and a community VPS relay are equally valid, and a peer can use both without trusting either.

The same is true for rendezvous. A peer can use a rendezvous server run by someone they've never met, because the objects served are signed by their issuers, not by the rendezvous operator.

### 13. The economic shape

This produces a network with a particular economic shape.

**Bottom of the stack: free.**

Reachability publication is free. Every participant does it because it's how they become reachable.

**Middle of the stack: volunteer.**

Rendezvous and light relay are volunteer-contributed. A hobbyist runs a Raspberry Pi because they want their own network to work. A community runs a shared VPS because the members want reliable rendezvous. A small business runs a server because they want their employees connected.

**Top of the stack: commercial.**

High-bandwidth, low-latency, guaranteed-uptime relay is a service worth paying for. Enterprises pay for it because they need SLA-backed connectivity. Commercial operators sell it because there's demand. The protocol makes the service interchangeable, so the market is competitive.

The interesting property is that **no layer depends on the layer above it.** A community that never pays for commercial relay still has a functional network. An enterprise that never uses volunteer infrastructure still has a functional network. Both can coexist, and a peer can move between them without friction.

---

## Part V — What this enables for applications

### 14. The application's problem

Every self-hosted application eventually faces the connectivity problem.

Immich, Jellyfin, Nextcloud, Home Assistant, Paperless, PhotoPrism, Vaultwarden, Gitea, and dozens of others each have a partial answer to "how do I let users reach this remotely?" Each answer is different, incomplete, and expensive to maintain.

The problem is that connectivity is orthogonal to the application's actual purpose. A photo app should be about photos. A media server should be about media. A file sync tool should be about files.

None of them should be about NAT traversal, relay infrastructure, or device pairing.

### 15. Three bad patterns applications fall into

**Pattern 1 — Build a cloud service.** *"Sign up for our cloud, and we'll handle connectivity."* Now the project is running a cloud service: uptime, support, compliance, abuse handling. It has stopped being a photo app and become an infrastructure company.

**Pattern 2 — Require an external tool.** *"Just install Tailscale and point the app at the local IP."* This works technically, but it burdens the user, fragments the documentation, and makes the app depend on a third party the app doesn't control.

**Pattern 3 — Roll your own.** *"We'll build a custom tunnel."* This is the worst option. The project ends up reimplementing identity, authorization, discovery, NAT traversal, relays, revocation, and every edge case, badly, with a small team, and shipping security bugs because connectivity isn't the team's expertise.

### 16. What Mesh changes for applications

Mesh lets an application say: *"I don't need to solve this. Somebody else already did."*

Instead of building connectivity, the application talks to a **local mesh agent** running on the user's device. The agent handles identity, pairing, discovery, NAT traversal, relay fallback, authorization, revocation, and freshness. The application asks the agent for a connection, and the agent returns a local URL. The application treats that URL like any other local service.

This means the application does not have to:

- Implement NAT traversal.
- Implement relay fallback.
- Implement device pairing.
- Implement certificate handling.
- Implement revocation.
- Implement offline-state handling.
- Implement cross-platform connectivity.
- Manage a user account system for connectivity.

The application retains its own *application-level* authorization — who can see which photos, who can admin the media server, who can access which files. That is the application's job, and it remains the application's job. Mesh only handles *network-level* identity and authorization.

The two layers are cleanly separated. The mesh agent says "this connection is from a cryptographically authenticated device belonging to Alice." The application decides "Alice can see the Kids albums but not the Work albums." Both are necessary; neither substitutes for the other.

### 17. The analogy to authentication

This is the same story that happened with user authentication.

Fifteen years ago, every app built its own login system: custom hashing, custom password reset, custom session management, custom MFA. Then the industry realized this was wasteful, and every app started delegating to Auth0, Okta, Firebase Auth, Google Sign-In. Today, almost no modern app builds its own authentication system.

The reason is simple: authentication is not the app's job. It's a shared problem with a shared solution.

Mesh extends this reasoning from *user* authentication to *device* authentication and *network* authorization. It's the same insight: some problems are better solved once and shared than solved many times and fragmented.

### 18. What integration looks like

A project integrating with Mesh does roughly this:

1. Bundles or recommends a mesh agent for the user's platform.
2. Uses the mesh agent's local API to establish connections.
3. Optionally receives mesh identity information for use in application-level decisions.

That is the extent of the integration. Everything else — pairing, NAT traversal, relay, revocation — is handled by the agent.

The commercial economics are straightforward. Building connectivity from scratch costs millions of dollars and years of engineering. Adopting Mesh costs a small integration effort and delivers the same functionality — often better, because it's protocol-level rather than product-level.

---

## Part VI — The ecosystem that results

### 19. Four participant types

The protocol produces a network with four natural participant types.

**Users.** They run a mesh agent on their devices, pair them, and use services. They contribute by publishing their own reachability. They consume what the network provides.

**Contributors.** Some users also run rendezvous servers or relays. These might be Raspberry Pis, home servers, VPSes, or shared community infrastructure. Contribution is proportionate to capacity.

**Applications.** They consume the mesh agent's API to provide remote access for their services. They integrate once and inherit the entire mesh connectivity story.

**Commercial operators.** They provide SLA-backed rendezvous, relay, support, and management services. They compete on reliability, latency, bandwidth, and support — not on lock-in.

These four types are not exclusive. A user can be a contributor. An application can be a commercial operator. An enterprise can be both a heavy user and a commercial buyer.

### 20. Why this is stable

The stability of this ecosystem comes from three properties.

**Property 1 — No privileged role.**

No participant has a privileged position in the protocol. A Raspberry Pi contributes what it can; a datacenter contributes what it can. Neither can exclude the other. Neither can capture the protocol.

**Property 2 — No exclusive dependency.**

No participant depends exclusively on any other. A user without commercial relay still works. An enterprise without volunteer infrastructure still works. A community without either still works. Every layer has fallbacks.

**Property 3 — No permanent lock-in.**

No participant is locked into any other. A user can switch rendezvous providers without losing identity. An enterprise can switch relay vendors without rebuilding trust. An application can switch mesh implementations without breaking its user's network.

These three properties make the ecosystem *robust against capture* and *resilient against failure*. They also make it *commercially viable*, because they allow operators to compete on quality rather than on the cost of leaving.

### 21. What the market looks like

The commercial shape of the Mesh ecosystem is not "one company owns the network." It's a market with several distinct segments.

**Rendezvous hosting.** A low-cost service for users who don't want to run their own. The economics are small but predictable, and the value is convenience.

**Relay bandwidth.** A competitive market for high-quality connectivity. This is where commercial operators make real money — bandwidth, latency, and reliability are genuinely valuable.

**Enterprise deployment.** Managed mesh infrastructure for organizations, with integration into existing identity providers, MDM, and compliance systems. This is a substantial market.

**Application integration.** Tooling, libraries, and support for applications that want to integrate Mesh. This is a smaller but important market.

**Infrastructure appliances.** Preconfigured hardware — routers, NAS devices, home-server appliances — that ship with mesh support built in. This is a natural fit for the existing hardware ecosystem.

The key property is that **each segment can be served by many operators, and none of them requires ownership of the network as a whole.** This is what makes the ecosystem competitive rather than monopolistic.

---

## Part VII — Edge cases and unusual scenarios

### 22. Offline for extended periods

A peer may be offline for weeks or months. What does the protocol do?

The peer's **identity** is unchanged. Its **relationships** are unchanged. Its **reachability** records expire and are forgotten. When the peer comes back online, it republishes reachability and everything resumes.

Authorization, however, is bounded. Leases expire. When the peer returns, it must renew its leases before accessing services. This is by design — it ensures that long-absent peers don't retain indefinite authorization.

The user experience is: "your server is online again, but your phone needs to renew its access." This is a reasonable and expected behavior.

### 23. Device replacement

A user replaces their phone. What happens?

The new phone has a **new device key**, but it belongs to the **same principal** (assuming the user transfers their identity, e.g., through a recovery flow or explicit device binding). The relationship with the user's server is preserved. The new device key is added to the identity document; the old one is revoked or retired.

The user experience is: "your new phone is now your phone." No re-pairing with every service is necessary if the identity transfer is done correctly.

### 24. Lost device

A user loses their phone. What happens?

The user (from another device or from a recovery flow) revokes the lost device's key. The revocation propagates to peers who care. Services the lost device was authorized for stop accepting its connections.

Because revocation is a signed object, it works even if the lost device is offline — the revocation is effective as soon as a verifier receives it. And because leases have maximum offline tolerance, even without an explicit revocation, a lost device eventually stops being able to access services.

The user experience is: "I revoked my old phone; it can't access my stuff anymore."

### 25. Rendezvous server disappears

A community's rendezvous server goes down. What happens?

Peers that have cached reachability records continue using them until they expire. Peers that haven't cached can try other rendezvous servers, if any are configured. If no rendezvous is reachable, peers may be unable to discover each other's current endpoints — but their *existing* sessions, their *identities*, and their *authorizations* are unaffected.

When the rendezvous server comes back online, or when another is configured, discovery resumes. The user experience is: "discovery was temporarily slow, but nothing was lost."

### 26. Relay operator is malicious

A user's traffic is being relayed by an operator who tries to attack. What can they do?

A relay sees:

- Source and destination endpoints.
- Volume and timing of traffic.
- The fact that two peers are communicating.

A relay does **not** see:

- Plaintext content (traffic is end-to-end encrypted).
- Authorization state (relays have no authority).
- Identity (relays see endpoint identifiers, not cryptographic identities).

A malicious relay can drop traffic, delay it, or attempt to inject traffic. The first two are availability problems; the third is detected by transport-layer encryption. The relay cannot impersonate either peer, cannot grant or revoke authorization, cannot read content.

The user experience is: "I switched to a different relay; the malicious one accomplished nothing."

### 27. Identity key is compromised

A user's Identity Root is stolen. This is the worst-case scenario.

A compromised Identity Root can produce valid signatures, so it can impersonate the user to peers. There is no in-band recovery mechanism for this — the protocol cannot distinguish a legitimate signature from a compromised signature.

Recovery is out-of-band: the user contacts their peers through a trusted channel, explains the compromise, and establishes a new identity. Peers accept the new identity through whatever mechanism the deployment uses (re-pairing, administrative action, social recovery).

This is why the Identity Root should be stored with the highest possible protection — offline, hardware-backed, or in a secure enclave. Compromise of the Identity Root is the highest severity event in the protocol.

### 28. Service moves between devices

A user moves their Jellyfin service from one server to another. What happens?

The service **identity** is preserved (assuming it was bound to a principal, not to a specific device). Grants and leases remain valid because they reference the service identity, not the device. Only the reachability changes — the new device publishes its own reachability records.

The user experience is: "I moved Jellyfin to a new machine; my phone doesn't have to re-pair." This is exactly what a user expects.

### 29. Peer on a network with no direct connectivity

A user is on a network that blocks direct peer-to-peer traffic (hotel Wi-Fi, corporate network, restrictive CGNAT). What happens?

The mesh agent detects that direct connection fails. It requests a relay path from an available relay. The relay forwards encrypted traffic, and the connection is established.

The user experience is: "It was slightly slower, but it worked." The relay is transparent to the application.

### 30. Application uses mesh identity for its own authorization

A user has two devices — a personal laptop and a work laptop. Both are paired to the same Jellyfin server. The user wants their personal laptop to access all libraries, and their work laptop to access only the Music library.

The mesh agent provides identity: "this connection is from device X." The application's own authorization (in Jellyfin) decides: "device X can access Music only."

This separation is important. The mesh agent handles *who the device is*. The application handles *what the device can do within the application*. Both are necessary, and they don't overlap.

---

## Part VIII — Frequently raised concerns

### 31. "Isn't this just a blockchain?"

No. Mesh has no global consensus, no ledger, no mining, no tokens, no global ordering. It uses cryptographic signatures and local verification, which is a fundamentally different approach.

Blockchain solves the problem of "how do independent parties agree on one global history." Mesh solves the problem of "how does one party verify another's identity and authorization." These are different problems requiring different solutions.

### 32. "Isn't this just Tor / I2P / Freenet?"

No. Those systems provide anonymity through routing. Mesh provides authenticated identity and authorization with explicit identity.

Mesh has no anonymity properties. It provides *confidentiality* of content and *portability* of identity. If a user needs anonymity, Mesh is not the right tool for that need.

### 33. "Isn't this just Tailscale / Cloudflare Tunnel?"

Similar in some ways, fundamentally different in others. Tailscale and Cloudflare Tunnel are products built around a specific company's infrastructure. Mesh is a protocol that any company can implement, and identity is portable across implementations.

The key difference is: if Tailscale disappears, your network is gone. If a Mesh infrastructure provider disappears, you point your peer at a different one — your identity, relationships, and authorizations are unaffected.

### 34. "Why not just use a VPN?"

VPNs solve a different problem. A VPN gives you access to a network. Mesh gives you access to a *service* with *identity* and *authorization* attached. VPNs are typically all-or-nothing; Mesh is per-service and per-relationship.

Also, VPNs typically require a single point of trust (the VPN server). Mesh explicitly avoids this — infrastructure is untrusted by design.

### 35. "What about performance?"

For direct connections, Mesh performs comparably to any other overlay network — the encrypted traffic goes over the same path. For relayed connections, performance depends on the relay. A nearby relay performs better than a distant one; a high-bandwidth relay performs better than a low-bandwidth one.

The protocol does not mandate a relay-selection algorithm. Different implementations may select relays by different criteria — latency, cost, policy, availability. This is left to the connectivity layer.

### 36. "What about metadata privacy?"

Mesh provides confidentiality of content and authorization, not anonymity of participation. Rendezvous servers see which peers query for which other peers. Relays see endpoints and traffic volume. This is stated explicitly in the protocol's non-properties.

If metadata privacy is a requirement, Mesh can be composed with additional layers — for example, onion routing for rendezvous lookups. This is deferred to future versions.

### 37. "What about governance?"

V1 has no governance mechanism. The protocol is a specification, not an organization. As independent implementations emerge, governance questions will need to be answered — but the protocol does not presuppose any particular answer. Options include reference-implementation-driven, benevolent-dictator, and standards-body models.

This is deliberately deferred. The protocol is stable enough at V1 that governance questions do not need to be answered yet. They will need to be answered before the protocol is deployed at scale.

### 38. "What if the Identity Root is compromised?"

V1 has no in-band recovery. This is intentional — any in-band recovery mechanism would be an authority the protocol cannot trust. Recovery is out-of-band: the user establishes a new identity through a trusted channel.

This is why Identity Root protection is critical. Users should store it offline, hardware-backed, or in a secure enclave, and should treat compromise as a catastrophic event.

---

## Part IX — What success looks like

### 39. Short-term success

In the near term, success looks like: **one working implementation, one working rendezvous server, and one application integrating.**

If a self-hoster can run a mesh agent, pair two devices, and reach a service across the internet — success.

If an application like Immich or Jellyfin integrates with the mesh agent and offers remote access without building connectivity itself — success.

If a small community can run a rendezvous server on a Raspberry Pi and keep its members connected — success.

### 40. Medium-term success

Over a few years, success looks like: **an ecosystem with multiple implementations, multiple rendezvous providers, and multiple applications integrating.**

If two independent implementations interoperate byte-for-byte — success.

If several rendezvous providers exist, and users can move between them without friction — success.

If dozens of applications integrate with the mesh agent — success.

If commercial operators offer relay services that compete on quality rather than lock-in — success.

### 41. Long-term success

Over a decade, success looks like: **Mesh becomes to device connectivity what TLS became to transport security.**

If a new open-source project in 2035 can say "we use Mesh for connectivity" the way a project today says "we use TLS for encryption" — success.

If "remote access to self-hosted services" becomes a solved problem, in the same way that "encrypted web traffic" became a solved problem — success.

If a company can no longer build a business on the sole basis of holding customer networks hostage — success.

### 42. What success does not look like

Success is not:

- Replacing Tailscale, Cloudflare, or any other vendor.
- Destroying the commercial connectivity industry.
- Achieving mainstream adoption.
- Being on every device in the world.
- Eliminating all centralization.

Success is: **making it possible for the people who care about portability to have it, and for the ecosystem to grow around that possibility.**

This is closer to how email succeeded than to how a startup succeeds. Email didn't kill commercial email providers — it made it possible for anyone to run one. The same is true for Mesh.

---

## Part X — Summary

### 43. The one-sentence summary

> Mesh is a cryptographic identity and authorization layer that turns whatever network connectivity happens to exist into a usable, replaceable connectivity fabric — so that private networks between your own devices don't have to be rented from a company.

### 44. The one-paragraph summary

Every self-hosted service eventually hits the same wall: "how do I reach this from somewhere else?" Today, the answer is either expose it to the internet, rent a company's account, or become an expert. Mesh is a fourth option. It separates identity, authorization, and reachability into distinct signed objects that participants verify locally. Infrastructure — rendezvous, relay — can be operated by anyone, including parties the user doesn't trust, because it cannot forge identity or grant authorization. The result is a protocol where private connectivity works like email: anyone can run infrastructure, anyone can switch providers, and no company gets to decide whether your network exists.

### 45. The one-line framing

**Your devices. Your identity. Your relationships. Not rented. Not revocable by a vendor. Not dependent on any single provider.**

---

## Appendix — Document map

This document is one of several in the project. For readers who want to go deeper:

- **`PROTOCOL.md`** — the normative protocol specification (v0.6.2).
- **`OBJECTS.md`** — canonical encoding, cryptographic constructions, object schemas, stream rules, test vectors.
- **`SECURITY.md`** — threat model, verifier processing rules, parser hardening, resource limits.
- **`IMPLEMENTATION.md`** — Mesh Agent architecture, local APIs, transport engine.
- **`CONNECTIVITY.md`** — direct connectivity, relay architecture, path abstraction, future multipath.
- **`VERSIONING.md`** — protocol versioning, compatibility, governance (may be folded into `PROTOCOL.md`).
- **`TEST-VECTORS/`** — byte-exact normative test cases.
- **`VISION.md`** — product positioning, disruption analysis, ecosystem model (may overlap with this document).
- **`ECOSYSTEM.md`** — community infrastructure, commercial services, enterprise layer (may overlap with this document).
- **`ROADMAP.md`** — V1, V1.x, V2, research agenda.

This document (`RATIONALE.md`) explains the *why*. The others explain the *what* and the *how*.

