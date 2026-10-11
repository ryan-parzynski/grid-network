# Addendum — Commercial Models, Relay Priority, Credit Pools, and Developer Funding

**Document:** `RATIONALE.md` — Addendum A
**Version:** 6.0
**Status:** Draft
**Scope:** The commercial layer only. How it funds itself. How it funds the protocol. How it expands the network rather than partitioning it.

---

## The one-sentence design principle

> Every participant — free user, contributor, commercial operator, enterprise — makes the network more valuable to every other participant. The commercial model exists to fund the protocol's maintenance and development, not to extract value from users.

This principle governs everything below. Where a commercial decision conflicts with it, the principle wins.

---

## Part I — What the commercial layer is, and is not

### 1. What it sells

The commercial layer sells **guarantees**, not access.

Free users can always connect. They get relay on a best-effort basis. Paid users get the same relay with a predictable quality level — higher priority, guaranteed capacity, consistent latency, SLA backing for enterprises.

The difference between free and paid is **predictability**, not availability. This is a critical distinction. It is the difference between "you must pay to use this" and "you can pay to use this reliably."

### 2. The relay layer's actual scope

The commercial layer exists for one purpose: relay. And relay is a fallback.

The connectivity preference order in a Mesh implementation is:

1. **Local LAN.** Direct. No relay.
2. **Direct IPv6.** Direct. No relay.
3. **Direct IPv4.** Direct. No relay.
4. **NAT traversal (hairpinning, hole punching).** Direct once established. No relay.
5. **Relay.** Direct failed. Fallback.

In a mature deployment with widespread IPv6 and working NAT traversal, most traffic never reaches step 5. Relay exists for the cases that steps 1–4 can't handle: symmetric NAT, CGNAT, corporate firewalls, hostile networks, and situations where the peer is genuinely unreachable otherwise.

In deployments where direct connectivity always works — a home LAN, an enterprise with well-connected infrastructure, a community with IPv6 throughout — the commercial layer is unused. The protocol works. No subscription, no account, no cost.

### 3. Relay is a burst absorber

The relay layer's most important function is not serving steady-state traffic. It's absorbing:

- **Network changes.** A peer moves from Wi-Fi to cellular. Direct connection is broken; relay bridges the gap.
- **Peak demand.** Many peers need relay simultaneously.
- **Outages.** A major cloud provider fails; peers that relied on direct connections now need relay.
- **Geographic variance.** A peer traveling in a region with poor connectivity.

These are inherently *variable* costs. Commercial relays are overprovisioned to handle surges. The surplus is idle most of the time and serves the free pool at no marginal cost.

### 4. The commercial layer is not a platform

A platform owns the customer's identity, data, or relationships. Mesh commercial operators own none of these. They sell services on top of the protocol. They do not own the protocol, the identity, or the relationship.

This is what forces them to compete on quality rather than on lock-in. A user can leave any operator at any time, taking their Peer ID, their relationships, and their grants with them. The only reason to stay is that the operator is genuinely better — faster, more reliable, better supported, better integrated.

This is the difference between a Mesh commercial operator and a traditional SaaS platform. A platform holds the customer's identity hostage. A Mesh operator competes on the value they add.

### 5. The one property everything rests on

The entire commercial model rests on one property: **identity is portable.**

A user's Peer ID, relationships, and grants are theirs, not the operator's. This means:

- No operator can hold a user hostage.
- Competition happens on quality rather than lock-in.
- A user can switch operators without rebuilding their network.
- Commercial operators cannot capture the protocol by capturing its users.

If identity were not portable, the commercial layer would inevitably become extractive. Because it is portable, the commercial layer is forced to be additive.

---

## Part II — Free users as the network's foundation

### 6. The contribution of the free tier

The free tier is not a loss leader. It is the network's foundation.

Free users contribute:

**Reachability publication.** Every free user publishes their own reachability records. Without this, there is no network.

**Peer-to-peer connections.** Every free user who can establish a direct connection reduces relay load. A free user streaming video to their own phone over LAN is not consuming relay capacity. A free user whose traffic goes direct is contributing to the network's aggregate efficiency by not needing relay.

