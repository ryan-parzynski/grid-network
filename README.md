# Grid Network

> **AI-assisted creation.** This repository was developed with
> substantial assistance from large language models. Human authorship
> directed the design, reviewed the drafts, and made the editorial
> decisions. Evaluate the content on its technical merits. Where a claim
> is wrong, the provenance is not the reason.

Grid Network is a control plane for identity, authorization, and
reachability. It sits above existing transports and lets two devices
establish and keep an authenticated, authorized relationship that
survives changes of network, provider, and hardware, with no company as
the permanent authority.

## Where to start

| If you want to | Read |
|---|---|
| Build it, or see how the work is ordered | [`PLAN.md`](PLAN.md) |
| Understand the protocol as currently written | [`reference/README.md`](reference/README.md), then [`reference/spec/PROTOCOL.md`](reference/spec/PROTOCOL.md) |
| See what changed between revisions | [`reference/REVISIONS.md`](reference/REVISIONS.md) |
| See what is known to be unfinished | [`reference/ROADMAP.md`](reference/ROADMAP.md) and [`reference/docs/FOLLOW-UPS.md`](reference/docs/FOLLOW-UPS.md) |

## What is in this repository

**`PLAN.md`** is the build plan: architecture, languages, which open-source
projects to adopt, milestones with exit criteria, practices, and the decisions
to make first.

**`reference/`** is the existing specification set, revision 2.6, protocol
v0.6.3, kept as reference material. It is documentation only: there is no
code and there are no test vectors. It is frozen. New work does not edit it,
and nothing in it is normative for the new specification until a recorded
decision adopts it. Its own README, revision history, validator and
self-test moved with it. Every path written inside those documents is
relative to `reference/`.

New code, vectors, and the next specification are created at the top level
beside `PLAN.md`, in the layout described in `PLAN.md` section 7.2.

## Checks

CI runs the validator for `reference/` on every push and pull request:

    python3 reference/tools/validate.py

The negative tests for the validator are run on a clean checkout with:

    python3 reference/tools/selftest.py

Both need Python 3 and the full git history (`fetch-depth: 0` in CI).

## License

The licensing terms of this repository are in
[`reference/LICENSE.md`](reference/LICENSE.md). They apply to the whole
repository until a decision on the license of new work is recorded
(`PLAN.md`, decision D14).

## Conduct and contributing

See [`reference/CODE_OF_CONDUCT.md`](reference/CODE_OF_CONDUCT.md) and
[`reference/CONTRIBUTING.md`](reference/CONTRIBUTING.md).
