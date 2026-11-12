---
title: Retrieve a dataset
description: GET a dataset back from the Gateway in the schema of your choice.
tags:
  - api
  - datasets
  - schemas
---

# Retrieve a dataset

**Applies to:** HDRUK 2.0.2 – 4.1.0 · GWDM 1.0 – 2.2

There are two ways to read a dataset back, and the one you want depends on
whether you need credentials.

| Endpoint | Auth | Use it for |
|---|:-:|---|
| `GET /api/v1/datasets/{id}` | **no** | reading published metadata — anyone's |
| `GET /api/v2/datasets/{id}` | **no** | the same, translated to HDRUK 4.0.0 by default |
| `GET /api/v1/integrations/datasets/{id}` | **yes** | reading back what *your* integration posted |

!!! tip "You probably do not need to authenticate"
    Reading published dataset metadata needs no private app. The public paths
    return 200 with no headers at all. Use the integrations path when you want
    the integration's own view — including DRAFT records, which are not public.

## The public read

=== "cURL"

    ```bash
    curl -s "https://api.healthdatagateway.org/api/v1/datasets/868"
    ```

=== "Python"

    ```python
    import requests

    API = "https://api.healthdatagateway.org/api/v1"

    response = requests.get(f"{API}/datasets/868", timeout=60)
    dataset = response.json()["data"]
    print(dataset["status"], dataset["pid"])
    ```

## The authenticated read

Use this for the dataset your integration created. It takes the two private-app
headers — see [making an authenticated request](../making-an-authenticated-request.md).

=== "cURL"

    ```bash
    curl -s "https://api.healthdatagateway.org/api/v1/integrations/datasets/<dataset_id>" \
      --header "x-application-id: <YOUR_APP_ID>" \
      --header "x-client-id: <YOUR_CLIENT_ID>"
    ```

=== "Python"

    ```python
    import requests

    API = "https://api.healthdatagateway.org/api/v1"
    headers = {
        "x-application-id": "<YOUR_APP_ID>",
        "x-client-id": "<YOUR_CLIENT_ID>",
    }

    response = requests.get(
        f"{API}/integrations/datasets/<dataset_id>", headers=headers, timeout=60
    )
    print(response.json()["message"])
    ```

## What comes back

The envelope is `{"message": "success", "data": {…}}`. `data` carries around
forty keys — Gateway bookkeeping, relationship counts, the team, and the version
history. The metadata itself is nested three deep.

```json
{
  "message": "success",
  "data": {
    "id": 868,
    "pid": "95cd1eac-59b5-4cb2-9c08-0b8a9067c760",
    "datasetid": "16f996e8-1cba-4f2a-b6aa-2fbf3456ea8a",
    "status": "ACTIVE",
    "create_origin": "GMI",
    "partner_context": "HDRUK",
    "team": { "…" },
    "collections": [], "durs": [], "publications": [], "tools": [],
    "linkages": { "…" },
    "versions": [
      {
        "id": 1234,
        "version": 1,
        "gwdm_version": "2.0",
        "title": "Diagnostic Imaging Dataset",
        "patch": { "…" },
        "metadata": {
          "gwdmVersion": "2.0",
          "metadata":          { "…the cleaned, stored record…" },
          "original_metadata": { "…exactly what was submitted…" }
        }
      }
    ]
  }
}
```

### The path to the metadata

`data.versions[0].metadata.metadata` — and yes, `metadata.metadata` is real. The
outer `metadata` is a wrapper with three keys:

| Key | What it is |
|---|---|
| `metadata` | the **stored GWDM** record, after translation and Gateway-side mutation |
| `original_metadata` | the payload **as submitted**, before translation |
| `gwdmVersion` | which GWDM version the stored record is in |

`original_metadata` is the useful one when debugging an ingest: it is what you
sent, so a diff against `metadata` shows exactly what translation did.

`versions` is ordered **newest first**, so `versions[0]` is current. Each row
also carries `gwdm_version` and a `patch` — the RFC 6902 delta from the previous
version — alongside the full snapshot.

!!! danger "`required.version` is the dataset's version, not the schema's"
    ```json
    "required": {
      "gatewayId": "868",
      "gatewayPid": "95cd1eac-59b5-4cb2-9c08-0b8a9067c760",
      "issued": "2024-10-08T11:32:38.745215Z",
      "modified": "2024-10-08T11:32:38.745231Z",
      "version": "7.0.0",
      "revisions": [
        { "url": "https://web.prod.hdruk.cloud//dataset/868?version=1.0.0", "version": "1.0.0" }
      ]
    }
    ```

    That `"version": "7.0.0"` is dataset 868's own semantic version — it has been
    revised seven times. It is **not** a schema version, and there is no HDRUK or
    GWDM 7.0.0.

    Earlier versions of this page showed `"version": "3.0.0"` here, which looked
    exactly like a schema version and was read as one. For the schema version,
    use `gwdmVersion` on the wrapper, or `gwdm_version` on the version row.

    Note also the `//` in that revisions URL. It is in the stored data.

## Getting a different schema back

Four controls decide the response schema, and which of them work depends on the
endpoint. Two examples here; the complete behaviour, with the verification, is on
[choosing your response schema](../response-schema.md).

