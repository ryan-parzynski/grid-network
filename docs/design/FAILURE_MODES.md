# Grid Network — Failure Modes and Pairing Addendum

**Status:** Companion to the Master Archive, the Detailed Reference Addendum, and the Design Defense Addendum
**Purpose:** Enumerate the failure modes the design must handle, including the ones we have discovered since the archive was assembled, and document the pairing model in enough detail to resolve the questions about time constraints, tunnel establishment, and server-side confirmation.

---

# Part 1 — The pairing model in full

## 1.1 The problem the pairing model solves

Pairing establishes a cryptographic relationship between two principals who have no prior knowledge of each other's keys. It has to be:

- **Simple enough for a non-expert.** The user experience target is "you call your mom, she types a number, she clicks yes, done."
- **Secure against a passive observer.** An attacker who sees the code or the wire traffic must not be able to impersonate either party.
- **Secure against an active attacker.** An attacker who can modify traffic must not be able to MITM the pairing.
- **Robust against slow networks.** The tunnel between the two peers may take a while to establish. The pairing must not be broken by slowness.
- **Time-bounded but not brittle.** The human coordination window is short (minutes). The technical window is longer (however long the tunnel takes).

These constraints shape the protocol.

## 1.2 The three phases

Pairing has three distinct phases, and the time bounds on each are different.

**Phase 1 — Human coordination (short-lived).**

One side displays a code or QR code. The other side receives it through a human channel (voice call, in-person, messaging, QR scan). This phase has a short window — typically 5 to 10 minutes — because the code is meant to be ephemeral. The window is long enough that the user can complete the coordination without rushing, but short enough that an attacker cannot realistically mount a targeted attack within it.

**Phase 2 — Authentication (single exchange).**

Once both sides have the code, they run an authenticated key exchange. The output is a shared session key and mutual proof that both sides know the code. This phase completes in a small number of round-trips once the two sides can communicate. If the two sides cannot communicate directly, the exchange is routed through a rendezvous server.

The code is *consumed* in this phase. After the exchange, the code is no longer valid, and no further attempt can use it.

**Phase 3 — Tunnel establishment (open-ended).**

Once authentication has succeeded, the two sides have a shared secret and a mutual recognition. They now attempt to establish a WireGuard tunnel (or whatever transport they choose). This phase has no time bound imposed by pairing — it can take as long as it takes for the network to allow it. If direct connection fails, the peers retry, fall back to relay, or wait for connectivity to return.

The critical design property: **Phase 2 and Phase 3 are decoupled.** Authentication completes in a single bounded exchange. Tunnel establishment continues independently, potentially for hours or days, using the shared secret established in Phase 2.

This resolves the concern about "the tunnel may take a bit." The pairing code's short lifetime applies only to Phase 1 and Phase 2. Once authentication succeeds, the code is gone and the tunnel establishment runs without any time pressure.

## 1.3 What "confirmation on the server end" means

The user experience for a non-expert can be simplified by adding a confirmation step to the receiving side.

Here is the flow:

1. **Alice initiates pairing** on her device. Her device generates a code and displays it.
2. **Alice tells the code to Bob** through a human channel (voice call, in-person, message).
3. **Bob enters the code** on his device. His device initiates the authenticated key exchange.
4. **Alice's device displays a confirmation prompt.** The prompt shows Bob's device identity (a human-readable label like "Ryan's iPhone") and asks: "Allow pairing with this device?"
5. **Alice confirms.** Once she does, the authenticated key exchange completes and both sides have the shared secret.
6. **Tunnel establishment proceeds** without any further user interaction.

The confirmation step serves two purposes. First, it makes the pairing a deliberate act on both sides — Alice has to actively approve the pairing, not just display a code. Second, it gives Alice a chance to notice if something is wrong (for example, if Bob's device name doesn't match what she expects).

The confirmation is **not a substitute for PAKE**. It's an additional human-verification step that complements the cryptographic exchange. Without PAKE, an attacker who observed the code could MITM the exchange, and Alice's confirmation wouldn't help. With PAKE, the exchange is secure even if the code is observed, and the confirmation is a final human check.

## 1.4 The QR code variant

For scenarios where a camera is available, the same flow can be simplified by encoding the pairing information in a QR code.