**Hairpinning and traversal.** Free users on networks that support traversal contribute to the network's ability to avoid relay. Each successful traversal is one less relay session.

**Local relays.** Some free users run their own relays — on a Raspberry Pi, a home server, a VPS. These contribute to the volunteer pool. The volunteer pool is what the free tier stands on.

**Reduced infrastructure cost.** The aggregate of the above means the network's infrastructure cost is significantly lower than it would be if all users needed relay. This is a measurable economic effect, not just a philosophical one.

**Discovering bugs and edge cases.** Free users exercise the protocol in diverse ways. Their bug reports, edge cases, and feedback improve the protocol for everyone.

**Ecosystem gravity.** A large free user base makes the network attractive to applications, contributors, and commercial operators. The free tier is the reason a commercial operator has a market at all.

### 7. Why free users make paid users more valuable

A network with one million free users and ten thousand paid users is more valuable than a network with ten thousand paid users and no free users.

Why:

- Applications integrate with the protocol because it reaches a large audience. That makes the paid tier more useful to enterprises, because their users already have mesh identities.
- Contributors run infrastructure because there are many users to serve. That expands the free pool for everyone.
- Commercial operators have a market because there are users who want guarantees. The existence of the free tier is what makes the paid tier sustainable.

The free users are the reason the paid users show up.

### 8. Free users who contribute infrastructure

Some free users do more than participate — they run infrastructure. These are *contributors*, and they earn credits for the capacity they contribute. Credits can be spent on priority relay capacity elsewhere.

This creates a contribution economy where users who contribute infrastructure offset their own consumption. A user who runs a Raspberry Pi relay for their family earns credits that pay for their phone's relay usage when they travel.

The contributor tier sits between the free tier and the paid tier. It's not "free" in the sense of doing nothing; it's "free" in the sense of not paying money, in exchange for contributing capacity.

### 9. The free tier and paid tier are complementary

A common failure mode for open-source funding is to treat free users as a burden. This is backwards.

Every free user makes the network more valuable to applications, more attractive to contributors, more credible to enterprises, cheaper to operate (through P2P connections), and more likely to have a commercial operator at all.

The commercial layer's job is not to convert free users. It's to serve the users who want guarantees, while strengthening the network that everyone else uses.

---

## Part III — The relay priority model

### 10. The core structure

Four properties:

**Property 1 — Free tier is real.** Free users can always connect. Relay is available on a best-effort basis, subject to fair-share limits. Free tier is not a demo.

**Property 2 — Paid tier is priority.** Paid users get guaranteed relay capacity, higher priority under contention, and consistent performance.

**Property 3 — Idle paid capacity flows to the public pool.** When a paid user or enterprise isn't using their reserved capacity, that capacity serves the free tier. This is not charity — it's efficient use of otherwise idle resources.

**Property 4 — Contribution earns credit.** Users who run their own relays earn credits for the capacity they contribute. Credits can be spent on priority relay capacity elsewhere.

Together, these four properties produce a model where commercial participation *expands* the network rather than partitioning it.

### 11. Priority classes

A relay ticket specifies source, destination, capability, time bounds, and priority class.

**Free class.** Served best-effort. Subject to fair-share limits. May be preempted under contention.

**Standard class.** Served with modest guaranteed share. Rarely preempted.

**Priority class.** Served with higher guaranteed share. Preempted only in emergencies.

**Dedicated class.** Served with reserved capacity. Never preempted.

The protocol provides the mechanism for tickets to carry priority information. A relay's policy determines how many classes exist and what guarantees each provides.

### 12. Priority is a claim, not an identity

Priority is a property of the ticket, not of the user's identity.

- A free-tier user with a priority ticket gets priority service.
- A priority-tier user with a free ticket gets best-effort service.
- The relay does not need to know who the user is to enforce priority. It only needs to verify the ticket.

This enables three properties:

**Privacy.** Relays don't need to maintain identity information about their users.

**Portability.** Priority moves with the user across operators. A user can buy priority from Operator A and use it on Operator B's relays.

**Composability.** Users can hold priority tickets from different authorities and use them flexibly.

