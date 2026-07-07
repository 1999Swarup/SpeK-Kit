---
id: LEARNING-LEDGER
type: Schema
title: Learning Ledger
description: Append-only record of lessons the kit has learned. This is the memory that makes SKGDD self-developing.
version: 0.1.0
---

# Learning Ledger

This is the kit's long-term memory. Loops produce observations; durable
observations are promoted here as `Lesson` nodes. `/skgdd.learn` reads and
appends; `/skgdd.plan` and `/skgdd.tools` consult it so the system stops
repeating mistakes — the mechanism behind "self-develop like a human."

## How a lesson is born

```
Loop iteration → observed signal (test failed, estimate wrong, tool underdelivered)
   → if it will recur → write Lesson (LS-*)
   → if it should change the rules → amend Constitution (C-*)
   → if it should change tool selection → annotate the Tool node
```

Each lesson records **evidence**, **the change it caused**, and **the nodes it
now informs**, so its influence is auditable — not a vague "we should do better."

## Ledger

<!-- Newest first. Append via /skgdd.learn. Never rewrite history; supersede. -->

### LS-0001 — Example lesson (delete me)
- **type:** Lesson
- **evidence:** L-2026-07-06-a — acceptance test TST-0101 failed because R-0042 never specified lockout after N attempts.
- **root cause:** requirement authored with `confidence: med` and no blocking Question.
- **change:** added Q-0005 template check to `/skgdd.clarify`; raised R-0042 acceptance criteria.
- **informs:** [R-0042]
- **amends:** [C-CLAR-01]
- **status:** active
