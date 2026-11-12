---
title: Worked examples
description: Example metadata payloads for the supported schemas.
tags:
  - schemas
  - examples
---

# Worked examples

**Applies to:** HDRUK 4.0.0 · GWDM 2.0 – 2.1 · SchemaOrg

Four real datasets from the Gateway, frozen into this repository so they cannot
drift, each shown in every schema the Gateway can produce from it.

The single most useful thing on this page is the tab set below: **the same
dataset, in four different shapes.** Comparing them tells you more about how
translation behaves than any amount of prose.

!!! info "These are real records, with contact details removed"
    Every payload here was harvested from a live Gateway dataset. Email addresses
    were replaced with `user@example.com` and telephone numbers with
    `+44 7700 000000` before the files were written — the harvest script refuses
    to write a file that still contains an unredacted match.

    Nothing else was altered. The awkward values are genuinely in the data.

!!! warning "The files carry a response envelope"
    These are captured TRASER and Gateway responses, so each is wrapped:

    ```json
    { "status_code": 200, "response": { … the metadata … } }
    ```

    A payload you submit is the contents of `response`, not the whole file. The
    GWDM fixtures are the exception — they are bare metadata objects.

## The four datasets

| Fixture | Dataset | Why it is here |
|---|---|---|
| **rich** | NHS England Diagnostic Imaging Dataset | Fully populated. 72 structural-metadata tables, complete coverage and provenance, a real population size |
| **minimal** | Oxford University Hospitals ARIA Radonc | The smallest thing that validates — required fields and little else |
| **awkward** | Sussex Integrated Dataset | `populationSize: -1`, a string `typicalAgeRange`, an `observations` array |
| **cruk** | Pancreatic Cancer Radiomics Cohort | **GWDM 2.1** under the **CRUK** partner context — the only live example of either |

Every file is in [`docs/examples/`](../examples/README.md), together with the
scripts that produced them.

## The same dataset in four schemas

The **minimal** dataset, because it is short enough to read side by side. This is
one stored record, translated four ways on read.

=== "GWDM 2.0"

    What the Gateway actually stores. No output schema requested means you get
    this, untranslated.

    ```json title="gwdm-2.0-minimal.json"
    --8<-- "examples/gwdm-2.0-minimal.json"
    ```

=== "HDRUK 4.0.0"

    The public-facing schema. Note `dataCustodian` where the GWDM has
    `summary.publisher`, and `identifier` where the GWDM has
    `required.gatewayPid`.

    ```json title="hdruk-4.0.0-minimal.json"
    --8<-- "examples/hdruk-4.0.0-minimal.json"
    ```

