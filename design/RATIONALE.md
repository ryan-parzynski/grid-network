# Grid Network — Design Rationale

---

## Executive Summary

Grid Network is a **control plane for identity, authorization, and reachability** that sits above whatever networking already exists.

Not a VPN. Not a tunnel. Not a replacement for WireGuard, IPv6, or any transport protocol. A layer that answers questions *about* devices and their permissions, using signed objects that participants hold and verify themselves.

---

## The Problem

Every self-hosted service, personal server, home automation system, and private application eventually hits the same wall:

> *"How do I reach this from somewhere else?"*

This is not a niche problem. It affects home servers running Jellyfin, Immich, Nextcloud; home automation running Home Assistant; NAS devices with file sharing; personal code repositories; backup infrastructure; game servers; development machines you want to SSH into.

The problem is not technical. The technology exists. The problem is **institutional**: no vendor-neutral way exists to establish and maintain portable identity and authorization.

### The Three Bad Choices Today

**Choice 1 — Expose to the Internet:** Open a port, forward on the router, hope nothing scans you. Firmware vulnerabilities, default credentials, automatic scanners, Shodan exposure, ransomware attacks.

**Choice 2 — Use a Proprietary Tunnel/Grid Network VPN:** Tailscale, Cloudflare Tunnel, ZeroTier, ngrok. Beautiful products, excellent UX. But: company owns the device graph, access policies, relationship data. Company is a permanent authority. If company changes terms, gets acquired, shuts down, changes pricing — user adapts or loses network. Underlying protocol is proprietary: no third-party implementations, no competing providers, can't switch without rebuild.

**Choice 3 — Build It Yourself:** Run your own VPN, manage certificates, handle dynamic DNS, deal with CGNAT, NAT traversal, relay infrastructure, revocation, offline state. Works, but requires sysadmin expertise most people don't have. Even technical people spend weekends debugging it.

### The Hidden Cost

The obvious framing: "This is inconvenient." The real framing: **"The ability to reach your own devices has become a subscription."**

A decade ago: open a port (risky but yours) or run a VPN (awkward but yours). Today: the easy path is to sign up for a service. Works beautifully. But you don't own your network anymore. You're renting the ability to reach your own stuff.

This is the same story as email, social media, cloud storage, and every other layer of the internet. Convenience slowly becomes dependence. It's not a conspiracy; it's how products work. But it creates a specific cost: **you don't own your digital relationships.** Your home server's relationship to your phone is mediated by Tailscale's servers. If Tailscale disappears, the relationship disappears. Not because the technology failed. Because you never actually owned it.

---

## The Solution

Grid Network is a **control plane for identity, authorization, and reachability** that sits above whatever networking already exists.

### The Three Questions

1. **Who is this?** — A cryptographic identity, controlled by the participant.
2. **What is it allowed to do?** — A signed authorization, verified locally.
3. **Where can I find it?** — An ephemeral reachability record, refreshed as networks change.

Every question is answered by signed objects. No answer requires contacting a central authority.

### What Grid Network Is Not

- Not a decentralized VPN (VPN is a transport; Grid is a control plane above transports)
- Not a DNS replacement (DNS maps names to addresses; Grid maps identities to reachability with authorization)
- Not an anonymity network (peers are identified; metadata visible to infrastructure operators)
- Not a blockchain (no global consensus, no ledger, no mining, no token)
- Not a peer-to-peer file system (no distributed storage)
- Not a company (no operator, no owner, no central authority)
- Not a Tor/I2P/Freenet replacement (those provide anonymity through routing)

---

## Five Key Design Properties

### Property 1 — Identity is Portable
A device's identity is a cryptographic keypair. It does not depend on any account, server, provider, vendor, or central authority. Survives network changes, device replacement, provider changes, infrastructure changes, service outages.

### Property 2 — Authorization is Local
A device verifies authorization itself, using state it holds locally. Enables offline authorization, partition-tolerant authorization, authority-independent verification, immediate revocation.

### Property 3 — Reachability is Ephemeral
Where a device currently is, is not part of its identity. It's a hint, refreshed as networks change. Enables seamless network transitions, IP address changes, untrusted rendezvous, infrastructure portability.

### Property 4 — Infrastructure is Untrusted
Rendezvous servers, relays, and any infrastructure can be operated by anyone, including parties the user doesn't trust. Enforces: no rendezvous server decides authorization, no relay decrypts content, no infrastructure becomes authority, every intermediary can be replaced.

