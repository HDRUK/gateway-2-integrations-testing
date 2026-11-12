#!/usr/bin/env python3
"""Generate docs/schemas/gwdm-reference.md from the field inventory TSVs.

Reads fields-gwdm-{2.0,2.1,2.2-UNVERIFIED}.tsv (produced by field_inventory.py)
and emits one collapsible section per top-level GWDM block, inside a content tab
per version, with an "introduced in" column derived by diffing the versions.

Usage, from the repo root:

    python3 docs/examples/gwdm_reference.py

Writes docs/schemas/gwdm-reference.md and prints a summary. Re-run after
regenerating the TSVs with:

    python3 docs/examples/field_inventory.py ../schemata-2
"""
import csv
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "schemas" / "gwdm-reference.md"

VERSIONS = [
    ("2.0", "fields-gwdm-2.0.tsv", False),
    ("2.1", "fields-gwdm-2.1.tsv", False),
    ("2.2", None, True),
]

# GWDM 2.2 now HAS a schema (2026-09-21). This projection predates it and
# should be regenerated from schemata's GWDM/2.2/schema.json.
# Confirmed by Calum 2026-09-10: 2.2 EXTENDS 2.1 — so the projection is 2.1's
# fields plus the three paths HDRUK 4.1.0 introduced. Swap this for a real
# fields-gwdm-2.2.tsv the moment one exists (FACTS.md F28).
GWDM_22_BASE = "2.1"
GWDM_22_ADDS = [
    {
        "path": "accessibility.usage.duoCodes",
        "type": "CommaSeparatedValues|null",
        "required": "",
        "enum": "",
        "description": "Machine-readable codes from the GA4GH Data Use Ontology "
                       "describing the permitted or restricted uses of this dataset.",
    },
    {
        "path": "accessibility.usage.dataUsePermissions",
        "type": "DataUsePermissions|null",
        "required": "",
        "enum": "",
        "description": "Permissions relating to how people and materials within this "
                       "dataset may be used, beyond the general access conditions.",
    },
    {
        "path": "accessibility.usage.dataUsePermissions.patientRecontact",
        "type": "boolean|null",
        "required": "",
        "enum": "",
        "description": "Indicates whether the people from whom the dataset is "
                       "generated can be recontacted as part of a follow-up or new study.",
    },
]

BLOCK_ORDER = [
    "required", "summary", "coverage", "provenance", "accessibility", "linkage",
    "observations", "structuralMetadata", "tissuesSampleCollection",
    "demographicFrequency", "omics", "icons", "projectGrants", "datasetFilters",
    "erd",
]

BLOCK_BLURB = {
    "required": "Identity and versioning. **Written by the Gateway API — see the warning below.**",
    "summary": "Title, description, keywords, publisher, population size. The block search relies on most.",
    "coverage": "Geographic, temporal and demographic reach of the cohort.",
    "provenance": "Where the data came from and how often it is refreshed.",
    "accessibility": "Access rights, formats, standards and usage conditions. Required.",
    "linkage": "Relationships to other datasets, publications, tools and media.",
    "observations": "Structured population counts, one entry per observed measure.",
    "structuralMetadata": "Table and column level technical metadata.",
    "tissuesSampleCollection": "MIABIS-aligned biosample collection metadata.",
    "demographicFrequency": "Age, ethnicity and disease frequency bins.",
    "omics": "Assay and platform for omics datasets.",
    "icons": "Calculated categorisation icons, added on export. GWDM 2.1+.",
    "projectGrants": "Associated project grants. GWDM 2.1+, driven by CRUK.",
    "datasetFilters": "Categorisation tags for cancer type, data type and access. GWDM 2.1+.",
    "erd": "Entity-relationship diagram of the dataset's tables. GWDM 2.1+.",
}

