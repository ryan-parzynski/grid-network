# Grid Network — Detailed Reference Addendum

**Status:** Companion to the Master Archive
**Purpose:** Provide the specific details, worked examples, and elaboration that the Master Archive summarizes. Where this addendum and the Master Archive differ, the Master Archive governs.

---

## How to use this addendum

The Master Archive is the map. This addendum is the reference manual.

- **Shape, invariants, authority model, failure semantics** → Master Archive
- **Byte-level constructions, worked crypto examples, threat enumeration, capacity math** → this addendum
- **The authoritative source for a specific byte sequence** → OBJECTS.md, referenced from the Master Archive
- **The authoritative source for a security property** → Part 9 of the Master Archive

Where this addendum and the Master Archive differ on a normative point, the Master Archive governs. Differences are called out inline.

---

# Part A — Cryptographic Constructions in Full

## A.1 The four representations of an object

An object in Grid Network passes through four distinct representations before it becomes a wire-format artifact. Confusing them is the single most common source of implementation bugs, so they are named explicitly:

```
1. unsigned_payload
       │
       │ (canonical CBOR, with tag string)
       ▼
2. commitment_preimage
       │
       │ (SHA-256)
       ▼
3. object_commitment
       │
       │ (combined with previous_chain_hash)
       ▼
4. chain_hash
       │
       │ (combined with tag, unsigned_payload, chain_hash)
       ▼
5. signature_input → signature
       │
       │ (added to unsigned_payload along with chain_hash)
       ▼
6. signed_object_bytes
```

Every step is deterministic. Given any unsigned_payload and the stream state, all downstream values are fully determined.

## A.2 Commitment preimage and object commitment

```
commitment_preimage =
    canonical_cbor([
        "grid/commitment/v1",
        domain_separator,
        unsigned_payload
    ])

object_commitment =
    SHA-256(commitment_preimage)
```

The tag string `"grid/commitment/v1"` is part of the preimage. This is what makes the commitment domain-separated from every other hash the protocol computes. Two objects with identical content but different domain separators produce different commitments.

`object_commitment` is the value that appears in the *next* object's `previous_hash` field.

## A.3 Chain base and chain hash

The chain base is bound to the specific stream, not just to the object type:

```
initial_chain_hash =
    SHA-256(canonical_cbor([
        "grid/chain-base/v1",
        domain_separator,
        stream_id
    ]))
```

This ensures that two distinct streams of the same object type cannot share an initial chain hash by accident.

The chain hash for the first object uses the chain base as the predecessor:

```
previous_chain_hash(1) = initial_chain_hash
previous_chain_hash(N) = chain_hash(N-1)          for N > 1

chain_hash(N) =
    SHA-256(canonical_cbor([
        "grid/chain/v1",
        previous_chain_hash(N),
        object_commitment(N)
    ]))
```

The chain hash commits to the entire history of the stream, not just to the previous object. This is what enables fork detection even when a verifier has seen only one branch.

**Fork detection walkthrough.** Suppose the issuer produces two conflicting objects at sequence 3:

```
Branch A:
  seq 1 (commitment: c1, chain: h1)
  seq 2 (commitment: c2, chain: h2 = F(h1, c2))
  seq 3 (commitment: c3, chain: h3 = F(h2, c3))

Branch B:
  seq 1 (commitment: c1, chain: h1)
  seq 2 (commitment: c2, chain: h2 = F(h1, c2))
  seq 3 (commitment: c3', chain: h3' = F(h2, c3'))
```

A verifier that has accepted sequence 2 has `chain_hash = h2`. When it receives the sequence-3 object from branch A, it recomputes `chain_hash = F(h2, c3)` and compares to the object's stated `chain_hash`. If they match, the object extends the accepted chain. If the verifier instead receives the object from branch B, it recomputes `F(h2, c3')` and gets a different value — the object's stated `chain_hash` (h3') will not match what the verifier computes. The verifier knows a fork has occurred even without having seen branch A's sequence-3 object.

With a linear chain (previous_hash only), the verifier would need to see both branches to detect the fork.

## A.4 Payload ID and object ID

Two identifiers serve different purposes.

```
payload_id =
    SHA-256(canonical_cbor([
        "grid/payload-id/v1",
        unsigned_payload
    ]))

object_id =
    SHA-256(canonical_cbor([
        "grid/object-id/v1",
        canonical_signed_object_bytes
    ]))
```

`payload_id` identifies the semantic content. It is computed before the signature and is one of the inputs to the signature. Two objects that mean the same thing have the same payload_id.

`object_id` identifies the specific signed artifact. It is computed after the signature. Two objects with identical payloads but different signatures (for example, signed by different keys) have different object_ids.

**Why the distinction matters.** A grant revocation must reference *the specific signed grant* it revokes, not "a grant that means roughly the same thing." So revocations carry `object_id`. But if a verifier wants to determine whether two revocation records are about the same underlying grant, it compares payload_ids. Having both lets the protocol express both relationships.

## A.5 Signature input and signature

```
signature_input(N) =
    canonical_cbor([
        "grid/signature/v1",
        domain_separator,
        unsigned_payload(N),
        chain_hash(N)
    ])

signature(N) =
    Ed25519_sign(signing_private_key, signature_input(N))
