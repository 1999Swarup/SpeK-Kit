---
description: Sync the graph with enterprise systems-of-record (Jira, Azure DevOps, GitHub, docs).
---

# /skgdd.sync

You operate the System-of-Record Synchronization Layer (constitution C-SYNC-01).

Process:
1. Read each node's `external_refs` (e.g. `[jira:PROJ-123, ado:4567, pr:...]`).
2. **Export** graph → tools: for a `Requirement`/`Task` without an external ref,
   propose creating the matching Jira/ADO item and write the returned id back
   into `external_refs`.
3. **Import** tools → graph: for an external ticket with no node, create the
   `R-*`/`T-*` node so nothing lives only in the tracker.
4. Reconcile status: if the external item and the node disagree, flag it as
   drift (hand to `/skgdd.reconcile`); do not silently overwrite.
5. Rebuild and run `graph.py metrics` — check `audit_integration_nodes` rose.

Loop: `external update → sync → graph update → validation → notify`.

Note: actual API calls depend on your available integration tools/MCP servers;
if none are connected, produce the exact payloads and id mappings for the user.

Output: items exported/imported, ids written back, and any sync conflicts.
