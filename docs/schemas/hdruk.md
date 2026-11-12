---
title: HDRUK schema
description: The HDRUK metadata schema — the recommended input schema for most partners.
tags:
  - schemas
  - hdruk-schema
---

# HDRUK schema

**Applies to:** HDRUK 2.0.2 – 4.1.0

The HDRUK schema is the public-facing HDR UK health data metadata schema. If you
are a UK health data custodian onboarding a dataset and you have a free choice,
**this is the schema to author in, at version 4.1.0.**

## Where the definition lives

The schema is defined as Pydantic v2 models in
[**`HDRUK/schemata`**](https://github.com/HDRUK/schemata), which generates the
JSON Schema, the registry of available versions, and the field documentation from
those models.

!!! note "The repository was renamed"
    It used to be `HDRUK/schemata-2`. Links to `github.com/HDRUK/schemata-2` and
    `raw.githubusercontent.com/.../schemata-2/...` still work by GitHub's rename
    redirect, but **`hdruk.github.io/schemata-2/` does not** — GitHub Pages does
    not redirect on rename. The published documentation is at
    [hdruk.github.io/schemata](https://hdruk.github.io/schemata/).

    The default branch is `dev`, and what was `master` is now `main`.

| What you want | Where |
|---|---|
| Field-by-field documentation | [hdruk.github.io/schemata](https://hdruk.github.io/schemata/) |
| The Pydantic source | [`hdr_schemata/models/HDRUK/`](https://github.com/HDRUK/schemata/tree/dev/hdr_schemata/models/HDRUK) |
| Enum definitions | [`hdr_schemata/definitions/`](https://github.com/HDRUK/schemata/tree/dev/hdr_schemata/definitions) |
| A machine-readable field inventory | [`fields-hdruk-4.1.0.tsv`](../examples/fields-hdruk-4.1.0.tsv) in this repo |

## How it differs from the GWDM

The HDRUK schema is what you write; the [GWDM](gwdm.md) is what the Gateway
stores. They are not the same model and the differences are not cosmetic — the
block names diverge, and so do the field types.

| | HDRUK schema | GWDM |
|---|---|---|
| Top-level blocks | `summary`, `documentation`, `coverage`, `provenance`, `accessibility`, `enrichmentAndLinkage`, `observations`, `structuralMetadata`, `demographicFrequency`, `omics`, `revisions` — plus the scalars `identifier`, `version`, `issued`, `modified` | `required`, `summary`, `coverage`, `provenance`, `accessibility`, `linkage`, `observations`, `structuralMetadata`, `tissuesSampleCollection`, `demographicFrequency`, `omics` |
| Linkage lives in | `enrichmentAndLinkage` | `linkage` |
| Identity lives in | `revisions` and top-level fields | `required` |
| `summary.keywords` | array of strings | `;,;`-delimited string |
| Lists generally | real JSON arrays | often delimited strings |

The translation between the two is a JSONata map, and going from HDRUK 4.1.0 to
GWDM 2.2 is 243 lines of it. You do not need to read that map to use the
Gateway — but if a field is not coming through, the map is where the answer is.

## Version history

Nine versions are reachable. **4.1.0 is current**; `4.0.0` is what the deployed
dev service serves today.

| Version | Status | Input | Output | What it is |
|---|---|---|---|---|
| **4.1.0** | **current** | ✓ | ✓ | Adds GA4GH DUO codes and patient recontact |
| `4.0.0` | supported | ✓ | ✓ | Adds `summary.datasetAliases` |
| `3.0.0` | supported | ✓ | ✓ | Large release — demographics, age ranges, linkage descriptors |
| `2.2.1` | supported | ✓ | ✓ | |
| `2.2.0` | supported | ✓ | ✓ | |
| `2.1.3` | supported | ✓ | ✓ | |
| `2.1.2` | supported | ✓ | ✓ | The root base class all later versions inherit from |
| `2.1.0` | legacy | ✓ | ✗ | Input only — no map produces it |
| `2.0.2` | legacy | ✓ | ✗ | Input only — no map produces it |
| `datasetv2` | legacy | ✓ | ✗ | Pre-2.0 format. Translates into `2.1.2` and `3.0.0` only |

"Supported" means a map exists and the version is in the registry. Nothing is
being switched off — but the further back you go, the more the newer fields
simply have nowhere to sit.

!!! tip "What \"supported\" does not mean"
    `2.0.2` and `2.1.0` are served by TRASER but are **not** in `schemata`'s own
    registry of available versions. They exist as translation-graph nodes rather
    than as published schemas. Do not author new metadata in them.

### What 4.1.0 adds over 4.0.0

Exactly three field paths, all under `accessibility.usage`, and nothing is
removed:

| Field | Purpose |
|---|---|
| `accessibility.usage.duoCodes` | Machine-readable [GA4GH Data Use Ontology](https://github.com/EBISPOT/DUO) codes describing permitted and restricted uses, for interoperability with other GA4GH-compliant systems |
| `accessibility.usage.dataUsePermissions` | Container for permissions beyond the general access conditions |
| `accessibility.usage.dataUsePermissions.patientRecontact` | Whether the people the dataset describes can be recontacted for follow-up or a new study |

One field also gained values rather than changing shape:
`accessibility.formatAndStandards.conformsTo` accepts three new standardised data
models — **`BNF`**, **`DDI`** and **`DCAT`** — alongside the existing HL7 FHIR,
OMOP, DICOM, CDISC and the rest.

That last change needs no mapping work in either direction: `conformsTo` passes
through the `$to_str` helper, so new values survive without an allow-list.

!!! success "4.1.0 is complete and deployed"
    Re-verified 2026-09-21. HDRUK 4.1.0 is in `schemata`, has maps in
    `traser-mapping-files`, is served by the deployed dev TRASER, and returns a
    translated payload from **production**. The two fields it adds are stored
    in [GWDM 2.2](gwdm.md), which is also complete and deployed.

### What 3.0.0 added

The largest release in the schema's history, and the reason most partners moved.
Highlights rather than the full list:

- `demographicFrequency` — age, ethnicity and disease frequency bins, aligned to
  ONS groupings and to ICD-10 / SNOMED CT / MeSH vocabularies
- `coverage.typicalAgeRangeMin` and `coverage.typicalAgeRangeMax` as integers,
  replacing the free-text range
- `coverage.materialType`, `coverage.followUp`, `coverage.datasetCompleteness`
- `enrichmentAndLinkage.derivedFrom` and `.isPartOf` as structured dataset
  descriptors with `pid` / `title` / `url`, rather than comma-separated strings
- `documentation.inPipeline`

The full generated changelog for every version is in
[`docs/HDRUK/`](https://github.com/HDRUK/schemata/tree/dev/docs/HDRUK) in the
`schemata` repository, one `X.Y.Z.change.md` per release.

## Using it

To submit metadata in HDRUK 4.1.0, see [creating metadata](creating-metadata.md)
and then [create a dataset](../api/datasets/create.md).

To read metadata back in an HDRUK version, name it on the request:

```bash
curl -s "https://api.healthdatagateway.org/api/v1/datasets/868" \
  -H "x-schema-model: HDRUK" \
  -H "x-schema-version: 4.0.0"
```

The same dataset, translated into HDRUK 4.0.0, is frozen as
[`hdruk-4.0.0-rich.json`](../examples/hdruk-4.0.0-rich.json) if you would rather
read it than run it.

## Where next

- [Creating metadata](creating-metadata.md) — authoring a record
- [Metadata validation](validation.md) — checking it before you send it
- [The GWDM explained](gwdm.md) — what happens to it after you send it
- [Example payloads](examples.md) — the same dataset in four schemas
