260920-01 V.01 Not DNS Design Document

# 260921-NotDNS Resolver

## Executive Summary: Resilient Mesh Rendezvous Project

## What We’re Building

NotDNS is an open protocol and local connectivity agent for privately locating and connecting authorized self-hosted application endpoints.

It helps a phone, laptop, or remote service reach a home server when:

- The server’s public IP changes.
- A phone moves between Wi-Fi and cellular.
- Devices are behind NAT or CGNAT.
- A coordinator becomes unavailable.
- A volunteer operator leaves the network.
- Direct connectivity fails and a relay is required.
- The application should access only one approved service rather than the entire LAN.

NotDNS is related to DNS because it resolves a stable service identity into a current connection path. However, it is not a replacement for DNS, a general VPN, an anonymity network, a public DHT, or an unrestricted proxy.

The system separates:

```text
What service is this?
Who is allowed to use it?
Where is it currently reachable?
How can the two endpoints connect?
What traffic is permitted?
```

Those responsibilities belong to different layers.

---

# Core Design Principle

> **Coordinators are replaceable infrastructure. Cryptographic identity, authorization, and signed state belong to the participating endpoints.**

A coordinator may store, replicate, cache, or return a record, but it does not become the ultimate authority merely because it hosts the database.

The system should remain useful when:

- One coordinator fails.
- Replicas are stale.
- Gossip is delayed.
- A volunteer stops operating an instance.
- A regional coordinator is overloaded.
- A public discovery service is unavailable.

The network should degrade gracefully rather than collapse around one homeserver or coordinator.

---

# Three Different Identities

The protocol must distinguish between **service identity**, **device identity**, and **service link**.

## Service identity

A stable cryptographic identity for an installed service.

Example:

```text
Alice’s home Immich installation
```

The service identity does not change when its IP address, port, hosting machine, or network changes.

It may be represented by an owner-controlled public key:

```text
service_identity = ed25519:immich-server-key
```

## Device identity

A stable cryptographic identity for one endpoint agent.

Examples:

```text
Alice’s home server agent
Bob’s iPhone agent
A VPS relay agent
A backup worker
```

Each device generates and stores its own keypair.

## Service link

A specific authorization relationship between devices and a service.

Examples:

```text
Bob’s phone → Alice’s Immich API
Alice’s phone → Alice’s Immich API
Backup worker → selected Immich endpoint
Remote agent → Jellyfin streaming capability
```

A single service can have multiple independent links:

```text
Alice’s Immich service
  ├── Alice phone → Immich API
  ├── Bob phone → Immich API
  ├── Backup service → upload API
  └── Remote admin device → administration capability
```

Revoking Bob’s phone must not change the stable Immich identity or affect Alice’s own link.

---

# Service-Link Policy

Authorization is expressed through a signed, service-specific policy:

```json
{
  "policy_type": "service-link-policy",
  "service_identity": "ed25519:immich-server-key",
  "service_link_id": "random-256-bit-link-id",
  "source_device": "ed25519:bob-phone-key",
  "destination_device": "ed25519:home-server-agent-key",
  "requested_capability": "immich-api",
  "transport": "tcp",
  "direction": "source-to-destination",
  "relay_allowed": true,
  "policy_generation": 42,
  "not_before": "2026-09-21T20:00:00Z",
  "expires_at": "2026-12-31T23:59:59Z",
  "signature": "owner-key-signature"
}
```

The policy determines:

- Which source device may connect.
- Which destination service may be reached.
- Which direction is allowed.
- Whether relays are permitted.
- Relay quotas and rate limits.
- The policy’s validity period.
- Which policy generation is current.

A valid device identity alone does not grant unrestricted access.

---

# Stable Identity Versus Temporary Reachability

## Stable identity and policy state

This answers:

```text
What is this service?
Who owns it?
Which devices are authorized?
Which coordinators are trusted?
What capabilities are permitted?
```

It changes infrequently and should be signed, exportable, and recoverable.

## Endpoint lease

This answers:

```text
Where can this service currently be reached?
```

An endpoint lease may contain:

- IPv4 and IPv6 candidates.
- UDP, TCP, or QUIC ports.
- NAT reachability hints.
- Transport capabilities.
- Relay availability.
- Publisher identity.
- Generation number.
- Issue time.
- Expiration time.
- Publisher signature.
- Recipient-encrypted endpoint data.

Endpoint leases are disposable soft state. They expire and are republished when the device wakes, changes network, or detects a new public endpoint.

A stable home server may use a longer lease, but no endpoint should remain valid indefinitely without renewal.

---

# Enrollment

A QR code must not contain a permanent shared transform key.

QR codes are easily copied, photographed, logged, or forwarded. Instead, the QR code contains:

```text
protocol: connect-v1
service_identity: ed25519:...
service_link_id: random-256-bit-id
owner_public_key: ed25519:...
initial_coordinators:
  - https://coord-a.example
  - https://coord-b.example
bootstrap_expiry: 2026-09-21T20:01:30Z
enrollment_capability: one-time-secret
```

Enrollment proceeds as follows:

```text
1. The owner displays a QR code.

2. The phone scans it.

3. The phone generates its own device keypair locally.

4. The phone proves possession of the one-time capability.

5. The owner or service approves the device.

6. The service issues a service-link policy.

7. The phone receives the signed coordinator manifest.

8. The one-time capability is consumed or expires.

9. Future access uses the device key, not the QR secret.
```

Each device is independently revocable.

---

# Coordinator Discovery Versus Endpoint Discovery

These are separate problems.

## Coordinator discovery

How does a device find infrastructure that can answer its lookup?

Sources include:

- QR bootstrap list.
- Cached signed coordinator manifest.
- Owner-provided recovery bundle.
- Self-hosted configuration.
- Optional future DHT pointer.
- Optional DNS or well-known bootstrap record.

## Endpoint discovery

How does an authorized device find the current path to a service?

Sources include:

- Local mDNS/DNS-SD.
- Cached endpoint lease.
- Authenticated coordinator lookup.
- Recipient-encrypted signed endpoint lease.
- Manually configured endpoint.
- User-owned reverse proxy or relay.

A public coordinator may be discoverable without being trusted to authorize access. Endpoint records remain signed, encrypted where appropriate, and policy-gated.

---

# Signed Coordinator Manifests

A service should not permanently depend on one coordinator URL.

The owner signs a coordinator-set manifest:

```json
{
  "record_type": "coordinator-set",
  "service_identity": "ed25519:immich-server-key",
  "generation": 43,
  "previous_manifest_hash": "sha256:...",
  "issued_at": "2026-09-21T20:00:00Z",
  "active_until": "2026-12-20T20:00:00Z",
  "recovery_until": "2027-09-21T20:00:00Z",
  "coordinators": [
    {
      "id": "coord-eu-1",
      "url": "https://eu1.example.net",
      "public_key": "ed25519:...",
      "roles": ["directory", "signal"],
      "priority": 20,
      "region_hint": "eu-west"
    },
    {
      "id": "coord-us-1",
      "url": "https://us1.example.net",
      "public_key": "ed25519:...",
      "roles": ["directory", "signal"],
      "priority": 10,
      "region_hint": "us-east"
    }
  ],
  "signature": "owner-signature"
}
```

Clients validate:

- Owner signature.
- Manifest generation.
- Previous-manifest lineage.
- Active or recovery expiration.
- Coordinator public keys.
- Declared coordinator roles.
- Service identity.

## Manifest lifetime

Use three states:

| State | Purpose | Suggested duration |
|---|---|---:|
| Active manifest | Normal coordinator selection | 30–90 days |
| Recovery manifest | Read-only recovery and recontact | 90–365 days |
| Owner recovery bundle | Offline restoration and key recovery | No automatic expiry |

An expired active manifest may be used in constrained recovery mode to contact listed coordinators and obtain a newer manifest. It must not silently authorize new enrollment or broaden policy.