### Property 5 — Protocol is Open
No proprietary component. Any implementation can speak to any other. Enables community implementations, competitive relays, interoperable infrastructure, no lock-in to any vendor, independent security audits.

---

## The Core Security Invariant

> Given a set of locally trusted anchors, authenticated protocol objects, known revocations, accepted chain state, and recorded observation history, a verifier must be able to deterministically establish the identity, authorization, validity, and freshness state of a peer **as of the verifier's most recent observation**, without contacting an authority.

This means:
- Rendezvous infrastructure CANNOT define identity
- Relays CANNOT define authorization
- DNS CANNOT define identity
- IP addresses CANNOT define identity
- WireGuard keys CANNOT by themselves define app-level authorization
- Temporary pairing codes CANNOT become permanent credentials

---

## How It Works in Practice

Alice sets up her home server. She installs a Grid agent. Bob wants to access Alice's Jellyfin server remotely. Alice gives Bob a QR code. Bob scans the QR code with his phone. The QR code initiates a pairing:

1. Devices exchange public keys (temporary pairing keys)
2. Bob's phone signs "I recognize Alice's server"
3. Alice's server signs "I recognize Bob's phone"
4. Mutual recognition established

Now Alice can grant Bob access:
1. Alice creates a Grant: "Bob's phone can stream from Jellyfin"
2. Grant is valid for 30 days, covers Jellyfin.stream capability
3. Bob's phone automatically renews the lease monthly

Bob accesses Jellyfin from anywhere:
1. Bob's phone reaches Alice's server (direct if possible, via relay if not)
2. Server verifies: "Bob's phone has a valid grant for Jellyfin.stream"
3. Grant verified locally (no contact with Alice or authority needed)
4. Connection established

Bob loses his phone:
1. Alice revokes the grant
2. The revocation is signed by Alice's identity root
3. Distributed to the network through normal protocol mechanisms
4. Bob's phone can no longer access anything
5. Alice issues a new grant to her new phone

Six months later Bob is offline:
1. Grant remains unchanged (signed, offline-verifiable)
2. Lease expires (short-lived proofs of current validity)
3. Bob comes back online
4. Bob requests fresh lease
5. Alice's system auto-renews (depending on policy)
5. Access restored

Alice switches infrastructure providers:
1. Alice's identity (Peer ID) doesn't change
2. Alice's relationships (with Bob) don't change
3. Alice's grants (to Bob) don't change
4. Only the rendezvous server changes
5. Bob's phone automatically finds Alice's reachability at new server
6. Everything continues working

**Key insight:** The infrastructure is replaceable. The relationships are not.

---

Every time you want to reach your own devices from outside your home, you have to choose between exposing them to the internet or renting a company's account to coordinate them. Grid Network is a cryptographic protocol that makes the coordination layer portable. Your identity and your relationships belong to you, not to a vendor. The result is private connectivity that behaves like email: anyone can run the infrastructure, anyone can switch providers, and no company gets to decide whether your network exists.

---

Grid Network makes private connectivity portable. Your devices, your identities, your relationships — owned by you, not rented from a company.

————-

Why Grid Network matters for projects like Immich, Jellyfin, Home Assistant, Nextcloud

The problem every self-hosted app eventually hits

Imagine you're building Immich. You're a photo app. Your job is photos: face recognition, albums, sharing, mobile sync, ML tagging. That's a full-time problem on its own.

Then one day a user says: "I want to access my photos from my phone when I'm not at home."

Now you have to answer a question that has nothing to do with photos:

· How does the phone find the server? The IP changes. The router blocks inbound traffic. The user is on CGNAT.
· How do we authenticate the phone? An account? A device token? A QR code?
· How do we authorize it? Does everyone in the family have the same access? Can a phone upload but not delete?
· What if the user's server goes down for a week? Do we cache the last known location?
· What if the user changes ISPs? Does the pairing survive?
· How do we handle NAT traversal?
· What if the network blocks peer-to-peer? Do we need a relay? Who runs it?
· How do we encrypt the traffic? Do we use a TLS certificate we can't have? Do we build our own?

Every one of these questions is a real, hard problem. Every one of them has a different answer depending on who's asking. And every one of them is completely orthogonal to "how should photos be organized."

This is the moment most self-hosted projects start making bad decisions.

The three bad decisions every project makes

