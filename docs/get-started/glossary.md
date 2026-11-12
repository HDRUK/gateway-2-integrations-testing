---
title: Glossary
description: Every acronym and term used on this site, defined once.
tags:
  - getting-started
---

# Glossary

Every term this site uses, defined once. If a page uses a word you do not
recognise, it should be here.

## The models

GWDM
:   **Gateway Working Data Model.** The Gateway's single internal storage model.
    Every dataset is translated into it on ingest and out of it on read, whatever
    schema it arrived in. Versions 1.0 → 2.2. Nobody authors in it by hand.
    See [The GWDM explained](../schemas/gwdm.md).

HDRUK schema
:   The public-facing HDR UK health data metadata schema — the one a data
    custodian authors in. Versions 2.0.2 → 4.1.0, with **4.1.0** current. Not the
    same thing as the GWDM, despite sharing several block names. See
    [HDRUK schema](../schemas/hdruk.md).

Partner schema
:   An output schema belonging to a named organisation, which becomes that
    organisation's default output shape. `CRUK:1.0.0` is the only live one.
    See [partner & output schemas](../schemas/partner-schemas.md).

Input schema
:   The schema *you* author and submit in. Detected from the payload or stated on
    the request.

Output schema
:   The schema the Gateway translates *into* when a record is read. Requested per
    call with `x-schema-model` / `x-schema-version`, or defaulted from your
    partner context.

Schema family
:   A group of versions under one name — `HDRUK`, `GWDM`, `CRUK`, `SchemaOrg`.
    A specific version is written `Family:version`, as in `GWDM:2.1`.

## The services

TRASER
:   The **TRAnslation SERvice**. A Node.js service that detects, validates and
    translates metadata between schemas, and also hosts a developer UI. It is the
    only component that knows about more than one schema. See
    [the TRASER API](../reference/traser-api.md).

`gateway-api-2`
:   The core Laravel REST API. Owns the database, authentication, and business
    logic; calls TRASER on ingest and on read. Writes the GWDM to MySQL.

`gateway-web-2`
:   The Next.js frontend. Builds the manual onboarding form from form hydration.

`schemata`
:   The Pydantic v2 source of truth for every schema definition. Generates the
    JSON Schema files, the registry of available versions, and the published
    field documentation. **Renamed from `schemata-2`** — see below.

`traser-mapping-files`
:   The repository holding the JSONata translation maps and the registry of which
    translations exist.

## Translation

JSONata
:   The query and transformation language the translation maps are written in.
    Lightweight, JSON-native, and — importantly — **it has no import
    mechanism**, so helper functions are copy-pasted between maps.
    See [the JSONata cookbook](../reference/jsonata-cookbook.md).

Map
:   One `translation.jsonata` file, translating one specific `Model:version` into
    one other. Stored output-first:
    `maps/{OutputModel}/{outputVersion}/{InputModel}/{inputVersion}/translation.jsonata`.

Template
:   TRASER's word for a map, as exposed by its `/list/templates` endpoint. The
    same thing.

Translation graph
:   The directed graph whose nodes are `Model:version` pairs and whose edges are
    maps. 46 edges over 18 nodes as deployed. See
    [the translation graph](../reference/translation-graph.md).

Multi-hop translation
:   A translation with no direct map, routed through intermediate schemas. Going
    from GWDM 2.1 to schema.org `default` takes four hops.

Dijkstra routing
:   How TRASER picks a route across the graph. **Every edge has weight 1**, so it
    minimises the number of hops and nothing else — which means the route chosen
    is not necessarily the one that preserves the most fields.

`available.json`
:   The registry file listing which versions exist. There is one in `schemata`
    (which schemas are defined) and one in `traser-mapping-files` (which
    translations exist). They are generated, not hand-edited.

## Identity and versioning

PID / `gatewayPid`
:   **Persistent identifier.** A UUID that identifies a dataset's metadata across
    all its versions. Stable; use this to refer to a dataset from outside.

