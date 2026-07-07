---
id: CS-FS-001
type: CurrentState
title: Scheduling today is manual on a dispatcher whiteboard/board
description: Existing brownfield reality the new design must replace and de-risk.
status: observed
layer: L2
confidence: high
source: "interview:dispatch-lead:2026-07-02"
owner: "@field-service"
tags: [brownfield, scheduling]
created: 2026-07-07
updated: 2026-07-07
constrains: [R-FS-001]
traces_to: [R-FS-001]
---

# Scheduling today is manual on a dispatcher board

## Observed fact
Dispatchers assign ~400 work orders/day by hand using the schedule board; skills
matching is tribal knowledge and travel time is not optimized.

## Implication for the new design
R-FS-001 must preserve a manual-override path (dispatchers will not accept a
black box) and prove parity before RSO is trusted to auto-book.
