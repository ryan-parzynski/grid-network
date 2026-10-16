# Grid Network — Rendezvous Operation Guide

**Revision:** 2.2
**Protocol version:** v0.6.3

**Repository path:** `operations/RENDEZVOUS.md`

This document is non-normative. It describes how to operate a
rendezvous server for the Grid Network. Where this document and the
Protocol Specification conflict, the Protocol Specification governs.

---

## 1. What a rendezvous server is

A rendezvous server stores ephemeral protocol state on behalf of peers.
It accepts reachability records, identity documents, and continuity
objects, and serves them on request. It does not define identity,
grant authorization, decide policy, or store authorization state.

A rendezvous server is replaceable. A peer that uses one may switch to
another without changing identity, relationships, or grants.

---

## 2. What a rendezvous server stores

| Object type | TTL | Notes |
|---|---|---|
| `ReachabilityRecord` | `DEFAULT_REACHABILITY_TTL` | Ephemeral. Not persisted beyond TTL. |
| `IdentityDocument` | Until superseded | The most recent document for each Peer ID. |
| `IdentityContinuity` | Retained | Required so verifiers can walk from an old anchor. |

The server does not store grants, leases, relationships, or any other
authorization state.

---

## 3. Publication endpoints

The wire protocol is specified in a future revision. The endpoints
described below are the interface a rendezvous server exposes to
peers.

### 3.1 Reachability records

- `POST /v1/reachability` — publish a reachability record.
- `GET /v1/reachability/{device_id}` — fetch the current record for a
  device.

### 3.2 Identity documents

- `POST /v1/identity` — publish an identity document. May include the
  continuity chain from the publisher's previous anchor.
- `GET /v1/identity/{peer_id}` — fetch the current document for a
  peer.
- `GET /v1/identity/{peer_id}/chain` — fetch the continuity chain.

### 3.3 Operator manifest

- `GET /v1/manifest` — fetch the rendezvous operator's manifest,
  declaring `serves_identity_state` and `current_relay_authority_key`.

All endpoints use HTTPS with certificate verification.

---

## 4. Trust model

A rendezvous server is untrusted. It can:

- Serve stale records.
- Serve false records.
- Deny service.
- Observe query patterns.

A rendezvous server cannot:

- Forge identity documents.
- Forge reachability records.
- Change authorization.
- Impersonate a peer.
- Decrypt content.

The protection against a stale record is the record's signature and
`identity_sequence`. The protection against a false record is
signature verification. The protection against denial of service is
multiple providers.

---

## 5. Persistence

A rendezvous server should persist its state to durable storage. The
state is signed by its publishers; persistence is a convenience for
availability, not a trust mechanism.

If a rendezvous server loses its state, its peers republish. Peers
should detect server failure and republish to an alternative server.

---

## 6. Rate limiting

A rendezvous server should rate-limit:

- Publications per peer per interval.
- Lookups per requester per interval.
- Failed authentications per source per interval.

The rate limits are policy; the protocol does not define them.
Defaults are in `spec/PARAMETERS.md`.

---

## 7. Capacity planning

State per peer:

- Reachability records are a few hundred bytes each. A single record
  per device.
- Identity documents are larger, a few kilobytes each, with growth
  proportional to the number of devices and services the principal
  has.
- Continuity chains grow with the number of root rotations. A chain of
  ten rotations is a few tens of kilobytes.

For a server handling a million peers with one device each, storage is
on the order of a few gigabytes. Publication traffic is proportional
to the number of peers times the publication frequency. Reachability
records are republished once per TTL. Identity documents are
republished only when they change.

Bandwidth is dominated by lookups, not publications, at typical use
ratios.

---

## 8. Availability

A rendezvous server may be unavailable for maintenance, failure, or
policy reasons. Peers should maintain at least two rendezvous servers
in their `RendezvousManifest`. A peer whose list becomes empty is
undiscoverable until it publishes to an available server.

---

## 9. Federation

Federation between rendezvous servers is a `planned` feature. In the
current protocol version, a rendezvous server is a standalone store.

A peer that wants redundancy publishes to multiple servers
independently. A verifier that wants redundancy queries multiple
servers.

---

## 10. Impersonation

A rendezvous server is authenticated by its TLS certificate. A peer
that connects to an impostor will not receive valid records, because
the impostor cannot forge signatures. However, an impostor can log
queries and deny service.

Mitigations: use a rendezvous server whose TLS certificate you trust,
or use multiple providers.

---

## 11. Selective suppression

A malicious rendezvous server can suppress specific records while
serving others. Peer A becomes unreachable to peer B while remaining
reachable to peer C. This is difficult to detect from a single query.

Mitigation: query multiple rendezvous servers and compare responses. A
verifier that finds a mismatch treats the record as unverified and
refreshes from the peer directly if possible.

---

## 12. Data loss

A rendezvous server that loses its data does not lose anything
irreplaceable. Publishers republish. Verifiers use alternative servers
or cached state.

The server should not treat data loss as a security event. It is an
availability event.

---

## 13. Operational monitoring

A rendezvous operator should monitor:

- Publication success rate.
- Lookup latency and success rate.
- Rate-limit hit rate.
- Storage growth.
- Peer count and record count.

The data belongs to the operator. The protocol does not export it and
does not require it to be shared.

---

## 14. Cost

The dominant cost of operating a rendezvous server is bandwidth. The
data is tiny, but queries are frequent. A server that serves a large
population of verifiers will see many more reads than writes.

Storage cost is negligible at typical scale. The server can run on
modest hardware: a single virtual machine or a low-cost dedicated
server is sufficient for a large number of peers.