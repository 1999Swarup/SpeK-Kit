# SKGDD — Spec & Knowledge-Graph Driven Development

> Packaged as **SpeK-Kit**.
>
> A developer kit that fuses **GitHub Spec Kit** (a workflow) with **Google's Open
> Knowledge Format** (a knowledge graph) and adds **Loop Engineering** (a
> self-improving feedback engine).
>
> Spec Kit gives you *process*. OKF gives you a *memory graph*. Neither has the
> other. SKGDD is both — plus the loop that lets the project **understand its own
> requirements better over time**, like a human would.

**License:** dual-licensed `MIT OR Apache-2.0` — see [LICENSE.md](LICENSE.md).

## Why this exists

| | Spec Kit | OKF | **SKGDD** |
|---|---|---|---|
| Workflow (specify→plan→tasks→implement) | ✅ | ❌ | ✅ |
| Cross-referenced knowledge graph | ❌ (flat files) | ✅ | ✅ |
| Traceability (requirement→task→test) | ❌ | ❌ | ✅ (three spines) |
| Change-impact / blast-radius analysis | ❌ | ❌ | ✅ (`graph.py impact`) |
| Tool catalogue & selection reasoning | ❌ | ❌ | ✅ (capability→tool map) |
| Learning / self-development | ❌ | ❌ | ✅ (Loops + Learning Ledger) |
| Machine-readable, agent-native | partial | ✅ | ✅ |

When you have **hundreds of requirements, hundreds of tools, and hundreds of
interlinked tasks**, a flat spec collapses. SKGDD turns every one of those into a
typed **node** in a directed graph so the hard questions become one command:

- *"If I change requirement R-0042, what breaks?"* → `graph.py impact R-0042`
- *"Which requirements aren't tested yet?"* → `graph.py trace`
- *"Which tool should I use for full-text search?"* → `graph.py tools`
- *"Where should I focus next?"* → `graph.py loop`

## The mental model: nodes, edges, spines, loops

- **Nodes** — one concept per Markdown file with OKF-style YAML frontmatter.
  Types: `Requirement`, `UserStory`, `Task`, `Tool`, `Capability`, `Decision`,
  `Risk`, `Test`, `Question`, `Component`, `Constraint`, `Milestone`, `Entity`,
  `Loop`, `Lesson`. See [.skgdd/schema/node-types.md](.skgdd/schema/node-types.md).
- **Edges** — typed links declared in frontmatter (`satisfies`, `verifies`,
  `uses_tool`, `depends_on`, `blocks`, …). See
  [.skgdd/schema/edge-types.md](.skgdd/schema/edge-types.md).
- **Three spines** — a requirement is only *done* when all three close:
  - **Value:** `UserStory → Requirement → Capability`
  - **Build:** `Capability → Component → Task → Tool`
  - **Trust:** `Task → Test → verifies → Requirement`
- **Loops** — every meaningful change runs Observe→Orient→Decide→Act→Reflect and
  is recorded, then promoted to a **Lesson** in the Learning Ledger. This is what
  makes the kit self-develop.

## Layout

```
SKGDD/
├─ README.md                     ← you are here
├─ methodology.md                ← the full SDD + OKF + Loop method
├─ meta-methodology.md           ← the self-evolving loops (traceability, drift, enrichment, impact)
├─ evals.md                      ← metric definitions + expected outcomes
├─ .skgdd/
│  ├─ memory/
│  │  ├─ constitution.md         ← non-negotiable principles (C-*)
│  │  └─ learning-ledger.md      ← lessons the kit has learned (LS-*)
│  ├─ schema/                    ← node types, edge types, frontmatter contract
│  ├─ templates/                 ← one template per node type (incl. current-state, review, amendment, pack)
│  ├─ packs/                     ← domain Knowledge Packs (security/data/frontend/dynamics365)
│  └─ scripts/graph.py           ← build / validate / lint / trace / impact / tools / loop / metrics
├─ .github/prompts/              ← /skgdd.* slash commands for your coding agent
└─ knowledge/                    ← YOUR bundle of nodes (a worked auth example ships here)
   ├─ index.md                   ← auto-generated manifest (OKF convention)
   ├─ graph.json                 ← auto-generated graph for tools/visualizers
   ├─ metrics.json               ← auto-generated eval metrics
   ├─ requirements/ stories/ questions/ capabilities/ tools/ tasks/ tests/ risks/
```

## Quickstart

