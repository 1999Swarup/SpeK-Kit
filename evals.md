---
type: Article
title: SKGDD Evals & Metrics
description: Objective measurement of SKGDD versus a spec-only (Spec Kit) workflow, with definitions and expected outcomes.
version: 0.1.0
---

# SKGDD Evals & Metrics

If SKGDD is better than a spec-only workflow, it should be **measurable**. This
document defines the metrics, how the engine computes them, and the outcomes to
expect. Run them anytime with:

```powershell
python .skgdd/scripts/graph.py metrics knowledge   # writes metrics.json
```

Because the metrics are derived from the graph, several of them are **structurally
impossible** in a spec-only workflow — there is no graph to measure. Those are the
clearest wins.

## A. Requirement understanding

| Metric | Definition | How computed | Direction |
|--------|-----------|--------------|-----------|
| **Ambiguity score** | % of requirements needing clarification | requirements that are `confidence: low` or blocked by an open `Question` | lower is better |
| **Clarification cycles** | avg iterations before a spec settles | count of `Loop` nodes of `loop_kind: specification` per requirement | lower over time |
| **Requirement drift** | changes after implementation started | count of `Amendment` nodes + requirements with `amended_by` | lower is better |

*Why SKGDD improves it:* the graph gives every requirement its surrounding
context (stories, constraints, questions), so ambiguity is surfaced and resolved
before planning instead of discovered mid-build.

## B. Traceability

| Metric | Definition | How computed | Direction |
|--------|-----------|--------------|-----------|
| **Trace coverage** | % nodes with a valid req→spec→task→test chain | requirements closing all three spines ÷ requirements | higher is better |
| **Orphan rate** | nodes with no connections | unconnected nodes ÷ total nodes | lower is better |
| **Broken link rate** | invalid references | dangling edges (target missing) | → 0 |

*Spec-only baseline:* undefined — flat files have no computable trace graph.

## C. Execution efficiency

| Metric | Definition | How computed | Direction |
|--------|-----------|--------------|-----------|
| **Spec→task conversion time** | time to break a spec into tasks | wall-clock (recorded per session) | lower over time |
| **Task rework rate** | % tasks rewritten | tasks with `amended_by` or `status: blocked` ÷ tasks | lower is better |
| **Cycle time** | requirement → deployment | timestamps on stage transitions | lower over time |

## D. Loop effectiveness

| Metric | Definition | How computed | Direction |
|--------|-----------|--------------|-----------|
| **Learning capture rate** | % done tasks with a learning | done tasks with `informed_by`/`changed_by` ÷ done tasks | higher is better |
| **Repeat failure rate** | same issue recurring | Lessons sharing a tag/root cause | lower over time |
| **Auto-improvement rate** | updates triggered by loops | nodes touched by `Loop` `changed` edges | higher is better |

*Spec-only baseline:* zero — there is no loop or learning ledger.

## E. Cognitive load

| Metric | Definition | How computed | Direction |
|--------|-----------|--------------|-----------|
| **Files per feature** | files needed to grasp a feature | total nodes ÷ requirements (proxy) | lower is better |
| **Navigation time** | time to locate info | measured; L1 indexes reduce it | lower is better |
| **Avg sections per file** | file heft | mean `##` count; cap is 7 | bounded |

*Why SKGDD improves it:* auto-generated per-folder `index.md` (L1) plus atomic
nodes mean you open one small file, not scroll one giant one.

## F. AI effectiveness

| Metric | Definition | How computed | Direction |
|--------|-----------|--------------|-----------|
| **AI task success rate** | tasks completed without correction | recorded per implement run | higher is better |
| **Context completeness** | % required context available | nodes with description + at least one edge ÷ total | higher is better |
| **Correction rate** | human edits needed | recorded per run | lower is better |

*Why SKGDD improves it:* the agent receives a typed, connected context window
(the node plus its neighbours), not a wall of prose — fewer wrong guesses.

## G. Enterprise readiness

| Metric | Definition | How computed | Direction |
|--------|-----------|--------------|-----------|
| **Audit traceability** | can every change be traced? | nodes with `external_refs` + amendment history | higher is better |
| **Compliance coverage** | % requirements validated against policy | requirements with `governed_by` a `C-*` article ÷ requirements | higher is better |
| **Integration sync rate** | accuracy vs Jira/ADO | nodes whose `external_refs` reconcile in `/skgdd.sync` | higher is better |

## Expected outcomes vs spec-only

| Area | Spec Kit only | SKGDD |
|------|---------------|-------|
| Requirement clarity | Medium | **High** (graph context) |
| Traceability | Partial | **Complete** (three spines) |
| Scalability | Medium | **High** (atomic nodes) |
| AI usability | Good | **Excellent** (typed context) |
| Change-impact visibility | Low | **High** (`impact` command) |
| Learning reuse | Weak | **Strong** (Learning Ledger) |
| Enterprise readiness | Medium | **High** (sync + audit) |

## Honest notes

- Time-based metrics (conversion time, cycle time, AI success/correction rate)
  need per-session recording — the engine computes the graph-derived metrics and
  leaves slots for the timed ones.
- Static proxies (e.g. files-per-feature) are directional, not absolute. Track the
  **trend** across a project, not a single snapshot.