Option 1: Use a central account system. "Just sign up for our cloud, and we'll handle connectivity through our servers." Now you're operating a cloud service. You're responsible for uptime, for user data, for abuse, for GDPR, for support. Congratulations — you've stopped being a photo app and become an infrastructure company. This is what Immich's paid cloud tier does, and it's a real burden that most projects can't afford.

Option 2: Tell users to run Tailscale. "Just install Tailscale and point the app at the local IP." This works, technically. But now every user of your app has to know what Tailscale is, has to make an account with a company, has to install a second piece of software, and has to understand that the app only works if that other thing is running. It's a support burden and an adoption barrier, and it makes your app's documentation depend on a third party you don't control.

Option 3: Roll your own. "We'll build a custom tunnel between the mobile app and the server." This is what a lot of projects attempt, and it's the worst option. You end up reimplementing identity, authorization, discovery, NAT traversal, relays, revocation, and every edge case, badly, with a small team, and you ship security bugs because you're a photo app team, not a networking team.

Every self-hosted app eventually picks one of these three, and all three are bad for different reasons.

What Grid Network changes

Grid Network is a protocol that lets an app say: "I don't need to solve this. Somebody else already did."

Instead of the app building or renting connectivity infrastructure, the app talks to a local Grid Network agent running on the user's device. The agent handles:

· Identity — who is this user, who is this device?
· Pairing — how did this phone first connect to this server?
· Discovery — where is the server right now?
· NAT traversal — how do we get through the router?
· Relay fallback — what if direct connection fails?
· Authorization — is this phone allowed to upload? To delete?
· Revocation — what if the user loses this phone?
· Freshness — is the authorization still current?

The app asks the agent one question: "Give me a connection to Alice's Immich server." The agent answers with a local URL. The app treats that URL like any other local service. It doesn't know or care whether the connection is going over LAN, direct internet, or a relay.

This means the app doesn't have to:

· Know about NAT. The agent handles it.
· Know about relays. The agent handles it.
· Know about certificates. The agent handles mutual authentication.
· Know about pairing. The agent handles the QR code / code exchange.
· Know about revocation. The agent handles it.
· Know about offline state. The agent handles leases.
· Know about key rotation. The agent handles it.

The app just uses a URL. That's it.

Why this matters more than it sounds

The immediate benefit is that apps get a whole category of functionality for free. But there's a larger structural benefit that's worth naming.

Right now, every self-hosted app reinvents the same connectivity layer, badly. Immich has its own sharing. Jellyfin has its own remote access. Home Assistant has its own Nabu Casa cloud. Nextcloud has its own federation. Syncthing has its own relay infrastructure. Paperless, PhotoPrism, Vaultwarden, Gitea, and dozens of others each have a partial answer to "how do I let users reach this remotely."

Every one of these is a different implementation of the same concepts:

· Identity
· Pairing
· Authorization
· Discovery
· NAT traversal
· Relay
· Revocation

And every one of them is a separate attack surface, a separate maintenance burden, a separate documentation problem, and a separate support queue.

Grid Network says: this is a shared problem. It should have one shared answer. The app should consume the shared answer, not reinvent it.

The analogy is to what happened with TLS. Twenty years ago, every app built its own encryption. Some used SSL, some used a custom protocol, some used nothing. Today, every app links against a TLS library and gets the same audited, correct implementation for free. Nobody writes their own crypto anymore, and the whole ecosystem is more secure as a result.

Grid Network wants to do for device identity and connectivity what TLS did for transport security. It's a shared, audited, correct primitive that apps consume instead of reinventing.

The specific advantages for a project like Immich

Concretely, here's what Immich gets from adopting Grid Network instead of building its own:

No cloud dependency. Immich doesn't have to run a service to make remote access work. Users install a Grid Network agent, pair their phone, and the phone reaches the server. Immich never sees a byte of coordination traffic.

No account system. Immich doesn't have to manage user accounts at the network layer. The Grid Network agent handles identity. Immich can still have its own user accounts for the application — Alice vs. Bob vs. Guest — but not for the network. Those are different problems and separating them is a good thing.

No NAT traversal code. This is a huge one. NAT traversal is genuinely hard: STUN, ICE, hole punching, TURN fallback, IPv6 reachability, CGNAT handling, symmetric NAT detection, port prediction. Every app that tries this either does it wrong or invests a huge amount of engineering. Immich gets it for free.

No relay infrastructure. If direct connectivity fails, the Grid Network agent falls back to a relay. Immich doesn't have to run one.

