---
id: RK-FS-001
type: Risk
title: Offline sync conflicts cause silent data loss
description: Concurrent edits on device and server may overwrite each other.
status: mitigating
severity: high
likelihood: med
confidence: med
owner: "@field-service"
tags: [mobile, offline]
created: 2026-07-07
updated: 2026-07-07
threatens: [R-FS-002]
mitigated_by: [T-FS-202]
---

# Offline sync conflicts cause silent data loss

## Mitigation
Explicit conflict-resolution policy (T-FS-202): field-level merge for notes,
server-wins for status transitions, with an audit trail.

## Early-warning signal
Rising count of sync conflict events per technician — watch in the verification loop.
