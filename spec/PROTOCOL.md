---
title: "Grid Network Protocol Specification"
status: DESIGN-REVIEW v0.6.2 — NOT IMPLEMENTATION-READY. NOT FROZEN.
version: v0.6.2 (design-review)
date: 2026-10-11
pending_decisions: see ../../design/DECISIONS.md (26 open; D-01..D-13 block V1)
---

# Grid Network Protocol Specification

> **Status:** DESIGN-REVIEW. NOT IMPLEMENTATION-READY. NOT FROZEN. Version v0.6.2 (kernel preserved from consolidated source); design-review edits (PENDING DECISION callouts, no promotion of PROPOSED items) applied 2026-10-11.
> **Pending decisions:** Twenty-six decisions remain open (D-01..D-26, see [`../../design/DECISIONS.md`](../../design/DECISIONS.md)). Until ACCEPTED, affected sections are marked PENDING DECISION below; current text reflects v0.6.2 and may change.

---

## §1 Abstract / §2 Core Security Invariant / §3 Design Goals / §4 Non-Goals

**Abstract.** Grid Network is an identity-, authorization-, and reachability-centric peer protocol using cryptographic identity roots, sequence-ordered identity histories, relationship-scoped assertions, signed grants/leases/capabilities, key revocation with pinning (pending D-04), pairing via PAKE (D-06), and rendezvous/reachability/relay layers. It requires no central authority; authorization is local; identity is a keypair.

**§2 Core Security Invariant.** A peer accepts an authorization statement only when: (a) the identity stream from root through sequence verifies against the root public key with strict Ed25519 (§58, D-13); (b) the authorization record is signed by an authorized key role (§9); (c) no revocation of the signing key or authorization exists at or before the record's sequence (§18–§20, D-04); (d) the peer's local verification state (§47) accepts the stream; and (e) freshness (§40, D-08) and clock/reboot (§40, D-12) conditions are met.

> **PENDING DECISION:** D-01 (stream identity model), D-02 (chain base derivation), D-03 (verifier outcomes/classification — four-outcome proposal NOT promoted; §14 stays v0.6.2 with PENDING D-03), D-04 (revocation pinning / fields), D-13 (Ed25519 strictness / domain separators). See [`../../design/decisions/DR-0001-stream-identity.md`](../../design/decisions/DR-0001-stream-identity.md), [`DR-0002`](../../design/decisions/DR-0002-chain-base.md), [`DR-0003`](../../design/decisions/DR-0003-verifier-outcomes.md), [`DR-0004`](../../design/decisions/DR-0004-revocation-pinning.md), [`DR-0013`](../../design/decisions/DR-0013-ed25519-and-references.md).

**§3 Design Goals.** (1) No central authority — identity = keypair; (2) Local authorization — grants/leases evaluated at peer; (3) Stream-verifiable history — each identity history ordered, pinned, verifiable; (4) Revocation with pinning — revoked keys cannot be replayed; (5) Pairing via PAKE — human-coordinated; (6) Reachability without exposure — rendezvous, relay, reachability records; (7) Offline operation — peers verify from local stream state.

**§4 Non-Goals.** (1) Global naming / DNS replacement (though rendezvous may use domain labels); (2) Application-layer protocol definition (application integration deferred, §55); (3) Multi-device synchronization (V1.1 / extension); (4) Commercial relay economics (extension, D-24); (5) Licensing commitment (D-25 deferred); (6) Implementation-language mandate (D-26 non-normative).

---

## §5 Architecture / §6 Peer Principal / §7 Peer ID / §8 Identity Root / §9 Key Roles / §10 Identity Documents / §11 Identity History / §12 Relationships / §13 Grants / §14 Leases / §15 Capabilities / §16 Authorization Policy / §17 Network vs Application Authorization

**§5 Architecture.** Peer (= identity root + key roles + stream) communicates over transport (§34) via rendezvous (§30–§31) and relay (§33) to reach other peers (§32); authorization (§16–§17) evaluated locally using stream (§11) and revocation (§18–§20) state.

**§6 Peer Principal.** A peer is identified by an Identity Root public key; all authorization derives from that root or from delegated key roles (§9). No account, no central registry.