If all listed coordinators disappear, the owner can restore the service using:

```text
Owner authority key
+ service identity
+ latest policy
+ coordinator manifest
+ recovery material
```

---

# Coordinator Resilience and Swarm Behavior

The system should not copy a Matrix-style model where one homeserver is the essential home of all active state.

A better model is:

```text
Service owner
    │
    ├── publication coordinator
    ├── selected replicas
    ├── cache coordinators
    └── recovery sources
```

## Coordinator roles

### Publication coordinator

Accepts authorized lease publications and enrollment operations.

### Replica coordinator

Stores signed copies of selected records and serves reads when the publication coordinator is unavailable.

### Cache coordinator

Fetches and caches records that users actually request.

### Bootstrap coordinator

Helps clients find current coordinator manifests.

### Relay coordinator

Issues relay tickets or helps agents find an approved relay.

A coordinator may perform multiple roles, but the roles should remain distinct in the protocol.

## No single point of failure

If the publication coordinator fails:

```text
- Existing direct connections continue.
- Clients try another coordinator in the signed manifest.
- Replicas serve recent valid leases.
- Devices publish to an available coordinator.
- The owner later removes the failed coordinator.
```

If every coordinator disappears temporarily:

```text
- Existing sessions continue.
- Local LAN discovery continues.
- Cached leases may work until expiry.
- Static or user-owned routes continue.
- The owner can restore infrastructure from recovery material.
```

Coordinator loss should cause degraded discovery, not loss of identity or ownership.

---

# Bounded Gossip and Anti-Entropy

The system can use swarm-like replication, but not unrestricted global gossip.

Coordinators exchange compact inventories:

```text
“I have service-link record X at generation 417.”
“I have record Y at generation 12.”
“I have no current record for Z.”
```

Peers then request only selected missing records.

Replication is constrained by:

- Maximum bytes per exchange.
- Maximum records per round.
- Maximum fetch depth.
- Maximum peer count.
- Namespace restrictions.
- Storage quotas.
- Bandwidth quotas.
- Expiration checks.
- Generation checks.
- Backoff after failure.
- No recursive uncontrolled fan-out.

Example:

```text
Regional exchange:
  max 1 MiB per minute
  max 1,000 inventory entries per round
  max 100 full-record fetches per round

Cross-region exchange:
  lower frequency
  lower bandwidth budget
  on-demand fetch for authorized live requests
```

Operators can choose:

- Which services they host.
- Which namespaces they replicate.
- Whether they accept new enrollment.
- Whether they operate read-only.
- Whether they provide relay services.
- Whether they accept cross-region traffic.
- When they are full or draining.

This gives the network swarm-like resilience without requiring every volunteer to store everything.

---

# Endpoint Records and Cryptography

The earlier XOR-obfuscation model is removed.

XOR is not meaningful confidentiality because the key may be shared with every QR recipient and cannot provide independent revocation.

Use authenticated encryption and signatures.

A lease envelope may look like:

```json
{
  "record_type": "endpoint-lease",
  "service_identity": "ed25519:immich-server-key",
  "service_link_id": "random-link-id",
  "publisher_device": "ed25519:home-server-agent-key",
  "generation": 417,
  "issued_at": "2026-09-21T20:00:00Z",
  "expires_at": "2026-09-21T20:30:00Z",
  "recipient": "ed25519:bob-phone-key",
  "ciphertext": "...",
  "signature": "publisher-signature"
}
```

The encrypted payload may contain:

```json
{
  "candidates": [
    {
      "address": "203.0.113.50",
      "port": 51820,
      "transport": "udp"
    },
    {
      "address": "2001:db8::50",
      "port": 443,
      "transport": "quic"
    }
  ],
  "service_identity": "ed25519:immich-server-key",
  "requested_capability": "immich-api",
  "relay_policy": "approved-relay-only"
}
```

A practical format is:

```text
COSE_Sign1
  └── canonical CBOR payload
  └── Ed25519 signature

Optional recipient encryption:
  COSE_Encrypt0 or HPKE envelope
```

