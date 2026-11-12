---
title: The GWDM — what we store
description: The Gateway Working Data Model: the single shape every dataset is stored in.
tags:
  - schemas
  - gwdm
---

# The GWDM — what we store

**Applies to:** GWDM 2.0 – 2.2

Every dataset on the HDR UK Gateway is stored in one shape, whatever shape it
arrived in. That shape is the **Gateway Working Data Model** — the GWDM.

This page explains what it is, how it is put together, and the four conventions
that decide whether your metadata survives contact with it. For the field-by-field
tables, see [the GWDM field reference](gwdm-reference.md).

## Why there is a storage model at all

The Gateway ingests metadata from many sources in many shapes, and has to do
three things with all of them at once: search across them uniformly, display them
in one UI, and serve them back out in whatever shape the reader asks for. Doing
that against a dozen input schemas directly would mean a dozen search indexes and
a dozen display paths.

So there is one internal model. Everything is translated into it on the way in
and out of it on the way out, and every part of the Gateway that is not TRASER
only ever sees the GWDM.

For you as a data partner this is mostly good news — you author in the schema you
already have, and the Gateway absorbs the difference. It has exactly one sharp
edge, and it is worth stating twice:

!!! important "The GWDM is the bottleneck"
    If a field has nowhere to live in the GWDM, it cannot survive the round trip,
    no matter how good your map is. Adding a field to a public-facing schema
    usually means adding it to the GWDM too.

### The GWDM is not the HDRUK schema

These are routinely confused, including in older Gateway documentation. They are
different models with different jobs.