`gatewayId`
:   The dataset's primary key in the Gateway's own database, as a string. Not
    stable across environments, and not the same as the PID.

    Beware: `summary.publisher.gatewayId` is a **team's** primary key, not a
    dataset's — and it is a raw key rather than that team's PID, which is a known
    inconsistency.

`required.version`
:   The **dataset's** metadata version, a semver like `7.0.0` that increments as
    the custodian revises the record. **Not** the schema version — a persistent
    source of confusion.

`gwdmVersion`
:   Which GWDM version a record is stored as, carried on the storage envelope
    rather than inside the metadata.

Delta versioning
:   The Gateway stores only the latest metadata version in full; earlier versions
    are stored as **RFC 6902 JSON Patch** documents and reconstructed by
    replaying the chain. A delta row's `metadata` column is empty by design.

`original_metadata`
:   The payload as the partner submitted it, kept alongside the translated GWDM.

## Requests

Partner context
:   A named organisation identity on a request, set with `x-partner-context`. It
    changes both the response envelope and the default output schema.

`x-gwdm-version`
:   Request header selecting which GWDM version to store a record as. Valid
    values `2.0`, `2.1`, `2.2`. Defaults to `2.0`.

`x-schema-model` / `x-schema-version`
:   Request headers selecting the output schema. Query parameters
    `?schema_model=` and `?schema_version=` do the same thing and take priority.

API-owned field
:   A field the Gateway computes and overwrites regardless of what you send —
    the whole `required` block and `summary.publisher`. See
    [the four conventions](../schemas/gwdm.md#the-four-conventions).

## Ingest

GMI
:   **Gateway Metadata Ingestion.** The federation mechanism: the Gateway
    periodically harvests metadata from a custodian's own endpoint rather than
    waiting to be pushed to. 195 of the 1,364 development datasets arrived this
    way. See [federation](../api/gmi/index.md).

FMA
:   The **former name for GMI**. If you find "FMA" in older documentation, code
    or ticket titles, read it as GMI. Nothing else changed.

`create_origin`
:   How a dataset arrived: `MANUAL` (typed into the Gateway form), `GMI`
    (harvested), or `API` (submitted directly).

Form hydration
:   The mechanism that builds the manual onboarding form's fields from a schema,
    so the form does not have to be hand-maintained per version.

    !!! warning "Actively being reworked"
        Form hydration is being reworked by the HDR UK team. There are
        currently **two** competing implementations serving the same purpose,
        and it is not settled which one wins. Do not build against either yet.

    See the [TRASER API reference](../reference/traser-api.md) for the
    `/get/form_hydration` endpoint as it behaves today.

## Conventions

`;,;`
:   The three-character delimiter that joins list members into a single string in
    many GWDM fields. Present in 87% of stored datasets.

    You will see it written `';,;'` in JSONata and PHP source. **The quotes are
    source syntax, not part of the delimiter.** See
    [the four conventions](../schemas/gwdm.md#1-list-fields-are-delimited-strings-joined-with).

`-1`
:   The sentinel for "unknown" in GWDM numeric fields — not `null`, not `0`.
    `summary.populationSize` is `-1` in 667 of 1,364 datasets.

DUO codes
:   Machine-readable codes from the [GA4GH Data Use Ontology](https://github.com/EBISPOT/DUO)
    describing permitted and restricted uses of a dataset. Added in HDRUK 4.1.0
    and stored in GWDM 2.2.

Structural metadata
:   Table-and-column level technical description of a dataset, in the
    `structuralMetadata` block. Unbounded — the richest record on the development
    instance carries 72 tables.

## Naming that changed

Two renames catch people out, and both still appear in live code and
documentation:

| Old name | Current name | Note |
|---|---|---|
| **FMA** | **GMI** | Gateway Metadata Ingestion. Same mechanism |
| **`HDRUK/schemata-2`** | **`HDRUK/schemata`** | `github.com` links redirect; **GitHub Pages links do not**. `master` is now `main`, and the default branch is `dev` |

## Where next

- [Key concepts](concepts.md) — how these fit together
- [Which path am I on?](choose-your-path.md) — where to go from here
