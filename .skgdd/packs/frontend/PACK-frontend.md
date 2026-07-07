---
id: PACK-frontend
type: KnowledgePack
title: Frontend Knowledge Pack
description: Accessibility, performance, and component-architecture best practices for UI work.
status: active
layer: L3
domain: frontend
version: 0.1.0
owner: "@frontend"
tags: [pack, frontend]
created: 2026-07-06
updated: 2026-07-06
---

# Frontend Knowledge Pack

## Best practices
- Accessibility (WCAG AA) is an acceptance criterion, not a follow-up.
- Budget performance: define a target for LCP/CLS/TTI up front.
- Prefer composition over configuration for components.
- Keep state local; lift only when shared.

## Validation rules (checked at /skgdd.analyze)
- [ ] Each UI requirement has an a11y acceptance criterion.
- [ ] Each interactive Component has a performance budget.
- [ ] Loading, empty, and error states are specified.

## Recommended tools
- `TL-vite` — fast build/dev.
- `TL-testing-library` — user-centric component tests.

## Anti-patterns (flag if seen)
- Inaccessible custom controls (div-as-button).
- Blocking the main thread with heavy synchronous work.
- Prop-drilling deep trees instead of composing.
