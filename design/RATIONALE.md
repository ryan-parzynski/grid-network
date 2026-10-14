# Grid Network — Design Rationale

**Revision:** 2.1
**Protocol version:** v0.6.2

This document is non-normative. It explains why the protocol is designed
the way it is. Where this document and the Protocol Specification
conflict, the Protocol Specification governs.

---

## 1. Purpose and reading guide

This document serves three readers.

A **reader evaluating the protocol** wants to know what problem it
solves and why the design is worth adopting. Sections 2 through 5
address that.

A **reader deciding whether to build on the protocol** wants to know
what it replaces, what it costs to integrate, and what the design
assumes. Sections 6 and 7 address that.

A **reader looking for a specific answer** — does the protocol handle
X? what happens if Y? — will find edge cases in Section 8 and a
question index in Section 9.

The Protocol Specification defines what the protocol does. This
document defines why.

---

## 2. The problem

### 2.1 The wall

Every self-hosted service, personal server, home automation system, and
private application eventually reaches the same point:

> The service works. Now how do I reach it from somewhere else?

This is not a niche problem. It affects home media servers, photo
backup servers, file sharing, home automation controllers, network
attached storage, personal code repositories, backup infrastructure,
game servers, and development machines that a user wants to reach from
outside their home network.

The technology to solve this exists. The problem is institutional:
there is no vendor-neutral way to establish and maintain portable
identity and authorization across changing network conditions.

### 2.2 The three options today

**Option 1 — expose the service to the internet.**

Open a port on the home router, forward it to the server, and hope
nothing scans it.

This works until it doesn't. Firmware vulnerabilities are found
continuously. Services run with default credentials. Scanners
automatically catalog every open port. A single exposed service can
become a foothold for ransomware. Users discover months later that a
security camera feed or a file share has been publicly indexed.

The problem is not that exposure is inherently wrong. The problem is
that exposure is the easy path and the easy path has no safety rail.

**Option 2 — use a proprietary tunnel or mesh VPN.**

Sign up for a service. Log in. Add devices. Set access rules. The
service records the device graph, stores the policies, and becomes a
permanent authority over the user's network.

Products in this category are excellent. They work well, onboard
cleanly, and are cross-platform. The problem is not the product. The
problem is the relationship. The vendor owns the device graph, the
access policies, and the relationship data. If the vendor changes
terms, the user adapts or leaves. If the vendor is acquired, the user
is affected. If the vendor shuts down, the relationships disappear. The
underlying protocol is proprietary, so third parties cannot implement
it and competitors cannot interoperate with it.

The vendor is not the transport. The vendor is the authority.

**Option 3 — build it yourself.**

Run a VPN. Manage certificates. Handle dynamic DNS. Deal with carrier
NAT. Configure NAT traversal. Build or rent relay infrastructure.
Manage revocation. Handle offline state and reconnection.

This works for people who can do it, and for everyone else it is out
of reach. It requires sysadmin expertise, continuous maintenance, and
personal responsibility for security. One misconfiguration breaks
everything. There is no support when it fails. Even technical users
spend weekends debugging it.

### 2.3 The hidden cost

The obvious framing is that self-hosted connectivity is inconvenient.
The accurate framing is that the ability to reach one's own devices has
become a subscription.

A decade ago, reaching a home server meant opening a port or running a
VPN. Both were risky, awkward, and owned by the user. Today, the easy
path is a managed service. It works beautifully, and it means the user
no longer owns the network.

This is the same pattern seen in email, social media, and cloud
storage. Convenience becomes dependence. The pattern is not
conspiratorial; it is how products work. But it produces a specific
cost that is rarely named: the user does not own the relationships
between their own devices. A phone recognizes a home server because a
vendor's servers say so. If the vendor disappears, the recognition
disappears, not because the technology failed, but because the user
never owned it.

### 2.4 Why the obvious alternatives do not solve it

**"Use a commercial mesh VPN."** These are excellent products and
companies. The coordination server is the source of truth for the
device graph, so changes to terms, acquisition, feature removal, or
jurisdictional exit affect the user. Self-hosting the coordination
layer replaces one problem with another: the user is now operating
infrastructure. It also inherits an account-based identity model that
is awkward for applications that care about device identity rather than
user identity. The underlying protocol is proprietary, so competitors
cannot speak it.

