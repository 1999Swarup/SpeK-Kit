---
id: TST-FS-201
type: Test
title: Offline edits sync and conflicts resolve without data loss
description: Acceptance test for offline mobile with conflict resolution.
level: acceptance
status: passing
confidence: high
owner: "@qa"
created: 2026-07-07
updated: 2026-07-07
verifies: [R-FS-002]
---

# Offline edits sync and conflicts resolve without data loss

## Method
- Given no network, then assigned work orders are available offline.
- Given concurrent edits, when reconnected, then the conflict policy applies and
  no field is silently lost.

## Last result
- status: passing
