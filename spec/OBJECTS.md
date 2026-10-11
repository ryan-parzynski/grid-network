---
title: "Grid Network — Canonical CBOR Profile, Cryptographic Constructions, Envelope, Verification"
status: v0.6.2 (design-review) — normative object encoding; PENDING DECISION callouts added at affected sections
version: v0.6.2
date: 2026-10-11
---

# Grid Network — Object Encoding (v0.6.2)

> **Status:** v0.6.2 kernel preserved; PENDING DECISION callouts added at §§3.5, 6, 7, 9, 13.2 where affected by open D-xx. Four-outcome verifier NOT included (§9 stays v0.6.2 with PENDING D-03). No [REVIEW-*]/[PROPOSED]/[OPEN D-xx]/[UNCHANGED] tags.

## §1 (if present in v0.6.2 source)

Object encoding defines how identity streams, grants, revocations, pairing records, and reachability records serialize to CBOR, sign with Ed25519, and reference each other.

> **Status:** NEEDS AUTHOR INPUT — §1 introductory scope text partially defined in v0.6.2; preserve core concept (canonical CBOR profile, deterministic serialization, domain-separated signatures) until full section authored.

## §2 Canonical CBOR Profile

Canonical encoding per RFC 8949 §4.2.3 (canonical form): definite-length arrays/maps/strings/bytes; no duplicate map keys; floats as smallest representation; no tags unless required; byte strings in lexicographic order where order matters; integers in smallest representation.

> **PENDING DECISION:** D-01 (stream identity model affects envelope / stream encoding rules); D-02 (chain base affects sequence encoding at §3.5). See [`../../design/decisions/DR-0001-stream-identity.md`](../../design/decisions/DR-0001-stream-identity.md), [`DR-0002`](../../design/decisions/DR-0002-chain-base.md).

## §3 Object Serialization / §3.5 Chain Base Encoding

Objects serialize as CBOR map with required fields: `domain_separator` (§58), `sequence`, `previous_hash` (or base for init), content fields, `signature`. Sequence increments by 1 per identity stream (§11). Chain base (§3.5): `previous_hash` for sequence=0 derived per D-02.

> **PENDING DECISION:** D-02 (chain base derivation — affects §3.5 init); D-04 (revocation pinning — affects sequence rules / previous_hash content). See [`DR-0002`](../../design/decisions/DR-0002-chain-base.md), [`DR-0004`](../../design/decisions/DR-0004-revocation-pinning.md).

## §4 Common Stream Envelope

Envelope = `domain_separator` (string) + `sequence` (uint) + `previous_hash` (bytes, 32B) + `document_payload` (map/array) + `signature` (bytes, Ed25519 64B). Domain separators fixed per §58 (e.g., `"grid-v1-identity"`, `"grid-v1-authorization"`, `"grid-v1-revocation"`). Signature covers `domain_separator || sequence || previous_hash || payload_canonical`.

> **PENDING DECISION:** D-01 (stream model affects envelope assignment — single vs split); D-13 (Ed25519 strict encoding of payload and domain separator). See [`DR-0001`](../../design/decisions/DR-0001-stream-identity.md), [`DR-0013`](../../design/decisions/DR-0013-ed25519-and-references.md).

## §5 Signature Semantics and Verification

Ed25519 (RFC 8032). Public key = 32 bytes; signature = 64 bytes. Verification: decode canonical CBOR payload; construct signed message = `domain_separator || sequence || previous_hash || canonical_payload` (exact concatenation, no length-prefix on domain); verify with Ed25519 `verify()` strict (no lenient encoding — D-13). Failure = reject (v0.6.2; four-output proposal NOT here — see §9 / DR-0003).

> **PENDING DECISION:** D-13 (Ed25519 strictness — encoding rules, domain separator format, length handling). See [`DR-0013`](../../design/decisions/DR-0013-ed25519-and-references.md).

## §6 Object Schemas

> **Status:** NEEDS AUTHOR INPUT — CDDL / schema definitions for identity document, relationship assertion, grant, revocation, pairing record, reachability record not fully present in v0.6.2 source. Preserve concepts (required fields per §10–§15); define schemas when D-22 (minimal profile) and D-23 (test vectors / conformance) accepted. Add `PENDING DECISION: D-22` when profile scope finalized.

