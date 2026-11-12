---
title: TRASER API
description: Every TRASER endpoint, its request shape and its response shape.
tags:
  - reference
  - traser
---

# TRASER API

**Applies to:** HDRUK 2.0.2 – 4.1.0 · GWDM 1.0 – 2.2

TRASER — the **TRA**nslation **SER**vice — is the component that knows about
schemas. It validates metadata, works out which schema a payload is in, and
translates between schemas. The Gateway API calls it on every dataset write and
on every read that asks for a schema other than the stored one.

You can call it directly, and if you are writing or debugging a translation map
you should. Nothing on this page needs authentication.

## The base URL

Every runnable sample on this site opens by setting this variable, then uses
`$TRASER` thereafter:

```bash
TRASER=https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app
```

!!! warning "This hostname is not stable, and it is the only one"
    That is a Cloud Run auto-generated hostname — `qmnkcg5qjq` is a
    project-specific hash and `ew` the region. It changes if the service is
    recreated in another project or region. There is no stable alias:
    `traser.dev.hdruk.cloud` and `traser.prod.hdruk.cloud` were both probed and
    answered nothing.

    This is why the URL is stated **here and nowhere else** on this site. If it
    changes, this page is the only one that needs editing. Do not copy the
    literal hostname into your own documentation — set it in one variable, the
    way the samples do.

Confirm it is up before you debug anything else:

```bash
curl -s "$TRASER/list/schemas"
```

## The endpoints at a glance

Read the two shape columns before you write any client code. They do not follow
a single convention, and the request and response inconsistencies do not line up
with each other.

