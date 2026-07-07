---
description: Turn a raw idea or a pile of requirements into atomic Requirement + UserStory + Question nodes in the graph.
---

# /skgdd.specify

You are converting intent into graph nodes. Focus on **what** and **why**, never
**how**.

Process:
1. Read `.skgdd/schema/node-types.md`, `.skgdd/schema/frontmatter.md`, and the
   templates in `.skgdd/templates/`.
2. Decompose the user's request into **atomic** requirements — one concept per
   node (Constitution article C-ATOM-01). If the input contains 100s of
   requirements, batch them but keep each as its own `R-*` file.
3. For each requirement create an `R-*` node from `requirement.node.md`:
   - Set `priority` (MoSCoW), `confidence`, and testable `acceptance` criteria.
   - Link `derived_from` to a `US-*` UserStory (create one if missing).
   - Link `governed_by` to any relevant `C-*` article.
4. For every ambiguity or unknown, create a `Q-*` Question node that `blocks` the
   requirement. **Do not paper over gaps** (C-CLAR-01).
5. Place files under `knowledge/requirements/`, `knowledge/stories/`,
   `knowledge/questions/`.
6. Run `python .skgdd/scripts/graph.py build knowledge` then `validate`.

Output: new nodes + a short summary of open questions that must be clarified.
