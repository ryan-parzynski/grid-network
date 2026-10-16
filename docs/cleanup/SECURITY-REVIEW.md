# Grid Network — SECURITY.md Traceability Review

**Repository path:** `docs/cleanup/SECURITY-REVIEW.md`

This document is non-normative. It records the independent, read-only
traceability review of `spec/SECURITY.md` performed before revision 2.4,
and what was done with each finding.

**Provenance.** The review was run by a separate reviewer that did not
draft `spec/SECURITY.md` and was given only the repository. It did not
use git history, the Security Addendum, or the earlier plan. The author
of revision 2.4 spot-checked the main findings against the cited
sections before applying them. No separate report file was saved. This
record is reconstructed from the reviewer's final findings and
classification table.

**Classes.** Traced: supported by the cited source. Misattributed:
supported by a source other than the one cited. Unsupported: no in-repo
source supports it. Contradicted: an in-repo source conflicts with it.
Deferred or out of scope: intentionally non-normative or explicitly
deferred.

**Result.** Most claims were traced. The unsupported, misattributed and
contradicted claims were corrected in revision 2.4 (commit `ccb0b1b`), with
the exceptions listed under "Not applied" below.

## 1. Findings that were contradicted or unsupported

| Location | Claim | Class | Source or absence of source | Correction applied |
|---|---|---|---|---|
| Header, lines 15–16 | Every statement traces to `PROTOCOL.md` or `OBJECTS.md` | Contradicted | The document cites `DEPLOYMENT.md`, `CONFORMANCE.md`, `REJECTED.md`, `EXTENSIONS.md`, `RELAYS.md`, `ROADMAP.md`, `PARAMETERS.md`, and some statements have no source | Reworded: each statement cites the section it relies on; non-PROTOCOL/OBJECTS sources are named |
| Threats table, Eavesdropper | "observe grants" | Unsupported | No source on grant confidentiality or visibility | Removed |
| Threats table, Lost or stolen device | "The issuer revokes the key… exposure ends when the verifier learns of the revocation or the lease expires" | Contradicted (partly) and Misattributed | §14 and §42: Identity Root signs `KeyRevocation`. §16 and §17: objects below `effective_sequence` stay valid until their own expiry. §31: no propagation bound | Rewritten to cite §14, §16, §17, §31, §42 |
| Threats table, Verifier with incorrect clock | Absolute timestamps "bounded by `MAX_CLOCK_SKEW`", cited to §32 and §39 | Misattributed and overstated | `MAX_CLOCK_SKEW` appears only in §39 F3, which calls it the "recommended mitigation" | Reworded; citation to §32 dropped |
| Threats table, Replay attacker | "Leases carry observation records" | Contradicted | §10 and §34 and §43 MUST 9: verifiers persist observation records | Rewritten: verifiers persist them; `MAX_LEASE_AGE` cited to §10 item 4 |
| Threats table, Man-in-the-middle at pairing | "password-authenticated key exchange"; "attempts are limited" (§20, §21) | Misattributed (wording) and Unsupported (attempt limit) | §20 says "authenticated key exchange… SPAKE2". No section states an attempt limit. The only mention is `PAIRING_MAX_ATTEMPTS` in PARAMETERS, whose "Defined in" cell points at §21, which does not define it | Attempt-limit clause removed (decision: do not cite PARAMETERS). Row rewritten to §20, §21.1, §21.3, §21.4, §21.6 |
| Section 2, after the table | F1–F6 "defined for each of these conditions"; "availability-preserving for reachability" | Overstated; second half Unsupported | §39 covers authorization, reachability, clock skew, revocation, forks, interruption. It does not cover Sybil, DoS, pairing MITM or replay. "Availability-preserving" is not in §39 | Rewritten to the terms of §39 F1 and F2 |
| Section 3, "Global surveillance resistance" | Network observer observes endpoints and volume | Unsupported and Misattributed | No such §47 bullet. §25 lists packet size, timing and identifiers observed by a relay. ROADMAP §6 covers metadata | Replaced by a "Metadata protection" bullet citing §47, §25, §46 |
| Section 3, "Endpoint compromise" | Compromised OS compromises keys | Unsupported | Nearest text is §21.6, which is limited to pairing | Recast to "Endpoint compromise during pairing" citing §21.6 |
| Section 3, "Quantum resistance" | Ed25519 not quantum-resistant, cited to §46 and EXTENSIONS | Misattributed | The vulnerability statement is in `DECISIONS.md` D18. §46 lists the feature only as planned | Cites D18 for the vulnerability; §46 and EXTENSIONS for planned status |
| Section 4, Network observer row | Metadata | Unsupported | No source describes a generic network observer | Row removed |
| Section 4, Application row | Capabilities already granted | Unsupported | An application is not a key role (§6). §37 limits the Application domain but says nothing about compromise | Row removed |
| Section 4, Service Key row | "None" cells and "Service records" under the Reachability column | Unsupported in part | §6 and §42 show only what the Service Key signs. No source discusses Service Key compromise | Sources note added. Table cell **not** changed (see "Not applied") |
| Section 4, Relay row | "Disruption" cited to §25 | Misattributed | §25 does not say so. `DEPLOYMENT.md §8.2` does | Sources note added citing DEPLOYMENT §8.2. Cell not changed |
| Section 5, Device Key compromise | Device removed from `device_bindings`; denial cited to §16, §27 | Misattributed | `CONFORMANCE.md` §2 Level 5 states the denial. `DEPLOYMENT.md §7` describes the removal. §16 and §27 do not mention `device_bindings` | Citations re-sourced; §27 cited only for the signing-key check |
| Section 5, Propagation | Recommended interval "is `DEFAULT_REVOCATION_POLL_INTERVAL`" | Unsupported (and dangling in PARAMETERS) | §31 does not name the symbol or any interval. ROADMAP §5 Q4 lists the normative interval as an open question | Replaced with a reference to the open question in `ROADMAP.md §5`. The dangling definition is recorded in FOLLOW-UPS item 3b |
| Section 6, "atomically" | Attributed to §43 | Misattributed | Source is `OBJECTS.md §8.1` | Attributed to `OBJECTS.md §8.1` |
| Section 6, "Keep an audit record" | Recommended, uncited | Misattributed | §43 SHOULD 7: log security events without key material | Recast to cite §43 |
| Section 6, "Generate keys and nonces with the OS CSPRNG" | No source | Unsupported | Nearest are §21.2 and §43 MUST NOT 6 | Removed |
| Section 6, "Keep revocation state coherent across caches" | No source | Unsupported | Related: §43 MUST NOT 3, §39 F4, F6 | Removed. Replaced by "Never cache authorization indefinitely" (§43 MUST NOT 3) |
| Section 7, proof-of-work "as admission policy" | Use as an admission policy is a deployment matter | Second half Unsupported | R8 rejects proof-of-work as a foundation. R7 covers admission control | Recast to R7 and R8 |
| Section 7, test vectors | "Defined in `CONFORMANCE.md`" | Overstated | `CONFORMANCE.md` defines format and levels. `ROADMAP.md §1` states no vectors are published | Reworded |
| Section 7, recovery-time targets | "The protocol defines no recovery time" | Unsupported as a scope statement | No source mentions recovery time | Bullet recast to §18 and §47 (no recovery authority) |

