# Grid Network

> **AI-assisted creation.** This specification was developed with
> substantial assistance from large language models. Human
> authorship directed the design, reviewed the drafts, and made
> the editorial decisions. The specification's content should be
> evaluated on its technical merits. Where a claim is wrong, the
> provenance is not the reason.


A cryptographic identity and authorization layer that turns whatever
network connectivity exists into a usable, portable, vendor-neutral
connectivity fabric.

---

## What this is

Grid Network is a control plane for identity, authorization, and
reachability. It sits above existing transports and answers three
questions:

1. **Who is this?** A cryptographic identity, controlled by the
   participant.
2. **What are they allowed to do?** A signed authorization, verified
   locally.
3. **Where can I find them?** An ephemeral reachability record,
   refreshed as networks change.

The protocol is not a VPN, not a tunnel, and not a replacement for
WireGuard, IPv6, or any transport. It is a layer that makes identity
and authorization portable across infrastructure changes.

---

## The property that makes it different

Today, the ability to reach your own devices from anywhere is rented
from companies. Commercial mesh VPNs, tunnels, and coordination
services own the device graph, the access policies, and the
relationships. If the provider changes terms, is acquired, or shuts
down, the relationships break.

The protocol makes the relationships the durable thing and the network
the replaceable thing. A device can move between networks, change
providers, go offline for months, and its relationships survive. No
company decides whether the network exists.

This is the property no widely-adopted system provides today. It is the
design's reason to exist.

---

## Repository layout

    spec/           Normative specification
      PROTOCOL.md     Protocol rules, objects, conformance
      OBJECTS.md      Byte-level encoding, cryptographic constructions
      PARAMETERS.md   All tunable values, as symbols
      VERSIONING.md   Document and protocol versioning
      GLOSSARY.md     Terms
      SECURITY.md     Security model, blast radius, compromise response

    design/         Non-normative rationale
      RATIONALE.md    Problem, solution, developer case
      DECISIONS.md    Decision log with rationale
      REJECTED.md     Rejected approaches and reopening conditions
      LINEAGE.md      What was learned from prior systems
      EXTENSIONS.md   Planned, deferred, and unscheduled features

    operations/     Non-normative operational guidance
      RELAYS.md       Relay operation and economics
      DEPLOYMENT.md   Deployment topologies and procedures

    commercial/     Non-normative commercial model
      MODEL.md        Free tier, paid tiers, credits, funding

    docs/           Project tracking
      FOLLOW-UPS.md   Deferred work from the revision 2.2 cleanup

    REVISIONS.md    Changelog of document revisions

---

## Where to start

**If you are evaluating the protocol:** read `design/RATIONALE.md`.
It explains the problem and why the design addresses it.

**If you are implementing the protocol:** read `spec/PROTOCOL.md` and
`spec/OBJECTS.md`. Sections marked `stable` are conformance-grade.
Sections marked `under-review` carry a known defect and must not be
built against yet.

**If you are operating infrastructure:** read `operations/RELAYS.md`
and `operations/DEPLOYMENT.md`.

**If you are integrating the protocol into an application:** read
`design/RATIONALE.md` §5 and `spec/PROTOCOL.md` §13.

**If you want to know why a specific decision was made:** read
`design/DECISIONS.md`. If you want to know why an approach was
rejected, read `design/REJECTED.md`.

---

## Status

**Document revision:** 2.3
**Protocol version:** v0.6.3

The specification is a living document. Sections marked `stable` are
conformance-grade and will not change without a protocol-version bump.
Sections marked `under-review` carry a known defect or open question.
Unmarked sections are the default state.

No reference implementation is available yet. No test vectors have been
published. The protocol is in a documentation and design phase.

---

## What the protocol is not

- Not a decentralized VPN. It is a control plane above transports.
- Not a DNS replacement. It maps identities to reachability, with
  authorization.
- Not an anonymity network. Peers are identified. Metadata is visible
  to infrastructure operators.
- Not a blockchain. No consensus, no ledger, no token.
- Not a peer-to-peer file system. No distributed storage.
- Not a company. No operator, no owner, no central authority.
- Not affiliated with any operator, provider, or organization.
- Not a standards-body publication. It is a project document.
- Not a security certification. It describes a design; it does not
  assert that the design has been verified against any threat model
  beyond the one in the specification.
- Not a governance document. Any governance structure is external.
- Not a specification for a specific product or implementation.

---

## How to participate

The specification is open. Contributions are welcome as review,
critique, or proposed patches. Every change is recorded in
`REVISIONS.md`.

The protocol is designed to be implementable by anyone, operable by
anyone, and replaceable at every infrastructure layer.

---

## License

See `LICENSE.md`.