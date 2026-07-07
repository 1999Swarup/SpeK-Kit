---
description: Brownfield current-state extraction — capture what exists today before designing the target.
---

# /skgdd.extract

You are building the Current-State Intelligence Layer. **Reality before design**
(constitution C-BROWN-01). Do this before `/skgdd.specify` on any existing system.

Process:
1. Explore the existing codebase/system (read code, config, runbooks, telemetry).
2. Create nodes from the templates:
   - `CS-*` `CurrentState` — concrete facts about what exists today (with `source`
     and `confidence`, because old assumptions rot).
   - `LegacyConstraint` — limits you cannot change yet; `constrains` new nodes.
   - `IP-*` `IntegrationPoint` — every boundary with an external/legacy system.
   - one `SystemMap` (L3) node summarizing how today's system fits together.
3. Link current-state nodes to the target design via `traces_to` / `constrains`.
4. Rebuild the graph and run `graph.py lint`.

Loop: `existing system → extract → map → compare → design → validate against reality`.

Output: current-state nodes, the system map, and the constraints the new spec
must respect.
