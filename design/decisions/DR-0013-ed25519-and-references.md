---
title: "Grid Network — Ed25519 verification strictness"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-13
severity: High
blocks: V1
linked_finding: —
opened: 2026-10-11
deciders: (pending acceptance)
---
---
title: "Grid Network — Ed25519 verification strictness"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-13
severity: High
blocks: V1
linked_finding: —
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-13 — Ed25519 verification strictness

> **Status:** PROPOSED — NOT ACCEPTED. Change only on merged PR with spec updates and CHANGELOG entry.

## Metadata

- ID: D-13
- Title: Ed25519 verification strictness
- Severity: High
- Blocks: V1
- Linked finding: [REVIEW-2026-10-11 —](../REVIEW-2026-10-11.md) (see section — or search tag)
- Date opened: 2026-10-11
- Status: PROPOSED

D-13: ED25519 VERIFICATION STRICTNESS AND KEY VALIDATION
[HIGH PRIORITY, AFFECTS INTEROPERABILITY]

Problem:
RFC 8032 Ed25519 implementations differ on small-order keys, non-canonical
signature encodings, and cofactor handling. Without specifying strictness,
verifiers will diverge: one implementation accepts a signature; another
rejects it. This is the top interoperability risk after the stream model
(H7).

Option A: Strict RFC 8032 verification [PROPOSED in §13.2]

  1. Pure Ed25519 (no Ed25519ph or Ed25519ctx variants).
  2. Reject signatures where S >= L (group order 2^252 + 27742317777372353535).
  3. Reject public keys and R values with non-canonical encodings.
  4. Reject public keys of small order (including identity/neutral point).
     Small order = any point P where 8P = identity (cofactor = 8).
  5. Verify using the cofactorless equation [S]B = R + [k]A.
  6. Publish edge-case vectors: small-order keys, non-canonical S/R/A, test
     against every implementation.

  Pros:
    - Interoperable: all verifiers agree.
    - Secure: rejects all known Ed25519 attacks.
    - Standard: based on RFC 8032.

  Cons:
    - Some libraries (libsodium, NaCl) use cofactored verification by default
      and don't reject small-order keys. Implementations must layer strictness
      on top.
    - Slightly slower (cofactorless verification, small-order check).

Option B: Permissive (library default)

  Accept whatever the cryptographic library does. No special validation.

  Pros:
    - Simplest: use library defaults.
    - Faster (no extra checks).

  Cons:
    - Verifiers diverge on edge cases.
    - Small-order keys could be used to construct signatures that verify
      under some implementations but not others.
    - Interoperability is not guaranteed.

Recommendation:
Accept Option A (strict RFC 8032). Implement the strictness layer explicitly.
Publish edge-case vectors and require every implementation to pass them.

Consequences:
  - §13.2: finalize strictness rules (as proposed).
  - Crypto reference: write a reference verifier showing the exact checks
    (pseudocode or Rust code).
  - Test vectors: at least one vector for each edge case (small-order key,
    non-canonical S, non-canonical R/A, valid signature, invalid S ≥ L).
  - Implementer guide: library-specific notes (libsodium: use
    crypto_sign_open_detached with cofactorless flag; etc.).
  - Conformance test: every verifier must pass the edge-case vectors or be
    marked non-conformant.

================================================================================
