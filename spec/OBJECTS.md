# Grid Network — Object Encoding Specification

**Revision:** 2.5
**Protocol version:** v0.6.3

This document defines the byte-level representation and cryptographic
constructions of every signed object in the Grid Network protocol. It
is normative and is subordinate only to the Protocol Specification.
Where this document and the Protocol Specification conflict, the
Protocol Specification governs.

---

## §1. Scope and terminology

This document defines:

- the canonical CBOR encoding profile;
- the constructions of `unsigned_payload`, `commitment_preimage`,
  `object_commitment`, `chain_hash`, `signature_input`, `signature`,
  `payload_id`, and `object_id`;
- the common stream envelope;
- sequence and chain rules;
- the semantics of `domain_separator`;
- the object registry;
- the verification procedure;
- the rejection classes.

**Normative terminology.**

- MUST, MUST NOT, SHOULD, SHOULD NOT, MAY as defined in RFC 2119.
- **Canonical** means the exact byte sequence produced by the encoding
  rules in §2.
- **Unsigned payload** means the CBOR map representing an object before
  `chain_hash` and `signature` are added.
- **Signed object** means the CBOR map representing an object after
  `chain_hash` and `signature` are added.
- **Sequence space** means the pair `(issuer, stream_id)`.
- **Stream** means the ordered sequence of objects sharing one sequence
  space.
- **Base state** means `initial_chain_hash`, the predecessor value for
  the first object in a stream.

**Two invariants govern this document.**

**I1 — Sequence-space invariant.** A sequence number has meaning only
within its `(issuer, stream_id)` sequence space. Sequence numbers from
different sequence spaces must not be compared.

**I2 — Vector normative invariant.** Normative test vectors define
exact byte-level behavior. If prose and a vector disagree, this
document must be corrected so they agree. Implementations must not
choose whichever interpretation they prefer.

---

## §2. Canonical CBOR profile

All protocol objects use CBOR (RFC 8949) with the deterministic
encoding constraints below. Where RFC 8949 permits alternatives, only
the form specified here is valid.

### §2.1 Allowed major types

| Major type | Allowed | Notes |
|---|---|---|
| 0 — unsigned integer | Yes | §2.2 |
| 1 — negative integer | No | Protocol values are non-negative |
| 2 — byte string | Yes | §2.3 |
| 3 — text string | Yes | §2.4 |
| 4 — array | Yes | §2.5 |
| 5 — map | Yes | §2.6, §2.7 |
| 6 — tag | No | Protocol uses no CBOR tags |
| 7 — simple and float | Partial | Only `null` (0xf6) and booleans |

Any object containing a major type not listed above is malformed.

### §2.2 Integer representation

Integers MUST be encoded in their shortest form.

- Values 0 through 23 use the additional-information encoding directly.
- Values above 23 use the shortest additional-info-24/25/26/27 form.

Non-shortest integer encodings are malformed. Negative integers are
not permitted. Permitted range: 0 to 2^64 − 1.

### §2.3 Byte strings

Byte strings MUST be definite-length. Byte string length MUST be
encoded in the shortest form.

### §2.4 Text strings

Text strings MUST be definite-length and MUST be valid UTF-8.

Text strings MUST be in Unicode Normalization Form C (NFC), computed
under Unicode version 15.0. A text string that is not in NFC under that
version is malformed.

A byte-order mark (U+FEFF) MUST NOT appear at the start of a text
string.

### §2.5 Arrays

Arrays MUST be definite-length.

An array's schema declares whether duplicate elements are permitted.
Unless a schema explicitly permits duplicates, duplicate elements are
malformed. Arrays that represent a set have additional constraints
(§2.8).

### §2.6 Maps

Maps MUST be definite-length. Map keys MUST be unique. A map containing
duplicate keys is malformed.

Map keys MUST be text strings unless the map's schema explicitly
permits other key types. Protocol map keys are always text strings.

### §2.7 Map key ordering

Map keys MUST be ordered by bytewise lexicographic comparison of their
canonical CBOR encodings. This is the ordering defined by RFC 8949
§4.2.1. Length-first ordering (RFC 7049 §3.9) is not used.

