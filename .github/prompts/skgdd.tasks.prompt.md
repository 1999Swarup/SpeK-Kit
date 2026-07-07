---
description: Break the plan into executable, verifiable Task nodes with dependency edges and tests.
---

# /skgdd.tasks

You are creating the executable graph. Each task must be atomic, ordered, and
traceable.

Process:
1. For each requirement/component, create `T-*` Task nodes from `task.node.md`:
   - `satisfies` >= 1 requirement (no orphan work — validation enforces this).
   - `depends_on` other tasks to encode order; `blocks` where relevant.
   - `uses_tool` the adopted `TL-*`.
2. For each requirement's acceptance criteria, create a `TST-*` Test node that
   `verifies` it. This closes the trust spine.
3. Rebuild and run `graph.py trace` — every `must` requirement should now show
   `[OK ]` (value + build + trust). Fix any `GAP`.

Output: ordered task list, tests created, and a trace report confirming spines.
