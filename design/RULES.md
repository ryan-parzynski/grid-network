# Grid Network — Design Rules and Anti-Patterns

**Revision:** 2.3
**Protocol version:** v0.6.3

**Repository path:** `design/RULES.md`

This document is non-normative. It records the rules the design follows
and the anti-patterns it avoids. Its purpose is to guide future
changes: an editor who understands the rules can apply them without
re-deriving the reasoning.

---

## 1. Anti-patterns

Each anti-pattern is a way of changing the specification that has been
observed or anticipated, and that would degrade the design. Each is
paired with the rule that prevents it.

### A1. Adding mechanisms "just in case"

Adding a mechanism because it might be useful, without a specific
problem it solves, accumulates complexity that does not pay for itself.

**Rule.** Before adding a concept, requirement, or mechanism, answer:

1. What authority or resource does it protect?
2. What specific attack or failure does it prevent?
3. What happens if it is removed?
4. What complexity does it introduce?
5. Which invariant does it serve?

If any answer is unsatisfactory, the mechanism is premature.

### A2. Conflating the layers

The specification, the design record, and the operator guide have
different purposes. Mixing them produces a document that is normative
in one section and aspirational in the next.

**Rule.** The specification is normative. The design record explains
why. The operator guide explains how. No section mixes the three.

### A3. Letting documentation become marketing

A specification is a technical document. Marketing claims dilute the
specification's authority.

**Rule.** The specification states requirements and defines behavior.
Claims about what the design "enables" belong in the design record.

### A4. Introducing vendor lock-in through the protocol

Any mechanism that requires a specific operator, provider, or
implementation is a defect.

**Rule.** Every infrastructure component is replaceable. No mechanism
requires a specific vendor.

### A5. Adding fields to `stable` sections

A `stable` section is a conformance surface. Changing it silently
breaks implementations that were built against it.

**Rule.** Any change to a `stable` section requires a protocol-version
bump in the same revision.

### A6. Omitting negative test vectors

A positive vector shows that an implementation accepts the right input.
It does not show that it rejects the wrong input.

**Rule.** Every positive vector has at least three negative
counterparts.

### A7. Silently extending the protocol

An implementation that adds an object type, a field, or a behavior
without a version bump produces objects that other implementations
cannot read.

**Rule.** Any protocol change requires a version bump per
`spec/VERSIONING.md`.

### A8. Writing a value into a rule

A normative rule that carries a literal value (`30 minutes`, `64
bytes`) becomes unchangeable without a protocol-version bump, and
unportable across deployments.

**Rule.** Every tunable value is a symbol in `spec/PARAMETERS.md`.

### A9. Leaving provenance in the specification

Session dates, chat attributions, and earlier-document references tell
the reader they are looking at a reconstructed artifact.

**Rule.** The specification has no provenance. History lives in
`REVISIONS.md`.

### A10. Using second person in normative text

"You must configure..." addresses a specific reader. A specification is
read by many.

**Rule.** Normative text is declarative. "An implementation MUST..." or
"The verifier MUST..." Never "you."

---

## 2. The rule for adding a mechanism

Before adding any new concept, requirement, or mechanism, answer these
questions. If any answer is unsatisfactory, the mechanism is premature.

1. **What problem does it solve?** A specific problem, not a category
   of problems.
2. **What is the authority boundary?** Which domain does it belong to,
   and does it escalate into another?
3. **Can it be tested?** A conformance scenario or a test vector must
   exist.
4. **Can it be removed?** If removal breaks the design, the mechanism
   is load-bearing and must be specified completely.
5. **Does it create new complexity?** Complexity must be justified by
   the problem it solves.
6. **Is it orthogonal to existing mechanisms?** If it overlaps, one of
   the two is redundant.
7. **What is the implementation cost?** The cost is paid by every
   implementation, not just the one that proposed it.
8. **What does it break?** A new mechanism may invalidate existing
   guarantees.

---

## 3. Gap taxonomy

Every proposed change that claims to fix a "gap" is classified before
action.

| Class | Meaning | Action |
|---|---|---|
| **Schema gap** | The object model is incomplete. A field or object is missing. | Add to `spec/OBJECTS.md`. |
| **Wire gap** | The protocol for using objects is missing. How objects are transmitted or exchanged. | Add to the relevant specification section or the operator guide. |
| **Documentation gap** | The design says or implies the answer but does not state it. | Add a clarifying sentence. |
| **Design limitation** | No protocol mechanism can address it. | Document in the Roadmap's known-limitations index. |

Treating a limitation as a gap is a common failure mode. It leads to
inventing mechanisms for problems that have no solution, which makes
the design more complex without making it more correct. Split-brain
identity is the clearest example: no protocol mechanism can distinguish
a legitimate root transition from an attacker-driven one. The correct
response is to name the limitation, not to invent a mechanism.

---

## 4. Structural mechanisms for keeping the specification clean

These are conventions and checks that mechanical tooling can enforce.
They are proposed, not yet implemented. Each is a candidate; the
archivist decides which become build steps.

### 4.1 Invariant registry

Every invariant has a stable identifier. Every normative rule cites the
invariant it serves. A rule with no citation is aspirational and does
not belong in the specification.

**Enforces.** No rule without a purpose.
**Fails loudly.** A rule without a citation; an invariant that no rule
cites.
**Cost.** Each new rule needs a tag.
**Failure mode.** It checks presence, not relevance. A rule can cite
the wrong invariant and pass.

