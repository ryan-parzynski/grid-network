# Grid Network — Conformance

**Revision:** 2.2
**Protocol version:** v0.6.3

**Repository path:** `spec/CONFORMANCE.md`

This document defines what it means for an implementation to conform to
the protocol. It defines conformance levels, test vector format,
conformance scenarios, and the production sequence for the vector
suite. It is normative with respect to what conformance means; it is
descriptive with respect to vectors that do not yet exist.

---

## 1. What conformance means

An implementation conforms to protocol version v0.6.3 if it satisfies
the requirements of `PROTOCOL.md §43` and passes the test vectors and
conformance scenarios defined in this document.

Conformance is defined by test vectors. If prose and a vector disagree,
the specification is corrected so they agree.

Conformance is not a security certification. It is not an
interoperability certification. It is not an operational audit. It is
an assertion that an implementation produces the behavior this
specification defines.

The terms "Grid-compatible" and "Grid-inspired" have no conformance
meaning.

---

## 2. Conformance levels

Levels are cumulative. An implementation at Level N satisfies Levels 1
through N for the object types and behaviors it claims to support.

### Level 1 — Basic cryptographic constructions

Tests canonical CBOR encoding, Ed25519 signatures, SHA-256 hashing, and
domain separator correctness.

A passing implementation:

- Encodes a given semantic value to a single canonical byte string.
- Verifies Ed25519 signatures against the correct signature input.
- Computes chain hashes per `OBJECTS.md §3.8`.
- Uses the correct domain tag for each construction.

### Level 2 — Object structure

Tests validation of each object type.

A passing implementation:

- Rejects malformed objects at the appropriate rejection class.
- Accepts well-formed objects whose signatures verify.
- Validates schema-specific fields.

### Level 3 — Stream processing

Tests sequence monotonicity, chain hash correctness, fork detection,
and fork resolution.

A passing implementation:

- Rejects an object whose `previous_hash` does not match the accepted
  predecessor.
- Detects a fork when two objects at the same sequence have different
  `chain_hash` values.
- Refuses to advance authorization for a forked stream until a valid
  `StreamResolution` is accepted.
- Accepts a fork resolution whose signatures satisfy the pre-fork
  authority requirement.

### Level 4 — Authorization logic

Tests grant and lease evaluation.

A passing implementation:

- Authorizes a peer with a valid grant and a valid lease.
- Denies a peer with no grant.
- Denies a peer whose lease has expired.
- Denies a peer whose grant has been revoked.
- Denies a peer whose signing key has been revoked at or after
  `effective_sequence`.
- Allows a peer whose signing key was revoked at a later sequence, if
  the verifier has an accepted predecessor chain for the object.

### Level 5 — Edge cases

Tests clock skew, offline tolerance, and infrastructure unavailability.

A passing implementation:

- Authorizes a lease whose relative validity survives clock skew up to
  the lease duration.
- Denies a peer whose `max_offline_tolerance` has been exceeded.
- Denies a peer whose device has been revoked from `device_bindings`.
- Denies a peer whose relationship has been terminated.
- Uses cached reachability when rendezvous is unavailable.
- Tries an alternative relay when the primary relay rejects the ticket.

### Level 6 — Security

Tests resistance to forgery and bypass.

A passing implementation:

- Rejects a signature that does not verify.
- Rejects a grant signed by a key other than the authorized
  Authorization Key.
- Rejects an object whose `chain_hash` does not match the stream.
- Rejects an `IdentityContinuity` object signed by only one root.
- Rejects a `StreamResolution` lacking a required authority signature.

---

## 3. Test vector format

A test vector is a JSON object with the following fields.

