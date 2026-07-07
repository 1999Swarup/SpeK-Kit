---
description: Produce the technical plan — Components, Decisions, and Constraints wired into the graph.
---

# /skgdd.plan

You are turning accepted requirements into an architecture, expressed as nodes.

Process:
1. Confirm no `must` requirement is blocked (run `graph.py validate`).
2. Create `CMP-*` Component nodes for the units of the solution; link
   `implements` to Capabilities and `depends_on` between components.
3. Record every significant technical choice as a `D-*` Decision node with
   alternatives and reversibility (C-REV-01). Link `uses_tool` to `TL-*`.
4. Capture boundaries as `Constraint` nodes and `constrains` the affected nodes.
5. Identify threats as `RK-*` Risk nodes; link `threatens` and `mitigated_by`.
6. Rebuild the graph and run `graph.py trace` to see which requirements still
   lack a build spine.

Output: components, decisions, constraints, risks, and the still-open build gaps.
