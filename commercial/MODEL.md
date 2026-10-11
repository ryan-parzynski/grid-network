# Grid Network — Commercial Model

## Executive Summary

Grid Network's commercial model exists to fund the protocol's maintenance, not to extract value from users. Every participant — free user, contributor, commercial operator, enterprise — makes the network more valuable to every other participant.

**Core principle:** Free tier is real. Paid tier gets priority, not access.

---

## 1. Tier Structure

### Free Tier (Best-Effort)
- Unlimited relay usage (subject to fair-share limits)
- Unlimited rendezvous queries
- Full protocol features
- No account required
- No payment information
- Limits: Fair-share bandwidth (e.g., 1 Mbps concurrent, 10 GB/month), best-effort relay priority, rate limits on rendezvous queries

### Standard Tier ($5-10/month)
- 10 Mbps minimum relay bandwidth (guaranteed)
- Priority queuing (after dedicated, before free)
- Higher rate limits (30 lookups/sec)
- SLA: 99% uptime (monthly)

### Priority Tier ($20-50/month)
- 50 Mbps minimum relay bandwidth
- Highest priority queuing
- Lowest latency routing
- SLA: 99.5% uptime + latency <100ms

### Dedicated Tier (Custom Pricing)
- Guaranteed capacity (custom per agreement)
- Private relay if desired
- Highest priority (always served first)
- SLA: 99.99% uptime + custom latency guarantees
- 24/7 support
- Custom integration

---

## 2. Idle Capacity Donation

When paid users don't use reserved capacity, it flows to free pool.

```
Relay capacity: 100 Gbps total

Allocation:
  Free users: 20 Gbps (first-come-first-served)
  Standard: 40 Gbps (reserved)
  Priority: 30 Gbps (reserved)
  Dedicated: 10 Gbps (reserved per customer)

During peak evening:
  Standard users using 35 Gbps (5 Gbps idle)
  Priority users using 25 Gbps (5 Gbps idle)
  Idle capacity: 10 Gbps

Free users get: 20 Gbps reserved + 10 Gbps idle = 30 Gbps available
```

This model ensures free users have bandwidth, doesn't penalize paid users, and encourages overprovisioning.

---

## 3. Credit System

Users earn credits by contribution and spend on relay usage.

### Contribution
- Running a relay: earn per byte relayed
- Running a rendezvous: earn per query served
- Sharing reachability: earn per connected hour

### Exchange Rate
- 1 credit = 1 GB of relay bandwidth (standard tier)
- Scarcity multiplier for scarce regions

### Example
- Alice runs Pi relay for 1 month → relays 100 GB → earns 100 credits
- Spends 50 credits on her own relay usage
- Remaining: 50 credits (carry over)

### Fair Exchange
User invests $2 electricity → gets 100 credits → spends 100 credits → gets $100 of relay service. User profits on investment!

---

## 4. Credit Pools

Users can share relay credits in pools (families, groups).

```
Alice's family pool:
  Alice: $10/month
  Bob: $10/month
  Charlie: $5/month
  Total: $25/month = 2500 credits
  Shared among: Alice's server, Bob's server, Charlie's phone
```

