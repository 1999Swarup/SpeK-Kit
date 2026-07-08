# SKGDD Knowledge Packs

Domain grounding for the kit. A pack bundles best practices, validation rules,
recommended tools, and anti-patterns for a domain. Selecting a pack injects that
intelligence into `/skgdd.specify`, `/skgdd.plan`, and `/skgdd.analyze`.

## Available packs

| Pack | Domain | Load with |
|------|--------|-----------|
| `PACK-security` | Secure development (OWASP-aligned) | `/skgdd.pack security` |
| `PACK-data` | Data modeling, storage, privacy | `/skgdd.pack data` |
| `PACK-frontend` | Accessibility, performance, UI arch | `/skgdd.pack frontend` |
| `PACK-dynamics365` | Dynamics 365 / Dataverse (ships a tool library + ALM lifecycle) | `/skgdd.pack dynamics365` |

## The Dynamics 365 pack ships a tool library

`PACK-dynamics365` is enriched beyond guidance: it includes ready-made
`Capability` and `Tool` nodes under `dynamics365/capabilities/` and
`dynamics365/tools/`, mapped to the skills available in this workspace
(`dv-metadata`/`dv-data`/`dv-query`, `dv-solution`/PAC CLI, Power Automate,
plugins, business rules, Copilot Studio `author`). Copy the ones you use into your
requirement bundle so `/skgdd.tools` ranks real, backed options and the ALM
lifecycle (`stage` → DEV/TEST/PROD) is explicit.

## Runtime behaviour

```
select domain → load pack → influence spec + plan + validation
```

When a pack is active, its `validation rules` become extra checks in
`/skgdd.analyze`, its `recommended tools` seed `/skgdd.tools`, and its
`anti-patterns` are flagged during review.

## Authoring a pack

Copy `.skgdd/templates/knowledge-pack.node.md`, set `domain`, and fill the four
sections. Packs are ordinary `KnowledgePack` nodes, so they live in the graph and
can `govern` constitution articles and recommend `Tool` nodes.
