---
id: PACK-data
type: KnowledgePack
title: Data Knowledge Pack
description: Data modeling, storage, migration, and privacy best practices, rules, and tools.
status: active
layer: L3
domain: data
version: 0.1.0
owner: "@data"
tags: [pack, data]
created: 2026-07-06
updated: 2026-07-06
---

# Data Knowledge Pack

## Best practices
- Model the domain first; choose storage second.
- Every table/collection has an owner and a retention policy.
- Migrations are forward-only and reversible-by-design.
- PII is classified, minimized, and encrypted at rest.

## Validation rules (checked at /skgdd.analyze)
- [ ] Each data Component declares its consistency and durability needs.
- [ ] Any PII field links to a governing privacy Constraint.
- [ ] Schema changes have a migration Task and a rollback note.

## Recommended tools
- `TL-postgres` — relational default.
- `TL-migrations` — versioned schema migrations.

## Anti-patterns (flag if seen)
- Storing derived data as source of truth.
- Unbounded row growth with no archival/retention plan.
- Cross-service shared database coupling.
