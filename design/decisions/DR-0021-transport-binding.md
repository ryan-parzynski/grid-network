---
title: "Grid Network — Transport binding"
status: PROPOSED (not ACCEPTED as of 2026-10-11)
version: 2026-10-11 (review)
date: 2026-10-11
id: D-21
severity: Low
blocks: EXT
linked_finding: M4
opened: 2026-10-11
deciders: (pending acceptance)
---

# D-21

> **Status:** PROPOSED — NOT ACCEPTED.



## Context / Problem

Objects are signed and chained at the protocol level, but transport is
separate (§11.4). A device connects via WireGuard today and IPv4 relay
tomorrow. How does reachability state bind to a transport session? Are
sessions bound to a ReachabilityRecord? Can an endpoint hint be used across
multiple transports?

## Options considered

Option A: Sessions are transport-agnostic; endpoints are hints only

  A ReachabilityRecord carries an endpoint (IP/port/transport type) as a hint.
  Applications connecting to a peer use any transport; the hint is advisory.
  If the hint is stale, connection falls back to another endpoint or relay.
  No session is signed to a specific transport.

  Pros:
    - Flexible: applications can change transports without re-negotiation.
    - Simple: no session-binding protocol.
    - Robust: stale endpoint hints do not break connectivity.

  Cons:
    - Endpoints leak metadata (ISP, region, uptime pattern).
    - No way to ensure a peer is "always reachable at this endpoint."
    - Replay attacker could serve old endpoints.

Option B: Reachability records are transport-specific and strictly
time-bounded

  A ReachabilityRecord is valid only for the transport and endpoint named.
  Sessions must re-verify reachability before switching transports. Endpoint
  freshness is critical.

  Pros:
    - More control: explicit per-transport validity.

  Cons:
    - Heavier: verifier must check reachability on transport switch.
    - More state: multiple records per device (IPv4, IPv6, relay, etc.).

## Recommendation (PROPOSED — NOT DECIDED)

> **PROPOSED:**

Accept Option A (transport-agnostic, endpoints are hints). Aligns with the
principle that "connectivity failure does not change authorization state."
Add a note in the wire protocol: endpoints are advisory; verifiers MUST NOT
reject a connection solely because the endpoint differs from the hint.

## Consequences

- §11.2: clarify endpoint semantics ("advisory hint, not ground truth").
  - Wire protocol (separate document): connection fallback logic when the
    endpoint hint fails.
  - Test vectors: successful connection to an endpoint; fallback when
    unreachable.

================================================================================
