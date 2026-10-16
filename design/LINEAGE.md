# Grid Network — Lineage

**Revision:** 2.6
**Protocol version:** v0.6.3

This document records what the protocol learned from prior systems. It
is non-normative. Its purpose is to credit prior work, to explain which
mechanisms were borrowed and why, and to identify where the design
departs from its predecessors.

The protocol is not novel in its parts. Its novelty is in the
composition.

---

## DNS

DNS solves the problem of finding services by name through untrusted
resolvers.

**Borrowed.** The resolver model, in which queries are answered by
servers the requester does not necessarily trust. Cache semantics that
do not require trust in the source. The TTL concept for ephemeral data.

**Departed.** DNS names are mutable; a name can be pointed at a new
address. Grid Peer IDs are immutable. DNS authority is hierarchical,
with a root; Grid authority is flat. DNS names are human-readable;
Grid identifiers are opaque.

**Why.** Mutable names enable hijacking. Hierarchical authority enables
censorship. The design chose immutability and flat authority to prevent
both.

**Contribution.** Mutable location with immutable identity.

---

## WireGuard

WireGuard solves tunnel encryption and authentication with a small,
auditable implementation.

**Borrowed.** Cryptographic simplicity. The choice of Ed25519 rather
than RSA or ECDSA. Key-based identity rather than certificate-based
identity. Stateless verification.

**Departed.** WireGuard is a transport. Grid is a control plane above
transports. WireGuard's identity has no lifecycle; Grid's identity has
relationships, authorization, and rotation.

**Why.** A transport does not need relationship management. A control
plane does.

**Contribution.** Identity above transport.

---

## Bitcoin

Bitcoin solves decentralized ownership without a central authority.

**Borrowed.** Cryptographic signatures as proof of ownership.
Hash-chain verification that detects tampering. Decentralized
verification without a central server. Offline verification.

**Departed.** Bitcoin uses consensus; Grid uses local verification.
Bitcoin has a global ledger; Grid has local caches. Bitcoin requires
proof-of-work; Grid uses signatures.

**Why.** Consensus is expensive and unnecessary for Grid's use case.
A global ledger creates privacy problems. Proof-of-work has an
environmental cost that is disproportionate.

**Contribution.** Offline verification without consensus.

---

## Tailscale

Tailscale (a commercial mesh VPN) solves the user-experience problem
of VPN setup.

**Borrowed.** QR code pairing. Automatic NAT traversal. Relays as
fallback. Per-peer authorization. Cross-platform support.

**Departed.** Tailscale is account-based. Grid is identity-based.
Tailscale has a central coordination server. Grid treats rendezvous as
replaceable infrastructure. Tailscale's protocol is proprietary; Grid's
is open.

**Why.** Accounts are easier to operate but create lock-in. Central
coordination is simpler but creates a single point of failure.
Proprietary protocols are easier to monetize but limit adoption.

**Contribution.** The same user experience with portability.

---

## Headscale

Headscale solves the problem of self-hosting a Tailscale-compatible
coordination server.

**Borrowed.** The self-hosting model. A community implementation.
Privacy-first design.

**Departed.** Headscale is Tailscale-compatible, which means it
implements Tailscale's protocol and inherits its account model. Grid
is open from the start, with no compatibility requirements.

**Why.** Compatibility with a proprietary protocol limits design
freedom. The design chose freedom over compatibility.

**Contribution.** Self-hosting and portability from the start.

---

## Matrix

Matrix solves federated communication between independent homeservers.

**Borrowed.** The federation model, in which any server can
interoperate with any other. Portable identity that carries across
servers. Event signing that makes objects self-authenticating.

**Departed.** Matrix is for messaging and requires eventual
consistency. Grid is for connectivity and requires only local
verification. Matrix synchronizes state across servers; Grid does not.

**Why.** Messaging needs convergence so that all parties see the same
history. Connectivity needs only verification.

**Contribution.** Federation for the infrastructure layer.

---

## SSH

SSH solves secure remote shell access.

**Borrowed.** Trust-on-first-use pairing. Key-based identity rather
than passwords. Host key verification. Session certificates.

**Departed.** SSH is for terminal access. Grid is application-agnostic.
SSH requires manual key verification; Grid automates pairing with a
PAKE.

**Why.** Terminal access requires strong manual verification because a
single wrong command is catastrophic. Connectivity can use automation.
Manual verification scales to hundreds of servers, not to thousands of
peers.

**Contribution.** Automated PAKE with application-agnostic
authorization.

---

## Kerberos

Kerberos solves enterprise authentication.

