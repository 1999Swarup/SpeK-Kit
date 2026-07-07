---
id: RK-FS-002
type: Risk
title: IoT false positives create noisy predictive work orders
description: Poor thresholds or telemetry bursts flood dispatch with false work orders.
status: open
severity: med
likelihood: high
confidence: med
owner: "@platform"
tags: [iot, azure]
created: 2026-07-07
updated: 2026-07-07
threatens: [R-FS-003]
mitigated_by: [T-FS-301]
caused_by: [Q-FS-301]
---

# IoT false positives create noisy predictive work orders

## Mitigation
Thresholding + deduplication window (T-FS-301) and Dataverse throttling backoff.
Residual risk depends on the threshold decided in Q-FS-301.

## Early-warning signal
Spike in auto-created work orders per asset per hour.
