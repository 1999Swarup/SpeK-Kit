---
id: AM-XXXX
type: Amendment
title: <what changed, e.g. "Tighten reset token expiry to 10 minutes">
description: <one sentence>
status: applied          # proposed|applied
layer: L2
confidence: high
owner: "@team"
tags: [amendment]
created: 2026-07-06
updated: 2026-07-06
# --- links ---
amends: []               # the node(s) changed (R-*/D-*/CMP-*)
supersedes: []           # prior node version if replaced
caused_by: []            # Review/Loop/Test that triggered the change
---

# <title>

Records a change to an existing node **after** implementation, so history is
never lost (constitution C-REV-01: supersede, don't overwrite).

## What changed
<Before → after.>

## Why
<Trigger: review finding, failed test, new evidence. Link it.>

## Impact
<Run `graph.py impact <amended-id>` and summarize the blast radius here.>