### 13. Idle capacity donation

Commercial operators overprovision to handle surges. The surplus is idle most of the time. That surplus serves the free pool, with priority classes allowing instant reclaim when paying customers need capacity back.

Three effects:

**The public pool expands.** Free users benefit from commercial overcapacity. The effective free-tier capacity is volunteer infrastructure plus idle commercial capacity.

**Commercial operators have a better story.** Their business model is not "extract revenue from users who need priority." It's "provide guaranteed capacity for users who want it, and use the surplus to strengthen the network for everyone."

**The economics of overprovisioning change.** Idle capacity becomes a public good rather than waste. Operators have a reason to overprovision slightly more than they otherwise would.

### 14. What the network looks like at steady state

- **Free users.** The majority of participants. Publish reachability, use direct connections, occasionally need relay.
- **Contributors.** Free users who also run relays or rendezvous. Earn credits for their contribution.
- **Volunteer infrastructure.** Rendezvous and relays run by hobbyists, communities, and small businesses.
- **Commercial priority infrastructure.** Relay capacity sold to paying users, with idle capacity flowing to the free pool.
- **Enterprise infrastructure.** Large-scale relay deployments, with idle capacity contributing to the public pool.

A free user's traffic is served from the aggregate. A paid user's traffic gets priority wherever it goes. The specific relay is a routing decision made by the agent; the priority class is what matters.

---

## Part IV — Credit pools and fair exchange

### 15. The family and group problem

Real users come in groups: families, small businesses, hobbyist clubs. A family credit pool needs:

- A way to declare membership. "These devices belong to this pool."
- A way to share contributions. "Any device in the pool contributes credits to the pool."
- A way to share consumption. "Any device in the pool can spend from the pool."
- A way to set limits. "The kids' devices can consume up to N credits per month."
- A way to recover. "If a device is lost, remove it from the pool."

### 16. Credit pool structure

A credit pool is:

- A group identity (not a peer principal, but a logical account).
- A membership list of devices or principals authorized to contribute and consume.
- A credit balance tracking contributed and consumed capacity.
- Policies for contribution minimums, consumption maximums, and priority classes.
- Administration for adding/removing members and adjusting policies.

The pool is not itself a peer. It's an account that peers reference.

### 17. How a family pool works

- Dad creates a pool. He's the administrator.
- Dad adds the family's devices to the pool.
- The home server runs a small relay. Credits flow to the pool when it serves traffic.
- Dad's VPS also runs a relay. Credits flow to the pool from there too.
- When any device needs relay, it consumes from the pool.
- Dad sets per-device consumption limits.
- When a device is lost, Dad removes it from the pool.

This is what users intuitively expect from a "family plan" — shared resources with per-member controls.

### 18. How accounting resolves

**At contribution time:** A device in the pool runs a relay, records sessions, and reports contribution to the pool as a signed credit receipt. The receipt says: "I contributed X units of capacity during time period Y, signed by [device key]."

**At consumption time:** A device consumes relay capacity. The relay issues a signed consumption receipt: "I served X units of capacity to [device key] during time period Y, signed by [relay operator]."

**At reconciliation time:** The pool reconciles:

```
balance = sum(contribution_receipts) - sum(consumption_receipts)
```

The hard parts are receipt propagation, verification, cross-operator reconciliation, and dispute handling.

### 19. Fair-to-fair credit exchange

Credits are not operator-specific. Operators can enter agreements to accept each other's credits, subject to exchange rates.

- Operator A runs relays in North America.
- Operator B runs relays in Europe.
- A user of A travels to Europe. Their traffic needs a European relay. Operator B accepts A's credits at some exchange rate. The user's traffic is served.
- Symmetrically, a user of B traveling to North America is served by A.

This is exactly how mobile network roaming works. Settlement is periodic. Disputes are resolved through established mechanisms.

The design goal is **operator-agnostic credits**: a user's contribution is valuable anywhere, not just with the operator they happened to contribute to.

### 20. The "someone else's box is better" case

The credit model handles a case that seems counterintuitive: **the premium box between two hosts may not be your own.**

