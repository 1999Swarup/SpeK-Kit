---
type: Article
title: The SKGDD Method
description: How Spec-Driven Development, the Open Knowledge Format, and Loop Engineering combine into one self-developing developer kit.
version: 0.1.0
---

# The SKGDD Method

SKGDD (Spec & Knowledge-Graph Driven Development) is a way of building software
where **understanding is a graph you grow**, not a document you freeze. It stands
on three ideas and welds them together.

## 1. The three ancestors

### Spec Kit — the workflow
GitHub's Spec Kit made specifications *executable*: `constitution → specify →
clarify → plan → tasks → analyze → implement`. Its insight is that shared context,
written down before coding, is what steers an AI agent to the right result. Its
limitation is structure: everything lives in a few long, flat Markdown files.
There is no way to ask "which tasks depend on this requirement?" without reading
everything.

### OKF — the knowledge substrate
Google's Open Knowledge Format made knowledge *agent-navigable*: a folder of
Markdown files, each with YAML frontmatter and typed links, plus an `index.md`
manifest, forming a graph an agent can walk. Its insight is that the
**relationships between pages** — the graph — are the part a flat scrape throws
away. Its limitation is that it is passive: a library, not a workflow. It
describes; it does not build or verify.

### Loop Engineering — the self-improvement engine
Loop Engineering treats every artifact as part of a feedback loop:
**Observe → Orient → Decide → Act → Reflect**. Fast inner loops (code–test–observe)
nest inside slow outer loops (spec–plan–review–learn). Its insight is that a
system that records what it observed and changed can *learn* — it gets better at
understanding its own problem. This is the piece that lets SKGDD "self-develop
like a human."

## 2. The synthesis

> **Spec Kit's workflow, executed against an OKF knowledge graph, closed by Loop
> Engineering feedback.**

Concretely:

- Every artifact Spec Kit would bury in `spec.md`/`plan.md`/`tasks.md` becomes an
  **atomic node** in an OKF-shaped bundle.
- Nodes connect through **typed edges**, so requirements, tasks, tools, tests,
  risks, and decisions form one directed graph.
- A tiny **graph engine** (`graph.py`, zero dependencies) validates the graph and
  answers traceability, impact, coverage, and tool-selection queries.
- Every meaningful change runs a **Loop** and, when durable, deposits a **Lesson**
  in the Learning Ledger that future planning consults.

## 3. The three spines (how "done" is defined)

A requirement is not done when someone says so. It is done when three chains
close on it:

```
VALUE :  UserStory ──derived_from──> Requirement ──implements──> Capability
BUILD :  Capability ──realized_by──> Component ──satisfied_by──> Task ──uses_tool──> Tool
TRUST :  Task ──verified_by──> Test ──verifies──> Requirement
```

`graph.py trace` reports any requirement missing a spine. This single rule
replaces a pile of process ceremony: coverage, traceability, and test-linkage are
one query.

## 4. Loop Engineering, operationalized

SKGDD defines six named loops. Each is a first-class `Loop` node when it runs.

| Loop | Observe | Orient | Decide | Act | Reflect |
|------|---------|--------|--------|-----|---------|
| **Discovery** | raw inputs, stakeholders | cluster into stories | what's in scope | create US-*/R-* | note unknowns as Q-* |
| **Specification** | requirements + questions | ambiguities, conflicts | sharpen or split | edit R-*, raise confidence | any new Q-* |
| **Planning** | requirements, constraints | architecture options | choose components/tools | create CMP-*/D-*/TL-* | record trade-offs |
| **Implementation** | task queue | dependencies | next unblocked task | write code, update T-* | discoveries → Loop |
| **Verification** | test results, telemetry | which spine broke | smallest fix | fix + rerun TST-* | failing pattern → Lesson |
| **Learning** | recent Loops | recurring signals | change a rule? | append LS-*, amend C-* | tool annotations |

The **fast loop** is Implementation↔Verification (minutes). The **slow loop** is
Discovery→Specification→Planning (the graph reshaping). The **meta loop** is
Learning, which edits the rules the other loops follow. Accuracy compounds
because each pass leaves the graph — and the ledger — smarter than it found them.

## 5. What SKGDD adds that neither parent had

1. **Traceability matrix for free** — the three spines, checked by one command.
2. **Change-impact analysis** — `graph.py impact <ID>` walks reverse-dependency
   edges to show the blast radius *before* you change anything. Neither Spec Kit
   nor OKF can do this.
3. **A tool graph** — capabilities and tools are nodes; selection is a ranked,
   reasoned, recorded decision, scaling to hundreds of tools without chaos.
4. **Confidence & provenance on every node** — the kit knows *how sure* it is and
   *where a fact came from*, so it can prioritize what to clarify.
5. **A learning ledger** — lessons are durable, evidence-linked, and feed back
   into planning and tool selection. The project improves its own understanding.
6. **Drift reconciliation** — `/skgdd.reconcile` keeps graph, spec, and code
   honest, because a stale graph is worse than none.

## 6. Accurate *and* flexible

These usually trade off. SKGDD keeps both:

- **Accuracy** comes from the schema: legal node types, legal edges, required
  fields, and validation that rejects orphan tasks, untested "done" requirements,
  and dangling links.
- **Flexibility** comes from the medium: it is all plain Markdown with YAML. You
  can hand-write a node, an agent can generate a hundred, and any OKF/agent tool
  can read the result. There is no database to migrate and no lock-in.

## 7. Extending the kit

- **New node types / edges** — extend `.skgdd/schema/*` and the `NODE_TYPES` /
  `INVERSE` maps in `graph.py`.
- **New commands** — drop a `.github/prompts/skgdd.<name>.prompt.md` file.
- **Visualization** — `graph.json` is emitted on every build; feed it to any
  graph viewer (D3, Cytoscape, Mermaid, Obsidian) to *see* the requirement map.
- **Presets/bundles** — like Spec Kit, you can package role- or domain-specific
  template overrides; because artifacts are OKF bundles, they are shareable as-is.

## 8. Honest limits (v0.1)

- The graph engine's tool ranking is a transparent heuristic, not an optimizer —
  it surfaces candidates and rationale; humans still decide.
- Reverse-tracing code against the graph (`/skgdd.reconcile`) is only as good as
  the agent running it; treat its drift report as advice.
- Like SDD generally, up-front graphing has a cost; for a throwaway script, skip
  it. The payoff scales with the number of requirements, tools, and tasks — which
  is exactly the "hundreds of interlinked things" case this kit was built for.
