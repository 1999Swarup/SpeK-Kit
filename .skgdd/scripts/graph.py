#!/usr/bin/env python3
"""
SKGDD graph engine.

Builds a directed knowledge graph from a bundle of Markdown nodes (OKF-shaped
frontmatter), validates it against the SKGDD schema, and answers the questions a
flat spec cannot: traceability, impact of change, coverage gaps, and tool ranking.

No third-party dependencies required (falls back to a minimal frontmatter parser
if PyYAML is unavailable).

Usage:
    python graph.py build     [bundle_dir]   # parse -> graph.json + refreshed index.md
    python graph.py validate  [bundle_dir]   # schema + edge legality + drift checks
    python graph.py trace     [bundle_dir]   # requirement spine coverage report
    python graph.py impact ID [bundle_dir]   # what is affected if ID changes
    python graph.py tools     [bundle_dir]   # rank tools per capability
    python graph.py loop      [bundle_dir]   # open loops / stale nodes / next actions
    python graph.py lint      [bundle_dir]   # typed-link + lifecycle + cognitive-load checks
    python graph.py metrics   [bundle_dir]   # eval metrics (SKGDD vs spec-only) as JSON+table
"""
from __future__ import annotations
import json
import os
import re
import sys
from collections import defaultdict, deque

# ---------------------------------------------------------------------------
# Schema: legal node types and edge (from-type -> to-type) constraints + inverses
# ---------------------------------------------------------------------------
NODE_TYPES = {
    "Constitution", "Requirement", "UserStory", "Constraint", "Assumption",
    "Question", "Decision", "Capability", "Tool", "Component", "Task", "Test",
    "Risk", "Milestone", "Entity", "Loop", "Lesson", "Schema",
    # brownfield / current-state intelligence layer
    "CurrentState", "LegacyConstraint", "IntegrationPoint", "SystemMap",
    # completion & evolution layer
    "Review", "Amendment",
    # domain grounding
    "KnowledgePack", "Index",
}

# Lifecycle-oriented knowledge flow. A node may not advance a stage until the
# guardrail for that stage is satisfied (see cmd_lint lifecycle checks).
LIFECYCLE_STAGES = [
    "draft", "specified", "planned", "implemented", "validated", "learned",
]

# Cognitive-load control: max markdown H2 sections before a file must be split.
MAX_SECTIONS = 7

# edge_name -> inverse_name
INVERSE = {
    "refines": "refined_by", "depends_on": "required_by", "derived_from": "derives",
    "satisfies": "satisfied_by", "verifies": "verified_by", "implements": "realized_by",
    "uses_tool": "used_by", "provides": "provided_by", "needs_tool": "serves",
    "alternative_to": "alternative_to", "conflicts_with": "conflicts_with",
    "constrains": "constrained_by", "governs": "governed_by", "threatens": "at_risk",
    "mitigated_by": "mitigates", "blocks": "blocked_by", "answered_by": "answers",
    "supersedes": "superseded_by", "traces_to": "traced_from", "related_to": "related_to",
    "includes": "included_in", "resolves": "resolved_by", "affects": "affected_by",
    "chosen_by": "chose", "caused_by": "causes", "observed": "observed_by",
    "changed": "changed_by", "spawned": "spawned_by", "amends": "amended_by",
    "informs": "informed_by",
}
# forward edges declared in frontmatter (inverses are materialized, not declared)
EDGE_FIELDS = set(INVERSE.keys())

# fields that are NOT edges
SCALAR_FIELDS = {
    "id", "type", "title", "description", "status", "priority", "confidence",
    "owner", "tags", "created", "updated", "source", "category", "maturity",
    "cost", "license", "estimate", "severity", "likelihood", "level", "loop_kind",
    "version", "acceptance", "observe", "orient", "decide", "act", "reflect",
    # new: lifecycle stage, abstraction layer (L1/L2/L3), external system refs,
    # brownfield markers, and learning capture flags
    "lifecycle", "stage", "layer", "external_refs", "reviewed", "learning",
    "pack", "domain",
}

