---
id: PACK-security
type: KnowledgePack
title: Security Knowledge Pack
description: OWASP-aligned best practices, validation rules, tool picks, and anti-patterns for secure development.
status: active
layer: L3
domain: security
version: 0.1.0
owner: "@security"
tags: [pack, security]
created: 2026-07-06
updated: 2026-07-06
governs: [C-SEC-01]
---

# Security Knowledge Pack

Selecting this pack injects security intelligence into specify/plan/analyze.

## Best practices
- Validate and encode all input at trust boundaries.
- Secrets live in a vault, never in nodes, code, or logs.
- Principle of least privilege for every identity and token.
- Short-lived, single-use tokens for sensitive flows (reset, invite).

## Validation rules (checked at /skgdd.analyze)
- [ ] Every endpoint requirement has an authn/authz acceptance criterion.
- [ ] No node contains a literal secret, key, or connection string.
- [ ] Password/token requirements specify entropy, expiry, and lockout.
- [ ] OWASP Top 10 reviewed for each externally reachable Component.

## Recommended tools
- `TL-vault` — secret storage.
- `TL-oauth` — delegated auth over hand-rolled sessions.

## Anti-patterns (flag if seen)
- Rolling your own crypto.
- Unbounded retry / no rate limiting on auth endpoints.
- Storing reset tokens in plaintext.