A user in Tokyo with a Frankfurt VPS talks to a Tokyo peer with a Tokyo VPS. The traffic is best served by the peer's Tokyo VPS, not by the user's own Frankfurt VPS. So the user's agent uses the peer's Tokyo relay, consuming credits, while the user's Frankfurt VPS sits idle.

Later, when the user travels to Europe, they use their Frankfurt VPS for their own traffic. The overall flow of credits between the two users balances out over time.

This produces a system where **capacity is used where it's most useful, not where it's owned.**

### 21. Preventing abuse of the credit system

**Fake contribution.** An attacker creates fake relays that appear to contribute but never serve traffic.
*Mitigation:* Credits are earned only for served traffic, verified by receiving peers. Statistical anomaly detection flags relays whose claimed activity is inconsistent. Reputation systems weight long-running relays.

**Circular traffic.** An attacker sets up two relays that relay traffic between themselves in a loop.
*Mitigation:* Circuit detection flags traffic that bounces between relays. Path length limits prevent absurdly long paths. Time-based checks flag patterns impossible for real users.

**Credit laundering.** An attacker obtains credits fraudulently and moves them through many accounts.
*Mitigation:* Credits are bound to a pool. A pool cannot transfer credits directly to another pool. Cross-operator exchanges are operator-mediated.

**Free-riding.** A user consumes credits but never contributes.
*Mitigation:* Free riders are limited to free-tier capacity, which is best-effort. Participation is optional; priority requires contribution.

**Fake identity multiplication.** An attacker creates many identities to multiply credit balance.
*Mitigation:* Credits are per-pool, not per-identity. Pool membership is administratively controlled. Cross-pool correlation flags suspicious patterns.

**Consumption fraud.** An attacker consumes credits they didn't earn.
*Mitigation:* Consumption is recorded by the relay, not the consumer. Per-device limits apply. Anomaly detection flags unusual patterns.

**Bonding.** Relay operators may post a bond, forfeited if abuse is proven. This makes abuse expensive.

The design principle: **the easiest way to earn credits is to actually contribute, and the easiest way to consume them is to actually need them.**

### 22. The dispute problem

Options for resolution:

- **Operator discretion.** Fast but centralized.
- **Multi-party review.** Slower but more trusted.
- **Cryptographic arbitration.** Faster and objective, but requires evidence retention.
- **Hybrid.** Routine disputes by operator policy; serious disputes by review board; cryptographic evidence retained throughout.

The hybrid approach is most likely to be adopted in practice.

---

## Part V — The blockchain question

### 23. The case for and against

Blockchains solve distributed consensus among anonymous parties. Mesh's credit system has a bounded number of identified operators with legal contracts. Notarized receipts — signed statements exchanged periodically between operators — solve the same problem at a fraction of the cost.

Blockchains have significant disadvantages in this context: energy cost, latency, transaction costs, complexity, regulatory exposure, and capture risk. None of these are fatal on their own, but together they make a full blockchain a poor fit.

### 24. The blockchain hybrid

A middle ground: use a blockchain only for the *notarization layer*. Operators maintain their own ledgers and publish hashes to a public blockchain for tamper-evidence. Low cost, low latency, regulatory distance.

This is what several existing systems do. It's a pragmatic compromise.

### 25. Recommendation

**Default: notarized receipts, no blockchain.** Operators maintain their own ledgers. They exchange signed notarizations. Disputes are resolved through established mechanisms.

**Optional: blockchain notarization.** Operators that want extra tamper-evidence can publish hashes of their ledger states to a public blockchain.

**Explicit non-recommendation: full blockchain.** A full blockchain for credit transactions is not recommended. The number of operators is small, trust between operators is possible, and settlement volume is low.

### 26. Design for the possibility, don't build for it

Credit receipts should be signed and tamper-evident from the start. Receipt IDs should be globally unique. Operator ledgers should be hashable. Notarizations should be publishable to any sink, including a blockchain.

If these properties hold, adding a blockchain notarization layer later is plumbing, not redesign.

---

## Part VI — Geographic scarcity and fairness

### 27. The Hawaii problem

