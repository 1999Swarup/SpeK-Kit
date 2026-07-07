---
description: Compute the SKGDD eval metrics and compare against a spec-only baseline.
---

# /skgdd.metrics

You produce objective evidence that SKGDD improves on a spec-only workflow.

Process:
1. Run `python .skgdd/scripts/graph.py metrics knowledge` (writes `metrics.json`).
2. Present the seven metric groups (A–G): requirement understanding,
   traceability, execution efficiency, loop effectiveness, cognitive load,
   AI effectiveness, enterprise readiness.
3. Interpret each: what a healthy value looks like and where this bundle stands.
4. Contrast with the **spec-only baseline** — trace coverage, impact visibility,
   loop effectiveness, and compliance coverage are structurally undefined without
   a graph, so SKGDD wins those by construction.
5. Flag the two weakest metrics and recommend the next command to improve them
   (e.g. low trace coverage → `/skgdd.tasks`; high ambiguity → `/skgdd.clarify`).

See `evals.md` for the metric definitions and expected-outcome table.

Output: the metrics table, the baseline contrast, and the top-2 improvement moves.
