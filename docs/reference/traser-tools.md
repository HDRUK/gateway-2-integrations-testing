---
title: TRASER developer tools
description: The TRASER web UI: playground, schema graph, schema view, results matrix.
tags:
  - reference
  - traser
  - jsonata
---

# TRASER developer tools

**Applies to:** HDRUK 2.0.2 – 4.1.0 · GWDM 1.0 – 2.2

TRASER is not only a JSON API. The same process serves a set of developer pages,
and one of them — the JSONata playground — is by a wide margin the fastest way to
write or debug a translation map. They have never been documented or linked from
anywhere, which is why almost nobody uses them.

!!! danger "Five of these seven pages 404 on the deployed dev service"
    Checked against
    `https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app`:

    | Path | Deployed dev | Reason |
    |---|---|---|
    | `/` | 200 | |
    | `/docs` | 200 | |
    | `/playground` | **404** | dev runs an older build |
    | `/schema-graph` | **404** | " |
    | `/schema-view` | **404** | " |
    | `/results` | **404** | " |
    | `/benchmark` | **404** | " |

    ```bash
    B=https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app
    for p in / /playground /schema-graph /schema-view /results /benchmark /docs; do
      printf "%-16s %s\n" "$p" "$(curl -sL -o /dev/null -w '%{http_code}' "$B$p")"
    done
    ```

    The routes are all declared in `traser/app/routes.ts`; the deployed build
    simply predates them. **Until dev is redeployed, run TRASER locally** — see
    below. Every screenshot-free description on this page was verified against a
    local instance, not inferred from source.

## Running TRASER locally

```bash
git clone https://github.com/HDRUK/traser
cd traser
cp env.example .env
npm install
npm run dev          # http://localhost:3001
```

Two variables in `.env` decide what the instance knows about:

| Variable | Set it to |
|---|---|
| `SCHEMA_LOCATION` | a local clone of [`HDRUK/schemata`](https://github.com/HDRUK/schemata), or its raw GitHub URL |
| `TEMPLATES_LOCATION` | a local clone of [`HDRUK/traser-mapping-files`](https://github.com/HDRUK/traser-mapping-files), or its raw URL |

Anything not starting with `http` is read from disk, so pointing both at local
clones is the setup you want while authoring a map: edit
`maps/…/translation.jsonata`, and the instance picks it up on its next template
refresh without a restart.

A locally-run instance is also ahead of dev in what it can translate — it carries
HDRUK 4.1.0 and the GWDM 2.2 maps. See
[the version matrix](version-matrix.md).

## Who can open what

Four of the pages are gated. TRASER reads a `token` cookie set by the Gateway
when you sign in, so on a deployment sitting behind the Gateway you are already
authenticated; on a local instance you are not, and the gated pages redirect.

| Page | Access | Behaviour when not signed in |
|---|---|---|
| `/` | open | — |
| `/playground` | **open** | — |
| `/docs` | open | — |
| `/schema-graph` | signed-in user | 302 → `/playground` |
| `/schema-view` | signed-in user | 302 → `/playground` |
| `/results` | **admin only** | 302 → `/playground` |
| `/benchmark` | **admin only** | 302 → `/playground` |

Verified by request, not read off the source:

```bash
for p in /playground /schema-graph /schema-view /results /benchmark /docs; do
  printf "%-16s %s\n" "$p" "$(curl -s -o /dev/null -w '%{http_code}' "http://localhost:3001$p")"
done
```

```text
/playground      200
/schema-graph    302
/schema-view     302
/results         302
/benchmark       302
/docs            200
```

Note the redirect target: an unauthenticated request to a gated page lands on the
**playground**, not on an error. If you clicked a link to the schema graph and
found yourself in the playground, that is why.

!!! note "Only send external readers to `/playground` and `/docs`"
    Those two are the ones that work without an HDR UK account. `/results` and
    `/benchmark` are internal tools and are described here for completeness.

---

## `/playground` — the JSONata sandbox

**Give this one your attention.** If you are mapping your own schema to the GWDM,
this is where you will spend your time. It runs JSONata in your browser against
JSON you paste in, so the edit-run loop is instant and nothing is submitted
anywhere.

Three panels: **JSON input** on the left, the **JSONata template** top right, the
**result** bottom right. Each collapses so you can give one of them the screen.

### What it does for you

**Detects the input schema.** Paste a payload, press **Find schema**, and it
calls `/find` and shows you what matched. Everything downstream keys off that
detection, so do it first — the mapping picker is disabled until you have, with
the tooltip *"Detect the input schema first."*

**Filters the mapping list to what is relevant.** **Load mapping…** lists only
the maps whose input side matches your detected schema, so from a GWDM 2.0
payload you see the maps *out of* GWDM 2.0 and not the other 46. Picking one
loads its real JSONata source into the editor — the same text
[`GET /get/map`](traser-api.md#get-getmap) returns, but editable.

**Validates the output as you type.** With a mapping loaded, the result panel
validates against **that mapping's target schema** automatically and shows
`Translated` or `Validation failed` with the AJV errors. This is the part that
makes the playground better than running JSONata locally: you find out that your
`keywords` output is an array where the GWDM wants a delimited string at the
moment you write it, not after an ingest is rejected.

**Tells you when you have diverged.** Edit a loaded map and the chip changes from
the mapping's name to **Custom (modified)** — so you always know whether the
result reflects a real map or your own work in progress.

**Lets you pick the validation target yourself.** In custom-template mode the
**Validate against** picker takes any schema and version, or `No output schema`
to switch validation off. That is how you develop a map for a target that does
not exist yet.

**Loads a real dataset.** **Load dataset…** searches TRASER's local dataset
cache and drops a real Gateway record into the input panel — via
`/get/dataset`, so it is the genuine stored payload with all its awkwardness,
not a tidy example.

**Shares a link.** The **Share** button copies a URL that carries your work:

```text
/playground?tpl=<base64-encoded template>&in=HDRUK:4.0.0&out=GWDM:2.0
```

`tpl` is the base64 of the URL-encoded template, `in` and `out` are
`Schema:version` pairs, and `pid` loads a cached dataset. Paste it to a colleague
and they open your exact state. There is a length cap on `tpl`; an oversized
template is dropped rather than truncated, so check that a shared link really
carried your map before assuming it did.

### Try this

A ten-minute exercise that teaches most of what you need. Use
[`hdruk-4.0.0-rich.json`](../examples/hdruk-4.0.0-rich.json) — remember the
fixture files are captured responses, so paste the contents of `response`, not
the whole file.

1. **Paste it into the input panel** and press **Find schema**. It should detect
   `HDRUK:4.0.0`.
2. **Load mapping…** and pick `HDRUK 4.0.0 → GWDM 2.0`. The editor fills with
   the real map — around 7,800 characters, opening with the helper-function
   definitions.
3. **Look at the result panel.** It should say `Translated`, because that map's
   output does validate against GWDM 2.0. You are now looking at exactly what
   the Gateway would store for this dataset.
4. **Find `$to_str` in the template** and read the four lines that define it.
   Then find `summary.keywords` in the result: an array in the input, a
   `;,;`-delimited string in the output. That single function is responsible for
   the GWDM's list convention, and it is copy-pasted into most of the 57 map
   files.
5. **Break something deliberately.** Change `$to_str($v.summary.keywords)` to
   `$v.summary.keywords` and watch the result panel go from `Translated` to
   `Validation failed` with a `CommaSeparatedValues` type error. That is the same
   error an ingest would have returned, three seconds instead of a round trip.
6. **Fix it, then press Share** and check the URL round-trips your state.

What you have learned by step 5 is the loop for the whole of
[writing a map](../playbooks/write-a-map.md): change the expression, read the
validation error, repeat.

---

## `/schema-graph` — the translation graph, drawn

A Mermaid flowchart of the same graph documented on
[the translation graph](translation-graph.md), rendered live from the current
template list rather than from a snapshot.

Two modes, via the toggle:

- **Full Graph** — every node and edge at once. Useful for orientation, dense at
  46 edges.
- **Paths from schema** — pick a **Source schema** and **Version** and see only
  what is reachable from it. This is the mode you want.

**Download SVG** exports what you are looking at, which is how you get a current
graph into a slide or a ticket without redrawing it.

Reach for this to answer *"can you get from my schema to X?"* — visually, in one
look, rather than by reading route strings. When you need the answer in a script
instead, [`GET /list/translations`](traser-api.md#get-listtranslations) gives you
the same information as text, plus the exact route.

Requires a signed-in user.

---

## `/schema-view` — a schema's structure, drawn

A Mermaid class diagram of one schema and version: blocks, their fields, and the
types. Pick **Schema** and **Version** and it renders; **Download SVG** exports
it.

This is the quickest way to get the shape of the GWDM into your head — far
quicker than reading `schema.json`, and it makes the block structure obvious in a
way a field table cannot. Read it alongside
[the GWDM](../schemas/gwdm.md) and [the field reference](../schemas/gwdm-reference.md),
which give you the same content as prose and as tables respectively.

Types are labelled as `String`, `Number`, `Boolean`, `Array`, `Null`, `Enum` and
`Root`, so an `anyOf: [Thing, null]` block reads as nullable rather than as two
alternatives.

Requires a signed-in user.

---

## `/results` — the pass/fail matrix

!!! hdruk "For HDR UK developers"
    This page documents internal Gateway processes. It is published openly
    but written for the HDR UK engineering team.

Every cached dataset × every schema, one cell each, colour-coded by whether the
translation succeeded and whether its output validated. This is how the team
spots a translation regression across the real corpus rather than one payload at
a time — a broken map shows up as a column going red.

Tabs: **Overview** (pie-chart summary), **Live Results**, **Draft Results**
(counted separately, because DRAFT datasets store the user-supplied form rather
than the cleaned one) and **Log**.

- Click a failed cell for the full TRASER response JSON that produced it.
- Click through from a cell to the playground and it opens with that dataset
  loaded — that is what the `pid` share parameter is for.
- **Refresh All** runs a two-phase background job: sync every ACTIVE and DRAFT
  dataset from the Gateway API, then translate-and-validate each one against
  every schema. It writes progress to disk as it goes, and only one refresh can
  run at a time.

The dataset cache behind it is swept on a TTL, so the matrix reflects a recent
sample of the corpus rather than a stable census. Admin only.

---

## `/benchmark` — translation latency

!!! hdruk "For HDR UK developers"
    This page documents internal Gateway processes. It is published openly
    but written for the HDR UK engineering team.

Runs timed batches of `/translate` calls against a chosen **Gateway API base
URL** and dataset **ID range**, at a configurable **Concurrency**, and reports
**Mean** and **Median** latency per run. Runs are saved, so you can **Compare**
two of them and see per-dataset `Identical` / `Changed` verdicts — which makes it
a regression check on translation *output* as well as on speed.

Completed runs are deleted on a TTL. Admin only.

---

## `/docs` — Swagger UI

Interactive documentation for the JSON endpoints, generated from JSDoc comments
on the route handlers. `/docs` redirects to `/docs/`, so follow redirects.

This is the one gated-free page that works on the deployed dev service, and it is
also the one most likely to mislead you there — the deployed spec is the old
Express service's, documents a `/translations` path that 404s, and omits
`/validate` entirely. [The TRASER API reference](traser-api.md#the-swagger-page)
has the detail.

---

## Which tool for which job

| I am… | Use |
|---|---|
| writing or debugging a JSONata map | [`/playground`](#playground-the-jsonata-sandbox) |
| working out whether a route exists | [`/schema-graph`](#schema-graph-the-translation-graph-drawn), or `/list/translations` in a script |
| trying to understand a schema's shape | [`/schema-view`](#schema-view-a-schemas-structure-drawn) |
| checking whether I broke translation for everyone | [`/results`](#results-the-passfail-matrix) |
| checking whether I made translation slower | [`/benchmark`](#benchmark-translation-latency) |
| looking up an endpoint's parameters | [`/docs`](#docs-swagger-ui), then [the API reference](traser-api.md) |
