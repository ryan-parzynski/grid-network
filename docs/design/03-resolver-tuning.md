260921-01-NotDNS Resovler Tuning

# 

## Executive Summary: Resilient Mesh Rendezvous Project

## What We’re Building

We are creating an open, lightweight **rendezvous and connectivity system** for self-hosted applications.

Its purpose is to help an authorized phone, laptop, or remote service find and connect to a home server even when:

- The server’s public IP changes.
- The client moves between Wi-Fi and cellular networks.
- Both sides are behind NAT or CGNAT.
- A coordinator becomes unavailable.
- A volunteer operator stops running an instance.
- The connection needs to be limited to one application or service.

The system is **not DNS**, although it performs a related discovery function. It is also not intended to be a general-purpose VPN, public DHT, anonymity network, or unrestricted proxy.

The system separates:

```text
Where is the service?
How do I reach it?
Am I authorized to use it?
What traffic am I allowed to send?
```

Those questions are handled by different components.

A coordinator helps locate a service. Endpoint agents establish and authenticate the connection. A relay may assist when direct connectivity fails. The application receives only a local connection and does not need to understand coordinators, NAT traversal, or relay selection.

---

## The Core Design Principle

The most important architectural decision is:

> **Coordinators are replaceable infrastructure. Endpoint identities, authorization, and signed state belong to the participants.**

A coordinator may store, replicate, cache, or return a record, but it does not become the ultimate authority merely because it hosts the database.

The system should continue working when:

- One coordinator goes offline.
- A replica is stale.
- Gossip is delayed.
- A volunteer leaves the network.
- A regional coordinator is overloaded.
- A public discovery service is unavailable.

This is where we borrow from BitTorrent, Syncthing, Matrix, Nostr, and the Fediverse—but only selectively.

We use:

- **BitTorrent-style redundancy and soft-state republishing.**
- **Syncthing-style device identity, approval, local discovery, and relay fallback.**
- **Matrix-style chosen authority and federation concepts.**
- **Nostr-style client-signed records stored by replaceable relays.**
- **Fediverse-style operator autonomy and migration.**
- **libp2p/ICE-style direct connectivity and relay upgrade.**
- **ACME-style enrollment, expiration, renewal, and revocation.**
- **Tor-style separation between stable service identity and changing network location.**

We do **not** copy any of these systems wholesale.

---

# Stable Identity and Temporary Reachability

The original two-blob idea remains useful, but the blobs need clearer security roles.

## 1. Stable identity and policy state

This answers:

```text
What service or device is this?
Who owns it?
Which devices are authorized?
Which coordinators are trusted?
What traffic is allowed?
```

It may include:

- Stable service or device identifier.
- Ed25519 or equivalent public identity key.
- Device public keys.
- Owner or administrator public key.
- Authorized device relationships.
- Allowed service and port policy.
- Coordinator-set manifest.
- Policy generation.
- Enrollment and revocation state.
- Recovery metadata.

This information changes infrequently. It should be signed, exportable, and recoverable.

It is not a reputation score that automatically grants trust. A device becoming older or sending more heartbeats should not silently gain broader access.

## 2. Short-lived endpoint lease

This answers:

```text
Where can this service currently be reached?
```

It may contain:

- Current network candidates.
- Observed public endpoint.
- IPv4/IPv6 information.
- UDP or QUIC port.
- Transport capabilities.
- NAT reachability hints.
- Relay availability.
- Publication generation.
- Issue time.
- Expiry time.
- Publisher signature.
- Recipient-encrypted payload where appropriate.

Endpoint leases are soft state. They expire naturally and are republished when the device wakes, changes network, or detects a new public endpoint.

A typical lease might last:

- A few minutes for a mobile device.
- Thirty minutes to several hours for a frequently changing endpoint.
- Longer for a stable home server, subject to refresh.
- Never indefinitely without renewal.

The lease is not the identity. If it expires, the service still exists and can publish a fresh lease later.

---

# Heartbeats and Liveness

Heartbeats are useful, but they should not be treated as a universal reputation system.

A heartbeat proves:

```text
The holder of this private key is still active enough to refresh its state.
```

It does not prove:

```text
This device is trustworthy.
This device deserves expanded permissions.
This device should be globally preferred.
```

A device may periodically send a signed heartbeat to its chosen coordinator or replica:

```json
{
  "record_type": "liveness",
  "service_link_id": "opaque-id",
  "publisher_key": "ed25519:...",
  "lease_generation": 417,
  "issued_at": "2026-09-21T20:00:00Z",
  "expires_at": "2026-09-21T20:30:00Z",
  "signature": "..."
}
```

The coordinator can use heartbeat history for operational purposes:

- Choosing an appropriate cache duration.
- Avoiding repeated storage of obviously dead records.
- Prioritizing frequently active devices.
- Reporting health statistics to the owner.
- Applying conservative publication limits.

However:

- Heartbeats do not replace authorization.
- Heartbeats do not override an owner’s revocation.
- Heartbeats do not make an endpoint valid after expiry.
- Coordinators should not create permanent trust based solely on uptime.
- Replicas must not extend a lease beyond the signed expiry.

For intermittent phones, a short lease is normal. When the phone wakes, it refreshes its endpoint. The stable identity and enrollment state remain available, so rescanning is unnecessary.

---

# Enrollment: No Static Transform Key

The earlier proposal used a QR-embedded transform key. That should be removed.

A QR code is frequently:

- Screenshot.
- Photographed.
- Backed up.
- Sent through messaging systems.
- Printed.
- Stored in logs or support tickets.

It should not contain a long-lived shared secret that grants broad access.

Instead, the QR code contains a short-lived enrollment capability and enough information to bootstrap trust:

```text
protocol: connect-v1
service_link_id: opaque-random-id
owner_public_key: ed25519:...
initial_coordinators:
  - https://coord-a.example
  - https://coord-b.example
bootstrap_expiry: 2026-09-21T20:01:30Z
enrollment_capability: one-time-secret
```

The enrollment flow is:

```text
1. Owner displays a QR code.

2. Phone scans the QR code.

3. Phone generates its own device keypair locally.

4. Phone proves possession of the one-time enrollment capability.

5. Owner or server approves the new device.

6. The phone receives a device-specific authorization policy.

7. The phone receives a signed coordinator-set manifest.

8. The enrollment capability is consumed or expires.

9. Future connections use the device key, not the QR secret.
```

Each device gets its own identity and can be revoked independently.

A compromised phone does not require replacing every other device’s credentials.

---

# Signed Coordinator Sets

A service should not permanently depend on one coordinator URL.

The owner signs a coordinator-set manifest:

```json
{
  "record_type": "coordinator-set",
  "service_link_id": "opaque-random-id",
  "generation": 42,
  "not_before": "2026-09-21T20:00:00Z",
  "expires_at": "2026-12-21T20:00:00Z",
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

- The owner signature.
- The manifest generation.
- The expiration time.
- The coordinator identity key.
- The coordinator’s declared role.
- The service link identity.

This prevents an arbitrary gossip participant from adding itself as a trusted coordinator.

If `coord-eu-1` disappears, the owner can publish generation 43 without changing the service identity or reenrolling every device.

The owner can also include:

- A self-hosted coordinator.
- A community coordinator.
- A friend-operated coordinator.
- A VPS coordinator.
- A read-only recovery coordinator.
- A local-only coordinator.

The coordinator set is not necessarily secret. The sensitive material is the endpoint lease and access policy.

---

# Coordinator Resilience: Home, Replicas, and Swarm Behavior

The system should not copy Matrix’s assumption that one homeserver is the essential home of a user’s active infrastructure.

A better model is:

```text
Owner or service identity
        │
        ├── chosen publication coordinator
        ├── selected replicas
        ├── optional cache coordinators
        └── emergency/recovery sources