A VPS in Hawaii provides scarcer capacity than a VPS in Frankfurt. Hawaii has fewer data centers, higher bandwidth costs, and less infrastructure in general.

Under a naive credit model, both VPSes earn the same credit per byte relayed. But the Hawaii VPS is providing *scarcer* capacity. This should be reflected in the credit system.

### 28. Geographic credit adjustment

A relay's credit value should depend on:

- **Base value.** Bytes relayed.
- **Scarcity multiplier.** Regions with fewer relays earn more per byte.
- **Latency value.** Low-latency relays earn more per byte.
- **Availability value.** High-uptime relays earn more per byte.
- **Priority class value.** Relays serving higher priority classes earn more per byte.

The scarcity multiplier is the key addition. A relay in Hawaii earns a higher multiplier per byte than a relay in Frankfurt. This makes contribution in scarce regions more attractive.

### 29. Exchange rates and fairness

When credits are exchanged across operators, the exchange rate reflects the relative value of the credits. German credits have a low exchange rate (Frankfurt is abundant). Hawaiian credits have a high exchange rate (Honolulu is scarce).

A user who contributes in Frankfurt and consumes in Hawaii trades Frankfurt credits for Hawaii credits at the exchange rate. If the exchange rate is fair, the user's effective cost is proportional to the value of what they consume, not to where they consume it.

This is exactly how foreign exchange works in the real world. The exchange rate equalizes value across regions.

### 30. Relays are replaceable, but geography isn't

A relay in Hawaii can be replaced by another relay in Hawaii, but not by a relay in Frankfurt. The Frankfurt relay has different latency, different paths, different network characteristics.

The credit system has to reflect that some relay locations are more valuable than others. The protocol doesn't mandate geographic adjustment, but it should be designed to allow it. Relay tickets should carry enough information (latency, region, priority) for the credit system to compute geographically adjusted credits.

### 31. Geographic diversity as a goal

The credit system should actively encourage infrastructure in underserved regions. A relay in an underserved region earns more credits per byte, creating a market incentive for geographic diversity.

A hobbyist in a region with poor connectivity has a natural opportunity: run a relay, earn credits at a higher rate, contribute to the network's geographic diversity. The same principle applies at enterprise scale.

---

## Part VII — Self-hosted priority and enterprise scale

### 32. Self-hosted priority on your own machine

A user with their own VPS or home server runs a mesh relay on it. When their traffic needs relay, the mesh agent prefers this relay. The user gets **self-priority**: their own relay serves their traffic at whatever priority they choose.

When the relay isn't reachable, the agent falls back to the free pool or commercial priority.

The user gets a hybrid model: own relay for priority most of the time, free pool for fallback, commercial priority for guaranteed capacity when needed.

### 33. Enterprise self-hosted priority

Enterprises run their own relay infrastructure. Users get priority on that infrastructure. When idle, it serves the public pool.

The enterprise gets:

- **Full control.** Their own infrastructure, their own policy.
- **Predictable cost.** They pay for the infrastructure they run, not a subscription.
- **Public good.** Their idle capacity contributes to the network.
- **Strategic visibility.** The enterprise is a visible contributor to the open network.

### 34. Enterprise scale — the full model

An enterprise at scale can run its own rendezvous infrastructure, its own relays, its own credit pool, and its own priority policy. It's essentially running its own mesh deployment using the open protocol.

The enterprise doesn't need a commercial operator for most of its needs. This is the same pattern as enterprise email.

### 35. The enterprise value proposition

- **No vendor lock-in.** The protocol is open; identity is portable.
- **No account model.** No commercial operator's account for users.
- **Full control.** The enterprise's infrastructure is its own.
- **Public good.** Idle capacity contributes to the open network.
- **Regulatory posture.** Device trust is under the enterprise's own control.
- **Cost efficiency.** Pay for infrastructure you run, not a vendor's markup.

This positions the enterprise as a peer in the network, not a customer of a vendor.

### 36. The accounting complexity at enterprise scale

