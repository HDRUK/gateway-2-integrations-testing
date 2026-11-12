---
title: Worked example — BioSchema
description: The BioSchema output mapping, and the bug that currently breaks it.
tags:
  - schemas
  - examples
  - jsonata
---

# Worked example — BioSchema

**Applies to:** HDRUK 4.1.0 · GWDM 2.2

!!! warning "Under construction"
    This page is being written as part of the metadata documentation rewrite.
    Owner: plan 08.

## What this page will cover

- The BioSchema output shape and its mapping.
- The `GWDM 1.2 → 1.1` hop returns HTTP 500, and it sits on the only route from GWDM 2.x, so schema.org `default` and BioSchema output are broken for every stored dataset (`LIMITATIONS.md` L7).
- The reproduction, and what a reader should do in the meantime.