### The public HDRUK schema

```bash
curl -s "https://api.healthdatagateway.org/api/v1/datasets/868?schema_model=HDRUK&schema_version=4.0.0"
```

```json
{ "message": "success", "data": { "…" } }
```

The metadata under `data.versions[0].metadata.metadata` is now HDRUK 4.0.0 —
`identifier`, `documentation`, `enrichmentAndLinkage`, `revisions` — rather than
the GWDM's `required`, `summary`, `linkage`.

**HDRUK 4.0.0 is the version to ask for.** 4.1.0 exists in the schema repository
but is not deployed on production or on dev:

```bash
curl -s "https://api.healthdatagateway.org/api/v1/datasets/868?schema_model=HDRUK&schema_version=4.1.0"
```

```json
{
  "message": "failed to translate",
  "details": {
    "traser_message": { "message": "Cannot support the output model (HDRUK:4.1.0)", "details": {} },
    "wasTranslated": false, "metadata": null, "statusCode": 400
  }
}
```

### schema.org for search engines

```bash
curl -s "https://api.healthdatagateway.org/api/v1/datasets/868?schema_model=SchemaOrg&schema_version=GoogleRecommended"
```

```json
{
  "@context": "https://schema.org/",
  "@id": "https://hdruk.ac.uk",
  "@type": "Dataset",
  "url": "https://hdruk.ac.uk/868",
  "name": "Diagnostic Imaging Dataset",
  "alternateName": "Diagnostic Imaging Dataset",
  "description": "The DID is a monthly collection of information about diagnostic imaging tests carried out on NHS patients in England …",
  "keywords": "…",
  "license": "…",
  "isAccessibleForFree": true
}
```

!!! danger "BioSchema and schema.org `default` do not work"
    Earlier versions of this page showed a **successful** BioSchema response. It
    fails today, for every one of the stored datasets:

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
        "wasTranslated": false, "metadata": null, "statusCode": 500
      }
    }
    ```

    Neither has a translation route from GWDM 2.x that does not cross a broken
    map. `GoogleRecommended` is unaffected because it has a direct edge.
    [Full detail](../../reference/translation-graph.md#the-broken-hop).

Both parameters are required together. To see what is routable before you ask:

```bash
TRASER=https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app

curl -s "$TRASER/list/translations?schema=GWDM&version=2.0" | jq -r '.[]'
```

## Listing datasets

```bash
curl -s "https://api.healthdatagateway.org/api/v1/datasets?per_page=1"
```

A standard Laravel paginator — `current_page`, `data`, `total`, `links`,
`per_page`. Statuses you will see are `ACTIVE`, `DRAFT` and `ARCHIVED`. Public,
no credentials.

## Errors

Every body here was produced by making the call. The complete catalogue is
[the error reference](../../reference/errors.md).

### The dataset id does not exist

Note this is a **400**, not a 404, and it is a different shape from the other
errors on this page:

```json
{
  "status": "INVALID_ARGUMENT",
  "message": "Invalid argument(s)",
  "errors": [
    { "reason": "EXISTS", "message": "The selected id is invalid.", "field": "id" }
  ]
}
```

### The dataset existed and was deleted

```json
{ "code": 500, "message": "Dataset with id=<dataset_id> cannot be found" }
```

### No credentials, or credentials that do not match

```json
{ "code": 401, "message": "Unauthorized" }
```

```json
{ "code": 401, "message": "No known integration matches the credentials provided" }
```

The first means the headers were absent; the second means they arrived and
matched nothing. Re-copy them from
`Integrations > API Management > Manage API > Authentication`.

### The app cannot see this dataset

```json
{ "code": 400, "message": "Application permissions do not allow this request" }
```

Valid credentials, wrong team. A private app can only act on its own team's
datasets.

### `schema_model` without `schema_version`

```json
{ "code": 500, "message": "You have given a schema_model but not a schema_version" }
```

All-or-nothing. A 500 for a client mistake is misleading — it is your request.

### An output schema that does not exist

```json
{
  "message": "failed to translate",
  "details": {
    "traser_message": {
      "error": "Translation not found",
      "message": "Request failed with status code 404",
      "details": "Translation for GWDM-1.1 to HDRUK-2.2.3 is not implemented"
    },
    "wasTranslated": false, "metadata": null, "statusCode": 400
  }
}
```

Read the **inner** message; the outer one only says which stage failed. The
versions it names are the failing **hop**, which may be neither of the ones you
asked for — the example above starts from a `GWDM:1.1` intermediate, not from the
stored `GWDM:2.0`.

`statusCode` inside `details` is what tells you whose problem it is: **400 means
your request** (a schema that does not exist, or no route), **500 means a map
failed** and is ours.

Check [the version matrix](../../reference/version-matrix.md#the-matrix) for what
is deployed.

## Next

| | |
|---|---|
| All four response-schema controls | [Choosing your response schema](../response-schema.md) |
| What the stored GWDM record contains | [The GWDM](../../schemas/gwdm.md) |
| Real payloads in four schemas side by side | [Worked examples](../../schemas/examples.md) |
| Update or delete | [Update](update.md) · [Delete](delete.md) |