> **PENDING DECISION:** D-09 (Identity Root custody / Relationship Key delegation). See [`../../design/decisions/DR-0009-root-custody.md`](../../design/decisions/DR-0009-root-custody.md).

**§7 Peer ID.** Peer identifier derived from root public key (format depends on D-01/D-22 profile). See design review for proposed identifier format; v0.6.2 preserved.

> **PENDING DECISION:** D-01 (stream identity model — affects identifier scope / stream assignment), D-22 (V1 minimal profile — defines required identifier forms). See [`DR-0001`](../../design/decisions/DR-0001-stream-identity.md), [`DR-0022`](../../design/decisions/DR-0022-v1-minimal-profile.md).

**§8 Identity Root.** The root keypair defines the identity; root signs identity documents (§10), history (§11), grants (§13), revocations (§18–§20), and termination (§5, D-05). Root custody: offline / hardware-backed recommended (D-09 Option A); delegation to Relationship Key (D-09 / D-07) proposed.

> **PENDING DECISION:** D-01, D-05 (continuity/termination), D-09 (custody/delegation), D-07 (relationship stream if delegated).

**§9 Key Roles.** (v0.6.2 table, preserved; PENDING D-09 / D-07 updates marked.) Identity Root (all); Relationship Key (proposed, D-09 — assertions/terminations V1 if accepted); Service Key (V1.1, proposed); Recovery Key (removed from V1, proposed); Relay Authority / Relay Node Keys (extension, proposed). See [`../../design/decisions/DR-0009-root-custody.md`](../../design/decisions/DR-0009-root-custody.md).

> **PENDING DECISION:** D-09 (Relationship Key role definition); D-07 (per-relationship stream if D-09 accepted); D-24 (relay keys — extension).

**§10 Identity Documents.** Documents signed by root or delegated role: identity declaration, device binding, key-authorization, relationship assertion/termination (if D-07), service record. Each document includes sequence, previous_hash reference, domain_separator (§58), timestamp / freshness (§40).

> **PENDING DECISION:** D-04 (revocation fields / pinning affects document validity); D-13 (Ed25519 strict encoding of signatures); D-18 (object reference stability of document references).

**§11 Identity History.** Sequence-ordered chain of identity documents; each entry includes sequence number, previous_hash, document content hash, root signature. Chain base (§11 init) derives from root + initial state (D-02); pinning of revocation (D-04) uses previous_hash + root_sequence.

> **PENDING DECISION:** D-02 (chain base derivation — affects init); D-04 (revocation pinning — affects sequence rules); D-19 (history checkpoints — interval/format); D-01 (stream identity model — single vs split stream).

**§12 Relationships.** Pairing (§24–§29) produces relationship_id; relationship assertions and terminations (if D-07 Option A) in per-relationship stream; match on relationship_id; termination requires both-party agreement or signed record (D-05).

> **PENDING DECISION:** D-06 (PAKE choice / pairing contract — affects relationship_id derivation); D-07 (stream privacy); D-05 (termination record); D-09 (Relationship Key signs assertions if delegated).

**§13 Grants / §14 Leases / §15 Capabilities / §16 Authorization Policy / §17 Network vs Application Authorization / §18 Revocation / §19 Revocation Hierarchy / §20 KeyRevocation / §21 Auth-Key Compromise / §22 Root Compromise / §23 Key Rotation**

**§13 Grants.** Signed authorization to a peer; includes resource, scope, expiration (lease §14) or permanent; revocable (§18). Constraint maps bounded (§13.6, proposed limits — D-11; values proposed, not normative until validated).

> **PENDING DECISION:** D-11 (resource limits — §13.6 table); D-04 (revocation affects grant validity); D-13 (signature strictness on grant).

**§14 Leases.** Time-bounded authorization (§14); expiration checked locally; revocation (§18) takes precedence over lease expiry if revoked at or before lease sequence.

> **Status:** v0.6.2 lease procedure preserved (sequence-based expiration; revocation takes precedence). Resolution of sequence-vs-clock semantics deferred to D-08 / D-12. §14 does NOT include the four-outcome verifier proposal; proposal stays in DR-0003. PENDING D-03 callout preserved.

