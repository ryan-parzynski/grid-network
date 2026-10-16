# Grid Network — Security Model

**Revision:** 2.5
**Protocol version:** v0.6.3

**Repository path:** `spec/SECURITY.md`

This document is non-normative. It records the security properties of
the protocol, the threats the protocol addresses, the threats it does
not address, the consequences of key compromise, and implementation
guidance. It introduces no object types, no authority, and no
requirement. Where this document and the Protocol Specification
conflict, the specification governs.

Each statement cites the section it relies on. Where the source is not
`PROTOCOL.md` or `OBJECTS.md`, the cited document is named. Where a rule
is cited, the cited section is the source.

---

## 1. Security model

The protocol's security comes from separation of authority:

- Identity establishes cryptographic control.
- Relationships establish recognition.
- Authorization establishes permission.
- Leases establish current validity.
- Reachability establishes current connectivity information.
- Rendezvous provides discovery.
- Relays provide transport.
- Applications consume authorized connections.

No intermediary becomes an authority by observing, storing, forwarding,
or relaying protocol data. A rendezvous server cannot create identity
or authorization. A relay cannot create authorization. A reachability
record does not grant access. Knowledge of an endpoint does not imply
identity. Possession of a signed object does not override the
verifier's trusted state. Transport success does not imply application
authorization.

These properties follow from the core security invariant
(`PROTOCOL.md §1`), the authority domains (`PROTOCOL.md §37`), and the
distinction between network and application authorization
(`PROTOCOL.md §13`).

Rendezvous and relay infrastructure operate outside the authority
chain (`PROTOCOL.md §23`, `PROTOCOL.md §25`). A compromise of discovery
or transport infrastructure therefore produces availability and
metadata consequences, not unauthorized access.

---

## 2. Threats addressed

Each row names an adversary, what the adversary attempts, and the rule
that bounds the outcome.

| Adversary | Attempt | Bound on the outcome |
|---|---|---|
| Malicious peer | Impersonate another principal or forge an authorization | Objects must verify against locally trusted anchors and the signing-authority matrix (`PROTOCOL.md §33`, `PROTOCOL.md §42`). A grant is valid only when signed by the issuer's Authorization Key (`PROTOCOL.md §9`) |
| Malicious rendezvous | Forge or alter reachability, or withhold records | Records are signed and are hints, not proof of access (`PROTOCOL.md §23`, `PROTOCOL.md §24`). Withholding and staleness degrade availability only; peers may use several rendezvous providers (`PROTOCOL.md §43`) |
| Malicious relay | Forge authorization or read traffic | A relay forwards traffic under a ticket and holds no authorization authority (`PROTOCOL.md §25`). Confidentiality is provided by the transport (`PROTOCOL.md §26`) |
| Eavesdropper | Read traffic | Traffic confidentiality is provided by the transport (`PROTOCOL.md §26`). Metadata observation is outside the protocol's protections (`PROTOCOL.md §47`, Section 3) |
| Lost or stolen device | Use a device's keys | The Identity Root publishes a `KeyRevocation` (`PROTOCOL.md §14`, `PROTOCOL.md §16`, `PROTOCOL.md §42`). Revocations are pulled and have no normative propagation bound (`PROTOCOL.md §31`). Objects below `effective_sequence` remain valid only if the verifier had already accepted their chain hashes, and only until their own expiry (`PROTOCOL.md §16`, `PROTOCOL.md §17`) |
| Insider | Exceed granted authority | Grants carry capabilities, and unknown capabilities never authorize access (`PROTOCOL.md §11`, `PROTOCOL.md §43`). Application authorization is separate (`PROTOCOL.md §13`) |
| Verifier with an incorrect clock | Cause leases to be judged wrongly | Relative lease validity survives clock skew up to the lease duration (`PROTOCOL.md §32`). Absolute timestamps are vulnerable, and `MAX_CLOCK_SKEW` is the recommended mitigation (`PROTOCOL.md §39`) |
| Replay attacker | Present captured objects again | Streams have monotonic sequence numbers and chain hashes (`OBJECTS.md §9`, `OBJECTS.md §3`). Verifiers persist observation records for relative lease validity, and a lease whose `issued_at` is older than `MAX_LEASE_AGE` is rejected (`PROTOCOL.md §10`) |
| Man-in-the-middle at pairing | Interpose between two devices | Pairing runs a PAKE (SPAKE2) with a high-entropy secret delivered out of band, bound to a transcript that includes both principals' identity roots. The receiving user confirms the pairing, and the secret is consumed on first successful use (`PROTOCOL.md §20`, `PROTOCOL.md §21.1`, `PROTOCOL.md §21.3`). Residual limits are stated in `PROTOCOL.md §21.6`. Unattended enrollment weakens the confirmation property (`PROTOCOL.md §21.4`) |
| Equivocating issuer | Publish two objects at one sequence | A verifier that observes both enters `FORK_DETECTED` and does not advance authorization until a `StreamResolution` is accepted (`OBJECTS.md §9.3`, `OBJECTS.md §9.4`, `PROTOCOL.md §40`) |
| Sybil attacker | Create many identities | The protocol does not prevent identity creation. Admission control and rate limiting are infrastructure policy (`design/REJECTED.md` R7, `PROTOCOL.md §43`) |
| Denial of service | Overwhelm infrastructure | Availability is outside the protocol's guarantees (`PROTOCOL.md §47`). Rate limiting is implementation guidance (`PROTOCOL.md §43`) |