**Borrowed.** Time-limited tickets. A trusted key server. Offline
operation using cached tickets. Terminal revocation.

**Departed.** Kerberos is enterprise-only and admin-controlled. Grid is
peer-to-peer and user-controlled. Kerberos requires wall-clock
synchronization; Grid uses relative validity.

**Why.** An enterprise has a central authority. A decentralized system
does not. An enterprise can enforce clock synchronization. A
distributed system cannot.

**Contribution.** Decentralized leases with relative validity.

---

## IPFS

IPFS solves distributed content storage and lookup.

**Borrowed.** Content addressing. Peer discovery. Multi-path routing.

**Departed.** IPFS is for immutable content. Grid is for mutable
identity. IPFS requires a DHT; Grid uses rendezvous. IPFS stores
content on arbitrary peers; Grid stores identity on the owner's chosen
rendezvous servers.

**Why.** Content addressing requires immutability. Identity requires
mutability because keys rotate and relationships change.

**Contribution.** Hash-like identification with mutability.

---

## Additional prior art

The entries below were added in revision 2.6. Each records a concept
from another system that relates to a part of Grid, where Grid differs,
and the sections of this specification that are involved. Descriptions
of the other systems are limited to the concept named. The entries do
not state that Grid derives from, equals, or improves on any of them.

---

## Keybase sigchains

A Keybase sigchain is a per-user ordered list of signed statements.
Each statement carries a sequence number and the hash of the previous
statement, and records changes such as adding or revoking a key.

**Borrowed.** A principal's key history as a signed, hash-linked
sequence in which each entry commits to its predecessor, so an entry
cannot be omitted or reordered without breaking the chain.

**Departed.** Grid divides a principal's history into several streams,
each signed by exactly one authority. Each object's signature covers
the cumulative chain hash, and two objects with the same sequence and
different chain hashes put a stream into `FORK_DETECTED` until a
`StreamResolution` is applied. A Grid Peer ID is opaque and is not
derived from a key. The specification defines no registry or log that
spans principals.

**Why.** Key rotation, revocation, and `effective_sequence` in Grid
depend on an ordered record in which each change commits to the one
before it.

**Grid sections.** `PROTOCOL.md §4`, `PROTOCOL.md §16`,
`PROTOCOL.md §19`, `PROTOCOL.md §36`, `PROTOCOL.md §47`,
`OBJECTS.md §3.8`, `OBJECTS.md §9.3`.

---

## Secure Scuttlebutt feeds

In Secure Scuttlebutt each identity has a feed: an append-only log of
messages signed by that identity. Each message carries a sequence
number and a reference to the previous message in the feed.

**Borrowed.** A per-author, append-only sequence in which each entry
carries a sequence number and a link to its predecessor, so that a
reader can check continuity.

**Departed.** A Grid stream is bound to one signing authority, and
several streams exist per principal. A verifier treats an object whose
predecessor is absent as unverifiable. Two objects at the same sequence
with different chain hashes are a fork, which a verifier does not
resolve without a `StreamResolution`. Grid objects are obtained from
rendezvous servers by pull. Rendezvous gossip is `planned`.

**Why.** Grid verification also relies on sequence continuity and
predecessor links, and verifiers work from cached signed objects
rather than from a live connection to the author.

**Grid sections.** `PROTOCOL.md §23`, `PROTOCOL.md §29`,
`PROTOCOL.md §36`, `PROTOCOL.md §46`, `OBJECTS.md §3.7`,
`OBJECTS.md §9.2`, `OBJECTS.md §9.3`.

---

## KERI

KERI (Key Event Receipt Infrastructure) describes self-certifying
identifiers, an append-only log of signed key events, a key
pre-rotation scheme, and witnesses that help detect duplicity, meaning
inconsistent statements about the same history.

**Borrowed.** Key rotation recorded as signed events in an append-only
log, and the detection of conflicting histories by comparing what
different observers have seen.

**Departed.** A Grid Peer ID is opaque and is not derived from a key;
it is bound to an Identity Root by a signed identity document. Root
rotation is recorded in an `IdentityContinuity` object signed by both
the previous and the new Identity Root. The specification defines no
pre-rotation commitment and no witness role. Grid provides no in-band
recovery from Identity Root compromise.

**Why.** Grid shares the goals of rotating keys without changing the
identifier and of detecting divergent histories. The specification
states why the Peer ID is not self-certifying: so that the Identity Root
can rotate without changing the ID.

**Grid sections.** `PROTOCOL.md §4`, `PROTOCOL.md §18`,
`PROTOCOL.md §19`, `PROTOCOL.md §42`, `OBJECTS.md §9.3`.