- **Multi-site infrastructure.** Separate accounting per region.
- **Multi-tenant pools.** Separate pools with cross-pool policies.
- **Regulatory requirements.** Different rules per jurisdiction.
- **Integration with existing systems.** Cost accounting, procurement, reporting.
- **Dispute resolution.** More common and more consequential at enterprise scale.

These are the "devil in the details" of the enterprise model. They're not insurmountable, but they're not trivial. The good news: these are the same challenges every enterprise infrastructure system faces, and the mechanisms are well-established.

---

## Part VIII — Keeping the databases in sync

### 37. The accounting problem

The credit system maintains consistent state across many independently-operated databases. The specific problems and their mitigations:

**Receipt propagation.** A relay issues a receipt; the receipt has to reach the pool. If either is offline, the receipt is delayed or queued.
*Mitigation:* Receipts are durable local state. They persist until acknowledged. Devices resync when reconnected.

**Duplicate receipts.** A receipt might reach the pool multiple times.
*Mitigation:* Receipts carry globally unique IDs. The pool deduplicates.

**Receipt ordering.** Receipts arrive in arbitrary order.
*Mitigation:* Receipts carry sequence numbers and timestamps. The pool buffers out-of-order receipts and processes them when orderable.

**Missing receipts.** Some receipts are never received.
*Mitigation:* Receipts are periodically re-issued from local store. If a device is permanently lost, its receipts are lost, and the accounting is adjusted.

**Conflicting receipts.** Two receipts claim the same traffic.
*Mitigation:* Receipts reference each other. Conflicting receipts are flagged and resolved by the operator.

**Partition tolerance.** Network partitions split the pool.
*Mitigation:* Eventual consistency with reconciliation on partition heal.

**Audit.** Auditors need to reconstruct pool state.
*Mitigation:* Receipts retained for a policy-defined period. Store is hashable. Auditors can verify integrity.

**Backup and recovery.** Pool state must be reconstructible.
*Mitigation:* Periodic snapshots published off-site. Recovery uses most recent snapshot plus receipts since.

**Scalability.** Millions of receipts.
*Mitigation:* Receipts aggregated into time-bucketed summaries. Raw receipts retained for audit.

**Cross-operator settlement.** Operators' ledgers have to reconcile.
*Mitigation:* Periodic notarizations. Discrepancies flagged and resolved.

### 38. Design implications

- Signed receipts with unique IDs.
- Durable local store with retry until ack.
- Indexing by receipt ID and time bucket.
- Eventual consistency with reconciliation.
- Periodic snapshots and notarizations.
- Aggregation for scale.
- Hashable state for audit.
- Clear dispute escalation paths.

---

## Part IX — What commercial operators sell

### 39. The six products

**Managed rendezvous.** Low-cost, always-available rendezvous for users who don't want to run their own.

**Priority relay capacity.** High-bandwidth, low-latency, SLA-backed relay.

**Credit exchange.** Service that exchanges credits between operators.

**Enterprise integration.** Integration with Okta, Entra, MDM, SIEM, compliance systems.

**Support and SLAs.** Responsive support, published uptime, escalation paths.

**Managed deployment.** Turnkey mesh deployments for organizations.

### 40. The public-good component of each product

- **Managed rendezvous** contributes to the public rendezvous mesh.
- **Priority relay capacity** contributes idle capacity to the public pool.
- **Credit exchange** makes credits useful across operators.
- **Enterprise integration** contributes enterprise idle capacity.
- **Support and SLAs** improve ecosystem health.
- **Managed deployment** grows the network.

The effect: money flowing into the commercial layer expands the network rather than extracting from it.

### 41. What "just works" really means

**Free tier:** the network works, but performance may vary.

**Standard tier:** the network works reliably. Relay guaranteed within a tier. No fair-share limits.

**Priority tier:** the network works reliably, even under peak load. Traffic is prioritized. Latency is bounded.

**Dedicated tier:** reserved capacity. No contention. SLA-backed.

The difference between tiers is not "access" but "predictability."

### 42. The urgency buyer

The natural customer for the priority tier is the *urgency buyer*: the traveler on hotel Wi-Fi who needs to reach their server, the person whose connection is failing and just wants it to work *right now*, the small business owner whose meeting depends on reaching a file.