```

The publication coordinator may be the administrative home, but it must not be a single point of failure for lookup.

## Coordinator roles

### Publication coordinator

Accepts authorized endpoint publications and enrollment operations.

### Replica coordinator

Stores signed copies of selected records and serves reads when the publication coordinator is unavailable.

### Cache coordinator

Fetches and temporarily caches records that users actually request. It does not need a global copy of the network.

### Bootstrap coordinator

Helps clients discover current coordinator manifests. It does not necessarily store endpoint data.

### Relay coordinator

Issues short-lived relay tickets or helps peers find an approved relay. It does not automatically carry application traffic.

One coordinator may perform several roles, but the protocol should distinguish them.

## The coordinator is not the permanent home of truth

The actual authority is distributed among:

- The owner’s signing key.
- The service or device identity key.
- The endpoint publisher’s signature.
- The device authorization policy.
- The signed coordinator-set manifest.
- The endpoint lease expiry.

A coordinator database is replaceable infrastructure.

If every coordinator disappears, recovery material should still allow the owner to recreate the service:

```text
Owner key
+ service identity
+ current policy
+ coordinator manifest
+ enrollment/recovery information
```

This is closer to **replicated soft state** than a centralized homeserver model.

---

# Swarm and Gossip Model

The system can use swarm-like behavior, but it should not become unrestricted global gossip.

The useful pattern is:

```text
Small peer groups
+ bounded anti-entropy
+ signed records
+ selective replication
+ cache-on-demand
+ multiple lookup paths
```

Each coordinator periodically exchanges compact inventories with a limited set of peers:

```text
Coordinator A:
  “I have record X at generation 417.”
  “I have record Y at generation 12.”
  “I have no current record for Z.”
```

The peer requests only selected missing records.

Replication should enforce:

- Maximum bytes per exchange.
- Maximum records per round.
- Maximum peer count.
- Maximum fetch depth.
- Maximum storage quota.
- Namespace or tenant restrictions.
- Expiration checks.
- Generation checks.
- Backoff after repeated failures.
- No recursive uncontrolled fan-out.

Example:

```text
Regional exchange:
  max 1 MiB per minute
  max 1,000 inventory entries per round
  max 100 full record fetches per round

Cross-region exchange:
  lower frequency
  lower bandwidth budget
  on-demand fetch for authorized live requests
```

This allows the network to behave like a swarm without forcing every volunteer to store or serve every service.

## Selective replication

A coordinator can declare:

```json
{
  "coordinator_id": "eu-west-1",
  "accepts_new_links": true,
  "read_mode": "replica-and-cache",
  "max_records": 100000,
  "max_storage_bytes": 1073741824,
  "max_replication_bytes_per_hour": 52428800,
  "accepted_regions": ["eu-west", "eu-central"],
  "public_lookup": false,
  "valid_until": "2026-09-21T21:30:00Z",
  "signature": "coordinator-signature"
}
```

Operators decide:

- Which services they will host.
- Which namespaces they will replicate.
- Whether they accept public enrollment.
- Whether they operate read-only.
- Whether they accept cross-region traffic.
- Whether they provide relay services.
- When they are full or draining.

This directly addresses volunteer burnout.

A coordinator can leave without taking the infrastructure with it.

---

# Endpoint Records: Signed and Encrypted Where Appropriate

The previous XOR design should be removed.

XOR with a QR-distributed key is not meaningful confidentiality because:

- The key is shared with every QR recipient.
- It cannot safely support independent revocation.
- A compromised recipient may decode all records using that key.
- It gives a false impression of security.
- It does not protect against a coordinator that already sees the publishing connection.
- It does not protect metadata such as timing or lookup behavior.

Use authenticated encryption instead.

An endpoint lease might conceptually contain:

```json
{
  "record_type": "endpoint-lease",
  "service_link_id": "opaque-random-id",
  "publisher_device_id": "device-key-hash",
  "generation": 417,
  "issued_at": "2026-09-21T20:00:00Z",
  "expires_at": "2026-09-21T20:30:00Z",
  "recipient": "authorized-device-key",
  "ciphertext": "...",
  "signature": "publisher-signature"
}
```

The payload may contain:

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
  "service_identity": "ed25519:...",
  "allowed_ports": [2283],
  "relay_policy": "approved-relay-only"
}
```

The coordinator may still observe the source IP of the publishing device. Encryption protects the record from:

- Passive storage replicas.
- Unauthorized readers.
- Database theft.
- Coordinators that are not authorized to decrypt the content.
- Cross-coordinator replication peers.

It does not magically hide transport metadata from the coordinator contacted directly.

## Metadata visibility

| Party | Typically learns |
|---|---|
| Primary coordinator | Source IP, timing, request frequency, credential identity, object ID, ciphertext size |
| Replica coordinator | Object ID, ciphertext size, expiry, replication timing |
| Authorized peer | Decrypted candidates, service identity, connection policy |
| Relay | Both network-facing addresses, timing, packet sizes, byte counts |
| Passive network observer | Encrypted traffic metadata, depending on transport |
| Unauthorized reader | No useful endpoint data if encryption and signatures are correct |

