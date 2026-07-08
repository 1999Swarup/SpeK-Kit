---
id: TL-pac-cli
type: Tool
title: Power Platform CLI (PAC)
description: Command-line solution lifecycle — export, unpack, import, promote.
status: accepted
category: alm
maturity: stable
cost: free
license: proprietary
confidence: high
tags: [dynamics365, alm]
created: 2026-07-08
updated: 2026-07-08
provides: [CAP-alm]
depends_on: [TL-dataverse]
---

# Power Platform CLI (PAC)
Backed here by the `dv-solution` skill. The unit of change is the solution.

## Known pitfalls
Never edit the default solution; avoid hard-coded GUIDs across environments.
