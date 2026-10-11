## §2: CANONICAL CBOR PROFILE

All protocol objects use CBOR (RFC 8949) with deterministic encoding constraints.

### 2.1 Allowed major types

| Major type | Allowed | Notes |
|------------|---------|-------|
| 0 — unsigned integer | Yes | §2.2 |
| 1 — negative integer | No | Protocol values are non-negative |
| 2 — byte string | Yes | §2.3 |
| 3 — text string | Yes | §2.4 |
| 4 — array | Yes | §2.5 |
| 5 — map | Yes | §2.6, §2.7 |
| 6 — tag | No | Protocol uses no CBOR tags |
| 7 — simple/float | Partial | Only null (0xf6) and booleans |

Any object containing a major type not listed above is malformed.

### 2.2 Integer representation

Integers MUST be encoded in their shortest form. Non-shortest integer encodings are malformed.
Permitted ranges: non-negative integers 0 to 2^64 − 1. Negative integers are not permitted.

### 2.3 Byte strings

Byte strings MUST be definite-length. Indefinite-length byte strings are malformed. Byte string length MUST be encoded in the shortest form.

### 2.4 Text strings

Text strings MUST be definite-length and MUST be valid UTF-8. Text strings MUST use Unicode Normalization Form C (NFC). Text strings that are not in NFC are malformed. Byte-order mark (U+FEFF) MUST NOT appear at the beginning of a text string.

### 2.5 Arrays

Arrays MUST be definite-length. Array schemas MUST explicitly specify whether duplicate elements are permitted. Unless a schema explicitly permits duplicates, duplicate elements are malformed.

### 2.6 Maps

Maps MUST be definite-length. Indefinite-length maps are malformed. Map keys MUST be unique. Maps containing duplicate keys are malformed. Map keys MUST be text strings unless the map's schema explicitly permits other key types. Protocol map keys are always text strings.

### 2.7 Map key ordering

Map keys MUST be ordered according to CBOR deterministic encoding (RFC 8949 §4.2.1):
1. First by the length of the encoded key (shorter first)
2. Then by bytewise lexicographic comparison of the encoded key bytes

This is the **length-first core deterministic encoding** (RFC 8949 §4.2.3), NOT the core deterministic encoding of §4.2.1 (which uses bytewise lexicographic ordering of the encoded key bytes). Non-canonical map ordering is malformed.

### 2.8 Set semantics

A protocol set<T> is encoded as a definite-length CBOR array whose elements are:
1. Unique — no two elements have identical canonical CBOR encodings
2. Sorted — elements are ordered by bytewise lexicographic comparison of their canonical CBOR encodings

An array that represents a set<T> but contains duplicate elements, or whose elements are not in the required order, is malformed. An empty set is encoded as an empty definite-length array.

### 2.8.1 Collection ordering distinction

Two distinct ordering semantics exist in the protocol:
- **Map key ordering (§2.7):** Map keys are ordered by the length-first core deterministic encoding (RFC 8949 §4.2.3): shorter encoded keys first, then bytewise lexicographic.
- **Set element ordering (§2.8):** Set elements are ordered by bytewise lexicographic comparison of their complete canonical CBOR encodings (no length prefix).

These are different orderings. A map's key order MUST NOT be inferred from set ordering rules, and vice versa.

### 2.9 Null and optional fields

null (CBOR 0xf6) is permitted only where an object schema explicitly declares a field as **optional-and-absent** AND explicitly permits null as a valid value. When a field is optional-and-absent, the field key MUST be omitted from the map, not set to null. An explicit null value is malformed unless a schema explicitly requires it. Boolean values (false = 0xf4, true = 0xf5) are permitted where a schema declares a boolean field.

**Terminology clarification:**
- **optional-and-absent:** The field may be omitted from the map. If present, it MUST NOT be null (unless the schema explicitly permits null as a value).
- **optional-and-nullable:** The field may be omitted, or present with a null value, or present with a non-null value. The schema MUST explicitly declare this.
- **required:** The field MUST be present with a non-null value.

Schemas MUST declare each field as exactly one of: required, optional-and-absent, or optional-and-nullable.

### 2.10 Floating-point prohibition

Floating-point values (major type 7, additional info 25–27) are prohibited. Any floating-point value is malformed. All numeric values in protocol objects are integers. Time values are represented as integer seconds (or integer milliseconds where a schema explicitly requires sub-second precision).

### 2.11 Indefinite-length prohibition

Indefinite-length encoding of byte strings, text strings, arrays, and maps is prohibited. All four MUST use definite-length encoding.

### 2.12 Duplicate-key prohibition

Maps MUST NOT contain duplicate keys. Sets MUST NOT contain duplicate elements. Arrays that are not sets MAY contain duplicate values if the schema permits; protocol arrays that carry lists of distinct values are declared as sets.

### 2.13 Integer bounds

All integers MUST fall within the range specified in §2.2. Schemas MAY impose narrower bounds; values outside a schema's bounds are malformed.

