# Grid Network — Object Encoding (OBJECTS.md v0.2)

**Status:** §1–§5 complete, §6–§10 pending  
**Depends on:** PROTOCOL.md v0.6.2  
**Purpose:** Byte-level encoding and cryptographic constructions for all signed objects

---

## TWO TOP-LEVEL INVARIANTS

**I1 — Sequence-space invariant.** A sequence number has meaning only within its (issuer, stream_id) sequence space. Sequence numbers from different sequence spaces MUST NOT be compared.

**I2 — Vector normative invariant.** Normative test vectors define exact byte-level behavior. If prose and a vector disagree, the specification MUST be corrected so they agree; implementations MUST NOT choose whichever interpretation they prefer.

---

## §1: SCOPE AND NORMATIVE TERMINOLOGY

This document defines the byte-level representation and cryptographic constructions of all signed objects in the protocol. It defines:

- The canonical CBOR encoding profile
- The construction of unsigned_payload, object_commitment, chain_hash, signature_input, signature, payload_id, and object_id
- The common stream envelope
- The sequence and chain rules
- The semantics of domain_separator
- Positive and negative test vectors

Object schemas are defined in §6 (pending). Conformance requirements are defined in §12 (pending).

Normative terminology:
- MUST, MUST NOT, SHOULD, SHOULD NOT, MAY as defined in RFC 2119
- Canonical means the exact byte sequence produced by the encoding rules
- Unsigned payload means the CBOR map representing an object before chain_hash and signature are added
- Signed object means the CBOR map representing an object after chain_hash and signature are added
- Sequence space means the pair (issuer, stream_id)
- Stream means the ordered sequence of objects sharing one sequence space
- Base state means initial_chain_hash, the predecessor value for the first object in a stream

---

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

This is NOT alphabetical ordering. The ordering is over the byte representation of the key. Non-canonical map ordering is malformed.

### 2.8 Set semantics

A protocol set<T> is encoded as a definite-length CBOR array whose elements are:
1. Unique — no two elements have identical canonical CBOR encodings
2. Sorted — elements are ordered by bytewise lexicographic comparison of their canonical CBOR encodings

An array that represents a set<T> but contains duplicate elements, or whose elements are not in the required order, is malformed. An empty set is encoded as an empty definite-length array.

### 2.9 Null and optional fields

null (CBOR 0xf6) is permitted only where an object schema explicitly declares a field optional-and-absent. When a field is optional-and-absent, the field key MUST be omitted from the map, not set to null. An explicit null value is malformed unless a schema explicitly requires it. Boolean values (false = 0xf4, true = 0xf5) are permitted where a schema declares a boolean field.

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

- canonical_cbor(V) — the byte string produced by encoding CBOR value V according to §2
- SHA-256(B) — the SHA-256 hash of byte string B, producing a 32-byte value
- Ed25519_sign(K, B) — the Ed25519 signature over byte string B using private key K, producing a 64-byte value
- Ed25519_verify(P, B, S) — verification of signature S over byte string B using public key P
- || — byte string concatenation

### 3.1 Value/byte distinction

Protocol constructions operate on two kinds of input:
- CBOR values — the abstract data structures
- Byte strings — the output of canonical_cbor or of hashing

The distinction is critical. In all definitions below:
- An operand described as a CBOR value is used as a value and is canonically encoded as part of the surrounding structure
- An operand described as a byte string is used as bytes and is encoded as a CBOR byte string when placed inside a surrounding CBOR structure

### 3.2 Unsigned payload

The unsigned payload of an object is the CBOR map containing all fields defined by the object schema, including common stream fields such as domain_separator, sequence, and previous_hash where the schema includes them. It excludes only two fields:
- chain_hash, which is derived from the unsigned payload and the stream state
- signature, which is derived from the unsigned payload and the chain hash

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
- Element 0 is the text string "grid/commitment/v1"
- Element 1 is the object's domain_separator as a text string
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