Rules:
- Credits allocated to a pool
- Pool operators manage distribution
- Credits don't transfer between pools (prevents laundering)
- Credits are account-specific (can't be sold)

---

## 5. Geographic Scarcity & Fairness

Problem: Some regions have many relays, others have few.

Solution: Geographic multiplier.

```
Relay in NYC (abundant): 1 credit per GB
Relay in rural Iowa: 3 credits per GB
Relay in remote region: 5+ credits per GB
```

Multiplier calculated monthly from demand/supply ratio. Incentivizes operators to deploy in underserved areas.

---

## 6. Developer Funding

Commercial operators contribute 20% of revenue to developer fund.

```
Relay operator revenue: $100,000/month
Distribution:
  Operator: $80,000
  Developer fund: $20,000
  Infrastructure cost: $50,000 (paid from $80k)
  Operator margin: $30,000
```

Developer fund (20%) covers:
- Protocol maintenance
- Specification work
- Test vector production
- Security audits
- Documentation
- Community support

Why structural revenue share? Donations/grants are unreliable. Revenue share scales with adoption and incentivizes operators to grow the network.

---

## 7. Stewardship Entity

Independent of any commercial operator. Responsibilities:
- Maintain protocol specification
- Produce test vectors
- Conduct security audits
- Manage RFC process
- Arbitrate disputes

Funded by 20% revenue share from all operators. Board elected by operators + users. Prevents commercial capture.

---

## 8. What Commercial Operators Sell

**Operators do NOT sell:**
- Access to the network (it's open)
- Device identity (owned by user)
- Relationship data (on user's device)
- Authorization grants (signed by user)

**Operators DO sell:**
1. Reliability — Guaranteed uptime/latency SLA
2. Bandwidth — Reserved relay capacity
3. Geographic placement — Relays near the user
4. Support — Responsive help when things break
5. Integration — Custom setups for enterprises
6. Compliance — Audit logs, HIPAA/FedRAMP/SOC2 support

---

## 9. Economic Shape (The Flywheel)

```
Free users create network effect
  ↓
Developers see value, integrate Grid
  ↓
Applications adopt Grid
  ↓
Users get connectivity automatically
  ↓
More users (free) = bigger network
  ↓
Enterprises need better SLA
  ↓
Enterprises pay for premium tiers
  ↓
Commercial operators run relays
  ↓
Operators fund developer work
  ↓
Protocol improves
  ↓
Back to: Free users see value, integrate
```

---

## 10. Commercial Disruption

If Grid Network succeeds:

**Today's market:**
- Tailscale: owns device graph, $39.95/month per user
- Cloudflare Tunnel: $180/month for enterprise
- ZeroTier: free tier + $99/month for central management

**Post-Grid market:**
- Device graph: free (commoditized, Grid layer)
- Relay operators: $7-500/month depending on tier
- Support/compliance: $100-5000/month

What changes:
- Vendors can no longer charge for "device identity"
- Competition moves from "lock-in" to "quality"
- Smaller operators can enter market
- Users can switch providers without losing relationships

What survives:
- Vendors that are genuinely excellent
- Enterprise integration (custom configs, support)
- Hardware appliances (routers with Grid built-in)
- Managed infrastructure (users who don't want to self-host)

---

*End of Commercial Model*

---

## Relay Economics (Detailed)

# Grid Network — 

**Purpose:** Provide the specific details, worked examples, and elaboration that the  summarizes. Where this document and the  differ, the  governs.

---

## How to use this document

The  is the map. This document is the reference manual.

- **Shape, invariants, authority model, failure semantics** → 
- **Byte-level constructions, worked crypto examples, threat enumeration, capacity math** → this document
- **The authoritative source for a specific byte sequence** → OBJECTS.md, referenced from the 
- **The authoritative source for a security property** → Part 9 of the 

Where this document and the  differ on a normative point, the  governs. Differences are called out inline.

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

The chain hash commits to the entire presented prefix of the stream. It does not by itself reveal unseen siblings. Fork detection requires eligible authenticated conflicting evidence — the verifier must receive and verify two objects at the same sequence number with different object commitments (or their chain hashes) to know a fork occurred.

**Fork evidence walkthrough.** Suppose the issuer produces two conflicting objects at sequence 3:

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

A verifier that has accepted sequence 2 holds `chain_hash = h2`. When it receives a sequence-3 object, it recomputes `F(h2, c3)` and compares to the object's stated `chain_hash`. If they match, the object extends the accepted chain. If the verifier later receives a *different* sequence-3 object (from branch B) with commitment `c3'` and chain hash `h3'`, it can compare the two commitments at the same sequence position. The conflict `c3 != c3'` (or equivalently `h3 != h3'` with the same predecessor `h2`) is the authenticated evidence of a fork. Without seeing both branches, the verifier cannot distinguish between a valid extension and a forked branch — the chain hash only commits to the prefix it has seen.

The "Fork detection walkthrough" in MODEL.md Part A.3 is replaced by the "Fork evidence walkthrough" above. The key correction: a verifier with only one branch's sequence-3 object accepts it as a valid chain extension. Fork detection occurs only when the verifier later receives an eligible authenticated conflicting object at the same sequence number from a different branch. The cumulative hash commits to the presented prefix; it does not reveal unseen siblings.
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

---

*End of Commercial Model*
