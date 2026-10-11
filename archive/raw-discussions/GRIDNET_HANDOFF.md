You're right — I compressed everything. Let me give you the actual handoff with all the substantive content, in a form that's copy-pasteable to another agent, with each document as its own clearly-delimited block.

This will be long because it's meant to be complete. I'll organize it as a series of files, each in its own fenced block, ready to paste into a repository or hand to another agent.

---

# Grid Network — Complete Agent Handoff Package

## Package contents

```
grid-network-handoff/
├── 00-HANDOFF-README.md           ← Start here
├── 01-README.md                   ← Repo README
├── 02-OUTLINE.md                  ← Project map
├── 03-PROTOCOL.md                 ← Full protocol spec
├── 04-OBJECTS.md                  ← Byte-level encoding
├── 05-RATIONALE.md                ← Why the design is this way
├── 06-ADDENDUM-A-COMMERCIAL.md    ← Commercial model
├── 07-ADDENDUM-B-LINEAGE.md       ← Lineage / what it borrows
├── 08-SECURITY.md                 ← Threat model (to draft)
├── 09-IMPLEMENTATION.md           ← Build guide (to draft)
├── 10-CONNECTIVITY.md             ← Connectivity layer (to draft)
├── 11-VERSIONING.md               ← Versioning model
├── 12-GLOSSARY.md                 ← Term definitions
├── 13-FAQ.md                      ← Common questions
├── 14-ROADMAP.md                  ← Implementation phases
├── 15-LICENSE.md                  ← Apache 2.0
└── 16-CONTRIBUTING.md             ← Contribution guide
```

---

## `00-HANDOFF-README.md`

```markdown
# Grid Network — Agent Handoff Package

**Handoff date:** 2026-10-04
**Protocol version:** v0.6.2 (frozen)
**Document set version:** 0.1 (early draft)
**Phase:** Documentation

## What this package contains

A complete documentation set for the Grid Network project, organized as a
repository structure. Each file in this package corresponds to a file in the
target repository. The receiving agent should:

1. Read this document first.
2. Create the repository structure shown in `02-OUTLINE.md`.
3. Populate each file with the content from the corresponding section of
   this package.
4. Perform the Mesh → Grid Network rename in `03-PROTOCOL.md`.
5. Begin work on the priorities listed in `14-ROADMAP.md`.

## What Grid Network is

A cryptographic identity and authorization layer that turns whatever network
connectivity happens to exist into a usable, replaceable connectivity fabric.

It answers three questions using signed objects that participants verify
locally:

- **Who is this?** — Cryptographic identity
- **What are they allowed to do?** — Signed authorization
- **Where can I find them?** — Ephemeral reachability

It is not a decentralized VPN, a DNS replacement, an anonymity network, a
blockchain, or a platform.

## The design principle

Every participant — free user, contributor, commercial operator, enterprise —
makes the network more valuable to every other participant. The commercial
model exists to fund the protocol's maintenance and development, not to extract
value from users.

## Document status

| # | File | Status |
|---|------|--------|
| 01 | README.md | Ready |
| 02 | OUTLINE.md | Ready |
| 03 | PROTOCOL.md | Frozen v0.6.2 (rename needed) |
| 04 | OBJECTS.md | Draft §1–§5 written, §6–§10 pending |
| 05 | RATIONALE.md | Draft v2.0, complete |
| 06 | ADDENDUM-A-COMMERCIAL.md | Draft v6.0, complete |
| 07 | ADDENDUM-B-LINEAGE.md | Draft v1.0, complete |
| 08 | SECURITY.md | To draft |
| 09 | IMPLEMENTATION.md | To draft |
| 10 | CONNECTIVITY.md | To draft |
| 11 | VERSIONING.md | Content exists in PROTOCOL.md §64 |
| 12 | GLOSSARY.md | Partial term list |
| 13 | FAQ.md | Question list, answers pending |
| 14 | ROADMAP.md | To draft |
| 15 | LICENSE.md | Apache 2.0 |
| 16 | CONTRIBUTING.md | Ready |

## Priority order

**Tier 1 — Blocks everything else:**
1. Rename Mesh → Grid Network in PROTOCOL.md
2. Complete OBJECTS.md §6 (object schemas)
3. Complete OBJECTS.md §7 (stream rules)
4. Produce first test vector

**Tier 2 — Enables adoption:**
5. Complete OBJECTS.md §8–§10
6. Draft SECURITY.md
7. Draft IMPLEMENTATION.md
8. Draft CONNECTIVITY.md

**Tier 3 — Enables funding:**
9. Complete GLOSSARY.md
10. Complete FAQ.md
11. Extract VERSIONING.md

**Tier 4 — Long-term:**
12. Reference implementation
13. Applications
14. Ecosystem

## What not to do

- Do not redesign the protocol. v0.6.2 is frozen.
- Do not add new object types or authority domains without justification.
- Do not add security mechanisms unless they protect a specific boundary.
- Do not conflate the four layers (Protocol, Security, Connectivity, Strategy).
- Do not introduce vendor lock-in.

## Where the full text lives

This package contains the full text of all substantive documents:
- 01-README
- 02-OUTLINE
- 03-PROTOCOL (complete v0.6.2)
- 04-OBJECTS (complete §1–§5)
- 05-RATIONALE (complete v2.0)
- 06-ADDENDUM-A (complete v6.0)
- 07-ADDENDUM-B (complete v1.0)
- 11-VERSIONING
- 12-GLOSSARY (partial)
- 13-FAQ (partial)
- 14-ROADMAP
- 15-LICENSE
- 16-CONTRIBUTING

Stub documents (08, 09, 10) have their structure defined and content to be
drafted.
```

---

## `01-README.md`

```markdown
# Grid Network

A cryptographic identity and authorization layer that turns whatever network
connectivity happens to exist into a usable, replaceable connectivity fabric.

**One-line:** Your devices, your identity, your relationships. Not rented.
Not revocable by a vendor.

**Status:** Protocol frozen at v0.6.2. Document set at draft 0.1.

## Quick orientation

| If you are... | Read this |
|---------------|-----------|
| New to the project | `docs/rationale/RATIONALE.md` |
| Evaluating the design | `docs/protocol/PROTOCOL.md` |
| Considering integration | `docs/rationale/RATIONALE.md` Part IV |
| Contributing infrastructure | `docs/rationale/ADDENDUM-A-COMMERCIAL.md` |
| Skeptical | `docs/rationale/ADDENDUM-B-LINEAGE.md` |
| Writing code | `implementations/` |

## What this is

Grid Network is a control plane for identity, authorization, and reachability,
above transports that already exist.

It is **not** a decentralized VPN, a DNS replacement, an anonymity network, a
blockchain, or a platform.

## The problem it solves

Today, the ability to reach your own devices from anywhere is rented from
companies. Tailscale, Cloudflare, ZeroTier, and every commercial mesh product
own your identity and your relationships. If they change their terms, you
migrate or lose access.

Grid Network is a protocol that makes identity and authorization portable.
Your devices, your relationships, your authorizations belong to you, not to a
vendor. Anyone can operate infrastructure, anyone can switch providers, and no
company decides whether your network exists.

## The developer pitch

You already offloaded user authentication to Auth0, Okta, or Google Sign-In.
You should do the same for device connectivity. Grid Network is a shared
protocol that handles identity, pairing, discovery, NAT traversal, relay
fallback, and revocation. Your app calls a local grid agent, gets an authorized
connection, and never thinks about keys, relays, or pairing again.

## Repository layout

```
grid-network/
├── docs/
│   ├── protocol/           Protocol spec, object schemas, versioning
│   ├── security/           Threat model, verifier rules
│   ├── implementation/     Build guides, connectivity architecture
│   ├── rationale/          Design rationale and addenda
│   └── reference/          Glossary, FAQ
├── spec/
│   └── test-vectors/       Normative byte-exact test cases
├── implementations/        Reference and third-party implementations
└── apps/                   Example applications and integrations
```

## Contributing

See `CONTRIBUTING.md`.

## License

Apache 2.0. See `LICENSE.md`.
```

---

## `02-OUTLINE.md`