=== "schema.org (Google)"

    `SchemaOrg:GoogleRecommended` — the subset
    [Google Dataset Search](https://datasetsearch.research.google.com/)
    recommends. Far smaller than the others: it is built for discovery, not for
    data access.

    ```json title="schemaorg-googlerecommended-minimal.json"
    --8<-- "examples/schemaorg-googlerecommended-minimal.json"
    ```

=== "schema.org (default)"

    !!! danger "This is a real failure response, kept deliberately"
        `SchemaOrg:default` and `SchemaOrg:BioSchema` are **unavailable for every
        one of the 1,364 stored datasets**. The only route from a GWDM 2.x record
        runs through the `GWDM 1.2 → 1.1` map, which returns HTTP 500.

        This is what a caller receives today. See
        [the schema landscape](landscape.md#two-things-the-diagram-is-telling-you).

    ```json title="schemaorg-default-minimal.json"
    --8<-- "examples/schemaorg-default-minimal.json"
    ```

### What to notice

Reading across those tabs, three things are worth taking away:

1. **The block names change, not just the values.** `summary.publisher` becomes
   `summary.dataCustodian`; `linkage` becomes `enrichmentAndLinkage`. A field
   that is "missing" is often present under a different name.
2. **Each hop can lose information.** The schema.org output is a fraction of the
   size, and that is by design — but the same effect happens accidentally when a
   route passes through an older schema that lacks a field. See
   [the translation graph](../reference/translation-graph.md).
3. **Failures are responses, not exceptions.** A broken translation gives you an
   HTTP 500 with a message naming the exact hop that failed. That message is the
   most useful diagnostic the system produces.

## The rich record

The fully-populated end of the range. 32 KB of GWDM, including 72 tables of
structural metadata — a realistic picture of what a large NHS dataset looks like
once onboarded.

??? example "GWDM 2.0 — NHS England Diagnostic Imaging Dataset (1,049 lines)"

    ```json title="gwdm-2.0-rich.json"
    --8<-- "examples/gwdm-2.0-rich.json"
    ```

??? example "HDRUK 4.0.0 — the same record (1,084 lines)"

    ```json title="hdruk-4.0.0-rich.json"
    --8<-- "examples/hdruk-4.0.0-rich.json"
    ```

??? example "schema.org GoogleRecommended — the same record"

    ```json title="schemaorg-googlerecommended-rich.json"
    --8<-- "examples/schemaorg-googlerecommended-rich.json"
    ```

This is also the best place to see
[the `;,;` convention](gwdm.md#1-list-fields-are-delimited-strings-joined-with)
in real data — `summary.keywords`,
`accessibility.formatAndStandards.formats` and
`accessibility.usage.dataUseRequirement` all carry it.

## The awkward record

Every dataset collection has records like this, and they are more instructive
than the clean ones.

??? example "GWDM 2.0 — Sussex Integrated Dataset (211 lines)"

    ```json title="gwdm-2.0-awkward.json"
    --8<-- "examples/gwdm-2.0-awkward.json"
    ```

Three things in it worth knowing about:

| What you see | What it means |
|---|---|
| `"populationSize": -1` | Population is **unknown**, not zero. [The `-1` sentinel](gwdm.md#2-1-means-unknown-in-numeric-fields) |
| `"typicalAgeRange": "0-120"` | A string, not a pair of integers. HDRUK 3.0.0 split this into `typicalAgeRangeMin` / `Max`; older records keep the string |
| `observations` populated | Structured population counts, which is where `populationSize` can be inferred from when it is absent |

## The CRUK record

The only live example of GWDM 2.1, and of a non-HDRUK partner context. All 20
CRUK datasets are stored as GWDM 2.1; the other 1,344 are GWDM 2.0.

??? example "GWDM 2.1 — Pancreatic Cancer Radiomics Cohort (171 lines)"

    ```json title="gwdm-2.1-cruk-gwdm21.json"
    --8<-- "examples/gwdm-2.1-cruk-gwdm21.json"
    ```

This record carries all five sections GWDM 2.1 added — `projectGrants`,
`datasetFilters`, `erd`, `icons` and `summary.funders`. Nothing else in the
database populates them. See
[partner & output schemas](partner-schemas.md#cruk-the-only-live-partner).

## Schema detection

`POST /find` tells you which schemas a payload is valid against. The results are
frozen too, and the contrast between two of them makes a point worth
internalising.

| Fixture | Matches |
|---|---|
| rich, minimal, awkward (GWDM 2.0) | `GWDM:2.0` **and** `GWDM:2.1` |
| cruk (GWDM 2.1) | `GWDM:2.1` **only** |

The GWDM 2.0 records match 2.1 as well because everything 2.1 added is optional —
a 2.0 record is a valid 2.1 record. The CRUK record matches only 2.1, because it
carries sections that do not exist in 2.0.

!!! tip "Detection tells you what a payload *could* be, not what it *is*"
    `/find` returns every schema the payload validates against. It cannot tell
    you which one the author had in mind, and for a minimal record that list is
    often long. State your input schema explicitly when you can.

??? example "The full `/find` response for the minimal record (257 lines)"

    Each entry carries `matches` and, where it fails, the AJV errors explaining
    why — which is a fast way to find out what a schema wants.

    ```json title="find-minimal.json"
    --8<-- "examples/find-minimal.json"
    ```

!!! danger "`/find` takes the bare payload"
    Unlike `/translate` and `/validate`, `/find` does **not** want
    `{"metadata": …}`. Wrap it and you get HTTP 200 with `matches: false` for
    everything and an error about a missing `required` property — because AJV
    validated your wrapper. Detail on [validation](validation.md).

## Regenerating these

The fixtures are pinned to specific dataset IDs, so a refresh reproduces the same
four examples rather than four arbitrary ones. The recipe and the scripts are in
[`docs/examples/README.md`](../examples/README.md).

## Where next

- [Creating metadata](creating-metadata.md) — build your own record
- [Metadata validation](validation.md) — check it
- [The GWDM explained](gwdm.md) — the conventions these examples demonstrate
- [GWDM field reference](gwdm-reference.md) — every field, generated
