---
title: Reference
description: "Look-up material: endpoints, cookbook, version matrix, errors."
tags:
  - reference
---

# Reference

Look-up material. The guides elsewhere on this site explain how to do something;
these pages tell you exactly what a thing is, what it returns, and what its
current state is.

Everything here was verified by making the call. Where a page shows an error
body, that body was produced, not composed.

## The pages

<div class="grid cards" markdown>

-   :material-api: **TRASER API**

    ---

    Every endpoint, with its request shape, its response shape, its parameters
    and its real errors. Also the one place the TRASER base URL is written down.

    [:octicons-arrow-right-24: TRASER API](traser-api.md)

-   :material-tools: **TRASER developer tools**

    ---

    The web UI nobody knows exists: a JSONata playground, the translation graph
    drawn live, a schema class diagram, and the internal test matrix.

    [:octicons-arrow-right-24: Developer tools](traser-tools.md)

-   :material-graph-outline: **Translation graph**

    ---

    Which schema can reach which, the routes it takes, and why the route it
    picks is not always the one you want.

    [:octicons-arrow-right-24: Translation graph](translation-graph.md)

-   :material-table-check: **Schema version matrix**

    ---

    Which versions exist, which are deployed, which have maps — and the three
    cases where those answers disagree.

    [:octicons-arrow-right-24: Version matrix](version-matrix.md)

-   :material-code-braces: **JSONata cookbook**

    ---

    The de-facto helper library every translation map copy-pastes, with a
    canonical version of each function.

    [:octicons-arrow-right-24: JSONata cookbook](jsonata-cookbook.md)

-   :material-alert-circle-outline: **Error reference**

    ---

    Every error the Gateway API and TRASER return, what each one actually means,
    and which of them are configuration problems rather than your mistake.

    [:octicons-arrow-right-24: Errors](errors.md)

-   :material-file-code-outline: **Example payloads**

    ---

    Four real datasets, frozen, each in several schemas — including the two
    translations that currently fail. With the scripts that harvested them.

    [:octicons-arrow-right-24: Example payloads](../examples/README.md)

</div>

## The two base URLs on this site

Stated once each, so that a change is a one-line edit rather than a sweep.

| Service | URL | Where it is defined |
|---|---|---|
| **Gateway API** | `https://api.healthdatagateway.org` | used directly in every sample |
| **TRASER** | a Cloud Run hostname, and a fragile one | [TRASER API](traser-api.md#the-base-url) — **the only page that spells it out** |

Runnable TRASER samples open with `TRASER=…` and use `$TRASER` thereafter, so
changing host means changing one line of a sample rather than sixteen.

`https://api.dev.hdruk.cloud` appears only where a page is specifically about the
development environment.

## Current known breakages

The four things most likely to make you think you have made a mistake when you
have not. Each is a real, reproduced defect the Gateway team owns.

| What | Effect | Detail |
|---|---|---|
| `GWDM 1.2 → 1.1` map returns 500 | schema.org `default` and BioSchema output unavailable for **every** stored dataset | [Translation graph](translation-graph.md#the-broken-hop) |
| CRUK partner default is `1.1.0`, which was never published | every read under `x-partner-context: CRUK` fails | [Version matrix](version-matrix.md#where-the-numbers-diverge-and-why) |
| `HDRUK:datasetv2` has maps but no schema | you can translate *out of* it; you can never validate *against* it | [Version matrix](version-matrix.md#hdrukdatasetv2-has-maps-but-no-schema-permanently) |
| The deployed dev TRASER predates its own UI | five developer pages 404 there | [Developer tools](traser-tools.md) |

## Looking for something else?

| I want… | Go to |
|---|---|
| the fields of the GWDM | [GWDM field reference](../schemas/gwdm-reference.md) |
| to know which schema to author in | [The schema landscape](../schemas/landscape.md) |
| to check my metadata before submitting | [Validating your metadata](../schemas/validation.md) |
| to control what schema I get back | [Choosing your response schema](../api/response-schema.md) |
| a term defined | [Glossary](../get-started/glossary.md) |