**"Use a tunnel provider."** These let a local machine connect
outbound so no public IP is needed. They work well. But they make the
provider part of the access path. If the provider changes terms,
filters traffic, has an outage, or exits the business, the access path
goes with it.

**"Build your own VPN."** This works. It is also why self-hosted
connectivity has remained niche. Running a VPN requires expertise most
people do not have. For people who do have it, it means
reimplementing NAT traversal, relay fallback, revocation, and offline
state on their own.

### 2.5 The insight

The insight behind Grid Network:

> Connectivity is not a feature. It is infrastructure.

It should be a shared, auditable, portable primitive that any project
can consume, the same way projects consume TLS for encryption, HTTP for
requests, or DNS for resolution.

The reason this has not happened is that connectivity has three parts
that are each hard to standardize independently:

1. **Identity** — who is this device?
2. **Authorization** — what is it allowed to do?
3. **Reachability** — where is it right now?

The current landscape conflates them. When separated, each can be
standardized independently and each can survive changes in the others.

### 2.6 Why this is hard

A reasonable skeptic might say: "This sounds solved. WireGuard exists,
NAT traversal exists, relays exist. What is new?"

The answer is that all of the pieces exist and none of them coordinate.

Identity must survive location changes. Today, everything is identified
by where it is. Moving locations breaks identity.

Authorization must work offline. A device that is offline for months
should neither lose its identity nor keep access forever.

Intermediaries must be untrusted. A rendezvous server should not decide
authorization. A relay should not grant access.

No single party can be the authority. No central server can disappear
and end the network.

The result must be portable. Identity, relationships, and
authorizations survive any change of infrastructure provider.

Each constraint rules out an easy solution. What remains is more
complex than a naive design. But the complexity lives in the protocol,
not in the user experience.

---

## 3. The solution

### 3.1 What the protocol is

Grid Network is a control plane for identity, authorization, and
reachability above whatever networking already exists.

It is not a VPN. It is not a tunnel. It is not a replacement for
WireGuard, IPv6, or any transport. It is a layer that answers questions
about devices and permissions, using signed objects that participants
hold and verify themselves.

### 3.2 The three questions

**Who is this?** A cryptographic identity, controlled by the
participant. Implemented as a keypair, a signed identity document, and
an opaque random identifier. The identity is portable across
providers, survives device replacement, and survives network changes.

**What are they allowed to do?** A signed authorization, verified
locally. Implemented as a long-lived directional permission (a grant)
and a short-lived proof of current validity (a lease). Authorization
works offline, can be verified without contacting an authority, can be
revoked, and can be scoped to specific resources.

**Where can I find them?** An ephemeral reachability record, refreshed
as networks change. Implemented as a signed endpoint hint, published to
an untrusted rendezvous server, refreshed as networks change. The
record is untrusted, is ephemeral, and is replaceable without changing
identity.

Every question is answered by a signed object. No answer requires
contacting a central authority.

### 3.3 What the protocol is not

Not a decentralized VPN. A VPN is a transport. The protocol is a
control plane above transports.

Not a DNS replacement. DNS maps names to addresses. The protocol maps
identities to reachability, with authorization.

Not an anonymity network. Peers are identified. Metadata is visible to
infrastructure operators. This is intentional.

Not a blockchain. There is no global consensus, no ledger, no mining,
and no token.

Not a peer-to-peer file system. There is no distributed storage.

Not a company. There is no operator, no owner, and no central
authority.

Not a Tor, I2P, or Freenet replacement. Those provide anonymity through
routing. The protocol provides identity and authorization above
transports.

### 3.4 Five properties

**Identity is portable.** A device's identity is a cryptographic
keypair. It does not depend on any account, server, provider, vendor,
or central authority. It survives network changes, device replacement,
provider changes, infrastructure changes, and service outages.

**Authorization is local.** A device verifies authorization itself,
using state it holds. This enables offline authorization, partition-
tolerant authorization, authority-independent verification, and
immediate revocation.

**Reachability is ephemeral.** Where a device is does not form part of
its identity. Reachability is a hint, refreshed as networks change.
This enables seamless network transitions, IP changes, untrusted
rendezvous, and infrastructure portability.

