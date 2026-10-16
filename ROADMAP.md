# Grid Network — Roadmap

**Revision:** 2.4
**Protocol version:** v0.6.3

**Repository path:** `ROADMAP.md`

This document is non-normative. It describes what work is planned,
what is deferred, and what is unscheduled. Where this document and the
Protocol Specification conflict, the Protocol Specification governs.

---

## 1. Status

The specification is in a documentation and design phase. No reference
implementation is available. No test vectors have been published. The
protocol version is v0.6.3. Four open questions remain (see §5).

---

## 2. Milestones

Milestones are ordered. Each states its completion criterion. The word
"Phase" is reserved for the three stages of the pairing flow and is not
used for roadmap planning.

### M0 — Specification complete

**Deliverables.** All object schemas defined. All stream rules defined.
All conformance levels defined. Every `under-review` marker either
resolved or explicitly accepted.

**Completion.** No section carries `under-review` unless its defect has
been recorded as an open question with a decision.

**Current state.** In progress. Object schemas exist for
`IdentityDocument`, `RelationshipAssertion`, `Grant`, `Lease`,
`ReachabilityRecord`, `ServiceRecord`, `RelayTicket`. Schemas for
`RendezvousManifest`, `OperatorManifest`, `KeyRevocation`,
`RelationshipTermination`, `IdentityContinuity`, `StreamResolution`,
`GrantRevocation`, `LeaseRevocation`, `RelayNodeRecord`, and
`CreditReceipt` are stubs.

### M1 — Test vector suite published

**Deliverables.** Levels 1 through 3 of `spec/CONFORMANCE.md` populated
with byte-exact vectors. Negative vectors at least three per positive.

**Completion.** Every object type has at least one positive vector and
three negative vectors. The vectors validate against the canonical
constructions in `OBJECTS.md`.

### M2 — Reference implementation

**Deliverables.** A single-language implementation that passes every
test vector and every conformance scenario.

**Completion.** The implementation passes `spec/CONFORMANCE.md` Levels
1 through 6.

### M3 — Independent implementation

**Deliverables.** A second implementation in a different language or by
a different author, passing the same vectors.

**Completion.** Two implementations produce identical bytes for
identical inputs, and disagree on nothing in the conformance suite.

### M4 — Local connectivity

**Deliverables.** LAN discovery. Local relay. Device pairing UI.
Cross-platform agent.

**Completion.** A user can reach a device on the same LAN without
external infrastructure.

### M5 — Remote reachability

**Deliverables.** NAT traversal with candidate exchange and hole
punching. Fallback ordering per `operations/DEPLOYMENT.md §3`.

**Completion.** `TARGET_DIRECT_CONNECTION_RATE` deployments achieve a
direct connection without relay. `TARGET_CONNECTION_SUCCESS_RATE`
attempts succeed on first try.

### M6 — Rendezvous resilience

**Deliverables.** Multiple rendezvous providers. Recovery manifests.
Peer detection of server failure and republish.

**Completion.** A peer can switch providers without any observable
change to identity, relationships, or grants.

### M7 — Relay fallback in production

**Deliverables.** Relay tickets. Bandwidth quotas. Priority classes.
Relay selection with failover.

**Completion.** Relay fallback operates in a real deployment with
quota enforcement and priority queuing.

### M8 — Mobile integration

**Deliverables.** iOS and Android agents. Background execution. Mobile
UI for pairing and management.

**Completion.** `TARGET_MOBILE_BATTERY_USE` met or better. A user can
manage the network from a phone.

### M9 and beyond — Advanced features

Multi-hop relay, multipath connectivity, privacy transport, threshold
recovery. Each is described in `design/EXTENSIONS.md`.

---

## 3. Release targets

The mapping of features to protocol versions is indicative. It is not a
commitment.

