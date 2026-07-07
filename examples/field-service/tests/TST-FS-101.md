---
id: TST-FS-101
type: Test
title: RSO books the best-fit technician and flags when none eligible
description: Acceptance test for the auto-scheduling requirement.
level: acceptance
status: passing
confidence: high
owner: "@qa"
created: 2026-07-07
updated: 2026-07-07
verifies: [R-FS-001]
---

# RSO books the best-fit technician and flags when none eligible

## Method
- Given a work order with skills + location, when RSO runs, then a booking to an
  eligible resource is created within SLA.
- Given no eligible resource, then the work order is flagged for manual dispatch.

## Last result
- status: passing