```powershell
# 1. Build the graph from the example bundle (or your own)
python .skgdd/scripts/graph.py build knowledge     # + auto-generates per-folder index.md

# 2. Check integrity (schema, spines, blocked requirements, dangling edges)
python .skgdd/scripts/graph.py validate knowledge

# 3. Lint: typed-link enforcement + lifecycle guardrails + cognitive-load
python .skgdd/scripts/graph.py lint knowledge

# 4. See which requirements are fully traced
python .skgdd/scripts/graph.py trace knowledge

# 5. Impact analysis before changing anything
python .skgdd/scripts/graph.py impact R-0042 knowledge

# 6. Rank tools per capability
python .skgdd/scripts/graph.py tools knowledge

# 7. Ask the loop where to focus
python .skgdd/scripts/graph.py loop knowledge

# 8. Eval metrics — objective SKGDD-vs-spec-only measurement
python .skgdd/scripts/graph.py metrics knowledge   # writes metrics.json
```

## Workflow (slash commands)

Run these with your coding agent (prompts live in `.github/prompts/`):

```
Core workflow
/skgdd.constitution   → set the guardrails (C-*)
/skgdd.extract        → brownfield: capture current state before designing
/skgdd.specify        → requirements + stories + questions as nodes
/skgdd.clarify        → resolve blocking questions (Loop step)
/skgdd.pack <domain>  → load a domain Knowledge Pack (security/data/frontend/d365)
/skgdd.tools          → capability→tool catalogue + adoption decisions
/skgdd.plan           → components, decisions, constraints, risks
/skgdd.tasks          → executable tasks + tests (closes the trust spine)
/skgdd.analyze        → go/no-go gate over the whole graph
/skgdd.implement      → build in dependency order, graph stays in sync
/skgdd.review         → post-implementation review + amendments (done = validated+reviewed+learned)

Meta-methodology (always-on)
/skgdd.lint           → typed-link + lifecycle + cognitive-load checks
/skgdd.impact <ID>    → blast-radius simulation before a change
/skgdd.reconcile      → heal drift between graph, specs, and code
/skgdd.loop           → run one Observe→Orient→Decide→Act→Reflect iteration
/skgdd.learn          → promote lessons into long-term memory
/skgdd.sync           → sync graph ↔ Jira / Azure DevOps / GitHub
/skgdd.metrics        → compute eval metrics vs spec-only baseline
```

## Which gap does what solve?

| Gap in Spec Kit / OKF | SKGDD answer | Where |
|-----------------------|--------------|-------|
| Untyped links / ambiguity | Typed Knowledge Enforcement (lint suggests the edge) | `graph.py lint`, [frontmatter.md](.skgdd/schema/frontmatter.md) |
| OKF has no workflow | Lifecycle stages + guardrails | `stage:` field, [node-types.md](.skgdd/schema/node-types.md) |
| Markdown explosion | 3-layer model + auto per-folder `index.md` + 7-section cap | `graph.py build`/`lint` |
| Brownfield blind spot | Current-State Intelligence Layer | `/skgdd.extract`, `CurrentState`/`SystemMap` nodes |
| Later-lifecycle gaps | Completion & Evolution loop | `/skgdd.review`, `Review`/`Amendment` nodes |
| Enterprise integration | System-of-Record sync | `external_refs`, `/skgdd.sync` |
| Domain grounding | Knowledge Packs | [.skgdd/packs/](.skgdd/packs/), `/skgdd.pack` |
| No self-improvement | Meta-Methodology loops | [meta-methodology.md](meta-methodology.md) |
| No proof of value | Eval metrics | [evals.md](evals.md), `graph.py metrics` |


## What makes it unique

1. **Graph-first, not file-first.** Every requirement/task/tool/decision is an
   addressable node — traceability and impact analysis are graph walks, not
   full-text searches.
2. **Tool intelligence Spec Kit lacks.** A first-class capability→tool map scales
   to hundreds of tools and ranks them with recorded rationale.
3. **Loop Engineering built in.** The project observes itself (tests, telemetry,
   reviews), reorients the graph, and learns — accuracy compounds over time.
4. **OKF-native.** The bundle *is* a valid OKF knowledge bundle, so any
   OKF/agent tool can read it, and you get an agent-navigable graph for free.
5. **Accurate *and* flexible.** The schema makes the graph strict enough to
   validate, while everything is still plain Markdown you can hand-edit.

See [methodology.md](methodology.md) for the complete method and rationale.