The QR code contains:
- The pairing code (or the secret that the code derives from).
- A hint about where to reach the pairing initiator (a rendezvous server URL, or a direct address).
- The pairing session identifier.

Bob scans the QR code with his device. His device extracts the pairing information and initiates the authenticated key exchange. The human coordination step is eliminated.

The QR code must not contain a long-lived shared secret. It contains a *temporary* secret that is only valid for the pairing session, and it is consumed when the pairing succeeds.

## 1.5 Why this design is secure

The security properties of this design:

**Property 1 — The code is ephemeral.** It is valid only for the human coordination window (5 to 10 minutes) and is consumed on first successful use.

**Property 2 — The exchange is authenticated.** PAKE ensures that both sides prove knowledge of the code without revealing it. An eavesdropper who captures the exchange cannot derive the code or the session key.

**Property 3 — Confirmation is required.** The receiving side must explicitly approve the pairing before it completes. This prevents silent pairing by an attacker.

**Property 4 — Establishment is decoupled.** Once authentication succeeds, the tunnel establishment runs without time pressure. Slow networks do not break the pairing.

**Property 5 — The output is a durable relationship.** The result of pairing is not a session key; it is a set of signed relationship assertions that both sides publish to their identity streams. This is what makes the relationship portable and durable.

## 1.6 What the design does not do

The design does not attempt to protect against:

- **A compromised device.** If either device is already compromised, the pairing is compromised. There is no defense against this at the protocol layer.
- **A coerced user.** If an attacker can force a user to confirm a pairing, the confirmation is not meaningful.
- **A malicious rendezvous server performing a full MITM.** PAKE protects against this, provided the code has not been intercepted. If the code is intercepted *and* the rendezvous is malicious, the attacker may still attempt an active attack. This is why the code window is short and the confirmation step exists.
- **A sophisticated attack on the human channel.** If the attacker can modify the voice call or intercept the QR scan, the code may be replaced. Human verification steps (like reading the code aloud and having the other side confirm) mitigate this, but the protocol cannot fully prevent it.

These are limitations of any pairing mechanism that relies on a human channel, and they should be named explicitly.

## 1.7 Optional hardening

For high-value pairings, additional hardening is possible:

- **Verification codes.** Both sides display a short verification code (derived from the pairing transcript) that the users compare over the human channel. This protects against a MITM who substitutes the code.
- **Longer codes.** A code longer than six digits is harder to guess and harder to brute-force. It is also harder for a user to read aloud accurately. Six digits is a reasonable balance for casual pairings; ten digits may be appropriate for sensitive ones.
- **Physical proximity.** If the two devices are physically present, the pairing can use an out-of-band channel (like NFC or an ultrasonic handshake) instead of a code. This is more secure but less convenient.

These are optional. The default pairing model is designed to be simple enough for a non-expert and secure enough for casual use.

---

# Part 2 — Failure modes not yet covered in the archive

The archive covers the major failure modes (network partition, key compromise, rendezvous unavailability). The following failure modes were discovered during design review but are not yet documented. Each is categorized by severity, and each includes a recommended treatment.

## 2.1 Cryptographic and key lifecycle failures

### 2.1.1 Root key loss (not compromise)

**Description.** The principal's machine fails, the backup fails, and the identity root private key is genuinely gone. This is distinct from compromise: no attacker has the key, but the principal cannot use it.

**Consequence.** The principal can no longer rotate keys, revoke subordinates, or update the identity document. Existing peers continue to trust the existing identity state, and existing leases continue to work until they expire. But the principal becomes a frozen identity — unable to evolve, unable to recover from any future subordinate key compromise.

**Recommended treatment.** Documentation change. Add a section to the security model: "Root key loss." Describe the failure mode, distinguish it from compromise, and recommend that recovery material be stored separately from the root key (encrypted backup in a physically separate location, or threshold sharding).

### 2.1.2 Delayed root key activation

**Description.** The root key is stolen, but the attacker does not use it for months. During that window, the legitimate principal continues to operate normally, unaware of the compromise.

**Consequence.** When the attacker finally uses the key, the damage is done. The principal has no way to know when the compromise occurred, so there is no clean point to revoke from. Any revocation issued by the principal may invalidate legitimate state or may fail to invalidate attacker state, depending on the effective_sequence chosen.