A signature covers `chain_hash` (`OBJECTS.md §3.12`). An object
therefore cannot be moved onto a different history without invalidating
its signature. A chain hash does not reveal a fork to a verifier that
has observed only one branch (`OBJECTS.md §3.8`).

The F1–F6 semantics (`PROTOCOL.md §39`) define failure behavior for
authorization failure, reachability failure, clock skew, revocation
ordering, forks, and communication interruption. F1 denies access when
any authorization check fails. F2 tries alternative endpoints and relays
when a reachability endpoint fails, and an unreachable peer is not a
denial.

---

## 3. Threats not addressed

The protocol does not provide the following. Where a rule states the
exclusion, the section is cited.

- **Anonymity.** Peers are identified. Rendezvous and relay operators
  can observe metadata (`PROTOCOL.md §47`).
- **Metadata protection.** Metadata is visible to infrastructure
  operators (`PROTOCOL.md §47`). A relay can observe packet size,
  timing, and source and destination identifiers (`PROTOCOL.md §25`).
  Metadata minimization is `planned` (`PROTOCOL.md §46`).
- **Endpoint compromise during pairing.** The protocol does not protect
  against a compromised device or a coerced user during pairing
  (`PROTOCOL.md §21.6`).
- **Availability.** Identity and authorization semantics survive
  infrastructure changes. Reachability does not (`PROTOCOL.md §47`).
- **Identity Root recovery.** Recovery is external and out of band
  (`PROTOCOL.md §18`).
- **Application authorization.** The protocol authorizes connectivity,
  not application roles or resource policy (`PROTOCOL.md §13`,
  `PROTOCOL.md §47`).
- **Quantum resistance.** Ed25519 is vulnerable to quantum attacks
  (`design/DECISIONS.md` D18). A post-quantum signature suite is a
  `planned` feature, not part of the current protocol version
  (`PROTOCOL.md §46`, `design/EXTENSIONS.md`).

Conformance is not a security certification (`PROTOCOL.md §44`).

---

## 4. Blast radius

Each key role is limited to the objects it signs (`PROTOCOL.md §6`,
`PROTOCOL.md §42`). The table states what an attacker who obtains the
component gains.

| Compromised component | Identity | Relationship | Authorization | Reachability |
|---|---|---|---|---|
| Identity Root | Total | Total | Total | Total |
| Authorization Key | None | None | Grants and leases signed by that key | None |
| Device Key | None | None | None | Reachability records for that device |
| Service Key | None | None | None | Service records for that service |
| Rendezvous server | None | None | None | Withholding, stale records, metadata |
| Relay | None | None | None | Disruption, metadata |

Notes:

- A compromised Authorization Key affects only the grants that key
  issued. Revoking it does not affect grants issued by other keys
  (`operations/DEPLOYMENT.md §7`).
- A Device Key signs only reachability records. It does not sign grants,
  leases, or identity objects (`PROTOCOL.md §42`).
- `GrantRevocation` is signed by the Identity Root, not by an
  Authorization Key (`PROTOCOL.md §15`, `PROTOCOL.md §42`).
