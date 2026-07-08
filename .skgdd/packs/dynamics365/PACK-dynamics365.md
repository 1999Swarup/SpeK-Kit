---
id: PACK-dynamics365
type: KnowledgePack
title: Dynamics 365 / Dataverse Knowledge Pack
description: Model-driven app, plugin, and Dataverse best practices, rules, tools, and ALM lifecycle for Power Platform.
status: active
layer: L3
domain: dynamics365
version: 0.2.0
owner: "@d365"
tags: [pack, dynamics365, dataverse, powerplatform, alm]
created: 2026-07-06
updated: 2026-07-08
needs_tool: [TL-dataverse, TL-power-automate, TL-plugin, TL-business-rule, TL-copilot-studio, TL-pac-cli]
governs: [C-SEC-01]
---

# Dynamics 365 / Dataverse Knowledge Pack

Selecting this pack injects D365/Power Platform intelligence into
`/skgdd.specify`, `/skgdd.plan`, `/skgdd.tools`, and `/skgdd.analyze`.

## Best practices
- Prefer platform features (business rules, flows) before custom code.
- Plugins are stateless, fast, and defensive; heavy or external work goes async.
- Solutions are the unit of change; keep managed/unmanaged discipline.
- Least-privilege security roles; test with a non-admin user.
- Idempotency for anything that creates records from external events (dedup key).

## Recommended tools (this workspace)
Map capabilities to the tools actually available here. The nodes live in
`.skgdd/packs/dynamics365/tools/` and are ranked by `/skgdd.tools`.

| Tool node | Backed by (skill/service) | Use for |
|-----------|---------------------------|---------|
| `TL-dataverse` | `dv-metadata`, `dv-data`, `dv-query` | tables, columns, relationships, records |
| `TL-power-automate` | Power Automate cloud flows | event automation, routing, integration |
| `TL-plugin` | Dataverse plugin (C#) | synchronous/transactional server logic |
| `TL-business-rule` | model-driven business rules | no-code field logic, UI behavior |
| `TL-copilot-studio` | `author` (Copilot Studio) | conversational agents, topics, actions |
| `TL-pac-cli` | `dv-solution` (PAC CLI) | solution export/import, ALM |

## Validation rules (checked at /skgdd.analyze)
- [ ] Each custom table has an ownership model and a security-role plan.
- [ ] Each plugin step declares message, stage, and filtering attributes.
- [ ] Prefer business rule / flow over plugin unless a plugin is justified in a Decision.
- [ ] Requirements needing customization link a `TL-pac-cli` solution-export Task.
- [ ] External-event record creation is idempotent (dedup window defined).
- [ ] Secrets (client secrets, connection strings) never appear in nodes.

## Anti-patterns (flag if seen)
- Synchronous plugins doing external I/O or long-running work.
- Editing the default solution directly.
- Hard-coded GUIDs / environment URLs across environments.
- Broad security roles ("System Administrator" for app users).
- Duplicating an existing table/column/flow (run `/skgdd.extract` first).

## Power Platform ALM lifecycle (maps to SpeK-Kit `stage`)
SpeK-Kit lifecycle stages map onto standard Power Platform ALM so `stage` reflects
real deployment progress. Track deployment items via `external_refs` (Azure DevOps).

| SpeK-Kit `stage` | Power Platform ALM step |
|------------------|-------------------------|
| `specified` | requirement agreed; unmanaged solution scoped in DEV |
| `planned` | components + tasks defined; solution structure created |
| `implemented` | built in DEV (tables/flows/plugins) in an unmanaged solution |
| `validated` | exported managed, imported to TEST, acceptance test passes |
| `learned` | promoted to PROD; review + lesson captured |

> Brownfield first: on an existing org, run `/skgdd.extract` (via `dv-connect` +
> `dv-query`/`dv-metadata`) before `/skgdd.specify` so new work does not duplicate
> or regress existing tables, plugins, flows, or security roles.