---

## UCAN

UCAN (User Controlled Authorization Network) describes capability-based
authorization in which an issuer signs a delegation, and delegations can
be chained, each restating or narrowing the capabilities it passes on.

**Borrowed.** Capabilities as the unit of authorization, signed by the
issuer's key, and verifiable by a party that holds the issuer's public
key.

**Departed.** A Grid `Grant` is a directional authorization between two
principals within a relationship. It is signed by an Authorization Key,
published in that key's stream, and paired with a `Lease` for freshness.
The specification defines no chaining of grants. Delegated authorization
trees are `unscheduled`.

**Why.** Grid scopes authorization by capability, and a verifier checks
signed objects against its trust anchors.

**Grid sections.** `PROTOCOL.md §8`, `PROTOCOL.md §9`,
`PROTOCOL.md §10`, `PROTOCOL.md §11`, `PROTOCOL.md §27`,
`PROTOCOL.md §33`, `PROTOCOL.md §46`.

---

## Biscuit

Biscuit is an authorization token verified with public-key signatures.
A holder can narrow a token's rights offline by appending blocks, and
authorization rules are expressed in a Datalog-based language.

**Borrowed.** Verification of an authorization by any party that holds
the issuer's public key, and the idea that rights are narrowed rather
than widened.

**Departed.** Grid defines no policy language. Capability constraints
are text-to-text maps that the protocol does not interpret, and
application authorization is outside the specification. A Grid `Grant`
is immutable; a change is a new grant. The specification defines no
holder-side narrowing of a grant.

**Why.** A Grid verifier checks signatures, streams, relationship state,
grant, lease, and revocation, and leaves resource policy to
applications.

**Grid sections.** `PROTOCOL.md §9`, `PROTOCOL.md §11`,
`PROTOCOL.md §13`, `PROTOCOL.md §27`, `PROTOCOL.md §47`.

---

## Macaroons

Macaroons are bearer credentials that carry caveats, which restrict
when, where, and by whom a target service accepts them. They are built
from a chain of nested HMAC values.

**Borrowed.** Authority restricted by explicit, contextual conditions
that travel with the credential.

**Departed.** Grid uses Ed25519 signatures, not chained HMAC values. A
`Grant` names an issuer and a subject and is not a bearer credential.
Its `constraints` and its lease policy bound it, and a lease must be
present and unexpired for access. The specification defines no way for
a holder to add conditions.

**Why.** Grid grants carry capability constraints and are paired with
time-bounded leases.

**Grid sections.** `PROTOCOL.md §9`, `PROTOCOL.md §10`,
`PROTOCOL.md §11`, `PROTOCOL.md §27`, `PROTOCOL.md §43`.

---

## Nebula

Nebula is an overlay network in which a certificate authority signs a
certificate for each node, and discovery nodes called lighthouses help
nodes find one another and optionally use UDP hole punching to connect.

**Borrowed.** A discovery role that helps peers find each other and
attempt direct connections through NATs and firewalls.

**Departed.** Grid has no certificate authority. An identity is a
self-controlled principal, and a verifier's trust anchors are its own
Identity Root and the roots of peers it recognizes through pairing.
Rendezvous servers store and serve signed records and cannot define
identity or grant authorization. Relay fallback uses signed relay
tickets.

**Why.** Rendezvous in Grid and lighthouses in Nebula both address how
peers behind NATs find each other. The specification states that
rendezvous has no authority over identity or authorization.

**Grid sections.** `PROTOCOL.md §23`, `PROTOCOL.md §25`,
`PROTOCOL.md §33`, `PROTOCOL.md §37`, `PROTOCOL.md §47`,
`DEPLOYMENT.md §3.4`.

---

## ZeroTier

ZeroTier uses root servers that peers contact first. The roots forward
initial packets and send rendezvous hints so that peers can attempt a
direct path, and traffic continues through relaying when a direct path
cannot be made.

**Borrowed.** Staged connectivity: prefer a direct path set up with
the help of infrastructure, and fall back to relaying when it fails.

**Departed.** The specification defines no fixed set of root servers. A
peer may use any rendezvous provider, several, or none, and may change
provider without changing identity. A reachability record is a signed
hint, and a verifier treats every endpoint in it as untrusted.

**Why.** Grid's connection order of direct connection, then NAT
traversal, then relay addresses the same connectivity problem.

**Grid sections.** `PROTOCOL.md §23`, `PROTOCOL.md §24`,
`PROTOCOL.md §25`, `DEPLOYMENT.md §3.1`, `DEPLOYMENT.md §3.5`.

---