A map whose keys are not in this order is malformed.

### §2.8 Set semantics

A protocol `set<T>` is encoded as a definite-length CBOR array whose
elements are:

1. Unique — no two elements have identical canonical CBOR encodings.
2. Sorted — elements are ordered by bytewise lexicographic comparison
   of their canonical CBOR encodings.

An array that represents a `set<T>` but contains duplicate elements, or
whose elements are not in the required order, is malformed.

An empty set is encoded as an empty definite-length array.

### §2.9 Null and optional fields

`null` (0xf6) is permitted only where an object schema explicitly
declares a field optional-and-absent. When a field is optional-and-
absent, the field key is omitted from the map, not set to `null`.

An explicit `null` value is malformed unless a schema explicitly
requires it.

Boolean values (`false` = 0xf4, `true` = 0xf5) are permitted where a
schema declares a boolean field.

Simple values other than `null`, `false`, and `true` are not permitted.

### §2.10 Floating-point prohibition

Floating-point values (major type 7, additional info 25–27) are
prohibited. All numeric values in protocol objects are integers. Time
values are integer seconds unless a schema explicitly requires integer
milliseconds; a schema must state the unit.

### §2.11 Indefinite-length prohibition

Indefinite-length encoding of byte strings, text strings, arrays, and
maps is prohibited. All four must use definite-length encoding.

### §2.12 Duplicate-key and duplicate-element prohibition

Maps must not contain duplicate keys. Sets must not contain duplicate
elements. Arrays that are not sets may contain duplicate values if the
schema permits; protocol arrays that carry lists of distinct values are
declared as sets.

### §2.13 Integer bounds

All integers must fall within the range specified in §2.2. Schemas may
impose narrower bounds; values outside a schema's bounds are malformed.

### §2.14 Rejection of non-canonical encodings

Any CBOR encoding that does not satisfy §2.1 through §2.13 is
malformed. Implementations MUST reject malformed encodings before any
semantic processing.

---

## §3. Object serialization

### §3.1 Notation

- `canonical_cbor(V)` — the byte string produced by encoding value V
  per §2.
- `SHA-256(B)` — the SHA-256 hash of byte string B, producing 32 bytes.
- `Ed25519_sign(K, B)` — an Ed25519 signature over B using private key
  K, producing 64 bytes.
- `Ed25519_verify(P, B, S)` — verification of S over B using public key
  P.

### §3.2 Value and byte distinction

Protocol constructions operate on two kinds of input:

- **CBOR values** — abstract data structures.
- **Byte strings** — the output of `canonical_cbor` or hashing.

In every definition below:

- An operand described as a CBOR value is canonically encoded as part of
  the surrounding structure.
- An operand described as a byte string is used as bytes and is encoded
  as a CBOR byte string when placed inside a surrounding CBOR
  structure.

### §3.3 Unsigned payload

The unsigned payload of an object is the CBOR map containing all fields
defined by the object schema, including common stream fields such as
`domain_separator`, `sequence`, and `previous_hash` where the schema
includes them. It excludes exactly two fields:

- `chain_hash`, which is derived.
- `signature`, which is derived.

All other object fields are part of the unsigned payload.

### §3.4 Commitment preimage

    commitment_preimage =
        canonical_cbor([
            "grid/commitment/v1",
            domain_separator,
            unsigned_payload
        ])

Element 0 is the text string `"grid/commitment/v1"`. Element 1 is the
object's `domain_separator` as a text string. Element 2 is the unsigned
payload as a CBOR value.

### §3.5 Object commitment

    object_commitment = SHA-256(commitment_preimage)

The object commitment is a 32-byte value.

### §3.6 Stream base state

Every stream has a base state represented by `initial_chain_hash`:

    initial_chain_hash =
        SHA-256(canonical_cbor([
            "grid/chain-base/v1",
            domain_separator,
            stream_id
        ]))

`stream_id` is the canonical CBOR encoding of the sequence-space
identifier. The four stream kinds are:

| Stream kind | `stream_id` encoding |
|---|---|
| Identity | `["peer", peer_id]` |
| Authorization | `["auth", auth_key_id]` |
| Reachability | `["device", device_id]` |
| Service | `["service", service_id]` |

Each is a definite-length array of two elements: a text string naming
the stream kind, followed by the identifier.

### §3.7 Previous hash and previous chain hash

Two distinct values serve different purposes and MUST NOT be conflated.

**Previous hash** (`previous_hash`) is an object field that commits to
the immediately preceding object's payload.

    previous_hash(1) = omitted (field absent)
    previous_hash(N) = object_commitment(N-1)   for N > 1

**Previous chain hash** (`previous_chain_hash`) is a computed input, not
a field.

    previous_chain_hash(1) = initial_chain_hash
    previous_chain_hash(N) = chain_hash(N-1)    for N > 1

### §3.8 Chain hash

    chain_hash(N) =
        SHA-256(canonical_cbor([
            "grid/chain/v1",
            previous_chain_hash(N),
            object_commitment(N)
        ]))

Element 1 is `previous_chain_hash(N)` as a CBOR byte string. Element 2 is
`object_commitment(N)` as a CBOR byte string.

The first object in every stream has `sequence = 1`. The value 0 is
reserved for "uninitialized" and MUST NOT appear in any signed object.

The chain hash commits to the entire stream history presented to the
verifier, not just to the previous object. Because the signature input
includes `chain_hash` (§3.12), the signature binds an object to the
specific history that precedes it. An object cannot be moved onto a
different history without invalidating its signature.

The chain hash does not by itself reveal a fork. A verifier that has
observed only one branch holds an internally consistent chain. A fork is
detected when a verifier observes two objects in the same stream with
the same `sequence` and different `chain_hash` values (§9.3). Equal
`chain_hash` values at the same `sequence` establish that two verifiers
hold identical history through that sequence, so two heads can be
compared without exchanging the objects.

### §3.9 Payload ID

    payload_id =
        SHA-256(canonical_cbor([
            "grid/payload-id/v1",
            unsigned_payload
        ]))

The payload ID depends only on the semantic content of the unsigned
payload. Two objects that mean the same thing have the same payload ID.
Payload IDs are not unique per stream position.

### §3.10 Object ID

    object_id =
        SHA-256(canonical_cbor([
            "grid/object-id/v1",
            canonical_signed_object_bytes
        ]))

Element 1 is `canonical_signed_object_bytes` as a CBOR byte string.
This value is the exact canonical CBOR encoding of the signed object —
the wire representation. Implementations MUST NOT re-encode the signed
object as a CBOR value before hashing.

### §3.11 Signed object

A signed object is a CBOR map containing all fields of the unsigned
payload, plus:

- `chain_hash` — a CBOR byte string.
- `signature` — a CBOR byte string, or a two-element array of byte
  strings for dual-signature schemas.

### §3.12 Signature input

    signature_input(N) =
        canonical_cbor([
            "grid/signature/v1",
            domain_separator,
            unsigned_payload,
            chain_hash(N)
        ])

The signature is computed as:

    signature(N) = Ed25519_sign(signing_private_key, signature_input(N))

The signature covers the unsigned payload directly. It covers
`chain_hash`. It does not cover `payload_id`, which is a derived value.

Non-circularity: the signature input is reconstructible from the
unsigned payload and the chain hash alone. The signature is not part of
any input to its own computation.

For dual-signature schemas, both signatures are over the same
`signature_input`.

### §3.13 Serialization invariants

**S1 — Canonical form.** Two objects that represent the same protocol
value have identical canonical CBOR encodings.

**S2 — Signature domain separation.** Every cryptographic construction
has a unique domain tag:

| Tag | Construction |
|---|---|
| `"grid/commitment/v1"` | `commitment_preimage` |
| `"grid/chain-base/v1"` | `initial_chain_hash` |
| `"grid/chain/v1"` | `chain_hash` |
| `"grid/signature/v1"` | `signature_input` |
| `"grid/payload-id/v1"` | `payload_id` |
| `"grid/object-id/v1"` | `object_id` |