> **PENDING DECISION:** D-03 (verifier outcomes — four-output proposal NOT promoted; §14 stays v0.6.2); D-08 (freshness — affects lease time evaluation); D-12 (reboot — affects clock continuity for lease expiry). See [`../../design/decisions/DR-0003-verifier-outcomes.md`](../../design/decisions/DR-0003-verifier-outcomes.md) — proposal lives ONLY here.

**§15 Capabilities.** Capability = authorization record + resource + scope; signed by granting key; verified against identity stream (§11) and revocation (§18). Capability does not grant new authority — only delegates existing.

**§16 Authorization Policy.** Local evaluation: grant + capability + identity stream + revocation + resource constraints (§13.6). A peer MUST NOT grant authorization solely on a revoked-state record (proposed tightening of v0.6.2 (§16); clarification proposed, not promoted — preserved in review, spec unchanged).

> **PENDING DECISION:** D-11 (constraint maps); D-04 (revocation pinning affects policy).

**§17 Network vs Application Authorization.** Network authorization = reachability / relay / transport (§34); application authorization = service-level grants (§13–§15) evaluated locally by application. Protocol defines network layer; application integration (§55) deferred.

**§18 Revocation / §19 Revocation Hierarchy / §20 KeyRevocation**

**§18 Revocation.** A key can be revoked by the root (or delegated role, D-09); revocation applies at sequence ≥ revoked_at_sequence; revocation propagates (§39). Revocation of authorization means grant/capability signed by revoked key is no longer valid.

> **PENDING DECISION:** D-04 (revocation pinning / fields / effective_sequence=0); D-09 (delegated revocation by Relationship Key); D-10 (local API revocation reference / availability).

**§19 Revocation Hierarchy.** Root revocation > key-role revocation > authorization revocation; hierarchy verified by stream (§11) and key roles (§9). A revocation signed by a lower role does not revoke a higher role.

> **PENDING DECISION:** D-09 (key-role delegation defines hierarchy); D-04 (pinning ensures ordered verification of hierarchy).

**§20 KeyRevocation.** Record included in identity stream (§11); fields (proposed D-04): revocation_type, revoked_key, revoked_at_sequence, pinned_previous_hash, pinned_root_sequence, revocation_signature; special case effective_sequence=0 needs resolution (conflicts with pinning); v0.6.2 text preserved with PENDING D-04. See design review C4 for proposal source.

> **PENDING DECISION:** D-04 (full record definition / effective_sequence=0 resolution / pinning rules). See [`../../design/decisions/DR-0004-revocation-pinning.md`](../../design/decisions/DR-0004-revocation-pinning.md).

**§21 Auth-Key Compromise / §22 Root Compromise / §23 Key Rotation**

**§21 Auth-Key Compromise.** Compromise of an authorization key (not root) = revoke key (§20) + issue new authorization signed by root or remaining valid key; peers verify stream (§11) to detect compromise.

**§22 Root Compromise.** Root compromise = identity termination (§5, D-05) or recovery (out-of-band, not V1; D-09 offline/hardware reduces risk). No in-band V1 recovery — v0.6.2 preserved.

> **PENDING DECISION:** D-05 (termination / continuity); D-09 (offline / hardware custody); D-01 (stream identity affects recovery reference).

**§23 Key Rotation.** Root rotates by new root declaration (signed by old root + new root public key) + sequence continuation; rotation record in stream (§11); peers update root reference. Rotation does not break identity — identity = root sequence + history.

> **PENDING DECISION:** D-01 (stream model affects rotation reference); D-02 (chain base affects rotation init if new root starts new chain — or continues).

---

## §24–§29 Pairing / §30 Rendezvous / §31 Rendezvous Evolution / §32 Reachability / §33 Relays / §34 Transport / §35 Enforcement / §36 Service Discovery / §37 Offline Operation / §38 Lease Expiry / §39 Revocation Propagation / §40 Time Semantics / §41–§44 Object Encoding / §45 Sequence and History / §46 Trust Anchors / §47 Verifier Local State / §48 Security State Machines / §49 Authority Domains / §50 Threat Model / §51 Compromise Model / §52 Service Identity / §53 Failure Semantics / §54 Reconciliation / §55 Application Integration / §56 V1 Scope / §57 Deferred Features / §58 Signing-Authority Matrix / §59 Implementation Requirements / §60 Test Vectors / §61 Conformance Scenarios / §62 Future Extensions / §63 Project Structure / §64 Versioning / §65 Triage