They aren't price-sensitive. They're reliability-sensitive. They'll happily pay for a moment of guaranteed reliability even if they use the network for free most of the time.

This is a different buyer than the enterprise customer. Enterprises buy SLAs, integration, and compliance. Urgency buyers buy a moment of certainty.

Both are valid. Both are served by the same priority infrastructure.

### 43. "No account" is a commercial feature

Mesh has no account system. This is not just a technical property — it's a commercial benefit for operators:

- No user database to maintain.
- No signup flow to build.
- No password reset system to build.
- No account recovery to worry about.
- No data breach risk from a credential store.
- No GDPR exposure from a user database.

For operators, this is a real operational and legal simplification. It reduces costs and reduces risk.

---

## Part X — Developer funding

### 44. The developer funding problem

Open-source infrastructure has a well-documented sustainability problem. Critical projects are often underfunded and maintained by a few volunteers. This creates fragility — Heartbleed, the XZ backdoor, and many other incidents are consequences of underfunded maintenance.

The problem is not that developers don't want to work on infrastructure. It's that the work is not funded in a way that allows sustained commitment.

Mesh has a specific advantage: **its commercial layer generates revenue that can fund developer work.** Unlike projects that depend entirely on donations or grants, Mesh has a direct path from commercial infrastructure to protocol maintenance.

### 45. What successful projects do

Patterns from projects that have funded developers sustainably:

**The Apache Software Foundation model.** Corporate sponsors provide the bulk of funding; individual donations provide additional support; the foundation operates with very low overhead. Sponsors include major technology companies. The foundation doesn't fund specific developers directly; it funds the infrastructure that allows project communities to function.

**The Linux Foundation model.** Corporate memberships, event revenue, and targeted sponsorships. The foundation provides the human infrastructure — legal structures, funding mechanisms, governance — that makes sustainable development possible.

**The Sovereign Tech Fund model.** Public funding from government, supporting open-source infrastructure as a matter of digital sovereignty. Direct financial support to maintainers.

**The postmarketOS model.** Excess donation income funds financial compensation for high-commitment contributors, with the same hourly rate for everyone regardless of location or task type.

**The ISC/Kea model.** Funding from grants, donations, premium feature sales, and professional technical support. Technical support proved the most sustainable; premium features were less profitable than expected.

**The endowment model.** Donations build a principal fund; only investment income is spent on grants. Creates permanent, stable funding.

**The Merit model.** Programmable revenue splits and stablecoin payouts that directly reward contributors based on impact.

### 46. What Mesh should learn

Three patterns are most relevant.

**Diversification.** Successful projects don't depend on a single funding source. Mesh should have multiple revenue streams: relay priority subscriptions, enterprise contracts, managed rendezvous, credit exchange fees.

**The 3A services model.** Companies build businesses on open-source by providing assurance (SLAs), adaptation (integration), and assistance (support). These services require participation in the project, which provides the project with resources.

**Direct contributor compensation.** Paying maintainers directly for their work is important. Maintainers do more than write code — they review, mentor, organize, and manage. Funding only code ignores most of the work.

### 47. The Mesh developer funding model

**Structural funding from commercial operators.** Commercial operators contribute a percentage of revenue to protocol development. This is not a donation; it's a structural line item, like a franchise fee.

**The stewardship entity.** A nonprofit entity, modeled on Apache or the Linux Foundation, receives the commercial contributions and manages the funds. Three responsibilities: maintain the protocol, fund developers, coordinate governance.

**Distribution mechanisms:**

- **Maintainer stipends.** Recurring payments for ongoing work.
- **Sponsored features.** A company or user funds a specific feature; once completed, the feature is available to everyone.
- **Bug bounties and security work.** Funds allocated for audits, bounties, hardening.
- **Ecosystem work.** Documentation, tooling, integration support, community management.
- **Fellowships.** Time-limited funded positions for strategic priorities.

**Funding sources:**

- **Commercial operator revenue share.** A percentage of every priority subscription, enterprise contract, and managed deployment.
- **Individual donations.** Recurring or one-time.
- **Grants.** Public grants, especially for security work.
- **Enterprise contributions.** Direct contributions from enterprises that use Mesh heavily.
- **Foundation endowments.** Long-term stable funding independent of year-to-year commercial fluctuations.

