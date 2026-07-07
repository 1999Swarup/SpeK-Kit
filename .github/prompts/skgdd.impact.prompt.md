---
description: Show the blast radius of changing a node before you change it.
---

# /skgdd.impact

You are performing change-impact analysis — a capability neither Spec Kit nor OKF
provides.

Process:
1. Ask for (or infer) the node ID the user intends to change.
2. Run `python .skgdd/scripts/graph.py impact <ID> knowledge`.
3. Explain the blast radius in plain language: which requirements, tasks, tests,
   tools, and risks are downstream, and which tests will need re-running.
4. Recommend the smallest safe change and whether it warrants a new `D-*`
   Decision (if it reverses a prior one) or a `Loop` record.

Output: the affected-node list grouped by type, plus a change recommendation.
