---
id: T-XXXX
type: Task
title: <verb-first action, e.g. "Implement password reset endpoint">
description: <one sentence>
status: draft            # draft|proposed|accepted|in-progress|blocked|done|verified
estimate: M              # XS|S|M|L|XL or hours
confidence: med
owner: "@dev"
tags: []
created: 2026-07-06
updated: 2026-07-06
# --- trace ---
satisfies: []            # R-* this task fulfills (>=1 required)
derived_from: []         # plan section or parent task
# --- execution graph ---
depends_on: []           # T-* that must finish first
blocks: []               # T-* waiting on this
uses_tool: []            # TL-* tools/libraries/services used
# --- trust ---
verified_by: []          # TST-* that proves completion
mitigates: []            # RK-* this task reduces
---

# <title>

## Objective
<What concrete artifact/behavior this produces.>

## Steps
1. ...
2. ...

## Definition of done
- [ ] Code/artifact exists and is committed.
- [ ] Linked TST-* passes.
- [ ] No governing C-* article violated.

## Notes / discoveries
<Anything learned while doing this feeds the next Loop.>