EDGE_RE = re.compile(r"^([A-Za-z0-9\-_.]+)(?:\s+@weight:([0-9.]+))?(?:\s+conf:(\w+))?$")
# Body wiki-links: [[R-0042]] or [[R-0042|label]]
WIKILINK_RE = re.compile(r"\[\[([A-Za-z0-9\-_.]+)(?:\|[^\]]+)?\]\]")
# Markdown H2 section headers
SECTION_RE = re.compile(r"^##\s+\S", re.MULTILINE)


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------
def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip("\n")
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(block) or {}
        return data if isinstance(data, dict) else {}
    except Exception:
        return _mini_yaml(block)


def _mini_yaml(block: str) -> dict:
    """Tiny YAML subset: scalars, inline [a, b], and dash lists."""
    out: dict = {}
    key = None
    for raw in block.splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.lstrip().startswith("- ") and key is not None:
            out.setdefault(key, [])
            if isinstance(out[key], list):
                out[key].append(line.lstrip()[2:].strip().strip("'\""))
            continue
        if ":" in line:
            k, _, v = line.partition(":")
            key = k.strip()
            v = v.strip()
            if v == "":
                out[key] = []  # assume list continues on following dash lines
            elif v.startswith("[") and v.endswith("]"):
                inner = v[1:-1].strip()
                out[key] = [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
            else:
                out[key] = v.strip("'\"")
    # collapse empty-list keys that got no items back to scalar-ish
    return out


# ---------------------------------------------------------------------------
# Graph model
# ---------------------------------------------------------------------------
class Graph:
    def __init__(self):
        self.nodes: dict[str, dict] = {}
        self.out: dict[str, list[tuple[str, str]]] = defaultdict(list)  # id -> [(edge, target)]
        self.inn: dict[str, list[tuple[str, str]]] = defaultdict(list)
        self.warnings: list[str] = []

    def add_edge(self, src, edge, dst):
        self.out[src].append((edge, dst))
        inv = INVERSE.get(edge, edge + "_of")
        self.inn[dst].append((inv, src))


def load(bundle_dir: str) -> Graph:
    g = Graph()
    for root, _dirs, files in os.walk(bundle_dir):
        if os.sep + ".git" in root:
            continue
        for fn in files:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            with open(path, "r", encoding="utf-8") as fh:
                text = fh.read()
            fm = parse_frontmatter(text)
            nid = fm.get("id")
            if not nid or not fm.get("type"):
                continue  # not a node (e.g. README)
            fm["_path"] = os.path.relpath(path, bundle_dir)
            # capture body for drift / cognitive-load analysis
            body = text[text.find("\n---", 3) + 4:] if text.startswith("---") else text
            fm["_body"] = body
            fm["_wikilinks"] = sorted(set(WIKILINK_RE.findall(body)))
            fm["_sections"] = len(SECTION_RE.findall(body))
            g.nodes[nid] = fm
    # second pass: edges
    for nid, fm in g.nodes.items():
        for field, val in fm.items():
            if field not in EDGE_FIELDS:
                continue
            for target in _as_list(val):
                tid = _edge_target(target)
                if tid:
                    g.add_edge(nid, field, tid)
    _validate_refs(g)
    return g


def _as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def _edge_target(raw: str) -> str | None:
    m = EDGE_RE.match(str(raw).strip())
    return m.group(1) if m else None


def _validate_refs(g: Graph):
    for src, edges in g.out.items():
        for edge, dst in edges:
            if dst not in g.nodes:
                g.warnings.append(f"[dangling] {src} --{edge}--> {dst} (target node missing)")


# ---------------------------------------------------------------------------
# Analyses
# ---------------------------------------------------------------------------
def cmd_build(g: Graph, bundle_dir: str):
    graph_json = {
        "nodes": [
            {"id": n, "type": d.get("type"), "title": d.get("title"),
             "status": d.get("status"), "confidence": d.get("confidence"),
             "path": d.get("_path")}
            for n, d in sorted(g.nodes.items())
        ],
        "edges": [
            {"from": s, "edge": e, "to": t}
            for s in sorted(g.out) for (e, t) in g.out[s]
        ],
        "stats": _stats(g),
    }
    out_path = os.path.join(bundle_dir, "graph.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(graph_json, fh, indent=2)
    _write_index(g, bundle_dir)
    print(f"Built graph: {len(g.nodes)} nodes, "
          f"{sum(len(v) for v in g.out.values())} edges -> {out_path}")
    _print_warnings(g)


def _stats(g: Graph):
    by_type = defaultdict(int)
    for d in g.nodes.values():
        by_type[d.get("type", "?")] += 1
    return {"total": len(g.nodes), "by_type": dict(sorted(by_type.items()))}


def _write_index(g: Graph, bundle_dir: str):
    lines = ["---", "type: Index", "title: Bundle Index",
             "description: Machine-readable manifest of every node in this SKGDD bundle.",
             "---", "", "# Bundle Index", "",
             "Auto-generated by `graph.py build`. Lists every node so an agent can",
             "survey the bundle before opening files (OKF convention).", ""]
    by_type = defaultdict(list)
    for nid, d in g.nodes.items():
        by_type[d.get("type", "?")].append((nid, d))
    for t in sorted(by_type):
        lines.append(f"## {t}")
        for nid, d in sorted(by_type[t]):
            title = d.get("title", "")
            status = d.get("status", "")
            lines.append(f"- `{nid}` — [{title}]({d.get('_path')}) _({status})_")
        lines.append("")
    with open(os.path.join(bundle_dir, "index.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    _write_folder_indexes(g, bundle_dir)


def _write_folder_indexes(g: Graph, bundle_dir: str):
    """L1 summary per folder (Cognitive Load Reduction: every folder has index.md)."""
    by_folder = defaultdict(list)
    for nid, d in g.nodes.items():
        folder = os.path.dirname(d.get("_path", ""))
        if folder:
            by_folder[folder].append((nid, d))
    for folder, items in by_folder.items():
        rel = folder.replace("\\", "/")
        lines = ["---", "type: Index", f"title: {rel} index",
                 f"description: L1 summary of the {len(items)} nodes in {rel}/.",
                 "layer: L1", "---", "", f"# {rel}", ""]
        for nid, d in sorted(items):
            base = os.path.basename(d.get("_path", ""))
            lines.append(f"- `{nid}` [{d.get('type','?')}/{d.get('status','')}] "
                         f"[{d.get('title','')}]({base})")
        with open(os.path.join(bundle_dir, folder, "index.md"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")


def cmd_validate(g: Graph, bundle_dir: str):
    problems = list(g.warnings)
    # required fields per type
    for nid, d in g.nodes.items():
        t = d.get("type")
        if t == "Requirement":
            if not d.get("priority"):
                problems.append(f"[missing] {nid} Requirement has no priority")
            if not _has(d, "satisfied_by") and d.get("status") in ("done", "verified"):
                problems.append(f"[spine] {nid} marked {d.get('status')} but nothing satisfies it")
        if t == "Task" and not _has(d, "satisfies"):
            problems.append(f"[trace] {nid} Task satisfies no requirement (orphan work)")
        if t == "Tool" and not _has(d, "provides"):
            problems.append(f"[tool] {nid} Tool provides no capability")
    # blocked-by-open-question on must requirements
    for nid, d in g.nodes.items():
        if d.get("type") == "Requirement" and d.get("priority") == "must":
            for edge, q in g.inn.get(nid, []) + g.out.get(nid, []):
                if edge == "blocked_by" or q.startswith("Q-"):
                    qd = g.nodes.get(q, {})
                    if qd.get("status") == "open":
                        problems.append(f"[blocked] must-requirement {nid} blocked by open {q}")
    _report(problems, "validation")


def _has(d, field):
    return bool(_as_list(d.get(field)))


def cmd_trace(g: Graph, bundle_dir: str):
    """Report which requirements close all three spines."""
    print("Requirement traceability (value / build / trust):\n")
    reqs = [n for n, d in g.nodes.items() if d.get("type") == "Requirement"]
    if not reqs:
        print("  (no requirements found)")
        return
    for nid in sorted(reqs):
        d = g.nodes[nid]
        value = _has(d, "derived_from") or _has(d, "refines")
        build = _has(d, "satisfied_by")
        trust = _has(d, "verified_by")
        flag = "OK " if (value and build and trust) else "GAP"
        print(f"  [{flag}] {nid} {d.get('title','')}")
        if not value:
            print("        - missing VALUE: no user story / parent requirement")
        if not build:
            print("        - missing BUILD: no task/component satisfies it")
        if not trust:
            print("        - missing TRUST: no test verifies it")


def cmd_impact(g: Graph, start: str, bundle_dir: str):
    """BFS over dependents/derivatives to show blast radius of a change."""
    if start not in g.nodes:
        print(f"Unknown node: {start}")
        return
    # follow reverse dependency edges: who relies on this node?
    follow = {"required_by", "satisfied_by", "verified_by", "refined_by",
              "derives", "realized_by", "used_by", "included_in", "at_risk",
              "answers", "affected_by", "blocked_by"}
    seen = {start}
    order = []
    q = deque([(start, 0)])
    while q:
        node, depth = q.popleft()
        for edge, nxt in g.inn.get(node, []) + g.out.get(node, []):
            if edge in follow and nxt not in seen:
                seen.add(nxt)
                order.append((nxt, depth + 1, edge, node))
                q.append((nxt, depth + 1))
    print(f"Impact of changing {start} ({g.nodes[start].get('title','')}):\n")
    if not order:
        print("  Nothing depends on this node — safe to change in isolation.")
    for nid, depth, edge, via in sorted(order, key=lambda x: x[1]):
        d = g.nodes.get(nid, {})
        print(f"  {'  '*depth}- {nid} [{d.get('type','?')}] "
              f"{d.get('title','')}  (via {edge} of {via})")


def cmd_tools(g: Graph, bundle_dir: str):
    """Rank candidate tools per capability using edges + fit heuristics."""
    caps = [n for n, d in g.nodes.items() if d.get("type") == "Capability"]
    print("Tool selection map (capability -> ranked tools):\n")
    if not caps:
        print("  (no capability nodes yet — run /skgdd.plan to derive them)")
    for cap in sorted(caps):
        providers = [t for (e, t) in g.inn.get(cap, []) if e in ("provided_by", "serves")]
        providers += [t for (e, t) in g.out.get(cap, []) if e == "needs_tool"]
        providers = sorted(set(providers))
        print(f"  {cap} — {g.nodes[cap].get('title','')}")
        if not providers:
            print("      (no tool provides this capability — GAP)")
        ranked = sorted(providers, key=lambda t: _tool_score(g.nodes.get(t, {})), reverse=True)
        for t in ranked:
            td = g.nodes.get(t, {})
            print(f"      {_tool_score(td):+d}  {t}  "
                  f"[{td.get('maturity','?')}/{td.get('cost','?')}/{td.get('status','?')}]")


_MATURITY = {"stable": 2, "beta": 0, "experimental": -1, "legacy": -2}
_COST = {"free": 1, "freemium": 0, "usage-based": -1, "paid": -1}
_STATUS = {"accepted": 2, "proposed": 0, "rejected": -5, "superseded": -3}


def _tool_score(d: dict) -> int:
    return (_MATURITY.get(d.get("maturity"), 0)
            + _COST.get(d.get("cost"), 0)
            + _STATUS.get(d.get("status"), 0))


def cmd_loop(g: Graph, bundle_dir: str):
    """Surface what the next feedback loop should look at."""
    print("Loop radar — where attention is needed:\n")
    open_q = [n for n, d in g.nodes.items()
              if d.get("type") == "Question" and d.get("status") == "open"]
    failing = [n for n, d in g.nodes.items()
               if d.get("type") == "Test" and d.get("status") == "failing"]
    low_conf = [n for n, d in g.nodes.items()
                if d.get("confidence") == "low"]
    open_risk = [n for n, d in g.nodes.items()
                 if d.get("type") == "Risk" and d.get("status") in ("open", "mitigating")]
    for label, items in [("Open questions (block clarity)", open_q),
                         ("Failing tests (break trust spine)", failing),
                         ("Low-confidence nodes (need evidence)", low_conf),
                         ("Live risks", open_risk)]:
        print(f"  {label}: {len(items)}")
        for n in sorted(items):
            print(f"      - {n} {g.nodes[n].get('title','')}")
    print("\nNext loop suggestion: resolve open questions, then re-run "
          "`graph.py trace` to confirm spines closed.")


# ---------------------------------------------------------------------------
# Typed Knowledge Enforcement + Lifecycle + Cognitive-Load lint
# ---------------------------------------------------------------------------
# Heuristic: infer the edge a body wiki-link probably means, by target type.
_EDGE_SUGGEST = {
    ("Task", "Requirement"): "satisfies",
    ("Test", "Requirement"): "verifies",
    ("Test", "Task"): "verifies",
    ("Requirement", "UserStory"): "derived_from",
    ("Requirement", "Requirement"): "refines",
    ("Task", "Tool"): "uses_tool",
    ("Task", "Task"): "depends_on",
    ("Tool", "Capability"): "provides",
    ("Decision", "Tool"): "uses_tool",
    ("Risk", "Requirement"): "threatens",
    ("Question", "Requirement"): "blocks",
    ("Component", "Capability"): "implements",
}

_STAGE_INDEX = {s: i for i, s in enumerate(LIFECYCLE_STAGES)}


def cmd_lint(g: Graph, bundle_dir: str):
    typed, lifecycle, cognitive = [], [], []

    # --- 1. Typed Knowledge Enforcement: body link must have a graph edge ---
    for nid, d in g.nodes.items():
        connected = {t for (_e, t) in g.out.get(nid, [])} | {
            s for (_e, s) in g.inn.get(nid, [])}
        for target in d.get("_wikilinks", []):
            if target == nid:
                continue
            if target not in connected:
                tt = g.nodes.get(target, {}).get("type", "?")
                st = d.get("type", "?")
                sugg = _EDGE_SUGGEST.get((st, tt), "related_to")
                typed.append(
                    f"[untyped-link] {nid} body links [[{target}]] with no graph "
                    f"edge — suggest `{sugg}: [{target}]`")
        # reverse: declared edge never referenced in prose (weaker signal)
        for _e, t in g.out.get(nid, []):
            if t in g.nodes and t not in d.get("_wikilinks", []) and _e not in (
                    "governed_by", "constrained_by", "related_to"):
                pass  # informational only; not emitted to keep noise down

    # --- 2. Lifecycle guardrails: cannot advance without prerequisites ---
    for nid, d in g.nodes.items():
        stage = d.get("stage") or d.get("lifecycle")
        if not stage or stage not in _STAGE_INDEX:
            if d.get("type") in ("Requirement", "Task"):
                lifecycle.append(f"[no-stage] {nid} has no lifecycle stage set")
            continue
        idx = _STAGE_INDEX[stage]
        has = lambda f: bool(_as_list(d.get(f)))
        if idx >= _STAGE_INDEX["planned"] and d.get("type") == "Requirement" and not has("satisfied_by"):
            lifecycle.append(f"[stage] {nid} at '{stage}' but nothing satisfies it (need tasks)")
        if idx >= _STAGE_INDEX["implemented"] and not has("verified_by") and d.get("type") in ("Requirement", "Task"):
            lifecycle.append(f"[stage] {nid} at '{stage}' but no test verifies it")
        if idx >= _STAGE_INDEX["validated"]:
            for _e, t in g.out.get(nid, []):
                if _e == "verified_by" and g.nodes.get(t, {}).get("status") == "failing":
                    lifecycle.append(f"[stage] {nid} at '{stage}' but its test {t} is failing")
        if idx >= _STAGE_INDEX["learned"] and not (has("informed_by") or has("changed_by")):
            lifecycle.append(f"[stage] {nid} at 'learned' but no Lesson/Loop informs it")

    # --- 3. Cognitive-load controls ---
    titles = defaultdict(list)
    for nid, d in g.nodes.items():
        if d.get("_sections", 0) > MAX_SECTIONS:
            cognitive.append(f"[oversized] {nid} has {d['_sections']} H2 sections "
                             f"(> {MAX_SECTIONS}) — split it")
        titles[(d.get("type"), (d.get("title") or "").strip().lower())].append(nid)
        edges_in = len(g.inn.get(nid, []))
        edges_out = len([e for e in g.out.get(nid, []) if e[1] in g.nodes])
        if edges_in == 0 and edges_out == 0 and d.get("type") not in (
                "Constitution", "Schema", "Index", "KnowledgePack", "SystemMap"):
            cognitive.append(f"[orphan] {nid} has no connections (unused or unlinked)")
    for (t, title), ids in titles.items():
        if title and len(ids) > 1:
            cognitive.append(f"[duplicate] {len(ids)} {t} nodes share title '{title}': {ids}")

    # folder-level index presence (soft)
    folders = defaultdict(int)
    for d in g.nodes.values():
        folders[os.path.dirname(d.get("_path", ""))] += 1
    for folder, count in folders.items():
        if folder and not os.path.exists(os.path.join(bundle_dir, folder, "index.md")):
            cognitive.append(f"[no-index] folder '{folder}/' has {count} nodes but no index.md")

    print("Typed Knowledge Enforcement:")
    _report(typed, "  typed-links")
    print("\nLifecycle guardrails:")
    _report(lifecycle, "  lifecycle")
    print("\nCognitive-load controls:")
    _report(cognitive, "  cognitive-load")
    total = len(typed) + len(lifecycle) + len(cognitive)
    print(f"\nLint total: {total} finding(s).")
    return total


# ---------------------------------------------------------------------------
# Evals & Metrics — objective SKGDD-vs-spec-only measurement
# ---------------------------------------------------------------------------
def cmd_metrics(g: Graph, bundle_dir: str):
    reqs = [d for d in g.nodes.values() if d.get("type") == "Requirement"]
    tasks = [d for d in g.nodes.values() if d.get("type") == "Task"]
    tests = [d for d in g.nodes.values() if d.get("type") == "Test"]
    lessons = [d for d in g.nodes.values() if d.get("type") == "Lesson"]
    loops = [d for d in g.nodes.values() if d.get("type") == "Loop"]
    amendments = [d for d in g.nodes.values() if d.get("type") == "Amendment"]
    total_nodes = len(g.nodes)
    total_edges = sum(len(v) for v in g.out.values())

    def pct(n, d):
        return round(100.0 * n / d, 1) if d else None

    def has(d, f):
        return bool(_as_list(d.get(f)))

    # A. Requirement understanding
    ambiguous = sum(1 for d in reqs
                    if d.get("confidence") == "low" or _blocked_by_open_q(g, d))
    drifted = sum(1 for d in reqs if has(d, "amended_by")) + len(amendments)

    # B. Traceability
    traced = sum(1 for d in reqs
                 if (has(d, "derived_from") or has(d, "refines"))
                 and has(d, "satisfied_by") and has(d, "verified_by"))
    orphans = sum(1 for nid, d in g.nodes.items()
                  if not g.inn.get(nid) and not [e for e in g.out.get(nid, []) if e[1] in g.nodes]
                  and d.get("type") not in ("Constitution", "Schema", "Index", "KnowledgePack"))
    broken = len(g.warnings)

    # C. Execution efficiency (static proxies)
    reworked = sum(1 for d in tasks if has(d, "amended_by")
                   or d.get("status") == "blocked")

    # D. Loop effectiveness
    done_tasks = [d for d in tasks if d.get("status") in ("done", "verified")]
    learned = sum(1 for d in done_tasks if has(d, "informed_by") or has(d, "changed_by"))
    loop_changes = sum(len(_as_list(d.get("changed"))) for d in loops)

    # E. Cognitive load
    avg_sections = round(sum(d.get("_sections", 0) for d in g.nodes.values())
                         / total_nodes, 1) if total_nodes else 0
    max_sections = max((d.get("_sections", 0) for d in g.nodes.values()), default=0)
    files_per_req = round(total_nodes / len(reqs), 1) if reqs else None

    # F. AI effectiveness (context completeness proxy)
    complete = sum(1 for d in g.nodes.values()
                   if d.get("description") and (g.out.get(d.get("id", "")) or []))
    context_completeness = pct(complete, total_nodes)

    # G. Enterprise readiness
    governed = sum(1 for d in reqs if has(d, "governed_by"))
    with_ext = sum(1 for d in g.nodes.values() if d.get("external_refs"))

    metrics = {
        "A_requirement_understanding": {
            "ambiguity_score_pct": pct(ambiguous, len(reqs)),
            "requirement_drift_count": drifted,
            "requirements": len(reqs),
        },
        "B_traceability": {
            "trace_coverage_pct": pct(traced, len(reqs)),
            "orphan_rate_pct": pct(orphans, total_nodes),
            "broken_link_count": broken,
        },
        "C_execution_efficiency": {
            "task_rework_rate_pct": pct(reworked, len(tasks)),
            "tasks": len(tasks),
        },
        "D_loop_effectiveness": {
            "learning_capture_rate_pct": pct(learned, len(done_tasks)),
            "loop_iterations": len(loops),
            "nodes_changed_by_loops": loop_changes,
            "lessons_recorded": len(lessons),
        },
        "E_cognitive_load": {
            "files_per_requirement": files_per_req,
            "avg_sections_per_file": avg_sections,
            "max_sections_in_a_file": max_sections,
        },
        "F_ai_effectiveness": {
            "context_completeness_pct": context_completeness,
        },
        "G_enterprise_readiness": {
            "compliance_coverage_pct": pct(governed, len(reqs)),
            "audit_integration_nodes": with_ext,
            "graph_edges": total_edges,
        },
    }
    out_path = os.path.join(bundle_dir, "metrics.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(metrics, fh, indent=2)

    print("SKGDD Eval Metrics\n" + "=" * 60)
    for group, vals in metrics.items():
        print(f"\n{group.replace('_', ' ').title()}")
        for k, v in vals.items():
            unit = "%" if k.endswith("_pct") else ""
            shown = "n/a" if v is None else f"{v}{unit}"
            print(f"  {k:<32} {shown}")
    print("\n" + "=" * 60)
    print("Spec-only baseline: trace_coverage, impact visibility, loop, and")
    print("compliance metrics are structurally 0/undefined (no graph to measure).")
    print(f"Written -> {out_path}")
    return metrics


def _blocked_by_open_q(g: Graph, d: dict) -> bool:
    nid = d.get("id")
    for e, t in g.inn.get(nid, []) + g.out.get(nid, []):
        if e == "blocked_by" or t.startswith("Q-"):
            if g.nodes.get(t, {}).get("status") == "open":
                return True
    return False


# ---------------------------------------------------------------------------
def _report(problems, label):
    if not problems:
        print(f"{label}: PASS — no issues found.")
        return
    print(f"{label}: {len(problems)} issue(s):")
    for p in problems:
        print(f"  {p}")


def _print_warnings(g: Graph):
    for w in g.warnings:
        print(f"  warning: {w}")


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    cmd = argv[0]
    if cmd == "impact":
        start = argv[1] if len(argv) > 1 else None
        bundle = argv[2] if len(argv) > 2 else "."
    else:
        start = None
        bundle = argv[1] if len(argv) > 1 else "."
    g = load(bundle)
    if cmd == "build":
        cmd_build(g, bundle)
    elif cmd == "validate":
        cmd_validate(g, bundle)
    elif cmd == "trace":
        cmd_trace(g, bundle)
    elif cmd == "impact":
        if not start:
            print("Usage: graph.py impact <NODE-ID> [bundle_dir]")
            return 1
        cmd_impact(g, start, bundle)
    elif cmd == "tools":
        cmd_tools(g, bundle)
    elif cmd == "loop":
        cmd_loop(g, bundle)
    elif cmd == "lint":
        cmd_lint(g, bundle)
    elif cmd == "metrics":
        cmd_metrics(g, bundle)
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