**S3 — Chain order.** The chain hash at sequence N depends on the chain
hash at sequence N−1 and the object commitment at sequence N.

**S4 — Determinism.** All constructions are deterministic functions of
their inputs.

**S5 — Byte and value boundary.** The distinction between CBOR values
and byte strings is normative in every construction.

**S6 — Reconstruction.** Every derived value required for verification
is reconstructible from the canonical unsigned payload, applicable
stream state, and the protocol rules. An implementation MUST NOT
depend on non-canonical source representations, parser-preserved
formatting, map insertion order, or locally generated serialization
choices.

---

## §4. Common stream envelope

Every signed object shares a common structural envelope.

### §4.1 Envelope shape

    signed_object = {
        domain_separator : text string,
        sequence         : integer ≥ 1,
        previous_hash?   : byte string (omitted at sequence 1),
        ...schema-specific fields,
        chain_hash       : byte string,
        signature        : byte string or [byte string, byte string]
    }

### §4.2 Field definitions

**`domain_separator`** — a CBOR text string identifying the object's
schema family and version. It is part of the unsigned payload and is
included in every derived value. There is no separate version field in
the envelope.

**`sequence`** — a CBOR unsigned integer, 1 to 2^64 − 1.

**`previous_hash`** — a CBOR byte string, present only at sequence
numbers greater than 1. At sequence 1 the field is omitted. A sequence-1
object that contains `previous_hash` is malformed.

**`chain_hash`** — a CBOR byte string, computed per §3.8.

**`signature`** — a CBOR byte string (64 bytes) for single-signature
schemas, or a definite-length array of exactly two 64-byte byte strings
for dual-signature schemas.

### §4.3 Envelope invariants

E1. `domain_separator` MUST be present.
E2. `sequence` MUST be present and ≥ 1.
E3. `previous_hash` MUST be omitted at sequence 1 and present at
    sequence > 1.
E4. `chain_hash` MUST be present.
E5. `signature` MUST be present.
E6. The unsigned payload MUST NOT contain a field named `chain_hash` or
    `signature`.
E7. The signed object MUST NOT contain any field outside the set of
    unsigned-payload fields plus `chain_hash` and `signature`.

---

## §5. Registered domain separators

Each domain separator identifies exactly one schema family and version.
A future schema version of the same family uses a distinct separator.
Unknown separators are rejected.

| Domain separator | Object |
|---|---|
| `grid/identity-document/v1` | `IdentityDocument` |
| `grid/device-binding/v1` | `DeviceBinding` |
| `grid/service-binding/v1` | `ServiceBinding` |
| `grid/key-binding/v1` | `KeyBinding` |
| `grid/key-revocation/v1` | `KeyRevocation` |
| `grid/relationship-assertion/v1` | `RelationshipAssertion` |
| `grid/relationship-termination/v1` | `RelationshipTermination` |
| `grid/rendezvous-manifest/v1` | `RendezvousManifest` |
| `grid/operator-manifest/v1` | `OperatorManifest` |
| `grid/relationship-grant/v1` | `Grant` |
| `grid/authorization-lease/v1` | `Lease` |
| `grid/grant-revocation/v1` | `GrantRevocation` |
| `grid/lease-revocation/v1` | `LeaseRevocation` |
| `grid/service-record/v1` | `ServiceRecord` |
| `grid/reachability-record/v1` | `ReachabilityRecord` |
| `grid/stream-resolution/v1` | `StreamResolution` |
| `grid/identity-continuity/v1` | `IdentityContinuity` |
| `grid/relay-ticket/v1` | `RelayTicket` |
| `grid/relay-node-record/v1` | `RelayNodeRecord` |
| `grid/credit-receipt/v1` | `CreditReceipt` |

---

## §6. Object registry and signing authority

Each object is signed by an authority role and belongs to a stream.
Objects with no stream (relay tickets, relay node records) carry the
full envelope but are not published in a sequence space.