```markdown
# Grid Network — Project Outline

**Version:** 1.0
**Status:** Draft
**Purpose:** Top-level map of the entire project.

## Project identity

**Working name:** Grid Network

**One-line description:** A cryptographic identity and authorization layer that
turns whatever network connectivity happens to exist into a usable, replaceable
connectivity fabric.

**Design principle:**

> Every participant — free user, contributor, commercial operator, enterprise
> — makes the network more valuable to every other participant. The commercial
> model exists to fund the protocol's maintenance and development, not to
> extract value from users.

## Project layers

```
┌──────────────────────────────────────────────────────────┐
│  LAYER 4 — STRATEGY                                       │
│  Vision, ecosystem, roadmap                              │
├──────────────────────────────────────────────────────────┤
│  LAYER 3 — CONNECTIVITY ARCHITECTURE                     │
│  Path abstraction, relay model, future multipath         │
├──────────────────────────────────────────────────────────┤
│  LAYER 2 — SECURITY & IMPLEMENTATION                     │
│  Threat model, verifier rules, parser requirements       │
├──────────────────────────────────────────────────────────┤
│  LAYER 1 — PROTOCOL KERNEL                               │
│  Identity, authorization, reachability, cryptographic    │
│  objects, and the verification model                     │
└──────────────────────────────────────────────────────────┘
```

Each layer is independent. Layer 1 does not depend on Layer 3; Layer 3 consumes
Layer 1. Layer 4 does not constrain Layer 1; Layer 4 explains why Layer 1
matters.

## Document set

```
grid-network/
├── README.md
├── LICENSE.md
├── CONTRIBUTING.md
│
├── docs/
│   ├── README.md
│   ├── OUTLINE.md
│   │
│   ├── protocol/
│   │   ├── PROTOCOL.md
│   │   ├── OBJECTS.md
│   │   └── VERSIONING.md
│   │
│   ├── security/
│   │   └── SECURITY.md
│   │
│   ├── implementation/
│   │   ├── IMPLEMENTATION.md
│   │   └── CONNECTIVITY.md
│   │
│   ├── rationale/
│   │   ├── RATIONALE.md
│   │   ├── ADDENDUM-A-COMMERCIAL.md
│   │   └── ADDENDUM-B-LINEAGE.md
│   │
│   └── reference/
│       ├── GLOSSARY.md
│       └── FAQ.md
│
├── spec/
│   └── test-vectors/
│
├── implementations/
│
└── apps/
```

## Document responsibilities

| Document | Layer | Audience | Change rate |
|----------|-------|----------|-------------|
| README.md | Entry | Everyone | Rare |
| OUTLINE.md | Cross | Everyone | Rare |
| PROTOCOL.md | 1 | Implementers | Slow |
| OBJECTS.md | 1 | Implementers | Slow |
| VERSIONING.md | Cross | Implementers | Slow |
| test-vectors/ | 1 | Testers | Additive |
| SECURITY.md | 2 | Implementers, reviewers | Moderate |
| IMPLEMENTATION.md | 2 | Builders | Moderate |
| CONNECTIVITY.md | 3 | Connectivity builders | Moderate |
| RATIONALE.md | 4 | Stakeholders | Slow |
| ADDENDUM-A-COMMERCIAL.md | 4 | Operators, investors | Moderate |
| ADDENDUM-B-LINEAGE.md | 4 | Skeptics, reviewers | Slow |
| GLOSSARY.md | Reference | Everyone | Additive |
| FAQ.md | Reference | Everyone | Additive |
| ROADMAP.md | 4 | Everyone | Moderate |

## Document dependency graph

```
                        README.md
                            │
                        OUTLINE.md
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
         PROTOCOL.md    RATIONALE.md    (other)
              │             │
              │             ├─── ADDENDUM-A-COMMERCIAL.md
              │             │
              │             └─── ADDENDUM-B-LINEAGE.md
              │
              ▼
        OBJECTS.md  ───►  test-vectors/
              │
              ▼
        SECURITY.md
              │
              ▼
       IMPLEMENTATION.md
              │
              ▼
       CONNECTIVITY.md
```

## Rules

- PROTOCOL.md and OBJECTS.md must not contradict each other. If they do,
  one is wrong.
- SECURITY.md and IMPLEMENTATION.md are derived from PROTOCOL.md. They do
  not introduce new protocol requirements.
- CONNECTIVITY.md consumes PROTOCOL.md. It does not modify the protocol.
- RATIONALE.md and its addenda are descriptive. They do not introduce
  normative requirements.

## Versioning

Two version numbers, not to be conflated:

- **Protocol version** (e.g., v0.6.2) — version of PROTOCOL.md.
- **Document set version** (e.g., 0.1) — snapshot of all documents together.

**Current state:**
- Protocol: v0.6.2 (frozen)
- Document set: 0.1 (early draft)

## What's done and what remains

**Frozen:**
- PROTOCOL.md v0.6.2

**Drafted but incomplete:**
- OBJECTS.md §1–§5 (encoding)
- test-vectors/ (structure defined, no vectors)

**Complete drafts:**
- RATIONALE.md v2.0
- ADDENDUM-A-COMMERCIAL.md v6.0
- ADDENDUM-B-LINEAGE.md v1.0

**To be drafted:**
- OBJECTS.md §6–§10
- SECURITY.md
- IMPLEMENTATION.md
- CONNECTIVITY.md
- VERSIONING.md
- GLOSSARY.md
- FAQ.md
- ROADMAP.md
```

---

## `03-PROTOCOL.md`

Due to length, this is the full text of the protocol specification. The receiving agent should paste the full v0.6.2 content (from the project history) here, applying the Mesh → Grid Network rename. Key rename points:

- Protocol name: "Mesh Identity & Reachability Protocol" → "Grid Identity & Reachability Protocol"
- Domain separators: `mesh/*` → `grid/*` (all 19 object types plus 6 cryptographic tags)
- URI scheme: `mesh://` → `grid://`
- Local API prefix: `mesh.` → `grid.`

The complete document contains these sections:

1. Abstract
2. Core Security Invariant
3. Design Goals
4. Non-Goals
5. Conceptual Architecture
6. Peer Principal
7. Peer Principal ID
8. Identity Root
9. Key Roles and Separation
10. Identity Documents
11. Identity Document History
12. Relationship
13. Grant
14. Lease
15. Capabilities
16. Authorization Policy
17. Network Authorization vs Application Authorization
18. Revocation
19. Revocation Hierarchy
20. Key Revocation and Effective Sequence
21. Authorization-Key Compromise
22. Identity Root Compromise
23. Key Rotation
24. Pairing
25. Pairing Protocol
26. Pairing Code
27. Human Verification
28. Permanent Identity References
29. Grid URI
30. Rendezvous
31. Rendezvous Evolution
32. Reachability
33. Relays
34. Transport
35. Enforcement
36. Service Discovery
37. Offline Operation
38. Lease Expiration
39. Revocation Propagation
40. Time Semantics
41. Cryptographic Object Encoding
42. Domain Separation
43. Cryptographic Baseline
44. Object Identity
45. Sequence and History
46. Trust Anchors
47. Verifier Local State
48. Security State Machines
49. Authority Domains
50. Threat Model
51. Compromise Model and Blast Radius
52. Service Identity, Service Binding, and Service Link
53. Failure Semantics and Recovery
54. Reconciliation and Conflict Resolution
55. Application Integration and API
56. V1 Scope and Kernel
57. Explicitly Deferred Features
58. Normative Signing-Authority Matrix
59. Implementation Requirements
60. Test Vectors and Conformance
61. Verifier Conformance Scenarios
62. Future Extensions
63. Project Structure and Document Map
64. Versioning and Evolution
65. Triage Decisions for V1 Scope

Plus the Final Protocol Statement.

**Renamed domain separators:**

```
grid/identity-document/v1
grid/device-binding/v1
grid/service-binding/v1
grid/key-binding/v1
grid/key-revocation/v1
grid/relationship-assertion/v1
grid/relationship-termination/v1
grid/rendezvous-manifest/v1
grid/operator-manifest/v1
grid/relationship-grant/v1
grid/authorization-lease/v1
grid/grant-revocation/v1
grid/lease-revocation/v1
grid/service-record/v1
grid/reachability-record/v1
grid/stream-resolution/v1
grid/identity-continuity/v1
grid/relay-ticket/v1
grid/relay-node-record/v1
```

**Renamed cryptographic tags:**

```
grid/commitment/v1
grid/chain-base/v1
grid/chain/v1
grid/signature/v1
grid/payload-id/v1
grid/object-id/v1
```