### 2.14 Rejection of non-canonical encodings

Any CBOR encoding that does not satisfy §2.1–§2.13 is malformed. Implementations MUST reject malformed encodings before any semantic processing.

---

## §3: OBJECT SERIALIZATION

### 3.0 Notation

- `canonical_cbor(V)` — the byte string produced by encoding CBOR value V according to §2
- `SHA-256(B)` — the SHA-256 hash of byte string B, producing a 32-byte value
- `Ed25519_sign(K, B)` — the Ed25519 signature over byte string B using private key K, producing a 64-byte value
- `Ed25519_verify(P, B, S)` — verification of signature S over byte string B using public key P
- `||` — byte string concatenation

### 3.1 Value/byte distinction

Protocol constructions operate on two kinds of input:
- CBOR values — the abstract data structures
- Byte strings — the output of `canonical_cbor` or of hashing

The distinction is critical. In all definitions below:
- An operand described as a CBOR value is used as a value and is canonically encoded as part of the surrounding structure
- An operand described as a byte string is used as bytes and is encoded as a CBOR byte string when placed inside a surrounding CBOR structure

### 3.2 Unsigned payload

The unsigned payload of an object is the CBOR map containing all fields defined by the object schema, including common stream fields such as `domain_separator`, `sequence`, and `previous_hash` where the schema includes them. It excludes only two fields:
- `chain_hash`, which is derived from the unsigned payload and the stream state
- `signature`, which is derived from the unsigned payload and the chain hash

All other object fields are part of the unsigned payload.

### 3.3 Commitment preimage

```
commitment_preimage =
    canonical_cbor([
        "grid/commitment/v1",
        domain_separator,
        unsigned_payload
    ])
```

Where:
- Element 0 is the text string `"grid/commitment/v1"`
- Element 1 is the object's `domain_separator` as a text string
- Element 2 is the unsigned payload as a CBOR value

The commitment preimage is a byte string.

### 3.4 Object commitment

```
object_commitment =
    SHA-256(commitment_preimage)
```

The object commitment is a byte string (32 bytes).

### 3.5 Chain state, previous hash, and chain hash

Every stream has a base state represented by initial_chain_hash.

```
initial_chain_hash =
    SHA-256(canonical_cbor([
        "grid/chain-base/v1",
        domain_separator,
        stream_id
    ]))
```

Two distinct chain links exist. They serve different purposes and MUST NOT be conflated.

**Previous hash (previous_hash):** commits directly to the immediately preceding object's payload. It is an object field.

```
previous_hash(1) = omitted                    (not present)
previous_hash(N) = object_commitment(N-1)     for N > 1
```

**Previous chain hash (previous_chain_hash):** the input to the chain construction. It is not an object field.

```
previous_chain_hash(1) = initial_chain_hash
previous_chain_hash(N) = chain_hash(N-1)      for N > 1
```

**Chain hash (chain_hash):** the cumulative stream-history hash. It is an object field.

```
chain_hash(N) =
    SHA-256(canonical_cbor([
        "grid/chain/v1",
        previous_chain_hash(N),
        object_commitment(N)
    ]))
```

Where:
- Element 0 is the text string "grid/chain/v1"
- Element 1 is previous_chain_hash(N) as a CBOR byte string
- Element 2 is object_commitment(N) as a CBOR byte string

The first object in every stream has sequence = 1. The value 0 is reserved for "uninitialized" and MUST NOT appear.

**Sequence-1 chain initialization:** For the first object in any stream (sequence = 1), the chain_hash is computed using the standard chain construction with previous_chain_hash(1) = initial_chain_hash. The chain_hash field of a sequence-1 object is therefore:

```
chain_hash(1) = SHA-256(canonical_cbor([
    "grid/chain/v1",
    initial_chain_hash,
    object_commitment(1)
]))
```

This is the ordinary sequence-1 chain hash. It is NOT equal to initial_chain_hash. The initial_chain_hash is the base state; chain_hash(1) is the first cumulative hash incorporating the first object's commitment.


### 3.6 Payload ID

```
payload_id =
    SHA-256(canonical_cbor([
        "grid/payload-id/v1",
        unsigned_payload
    ]))
```

The payload ID depends only on the semantic content of the unsigned payload.

### 3.7 Object ID

```
object_id =
    SHA-256(canonical_cbor([
        "grid/object-id/v1",
        canonical_signed_object_bytes
    ]))
```

Where `canonical_signed_object_bytes` is the exact canonical CBOR encoding of the signed object — the byte-for-byte wire representation. It is not a CBOR value; it is a byte string in this construction.

Implementations MUST NOT re-encode the signed object as a CBOR value before hashing.

### 3.8 Signed object

A signed object is a CBOR map containing all fields of the unsigned payload, plus:
- `chain_hash` — a byte string
- `signature` — a byte string (or two-element array of byte strings for dual-signature schemas)

The signed object is a CBOR value.

### 3.9 Signature input