No QR code / pairing protocol. Pairing a phone with a server is a subtle cryptographic problem — you need a PAKE, you need to prevent man-in-the-middle, you need to bind the pairing to the actual identities being paired, you need rate limiting. The Grid Network agent handles this.

No revocation. If Alice loses her phone, she revokes the phone's authorization. Immich doesn't have to implement this.

No key rotation. If the server's identity key is compromised, the user rotates it. Immich doesn't have to implement this.

No offline-state handling. If the phone is offline for a week, the Grid Network agent handles whether the authorization is still valid. Immich just sees "connection available" or "connection refused."

No cross-platform complexity. The Grid Network agent has native support for iOS, Android, Linux, macOS, Windows. Immich's mobile app doesn't have to write connectivity code for each platform.

No security review burden for connectivity. The Grid Network protocol is a single, audited, versioned specification. Immich doesn't have to defend its own connectivity code against review — there isn't any.

No documentation burden. "Install Grid Network agent, scan this QR code, done." That's the entire remote access documentation for Immich.

That's a large amount of work Immich doesn't have to do.

The specific advantages for a project like Jellyfin

Jellyfin has a slightly different problem, and it's worth naming because it clarifies what Grid Network actually provides.

Jellyfin is a media streaming server. Its users want to watch movies and shows from wherever they are: home, work, hotel, parents' house. Jellyfin's security model involves identifying users, granting them access to libraries, and streaming media to them over HTTP.

Right now, Jellyfin's remote access story is: "the user has to set up port forwarding, or use a reverse proxy, or install a VPN." None of these are Jellyfin's job. All of them are user-facing friction.

With Grid Network:

· The user installs a Grid Network agent on the Jellyfin server and on the client.
· The user pairs them.
· The Jellyfin client sees the server as a local service.
· Streaming just works, from anywhere.

But there's a subtlety: Jellyfin's application-level authorization — who can see which libraries, who can admin the server, who can add plugins — remains Jellyfin's problem. Grid Network provides network-level identity and authorization. Jellyfin provides application-level authorization. Both are needed, and they're cleanly separated.

This separation is important because it means:

· Jellyfin doesn't have to give up its user model.
· Jellyfin doesn't have to trust the Grid Network agent's authorization for application decisions.
· Jellyfin can use the Grid Network identity as one input among many.

The Grid Network agent says "this connection is from a device that is cryptographically authenticated as Alice's phone." Jellyfin decides "Alice's phone is allowed to stream from the Kids library but not the Horror library." Two different problems, two different layers, no confusion.

The general pattern

The general pattern is this: every self-hosted app has the same list of hard connectivity problems, and none of them are the app's actual job.

The app should be excellent at its domain: photos, media, notes, files, home automation, whatever. It should not be excellent at NAT traversal, key management, relay infrastructure, or offline authorization. Those are solved problems that belong in a shared layer.

Grid Network is the shared layer.

Once an app integrates with Grid Network, it stops carrying connectivity as a burden. It gets:

· Remote access that works out of the box.
· Pairing UX that users actually understand.
· Revocation that actually works.
· Offline state that behaves correctly.
· Cross-platform support for free.
· A shared security model that someone else audits.

And it gives up nothing. The app retains its own user model, its own authorization decisions, its own data, its own service. Grid Network only handles the parts that aren't the app's responsibility.

Think about what HTTP did for the web. Before HTTP, every application built its own protocol for retrieving documents. After HTTP, applications got a shared, universal protocol, and they focused on what made them different.

Think about what TLS did for encryption. Before TLS, every application built its own crypto. After TLS, applications got a shared, audited primitive, and they focused on what made them different.

Grid Network wants to be that for device identity and connectivity. A single shared primitive that every self-hosted app can consume, so that they can spend their engineering effort on the parts of their app that users actually care about.

If it works, a small open-source project in 2028 should be able to say: "remote access works, we use Grid Network for that" — the same way a small project today says "encryption works, we use TLS for that."

That's the win. Not just for users, who get better remote access from more apps. But for developers, who get to stop solving the same problem over and over.

---

How commercial projects benefit — the "we offloaded SSO, why not this too" argument

The self-hosted story is where Grid Network starts, but the commercial story is where it gets interesting. Because commercial projects have already shown they're willing to offload a whole category of functionality to a third party — and they did it for exactly the same reasons that make Grid Network useful.

The precedent: how commercial apps offloaded sign-on

If you look at what happened to authentication over the last 15 years, it's a story of progressive delegation.