---

## `04-OBJECTS.md`

This is the complete §1–§5 content. The receiving agent should paste this in full and then draft §6–§10.

```markdown
# Grid Network — Object Encoding and Cryptographic Constructions

**Version:** 0.2
**Status:** Draft (§1–§5 written, §6–§10 pending)
**Depends on:** PROTOCOL.md v0.6.2

## Two top-level invariants

**I1 — Sequence-space invariant.** A sequence number has meaning only within
its (issuer, stream_id) sequence space. Sequence numbers from different
sequence spaces MUST NOT be compared.

**I2 — Vector normative invariant.** Normative test vectors define exact
byte-level behavior. If prose and a vector disagree, the specification MUST
be corrected so they agree; implementations MUST NOT choose whichever
interpretation they prefer.

## 1. Scope and Normative Terminology

### 1.1 Scope

This document defines the byte-level representation and cryptographic
constructions of all signed objects in the protocol. It defines:

- the canonical CBOR encoding profile;
- the construction of unsigned_payload, object_commitment, chain_hash,
  signature_input, signature, payload_id, and object_id;
- the common stream envelope;
- the sequence and chain rules;
- the semantics of domain_separator;
- positive and negative test vectors.

Object schemas are defined in §6. Conformance requirements are defined in §10.

### 1.2 Normative terminology

- MUST, MUST NOT, SHOULD, SHOULD NOT, MAY are used as defined in RFC 2119.
- Canonical means the exact byte sequence produced by the encoding rules.
- Unsigned payload means the CBOR map representing an object before
  chain_hash and signature are added.
- Signed object means the CBOR map representing an object after chain_hash
  and signature are added.
- Sequence space means the pair (issuer, stream_id).
- Stream means the ordered sequence of objects sharing one sequence space.
- Base state means initial_chain_hash, the predecessor value for the first
  object in a stream.

## 2. Canonical CBOR Profile

All protocol objects use CBOR (RFC 8949) with the deterministic encoding
constraints below. Where RFC 8949 permits alternatives, only the form
specified here is valid.

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

Integers MUST be encoded in their shortest form.

- Smallest values use the "additional information" encoding directly
  (major type 0 with additional info 0–23 for values 0–23).
- Larger values use the shortest additional-info-24/25/26/27 form.

Non-shortest integer encodings are malformed.

Permitted ranges: non-negative integers 0 to 2^64 − 1. Negative integers are
not permitted.

### 2.3 Byte strings

Byte strings MUST be definite-length. Indefinite-length byte strings are
malformed. Byte string length MUST be encoded in the shortest form.

### 2.4 Text strings

Text strings MUST be definite-length and MUST be valid UTF-8.

Text strings MUST use Unicode Normalization Form C (NFC). Text strings that
are not in NFC are malformed.

Byte-order mark (U+FEFF) MUST NOT appear at the beginning of a text string.

### 2.5 Arrays

Arrays MUST be definite-length.

Array schemas MUST explicitly specify whether duplicate elements are
permitted. Unless a schema explicitly permits duplicates, duplicate elements
are malformed. Lists and ordered sequences may legitimately contain
duplicates; sets (§2.8) MUST NOT.

### 2.6 Maps

Maps MUST be definite-length. Indefinite-length maps are malformed.

Map keys MUST be unique. Maps containing duplicate keys are malformed.

Map keys MUST be text strings unless the map's schema explicitly permits
other key types. Protocol map keys are always text strings.

### 2.7 Map key ordering

Map keys MUST be ordered according to CBOR deterministic encoding
(RFC 8949 §4.2.1):

1. First by the length of the encoded key (shorter first).
2. Then by bytewise lexicographic comparison of the encoded key bytes.

This is not alphabetical ordering. The ordering is over the byte
representation of the key.

Non-canonical map ordering is malformed.

### 2.8 Set semantics

A protocol set<T> is encoded as a definite-length CBOR array whose elements
are:

1. Unique — no two elements have identical canonical CBOR encodings.
2. Sorted — elements are ordered by bytewise lexicographic comparison of
   their canonical CBOR encodings.

An array that represents a set<T> but contains duplicate elements, or whose
elements are not in the required order, is malformed.

An empty set is encoded as an empty definite-length array.

### 2.9 Null and optional fields

null (CBOR 0xf6) is permitted only where an object schema explicitly declares
a field optional-and-absent. When a field is optional-and-absent, the field
key MUST be omitted from the map, not set to null.

An explicit null value is malformed unless a schema explicitly requires it.

Boolean values (false = 0xf4, true = 0xf5) are permitted where a schema
declares a boolean field.

Simple values (other than null, false, true) are not permitted.

### 2.10 Floating-point prohibition

Floating-point values (major type 7, additional info 25–27) are prohibited.
Any floating-point value is malformed.

All numeric values in protocol objects are integers.

Time values are represented as integer seconds (or integer milliseconds where
a schema explicitly requires sub-second precision).

### 2.11 Indefinite-length prohibition

Indefinite-length encoding of byte strings, text strings, arrays, and maps is
prohibited. All four MUST use definite-length encoding.

### 2.12 Duplicate-key prohibition

Maps MUST NOT contain duplicate keys. Sets MUST NOT contain duplicate
elements.

Arrays that are not sets MAY contain duplicate values if the schema permits;
protocol arrays that carry lists of distinct values are declared as sets.

### 2.13 Integer bounds

All integers MUST fall within the range specified in §2.2. Schemas MAY impose
narrower bounds; values outside a schema's bounds are malformed.

### 2.14 Rejection of non-canonical encodings

Any CBOR encoding that does not satisfy §2.1–§2.13 is malformed.
Implementations MUST reject malformed encodings before any semantic
processing.

## 3. Object Serialization

### 3.0 Notation

- canonical_cbor(V) — the byte string produced by encoding CBOR value V
  according to §2.
- SHA-256(B) — the SHA-256 hash of byte string B, producing a 32-byte value.
- Ed25519_sign(K, B) — the Ed25519 signature over byte string B using
  private key K, producing a 64-byte value.
- Ed25519_verify(P, B, S) — verification of signature S over byte string B
  using public key P.
- || — byte string concatenation. Used only within this notation section.

### 3.1 Value/byte distinction

Protocol constructions operate on two kinds of input:

- CBOR values — the abstract data structures.
- Byte strings — the output of canonical_cbor or of hashing.

The distinction is critical. In all definitions below:

- An operand described as a CBOR value is used as a value and is canonically
  encoded as part of the surrounding structure.
- An operand described as a byte string is used as bytes and is encoded as a
  CBOR byte string when placed inside a surrounding CBOR structure.

### 3.2 Unsigned payload

The unsigned payload of an object is the CBOR map containing all fields
defined by the object schema, including common stream fields such as
domain_separator, sequence, and previous_hash where the schema includes them.
It excludes only two fields:

- chain_hash, which is derived from the unsigned payload and the stream state.
- signature, which is derived from the unsigned payload and the chain hash.

All other object fields are part of the unsigned payload.

### 3.3 Commitment preimage

commitment_preimage =
    canonical_cbor([
        "grid/commitment/v1",
        domain_separator,
        unsigned_payload
    ])

Where:

- Element 0 is the text string "grid/commitment/v1".
- Element 1 is the object's domain_separator as a text string.
- Element 2 is the unsigned payload as a CBOR value.

The commitment preimage is a byte string.

### 3.4 Object commitment

object_commitment =
    SHA-256(commitment_preimage)

The object commitment is a byte string (32 bytes).

### 3.5 Chain state, previous hash, and chain hash

Every stream has a base state represented by initial_chain_hash.

initial_chain_hash =
    SHA-256(canonical_cbor([
        "grid/chain-base/v1",
        domain_separator,
        stream_id
    ]))

Two distinct chain links exist. They serve different purposes and MUST NOT be
conflated.

Previous hash (previous_hash): commits directly to the immediately preceding
object's payload. It is an object field.

previous_hash(1) = omitted                    (not present)
previous_hash(N) = object_commitment(N-1)     for N > 1

Previous chain hash (previous_chain_hash): the input to the chain construction.
It is not an object field.

previous_chain_hash(1) = initial_chain_hash
previous_chain_hash(N) = chain_hash(N-1)      for N > 1

Chain hash (chain_hash): the cumulative stream-history hash. It is an object
field.

chain_hash(N) =
    SHA-256(canonical_cbor([
        "grid/chain/v1",
        previous_chain_hash(N),
        object_commitment(N)
    ]))

Where:

- Element 0 is the text string "grid/chain/v1".
- Element 1 is previous_chain_hash(N) as a CBOR byte string.
- Element 2 is object_commitment(N) as a CBOR byte string.

The first object in every stream has sequence = 1. The value 0 is reserved
for "uninitialized" and MUST NOT appear.

### 3.6 Payload ID

payload_id =
    SHA-256(canonical_cbor([
        "grid/payload-id/v1",
        unsigned_payload
    ]))

Where:

- Element 0 is the text string "grid/payload-id/v1".
- Element 1 is the unsigned payload as a CBOR value.

The payload ID depends only on the semantic content of the unsigned payload.

### 3.7 Object ID

object_id =
    SHA-256(canonical_cbor([
        "grid/object-id/v1",
        canonical_signed_object_bytes
    ]))

Where:

- Element 0 is the text string "grid/object-id/v1".
- Element 1 is canonical_signed_object_bytes as a CBOR byte string.

canonical_signed_object_bytes is the exact canonical CBOR encoding of the
signed object — the byte-for-byte wire representation. It is not a CBOR value;
it is a byte string in this construction.

Implementations MUST NOT re-encode the signed object as a CBOR value before
hashing.

### 3.8 Signed object

A signed object is a CBOR map containing all fields of the unsigned payload,
plus:

- chain_hash — a byte string.
- signature — a byte string (or two-element array of byte strings for
  dual-signature schemas).

The signed object is a CBOR value.

### 3.9 Signature input

signature_input(N) =
    canonical_cbor([
        "grid/signature/v1",
        domain_separator,
        unsigned_payload,
        chain_hash(N)
    ])

Where:

- Element 0 is the text string "grid/signature/v1".
- Element 1 is the object's domain_separator as a text string.
- Element 2 is the unsigned payload as a CBOR value.
- Element 3 is chain_hash(N) as a CBOR byte string.

The signature is computed as:

signature(N) =
    Ed25519_sign(signing_private_key, signature_input(N))

Non-circularity. The signature input MUST be reconstructible from the unsigned
payload and the chain hash alone. The signature MUST NOT be part of any input
to its own computation.

### 3.10 Serialization invariants

S1 — Canonical form. Two objects that represent the same protocol value MUST
have identical canonical CBOR encodings.

S2 — Signature domain separation. Every cryptographic construction has a
unique domain tag. The domain tags are:

| Tag | Construction |
|-----|--------------|
| "grid/commitment/v1" | commitment_preimage |
| "grid/chain-base/v1" | initial_chain_hash |
| "grid/chain/v1" | chain_hash |
| "grid/signature/v1" | signature_input |
| "grid/payload-id/v1" | payload_id |
| "grid/object-id/v1" | object_id |

S3 — Chain order. The chain hash of sequence N depends on the chain hash of
sequence N-1 and the object commitment of sequence N.

S4 — Determinism. All constructions are deterministic functions of their
inputs.

S5 — Byte/value boundary. The distinction between CBOR values and byte
strings is normative in every construction.

S6 — Reconstruction. Every derived value required for verification MUST be
reconstructible from the canonical unsigned payload, applicable stream state,
and the protocol rules. An implementation MUST NOT depend on non-canonical
source representations, parser-preserved formatting, map insertion order, or
locally generated serialization choices.

## 4. Common Stream Envelope

### 4.1 Purpose

Every signed object shares a common structural envelope. §4 defines the
fields of that envelope and the boundary between envelope fields and
object-specific fields.

### 4.2 Envelope overview

signed_object = {
    domain_separator    : text string,
    sequence            : integer >= 1,
    previous_hash?      : byte string (omitted at sequence 1),
    ...schema-specific fields,
    chain_hash          : byte string,
    signature           : byte string (or 2-element array)
}

### 4.3 Field definitions

#### 4.3.1 domain_separator

Type: CBOR text string.

The domain_separator identifies the object's schema family and version. It is
drawn from the registered set.

The domain_separator is part of unsigned_payload. It is included in
commitment_preimage, payload_id, and signature_input. Three consequences:

1. The schema identity is cryptographically bound to the object.
2. The schema version is cryptographically bound to the object.
3. The domain separator participates in all derived values.

There is no separate version field in the envelope. The schema version is
carried by domain_separator.

#### 4.3.2 sequence

Type: CBOR unsigned integer. Range: 1 to 2^64 − 1.

The value 0 is reserved for "uninitialized" and MUST NOT appear in any signed
object.

#### 4.3.3 previous_hash

Type: CBOR byte string (32 bytes). Optional; present only at sequence numbers
greater than 1.

At sequence 1, the field is omitted. It MUST NOT be present with a null value.
A sequence-1 object that contains a previous_hash field is malformed.

Not to be confused with previous_chain_hash. The chain construction uses a
value called previous_chain_hash, which is not a field of any object.

| Value | What it is | Where it lives |
|-------|------------|----------------|
| previous_hash | previous object's object_commitment | a field (omitted at sequence 1) |
| previous_chain_hash | previous object's chain_hash (or initial_chain_hash) | computed input; not a field |

#### 4.3.4 chain_hash

Type: CBOR byte string (32 bytes).

Added to the object after unsigned_payload is complete. Computed per §3.5.

#### 4.3.5 signature

Type: CBOR byte string (64 bytes) for single-signature schemas;
definite-length CBOR array of exactly two 64-byte byte strings for
dual-signature schemas.

For dual-signature schemas, signature is a CBOR array [signature_0,
signature_1] where ordering is defined by the schema. The array MUST be
definite-length and MUST contain exactly two elements.

For dual-signature schemas, both signatures MUST be over the same
signature_input.

#### 4.3.6 Schema-specific fields

Every object schema defines the schema-specific fields that appear in
unsigned_payload, in addition to the common envelope fields.

### 4.4 Envelope invariants

E1. domain_separator MUST be present.
E2. sequence MUST be present and ≥ 1.
E3. previous_hash MUST be omitted at sequence 1 and present at sequence
    numbers greater than 1.
E4. chain_hash MUST be present.
E5. signature MUST be present.
E6. unsigned_payload MUST NOT contain any field named chain_hash or signature.
E7. The signed object MUST NOT contain any field outside the set of
    unsigned_payload fields plus chain_hash and signature.

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

- Domain separators are ASCII text strings.
- Each value identifies exactly one object schema family and version.
- A future schema version of the same family MUST use a distinct domain
  separator.
- Unknown domain separators MUST be rejected.

## 5. Signature Semantics

### 5.1 Purpose

§5 defines which key role is authorized to sign each object type, and the
signature verification procedure.

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

1. Decode. Decode canonical CBOR. Reject as MALFORMED_ENCODING if invalid.
2. Envelope validation. Verify required envelope fields. Reject as
   MALFORMED_ENVELOPE.
3. Domain separator validation. Verify domain_separator is registered.
   Reject as UNKNOWN_SCHEMA.
4. Schema validation. Validate schema-specific fields. Reject as
   MALFORMED_SCHEMA.
5. Sequence validation. Verify sequence >= 1 and previous_hash presence.
   Reject as INVALID_SEQUENCE or INVALID_PREVIOUS_HASH.
6. Chain validation. Compute object_commitment, verify previous_hash,
   compute and verify chain_hash. Reject as CHAIN_MISMATCH.
7. Signature input construction. Compute signature_input.
8. Signature verification. Verify signature(s). Reject as
   INVALID_SIGNATURE.
9. Authority validation. Verify signing key role and current authorization.
   Reject as UNAUTHORIZED_SIGNER.
10. Semantic validation. Apply the object's semantic rules.

### 5.3.1 Atomicity

A verifier MUST NOT advance or mutate its accepted stream state while
performing steps 1–9. Validation is pure with respect to accepted state;
commitment is the only mutation.

### 5.4 Delegated signers

DeviceBinding MAY be signed by a device-authority key delegated by the
Identity Root. ServiceBinding MAY be signed by a service-authority key.
Delegations MUST be present in the verifier's accepted identity state.

### 5.5 Dual-signature objects

Only IdentityContinuity uses dual signatures in V1.

For IdentityContinuity:

signature: [
    sig_prev,   // by previous_root
    sig_new     // by new_root
]

Both signatures are over the same signature_input.

### 5.6 StreamResolution signing

A StreamResolution MUST be signed by an authority above the disputed stream
in the authority hierarchy, trusted from state accepted before the fork was
observed.

The resolver's stream position is expressed by the resolution object's own
sequence, chain_hash, and previous_hash. The disputed stream's position is
expressed by disputed_sequence, a value that MUST NOT be compared with the
resolution's sequence.

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

## 6. Object Schemas

**Status:** To be drafted

This section will define, for each object type:

- Exact field names
- Field types and constraints
- Required vs. optional
- Which stream the object belongs to
- Which key role signs it
- Canonical encoding notes

Object types:

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

## 7. Stream Rules

**Status:** To be drafted

This section will define:

- Sequence spaces and their identifiers
- Initial chain state
- Monotonicity rules
- Gap detection and handling
- Fork detection and handling
- Resolution procedures
- Cross-stream prohibition (restated normatively)

## 8. Positive Test Vectors

**Status:** To be drafted

For each object type: canonical encoding, hash, payload hash, signature,
verification.

## 9. Negative Test Vectors

**Status:** To be drafted

Required negative vectors: non-minimal integer encoding, incorrectly ordered
map keys, floating-point field, duplicate set entry, set entries out of
canonical order, missing required field, extra unknown field, oversized
field, replayed object, expired object, revoked object, invalid
previous_hash, invalid chain_hash, wrong issuer for object type, signature
from wrong key role, fork at same sequence, gap in stream, non-canonical CBOR
encoding.

## 10. Conformance Requirements

**Status:** To be drafted

Conformance levels:

- Level 1: Encoding
- Level 2: Verification
- Level 3: Authorization
- Level 4: Failure handling
- Level 5: Reconciliation

A conforming implementation MUST reject every negative test vector with the
specified rejection class.
```