| Method | Path | Request body | Response body |
|---|---|---|---|
| POST | [`/find`](#post-find) | **bare metadata** | bare array |
| POST | [`/validate`](#post-validate) | `{"metadata": …}` | `{"details": "all ok"}` or `{"error", "details", "data"}` |
| POST | [`/translate`](#post-translate) | `{"metadata": …, "extra": …}` | **the translated metadata, bare** |
| GET | [`/list/schemas`](#get-listschemas) | — | bare `{family: [versions]}` |
| GET | [`/list/templates`](#get-listtemplates) | — | bare array of edges |
| GET | [`/list/translations`](#get-listtranslations) | — | bare array of route strings |
| GET | [`/get/schema`](#get-getschema) | — | `{name, version, schema}` |
| GET | [`/get/map`](#get-getmap) | — | `{input_schema, …, translation_map}` |
| GET | [`/get/form_hydration`](#get-getform_hydration) | — | bare hydration object |
| GET | [`/list/datasets`](#developer-tooling-listdatasets-and-getdataset) | — | bare array |
| GET | [`/get/dataset`](#developer-tooling-listdatasets-and-getdataset) | — | bare metadata |
| GET | [`/docs`](#the-swagger-page) | — | Swagger UI (HTML) |

!!! danger "Three request shapes, four response shapes, and they do not agree"
    `/find` is the odd one on the way **in** — it takes the bare metadata object,
    while `/translate` and `/validate` take it wrapped in `{"metadata": …}`.

    `/get/schema` and `/get/map` are the odd ones on the way **out** — they nest
    the payload under a named key, while `/find`, `/translate` and every `/list/*`
    endpoint return theirs bare.

    So `/find` is unusual inbound and conventional outbound; `/get/schema` is the
    reverse. A caller who writes `body["schema"]["required"]` against
    `/get/schema` and reuses the pattern on `/validate` gets a `KeyError`.
    There is no convention to infer. Check each endpoint.

### Two behaviours that catch people out

**Validation can change your data.** AJV is configured with `coerceTypes: true`
and `useDefaults: true`, so validating an object mutates it — coercing `"5"` to
`5`, filling in schema defaults. TRASER clones the object before validating, so
*its* callers are safe. If you run AJV yourself against a schema fetched from
`/get/schema`, use the same flags knowingly or clone first.

**Large bodies are rejected outright.** Anything over `MAX_BODY_MB` (default
512 MB) gets a 413 rather than a parse error. Structural metadata for a dataset
with thousands of tables can be large, but not that large — if you see a 413,
something is wrong with your request, not with your dataset.

---

## POST `/find`

**What it is for:** you have a payload and you want to know what the Gateway
thinks it is. This is the first call to make when an ingest is rejected and you
do not know why.

`/find` validates the payload against **every** loaded schema and tells you which
ones it matches.

=== "cURL"

    ```bash
    curl -s -X POST "$TRASER/find" \
      -H 'Content-Type: application/json' \
      --data @gwdm-2.0-minimal.json
    ```

=== "Python"

    ```python
    import json
    import os

    import requests

    TRASER = os.environ["TRASER"]     # set once — see "The base URL" above

    metadata = json.load(open("gwdm-2.0-minimal.json"))

    # note: the bare metadata object, NOT {"metadata": metadata}
    response = requests.post(f"{TRASER}/find", json=metadata, timeout=60)
    matches = [f"{e['name']}:{e['version']}" for e in response.json() if e["matches"]]
    print(matches)
    ```

Run against [`gwdm-2.0-minimal.json`](../examples/gwdm-2.0-minimal.json), the
matching entries are:

```json
[
  { "name": "GWDM", "version": "2.0", "matches": true },
  { "name": "GWDM", "version": "2.1", "matches": true }
]
```

Two matches, not one, because everything GWDM 2.1 added is optional — so a valid
2.0 record is also a valid 2.1 record. That is normal and it is why
`select_first_matching` exists.

### Parameters

| Query parameter | Values | Default | Effect |
|---|---|---|---|
| `with_errors` | `0` or `1` | `0` | Include the AJV error array for schemas that did **not** match |

`with_errors=1` is what makes the endpoint useful for iterating. Each miss gains
an `errors` array telling you exactly why:

```json
{
  "name": "HDRUK",
  "version": "2.0.2",
  "matches": false,
  "errors": [
    {
      "instancePath": "",
      "schemaPath": "#/required",
      "keyword": "required",
      "params": { "missingProperty": "identifier" },
      "message": "must have required property 'identifier'"
    }
  ]
}
```

!!! danger "Wrapping the body silently ruins the result"
    Posting `{"metadata": …}` to `/find` does **not** error. It returns HTTP 200
    with `matches: false` for all 17 schemas and the message *"must have required
    property 'required'"* — because AJV is dutifully validating your wrapper
    object, which is not metadata in any schema.

    If every schema misses and the errors all complain about a single missing
    top-level property, check your body shape first. This site's own
    documentation used to make exactly this mistake.

### Errors

| Cause | Status | Body |
|---|---|---|
| Missing or non-JSON `Content-Type` | 400 | `{"errors":[{"type":"field","value":…,"msg":"Invalid content type. Expected JSON.","path":"","location":"body"}]}` |
| `with_errors` not `0` or `1` | 400 | `{"errors":[{"type":"field","value":"yes","msg":"Invalid value","path":"with_errors","location":"query"}]}` |

`/find` is POST-only. A GET returns 404, so a clickable link to it in a browser
looks broken even when the service is healthy.

---

## POST `/validate`

**What it is for:** you know which schema you are targeting and you want the
complete list of what is wrong.

=== "cURL"

    ```bash
    # note the wrapper: {"metadata": …}
    jq '{metadata: .}' gwdm-2.0-rich.json > body.json

    curl -s -X POST "$TRASER/validate?input_schema=GWDM&input_version=2.0" \
      -H 'Content-Type: application/json' \
      --data @body.json
    ```

=== "Python"

    ```python
    import json
    import os

    import requests

    TRASER = os.environ["TRASER"]     # set once — see "The base URL" above

    metadata = json.load(open("gwdm-2.0-rich.json"))

    response = requests.post(
        f"{TRASER}/validate",
        params={"input_schema": "GWDM", "input_version": "2.0"},
        json={"metadata": metadata},          # wrapped
        timeout=60,
    )
    print(response.status_code, response.json())
    ```

On success — HTTP 200:

```json
{ "details": "all ok" }
```

### Parameters

| Query parameter | Required | Effect |
|---|---|---|
| `input_schema` | yes | Schema family, e.g. `GWDM`, `HDRUK` |
| `input_version` | yes | Version within that family, e.g. `2.0`, `4.0.0` |
| `subsection` | no | Validate only one top-level block, e.g. `summary` |

`subsection` is how the Gateway validates a partially-filled onboarding form. It
returns `{"details": "all ok"}` for a payload that would fail whole-document
validation, so do not use it as a substitute for the full check.

### Reading the error array

AJV runs with `allErrors: true`, so the array is **complete** rather than
stopping at the first problem. This is what makes `/validate` worth looping on.
A real failure — an invalid `timeLag` against HDRUK 4.0.0:

```json
{
  "error": "metadata validation failed",
  "details": [
    {
      "instancePath": "/provenance/temporal/timeLag",
      "schemaPath": "#/$defs/TimeLagV2/enum",
      "keyword": "enum",
      "params": {
        "allowedValues": [
          "Less than 1 week", "1-2 weeks", "2-4 weeks", "1-2 months",
          "2-6 months", "More than 6 months", "Variable",
          "Not applicable", "Other"
        ]
      },
      "message": "must be equal to one of the allowed values"
    },
    {
      "instancePath": "/provenance",
      "schemaPath": "#/properties/provenance/anyOf/1/type",
      "keyword": "type",
      "params": { "type": "null" },
      "message": "must be null"
    },
    {
      "instancePath": "/provenance",
      "schemaPath": "#/properties/provenance/anyOf",
      "keyword": "anyOf",
      "params": {},
      "message": "must match a schema in anyOf"
    }
  ],
  "data": { "…the entire payload you sent…" }
}
```

Three things to know about that shape:

1. **`instancePath` is a JSON Pointer into your payload.** It is the field to
   fix. `schemaPath` points into the schema and is only useful for finding the
   enum definition.
2. **One mistake produces several entries.** The block containing the bad field
   is usually `anyOf: [Thing, null]`, so a single bad value inside it fails the
   `Thing` branch, fails the `null` branch, and then fails the `anyOf`. Fix the
   deepest `instancePath` and the other two go away. Read the array from the
   longest path upwards.
3. **`data` echoes your whole payload back.** For a large dataset the useful part
   of the response is a fraction of a percent of its size, so extract `details`
   and discard the rest — and be aware the echo puts your payload in whatever
   logs the response.

### Errors

| Cause | Status | Body |
|---|---|---|
| Missing `input_schema` / `input_version` | 400 | `{"message":"Validation has failed","errors":[{"type":"field","msg":"Invalid value","path":"input_schema","location":"query"}, …]}` |
| Missing or non-object `metadata` | 400 | same shape, with `"path":"metadata","location":"body"` |
| Validation failed | 400 | `{"error":"metadata validation failed","details":[…],"data":{…}}` |

---

## POST `/translate`

**What it is for:** the core of the service. Convert metadata from one schema to
another, chaining maps as needed.

=== "cURL"

    ```bash
    jq '{metadata: .}' gwdm-2.0-rich.json > body.json

    curl -s -X POST "$TRASER/translate?input_schema=GWDM&input_version=2.0&output_schema=HDRUK&output_version=4.0.0" \
      -H 'Content-Type: application/json' \
      --data @body.json
    ```

=== "Python"

    ```python
    import json
    import os

    import requests

    TRASER = os.environ["TRASER"]     # set once — see "The base URL" above

    metadata = json.load(open("gwdm-2.0-rich.json"))

    response = requests.post(
        f"{TRASER}/translate",
        params={
            "input_schema": "GWDM", "input_version": "2.0",
            "output_schema": "HDRUK", "output_version": "4.0.0",
        },
        json={"metadata": metadata},
        timeout=120,
    )
    # the response IS the translated metadata — no envelope
    translated = response.json()
    print(sorted(translated))
    ```

```text
['accessibility', 'coverage', 'demographicFrequency', 'documentation',
 'enrichmentAndLinkage', 'identifier', 'issued', 'modified', 'observations',
 'omics', 'provenance', 'revisions', 'structuralMetadata', 'summary', 'version']
```

### Parameters

| Query parameter | Default | Effect |
|---|---|---|
| `input_schema` / `input_version` | auto-detected | Omit both and TRASER runs `/find` internally to work out what you sent |
| `output_schema` / `output_version` | service default | The target |
| `validate_input` | `1` | Set `0` to skip validating what you sent |
| `validate_output` | `1` | Set `0` to skip validating the result |
| `subsection` | — | Validate only one top-level block, on both sides |
| `select_first_matching` | `true` | On auto-detection, accept the first schema that matches |

Anything other than the literal `0` leaves `validate_input` / `validate_output`
on — so `validate_output=false` does **not** disable validation. Use `0`.

### Auto-detection and `select_first_matching`

Omit `input_schema` and `input_version` and TRASER detects the input for you.
Because a GWDM 2.0 record also validates as GWDM 2.1, detection is often
ambiguous. `select_first_matching` decides what happens then:

- `true` (the default) — take the first match and carry on.
- `false` — refuse to guess:

```json
{
  "message": "Input metadata object matched multiple schemas! Something could be wrong..",
  "details": [
    { "name": "GWDM", "version": "2.0", "matches": true },
    { "name": "GWDM", "version": "2.1", "matches": true },
    "…"
  ]
}
```

!!! warning "`select_first_matching=false` does nothing on the deployed dev service"
    The deployed dev build never coerced the query string, so the rejecting
    branch is dead there — the ambiguous request above succeeds. The behaviour
    shown is that of the current TRASER source, and is what you will get once dev
    is redeployed. If you are relying on `false` today, verify it rejects before
    you trust it.

Whichever way you go, **pass `input_schema` and `input_version` explicitly in
anything automated.** Detection is a debugging convenience, not a contract: add a
schema version to `schemata` and a payload that detected as one thing yesterday
can detect as another today.

### `validate_output=0`, and when you need it

You need it whenever the target schema is not defined in `schemata`.

!!! success "GWDM 2.2 no longer needs this"
    GWDM 2.2 **is** now defined in `schemata` and served by the deployed TRASER
    (checked 2026-09-21), so translations targeting it validate normally.
    `validate_output=0` is no longer required for 2.2.

The example below is retained because the *mechanism* still applies to any
target that has maps but no schema — `HDRUK:datasetv2` is the remaining
permanent case:

```json
{
  "message": "Output metadata validation failed",
  "details": [{ "message": "Schema HDRUK:datasetv2 is not known" }],
  "data": { "…the translated metadata, which is fine…" }
}
```

Note that `data` carries the translated output. The translation worked; only the
check failed. Add `validate_output=0` and the same call returns the metadata:

```bash
curl -s -X POST "$TRASER/translate?input_schema=HDRUK&input_version=4.1.0&output_schema=GWDM&output_version=2.2&validate_output=0" \
  -H 'Content-Type: application/json' --data @body.json
```

    **No longer true as of 2026-09-21** — the deployed dev TRASER now carries
    the GWDM 2.2 maps, so `GWDM:2.2` is a node in its graph and this call
    succeeds.

### The `extra` binding

Every map is evaluated against `{ input: <metadata>, extra: <supplementary> }`,
so a map can reference `extra.publisherName` as well as `input.summary.title`.
`extra` is the second, optional key in the request body — it is for values the
Gateway knows but the submitted metadata does not contain.

```json
{
  "metadata": { "…" },
  "extra": {
    "id": "DEMO-1",
    "pid": "demo-pid-0001",
    "publisherName": "Demo Custodian"
  }
}
```

Translating the same HDRUK 4.0.0 payload to GWDM 2.0 with and without that
`extra` block, the difference is visible in `required`:

| | `gatewayId` | `gatewayPid` |
|---|---|---|
| without `extra` | `95cd1eac-59b5-4cb2-9c08-0b8a9067c760` | `95cd1eac-59b5-4cb2-9c08-0b8a9067c760` |
| with `extra` above | `DEMO-1` | `demo-pid-0001` |

The map reads `extra.id ? extra.id : $truncate(input.identifier, 50)` — `extra`
wins where it is set and the payload is the fallback. `publisherName` is the
other way round: `input.summary.dataCustodian.name` wins and `extra` is the
fallback, so it changed nothing here.

The keys the Gateway API itself sends on ingest are `id`, `pid`, `datasetType`,
`publisherId` and `publisherName` — all five are placeholders or team values that
cannot be in a partner's own payload. Across all 57 map files 28 distinct `extra.*`
keys are referenced; if you are writing a map, `/get/map` on a neighbouring
edge is the reliable way to see which ones your target expects.

!!! note "`extra` is a sibling of `metadata`, not a field inside it"
    `{"metadata": {…}, "extra": {…}}`. Putting `extra` inside the metadata object
    makes it an unexpected additional property, and most schemas reject those.

### Multi-hop chaining

If there is no direct map from your input to your output, TRASER finds a route
through the graph and applies each map in turn. You do not ask for this and you
cannot see it in the response — see [the translation graph](translation-graph.md)
for how routes are chosen, why the shortest one is not always the best, and how
to force a specific route.

A same-schema translation is a **no-op**: if `input_schema == output_schema` and
`input_version == output_version`, the metadata is returned unchanged without any
map being evaluated. That is deliberate and it is how the Gateway can send every
ingest through `/translate` regardless of what arrived.

### Errors

| Cause | Status | Body |
|---|---|---|
| Output schema not a graph node | 400 | `{"message":"Cannot support the output model (HDRUK:9.9.9)","details":{}}` |
| Input schema not a graph node | 400 | `{"message":"Cannot support the input model (…)","details":{}}` |
| No route between two real nodes | 400 | forwarded from the graph, with the message naming both ends |
| Input failed validation | 400 | `{"message":"Input metadata validation failed","details":{"validationErrors":[…],"data":{…}}}` |
| Output failed validation | 400 | `{"message":"Output metadata validation failed","details":[…],"data":{…}}` |
| A map itself threw | 500 | `{"message":"Failed to execute translation between GWDM:1.2 and GWDM:1.1","details":{}}` |
| Missing `metadata` key | 400 | `{"message":"Translation has failed.","errors":[{"path":"metadata","location":"body", …}]}` |

The 500 above is not hypothetical — it is the real, current failure on the
`GWDM 1.2 → GWDM 1.1` hop, and because that hop sits on the only route from
stored GWDM to schema.org `default` and BioSchema, it takes both of those
outputs down. See [the translation graph](translation-graph.md#the-broken-hop)
and [errors](errors.md).

Note the distinction the status codes are trying to draw: **400 means the request
was wrong** (bad schema name, unroutable, invalid metadata) and **500 means a map
failed**, which is our problem, not yours.

---

## GET `/list/schemas`

Every schema family and version the service has loaded. This is the definitive
answer to "what can I send you?" for whichever deployment you are pointed at.

```bash
curl -s "$TRASER/list/schemas"
```

```json
{
  "HDRUK": ["2.0.2", "2.1.0", "2.1.2", "2.1.3", "2.2.0", "2.2.1", "3.0.0", "4.0.0"],
  "GWDM": ["1.0", "1.1", "1.2", "2.0", "2.1"],
  "CRUK": ["1.0.0"],
  "SchemaOrg": ["BioSchema", "default", "GoogleRecommended"]
}
```

That is the **deployed dev** service. It is behind the repositories: no HDRUK
4.1.0, no GWDM 2.2. See [the version matrix](version-matrix.md) for what exists
where.

---

## GET `/list/templates`

One entry per available translation map — that is, one directed edge of the
translation graph.

```bash
curl -s "$TRASER/list/templates" | jq 'length'
# 46
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
    "input_model": "HDRUK",
    "input_version": "2.1.3"
  }
]
```

**Read it output-first.** Each entry says "there is a map that produces
`output_model:output_version` *from* `input_model:input_version`", which matches
the directory layout in `traser-mapping-files`:
`maps/{OutputModel}/{outputVersion}/{InputModel}/{inputVersion}/translation.jsonata`.
Reading a row left to right as a direction of travel gets you the arrow backwards.

To treat it as a graph, invert each row into an edge `input → output`. That is
what [the translation graph](translation-graph.md) page does, and
[`translation_graph.py`](../examples/translation_graph.py) is the script.

Note that `HDRUK:datasetv2` appears here as an input but is **not** in
`/list/schemas` — a legacy edge with a map but no schema. You can translate out
of it; you cannot validate against it.

---

## GET `/list/translations`

Every destination reachable from one starting node, **with the route** TRASER
would take. This is the single most useful endpoint for answering "can I get from
my schema to X, and what will it go through on the way?"

```bash
curl -s "$TRASER/list/translations?schema=GWDM&version=2.1" | jq -r '.[]'
```

```text
GWDM:2.1 -> GWDM:2.0 -> GWDM:1.2 -> GWDM:1.1 -> HDRUK:2.1.2
GWDM:2.1 -> GWDM:2.0 -> GWDM:1.2 -> GWDM:1.1 -> HDRUK:2.1.2 -> HDRUK:2.1.3
GWDM:2.1 -> GWDM:2.0 -> HDRUK:3.0.0 -> HDRUK:2.2.1 -> HDRUK:2.2.0
GWDM:2.1 -> GWDM:2.0 -> HDRUK:3.0.0 -> HDRUK:2.2.1
GWDM:2.1 -> GWDM:2.0 -> HDRUK:3.0.0
GWDM:2.1 -> GWDM:2.0 -> HDRUK:4.0.0
GWDM:2.1 -> GWDM:2.0 -> GWDM:1.2 -> GWDM:1.1 -> GWDM:1.0
GWDM:2.1 -> GWDM:2.0 -> GWDM:1.2 -> GWDM:1.1
GWDM:2.1 -> GWDM:2.0 -> GWDM:1.2
GWDM:2.1 -> GWDM:2.0
GWDM:2.1
GWDM:2.1 -> CRUK:1.0.0
GWDM:2.1 -> GWDM:2.0 -> GWDM:1.2 -> GWDM:1.1 -> SchemaOrg:BioSchema
GWDM:2.1 -> GWDM:2.0 -> GWDM:1.2 -> GWDM:1.1 -> SchemaOrg:default
GWDM:2.1 -> GWDM:2.0 -> SchemaOrg:GoogleRecommended
```

Both parameters are required. Destinations with no route are simply absent from
the list, so a family you expected and cannot find is unreachable, not broken.
The single-element `GWDM:2.1` entry is the no-op self-translation.

| Query parameter | Required |
|---|---|
| `schema` | yes |
| `version` | yes |

Omitting either gives a 400:

```json
{
  "message": "Translation has failed.",
  "errors": [
    { "type": "field", "msg": "Invalid value", "path": "schema", "location": "query" },
    { "type": "field", "msg": "Invalid value", "path": "version", "location": "query" }
  ]
}
```

!!! note "The Swagger page documents this endpoint at the wrong path"
    The deployed dev Swagger UI lists it as `/translations`. That path returns
    404; the working path is `/list/translations`. See
    [the Swagger page](#the-swagger-page).

---

## GET `/get/schema`

The compiled JSON Schema for one schema and version. Use it to see the real
required-field list and enum values rather than inferring them from error
messages.

=== "cURL"

    ```bash
    curl -s "$TRASER/get/schema?name=HDRUK&version=4.0.0" | jq '.schema.required'
    ```

=== "Python"

    ```python
    import os

    import requests

    TRASER = os.environ["TRASER"]     # set once — see "The base URL" above

    body = requests.get(
        f"{TRASER}/get/schema",
        params={"name": "HDRUK", "version": "4.0.0"},
        timeout=30,
    ).json()

    schema = body["schema"]              # nested — see the note below
    print("blocks:  ", sorted(schema["properties"]))
    print("required:", schema["required"])
    ```

| Query parameter | Required | Notes |
|---|---|---|
| `name` | yes | Family, e.g. `HDRUK` |
| `version` | no | Omit for the latest loaded version |

!!! warning "The payload is nested under `schema`"
    The response is `{"name": …, "version": …, "schema": {…}}`. Indexing
    `body["required"]` raises a `KeyError`; you want `body["schema"]["required"]`.
    This is the endpoint that most often catches people, because `/translate`
    beside it returns its payload bare.

### Errors

| Cause | Status | Body (current source) | Body (deployed dev) |
|---|---|---|---|
| Missing `name` | 400 | `{"message":"Invalid query parameters.","errors":[{"path":"name","location":"query", …}]}` | same |
| Unknown schema or version | 400 | `{"error":"Schema HDRUK:9.9.9 not found"}` | `{"error":"Cannot read properties of undefined (reading 'schema')"}` |

That second row is worth remembering. On the deployed dev service, asking for a
version that does not exist gets you a leaked JavaScript `TypeError`, not a
message about schemas. If you see it, you have a typo in `version`, or you are
asking for something that only exists in the repositories.

---

## GET `/get/map`

The raw JSONata source of one translation map. This is how you read an existing
map without cloning `traser-mapping-files`, and it is the fastest way to answer
"what does the Gateway actually do with my `keywords` field?"

```bash
curl -s "$TRASER/get/map?input_schema=HDRUK&input_version=4.0.0&output_schema=GWDM&output_version=2.0" \
  | jq -r '.translation_map' | head -20
```

```text
(
/*function to enforce any arrays to be strings */
$to_str := function($x){
  $x = null ? "" :
  $type($x) = "array" ? $join($x,';,;') :
  $x
};
```

All four parameters are required. The response nests the source under
`translation_map`:

```json
{
  "input_schema": "HDRUK",
  "input_version": "4.0.0",
  "output_schema": "GWDM",
  "output_version": "2.0",
  "translation_map": "(\n/*function to enforce any arrays…"
}
```

!!! warning "A missing map returns 200 with `translation_map: null` on deployed dev"
    Asking for an edge that does not exist —
    `input_schema=HDRUK&input_version=4.0.0&output_schema=SchemaOrg&output_version=BioSchema`
    — gives HTTP **200** and a null map on the deployed dev service. The current
    source returns a 400 instead:

    ```json
    {
      "error": "Translation not found",
      "message": "Translation for HDRUK-4.0.0 to SchemaOrg-BioSchema is not implemented",
      "details": "Translation for HDRUK-4.0.0 to SchemaOrg-BioSchema is not implemented"
    }
    ```

    So do not treat a 200 from `/get/map` as proof the edge exists. Check
    `translation_map` is non-null, or check `/list/templates`.

---

## GET `/get/form_hydration`

Returns a form definition — field labels, components, guidance text — derived
from a schema by a JSONata hydration template. `gateway-web-2` uses it to build
the manual dataset-onboarding form.

```bash
curl -s "$TRASER/get/form_hydration?name=HDRUK&version=4.0.0" | jq '.schema_fields[0]'
```

```json
{
  "title": "Dataset identifier",
  "is_array_form": false,
  "description": "System dataset identifier.",
  "location": "identifier",
  "guidance": "N/A",
  "field": {
    "component": "TextField",
    "name": "Dataset identifier",
    "placeholder": "226fb3f1-4471-400a-8c39-2b66d46a39b6",
    "label": "System dataset identifier.",
    "limit": 36,
    "required": false,
    "hidden": true
  }
}
```

| Query parameter | Required | Notes |
|---|---|---|
| `name` | yes | Schema family |
| `version` | no | Falls back to the `HYDRATION_MAP_VERSION` env var |
| `dataTypes` | no | Comma-separated list injected into the hydration source, e.g. `Genomics,Imaging` |

!!! warning "Actively being reworked"
    Form hydration currently has two competing implementations — this endpoint,
    and a separate `config/form_hydration.php` in the Gateway API that fetches
    `.form.json` files from the `schemata` repository. They are two sources of
    truth for the same concept, and no `4.1.0.form.json` exists anywhere, so the
    current schema cannot be hydrated by the second mechanism at all.

    Document against it if you must, but do not build on it yet.

A hydration template that matches nothing evaluates to `undefined`, which would
serialise to a malformed empty body, so you get a 400
`{"message":"Hydration failed."}` instead.

---

## Developer tooling: `/list/datasets` and `/get/dataset`

!!! danger "Not a data API"
    These two read TRASER's **local cache of Gateway datasets**, which exists so
    the [results matrix](traser-tools.md#results-the-passfail-matrix) and the
    [playground](traser-tools.md#playground-the-jsonata-sandbox) have real
    payloads to work with. The cache is swept on a TTL, holds whatever the last
    sync happened to fetch, and is deliberately excluded from the OpenAPI spec.

    For real dataset retrieval use the Gateway API —
    [retrieve a dataset](../api/datasets/retrieve.md).

```bash
curl -s "$TRASER/list/datasets" | jq '.[0]'
```

```json
{
  "pid": "195920d6-ee4b-4eb5-80b4-8d8f60e9c799",
  "title": "1958 National Child Development Study - Pain data",
  "gatewayId": "735",
  "status": "ACTIVE"
}
```

`/get/dataset?pid=<pid>` then returns that dataset's bare metadata. Missing `pid`
gives 400 `{"message":"pid query param is required"}`; an unknown one gives 404
`{"message":"Dataset <pid> not found"}`.

Both are **404 on the deployed dev service** — it is an older build that does not
carry them. They work on a local instance.

---

## The Swagger page

`GET /docs` serves an interactive Swagger UI covering the JSON endpoints. `/docs`
301-redirects to `/docs/`, so follow redirects.

The current source also serves the raw spec at `GET /openapi.json`, generated
from JSDoc comments on the route handlers. It documents nine paths — the two
dataset-cache endpoints above are intentionally omitted.

!!! warning "The deployed dev Swagger page is the old Express service's, and it is wrong in two ways"
    On `https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app`:

    - `/openapi.json` returns **404**. The spec is embedded in
      `/docs/swagger-ui-init.js`; `/docs/swagger.json` serves HTML, not JSON.
    - The spec is titled *"Express API for metadata JSON translation service"*. It
      documents `/translations`, which **404s** — the working path is
      `/list/translations` — and it does **not** document `/validate`, which
      works.

    Treat this page as a starting point, not as the contract. This page is the
    contract.

---

## Which endpoint do I want?

| I want to… | Call |
|---|---|
| find out what schema my payload is in | [`POST /find`](#post-find) |
| get the full list of what is wrong with it | [`POST /validate`](#post-validate) with `input_schema` set |
| see what the Gateway will store | [`POST /translate`](#post-translate) to `GWDM:2.0` |
| see what a consumer will get | `POST /translate` to their output schema |
| know whether a route exists at all | [`GET /list/translations`](#get-listtranslations) |
| know what versions I can use | [`GET /list/schemas`](#get-listschemas) |
| read the real required fields and enums | [`GET /get/schema`](#get-getschema) |
| read an existing map | [`GET /get/map`](#get-getmap) |

The four-step journey those first calls make up is set out on
[validating your metadata](../schemas/validation.md).
