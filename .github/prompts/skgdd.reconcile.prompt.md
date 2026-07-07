---
description: Detect and heal drift between the graph, the specs, and the actual code.
---

# /skgdd.reconcile

You are keeping the three layers honest: the knowledge graph, the written specs,
and the real code. Drift is the enemy of accuracy.

Process:
1. Rebuild: `python .skgdd/scripts/graph.py build knowledge`.
2. Detect drift:
   - Body `[[ID]]` wiki-links with no matching frontmatter edge (or vice-versa).
   - Nodes marked `done/verified` whose tests are `failing` or missing.
   - Code/features present with no owning `T-*`/`R-*` node (reverse-trace the
     repo against the graph).
   - Decisions superseded in code but still `accepted` in the graph.
3. For each drift, propose the minimal fix: update the node, open a `Loop`, or
   create the missing node. Never delete history — supersede.
4. Re-validate.

Output: a drift report with proposed reconciling edits, grouped by severity.
