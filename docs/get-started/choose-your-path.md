---
title: Which path am I on?
description: Route yourself to the right part of the site in one page.
tags:
  - getting-started
---

# Which path am I on?

Four journeys. Find the sentence that sounds like you.

## "I have metadata in a schema you already support"

You are authoring in HDRUK, or in CRUK, and you want to push datasets to the
Gateway or read them back.

**Your path:**

1. [Key concepts](concepts.md) — ten minutes, and it will save you more
2. [The schema landscape](../schemas/landscape.md) — confirm your schema and
   version are supported in the direction you need
3. [Creating metadata](../schemas/creating-metadata.md) — author the record
4. [Metadata validation](../schemas/validation.md) — check it before you send it
5. [Making an authenticated request](../api/making-an-authenticated-request.md) —
   get a token
6. [Create a dataset](../api/datasets/create.md) — send it

Then [retrieve](../api/datasets/retrieve.md),
[update](../api/datasets/update.md) and [delete](../api/datasets/delete.md) as
you need.

!!! tip "If you would rather we came to you"
    You do not have to push. The Gateway can harvest metadata from an endpoint
    you host, on a schedule — 195 of the datasets on the development instance
    arrived that way. See [federation](../api/gmi/index.md).

## "I want you to accept a schema of my own"

You have a catalogue in a format the Gateway has never seen — an institutional
standard, a bespoke internal shape, or a community profile such as Bioschemas.

**Your path** is [Bring your own schema](../byos/index.md), which is five steps:
[define](../byos/1-define.md) → [publish](../byos/2-publish.md) →
[map](../byos/3-map.md) → [test](../byos/4-test.md) →
[go live](../byos/5-go-live.md).

Read these two first, because they set the constraints everything else works
inside:

- [Key concepts](concepts.md) — and particularly
  [why the GWDM is the bottleneck](concepts.md#the-gwdm-is-the-bottleneck)
- [The GWDM explained](../schemas/gwdm.md) — you are mapping *into* this, so you
  need to see the target

!!! warning "The honest version"
    Bringing your own schema is not a self-service operation. Your schema has to
    be defined in `schemata`, your maps have to be reviewed and merged into
    `traser-mapping-files`, and if you need a field the GWDM does not have, the
    GWDM has to change first. All three are HDR UK-side changes.

    Expect to work with us rather than around us. The documentation is here so
    that conversation starts from a shared understanding.

## "I am an HDR UK developer changing a schema"

You are adding a field, changing an enum, cutting a version, or onboarding a
partner.

**Your path** is the [playbooks](../playbooks/index.md) — one per task, each
listing the repositories to touch, in order, with the verification step:

| Task | Playbook |
|---|---|
| Add a field to a public-facing schema | [Add a field](../playbooks/add-a-field.md) |
| Add a field to the GWDM | [Add a GWDM field](../playbooks/add-a-gwdm-field.md) |
| Change the permitted values of a field | [Change an enum](../playbooks/change-an-enum.md) |
| Cut a new version of an existing schema | [New schema version](../playbooks/new-schema-version.md) |
| Introduce a whole new schema | [New schema](../playbooks/new-schema.md) |
| Write or fix a translation map | [Write a map](../playbooks/write-a-map.md) |
| Onboard a new partner | [New partner](../playbooks/new-partner.md) |

The [Reference](../reference/index.md) section carries the
[architecture](../reference/architecture.md) and an honest
[register of the things that are currently broken](../reference/known-limitations.md).

!!! hdruk "Adding a field is two changes, not one"
    A field on a public-facing schema that has nowhere to live in the GWDM will
    not survive the round trip. [Add a field](../playbooks/add-a-field.md) covers
    both halves; do not do only the visible one.

## "I just want to look something up"

| You want | Page |
|---|---|
| A GWDM field's type, enum or version | [GWDM field reference](../schemas/gwdm-reference.md) |
| A TRASER endpoint's signature | [TRASER API](../reference/traser-api.md) |
| Which versions exist and which are deployed | [Version matrix](../reference/version-matrix.md) |
| Which translations are possible | [Translation graph](../reference/translation-graph.md) |
| What an error message means | [Errors](../reference/errors.md) |
| A JSONata helper function | [JSONata cookbook](../reference/jsonata-cookbook.md) |
| A real payload to work from | [Example payloads](../examples/README.md) |
| A term defined | [Glossary](glossary.md) |

## Still not sure?

Read [key concepts](concepts.md). It is one page, it is the foundation for
everything else, and by the end of it you will know which of the four above you
are.
