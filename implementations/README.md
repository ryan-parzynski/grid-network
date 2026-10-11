# Implementations

Reference implementations and implementation guides.

## Files

- `README.md` — This file.

## Reading Order

1. Implementation guide (to be created).
2. Platform-specific guides (to be created).

## Current Status

Phase 1 (Reference Implementation) not yet started. See `../ROADMAP.md` for timeline.

The prototype outline in `../design/PROTOTYPE.md` describes the recommended vertical-slice approach:
- Phase 0: Canonical CBOR + crypto (byte-level foundation)
- Phase 1: Object/stream engine (state integrity)
- Phase 2: Identity (cryptographic identity)
- Phase 3: Relationships (mutual recognition)
- Phase 4: Authorization (trust decisions)
- Phase 5: Local agent (usable abstraction)
- Phase 6: Reachability (endpoint discovery)
- Phase 7: Direct transport (real connectivity)
- Phase 8: Rendezvous (decentralized discovery)
- Phase 9: Relay (connectivity fallback)
- Phase 10: Application SDK (real application integration)
- Phase 11: Pairing (human-friendly enrollment)
- Phase 12: Production hardening (real deployment)
- Phase 13+: Enterprise/privacy/etc. (ecosystem expansion)

Each phase should leave a working artifact. Don't implement the spec in document order — implement in dependency order (crypto → objects → streams → identity → authorization → agent → network → discovery → relay → applications).
