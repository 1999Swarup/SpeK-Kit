---
description: Cross-artifact consistency and coverage analysis over the whole graph before implementation.
---

# /skgdd.analyze

You are the gatekeeper before implementation. Use the graph, not guesswork.

Run and interpret:
1. `python .skgdd/scripts/graph.py build knowledge`
2. `python .skgdd/scripts/graph.py validate knowledge` — schema + trace + blocked checks.
3. `python .skgdd/scripts/graph.py trace knowledge` — spine coverage per requirement.
4. `python .skgdd/scripts/graph.py loop knowledge` — open questions, failing tests, live risks.

Then check, node by node, that no node violates a governing `C-*` article
(especially C-SEC-01 / OWASP). Report:
- Requirements missing a value/build/trust spine.
- Tasks that satisfy nothing; tools that provide nothing.
- Contradictions (`conflicts_with`) and dangling edges.
- Governance violations.

Do NOT proceed to implement while any `must` requirement has a GAP or a live
blocker. Output a go/no-go summary with the exact blocking node IDs.
