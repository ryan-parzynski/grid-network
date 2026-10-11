# Grid Network Roadmap

## Phase 0 — Documentation (Current)
**Timeline:** current (review-stage)
**Deliverables:**
- Protocol spec v0.6.2 (design-review) ✓
- Design rationale (complete) ✓
- Security model (complete) ✓
- Commercial model (complete) ✓
- Relay architecture (complete) ✓
- OBJECTS.md §6–§10 (in progress)
- First test vectors (pending)
- Docs finalized

## Phase 1 — Reference Implementation
**Timeline:** review-stage
**Deliverables:**
- Core agent (identity, auth, reachability)
- Local API (Unix socket / HTTP)
- CLI tools
- Test suite (passes all vectors)
- 2+ independent implementations

## Phase 2 — Local Connectivity
**Timeline:** review-stage
**Deliverables:**
- LAN discovery (mDNS/DNS-SD)
- Local relay
- Device pairing UI
- Cross-platform support

## Phase 3 — Remote Reachability
**Timeline:** review-stage
**Deliverables:**
- NAT traversal (STUN, hole punching)
- Candidate gathering
- 70%+ direct connection success rate

## Phase 4 — Coordinator Resilience
**Timeline:** review-stage
**Deliverables:**
- Multiple rendezvous servers
- Replica behavior
- Recovery manifests
- Survives coordinator downtime >24h

## Phase 5 — Relay Fallback
**Timeline:** review-stage
**Deliverables:**
- Relay protocol
- Relay tickets
- Bandwidth quotas
- Priority classes (free/standard/priority/dedicated)
- **At Phase 5: PROTOCOL.md freezes as v1.0 (spec/PROTOCOL.md)**

## Phase 6 — Mobile Integration
**Timeline:** review-stage
**Deliverables:**
- iOS agent
- Android agent
- Background execution
- Battery <5%/day

## Phase 7 — Community Infrastructure
**Timeline:** review-stage
**Deliverables:**
- Operator tooling
- Capacity declarations
- Federation support
- 10+ community relays operational
- Credit system active

## Phase 8 — Advanced Features
**Timeline:** future (TBD)
**Deliverables:**
- Multi-hop relay
- Multipath
- Privacy transport
- Threshold recovery