## libp2p

libp2p is a modular networking stack. A peer is identified by an ID that
is conceptually a hash of its public key, and the stack supports
multiple transports.

**Borrowed.** Transport independence, and describing a peer's endpoints
as an address paired with a transport.

**Departed.** A Grid Peer ID is opaque and is not derived from a key.
Grid also specifies relationships, grants, and leases above
reachability. DHT-based discovery is `planned`; the current version
uses rendezvous servers. Grid does not select a transport.

**Why.** Grid's `Endpoint` structure and its transport-independence
statement address the same layering question.

**Grid sections.** `PROTOCOL.md §4`, `PROTOCOL.md §8`,
`PROTOCOL.md §23`, `PROTOCOL.md §24`, `PROTOCOL.md §26`,
`PROTOCOL.md §46`.

---

## Certificate Transparency

Certificate Transparency is a system of publicly auditable, append-only
logs of certificates, organized as Merkle trees. Log operators sign tree
heads, and monitors check the logs.

**Borrowed.** Append-only records whose consistency can be checked by
comparing commitments, and detection of inconsistent histories rather
than prevention of them.

**Departed.** Grid uses a hash chain per stream, not a Merkle tree, and
defines no log operator or monitor role. A verifier detects a fork when
it observes two objects with the same sequence and different chain
hashes. The specification defines no log that spans principals.
Chain-extension proofs, which would allow skip-ahead verification of
long streams, are `planned`.

**Why.** Chain-extension proofs raise the question of how a verifier
trusts a commitment without the intermediate objects. This entry
records Certificate Transparency as related background for that
planned feature. The specification defines no design for it.

**Grid sections.** `OBJECTS.md §3.8`, `OBJECTS.md §9.3`,
`PROTOCOL.md §40`, `PROTOCOL.md §46`, `PROTOCOL.md §47`.

---

## Trillian

Trillian is an open-source implementation of verifiable data
structures, including an append-only log built on a Merkle tree. It is
used to build Certificate Transparency logs.

**Borrowed.** A verifiable log kept as a component separate from the
application that defines what is logged.

**Departed.** The specification defines no log server. Rendezvous
servers store and serve signed objects, and they do not define
identity, grant authorization, or decide policy. Version v0.6.3
contains no log role.

**Why.** This entry is relevant only to the planned chain-extension
proofs. It is recorded so that a future decision on a log role can
start from the existing list of prior systems. No such decision has
been made.

**Grid sections.** `PROTOCOL.md §23`, `PROTOCOL.md §46`,
`PROTOCOL.md §47`, `OBJECTS.md §3.8`.

---

## TUF

The Update Framework (TUF) separates trust into top-level roles: root,
targets, snapshot, and timestamp. Each role can require a threshold of
signatures, metadata carries an expiration date, and one stated goal is
to limit the impact of key compromise.

**Borrowed.** Separation of key roles so that compromise of one key
affects only what that role signs, expiration as a freshness mechanism,
and thresholds as a concept for the most sensitive key.

**Departed.** Grid's key roles are Identity Root, Device Key, Service
Key, Authorization Key, and Recovery Key, with separation rules between
them, and each stream has exactly one signing authority. Grid measures lease validity from the verifier's
observation, as well as from dates in objects. Threshold signing is not
in v0.6.3; threshold recovery is `planned`.

**Why.** Grid's statement that a compromised Authorization Key affects
only the grants that key issued relies on the role-separation concept
named above.

**Grid sections.** `PROTOCOL.md §6`, `PROTOCOL.md §10`,
`PROTOCOL.md §17`, `PROTOCOL.md §18`, `PROTOCOL.md §32`,
`PROTOCOL.md §42`, `PROTOCOL.md §46`, `DEPLOYMENT.md §7.2`.

---

## Signal

Signal lets two users compare a safety number, derived from both
parties' keys, over a separate channel, to check that each holds the
other's keys.

**Borrowed.** Out-of-band comparison of a short value that both sides
derive, to detect an intermediary.

**Departed.** In Grid the verification code is derived from the PAKE
transcript. The PAKE is SPAKE2, seeded by an out-of-band secret, and
the receiving side confirms the attempt. The durable output of pairing
is a set of signed relationship assertions. Grid defines no message
encryption or ratchet; confidentiality and forward secrecy are provided
by the transport.

**Why.** Grid's human verification step during pairing addresses the
same question: whether two devices hold each other's keys.

**Grid sections.** `PROTOCOL.md §20`, `PROTOCOL.md §21.2`,
`PROTOCOL.md §21.3`, `PROTOCOL.md §21.6`, `PROTOCOL.md §26`.

