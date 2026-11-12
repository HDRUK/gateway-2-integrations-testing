#!/usr/bin/env python3
"""Snapshot the deployed translation graph and the routes it implies.

Usage:  python3 docs/examples/translation_graph.py

Writes:
  translation-templates.json  raw /list/templates response
  translation-edges.tsv       one row per directed edge, input -> output
  translation-routes.tsv      shortest path for the routes the docs rely on

Every edge has weight 1, so the shortest path is the fewest hops regardless of
how much metadata each hop loses. The routes file makes that visible.
"""

import json
import urllib.request
from collections import deque
from pathlib import Path

TRASER = "https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app"
HERE = Path(__file__).parent

with urllib.request.urlopen(f"{TRASER}/list/templates", timeout=120) as response:
    templates = json.load(response)

(HERE / "translation-templates.json").write_text(json.dumps(templates, indent=2) + "\n")

edges = []
graph = {}
for t in templates:
    source = f"{t['input_model']}:{t['input_version']}"
    target = f"{t['output_model']}:{t['output_version']}"
    edges.append((source, target))
    graph.setdefault(source, []).append(target)

edges.sort()
with (HERE / "translation-edges.tsv").open("w") as handle:
    handle.write("input\toutput\n")
    for source, target in edges:
        handle.write(f"{source}\t{target}\n")


def path(start, end):
    if start == end:
        return [start]
    queue = deque([[start]])
    seen = {start}
    while queue:
        route = queue.popleft()
        for nxt in sorted(graph.get(route[-1], [])):
            if nxt == end:
                return route + [nxt]
            if nxt not in seen:
                seen.add(nxt)
                queue.append(route + [nxt])
    return None


ROUTES = [
    ("GWDM:2.0", "SchemaOrg:GoogleRecommended"),
    ("GWDM:2.0", "SchemaOrg:default"),
    ("GWDM:2.0", "SchemaOrg:BioSchema"),
    ("GWDM:2.1", "SchemaOrg:GoogleRecommended"),
    ("GWDM:2.1", "SchemaOrg:default"),
    ("GWDM:2.1", "SchemaOrg:BioSchema"),
    ("GWDM:2.0", "HDRUK:4.0.0"),
    ("GWDM:2.1", "HDRUK:4.0.0"),
    ("HDRUK:4.0.0", "GWDM:2.0"),
    ("HDRUK:4.0.0", "GWDM:2.1"),
    ("HDRUK:2.1.2", "GWDM:2.0"),
    ("SchemaOrg:default", "GWDM:2.0"),
]

with (HERE / "translation-routes.tsv").open("w") as handle:
    handle.write("from\tto\thops\troute\n")
    for start, end in ROUTES:
        route = path(start, end)
        hops = str(len(route) - 1) if route else "unreachable"
        handle.write(f"{start}\t{end}\t{hops}\t{' -> '.join(route) if route else '-'}\n")

nodes = sorted(set(graph) | {t for _, t in edges})
print(f"{len(templates)} templates, {len(nodes)} nodes")
inbound = {}
for source, target in edges:
    inbound.setdefault(target, []).append(source)
for node in nodes:
    if node.startswith("SchemaOrg"):
        print(f"  inbound to {node}: {sorted(inbound.get(node, [])) or 'NONE'}")
