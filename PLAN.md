# Grid — Build Plan

**Status:** working plan, revision 1 (4 November 2026). **Builds on:** the Redesign Plan (spec checkpoints CP0–CP9), the State Distribution Hypotheses, the Consolidated Baseline, and the repository's `ROADMAP.md` (M0–M9) and `docs/FOLLOW-UPS.md` item 11. **Units:** effort is in *sessions* (one focused 2–4 hour block of you directing AI models), the same unit as the Redesign Plan.

---

## 1. The plan in one page

Grid is two projects that have to be built in a fixed order: a **verification kernel** (signed objects, streams, leases, a verifier that decides offline) and a **connectivity product** (an agent that pairs devices, finds them, connects them, and asks the kernel whether each connection is allowed). The kernel is where the security lives and where every past defect came from, so it goes first, it is specified by executable test vectors, and nothing on the wire is built until its bytes are frozen. The Redesign Plan already covers this part (CP0–CP9). This plan adds what comes after and around it.

Eight recommendations carry most of the weight:

1. **Stop revising the prose specification and start executing it.** Revisions 2.2–2.6 fixed documentation. Defects F-01 (revoked objects break their stream), F-02 (every identity stream shares one chain base) and F-03 (two map-key orderings) are the kind a running verifier finds in minutes and prose review missed for months. Freeze the existing documents as the design record under `reference/`, and put the next spec, its vectors and its code at the top level of this repository.
2. **Languages: Python for the reference verifier and vector generator, Rust for everything you ship, Swift and Kotlin only as thin mobile shells.** Build the Rust core from the spec alone at CP8 and it becomes the independent second implementation (M3) and the production core at the same time. Two implementation languages, not three.
3. **Do not build NAT traversal or relays. Evaluate iroh first.** Iroh 1.0 (June 2026) dials devices by Ed25519 public key, hole-punches over QUIC, falls back to stateless relays that cannot decrypt, supports multipath, and promises wire and API stability across 1.x. Its documentation says it does not solve initial key exchange. That gap is Grid: identity, authorization, pairing. If a two-session spike confirms it, milestones M5 and M7 shrink from the largest engineering work in the roadmap to integration.
4. **Ship application-level connections before a full-network tunnel.** The developer API in the baseline (B12) already gives applications a local URL, not raw network access. Build that first: the agent proxies a local port to an authorized remote service. A TUN device, routes, DNS and OS VPN permissions come later, and only if users ask for them.
5. **Run the Biscuit test (H0.1) before writing the brief.** If Biscuit can carry `max_offline_tolerance` without a fork, Grid defines a Biscuit profile instead of a grant format, and that becomes a fixed constraint the design models must see. It costs one session and changes what the design phase designs.
6. **Make every protocol state machine sans-IO.** The kernel, the freshness protocol and the pairing protocol take bytes and time in and return bytes and decisions out. That one rule makes vectors, model checking, deterministic simulation and fuzzing all possible on the same code.
7. **Decide the license before anyone else contributes.** GPLv3 on a library that ships inside iOS apps runs into App Store terms, and copyleft on the spec and vectors discourages independent implementers. Apache-2.0 OR MIT for code, CC-BY-4.0 for the spec and CC0 for vectors is the usual combination for a protocol that wants implementers. This is decision D14, and it is cheapest to make now.
8. **Target self-hosters first, as the Hypotheses document already narrows it, and dogfood from milestone B3 on.** Your own home server, laptop and phone are the first deployment. Every milestone after B2 ends with a demo you run on your own devices.

Rough total to a self-hoster beta (through milestone B6): about 105–190 sessions, of which 30–60 are the spec checkpoints, plus about 30 more if iroh does not fit. The range is dominated by whether iroh holds up (§5) and how many guesses the independent implementation surfaces at CP8.

---

## 2. Where things stand

| Item | State |
|---|---|
| Existing documents, now under `reference/` | Revision 2.6, protocol v0.6.3, documentation only. No code, no vectors. `reference/tools/validate.py` and `reference/tools/selftest.py` guard them. Reference material: read-only from here on. |
| Known spec defects | F-01, F-02, F-03 (above), plus the 41-item findings register in the Consolidated Baseline. The repository still governs until they are applied. |
| Spec process | The Redesign Plan: clean-sheet brief, two isolated designs, decision log, adversarial review, spec v0.1, reference verifier, vectors, independent implementation, comparison against the old design (CP0–CP9, 30–60 sessions). |
| State distribution | Hypotheses H0–H8: signed stream heads, freshness signers with "max of any", fork-as-terminal revocation, mobile observation clock. None tested yet. |
| Open decisions | Redesign Plan D1–D15, Hypotheses D16–D19, FOLLOW-UPS item 11 (language), item 12 (stability list). |
| Implementation | None. |

