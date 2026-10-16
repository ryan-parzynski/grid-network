# Grid Network — Contributing

**Revision:** 2.3

**Repository path:** `CONTRIBUTING.md`

---

## What this document covers

How to propose a change, how proposals are reviewed, and what a
contributor is expected to know before proposing.

The protocol is a living document. The specification advances through
revisions, each recorded in `REVISIONS.md`. Contributions are welcome
as review, critique, or proposed patches.

---

## Before proposing a change

Read, at minimum:

- `README.md` — the entry point.
- `spec/PROTOCOL.md` — the normative specification.
- `design/RULES.md` — the rules the design follows.
- `spec/VERSIONING.md` — how versions advance.
- `REVISIONS.md` — what has already been decided.

A proposal that contradicts an existing decision should cite the
decision and explain what has changed.

---

## Types of contribution

### 1. Clarification

A change that makes existing text clearer without changing meaning.

**Example.** "This sentence is ambiguous" → proposed rewrite.

**Review.** Maintainer review. No version bump required.

### 2. Correction

A change that fixes a defect — a broken cross-reference, a
contradiction between two sections, a malformed example.

**Review.** Maintainer review. A document revision advances. A
protocol-version bump is required if the correction touches a `stable`
section.

### 3. Schema addition

A new object, a new field, or a new enum value.

**Review.** RFC process. Discussion period. Maintainer decision. A
protocol-version bump is required unless the object is only used in a
future version.

### 4. Behavioral change

A change to how a verifier decides, how a stream is validated, or how
an object is constructed.

**Review.** RFC process. Longer discussion period. Consensus required.
A protocol-version bump and a migration path are required.

### 5. Objection to a decision

A critique of a decision recorded in `design/DECISIONS.md`.

**Review.** The objection is recorded in `design/REJECTED.md` or in
the decision log as an open question. A decision is reopened only if
the objection identifies a failure mode the original decision did not
consider.

---

## The gap taxonomy

Every proposed change that claims to fix a "gap" is classified first.

- **Schema gap** — the object model is incomplete.
- **Wire gap** — the protocol for using objects is missing.
- **Documentation gap** — the design says or implies the answer but
  does not state it.
- **Design limitation** — no protocol mechanism can address it.

A change that treats a design limitation as a gap will be returned for
reconsideration.

---

## The rule for adding a mechanism

Before proposing a new concept, requirement, or mechanism, answer:

1. What problem does it solve?
2. What is the authority boundary?
3. Can it be tested?
4. Can it be removed?
5. Does it create new complexity?
6. Is it orthogonal to existing mechanisms?
7. What is the implementation cost?
8. What does it break?

A proposal without answers to these questions will be returned for
completion.

---

## How to propose a change

1. **Search the existing decisions.** Check `design/DECISIONS.md`,
   `design/REJECTED.md`, and `REVISIONS.md` for a related decision.

2. **Describe the problem.** State what is wrong or missing. State how
   you discovered it. If it is a specific case, describe the case.

3. **Describe the change.** Quote the current text. State the proposed
   replacement. If the change affects multiple sections, list them.

4. **Explain the rationale.** Why this change and not another? What
   does it enable? What does it break?

5. **State the classification.** Per the gap taxonomy.

6. **State the impact.** If this change touches a `stable` section, or
   changes a rule that implementations depend on, say so.

A proposal in the form of a patch is welcome, but the classification
and rationale are required regardless of format.

---

## Review process

### Maintainer review

Used for clarifications and corrections. A maintainer decides whether
to apply the change, request revision, or decline. The decision is
recorded in `REVISIONS.md`.

### RFC process

Used for schema additions and behavioral changes.

- **Discussion period.** Fourteen days for schema additions. Thirty
  days for behavioral changes.
- **Consensus.** Maintainer decision. For behavioral changes,
  consensus among active implementers is required.
- **Recording.** The RFC and its outcome are recorded in `REVISIONS.md`.

### Reopening a decision

A decision is reopened when a proposal identifies a failure mode the
original decision did not consider. The original decision is not
reopened because a contributor disagrees with it.

---

## Style

- Use declarative sentences in normative text.
- Do not use second person.
- Every tunable value is a symbol in `spec/PARAMETERS.md`.
- Every cross-reference uses a section number that resolves.
- Every example is validated against the rule it illustrates.
- Stability markers are applied per `spec/VERSIONING.md`.

A style violation is a documentation defect and is corrected by
maintainer review.

---

## What is not accepted

- Changes that add mechanisms without a problem they solve.
- Changes that conflate layers (specification with design record, or
  with operator guide).
- Changes that introduce vendor lock-in.
- Changes that add fields to `stable` sections without a
  protocol-version bump.
- Changes that omit negative test vectors.
- Changes that restate a rejected approach without addressing why it
  was rejected.