### 3.1 Positive vectors

    {
      "name": "identity-document-seq1-basic",
      "version": "0.6.2",
      "type": "positive",
      "description": "Minimal identity document, sequence 1",
      "input": {
        "peer_id": "peer:v1:...",
        "identity_root": "<hex>",
        "authorized_keys": [ { "key_role": "device", "public_key": "<hex>", "effective_sequence": 1 } ],
        "device_bindings": [],
        "service_bindings": [],
        "issued_at": 1705312800,
        "not_before": 1705312800
      },
      "canonical_cbor": "<hex>",
      "expected": {
        "payload_id": "sha256:<hex>",
        "object_id": "sha256:<hex>",
        "chain_hash": "sha256:<hex>"
      },
      "signature": "ed25519:<hex>",
      "steps": [
        "Parse canonical CBOR",
        "Validate envelope",
        "Validate domain separator",
        "Validate schema",
        "Validate sequence",
        "Compute object_commitment",
        "Compute chain_hash",
        "Recompute payload_id",
        "Recompute signature_input",
        "Verify signature"
      ],
      "reference": "PROTOCOL §7, OBJECTS §7.2"
    }

### 3.2 Negative vectors

    {
      "name": "identity-document-tampered-signature",
      "version": "0.6.2",
      "type": "negative",
      "description": "Identity document with one byte of the signature changed",
      "canonical_cbor": "<hex>",
      "modification": "Flipped bit 0 of byte 10 of signature",
      "expected_rejection": "INVALID_SIGNATURE",
      "reference": "OBJECTS §8 Step 8"
    }

### 3.3 Required coverage

Every object type requires at least one positive vector and three
negative vectors.

Negative vectors must cover at least:

- Malformed encoding.
- Invalid signature.
- Broken chain (chain hash or previous hash mismatch).
- One schema-specific failure per object type.

### 3.4 Parameters in vectors

Every vector that depends on a tunable value carries the value in its
`input` block. A vector must not rely on a default from
`spec/PARAMETERS.md`; it must state its parameters. This makes the
vector portable across deployments.

---

## 4. Conformance scenarios

Scenarios describe end-to-end behaviors. Each scenario names the setup,
the action, the expected outcome, and the properties the implementation
must exhibit.

### C1 — Basic pairing

**Given** two devices with no prior relationship.
**When** the user completes pairing per `PROTOCOL §21`.
**Then** both devices accept a `RelationshipAssertion` from the other.
**Verify** the relationship state transitions to RECOGNIZED.

### C2 — Grant issuance

**Given** two devices in a RECOGNIZED relationship.
**When** Alice issues a grant to Bob for a capability.
**Then** Bob can access the resource covered by the capability.
**Verify** the grant is signed by an Authorization Key and is published
in the correct stream.

### C3 — Lease expiration

**Given** a grant with a valid lease.
**When** the lease's validity period elapses.
**Then** the subject is unauthorized.
**Verify** the verifier rejects the lease based on its validity window.

### C4 — Revocation propagation

**Given** a grant in active use.
**When** the issuer publishes a `GrantRevocation`.
**Then** verifiers that receive the revocation deny access.
**Verify** the revocation is in the identity stream and signed by the
Identity Root.

### C5 — Offline operation

**Given** a subject with a valid grant and lease.
**When** the subject is offline for less than `max_offline_tolerance`.
**Then** the subject can resume on cached state.
**Verify** relative validity survives the offline period.

### C6 — Offline tolerance exceeded

**Given** a grant with `max_offline_tolerance` of a defined duration.
**When** the subject is offline for longer than that duration.
**Then** the subject is unauthorized on return.
**Verify** the verifier rejects based on the tolerance bound.

### C7 — Fork detection

**Given** a stream in normal operation.
**When** two objects at the same sequence with different `chain_hash`
values are observed.
**Then** the verifier marks the stream FORK_DETECTED.
**Verify** authorization is suspended for the forked stream.

### C8 — Fork resolution

**Given** a stream in FORK_DETECTED state.
**When** a valid `StreamResolution` is accepted.
**Then** the stream returns to RECOGNIZED on the accepted branch.
**Verify** the resolution carries signatures from every pre-fork
authority.

### C9 — Identity Root rotation

**Given** a principal with an established Identity Root.
**When** the principal publishes an `IdentityContinuity` object.
**Then** the new root is authoritative.
**Verify** the object is signed by both roots.

### C10 — Device revocation

**Given** an identity document listing two devices.
**When** the principal publishes a new identity document omitting one
device and revoking its key.
**Then** the omitted device cannot sign reachability.
**Verify** the omitted device's reachability records are rejected.

