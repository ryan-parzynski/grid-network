# Grid Network — Security Model

**Revision:** 2.3
**Protocol version:** v0.6.3

**Repository path:** `spec/SECURITY.md`

This document is non-normative. It records the security properties of
the protocol, the threats the protocol addresses, the threats it does
not address, the consequences of key compromise, and implementation
guidance. It introduces no object types, no authority, and no
requirement. Where this document and the Protocol Specification
conflict, the specification governs.

Every statement in this document traces to a rule in `PROTOCOL.md` or
`OBJECTS.md`. Where a rule is cited, the cited section is the source.

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
| Eavesdropper | Read traffic or observe grants | Traffic confidentiality is provided by the transport (`PROTOCOL.md §26`). Metadata observation is outside the protocol's protections (Section 3) |
| Lost or stolen device | Use a device's keys | The issuer revokes the key (`PROTOCOL.md §16`). Exposure ends when the verifier learns of the revocation (`PROTOCOL.md §31`) or the lease expires (`PROTOCOL.md §10`) |
| Insider | Exceed granted authority | Grants carry capabilities, and unknown capabilities never authorize access (`PROTOCOL.md §11`, `PROTOCOL.md §43`). Application authorization is separate (`PROTOCOL.md §13`) |
| Verifier with an incorrect clock | Cause leases to be judged wrongly | Relative lease validity survives clock skew; absolute timestamps are bounded by `MAX_CLOCK_SKEW` (`PROTOCOL.md §32`, `PROTOCOL.md §39`) |
| Replay attacker | Present captured objects again | Streams have monotonic sequence numbers and chain hashes (`OBJECTS.md §9`, `OBJECTS.md §3`). Leases carry observation records, and `MAX_LEASE_AGE` bounds replayed leases (`PROTOCOL.md §10`, `PROTOCOL.md §32`) |
| Man-in-the-middle at pairing | Interpose between two devices | Pairing runs a password-authenticated key exchange over a secret delivered out of band, and attempts are limited (`PROTOCOL.md §20`, `PROTOCOL.md §21`) |
| Equivocating issuer | Publish two objects at one sequence | A verifier that observes both enters `FORK_DETECTED` and does not advance authorization until a `StreamResolution` is accepted (`OBJECTS.md §9.3`, `OBJECTS.md §9.4`, `PROTOCOL.md §40`) |
| Sybil attacker | Create many identities | The protocol does not prevent identity creation. Admission control and rate limiting are infrastructure policy (`design/REJECTED.md` R7, `PROTOCOL.md §43`) |
| Denial of service | Overwhelm infrastructure | Availability is outside the protocol's guarantees (`PROTOCOL.md §47`). Rate limiting is implementation guidance (`PROTOCOL.md §43`) |

A signature covers `chain_hash` (`OBJECTS.md §3.12`). An object
therefore cannot be moved onto a different history without invalidating
its signature. A chain hash does not reveal a fork to a verifier that
has observed only one branch (`OBJECTS.md §3.8`).

Failure behavior under each of these conditions is defined by the F1–F6
semantics (`PROTOCOL.md §39`). The semantics are fail-closed for
authorization and availability-preserving for reachability.

---

## 3. Threats not addressed

The protocol does not provide the following. Where a rule states the
exclusion, the section is cited.

- **Anonymity.** Peers are identified. Rendezvous and relay operators
  can observe metadata (`PROTOCOL.md §47`).
- **Global surveillance resistance.** A network observer can observe
  endpoints and traffic volume. The protocol does not hide them
  (`PROTOCOL.md §47`).
- **Endpoint compromise.** If the operating system of a device that
  holds keys is compromised, the keys held on that device are
  compromised. The protocol cannot protect them.
- **Availability.** Identity and authorization semantics survive
  infrastructure changes. Reachability does not (`PROTOCOL.md §47`).
- **Identity Root recovery.** Recovery is external and out of band
  (`PROTOCOL.md §18`).
- **Application authorization.** The protocol authorizes connectivity,
  not application roles or resource policy (`PROTOCOL.md §13`,
  `PROTOCOL.md §47`).
- **Quantum resistance.** Ed25519 is not quantum-resistant. A
  post-quantum signature suite is a `planned` feature, not part of the
  current protocol version (`PROTOCOL.md §46`,
  `design/EXTENSIONS.md`).

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
| Network observer | None | None | None | Metadata |
| Application | None | None | Capabilities already granted to it | None |

Notes:

- A compromised Authorization Key affects only the grants that key
  issued. Revoking it does not affect grants issued by other keys
  (`operations/DEPLOYMENT.md §7`).
- A Device Key signs only reachability records. It does not sign grants,
  leases, or identity objects (`PROTOCOL.md §42`).
- `GrantRevocation` is signed by the Identity Root, not by an
  Authorization Key (`PROTOCOL.md §15`, `PROTOCOL.md §42`).

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
`KeyRevocation` for the device key, and the device is removed from the
identity document's `device_bindings`. A verifier denies a peer whose
device has been revoked from `device_bindings`
(`PROTOCOL.md §16`, `PROTOCOL.md §27`, `CONFORMANCE.md §2`,
`operations/DEPLOYMENT.md §7`).

**Identity Root compromise.** The protocol provides no in-band
recovery. Any in-band mechanism would be an authority the protocol
cannot trust. Recovery is external and out of band, and the protocol
defines no recovery authority, no proof-of-ownership criteria, and no
adjudication procedure (`PROTOCOL.md §18`, `design/REJECTED.md` R5).
Threshold recovery is a `planned` feature and is not in the current
protocol version.

**Propagation.** Revocations are pulled, not pushed. The protocol
defines no normative propagation bound (`PROTOCOL.md §14`,
`PROTOCOL.md §31`, `design/REJECTED.md` R15). The recommended polling
interval is `DEFAULT_REVOCATION_POLL_INTERVAL`.

---

## 6. Implementation guidance

The normative requirements for implementations are in
`PROTOCOL.md §43`. This section adds no requirements. It summarizes the
security-relevant items and records further guidance.

Requirements already stated in `PROTOCOL.md §43` that carry the most
security weight:

- Verify every signature and reject non-canonical or malformed
  encodings before semantic processing.
- Apply the verification procedure in `OBJECTS.md §8` atomically
  (`OBJECTS.md §8.1`).
- Fail closed on missing information.
- Never allow wall-clock time to extend authorization validity.
- Never auto-resolve a fork without an explicit `StreamResolution`.
- Never log credentials, grants, or leases, and never transmit private
  keys.

Further guidance, not required by the specification:

- Generate keys and nonces with the operating system's cryptographically
  secure random number generator.
- Keep an audit record of security-relevant events without key material.
- Keep revocation state coherent across caches so that a revoked key is
  not honored from a stale copy.
- Protect the Identity Root offline or in hardware, and keep backups
  apart from running keys (`operations/DEPLOYMENT.md §7`).

---

## 7. Out of scope

The following are not covered by this document. Where a feature is
absent from the current protocol version, its status is stated.

- Relay capacity planning and hardware (see `operations/RELAYS.md`).
- Computational admission cost for infrastructure. Proof-of-work as a
  foundation is rejected (`design/REJECTED.md` R8). Any use as an
  admission policy is a deployment matter.
- A security test program and security roadmap. Test vectors and
  conformance levels are defined in `spec/CONFORMANCE.md`; the
  development plan is in `ROADMAP.md`.
- Recovery-time targets. The protocol defines no recovery time.