**§24–§29 Pairing.** Human-coordinated (QR / short code) → PAKE (D-06) → pairing output contract (both root pubkeys / device IDs / session secret derivation label / transcript) → relationship_id derivation (depends on D-06 transcript). Minimum pairing contract independent of SPAKE2 vs CPace (design review C2 proposed; v0.6.2 preserved).

> **PENDING DECISION:** D-06 (PAKE / contract). Pairing proposal from design review (see `../../design/REVIEW-2026-10-11.md`).

**§30 Rendezvous / §31 Rendezvous Evolution.** HTTPS V1 (unchanged v0.6.2); publication of reachability records (§32); ingestion rules (M4 proposed — preserved in review): accept supported records, reject unknown formats (log, not fail); evolution deferred.

> **PENDING DECISION:** D-21 (transport binding — HTTPS V1 preserved; wire deferred); D-07 (relationship stream privacy affects what is published to rendezvous — H1).

**§32 Reachability / §33 Relays / §34 Transport.** ReachabilityRecord (domain_separator, sequence, endpoint, expiration); relays (operator/coordinator model — extension, D-24); transport (HTTPS V1; other deferred).

> **PENDING DECISION:** D-20 (multi-store / replication); D-21 (transport); D-24 (relay economy / scope); D-11 (resource limits affect relay load).

**§35 Enforcement / §36 Service Discovery / §37 Offline Operation / §38 Lease Expiry / §39 Revocation Propagation / §40 Time Semantics.** Local enforcement (§35); service discovery via rendezvous (§36); offline = verify from local stream (§37); lease expiry (§38) — see §14 NEEDS AUTHOR INPUT; revocation propagation (§39) — local + rendezvous; time (§40) — see D-08 / D-12.

> **Status:** v0.6.2 lease-expiry reference (§38) preserved; sequence-vs-clock evaluation deferred to D-08 / D-12 (see §14).

> **PENDING DECISION:** D-08 (freshness); D-12 (reboot/clock); D-04 (revocation propagation depends on pinning); D-10 (local API revocation reference).

**§41–§44 Object Encoding / §45 Sequence and History / §46 Trust Anchors / §47 Verifier Local State / §48 Security State Machines / §49 Authority Domains**

**§41–§44 Object Encoding.** Canonical CBOR profile (§41); object serialization (§42); common stream envelope (§43); reference rules (§44 — D-18; see also §13.2, PENDING D-13/D-17/D-18). See [`../../spec/OBJECTS.md`](../../spec/OBJECTS.md) §2–§5.

> **PENDING DECISION:** D-01 (stream identity affects envelope); D-02 (chain base affects sequence encoding); D-13 (Ed25519 strict encoding); D-18 (reference stability).

**§45 Sequence and History.** Sequence = ordered integer per stream (§11); history = chain of documents from root through current sequence; previous_hash links sequence n to n-1; chain initialization (§11) uses D-02 base; checkpoints (§19, D-19) at intervals.

> **PENDING DECISION:** D-02, D-19 (checkpoints), D-17 (previous_hash redundancy — kept; PENDING at §13.2).

**§46 Trust Anchors.** Root public key = trust anchor; no external CA; root can be updated by signed rotation (§23); anchors verified by peer's local state (§47).

**§47 Verifier Local State.** Each peer maintains: identity streams (§11) it trusts; revocation state (§18–§20, D-04); authorization records (§13–§15); freshness (§40, D-08); clock/reboot (§40, D-12). Verification (§47) produces accept / reject (v0.6.2 three-class); four-output proposal (D-03) lives ONLY in `DR-0003` — NOT promoted.

> **PENDING DECISION:** D-03 — four-outcome proposal explicitly NOT in this section. §14 (leases/verification) and §47 (verifier) remain v0.6.2. See [`../../design/decisions/DR-0003-verifier-outcomes.md`](../../design/decisions/DR-0003-verifier-outcomes.md).

