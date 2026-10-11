---
title: "Grid Network — Open Design Decisions"
status: All decisions PROPOSED. None ACCEPTED as of 2026-10-11.
version: 2026-10-11
---

# Grid Network — Open Design Decisions

Twenty-six decisions (D-01..D-26) remain open. None is ACCEPTED. To accept: change status to ACCEPTED in the corresponding `design/decisions/DR-00xx-*.md`; update `spec/PROTOCOL.md` / `spec/OBJECTS.md` (remove PENDING DECISION callout / promote section); update `spec/CHANGELOG.md`; merge in one PR.

| D-xx | Title | Severity | Blocks | Linked finding | Status | Rec. summary | Link |
|---|---|---|---|---|---|---|---|
| D-01 | Stream identity model | High | V1 | C5 | PROPOSED | Option A: single identity stream per root | [DR-0001](decisions/DR-0001-stream-identity.md) |
| D-02 | Chain base derivation | High | V1 | C4 | PROPOSED | Derive from previous_hash + root + sequence | [DR-0002](decisions/DR-0002-chain-base.md) |
| D-03 | Verifier outcomes & classification | High | V1 | C3 | PROPOSED | Four-outcome proposal (NOT in spec); v0.6.2 3-class kept | [DR-0003](decisions/DR-0003-verifier-outcomes.md) |
| D-04 | KeyRevocation history pinning | High | V1 | C1/C4 | PROPOSED | Pin to sequence + previous_hash; add fields | [DR-0004](decisions/DR-0004-revocation-pinning.md) |
| D-05 | Identity continuity termination | High | V1 | C5 | PROPOSED | Termination requires signed record + root | [DR-0005](decisions/DR-0005-identity-continuity.md) |
| D-06 | PAKE algorithm and transcript | High | V1 | C2/C6 | PROPOSED | SPAKE2 vs CPace; define contract independent | [DR-0006](decisions/DR-0006-pake.md) |
| D-07 | Relationship privacy | High | V1 | H1/M1 | PROPOSED | Per-relationship stream (Option A) | [DR-0007](decisions/DR-0007-relationship-privacy.md) |
| D-08 | Freshness attestation | Med | V1.1 | H5 | PROPOSED | Timestamp / nonce proof | [DR-0008](decisions/DR-0008-freshness.md) |
| D-09 | Identity Root custody | High | V1 | H2/H3 | PROPOSED | Root offline/hardware; Relationship Key option | [DR-0009](decisions/DR-0009-root-custody.md) |
| D-10 | Local API caller authentication | Med | V1.1 | H4/H7 | PROPOSED | Caller identity + capability proof | [DR-0010](decisions/DR-0010-local-api-security.md) |
| D-11 | Resource limits | High | V1 | — | PROPOSED | Per-peer + per-object bounded limits (§13.6) | [DR-0011](decisions/DR-0011-resource-limits.md) |
| D-12 | Monotonic clock reset on reboot | Med | V1.1 | — | PROPOSED | Clock reset handling; freshness impact | [DR-0012](decisions/DR-0012-clock-reboot.md) |
| D-13 | Ed25519 verification strictness | High | V1 | — | PROPOSED | Strict encoding; no lenient parsing; domain sep | [DR-0013](decisions/DR-0013-ed25519-and-references.md) |
| D-14 | Fork resolution and dispute handling | High | EXT | — | PROPOSED | Resolution order; dispute evidence | [DR-0014](decisions/DR-0014-fork-resolution.md) |
| D-15 | Transmissible fork-proof object | Med | EXT | — | PROPOSED | Object form; reference rules | [DR-0015](decisions/DR-0015-fork-proof-object.md) |
| D-16 | Same-sequence key revocations | Med | V1.1 | — | PROPOSED | Ordering / dedup rules | [DR-0016](decisions/DR-0016-same-sequence-revocations.md) |
| D-17 | previous_hash redundancy | Med | V1.1 | — | PROPOSED | Redundant chain link justification | [DR-0017](decisions/DR-0017-previous-hash-redundancy.md) |
| D-18 | Object identity and reference stability | Med | V1.1 | H6 | PROPOSED | Reference form; stable IDs | [DR-0018](decisions/DR-0018-object-identity.md) |
| D-19 | History checkpoints | Med | EXT | — | PROPOSED | Checkpoint format; verification | [DR-0019](decisions/DR-0019-history-checkpoints.md) |
| D-20 | Multi-store publication | Low | EXT | — | PROPOSED | Replication / conflict | [DR-0020](decisions/DR-0020-multi-store-publication.md) |
| D-21 | Transport binding | Low | EXT | M4 | PROPOSED | HTTPS / wire mapping | [DR-0021](decisions/DR-0021-transport-binding.md) |
| D-22 | V1 minimal profile | High | V1 | L1 | PROPOSED | Minimal profile; excluded features | [DR-0022](decisions/DR-0022-v1-minimal-profile.md) |
| D-23 | Test vectors and conformance | High | V1 | — | PROPOSED | Vector format; conformance scenarios (§60) | [DR-0023](decisions/DR-0023-test-vectors.md) |
| D-24 | Relay economy and extension scope | Low | EXT | — | PROPOSED | Relay cost; scope boundaries | [DR-0024](decisions/DR-0024-relay-economy.md) |
| D-25 | Licensing | Low | — | L3 | PROPOSED | License selection; original content | [DR-0025](decisions/DR-0025-licensing.md) |
| D-26 | Implementation language | Low | — | — | PROPOSED | Language / runtime choice | [DR-0026](decisions/DR-0026-implementation-language.md) |

All links resolve to `design/decisions/DR-00xx-*.md`; all statuses = PROPOSED.