```
signature_input(N) =
    canonical_cbor([
        "grid/signature/v1",
        domain_separator,
        unsigned_payload,
        chain_hash(N)
    ])
```

The signature is computed as:

```
signature(N) =
    Ed25519_sign(signing_private_key, signature_input(N))
```

**Non-circularity:** The signature input MUST be reconstructible from the unsigned payload and the chain hash alone. The signature MUST NOT be part of any input to its own computation.

### 3.10 Serialization invariants

**S1 — Canonical form.** Two objects that represent the same protocol value MUST have identical canonical CBOR encodings.

**S2 — Signature domain separation.** Every cryptographic construction has a unique domain tag:

| Tag | Construction |
|-----|--------------|
| `"grid/commitment/v1"` | `commitment_preimage` |
| `"grid/chain-base/v1"` | `initial_chain_hash` |
| `"grid/chain/v1"` | `chain_hash` |
| `"grid/signature/v1"` | `signature_input` |
| `"grid/payload-id/v1"` | `payload_id` |
| `"grid/object-id/v1"` | `object_id` |

**S3 — Chain order.** The chain hash of sequence N depends on the chain hash of sequence N-1 and the object commitment of sequence N.

**S4 — Determinism.** All constructions are deterministic functions of their inputs.

**S5 — Byte/value boundary.** The distinction between CBOR values and byte strings is normative in every construction.

**S6 — Reconstruction.** Every derived value required for verification MUST be reconstructible from the canonical unsigned payload, applicable stream state, and the protocol rules. An implementation MUST NOT depend on non-canonical source representations, parser-preserved formatting, map insertion order, or locally generated serialization choices.

---

## §4: COMMON STREAM ENVELOPE

### 4.1 Purpose

Every signed object shares a common structural envelope. §4 defines the fields of that envelope and the boundary between envelope fields and object-specific fields.

### 4.2 Envelope overview

```
signed_object = {
    domain_separator    : text string,
    sequence            : integer >= 1,
    previous_hash?      : byte string (omitted at sequence 1),
    ...schema-specific fields,
    chain_hash          : byte string,
    signature           : byte string (or 2-element array)
}
```

### 4.3 Field definitions

#### 4.3.1 domain_separator

Type: CBOR text string. The `domain_separator` identifies the object's schema family and version. It is drawn from the registered set (§4.5). The `domain_separator` is part of `unsigned_payload`. It is included in `commitment_preimage`, `payload_id`, and `signature_input`.

There is no separate version field in the envelope. The schema version is carried by `domain_separator`.

#### 4.3.2 sequence

Type: CBOR unsigned integer. Range: 1 to 2^64 − 1. The value 0 is reserved for "uninitialized" and MUST NOT appear in any signed object.

#### 4.3.3 previous_hash

Type: CBOR byte string (32 bytes). Optional; present only at sequence numbers greater than 1. At sequence 1, the field is omitted. It MUST NOT be present with a null value. A sequence-1 object that contains a `previous_hash` field is malformed.

Not to be confused with `previous_chain_hash`. The chain construction uses a value called `previous_chain_hash`, which is not a field of any object.

| Value | What it is | Where it lives |
|-------|------------|----------------|
| `previous_hash` | previous object's `object_commitment` | a field (omitted at sequence 1) |
| `previous_chain_hash` | previous object's `chain_hash` (or `initial_chain_hash`) | computed input; not a field |

#### 4.3.4 chain_hash

Type: CBOR byte string (32 bytes). Added to the object after `unsigned_payload` is complete. Computed per §3.5.

#### 4.3.5 signature

Type: CBOR byte string (64 bytes) for single-signature schemas; definite-length CBOR array of exactly two 64-byte byte strings for dual-signature schemas.

For dual-signature schemas, `signature` is a CBOR array `[signature_0, signature_1]` where ordering is defined by the schema. The array MUST be definite-length and MUST contain exactly two elements. For dual-signature schemas, both signatures MUST be over the same `signature_input`.

#### 4.3.6 Schema-specific fields

Every object schema defines the schema-specific fields that appear in `unsigned_payload`, in addition to the common envelope fields.

### 4.4 Envelope invariants

**E1.** `domain_separator` MUST be present.
**E2.** `sequence` MUST be present and ≥ 1.
**E3.** `previous_hash` MUST be omitted at sequence 1 and present at sequence numbers greater than 1.
**E4.** `chain_hash` MUST be present.
**E5.** `signature` MUST be present.
**E6.** `unsigned_payload` MUST NOT contain any field named `chain_hash` or `signature`.
**E7.** The signed object MUST NOT contain any field outside the set of `unsigned_payload` fields plus `chain_hash` and `signature`.

### 4.5 Registered domain separators

