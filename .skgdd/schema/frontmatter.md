---
type: Schema
title: SKGDD Frontmatter Contract
description: The base YAML frontmatter every node must carry, plus ID and linking conventions.
version: 0.1.0
---

# SKGDD Frontmatter Contract

Every node begins with a YAML block. This is deliberately OKF-shaped so any
OKF-aware agent can read an SKGDD bundle as knowledge, while SKGDD-aware tooling
gets the extra workflow fields.

## Base fields (all nodes)

```yaml
---
id: R-0042                       # stable, unique, human-typeable (see ID scheme)
type: Requirement                # one of the SKGDD node types
title: Users can reset password  # short imperative phrase
description: One-sentence summary an agent reads before opening the body.
status: accepted                 # lifecycle state
owner: "@teamname"               # optional accountable party
tags: [auth, security]
created: 2026-07-06
updated: 2026-07-06
# --- edges (any subset, values are node IDs) ---
depends_on: [R-0011]
satisfied_by: [T-0101, T-0102]
governed_by: [C-SEC-01]
# --- provenance / loop ---
confidence: high                 # low | med | high — how sure are we?
source: "interview:2026-07-01"   # where this node came from
---
```

## ID scheme

IDs are short, typed, and stable. Never renumber; supersede instead.

| Prefix | Type | Example |
|--------|------|---------|
| `R-` | Requirement | `R-0042` |
| `US-` | UserStory | `US-007` |
| `T-` | Task | `T-0101` |
| `TL-` | Tool | `TL-postgres` |
| `CAP-` | Capability | `CAP-search` |
| `D-` | Decision (ADR) | `D-0003` |
| `RK-` | Risk | `RK-0002` |
| `Q-` | Question | `Q-0005` |
| `TST-` | Test | `TST-0101` |
| `CMP-` | Component | `CMP-api` |
| `E-` | Entity | `E-tenant` |
| `M-` | Milestone | `M-mvp` |
| `L-` | Loop | `L-2026-07-06-a` |
| `LS-` | Lesson | `LS-0009` |
| `C-` | Constitution article | `C-SEC-01` |

Tool IDs may use a readable slug (`TL-postgres`) rather than a number, since
tools are referenced constantly and slugs aid recall.

## Linking conventions

- Edges are declared in frontmatter (machine layer).
- In the **body**, cross-reference with `[[R-0042]]` wiki-links for humans; the
  graph builder resolves them and warns on any body link missing a frontmatter
  edge (drift detection).
- `index.md` at the bundle root lists every node so an agent can survey the
  bundle before opening files (OKF convention).

## Confidence & source are first-class

Unlike Spec Kit, SKGDD records **how sure** it is about each node and **where it
came from**. Low-confidence nodes surface first in `/skgdd.clarify`, and the
learning loop raises confidence as evidence accumulates. This is what lets the
kit "understand requirements better over time" instead of freezing them at
authoring time.

## Lifecycle, layer, and enterprise fields

Three optional-but-recommended scalar fields power the newer capabilities:

```yaml
stage: planned          # lifecycle backbone (Requirements & Tasks) — see node-types.md
layer: L2               # L1 summary | L2 structured node | L3 deep artifact
external_refs:          # System-of-Record synchronization layer
  [jira:PROJ-123, ado:4567, pr:github.com/acme/app/pull/88, doc:confluence/x]
```

- `stage` is checked by `graph.py lint`: a node cannot legally sit at a stage
  whose guardrail is unmet.
- `external_refs` links a node to enterprise trackers. `/skgdd.sync` reconciles
  the graph with those systems, and the `metrics` command uses them to score
  **audit traceability** and **integration sync**.
- Write `external_refs` as a list of `system:id` strings (parses with or without
  PyYAML) or, if you use PyYAML, as a nested mapping.

## Typed Knowledge Enforcement (body links ↔ graph edges)

A body `[[ID]]` wiki-link is only valid if a graph edge connects the two nodes
in **either** direction. `graph.py lint` reports any `[[ID]]` with no backing
edge and **suggests the correct edge type** from the node-type pair — so the
graph never silently drifts from the prose. The authoring flow is:

```
Create node → add [[links]] in prose → declare graph: edges → lint → commit
```
