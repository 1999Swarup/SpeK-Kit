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
| `PACK-dynamics365` | Dynamics 365 / Dataverse | `/skgdd.pack dynamics365` |

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