| Domain separator | Object |
|------------------|--------|
| `"grid/identity-document/v1"` | IdentityDocument |
| `"grid/device-binding/v1"` | DeviceBinding |
| `"grid/service-binding/v1"` | ServiceBinding |
| `"grid/key-binding/v1"` | KeyBinding |
| `"grid/key-revocation/v1"` | KeyRevocation |
| `"grid/relationship-assertion/v1"` | RelationshipAssertion |
| `"grid/relationship-termination/v1"` | RelationshipTermination |
| `"grid/rendezvous-manifest/v1"` | Principal RendezvousManifest |
| `"grid/operator-manifest/v1"` | OperatorManifest |
| `"grid/relationship-grant/v1"` | Grant |
| `"grid/authorization-lease/v1"` | Lease |
| `"grid/grant-revocation/v1"` | GrantRevocation |
| `"grid/lease-revocation/v1"` | LeaseRevocation |
| `"grid/service-record/v1"` | ServiceRecord |
| `"grid/reachability-record/v1"` | ReachabilityRecord |
| `"grid/stream-resolution/v1"` | StreamResolution |
| `"grid/identity-continuity/v1"` | IdentityContinuity |
| `"grid/relay-ticket/v1"` | RelayTicket |
| `"grid/relay-node-record/v1"` | RelayNodeRecord |

Registry rules:
- Domain separators are ASCII text strings
- Each value identifies exactly one object schema family and version
- A future schema version of the same family MUST use a distinct domain separator
- Unknown domain separators MUST be rejected

---

## §5: SIGNATURE SEMANTICS AND VERIFICATION

### 5.1 Purpose

§5 defines which key role is authorized to sign each object type, and the single authoritative verification procedure for all objects.

### 5.2 Signing-authority assignment

| Object | Authorized signer |
|--------|-------------------|
| IdentityDocument | Identity Root |
| DeviceBinding | Identity Root (or delegated device-authority key) |
| ServiceBinding | Identity Root (or delegated service-authority key) |
| KeyBinding | Identity Root |
| KeyRevocation | Identity Root |
| RelationshipAssertion | One principal's Identity Root (the issuer) |
| RelationshipTermination | One principal's Identity Root (the terminating principal) |
| Principal RendezvousManifest | Principal's Identity Root |
| OperatorManifest | Operator's Identity Root |
| Grant | Authorization Key |
| Lease | Authorization Key |
| GrantRevocation | Authorization Key |
| LeaseRevocation | Authorization Key |
| ServiceRecord | Service Key |
| ReachabilityRecord | Device Key |
| StreamResolution | Pre-fork authority above the disputed stream |
| IdentityContinuity | Both previous and new Identity Roots (dual signature) |
| RelayTicket | Relay Authority Key |
| RelayNodeRecord | Relay Node Key |

### 5.3 Verification procedure (atomic, mutation-free)

When a verifier receives an object, it MUST execute the following procedure. Steps 1–11 are **validation phases** — the verifier MUST NOT advance or mutate its accepted stream state during these phases. Validation is pure with respect to accepted state; commitment (step 12) is the only mutation.

**Step 1: Parse CBOR**
- Decode the input as CBOR.
- Verify it is in canonical form per §2.
- If invalid or non-canonical: REJECT as `MALFORMED_ENCODING`.

**Step 2: Validate envelope structure**
- Verify all required envelope fields are present: `domain_separator`, `sequence`, `chain_hash`, `signature`.
- Verify `sequence` ≥ 1.
- Verify `previous_hash` is absent when `sequence == 1` and present when `sequence > 1`.
- Verify no unknown fields exist (E7).
- If any check fails: REJECT as `MALFORMED_ENVELOPE`.

**Step 3: Validate domain separator**
- Verify `domain_separator` is a registered value (§4.5).
- If not registered: REJECT as `UNKNOWN_SCHEMA`.

**Step 4: Validate schema-specific fields**
- Validate all schema-specific fields per the object's schema (§6).
- If validation fails: REJECT as `MALFORMED_SCHEMA`.

**Step 5: Validate sequence and previous_hash consistency**
- Verify `sequence` ≥ 1.
- Verify `previous_hash` presence matches sequence (absent at 1, present at >1).
- If `sequence > 1`, verify `previous_hash` is a 32-byte byte string.
- If any check fails: REJECT as `INVALID_SEQUENCE` or `INVALID_PREVIOUS_HASH` respectively.

**Step 6: Reconstruct and verify chain linkage**
- Reconstruct `unsigned_payload` = signed object minus `{chain_hash, signature}`.
- Compute `commitment_preimage` = `canonical_cbor(["grid/commitment/v1", domain_separator, unsigned_payload])`.
- Compute `object_commitment` = `SHA-256(commitment_preimage)`.
- If `sequence == 1`: expected `previous_chain_hash` = `initial_chain_hash` (computed per §3.5).
- If `sequence > 1`: expected `previous_chain_hash` = the accepted `chain_hash` of sequence-1 in this stream.
- Verify `previous_hash` (if present) equals `object_commitment(sequence-1)`.
- Compute `chain_hash` = `SHA-256(canonical_cbor(["grid/chain/v1", previous_chain_hash, object_commitment]))`.
- Verify computed `chain_hash` equals the object's `chain_hash` field.
- If any check fails: REJECT as `CHAIN_MISMATCH`.