DELIMITED = {
    "summary.keywords", "summary.datasetType", "summary.datasetSubType",
    "summary.funders", "coverage.spatial", "provenance.origin.purpose",
    "provenance.origin.source", "provenance.origin.collectionSituation",
    "accessibility.access.jurisdiction", "accessibility.access.accessRights",
    "accessibility.access.accessRequestCost",
    "accessibility.formatAndStandards.vocabularyEncodingSchemes",
    "accessibility.formatAndStandards.conformsTo",
    "accessibility.formatAndStandards.formats",
    "accessibility.formatAndStandards.languages",
    "accessibility.usage.dataUseLimitation",
    "accessibility.usage.dataUseRequirement",
    "accessibility.usage.duoCodes",
    "accessibility.usage.resourceCreator.name",
    "linkage.associatedMedia", "linkage.tools",
}

API_OWNED = {
    "required", "required.gatewayId", "required.gatewayPid", "required.issued",
    "required.modified", "required.revisions", "summary.publisher",
}


def load(name):
    rows = {}
    with open(HERE / name, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            rows[r["path"]] = r
    return rows


def block_of(path):
    return path.split(".")[0].split("[")[0]


def esc(text):
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def enum_cell(raw):
    if not raw:
        return ""
    vals = [v.strip() for v in raw.split("|") if v.strip()]
    if len(vals) > 6:
        shown = ", ".join(f"`{v}`" for v in vals[:6])
        return f"{shown} … ({len(vals)} values)"
    return ", ".join(f"`{v}`" for v in vals)


def main():
    data = {v: load(f) for v, f, _ in VERSIONS if f}
    projected = dict(data[GWDM_22_BASE])
    for row in GWDM_22_ADDS:
        projected[row["path"]] = row
    data["2.2"] = projected

    introduced = {}
    for path in data["2.0"]:
        introduced[path] = "2.0"
    for path in data["2.1"]:
        introduced.setdefault(path, "2.1")
    for path in data["2.2"]:
        introduced.setdefault(path, "2.2")

    lines = []
    w = lines.append

    w("---")
    w("title: GWDM field reference")
    w("description: Every field in the Gateway Working Data Model, by version and by block.")
    w("tags:")
    w("  - reference")
    w("  - schemas")
    w("  - gwdm")
    w("---")
    w("")
    w("<!-- GENERATED FILE — do not edit by hand.")
    w("     Regenerate with: python3 docs/examples/gwdm_reference.py")
    w("     Source: docs/examples/fields-gwdm-*.tsv -->")
    w("")
    w("# GWDM field reference")
    w("")
    w("**Applies to:** GWDM 2.0 · 2.1 · 2.2")
    w("")
    w("Every field in the Gateway Working Data Model, grouped by top-level block.")
    w("This page is **generated** from the schemas themselves, so it does not drift")
    w("from the model the way a hand-written list would.")
    w("")
    w("!!! info \"Where the full field descriptions live\"")
    w("    This page gives you the shape: path, type, whether it is required, the")
    w("    permitted values, and which GWDM version introduced it. For the complete")
    w("    prose description of each field, see the generated schema documentation at")
    w("    [hdruk.github.io/schemata](https://hdruk.github.io/schemata/), which is")
    w("    built from the Pydantic models directly.")
    w("")
    w("    Descriptions below are truncated to one line. Where they disagree with")
    w("    `schemata`, `schemata` is right and this page is stale — please")
    w("    [raise an issue](https://github.com/HDRUK/gateway-2-integrations-testing/issues).")
    w("")
    w("## Before you read the tables")
    w("")
    w("Three conventions decide whether your metadata survives the round trip. They")
    w("are explained in full on [The GWDM explained](gwdm.md); in brief:")
    w("")
    w("- **Fields marked 🔒 are written by the Gateway API** and overwrite whatever")
    w("  you send. Do not compute them.")
    w("- **Fields marked ⁂ are delimited strings**, not arrays — a list is joined")
    w("  with `;,;` into a single string.")
    w("- **`-1` means \"unknown\"** in numeric fields, not zero.")
    w("")

    counts = {}
    for version, _, unverified in VERSIONS:
        rows = data[version]
        counts[version] = len(rows)

    w("## Field counts")
    w("")
    w("| Version | Fields | Blocks | Source |")
    w("|---|---|---|---|")
    for version, fname, unverified in VERSIONS:
        blocks = len({block_of(p) for p in data[version]})
        src = (f"**projected: GWDM {GWDM_22_BASE} + {len(GWDM_22_ADDS)} DUO paths**"
               if unverified else f"`GWDM/{version}/schema.json`")
        w(f"| GWDM {version} | {counts[version]} | {blocks} | {src} |")
    w("")

    for version, fname, unverified in VERSIONS:
        rows = data[version]
        w(f'=== "GWDM {version}"')
        w("")
        if unverified:
            w("    No GWDM 2.2 schema exists yet, so the rows below are **projected**:")
            w(f"    GWDM {GWDM_22_BASE}'s fields plus the {len(GWDM_22_ADDS)} paths HDRUK 4.1.0")
            w("    introduced. **GWDM 2.2 extends 2.1**, so it is a superset of everything in")
            w("    the 2.1 tab — including `projectGrants`, `datasetFilters`, `erd`, `icons`")
            w("    and `summary.funders`.")
            w("")
            w("    Treat the three DUO rows as indicative on **shape** — whether `duoCodes`")
            w("    lands as a delimited string or a real array, and whether")
            w("    `patientRecontact` stays nested, is not settled until the model is")
            w("    written. See [The GWDM explained](gwdm.md#how-22-relates-to-21).")
            w("")
            w("    !!! note \"The current translation map lags this\"")
            w("        `maps/GWDM/2.2/HDRUK/4.1.0/translation.jsonata` is scaffolding copied")
            w("        from the 2.0-targeted map, so it emits only 2.0's fields plus the DUO")
            w("        paths — not the 2.1 sections. That is an **unfinished map**, not the")
            w("        design. A field-by-field record of what it emits today is in")
            w("        [`fields-gwdm-2.2-UNVERIFIED.tsv`](../examples/fields-gwdm-2.2-UNVERIFIED.tsv).")
            w("")

        present = [b for b in BLOCK_ORDER if any(block_of(p) == b for p in rows)]
        extra = sorted({block_of(p) for p in rows} - set(BLOCK_ORDER))
        for block in present + extra:
            paths = sorted(p for p in rows if block_of(p) == block)
            blurb = BLOCK_BLURB.get(block, "")
            w(f'    ??? note "`{block}` — {len(paths)} field{"s" if len(paths) != 1 else ""}"')
            w("")
            if blurb:
                w(f"        {blurb}")
                w("")
            w("        | Field | Type | Req | Values | Introduced | Description |")
            w("        |---|---|---|---|---|---|")
            for p in paths:
                r = rows[p]
                flags = ""
                if p in API_OWNED:
                    flags += " 🔒"
                if p in DELIMITED:
                    flags += " ⁂"
                req = "✓" if (r.get("required") or "").strip() == "yes" else ""
                desc = esc(r.get("description"))
                if len(desc) > 110:
                    desc = desc[:107].rstrip() + "…"
                intro = introduced.get(p, version)
                w(f"        | `{p}`{flags} | {esc(r.get('type'))} | {req} | "
                  f"{enum_cell(r.get('enum'))} | {intro} | {desc} |")
            w("")

    w("## Regenerating this page")
    w("")
    w("```bash")
    w("# 1. refresh the field inventories from schemata")
    w("python3 docs/examples/field_inventory.py ../schemata-2")
    w("")
    w("# 2. rebuild this page from them")
    w("python3 docs/examples/gwdm_reference.py")
    w("```")
    w("")
    w("Both scripts are committed next to their output in `docs/examples/`. Step 1")
    w("needs a local checkout of [`HDRUK/schemata`](https://github.com/HDRUK/schemata);")
    w("step 2 needs nothing but the TSVs.")
    w("")
    w("Once GWDM 2.2 lands in `schemata`, set its `VERSIONS` row in")
    w("`gwdm_reference.py` to the real `fields-gwdm-2.2.tsv` and clear its")
    w("`unverified` flag. The projection and both admonitions then disappear on")
    w("their own — see `FACTS.md` F28 for the full fill-in list.")
    w("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    total = sum(counts.values())
    print(f"wrote {OUT.relative_to(HERE.parent.parent)}  "
          f"({len(lines)} lines, {total} field rows across {len(VERSIONS)} versions)")
    for v, _, _ in VERSIONS:
        print(f"  GWDM {v}: {counts[v]} fields")


if __name__ == "__main__":
    sys.exit(main())
