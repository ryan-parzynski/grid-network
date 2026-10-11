---
title: "Grid Network — Object identity and reference stability"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-18
severity: Med
blocks: V1.1
linked_finding: H6
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-18

> **Status:** PROPOSED — NOT ACCEPTED.



## Context / Problem

§13.2 defines object_id = SHA256(canonical_signed_object_bytes), hashing the
exact bytes including the signature. But Ed25519 signatures are deterministic
under RFC 8032, so the same private key and input produce the same signature;
however, D-13 (Ed25519 strictness) raises a concern: is it possible for the
same payload to have two different valid signatures under the same key due to
ambiguity in the verification process? If so, object_id is non-unique. H7
flags this.

## Options considered

Option A: Use object_commitment for references; object_id is storage-only
[PROPOSED in §13.2]

  object_commitment = SHA256(...unsigned_payload) identifies the content.
  object_id = SHA256(signed_bytes) remains for deduplication in storage, but
  protocol-level references (revocations, API calls, cross-references) use
  object_commitment.

  Pros:
    - object_commitment is stable per unsigned_payload (content-addressed).
    - object_id remains usable for storage deduplication.
    - No ambiguity: one content = one commitment.

  Cons:
    - Two identifier types; implementers must not confuse them.
    - API must change (grid.revoke takes object_commitment, not object_id).

Option B: Remove object_id entirely; use only object_commitment

  object_id is not defined or used in the protocol.

  Pros:
    - One identifier type: simpler.
    - Definitely stable (content-addressed).

  Cons:
    - Storage deduplication is less explicit (implementer responsibility).

## Recommendation (PROPOSED — NOT DECIDED)

> **PROPOSED:**

Accept Option A (object_commitment for references; object_id storage-only).
Update the local API (D-10) and all cross-reference examples to use
object_commitment.

## Consequences

- §13.2: clarify object_commitment as the protocol identifier.
  - §17: grid.revoke(object_commitment) instead of grid.revoke(object_id).
  - Test vectors: object_commitment values and verification.
  - D-13 (strictness) should prove that Ed25519 signatures are deterministic
    even under strict rules (they are, per RFC 8032).



================================================================================
PART V — OPEN DECISIONS D-19 THROUGH D-26
================================================================================
