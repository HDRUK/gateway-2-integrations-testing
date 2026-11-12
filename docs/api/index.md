---
title: Gateway APIs
description: Authenticate, then create, read, update and delete dataset metadata.
tags:
  - api
---

# Gateway APIs

The Gateway's REST API is how you get dataset metadata in and out programmatically
instead of through the web onboarding form. Everything here is about the **Gateway
API**. The separate translation service, TRASER, is documented under
[Reference](../reference/traser-api.md).

## The host

Every sample on this site uses:

```text
https://api.healthdatagateway.org
```

`https://api.dev.hdruk.cloud` appears only where a page is specifically about the
development environment. If you are integrating, build against production and
test against dev — but be aware they hold different data, and dev in particular
carries a lot of test records.

Interactive Swagger documentation:
[api.healthdatagateway.org/api/documentation](https://api.healthdatagateway.org/api/documentation#/).

## Read this in order

If you are starting from nothing, the first three pages are prerequisites for
everything after them.

<div class="grid cards" markdown>

-   :material-login: **1. Sign in to the Gateway**

    ---

    You need a Gateway account and membership of a team before you can create
    credentials.

    [:octicons-arrow-right-24: Sign in](fe-login.md)

-   :material-key-variant: **2. Get a private app**

    ---

    A private app is your API credential. It belongs to one team and carries an
    App ID and a Client ID.

    [:octicons-arrow-right-24: What it is](private-app-what.md) ·
    [Create](private-app-create.md) ·
    [Manage](private-app-manage.md)

-   :material-shield-key: **3. Make an authenticated request**

    ---

    The two headers every authenticated call needs, with samples.

    [:octicons-arrow-right-24: Authenticated requests](making-an-authenticated-request.md)

-   :material-database-edit: **4. Work with datasets**

    ---

    The CRUD operations on dataset metadata.

    [:octicons-arrow-right-24: Create](datasets/create.md) ·
    [Retrieve](datasets/retrieve.md) ·
    [Update](datasets/update.md) ·
    [Delete](datasets/delete.md)

</div>

## Then, when you need them

<div class="grid cards" markdown>

-   :material-swap-horizontal: **Choosing your response schema**

    ---

    Four different controls decide which schema you get back, and they do not
    all work on every endpoint.

    [:octicons-arrow-right-24: Response schema](response-schema.md)

-   :material-lan-connect: **Federation (GMI)**

    ---

    Have the Gateway pull metadata from an endpoint you host, rather than pushing
    it to us.

    [:octicons-arrow-right-24: Federation](gmi/index.md)

</div>

## What needs authentication and what does not

This catches people out in both directions — they authenticate reads that need no
credentials, and are surprised when writes are rejected.

| Endpoint | Auth | Notes |
|---|:-:|---|
| `GET /api/v1/datasets` | **no** | public listing, standard Laravel paginator |
| `GET /api/v1/datasets/{id}` | **no** | returns the stored GWDM by default |
| `GET /api/v2/datasets/{id}` | **no** | returns HDRUK 4.0.0 by default |
| `GET /api/v1/integrations/datasets/{id}` | **yes** | the integration read path |
| `POST` / `PUT` / `DELETE` on `integrations/datasets` | **yes** | all writes |

Verified: an unauthenticated request to the integrations path returns

```json
{ "code": 401, "message": "Unauthorized" }
```

while the public read paths return 200 with no headers at all. So if you only
need to *read* published metadata, you do not need a private app.

## The two API versions

There are two dataset read endpoints and they behave differently even with no
parameters set:

| | `/api/v1/datasets/{id}` | `/api/v2/datasets/{id}` |
|---|---|---|
| Default response schema | the stored **GWDM** | translated to **HDRUK 4.0.0** |
| `?schema_model` / `?schema_version` | honoured | honoured, and beats the headers |
| `x-schema-model` / `x-schema-version` | **ignored** | honoured |
| `x-gwdm-version` | **ignored** | honoured |
| Version wrapper keys | `gwdmVersion`, `metadata`, `original_metadata` | `metadata` |

**Migrating a client from v1 to v2 changes the schema of your payload** even
though nothing about your request changed. Full detail, with the verification, on
[choosing your response schema](response-schema.md#first-which-endpoint-are-you-calling).

## Response envelopes

Successful responses are wrapped:

```json
{ "message": "success", "data": { "…" } }
```

Errors come in **two** shapes, which is worth knowing before you write a handler:

=== "Application errors"

    ```json
    { "code": 401, "message": "No known integration matches the credentials provided" }
    ```

=== "Validation errors"

    ```json
    {
      "status": "INVALID_ARGUMENT",
      "message": "Invalid argument(s)",
      "errors": [
        { "reason": "EXISTS", "message": "The selected id is invalid.", "field": "id" }
      ]
    }
    ```

And a translation failure nests the real error one level deeper again, under
`details.traser_message`. Every body you can receive, and what to do about each,
is on [the error reference](../reference/errors.md).

!!! note "A nonexistent dataset is a 400, not a 404"
    `GET /api/v1/datasets/99999999` returns HTTP **400** with the validation
    shape above. Verified on both v1 and v2. If you are switching on status codes,
    do not expect 404.

## Before you send anything

Validate against TRASER first. It needs no credentials, gives you the complete
error list rather than the first problem, and will tell you both what the Gateway
would store and what your consumers would receive:

[:octicons-arrow-right-24: Validating your metadata](../schemas/validation.md)
