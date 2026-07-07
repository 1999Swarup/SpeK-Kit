---
id: TST-XXXX
type: Test
title: <what is being verified>
description: <one sentence>
level: acceptance         # unit|integration|acceptance|manual
status: pending           # pending|passing|failing|flaky
confidence: high
owner: "@qa"
created: 2026-07-06
updated: 2026-07-06
# --- trust spine ---
verifies: []              # R-*/T-* this test proves
---

# <title>

## Verifies
<Which requirement/task and which acceptance criterion.>

## Method
<Given / When / Then, or the concrete check performed.>

## Last result
- status: <pending|passing|failing>
- run: <date / CI link>
- notes: <if failing, this feeds a Loop>
