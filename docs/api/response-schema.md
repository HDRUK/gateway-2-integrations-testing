---
title: Choosing your response schema
description: The headers and query parameters that decide what schema you get back.
tags:
  - api
  - schemas
  - traser
---

# Choosing your response schema

**Applies to:** HDRUK 2.0.2 – 4.1.0 · GWDM 1.0 – 2.2

The Gateway stores every dataset as the GWDM and can translate it into any schema
it has a route to. Four different request-level controls decide what you get
back, and they do not all work on every endpoint.

This page documents each one, verified against the live API.

## The four controls

| Control | Sets | Priority |
|---|---|---|
| `?schema_model=` + `?schema_version=` | the output schema | **1 — highest** |
| `x-schema-model` + `x-schema-version` headers | the output schema | 2 |
| `x-partner-context` header | the *default* output schema, and the response shape | 3 |
| *(nothing)* | falls back — see [below](#what-you-get-if-you-set-nothing) | 4 |

Separately, and a **different concern**:

| Control | Sets |
|---|---|
| `x-gwdm-version` header | which stored GWDM version is read or written — *not* the response schema |

## First: which endpoint are you calling?

This matters more than anything else on the page. The two dataset read endpoints
honour different subsets of the controls.

| Control | `/api/v1/datasets/{id}` | `/api/v2/datasets/{id}` |
|---|:-:|:-:|
| `?schema_model` / `?schema_version` | ✅ | ✅ (and beats the headers) |
| `x-schema-model` / `x-schema-version` | ❌ **silently ignored** | ✅ |
| `x-partner-context` | ❌ no effect on output schema | ✅ |
| `x-gwdm-version` | ❌ **silently ignored** | ✅ |
| Default with nothing set | stored **GWDM**, untranslated | translated to **HDRUK 4.0.0** |

!!! danger "The headers do nothing on `/api/v1/`, and fail silently"
    Send `x-schema-model: SchemaOrg` to `/api/v1/datasets/868` and you get
    HTTP 200 with the **stored GWDM**. No error, no warning. Verified:

    ```bash
    A=https://api.healthdatagateway.org
    T=https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app

    detect() {   # ask TRASER what schema a payload is in
      curl -s "$1" | jq '.data.versions[0].metadata.metadata' \
        | curl -s -X POST "$T/find" -H 'Content-Type: application/json' --data @- \
        | jq -r '.[] | select(.matches) | "\(.name):\(.version)"'
    }

    curl -s -H 'x-schema-model: SchemaOrg' -H 'x-schema-version: GoogleRecommended' …
    ```

    | Request | Detected schema of the response |
    |---|---|
    | v2, headers `SchemaOrg` / `GoogleRecommended` | `SchemaOrg:default`, `SchemaOrg:GoogleRecommended` |
    | **v1, same headers** | **`GWDM:2.0`, `GWDM:2.1`** — ignored |
    | v1, `?schema_model=HDRUK&schema_version=3.0.0` | `HDRUK:3.0.0` — honoured |
    | v2, query `HDRUK`/`3.0.0` **and** headers `SchemaOrg`/`GoogleRecommended` | `HDRUK:3.0.0` — the query params win |

    **If you only need one mechanism, use the query parameters.** They work
    everywhere and their precedence is unambiguous.

---

## `?schema_model` and `?schema_version`

The query parameters. Highest priority, honoured on both endpoints, and the ones
to reach for.

=== "cURL"

    ```bash
    curl -s "https://api.healthdatagateway.org/api/v1/datasets/868?schema_model=HDRUK&schema_version=4.0.0"
    ```

=== "Python"

    ```python
    import requests

    API = "https://api.healthdatagateway.org/api/v1"

    response = requests.get(
        f"{API}/datasets/868",
        params={"schema_model": "HDRUK", "schema_version": "4.0.0"},
        timeout=60,
    )
    print(response.json()["message"])
    ```

```json
{ "message": "success", "data": { "…" } }
```

!!! warning "They are all-or-nothing, and half of them is a 500"
    ```bash
    curl -s "https://api.healthdatagateway.org/api/v1/datasets/868?schema_model=HDRUK"
    ```

    ```json
    { "code": 500, "message": "You have given a schema_model but not a schema_version" }
    ```

    A 500 for a client mistake is misleading. It is your request, not the server.
    Send both or neither.

Valid combinations are whatever the deployed TRASER can route to — see
[the version matrix](../reference/version-matrix.md#the-matrix). Two that will
disappoint you:

| Request | Result |
|---|---|
| `schema_model=HDRUK&schema_version=4.1.0` | **400** — `Cannot support the output model (HDRUK:4.1.0)`. Not deployed anywhere yet, production included |
| `schema_model=SchemaOrg&schema_version=BioSchema` | **400** — the route is broken, [see below](#which-output-schemas-actually-work) |

---

## `x-schema-model` and `x-schema-version`

The same choice as headers, so a client can set it once globally instead of
appending query parameters to every URL. That is what they exist for — the HDRUK
portal and partner frontends set them per-deployment.

```bash
curl -s \
  -H 'x-schema-model: SchemaOrg' \
  -H 'x-schema-version: GoogleRecommended' \
  "https://api.healthdatagateway.org/api/v2/datasets/868"
```

**`/api/v2/` only.** They are read by `OutputSchemaContext`, which the v1
controllers do not use.

Query parameters beat headers, so a client with global headers can still override
per-request by appending `?schema_model=…&schema_version=…` — which is the
intended pattern rather than a quirk.

---

## `x-partner-context`

Sets the active **partner**, which does two things at once:

1. Chooses the API Resource class that shapes the response envelope.
2. Provides the **default** output schema, used when neither the query
   parameters nor the schema headers are set.

```bash
curl -s -H 'x-partner-context: CRUK' \
  "https://api.dev.hdruk.cloud/api/v2/datasets/2187"
```

Resolution is: the `x-partner-context` header → the `DEFAULT_PARTNER_CONTEXT`
environment variable → the hard-coded fallback `HDRUK`. The per-partner defaults
live in `config/partners.php`:

| Partner | Default output schema |
|---|---|
| `HDRUK` | `HDRUK` at `HDRUK_CURRENT_VERSION` (currently **4.0.0**) |
| `CRUK` | `CRUK:1.1.0` |
| `PRUK` | `PRUK:0.0.0` — a placeholder, not a real schema |

!!! danger "`x-partner-context: CRUK` fails on every read today"
    ```bash
    curl -s -H 'x-partner-context: CRUK' \
      "https://api.dev.hdruk.cloud/api/v2/datasets/2187"
    ```

    ```json
    {
      "message": "failed to translate",
      "details": "{\"message\":\"Cannot support the output model (CRUK:1.1.0)\", …}"
    }
    ```

    The config points at CRUK **1.1.0**. `schemata` and TRASER only publish CRUK
    **1.0.0**, so the partner default asks for a schema that does not exist.

    **Workaround:** pass the schema explicitly and skip the partner default —
    `?schema_model=CRUK&schema_version=1.0.0` returns 200.

    This is a configuration defect the Gateway team owns, not something you can
    fix from the client. Detail in
    [the version matrix](../reference/version-matrix.md#where-the-numbers-diverge-and-why).

There is also `allow_cross_context_read`, on by default: the HDRUK operator
context sees datasets belonging to **all** partners, while a partner context sees
only its own. So a dataset that 404s under a partner context may exist and simply
belong elsewhere.

---

## `x-gwdm-version`

This one is a different concern from the other three, and conflating them causes
real confusion.

The other three controls choose **what shape you are given**. `x-gwdm-version`
chooses **which stored representation is read or written**. It does not translate
anything.

### On writes

Selects the GWDM version the incoming metadata is stored as. It never fails: an
unrecognised value silently falls back to the system default
(`GWDM_CURRENT_VERSION`, currently `2.0`). That is deliberate — the header is
resolved by middleware on *every* request, so throwing would 500 unrelated
requests over a stray header.

### On reads

Selects the stored dataset **version row** whose GWDM version matches. Three
outcomes, all verified against production:

=== "Match"

    ```bash
    curl -s -o /dev/null -w '%{http_code}\n' \
      -H 'x-gwdm-version: 2.1' \
      "https://api.dev.hdruk.cloud/api/v2/datasets/2187"
    # 200
    ```

    Dataset 2187 on the development environment is stored at GWDM 2.1, so this
    returns it.

=== "No such stored version"

    ```bash
    curl -s -H 'x-gwdm-version: 2.0' \
      "https://api.dev.hdruk.cloud/api/v2/datasets/2187"
    ```

    ```json
    { "message": "No dataset version found with GWDM version '2.0'." }
    ```

    HTTP **404**. Same dataset, asking for a version it does not have. The
    Gateway will **not** translate 2.1 down to 2.0 to satisfy you — this is
    row selection, not conversion.

=== "Unsupported value"

    ```bash
    curl -s -H 'x-gwdm-version: 9.9' \
      "https://api.healthdatagateway.org/api/v2/datasets/868"
    ```

    ```json
    { "message": "Unsupported GWDM version '9.9'. Supported versions: 2.0, 2.1." }
    ```

    HTTP **400** — and the message enumerates what production supports, which is
    the fastest way to check whether GWDM 2.2 has shipped.

!!! warning "Reads 400 on a bad value; writes do not. And v1 ignores it entirely"
    The write path (`targetVersion()`) never throws and falls back to the
    default. The read path (`requestedVersion()`) throws, and the v2 controller
    turns that into a 400.

    So the *same* invalid header value is a silent fallback on a write and a hard
    400 on a read — and on `/api/v1/datasets/{id}` it is ignored in both
    directions, returning 200 with the newest stored version. That asymmetry is
    intentional but it looks like a bug from the outside, so it is worth knowing
    before you report one.

    Production reports `Supported versions: 2.0, 2.1`. The `2.2` handler exists
    on a feature branch; `x-gwdm-version: 2.2` will 400 until that releases.

---

## What you get if you set nothing

The two endpoints differ, and this is the difference most likely to surprise you
when migrating from v1 to v2.

=== "`/api/v1/datasets/{id}`"

    The **stored GWDM, untranslated**. Top-level metadata blocks:

    ```text
    accessibility  coverage  demographicFrequency  linkage  observations
    omics  provenance  required  structuralMetadata  summary
    tissuesSampleCollection
    ```

    The version wrapper carries three keys — `gwdmVersion`, `metadata` and
    `original_metadata` — so you can see the storage version and the payload as
    originally submitted alongside the cleaned one.

=== "`/api/v2/datasets/{id}`"

    **Translated to HDRUK 4.0.0** — the `HDRUK` partner default. Top-level
    blocks:

    ```text
    accessibility  coverage  demographicFrequency  documentation
    enrichmentAndLinkage  identifier  issued  modified  observations
    omics  provenance  revisions  structuralMetadata  summary  version
    ```

    Confirmed by posting the response to TRASER's `/find`, which matches
    `HDRUK:4.0.0` and nothing else. The version wrapper carries only `metadata`.

The tells are `required` versus `identifier`, and `linkage` versus
`enrichmentAndLinkage`. If you see `required` you have the GWDM; if you see
`identifier` and `revisions` you have the HDRUK schema.

!!! note "This is why an unparameterised v1 → v2 migration changes your payload"
    Nothing about your request changed and the schema of the response did. If you
    are moving a client from v1 to v2 and want the stored GWDM to keep coming
    back, ask for it: `?schema_model=GWDM&schema_version=2.0`.

---

## Which output schemas actually work

Verified against `https://api.healthdatagateway.org/api/v1/datasets/868`:

| `schema_model` / `schema_version` | Status | Note |
|---|:-:|---|
| *(none)* | 200 | stored GWDM on v1, HDRUK 4.0.0 on v2 |
| `GWDM` / `2.0` | 200 | |
| `HDRUK` / `3.0.0` | 200 | |
| `HDRUK` / `4.0.0` | 200 | the recommended output |
| `HDRUK` / `4.1.0` | 200 | **now complete and deployed** (re-checked 2026-09-21) |
| `SchemaOrg` / `GoogleRecommended` | 200 | the working schema.org output |
| `SchemaOrg` / `default` | **400** | broken route |
| `SchemaOrg` / `BioSchema` | **400** | broken route |
| `CRUK` / `1.0.0` | 200 | |

!!! danger "schema.org `default` and BioSchema are unavailable for every dataset"
    ```bash
    curl -s "https://api.healthdatagateway.org/api/v1/datasets/868?schema_model=SchemaOrg&schema_version=BioSchema"
    ```

    ```json
    {
      "message": "failed to translate",
      "details": {
        "traser_message": {
          "message": "Failed to execute translation between GWDM:1.2 and GWDM:1.1",
          "details": []
        },
        "wasTranslated": false,
        "metadata": null,
        "statusCode": 500
      }
    }
    ```

    Neither has an inbound translation edge from GWDM 2.x, so the only route runs
    `GWDM 2.0 → 1.2 → 1.1 → SchemaOrg` and the middle hop is broken. Note the
    inner `statusCode: 500` — that is our fault, not a problem with your request.

    `GoogleRecommended` is unaffected: it has a direct `GWDM:2.0` edge.
    [Full detail](../reference/translation-graph.md#the-broken-hop).

To find out what is routable rather than guessing, ask TRASER:

```bash
TRASER=https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app

curl -s "$TRASER/list/translations?schema=GWDM&version=2.0" | jq -r '.[]'
```

A destination absent from that list is unreachable, and no combination of headers
will produce it.

## When no route exists

The Gateway forwards TRASER's refusal inside a `traser_message`:

```json
{
  "message": "failed to translate",
  "details": {
    "traser_message": {
      "error": "Translation not found",
      "message": "Request failed with status code 404",
      "details": "Translation for GWDM-1.1 to HDRUK-2.2.3 is not implemented"
    },
    "wasTranslated": false,
    "metadata": null,
    "statusCode": 400
  }
}
```

Read the **inner** message. The outer `"failed to translate"` only tells you
which stage failed. `statusCode` inside `details` is the one that says whose
fault it is: 400 means your request, 500 means a map failed.

## Choosing, in one table

| I want… | Send |
|---|---|
| the public HDRUK schema | `?schema_model=HDRUK&schema_version=4.0.0` |
| exactly what is stored | `?schema_model=GWDM&schema_version=2.0`, or call `/api/v1/` with nothing |
| something search engines index | `?schema_model=SchemaOrg&schema_version=GoogleRecommended` |
| to set it once for a whole client | `x-schema-model` / `x-schema-version` headers, on `/api/v2/` |
| a specific stored GWDM version | `x-gwdm-version`, on `/api/v2/` — and expect a 404 if it is not stored |

## Next

| | |
|---|---|
| Retrieve a dataset end to end | [Retrieve a dataset](datasets/retrieve.md) |
| What the GWDM is, and why translation loses things | [The GWDM](../schemas/gwdm.md) |
| Every route, and the shortest-path pitfall | [Translation graph](../reference/translation-graph.md) |
| Which versions are deployed | [Version matrix](../reference/version-matrix.md) |
| Every error body | [Error reference](../reference/errors.md) |