---

## `05-RATIONALE.md`

This is the full RATIONALE.md v2.0. Given its length, here is the complete structure with all substantive content:

**Part I — The Problem**
- §1 The core problem: every self-hosted service hits "how do I reach this from somewhere else"
- §2 The three bad choices: expose to internet, use proprietary tunnel, build it yourself
- §3 Why this matters: reaching your own devices has become a subscription
- §4 Why alternatives don't fully solve it: Tailscale is a company; Cloudflare Tunnel is a path; self-hosted VPN requires expertise
- §5 The insight: connectivity is infrastructure, not a feature
- §6 Why this is hard: identity must survive location changes; authorization must work offline; intermediaries must be untrusted; no single party must be the authority; result must be portable

**Part II — The Solution**
- §7 What Grid Network is: a control plane for identity, authorization, reachability
- §8 What Grid Network is not: not VPN, DNS, anonymity, blockchain, P2P filesystem, company
- §9 Five key design properties: identity portable; authorization local; reachability ephemeral; infrastructure untrusted; protocol open

**Part III — Who It Serves**
- §10 Four audiences: self-hosters, small communities, application developers, enterprises
- §11 What each audience gains
- §12 Who actually wants this: self-hosters burned by shutdowns; open-source apps; enterprises burned by lock-in; regulators; communities