Where canonical_signed_object_bytes is the exact canonical CBOR encoding of the signed object — the byte-for-byte wire representation. It is not a CBOR value; it is a byte string in this construction.

Implementations MUST NOT re-encode the signed object as a CBOR value before hashing.

### 3.8 Signed object

A signed object is a CBOR map containing all fields of the unsigned payload, plus:
- chain_hash — a byte string
- signature — a byte string (or two-element array of byte strings for dual-signature schemas)

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

Non-circularity: The signature input MUST be reconstructible from the unsigned payload and the chain hash alone. The signature MUST NOT be part of any input to its own computation.

### 3.10 Serialization invariants

**S1 — Canonical form.** Two objects that represent the same protocol value MUST have identical canonical CBOR encodings.

**S2 — Signature domain separation.** Every cryptographic construction has a unique domain tag:

| Tag | Construction |
|-----|--------------|
| "grid/commitment/v1" | commitment_preimage |
| "grid/chain-base/v1" | initial_chain_hash |
| "grid/chain/v1" | chain_hash |
| "grid/signature/v1" | signature_input |
| "grid/payload-id/v1" | payload_id |
| "grid/object-id/v1" | object_id |

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

Type: CBOR text string. The domain_separator identifies the object's schema family and version. It is drawn from the registered set (§4.5). The domain_separator is part of unsigned_payload. It is included in commitment_preimage, payload_id, and signature_input.

There is no separate version field in the envelope. The schema version is carried by domain_separator.

#### 4.3.2 sequence

Type: CBOR unsigned integer. Range: 1 to 2^64 − 1. The value 0 is reserved for "uninitialized" and MUST NOT appear in any signed object.

#### 4.3.3 previous_hash

Type: CBOR byte string (32 bytes). Optional; present only at sequence numbers greater than 1. At sequence 1, the field is omitted. It MUST NOT be present with a null value. A sequence-1 object that contains a previous_hash field is malformed.

Not to be confused with previous_chain_hash. The chain construction uses a value called previous_chain_hash, which is not a field of any object.

| Value | What it is | Where it lives |
|-------|------------|----------------|
| previous_hash | previous object's object_commitment | a field (omitted at sequence 1) |
| previous_chain_hash | previous object's chain_hash (or initial_chain_hash) | computed input; not a field |

#### 4.3.4 chain_hash

Type: CBOR byte string (32 bytes). Added to the object after unsigned_payload is complete. Computed per §3.5.

#### 4.3.5 signature

Type: CBOR byte string (64 bytes) for single-signature schemas; definite-length CBOR array of exactly two 64-byte byte strings for dual-signature schemas.

For dual-signature schemas, signature is a CBOR array [signature_0, signature_1] where ordering is defined by the schema. The array MUST be definite-length and MUST contain exactly two elements. For dual-signature schemas, both signatures MUST be over the same signature_input.

#### 4.3.6 Schema-specific fields

Every object schema defines the schema-specific fields that appear in unsigned_payload, in addition to the common envelope fields.

### 4.4 Envelope invariants

E1. domain_separator MUST be present.
E2. sequence MUST be present and ≥ 1.
E3. previous_hash MUST be omitted at sequence 1 and present at sequence numbers greater than 1.
E4. chain_hash MUST be present.
E5. signature MUST be present.
E6. unsigned_payload MUST NOT contain any field named chain_hash or signature.
E7. The signed object MUST NOT contain any field outside the set of unsigned_payload fields plus chain_hash and signature.

### 4.5 Registered domain separators