Privacy from the primary coordinator would require an optional privacy proxy or relay:

```text
Device → privacy proxy → coordinator
```

That is an advanced mode with additional cost, latency, and operational complexity.

---

# Real Connectivity Is More Than Discovery

Finding an endpoint is only one part of making a connection.

The connectivity agent should handle:

```text
1. Local discovery.
2. Candidate gathering.
3. Public endpoint observation.
4. Direct connection attempts.
5. NAT traversal.
6. Relay fallback.
7. Connection upgrade.
8. Idle cleanup.
9. Reconnection after network changes.
```

## Local-first path

```text
Phone joins home Wi-Fi
        ↓
mDNS/DNS-SD finds candidate agent
        ↓
Phone verifies expected service identity
        ↓
Direct local connection
        ↓
No WAN coordinator or relay required
```

mDNS is only a discovery mechanism. A malicious LAN device can advertise a fake service. The phone must verify the discovered device’s cryptographic identity before sending credentials or application traffic.

## Remote path

```text
Phone wakes
        ↓
Reads cached signed coordinator manifest
        ↓
Queries several coordinators with bounded timeouts
        ↓
Receives current signed endpoint lease
        ↓
Attempts direct IPv6/UDP/QUIC connectivity
        ↓
Uses relay if direct connection fails
        ↓
Provides a local application connection
```

The system should prefer:

1. Direct LAN connection.
2. Direct IPv6.
3. Direct UDP/QUIC.
4. Direct TCP/TLS where available.
5. User-owned relay.
6. Approved shared relay.
7. Clear failure.

A cached endpoint is useful for reducing lookup time, but it is not a replacement for NAT traversal. A cached endpoint may be stale, unreachable, or invalid after a NAT mapping changes.

---

# Relay Behavior

Relays are necessary for some network combinations:

- Symmetric NAT.
- Carrier-grade NAT.
- UDP-blocking networks.
- Hotel or corporate firewalls.
- IPv4/IPv6 incompatibility.
- Two devices that cannot establish a direct path.

The relay should be:

- Optional.
- Pair-bound.
- Short-lived.
- Destination-bound.
- Service-scoped.
- Quota-limited.
- End-to-end encrypted.
- Replaceable.

A relay ticket might be restricted to:

```json
{
  "connection_id": "random-id",
  "source_device": "phone-key",
  "destination_device": "server-key",
  "destination_service": "immich-api",
  "destination_port": 2283,
  "issued_at": "2026-09-21T20:00:00Z",
  "expires_at": "2026-09-21T20:05:00Z",
  "max_bytes": 104857600,
  "max_rate_bps": 5000000,
  "signature": "relay-authority-signature"
}
```

The agent should attempt a direct upgrade:

```text
1. Establish temporary relay path.
2. Exchange candidates through the relay.
3. Attempt direct connectivity.
4. Close the relay if direct succeeds.
5. Keep the relay only when direct connectivity is impossible.
```

A direct upgrade is not guaranteed. Some peers will require a relay for the entire session.

For high-volume Jellyfin streaming or large media uploads, users should be able to provide:

- Their own VPS relay.
- A reverse proxy.
- A static public endpoint.
- An existing mesh service.
- A private relay operated by a friend or organization.

A volunteer-operated shared relay should not silently become an unlimited media-transfer service.

---

# The Application-Facing API

Applications should not receive raw endpoints, coordinator URLs, relay credentials, or network topology.

The application should express intent:

```http
POST /v1/connect
Content-Type: application/json

{
  "service_link": "home-immich",
  "protocol": "http",
  "remote_port": 2283,
  "purpose": "mobile-backup",
  "idle_timeout_seconds": 300
}
```

The agent returns a local connection:

```json
{
  "connection_id": "random-id",
  "local_address": "127.0.0.1",
  "local_port": 41873,
  "expires_at": "2026-09-21T21:00:00Z"
}
```

The application connects normally:

```text
Immich → http://127.0.0.1:41873 → local connectivity agent → remote Immich service
```

The agent handles:

- Coordinator selection.
- Manifest validation.
- Endpoint lease retrieval.
- Local discovery.
- NAT traversal.
- Relay selection.
- Transport encryption.
- Policy enforcement.
- Reconnection.
- Idle cleanup.
- Quotas.
- Logging and diagnostics.

