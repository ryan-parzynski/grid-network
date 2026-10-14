# Grid Network — Deployment Guide

**Revision:** 2.1
**Protocol version:** v0.6.2

This document is non-normative. It describes how to deploy the protocol
in practice: how rendezvous servers are operated, how NAT traversal
proceeds, how paths are selected, and how a deployment migrates between
providers.

Where this document and the Protocol Specification conflict, the
Protocol Specification governs.

---

## 1. Deployment topologies

The protocol supports a range of topologies. Three are common.

**Solo.** One principal, one or more devices, no external relationships.
The devices are authorized by `device_bindings` in the principal's
identity document. No grants or leases are required within a single
principal. A rendezvous server may be used for reachability, or direct
connections may suffice on a local network.

**Household or small group.** A small number of principals, each with
several devices. Relationships are established by pairing. Grants flow
between principals as needed. A shared rendezvous provider or a
self-hosted one serves discovery.

**Organization.** A larger number of principals, with delegated
administration and broader authorization. Multiple authorization keys
per principal. Multiple rendezvous providers for redundancy.

The protocol does not distinguish these topologies at the wire level.
The distinction is operational.

---

## 2. Rendezvous operation

A rendezvous server stores ephemeral protocol state on behalf of peers.
It accepts reachability records, identity documents, and continuity
objects, and serves them on request.

### 2.1 What a rendezvous server stores

- Reachability records, with a TTL bounded by
  `DEFAULT_REACHABILITY_TTL`.
- Identity documents, updated when a peer publishes a new one.
- `IdentityContinuity` objects, retained so that verifiers can walk
  from an old anchor to the current one.

The server does not store grants, leases, relationships, or any other
authorization state. The server does not decide authorization.

### 2.2 Persistence

A rendezvous server should persist its state to durable storage. The
state is signed by its publishers; persistence is a convenience for
availability, not a trust mechanism.

If a rendezvous server loses its state, its peers republish. Peers
should detect server failure and republish to an alternative server.

### 2.3 Rate limiting

The rendezvous server should rate-limit:

- Publications per peer per interval.
- Lookups per requester per interval.
- Failed authentications per source per interval.

The rate limits are policy; the protocol does not define them. Defaults
are in `PARAMETERS.md`.

### 2.4 Federation

Federation between rendezvous servers is a `planned` feature. In the
current protocol version, a rendezvous server is a standalone store.
A peer that publishes to multiple servers maintains the publications
independently.

### 2.5 Availability

A rendezvous server may be unavailable for maintenance, failure, or
policy reasons. Peers should maintain a list of at least two rendezvous
servers in their `RendezvousManifest`. A peer whose list becomes empty
is undiscoverable until it publishes to an available server.

---

## 3. NAT traversal

NAT traversal is how two peers establish a direct connection when at
least one is behind a NAT.

### 3.1 Preference order

A verifier tries connection methods in the following order, stopping
at the first success.

1. Local network discovery (mDNS).
2. Direct connection using a routable address from the reachability
   record.
3. NAT traversal using a candidate exchange and hole-punching.
4. Relay.

The order reflects lower latency and lower cost. An implementation may
deviate if it has information that changes the tradeoffs.

### 3.2 Local network discovery

mDNS or an equivalent mechanism discovers peers on the local network.
Discovery is a hint, not an identity source. A peer discovered via mDNS
must still be verified against its identity document.

### 3.3 Direct connection

If the reachability record contains a routable address, the verifier
connects directly. Latency is bounded by geography. Encryption is
provided by the transport.

### 3.4 NAT traversal

The candidate exchange reveals each peer's NAT characteristics. The
peers attempt hole-punching. Success depends on the NAT type: full-cone
and port-restricted NATs succeed more often than symmetric NATs.

If hole-punching fails, the connection falls through to relay.

### 3.5 Relay fallback

The relay path is used when direct connection fails. Relay adds latency
and consumes relay capacity. A verifier should prefer relay endpoints
with higher priority but should not require any particular endpoint.

### 3.6 Networks that block UDP

Some networks block UDP entirely. A conformant implementation must
support at least one transport that survives such networks. TLS over
TCP port 443 is the recommended default. QUIC is an acceptable
alternative.

A deployment that uses only UDP-based transports will be unreachable on
UDP-blocking networks.

---

## 4. Path selection

A verifier selects a path among the available options. The selection
algorithm is implementation-defined, but the following properties are
required.

**Failure does not become denial.** A path failure is an availability
failure. It does not change authorization state.