**Infrastructure is untrusted.** Rendezvous servers, relays, and any
infrastructure can be operated by anyone, including parties the user
does not trust. No rendezvous server decides authorization. No relay
decrypts content. No infrastructure becomes an authority.

**The protocol is open.** No proprietary component. Any implementation
can speak to any other. This enables community implementations,
competitive relays, interoperable infrastructure, no vendor lock-in,
and independent security audits.

### 3.5 The core security invariant

The invariant that makes the design work:

> Given locally trusted anchors, authenticated protocol objects, known
> revocations, accepted chain state, and recorded observation history,
> a verifier must be able to deterministically establish the identity,
> authorization, validity, and freshness state of a peer as of its
> most recent observation, without contacting an authority.

The consequences:

- Rendezvous infrastructure cannot define identity.
- Relays cannot define authorization.
- DNS cannot define identity.
- IP addresses cannot define identity.
- WireGuard keys cannot by themselves define application-level
  authorization.
- Temporary pairing codes cannot become permanent credentials.

The invariant is what separates this protocol from every existing
system. It is the property that makes identity portable and
relationships durable.

### 3.6 How it works in practice

**Setup.** Alice installs a Grid agent on her home server. She pairs
her phone with the server using a QR code. The pairing produces a pair
of signed relationship assertions, one in each principal's identity
stream.

**Grant.** Alice issues a grant to a friend, Bob, permitting Bob's
phone to stream from her media server. The grant is valid for
`DEFAULT_LEASE_DURATION_MEDIA`. Bob's phone renews the lease
periodically.

**Access.** Bob's phone reaches Alice's server. Direct if possible,
via relay if not. The server verifies the grant and lease locally. No
contact with Alice is required for verification.

**Compromise.** Bob loses his phone. Alice revokes the grant. The
revocation is signed by her Identity Root, distributed through normal
protocol mechanisms, and cached by verifiers. Bob's phone can no longer
access anything, and Alice issues a new grant to her new phone.

**Offline.** Bob is offline for six months. The grant is unchanged.
The lease expires. When Bob returns online, he requests a fresh lease.
Depending on Alice's policy, the lease is auto-renewed. Access is
restored.

**Infrastructure change.** Alice changes rendezvous providers. Her
Peer ID is unchanged, her relationships are unchanged, her grants are
unchanged. Only the rendezvous server changes. Bob's phone finds her
reachability at the new server without any manual action.

The infrastructure is replaceable. The relationships are not.

---

## 4. Why this matters

### 4.1 The design is Linux, not a startup

A startup is designed to capture value. It has investors, a growth plan,
and an exit. Its success is measured by market share.

This protocol is not a startup. It is infrastructure, in the same sense
that Linux is infrastructure. Its success is measured by adoption, by
the number of applications and users who find it useful enough to build
on.

The distinction changes what success means. A startup succeeds by
dominating a market. Infrastructure succeeds by being adopted widely
enough to matter. A startup optimizes for growth and defensibility.
Infrastructure optimizes for openness and ease of use.

The protocol is optimized for the second model. It is free, the
objects are open, the identity is portable, and the design has no
mechanism that would allow a single entity to capture the network.

### 4.2 What the design makes portable

The protocol is not a system that connects devices. It is a system
that makes trust portable.

Every device that exists today has a set of relationships: with its
owner, with other devices, with services, with peers. Those
relationships are usually defined by the network the device is on. Move
the device to a different network, and the relationships break. Change
the network's provider, and the relationships break.

The protocol makes the relationships themselves durable and the network
replaceable. A device can move between networks, change providers, go
offline for months, and its relationships survive.

This is a property no widely-adopted system provides today. It is the
difference between "remote access works today" and "remote access will
still work in ten years, regardless of what happens to the vendors
involved."

### 4.3 What the design assumes

The design assumes:

- Peers periodically communicate to keep state fresh. Long disconnection
  degrades discovery.
- Rendezvous infrastructure remains available over the relevant
  timescale. Infrastructure churn over years degrades discovery for
  peers that have not communicated in the interim.
- Backups of key material are maintained and current. A stale backup
  may not chain to the current identity state.
- Clock skew between peers is bounded. Relative validity survives skew
  up to the lease duration; absolute validity does not.
- At least one transport is available that survives the deployment's
  network conditions. Conformant implementations must support a
  transport that survives UDP-blocking networks.

