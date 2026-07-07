---
id: L-YYYY-MM-DD-x
type: Loop
title: <what triggered this loop iteration>
description: <one sentence>
loop_kind: implementation   # discovery|specification|planning|implementation|verification|learning
status: closed              # open|closed
confidence: high
owner: "@agent-or-dev"
created: 2026-07-06
updated: 2026-07-06
# --- what this loop touched ---
observed: []               # nodes/signals examined
changed: []                # nodes changed as a result
spawned: []                # new nodes created (Q-*, RK-*, T-*, LS-*)
---

# <title>

Loop Engineering record. One pass of Observe → Orient → Decide → Act → Reflect.

## Observe (signals)
<Test results, telemetry, review comments, failing assumptions, new input.>

## Orient (make sense in the graph)
<How the signal changes our understanding. Which nodes are now wrong/stale?>

## Decide (choose the smallest correct change)
<The minimal graph edit or task that responds to the signal.>

## Act (what was done)
<Nodes created/updated; commits made.>

## Reflect (did it work? what's the lesson?)
<Outcome. If durable, promote to a Lesson (LS-*) in the Learning Ledger.>