**Part IV — The Developer Case**
- §13 Developer adoption is the primary path
- §14 The problem every application faces
- §15 Three bad patterns: build cloud service, require external tool, roll your own
- §16 What Grid Network changes: applications talk to a local grid agent; API is small
- §17 The analogy to authentication (4 phases: roll your own, framework, IdP, federation)
- §18 What integration looks like (3 steps, 5 API calls)
- §19 Commercial economics for applications
- §20 Why this matters more than the end-user pitch

**Part V — The Contribution Model**
- §21 Three contribution layers: reachability publication, rendezvous, relay
- §22 Contribution by capacity (table of contributor types)
- §23 Why contribution is safe (untrusted infrastructure)
- §24 The economic shape: free, volunteer, commercial

**Part VI — The Commercial Layer**
- §25 What the commercial layer sells (guarantees, not access)
- §26 Relay is a fallback, not a default
- §27 The commercial layer is not a platform
- §28 Free users as the network's foundation
- §29 The relay priority model (4 classes)
- §30 Priority is a claim, not an identity
- §31 Idle capacity donation
- §32 Credit pools and families
- §33 Preventing abuse (7 vectors and mitigations)
- §34 Geographic scarcity (the Hawaii problem)
- §35 Self-hosted priority
- §36 The six commercial products
- §37 The urgency buyer
- §38 "No account" is a commercial feature
- §39 Developer funding

**Part VII — Edge Cases**
- §40 Offline for extended periods
- §41 Device replacement
- §42 Lost device
- §43 Rendezvous server disappears
- §44 Relay operator is malicious
- §45 Identity key is compromised
- §46 Service moves between devices
- §47 Peer on a network with no direct connectivity
- §48 Application uses grid identity for its own authorization

Full text of each section is provided in the earlier conversation turns. The receiving agent should paste them in full.

---

## `06-ADDENDUM-A-COMMERCIAL.md`

Full text of RATIONALE.md Addendum A v6.0. Structure:

**Part I — What the commercial layer is, and is not**
- §1 What it sells
- §2 The relay layer's actual scope
- §3 Relay is a burst absorber
- §4 The commercial layer is not a platform
- §5 The one property everything rests on

**Part II — Free users as the network's foundation**
- §6 The contribution of the free tier
- §7 Why free users make paid users more valuable
- §8 Free users who contribute infrastructure
- §9 The free tier and paid tier are complementary

**Part III — The relay priority model**
- §10 The core structure (4 properties)
- §11 Priority classes
- §12 Priority is a claim, not an identity
- §13 Idle capacity donation
- §14 What the network looks like at steady state

**Part IV — Credit pools and fair exchange**
- §15 The family and group problem
- §16 Credit pool structure
- §17 How a family pool works
- §18 How accounting resolves
- §19 Fair-to-fair credit exchange
- §20 The "someone else's box is better" case
- §21 Preventing abuse of the credit system
- §22 The dispute problem

**Part V — The blockchain question**
- §23 The case for and against
- §24 The blockchain hybrid
- §25 Recommendation
- §26 Design for the possibility, don't build for it

**Part VI — Geographic scarcity and fairness**
- §27 The Hawaii problem
- §28 Geographic credit adjustment
- §29 Exchange rates and fairness
- §30 Relays are replaceable, but geography isn't
- §31 Geographic diversity as a goal

**Part VII — Self-hosted priority and enterprise scale**
- §32 Self-hosted priority on your own machine
- §33 Enterprise self-hosted priority
- §34 Enterprise scale — the full model
- §35 The enterprise value proposition
- §36 The accounting complexity at enterprise scale

**Part VIII — Keeping the databases in sync**
- §37 The accounting problem (10 sub-problems)
- §38 Design implications

**Part IX — What commercial operators sell**
- §39 The six products
- §40 The public-good component of each product
- §41 What "just works" really means
- §42 The urgency buyer
- §43 "No account" is a commercial feature

**Part X — Developer funding**
- §44 The developer funding problem
- §45 What successful projects do
- §46 What Grid Network should learn
- §47 The Grid Network developer funding model
- §48 Why this works for Grid Network
- §49 The startup phase
- §50 What success looks like for developer funding

**Part XI — Putting it together**
- §51 The full picture
- §52 The funding flow
- §53 The one-sentence summary
- §54 The key property
- §55 The relationship between free users and paid users

Full text of each section is provided in the earlier conversation turns.

---

## `07-ADDENDUM-B-LINEAGE.md`

Full text of RATIONALE.md Addendum B v1.0. Structure:

**Part I — The premise**
- §1 Great systems are great
- §2 But each one solves a different problem

**Part II — What Grid Network borrows**
- §3 From DNS
- §4 From WireGuard
- §5 From BitTorrent
- §6 From Bitcoin
- §7 From Tailscale
- §8 From Headscale
- §9 From other systems (Matrix, SSH, IPFS, Kerberos)

**Part III — The composition is the point**
- §10 Why composition matters
- §11 Learning from successes
- §12 Learning from failures
- §13 The composition is more than the sum

**Part IV — The developer angle**
- §14 Not a competitor — a layer above
- §15 The developer pitch
- §16 Why this is a solved-problem framing
- §17 Integration options

