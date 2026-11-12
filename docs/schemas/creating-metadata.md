---
title: Creating your metadata
description: Choose a supported schema and build metadata the Gateway will accept.
tags:
  - schemas
  - hdruk-schema
---

# Creating your metadata

**Applies to:** HDRUK 2.0.2 – 4.1.0 · GWDM 2.0 – 2.2

You author metadata in a schema the Gateway supports and `POST` it to the API.
TRASER validates it, translates it into the [GWDM](gwdm.md), and the Gateway
stores it. This page covers choosing the schema and building the record; sending
it is [create a dataset](../api/datasets/create.md).

## Which schema

!!! tip "Recommended: HDRUK 4.1.0"
    [**HDRUK 4.1.0**](hdruk.md) is the current public-facing schema and the one
    the Gateway's own onboarding forms are built from. Use it unless you have a
    specific reason not to.

    Note that **4.0.0 is what the deployed development service serves today** —
    4.1.0 is committed but not yet deployed. If you are testing against dev
    right now, author 4.0.0 and add the three
    [4.1.0 fields](hdruk.md#what-410-adds-over-400) when it lands.

| Schema | Use it when |
|---|---|
| [HDRUK 4.1.0](hdruk.md) | You are a UK health data custodian and have a free choice |
| HDRUK 3.0.0 / 2.2.x / 2.1.x | You already author in one of these — all still supported |
| [CRUK 1.0.0](partner-schemas.md) | You are publishing through the CRUK partner context |
| [GWDM 2.x](gwdm.md) | Rarely. It is the internal model; you would normally let us produce it |
| [BioSchema](https://bioschemas.org/) | Your metadata is already a Bioschemas profile. More limited coverage |
| Something else | See [Bring your own schema](../byos/index.md) |

The full picture, including which direction each works in, is on
[the schema landscape](landscape.md).

Field-by-field documentation for every schema is published at
[**hdruk.github.io/schemata**](https://hdruk.github.io/schemata/), generated from
the [Pydantic models](https://github.com/HDRUK/schemata/tree/dev/hdr_schemata/models)
that are the source of truth. Each model is also exported as
[JSON Schema](https://json-schema.org/).

## Asking the service what it supports

Rather than trusting a list in documentation — including this one — ask TRASER.
It answers from what is actually deployed.

All samples below use a shell variable for the base URL, so you change one line
rather than every line. The current value and the reason it is worth
double-checking are on [the TRASER API reference](../reference/traser-api.md).

```bash
TRASER=https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app
```

### Supported schemas

=== "cURL"

    ```bash
    curl -s "$TRASER/list/schemas"
    ```

    ```json
    {
      "HDRUK": ["2.0.2","2.1.0","2.1.2","2.1.3","2.2.0","2.2.1","3.0.0","4.0.0"],
      "GWDM": ["1.0","1.1","1.2","2.0","2.1"],
      "CRUK": ["1.0.0"],
      "SchemaOrg": ["BioSchema","default","GoogleRecommended"]
    }
    ```

=== "Python"

    ```python
    import json
    import requests

    TRASER = "https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app"

    response = requests.get(f"{TRASER}/list/schemas", timeout=30)
    response.raise_for_status()
    print(json.dumps(response.json(), indent=2))
    ```

=== "Browser"

    [`/list/schemas`](https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app/list/schemas)

Response verified against the deployed development service. Note what is
**absent**: HDRUK 4.1.0 and GWDM 2.2, both of which exist in the repositories.
This is the deployed-versus-in-repo gap described on
[the version matrix](../reference/version-matrix.md).

### Supported translations

Which schema can become which. A pair not listed here can still be translated if
a route exists through intermediate schemas — see
[the translation graph](../reference/translation-graph.md).

=== "cURL"

    ```bash
    curl -s "$TRASER/list/templates"
    ```

    ```json
    [
      {
        "output_model": "HDRUK",
        "output_version": "2.1.2",
        "input_model": "HDRUK",
        "input_version": "datasetv2"
      },
      {
        "output_model": "HDRUK",
        "output_version": "2.1.2",
        "input_model": "GWDM",
        "input_version": "1.0"
      }
    ]
    ```

    Truncated — 46 entries are returned.

=== "Python"

    ```python
    import collections
    import requests

    TRASER = "https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app"

    templates = requests.get(f"{TRASER}/list/templates", timeout=30).json()
    print(f"{len(templates)} translations available")

    by_output = collections.defaultdict(list)
    for t in templates:
        key = f"{t['output_model']}:{t['output_version']}"
        by_output[key].append(f"{t['input_model']}:{t['input_version']}")

    for target in sorted(by_output):
        print(f"{target} ← {', '.join(sorted(by_output[target]))}")
    ```

=== "Browser"

    [`/list/templates`](https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app/list/templates)

A frozen snapshot of all 46 is committed as
[`translation-templates.json`](../examples/translation-templates.json), so you can
work offline and see what the graph looked like when this page was written.

### Getting a schema itself

To fetch the JSON Schema for a specific version — useful for generating a
skeleton, or for validating locally before you send anything:

=== "cURL"

    ```bash
    curl -s "$TRASER/get/schema?name=HDRUK&version=4.0.0"
    ```

=== "Python"

    ```python
    import requests

    TRASER = "https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app"

    body = requests.get(
        f"{TRASER}/get/schema",
        params={"name": "HDRUK", "version": "4.0.0"},
        timeout=30,
    ).json()

    schema = body["schema"]                  # note: nested, see below
    print("blocks:  ", sorted(schema["properties"]))
    print("required:", schema["required"])
    ```

!!! note "`/get/schema` nests its payload, and does it differently again"
    The response is `{"name": …, "version": …, "schema": {…}}` — the JSON Schema
    is under **`schema`**, and there is no `status_code` / `response` envelope of
    the kind the frozen fixtures carry. Three endpoints, three body shapes; check
    what you have before indexing into it.

## Building the record

### Start from a real one

The fastest way to a valid record is to start from one that already is. Four real
datasets are frozen in this repository, each in several schemas:

| Fixture | What it demonstrates |
|---|---|
| [`hdruk-4.0.0-minimal.json`](../examples/hdruk-4.0.0-minimal.json) | The smallest thing that validates |
| [`hdruk-4.0.0-rich.json`](../examples/hdruk-4.0.0-rich.json) | Fully populated, 72 structural-metadata tables |
| [`hdruk-4.0.0-awkward.json`](../examples/hdruk-4.0.0-awkward.json) | Unknown population size, awkward age range |
| [`hdruk-4.0.0-cruk-gwdm21.json`](../examples/hdruk-4.0.0-cruk-gwdm21.json) | A partner-context record |

!!! warning "The fixtures carry a response envelope"
    These files are captured TRASER responses, so each is wrapped:

    ```json
    { "status_code": 200, "response": { … the metadata … } }
    ```

    The metadata you send is the contents of `response`, not the whole file.

See [example payloads](examples.md) for the same dataset side by side in four
different schemas.

### The three blocks you cannot omit

HDRUK 4.x requires eight top-level members: `identifier`, `version`,
`revisions`, `issued`, `modified`, `summary`, `accessibility` and `observations`.

In practice `summary` and `accessibility` are the two that take thought.
`identifier`, `issued`, `modified`, `revisions` and `version` describe the
record's identity and lifecycle, and much of that is
[rewritten by the API](gwdm.md#3-some-fields-are-written-by-the-api-and-will-overwrite-what-you-send)
once stored — so do not spend long computing them.

### Conventions that will catch you

These are properties of the **GWDM**, which is what your metadata becomes. They
are covered in full in [the four conventions](gwdm.md#the-four-conventions), and
they are the difference between a record that round-trips and one that quietly
loses fields.

- **Unknown numbers are `-1`**, not `0` and not `null`. `summary.populationSize`
  is `-1` in nearly half of all stored datasets.
- **Some list fields become `;,;`-delimited strings on storage.** You send an
  array in the HDRUK schema; it is joined on the way in and split on the way out.
  You do not need to do this yourself — but it explains what you see if you read
  the raw GWDM back.
- **Do not compute `summary.publisher`** or anything in the GWDM `required`
  block. The API overwrites them from its own database.

## Before you send it

Validate. It is one call, and it is much cheaper than debugging a rejected
`POST`:

```bash
curl -s -X POST "$TRASER/validate?input_schema=HDRUK&input_version=4.0.0" \
  -H "Content-Type: application/json" \
  -d '{"metadata": { … your record … }}'
```

Or ask which schemas it *already* matches, if you are not sure what you have:

```bash
curl -s -X POST "$TRASER/find" \
  -H "Content-Type: application/json" \
  -d '{ … your record … }'
```

!!! danger "`/find` takes the bare record — the others take it wrapped"
    `/translate` and `/validate` expect `{"metadata": …}`. **`/find` expects the
    metadata object on its own.**

    Wrap it for `/find` and you get HTTP 200 with `matches: false` for every
    schema and a misleading error about a missing `required` property — because
    the wrapper is what got validated. It is a silent failure, and it is easy to
    do.

Full detail on both endpoints is on [metadata validation](validation.md).

## Choosing how it is stored

Two optional request headers change what happens after TRASER hands your record
to the Gateway. Both have sensible defaults and most partners never set either.

| Header | Effect | Default |
|---|---|---|
| `x-gwdm-version` | Which GWDM version to store as: `2.0`, `2.1`, `2.2` | `2.0` |
| `x-partner-context` | Which partner identity to store under | `HDRUK` |

Query parameters `?schema_model=` and `?schema_version=` do the equivalent job on
the **read** path, and take priority over the `x-schema-model` /
`x-schema-version` headers. See
[key concepts](../get-started/concepts.md#three-things-people-conflate) for why
the write-side and read-side controls are separate.

## Where next

- [Metadata validation](validation.md) — check the record properly
- [Create a dataset](../api/datasets/create.md) — send it
- [The GWDM explained](gwdm.md) — what it becomes
- [Example payloads](examples.md) — the same record in four schemas