> **PENDING DECISION:** D-13 (Ed25519 strict verification rules); D-03 (outcome classification — proposal only); D-10 (local API reference state).

**§48 Security State Machines / §49 Authority Domains / §50 Threat Model / §51 Compromise Model / §52 Service Identity / §53 Failure Semantics / §54 Reconciliation / §55 Application Integration**

**§48 Security State Machines.** States: UNVERIFIED → VERIFYING → ACCEPTED / REJECTED; transitions on stream update, revocation, clock change, root rotation. Failure = REJECTED (safe denial); not ACCEPTED by default.

**§49 Authority Domains.** Authorization bounded by root / key-role scope; a grant from root A does not apply to identity root B; cross-root references only via explicit delegation (not V1).

**§50 Threat Model / §51 Compromise Model** (preserved from v0.6.2 — entries include: malicious rendezvous (§33); malicious relay (§33); root compromise (§22); key compromise (§21); replay (§18, D-04); inference (§7, D-07); DoS (§11 resource limits, D-11); man-in-the-middle pairing (§24–§29, D-06)).

> **PENDING DECISION:** D-04 (replay prevented by pinning); D-07 (inference prevented by stream privacy); D-11 (DoS bounded by limits); D-06 (MITM prevented by PAKE).

**§52 Service Identity / §53 Failure Semantics / §54 Reconciliation / §55 Application Integration**

**§52 Service Identity.** Service = peer + service record (§10); service auth via Service Key (§9, D-09/V1.1) or root; service identity does not create new authority.

**§53 Failure Semantics.** Failure = authorization denied (safe); failure does not grant access; failure events logged locally; no remote failure notification required (privacy, §7).

**§54 Reconciliation.** Peers reconcile streams (§11) by comparing highest sequence + previous_hash; conflicts resolved by sequence + root signature; checkpoints (§19, D-19) speed reconciliation.

> **PENDING DECISION:** D-19 (checkpoint format); D-01 (stream split affects reconciliation); D-20 (multi-store replication conflicts).

**§55 Application Integration.** Protocol defines authorization / reachability; application defines resource / action; integration via capability (§15) and local authorization (§16–§17). Deferred to v1.1 / extension; needs application-specific profile (not normative here).

> **Status:** NEEDS AUTHOR INPUT — §55 application-integration profile requires design of capability-to-application-resource mapping (not in v0.6.2 source). Preserve until application-layer profile completed.

**§56 V1 Scope / §57 Deferred Features / §58 Signing-Authority Matrix / §59 Implementation Requirements / §60 Test Vectors / §61 Conformance Scenarios / §62 Future Extensions / §63 Project Structure / §64 Versioning / §65 Triage**

**§56 V1 Scope.** Identity + authorization + reachability + pairing + rendezvous + revocation + stream verification; excludes: multi-device sync, application-layer relay economics (D-24), licensing (D-25), non-HTTPS transport (D-21), multi-store replication (D-20), recovery key (removed). See [`../../design/decisions/DR-0022-v1-minimal-profile.md`](../../design/decisions/DR-0022-v1-minimal-profile.md).

> **PENDING DECISION:** D-22 (profile definition); D-01–D-13 (blocking V1); D-23 (vectors).

**§57 Deferred Features.** Recovery Key (removed from V1); relay operator economics (EXT); multi-store (EXT); non-HTTPS transport (EXT); application integration profile (v1.1); licensing (D-25); language mandate (D-26 non-normative).

**§58 Signing-Authority Matrix.** Root signs identity docs + history + grants + revocations + rotation; Relationship Key (if D-09) signs assertions/terminations; Service Key signs service records; Authorization Key (delegated) signs grants; each with domain separator (§58). Signature = Ed25519 (strict, D-13); domain = context string (e.g., "grid-v1-identity").

> **PENDING DECISION:** D-13 (Ed25519 strict encoding / domain separators); D-09 (key roles / delegation); D-04 (revocation signature fields).