The repository's `ROADMAP.md` milestones M0–M3 (spec, vectors, reference implementation, independent implementation) are what CP0–CP9 produce for the first slice. M4–M8 (LAN, remote reachability, rendezvous resilience, relay, mobile) are what this plan schedules.

---

## 3. Architecture to build toward

### 3.1 Components

| Component | What it is | Runs where |
|---|---|---|
| **grid-core** | Pure library: strict CBOR, the six constructions, object schemas, stream and chain state, the verifier, the access decision, reason codes. No I/O, no clock, no network. Time and stored state are passed in. | Everywhere |
| **grid-store** | Durable verifier state and the persisted observation clock (SQLite, WAL, `synchronous=FULL`, one transaction per commit; boot identifier and suspend-aware monotonic reading per observation). | Agent |
| **grid-proto** | Sans-IO state machines for freshness refresh, state sync (heads, prefix fetch, fork proofs) and pairing. | Agent, servers |
| **grid-agent** | The daemon. Holds keys (OS keystore), runs grid-core and grid-proto, owns the connectivity endpoint, exposes the local API (`discover`, `resolve`, `connect`, `authorize`, `revoke`, `status`) over a Unix socket or named pipe, and proxies authorized connections to local ports. | Each device |
| **grid** (CLI) | Thin client of the agent API, plus offline tools: keygen, inspect object, verify vector, `grid doctor`. | Each device |
| **grid-rendezvous** | One self-hostable binary: stores and serves signed identity state, heads, reachability records and fork proofs; optionally hosts a freshness signer for its owner. Holds no authority. | VPS, home server |
| **Relay** | Iroh's relay server if iroh is adopted (self-hosted for self-hosters), otherwise a Grid relay. Forwards ciphertext, holds no authority. | VPS |
| **Mobile shells** | Swift (iOS Network Extension or app process) and Kotlin (Android `VpnService` or foreground service) around one Rust library exposed through UniFFI. UI only; all protocol logic stays in Rust. | Phones |
| **grid-ref** (Python) | Reference verifier that reads like the spec; conformance runner. | CI, your laptop |
| **grid-vectors** (Python, separate package) | Vector generator. Shares no source files with grid-ref or grid-core. | CI |

### 3.2 The four architectural rules

1. **Functional core, imperative shell.** grid-core and grid-proto never read a clock, a socket or a disk. The agent does all I/O and passes results in. This is what makes one verifier run identically in a test vector, a model checker trace, a simulation, a fuzzer, a server and a phone.
2. **Authorization and connectivity never mix.** The connectivity layer (iroh or otherwise) may tell the agent "this remote endpoint proved key K". Only grid-core decides whether K belongs to a device bound in an accepted identity, whether a grant covers the request, and whether the lease is valid and fresh. A failed path is an availability failure, never an authorization change (INV-6).
3. **The transport key is bound, not trusted.** If iroh is adopted, each device's iroh endpoint key is a separate key role, bound in the identity document by the Identity Root, distinct from the Device Key that signs reachability records. This answers open question Q33 (transport-to-identity binding) and keeps the one-key-one-role invariant (INV-7).
4. **Everything the user sees has a reason code.** `REFRESH_UNAVAILABLE`, `STATE_INCOMPLETE`, `STREAM_TERMINATED`, `REVOKED`, `DENIED`, plus connectivity codes (`UNREACHABLE`, `RELAY_UNAVAILABLE`). The agent logs them, the CLI prints them, `grid doctor` explains them. A self-hoster debugging alone needs to tell "not allowed" from "can't reach" in one line.

### 3.3 Connection modes, in order

| Mode | What the user gets | When |
|---|---|---|
| **Local port proxy** | `grid connect nas/jellyfin` opens `127.0.0.1:<port>`; the agent carries the bytes over an authenticated QUIC stream to the remote agent, which forwards to the service after checking the grant. | B3 |
| **App API** | An application calls the agent's API and receives a local URL (baseline B12). | B6 |
| **Full tunnel** | A virtual network interface with Grid peers addressable by IP; WireGuard (boringtun) or iroh-carried IP packets. | After beta, if demanded |

