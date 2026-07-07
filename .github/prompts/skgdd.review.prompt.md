---
description: Post-implementation review + amendment loop. A task is not done until validated, reviewed, and learned.
---

# /skgdd.review

You run the Completion & Evolution loop:
`implement → validate → review → amend → stabilize → learn` (constitution C-DONE-01).

Process:
1. Pick a completed Task/Requirement. Confirm its `TST-*` is passing.
2. Create an `RV-*` `Review` node from `review.node.md`:
   - Check acceptance criteria, governing `C-*` articles, tests, and drift.
3. For each accepted change, create an `AM-*` `Amendment` node that `amends` the
   affected node (supersede, never overwrite — C-REV-01). Run
   `graph.py impact <id>` and record the blast radius in the amendment.
4. Capture durable insight via `/skgdd.learn` (a `Lesson`). If none, say so.
5. Only then set the node `stage: validated` → `learned` and `status: verified`.

Output: the review record, amendments, learning captured, and the node's new stage.
