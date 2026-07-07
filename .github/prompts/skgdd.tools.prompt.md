---
description: Build the tool catalogue — map capabilities to candidate tools, rank them, and record adoption as decisions.
---

# /skgdd.tools

You are building the tool-selection layer that Spec Kit lacks. This scales to
100s of tools by making each a node linked to the capabilities it provides.

Process:
1. Derive `CAP-*` Capability nodes from the requirements/plan (the abstract
   abilities the system needs).
2. For each candidate tool create a `TL-*` node from `tool.node.md`:
   - Fill `category`, `maturity`, `cost`, `license`.
   - Link `provides` to the capabilities it satisfies.
   - Link `alternative_to` between competing tools; `conflicts_with` when
     incompatible; `depends_on` for prerequisites.
3. Consult `.skgdd/memory/learning-ledger.md` — surface past lessons about each
   tool under "Known pitfalls".
4. Run `python .skgdd/scripts/graph.py tools knowledge` to rank tools per
   capability. Where a capability has no provider, flag it as a GAP.
5. For each adopted tool, create a `D-*` Decision (C-TOOL-01) listing the
   alternatives considered; set the chosen tool `status: accepted`, `chosen_by`.

Output: capability→tool map, ranked candidates, adoption decisions, and any
capability gaps needing new tools.