Each assumption is a design choice. Where an assumption does not hold,
the protocol's behavior is documented in the failure modes catalog.

---

## 5. The developer case

### 5.1 The insight for developers

Developers do not want to build connectivity. They want to build
applications.

Just as developers offload authentication, developers should be able to
offload connectivity.

### 5.2 What developers face today

Every application that wants remote access must solve:

1. Device pairing.
2. Device authentication.
3. Device discovery.
4. NAT traversal.
5. Relay fallback.
6. Revocation.
7. Offline state.
8. Cross-platform networking.

Each is a hard problem. Each has different answers depending on
context. Applications either build their own, use a proprietary VPN, or
give up on remote access.

### 5.3 The protocol as a dependency

The protocol is a shared dependency, like TLS or HTTP. An application
that wants remote access adds a local agent and calls one API.

    connection = grid.connect(
        peer_id = "peer:v1:bob_server",
        capability = "org.media.stream"
    )

The agent handles identity, authorization, reachability, NAT traversal,
and relay fallback. The application receives an authorized local
connection.

### 5.4 What the developer gains

The integration eliminates NAT traversal code, relay infrastructure,
pairing UI, revocation implementation, key management, and
cross-platform networking code. It reduces time-to-market and removes
the need for network specialists.

The integration improves security because the crypto is tested and
audited, revocation is built-in, and identity is portable.

### 5.5 Network versus application authorization

The protocol handles the network layer. The application handles the
application layer.

Network authorization asks whether a peer may connect. Application
authorization asks what a user may do once connected. Both layers are
required.

An example: the protocol verifies that Bob's phone holds a grant
permitting media streaming. The media application verifies that Bob's
user account has permission to view a specific library. If either
check fails, access is denied.

---

## 6. The contribution model

### 6.1 Three layers

The network is sustained by three layers of contribution.

**Users.** Operate on the network, publish reachability, forward
traffic through their devices, and build community.

**Operators.** Run relays and rendezvous servers, provide bandwidth
and capacity, and contribute to developer funding through a revenue
share.

**Maintainers.** Maintain the specification, conduct security audits,
produce test vectors, and support the community.

### 6.2 What users contribute

A user's home server publishes reachability, forwards traffic for other
peers when required, runs a local rendezvous cache, and attracts
ecosystem gravity. The free tier is fully functional; a user can earn
credits by running a local relay.

At a modest adoption rate, home relays contribute substantial
capacity. The specific capacity figures depend on the deployment mix.

### 6.3 What operators contribute

An operator invests in relay and rendezvous infrastructure, earns
revenue from paid tiers, contributes a fixed fraction to developer
funding, and may reinvest in capacity expansion.

The incentive is aligned: building a larger network earns more, and a
larger network attracts more users.

### 6.4 What maintainers do

Maintenance covers the specification, security audits, test vectors,
the RFC process, versioning, and community support.

### 6.5 The economic shape

The network grows in a cycle. More free users increase network value.
Higher network value attracts applications. Applications attract more
users. More users create operator opportunity. Better infrastructure
increases network value again.

Each layer funds the next.

### 6.6 The free tier is real

A free tier that is a loss leader is a free tier that will be removed.
The design treats free users as foundation, not funnel. They contribute
reachability, peer-to-peer efficiency, and local relays. Removing them
would reduce the value of the network for every paid user.

---

## 7. Edge cases and limits

### 7.1 Offline for an extended period

A device that has been offline for longer than `max_offline_tolerance`
is unauthorized on return. Access is restored when the issuer issues a
new lease, subject to the issuer's policy.

A device that has been offline for less than `max_offline_tolerance`
resumes operation on cached state. No online verification is required.

### 7.2 Lost device

A lost device with valid leases can access protected resources until
the issuer publishes a revocation and the revocation propagates. The
window is bounded by the propagation delay and the lease duration.

Revocation is the primary defense. Lease expiration is the secondary
defense.

### 7.3 Malicious rendezvous server

A rendezvous server can serve stale records, serve false records, deny
service, and observe query patterns.

A rendezvous server cannot forge grants, leases, identity documents,
or signatures. It cannot change authorization, impersonate a peer, or
decrypt content.

Mitigations: multiple rendezvous providers, relay fallback, cached
reachability, and distribution of queries across servers.