**Step 7: Reconstruct signature input**
- Compute `signature_input` = `canonical_cbor(["grid/signature/v1", domain_separator, unsigned_payload, chain_hash])`.

**Step 8: Verify signature(s)**
- Determine the expected signing public key per §5.2 and the current accepted authority state.
- For single-signature schemas: verify `Ed25519_verify(public_key, signature_input, signature)`.
- For dual-signature schemas (`IdentityContinuity`): verify both signatures against the same `signature_input` using `previous_root` and `new_root` respectively.
- If verification fails: REJECT as `INVALID_SIGNATURE`.

**Step 9: Validate signing authority**
- Verify the signing key's role matches the authorized signer for this object type (§5.2).
- Verify the key is currently authorized (not revoked, not superseded beyond its effective sequence).
- If authority validation fails: REJECT as `UNAUTHORIZED_SIGNER`.

**Step 10: Validate temporal and revocation state**
- Verify `issued_at` ≤ current time + `MAX_CLOCK_SKEW` (5 minutes).
- Verify `not_before` ≤ current time + `MAX_CLOCK_SKEW` (or object is not yet effective).
- Verify `expires_at` > current time - `MAX_CLOCK_SKEW` (or object is expired).
- Verify no applicable revocation invalidates this object (key revocation, grant revocation, lease revocation, relationship termination).
- If any check fails: REJECT as `EXPIRED`, `NOT_YET_VALID`, `REVOKED`, or `TERMINATED` respectively.

**Step 11: Validate semantic rules**
- Apply the object-type-specific semantic rules (§6–§8, §54).
- For `StreamResolution`: verify resolution authority, fork position, hash selection, monotonicity.
- For `IdentityContinuity`: verify sequence=1, omitted previous_hash, chain_hash matches successor initial_chain_hash, dual signatures, trust chain, predecessor chain_hash match, no duplicate successor stream, not expired.
- For authorization objects (Grant, Lease): verify relationship is `RECOGNIZED`, grant is `GRANTED`, key is `ACTIVE`/`SUPERSEDED`, no revocation applies, offline tolerance not exceeded.
- If any semantic rule fails: REJECT as `SEMANTIC_VIOLATION`.

**Step 12: Commit**
- If all steps 1–11 pass: ACCEPT the object.
- Atomically update the verifier's accepted state for the relevant stream and any derived state (relationship, grant, lease, chain state).
- The object is now part of the accepted state.

### 5.4 Delegated signers

`DeviceBinding` MAY be signed by a device-authority key delegated by the Identity Root. `ServiceBinding` MAY be signed by a service-authority key. Delegations MUST be present in the verifier's accepted identity state.

### 5.5 Dual-signature objects

Only `IdentityContinuity` uses dual signatures in V1.

For `IdentityContinuity`:
```
signature: [
    sig_prev,   // by previous_root
    sig_new     // by new_root
]
```

Both signatures are over the same `signature_input`.

### 5.6 StreamResolution signing

A `StreamResolution` MUST be signed by an authority above the disputed stream in the authority hierarchy, trusted from state accepted **before** the fork was observed. The resolver's stream position is expressed by the resolution object's own `sequence`, `chain_hash`, and `previous_hash`. The disputed stream's position is expressed by `disputed_sequence`, a value that MUST NOT be compared with the resolution's `sequence`.

### 5.7 Rejection classes

When verification fails, the verifier MUST classify the failure into exactly one of the following classes. Classes are ordered by precedence — the first matching class applies.

| Class | Meaning | When raised (step) |
|-------|---------|-------------------|
| `MALFORMED_ENCODING` | Input is not valid canonical CBOR | Step 1 |
| `MALFORMED_ENVELOPE` | Envelope fields missing, mistyped, unknown fields present, or E1–E7 violated | Step 2 |
| `UNKNOWN_SCHEMA` | `domain_separator` not registered | Step 3 |
| `MALFORMED_SCHEMA` | Schema-specific fields fail validation | Step 4 |
| `INVALID_SEQUENCE` | `sequence` is 0 or otherwise invalid | Step 5 |
| `INVALID_PREVIOUS_HASH` | `previous_hash` presence/type does not match sequence | Step 5 |
| `CHAIN_MISMATCH` | `previous_hash` or `chain_hash` does not match stream state | Step 6 |
| `INVALID_SIGNATURE` | Signature does not verify | Step 8 |
| `UNAUTHORIZED_SIGNER` | Signing key role is not authorized or key is revoked/superseded | Step 9 |
| `EXPIRED` | Object timestamp check failed (expired) | Step 10 |
| `NOT_YET_VALID` | Object `not_before` in the future | Step 10 |
| `REVOKED` | Object invalidated by key revocation, grant revocation, or lease revocation | Step 10 |
| `TERMINATED` | Relationship terminated by accepted `RelationshipTermination` | Step 10 |
| `SEMANTIC_VIOLATION` | Object-type-specific semantic rule violated | Step 11 |