### 4.2 Single-source schemas

Each object's fields, types, and enums are defined once in a machine-
readable form. Prose tables, struct listings, and examples are derived
from it or validated against it.

**Enforces.** Schema consistency.
**Fails loudly.** A struct listing or example that differs from the
definition.
**Cost.** Editors change the definition, not the prose.
**Failure mode.** It covers structure, not semantics. Free-text
descriptions can still contradict the definition.

### 4.3 Cross-reference checker

Every internal reference resolves to a section that exists.

**Enforces.** Referential integrity.
**Fails loudly.** An unresolved reference; a reference to a renamed
section.
**Cost.** References use stable identifiers, not hand-typed numbers.
**Failure mode.** It checks existence, not meaning. A reference can
resolve to a real section that no longer says what the sentence needs.

### 4.4 Symbol checker

Every symbol used in a rule appears in `spec/PARAMETERS.md`. Every
table entry is used by at least one rule.

**Enforces.** Parameter consistency.
**Fails loudly.** An undefined symbol; an unused table row.
**Cost.** Editors define a symbol before using it.
**Failure mode.** It cannot distinguish a symbol from an ordinary
capitalized token unless symbols have a distinctive form.

### 4.5 Vocabulary lock

A controlled term list. Each concept has one canonical term. Declared
synonyms are allowed; other variants are rejected.

**Enforces.** Vocabulary consistency.
**Fails loudly.** A banned variant; a term not in the list.
**Cost.** New terms go on the list first.
**Failure mode.** The list only catches variants someone has already
thought of.

### 4.6 Scenario parameterization

Every conformance scenario uses symbols from `spec/PARAMETERS.md`.
Literal values do not appear.

**Enforces.** Portability of scenarios.
**Fails loudly.** A bare numeric duration in a scenario.
**Cost.** Scenarios are written against symbols.
**Failure mode.** Numbers that are not parameters (sequence numbers,
counts) trigger false positives unless exempted.

### 4.7 Stability markers

Sections are marked `stable` or `under-review` per
`spec/VERSIONING.md`. A change to a `stable` section triggers a
protocol-version bump.

**Enforces.** The cost of changing conformance-critical text.
**Fails loudly.** A diff to a `stable` section without a version bump.
**Cost.** Editors think before touching a `stable` section.
**Failure mode.** It cannot distinguish a typo fix from a semantic
change, so it blocks both.

### 4.8 Section-owns-its-context

A section uses only terms, symbols, and objects defined within it, in
the glossary, or in a declared dependency list.

**Enforces.** Section independence.
**Fails loudly.** An undeclared dependency.
**Cost.** Each section opens with a short dependency line.
**Failure mode.** It matches by string, so an undefined concept that
happens to use a word appearing elsewhere passes.

### 4.9 Tombstones on deletion

Any removal leaves a stub recording what was removed, at which
revision, and why.

**Enforces.** Traceability of deletions.
**Fails loudly.** A previously present identifier absent with no
tombstone.
**Cost.** Deleting is a two-step act.
**Failure mode.** It needs a baseline list of identifiers to compare
against.

### 4.10 Derived-count assertions

Any stated count ("N sections", "N scenarios") is computed from the
document, not written by hand.

**Enforces.** Count consistency.
**Fails loudly.** A stated number that differs from the computed count.
**Cost.** Editors write counts as generated references.
**Failure mode.** It only catches counts it can recognize and attach to
a countable item.

### 4.11 Forbidden-residue patterns

No dated markers, chat attributions, "TODO", "pending", or personal
handles in normative text.

**Enforces.** Publication readiness.
**Fails loudly.** A match against the pattern list.
**Cost.** Editors keep provenance out of the specification.
**Failure mode.** Legitimate uses are caught, such as "pending" in a
state name. It needs an exempt list.

### 4.12 Examples validated against the rules

Each worked example states its inputs in a structured block. A checker
evaluates the example against the rule it illustrates.

**Enforces.** Example correctness.
**Fails loudly.** An example whose stated outcome differs from the
computed outcome.
**Cost.** Examples are written as data first.
**Failure mode.** It only covers rules simple enough to evaluate
mechanically.

### 4.13 Clock-source tags

Every rule involving time names one clock class: issuer-asserted,
verifier-monotonic, or verifier-wall-clock.

**Enforces.** Time semantics clarity.
**Fails loudly.** A time-related rule with no tag.
**Cost.** A tag on each time-related rule.
**Failure mode.** Detecting "time-related" is keyword-based.

### 4.14 Defined-before-use for object and field names

Every object or field name appearing in prose resolves to a schema
definition.

**Enforces.** No use of undefined objects.
**Fails loudly.** A name with no definition.
**Cost.** A new object is defined before it is cited.
**Failure mode.** Common words that coincide with object names produce
false positives.

---

## 5. What survives every review

The following are the invariants that have held across every review the
design has undergone. They are the load-bearing elements. A change that
weakens one of them is a change to the design's core, not a refinement.

- The byte-level constructions in `OBJECTS.md §2`, §3, §4, §8.
- The sequence-space invariant (I1).
- Fail-closed on missing information (F1).
- Terminal revocation.
- Key-role separation.
- Opaque Peer IDs.
- The separation of authority domains.

A proposed change that touches one of these requires a review closure
recorded in `REVISIONS.md`.

---

## 6. What this document is not

It is not a specification. It is not a style guide. It is a record of
the rules the design follows, so that future edits do not silently
violate them.