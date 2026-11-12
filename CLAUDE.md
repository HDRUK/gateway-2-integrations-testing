# CLAUDE.md

Guidance for any agent or developer working in
`HDRUK/gateway-2-integrations-testing`.

## What this repo is

The **Gateway metadata & schema documentation site** — an MkDocs-Material site
published to GitHub Pages. It documents how third parties and HDR UK developers
get metadata into and out of the HDR UK Gateway: the GWDM, the HDRUK schema,
partner schemas, TRASER translation, and the Gateway APIs.

It is a documentation repo — no application code, though the root holds a few
example and tutorial assets (`Tutorial.ipynb`, `translation-test.py`,
`example-gwdm20.json`, `example-hdruk300.json`) that published pages link to by
raw GitHub URL. See `OPEN-QUESTIONS.md` Q4 before moving them.

## ⚠️ Read this first: a rewrite programme is live

A staged documentation rewrite is in progress. **Before doing anything in this
repo, read `plans/state/` in full** — all five ledgers:

| File | What it holds |
|---|---|
| `plans/state/PROGRESS.md` | Which of the twelve plans are done, and what they produced |
| `plans/state/FACTS.md` | Verified facts with evidence. **Never re-derive anything here** |
| `plans/state/DECISIONS.md` | Decisions already made, with rationale |
| `plans/state/LIMITATIONS.md` | Known problems found and deliberately not fixed |
| `plans/state/OPEN-QUESTIONS.md` | Blockers awaiting Calum — do not guess these |

Then read **`plans/TRACKS.md`** — it defines the a)/b)/c) split and is the
entry point above everything else — followed by `plans/00-INDEX.md` for the
track a) programme, and the specific plan you have been asked to execute.

A plan is not complete until it has written back to `plans/state/` as directed
by its own Handoff section.

`plans/` is temporary scaffolding, outside `docs/`, and is not published.

## Hard scope rules

1. **HDRUK 5.0.0 and GWDM 3.0 do not exist.** Confirmed by Calum, 2026-09-21.
   They were **committed as removed** on 2026-09-10 (`5521971`), so they are
   not uncommitted drafts you have to guard against either (`FACTS.md` F34,
   L6 closed). Latest is HDRUK **4.1.0** and GWDM **2.2**.
   `DECISIONS.md` D2 keeping them out of scope still stands. Beware stale
   sources: four of the six `../metadata-management/*.md` files still describe
   GWDM 3.0 as current or parked, and one claims it was decomposed into SQL
   tables — which was **never true**.
2. **Latest = HDRUK 4.1.0 and GWDM 2.2 — both COMPLETE and deployed.**
   Confirmed by Calum 2026-09-21 and verified by call (`FACTS.md` **F37**):
   both are in `schemata`, on the deployed TRASER (52 templates), and on
   **production**, which enumerates `Supported versions: 2.0, 2.1, 2.2`.
   Everything from HDRUK 2.0.2 → 4.0.0 and GWDM 1.0 → 2.1 is "supported" and
   keeps working docs.

   > ⚠ **Do not describe either as imminent, in-progress or unpublished.** Many
   > earlier `plans/` and `plans/state/` entries do; F37 lists the four specific
   > claims it retires. The deployed-versus-in-repo gap that used to matter here
   > has closed — the only surviving divergence is the deployed TRASER's **UI
   > routes**, which still 404.
3. **Do not fix code.** This programme documents the system as it is. Record
   problems in `plans/state/LIMITATIONS.md`; add a warning admonition where a
   reader is affected. The Gateway team owns the fixes.
4. **No real PII.** Examples harvested from live APIs must have contact details
   replaced with `Jane Doe` / `user@example.com` / `+44 7700 000000` before they
   land in a page.
5. **British spelling** in prose, headings and identifiers — except where an
   API field name or CSS property demands the American form.
6. **Never commit `.env`** or any credential from any repo you touch.
7. **Do not commit or push** without being asked.

## Sibling repos

All under `/Users/calummacdonald/Software/Gateway2.0/` locally, and public at
`https://github.com/HDRUK/<repo>`.

| Repo | Local path | Role in the metadata pipeline |
|---|---|---|
| `gateway-api-2` | `../gateway-api-2` | Laravel core API. Writes the GWDM to MySQL, calls TRASER on ingest and on read, owns the partner / output-schema / GWDM-version contexts |
| `gateway-web-2` | `../gateway-web-2` | Next.js frontend. Consumes form hydration to build the manual onboarding form |
| `schemata-2` | `../schemata-2` | Pydantic v2 source of truth → generated `schema.json`, `available.json` and docs |
| `traser` | `../traser` | React Router v7 app. The translation JSON API **and** the developer UI (JSONata playground, schema graph, schema view, results matrix, Swagger) |
| `traser-mapping-files` | `../traser-mapping-files` | The `translation.jsonata` map files plus the `available.json` registry |

The pipeline in one line: a partner schema is defined in `schemata-2`, mapped to
the GWDM by JSONata in `traser-mapping-files`, translated by `traser`, stored as
GWDM by `gateway-api-2`, and translated back out to a requested output schema on
read.

## Local commands

```bash
pip install -r requirements.txt
mkdocs serve            # preview at http://127.0.0.1:8000
mkdocs build --strict   # must pass with zero warnings before any PR
```

`mkdocs build --strict` currently passes clean — see `FACTS.md` F15. Keep it
that way. CI now runs it on pull requests, but it is not a required check, so
run it yourself as well.

## Docs conventions

Established by plan 03. `DECISIONS.md` D9–D11 carry the rationale; the page
ownership map is `FACTS.md` F25.

### Directory layout