Phase 1 — roll your own. Every app built its own username/password system. Custom hashing, custom password reset, custom session management, custom password policies, custom everything. This was a support nightmare, a security nightmare, and duplicated across every product in the industry.

Phase 2 — use a framework. Apps started using Django's auth, Rails' Devise, Spring Security, passport.js. This was better — you still had your own user database, but at least the crypto was handled by people who knew what they were doing. But you still owned the account, the passwords, the resets, the policy, the compliance.

Phase 3 — offload to an identity provider. Auth0, Okta, Firebase Auth, Cognito, Clerk, Supabase Auth, AWS IAM. The app no longer stores passwords, doesn't handle resets, doesn't manage MFA, doesn't worry about compliance. The app calls an IdP, gets a token, and treats "who is this user" as a solved problem.

Phase 4 — federate to third parties. "Sign in with Google," "Sign in with GitHub," "Sign in with Apple." Now the app doesn't even manage the identity provider — it delegates to a provider the user probably already has an account with. The app gets a token that says "this is [email protected], verified by Google."

The overall trend is unmistakable: every commercial app has progressively decided that user identity is not their problem. They don't want to store passwords. They don't want to manage MFA. They don't want to handle account recovery. They don't want to be the authority on "who is this person."

They've offloaded it because it's expensive, risky, and completely orthogonal to what makes the app valuable.

The same argument applies to Grid Network

Grid Network says: the same thing should happen for device identity, network authorization, and reachability.

Today, commercial apps handle this themselves. A SaaS file-sharing product builds its own device-approval system. A commercial IoT platform builds its own NAT traversal. A remote-desktop product builds its own relay infrastructure. An on-prem enterprise tool builds its own device trust model.

Every one of them is duplicating the same work, badly, and paying for it in engineering, support, and security.

Grid Network says: this is a shared layer. Offload it.

What commercial projects actually gain

1. They stop being network infrastructure companies

A commercial photo-sharing product has to build or buy:

· Device pairing UX
· Device identity and authentication
· Access control between devices
· NAT traversal
· Relay infrastructure
· Revocation when a device is lost
· Offline-state handling
· Cross-platform support for mobile, desktop, and web

None of this is photography. None of it is a competitive advantage. All of it is a cost center.

When they adopt Grid Network, all of that is handled by the Grid Network agent. The app calls Grid Network.connect() and gets a local URL. It doesn't know or care how the connection was established.

The engineering savings are large and immediate.

2. They gain portability of trust relationships

This is subtle but commercially important.

Right now, if a company wants to let employees access internal resources, they build a device trust model. When an employee leaves, they revoke access. When the company switches VPN vendors, they migrate or rebuild all of it.

With Grid Network, the device identity and relationship are independent of the vendor. If the company switches from one Grid Network provider to another — or from commercial to self-hosted — the relationships carry forward. Employee offboarding still revokes the right things. New employee onboarding still establishes the right things. The underlying trust graph doesn't have to be rebuilt just because the infrastructure vendor changed.

For enterprises, this is a real strategic advantage: they can negotiate vendor contracts without the vendor's lock-in being the basis of the negotiation.

3. They gain a credible story for BYOD, IoT, and edge

Modern enterprises have a device sprawl problem. Employees' phones, contractors' laptops, IoT devices, edge sensors, remote sites, partner networks. Every one of these is a connectivity problem with a device identity problem underneath it.

Today, most enterprises handle this with:

· MDM for managed devices.
· An identity provider for users.
· A VPN for network access.
· Custom integrations for edge cases.

Grid Network gives them a unified model for all of these that's independent of the vendor and works across the entire device population. A contractor's phone can be paired to a specific service and only that service. An edge sensor can be paired to its gateway. An executive's laptop can be paired to the internal wiki. All with the same protocol, all with the same revocation model, all with the same offline semantics.

This is a meaningful improvement over the current patchwork.

4. They gain a shared story with open-source and self-hosted worlds

Commercial SaaS products and self-hosted projects often serve the same customers. Someone uses Nextcloud at home and Dropbox at work. Someone runs Jellyfin at home and uses a commercial streaming product for work-related media.

If both the commercial product and the open-source alternative speak the same Grid Network protocol, the user's device relationships are portable between them. A user's phone can be authorized to their home Immich server and to a commercial photo-sharing product they pay for, without the two systems having to coordinate.

This is directly analogous to what happened with "Sign in with Google." A commercial app got the benefit of every user who already had a Google account, without having to build its own identity system for those users.

