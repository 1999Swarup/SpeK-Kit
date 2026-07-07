---
description: Load a domain Knowledge Pack so its best practices, rules, and tools influence spec/plan/analyze.
---

# /skgdd.pack

You are activating domain grounding.

Process:
1. If the user names a domain, load `.skgdd/packs/<domain>/PACK-<domain>.md`.
   Available: security, data, frontend, dynamics365. If unsure, list them.
2. Announce the pack's **validation rules** — these become extra checks in
   `/skgdd.analyze`.
3. Seed `/skgdd.tools` with the pack's **recommended tools** (create `TL-*` nodes
   if missing) and note its **anti-patterns** to watch for.
4. Link the pack's `governs` edges into the active constitution where relevant.

Runtime: `select domain → load pack → influence spec + plan + validation`.

To author a new pack, copy `.skgdd/templates/knowledge-pack.node.md`.

Output: the activated pack, its rules now in force, and recommended tools.