**Recommended treatment.** Documentation change. Add to the threat model: "Delayed root key activation." Note that detection requires out-of-band monitoring (peers that observe unexpected identity documents should notify the principal). Recommend that high-value principals periodically verify that their identity state has not been modified by anyone else.

### 2.1.3 Partial key compromise

**Description.** A key is leaked but the principal does not yet know it. The window between compromise and detection is the dangerous one.

**Consequence.** The design's defense is bounded exposure via leases and effective_sequence. But the design does not describe how quickly detection is expected, or what signals indicate compromise.

**Recommended treatment.** Documentation change. Add a section on "Detection and response." Describe signals that might indicate compromise (unexpected grants, unexpected identity documents, peer reports of strange behavior) and the recovery steps once detection occurs.

### 2.1.4 Compromise during pairing

**Description.** A device is compromised *before* it pairs with a peer. The attacker controls the device's keys during the pairing, and can establish pairings on behalf of the device.

**Consequence.** The pairing succeeds, but the relationship is with the attacker, not with the legitimate user. The principal may not notice until something goes wrong.

**Recommended treatment.** Documentation change. Add to the pairing section: "Pairing with a compromised device." Note that the protocol cannot detect this; the mitigation is user vigilance and out-of-band verification of the paired device's identity.

## 2.2 Identity state consistency failures

### 2.2.1 Identity document rollback via stale cache

**Description.** A verifier has an old identity document cached. The issuer has published a newer document, but the verifier has not received it. Two verifiers can disagree about the current identity state.

**Consequence.** Inconsistency between verifiers. A verifier that has the new state may accept an object that another verifier rejects, or vice versa.

**Recommended treatment.** Documentation change. Add to the verifier model: "State freshness." Describe how a verifier detects that its cached identity state is stale (a peer presents a signature it cannot verify, or a stream-resolution appears for a sequence the verifier does not have) and what it does about it (query multiple rendezvous servers, ask the peer directly).

### 2.2.2 Identity document chain pruning

**Description.** A principal with many root rotations has a long identity chain. A verifier joining recently does not want to download the entire history.

**Consequence.** Without pruning, verifiers must download and verify every historical document to establish the current state.

**Recommended treatment.** Documentation change. Make explicit that a verifier can bootstrap trust from any `IdentityContinuity` object whose `previous_root` is already trusted. This allows history to be compressed — the verifier does not need the full chain.

### 2.2.3 Service identity and root key rotation

**Description.** Service identities are bound to a principal via service bindings. When the root rotates, does the service identity survive?

**Consequence.** If the service identity does not survive root rotation, service authorization must be re-established after every rotation, which is expensive and error-prone.

**Recommended treatment.** Documentation change. Add to the service identity section: "Service identities survive root key rotation, because they are bound to the principal's Peer ID, not to the root key."

## 2.3 Pairing failures

### 2.3.1 Pairing code interception

**Description.** An attacker obtains the code (photographs the QR code, intercepts the message, overhears the voice call) before the legitimate peer uses it.

**Consequence.** If the attacker uses the code before the legitimate peer, the sharing peer may accept a pairing with the attacker. The code is single-use, so the legitimate peer is blocked until the code expires.

**Recommended treatment.** Documentation change. Add to the pairing section: "Pairing code interception." Note that PAKE protects against a passive observer but not against an active attacker who obtains the code first. The mitigation is short code lifetimes, single-use codes, and the human confirmation step on the receiving side.

### 2.3.2 Pairing code brute force

**Description.** An attacker attempts to guess a six-digit code by trying many codes in sequence.

**Consequence.** If the code space is 20 bits and the code is valid for 5 minutes, and the attacker can try codes quickly, the code could be found by brute force.

**Recommended treatment.** Documentation change. Add to the pairing section: "Code brute-force resistance." Note that pairing attempts must be rate-limited (both per-code and per-IP), and that after a small number of failed attempts the code is invalidated.

### 2.3.3 Pairing during network partition

**Description.** The two devices cannot reach each other or the rendezvous server during Phase 2 (authentication).

**Consequence.** The authentication exchange cannot complete, and the pairing fails.

