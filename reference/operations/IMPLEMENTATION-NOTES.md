# Grid Network — Implementation Notes

**Revision:** 2.6
**Protocol version:** v0.6.3

**Repository path:** `operations/IMPLEMENTATION-NOTES.md`

This document is non-normative implementation guidance. It restates
constraints that the specification already contains and that affect how
an implementation is built. It adds no requirement, parameter, schema,
object field, or protocol behavior, and it does not select a language,
library, or platform. Where this document and the specification differ,
the specification governs.

Each statement below cites the section it relies on. A statement that
describes a requirement does not restate it; the cited section does.

---

## 1. Encoding and canonicalization

- The specification defines one valid byte encoding for each protocol
  value: CBOR with the deterministic constraints of `OBJECTS.md §2`.
  Where RFC 8949 permits alternatives, only the form in that section is
  valid (`OBJECTS.md §2`).
- Negative integers, floating-point values, indefinite-length items,
  duplicate map keys, and duplicate set elements are excluded
  (`OBJECTS.md §2.1`, `OBJECTS.md §2.10`, `OBJECTS.md §2.11`,
  `OBJECTS.md §2.12`).
- Map keys are ordered by bytewise lexicographic comparison of their
  canonical CBOR encodings, and a map whose keys are out of order is
  malformed (`OBJECTS.md §2.7`). A set is a definite-length array with
  unique, sorted elements (`OBJECTS.md §2.8`). The endpoints of a
  reachability record are sorted by canonical CBOR encoding
  (`PROTOCOL.md §24`).
- An optional field that is absent is omitted from the map and is not
  encoded as null (`OBJECTS.md §2.9`).
- Time values are integer seconds unless a schema states integer
  milliseconds, and a schema states its unit (`OBJECTS.md §2.10`).
- Bytes that are not canonical are rejected with the class
  `MALFORMED_ENCODING`, and malformed CBOR is rejected before semantic
  processing (`OBJECTS.md §8`, `PROTOCOL.md §43`).
- The `object_id` is computed over the exact canonical bytes of the
  signed object, and the cited section prohibits re-encoding the signed
  object as a CBOR value before hashing (`OBJECTS.md §3.10`).
- Every derived value is reconstructible from the canonical unsigned
  payload, the applicable stream state, and the protocol rules. The
  specification excludes dependence on non-canonical source
  representations, parser-preserved formatting, map insertion order,
  and locally generated serialization choices (`OBJECTS.md §3.13`).
- The distinction between CBOR values and byte strings is normative in
  every construction, and a byte-string operand is encoded as a CBOR
  byte string inside a surrounding structure (`OBJECTS.md §3.2`,
  `OBJECTS.md §3.13`).

---

## 2. Domain separation and chain-hash construction

- Each cryptographic construction has its own domain tag, each object
  schema has a registered domain separator, and unknown separators are
  rejected (`OBJECTS.md §3.13`, `OBJECTS.md §5`).
- The constructions are the object commitment, the initial chain hash,
  the chain hash, the payload ID, the object ID, and the signature
  input (`OBJECTS.md §3.4`, `OBJECTS.md §3.5`, `OBJECTS.md §3.6`,
  `OBJECTS.md §3.8`, `OBJECTS.md §3.9`, `OBJECTS.md §3.10`,
  `OBJECTS.md §3.12`). They are summarized in `PROTOCOL.md §41`.
- The previous hash and the previous chain hash are different values.
  The first is an object field and the second is a computed input
  (`OBJECTS.md §3.7`).
- The chain hash at sequence N depends on the chain hash at sequence
  N−1 and the object commitment at sequence N. The first object in a
  stream has sequence 1, and the value 0 is reserved
  (`OBJECTS.md §3.8`, `OBJECTS.md §3.13`).
- The signature input covers the unsigned payload and the chain hash,
  and it does not cover `payload_id` (`OBJECTS.md §3.12`).
- The chain hash commits to the stream history presented to the
  verifier and does not by itself reveal a fork. A fork is detected when
  two objects in one stream have the same sequence and different chain
  hashes (`OBJECTS.md §3.8`, `OBJECTS.md §9.3`).
