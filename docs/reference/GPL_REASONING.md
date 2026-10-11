261004-GPL v 3 Reasoning

# License choice: GPL v3 (Copyleft, like Linux)

## Why GPL v3?

Grid Network uses the GNU General Public License v3.0, inspired by Linux's
GPL model.

## Why GPL v3 and not v2?

Linux uses GPL v2 (1991). Linus Torvalds chose v2 for simplicity:

> "GPL v2 is simple. It says: you use our code, you contribute back."

We use GPL v3 (2007) for the same reason, but with important improvements:

### Patent clarity

GPL v2 has an implicit patent grant. v3 makes it explicit:

> If you distribute GPL v3 software, you also grant patent rights to users.

This is important for cryptographic protocols, where patent issues can arise.

### Anti-tivoization

GPL v3 prevents hardware manufacturers from using copyright to lock you out
of modified software:

> You can't use copyright to prevent someone from running modified versions
> on specific hardware.

Linux runs on locked devices (routers, set-top boxes), so Linus didn't want
this. But it's important for decentralized identity.

### Simplicity

Like v2, v3 has one core rule: **If you use our code, your modifications must
be shared.**

We don't use AGPL (which adds a second rule about services) because:

1. **Complexity** — AGPL adds ambiguity about what counts as "running a service"
2. **Linus's principle** — simple licenses are clearer and more enforceable
3. **Pragmatism** — if someone implements a relay from the spec (not our code),
   AGPL wouldn't cover it anyway

## What this means in practice

✅ **You CAN:**
- Run a commercial relay service (but code must be open)
- Contribute improvements (which then benefit everyone)
- Build a proprietary app using Grid
- Modify Grid for your own use

❌ **You CAN'T:**
- Use our reference relay code and keep your modifications proprietary
- Close-source derived works of Grid itself
- Hide improvements to the protocol if you use our code

## Why GPL and not Apache?

Apache says "anyone can do anything." GPL says "if you use our work, the
community benefits."

Grid Network is built on the principle that identity and authorization
should be decentralized and community-owned. GPL enforces that.

## Why Linus chose GPL v2, and why we choose v3

From a 2006 interview, Linus explained GPL v2:

> "You use our code, you contribute back. That's it. Simple rule."

Linus rejected GPL v3 for its complexity (particularly the anti-tivoization
clause, which he felt was too aggressive).

We agree with Linus's principle — simpler is better. But we use v3 instead
of v2 because:

1. **Software patents are now a real threat** (they weren't in 1991)
2. **Explicit is better than implicit** (v3's patent grant is clearer)
3. **We want to prevent hardware lockdown** (v3's anti-tivoization clause applies
   to decentralized identity)

We do NOT use AGPL because we agree with Linus that adding extra rules (about
services) makes the license too complex.

## For relay and rendezvous operators

If you use our reference implementation:

- You must open-source your relay code
- You keep any proprietary features on top
- You can charge for hosting, support, uptime, better latency
- You compete on service, not on keeping code secret

This is how Linux companies work (Red Hat, Canonical). They make billions
on open-source software, not by closing it.

## Questions?

See [Contributing](CONTRIBUTING.md) if you want to discuss the license choice.
