---
description: Run the graph linter — typed-link enforcement, lifecycle guardrails, and cognitive-load controls.
---

# /skgdd.lint

You enforce structural quality across the graph.

Run `python .skgdd/scripts/graph.py lint knowledge` and interpret the three groups:

1. **Typed Knowledge Enforcement** — every body `[[ID]]` link must be backed by a
   graph edge. For each finding, add the **suggested edge** to the node's
   frontmatter (or fix the link). Re-run until clean.
2. **Lifecycle guardrails** — a node cannot sit at a `stage` whose prerequisite
   is unmet. Either advance the missing prerequisite or correct the stage.
3. **Cognitive-load controls** — split any file over 7 `##` sections, resolve
   duplicate-title nodes, and connect or delete orphans. (`build` auto-creates
   per-folder `index.md`.)

Output: findings fixed and remaining ones with the exact edit to make.