| | GWDM | HDRUK schema |
|---|---|---|
| **Role** | Internal storage and search | Public-facing input and output |
| **Audience** | The Gateway's own code | Data custodians and consumers |
| **Who authors in it** | Nobody, by hand | You do |
| **Versions** | 1.0 → 2.2 | 2.0.2 → 4.1.0 |
| **Where it is defined** | [`HDRUK/schemata`](https://github.com/HDRUK/schemata), `models/GWDM/` | Same repo, `models/HDRUK/` |

They are similar enough to mislead — both have `summary`, `provenance`,
`accessibility` — and different enough to break you. `summary.keywords` is an
array of strings in the HDRUK schema and a delimited string in the GWDM. Do not
assume a field means the same thing in both.

## The top-level structure

A GWDM record is an object of up to fifteen blocks. Three are required:
`required`, `summary` and `accessibility`.

| Block | Required | What it holds |
|---|---|---|
| `required` | ✓ | Identity and versioning. **The API writes this** |
| `summary` | ✓ | Title, description, keywords, publisher, population size |
| `accessibility` | ✓ | Access rights, formats, standards, usage conditions |
| `coverage` | | Geographic, temporal and demographic reach |
| `provenance` | | Origin of the data and how often it is refreshed |
| `linkage` | | Links to other datasets, publications, tools, media |
| `observations` | | Structured population counts |
| `structuralMetadata` | | Table and column level technical metadata |
| `tissuesSampleCollection` | | MIABIS-aligned biosample metadata |
| `demographicFrequency` | | Age, ethnicity and disease frequency bins |
| `omics` | | Assay and platform, for omics datasets |
| `icons` | | Categorisation icons, calculated on export. 2.1+ |
| `projectGrants` | | Associated project grants. 2.1+ |
| `datasetFilters` | | Categorisation tags. 2.1+ |
| `erd` | | Entity-relationship diagram of the tables. 2.1+ |

`structuralMetadata` is the one worth knowing about in advance: it is where table
and column definitions go, and it is unbounded. The richest record on the
development instance carries 72 tables in it.

## The four conventions

None of these are guessable from the field names, and all four cause support
tickets. If you read nothing else on this page, read this section.

### 1. List fields are delimited strings, joined with `;,;`

Many GWDM fields that hold a list are stored as **a single string** with the
members joined by the three characters `;,;` — not as a JSON array.

From the frozen fixture [`gwdm-2.0-rich.json`](../examples/gwdm-2.0-rich.json),
which is a real stored record:

```json title="summary.keywords, as actually stored"
"keywords": "Scan;,;Radiology;,;Diagnostic Image;,;X-Ray;,;Plain radiography"
```

```json title="accessibility.formatAndStandards.formats"
"formats": "XML;,;CSV;,;Text"
```

!!! danger "The delimiter is `;,;` — three characters, no quotes"
    You will see it written `';,;'` in JSONata maps, in PHP source, and in this
    project's own notes. **The quotes are source syntax, not part of the
    delimiter.** A value of `"A';,;'B"` is wrong; `"A;,;B"` is right.

    This has caught people out, including us — see `LIMITATIONS.md` L13.

**The round trip.** On the way in, the JSONata maps call `$to_str`, which joins
an array with the delimiter and passes anything else through untouched:

```javascript title="the canonical $to_str, copied into map after map"
$to_str := function($x){
  $x = null ? "" :
  $type($x) = "array" ? $join($x,';,;') :
  $x
};
```

On the way out, the Gateway API splits it again for indexing, in
`GwdmMetadataHandler::normalizeDelimited()`:

```php
return array_values(array_filter(explode(';,;', $value)));
```

Note that `normalizeDelimited()` accepts an array as well as a string and passes
it straight through. The write path is stricter than the read path, so a payload
with a real array in a delimited field may store and index fine and still fail
validation on a later translation.

**Which fields.** 19 GWDM paths carry the delimiter across the 1,364 datasets on
the development instance. The common ones, with how many datasets use them:

| Field | Datasets |
|---|---|
| `summary.keywords` | 1,109 |
| `accessibility.usage.dataUseRequirement` | 438 |
| `accessibility.formatAndStandards.formats` | 388 |
| `provenance.origin.collectionSituation` | 362 |
| `accessibility.formatAndStandards.vocabularyEncodingSchemes` | 326 |
| `summary.datasetType` | 260 |
| `linkage.associatedMedia` | 178 |
| `coverage.spatial` | 147 |
| `accessibility.usage.resourceCreator.name` | 113 |
| `accessibility.usage.dataUseLimitation` | 103 |

The full set is marked ⁂ in [the field reference](gwdm-reference.md). In total
**1,192 of 1,364 stored datasets (87%)** contain the delimiter somewhere, so it
is not an edge case — it is how the model works.

### 2. `-1` means "unknown" in numeric fields

A numeric field whose value is genuinely unknown is stored as `-1`, not as `null`
and not as `0`. The maps do this with `$null_to_number`.

`summary.populationSize` is where you will meet it: **667 of 1,364 datasets**
carry `-1` there — very nearly half.

```json title="gwdm-2.0-awkward.json — a real record with unknown population"
"populationSize": -1
```

If you are consuming Gateway metadata, treat a negative population size as
missing data. If you are producing it, send `-1` rather than `0` when you do not
know, because `0` is a factual claim that the cohort is empty.

### 3. Some fields are written by the API and will overwrite what you send

Two parts of every record are computed by the Gateway from its own database, in
`Gwdm2xHandler::prepareMetadata()`. Whatever you send in them is discarded.

**The whole `required` block:**

| Field | What the API writes |
|---|---|
| `required.gatewayId` | The dataset's primary key |
| `required.gatewayPid` | The dataset's persistent identifier |
| `required.issued` | Creation timestamp, from the database |
| `required.modified` | Last-modified timestamp, from the database |
| `required.revisions` | Computed list of prior versions |
| `required.version` | The dataset's semver — **see the exception below** |

**And `summary.publisher`**, which is rebuilt as `{ gatewayId, name }` from your
team record.

!!! tip "The one exception: `required.version`"
    `required.version` is the only field in the block the API will keep if you
    supply it — `prepareMetadata()` preserves an incoming value and only computes
    one when it is absent. Every other key is overwritten from the database
    unconditionally.

There are two live oddities here that are worth knowing about rather than being
surprised by:

- `summary.publisher.gatewayId` is the team's **raw primary key**, such as `"07"`,
  not its persistent identifier. This is inconsistent with the rest of the model,
  and is flagged as a known issue in the handler's own source.
- Nothing checks that the requesting team is allowed to publish as the named
  team: if you send a `summary.publisher.gatewayId` that resolves to any existing
  team, your publisher block is kept as sent.

Neither is something a partner should build on. Send no publisher block and let
the API fill it in.

### 4. Enum-constrained fields, and where the values live

Many fields accept only a fixed set of values, and the sets changed shape at GWDM
2.0 — from `SCREAMING CASE` to sentence case. `accrualPeriodicity` went from
`'STATIC','IRREGULAR','CONTINUOUS'…` to `'Static','Irregular','Continuous'…`,
and `deliveryLeadTime` from `'LESS 1 WEEK'` to `'Less than 1 week'`. A GWDM 1.x
value will fail validation against 2.x.

The enums are defined in Python, one class per enum, in
[`hdr_schemata/definitions/`](https://github.com/HDRUK/schemata/tree/dev/hdr_schemata/definitions).
Permitted values for every constrained field are listed in
[the field reference](gwdm-reference.md).

## Version history

The GWDM has had six versions. `schemata` publishes a generated changelog for
each, which is the authoritative record; this is the shape of it.

=== "1.0 → 1.1"

    The cohort-description expansion. Added nine `coverage.*` descriptive fields
    (`gender`, `lifestyle`, `physical`, `psychological`, `socioeconomic`,
    `anthropometric`, `biologicalsamples`), the whole
    `tissuesSampleCollection` block, `summary.populationSize` and
    `required.version`.

    **Breaking:** `summary.publisher` changed from a `Publisher` type to an
    `Organisation`, replacing `publisherGatewayId` / `publisherName` with
    `gatewayId` / `name`. The Gateway still carries fallback code for the old
    shape.

=== "1.1 → 1.2"

    Two fields: `accessibility.access.accessServiceCategory` and
    `linkage.syntheticDataWebLink`.

=== "1.2 → 2.0"

    The big one, and the current baseline. Added `demographicFrequency`, `omics`,
    `coverage.datasetCompleteness`, `coverage.followUp`,
    `summary.inPipeline`, `provenance.origin.imageContrast`, and the
    publication-linkage fields.

    **Breaking, and the reason 1.x records cannot simply be revalidated as 2.x:**

    - The nine `coverage.*` cohort-description fields added in 1.1 were
      **removed** again.
    - Every enum was recased, as described above.
    - `linkage.datasetLinkage.*` changed from comma-separated strings to lists of
      `DatasetDescriptor` objects.
    - `accessibility` became required; a long list of previously-required fields
      became optional.

=== "2.0 → 2.1"

    Five new blocks and one field, all driven by the CRUK partner integration:
    `projectGrants` (8 fields), `datasetFilters` (5 fields), `erd`, `icons`, and
    `summary.funders`. Nothing removed, nothing recased — 2.1 is a clean superset
    of 2.0.

    All 20 GWDM 2.1 records on the development instance are CRUK records; they are
    the only place these blocks are populated in practice.

=== "2.2"

    **Extends 2.1** — everything in the 2.1 tab is carried forward. On top of
    that it adds the GA4GH Data Use Ontology fields that HDRUK 4.1.0 introduced:

    - `accessibility.usage.duoCodes` — machine-readable DUO codes, as a
      `;,;`-delimited string
    - `accessibility.usage.dataUsePermissions.patientRecontact` — whether the
      cohort can be recontacted

    `Gwdm22Handler` is the only handler that differs from its parent, and it
    differs by exactly one thing: it adds `duoCodes` to the searchable fields so
    DUO codes become a search facet.

    Because TRASER has no schema for `GWDM:2.2`, a `/translate` request targeting
    it must pass `validate_output=0` or it returns HTTP 400.

    The translation map into 2.2 is not finished and currently drops the 2.1
    sections — see [how 2.2 relates to 2.1](#how-22-relates-to-21).

### How 2.2 relates to 2.1

**GWDM 2.2 extends 2.1.** It is a superset: everything 2.1 added over 2.0 —
`summary.funders`, `icons`, `projectGrants`, `datasetFilters` and `erd` — is
carried forward, plus the two DUO paths above. The version line is
2.0 → 2.1 → 2.2, not two branches from 2.0.

That is worth stating plainly because **the current translation map does not
behave that way yet**, and if you read the map you would conclude otherwise.

!!! warning "The 2.2 translation map is unfinished scaffolding"
    `maps/GWDM/2.2/HDRUK/4.1.0/translation.jsonata` was created by copying the
    `GWDM 2.0`-targeted map and adding the two DUO fields. It therefore emits
    2.0's fields plus DUO, and **not** the five sections 2.1 added.

    That is an incomplete map, not a design decision — it is item 5 on the map's
    own to-do list. Until it is finished, a translation into GWDM 2.2 loses the
    2.1 sections.

The reason this matters more than an ordinary unfinished map is routing. Every
edge in the translation graph has weight 1, so TRASER minimises hop count:

| Route | Hops | Carries the 2.1 sections? |
|---|---|---|
| `HDRUK 4.1.0 → GWDM 2.2` | **1** | no — the incomplete map |
| `HDRUK 4.1.0 → 4.0.0 → GWDM 2.0 → 2.1 → 2.2` | 4 | yes |

**The one-hop route wins**, so the lossy path is the one that gets taken, and
there is no way to ask for the longer one. A CRUK-style record with
`projectGrants` translated into GWDM 2.2 arrives without them today — and CRUK is
the only partner on 2.1, so this lands on exactly the records it hurts most.

Once the map is completed the discrepancy goes away and 2.2 behaves as the
superset it is defined to be. Treat the table above as a description of the
present, not of the model.

## A stored GWDM 2.0 record

The smallest real record on the development instance — required fields only,
frozen as a fixture so it does not drift ([`DECISIONS.md` D8](https://github.com/HDRUK/gateway-2-integrations-testing)).

```json title="gwdm-2.0-minimal.json"
--8<-- "examples/gwdm-2.0-minimal.json"
```

For a fully-populated record, a deliberately awkward one, and the same dataset in
four different schemas, see [example payloads](examples.md).

## Where next

- [GWDM field reference](gwdm-reference.md) — every field, every version
- [The schema landscape](landscape.md) — how the GWDM relates to everything else
- [Creating metadata](creating-metadata.md) — authoring your first record
- [Add a GWDM field](../playbooks/add-a-gwdm-field.md) — the internal playbook