| Protocol version | Feature set |
|---|---|
| v0.6.3 | Current. Identity, authorization, reachability, rendezvous, relays, pairing. |
| v0.7.0 | Object schemas completed, test vectors published, clarifications. |
| v0.8.0 | Multipath connectivity, metadata minimization. |
| v0.9.0 | Rendezvous federation, gossip, DHT discovery. |
| v1.0.0 | Stabilization. Long-term support begins. |

Features that are `deferred` or `unscheduled` are not assigned to a
version.

---

## 4. Specification work queue

The following are not yet written. Each is a specification task, not a
protocol feature.

| Task | Target | Status |
|---|---|---|
| Object schemas for the ten stubbed types | `spec/OBJECTS.md §7` | Not started |
| Test vector format and first vectors | `spec/CONFORMANCE.md` | Not started |
| Conformance scenarios fully specified | `spec/CONFORMANCE.md` | Drafted, not finalized |
| Rendezvous wire protocol | `spec/OBJECTS.md` | Not started |
| NAT traversal wire specification | `operations/DEPLOYMENT.md` | Drafted, not normative |
| Credit settlement protocol | `commercial/MODEL.md` | Not started |
| Prior-art expansion for libp2p, Noise, QUIC | `design/LINEAGE.md` | Not started |

---

## 5. Open questions

These are unresolved. Each requires a decision before the specification
can be marked complete.

**Q1. Revocation effect on active sessions.** When a grant is revoked
while a session is active, does the session terminate immediately, or
does it continue until the next authorization check?

**Q2. Lease renewal under concurrent attempts.** When both issuer and
subject attempt to renew a lease simultaneously, how are the two leases
reconciled?

**Q3. Relationship decay policy.** Is idle relationship state pruned
after a defined period? If yes, what is the default period, and how is
the user warned?

**Q4. Revocation propagation bound.** Does the protocol define a
normative poll interval for revocations, or is propagation unbounded?

Each question is tracked in `design/DECISIONS.md` under "Open
decisions."

---

## 6. Known limitations

These are design limits, not defects. They are stated so that reviewers
see what the protocol does not solve.

| Limitation | Why it exists | Mitigation |
|---|---|---|
| Two peers that have not communicated in years may not reach each other without out-of-band contact | The protocol has no state distribution mechanism that works when peers are disconnected for long periods | Rendezvous serves identity state; peers refresh when they can |
| A peer that loses all keys and all infrastructure is unreachable | No in-band recovery for Identity Root compromise | Out-of-band coordination |
| A peer that changes its identity cannot be found under its old identity | Identity is bound to a Peer ID | Re-pairing under the new identity |
| A fork whose signing keys are lost is unrecoverable | StreamResolution requires the pre-fork authority | None. Design limit. |
| Revocation propagation is not immediate | Revocations are pull-based | Short leases; `DEFAULT_REVOCATION_POLL_INTERVAL` |
| Metadata is visible to infrastructure operators | Peers are identified by design | Multiple providers; privacy transport is `planned` |
| Post-quantum security is not yet provided | Ed25519 is the current signature algorithm | Post-quantum suite is `planned` |

---

## 7. Deferred and unscheduled features

See `design/EXTENSIONS.md` for design sketches. Status words are defined
in `spec/VERSIONING.md`.

| Feature | Status |
|---|---|
| Multipath connectivity | planned |
| Metadata minimization | planned |
| Chain-extension proofs | planned |
| Service ownership transfer | planned |
| Rendezvous federation | planned |
| Rendezvous gossip | planned |
| DHT-based discovery | planned |
| Post-quantum signature suite | planned |
| Threshold recovery | planned |
| Hardware-backed root keys | unscheduled |
| Delegated authorization trees | unscheduled |
| Anonymity transport | unscheduled |

---

## 8. Administrative tasks

Not protocol work, but required before the repository is complete.

| Task | Notes |
|---|---|
| LICENSE.md | The original repository used GPL v3. Confirm or replace. |
| CONTRIBUTING.md | Describes how to propose changes. |
| CODE_OF_CONDUCT.md | Community standards. |
| Test vector repository | `spec/test-vectors/` structure. |
| Example integrations | `apps/` directory. |