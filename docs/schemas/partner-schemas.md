---
title: Partner & output schemas
description: Schemas the Gateway translates to and from on behalf of specific partners.
tags:
  - schemas
  - partner
---

# Partner & output schemas

**Applies to:** HDRUK 4.1.0 · GWDM 2.2 · CRUK 1.0.0

Some organisations run their own portal on top of Gateway data. A **partner
schema** lets them read and write metadata in their own shape, without the
Gateway storing anything differently.

## Partner schema or output schema?

The terms get used interchangeably and they are not the same thing.

**An output schema** is any shape the Gateway can translate *into* on read. You
ask for one per request, with a header or a query parameter. `HDRUK:4.0.0`,
`SchemaOrg:GoogleRecommended` and `CRUK:1.0.0` are all output schemas.

**A partner schema** is an output schema plus an identity. It belongs to a named
organisation, it becomes that organisation's *default* output schema, and it
comes with a **partner context** that also changes the shape of the response
envelope around the metadata.

So: every partner schema is an output schema. Most output schemas are not partner
schemas.

## Partner context

The partner context is set with the **`x-partner-context`** request header. It
resolves in this order:

1. The `x-partner-context` header on the request
2. The `DEFAULT_PARTNER_CONTEXT` environment variable
3. Fallback to `HDRUK`

It then drives two independent things:

| It decides | Which means |
|---|---|
| Which API resource class shapes the response | The envelope around the metadata differs — field names, nesting, what is included |
| The default output schema | What the metadata itself is translated into, when the request does not say |

That second one is only a *default*. An explicit `x-schema-model` /
`x-schema-version` on the request still wins, so a partner can ask for something
other than their own shape whenever they want.

### The configuration

Partner schemas are configured in `gateway-api-2`, in `config/partners.php`:

```php
'schema' => [
    'HDRUK' => ['model' => 'HDRUK', 'version' => env('HDRUK_CURRENT_VERSION', '4.0.0')],
    'CRUK'  => ['model' => 'CRUK',  'version' => '1.1.0'],
    // PRUK schema version is not yet finalised — placeholder until confirmed.
    'PRUK'  => ['model' => 'PRUK',  'version' => '0.0.0'],
],
```

There is one more setting worth knowing about:

```php
'allow_cross_context_read' => env('HDRUK_CROSS_CONTEXT_READ', true)
```

When true — and it defaults to true — the `HDRUK` operator context can read
datasets belonging to *every* partner. A partner context sees only its own.

!!! warning "The CRUK version in config does not exist"
    `config/partners.php` names CRUK `1.1.0` as the default output schema, but
    `schemata` and the deployed TRASER only publish CRUK **`1.0.0`**. There is no
    1.1.0 anywhere.

    Treat `1.0.0` as the real CRUK schema version. If you are adding a partner,
    do not copy the `1.1.0` line as a model.

`PRUK` is a placeholder — a reserved name with a `0.0.0` version and no schema,
no maps and no datasets. It is not usable.

## CRUK — the only live partner

Cancer Research UK is the sole non-HDRUK partner context in production use, and
is therefore the working precedent for every partner that follows.

| | |
|---|---|
| Partner context | `CRUK` |
| Schema | `CRUK:1.0.0` |
| Datasets | **20** |
| Stored as | **GWDM 2.1** — all 20 of them |
| Direction | Bidirectional with GWDM 2.0 and GWDM 2.1 |

Those 20 datasets are the only records in the entire 1,364-dataset development
database stored as GWDM 2.1, and the only place the five GWDM 2.1 blocks —
`projectGrants`, `datasetFilters`, `erd`, `icons` and `summary.funders` — are
populated in practice. GWDM 2.1 exists *because of* CRUK.

That is the pattern a partner integration follows: the partner's requirements
drive new GWDM fields, the new fields land in a new GWDM version, and the
partner's records are stored in it while everyone else stays on the older one.

One CRUK record is frozen as a fixture —
[`gwdm-2.1-cruk-gwdm21.json`](../examples/gwdm-2.1-cruk-gwdm21.json) — if you
want to see what a populated GWDM 2.1 record looks like.

!!! tip "A ready-made teaching example"
    Run the three GWDM 2.0 fixtures through TRASER's `/find` and they match
    **both** `GWDM:2.0` and `GWDM:2.1`, because everything 2.1 added is optional.
    Run the CRUK fixture through and it matches `GWDM:2.1` **only** — it carries
    the 2.1-only blocks, so it cannot be 2.0.

    Schema detection tells you the *most specific* schema a payload is valid
    against, not the one it was authored in.

## The schema.org family

`SchemaOrg:default`, `SchemaOrg:GoogleRecommended` and `SchemaOrg:BioSchema` are
output schemas but **not** partner schemas — no organisation owns them and no
partner context defaults to them. They exist for discovery: publishing Gateway
datasets in a shape that search engines and life-science aggregators understand.

Nobody submits metadata to the Gateway as schema.org. Inbound maps do exist for
`default` and `BioSchema`, but they are there to complete the graph.

!!! danger "`default` and `BioSchema` output are broken today"
    Requesting either returns `{"message": "failed to translate"}` for every one
    of the 1,364 stored datasets. The only route from GWDM 2.x runs through the
    `GWDM 1.2 → 1.1` map, which returns HTTP 500.

    `GoogleRecommended` works — it has a direct edge from GWDM 2.0.

    See [the schema landscape](landscape.md#two-things-the-diagram-is-telling-you).

## Requesting an output schema

Three ways, in the order they are resolved. Query parameters beat headers; headers
beat your partner default.

=== "Headers"

    ```bash
    curl -s "https://api.healthdatagateway.org/api/v1/datasets/868" \
      -H "x-schema-model: HDRUK" \
      -H "x-schema-version: 4.0.0"
    ```

=== "Query parameters"

    ```bash
    curl -s "https://api.healthdatagateway.org/api/v1/datasets/868?schema_model=HDRUK&schema_version=4.0.0"
    ```

=== "Partner default"

    ```bash
    curl -s "https://api.healthdatagateway.org/api/v1/datasets/868" \
      -H "x-partner-context: CRUK"
    ```

    No output schema named, so CRUK's configured default applies.

Name **no** output schema at all and you get the stored GWDM back, untranslated.
That is often what you want, and it is the only way to see a record exactly as
the Gateway holds it.

## Adding a partner

The mechanism above is what a new partner such as PRUK will use. The end-to-end
process — schema definition, maps, config, going live — is covered by two pages
written for the people doing it:

- [New partner](../playbooks/new-partner.md) — the playbook

## Where next

- [The schema landscape](landscape.md) — every family and which direction it works in
- [The GWDM explained](gwdm.md) — what partner metadata becomes on storage
- [Retrieving a dataset](../api/datasets/retrieve.md) — the read path in full
