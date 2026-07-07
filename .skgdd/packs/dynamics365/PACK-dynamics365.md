---
id: PACK-dynamics365
type: KnowledgePack
title: Dynamics 365 / Dataverse Knowledge Pack
description: Model-driven app, plugin, and Dataverse best practices, rules, and tools.
status: active
layer: L3
domain: dynamics365
version: 0.1.0
owner: "@d365"
tags: [pack, dynamics365, dataverse]
created: 2026-07-06
updated: 2026-07-06
---

# Dynamics 365 / Dataverse Knowledge Pack

## Best practices
- Prefer platform features (business rules, flows) before custom code.
- Plugins are stateless, fast, and defensive; heavy work goes async.
- Solutions are the unit of change; keep managed/unmanaged discipline.
- Least-privilege security roles; test with a non-admin user.

## Validation rules (checked at /skgdd.analyze)
- [ ] Each custom table has an ownership and security-role plan.
- [ ] Each plugin step declares message, stage, and filtering attributes.
- [ ] Requirements needing customization link a solution export Task.

## Recommended tools
- `TL-pac-cli` — Power Platform CLI for solution lifecycle.
- `TL-dataverse-sdk` — typed data access.

## Anti-patterns (flag if seen)
- Synchronous plugins doing external I/O.
- Editing the default solution directly.
- Hard-coded GUIDs across environments.