**Precedence note:** Steps execute sequentially. The first rejection encountered determines the class. An object that is both `MALFORMED_ENCODING` and `INVALID_SIGNATURE` is classified as `MALFORMED_ENCODING` because step 1 fails before step 8 is reached.

---

## §6: OBJECT SCHEMAS

[Unchanged — placeholder for object schemas]

---

## §7: STREAM IDENTITY

### Stream Identity

**Core Concepts**

| Term | Definition |
|------|------------|
| **principal_id** | Globally unique identifier for the entity (human, service, device) that originates or controls the stream. Immutable for the lifetime of the principal.
| **signing_key_id** | Identifier for a specific public key used to sign stream frames. Bound to a principal via a *key authorization record*. Rotatable; multiple keys may be active concurrently.
| **stream_id** | Deterministic identifier for a logical data stream. Derived as `stream_id = H(principal_id || signing_key_id || stream_context || epoch)` where `H` is the protocol hash function, `stream_context` is an application-defined namespace, and `epoch` is the generation counter.
| **stream_epoch** | Monotonically increasing generation counter for a given (principal, signing_key, stream_context) tuple. Starts at 0; increments on key rotation, re-keying, or explicit rebinding. Encoded as a varint.
| **issuer** | The principal that *authorizes* a signing_key for use with a specific stream_context. May equal the principal (self-issued) or be a distinct delegating authority. Recorded in the key authorization record.
| **stream_context** | Application-scoped namespace string (e.g., "grid.msg.v1", "grid.fs.v2/logs") that disambiguates streams sharing the same principal and signing key. Chosen by the issuer at stream creation.

**Derivation**

```
stream_id = hash(principal_id || signing_key_id || stream_context || encode_varint(stream_epoch))
```

The `stream_id` is stable within an epoch. Changing any input produces a new `stream_id`, which signals a new logical stream to routers and verifiers.

**Key Authorization Record**

A signed structure published by the issuer binding `(principal_id, signing_key_id, stream_context, epoch)` with validity windows and revocation flags. Verifiers fetch this record to confirm that a signing key is authorized for the claimed stream.

**Identity Refresh**

When `stream_epoch` increments, the issuer publishes a new key authorization record. The old `stream_id` remains verifiable for its validity window; the new `stream_id` takes over for subsequent frames. Continuity is proven via the epoch chain in the authorization records — **not** by hashing frame payloads (see PROTOCOL.md §Stream Resolution).

---
*Missing schema bindings (flagged for SCHEMA.md):*
- KeyAuthorizationRecord wire format
- stream_context encoding rules (length, charset)
- epoch varint encoding (which varint spec)
- issuer delegation chain representation
- principal_id format (DID? raw key? UUID?)
- signing_key_id format (key fingerprint? JWK thumbprint?)

*Open dependencies (see open_dependencies output):*
- SCHEMA.md: KeyAuthorizationRecord, stream_context, epoch encoding
- PROTOCOL.md: stream resolution algorithm, epoch chain verification
- CRYPTO.md: hash function H, signature algorithm bindings
- ENCODING.md: varint spec, canonical serialization for derivation inputs
- ROUTING.md: routing key definition, epoch-aware updates
- CONTINUITY.md: epoch chain as sole continuity mechanism

---

## §8: CANONICAL FORMS

[Unchanged — placeholder for canonical forms]

---

## §9: VERIFICATION PROCEDURE — DETAILED REFERENCE

**This section provides a reference-level restatement of the verification procedure defined in §5.3. It is normative. In case of any discrepancy between §5.3 and this section, §5.3 takes precedence.**

The verification procedure consists of 12 sequential validation phases. Validation is pure with respect to accepted state; commitment is the only mutation.

### Phase 1: CBOR Parsing and Canonical Form
- Decode input as CBOR.
- Verify canonical encoding per §2 (major types, integer representation, byte/text string constraints, array/map definiteness, key ordering, set semantics, null/optional rules, floating-point prohibition, indefinite-length prohibition, duplicate prohibition, integer bounds).
- Reject as `MALFORMED_ENCODING` if any check fails.

### Phase 2: Envelope Structure Validation
- Verify required fields: `domain_separator`, `sequence`, `chain_hash`, `signature` present.
- Verify `sequence` ≥ 1.
- Verify `previous_hash` absent iff `sequence == 1`; present and 32-byte iff `sequence > 1`.
- Verify no fields outside `unsigned_payload` ∪ `{chain_hash, signature}` (E7).
- Reject as `MALFORMED_ENVELOPE` if any check fails.

### Phase 3: Domain Separator Validation
- Verify `domain_separator` is in the registered set (§4.5).
- Reject as `UNKNOWN_SCHEMA` if not registered.

### Phase 4: Schema-Specific Field Validation
- Validate all schema-specific fields against the schema for the registered `domain_separator` (§6).
- Reject as `MALFORMED_SCHEMA` if validation fails.

