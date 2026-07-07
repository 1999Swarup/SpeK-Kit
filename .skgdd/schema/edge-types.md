---
type: Schema
title: SKGDD Edge Types
description: The typed relationships that connect nodes into a directed, queryable knowledge graph.
version: 0.1.0
---

# SKGDD Edge Types

Edges are declared **inside a node's frontmatter** as lists of target node IDs.
This keeps the graph inside plain Markdown (OKF-compatible) while making it
machine-walkable. Each edge has a direction and an inverse the graph builder
materializes automatically, so you only declare it once.

## Edge catalogue

| Edge | From → To | Meaning | Inverse |
|------|-----------|---------|---------|
| `refines` | Requirement → Requirement | child sharpens a parent requirement | `refined_by` |
| `depends_on` | any → any | source needs target to exist first | `required_by` |
| `derived_from` | Requirement/Task → UserStory/Requirement | provenance / traceability up | `derives` |
| `satisfies` | Task/Component → Requirement | work fulfills a requirement | `satisfied_by` |
| `verifies` | Test → Requirement/Task | proof a thing works | `verified_by` |
| `implements` | Component → Capability | concrete realizes abstract | `realized_by` |
| `uses_tool` | Task/Decision/Component → Tool | selects a tool for the work | `used_by` |
| `provides` | Tool → Capability | tool grants an ability | `provided_by` |
| `needs_tool` | Capability → Tool | ability requires tooling | `serves` |
| `alternative_to` | Tool → Tool | competing options (for selection) | `alternative_to` |
| `conflicts_with` | any → any | mutually exclusive / contradictory | `conflicts_with` |
| `constrains` | Constraint → any | boundary applied to a node | `constrained_by` |
| `governs` | Constitution → any | principle that rules a node | `governed_by` |
| `threatens` | Risk → any | risk endangers a node | `at_risk` |
| `mitigated_by` | Risk → Task/Decision | how a risk is reduced | `mitigates` |
| `blocks` | Question/Task/Risk → any | target cannot proceed | `blocked_by` |
| `answered_by` | Question → Decision/Requirement | resolution of an unknown | `answers` |
| `supersedes` | Decision/Requirement → same | replaces an older node | `superseded_by` |
| `traces_to` | any → any | explicit trace link (audit) | `traced_from` |
| `related_to` | Entity → any | soft glossary association | `related_to` |
| `includes` | Milestone → Requirement/Task | scope of a release slice | `included_in` |
| `observed` / `changed` / `spawned` | Loop → any | what a loop iteration touched | `observed_by` etc. |

## The three spines

Reading the graph is easy once you know its three backbones:

1. **Value spine (why):** `UserStory → Requirement → Capability`
2. **Build spine (how):** `Capability → Component → Task → Tool`
3. **Trust spine (proof):** `Task → Test → verifies → Requirement`

A requirement is only **truly done** when all three spines close on it: it is
derived from value, realized by a component/task, and verified by a passing test.
The `trace` command reports any requirement missing a spine.

## Legal-edge enforcement

The graph builder rejects edges that violate the taxonomy (e.g. a `Test` that
`uses_tool` a `Requirement`). This is what keeps the graph **accurate** rather
than a pile of arbitrary links — the schema is the contract.

## Edge weight & confidence (optional)

Any edge target may be written as `ID @weight:0.8 conf:med` to record strength
and confidence. Tool-selection and risk-propagation use these to rank. Absent
values default to `weight:1.0 conf:high`.