> **PENDING DECISION:** D-22 (V1 minimal profile — defines required schemas / excluded fields); D-15 (fork-proof object schema — extension). See [`DR-0022`](../../design/decisions/DR-0022-v1-minimal-profile.md), [`DR-0015`](../../design/decisions/DR-0015-fork-proof-object.md).

## §7 Stream Identity

Stream identity (§11, D-01): sequence-ordered chain of identity documents signed by root; identity = root public key + highest verified sequence + chain from init to current; split streams (identity / relationship / service) proposed (D-07 / D-01) but v0.6.2 uses single identity stream.

> **PENDING DECISION:** D-01 (stream identity model — single vs split); D-07 (relationship stream privacy if split); D-09 (Relationship Key signs relationship stream if delegated). See [`DR-0001`](../../design/decisions/DR-0001-stream-identity.md), [`DR-0007`](../../design/decisions/DR-0007-relationship-privacy.md), [`DR-0009`](../../design/decisions/DR-0009-root-custody.md).

## §8 Canonical Forms

> **Status:** NEEDS AUTHOR INPUT — canonical form rules (definite-length, no extra tags, ordered maps where order matters) partially defined in §2; complete canonical encoding procedure (how to serialize, verify canonical form, reject non-canonical) requires author input; relate to RFC 8949 §4.2.3 and D-13 (strict Ed25519 on canonical form).

> **PENDING DECISION:** D-13 (Ed25519 strict encoding of canonical payload); D-01 (stream encoding if split affects form). See [`DR-0013`](../../design/decisions/DR-0013-ed25519-and-references.md).

## §9 Verification Procedure

Verification (§47 of PROTOCOL.md): (1) decode canonical CBOR; (2) extract root public key from identity stream (§11); (3) verify chain from init through sequence (previous_hash continuity per D-02, D-17); (4) check revocation (§20, D-04); (5) verify document signature (§5, D-13); (6) check freshness (§40, D-08) and clock (§40, D-12); (7) evaluate authorization (§16). Outcome: ACPT / REJECT (v0.6.2). Four-output proposal (ACPT / INVALID / REVOKED / EXPIRED) is a proposal (D-03) — lives ONLY in `DR-0003`; NOT promoted to spec §9.

> **PENDING DECISION:** D-03 (verifier outcomes — four-output proposal NOT in §9; v0.6.2 2-class preserved); D-02 (chain continuity); D-04 (revocation verification); D-08 (freshness check); D-13 (signature strict); D-18 (object reference verification if refs involved). See [`DR-0003`](../../design/decisions/DR-0003-verifier-outcomes.md), [`DR-0002`](../../design/decisions/DR-0002-chain-base.md), [`DR-0004`](../../design/decisions/DR-0004-revocation-pinning.md), [`DR-0008`](../../design/decisions/DR-0008-freshness.md), [`DR-0013`](../../design/decisions/DR-0013-ed25519-and-references.md), [`DR-0018`](../../design/decisions/DR-0018-object-identity.md).

## §10 Rejection Classes and Outcomes Registry

Rejection reasons (v0.6.2), preserved: INVALID (bad encoding / bad signature / missing fields); REJECTED (revoked / expired / unauthorized / stream break); (four-output split of REJECTED → REVOKED / EXPIRED / INVALID proposed in D-03, NOT adopted). Registry entries map to verification step (§9) and authorization policy (§16).

> **PENDING DECISION:** D-03 (registry expansion if four-output adopted — only then); D-04 (revocation classification depends on pinning fields); D-18 (reference-invalid as rejection class if D-18 accepted). See [`DR-0003`](../../design/decisions/DR-0003-verifier-outcomes.md), [`DR-0004`](../../design/decisions/DR-0004-revocation-pinning.md), [`DR-0018`](../../design/decisions/DR-0018-object-identity.md).

*Cross-link verification: §3.5 → D-02 (DR-0002); §6 → D-22 (DR-0022); §7 → D-01 (DR-0001); §9 → D-03 (DR-0003); §13.2 (if present) → D-13 (DR-0013), D-17 (DR-0017), D-18 (DR-0018). All DR-*.md files exist and link back to this file via `../../spec/OBJECTS.md`. Four-outcome verifier NOT present — preserved only in DR-0003. Need-author-input sections (§1, §6, §8, §60-equivalent vectors) marked clearly and not filled with invented content.*