For Linux deployments, a Unix socket is preferable:

```text
/var/run/connect-agent/immich.sock
```

The application should not be able to request:

```text
- Arbitrary LAN access.
- Arbitrary destination ports.
- Reverse server-to-phone connections.
- Unrestricted relay usage.
- Another application’s service link.
- Raw coordinator records.
```

This keeps Immich and Jellyfin decoupled from the connectivity implementation.

---

# Service-Scoped Authorization

Authorization should be explicit and narrow:

```json
{
  "service_link_id": "home-immich",
  "source_device": "alice-phone-device-key",
  "destination_device": "home-server-device-key",
  "transport": "tcp",
  "destination_service": "immich-api",
  "destination_port": 2283,
  "direction": "phone-to-server",
  "relay_allowed": true,
  "max_relay_bytes_per_day": 268435456,
  "max_relay_rate_bps": 5000000,
  "not_before": "2026-09-21T20:00:00Z",
  "expires_at": "2026-12-31T23:59:59Z",
  "policy_generation": 42,
  "signature": "owner-signature"
}
```

A valid device identity alone is not enough.

The policy must determine:

- Which device may connect.
- Which service it may reach.
- Which port is allowed.
- Which direction is allowed.
- Whether relay use is permitted.
- How much relay traffic is permitted.
- When the authorization expires.
- Which policy generation is current.

This prevents an Immich connection from accidentally becoming a general VPN into the home LAN.

---

# The Real Lifecycle

## Initial setup

```text
1. Alice installs the connectivity agent beside her Immich server.

2. The server generates a stable service identity.

3. Alice selects:
   - A self-hosted coordinator.
   - A community coordinator.
   - Several coordinators.
   - Or a combination.

4. The server creates a signed coordinator-set manifest.

5. Alice displays a one-time enrollment QR code.

6. Bob’s phone scans the QR code.

7. Bob’s phone generates its own device key.

8. Alice approves Bob’s device.

9. Bob receives a service-specific policy.
```

## Normal connection

```text
1. Bob opens Immich.

2. The local agent tries mDNS/DNS-SD.

3. If Alice’s server is local, the agent connects directly.

4. Otherwise, the agent reads the cached coordinator manifest.

5. It queries several coordinators in parallel or sequence.

6. It verifies the endpoint lease signature and expiry.

7. It attempts direct connectivity.

8. If direct connectivity fails, it requests an approved relay ticket.

9. Immich receives a local connection endpoint.

10. Immich operates normally without knowing the path used.
```

## Address change

```text
1. Alice’s ISP changes her public address.

2. The server detects the change through:
   - Network state changes.
   - STUN observation.
   - Failed connectivity checks.
   - Periodic reachability tests.

3. The server publishes a new endpoint lease.

4. The generation increments.

5. The selected coordinator stores it.

6. Replicas and caches receive it through bounded replication.

7. Bob’s next connection retrieves the newer lease.

8. The old lease expires naturally.
```

## Coordinator failure

```text
1. Bob tries coordinator A.

2. Coordinator A times out.

3. The agent opens its circuit breaker for A.

4. Bob tries coordinator B or C from the signed manifest.

5. A replica returns the most recent valid endpoint lease.

6. The connection proceeds.

7. The server later republishes to an available coordinator.

8. The owner eventually removes coordinator A in a new signed manifest.
```

## Total coordinator loss

If all coordinators for a service are temporarily unavailable:

- Existing direct connections continue.
- Cached endpoint leases may continue working until expiry.
- Local LAN discovery still works.
- User-owned static routes still work.
- The owner can restore a coordinator from exported recovery material.
- A signed coordinator-set update can redirect clients later.
- The service identity and device approvals do not need to change.

This is the resilience goal: **coordinator loss causes degraded discovery, not loss of identity or ownership.**

---

# Coordinator Metadata and Privacy

The system should make no claim that coordinators are blind.

A coordinator contacted directly by a device normally sees:

- The source IP address.
- The source port or connection metadata.
- Request timing.
- Refresh frequency.
- Credential or public identity reference.
- Object identifiers.
- Ciphertext sizes.
- Whether the device is currently publishing.

A replica may see less if it stores recipient-encrypted records.

