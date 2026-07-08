---
id: TL-plugin
type: Tool
title: Dataverse Plugin (C#)
description: Server-side, in-transaction business logic registered on messages.
status: proposed
category: server-logic
maturity: stable
cost: free
license: proprietary
confidence: high
tags: [dynamics365, plugin]
created: 2026-07-08
updated: 2026-07-08
provides: [CAP-server-logic]
depends_on: [TL-dataverse]
alternative_to: [TL-power-automate]
---

# Dataverse Plugin (C#)
Use only when transactional/synchronous logic is required and platform features
cannot express it — justify adoption in a Decision node.

## Known pitfalls
Synchronous plugins doing external I/O are an anti-pattern; keep them fast and
defensive, declare message/stage/filtering attributes explicitly.