| Object | Signer | Stream |
|---|---|---|
| IdentityDocument | Identity Root | `stream:identity` |
| DeviceBinding | Identity Root (or delegated device authority) | `stream:identity` |
| ServiceBinding | Identity Root (or delegated service authority) | `stream:identity` |
| KeyBinding | Identity Root | `stream:identity` |
| KeyRevocation | Identity Root | `stream:identity` |
| RelationshipAssertion | Identity Root | `stream:identity` |
| RelationshipTermination | Identity Root | `stream:identity` |
| IdentityContinuity | Previous and New Identity Root | `stream:identity` |
| StreamResolution | Pre-fork authority | `stream:identity` |
| RendezvousManifest | Identity Root | `stream:identity` |
| OperatorManifest | Identity Root | `stream:identity` |
| Grant | Authorization Key | `stream:authorization:{auth_key_id}` |
| Lease | Authorization Key | `stream:authorization:{auth_key_id}` |
| GrantRevocation | Identity Root | `stream:identity` |
| LeaseRevocation | Authorization Key | `stream:authorization:{auth_key_id}` |
| ReachabilityRecord | Device Key | `stream:reachability:{device_id}` |
| ServiceRecord | Service Key | `stream:service:{service_id}` |
| RelayTicket | Relay Authority Key | not streamed |
| RelayNodeRecord | Relay Node Key | not streamed |
| CreditReceipt | Operator | `stream:credit:{operator_id}` |

### §6.1 Object schema stubs

Each object is fully specified in §7. Where an object is registered but
not yet specified, this section records the fact.

| Object | Status |
|---|---|
| KeyBinding | schema specified in §7 |
| DeviceBinding | schema specified in §7 |
| ServiceBinding | schema specified in §7 |
| OperatorManifest | schema not yet specified |
| LeaseRevocation | schema not yet specified |
| RelayNodeRecord | schema not yet specified |
| CreditReceipt | schema not yet specified |
| Relay Authority Key | role, not an object |
| Relay Node Key | role, not an object |

---

## §7. Object schemas

### §7.1 Canonical examples

Examples below are illustrative. They use `Alice`, `Bob`, and `Charlie`
as example principals. Bytes are shown as canonical CBOR byte strings.
`previous_hash` is omitted at sequence 1 and present at later sequences.

### §7.2 IdentityDocument

    {
        "domain_separator": "grid/identity-document/v1",
        "sequence": 1,
        "peer_id": "peer:v1:7f3a9c2e5d91b0a4c7e8126fa31d449b",
        "identity_root": <byte string>,
        "authorized_keys": [ <KeyBinding>, ... ],
        "device_bindings": [ <DeviceBinding>, ... ],
        "service_bindings": [ <ServiceBinding>, ... ],
        "issued_at": <integer>,
        "not_before": <integer>,
        "chain_hash": <byte string>,
        "signature": <byte string>
    }

`authorized_keys`, `device_bindings`, and `service_bindings` are sets,
encoded per §2.8.

### §7.3 RelationshipAssertion

    {
        "domain_separator": "grid/relationship-assertion/v1",
        "sequence": <integer>,
        "previous_hash": <byte string>,   (present when sequence > 1)
        "relationship_id": <uuid as byte string>,
        "subject_principal": "peer:v1:...",
        "issued_at": <integer>,
        "not_before": <integer>,
        "expires_at": <integer>,          (optional; omit if absent)
        "chain_hash": <byte string>,
        "signature": <byte string>
    }

### §7.4 Grant

    {
        "domain_separator": "grid/relationship-grant/v1",
        "sequence": <integer>,
        "previous_hash": <byte string>,
        "grant_id": <uuid as byte string>,
        "relationship_id": <uuid as byte string>,
        "issuer": "peer:v1:...",
        "subject": "peer:v1:...",
        "device_scope": [ <device_id>, ... ],       (optional; set)
        "capabilities": [ <Capability>, ... ],       (set)
        "resources": [ <Resource>, ... ],            (set)
        "constraints": { <text string>: <text string> },
        "lease_policy": {
            "default_duration": <integer seconds>,
            "max_duration": <integer seconds>,
            "max_offline_tolerance": <integer seconds>
        },
        "issued_at": <integer>,
        "not_before": <integer>,
        "expires_at": <integer>,         (optional)
        "note": <text string>,           (optional)
        "chain_hash": <byte string>,
        "signature": <byte string>
    }