### Phase 5: Sequence and Previous_Hash Consistency
- Verify `sequence` ≥ 1 (redundant with Phase 2 but explicit).
- Verify `previous_hash` presence matches `sequence`.
- If `sequence > 1`, verify `previous_hash` is a 32-byte byte string.
- Reject as `INVALID_SEQUENCE` or `INVALID_PREVIOUS_HASH` respectively.

### Phase 6: Chain Linkage Verification
- Reconstruct `unsigned_payload` = object minus `{chain_hash, signature}`.
- Compute `commitment_preimage` per §3.3.
- Compute `object_commitment` per §3.4.
- Determine `previous_chain_hash`:
  - If `sequence == 1`: `initial_chain_hash` per §3.5.
  - If `sequence > 1`: the verifier's accepted `chain_hash` for `sequence-1` in the same `(issuer, stream_id)`.
- Verify `previous_hash` == `object_commitment(sequence-1)` (when `sequence > 1`).
- Compute `chain_hash` per §3.5 using `previous_chain_hash` and `object_commitment`.
- Verify computed `chain_hash` == object's `chain_hash` field.
- Reject as `CHAIN_MISMATCH` if any check fails.

### Phase 7: Signature Input Reconstruction
- Compute `signature_input` per §3.9 using `domain_separator`, `unsigned_payload`, and verified `chain_hash`.

### Phase 8: Signature Verification
- Determine expected signing public key from accepted authority state per §5.2.
- For single-signature: verify `Ed25519_verify(pubkey, signature_input, signature)`.
- For dual-signature (`IdentityContinuity`): verify both `signature[0]` under `previous_root` and `signature[1]` under `new_root`, both over the same `signature_input`.
- Reject as `INVALID_SIGNATURE` if verification fails.

### Phase 9: Authority Validation
- Verify signing key role matches authorized signer for `domain_separator` (§5.2).
- Verify key is currently authorized:
  - Not revoked by `KeyRevocation` with `effective_sequence` ≤ object's sequence (for authorization stream objects).
  - Not superseded without valid transition.
  - Delegation chain valid (for delegated signers).
- Reject as `UNAUTHORIZED_SIGNER` if validation fails.

### Phase 10: Temporal and Revocation Validation
- `issued_at` ≤ now + `MAX_CLOCK_SKEW` (else `EXPIRED` semantics if past, but `issued_at` in future is `NOT_YET_VALID`).
- `not_before` ≤ now + `MAX_CLOCK_SKEW` (else `NOT_YET_VALID`).
- `expires_at` > now - `MAX_CLOCK_SKEW` (else `EXPIRED`).
- No applicable revocation: key revocation, grant revocation, lease revocation, relationship termination.
- Reject as `EXPIRED`, `NOT_YET_VALID`, `REVOKED`, or `TERMINATED` respectively.

### Phase 11: Semantic Validation
- Apply object-type-specific semantic rules:
  - `StreamResolution`: authority above disputed stream trusted pre-fork; `disputed_sequence` matches observed fork; `accepted_hash` ∈ `disputed_hashes`; monotonic in resolver's stream; chain valid.
  - `IdentityContinuity`: `sequence==1`; `previous_hash` omitted; `chain_hash` == successor `initial_chain_hash`; dual signatures valid; trust chain from pre-transition root; `previous_chain_hash` matches accepted terminal hash; no duplicate successor; not expired.
  - Authorization objects (Grant, Lease): relationship `RECOGNIZED`; grant `GRANTED`; key `ACTIVE`/`SUPERSEDED`; no revocation; offline tolerance not exceeded.
  - Other types: per their schema (§6–§8, §54).
- Reject as `SEMANTIC_VIOLATION` if any rule fails.

### Phase 12: Acceptance and State Commitment
- If all phases 1–11 pass: ACCEPT.
- Atomically update accepted stream state and all derived state (chain state, relationship state, grant state, lease state, key state).
- Record `acceptance_time` (monotonic) for relative validity.

---

## §10: REJECTION CLASSES AND OUTCOMES REGISTRY

### 10.1 Rejection Classes (Authoritative)

The following table defines the complete, exhaustive set of rejection classes. Every verification failure maps to exactly one class. The classes are listed in the order they are encountered during the verification procedure (§5.3 / §9). The first matching class applies.

