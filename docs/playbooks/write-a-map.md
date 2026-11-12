---
title: Write a JSONata translation map
description: Author, test and register a translation map.
tags:
  - playbook
  - jsonata
---

# Write a JSONata translation map

**Applies to:** HDRUK 2.0.2 – 4.1.0 · GWDM 1.0 – 2.2

!!! warning "Under construction"
    This page is being written as part of the metadata documentation rewrite.
    Owner: plan 07.

    The steps below were drafted by plan 06 and are accurate. Plan 07 owns the
    final format pass so that every playbook shares one shape.

The condensed runbook. The teaching version is
[Write your JSONata maps](../byos/3-map.md); the function library is
[the cookbook](../reference/jsonata-cookbook.md).

## Preconditions

- The input and output schemas both exist in
  [`HDRUK/schemata`](https://github.com/HDRUK/schemata) and appear in
  `GET /list/schemas`. A map to a schema TRASER cannot load will fail output
  validation on every call.
- You can push a branch to
  [`HDRUK/traser-mapping-files`](https://github.com/HDRUK/traser-mapping-files).
- A local TRASER, for testing before the map is merged — see
  [Running TRASER locally](../reference/traser-tools.md#running-traser-locally).
- At least two sample documents in the input schema: one rich, one minimal.

## Steps

### 1. Decide the direction and the path

```text
maps/{OutputModel}/{outputVersion}/{InputModel}/{inputVersion}/translation.jsonata
```

The **output comes first**. Write the path down before you start; getting it
backwards is the most common mistake, and the symptom is a map that appears to
be ignored.

**Verify:** read the path back as a sentence — "converts *{InputModel}
{inputVersion}* into *{OutputModel} {outputVersion}*".

### 2. Check whether a route already exists

```bash
TRASER=https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app
curl -s "$TRASER/list/translations?schema=GWDM&version=2.0"
```

TRASER chains maps via a shortest-path search, so a direct map may not be
needed — but every edge has weight 1, so a new direct map **will** be preferred
over an existing longer chain. Adding one changes routing for existing callers.

**Verify:** you can state which routes your new edge will short-circuit.

### 3. Draft the expression in the playground

Open `/playground` on a local instance, paste one sample document, and build the
map incrementally — one target block at a time, checking the output after each.

Copy helper functions from [the cookbook](../reference/jsonata-cookbook.md),
not from a neighbouring map: eight of the shared helpers have drifted between
copies and the one you open may be an outdated variant.

**Verify:** the expression evaluates without error and the output looks right
for both sample documents.

### 4. Handle the four traps

- **Explicit nulls.** `$exists(null)` is `true`. Guard with
  `($exists($x) and $x != null)` wherever the input may carry a JSON `null`,
  or the translation returns HTTP 500.
- **Single-element arrays** collapse to bare values. Wrap in `[ ]` anything the
  target schema types as an array.
- **`0` is falsy.** Test for it explicitly where it is a legitimate value.
- **GWDM list fields** are `';,;'`-joined strings, and unknown numerics are
  `-1`. Do not emit `summary.publisher` or the `required` block — the API
  overwrites both.

**Verify:** the minimal sample, with keys set to `null` rather than omitted,
still translates.

### 5. Save the file and regenerate the registry

```bash
cd traser-mapping-files
# save your map at the path from step 1
python utils/list_maps.py     # rescans maps/** and rewrites available.json
```

A map missing from `available.json` is invisible to TRASER.

**Verify:** `git diff available.json` shows your new edge.

### 6. Test against a local TRASER

Point `TEMPLATES_LOCATION` at your clone, then:

```bash
curl -s -X POST "http://localhost:3001/translate?input_schema={In}&input_version={v}&output_schema={Out}&output_version={v}" \
  -H 'Content-Type: application/json' --data '{"metadata": { … }}'
```

**Verify:** HTTP 200 for both samples with output validation on (the default).
A 400 names the failing fields; a 500 means the expression threw.

### 7. Test the round trip

If the reverse map exists, translate out and back and compare against the
original.

**Verify:** you can account for every field that changed. Some loss is expected
— `$to_str` turns `null` into `""`, and enum values outside the allow-list are
dropped silently — but each instance should be a decision, not a surprise.

### 8. Open the pull request

Commit the map **and** the regenerated `available.json` together. Branch
`dev` → development, `preprod` → pre-production, `master` → production; a push
uploads the repository to the environment's bucket, and the running TRASER
picks it up from there.

**Verify:** the PR describes which routes the new edge changes, and states any
helper function you altered relative to the cookbook.

## Acceptance criteria

- [ ] The file is at the output-first path, and the direction is stated in the PR
- [ ] `available.json` is regenerated and committed in the same commit
- [ ] Both samples translate with HTTP 200 and output validation enabled
- [ ] A document with explicit `null`s translates without a 500
- [ ] Array-typed target fields are array-wrapped, tested with a one-element input
- [ ] Helper functions match the cookbook, or the divergence is called out
- [ ] The routes the new edge short-circuits are named