The proxy mode needs no root privileges, no OS VPN entitlement, no routing table changes and no DNS interception, which is most of the platform pain in tools of this kind.

---

## 4. Languages

This resolves FOLLOW-UPS item 11. It agrees with the Redesign Plan's D6 (Python reference) and D7 (Rust production) and narrows D13 (independent implementation) to Rust.

| Area | Language | Why | Alternative and when to switch |
|---|---|---|---|
| Reference verifier | Python 3.12+, frozen dataclasses, `mypy --strict`, Hypothesis | Changes fast while the spec moves; reads like the spec; performance is not its job | — |
| Vector generator | Python, separate package | Language-neutral JSON + hex output; separate code so one bug cannot make generator and verifier agree | — |
| Models of multi-actor behavior | Quint (Apalache or TLC backend) | TLA+ semantics with syntax one person can maintain | TLA+ directly |
| grid-core, grid-proto, grid-store, agent, CLI | Rust | Memory safety on hostile input, no GC, one library for desktop, server and mobile (UniFFI), and the best-fitting dependencies (iroh, biscuit-auth, rustls, quinn, boringtun, ed25519-dalek) are Rust | Go, if Rust velocity becomes the bottleneck after B2; you would then lose the shared mobile core |
| Rendezvous and relay servers | Rust | Same core, same object code, one toolchain, one CI | Go is a reasonable choice for servers alone; not worth a third language for a solo developer |
| iOS shell | Swift, SwiftUI | Required by the platform | — |
| Android shell | Kotlin, Jetpack Compose | Required by the platform | — |
| Web admin UI (optional, late) | TypeScript | Only if a local web UI beats the CLI for self-hosters | Skip entirely |
| Spec | Markdown, mdBook, RFC 2119 keywords, requirement IDs | Spec, vectors and code in one review flow | kramdown-rfc only if a standards venue becomes a goal |

**How independence is kept with only two languages.** The Python reference is written during CP5–CP6 alongside the spec. The Rust core is written at CP8 in a fresh context from the spec text alone, with vectors withheld until it compiles, exactly as the Redesign Plan specifies for the independent implementation. The guess list from that build is the deliverable that fixes the spec. After CP8 the Rust core is the production core, and the Python reference stays as the oracle every Rust change is differentially tested against.

---

## 5. What to take from open source

Three categories: **adopt** (a dependency), **study** (read the design and the code, borrow ideas, do not depend on it), **avoid** (for a stated reason). Check maintenance status and license at the moment of adoption; the notes below are as of this plan.

### 5.1 Adopt

