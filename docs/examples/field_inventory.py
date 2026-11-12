#!/usr/bin/env python3
"""Generate a flat field inventory for each in-scope schema.

Usage:  python3 docs/examples/field_inventory.py [path-to-schemata-2]

Reads the generated schema.json for each schema below and writes one TSV per
schema: path, type, required, enum values, description. Hand-transcribed field
lists rot; these are regenerated from the source of truth.

HDRUK 5.0.0 and GWDM 3.0 are deliberately excluded from TARGETS.

GWDM 2.2 NOW HAS a schema.json (verified 2026-09-21); this projection predates
it and should be regenerated. Historically it could not be inventoried from a published
schema. Its inventory is derived from
traser-mapping-files/maps/GWDM/2.2/HDRUK/4.1.0/translation.jsonata, whose own
header states it is a verbatim copy of the GWDM 2.0-targeted map plus the
additions listed in DERIVED_ADDITIONS. Every row of it is UNVERIFIED.
"""

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
REPO = Path(sys.argv[1] if len(sys.argv) > 1 else "../schemata-2").expanduser()

TARGETS = [
    ("GWDM", "2.0"),
    ("GWDM", "2.1"),
    ("HDRUK", "4.0.0"),
    ("HDRUK", "4.1.0"),
]

MAX_DEPTH = 12


def resolve(node, defs, seen):
    while isinstance(node, dict) and "$ref" in node:
        name = node["$ref"].rsplit("/", 1)[-1]
        if name in seen:
            return {"type": f"<recursive {name}>"}
        seen = seen | {name}
        node = defs.get(name, {})
    return node


def describe(node):
    if not isinstance(node, dict):
        return ""
    if "type" in node:
        return node["type"] if isinstance(node["type"], str) else "|".join(node["type"])
    for key in ("anyOf", "oneOf", "allOf"):
        if key in node:
            parts = []
            for option in node[key]:
                parts.append(option.get("type") or option.get("$ref", "").rsplit("/", 1)[-1] or "?")
            return "|".join(str(p) for p in parts)
    if "enum" in node:
        return "enum"
    return ""


def enums(node, defs, seen):
    if not isinstance(node, dict):
        return ""
    if "enum" in node:
        return ", ".join("null" if v is None else str(v) for v in node["enum"])
    for key in ("anyOf", "oneOf"):
        for option in node.get(key, []) or []:
            got = enums(resolve(option, defs, seen), defs, seen)
            if got:
                return got
    return ""


def walk(node, defs, prefix, required, rows, depth, seen):
    if depth > MAX_DEPTH:
        return
    node = resolve(node, defs, seen)
    if not isinstance(node, dict):
        return

    props = node.get("properties")
    if not props:
        for key in ("anyOf", "oneOf", "allOf"):
            for option in node.get(key, []) or []:
                option = resolve(option, defs, seen)
                if isinstance(option, dict) and option.get("properties"):
                    props = option["properties"]
                    required = option.get("required", required)
                    break
            if props:
                break

    if props:
        node_required = set(node.get("required", []) or required or [])
        for name, child in props.items():
            path = f"{prefix}.{name}" if prefix else name
            target = resolve(child, defs, seen)
            rows.append(
                {
                    "path": path,
                    "type": describe(target) or describe(child),
                    "required": "yes" if name in node_required else "",
                    "enum": enums(child, defs, seen),
                    "description": (target.get("description") or child.get("description") or "")
                    .replace("\n", " ")
                    .strip(),
                }
            )
            walk(child, defs, path, [], rows, depth + 1, seen)
        return

    items = node.get("items") if node.get("type") == "array" else None
    if items is None:
        for key in ("anyOf", "oneOf"):
            for option in node.get(key, []) or []:
                option = resolve(option, defs, seen)
                if isinstance(option, dict) and option.get("type") == "array" and "items" in option:
                    items = option["items"]
                    break
            if items is not None:
                break
    if items is not None:
        walk(items, defs, f"{prefix}[]", [], rows, depth + 1, seen)


for model, version in TARGETS:
    source = REPO / "hdr_schemata" / "models" / model / version / "schema.json"
    if not source.exists():
        print(f"SKIP {model} {version} — no schema.json at {source}")
        continue
    schema = json.loads(source.read_text())
    rows = []
    walk(schema, schema.get("$defs", {}), "", schema.get("required", []), rows, 0, frozenset())

    out = HERE / f"fields-{model.lower()}-{version}.tsv"
    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["path", "type", "required", "enum", "description"], delimiter="\t"
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"{model} {version}: {len(rows)} fields -> {out.name}")

DERIVED_ADDITIONS = [
    {
        "path": "accessibility.usage.duoCodes",
        "type": "string|null",
        "required": "",
        "enum": "",
        "description": "UNVERIFIED - map emits a ';,;'-joined string; the 2.2 schema may model it as a list",
    },
    {
        "path": "accessibility.usage.dataUsePermissions",
        "type": "object|null",
        "required": "",
        "enum": "",
        "description": "UNVERIFIED - map emits a nested object carrying patientRecontact only",
    },
    {
        "path": "accessibility.usage.dataUsePermissions.patientRecontact",
        "type": "unknown",
        "required": "",
        "enum": "",
        "description": "UNVERIFIED - passed through unchanged from HDRUK 4.1.0",
    },
]

base = HERE / "fields-gwdm-2.0.tsv"
if base.exists():
    with base.open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        row["description"] = f"UNVERIFIED (inherited from GWDM 2.0) {row['description']}".strip()
    rows.extend(DERIVED_ADDITIONS)
    rows.sort(key=lambda r: r["path"])
    out = HERE / "fields-gwdm-2.2-UNVERIFIED.tsv"
    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["path", "type", "required", "enum", "description"], delimiter="\t"
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"GWDM 2.2 (derived, unverified): {len(rows)} fields -> {out.name}")