- A sequence number has meaning only within one issuer and stream
  sequence space, and neither sequence numbers nor chain hashes are
  compared or merged across streams (`PROTOCOL.md §36`,
  `OBJECTS.md §9.5`).
- A verifier processes a candidate object in ten ordered steps, each
  with a named rejection class (`OBJECTS.md §8`).

---

## 3. Test vectors and interoperability claims

- The specification states that conformance is defined by test vectors,
  and that conformance is not an interoperability certification
  (`CONFORMANCE.md §1`, `PROTOCOL.md §44`).
- A passing implementation produces byte-exact output for every
  positive vector and rejects every negative vector with the specified
  rejection class (`CONFORMANCE.md §7`).
- Required coverage is at least one positive vector and three negative
  vectors for every object type (`CONFORMANCE.md §3.3`).
- A vector carries its own parameters and does not rely on a default
  from `PARAMETERS.md` (`CONFORMANCE.md §3.4`).
- No test vectors have been published (`ROADMAP.md §1`). The vector
  format, the production sequence, and the repository layout are
  defined in `CONFORMANCE.md §3`, `CONFORMANCE.md §5`, and
  `CONFORMANCE.md §6`.
- Ten object types have stub schemas, and the schemas, the vectors, and
  the conformance suite are listed as not yet specified
  (`OBJECTS.md §7.9`, `OBJECTS.md §10`, `ROADMAP.md §2`).
- The completion criterion for an independent implementation is that
  two implementations produce identical bytes for identical inputs and
  disagree on nothing in the conformance suite (`ROADMAP.md §2`).

---

## 4. Verifier state and persistence

- A verifier keeps local state for known peers, relationships, grants,
  leases, revocations, reachability records, stream caches, chain-hash
  caches, observation records, and an observation clock. The
  representation of the derived state structures is
  implementation-defined (`PROTOCOL.md §34`).
- The specification requires observation records to be persisted, both
  in the verifier state rules and in the freshness rules for relative
  lease validity (`PROTOCOL.md §34`, `PROTOCOL.md §10`,
  `PROTOCOL.md §43`).
- State corruption requires re-establishing trust from scratch. The
  specification names atomic writes and checksums as the means of
  reducing the risk (`PROTOCOL.md §34`, `DEPLOYMENT.md §7.6`).
- The cited section prohibits changing accepted stream state during the
  verification steps, and commits a verified object to local state as a
  single atomic operation (`OBJECTS.md §8.1`).
- If an observation record is lost, or the system boot identifier has
  changed, elapsed time is treated as the maximum and the verifier fails
  closed (`PROTOCOL.md §10`).
- If the same lease is observed again, the original observation start
  is preserved (`PROTOCOL.md §10`).
- A verifier without durable storage is excluded from relative lease
  validity (`PROTOCOL.md §10`).
- A revocation received before its target is cached and applied when
  the target arrives (`PROTOCOL.md §14`, `PROTOCOL.md §31`).

---

## 5. Clocks and suspend or resume

- Every rule that involves time names one of three clock classes:
  issuer-asserted, verifier-monotonic, or verifier-wall-clock
  (`PROTOCOL.md §32`).
- Verifier-monotonic time is elapsed time measured on a clock that
  advances during system suspend. The implementation requirements list
  a monotonic clock that advances during suspend, or failing closed
  (`PROTOCOL.md §32`, `PROTOCOL.md §10`, `PROTOCOL.md §43`).
- Wall-clock time does not extend authorization validity, and a
  persisted wall-clock high-water mark is permitted as a lower bound on
  elapsed time (`PROTOCOL.md §32`, `PROTOCOL.md §10`,
  `PROTOCOL.md §43`).
- The specification names the property required of the clock and does
  not name a platform facility that provides it (`PROTOCOL.md §32`,
  `PROTOCOL.md §43`).
- A lease whose `issued_at` is older than `MAX_LEASE_AGE`, a
  configurable bound, is rejected (`PROTOCOL.md §10`).
- Relative validity survives clock skew up to the lease duration, and
  absolute validity depends on time synchronization. The deployment
  guidance keeps the clock within `MAX_CLOCK_SKEW` of a reliable source
  (`PROTOCOL.md §32`, `PROTOCOL.md §39`, `DEPLOYMENT.md §7.5`).

