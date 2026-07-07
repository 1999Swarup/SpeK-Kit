---
type: Schema
title: SKGDD Node Types
description: The canonical set of node kinds that live in the knowledge graph. Every markdown file in a bundle is exactly one node.
version: 0.1.0
---

# SKGDD Node Types

Every file in an SKGDD bundle is a **node**. A node is a Markdown file whose YAML
frontmatter declares its `type`. The `type` decides which fields are required,
which edges are legal, and how the node participates in traceability and loops.

> Design rule: **one concept per file**. If a file describes two requirements,
> split it. The graph is only as accurate as its atomicity.

## Node taxonomy

| Type | Purpose | Answers the question | Primary out-edges |
|------|---------|----------------------|-------------------|
| `Constitution` | Non-negotiable principles & guardrails | "What rules must never be broken?" | `governs` |
| `Requirement` | A single atomic capability the system must have | "What must be true?" | `refines`, `depends_on`, `conflicts_with`, `traces_to` |
| `UserStory` | A requirement framed as user value | "Who needs this and why?" | `derived_from`, `satisfied_by` |
| `Constraint` | A boundary (budget, latency, compliance, stack) | "What limits us?" | `constrains` |
| `Assumption` | Something believed true but unverified | "What are we betting on?" | `supports`, `at_risk_from` |
| `Question` | An open unknown blocking confidence | "What don't we know yet?" | `blocks`, `answered_by` |
| `Decision` | An ADR: a choice + rationale + alternatives | "Why did we choose X?" | `resolves`, `supersedes`, `uses_tool` |
| `Capability` | An abstract ability (e.g. "full-text search") | "What can the system do?" | `realized_by`, `needs_tool` |
| `Tool` | A concrete tool/library/service/MCP server | "What do we build with?" | `provides`, `alternative_to`, `conflicts_with` |
| `Component` | A unit of the solution (module, service, page) | "What is built?" | `implements`, `depends_on` |
| `Task` | An executable, verifiable unit of work | "What action produces the result?" | `satisfies`, `depends_on`, `uses_tool`, `verified_by`, `blocks` |
| `Test` | A verification (unit/integration/acceptance) | "How do we know it works?" | `verifies` |
| `Risk` | A named threat to success | "What could go wrong?" | `threatens`, `mitigated_by` |
| `Milestone` | A convergence point / release gate | "When is a slice done?" | `includes` |
| `Entity` | Glossary term / domain concept | "What does this word mean?" | `related_to` |
| `Loop` | A recorded feedback-loop iteration | "What did we observe and change?" | `observed`, `changed`, `spawned` |
| `Lesson` | A learned insight promoted from a Loop | "What will we do differently?" | `amends`, `informs` |
| `CurrentState` | A snapshot of an existing (brownfield) system fact | "What exists today?" | `traces_to`, `constrains` |
| `LegacyConstraint` | A limitation imposed by the existing system | "What can't we change (yet)?" | `constrains` |
| `IntegrationPoint` | A boundary with an external/legacy system | "Where do we connect?" | `depends_on`, `related_to` |
| `SystemMap` | An L3 overview of the current architecture | "How does today's system fit together?" | `includes` |
| `Review` | A post-implementation review record | "Was it built right?" | `verifies`, `informs` |
| `Amendment` | A recorded change to an existing node after implementation | "What changed and why?" | `amends`, `supersedes` |
| `KnowledgePack` | A domain grounding pack (best practices, rules, tools) | "What does this domain demand?" | `governs`, `needs_tool` |

## Lifecycle-oriented knowledge flow (`stage`)

Beyond `status`, every **Requirement** and **Task** carries a `stage` on the
lifecycle backbone. A node may not advance a stage until its guardrail is met
(enforced by `graph.py lint`):

```
draft → specified → planned → implemented → validated → learned
```

| Stage | Guardrail to enter |
|-------|--------------------|
| `specified` | has a testable statement / acceptance criteria |
| `planned` | (Requirement) something `satisfies` it (tasks exist) |
| `implemented` | a `Test` node `verifies` it |
| `validated` | that test is **passing** (not `failing`) |
| `learned` | a `Lesson`/`Loop` `informs` it (learning captured) |

This is the fix for OKF's missing workflow: the graph is not just linked, it
**flows**, and the flow is checked.

## Three-layer abstraction (`layer`) — cognitive-load control

To stop "markdown explosion", nodes and files are tagged by abstraction layer:

| Layer | Purpose | Examples |
|-------|---------|----------|
| `L1` | Summary / navigation | `index.md` (auto-generated per folder) |
| `L2` | Structured nodes | requirements, specs, tasks, tools |
| `L3` | Deep artifacts | logs, contracts, research, `SystemMap` |

Controls (enforced by `lint`): every folder has an auto-generated `index.md`
(L1); any file over **7 `##` sections** must be split; duplicate and orphan
nodes are flagged.

## Required frontmatter per node

All nodes share the base frontmatter (see `frontmatter.md`). Additional required
fields by type:

- `Requirement`: `priority` (must/should/could/wont), `status`, `acceptance`
- `Task`: `status`, `estimate`, `satisfies` (>=1 requirement)
- `Tool`: `category`, `maturity`, `cost`, `provides` (>=1 capability)
- `Decision`: `status` (proposed/accepted/superseded), `alternatives`
- `Risk`: `severity`, `likelihood`, `mitigated_by`
- `Loop`: `loop_kind`, `observed`, `orient`, `decide`, `act`, `reflect`
- `Question`: `status` (open/answered), `blocks`

## Lifecycle states (`status`)

Nodes move through a state machine. The `reconcile` command flags illegal states
(e.g. a `Task` marked `done` whose `Test` node is `failing`).

```
draft → proposed → accepted → in-progress → done → verified → superseded
                     └────────────── blocked ──────────────┘
```

## Why nodes and not sections

Spec Kit keeps everything in a few long files (`spec.md`, `plan.md`,
`tasks.md`). That is readable but **un-navigable at scale** — you cannot ask
"which tasks are affected if Requirement R-042 changes?" SKGDD makes every
requirement, task, tool and decision its own addressable node so the answer is a
graph walk, not a full-text search.
