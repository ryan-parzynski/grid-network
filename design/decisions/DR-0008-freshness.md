---
title: "Grid Network — Freshness attestation"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-08
severity: Med
blocks: V1.1
linked_finding: H5
opened: 2026-10-11
deciders: (pending acceptance)
---
---
title: "Grid Network — Freshness attestation"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-08
severity: Med
blocks: V1.1
linked_finding: H5
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-08 — Freshness attestation

> **Status:** PROPOSED — NOT ACCEPTED. Change only on merged PR with spec updates and CHANGELOG entry.

## Metadata

- ID: D-08
- Title: Freshness attestation
- Severity: Med
- Blocks: V1.1
- Linked finding: [REVIEW-2026-10-11 H5](../REVIEW-2026-10-11.md) (see section H5 or search tag)
- Date opened: 2026-10-11
- Status: PROPOSED

D-08: FRESHNESS ATTESTATION AND REFRESH OBJECTS
[HIGH PRIORITY, BLOCKS AUTHORIZATION]

Problem:
v0.6.2 distinguishes lease validity from authorization freshness, but has no
signed object that records a "successful refresh." Freshness therefore cannot
be computed from signed state as the core invariant requires (H2). A verifier
cannot tell if it has truly seen all revocations from an issuer; it can only
count elapsed time.

Option A: FreshnessAttestation, ephemeral, with issuer stream head
[PROPOSED in §12, H2]

  New separator: grid/freshness-attestation/v1.
  Fields: issuer_principal, authorization_stream_id, head_sequence,
  head_chain_hash (the issuer's current stream head), subject_principal
  (requester), verifier_nonce (32 random bytes chosen by requester),
  issued_at.
  Signed by the Authorization Key that owns the stream.
  EPHEMERAL: not stored by rendezvous, not retransmitted, not part of any
  stream.

  Verification: signature valid, nonce matches outstanding request, and
  verifier's accepted head equals head_sequence/head_chain_hash (after
  syncing). If valid, reset elapsed_since_last_successful_authorization_refresh
  to zero.

  Pros:
    - Issuer commits to their current stream state; verifier knows it has
      seen all published revocations up to that point.
    - Ephemeral: no storage overhead; no archival burden.
    - Nonce prevents replay and replay-to-other-verifier.
    - Derives from the exact protocol logic: a verifier is fresh iff it has
      synchronized to the issuer's head.

  Cons:
    - Requires an interactive exchange: requester sends nonce, issuer
      responds with attestation.
    - Adds a message round-trip to every freshness refresh (bandwidth cost).
    - Issuer key must be online to sign freshness attestations.

Option B: Signed LeaseRefresh object in the authorization stream

  New object: grid/lease-refresh/v1, in the Authorization Key's stream.
  Fields: lease_id, refresh_issued_at, expires_at, issuer_nonce.
  Signed by the Authorization Key.
  Stored in the stream; acts as a recorded proof that a lease was valid at a
  certain time.

  Pros:
    - Asynchronous: issuer can pre-generate multiple refreshes and store them.
    - Simpler implementation: verifier just checks the object's signature and
      timestamp.

  Cons:
    - Stream grows unboundedly with refreshes; a cleanup/checkpoint mechanism
      (D-19) is required.
    - Issuer must predict future refresh times or issue on-demand (either way,
      it's active work).
    - Does not prove the issuer has seen all revocations; it only proves a
      lease was valid at issuance time. Subsequent revocations invalidate it,
      but the refresh doesn't know about them.
    - Breaks the "freshness = seen all revocations" semantic.

Option C: Time-based freshness only; no explicit refresh

  A lease is fresh if elapsed_since_issuance <= MAX_FRESHNESS_AGE. No
  explicit refresh objects.

  Pros:
    - Simplest: no new objects or interactions.

  Cons:
    - Does not prove the issuer has seen all revocations.
    - Verifier cannot distinguish "issuer is offline" from "issuer revoked
      this grant."
    - Violates the core invariant (cannot establish freshness from signed
      state alone).

Recommendation:
Accept Option A (FreshnessAttestation, interactive, with stream head).
Provides cryptographic proof that the verifier has seen all revocations
without requiring a new stream. The interactive round-trip is the cost of
certainty; applications can batch multiple freshness requests per connection.

Consequences:
  - Add grid/freshness-attestation/v1 to the separator registry, marked
    EPHEMERAL (not stored by rendezvous, not persisted by verifier, not
    part of a stream).
  - OBJECTS.md: FreshnessAttestation schema.
  - §12 and §17: update freshness semantics and local API.
  - Wire protocol: define nonce generation, request/response pairing,
    timeout.
  - Test vectors: successful attestation, stale head, replay attempts.
  - D-08 allows D-12 (reboot rule) to treat relative validity correctly.

================================================================================