The design goal is not perfect metadata privacy. The goal is:

```text
- Coordinators cannot forge endpoint records.
- Replicas cannot read records they are not authorized to read.
- Stolen databases do not immediately reveal endpoint contents.
- Unauthorized users cannot enumerate service access.
- Relays cannot read application payloads.
- Clients can detect stale or malicious responses.
```

If stronger privacy is needed later, add an optional privacy proxy. Do not make it a Phase 1 requirement.

---

# What We Decided Against

## Not a general VPN

The default model is app-scoped connectivity through a local agent.

WireGuard may be supported as an optional backend, but the public API should not require:

- TUN interfaces.
- Kernel modules.
- Full overlay routing.
- Broad LAN access.
- Elevated container privileges.

QUIC/TLS or another user-space encrypted transport may be a better default for app-scoped connections.

## Not a single Matrix-style home server

A chosen home coordinator may exist, but it is not a permanent single point of failure.

The system uses:

- Signed manifests.
- Multiple coordinators.
- Selected replicas.
- Cache-on-demand.
- Bounded anti-entropy.
- Exportable recovery information.
- Owner-controlled migration.

The network should remain useful when the administrative home is offline.

## Not unrestricted global gossip

Coordinators do not replicate every record to every other coordinator.

Replication is:

- Bounded.
- Selective.
- Operator-controlled.
- Expiring.
- Namespace-aware.
- Based on signed inventories.
- Limited by storage and bandwidth quotas.

## Not a public endpoint DHT

A DHT may be considered later for discovering signed coordinator manifests, but not for publishing raw live home-server or phone endpoints.

A public DHT creates risks involving:

- Endpoint disclosure.
- Presence tracking.
- Sybil and eclipse attacks.
- Record poisoning.
- Lookup monitoring.
- Mobile battery usage.
- Abuse and unwanted targeting.

## Not XOR obfuscation

Use authenticated encryption and signatures where endpoint confidentiality is needed.

Obfuscation can still be used for non-security purposes, but it must not be presented as protection.

## Not a permanent shared relay

Relays are expensive and expose traffic metadata.

Use:

- Direct connectivity whenever possible.
- Temporary relay paths for setup and fallback.
- User-owned relays for sustained heavy traffic.
- Pair-bound tickets.
- Quotas and expiration.
- Clear failure behavior.

## Not automatic trust through reputation

Heartbeat history may help with operational TTL decisions, but it does not grant authorization or expand permissions.

Trust comes from:

- Device approval.
- Public-key identity.
- Signed policy.
- Explicit owner authorization.
- Revocation and expiration.

## Not a centralized account platform

The coordinator does not need to become:

- A global user database.
- A billing system.
- A social identity provider.
- A public service directory.
- A universal authentication authority.

---

# Deployment Model

A basic coordinator can still be lightweight:

```text
HTTP/QUIC API
SQLite or RocksDB
Signed record validation
Short-lived lease cleanup
Bounded replication
Capacity declaration
Health and rate limits
```

But the data model should now reflect the architecture.

## Core tables

### Service identities

Stores:

- Service link ID.
- Owner public key.
- Service/device public keys.
- Policy generation.
- Coordinator manifest generation.
- Enrollment metadata.
- Revocation state.
- Recovery metadata.
- Creation and update timestamps.

### Device authorizations

Stores:

- Service link ID.
- Device public key.
- Authorization scope.
- Allowed service.
- Allowed port.
- Direction.
- Relay policy.
- Quota.
- Expiration.
- Revocation state.
- Policy generation.

### Endpoint leases

Stores:

- Service link ID.
- Publisher device ID.
- Record generation.
- Signed ciphertext or encrypted endpoint payload.
- Issue time.
- Expiry time.
- Publisher signature.
- Replication status.
- Last observed source metadata, where operationally necessary.

### Coordinator peers

Stores:

- Coordinator ID.
- Public key.
- URL or transport address.
- Roles.
- Region hint.
- Replication agreement.
- Capacity policy.
- Last successful exchange.
- Circuit-breaker state.

### Enrollment records

Stores:

- One-time capability hash.
- Service link ID.
- Intended device or invitation scope.
- Creation time.
- Expiry time.
- Consumed state.
- Approval state.

The endpoint lease remains small, but the system now has enough structure to support