---

## Noise protocol

The Noise Protocol Framework describes how to build handshake protocols
from Diffie-Hellman key agreement, using named handshake patterns.

**Borrowed.** The concept of an authenticated key-exchange handshake
assembled from defined patterns, as one way a transport can be built.

**Departed.** Grid does not select a handshake or a transport. The
protocol is transport-independent, names WireGuard, QUIC, and TLS as
options, and gives mutual authentication to the Grid layer.

**Why.** The choice of transport handshake is left to implementations.
This entry records the framework as related background for that choice.

**Grid sections.** `PROTOCOL.md §20`, `PROTOCOL.md §26`,
`OBJECTS.md §3.12`.

---

## SPIFFE

SPIFFE defines workload identifiers (SPIFFE IDs), identity documents
(SVIDs) that are valid when signed by an authority in the identifier's
trust domain, and trust bundles used to verify them.

**Borrowed.** The concept of verifying identity documents against a
set of trusted roots.

**Departed.** A Grid verifier's trust anchors are its own Identity Root
and the roots of recognized peers, established through pairing. They
are not roots published by an issuing authority. A Grid identity
document is signed by the principal's own Identity Root.

**Why.** Grid also identifies services within a principal, through a
Service Key and a `ServiceRecord`.

**Grid sections.** `PROTOCOL.md §7`, `PROTOCOL.md §33`,
`PROTOCOL.md §38`, `PROTOCOL.md §42`, `PROTOCOL.md §47`.

---

## ICE/STUN/TURN

ICE, STUN, and TURN are IETF protocols for connectivity through NATs.
STUN lets a host learn its address as seen from outside, ICE gathers
and tests candidate address pairs, and TURN relays traffic through a
server.

**Borrowed.** Candidate exchange followed by connectivity attempts,
with a relay as the last resort.

**Departed.** The NAT traversal wire specification is drafted and is
not normative, and the specification does not adopt the ICE, STUN, or
TURN message formats. Relay access is by a signed `RelayTicket` bound
to a source and destination pair. Reachability records carry endpoints
as signed hints that a verifier treats as untrusted.

**Why.** Grid's connection order of direct connection, then NAT
traversal with candidate exchange, then relay addresses the same
connectivity problem.

**Grid sections.** `PROTOCOL.md §24`, `PROTOCOL.md §25`,
`DEPLOYMENT.md §3.1`, `DEPLOYMENT.md §3.4`, `DEPLOYMENT.md §3.5`,
`ROADMAP.md §4`.

---

## QUIC

QUIC is a transport protocol that runs over UDP, integrates TLS 1.3,
and multiplexes streams within a connection.

**Borrowed.** QUIC as a transport option.

**Departed.** Grid defines no transport. QUIC appears as one of three
named transport options and as a value of the `transport` field of an
`Endpoint`. A Grid stream is an ordered chain of signed objects that
shares one sequence space. It is unrelated to a QUIC stream.

**Why.** The two uses of the word "stream" differ, and a reader who
meets both should not conflate them.

**Grid sections.** `PROTOCOL.md §24`, `PROTOCOL.md §26`,
`PROTOCOL.md §36`, `DEPLOYMENT.md §3.6`.

---

## Git

Git stores history as content-addressed objects in which each commit
records the hashes of its parent commits.

**Borrowed.** History committed by hash, so that an object's identity
depends on what precedes it and the history cannot be altered without
changing every identifier that follows.

**Departed.** A Grid stream is linear: one sequence space, strictly
increasing sequence numbers, and one signing authority. Divergent
histories are an ordinary state in Git. Two Grid objects at the same
sequence with different chain hashes are a fork, which a verifier does
not resolve automatically.

**Why.** Grid's chain hash commits to the stream history in the way a
commit commits to its parents. The treatment of divergence is the main
difference.

**Grid sections.** `PROTOCOL.md §36`, `PROTOCOL.md §40`,
`PROTOCOL.md §43`, `OBJECTS.md §3.7`, `OBJECTS.md §3.8`,
`OBJECTS.md §9.2`, `OBJECTS.md §9.3`.

---

## What is new

Each borrowed mechanism is well-proven. The composition is what is new.

The composition provides:

- Offline-verifiable leases. Kerberos assumes online operation.
- Federated identity without synchronization. Matrix requires eventual
  consistency.
- Portable credentials for mutable identity. IPFS addresses immutable
  content.
- Replaceable infrastructure. Tailscale's coordination server is not
  replaceable without leaving the ecosystem.

A system that is proven in its parts, novel in its composition, and
pragmatic in its scope.