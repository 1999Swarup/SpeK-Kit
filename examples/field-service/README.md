# Example: Dynamics 365 Field Service on Power Platform + Azure

A worked SpeK-Kit bundle applying the kit to **3 mock requirements** spanning
Microsoft CRM (Dynamics 365), Field Service, Power Platform, and Azure.

## The three requirements

| ID | Requirement | Stack |
|----|-------------|-------|
| `R-FS-001` | Auto-schedule work orders to the best-fit technician via **Resource Scheduling Optimization** | Dynamics 365 Field Service, RSO, Power Automate, Dataverse |
| `R-FS-002` | Field technicians **view/update work orders offline**, syncing on reconnect | Field Service Mobile (Power Apps), Dataverse |
| `R-FS-003` | Equipment **telemetry auto-creates predictive maintenance work orders** | Azure IoT Hub, Azure Functions → Dataverse (Connected Field Service) |

## What the graph demonstrates

Run any of these from the repo root:

```powershell
$b = "examples/field-service"
python .skgdd/scripts/graph.py build   $b   # 32 nodes, 65 edges
python .skgdd/scripts/graph.py trace   $b   # R-FS-001/002 OK; R-FS-003 GAP (no test yet)
python .skgdd/scripts/graph.py tools   $b   # ranks RSO/Azure tools; rejected custom scheduler scores -7
python .skgdd/scripts/graph.py impact R-FS-002 $b   # blast radius: tasks, test, risk
python .skgdd/scripts/graph.py loop    $b   # surfaces open question + live risks
python .skgdd/scripts/graph.py metrics $b   # eval metrics -> metrics.json
```

### Highlights

- **Traceability:** R-FS-001 and R-FS-002 close all three spines (value/build/trust).
  R-FS-003 is honestly a **GAP** — it is `should`-priority, blocked by an open
  question (`Q-FS-301`, the telemetry threshold), so it has no test yet. The kit
  shows this instead of pretending it's done.
- **Tool selection:** the graph ranks the first-party tools (RSO, Field Service
  Mobile, IoT Hub, Functions) and pushes the rejected `TL-custom-scheduler` to the
  bottom (`-7`), with the rationale recorded in `D-FS-001`.
- **Brownfield:** `CS-FS-001` captures that scheduling is manual today and
  constrains R-FS-001 to keep a manual-override path.
- **Enterprise sync:** several nodes carry `external_refs` (Azure DevOps IDs,
  Confluence docs) — `audit_integration_nodes = 4`.
- **Loop radar:** flags the open `Q-FS-301` and the two live IoT/offline risks as
  the next things to resolve.

### Sample metrics (this bundle)

| Group | Metric | Value |
|-------|--------|-------|
| A | Ambiguity score | 33.3% (1 of 3 blocked/low-confidence) |
| B | Trace coverage | 66.7% (2 of 3 fully traced) |
| B | Orphan / broken links | 0% / 0 |
| F | Context completeness | 90.6% |
| G | Compliance coverage | 100% (all requirements `governed_by` an article) |
| G | Audit-integrated nodes | 4 |

The two weakest metrics (ambiguity, trace coverage) point straight at the next
move: resolve `Q-FS-301` via `/skgdd.clarify`, then add the test for R-FS-003.