- Sources for the table. Identity Root: `PROTOCOL.md §18`.
  Authorization Key and Device Key: `PROTOCOL.md §6` and
  `PROTOCOL.md §42`. Service Key: `PROTOCOL.md §6` and `PROTOCOL.md §42`;
  the protocol does not separately describe Service Key compromise, so
  the "None" cells for that row follow from the signing-authority
  matrix alone. Rendezvous server: `PROTOCOL.md §23` and
  `PROTOCOL.md §47`. Relay: `PROTOCOL.md §25` and `PROTOCOL.md §47`; the
  loss of a relay interrupts the relay sessions that use it
  (`operations/DEPLOYMENT.md §8.2`).
- The protocol does not describe the compromise of an application or
  of a network observer as a key role, so the table has no rows for
  them (`PROTOCOL.md §6`).

---

## 5. Compromise response

The responses below restate the protocol rules. They define no new
procedure.

**Authorization Key compromise.** The Identity Root publishes a
`KeyRevocation` for the key with an `effective_sequence`. Objects signed
by the key at or after `effective_sequence` are invalid. Objects signed
earlier remain valid only if the verifier accepted their chain hashes
before observing the revocation, and only until the grant or lease
expires. The issuer provisions a new Authorization Key and re-issues
grants under it (`PROTOCOL.md §16`, `PROTOCOL.md §17`).

**Device Key compromise or device loss.** The Identity Root publishes a
`KeyRevocation` for the device key (`PROTOCOL.md §16`,
`PROTOCOL.md §42`). `operations/DEPLOYMENT.md §7` describes removing the
device from the identity document. A verifier denies a peer whose
device has been revoked from `device_bindings` (`CONFORMANCE.md §2`,
Level 5), and checks that signing keys are current and not revoked
(`PROTOCOL.md §27`).

**Identity Root compromise.** The protocol provides no in-band
recovery. Any in-band mechanism would be an authority the protocol
cannot trust. Recovery is external and out of band, and the protocol
defines no recovery authority, no proof-of-ownership criteria, and no
adjudication procedure (`PROTOCOL.md §18`, `design/REJECTED.md` R5).
Threshold recovery is a `planned` feature and is not in the current
protocol version (`PROTOCOL.md §46`, `design/EXTENSIONS.md`).

**Propagation.** Revocations are pulled, not pushed. The protocol
defines no normative propagation bound (`PROTOCOL.md §14`,
`PROTOCOL.md §31`). Pull-based revocation is the accepted model
(`design/REJECTED.md` R15). Whether the protocol should define a
normative polling interval is an open question (`ROADMAP.md §5`).

---

## 6. Implementation guidance

The normative requirements for implementations are in
`PROTOCOL.md §43`. This section adds no requirements. It summarizes the
security-relevant items and records further guidance.

Requirements already stated in `PROTOCOL.md §43` that carry the most
security weight:

- Verify every signature and reject non-canonical or malformed
  encodings before semantic processing.
- Apply the verification procedure in `OBJECTS.md §8`. `OBJECTS.md §8.1`
  defines that procedure as a single atomic operation.
- Fail closed on missing information.
- Never cache authorization indefinitely.
- Never allow wall-clock time to extend authorization validity.
- Never auto-resolve a fork without an explicit `StreamResolution`.
- Never log credentials, grants, or leases, and never transmit private
  keys.

Further guidance, not required by the specification:

- Log security events without key material. `PROTOCOL.md §43` lists this
  as recommended.
- Protect the Identity Root offline or in hardware, and keep backups
  apart from running keys (`operations/DEPLOYMENT.md §7`).

---

## 7. Out of scope

The following are not covered by this document. Where a feature is
absent from the current protocol version, its status is stated.

- Relay capacity planning and hardware (see `operations/RELAYS.md`).
- Admission control for infrastructure. It is a deployment policy
  (`design/REJECTED.md` R7). Proof-of-work as a foundation is rejected
  (`design/REJECTED.md` R8).
- A security test program and security roadmap. The test vector format
  and conformance levels are defined in `spec/CONFORMANCE.md`; no test
  vectors have been published (`ROADMAP.md §1`). The development plan
  is in `ROADMAP.md`.
