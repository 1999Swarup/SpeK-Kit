---
id: IP-XXXX
type: IntegrationPoint
title: <external boundary, e.g. "Billing via Stripe webhook">
description: <one sentence>
status: active           # active|deprecated|planned
layer: L2
confidence: high
owner: "@team"
tags: [integration]
created: 2026-07-06
updated: 2026-07-06
external_refs: []        # [doc:..., pr:...]
# --- links ---
depends_on: []           # TL-* / CurrentState it relies on
related_to: []
constrained_by: []       # LegacyConstraint nodes
---

# <title>

## Boundary
<What system we integrate with, direction of data, protocol.>

## Contract
<Payload shape, auth, rate limits, failure modes.>

## Risk / fragility
<What breaks if the other side changes. Link RK-* if material.>