---

## 6. Transport, NAT traversal, relay fallback, and path selection

- The protocol is transport-independent. It names WireGuard, QUIC, and
  TLS as transports chosen by the implementation (`PROTOCOL.md §26`).
- The Grid layer provides mutual authentication, and the transport
  provides confidentiality, integrity, and forward secrecy
  (`PROTOCOL.md §26`).
- The specification lists, as a conformance condition, support for at
  least one transport that survives networks that block UDP. TLS over
  TCP port 443 is the recommended default
  (`PROTOCOL.md §26`, `DEPLOYMENT.md §3.6`).
- The connection order is local discovery, direct connection, NAT
  traversal with candidate exchange and hole punching, and relay. The
  same section permits deviation when an implementation has information
  that changes the tradeoffs (`DEPLOYMENT.md §3.1`).
- The NAT traversal wire specification is drafted and is not normative,
  and the rendezvous wire protocol is not started (`ROADMAP.md §4`).
- The path selection algorithm is implementation-defined. The stated
  properties are that failure does not become denial, alternatives are
  tried, there is no silent downgrade to a weaker transport without
  explicit configuration, and several endpoints are supported
  (`DEPLOYMENT.md §4`).
- A path failure is an availability failure and does not change
  authorization state (`DEPLOYMENT.md §4`, `PROTOCOL.md §39`).
- A relay's rejection of a ticket is an availability failure, and a
  verifier treats it as a signal to try an alternative relay
  (`PROTOCOL.md §25`).
- A reachability record lists endpoints with a protocol, an address, a
  priority, and a transport of udp, tcp, or quic. A verifier treats
  every endpoint as untrusted and is not required to try endpoints in
  priority order (`PROTOCOL.md §24`).
- Multipath connectivity is `planned` and is not in protocol v0.6.3
  (`PROTOCOL.md §46`).

---

## 7. Platform differences

- The Identity Root is normally kept offline or hardware-protected and
  does not take part in routine network sessions. Where the root stays
  online, hardware-backed keys are recommended (`PROTOCOL.md §5`,
  `DEPLOYMENT.md §7.1`).
- Support for hardware-backed keys appears in the specification's list
  of recommended implementation items, and hardware-backed root keys are
  `unscheduled` (`PROTOCOL.md §43`, `PROTOCOL.md §46`).
- The specification defines no key-storage interface and does not state
  which platforms provide hardware-backed keys (`PROTOCOL.md §43`,
  `PROTOCOL.md §46`).
- A device key is bound to one device. When a device is lost, its key is
  revoked and the device is removed from the identity document
  (`DEPLOYMENT.md §7.3`).
- A backup is useful only if it chains to the current identity state,
  and a backup stored with the key does not protect against compromise
  (`DEPLOYMENT.md §7.4`).
- Pairing is human-mediated. One side displays a code or QR payload,
  the other side receives it out of band, and the receiving side
  confirms the attempt (`PROTOCOL.md §21.1`, `PROTOCOL.md §21.3`,
  `PROTOCOL.md §21.5`).
- Unattended enrollment for headless devices uses out-of-band
  verification of a pinned fingerprint or a one-time token, and it
  weakens the confirmation property of interactive pairing
  (`PROTOCOL.md §20`, `PROTOCOL.md §21.4`).
- The pairing section carries the `under-review` marker, and the
  versioning rules state that implementations are not to build against
  an `under-review` section yet (`PROTOCOL.md §21`, `PROTOCOL.md §45`;
  `spec/VERSIONING.md`, Stability markers).
- The selected PAKE is SPAKE2. The specification states no fallback PAKE
  and does not state which platforms provide a SPAKE2 implementation. It
  defines out-of-band verification as a second pairing mechanism for
  unattended and enterprise cases (`PROTOCOL.md §20`).
- The specification prohibits implementing cryptographic primitives
  directly (`PROTOCOL.md §43`).
- The mobile milestone lists iOS and Android agents and background
  execution, and the specification measures elapsed time on a clock that
  advances during system suspend (`ROADMAP.md §2`, `PROTOCOL.md §32`).