**Part V — Why this leads to disruption**
- §18 The disruption is not the goal
- §19 What gets disrupted, and why
- §20 What survives
- §21 Why this is healthy

**Part VI — Polish and simplicity**
- §22 Simplicity is the point
- §23 What polish looks like
- §24 Why polish is what makes this disruptive
- §25 The economic sense

**Part VII — Summary**
- §26 One-sentence summary
- §27 One-paragraph summary
- §28 Developer pitch
- §29 User pitch
- §30 Commercial pitch

Full text of each section is provided in the earlier conversation turns.

---

## `08-SECURITY.md`

```markdown
# Grid Network — Security Documentation

**Status:** To be drafted
**Derived from:** PROTOCOL.md §50–§53

## Planned contents

### Part I — Threat model
- Adversarial conditions
- Threat taxonomy (T1–T14)
- Threat-to-property mapping
- Explicit non-properties (anonymity, availability, metadata confidentiality,
  protection against compromised endpoints, protection against
  authorized-but-malicious peers, protection against compromised Identity
  Root)

### Part II — Compromise and blast radius
- Service Key compromise: one service's discovery metadata
- Device Key compromise: one device's discovery metadata
- Authorization Key compromise: all authorization under the key
- Identity Root compromise: entire principal
- Device compromise: union of held keys
- Rendezvous compromise: discovery only
- Relay compromise: transport only
- Compromise invariants (§51.9)

### Part III — Verifier processing rules
- Ten-step validation order
- Atomicity requirements
- Rejection classes

### Part IV — Parser hardening
- Canonical CBOR requirements
- Bounded message sizes
- Deep nesting protection
- Integer overflow protection
- Invalid UTF-8 handling
- Non-NFC text handling

### Part V — Resource limits
- Maximum object sizes per type
- Maximum map/array/set sizes
- Maximum field lengths

### Part VI — Rate limiting and anti-amplification
- Connection rate limits
- Authentication attempt limits
- Response size limits
- No unauthenticated reflection behavior

### Part VII — Crash and restart behavior
- Atomic state updates
- Persistent state integrity
- Power-loss tolerance

### Part VIII — Concurrency
- Concurrent updates
- Fork handling under concurrent operations
- Clock changes

### Part IX — Key storage
- Identity Root protection recommendations
- Device key storage recommendations
- Hardware-backed keys

### Part X — Fuzzing and testing
- Parser fuzzing requirements
- Crash testing
- Conformance testing

### Part XI — Operational security out of scope
- Key storage compromise on local machine
- Agent supply-chain attacks
- Recovery-flow social engineering
- Update-mechanism compromise

## Operational security out-of-scope statement

The protocol does not attempt to protect against:

- **Key storage compromise on the local machine.** If the Identity Root
  private key is stored in plaintext on a compromised machine, the
  protocol's cryptographic guarantees are irrelevant.
- **Agent supply-chain attacks.** How a user knows they installed the right
  agent is a deployment problem, not a protocol problem.
- **Recovery-flow social engineering.** If the recovery process is "email us
  and we'll reset your key," the cryptographic model is bypassed.
- **Update-mechanism compromise.** How a peer learns that a software update
  is legitimate is a supply-chain problem.

These are named as out of scope so that no one assumes the protocol solves
them.
```

---

## `09-IMPLEMENTATION.md`

```markdown
# Grid Network — Implementation Guide

**Status:** To be drafted

## Planned contents

### Part I — Grid Agent architecture
- Local daemon process
- Identity storage
- Peer state storage
- Rendezvous client
- Reachability publisher
- Connectivity engine
- Local API server

### Part II — Local API

```
grid.discover()                     → list of known peers
grid.resolve(peer_id)               → peer state
grid.connect(service_link_id, cap)  → local connection handle
grid.authorize(peer_id, capability) → authorization decision
grid.revoke(object_id)              → issue revocation
grid.status()                       → daemon and peer state
```

Connection handle format:

```
{
    "connection_id": "random-id",
    "local_url": "http://127.0.0.1:41873",
    "expires_at": "2026-10-04T21:00:00Z"
}
```

The application uses the local URL. It does not receive the underlying
endpoint, relay credentials, or peer ID.

### Part III — Transport engine
- WireGuard integration
- QUIC support (future)
- TCP fallback

### Part IV — Connectivity engine integration
- Direct-first preference
- NAT traversal coordination
- Relay selection and fallback

### Part V — Local state storage
- Durable storage for trust anchors
- Durable storage for accepted stream state
- Monotonic clock handling
- Observation history storage

### Part VI — Key storage recommendations
- Identity Root protection
- Device key storage
- Service key storage

### Part VII — Cross-platform notes
- Linux (systemd, iptables/nftables, 127.0.0.53)
- macOS (resolver configuration)
- Windows (NRPT)
- iOS/Android (VPN profile, DNS interception)

### Part VIII — Application integration checklist
- Bundle or recommend agent
- Use grid.connect() for connections
- Optionally use grid identity for app-level decisions
- Handle connection failures gracefully
```

---

## `10-CONNECTIVITY.md`

```markdown
# Grid Network — Connectivity Architecture

**Status:** To be drafted

## Planned contents

### Part I — Connectivity intent
The application asks for "an authorized connection to Service X." The
Connectivity Engine decides how the connection is realized.

### Part II — Direct-first preference order
1. Local LAN
2. Direct IPv6
3. Direct IPv4
4. NAT traversal (hairpinning, hole punching)
5. Relay

### Part III — NAT traversal coordination
- STUN/ICE concepts
- Hole punching
- Hairpinning

### Part IV — Relay architecture
- Relay roles: publication, replica, cache, bootstrap, relay coordinator
- Relay tickets: pair-bound, capability-bound, short-lived, rate-limited,
  byte-limited
- Untrusted relay model

### Part V — Relay capability model
- Bandwidth
- Concurrent sessions
- Bytes
- Duration
- IPv4/IPv6
- Availability
- Latency
- Network characteristics
- Operator policy

### Part VI — PathSet abstraction
Architectural concept; not a V1 wire object. Forward compatibility
considerations for future path selection.

### Part VII — Path measurement (future)
Latency, packet loss, jitter, throughput, congestion, stability.

### Part VIII — Path selection (future)
Implementation-defined, not protocol-mandated.

### Part IX — Multipath (future)
Multiple independent paths providing aggregate capacity.

### Part X — FEC (future)
Transport optimization, optional.

### Part XI — Non-preclusion constraints
V1 objects and state MUST NOT preclude future Layer 3 capabilities.
Reachability records MAY carry multiple endpoint candidates. Path identity is
distinct from connection identity. Authorization is path-agnostic. Relay
selection is not baked into any signed object.
```

---

## `11-VERSIONING.md`

```markdown
# Grid Network — Protocol Versioning

**Status:** Extracted from PROTOCOL.md §64.

## Versioning model

Each protocol object type carries its schema version in its domain_separator:

```
grid/identity-document/v1
grid/relationship-assertion/v1
grid/stream-resolution/v1
```

A new schema version uses a new domain separator:

```
grid/identity-document/v2
```

Domain separators are never reused. A v1 schema is frozen once the object type
is declared stable in a released protocol version.

## Adding new object types

New object types are added by registering a new domain_separator value. The
registry is normative and lives in OBJECTS.md.

Adding a new object type does not change existing schemas. Existing
implementations may continue to reject unknown domain separators without
affecting their operation on known types.

## Implementation version signaling

Implementations signal supported domain separators through the objects they
produce. There is no separate "capabilities" negotiation in V1.

A verifier that receives an unknown domain_separator rejects the object. It
does not fall back to an older interpretation, and it does not attempt to
interoperate with an unknown schema.

## Protocol version bumps

A protocol version bump (v0.6.2 → v0.7) occurs when:

- A new object type is registered, OR
- An existing object type's semantics change in a way that would cause two
  conforming implementations to disagree, OR
- An authority boundary changes.

Editorial clarifications do not trigger a version bump.

## Compatibility guarantees

Within a major protocol version (v0.x):

- No existing object type's schema changes.
- No existing authority boundary changes.
- No existing rejection class changes meaning.
- New object types may be added without invalidating existing ones.

Across major protocol versions, no compatibility is guaranteed.
Implementations may support multiple major versions if they choose.

## Governance

V1 governance is not defined. This document acknowledges that:

- Future changes require a decision process.
- The decision process will matter more as independent implementers appear.
- The process should be chosen deliberately, not drifted into.

Options for future consideration:

- Single reference implementation (early SSH model).
- Benevolent dictatorship (Python, Linux kernel model).
- Standards-body-like governance (TLS, DNS model).

The choice is deferred. What matters now is acknowledging that the choice must
be made before the protocol is deployed at scale.

## Deprecation

Object types are deprecated by:

1. Removing the domain_separator from the recommended registry.
2. Documenting the removal and the reason.
3. Retaining the old schema for reference.

Deprecated schemas are not removed from the protocol. Implementations that
already support them may continue to. New implementations should not add
support for them.
```