The format must provide:

- Canonical serialization.
- Explicit protocol version.
- Domain separation by record type.
- Publisher and service identity binding.
- Recipient binding.
- Generation and expiration.
- Anti-replay validation.
- No custom cryptographic construction.

---

# Cryptographic Roles

Use separate keys for separate purposes:

| Key | Owner | Purpose |
|---|---|---|
| Owner authority key | Service owner | Policies, manifests, revocations, enrollment approval |
| Device identity key | Phone/server agent | Device authentication and lease signatures |
| Transport key | Connectivity agent | Authenticated encrypted path |
| Record-encryption key | Recipient device | Decrypting endpoint records |
| Coordinator identity key | Coordinator operator | Federation and status signatures |
| Relay authority key | Relay ticket issuer | Short-lived relay authorization |
| Relay node key | Relay operator | Relay endpoint authentication |

A prototype may simplify key handling, but production designs should avoid casually reusing one private key for identity, encryption, transport, and authorization.

---

# Lease Rules

Lease behavior must be deterministic:

```text
Generation:
  Strictly increasing per publisher and service link.

Clock skew:
  Small acceptance window, such as ±5 minutes.

Maximum lifetime:
  Coordinator enforces a protocol-defined cap.

Refresh:
  Excessive refreshes receive rate limits and Retry-After.

Replacement:
  Higher valid generation supersedes lower generation.

Expiry:
  Replicas cannot extend signed expiration.

Rollback:
  Lower generations are rejected unless an explicit signed reset exists.

Replay:
  Clients verify signer, authorization, generation, policy generation, and expiry.
```

Heartbeats may help estimate operational liveness or choose conservative cache durations, but they do not grant trust or expanded permissions.

---

# Connectivity Flow

## Local path

```text
Phone joins home Wi-Fi
        ↓
mDNS/DNS-SD finds candidate agent
        ↓
Phone verifies expected service identity
        ↓
Direct local encrypted connection
        ↓
No WAN coordinator or relay required
```

mDNS only supplies a candidate address. Being on the same LAN is not sufficient proof of identity.

## Remote path

```text
Phone wakes
        ↓
Reads cached signed coordinator manifest
        ↓
Queries a small number of coordinators
        ↓
Validates endpoint lease and service-link policy
        ↓
Gathers local and public candidates
        ↓
Attempts direct IPv6, UDP, QUIC, or permitted TCP paths
        ↓
Requests a relay only after direct failure
        ↓
Returns a local application connection
```

Connection preference:

```text
1. Direct LAN.
2. Direct IPv6.
3. Direct UDP/QUIC.
4. Direct TCP/TLS.
5. User-owned relay.
6. Approved shared relay.
7. Clear failure.
```

A cached endpoint reduces lookup time but does not replace NAT traversal. A cached endpoint can be stale or unusable after a NAT mapping changes.

---

# Relay Model

Relays support difficult cases such as:

- Symmetric NAT.
- CGNAT.
- UDP-blocking networks.
- Hotel or corporate firewalls.
- IPv4/IPv6 incompatibility.

A relay ticket is:

- Pair-bound.
- Service-bound.
- Short-lived.
- Rate-limited.
- Byte-limited.
- End-to-end encrypted.
- Replaceable.

```json
{
  "ticket_id": "random-id",
  "source_device": "phone-key",
  "destination_device": "server-key",
  "service_link_id": "random-link-id",
  "requested_capability": "immich-api",
  "issued_at": "2026-09-21T20:00:00Z",
  "expires_at": "2026-09-21T20:05:00Z",
  "max_bytes": 104857600,
  "max_rate_bps": 5000000,
  "signature": "relay-authority-signature"
}
```

The agent should attempt direct upgrade:

```text
1. Establish temporary relay path.
2. Exchange candidates.
3. Attempt direct connectivity.
4. Close the relay if direct succeeds.
5. Keep the relay only when direct connectivity is impossible.
```

