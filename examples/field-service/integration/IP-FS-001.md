---
id: IP-FS-001
type: IntegrationPoint
title: Azure IoT Hub → Dataverse (Connected Field Service)
description: Boundary where telemetry-driven events create CRM work orders.
status: planned
layer: L2
confidence: med
owner: "@platform"
tags: [integration, azure, iot]
external_refs: [doc:confluence/fs/cfs-integration]
created: 2026-07-07
updated: 2026-07-07
depends_on: [TL-azure-iot-hub, TL-azure-functions]
constrained_by: []
related_to: [R-FS-003]
---

# Azure IoT Hub → Dataverse (Connected Field Service)

## Boundary
Cloud-to-CRM: Azure Function (triggered from IoT Hub) calls the Dataverse Web API
to create/update work orders using a service principal.

## Contract
Auth via Entra ID app registration (least privilege); idempotency key per asset to
avoid duplicate work orders; ret/backoff on 429/5xx.

## Risk / fragility
Dataverse API throttling under telemetry bursts — see RK-FS-002 mitigation.