### 7.4 Malicious relay operator

A relay can observe packet size, source and destination identifiers,
and timestamp. It can drop traffic, inject traffic, or deny service.

A relay cannot decrypt content, forge tickets, impersonate either
party, or change authorization.

Mitigations: multiple relays, transport-level encryption, and the
option to accept the metadata tradeoff knowingly.

### 7.5 Clock skew

A verifier whose clock differs from the issuer's handles relative
validity correctly because the validity is measured from the verifier's
own observation. Absolute validity is vulnerable; the protocol uses
relative validity by default for leases.

The recommended mitigation for absolute timestamps is
`MAX_CLOCK_SKEW`.

### 7.6 Fork in a stream

Two objects at the same sequence with different chain hashes constitute
a fork. The stream enters `FORK_DETECTED` state. Authorization for the
stream is suspended until a `StreamResolution` object is accepted.

Fork resolution requires signatures from the authorities present in the
forked history. A fork whose signing keys are lost is unrecoverable
within the protocol.

### 7.7 Identity Root compromise

A compromised Identity Root allows the attacker to forge identity
documents, grants, and relationships. There is no in-band recovery.

Recovery is external and out-of-band. The principal contacts peers
who recognized the old identity, proves ownership by a mechanism agreed
outside the protocol, and re-establishes relationships under a new
principal.

Threshold recovery is a planned feature.

### 7.8 Partial network outage

Multiple rendezvous providers reduce the effect of a single provider's
outage. A verifier that cannot reach a provider queries another.

A verifier that cannot reach any provider uses cached state. Known
grants continue to work.

### 7.9 FAQ

**What happens if a device's clock is wrong?**
Relative-validity leases survive clock skew up to the lease duration.
Absolute timestamps do not.

**What happens if a device is lost?**
The issuer publishes a revocation. Access ends when the revocation
propagates or the lease expires, whichever is sooner.

**What happens if a rendezvous server disappears?**
A verifier queries another provider. If none is available, cached
state is used.

**What happens if a relay goes down?**
A verifier tries another endpoint, then another relay. If all fail,
the connection is unreachable. This is not an authorization failure.

**How is the Identity Root key changed?**
By publishing an `IdentityContinuity` object signed by both the old
and new roots.

**What happens if someone steals a phone?**
The issuer revokes the relevant grants. The attacker has a bounded
window of access, determined by revocation propagation and lease
duration.

**Can an operator see who accessed a server?**
The protocol does not log access at the network layer. Applications
may log at the application layer.

**Can a rendezvous server see traffic?**
No. A rendezvous server sees queries and record publications only.

**Can a relay see traffic?**
A relay sees packet size and timing. It does not see content.

**Are multiple devices per principal supported?**
Yes. Each device has its own device key. Grants are per-principal.

**How is a single device revoked?**
By removing it from `device_bindings` in the identity document and
revoking its device key.

**What happens if a grant issuer goes offline permanently?**
Existing leases continue to work until they expire. New leases cannot
be issued. Access is restored when the subject obtains a new grant
from a different authority.

**Can the protocol be used without trusting any operator?**
Yes. A deployment may run its own rendezvous servers and relays.

**Is the protocol an anonymity network?**
No. Peers are identified. Metadata is visible to infrastructure
operators.

---

## 8. Naming

The protocol is named Grid Network.

The name was chosen to be descriptive of a distributed, resilient
topology, uncollided with existing networking projects, memorable,
scalable across audiences, and aligned with the design's vision of
distributed infrastructure.

Earlier working names included a technical descriptive term, a
negation-based name, and several single-word candidates. Each was
rejected because it defined the project by what it was not, collided
with an existing project, or failed to communicate the design's
purpose. The final name is the one that survived those constraints.

---

## 9. What this document is not

This document is not a specification. Where it describes behavior, the
specification is the authority.

This document is not a roadmap. Work that is planned, deferred, or
unscheduled is described in the Roadmap.

This document is not an operator guide. Deployment, relay operation,
commercial tiers, and integration guidance are described in the
Operator Guide.

This document is not a security certification. It explains design
choices. It does not assert that the design has been verified against
any threat model beyond the one in the Protocol Specification.

This document is not affiliated with any operator, provider, or
organization.