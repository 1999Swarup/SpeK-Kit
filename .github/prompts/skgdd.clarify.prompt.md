---
description: Resolve open Question nodes so must-priority requirements are unblocked before planning.
---

# /skgdd.clarify

You are closing knowledge gaps. This is a Loop Engineering step: observe unknowns,
decide answers, update the graph.

Process:
1. Run `python .skgdd/scripts/graph.py loop knowledge` to list open `Q-*` and
   low-confidence nodes.
2. For each open Question, ask the user the minimum set of questions needed to
   resolve it. Prefer concrete options over open-ended prompts.
3. When answered, create a `D-*` Decision node (`resolves` the Question, records
   alternatives) and set the Question `status: answered`, `answered_by: [D-*]`.
4. Raise the `confidence` of any requirement whose blocking questions are now closed.
5. Rebuild and re-validate the graph.

Stop condition: no `must`-priority requirement has an open blocking question.
Output: decisions made, requirements unblocked, remaining low-confidence areas.
