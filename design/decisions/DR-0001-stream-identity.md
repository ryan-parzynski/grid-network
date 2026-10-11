---
title: "Grid Network — Stream identity model"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-01
severity: High
blocks: V1
linked_finding: C5
opened: 2026-10-11
deciders: (pending acceptance)
---
---
title: "Grid Network — Stream identity model"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-01
severity: High
blocks: V1
linked_finding: C5
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-01 — Stream identity model

> **Status:** PROPOSED — NOT ACCEPTED. Change only on merged PR with spec updates and CHANGELOG entry.

## Metadata

- ID: D-01
- Title: Stream identity model
- Severity: High
- Blocks: V1
- Linked finding: [REVIEW-2026-10-11 C5](../REVIEW-2026-10-11.md) (see section C5 or search tag)
- Date opened: 2026-10-11
- Status: PROPOSED

D-01: STREAM IDENTITY MODEL — HASH-DERIVED VS TEXT NAMES
[BLOCKING, HIGH PRIORITY]

Problem:
OBJECTS.md §7 defines hash-derived stream_id = H(principal_id || signing_key_id
|| stream_context || epoch), with key-authorization records and varint
encoding. PROTOCOL.md §45.1 defines text stream names: stream:identity,
stream:reachability:<device_id>, etc. These models are incompatible. Choice
affects IdentityContinuity (C1), chain base derivation (C2), rendezvous
serialization, and wire protocol.

Option A: Text names, qualified by role key ID

  stream:identity:<root_key_id>
  stream:relationship:<relationship_id>  (if D-07 Option A accepted)
  stream:authorization:<authorization_key_id>
  stream:reachability:<device_id>
  stream:service:<service_id>

  Pros:
    - Human-readable, debuggable logs and diagnostics.
    - Simpler to implement: no hash computation, no epoch management.
    - Supports IdentityContinuity: predecessor and successor streams have
      different root_key_ids and therefore different stream names.

  Cons:
    - Identifier length grows with role key IDs (roughly 20 bytes hex each).
    - Rendezvous lookup must parse the qualified form or store multiple
      entries; a hash would compress.
    - Adds Unicode/ASCII identifier rules (§5.2).

Option B: Hash-derived with epoch, varint encoding

  stream_id = H(principal_id || signing_key_id || stream_context || epoch)
  Varint encoding of the hash for transport.
  Epoch counter for rotation without hash collision.

  Pros:
    - Compact: 32-byte hash → 4–5 bytes in varint form.
    - Rendezvous queries and storage are simple: all streams for one
      principal hash to a short key.
    - Epoch explicitly handles key rotation.

  Cons:
    - Hash encoding adds a second encoding rule (varint) on top of CBOR.
      The spec forbids non-CBOR encoding; this violates §13.1.
    - IdentityContinuity doesn't work: old and new roots have the same
      principal_id, so if stream_context is fixed, they hash to the same
      stream_id. If stream_context changes, the epoch field is redundant.
    - Debugging is harder: logs show hashes, not roles.

Recommendation:
Accept Option A (text names, qualified). Addresses C1 directly. Adds
identifiers per §5.2 (ASCII, max 128 bytes). Update PROTOCOL.md §45.1 and
OBJECTS.md §7 to use this model everywhere. Delete varint encoding.

Consequences:
  - §5.2: Add identifier restrictions (ASCII, length limit).
  - §13.2: Update chain base to stream_class + stream_id (D-02).
  - All wire protocol and rendezvous examples use text names.
  - Test vectors: include stream_id in every object.

================================================================================
