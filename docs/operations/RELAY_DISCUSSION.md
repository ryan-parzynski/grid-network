261004-notdns relay discussion 
Absolutely. I’d encapsulate the discussion as a future protocol extension/design concept, not fold it into v0.6.1. The key is preserving the distinction between basic relay service, relay capabilities, and a future privacy transport.

Relay Capability, Path Selection & Privacy Extension

Status: Future extension / architectural concept
Scope: Relay infrastructure, relay capability advertisement, path selection, and optional privacy transport
Relationship to v0.6: No changes to the v0.6 kernel are implied by this document.

1. Purpose

The protocol’s relay architecture should scale from a small self-hosted device such as a Raspberry Pi to high-capacity bare-metal infrastructure without making hardware class part of the protocol’s fundamental semantics.

A relay is infrastructure for forwarding traffic when a direct path is unavailable or undesirable. It is not an identity authority, authorization authority, or ownership authority.

Relay selection should therefore be based primarily on advertised capabilities, operational limits, policy, and current availability, rather than on the physical hardware running the relay.

The application should request connectivity properties rather than select a specific relay.

2. Relay as a Capability Provider

A relay may advertise properties including:

* maximum concurrent sessions
* aggregate bandwidth
* maximum per-session bandwidth
* maximum bytes per session
* maximum aggregate or periodic transfer
* maximum connection lifetime
* supported transports
* IPv4/IPv6 availability
* current or estimated utilization
* geographic/region metadata
* latency characteristics
* availability characteristics
* supported relay modes
* privacy-related capabilities
* operator access policy

Hardware characteristics such as CPU architecture, CPU count, or RAM SHOULD NOT be fundamental protocol requirements. They may exist as operational metadata, but clients should normally reason about the capabilities that result from the hardware.

A Raspberry Pi and a bare-metal server therefore implement the same relay protocol while advertising very different capacity envelopes.

3. Example Capability Classes

Implementations may define profiles such as:

BASIC

Ordinary encrypted forwarding with resource limits.

HIGH_CAPACITY

Optimized for high aggregate bandwidth and large numbers of concurrent sessions.

LOW_LATENCY

Optimized for path latency rather than maximum throughput.

LONG_LIVED

Supports long-duration forwarding sessions.

COMMUNITY

Operator-volunteered infrastructure with explicitly declared access and resource policies.

PRIVACY

Supports additional privacy-oriented forwarding capabilities.

These profiles are descriptive capability groupings rather than separate protocol architectures.

4. Relay Operational State

Static relay capacity is insufficient for good path selection.

A relay may expose current operational state such as:

load {
    active_sessions
    utilization
    available_bandwidth_bps
}

This information may be ephemeral and should not be treated as identity or authorization state.

For example:

Relay A:
    capacity:       100 sessions
    active:          97
    available:        3
Relay B:
    capacity:     10,000 sessions
    active:           4
    available:     9,996

A client can consequently prefer Relay B without requiring a centralized load balancer.

5. Path Requirements

Applications or local agents should eventually be able to express connectivity requirements rather than selecting relay infrastructure directly.

Conceptual example:

path_requirements {
    direct: preferred
    relay: permitted
    min_bandwidth_bps: 20000000
    max_latency_ms: 100
    max_hops: 3
    ipv6: preferred
    privacy_level: 0
    minimum_path_lifetime: 2h
}

The local agent evaluates available paths and selects one satisfying the applicable requirements.

A possible decision sequence is:

1. Attempt direct connectivity.
2. If direct connectivity fails, evaluate relay paths.
3. Filter candidates by hard requirements.
4. Rank remaining paths by preferences.
5. Establish the selected path.
6. Fall back or migrate if the path becomes unsuitable.

The application should not need to know whether the resulting connection uses:

application → direct peer

or:

application → relay → peer

6. Relay Authority Boundary

The relay remains outside the identity and authorization authority model.

A relay may enforce:

* ticket validity
* ticket expiration
* byte limits
* bandwidth limits
* session lifetime
* connection limits
* operator resource policy

A relay MUST NOT thereby acquire authority to:

* create identities
* grant application capabilities
* establish relationships
* modify authorization
* become an identity authority
* redefine ownership

The existing RelayTicket mechanism remains the appropriate foundation for authorized forwarding.

7. End-to-End Encryption

The preferred relay model is forwarding of traffic that remains cryptographically protected between the communicating endpoints.

Conceptually:

