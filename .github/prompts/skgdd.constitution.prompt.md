---
description: Create or update the project constitution — the non-negotiable principles that govern every node.
---

# /skgdd.constitution

You are establishing the governance spine of an SKGDD bundle.

1. Read `.skgdd/memory/constitution.md` and `.skgdd/schema/*` for context.
2. Interview the user (or infer from their prompt) for principles across: code
   quality, testing, security/privacy, tool-adoption policy, reversibility, and
   how loops/learning are handled.
3. Write each principle as a `C-*` article with a stable ID and a one-line rule.
4. Every article is a node that can `govern` other nodes.
5. Do NOT invent scope. Keep articles few, sharp, and enforceable — `/skgdd.analyze`
   will check nodes against them.

Output: an updated `.skgdd/memory/constitution.md`. Report the article IDs created.
