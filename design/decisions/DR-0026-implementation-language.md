---
title: "Grid Network — Implementation language"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-26
severity: Low
blocks: —
linked_finding: —
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-26

> **Status:** PROPOSED — NOT ACCEPTED.



## Context / Problem

No implementation language is established in the supplied files. The spec
requires specific properties: safe CBOR parsing (R1), mobile embedding (R2),
WireGuard integration (R3), small relay footprint (R4), strict cryptography
(R5), and community approachability (R6).

## Options considered

Option A: Rust for the core, Go for rendezvous/relay [PROPOSED]

  Core library (verifier, state machine, store, local API): Rust.
    Justification: memory-safe (R1), mature WireGuard support (boringtun),
    mobile bindings (R2, C ABI), small binaries (R4), strict crypto libraries
    available (R5).
  Rendezvous and relay daemons: Go.
    Justification: proven in production (Tailscale, others), good http/REST
    support, easier for community (R6), sufficient for stateless daemons.
  Vector checker and test harness: Python or TypeScript.
    Justification: rapid prototyping, clear test structure, second
    independent verifier (D-23).

  Pros:
    - Addresses all requirements (R1–R6) with appropriate tools.
    - Clear separation: Rust safety for the boundary, Go for auxiliary
      services.
    - Mobile: Rust library is straightforward to bind to Swift/Kotlin.

  Cons:
    - Two languages: build/CI complexity.
    - Rust learning curve for contributors (R6 tradeoff).

Option B: Go for everything

  All code (core, rendezvous, relay, test harness) in Go.

  Pros:
    - One language: simpler build and contributor onboarding (R6).
    - Go toolchain is familiar to many (good for community).

  Cons:
    - Go GC is not ideal for embedded/mobile (R2 risk).
    - Go's crypto libraries are less strict (R5 requires layering).
    - Goroutines are harder to reason about in a security-critical verifier.
    - No good WireGuard integration (R3).

Option C: C/C++ for maximum performance

  Core and daemons in C/C++.

  Pros:
    - Maximum performance and size (R4).

  Cons:
    - Memory safety is a major risk for parsing hostile CBOR (R1 fails).
    - Requires careful Valgrind/AddressSanitizer testing.
    - Higher barrier to contribution (R6).

Option D: TypeScript/Node.js for simplicity

  All code in TypeScript.

  Pros:
    - Familiar to web developers (good for community growth).
    - Rapid development.

  Cons:
    - Runtime overhead (R4 relay footprint).
    - Performance not suitable for relays on Pi-class hardware.
    - CBOR parsing libraries are not typically strict (R5).

## Recommendation (PROPOSED — NOT DECIDED)

> **PROPOSED:**

Accept Option A (Rust core + Go rendezvous/relay + Python/TS test harness).
Rust address the highest-risk decision (R1: memory-safe CBOR parsing of
hostile input in a security boundary). Go and Python are acceptable for
stateless/auxiliary roles.

Implement the core library in Rust with a published C FFI or WASM binding for
mobile (Swift/Kotlin on iOS/Android; embed or call from browser). Rendezvous
and relay in Go (proven reliability, community expertise in Tailscale and
WireGuard projects). Test harness in Python or TypeScript (fast iteration,
clear test logic).

## Consequences

- Toolchain: Rust 1.70+, Go 1.21+, Python 3.11+ or Node 18+.
  - Repository structure: core/rust/, rendezvous/go/, relay/go/,
    reference/python/, conformance/python/.
  - CI: rustfmt/clippy (Rust), gofmt/go vet (Go), Python linting
    (pytest/black).
  - Mobile: Rust FFI bindings in reference/bindings/{swift,kotlin}/.
  - Documentatio: language-specific setup guides in implementations/README.md.
  - D-26 unblocks the build planning (D-27).
