---
id: RK-XXXX
type: Risk
title: <the threat, e.g. "Third-party auth provider outage">
description: <one sentence>
status: open             # open|mitigating|accepted|closed
severity: high           # low|med|high|critical
likelihood: med          # low|med|high
confidence: med
owner: "@team"
tags: []
created: 2026-07-06
updated: 2026-07-06
# --- links ---
threatens: []            # R-*/T-*/M-* endangered nodes
mitigated_by: []         # T-*/D-* actions reducing it
caused_by: []            # Assumption/Question nodes
---

# <title>

## Description
<What could go wrong and how it would manifest.>

## Exposure
- Severity: <impact if it happens>
- Likelihood: <how probable>
- Blast radius: <which nodes it threatens — auto-computed by the graph>

## Mitigation
<Linked T-*/D-* and residual risk after mitigation.>

## Early-warning signal
<What the Loop system should watch for to catch this early.>