### §7.5 Lease

    {
        "domain_separator": "grid/authorization-lease/v1",
        "sequence": <integer>,
        "previous_hash": <byte string>,
        "grant_id": <uuid as byte string>,
        "valid_until_absolute": <integer>,   (exactly one of these
        "valid_for_duration": <integer>,      two is present)
        "issued_at": <integer>,
        "issuer": "peer:v1:...",
        "chain_hash": <byte string>,
        "signature": <byte string>
    }

### §7.6 ReachabilityRecord

    {
        "domain_separator": "grid/reachability-record/v1",
        "sequence": <integer>,
        "previous_hash": <byte string>,
        "device_id": <uuid as byte string>,
        "device_key": <byte string>,
        "endpoints": [
            {
                "protocol": "direct",
                "address": "203.0.113.42:51820",
                "priority": 100,
                "transport": "udp"
            },
            {
                "protocol": "relay",
                "address": "relay-region-a.grid.example",
                "priority": 50,
                "transport": "tcp"
            }
        ],
        "issued_at": <integer>,
        "expires_at": <integer>,
        "published_at": <integer>,
        "identity_sequence": <integer>,
        "chain_hash": <byte string>,
        "signature": <byte string>
    }

`endpoints` is a set, encoded per §2.8. It is ordered by bytewise
lexicographic comparison of canonical element encodings, not by
priority.

### §7.7 ServiceRecord

    {
        "domain_separator": "grid/service-record/v1",
        "sequence": <integer>,
        "previous_hash": <byte string>,
        "service_id": <uuid as byte string>,
        "service_key": <byte string>,
        "service_type": <text string>,
        "endpoint": <text string>,
        "metadata": { <text string>: <text string> },
        "issued_at": <integer>,
        "expires_at": <integer>,
        "chain_hash": <byte string>,
        "signature": <byte string>
    }

### §7.8 RelayTicket

    {
        "domain_separator": "grid/relay-ticket/v1",
        "sequence": <integer>,
        "previous_hash": <byte string>,
        "relay_id": <byte string>,
        "relay_key": <byte string>,
        "subject_peer": "peer:v1:...",
        "subject_device": <uuid as byte string>,
        "destination_peer": "peer:v1:...",
        "destination_device": <uuid as byte string>,
        "capacity": <integer bytes>,
        "duration": <integer seconds>,
        "issued_at": <integer>,
        "expires_at": <integer>,
        "priority_class": "free" | "standard" | "priority" | "dedicated",
        "chain_hash": <byte string>,
        "signature": <byte string>
    }

### §7.9 Remaining schemas

`RendezvousManifest`, `OperatorManifest`, `KeyRevocation`,
`RelationshipTermination`, `IdentityContinuity`, `StreamResolution`,
`GrantRevocation`, `LeaseRevocation`, `RelayNodeRecord`, `CreditReceipt`
follow the same envelope structure. Their schemas are planned and are
not yet specified in this document (§10).

---

## §8. Verification procedure

A verifier processes a candidate object in the order below. Each step
has a specific rejection class.

**Step 1 — Parse.** Decode bytes as CBOR per §2. Reject
`MALFORMED_ENCODING` if the bytes are not canonical.

**Step 2 — Envelope validation.** Verify required envelope fields
(§4.3 E1–E7). Reject `MALFORMED_ENVELOPE`.

**Step 3 — Domain separator validation.** Verify the separator is
registered (§5). Reject `UNKNOWN_SCHEMA`.

**Step 4 — Schema validation.** Validate schema-specific fields.
Reject `MALFORMED_SCHEMA`.

