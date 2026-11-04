# Grid Network — Commercial Model

**Revision:** 2.6
**Protocol version:** v0.6.3

This document is non-normative. It describes a commercial model that
funds protocol maintenance and infrastructure operation. Where this
document and the Protocol Specification conflict, the Protocol
Specification governs.

---

## 1. The principle

The free tier is real. Paid tiers get priority, not access.

This inverts the standard software-as-a-service model. In the standard
model, the free tier is crippled and the paid tier restores
functionality. In this model, the free tier is fully functional and
the paid tier adds guarantees.

The reason is that free users make the network valuable. They
contribute reachability, peer-to-peer efficiency, local relays, and
ecosystem gravity. Without them, there is nothing distinctive to sell
to paying users.

---

## 2. Free tier

A free user receives:

- Full protocol functionality.
- Unlimited rendezvous queries, subject to rate limits.
- Unlimited relay usage, subject to fair-share limits.
- No account requirement.
- No payment information.

Limits:

- Fair-share bandwidth: `DEFAULT_FREE_TIER_LIMITS`.
- Best-effort relay priority.
- Rate limit: `DEFAULT_FREE_RATE_LIMIT`.

A typical free user runs a self-hosted service, shares it with a small
group, and uses a public relay for fallback when direct connection
fails. The relay provides a small share of bandwidth; direct
connections provide the primary path.

The cost to an operator of supporting a free user is small. The value
to the free user is substantial.

---

## 3. Standard tier

A standard user receives:

- Guaranteed minimum relay bandwidth: `DEFAULT_STANDARD_MIN_BPS`.
- Priority queuing above free users.
- Higher rate limit: `DEFAULT_STANDARD_RATE_LIMIT`.
- Monthly uptime SLA: `DEFAULT_STANDARD_SLA_UPTIME`.

The standard tier is for users whose use of the network is significant
enough that best-effort bandwidth is insufficient. Typical use: a
self-hosted media or file server with regular remote access.

---

## 4. Priority tier

A priority user receives:

- Guaranteed minimum relay bandwidth: `DEFAULT_PRIORITY_MIN_BPS`.
- Highest priority queuing.
- Latency bound: `DEFAULT_PRIORITY_SLA_LATENCY`.
- Uptime SLA: `DEFAULT_PRIORITY_SLA_UPTIME`.

The priority tier is for deployments where reliability and latency
matter to a business function. Typical use: a small organization's
internal services.

---

## 5. Dedicated tier

A dedicated user receives:

- Guaranteed capacity, per agreement.
- Private relay if desired.
- Highest priority.
- Uptime SLA: `DEFAULT_DEDICATED_SLA_UPTIME`.
- Support and integration services.

Pricing is custom. The dedicated tier is for enterprises whose
reliance on the network justifies an explicit contract.

---

## 6. Idle capacity

When paid users do not use their reserved capacity, the idle capacity
flows to the free pool.

For example, an operator with 100 Gbps of total capacity might reserve
20 Gbps for free users, 40 Gbps for standard, 30 Gbps for priority, and
10 Gbps for dedicated. During off-peak hours, the standard, priority,
and dedicated reservations are not fully used. The unused capacity is
available to free users.

This model:

- Ensures free users have bandwidth.
- Does not penalize paid users; their reservations are guaranteed.
- Encourages overprovisioning, because more capacity means more free
  capacity during troughs.
- Aligns operator incentives with network value.

---

## 7. Credit pools

Users may share relay credits in a pool. A family, a household, or a
small group can contribute to a single pool and allocate credits among
the participants.

Rules:

- Credits are allocated to a pool.
- Pool operators manage distribution.
- Credits are not transferable between pools.
- Credits are account-specific.

The pool model preserves the sharing benefit without introducing
laundering, regulatory, or tax complications.

---

## 8. Fair exchange

Credits are earned by contribution and spent on usage.

Contribution:

- Running a relay: credits earned per byte forwarded.
- Running a rendezvous server: credits earned per query served.
- Publishing reachability: credits earned per unit of time.

Exchange:

- `CREDIT_TO_GB_RATIO` defines the base rate.
- Geographic multipliers adjust the rate for scarce regions.

A user who runs a home relay earns credits that offset their own relay
usage. A user who runs a large relay earns credits that may exceed
their own usage.

---

## 9. Geographic scarcity

Some regions have many relays; others have few. A region with high
demand and low supply needs more relays. The multiplier draws
infrastructure to where it is needed.

Defaults:

- `GEOGRAPHIC_MULTIPLIER_ABUNDANT` for regions with abundant relays.
- `GEOGRAPHIC_MULTIPLIER_SCARCE` for regions with few relays.
- `GEOGRAPHIC_MULTIPLIER_VERY_SCARCE` for regions with very few relays.

The multipliers are set by the operator's policy. The protocol does not
define them. The defaults are illustrative.

An operator in a scarce region earns more per byte. A new operator
deploying in a scarce region earns more than a new operator deploying
in an abundant one. The effect is to balance supply across regions.

---

## 10. Developer funding

Commercial operators contribute a fraction of revenue to developer
funding. The default fraction is `DEFAULT_DEVELOPER_FUND_SHARE`.

The fund supports:

- Protocol specification maintenance.
- Test vector production.
- Security audits.
- Documentation.
- Community support.

A structural revenue share is preferred to donations and grants
because it scales with adoption and provides predictable funding.

---

## 11. Stewardship

A stewardship entity, independent of any commercial operator, maintains
the specification.

The entity's responsibilities:

- Maintain the protocol specification.
- Produce and maintain test vectors.
- Conduct security audits.
- Manage the change process.
- Arbitrate disputes among operators.

The protocol does not define the entity's composition, funding, or
authority. Those are external concerns. The specification is
maintained by whoever has the authority to publish revisions; the
stewardship entity is one possible arrangement.

The protocol's design does not depend on the entity's existence. A
deployment that runs its own rendezvous servers and relays is
functional without any operator or stewardship arrangement.

---

## 12. What operators sell

Operators do not sell:

- Access to the network. The protocol is open.
- Device identity. Identity belongs to the user.
- Relationship data. Relationships are on the user's devices.
- Authorization grants. Grants are signed by the user.

Operators sell:

- Reliability, through uptime and latency guarantees.
- Bandwidth, through reserved capacity.
- Geographic placement, through relays near the user.
- Support, through responsive assistance.
- Integration, through custom setups.
- Compliance, through audit logs and standards certifications.

The distinction is that the user owns everything of substance. The
operator provides infrastructure quality.

---

## 13. The economic shape

The network grows in a cycle:

1. Free users make the network valuable.
2. Developers see value and integrate the protocol.
3. Applications adopt the protocol, bringing more users.
4. A larger user base attracts more operators.
5. Operators contribute to developer funding.
6. Funding improves the protocol.
7. Improvements attract more free users.

Each layer funds the next. The cycle is self-reinforcing when the
protocol is useful and the operators are reliable.

---

## 14. What changes if the model succeeds

If the protocol is widely adopted:

- Device identity becomes a commodity rather than a paid product.
- Competition shifts from lock-in to quality.
- Smaller operators can enter the market without central coordination.
- Users can switch providers without losing relationships.
- Providers that offer genuinely better service survive; providers that
  rely on lock-in do not.
- New categories emerge: hardware with protocol support built in,
  managed infrastructure for users who do not wish to self-host,
  integration services for enterprises.

What does not change:

- The protocol remains open.
- Identity remains portable.
- No operator becomes mandatory.
- No user is required to pay for basic functionality.