```

The signature covers the *unsigned payload directly*, not its hash. This is deliberate. If the signature covered the payload hash, an attacker who could produce a hash collision could substitute a different payload for the same signature. Signing the payload itself (within a canonical CBOR framing) removes that attack.

The `chain_hash` is included in the signature input, so the signature commits to the entire stream history as well as to the current object's content.

**Non-circularity.** The signature is not part of its own input. The `chain_hash` is derived from the unsigned payload and the stream state; the signature is derived from the `chain_hash` and the unsigned payload. There is no cycle.

---

# Part B — Verification Procedure in Full

## B.1 The ten steps

A verifier processes a candidate object in this order. Each step has a specific rejection class.

**Step 1 — Parse.** Decode the bytes as CBOR according to the canonical profile. Reject as `MALFORMED_ENCODING` if the bytes are not valid CBOR or violate any canonical-form rule.

**Step 2 — Envelope validation.** Verify that the object contains `domain_separator`, `sequence`, `previous_hash` (omitted at sequence 1), `chain_hash`, and `signature` as text/byte strings of the correct types. Reject as `MALFORMED_ENVELOPE` if any required field is missing, mistyped, or if any unknown top-level field is present.

**Step 3 — Domain separator validation.** Verify that the `domain_separator` is in the registered set. Reject as `UNKNOWN_SCHEMA` if the value is not registered.

**Step 4 — Schema validation.** Validate the object's schema-specific fields according to the object type's schema definition. Reject as `MALFORMED_SCHEMA` if any field fails validation.

**Step 5 — Sequence validation.** Verify that `sequence >= 1`. Verify that `previous_hash` is present if and only if `sequence > 1`. Reject as `INVALID_SEQUENCE` or `INVALID_PREVIOUS_HASH` respectively.

**Step 6 — Chain validation.** Compute `object_commitment` from the unsigned payload. If `sequence > 1`, retrieve the accepted object at sequence `N-1` in the same `(issuer, stream_id)` sequence space and compute its `object_commitment`. Verify that the candidate's `previous_hash` equals that commitment. Compute the expected `chain_hash` using the accepted predecessor's chain hash and the candidate's object commitment. Verify that the candidate's `chain_hash` matches. Reject as `CHAIN_MISMATCH` on any failure.

**Step 7 — Signature input construction.** Compute `signature_input` from the unsigned payload and the chain hash.

**Step 8 — Signature verification.** Verify the Ed25519 signature over `signature_input` against the public key authorized for this object type and stream. For dual-signature objects, verify both signatures over the same input. Reject as `INVALID_SIGNATURE` on any failure.

**Step 9 — Authority validation.** Verify that the signing key's role is authorized for the object type. Verify that the signing key is currently authorized for the stream: not revoked, not superseded at the object's sequence position, and covered by the object's delegation chain. Reject as `UNAUTHORIZED_SIGNER` on any failure.

**Step 10 — Semantic validation.** Apply the object's semantic rules (identity document binding, grant scope, lease policy, and so on).

## B.2 Atomicity

Verification must be pure with respect to accepted state. No step in the procedure may advance or mutate accepted stream state. Only after all ten steps pass is the object committed to local state as a single atomic operation.

If processing fails at any step, the verifier retains its previous accepted state. There is no partial application.

## B.3 Rejection classes

| Class | Trigger |
|-------|---------|
| `MALFORMED_ENCODING` | Not valid canonical CBOR |
| `MALFORMED_ENVELOPE` | Envelope field missing, mistyped, or unknown field present |
| `UNKNOWN_SCHEMA` | `domain_separator` not in registry |
| `MALFORMED_SCHEMA` | Schema-specific field fails validation |
| `INVALID_SEQUENCE` | `sequence` is 0 or otherwise invalid |
| `INVALID_PREVIOUS_HASH` | Presence of `previous_hash` does not match `sequence` |
| `CHAIN_MISMATCH` | `previous_hash` or `chain_hash` does not match stream state |
| `INVALID_SIGNATURE` | Signature does not verify |
| `UNAUTHORIZED_SIGNER` | Signing key is not authorized |
| `REVOKED` | Signing key or target object is revoked |
| `EXPIRED` | Validity interval has elapsed |
| `FORK_DETECTED` | Stream is in `FORKED` state |

Individual schemas may define additional rejection classes for schema-specific failures.

---

# Part C — Security Model in Full

## C.1 Threat enumeration

Each threat below names the attacker's goal, the mechanism they would use, the defense the protocol provides, and the outcome.

**T1 — Identity forgery.** Attacker attempts to claim another principal's Peer ID. Mechanism: signs an identity document with their own key. Defense: identity documents must be signed by the declared identity root. Outcome: signature verification fails; object rejected as `INVALID_SIGNATURE`.

**T2 — Authorization forgery.** Attacker attempts to create a grant authorizing themselves without the issuer's consent. Mechanism: signs a grant with their own key. Defense: grants must be signed by an authorization key that the verifier trusts for that issuer. Outcome: signature verification fails or authority validation fails.

**T3 — Endpoint poisoning.** Attacker with access to a rendezvous server serves a stale or false endpoint. Mechanism: returns a cached or fabricated reachability record. Defense: reachability records are signed by the device key; verifier validates signature and tries candidates in order. Outcome: connection delay; the attacker cannot redirect to a different peer because the endpoint's identity is bound to the device key, not to the address.

**T4 — Relay observation.** Attacker operates a relay and attempts to read forwarded traffic. Mechanism: inspects packets. Defense: transport encryption (WireGuard, QUIC, or TLS). Outcome: relay sees only ciphertext plus timing and volume metadata.

**T5 — Passive network observation.** Attacker intercepts traffic on the network. Mechanism: taps the wire. Defense: transport encryption. Outcome: same as T4.

**T6 — Lost or stolen device.** Attacker gains physical access to a device with active leases. Mechanism: uses the device to access protected services. Defense: revocation (short propagation window) plus lease expiration (bounded exposure). Outcome: access is denied within `min(revocation_propagation, lease_expiry)`, typically 30 minutes to 30 days depending on policy.

**T7 — Sybil attack.** Attacker generates many identities to flood infrastructure. Mechanism: creates random Peer IDs and publishes dummy documents. Defense: the protocol does not prevent identity creation. Mitigation is at the deployment layer: rate limits, admission control, resource quotas. Outcome: attacker can create identities but cannot consume unbounded resources.

**T8 — Authorization escalation.** An authorized subject attempts to perform an operation beyond its grant. Mechanism: requests a capability not covered by the grant. Defense: network-level capability check plus application-level role check. Outcome: rejected at whichever layer first detects the mismatch.

**T9 — Authorization key compromise.** Attacker obtains an Authorization Key's private material. Mechanism: signs grants, leases, or revocations with the compromised key. Defense: `KeyRevocation` with `effective_sequence` bounds the exposure to forward time. Outcome: existing grants and leases survive; objects signed at or after the effective sequence are invalid.

**T10 — Device key compromise.** Attacker obtains a Device Key. Mechanism: signs reachability records. Defense: Device Keys sign only reachability; reachability is untrusted. Outcome: attacker can publish false endpoints, causing connection delays, but cannot affect authorization.

**T11 — Identity Root compromise.** Attacker obtains the Identity Root's private material. Mechanism: forges identity documents, grants, relationships, revocations. Defense: none in-band. Outcome: the entire principal is compromised. Recovery requires out-of-band coordination.

**T12 — Replay.** Attacker captures a valid object and presents it later. Mechanism: re-sends the captured bytes. Defense: validity intervals and sequence requirements. Outcome: expired objects are rejected; sequence-based rollback is rejected.

**T13 — Man-in-the-middle during pairing.** Attacker intercepts the pairing exchange and attempts to impersonate one of the parties. Mechanism: intercepts messages and substitutes their own key. Defense: PAKE with transcript binding and human verification. Outcome: pairing fails unless the attacker knows the shared secret.

**T14 — Clock skew.** Verifier's clock is significantly different from the issuer's. Mechanism: causes absolute-validity checks to misclassify. Defense: relative validity for leases. Outcome: authorization survives up to the lease duration in either direction of skew.

## C.2 Explicit non-properties

The protocol does not provide:

- **Anonymity.** Peer IDs are stable identifiers.
- **Metadata confidentiality against a global observer.** Traffic patterns, timing, and endpoint addresses are visible to infrastructure operators and on-path observers.
- **Protection against OS compromise.** If the device's operating system is compromised, all keys on that device are compromised.
- **Post-quantum security.** Ed25519 is vulnerable to quantum attacks.
- **Availability under adversarial conditions.** A determined attacker can deny access even if it cannot forge authorization.
- **Protection against authorized-but-malicious peers.** A peer with a valid grant can abuse it within the scope of the grant.

## C.3 Blast radius

| Compromised asset | Identity | Authorization | Reachability | Notes |
|-------------------|----------|---------------|--------------|-------|
| Identity Root | total | total | total | Everything under the principal is compromised |
| Authorization Key | no | total (forward) | no | Existing grants/leases survive until expiry |
| Device Key | no | no | total | Only reachability is affected |
| Service Key | no | no | no | Only service metadata is affected |
| Rendezvous server | no | no | partial | Can serve stale endpoints; cannot forge authorization |
| Relay | no | no | no | Metadata only; cannot decrypt |
| Application | no | no | no | Cannot exceed capabilities granted to it |

## C.4 Compromise response procedures

**Authorization Key compromise.** The Identity Root publishes a `KeyRevocation` targeting the compromised key with an `effective_sequence`. All objects signed by the compromised key at or after that sequence become invalid. Existing grants and leases signed before that sequence remain valid. A new Authorization Key is provisioned and legitimate grants are re-issued under it.

**Device Key compromise.** The Identity Root publishes a `KeyRevocation` targeting the device key and removes the corresponding entry from `device_bindings` in the next identity document. The device can no longer sign reachability. Reachability records previously signed by the device are rejected as untrusted.

**Identity Root compromise.** There is no in-band recovery. The principal must establish a new identity through an out-of-band mechanism (social coordination with peers, or an agreed threshold protocol added in a future version). Peers who previously trusted the old root must be informed out of band.

## C.5 Implementation requirements

Implementations must:

- Use constant-time comparisons for cryptographic operations.
- Validate canonical CBOR before semantic processing.
- Use standard library cryptographic implementations; do not implement primitives directly.
- Use OS-provided randomness for key and nonce generation.
- Clear private key material from memory after use.
- Not log private keys, credentials, or lease contents.
- Enforce rate limits on rendezvous queries and relay sessions.
- Validate timestamp ranges and sequence bounds.

Implementations should:

- Use hardware-backed key storage where available.
- Persist accepted stream state durably across restarts.
- Use monotonic time for relative-validity calculations.
- Provide diagnostic logging that does not include secrets.

---

# Part D — Connectivity and Relay in Full

## D.1 Preference order

When establishing a connection, the verifier attempts the following in order and stops at the first success:

1. **Local LAN** via mDNS or equivalent. Fastest; no cost.
2. **Direct IPv6** if both peers have routable addresses.
3. **Direct IPv4** if both peers have routable addresses.
4. **NAT traversal** via STUN/ICE-style candidate exchange and hole-punching.
5. **Relay** using the highest-priority relay in the reachability record.
6. **Alternative relay** in priority order if the first fails.

The preference order is not a protocol rule; it is the natural outcome of lower-latency and lower-cost paths being tried first. An implementation may deviate if it has information that changes the tradeoffs.

## D.2 Relay capability model

A relay advertises its capabilities as a set of properties:

- Maximum bandwidth
- Maximum concurrent sessions
- Maximum total bytes per session
- Maximum session duration
- Supported transport families (IPv4, IPv6)
- Expected latency characteristics
- Expected availability
- Geographic region
- Operator policy

The protocol does not standardize how these properties are published. The default is that a relay's reachability record includes a set of endpoints, and each endpoint's priority is determined by the reachability publisher's local policy.

## D.3 Raspberry Pi 3B reference numbers

These are illustrative, not normative. Actual numbers depend on the specific operating system, kernel networking stack, WireGuard implementation, and traffic profile.

- **WireGuard-encrypted forwarding throughput:** 100–150 Mbps
- **Concurrent sessions:** 100–200 depending on packet size
- **Per-session state:** roughly 500 KB
- **Base system memory:** roughly 200 MB
- **Power draw:** roughly 5 W sustained
- **Electricity cost at $0.12/kWh:** roughly $0.50/month
- **Hardware cost:** roughly $35 one-time
- **Break-even against electricity alone:** roughly 70 months

The Pi's practical limit is almost never the Pi. It is the residential uplink. A home connection with 20 Mbps upload can relay 20 Mbps regardless of what the Pi is capable of.

## D.4 Residential ISP constraints

Residential internet is asymmetric. Typical values:

- **Download:** 100–500 Mbps
- **Upload:** 5–50 Mbps
- **NAT type distribution:** roughly 5% symmetric, 20–30% address-restricted, 50–60% port-restricted, 5–15% full-cone
- **UPnP availability:** roughly 30–50% of routers
- **Data caps:** often 500 GB–1 TB/month on non-fiber connections

These constraints determine where relays are actually useful. A peer with full-cone NAT may be reachable directly. A peer with symmetric NAT likely requires a relay. A peer on satellite internet may have very high latency regardless of path.

## D.5 Multipath constraint list

These design decisions in V1 exist because they preserve the option to add multipath in a future version without a breaking change:

- Reachability records may carry multiple endpoint candidates.
- Relay tickets specify a source peer and a destination peer, not a specific connection.
- Path identity is distinct from connection identity.
- Authorization is path-agnostic.
- Relay selection is not encoded into any signed object.

No V1 implementation is required to use multiple paths. The constraints simply ensure that a V1.5 or V2 implementation can introduce multipath without changing the object model.

## D.6 Relay operator economics

These are illustrative. Actual margins depend on infrastructure costs, user mix, and pricing.

**Small operator, 10 Gbps capacity:**
- Monthly infrastructure cost: roughly $1000
- Users at $7/month average: 200
- Monthly revenue: $1400
- Monthly margin: $400 before developer share
- Developer share at 20%: $280
- Net margin: $120

**Medium operator, 100 Gbps capacity:**
- Monthly infrastructure cost: roughly $10,000
- Users at $7/month average: 2000
- Monthly revenue: $14,000
- Monthly margin: $4000 before developer share
- Developer share at 20%: $2800
- Net margin: $1200

**Large operator, 1 Tbps capacity:**
- Monthly infrastructure cost: roughly $100,000
- Users at $7/month average: 20,000
- Monthly revenue: $140,000
- Monthly margin: $40,000 before developer share
- Developer share at 20%: $28,000
- Net margin: $12,000

The economics improve with scale and with better peering arrangements. Operators that own their own fiber or have favorable peering have significantly lower per-Gbps costs.

---

# Part E — Where This Addendum Differs from the Master Archive

There are two places where a reader might notice an apparent difference between this addendum and the Master Archive. In both cases, the Master Archive governs.

**Chain hash base case.** This addendum uses the construction from OBJECTS.md §8.3.5, which is `SHA-256(canonical_cbor(["grid/chain-base/v1", domain_separator, stream_id]))`. A version of the object model sometimes circulated as "previous_chain_hash = domain_separator at sequence 1" is incorrect; the base state is always SHA-256-wrapped and includes `stream_id`.

**Signature input structure.** This addendum uses `canonical_cbor(["grid/signature/v1", domain_separator, unsigned_payload, chain_hash])`. A version that signs a structure containing `payload_id` in place of `unsigned_payload` is not the same wire format; the signature covers the payload directly, and `payload_id` is a derived value that happens to be computed from that same payload.

Everything else in this addendum is compatible with the Master Archive. Where the addendum is silent, the archive's position stands.

---

# Part F — Relationship to the Master Archive

The Master Archive remains the primary document. This addendum:

- Fills in byte-level construction details
- Provides worked examples for cryptographic operations
- Enumerates the full threat model with per-threat detail
- Gives illustrative performance and economic numbers
- Explicitly reconciles the two drift points above

It does not introduce new protocol objects, new authority domains, or new invariants. Every construction it describes is derived from OBJECTS.md §8.3 and the Master Archive's protocol summary.

When implementing:

1. Read the Master Archive for the shape of the protocol.
2. Read this addendum for the specific constructions.
3. Read OBJECTS.md for the exact byte-level encoding when implementing.
4. Read Part 9 of the Master Archive for the security model when auditing.

---

# End of Addendum


# Grid Network — Design Defense Addendum

**Status:** Companion to the Master Archive and the Detailed Reference Addendum
**Purpose:** Record the specific criticisms the design has faced, the objections that were originally raised against it, and the clarifications that resolved them. This is the document a skeptical reviewer should read first, because it anticipates and answers the questions they will ask.

---

## Why this addendum exists

Every protocol that survives gets criticized. The criticisms are usually the same set, asked in roughly the same order, by every serious reviewer. If the protocol has good answers, the criticisms become predictable enough to document. If the protocol does not have good answers, the criticisms become fatal.

This addendum records:

1. The criticisms that were raised during the design process.
2. The objections that were initially made (including by reviewers who were sympathetic to the goal but skeptical of the approach).
3. The clarifications that turned each objection from "this is a problem" into "this is a design decision with tradeoffs."

The document is written for a reviewer who has not yet read the Master Archive. It is not a substitute for the archive; it is the argument for why the archive is worth reading.

---

# Part 1 — The criticisms that were raised

## 1.1 "This is just Tailscale"

The most common first reaction. It expresses three distinct concerns that need to be answered separately:

- **Concern A:** The feature set overlaps with existing products.
- **Concern B:** Existing products work well, so why build another?
- **Concern C:** The market is already served, so adoption is unlikely.

**The answer to Concern A** is that the feature set overlaps at the surface but not at the foundation. Tailscale is a mesh VPN product. Grid Network is a control plane for identity and authorization that *can be used* to build a mesh VPN. The distinction matters because Tailscale's identity model is account-based and its protocol is proprietary. Grid Network's identity is portable and its protocol is open. Two systems can have similar UX and radically different architectural properties.

**The answer to Concern B** is that Tailscale works well *for the problems Tailscale was designed to solve*. It does not solve portability of identity across providers, self-hosting without a vendor, or application-level device identity that survives vendor changes. Those are problems Grid Network is designed around, and they are not solved by any current product.

**The answer to Concern C** is that the market is not a single market. It is at least three overlapping markets:

- Users who want a managed mesh VPN with excellent UX (Tailscale's market).
- Users who want self-hosted connectivity without a vendor (partially served by Headscale, Netmaker, and others).
- Users who want an application-level protocol they can integrate against, so that "remote access" becomes a solved problem for their product (not served by any current product).

Grid Network targets the third market primarily. If it succeeds there, it may also serve the second and compete in the first. But the third is where the design is differentiated.

## 1.2 "This is too complex"

The second-most common reaction. It expresses a concern that the design has accumulated more mechanisms than the problem requires.

This criticism is partially correct and worth stating honestly.

The design has:

- Six authority domains
- Four key roles (with sub-roles)
- Five object hierarchies
- Three contribution layers
- Two pairing mechanisms
- Two time models (absolute and relative validity)

Each of these exists for a reason. Six authority domains exist because collapsing them causes specific attacks (a rendezvous server that can grant authorization, a relay that can impersonate a peer, an application that can decide device identity). Four key roles exist because key compromise needs to be bounded. Five object hierarchies exist because identity, authorization, reachability, and service state have different lifecycles.

The question is not "could this be simpler in isolation?" The question is "could this be simpler without losing the properties that make it work?"

The answer is: some of it could, and the design has been trimmed repeatedly during its development. Earlier drafts had more concepts; they were rejected because the additional complexity did not protect a specific boundary.

What remains is the minimum complexity that preserves the invariants. If a future revision finds a way to preserve the same invariants with fewer concepts, that is a strict improvement and should be adopted.

## 1.3 "Nobody cares about portability"

The third-most common reaction. It expresses a belief that the specific property Grid Network is designed around — portability of identity across infrastructure providers — is not a property that users actually want.

This criticism is empirically testable and the design process treated it as such.

The counter-argument is that users *do* care about portability, but only *after they have been burned by its absence*. A user who has never had a service shut down does not think about portability. A user whose NAS maker restricted the built-in remote access feature, or whose VPN vendor was acquired and changed pricing, or whose coordination server shut down, thinks about it constantly.

The relevant audience is therefore not "all users" but "users who have already encountered the problem portability solves." That audience exists, is growing, and is not well-served today.

The design does not require that all users care about portability. It requires that enough users care to sustain the initial ecosystem. The argument for that threshold being reachable is:

- Open-source application developers are a natural first adopter, because they are the ones who currently bear the cost of building connectivity infrastructure themselves.
- Self-hosters who have been burned are a natural second adopter.
- Enterprises with vendor-lock-in concerns are a natural third adopter.

If any of these three groups adopts in sufficient numbers, the network reaches a sustainable scale. If none do, the design remains a well-constructed argument rather than a working network.

## 1.4 "This is a solution in search of a problem"

A subtler criticism. It expresses a belief that the design was assembled from interesting mechanisms without a genuine need driving it.

The answer is that the design has a specific problem statement, and it has been consistent throughout:

> Every self-hosted service eventually needs remote access. Today the choices are to expose to the internet, to depend on a vendor, or to become a sysadmin. None of these is acceptable for the users who most need it.

The problem is not invented. It is the observed status quo for every self-hosted application. The design has not changed the problem statement during its development; it has refined the solution.

## 1.5 "The commercial model won't work"

A critique from reviewers with market-design backgrounds. It expresses concern that the relay priority classes, credit pools, geographic multipliers, and revenue share mechanisms have not been tested at any scale.

This is correct. The commercial model is a hypothesis, not a proven design.

The response is not to defend the model but to reframe its status. The commercial model is *conditional*. It describes what the network *could* sustain if it reached the scale at which commercial infrastructure became necessary. It is not a requirement of the protocol. If the network reaches scale and the model does not work, the community can invent a different one; the protocol does not commit to the specific model.

What the protocol does commit to is:

- Free tier is unconditional.
- No user is required to pay for basic functionality.
- Infrastructure is replaceable.
- No operator is required.

Those commitments make it possible to experiment with commercial models over time. The specific model proposed is the one that seems most likely to work, based on analogies to email providers, CDNs, and mobile roaming. It is not the only possible model.

## 1.6 "The security model has holes"

A critique from security reviewers. It expresses concern that some scenarios are not fully defended.

The honest answer is that some scenarios are not defended, and the design names them explicitly rather than hiding them. The explicit non-properties are:

- Anonymity.
- Metadata confidentiality against a global observer.
- Protection against OS compromise.
- Post-quantum security.
- Availability under adversarial conditions.
- Protection against authorized-but-malicious peers.

Each of these is a real gap. None of them is a gap the design *claims* to fill. The distinction between "not defended" and "claimed to be defended and not" is important; the first is an honest limitation, the second is a security bug.

The one gap that is worth calling out as *sharp* is Identity Root compromise. If the root is compromised, the entire principal is compromised, and there is no in-band recovery. This is a deliberate choice — any in-band recovery mechanism would be an authority the protocol cannot trust — but it means that protecting the root is critical and there is no protocol-level fallback if protection fails.

This is not a defect. It is a design tradeoff. The alternative (an in-band recovery authority) introduces a new authority that must be trusted, and the design process concluded that the tradeoff was worse.

## 1.7 "The design is overengineered for what it delivers"

A critique from pragmatic engineers. It expresses concern that the design spends a lot of complexity on properties (portability, offline verification, authority separation) that might not be worth their cost.

The response is that these properties are the *point*. A protocol that delivers Tailscale-equivalent functionality without portability would be a strictly worse version of Tailscale. The only reason to build something new in this space is to deliver properties that existing systems do not.

The complexity exists to produce those properties. Whether it is worth it is a judgment call that depends on how much the adopter values the properties. For users who do not care about portability, Tailscale is better. For users who do, Grid Network is the only option.

## 1.8 "The naming is wrong"

A critique that was raised repeatedly during development, and led to a full renaming.

The original name "NotDNS" was rejected because it defined the project by what it was not. "Mesh Coordinator" was rejected as too generic. "Mesh Identity & Reachability Protocol" was rejected because the acronym was awkward. Several single-word candidates (Lattice, Signet, Ravelin) were rejected because of collisions.

"Grid Network" was selected because it is descriptive, uncollided, memorable, and scales across audiences. It is not perfect — "Grid" is a common word and may collide with unrelated products — but it is better than the alternatives.

The naming decision is documented in Part 19 of the Master Archive. If a better name is found later, the protocol can be renamed once, before any implementations adopt the current name. After that, renaming becomes expensive.

---

# Part 2 — The objections that were made

The criticisms above are the general ones that every reviewer raises. The objections below are the specific ones that came up during development, including objections made by reviewers who were sympathetic to the goal but skeptical of specific decisions.

## 2.1 "Self-certifying IDs would be simpler"

**The objection:** Peer IDs could be hashes of identity roots, which would mean a verifier could compute the ID from the public key and verify the binding without an identity document.

**Why it was considered:** Self-certifying IDs are elegant. They remove a class of attacks (identity document substitution) and reduce the number of objects a verifier must process.

**Why it was rejected:** Self-certifying IDs cannot rotate the identity root without changing the ID. Since root rotation is a core requirement (for key compromise recovery, for algorithm migration), the design would have to either (a) never rotate roots, which is unacceptable, or (b) accept that rotation changes the peer's identity, which means it is not really a durable identity at all.

Opaque IDs with signed identity documents solve this. The cost is one extra object (the identity document) that must be verified. The benefit is that rotation is possible without changing identity.

## 2.2 "One stream per issuer is overkill"

**The objection:** Grants, leases, and revocations could share a single global stream, with sequence numbers that are globally ordered. This would be simpler than maintaining per-issuer streams.

**Why it was considered:** Global sequence numbers are easier to reason about for a naive implementation. There is one counter, and it always goes up.

**Why it was rejected:** Global sequence numbers require global coordination. Two issuers signing objects simultaneously would have to agree on which one goes first. That agreement is not possible without a consensus mechanism, which the design deliberately does not have.

Per-issuer streams avoid this. Each issuer maintains their own sequence, and there is no coordination required. The cost is that a verifier must not compare sequence numbers across streams. This is a discipline requirement, not a complexity requirement.

## 2.3 "Cumulative chain hashes are expensive"

**The objection:** Each chain hash commits to the entire stream history, not just the previous object. This means each object carries a hash that grows in computation cost as the stream grows.

**Why it was considered:** A linear chain (each object links only to the previous) would be cheaper to compute.

**Why it was rejected:** A linear chain cannot detect forks when a verifier has seen only one branch. The verifier sees branch A and has no way to know that branch B exists. With cumulative hashing, the verifier can detect the fork immediately because the fork's chain hash will not match what the verifier would compute.

The cost of cumulative hashing is one extra hash computation per object, which is negligible on modern hardware. The benefit is fork detection that works from a single branch.

## 2.4 "PAKE is overkill for pairing"

**The objection:** For pairing two devices, a simpler mechanism would suffice. Both sides could simply exchange public keys and confirm them via the human-readable code.

**Why it was considered:** PAKE requires a cryptographic library and careful implementation. A simpler exchange would be easier to implement.

**Why it was rejected:** A simpler exchange is vulnerable to man-in-the-middle attacks. An attacker who intercepts the exchange can substitute their own public key for one of the parties' keys, and the human-readable code would still match if the attacker is careful. PAKE prevents this by binding the session to the shared secret, which the attacker does not have.

The cost is a PAKE library and a correct implementation of the protocol transcript. The benefit is that pairing is secure against active attackers, which is essential because pairing is when the trust relationship is established.

## 2.5 "Revocation should be reversible"

**The objection:** Sometimes a revocation is issued in error. Being able to un-revoke would let the issuer correct mistakes without forcing the subject to re-establish authorization.

**Why it was considered:** Reversibility is a common feature in access control systems. It reduces friction when mistakes are made.

**Why it was rejected:** Reversibility creates a class of subtle bugs. If a revocation is reversible, then every verifier must decide whether to trust the un-revocation, which requires the un-revocation to be signed and distributed, which reintroduces the state that the original revocation removed. Attackers can exploit races between revocation and un-revocation. The design chose terminal revocation because it is simpler and safer.

If an issuer revokes by mistake, the recovery is to issue a new grant. The new grant has a new `grant_id`, so there is no ambiguity about which grant is currently authorized.

## 2.6 "Offline tolerance is a footgun"

**The objection:** Allowing a verifier to continue authorizing for up to `max_offline_tolerance` without refreshing state means the verifier may authorize on stale information for a long time. This is a security risk.

**Why it was considered:** It would be safer to require freshness for every authorization decision, which would mean the verifier must contact the issuer or a freshness source before every decision.

**Why it was rejected:** Requiring freshness before every decision breaks offline operation. A device that goes offline cannot authorize on return until it has refreshed, which means the device cannot use any resource until it has reconnected. That is unacceptable for many use cases.

The design chose to make the tradeoff explicit via `max_offline_tolerance`, which is a per-grant policy. A grant with tolerance of zero means "always require freshness"; a grant with tolerance of thirty days means "allow offline authorization for up to thirty days." The issuer decides the tradeoff per grant.

## 2.7 "The protocol should include multipath"

**The objection:** Since the design discusses multipath extensively, it should be in V1 rather than deferred.

**Why it was considered:** Multipath is a genuinely useful capability. Deferring it means users with high-bandwidth needs cannot benefit from it in V1.

**Why it was rejected:** Multipath requires coordination between paths (sequence numbers across paths, packet reordering, congestion control across paths) that is genuinely hard to get right. It also requires relay selection algorithms that are implementation-specific. Putting it in V1 would complicate the protocol kernel with an orthogonal concern.

The design chose to constrain V1's objects so that multipath *can* be added later without a breaking change, while not requiring it in V1. This is the standard pattern for protocols that expect to grow.

## 2.8 "Why not just use DNS for discovery"

**The objection:** DNS already solves the "given a name, find an address" problem. The rendezvous layer duplicates that.

**Why it was considered:** DNS is universal, well-understood, and has an enormous infrastructure. Reusing it would eliminate the need for a custom discovery protocol.

**Why it was rejected:** DNS is a name-to-address mapping. Grid Network's discovery is an identity-to-reachability mapping with authorization attached. The semantics are different: a DNS record says "this name is currently at this address"; a reachability record says "this authenticated peer is currently reachable at these candidates, and this record is signed by the peer's device key." DNS cannot carry the signature or bind the record to the peer's identity.

Grid Network can *use* DNS for bootstrap (a well-known DNS name pointing at a rendezvous server), but DNS cannot replace the rendezvous layer's semantics.

## 2.9 "The four-layer model is arbitrary"

**The objection:** The choice of four layers (protocol, security, connectivity, strategy) seems arbitrary. Why four? Why not three or five?

**Why it was considered:** The layering is a project-management tool, and its boundaries could be drawn differently.

**Why it was kept:** The four layers correspond to distinct audiences with distinct concerns. Protocol is for implementers. Security is for reviewers. Connectivity is for infrastructure builders. Strategy is for adopters and operators. Collapsing any two would put material in front of an audience that does not need it, and separating them further would fragment the material unnecessarily.

The layering is not normative. If a specific project has a different organizational structure, it can reorganize the documents. The four-layer model is a default, not a requirement.

---

# Part 3 — The clarifications that made it interesting

The objections above were resolved by clarifications. In several cases, the clarification was not "here is the answer to your objection" but "here is why the objection is based on a different framing than the design uses." These are the clarifications that turned the design from "interesting but questionable" into "interesting and defensible."

## 3.1 "The protocol does not negotiate identity — it verifies it"

The most important clarification. It resolves a large number of objections at once.

The design is not a system that *decides* who a peer is. It is a system that *verifies* who a peer has already claimed to be. The verifier does not ask a server "who is this peer?" The verifier holds the peer's identity document and evaluates it locally.

This reframing resolves:

- "What if the rendezvous is malicious?" — Rendezvous does not decide identity, so a malicious rendezvous cannot change who a peer is.
- "What if the relay is malicious?" — Relays do not decide identity, so a malicious relay cannot substitute a different peer.
- "What if the DNS is hijacked?" — DNS does not decide identity, so hijacking it cannot change who a peer is.

The question "who decides identity?" has a specific answer in the design: the identity document, signed by the identity root, verified locally. No infrastructure component decides identity.

## 3.2 "Failure is not a state change"

The second most important clarification. It resolves a large class of failure-handling objections.

Many systems treat failures as events that can change state. A network failure means a peer is offline. A rendezvous failure means a peer is unreachable. A relay failure means a connection is broken.

The design treats failures as conditions that affect *availability* but never *authorization*. A network failure means "the peer is currently unreachable" but does not mean "the peer is not authorized." A rendezvous failure means "the current endpoint is unknown" but does not mean "the peer's identity has changed." A relay failure means "the current path is broken" but does not mean "the peer's authorization has been revoked."

This reframing means that failure-handling code never has to make a security decision. It only has to make an availability decision. Security decisions are always made from accepted state, which failures never modify.

## 3.3 "Bounded exposure is not unbounded exposure"

A clarification that resolves a class of concerns about leakage.

Any system that has limits on how long authorization can persist without refresh has to choose a limit. A limit of zero means authorization is effectively useless offline. A limit of infinity means authorization never expires. Neither extreme is acceptable.

The design uses `max_offline_tolerance` as a per-grant policy. The issuer chooses how long the grant can authorize without refresh. A grant for a low-risk capability may have a thirty-day tolerance; a grant for a high-risk capability may have a one-hour tolerance.

The clarification is that "bounded exposure" is different from "unbounded exposure." A system with a thirty-day tolerance has a *measurable* security property: after thirty days, authorization is revoked even if the verifier has not received a revocation. This is a weaker property than "authorization is revoked immediately on compromise," but it is a *definite* property, and it is measurable.

## 3.4 "Rendezvous and relay are infrastructure, not authorities"

A clarification that resolves a class of concerns about trust.

Infrastructure components in the design have a specific property: they can *fail* but they cannot *lie convincingly*. A rendezvous server can refuse to serve a query. A relay can refuse to forward traffic. But neither can forge a signature, modify a signed object without detection, or grant authorization.

The clarification is that this is not "the infrastructure is not trusted" in the sense of "we hope the operator is not malicious." It is "the infrastructure *cannot* be malicious in the ways that matter, because the protocol does not give it the ability."

A malicious rendezvous server can:
- Serve stale endpoints (delay connections).
- Serve false endpoints (cause connections to fail).
- Refuse to serve queries (deny service).

A malicious rendezvous server cannot:
- Change a peer's identity.
- Create or modify authorization.
- Decrypt traffic.

The second list is empty because the protocol does not have mechanisms that could be abused this way. The infrastructure is not trusted; it is *not trusted with anything important*.

## 3.5 "Offline verification is not a compromise, it is a requirement"

A clarification that resolves a class of concerns about freshness.

Some systems are designed to always require freshness. Every authorization decision requires the verifier to contact the issuer or a designated freshness source.

The design takes the opposite position: freshness is a *bounded* property, but it is not *required* for every decision. A verifier can make decisions offline, up to the grant's `max_offline_tolerance`.

The clarification is that "offline verification" is not a compromise between security and availability. It is a *design requirement* that comes from the use case. If a device goes offline for six months, it must still be able to operate on cached state when it comes back online. A system that requires online verification cannot serve this use case.

The security cost is bounded: an offline verifier may authorize on stale information, but only for the duration of the tolerance. The security benefit is that the system remains useful in conditions that would otherwise break it.

## 3.6 "Identity is not a service, it is a keypair"

A clarification that resolves a class of concerns about provisioning.

Many systems treat identity as a service: an authority issues identities, an authority provisions devices, an authority controls access.

The design treats identity as a keypair: a peer generates its own keys, binds them to a peer ID via a signed identity document, and publishes that document to peers who want to recognize it. No authority is involved.

The clarification is that this eliminates a class of attacks (identity issuer compromise), a class of costs (identity provisioning infrastructure), and a class of vendor dependencies (no need to sign up with anyone).

The tradeoff is that identity must be established out of band (via pairing), because there is no authority to issue it. This is the same tradeoff that SSH and Signal made, and it is the correct tradeoff for a protocol that needs to work without a central authority.

## 3.7 "The commercial layer is optional"

A clarification that resolves a class of concerns about sustainability.

Some protocols require commercial adoption to function. If no one pays, the protocol cannot operate.

The design does not require commercial adoption. The relay layer is a fallback for cases where direct connectivity fails. If no commercial relay exists, the network still works for the cases where direct connectivity succeeds (which is most cases). If no one pays for anything, the network still works for the users who care about the fallback being available, using volunteer infrastructure.

The clarification is that "commercial sustainability" is a property of the ecosystem, not a requirement of the protocol. The protocol works without any commercial infrastructure. Commercial infrastructure is an *addition* that makes the network better for users who want guarantees. It is not a *requirement* for the network to function.

This is the same model as email. Email works without paid providers. Paid providers make email better for users who want specific guarantees. The protocol itself does not require any provider.

## 3.8 "The design is Linux, not a startup"

A clarification that reframes the entire project.

A startup is designed to capture value. It has investors, a growth plan, and an exit. Its success is measured by its market share.

The design is not a startup. It is infrastructure, in the same sense that Linux is infrastructure. Its success is not measured by capturing value; it is measured by *adoption* — by the number of applications and users who find it useful enough to build on.

The clarification is that this reframing changes what "success" means:

- A startup succeeds by dominating a market.
- Infrastructure succeeds by being adopted widely enough to matter.
- A startup optimizes for growth and defensibility.
- Infrastructure optimizes for openness and ease of use.

The design is optimized for the second model. This is why the protocol is free, why the objects are open, why the identity is portable, and why the design has no mechanism that would allow a single entity to capture the network.

If the design were optimized for the startup model, it would be a different design. It would have proprietary elements, a capture mechanism, and a growth plan that ends in a defensible position. It has none of these things, and that is intentional.

---

# Part 4 — The framing that makes the design interesting

When the criticisms and objections are resolved, the design becomes interesting because of a specific reframing:

> **The design is not a system that connects devices. It is a system that makes trust portable.**

Every device that exists today has a set of relationships — with its owner, with other devices, with services, with peers. Those relationships are usually defined by the network the device is on. Move the device to a different network and the relationships break. Change the network's provider and the relationships break.

The design makes the relationships themselves the durable thing and the network the replaceable thing. A device can move between networks, change providers, go offline for months, and its relationships survive.

This is the property that no other system provides today. It is not "secure remote access" (Tailscale provides that). It is not "self-hosted VPN" (Headscale provides that). It is "relationships that survive infrastructure changes," which is a property that has not been provided by any widely-adopted system.

The design exists because this property is the thing that makes the difference between "I have remote access today" and "I have remote access that will still work in ten years, regardless of what happens to the vendors involved."

---

# Part 5 — What to tell a skeptical reviewer

If a reviewer asks "why should I care about this?" the answer is:

> Because the alternative is that every device you own has relationships that are owned by a vendor. Your phone recognizes your server because Tailscale's servers say so. Your laptop recognizes your NAS because your NAS signed up for a DDNS service. If any of those vendors changes their terms, changes their pricing, or shuts down, your relationships break.
>
> The protocol you are reviewing makes relationships portable. It separates what the relationships *are* (identity, authorization, reachability) from the infrastructure that *helps establish* them (rendezvous, relays). If the infrastructure changes, the relationships survive.
>
> This is a property that does not exist today. It is the property that the protocol is designed around. Every other design decision — the crypto, the objects, the failure semantics, the commercial model — is downstream of that single property.

If the reviewer asks "what makes it different from Tailscale?" the answer is:

> Tailscale is a mesh VPN product. Grid Network is a control plane for identity and authorization that can be used to build a mesh VPN. The distinction matters because Tailscale's identity model is account-based and its protocol is proprietary. Grid Network's identity is portable and its protocol is open.
>
> If you want the best mesh VPN product, use Tailscale. If you want an identity layer that you can carry with you across providers, that is what Grid Network is for.

If the reviewer asks "why should I believe this will work?" the answer is:

> You should not believe it will work. You should believe that the design is coherent and that the argument for why it could work is strong. Whether it actually works depends on implementation, adoption, and the ecosystem that emerges. The design does not guarantee success; it provides a foundation that makes success possible.

The design is not asking for belief. It is asking for engagement. The reviewer is invited to find flaws in the reasoning, propose alternate approaches, and test the design against their own use cases. The design has been revised many times during its development, and it will be revised again if specific flaws are found.

---

# End of Addendum

This addendum is complete. It should be stored alongside the Master Archive and the Detailed Reference Addendum as `ADDENDUM-DEFENSE.md`. Together, the three documents provide:

- **Master Archive:** The map of the protocol.
- **Detailed Reference Addendum:** The specifics.
- **Design Defense Addendum:** The argument for why the specifics matter.

This addendum is complete and self-contained. It should be stored alongside the Master Archive as `ADDENDUM-DETAIL.md`.