### C11 — Stale rendezvous endpoint

**Given** a reachability record with a stale endpoint.
**When** the verifier attempts to connect.
**Then** the direct connection fails.
**Verify** the verifier tries the next endpoint, then a relay.

### C12 — Relay rejection

**Given** a relay at capacity.
**When** the verifier requests a ticket.
**Then** the relay rejects the request.
**Verify** the verifier tries an alternative relay. The rejection is
treated as an availability failure, not an authorization failure.

### C13 — Clock skew

**Given** a verifier whose clock differs from the issuer's.
**When** the verifier receives a lease with relative validity.
**Then** the lease is valid for its duration from the verifier's
observation.
**Verify** the clock difference does not cause false denial.

### C14 — Relationship termination

**Given** a RECOGNIZED relationship.
**When** either principal publishes a `RelationshipTermination`.
**Then** the relationship transitions to TERMINATED.
**Verify** the state is terminal; a new relationship requires a new
`relationship_id`.

### C15 — Multi-relay fallback

**Given** a reachability record with multiple relay endpoints.
**When** the primary relay is unavailable.
**Then** the verifier tries the next endpoint.
**Verify** the connection succeeds if any endpoint is reachable.

### C16 — Authorization Key compromise

**Given** an Authorization Key in use.
**When** the Identity Root publishes a `KeyRevocation` with an
`effective_sequence`.
**Then** objects signed at or after that sequence are invalid.
**Verify** objects signed before the sequence remain valid if their
chain hash was accepted before the revocation was observed.

### C17 — End-to-end system test

**Given** Alice, Bob, and a service.
**When** Alice pairs with Bob, issues a grant, Bob accesses the service
via relay, Alice revokes the grant, and the lease expires.
**Then** every intermediate state is correct.
**Verify** the state transitions at each step match the specification.

---

## 5. Test vector production sequence

Vectors are produced in seven groups. Each group builds on the previous.

| Group | Coverage | Vector count (minimum) |
|---|---|---|
| A | Basic crypto: canonical CBOR, Ed25519, SHA-256, domain separators | 2 |
| B | Identity: `IdentityDocument`, `KeyBinding`, `DeviceBinding`, `ServiceBinding` | 4 |
| C | Relationships: `RelationshipAssertion`, `RelationshipTermination` | 3 |
| D | Authorization: `Grant`, `Lease`, `GrantRevocation`, `LeaseRevocation` | 6 |
| E | Reachability: `ReachabilityRecord`, `Endpoint` | 3 |
| F | Negative vectors, at least three per positive | 54 |
| G | Conformance scenarios C1–C17 | 17 |

Minimum total: 89 vectors.

A group is complete when all of its positive vectors and their negative
counterparts are present and validate against the canonical
constructions in `OBJECTS.md`.

---

## 6. Test vector repository layout

    spec/test-vectors/v0.6.3/
    ├── README.md
    ├── positive/
    │   ├── identity-document/
    │   ├── relationship-assertion/
    │   ├── grant/
    │   ├── lease/
    │   ├── reachability-record/
    │   ├── service-record/
    │   └── relay-ticket/
    ├── negative/
    │   ├── identity-document/
    │   ├── relationship-assertion/
    │   ├── grant/
    │   ├── lease/
    │   ├── reachability-record/
    │   ├── service-record/
    │   └── relay-ticket/
    └── scenarios/
        └── C1 through C17

Each vector file is named after the object type and a short
description: `grant-basic-validity.json`,
`grant-expired-lease.json`, and so on.

---

## 7. What a passing implementation exhibits

An implementation that passes all levels and all scenarios:

- Produces byte-exact output for every positive vector.
- Rejects every negative vector with the specified rejection class.
- Handles every conformance scenario per its specification.
- Preserves the core security invariant in `PROTOCOL.md §1`.

An implementation that passes some levels is conformant at that level
for the object types it supports. It may claim "conforms to Grid
Network v0.6.3 Level N" but not "conforms to Grid Network v0.6.3" in
full.