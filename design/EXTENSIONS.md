# Grid Network — Extensions

**Revision:** 2.5
**Protocol version:** v0.6.3

This document describes features that are not in the current protocol
version. Each carries a status word: `planned`, `deferred`, or
`unscheduled`.

It is non-normative. A feature described here is not a commitment.

---

## Status words

- **`planned`** — the design is defined, the implementation is
  scheduled. The design below is the intended shape.
- **`deferred`** — the design is defined, the implementation is not
  scheduled. The feature is not in the roadmap.
- **`unscheduled`** — the design is not defined. The feature is a
  direction, not a plan.

---

## Multipath connectivity

**Status:** planned

**Concept.** Use multiple network paths simultaneously to increase
throughput, reduce latency, or tolerate failures.

**Design sketch.** A `PathSet` abstraction. A verifier uses direct
paths and relay paths in parallel. Sequence numbers per path are used
to reorder delivery at the endpoint. Congestion control is per path.
Retransmission uses the fastest path.

**Constraints on the current protocol that preserve multipath.** Every
relay ticket carries a throughput bound. Every relay ticket is
pair-bound. Reachability records support multiple endpoints. Relay
selection is not encoded in any signed object.

**Open questions.** Duplicate delivery at the application layer.
Sequence-number synchronization across paths. Acceptable latency
difference between paths.

---

## Metadata minimization

**Status:** planned

**Concept.** Reduce what rendezvous and relay infrastructure can
observe about which peers are communicating.

**Design sketch.** Rotating pseudonyms for lookups. Encrypted
query-response pairs. Obfuscated timing.

**Trade-off.** Higher latency, higher bandwidth, less observable.

---

## Chain-extension proofs

**Status:** planned

**Concept.** Skip-ahead verification of long streams.

**Design sketch.** A cryptographic commitment that proves the validity
of intermediate objects without revealing them. A verifier downloads
the commitment and verifies only the endpoints.

**Benefit.** Faster verification for long-lived streams. A stream with
a thousand leases can be verified in constant time rather than linear
time.

**Design question.** How does the verifier trust the commitment
without the intermediate objects?

---

## Service ownership transfer

**Status:** planned

**Concept.** Transfer a service from one principal to another.

**Design sketch.** An authenticated transfer object signed by both
principals. A rule for what happens to outstanding grants. A rule for
in-flight leases.

**Open questions.** What authority decides that a transfer is valid?
What happens to grants that reference the old principal?

---

## Rendezvous federation

**Status:** planned

**Concept.** Rendezvous servers replicate records to a small set of
peer servers. A record published to one server is available at its
federation peers.

**Design sketch.** Each rendezvous server maintains a list of
replication peers. Publication replicates to peers. A lookup that
misses locally is forwarded to federation peers.

**Benefit.** A record survives the loss of the server it was published
to. Discovery is more robust.

**Design analogy.** Matrix homeserver federation.

---

## Rendezvous gossip

**Status:** planned

**Concept.** Rendezvous servers periodically exchange state with a
random subset of other servers. Over time, all servers converge on the
current state.

**Design sketch.** Each server sends its newest records to a random
subset of peers each round. Servers accept and re-gossip. Convergence
is eventual.

**Benefit.** More robust than federation. A record survives the loss of
multiple servers.

**Design analogy.** BitTorrent trackerless torrents.

---

## DHT-based discovery

**Status:** planned

**Concept.** Store reachability records at specific nodes determined
by hashing the peer ID. A lookup routes through the DHT to the
responsible node.

**Design sketch.** A peer publishes to the DHT node responsible for its
ID. A lookup routes to the same node.

**Trade-off.** Fully decentralized. Lookup latency is seconds, not
milliseconds. Trust assumptions change; peers store records for other
peers.

**Design analogy.** The IPFS DHT.

---

## Post-quantum signature suite

**Status:** planned

**Concept.** A post-quantum signature algorithm alongside Ed25519.

**Design sketch.** Identity documents carry a signature suite
identifier. Transition is via `IdentityContinuity` from an Ed25519 root
to a post-quantum root.

**Open questions.** Which algorithm. Whether the identity document
schema needs a suite field in the current protocol version to
facilitate transition.

---

## Threshold recovery

**Status:** planned

**Concept.** Split the Identity Root key into shares so that a
threshold of shares is required to sign.

**Design sketch.** An M-of-N threshold scheme. Recovery from root
compromise requires M shares. A single stolen share does not compromise
the principal.

**Benefit.** Root compromise requires stealing multiple shares.

**Design analogy.** Not directly analogous to any prior system in the
lineage. Closest to Shamir secret sharing.

---

## Hardware-backed root keys

**Status:** unscheduled

**Concept.** Store the Identity Root private key in a hardware security
module or secure element.

**Design sketch.** Undefined.

**Benefit.** Root key compromise requires physical access to the
hardware.

---

## Delegated authorization trees

**Status:** unscheduled

**Concept.** A principal may delegate authorization authority to a
tree of subordinates.

**Design sketch.** Undefined.

**Benefit.** Organizations can scope authorization without sharing the
root key.

---

## Anonymity transport

**Status:** unscheduled

**Concept.** Route traffic through anonymity-preserving paths.

**Design sketch.** Undefined.

**Note.** The protocol is not an anonymity network. An anonymity
transport would be an optional layer above the protocol, not a change
to the protocol itself.