A shared relay should not promise unlimited Jellyfin streaming or unrestricted media transfer. Heavy users should provide their own VPS, reverse proxy, or relay.

---

# Application API

Applications should not receive raw endpoints, relay credentials, coordinator URLs, or network topology.

They request a named capability:

```http
POST /v1/connect
Content-Type: application/json

{
  "service_link_id": "random-link-id",
  "requested_capability": "immich-api",
  "protocol": "http",
  "idle_timeout_seconds": 300
}
```

The agent returns a local connection:

```json
{
  "connection_id": "random-id",
  "local_url": "http://127.0.0.1:41873",
  "expires_at": "2026-09-21T21:00:00Z",
  "path_type": "lan-direct"
}
```

`path_type` is diagnostic-only. The application must not use it for authorization.

The agent handles:

- Coordinator selection.
- Manifest validation.
- Endpoint retrieval.
- LAN discovery.
- NAT traversal.
- Relay selection.
- Transport encryption.
- Policy enforcement.
- Reconnection.
- Quotas.
- Idle cleanup.

For Linux, a Unix socket is preferable:

```text
/var/run/connect-agent/immich.sock
```

---

# Core Coordinator Data

## Service identities

Stores:

- Service identity.
- Owner public key.
- Device public keys.
- Current policy generation.
- Manifest generation.
- Enrollment metadata.
- Revocation state.
- Recovery metadata.

## Service-link authorizations

Stores:

- Service link ID.
- Source device.
- Destination device.
- Requested capability.
- Direction.
- Relay policy.
- Quotas.
- Expiration.
- Revocation state.
- Policy generation.

## Endpoint leases

Stores:

- Service link ID.
- Publisher device.
- Generation.
- Signed encrypted payload.
- Issue time.
- Expiry time.
- Replication metadata.

## Coordinator peers

Stores:

- Coordinator ID.
- Public key.
- URL or transport address.
- Roles.
- Replication agreement.
- Capacity declaration.
- Last successful exchange.
- Circuit-breaker state.

## Relay tickets

Stores only enforcement and replay data:

- Ticket ID.
- Source and destination identities.
- Service link.
- Capability.
- Issue and expiry times.
- Byte and rate limits.
- Concurrent-stream limit.
- Accounting counters.
- Revocation or consumed state where required.

## Desired-state records

Use one replaceable record per device/service-link relationship, not a permanent message queue.

```json
{
  "record_type": "desired-state",
  "service_link_id": "random-link-id",
  "recipient_device": "phone-key-hash",
  "generation": 1842,
  "reason_flags": ["sync_needed", "policy_changed"],
  "expires_at": "2026-10-12T20:00:00Z",
  "ciphertext": "...",
  "signature": "owner-or-service-signature"
}
```

Newer state replaces older state:

```text
generation = max(existing, incoming)
```

## Audit and abuse records

Keep records minimal and retention-bound:

- Enrollment approval and revocation.
- Policy changes.
- Manifest updates.
- Quota violations.
- Relay accounting.
- Replication failures.
- Security validation failures.

Do not store application payloads or long-term endpoint history unless explicitly required by the operator.

---

# Coordinator API

## Device-to-coordinator

```text
POST /v1/enrollment/request
POST /v1/enrollment/approve
POST /v1/lease/publish
GET  /v1/lease/resolve
GET  /v1/desired-state
POST /v1/desired-state/ack
GET  /v1/coordinator-manifest
POST /v1/relay-ticket/request
```

Non-bootstrap actions require:

- Device authentication.
- Capability authorization.
- Bounded payload sizes.
- Replay prevention.
- Rate limiting.
- Expiration checks.

## Coordinator-to-coordinator

```text
POST /v1/federation/inventory
POST /v1/federation/fetch
POST /v1/federation/push
GET  /v1/federation/status
```

Requirements:

- Mutual coordinator authentication.
- Signed inventory entries.
- Namespace authorization.
- Per-peer object and byte budgets.
- No recursive fetch chains.
- Expiry enforcement.
- Operator-controlled replication agreements.
- Ability to withdraw or terminate federation.