## 2. Parameter citations

| Symbol | Result | Action |
|---|---|---|
| `MAX_CLOCK_SKEW` | Defined in §39 F3. Valid | None |
| `MAX_LEASE_AGE` | Defined in §10 item 4. Valid | Cite §10 only |
| `DEFAULT_REVOCATION_POLL_INTERVAL` | Dangling. §31 does not state it | Removed from SECURITY.md. FOLLOW-UPS item 3b |
| `PAIRING_MAX_ATTEMPTS` | Dangling. §21 does not state it | Attempt-limit clause removed. FOLLOW-UPS item 3b. Not cited from PARAMETERS |
| Eleven other PARAMETERS "Defined in" cells | Mechanical scan found the symbol absent from the cited section | Not in SECURITY.md. FOLLOW-UPS item 3b |

## 3. Traced claims

These were supported by the cited source and were left unchanged.

- Non-normative status, and the statement that the specification governs (header).
- Separation-of-authority list and its consequences (§1), with the citations to §1, §13, §23, §25, §37, §47.
- Threats table rows for malicious peer, malicious rendezvous, malicious relay, insider, Sybil, DoS and equivocating issuer, each traced to §9, §23, §24, §25, §26, §11, §43, §47, OBJECTS §9.3–9.4, §40.
- Chain-hash sentence, traced to OBJECTS §3.8 and §3.12 (also corrected in revision 2.2).
- Blast-radius notes on the Authorization Key, Device Key and GrantRevocation signer (traced to DEPLOYMENT §7.2, §8.6, §36, §42, §15).
- Compromise response for Authorization Key compromise (§16, §17) and for the Identity Root (§18, R5).
- Implementation requirements traced to §43 MUST 3, 4, 7, 8, 9, 10 and MUST NOT 7, 8, 9, 10; and SHOULD 6.
- Out-of-scope bullets for availability, application authorization and identity recovery (§47, §18).
- Conformance is not certification (§47).
- Relay capacity planning (RELAYS §4).
- Post-quantum and threshold recovery are `planned` (§46, EXTENSIONS).