| Domain separator | Object |
|------------------|--------|
| "grid/identity-document/v1" | IdentityDocument |
| "grid/device-binding/v1" | DeviceBinding |
| "grid/service-binding/v1" | ServiceBinding |
| "grid/key-binding/v1" | KeyBinding |
| "grid/key-revocation/v1" | KeyRevocation |
| "grid/relationship-assertion/v1" | RelationshipAssertion |
| "grid/relationship-termination/v1" | RelationshipTermination |
| "grid/rendezvous-manifest/v1" | Principal RendezvousManifest |
| "grid/operator-manifest/v1" | OperatorManifest |
| "grid/relationship-grant/v1" | Grant |
| "grid/authorization-lease/v1" | Lease |
| "grid/grant-revocation/v1" | GrantRevocation |
| "grid/lease-revocation/v1" | LeaseRevocation |
| "grid/service-record/v1" | ServiceRecord |
| "grid/reachability-record/v1" | ReachabilityRecord |
| "grid/stream-resolution/v1" | StreamResolution |
| "grid/identity-continuity/v1" | IdentityContinuity |
| "grid/relay-ticket/v1" | RelayTicket |
| "grid/relay-node-record/v1" | RelayNodeRecord |

Registry rules:
- Domain separators are ASCII text strings
- Each value identifies exactly one object schema family and version
- A future schema version of the same family MUST use a distinct domain separator
- Unknown domain separators MUST be rejected

---

## §5: SIGNATURE SEMANTICS

### 5.1 Purpose

§5 defines which key role is authorized to sign each object type, and the signature verification procedure.

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

### 5.3 Verification procedure

When a verifier receives an object:

1. **Decode.** Decode canonical CBOR. Reject as MALFORMED_ENCODING if invalid.
2. **Envelope validation.** Verify required envelope fields. Reject as MALFORMED_ENVELOPE.
3. **Domain separator validation.** Verify domain_separator is registered. Reject as UNKNOWN_SCHEMA.
4. **Schema validation.** Validate schema-specific fields. Reject as MALFORMED_SCHEMA.
5. **Sequence validation.** Verify sequence >= 1 and previous_hash presence. Reject as INVALID_SEQUENCE or INVALID_PREVIOUS_HASH.
6. **Chain validation.** Compute object_commitment, verify previous_hash, compute and verify chain_hash. Reject as CHAIN_MISMATCH.
7. **Signature input construction.** Compute signature_input.
8. **Signature verification.** Verify signature(s). Reject as INVALID_SIGNATURE.
9. **Authority validation.** Verify signing key role and current authorization. Reject as UNAUTHORIZED_SIGNER.
10. **Semantic validation.** Apply the object's semantic rules.

#### 5.3.1 Atomicity

A verifier MUST NOT advance or mutate its accepted stream state while performing steps 1–9. Validation is pure with respect to accepted state; commitment is the only mutation.

### 5.4 Delegated signers

DeviceBinding MAY be signed by a device-authority key delegated by the Identity Root. ServiceBinding MAY be signed by a service-authority key. Delegations MUST be present in the verifier's accepted identity state.

### 5.5 Dual-signature objects

Only IdentityContinuity uses dual signatures in V1.

For IdentityContinuity:
```
signature: [
    sig_prev,   // by previous_root
    sig_new     // by new_root
]
```

Both signatures are over the same signature_input.

### 5.6 StreamResolution signing

A StreamResolution MUST be signed by an authority above the disputed stream in the authority hierarchy, trusted from state accepted before the fork was observed. The resolver's stream position is expressed by the resolution object's own sequence, chain_hash, and previous_hash. The disputed stream's position is expressed by disputed_sequence, a value that MUST NOT be compared with the resolution's sequence.

### 5.7 Rejection classes

| Class | Meaning |
|-------|---------|
| MALFORMED_ENCODING | Not valid canonical CBOR |
| MALFORMED_ENVELOPE | Envelope fields missing, mistyped, or unknown fields present |
| UNKNOWN_SCHEMA | domain_separator not registered |
| MALFORMED_SCHEMA | Schema-specific fields fail validation |
| INVALID_SEQUENCE | sequence is 0 or otherwise invalid |
| INVALID_PREVIOUS_HASH | previous_hash presence does not match sequence |
| CHAIN_MISMATCH | previous_hash or chain_hash does not match stream state |
| INVALID_SIGNATURE | Signature does not verify |
| UNAUTHORIZED_SIGNER | Signing key role is not authorized |

