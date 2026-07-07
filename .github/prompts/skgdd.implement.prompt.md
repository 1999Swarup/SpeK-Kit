---
description: Execute tasks in dependency order, keeping the graph in sync with the code.
---

# /skgdd.implement

You are building. The graph is your task queue and your source of truth.

Process:
1. Run `graph.py analyze` first; refuse to start if a `must` requirement is
   blocked or has a GAP.
2. Topologically order tasks by `depends_on`. Implement the first unblocked task.
3. As you complete each task:
   - Set the `T-*` node `status: done`.
   - Run its linked `TST-*`; set the test `status: passing|failing`.
   - If the test fails or you discover something new, open a `Loop` (see
     `/skgdd.loop`) instead of silently patching.
4. After each task, rebuild the graph so trace/coverage stay live.
5. When a requirement's tasks are done and tests pass, set it `verified`.

Output: per-task progress, test results, and any Loops opened.