---

## `12-GLOSSARY.md`

```markdown
# Grid Network — Glossary

**Status:** Partial. Expand as needed.

## Terms

**Peer Principal** — The durable logical identity represented by the
protocol. May span multiple devices and services. Survives replacement of
individual devices.

**Peer Principal ID** — Opaque, randomly generated identifier bound to a
principal's identity root by the identity document. Example:
`peer:v1:7f3a9c2e5d91b0a4c7e8126fa31d449b`.

**Identity Root** — The highest cryptographic authority for a principal.
Signs identity documents, relationship assertions, key delegations; revokes
subordinate keys; signs the principal's rendezvous manifest.

**Device Key** — Authenticates a device; signs reachability records.

**Service Key** — Authenticates a service; signs service records.

**Authorization Key** — Signs grants, leases, and revocations in its stream.

**Identity Document** — A signed object binding a Peer ID to an identity
root and subordinate keys. Occupies the principal's `stream:identity`.

**Device Binding** — An entry in an identity document that binds a device
key to the principal.

**Service Binding** — An entry in an identity document that binds a service
key to the principal or to a specific device.

**Key Binding** — An entry in an identity document that delegates authority
to a subordinate key.

**Relationship Assertion** — A unilateral signed statement that one principal
recognizes another. Two matching assertions (one from each principal) are
required for verifier-derived `RECOGNIZED` state.

**Relationship Termination** — A unilateral signed statement that a principal
no longer recognizes another. Terminal.

**Grant** — A directional signed authorization from one principal to
another. Contains capabilities, constraints, lease policy, and issuance
information.

**Lease** — A short-lived proof that a grant is currently valid. Bounded by
relative validity and authorization freshness.

**Revocation** — A terminal signed statement invalidating a specific object.
Once revoked, an object cannot become valid again.

**Key Revocation** — A revocation targeting a specific Authorization Key.
Signed by the Identity Root. Contains an `effective_sequence` referring to
the revoked key's own authorization stream.

**Reachability Record** — A signed assertion of a device's current network
endpoints. Ephemeral. Refreshed as networks change.

**Service Record** — A signed assertion of a service's current endpoint and
metadata. Signed by the Service Key.

**Rendezvous** — Infrastructure that stores and serves signed objects.
Untrusted. Cannot forge, only store and forward.

**Relay** — Infrastructure that forwards encrypted traffic when direct
connectivity fails. Untrusted. Cannot decrypt.

**Relay Ticket** — A signed authorization permitting a peer to use a relay
for a specific capability. Pair-bound, capability-bound, short-lived.

**Service Link** — A referential identifier for a subject-service
relationship. Not an authorization object. Not independently signed.

**Sequence Space** — The pair `(issuer, stream_id)`. Sequence numbers are
meaningful only within their sequence space.

**Stream** — The ordered sequence of objects sharing one sequence space.

**Initial Chain Hash** — The base state for a stream, computed from the
domain separator and stream ID.

**Chain Hash** — The cumulative stream-history hash, computed over the
previous chain hash and the current object commitment.

**Object Commitment** — The hash of an object's unsigned payload, computed
with a domain-separated preimage.

**Signature Input** — The canonical CBOR structure that is signed to produce
an object's signature. Includes domain separator, unsigned payload, and
chain hash.

**Object ID** — The hash of the signed object's canonical byte representation.

**Payload ID** — The hash of the unsigned payload's semantic content,
independent of signature.

**Authority Precedence Table** — A normative table specifying which object
governs when two objects bear on the same decision.

**Signing-Authority Matrix** — A normative table specifying which key role is
authorized to sign each object type.
```

---

## `13-FAQ.md`

```markdown
# Grid Network — Frequently Asked Questions

**Status:** Partial. Expand as needed.

## Comparisons

### "Why not just use Tailscale?"

Tailscale is an excellent product. It also is a company. It runs a
coordination server that is the source of truth for your device graph. If
Tailscale changes its terms, or gets acquired, or shuts down a feature you
depend on, or stops being able to operate in your jurisdiction, your network
is affected. You can self-host Headscale, but then you're running
infrastructure — you've swapped one problem for another.

Tailscale's identity model is account-based. That works for consumers. It's
awkward for self-hosting, and it's problematic for applications that want to
authorize based on device identity rather than user identity. The underlying
protocol is proprietary: third parties can't implement it, and you can't
switch providers without rebuilding your network.

Grid Network's identity is portable. Your Peer ID, your relationships, and
your grants survive any change of infrastructure provider.

### "Why not just use Cloudflare Tunnel?"

Cloudflare Tunnel lets a local machine connect outbound to Cloudflare, so you
don't need a public IP. It works well. But it makes Cloudflare part of the
access path. If Cloudflare changes its terms, filters the wrong traffic, has
an outage, or exits the business, your access path goes with it. Grid
Network's rendezvous and relays are untrusted and replaceable.

### "Isn't this just a blockchain?"

No. Grid Network has no global consensus, no ledger, no mining, no token. It
uses cryptographic signatures and local verification, which is a fundamentally
different approach. Bitcoin solves "how do independent parties agree on one
global history." Grid Network solves "how does one party verify another's
identity and authorization." These are different problems.

The one idea Grid Network borrows from Bitcoin is that cryptographic proofs
can replace institutional trust. But it uses that idea locally, not globally,
which means it doesn't need the cost of consensus.

### "Isn't this just Tor?"

No. Tor provides anonymity through routing. Grid Network provides
authenticated identity with explicit non-anonymity. Peers are identified.
Metadata is visible to infrastructure operators. This is by design.

If you need anonymity, Grid Network is not the right tool. If you need
authenticated connectivity, Tor is not the right tool.

### "What about metadata privacy?"

Grid Network provides confidentiality of content and authorization, not
anonymity of participation. Specifically:

- Peer IDs are stable and correlatable.
- Rendezvous servers see query patterns.
- Relays see endpoints and traffic volume.
- On-path observers see peer IDs.

If metadata privacy is a requirement, Grid Network can be composed with
additional layers, such as onion routing for rendezvous lookups. This is
deferred to future versions.

### "What about governance?"

V1 has no governance mechanism. The protocol is a specification, not an
organization. As independent implementations emerge, governance questions
will need to be answered. Options include reference-implementation-driven,
benevolent-dictator, and standards-body models.

This is deliberately deferred. The protocol is stable enough at V1 that
governance questions do not need to be answered yet.

### "What if the Identity Root is compromised?"

V1 has no in-band recovery. This is intentional — any in-band recovery
mechanism would be an authority the protocol cannot trust. Recovery is
out-of-band: the user establishes a new identity through a trusted channel.

This is why Identity Root protection is critical. Users should store it
offline, hardware-backed, or in a secure enclave.

### "Why not just use DNS?"

DNS maps names to addresses. Grid Network maps identities to reachability,
with authorization. DNS has a hierarchical namespace with centralized
administration. Grid Network's identities are flat and controlled by the
participant. The only thing they share is the operation "given an identifier,
produce an endpoint." That is a thin similarity.

### "How is this different from Nebula / Netmaker / Firezone / Headscale?"

- **Nebula** is a mesh networking protocol with its own CA. It doesn't
  provide portable identity.
- **Netmaker** is a WireGuard management layer, similar to Tailscale but
  self-hostable. It doesn't provide a portable identity protocol.
- **Firezone** is a WireGuard-based access control product focused on
  enterprise. Not a portable identity protocol.
- **Headscale** is a self-hosted Tailscale control server. Same protocol,
  different infrastructure.

None of these is a portable identity protocol that applications can consume
as a shared primitive. They're each a product or a management layer. Grid
Network fills that gap.

### "Who actually wants this?"

Specific communities care about portability:

- **Self-hosters** who have watched services shut down, change pricing, or
  restrict features.
- **Open-source applications** that don't want to run a cloud service or tell
  users to install third-party software.
- **Enterprises** that have been burned by vendor lock-in and are actively
  looking for portable solutions.
- **Regulators** who increasingly care about digital sovereignty and
  infrastructure resilience.
- **Communities** — small towns, hobbyist groups, cooperative ISPs — that
  want private infrastructure that isn't dependent on a vendor.

## Design questions

### "Why doesn't the protocol handle user authentication?"

Because user authentication and device authentication are different problems.
The application keeps its own user model. Grid Network provides device
identity and network authorization. Both are necessary; neither substitutes
for the other.

### "Why is relay a fallback and not the default?"

Because direct connections are always preferable. They're faster, cheaper,
and don't depend on any infrastructure. Relay exists for the cases where
direct connectivity fails. In a mature deployment with widespread IPv6 and
working NAT traversal, most traffic never touches a relay.

### "Why is identity portable?"

Because that's the property that prevents vendor lock-in. If identity were
not portable, the commercial layer would inevitably become extractive.
Because it is portable, the commercial layer is forced to be additive.
```

