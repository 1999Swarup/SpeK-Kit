---
id: TL-dataverse
type: Tool
title: Microsoft Dataverse
description: Power Platform data platform underpinning Dynamics 365 CRM.
status: accepted
category: data
maturity: stable
cost: paid
license: proprietary
confidence: high
tags: [dynamics365, dataverse]
created: 2026-07-08
updated: 2026-07-08
provides: [CAP-crm-data]
---

# Microsoft Dataverse
System of record for CRM tables, columns, relationships, and records.
Backed here by the `dv-metadata`, `dv-data`, and `dv-query` skills.

## Known pitfalls
API throttling under burst writes; use batching and backoff.