| Directory | Tab | Audience |
|---|---|---|
| `docs/get-started/` | Get started | both |
| `docs/api/` | Gateway APIs | external |
| `docs/schemas/` | Metadata & schemas | both |
| `docs/byos/` | Bring your own schema | external |
| `docs/playbooks/` | Playbooks | both, and agents |
| `docs/reference/` | Reference | both |
| `docs/examples/` | linked from Reference | frozen fixtures, not prose |

Every page carries front matter:

```yaml
---
title: <Page Title>
description: <one line>
tags: [<from the controlled list below>]
---
```

Tags in use: `getting-started`, `api`, `auth`, `datasets`, `gmi`, `schemas`,
`gwdm`, `hdruk-schema`, `partner`, `traser`, `jsonata`, `playbook`,
`reference`, `examples`. Add a new one only if it will apply to more than one
page. The `internal` tag is **retired** — see convention 1.

### The convention snippets

Use these **verbatim** — identical wording everywhere is the point.

**1. ~~Internal pages.~~ RETIRED 2026-09-21 — there is no internal section.**

`docs/internal/` has been **withdrawn from the published site**
(`DECISIONS.md` **D17**). Internal audience now means internal distribution:
tracks b) and c) live in the gitignored `internal-notes/`, bound for Confluence.
See `plans/TRACKS.md`.

Two of its pages were kept as public reference, because they describe how the
system works *today* rather than how it should: `reference/architecture.md` and
`reference/known-limitations.md`. **A known bug is still a fact** — it belongs
on the public site with a warning admonition, not hidden. Do not move candid
content off the site; `OPEN-QUESTIONS.md` Q3 settled that.

**2. Version applicability.** Every schema-specific page carries a line
immediately under the `#` heading:

```markdown
**Applies to:** HDRUK 4.1.0 · GWDM 2.2
```

Use a range where a page covers several: `**Applies to:** HDRUK 2.0.2 – 4.1.0`.
This convention is what the site does *instead* of versioned docs (Q5).

**3. ~~Unverified GWDM 2.2 content.~~ RETIRED 2026-09-21 — do not use.**

GWDM 2.2 **has landed**. It is defined in `schemata/available.json` and served
by the deployed dev TRASER (`FACTS.md` F36), which closes `LIMITATIONS.md` L1
and `OPEN-QUESTIONS.md` Q1. The old "not yet published" admonition was removed
from all 11 pages that carried it, and from the generator that emits
`docs/schemas/gwdm-reference.md`.

What still needs saying on 2.2 pages is narrower, and is **not** a blanket
warning: `maps/GWDM/2.2/HDRUK/4.1.0/` was built by copying the 2.0-targeted map
and adding two DUO fields, so it emits 2.0's fields plus DUO and **not** the
five sections 2.1 added. `docs/schemas/gwdm.md` already states this correctly —
follow that page's wording rather than inventing a new admonition.

**4. Deprecation.**

```markdown
!!! danger "Being deprecated"
    This mechanism is on its way out. Document it, do not build on it.
```

⚠ **Do not apply convention 4 to form hydration.** `LIMITATIONS.md` L2's own
correction withdraws it: "being deprecated" is not established, and Calum is
actively reworking 4.1.0, 2.2 and form hydration. Use
`!!! warning "Actively being reworked"` there instead.

### Hosts and base URLs

The site currently carries two API hosts and 16 copies of one Cloud Run
hostname. One of each from now on:

- **Gateway API:** `https://api.healthdatagateway.org` in every sample. Mention
  `https://api.dev.hdruk.cloud` only where a page is specifically about the dev
  environment.
- **TRASER:** the base URL is stated **once**, on `reference/traser-api.md`.
  Other pages link to it rather than repeating it. Runnable samples open with
  `TRASER=https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app` and use
  `$TRASER` thereafter, so a reader changes one line, not sixteen. The
  hostname is fragile (`FACTS.md` F23) — never bury it in prose.

### Fixtures, snippets and code fences

Frozen fixtures live in `docs/examples/` (`DECISIONS.md` D8). Include them
rather than inlining payloads — `pymdownx.snippets` has `base_path: ["docs"]`,
so paths are relative to `docs/`:

````markdown
```json title="gwdm-2.0-minimal.json"
--8<-- "examples/gwdm-2.0-minimal.json"
```
````

`check_paths: true` is on, so a wrong path fails the build rather than
silently emitting the literal text.

Always give a fence a language (` ```bash `, ` ```json `, ` ```python `).
Several existing pages use bare fences; fix that as you rewrite a page, not
before. Multi-language samples use `=== "Python"` / `=== "cURL"` tabs.

Diagrams are mermaid, in a ` ```mermaid ` fence — rendered natively, no plugin.

### Stubs

A page that is scaffolded but not yet written carries:

```markdown
!!! warning "Under construction"
    This page is being written as part of the metadata documentation rewrite.
    Owner: plan NN.
```

Naming the owning plan means a later session can find its work without reading
all twelve plans. Delete the admonition when the page is written; plan 12
treats any surviving one as an incomplete deliverable.

## Contributing

- Branch from `master`. Working branch for the rewrite programme: see
  `DECISIONS.md` D7.
- `master` is protected: **one** approving review required, conversation
  resolution required, no force-pushes, admins included. There are **no
  required status checks** — a red pipeline will not block a merge, so verify
  `mkdocs build --strict` locally.
- Tickets are `GAT-NNNN`.
- CI (`.github/workflows/ci.yml`) runs `mkdocs build --strict` on every pull
  request and on pushes to `master`, and runs `mkdocs gh-deploy --force` only on
  a push to `master`. Pushing any other branch no longer publishes the site
  (`OPEN-QUESTIONS.md` Q6, fixed 2026-11-12).