---

# Failure Semantics

| Failure | Expected behavior |
|---|---|
| One coordinator fails | Try another coordinator in the signed set |
| Replica is stale | Reject expired or lower-generation data |
| All coordinators unavailable | Existing sessions and LAN paths continue; new remote discovery is degraded |
| Endpoint changes | Publish a higher-generation lease |
| Device sleeps for weeks | Lease expires; identity and policy remain |
| Relay fails | Retry direct paths or use another approved relay |
| Phone is stolen | Revoke its service link and device identity |
| Coordinator is malicious | It may deny service and observe metadata, but cannot forge signed state |
| Relay is malicious | It may observe timing, addresses, and volume, but not authenticated payload content |
| Owner key is compromised | Execute emergency owner-key rotation and manifest replacement |

---

# Implementation Roadmap

## Stage 0: Protocol foundation

- Identity and service-link definitions.
- Threat model.
- Signed record formats.
- Test vectors.
- Lease and generation rules.

## Stage 1: Minimal two-agent system

- Two Linux agents.
- One service identity.
- One service link.
- Manual coordinator.
- Signed endpoint lease.
- App-scoped local proxy.
- Known endpoint transport.

## Stage 2: Local discovery

- mDNS/DNS-SD.
- Cryptographic identity verification.
- Local-first path selection.

## Stage 3: Remote reachability

- STUN or equivalent endpoint observation.
- Candidate gathering.
- Direct UDP/QUIC/TCP attempts.
- Network-change reconnection.

## Stage 4: Coordinator resilience

- Signed coordinator manifests.
- Multiple coordinators.
- Replica and cache behavior.
- Bounded anti-entropy.
- Recovery manifests.
- Migration away from failed coordinators.

## Stage 5: Relay fallback

- User-owned relay.
- Pair-bound tickets.
- Byte and rate quotas.
- Relay-to-direct upgrade.
- Clear failure behavior.

## Stage 6: Mobile integration

- iOS and Android agent behavior.
- Keychain/secure storage.
- Background execution constraints.
- Network transitions.
- Battery-aware refresh behavior.

## Stage 7: Community infrastructure

- Independent coordinator operators.
- Capacity declarations.
- Federation agreements.
- Optional shared relays.
- Abuse and incident procedures.

## Stage 8: Optional advanced discovery

Only after the rest is stable:

- DHT pointers for coordinator manifests.
- Privacy proxies.
- Stronger metadata protection.
- Advanced relay selection.

Raw live endpoint records should not be placed in a public DHT.

---

# What NotDNS Is Not

NotDNS is not:

- A general-purpose VPN.
- A replacement for DNS.
- An anonymity network.
- A public endpoint directory.
- A permanent global relay service.
- A centralized account platform.
- A global event log.
- A public DHT of home and mobile endpoints.
- An automatic trust or reputation authority.
- A replacement for reverse proxies or existing mesh systems.
- A guarantee that direct connectivity always succeeds.

---

# Final Architecture Statement

> NotDNS is an open protocol and local connectivity agent for privately locating and connecting authorized self-hosted application endpoints.
>
> It uses stable cryptographic service and device identities, independently authorized service links, owner-signed policies and coordinator manifests, short-lived signed reachability leases, local-first discovery, multiple replaceable coordinators, direct encrypted paths where possible, and pair-bound relays only when necessary.
>
> Applications receive a local scoped connection rather than raw network topology or broad VPN access. Coordinators provide replaceable rendezvous infrastructure, while endpoint agents retain authority over identity, authorization, signatures, and encrypted transport.
>
> The network is resilient through redundancy, bounded replication, cache-on-demand behavior, operator autonomy, signed migration, and offline recovery—not through a single permanent homeserver or unrestricted global gossip.

The central question is therefore:

```text
Can an authorized application reconnect to the correct service
even when addresses, networks, coordinators, replicas, and relay paths change?
```

That is the actual problem NotDNS is designed to solve.