---

## §6: OBJECT SCHEMAS (PENDING)

**Status:** To be drafted.

This section will define, for each object type:
- Exact field names
- Field types and constraints
- Required vs. optional
- Which stream the object belongs to
- Which key role signs it
- Canonical encoding notes

Object types (19 total):
- IdentityDocument
- DeviceBinding
- ServiceBinding
- KeyBinding
- KeyRevocation
- RelationshipAssertion
- RelationshipTermination
- RendezvousManifest
- OperatorManifest
- Grant
- Lease
- GrantRevocation
- LeaseRevocation
- ServiceRecord
- ReachabilityRecord
- StreamResolution
- IdentityContinuity
- RelayTicket
- RelayNodeRecord

### Encoding Decisions (Frozen)

The following decisions are frozen and will be reflected in all schemas:

1. **CBOR field names:** Use snake_case exactly as in PROTOCOL.md pseudo-schemas (peer_id, domain_separator, identity_root, etc.)
2. **Enum encoding:** Text strings (not integers) for key_role, capability namespaces, etc. — self-documenting, survives schema evolution
3. **ID formats:**
   - peer_id: text string, `peer:v1:<64 hex chars>`
   - device_id: text string, UUID v4 format (e.g., `550e8400-e29b-41d4-a716-446655440000`)
   - service_id: text string, UUID v4 format
4. **Timestamp encoding:** Unix epoch seconds as unsigned integer (no milliseconds, no ISO 8601 text)
5. **Test keypair:** RFC 8032 §7.1 test vector 1 seed:
   - Seed: `9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60`
   - Public key: `d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a`
   - Marked as PUBLIC TEST VECTOR — never use for real purposes

---

## §7: STREAM RULES (PENDING)

**Status:** To be drafted.

This section will define:
- Sequence spaces and their identifiers
- Initial chain state
- Monotonicity rules
- Gap detection and handling
- Fork detection and handling
- Resolution procedures
- Cross-stream prohibition (restated normatively)

---

## §8: CANONICAL FORMS (PENDING)

**Status:** To be drafted.

This section will provide byte-exact canonical forms for each object type.

---

## §9: VERIFICATION PROCEDURE (10 STEPS) — DETAILED

When a verifier receives an object:

**Step 1: Parse CBOR**
- Ensure it's valid CBOR
- Ensure it's in canonical form
- Reject if not

**Step 2: Extract envelope**
- Verify sequence is positive integer
- Verify previous_hash is hex or null
- Verify chain_hash is hex
- Verify signature is hex (128 chars for Ed25519)

**Step 3: Verify domain separator**
- Extract from type-specific fields
- Ensure it matches object type (e.g., "grid/identity-document/v1")

**Step 4: Recompute payload_id**
- Remove sequence, previous_hash, chain_hash, signature
- CBOR encode remaining fields
- Hash with domain_separator prefix
- Compare to object's stated payload_id

**Step 5: Recompute chain_hash**
- If sequence == 1: use domain_separator as previous
- If sequence > 1: lookup previous object's chain_hash
- Hash with object_id
- Compare to object's stated chain_hash

**Step 6: Verify signature**
- Reconstruct signature_input (sequence, previous_hash, chain_hash, payload_id)
- Verify Ed25519 signature against appropriate key

**Step 7: Check stream membership**
- Verify object type matches stream type
- Verify sequence is monotonically increasing
- Detect forks (same sequence, different hash)

**Step 8: Check revocations**
- Is the signing key revoked?
- Is the object's grant revoked?
- Is the relationship terminated?

**Step 9: Check timestamps**
- issued_at <= now
- not_before <= now or object is not effective
- expires_at > now or object is expired

**Step 10: Accept or reject**
- If all checks pass: ACCEPT
- If any check fails: REJECT with error class

---

