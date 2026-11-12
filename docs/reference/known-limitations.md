---
title: Known limitations
description: Problems in the metadata pipeline that are known, recorded and not yet fixed.
tags:
  - reference
---

# Known limitations

!!! warning "Under construction"
    This page is being written as part of the metadata documentation rewrite.
    Owner: plan A.

## What this page will cover

The reader-facing subset of `plans/state/LIMITATIONS.md` — problems that change
what a reader should expect, stated plainly.

- The broken `GWDM 1.2 → 1.1` hop, which kills schema.org and BioSchema output (L7).
- Form hydration's missing `4.1.0.form.json` (L8).
- The CRUK partner context failing on every read (L17).
- The GMI test server page cannot currently be followed successfully (L11).

!!! note "Closed since this stub was written"
    GWDM 2.2 **is** now defined in `schemata` and served by the deployed TRASER
    (`FACTS.md` F36), so L1 is closed. Do not carry it onto this page.