### 48. Why this works for Mesh

The commercial layer's revenue is proportional to the network's usefulness. The more people use the network, the more revenue there is to fund development. This is different from donation-based models, where revenue is decoupled from usage.

It also aligns incentives. Commercial operators benefit from a healthy protocol. They have a direct interest in funding its maintenance.

### 49. The startup phase

Before commercial revenue exists, Mesh needs seed funding:

- **Bootstrapping.** Development funded by the founder's time and modest donations.
- **Grants.** Applying to programs like the Sovereign Tech Fund or similar.
- **Angel contributions.** Individuals who believe in the project contribute early.
- **Early commercial partnerships.** A commercial operator that wants Mesh to exist can fund early development.

The goal during the startup phase is not to be sustainable immediately. It is to reach the point where the commercial layer generates enough revenue to fund ongoing development.

### 50. What success looks like for developer funding

Success is: **a developer can work on Mesh full-time and be paid fairly for it.**

This sounds basic, but it is rare. Most open-source infrastructure is maintained by people who work on it in their spare time because they cannot afford to do otherwise.

If Mesh reaches the point where:

- Core maintainers are paid for their work.
- Security work is funded.
- Documentation and tooling are funded.
- New contributors can be mentored and compensated.

Then the protocol will be sustainable. If it doesn't, the protocol will eventually stagnate or become unmaintained, regardless of how good the design is.

---

## Part XI — Putting it together

### 51. The full picture

**Volunteer contributors.** Hobbyists running rendezvous and relays. Communities sharing infrastructure. Small businesses running their own.

**Commercial operators.** Managed rendezvous, priority relay, credit exchange, enterprise integration, support, managed deployment.

**The stewardship entity.** Maintains the protocol, funds developers, coordinates governance. Funded by commercial operators, enterprises, grants, and donations.

**Applications.** Integrate with mesh agents. Offer remote access without building connectivity.

**Users.** Free tier with best-effort service. Paid tier with priority. Contribution tier earning credits. Enterprise tier with SLA-backed service.

### 52. The funding flow

```
Free users            →  Use the network, contribute reachability, run local relays
Contributors          →  Run relays, earn credits, offset consumption
Paid users            →  Pay for priority, fund commercial operators
Commercial operators  →  Run infrastructure, contribute idle capacity, pay revenue share
Stewardship entity    →  Receives revenue share, funds developers, maintains protocol
Developers            →  Maintain protocol, improve security, build tooling
```

Every participant contributes to the network, and every participant benefits from the network.

### 53. The one-sentence summary

**Free protocol, paid priority, volunteer contribution, developer funding — all from the same commercial layer that strengthens the network.**

### 54. The key property

**Every commercial product has a public-good component, and every contribution to the network — including the free tier — strengthens it.**

This is what makes the model sustainable. The free tier is not a cost center. The commercial layer is not an extractive platform. And developers are funded by the value the network creates.

### 55. The relationship between free users and paid users

Free users and paid users are not opposed. They are complementary.

Free users provide the network's foundation: reachability, peer-to-peer efficiency, contributor infrastructure, ecosystem gravity.

Paid users provide the network's funding: revenue that supports commercial infrastructure, idle capacity that flows to the public pool, and the demand signal that makes the ecosystem worth building for.

Both are necessary. Neither is more important. The commercial layer exists to serve the users who want guarantees, while strengthening the network that everyone else uses.

---

## Appendix — Cross-references

This addendum sits alongside `RATIONALE.md`. It assumes familiarity with:

- **`PROTOCOL.md`** — the protocol specification.
- **`RATIONALE.md`** — the design rationale and contribution model.
- **`ECOSYSTEM.md`** (when drafted) — the ecosystem-level view of participants and roles.
- **`ROADMAP.md`** (when drafted) — the phased introduction of commercial infrastructure.

This addendum does not modify any normative protocol requirement. It documents a coherent funding model that the protocol is compatible with, not a requirement of the protocol itself.