## 4. Inferential claims left unchanged

The reviewer classed these as traced by inference, not by literal text. They were left as written.

- Identity Root row: the Reachability column is "Total". §18 lists identity, relationships, revocations and grants, not reachability. §5 says the Root authorizes device and service keys.
- Authorization Key row: the Relationship column is "None". §42 gives relationship assertions to the Identity Root only.
- Device Key row: the reachability records cell is accurate. The row does not mention that the Device Key authenticates the device (§6).
- Separation-of-authority bullets and the "transport success" and "signed object" sentences are paraphrases.

## 5. Not applied in revision 2.4

These were raised by the review but not changed in revision 2.4. Each is recorded in `docs/FOLLOW-UPS.md` unless marked otherwise.

| Location | Issue | Status |
|---|---|---|
| Section 4, Service Key row | "Service records" sits under the Reachability column, and the "None" cells rest on the signing matrix alone | Not changed. Table placement is a judgement the reviewer suggested; sources note added. Not recorded as a separate item |
| Section 4, Relay row | "Disruption" is cited to §25 in the reviewer's view | Partly addressed by the sources note. Not recorded separately |
| Section 4, Device Key row | Omits that the Device Key authenticates the device | Not changed. Optional |
| Section 2, Lost or stolen device | Revocation exposure wording beyond §16/§17 | Changed. Residual judgement not recorded |
| Section 6, "Requirements already stated in §43" | §43 MUST 10 (monotonic clock) is missing from the list | Not added. Recorded here only |
| Section 5 / threats: QUARANTINED state | §40 moves FORK_DETECTED to QUARANTINED; SECURITY.md omits it | Not changed. Recorded here only |
| PROTOCOL §6 table and §2 goal 13 | "Deferred" for threshold recovery, against "planned" in §46 and §18 | Recorded in FOLLOW-UPS item 10 for §6 only. §2 goal 13 is not listed there |
| OBJECTS §8.2 | "FORKED" where the state is `FORK_DETECTED` | FOLLOW-UPS item 10 |
| PROTOCOL §16 example | KeyRevocation placed in an Authorization Key sequence | FOLLOW-UPS item 10 |
| PARAMETERS introduction | "Literal values do not appear in normative text", but §21.2 contains literals | FOLLOW-UPS item 10 |
| Section 2 threats table, pairing row, "Defined in" | `PAIRING_MAX_ATTEMPTS` dangling definition | FOLLOW-UPS item 3b |
| Review scope | Evidence pass not exhaustive against the Security Addendum or the consolidated archive | FOLLOW-UPS item 6b |
| Revision 2.2 normative equivalence | Whether v0.6.3 differs normatively from v0.6.2 is not stated | FOLLOW-UPS item 9 |

## 6. Intentionally deferred

The Security Addendum sections not yet reviewed for inclusion, and the
earlier threat model, are deferred under FOLLOW-UPS item 6. Nothing from
them was imported. The reviewer did not review them.
