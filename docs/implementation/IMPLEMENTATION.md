# Grid Network — Implementation Guide

**Status:** To be drafted (Tier 2 task)  
**Depends on:** PROTOCOL.md v0.6.2, OBJECTS.md §1–§5, SECURITY.md

---

## §1: GRID AGENT ARCHITECTURE

### 1.1 Components

```
┌─────────────────────────────────────────────────────────┐
│                    Grid Agent                           │
├─────────────────────────────────────────────────────────┤
│  Identity Manager      │  Auth Manager      │  Reach    │
│  - Key storage         │  - Grant eval      │  - mDNS   │
│  - Stream tracking     │  - Lease mgmt      │  - STUN   │
│  - Verifier            │  - Revocation      │  - Rendezvous│
├─────────────────────────────────────────────────────────┤
│  Transport Manager     │  Local API         │  Config   │
│  - WireGuard           │  - Unix socket     │  - File   │
│  - QUIC (future)       │  - HTTP (opt)      │  - Env    │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Data flow

```
Application → Local API → Auth Manager → Verifier → Reachability → Transport
                ↑                                        ↓
           Response ← Connection Handle ← WireGuard Config ← Handshake
```

---

## §2: LOCAL STORAGE

### 2.1 Required persistent state

- Trust anchors (self + recognized peers' Identity Roots)
- Accepted stream state (sequence + chain_hash per stream)
- Local observation history (first_observed_at for relative validity)
- Key material (Identity Root, Device Key, Service Key, Auth Key)
- Cached reachability records (with TTL)

### 2.2 Storage requirements

- Atomic writes (crash-safe)
- Encryption at rest (recommended)
- Backup/export for recovery

---

## §3: CROSS-PLATFORM CONSIDERATIONS

### 3.1 Linux
- systemd service
- WireGuard kernel module / wireguard-go
- mDNS via avahi or mdns-sd

### 3.2 macOS
- launchd service
- wireguard-go
- mDNS via Bonjour/mdns-sd

### 3.3 Windows
- Windows Service
- wireguard-go / Wintun
- mDNS via Bonjour SDK

### 3.4 iOS
- Network Extension framework
- Background modes (VoIP, background fetch)
- Keychain for key storage

### 3.5 Android
- VpnService
- WorkManager for background
- Android Keystore for key storage

---

## §4: LOCAL API

### 4.1 Unix socket (preferred)

```
/var/run/grid-agent/grid.sock
```

### 4.2 API surface

```json
// Discover known peers
GET /v1/peers

// Resolve peer state
GET /v1/peers/{peer_id}

// Request authorized connection
POST /v1/connect
{
  "peer_id": "peer:v1:...",
  "capability": "org.jellyfin.stream"
}

// Response
{
  "connection_id": "uuid",
  "local_url": "http://127.0.0.1:41873",
  "expires_at": "2024-01-15T10:00:00Z"
}

// Authorization decision
POST /v1/authorize
{
  "peer_id": "peer:v1:...",
  "capability": "org.jellyfin.stream"
}

// Issue revocation
POST /v1/revoke
{
  "object_id": "sha256:...",
  "type": "grant_revocation"
}

// Daemon status
GET /v1/status
```

---

## §5: WIREGUARD INTEGRATION

### 5.1 Peer configuration

The agent manages WireGuard peer configs:
- Private key (Device Key or dedicated transport key)
- Peer public keys
- AllowedIPs (minimal: just the tunnel endpoint)
- Endpoint (updated from reachability)
- PersistentKeepalive (25s for NAT)

### 5.2 Dynamic reconfiguration

When reachability changes:
1. Agent receives new endpoint
2. Updates WireGuard peer endpoint
3. Sends handshake initiation
4. Connection resumes

---

## §6: REFERENCE IMPLEMENTATION ROADMAP

### Language priorities:

1. **Go** — Primary reference (WireGuard ecosystem, cross-platform)
2. **Rust** — Secondary (memory safety, performance)
3. **Python** — Tertiary (prototyping, testing)

### Milestone 1: Core crypto (2 weeks)
- Ed25519, SHA-256, CBOR encoding
- Domain separators, chain construction
- Signature verification procedure

### Milestone 2: Stream tracking (2 weeks)
- Identity document validation
- Sequence/chain validation
- Fork detection

### Milestone 3: Authorization (2 weeks)
- Grant/lease evaluation
- Relative validity
- Revocation handling

### Milestone 4: Reachability (3 weeks)
- mDNS discovery
- STUN client
- Rendezvous client
- Relay client

### Milestone 5: Local API + WireGuard (3 weeks)
- Unix socket server
- WireGuard config management
- Connection handling

### Milestone 6: Integration testing (2 weeks)
- Conformance test suite
- Interop with other implementations
- Edge case validation

**Total: ~14 weeks for minimal viable agent**

---

*End of Implementation Guide placeholder — to be drafted as Tier 2 task*
