# Contributing to Grid Network

Thank you for your interest in contributing to Grid Network!

## Current Phase: Documentation & Design (Phase 0)

The protocol specification (PROTOCOL.md v0.6.2) is **frozen**. Current work focuses on:

1. **Complete OBJECTS.md** — Byte-level encoding schemas (§6–§10)
2. **Produce test vectors** — Canonical CBOR + cryptographic constructions
3. **Build reference implementation** — Validate the design

## How to Contribute

### Documentation
- Fix typos, clarify wording in existing documents
- Help complete OBJECTS.md object schemas
- Write test vector descriptions

### Implementation (Phase 1+)
- Reference implementation in Go/Rust/Python
- Cross-platform agent (Linux, macOS, Windows, iOS, Android)
- Application integrations (Jellyfin, Immich, Nextcloud, etc.)

### Protocol Design
- All protocol changes require version bump (see VERSIONING.md)
- Discuss proposals in GitHub Issues before implementing
- Maintain layer separation (protocol / security / connectivity / strategy)

## Development Setup

```bash
# Clone
git clone https://github.com/ryan-parzynski/grid-network
cd grid-network

# View protocol spec
cat docs/protocol/PROTOCOL-v0.6.2.md

# View roadmap
cat docs/operations/ROADMAP.md
```

## Code of Conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you agree to uphold this code.

## Licensing

Grid Network is licensed under **GPL v3**. See [LICENSE.md](LICENSE.md).

Contributions are accepted under the same license. By submitting a PR, you agree to license your contribution under GPL v3.