Grid Network gives commercial products the benefit of every user who already has a Grid Network identity — from their home server, their NAS, their phone, whatever. The commercial product doesn't have to be the origin of the identity; it just has to accept it.

5. They gain enterprise delegation

This is where it gets commercially interesting for large vendors.

A commercial product that ships Grid Network support can say to its enterprise customers: "Device identity and authorization are handled by the Grid Network protocol. Your existing identity infrastructure — Okta, Entra, your MDM — plugs into this at the policy layer. We don't store your device graph; you do. We don't decide who's authorized; you do."

That's a very strong sales pitch in an enterprise market that has become allergic to vendor lock-in and data residency problems. It's the same reason enterprises demand SAML and SCIM support: they want identity to live in their system, not the vendor's.

Grid Network extends that demand from user identity to device identity, which enterprises have wanted for years and haven't had a portable protocol for.

6. They gain a real answer to "what happens if you go out of business?"

Commercial customers, especially enterprise ones, ask this question seriously. "If your company shuts down, what happens to our data? Our devices? Our relationships?"

For most SaaS products, the honest answer is: "You lose everything. You migrate to a new product and start over."

With Grid Network, the honest answer is: "Your device identities, your relationships, and your authorization grants are held by your devices. If we shut down, you plug into a different Grid Network provider and everything keeps working. You migrate your application data separately, but the trust graph is yours."

This is a genuinely stronger answer, and it's the kind of answer that wins enterprise deals in regulated industries.

The commercial framing

You offloaded user authentication to Auth0, Okta, or Google. Why are you still building device authentication, NAT traversal, and revocation infrastructure yourself?

Grid Network is the same story, applied to a problem you've been stuck with. Your app calls a local Grid Network agent, gets an authorized connection, and never thinks about keys, relays, or pairing again.

Your users get remote access that works out of the box. Your engineering team stops maintaining network plumbing. Your enterprise customers get portability of device trust that they've been asking for.

And when you need to sell to the Fortune 500, you can say: "Your identity infrastructure stays yours. We don't own your device graph. We just make it work."

What a commercial vendor actually has to build

Not much. The commercial vendor has to:

1. Install or bundle the Grid Network agent with their app (or provide installation instructions).
2. Integrate with the Grid Network agent's local API — the Grid Network.connect() call.
3. Optionally, expose Grid Network identity to their own application-level authorization (so that "Alice's phone" from the Grid Network layer can be used in their user model).
4. Optionally, provide a service binding in their identity document, so the Grid Network layer knows how their service is identified.

That's it. A few hundred lines of integration code, and the vendor gets:

· Remote access that works from anywhere.
· Pairing UX they didn't build.
· Revocation they didn't build.
· Offline-state handling they didn't build.
· Cross-platform support they didn't build.
· A trust-portability story they couldn't build alone.
· An enterprise sales narrative about not owning their customers' device graph.

The economics are stark. Building this from scratch costs millions and takes years. Adopting Grid Network costs weeks and delivers the same functionality — better, actually, because it's protocol-level rather than product-level.

1. The immediate engineering savings. "You stop writing NAT traversal code, relay code, pairing code, revocation code. That's a team you don't have to hire."

2. The strategic answer to lock-in anxiety. "Your customers stop worrying about whether you'll exist in five years. Their trust graph is portable. You compete on quality, not on lock-in."

3. The enterprise sales story. "You can tell CISOs: your device identities live with you, not with us. We're a conduit, not a chokepoint."

Those three things, together, are a compelling case for a commercial product to adopt Grid Network as a shared layer — even if they have the resources to build something themselves. Because the build-versus-buy calculation tilts heavily toward "share the protocol and compete on top of it."

The analogy to make explicit

The pattern is exactly what happened with TLS. Twenty years ago, every commercial product built its own crypto. They built their own key exchange, their own cipher suites, their own certificate validation. Every vendor had a security team whose job was to reimplement SSL.

Then the industry converged on TLS. Not because anyone was forced to, but because building it yourself was obviously worse. The vendors that adopted TLS early got to market faster, were more secure, and could compete on application features instead of crypto implementations.

Grid Network is the same argument for device identity and connectivity. A commercial vendor that adopts Grid Network is doing what a commercial vendor in 2005 did when they adopted TLS: taking a shared, audited primitive and moving their engineering effort to the parts of their product that customers actually pay for.

The pitch to commercial projects is: you already offloaded sign-on. Offload this too. It's the same calculation.