Endpoint A
    │
    │ end-to-end encrypted traffic
    ▼
Relay
    │
    │ forwarded encrypted traffic
    ▼
Endpoint B

The relay therefore does not need to inspect application payloads.

A relay may know enough metadata to perform forwarding, accounting, and enforcement, but the protocol should avoid making relay decryption part of the basic model.

This keeps the relay replaceable and reduces the trust placed in relay operators.

8. Privacy vs. Anonymity

Ordinary relaying provides endpoint privacy, not necessarily anonymity.

For example, a destination may see the relay’s network address rather than the source endpoint’s address.

However, the relay itself may still observe:

source → relay → destination

A stronger anonymity property requires a separate multi-hop privacy mechanism.

Therefore:

Relay forwarding MUST NOT be described as providing anonymity unless a specific privacy transport establishes such a property.

9. Future Onion/Privacy Transport

A future extension could provide optional multi-hop privacy transport:

Endpoint A
    │
    ▼
Relay A
    │
    ▼
Relay B
    │
    ▼
Relay C
    │
    ▼
Endpoint B

With appropriate layered encryption, each intermediate relay could learn only the information required for its hop.

This extension could eventually address:

* multi-hop circuits
* layered encryption
* relay selection
* entry/exit separation
* circuit rotation
* traffic padding
* timing resistance
* privacy-oriented path requirements
* relay diversity

This should be treated as a distinct transport/privacy extension rather than being implicitly promised by ordinary relay operation.

10. Privacy Claims and Attestation

Relay capability and operator policy must remain distinct.

For example:

Capability:
    supports onion forwarding
Operator policy:
    claims not to retain connection metadata
Attestation:
    an independent mechanism verifies a particular property

A relay MUST NOT acquire a cryptographic “anonymous” status merely by self-declaring that it keeps no logs.

This leaves room for future independent verification, enterprise policy, or privacy certification without introducing a mandatory central authority into the protocol.

11. Geography and Network Metadata

Relays may advertise network metadata such as:

region
country
network/ASN
IPv4 availability
IPv6 availability

Such information is locator and selection metadata, not identity authority.

A declared geographic region MUST NOT by itself be interpreted as a cryptographic proof of physical location.

12. Economic and Operator Policy

A relay may eventually advertise policies such as:

access:
    public
    relationship-required
    operator-approved
contribution:
    free
    paid
    reciprocal

Payment, accounting, or marketplace mechanisms SHOULD remain outside the protocol kernel.

The core protocol only needs to express the applicable service or access requirement.

This permits future commercial relay networks without making commercial operation a prerequisite for the protocol.

13. Scaling Model

The intended progression is:

                    Relay capacity
                         ▲
                         │
   Raspberry Pi ─────────┼───────── Bare-metal cloud
   home server            │          10 Gbps+
   NAS                     │          100k sessions
   router                  │
                           │
                 same relay protocol

The protocol does not need separate architectures for different scales.

A small operator can contribute modest forwarding capacity, while a professional operator can provide high-capacity infrastructure.

14. Architectural Principle

The important abstraction is:

Applications request connectivity properties; the mesh selects a path that satisfies them.

This separates application intent from network implementation.

An application can request:

low latency
minimum bandwidth
direct preferred
relay permitted
privacy required
maximum path length
minimum path lifetime

without knowing which relay, network, transport, or physical server ultimately provides the connection.

15. Relationship to the Core Protocol

This design should remain outside the v0.6.1 architectural freeze.

The existing kernel requires only the fundamental concepts:

Identity
Authorization
Reachability
Transport
Relay

Future work may add:

Relay capability advertisement
Path requirements
Dynamic relay load information
Path selection
Multi-hop privacy transport
Onion routing
Privacy attestations
Economic/operator policies

These should be layered onto the existing authority model rather than changing the meaning of identity, relationship, authorization, or relay authority.

16. Design Goal

The resulting system should allow the same open protocol to operate across:

* a Raspberry Pi volunteered by an individual
* a home NAS
* a router
* a community relay
* a VPS
* a regional relay operator
* high-capacity bare-metal infrastructure

without requiring the protocol to know or care which class of hardware is involved.

The relay is a replaceable connectivity resource.

Identity remains with the endpoints.
Authorization remains with the principals.
The application remains independent of the path.
The network chooses the path according to declared requirements and available capabilities.

This is a good candidate for a future RELAY.md / PATH_SELECTION.md design document rather than adding substantial machinery to the core spec now.