**Alternatives are tried.** When a path fails, the verifier tries the
next. The order is implementation-defined.

**No silent downgrade.** A verifier should not accept a weaker
transport without explicit configuration.

**Multiple endpoints are supported.** The reachability record may list
several endpoints. The verifier treats each as an independent
candidate.

A deployment that needs deterministic behavior should configure an
explicit policy for endpoint preference.

---

## 5. Migrating between providers

A peer may change its rendezvous provider without changing identity,
relationships, or grants.

### 5.1 Migration steps

1. Establish an account or arrangement with the new provider.
2. Publish the peer's current identity document to the new provider.
3. Publish the peer's current reachability records to the new
   provider.
4. Update the peer's `RendezvousManifest` to include the new provider.
5. Wait for the manifest update to propagate to peers that need it.
6. Remove the old provider from the manifest.
7. Remove the peer's publications from the old provider.

### 5.2 What is unaffected

The peer's Peer ID is unchanged. Relationships are unchanged. Grants
are unchanged. Leases are unchanged. The device keys are unchanged.

### 5.3 What is affected

Peers that query the old provider will fail to find the peer after
publications are removed. They will succeed at the new provider once
the manifest update reaches them. During the transition, both providers
serve the peer.

### 5.4 Minimum overlap

The transition requires an overlap window long enough for the manifest
update to propagate. The window is bounded by the reachability TTL and
by the update rate of the peers' caches. A conservative window is
several times the reachability TTL.

---

## 6. Monitoring and diagnostics

An operator or administrator should monitor:

- Rendezvous query latency and success rate.
- Relay bandwidth utilization and rejection rate.
- Direct connection success rate.
- NAT traversal success rate by NAT type.
- Revocation propagation delay.
- Lease renewal success rate.

The protocol does not define a diagnostic interface. Implementations
may expose one; deployments may build one.

---

## 7. Security guidance

### 7.1 Identity Root protection

The Identity Root should be offline or hardware-protected. If the root
is lost, the principal's identity is frozen. If the root is
compromised, the principal is compromised.

For solo deployments where the root must remain online, use a
hardware-backed key if available. Document the procedure for rotating
the root.

### 7.2 Authorization Key separation

Each administrator should have their own Authorization Key. A
compromised key affects only the grants that key issued. Revoking the
key does not affect grants issued by other keys.

### 7.3 Device Key protection

A device key is bound to one device. If the device is lost, the key is
revoked and the device is removed from the identity document.

### 7.4 Backup

Back up the Identity Root and the Authorization Keys. A backup is only
useful if it chains to the current identity state. A stale backup
requires recovery through the current state, or re-pairing.

Store backups separately from the running keys. A backup co-located
with the key does not protect against compromise.

### 7.5 Clock

Keep the system clock within `MAX_CLOCK_SKEW` of a reliable source.
Relative validity survives larger skew, but absolute timestamps in
grants do not.

### 7.6 State corruption

Use atomic writes and checksums for persisted state. If the state is
corrupted, re-establish trust from scratch. A corrupted verifier that
continues to operate may authorize incorrectly.

---

## 8. Failure response

### 8.1 Rendezvous server failure

Peers detect failure and republish to an alternative server. Verifiers
query alternatives. If no alternative is available, cached state is
used.

### 8.2 Relay failure

Peers with active relay sessions lose connectivity. Verifiers retry
via alternatives. If no alternative is available, the connection is
unreachable. Authorization state is unchanged.

### 8.3 Provider exit

A provider that exits the business stops serving. Peers migrate to
another provider. Relationships, grants, and leases are unaffected.

### 8.4 Identity Root compromise

The principal is compromised. Recovery is external. The principal
contacts peers who recognized the old identity and re-establishes
relationships under a new principal.

### 8.5 Device compromise

The compromised device key is revoked and the device is removed from
the identity document. Other devices of the same principal are
unaffected.

### 8.6 Authorization Key compromise

The compromised key is revoked by the identity root. Grants issued by
that key are affected per `effective_sequence`. Grants issued by other
keys are unaffected.

---

## 9. What deployment does not require

A deployment does not require:

- A specific rendezvous provider.
- A specific relay provider.
- A specific transport.
- A specific number of devices or principals.
- A specific clock source, beyond the accuracy needed for
  `MAX_CLOCK_SKEW`.
- A specific backup policy, though one is recommended.
- Registration with any authority.
- Payment to any entity, for the free tier.

A deployment that uses the free tier and runs its own rendezvous server
and relays has no external dependency beyond the network itself.