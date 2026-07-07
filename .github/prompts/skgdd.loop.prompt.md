---
description: Run one Loop Engineering iteration — Observe, Orient, Decide, Act, Reflect — and record it.
---

# /skgdd.loop

You are running the engine that makes SKGDD self-developing. A Loop is one pass of
Observe → Orient → Decide → Act → Reflect, recorded as an `L-*` node.

Trigger this whenever a signal arrives: a failing test, wrong estimate, new
requirement, telemetry, review comment, or a tool underdelivering.

Process:
1. **Observe** — gather the signal(s). Run `graph.py loop knowledge` for the radar.
2. **Orient** — locate the affected nodes in the graph. Which are now stale or wrong?
   Use `graph.py impact <ID>` to see the blast radius.
3. **Decide** — choose the *smallest correct* change (a node edit, a new Question,
   a re-prioritization). Prefer reversible moves (C-REV-01).
4. **Act** — make the edits. Record created/changed/spawned node IDs.
5. **Reflect** — did it resolve the signal? Write the `L-*` node from
   `loop.node.md`. If the insight is durable, hand off to `/skgdd.learn`.

Output: the Loop node, the nodes it touched, and whether a Lesson should be promoted.