**Step 5 — Sequence validation.** Verify `sequence ≥ 1`. Verify
`previous_hash` presence matches `sequence`. Reject `INVALID_SEQUENCE`
or `INVALID_PREVIOUS_HASH`.

**Step 6 — Chain validation.**

Compute `object_commitment` per §3.5. If `sequence = 1`, the expected
`previous_chain_hash` is `initial_chain_hash` per §3.6. If
`sequence > 1`, retrieve the accepted object at `N−1` in the same
sequence space, compute its `object_commitment`, and verify the
candidate's `previous_hash` equals it. Compute the expected
`chain_hash` per §3.8. Verify the candidate's `chain_hash` matches.
Reject `CHAIN_MISMATCH` on any failure.

**Step 7 — Signature input construction.** Compute `signature_input`
per §3.12.

**Step 8 — Signature verification.** Verify the Ed25519 signature
over `signature_input` against the public key authorized for the object
type and stream (§6). For dual-signature objects, verify both
signatures. Reject `INVALID_SIGNATURE`.

**Step 9 — Authority validation.** Verify that the signing key's role
is authorized for the object type. Verify the key is currently
authorized: not revoked at the object's sequence position, and covered
by the object's delegation chain. Reject `UNAUTHORIZED_SIGNER`.

**Step 10 — Semantic validation.** Apply the object's semantic rules.

### §8.1 Atomicity

A verifier MUST NOT advance or mutate accepted stream state during
steps 1–9. Only after all ten steps pass is the object committed to
local state, as a single atomic operation. If any step fails, the
verifier retains its previous accepted state.

### §8.2 Rejection classes

| Class | Trigger |
|---|---|
| `MALFORMED_ENCODING` | Bytes are not valid canonical CBOR |
| `MALFORMED_ENVELOPE` | Envelope field missing, mistyped, or unknown field present |
| `UNKNOWN_SCHEMA` | `domain_separator` not in the registry |
| `MALFORMED_SCHEMA` | A schema-specific field fails validation |
| `INVALID_SEQUENCE` | `sequence` is 0 or out of range |
| `INVALID_PREVIOUS_HASH` | Presence of `previous_hash` does not match `sequence` |
| `CHAIN_MISMATCH` | `previous_hash` or `chain_hash` does not match stream state |
| `INVALID_SIGNATURE` | Signature does not verify |
| `UNAUTHORIZED_SIGNER` | Signing key is not authorized for this object type and stream |
| `REVOKED` | Signing key or target object is revoked |
| `EXPIRED` | Validity interval has elapsed |
| `FORK_DETECTED` | Stream is in `FORKED` state |

Individual schemas may define additional classes for schema-specific
failures.

---

## §9. Stream rules

### §9.1 Sequence spaces

A stream is identified by its `stream_id` (§3.6). Every object in a
stream shares one sequence space and one signing authority.

### §9.2 Monotonicity

Within a stream, `sequence` values are strictly increasing. Gaps
indicate missing objects; a verifier MUST treat an object whose
predecessor is not present as unverifiable.

### §9.3 Fork detection

Two objects in the same stream with the same `sequence` and different
`chain_hash` constitute a fork. A verifier that observes a fork enters
`FORK_DETECTED` state for that stream.

### §9.4 Fork resolution

A fork is resolved by a `StreamResolution` object (§7.9; its schema
is planned, see §10). Until resolution, a verifier MUST NOT
advance authorization for that stream.

### §9.5 Cross-stream prohibition

A verifier MUST NOT compare sequence numbers from different streams.
It MUST NOT merge chain hashes across streams. Each stream's history is
independent.

---

## §10. Pending sections

The following are not yet specified in this document:

- Full schemas for `RendezvousManifest`, `OperatorManifest`,
  `KeyRevocation`, `RelationshipTermination`, `IdentityContinuity`,
  `StreamResolution`, `GrantRevocation`, `LeaseRevocation`,
  `RelayNodeRecord`, `CreditReceipt`.
- Test vectors, positive and negative, for every object type.
- Conformance test suite.

Until these are produced, the schema registry in §5 and §6 is
authoritative for which objects exist and who signs them.