**§59 Implementation Requirements.** Must implement §58 (strict Ed25519), §11 (stream verification), §18–§20 (revocation), §24–§29 (pairing contract, D-06), §30–§31 (rendezvous V1). Vectors (§60) required for conformance (§61). CI gates: CDDL validation, vector diff, cross-reference checker, fuzz smoke (see `CONTRIBUTING.md`).

> **PENDING DECISION:** D-23 (test vectors / conformance); D-06 (PAKE interop); D-13 (encoding interop).

**§60 Test Vectors / §61 Conformance Scenarios / §62 Future Extensions / §63 Project Structure / §64 Versioning / §65 Triage**

**§60 Test Vectors.** Canonical CBOR + hex outputs for: identity document (§10), stream segment (§11), revocation (§20, D-04 fields), pairing record (§29), authorization (§13), reachability (§32). Generated from reference implementation; regenerated on spec change; diff checked in CI.

> **Status:** v0.6.2 test-vector procedure preserved (§60); canonical CBOR + hex outputs defined for identity/stream/revocation/pairing/auth/reachability; regeneration diff + CDDL finalized at v0.7.0 per D-23. Reference values require running implementation (see DR-0023).

> **PENDING DECISION:** D-23 (vector format / regeneration rules / diff gate).

**§61 Conformance Scenarios.** Scenarios cover: identity creation (§8); stream verification (§11); revocation (§20); pairing (§24); authorization (§16); reachability (§32); failure (§53); reconciliation (§54). Each scenario = input + expected verification outcome (accept/reject per v0.6.2; four-output proposal only in DR-0003).

**§62 Future Extensions.** Multi-store (D-20), relay economics (D-24), non-HTTPS transport (D-21), application profile (§55), recovery mechanism (out-of-band, not V1), licensing resolution (D-25).

**§63 Project Structure / §64 Versioning / §65 Triage**

**§63 Project Structure.** Source docs: `spec/` (PROTOCOL.md, OBJECTS.md, CHANGELOG.md), `design/` (REVIEW-2026-10-11.md, DECISIONS.md, decisions/DR-*.md, TEMPLATE.md, INDEX.md), `README.md`, `CONTRIBUTING.md`, `VERSIONING.md`. See `README.md` repository map.

**§64 Versioning.** Protocol SemVer (MAJOR/MINOR/PATCH); document per-file; accepted-decision mechanism (`design/DECISIONS.md` → `DR-*.md` ACCEPTED → spec update → CHANGELOG → version bump). See [`VERSIONING.md`](../../VERSIONING.md). v0.7.0 = D-01..D-13 accepted; v0.8.0 = D-01..D-26 + CDDL + vectors.

**§65 Triage.** Open contradictions (C1–C6) → D-01..D-06; holes (H1–H7) → D-07..D-10; modifications (M1–M5) → D-07..D-04/D-22; limitations (L1–L3) → D-22/D-25. All mapped in `design/REVIEW-2026-10-11.md` index and `design/DECISIONS.md`.

---

## Change log (spec-level, from design-review baseline)

- **v0.6.2 (2026-10-11)**: Design-review baseline. Kernel (§1–§65) preserved from consolidated source. No proposal/review/unchanged/open-decision tags embedded in normative text (rule 3, 4). PENDING DECISION callouts added at affected sections (§5–§9, §12, §13, §14, §18–§20, §24, §30–§31, §40, §41–§47, §56, §60). Four-outcome verifier (§14, §47) NOT promoted — proposal stays in `DR-0003`; v0.6.2 three-class preserved. Sections with NEEDS AUTHOR INPUT marked (§14 lease expiry, §6 object schema, §55 integration, §60 vectors, §13.2 Ed25519 refs if present). Cross-references verified (D-01..D-26 → DR-0001..DR-0026 exist and resolve).
- **v0.7.0 (placeholder)**: To be written when decisions D-01 through D-13 are ACCEPTED; will include updated §8–§11 (stream), §18–§20 (revocation pinning), §24–§29 (PAKE contract), §9 (key roles / D-09), §12 (privacy / D-07), §40 (freshness / D-08), §13.6 (limits / D-11), §47 (§14 verification updated if D-03 accepted), §56 (profile / D-22).

See [`../../design/CHANGELOG.md`](../../spec/CHANGELOG.md) for full entries.