| Class | Meaning | Source Phase | Notes |
|-------|---------|--------------|-------|
| `MALFORMED_ENCODING` | Input is not valid canonical CBOR | §9 Phase 1 | Includes non-canonical map ordering, non-shortest integers, indefinite lengths, disallowed major types, invalid UTF-8, non-NFC text, duplicate keys/elements, wrong key types, floating-point values |
| `MALFORMED_ENVELOPE` | Envelope structure invalid per E1–E7 | §9 Phase 2 | Missing required fields, `sequence` < 1, `previous_hash` presence mismatch, unknown fields |
| `UNKNOWN_SCHEMA` | `domain_separator` not in registry | §9 Phase 3 | |
| `MALFORMED_SCHEMA` | Schema-specific fields fail validation | §9 Phase 4 | Per-object schema rules (§6) |
| `INVALID_SEQUENCE` | `sequence` == 0 or out of range | §9 Phase 5 | |
| `INVALID_PREVIOUS_HASH` | `previous_hash` presence/type inconsistent with `sequence` | §9 Phase 5 | Present at seq 1, absent at seq > 1, wrong length |
| `CHAIN_MISMATCH` | `previous_hash` or `chain_hash` inconsistent with stream state | §9 Phase 6 | Includes wrong `previous_chain_hash`, wrong `object_commitment` |
| `INVALID_SIGNATURE` | Signature verification fails | §9 Phase 8 | Wrong key, tampered data, dual-sig mismatch |
| `UNAUTHORIZED_SIGNER` | Signer lacks required role or key not authorized | §9 Phase 9 | Role mismatch, key revoked, key superseded, delegation missing |
| `NOT_YET_VALID` | `not_before` > now + `MAX_CLOCK_SKEW` | §9 Phase 10 | |
| `EXPIRED` | `issued_at` or `expires_at` check failed | §9 Phase 10 | |
| `REVOKED` | Object invalidated by accepted revocation | §9 Phase 10 | Key revocation, grant revocation, lease revocation |
| `TERMINATED` | Relationship terminated | §9 Phase 10 | Accepted `RelationshipTermination` for the `relationship_id` |
| `SEMANTIC_VIOLATION` | Object-type-specific semantic rule violated | §9 Phase 11 | Covers `StreamResolution`, `IdentityContinuity`, auth rules, etc. |

### 10.2 Outcomes Registry (Authoritative)

The verification procedure produces exactly one of the following outcomes. There are no other outcomes.

| Outcome | Meaning | State Effect |
|---------|---------|--------------|
| `ACCEPT` | All validation phases passed | Atomic state commit (§5.3 Step 12 / §9 Phase 12) |
| `REJECT: <class>` | Validation failed at the first class encountered | No state mutation; failure recorded for diagnostics |

**Invariant:** Verification is a pure function of (input object, accepted state, current time). It produces either `ACCEPT` or `REJECT: <class>`. It never produces a partial acceptance or an intermediate state.

### 10.3 Processing Model Summary

```
function verify(object_bytes, accepted_state, now):
    for phase in 1..11:
        result = run_phase(phase, object_bytes, accepted_state, now)
        if result != CONTINUE:
            return REJECT(result.class)
    return ACCEPT(commit(accepted_state, object))
```

---

## Unresolved Dependencies

1. **§6 Object Schemas** — The semantic validation rules in §5.3 Step 11 / §9 Phase 11 and the `MALFORMED_SCHEMA` rejection class require complete object schemas for all 19 object types. These schemas are not yet specified in OBJECTS.md.

2. **Stream State Lookup Semantics** — Phase 6 (§9) and Step 6 (§5.3) refer to "the verifier's accepted `chain_hash` for sequence-1 in the same `(issuer, stream_id)`". The precise API/interface for this lookup (including handling of gaps, forks, and the `SYNCING`/`FORKED` states from PROTOCOL.md §47) is defined in PROTOCOL.md §47 but the interaction contract between the verification procedure and the stream state machine needs explicit specification.

3. **Authority State Representation** — Step 9 / Phase 9 requires determining "the expected signing public key from accepted authority state per §5.2". The representation of accepted authority state (identity root, authorized keys, delegations, revocation state, key status) is defined in PROTOCOL.md §47 but the query interface (e.g., "is key K authorized for role R at sequence S?") is not formally specified in OBJECTS.md.

4. **Revocation State Query** — Step 10 / Phase 10 requires checking "no applicable revocation". The revocation state machine (PROTOCOL.md §48.4, §20) defines states but the verification-time query "does revocation X invalidate object Y at sequence Z?" needs a precise specification.

5. **Relationship State Derivation** — The semantic check for authorization objects requires the verifier-derived `RECOGNIZED` relationship state (PROTOCOL.md §12.4, §47.3). The exact algorithm for deriving this state from accepted `RelationshipAssertion` and `RelationshipTermination` objects is specified in PROTOCOL.md but the verification procedure's dependency on it should be acknowledged.

6. **Clock and Time Source** — `MAX_CLOCK_SKEW = 5 minutes` is defined in PROTOCOL.md §40.4. The verification procedure assumes access to a wall clock with this skew tolerance and a monotonic clock for `acceptance_time`. The interface is not specified in OBJECTS.md.

7. **Conformance Scenarios (PROTOCOL.md §61)** — The 17 conformance scenarios will test the verification procedure end-to-end. Any gaps in the procedure will surface there.

8. **Test Vectors (§11)** — The test vector format (§11.1) references rejection classes and verification steps. The classes in §10.1 must align with the `expected_rejection` values in negative test vectors.

9. **Wire Protocol / Transport** — Object delivery, fetching missing objects during gaps (`SYNCING` state), and rendezvous interaction are outside OBJECTS.md scope but affect when/which objects are presented to verification.