**Recommended treatment.** Documentation change. Add to the pairing section: "Pairing during network partition." Note that pairing requires connectivity between the two devices or through a rendezvous. If no connectivity exists, the pairing cannot proceed and the user should retry when connectivity is available.

### 2.3.4 Pairing confirmation abuse

**Description.** An attacker who can trigger a pairing prompt on the receiving device could trick the user into confirming a pairing with the attacker.

**Consequence.** If the user confirms, the attacker gains a relationship.

**Recommended treatment.** Documentation change. Add to the pairing section: "Confirmation abuse." Note that confirmation prompts should display enough information for the user to verify the pairing is expected (device name, other user's identity if available), and that unsolicited prompts should be treated with suspicion.

## 2.4 Authorization and lease failures

### 2.4.1 Grant issuer disappearance

**Description.** The issuer of a grant disappears (goes offline permanently, shuts down, loses their key). Existing leases continue to work until they expire, but no new leases can be issued.

**Consequence.** The subject's access ends when the last lease expires. This is by design — the design does not permit an intermediary to issue new leases on behalf of the issuer.

**Recommended treatment.** Documentation change. Add to the authorization section: "Issuer disappearance." Describe the failure mode and note that the mitigation is grant re-issuance by a new authority, which requires the subject to obtain a new grant from a different source.

### 2.4.2 Lease renewal race condition

**Description.** A lease is about to expire and both the issuer and the subject attempt to renew it simultaneously.

**Consequence.** Ambiguity about which lease is current. Without explicit semantics, different verifiers could evaluate the same subject differently.

**Recommended treatment.** Documentation change. Add to the lease section: "Lease renewal semantics." Describe how renewal handles concurrent attempts and how in-flight leases interact with new ones.

### 2.4.3 Grant expiration vs. lease expiration mismatch

**Description.** A grant has a validity interval. A lease has a validity interval. If the grant expires before the lease, the lease's authority is gone even though the lease itself has not expired.

**Consequence.** Without explicit semantics, implementations may disagree about whether an expired grant invalidates its leases.

**Recommended treatment.** Documentation change. Add to the lease section: "Lease validity depends on grant validity." Make explicit that an expired grant invalidates all its leases regardless of the lease's own validity.

### 2.4.4 Revocation effect on active sessions

**Description.** A grant is revoked while a session is active.

**Consequence.** Ambiguity about whether the session terminates immediately or continues until the next authorization check.

**Recommended treatment.** Design decision. Specify whether revocation terminates active sessions immediately or lets them complete. The current design implies "the session continues until the next authorization check," but this should be normative.

## 2.5 Rendezvous and discovery failures

### 2.5.1 Rendezvous server data loss

**Description.** A rendezvous server loses its database (disk failure, misconfiguration). All records are gone.

**Consequence.** Peers that published to it must republish. Peers that query it get nothing and must query elsewhere.

**Recommended treatment.** Documentation change. Add to rendezvous operations: "Server data loss." Note that rendezvous servers should use persistent storage, and that peers should detect server failure and republish elsewhere.

### 2.5.2 Rendezvous server selective denial of service

**Description.** An attacker with access to a rendezvous server suppresses records for specific peers while serving records for others.

**Consequence.** Peer A becomes unreachable to peer B while remaining reachable to peer C. This is difficult to detect from any single query.

**Recommended treatment.** Documentation change. Add to the rendezvous trust model: "Selective denial of service." Note that the mitigation is to use multiple rendezvous servers and to compare responses.

### 2.5.3 Rendezvous server impersonation

**Description.** An attacker runs a server that impersonates a legitimate rendezvous server. Queries are routed to the impostor.

**Consequence.** The impostor cannot serve false records (records are signed), but can log queries and can refuse to serve legitimate records.

**Recommended treatment.** Documentation change. Add to the rendezvous trust model: "Rendezvous impersonation." Note that the defense is HTTPS with certificate verification, and that rendezvous servers should be authenticated by their TLS certificate.

### 2.5.4 All rendezvous servers for a peer go offline

**Description.** All rendezvous servers a peer has published to become unreachable simultaneously.

**Consequence.** The peer becomes undiscoverable. Other peers cannot find its current endpoint.

**Recommended treatment.** Documentation change. This is the fundamental discovery limitation described in the Discovery Roadmap. Add explicit guidance: implementations should implement rendezvous failover behavior (peers detect failure and republish to alternative servers), and users should maintain multiple rendezvous servers in a peer's manifest.

## 2.6 Transport and relay failures

### 2.6.1 Relay ticket replay

**Description.** An attacker captures a relay ticket and attempts to reuse it.

**Consequence.** If the ticket is not properly bound to the source and destination, the attacker may be able to use it.

**Recommended treatment.** Documentation change. Add to the relay section: "Ticket replay." Note that tickets are pair-bound and single-use (or session-bound), and that replays from a different source or destination fail.

### 2.6.2 Relay compromise during active session

**Description.** A relay is compromised while a session is in progress.

**Consequence.** The relay can drop traffic, inject traffic (which will be rejected by transport encryption), or observe metadata. It cannot read content or change authorization.

**Recommended treatment.** Documentation change. Add to the relay compromise section: "Effect on active sessions." Note that compromise affects availability and metadata, not content or authorization.

### 2.6.3 Transport downgrade

**Description.** An attacker MITMs the connection and attempts to downgrade to a weaker transport.

**Consequence.** If the downgrade succeeds, the session may be less secure than intended.

**Recommended treatment.** Documentation change. Add to the transport section: "Transport selection." Note that transport selection is implementation policy, and that downgrade attacks are mitigated by refusing to negotiate downward without explicit configuration.

## 2.7 Local state failures

### 2.7.1 Local state corruption

**Description.** Security-significant state is corrupted (power loss during write, disk failure, memory corruption).

**Consequence.** Without proper handling, corrupted state can lead to incorrect authorization decisions.

**Recommended treatment.** Documentation change. Add to the local state section: "State corruption." Note that corrupted state requires re-establishing trust from scratch (re-pairing), and that implementations should use atomic writes and checksums to minimize the risk.

### 2.7.2 Clock rollback

**Description.** The monotonic clock itself rolls back (hardware failure, VM migration).

**Consequence.** Relative validity calculations based on monotonic time may be incorrect.

**Recommended treatment.** Documentation change. Add to the time semantics section: "Monotonic clock failure." Note that if the monotonic clock is unavailable or unreliable, the verifier should refuse to evaluate relative validity rather than falling back to wall-clock time.

### 2.7.3 Memory exhaustion during verification

**Description.** An attacker sends objects that are structurally valid but consume excessive memory (huge arrays, deeply nested structures).

**Consequence.** The verifier runs out of memory and crashes.

**Recommended treatment.** Documentation change. Add to the implementation requirements: "Resource limits." Specify maximum object sizes, maximum nesting depth, and maximum field counts. An implementation that does not enforce these is vulnerable to resource exhaustion.

## 2.8 Protocol evolution failures

### 2.8.1 Version confusion

**Description.** Two peers speak different protocol versions.

**Consequence.** Without explicit handling, they may silently misinteroperate.

**Recommended treatment.** Documentation change. Add to the versioning section: "Version negotiation." Note that V1 has no version negotiation; a peer that does not understand a domain separator rejects the object. Future versions may add explicit version negotiation.

### 2.8.2 Deprecated object acceptance

**Description.** An object type is deprecated, but an existing implementation still supports it.

**Consequence.** The deprecated type remains usable by peers who have not updated.

**Recommended treatment.** Documentation change. Add to the deprecation section: "Handling deprecated objects." Note that existing implementations may continue to support deprecated types, but new implementations should not add support. This means deprecated types eventually become unusable as new implementations refuse to process them.

### 2.8.3 Protocol downgrade

**Description.** An attacker MITMs the connection and attempts to force both peers to use an older protocol version.

**Consequence.** If the downgrade succeeds, the session may be less secure than intended.

**Recommended treatment.** Documentation change. Add to the versioning section: "Downgrade protection." Note that V1 does not have downgrade protection; peers should prefer the highest version both can support.

## 2.9 Application integration failures

### 2.9.1 Application over-trust

**Description.** An application trusts the grid agent without verifying the connection's authorization state.

**Consequence.** The application may grant access to a peer that the grid agent would have rejected.

**Recommended treatment.** Documentation change. Add to the application integration section: "Trust boundary." Note that the grid agent provides authorization information, but the application is responsible for acting on it.

### 2.9.2 Grid agent compromise

**Description.** The grid agent is compromised.

**Consequence.** The attacker can grant access to any peer, because the agent holds the keys.

**Recommended treatment.** Documentation change. Add to the application integration section: "Agent compromise." Note that agent compromise is equivalent to OS compromise — the attacker has the keys and can grant access to anyone.

### 2.9.3 Application-level policy vs. network-level policy mismatch

**Description.** The application's policy differs from the grid layer's authorization.

**Consequence.** Ambiguity about which policy wins.

**Recommended treatment.** Documentation change. Add to the application integration section: "Policy layering." Note that the grid layer and application layer are both required — the grid layer establishes who can connect, and the application layer establishes what they can do. A request must pass both checks to be honored.

## 2.10 Operational failures

### 2.10.1 Rendezvous server operator disappearance

**Description.** The operator of a rendezvous server disappears. The server goes offline.

**Consequence.** Peers that published to it must find alternatives.

**Recommended treatment.** Documentation change. Same as the general discovery limitation.

### 2.10.2 Relay operator price change

**Description.** A relay operator raises prices significantly.

**Consequence.** Users who relied on the relay must either pay more or switch.

**Recommended treatment.** Documentation change. Add to the commercial model: "Relay price changes." Note that users can switch relays without losing identity or authorization.

### 2.10.3 Network path failure

**Description.** A network path fails between two peers and their relay.

**Consequence.** The connection is broken.

**Recommended treatment.** Documentation change. Add to the connectivity section: "Path failure." Note the failover behavior and the order in which alternatives are tried.

---

# Part 3 — Summary of recommended treatments

The failure modes above divide into three categories by severity.

**Category A — Design changes recommended.** These are cases where the current design leaves a genuine ambiguity that implementations would resolve differently.

- Revocation effect on active sessions (§2.4.4)
- The published_at timestamp on reachability records (referenced in the Discovery Roadmap)
- Explicit delegation of `IdentityContinuity` bootstrap rules

**Category B — Documentation changes recommended.** These are cases where the design is correct, but the failure mode is not documented.

- All of §2.1 (root key loss, delayed activation, partial compromise)
- §2.2 (state freshness, pruning, service identity rotation)
- §2.3 (pairing code interception, brute force, network partition, confirmation abuse)
- §2.4.1 through §2.4.3 (issuer disappearance, renewal races, grant/lease mismatch)
- §2.5 through §2.7 (rendezvous, transport, local state failures)
- §2.8 through §2.10 (protocol evolution, application, operational)

**Category C — Already documented, cross-reference only.** These failure modes are covered in the archive but would benefit from explicit cross-references.

- The discovery limitation (already in the Discovery Roadmap)
- The Identity Root compromise limitation (already in the security model)

## 3.1 Suggested document structure

To keep the archive navigable, the following structure is suggested for the failure modes.

- **`KNOWN-LIMITATIONS.md`** — a single document listing every known limitation, its severity, its mitigation, and the section of the archive it relates to. This is the entry point for someone reviewing the design's honesty about what it does not solve.
- **`PAIRING.md`** — a standalone document describing the pairing model in detail, as above. Referenced from the master archive's pairing section.
- **Inline additions** to the master archive — the design changes and documentation additions described above, integrated into the sections they relate to.

## 3.2 What the failure modes list is not

The list above is not a bug list. The protocol is not defective because it has failure modes. Every protocol has failure modes. The list is a *catalog* of what the design does not solve, so that reviewers can see that the design's author knew about the failure modes and made deliberate choices about how to handle them.

The design's position is:

- Failures that are handled by the protocol are handled correctly.
- Failures that are not handled are named, explained, and deferred.
- Failures that are inherent limits of the design are documented as such.

A design that enumerates its own failure modes is more credible than one that does not. This document is intended to make that enumeration explicit.

---

# End of Addendum

This addendum is complete. It should be stored alongside the other three documents as `ADDENDUM-FAILURE-MODES.md`. Together, the four documents provide:

- **Master Archive** — the map of the protocol
- **Detailed Reference Addendum** — the specifics
- **Design Defense Addendum** — the argument
- **Failure Modes and Pairing Addendum** — the honest accounting of what the design does not solve