| Need | Take | Notes and risks |
|---|---|---|
| Hole punching, relay fallback, QUIC transport, multipath | **iroh** (n0) | 1.0 released 15 June 2026; wire compatibility across 1.x; API stable without a major bump; Swift and Kotlin bindings exist. Does not do key exchange, identity or authorization, which is Grid's job. Spike first (§6, S2). Iroh's own discovery (DNS-based) can be used for B3, then replaced by Grid's signed reachability records published to Grid rendezvous. |
| Grants (if H0.1 passes) | **biscuit-auth** (Eclipse Biscuit) | Datalog authorization with attenuation; verifier-supplied facts make the lease bound expressible. Tokens are protobuf, carried as opaque bytes in Grid's CBOR envelope (D16). |
| Ed25519 | **ed25519-dalek** (`verify_strict`) or **ed25519-zebra** (ZIP-215 rules) | Choose the one that matches the verification rule pinned at CP3 (D9). PyNaCl/libsodium on the Python side. Edge-case signature vectors catch any disagreement. |
| SHA-256 | **sha2** (RustCrypto); `hashlib` in Python | — |
| CBOR | Hand-written strict decoder/encoder in each implementation; **minicbor** at token level or **cbor2** (Python) only in differential tests | General libraries accept non-canonical input and some merge duplicate keys. |
| TLS (rendezvous HTTPS) | **rustls** | — |
| HTTP server | **axum** on **tokio** | Rendezvous API. |
| Storage | **rusqlite** (bundled SQLite) | WAL, `synchronous=FULL`. |
| OS key storage | **keyring** crate (Keychain, Credential Manager, Secret Service); platform APIs on mobile | Apple's Secure Enclave and most hardware keystores sign with P-256, not Ed25519. Hardware-backed device keys therefore need algorithm agility (D10) or stay software keys in the keystore. |
| Secret hygiene | **zeroize**, **secrecy** | — |
| Mobile bindings | **UniFFI** (Mozilla) | One Rust library, generated Swift and Kotlin. |
| LAN discovery | **mdns-sd** | B3, if iroh's local discovery does not cover it. |
| Full-tunnel mode (later) | **boringtun** | Cloudflare's original repository is quiet; maintained forks exist (for example Defguard's, with UniFFI Swift bindings). Re-evaluate when the tunnel mode is scheduled. |
| PAKE for pairing | **spake2** (RustCrypto PAKEs), as the spec currently selects | Its own documentation says it has never had an independent audit and is probably not constant-time. Pairing is milestone B5; budget a review of this dependency, or reopen the PAKE choice (CPace is the CFRG's recommended balanced PAKE) before B5. |
| Deterministic network simulation | **turmoil** (tokio) | Simulated network with partition, delay, drop, reorder; reproducible from a seed. |
| Testing | **proptest**, **cargo-fuzz** (libFuzzer), **insta** (snapshot); **Hypothesis**, **pytest** | — |
| Model checking | **Quint** with **Apalache** | — |
| Supply chain | **cargo-deny** (licenses, advisories, bans), **cargo-audit**, **cargo-vet**, **cargo-dist** (release builds), **cargo-cyclonedx** (SBOM), **Sigstore/cosign** (signing) | — |

### 5.2 Study, do not depend on

| Project | What to take from it |
|---|---|
| **magic-wormhole** (and magic-wormhole.rs) | The closest prior art for Grid pairing: a short human-transferable code, SPAKE2 over a rendezvous "mailbox" server that sees only ciphertext, then a transit relay. The `spake2` crate was originally written for it. Read its protocol docs before writing the pairing spec. |
| **Tailscale** (client, DERP, magicsock, Tailnet Lock) | DERP shows the "relay first, then upgrade to direct" order that makes connections succeed immediately; Tailnet Lock is the nearest existing design to signed identity state controlled by the user. BSD-3. |
| **Headscale** | What a self-hosted coordination server needs operationally (database, upgrades, ACL UX), and what self-hosters complain about. |
| **Syncthing** | Device IDs, a global discovery server, a public relay pool, and fifteen years of self-hoster support experience. Its discovery and relay protocols are small and well documented. |
| **Keybase sigchains, TUF, Certificate Transparency** | Signed append-only histories, role keys, freshness and rollback protection (TUF's timestamp role versus Grid's nonce-bound freshness signer). The Hypotheses document still lists these as not re-verified (§7). |
| **libp2p** (DCUtR, relay v2, AutoNAT) | An alternative connectivity stack and a source of NAT-traversal measurement data. |
| **quinn / quinn-proto** | The model for sans-IO protocol design in Rust. |
| **WireGuard** | Small, auditable protocol design; the reason to keep any Grid wire protocol small. |

### 5.3 Avoid

| What | Why |
|---|---|
| Writing your own NAT traversal, relay protocol or QUIC stack | The largest, slowest and most network-specific work in the roadmap, and iroh and libp2p already exist. Build it only if the iroh spike fails and libp2p fails too. |
| Implementing any cryptographic primitive | Already forbidden by the spec (`PROTOCOL.md §43`). |
| General-purpose CBOR libraries as the decoder of record | They accept non-canonical input; canonical rejection is a security property here. |
| Blockchains, DHTs, global consensus | Non-goals in the baseline (B13). |
| An OS tunnel in the first release | See §3.3. |

---

## 6. Milestones

### 6.0 How the two tracks fit

```
Spikes (S1–S3)  ──► CP0 decisions ──► CP1 brief ──► CP2–CP4 designs, decisions, review
                                                        │
                                   CP5 spec v0.1 ──► CP6 reference + vectors ──► CP7 negatives
                                                                                   │
                                   CP8 Rust core from spec alone ──► CP9 comparison
                                                                                   │
B1 core hardening ──► B2 agent + CLI (offline) ──► B3 connect over iroh ──► B4 rendezvous + freshness
        ──► B5 pairing ──► B6 self-hoster beta ──► B7 mobile ──► B8 resilience and federation
```

Each build milestone that needs a new wire protocol (B4 state sync and freshness, B5 pairing) runs its own small spec cycle first: spec section with requirement IDs → vectors → Python reference → Rust → integration. It is the same discipline as CP5–CP8, at a smaller scale.

### 6.1 Spikes (before or alongside CP0)

Spikes produce evidence, not design. They are run outside the design models' contexts, and their results enter the decision log at CP3 the same way the Hypotheses document does.

| # | Spike | Exit | Effort |
|---|---|---|---|
| S1 | **H0.1 Biscuit lease bound.** Build the construction in the Hypotheses document §1.2 with `biscuit-auth`; run the four vectors and the two-facts case. | Recorded pass/fail. Pass → D16 adopted and Biscuit becomes a fixed constraint in the brief. Fail → Grid defines its own grant format. | 1 session |
| S2 | **Iroh fit.** Two machines on different networks (one behind CGNAT or a phone hotspot), dial by key, measure direct versus relayed; self-host `iroh-relay` on a VPS; force a UDP-blocked network and confirm relay fallback still connects; proxy a TCP service through a QUIC stream. | Connects in all three network setups; self-hosted relay works; written list of anything Grid needs that iroh does not expose (for example control over discovery publishing, or binding an endpoint key to an external identity). | 2 sessions |
| S3 | **Edge-case signatures.** Run the "Taming the many EdDSAs" style edge cases through PyNaCl, ed25519-dalek `verify_strict` and ed25519-zebra. | A table of which library accepts what; feeds D9. | 1 session |

### 6.2 Spec track (CP0–CP9, from the Redesign Plan)

Unchanged, with three additions:
- CP0 also records D20–D23 (§9).
- CP6's reference verifier and CP8's independent implementation must both expose the same `verify <vector.json>` CLI, so one conformance runner drives both.
- CP8's independent implementation is the Rust grid-core crate, built in a fresh context from the spec alone.

These checkpoints produce `ROADMAP.md` M0–M3 for the first slice (local verification).

### 6.3 Build milestones

**B1 — Core hardening.** *Depends on:* CP8.
- *Deliverables:* grid-core and grid-store crates; `#![forbid(unsafe_code)]`; fuzz targets for the decoder, every object parser and the verifier; differential test against the Python reference on generated inputs; persisted observation clock with platform clock sources for Linux, macOS and Windows.
- *Exit:* every vector passes in both implementations in CI; each fuzz target has run at least 24 CPU-hours with no crash; zero differential disagreements; a simulated suspend and a simulated reboot each produce the specified lease behavior.
- *Effort:* 15–25 sessions.

**B2 — Agent and CLI, offline.** *Depends on:* B1.
- *Deliverables:* grid-agent daemon with the local API over a Unix socket or named pipe; keys in the OS keystore; `grid` CLI for creating an identity, adding a device, issuing a grant and lease, revoking, and inspecting state; "manual pairing" by exchanging identity documents as files plus a fingerprint comparison (a stand-in until B5).
- *Exit (demo):* two identities on two machines with no network between them; Alice grants Bob, Bob's agent verifies, Alice revokes, the revocation file is carried over, and Bob's agent denies with `REVOKED`. Every step prints a reason code.
- *Effort:* 10–20 sessions.

**B3 — Connect over iroh.** *Depends on:* B2, S2 passed.
- *Deliverables:* iroh endpoint inside the agent; endpoint key as a bound key role; `grid connect peer/service` local port proxy; the remote agent checks grant and lease before forwarding; self-hosted iroh relay; LAN and remote both work. This covers `ROADMAP.md` M4 and most of M5 and M7.
- *Exit (demo, dogfood starts):* from your laptop on a mobile hotspot, `grid connect home/ssh` reaches your home server's SSH; revoking the laptop's grant on the server ends access at the next authorization check; relay-only works when UDP is blocked.
- *Effort:* 10–20 sessions if iroh holds; 40+ if connectivity has to be built on libp2p or from parts.

**B4 — Rendezvous, state distribution and freshness.** *Depends on:* B3, a spec cycle for state sync and freshness.
- *Deliverables:* spec sections for signed heads, prefix fetch, fork proofs, nonce-bound freshness attestations and receipts (Hypotheses §3); Quint models H5.1 and H8.1; grid-rendezvous binary (publish and fetch identity state, heads, reachability, fork proofs; optional freshness signer); agents publish reachability records there instead of using iroh's discovery.
- *Exit:* the Quint models pass at stated bounds; a revocation issued on the home server reaches the laptop through a rendezvous without the two ever being online together; the laptop's lease fails closed with `REFRESH_UNAVAILABLE` after `max_offline_tolerance` when every signer is unreachable; a restored stale backup cannot fork the stream when any signer is reachable (H8.3).
- *Effort:* 12–20 sessions.

**B5 — Pairing.** *Depends on:* B4, a spec cycle for pairing, the PAKE dependency reviewed or replaced.
- *Deliverables:* pairing wire spec (resolving Q15: hint format, PAKE transport, initiator choice); QR and typed-code flows in the CLI; transcript code comparison; receiving-side confirmation; rate limits and single-use secrets; headless enrollment decided (Q28).
- *Exit:* two devices that have never exchanged keys pair in under two minutes; every negative pairing vector (wrong code, replayed secret, transcript mismatch, expired code) is rejected; a failed pairing leaves no state.
- *Effort:* 8–15 sessions.

**B6 — Self-hoster beta.** *Depends on:* B5.
- *Deliverables:* packages for Linux (deb, rpm, static binary, systemd unit), macOS and Windows; a Docker image for grid-rendezvous plus iroh-relay; app API (`connect` returns a local URL); one documented integration end to end (for example Jellyfin, Home Assistant or SSH); a setup guide timed against H5.3 (off-NAT signer in under 30 minutes); `grid doctor`; a security policy and disclosure address; the first external review of the spec.
- *Exit:* five self-hosters other than you install it from the guide without help; the five failure stories in H1 (lost phone, NAS restore, provider change, phone reboot offline, revoked laptop) are each resolved from the documentation alone.
- *Effort:* 15–25 sessions.

**B7 — Mobile.** *Depends on:* B6. Covers `ROADMAP.md` M8.
- *Deliverables:* the Rust library through UniFFI; iOS and Android shells; refresh-on-use and suspend-on-reboot (Hypotheses §4); key storage available after first unlock; the H7 device tests on at least one iPhone, one Pixel, one Samsung and one Xiaomi device.
- *Exit:* H7.1–H7.3 pass; the reboot-offline screens in Hypotheses §4.3 appear with the right reason codes; App Store and Play review passed (license decision made by then).
- *Effort:* 25–45 sessions.

**B8 — Resilience and federation.** *Depends on:* B6. Covers `ROADMAP.md` M6.
- *Deliverables:* multiple rendezvous per identity; RendezvousManifest active and recovery windows; provider switch drill; then rendezvous federation if still wanted.
- *Exit:* the provider-change simulation in Hypotheses H3 (contact on day 1, 15 and 31 of a 30-day window) behaves as specified.
- *Effort:* 10–20 sessions.

The commercial layer, credit settlement, multi-hop relay, metadata minimization and threshold recovery stay out of scope until after B8.

---

## 7. How to work each chunk

### 7.1 The loop for any feature that touches bytes or authorization

1. **Spec first.** Write the section with requirement IDs on every MUST. Name what is out of scope.
2. **Vectors second.** Positive vectors plus at least three negatives each, from the generator package.
3. **Reference third.** Python reference passes the vectors.
4. **Rust fourth.** Rust passes the same vectors and agrees with the reference in differential tests.
5. **Integrate.** Wire it into the agent behind the sans-IO boundary; add a simulation scenario.
6. **Dogfood.** Run it on your own devices for a week before calling the milestone done.

Spec, vectors and code for one change land in **one commit**. This is the Redesign Plan's mitigation for its top-ranked risk (spec drift), and it is the main reason for keeping everything in one repository.

### 7.2 Repository layout

```
grid-network/
  PLAN.md          this plan
  README.md        entry point
  reference/       the revision 2.6 documents, frozen: spec, design, operations, commercial,
                   docs, tools (validator and self-test), and their own README and REVISIONS
  spec/            new: mdBook sources, requirement IDs, decision log, models/ (Quint)
  vectors/         new: JSON vectors, JSON Schema for the format, published key seeds
  refimpl/         new: Python reference verifier and conformance runner
  vectorgen/       new: Python vector generator (no imports from refimpl/)
  crates/
    grid-core/     pure verifier
    grid-store/    durable state and observation clock
    grid-proto/    sans-IO freshness, sync, pairing
    grid-agent/    daemon
    grid-cli/
    grid-rendezvous/
    grid-ffi/      UniFFI surface for mobile
  sim/             turmoil scenarios
  apps/ios/  apps/android/
  tools/           new: lint scripts (requirement IDs, cross-references, import-graph check)
  AGENTS.md        rules for AI sessions in this repository
```

`reference/` is the read-only design record, and no 2.x revision is issued against it. Its validator keeps running in CI, so the record cannot drift unnoticed. The name `reference/` is deliberate: nothing new is written there, and nothing under it is normative for the new spec until a decision in the log adopts it.

**Isolation.** The Redesign Plan chose a new repository so design contexts would carry nothing from the old spec. With one repository, the same guarantee comes from the workspace instead: the CP2 design sessions run in empty workspaces, are never given this repository or `reference/`, and receive only the brief. The checks in the Redesign Plan §A (clean-room setup record, brief lint, prompt log, canary check) apply unchanged, and `reference/` counts as old-design material on the blocklist side.

### 7.3 Size every task to a session

A task fits one session if it has one named exit check you can run in under a minute (a test, a script, a demo command). If you cannot name the check, split the task. End every session with a commit that includes the check's output, as the Redesign Plan's risk 8 (solo review fatigue) requires.

---

## 8. Practices

### 8.1 Testing, by layer

| Layer | Tool | Catches |
|---|---|---|
| Normative vectors | JSON vectors, both implementations | Byte disagreements, wrong acceptance rules |
| Property tests | Hypothesis, proptest | Invariants over generated objects and streams (for example "revoke-then-target equals target-then-revoke") |
| Fuzzing | cargo-fuzz on every parser and the verifier | Crashes, accepted malformed input |
| Differential | Python reference vs Rust; strict decoder vs a general CBOR library | Silent divergence |
| Model checking | Quint | Ordering and race bugs across actors (revocation vs renewal, fork vs resolution, signer suppression) |
| Deterministic simulation | turmoil, seeded | Agent and rendezvous behavior under partition, delay, reorder, clock jump, suspend, reboot; every failure reproducible from its seed |
| Real networks | Linux namespaces + `tc netem`; a test matrix of home router, CGNAT, mobile hotspot, UDP-blocked corporate Wi-Fi | What simulation cannot model |
| Platform clocks | Device tests H7.1–H7.2 | Clocks that stop in deep sleep, missed reboots |
| Dogfood | Your own devices from B3 on | Everything else |

### 8.2 Security

- No cryptographic primitives of your own; no `unsafe` in grid-core, grid-proto or grid-store.
- Every encoded input is hostile: size, nesting and field-count limits are checked before any expensive work.
- Keys live in the OS keystore, are zeroized in memory, and never appear in logs, crash reports or error messages. Log lines carry reason codes and object IDs only.
- The Identity Root stays offline: generate it on a machine that is not the agent, print a recovery sheet, and give the agent only subordinate keys. The CLI should make this the default path, not an expert option.
- Every milestone ends with a threat review of what it added: which TH-n threats it touches, which defense applies, which LIM-n limit the user should be told about.
- Security-critical changes (decoder, constructions, verifier, freshness, pairing) are reviewed by a different model context from the one that wrote them, against the spec text, before merge.
- Before anyone outside the self-hoster beta relies on Grid, commission an external audit of grid-core and the pairing implementation. NLnet's NGI Zero programme has funded audits and development for protocols of this kind; check its current calls.

### 8.3 Dependencies and releases

- `cargo-deny` in CI: an allow-list of licenses, banned crates, advisory check. Lockfiles committed. Automated update pull requests (Renovate or Dependabot) are reviewed, never auto-merged, for anything in the security path.
- Keep grid-core's dependency list short enough to read in one sitting.
- Two version numbers, kept separate: the **protocol version** (changes only with object bytes or acceptance rules; tied to domain separators) and the **software version** (semver per binary).
- Releases are built in CI with cargo-dist, signed with Sigstore, published with an SBOM. Aim for reproducible builds before B6.

### 8.4 Working solo with AI models

- Put the rules in `AGENTS.md` in the repository: requirement IDs on every MUST, one commit per spec+vector+code change, no new dependencies without a note, no custom crypto, no network or clock calls in the core crates. Every session's model reads it first.
- Keep isolation where independence matters: the vector generator, the reference verifier and the Rust core come from separate contexts; tests for security-critical code are written by a different context from the code.
- Let CI be the reviewer that does not get tired. Every exit criterion that can be scripted is scripted, and its output is attached to the closing commit.
- Keep a `BACKLOG.md`. Anything outside the current milestone goes there, which is the plan's defense against scope creep (Redesign Plan risk 7).
- Record decisions as short entries: decision, options, evidence, what would change it. The Consolidated Baseline's open-questions table is the right format.

---

## 9. Decisions to make now

These join the Redesign Plan's D1–D15 and the Hypotheses' D16–D19 at CP0.

| # | Decision | Options | Recommended |
|---|---|---|---|
| D20 | Product language | Rust; Go | Rust (§4). Also closes FOLLOW-UPS item 11. |
| D21 | Connectivity substrate | iroh; libp2p; build on quinn plus ICE | iroh, if spike S2 passes |
| D22 | First connection mode | Local port proxy and app API; full tunnel | Proxy and app API first (§3.3) |
| D23 | Transport key binding | Separate bound key role for the transport endpoint key; reuse the Device Key | Separate role (§3.2 rule 3) |
| D14 | License (from the Redesign Plan) | Keep GPLv3; Apache-2.0 OR MIT for code, CC-BY-4.0 spec, CC0 vectors | The permissive set, decided before any outside contribution |
| D15 | Repository (from the Redesign Plan) | New repository; this repository with the old documents under `reference/` | This repository, with `reference/` frozen and new work beside it (§7.2). Decided: 4 November 2026. |
| D10 | Algorithm agility (from the Redesign Plan) | Require an algorithm identifier; Ed25519 only | Require it. Hardware keystores sign with P-256, so hardware-backed device keys need it. |
| D16 | Biscuit for grants | Adopt; own format | Decide from spike S1 before CP1 |

---

## 10. Risks specific to building

| Risk | Signal | Mitigation |
|---|---|---|
| Iroh does not fit (cannot bind its endpoint key to Grid identity, or hides discovery and relay choices Grid must control) | S2 lists gaps that need iroh changes | Upstream issue or small patch first; libp2p second; own stack last. Decide at the end of S2, not mid-B3. |
| A dependency in the security path goes unmaintained (PAKE crate, a WireGuard fork) | No releases for 12 months; open advisories | Choose dependencies with that failure in mind; keep the surface Grid uses small enough to fork or vendor. |
| Mobile background limits make leases unusable | H7.3 or H7.4 fails | The Hypotheses document already names the fallback (reconsider a bounded wall-clock bridge); do not ship mobile before H7 passes. |
| Spec work never ends | CP checkpoints slip past their effort ranges twice | The Redesign Plan's slip column says what to cut at each checkpoint; use it rather than extending. |
| Building for everyone at once | Requests from home users or enterprises shape B3–B6 | Self-hosters only through B6, as H1 states; everything else to BACKLOG.md. |
| `reference/` keeps absorbing sessions | New edits under `reference/` after CP0 | Treat it as read-only. The CI validator already fails on unintended changes there. |

---

## 11. The first ten sessions

| Session | Work | Exit check |
|---|---|---|
| 1 | CP0: answer D1–D23 (accept defaults where you have no reason to differ) | Every decision has an answer in a committed file |
| 2 | Spike S1 (Biscuit) | Four vectors recorded pass/fail |
| 3–4 | Spike S2 (iroh) | Three network setups connect; gap list written |
| 5 | Spike S3 (Ed25519 edge cases); top-level skeleton (the directories in §7.2), CI for the new code, `AGENTS.md`, license files, `cargo-deny` | CI green on an empty workspace; edge-case table committed |
| 6–9 | CP1 brief, traceability table, blind gap check | Brief lint 0 hits; 0 unmapped baseline IDs |
| 10 | Start CP2 design A in its isolated workspace | Isolation setup recorded per the Redesign Plan §A |

After session 10 the Redesign Plan's checkpoints set the pace until CP9, and then B1 begins.

---

## Sources

- [Iroh 1.0: Dial Keys, Not IPs (Pinggy)](https://pinggy.io/amp/blog/iroh_1_0_dial_keys_not_ips/)
- [Release notes for iroh v1.0.0 and v1.0.1](https://instagit.com/n0-computer/iroh/release-notes-for-iroh/)
- [spake2 crate documentation (docs.rs)](https://docs.rs/spake2)
- [RustCrypto PAKEs repository](https://github.com/RustCrypto/PAKEs)
- [Defguard: BoringTun](https://docs.defguard.net/in-depth/boringtun.md)
- [cloudflare/boringtun](https://github.com/cloudflare/boringtun)
- [Eclipse Biscuit: biscuit-auth 6.0.0 release](https://projects.eclipse.org/projects/technology.biscuit/releases/biscuit-auth-6.0.0/review)
- Project docs: Grid Redesign Plan, Grid State Distribution Hypotheses, Grid Consolidated Baseline; repository `ROADMAP.md` and `docs/FOLLOW-UPS.md` item 11.