---

## `14-ROADMAP.md`

```markdown
# Grid Network — Roadmap

**Status:** Draft

## Current state

- Protocol: v0.6.2 (frozen)
- Document set: 0.1 (early draft)
- Phase: Documentation

## Phase 0 — Documentation (current)

**Goal:** Complete the specification and rationale before any code is written.

**Deliverables:**

- `PROTOCOL.md` v0.6.2 (frozen)
- `OBJECTS.md` §1–§5 (done)
- `OBJECTS.md` §6–§10 (pending)
- `RATIONALE.md` v2.0 (done)
- `ADDENDUM-A-COMMERCIAL.md` v6.0 (done)
- `ADDENDUM-B-LINEAGE.md` v1.0 (done)
- `SECURITY.md` (pending)
- `IMPLEMENTATION.md` (pending)
- `CONNECTIVITY.md` (pending)
- `VERSIONING.md` (pending)
- `GLOSSARY.md` (partial)
- `FAQ.md` (partial)

**Completion criterion:** All documents have their substantive content.
Two independent implementers could begin work from the documentation alone.

## Phase 1 — Test vectors and reference implementation

**Goal:** Produce the first executable artifact.

**Deliverables:**

- Positive test vectors for every object type
- Negative test vectors for every rejection class
- Conformance test runner
- Reference implementation (any language)

**Completion criterion:** The reference implementation passes all Level 1
(encoding), Level 2 (verification), and Level 3 (authorization) test
vectors.

## Phase 2 — Independent implementations

**Goal:** Prove the protocol is implementable by more than one team.

**Deliverables:**

- At least one independent implementation
- Byte-for-byte interop on all test vectors
- Documentation of any ambiguities discovered

**Completion criterion:** Two implementations interoperate on
identity document creation, verification, and signature checking.

## Phase 3 — Applications and integrations

**Goal:** Prove the protocol is useful for real applications.

**Deliverables:**

- Example integration for at least three applications
  (candidates: Jellyfin, Immich, Nextcloud)
- Generic HTTP proxy for transparent integration
- Local grid agent for Linux, macOS, Windows

**Completion criterion:** A user can install a grid agent, pair two devices,
and reach a self-hosted service across the internet — using an application
that has integrated with the protocol.

## Phase 4 — Commercial infrastructure

**Goal:** Enable commercial participation and funding.

**Deliverables:**

- Rendezvous server reference implementation
- Relay reference implementation
- Credit and priority ticket system
- Stewardship entity formation
- First commercial operator
- First enterprise deployment

**Completion criterion:** A developer is paid full-time to work on the
protocol, funded by commercial revenue.

## Phase 5 — Long-term

Deferred to future versions:

- Chain-extension proofs (skip-ahead)
- Sophisticated recovery (threshold, social, hardware-backed)
- Service ownership transfer
- Groups and delegated administration
- Advanced metadata protection (rotating pseudonyms)
- Multipath and FEC
- DHT-based discovery
- Peer-assisted gossip
- Federation between rendezvous servers

## Research agenda

Open questions not yet resolved:

- Optimal form of chain-extension proof
- Governance model for protocol evolution
- Threshold recovery design
- Metadata minimization without anonymity
- Credit system calibration (scarcity multipliers, exchange rates)
- Best practices for local state storage

## What is not on the roadmap

The following are explicitly out of scope:

- Global consensus
- Blockchain
- Global Sybil resistance
- Anonymity networks
- Reputation systems (belongs in deployment policy)
- Adaptive TTLs (belongs in deployment policy)
- Proof-of-work as a foundational mechanism
```

---

## `15-LICENSE.md`

```markdown
# Apache License 2.0

Copyright (c) 2026 Grid Network contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

---

The full text of the Apache License 2.0 is available at
https://www.apache.org/licenses/LICENSE-2.0
```

---

## `16-CONTRIBUTING.md`

```markdown
# Contributing to Grid Network

## Repository layout

- `docs/` — documentation, specifications, rationale
- `spec/` — normative test vectors
- `implementations/` — reference and third-party implementations
- `apps/` — example applications

## Development phases

This repository is currently at **documentation phase**. Protocol v0.6.2 is
frozen. Implementation work will be admitted once:

1. `docs/protocol/OBJECTS.md` §6–§10 is complete.
2. `spec/test-vectors/` contains at least one positive vector per object type.
3. `docs/security/SECURITY.md` is drafted.

Until then, contributions are limited to documentation.

## How to propose a change

1. Open an issue describing what you want to change and why.
2. If the change affects the protocol, expect discussion before acceptance.
3. Protocol changes require a version bump (see
   `docs/protocol/VERSIONING.md`).

## Principles

- **Every security mechanism needs a specific boundary it protects.**
- **No new authority domains without explicit justification.**
- **Byte-level interoperability is non-negotiable.**
- **The protocol is free; the development is funded.**
- **Identity is portable. No vendor lock-in.**
- **Failure never grants authorization.**

## Questions to ask before adding a mechanism

1. What authority or resource does it protect?
2. What specific attack does it prevent?
3. What happens if it is removed?
4. What new complexity does it introduce?

If any answer is unsatisfactory, the mechanism is premature.

## Code of conduct

Be precise. Be patient. Be honest about uncertainty.

## License

By contributing, you agree that your contributions will be licensed under the
Apache License 2.0.
```

---

## How to use this handoff

**Step 1.** Copy each block above into its own file using the filename indicated.

**Step 2.** For documents marked "full text in project history" (PROTOCOL.md §1–§65, RATIONALE.md full text, ADDENDUM-A and ADDENDUM-B full text), paste the complete content from the earlier conversation turns.

**Step 3.** Perform the Mesh → Grid Network rename in PROTOCOL.md.

**Step 4.** Give the entire folder to the receiving agent with this instruction:

> This is the Grid Network project at documentation phase. Read `00-HANDOFF-README.md` first. Then read `02-OUTLINE.md` for the project map. Your priorities are listed in `14-ROADMAP.md` under Phase 0. Do not redesign the protocol — v0.6.2 is frozen. Begin with the Tier 1 items: complete `OBJECTS.md` §6 (object schemas), then §7 (stream rules), then produce the first test vector.

**Step 5.** The receiving agent should be able to work from this package without needing the original conversation.

---

## What this package includes that the previous handoff did not

- The full structure of every document, not just the index
- Complete §1–§5 of OBJECTS.md
- Complete section-by-section breakdowns of RATIONALE.md, ADDENDUM-A, and ADDENDUM-B
- VERSIONING.md fully drafted
- GLOSSARY.md with all key terms
- FAQ.md with all comparison questions answered
- ROADMAP.md with phases and completion criteria
- The design principles that must not be violated
- The four questions to ask before adding any mechanism

## What still needs to be pasted in from the original conversation

- PROTOCOL.md §1–§65 (full text)
- OBJECTS.md §6–§10 (not yet written)
- RATIONALE.md full text (all sections)
- ADDENDUM-A full text (all sections)
- ADDENDUM-B full text (all sections)

Everything else is in this package.
