---
id: CONSTITUTION
type: Constitution
title: SKGDD Project Constitution
description: Non-negotiable principles that govern every node, plan, and task in this bundle.
version: 0.1.0
status: accepted
---

# Project Constitution

The constitution is the root of the **governance spine**. Every principle here is
a node (`C-*`) that `governs` other nodes. When `/skgdd.analyze` runs, any node
that violates a governing article is flagged before implementation.

> Edit this file to fit your project. The articles below are starter defaults.

## C-GRAPH-01 — The graph is the source of truth
Requirements, tasks, tools, and decisions live as nodes. No requirement exists
only in chat or code. If it isn't a node, it isn't real.

## C-TRACE-01 — Nothing is "done" without a closed trust spine
A requirement may only reach `verified` when it is (a) derived from value,
(b) satisfied by at least one task/component, and (c) verified by a passing test.

## C-ATOM-01 — One concept per node
Split any node that describes more than one requirement, task, or decision.
Atomicity is what makes impact analysis accurate.

## C-CLAR-01 — Ambiguity is a blocker, not a footnote
Every unknown becomes a `Question` node that `blocks` its dependents. Planning
cannot start while a `must`-priority requirement has an open blocking question.

## C-TOOL-01 — Tool choices are decisions, with alternatives
No tool is adopted implicitly. Each adoption is a `Decision` node that lists the
alternatives considered and links `uses_tool` to the chosen `Tool` node.

## C-LOOP-01 — Every change closes a loop
Significant changes (new evidence, failed test, scope shift) are recorded as a
`Loop` node and, if durable, promoted to a `Lesson`. The system learns in the
open.

## C-REV-01 — Reversibility before speed
Prefer decisions that are cheap to reverse. Irreversible choices (data model,
public API, vendor lock-in) require an explicit `Decision` node and owner sign-off.

## C-SEC-01 — Security and privacy are constraints, not features
Inputs are validated at boundaries; secrets never enter nodes; OWASP Top 10 is a
standing checklist applied at `/skgdd.analyze`.

## C-DONE-01 — "Done" means validated, reviewed, and learned
No task is done until: its test passes ✅, a `Review` node approves it ✅, and any
learning is captured as a `Lesson` (or explicitly marked none needed) ✅.

## C-BROWN-01 — Reality before design (brownfield)
For existing systems, no requirement is planned before the current state is
captured as `CurrentState`/`SystemMap`/`LegacyConstraint` nodes and compared
against the target.

## C-LIFE-01 — Nodes flow, they don't jump
A Requirement or Task may not advance a lifecycle `stage` until that stage's
guardrail is met (`graph.py lint` enforces this).

## C-SYNC-01 — The graph and systems-of-record stay in sync
Nodes that map to enterprise trackers carry `external_refs`; `/skgdd.sync`
reconciles them so audit traceability is never broken.

## C-DRIFT-01 — Drift is a defect
When spec ≠ implementation, it is treated as a bug: detect, flag, then either fix
the code or amend the node — never leave them divergent.