## §10: REJECTION CLASSES (DETAILED)

When verification fails, specify why:

| Class | Meaning | Example |
|-------|---------|---------|
| MALFORMED | Object not parseable | Invalid CBOR |
| NOT_CANONICAL | CBOR not in canonical form | Non-sorted map keys |
| INVALID_SIGNATURE | Signature verification failed | Wrong key or tampered |
| WRONG_STREAM | Object in wrong stream | Grant in identity stream |
| FORK_DETECTED | Two objects, same seq, different hash | Conflicting history |
| REVOKED | Signing key or grant revoked | Key revocation applies |
| EXPIRED | Object timestamp check failed | expires_at < now |
| KEY_NOT_FOUND | Cannot verify (no key available) | Unknown issuer |
| SEQUENCE_GAP | Missing intermediate objects | Seq 1, then seq 3 (no seq 2) |
| CHAIN_BROKEN | Previous hash doesn't match | History corruption |

---

## §11: TEST VECTOR SPECIFICATION

### 11.1 Vector format

Each test vector is a JSON file with:

```json
{
  "name": "identity-document-seq1-basic",
  "version": "0.6.2",
  "type": "positive",
  "description": "Minimal identity document, sequence 1, no relationships",
  "input": { ... },
  "canonical_cbor": "a1...",
  "expected_hashes": {
    "payload_id": "sha256:abcd1234...",
    "object_id": "sha256:xyz789...",
    "chain_hash": "sha256:chain_hash_value..."
  },
  "expected_signature": "ed25519:sig_value...",
  "verification_steps": [
    "Parse CBOR",
    "Verify domain separator",
    "Recompute payload_id",
    "Recompute chain_hash",
    "Verify Ed25519 signature",
    "Accept object"
  ],
  "spec_reference": "PROTOCOL.md §7.8, OBJECTS.md §6"
}
```

Negative test vector format:

```json
{
  "name": "identity-document-tampered-field",
  "version": "0.6.2",
  "type": "negative",
  "description": "Identity document with one byte changed",
  "canonical_cbor": "a1...",
  "modification": "Changed first byte of peer_id",
  "expected_rejection": "INVALID_SIGNATURE",
  "expected_rejection_reason": "Signature does not verify",
  "spec_reference": "OBJECTS.md §8.5.3 Step 8"
}
```

### 11.2 Test vector repository structure

```
spec/test-vectors/v0.6.2/
├── README.md
├── positive/
│   ├── identity-document/
│   ├── relationship-assertion/
│   ├── grant/
│   ├── lease/
│   ├── reachability-record/
│   └── ... (one per object type)
├── negative/
│   ├── identity-document/
│   ├── relationship-assertion/
│   └── ... (one per object type, 3+ variants)
└── conformance-scenarios/
    └── ... (all 17 scenarios from PROTOCOL.md §61)
```

### 11.3 Test vector production sequence

Phase A — Basic Crypto (2 vectors)
Phase B — Identity (4 vectors)
Phase C — Relationships (3 vectors)
Phase D — Authorization (6 vectors)
Phase E — Reachability (3 vectors)
Phase F — Negative (18+ variants)
Phase G — Scenarios (17 vectors)

Total: 53+ test vectors

---

## §12: CONFORMANCE REQUIREMENTS (PENDING)

**Status:** To be drafted.

An implementation conforms to Grid Network v0.6.2 if:
1. It implements all normative requirements from PROTOCOL.md
2. It produces objects that conform to OBJECTS.md encoding
3. It passes all test vectors (when published)
4. It exhibits correct failure semantics (PROTOCOL.md §53 F1–F6)
5. It maintains correct state machines (PROTOCOL.md §48)
6. It respects authority domains (PROTOCOL.md §49)
7. It implements verifier rules (OBJECTS.md §9)
8. It handles all 17 conformance scenarios (PROTOCOL.md §61)

---

*End of OBJECTS.md v0.2 (partial — §6–§10 pending)*
