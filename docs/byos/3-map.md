---
title: 3. Write your JSONata maps
description: Map your schema to the GWDM, and the GWDM back to your schema.
tags:
  - jsonata
  - schemas
  - partner
---

# 3. Write your JSONata maps

**Applies to:** HDRUK 2.0.2 – 4.1.0 · GWDM 1.0 – 2.2

By this point your schema is defined ([step 1](1-define.md)) and published
([step 2](2-publish.md)). This step is the one that makes it usable: a pair of
JSONata templates that convert a document in your schema into the Gateway's
internal model, and back again.

This page assumes no prior JSONata. It builds up to a small but complete map you
can run. Keep [the cookbook](../reference/jsonata-cookbook.md) open alongside it
— that is where the helper functions live.

## What JSONata is, and why we use it

JSONata is a query and transformation language for JSON. A map is a single
expression that takes one JSON document and evaluates to another.

The reason the Gateway uses it, rather than accepting a JavaScript transform, is
that **a map is data, not code**. TRASER fetches your `translation.jsonata` at
runtime from the `traser-mapping-files` repository and evaluates it in a
sandboxed interpreter. It cannot open a socket, read a file, or reach anything
in our infrastructure. That is precisely what makes it safe for us to accept a
map written by a third party, and it is why we will not take a JavaScript
function instead.

The practical consequences for you:

- Everything is an expression. There are no statements and no mutation.
- There is no `import`, so every helper function is defined inline in every map
  that uses it. See [the cookbook](../reference/jsonata-cookbook.md) for the
  canonical bodies to copy.
- There is no I/O. A map can only see what it is handed.

## The binding: `input` and `extra`

Every template is evaluated against exactly one object:

```json
{ "input": { "…your metadata…" }, "extra": { "…supplementary values…" } }
```

So a template refers to `input.summary.title`, never to `summary.title` on its
own. `extra` carries values the caller supplies alongside the document — see
[the TRASER API reference](../reference/traser-api.md) for how it is populated
on a `/translate` call.

!!! danger "Never rename these two"
    `input` and `extra` are hard-coded in TRASER's evaluation call. All 57 maps
    in the repository depend on them.

## Direction, and the output-first path convention

Map files live at:

```text
maps/{OutputModel}/{outputVersion}/{InputModel}/{inputVersion}/translation.jsonata
```

**The output comes first.** This is the single most common early mistake, so
read one out loud before you start:

```text
maps/GWDM/2.2/HDRUK/4.1.0/translation.jsonata
     └──┬──┘ └┬┘ └──┬──┘ └─┬─┘
        │     │     │      └─ input version  4.1.0
        │     │     └──────── input model    HDRUK
        │     └────────────── output version 2.2
        └──────────────────── output model   GWDM
```

That file converts **HDRUK 4.1.0 into GWDM 2.2**. The map that goes the other
way is a different file, `maps/HDRUK/4.1.0/GWDM/2.2/translation.jsonata`.

Confusingly, the API parameters are *not* in path order — `/get/map` names them
explicitly, so order does not matter there:

```bash
TRASER=https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app

curl -s "$TRASER/get/map?input_schema=HDRUK&input_version=4.0.0&output_schema=GWDM&output_version=2.0"
# {"input_schema":"HDRUK","input_version":"4.0.0","output_schema":"GWDM","output_version":"2.0","translation_map":"(\n…"}
```

!!! note "You need two maps, not one"
    The Gateway stores metadata as the GWDM and translates back out on read.
    A map **into** the GWDM makes your data ingestible; a map **out of** the
    GWDM is what lets anyone request their data in your schema. Step 3 is not
    finished until both exist. They are rarely symmetrical — see
    [the round trip](4-test.md).

## Language essentials

Every example below runs against `gwdm-2.0-rich.json` from
[the frozen fixtures](../examples/README.md), bound as `input`. Paste the fixture and the
expression into [the TRASER playground](../reference/traser-tools.md#playground-the-jsonata-sandbox)
to reproduce any of them.

### Paths

```jsonata
input.summary.title
```
```text
"Diagnostic Imaging Dataset"
```

A path that matches nothing evaluates to **undefined** — not `null`, and not an
error:

```jsonata
{ "title": input.summary.title, "doi": input.summary.notAField }
```
```json
{"title": "Diagnostic Imaging Dataset"}
```

The `doi` key is absent from the result. JSONata drops undefined keys from an
object constructor silently. This is a feature — it is how you emit a key only
when the source has one — but it is also the reason a mistyped path produces a
missing field rather than a complaint.

### Arrays flatten when they have one element

This catches everyone. A path that selects from an array returns a **sequence**,
and a sequence of one collapses to a bare value:

```jsonata
$count(input.observations)         /* 1 */
input.observations.observedNode    /* "Persons"  — a string, not an array */
```

The same applies to `$map`:

| Expression | Result |
|---|---|
| `$map([1], function($v){$v*2})` | `2` |
| `$map([1,2], function($v){$v*2})` | `[2,4]` |
| `[$map([1], function($v){$v*2})]` | `[2]` |

Wrap the whole expression in `[ ]` whenever the output must be an array
regardless of how many items matched. Omitting those brackets is the most
common shape bug in a new map, and it only shows up when a dataset happens to
have exactly one of something.

### `$map`, `$filter`, `$reduce`

```jsonata
$map(input.observations, function($o){ $o.observedNode })
$filter(input.observations, function($o){ $o.observedNode = "Persons" }).measuredValue
```
```text
"Persons"
18479800
```

The callback signature is `function($value, $index, $array)`; take only the
arguments you need.

### Conditionals and the `$exists` guard

```jsonata
$exists(input.summary.doiName) ? "has doi" : "no doi"
```
```text
"has doi"
```

`? :` is the only conditional. There is no `if`.

!!! warning "`$exists` tests definedness, not truthiness"
    `$exists()` is `false` only when a path matches nothing. A key that is
    present and set to `null` **exists**:

    | Expression | Result |
    |---|---|
    | `$exists(a.missing)` | `false` |
    | `$exists(a.n)` where `a.n` is `null` | `true` |

    This distinction causes real translation failures — see
    [Debugging](#debugging) below.

### Object and array constructors

```jsonata
{
  "summary": { "title": input.summary.title },
  "keywords": [ "a", "b" ]
}
```

Nested object literals are how a map is built: one constructor per block of the
target schema.

### Variables, sequences, and the last expression

Parentheses introduce a block. Inside one you can bind variables with `:=`,
separated by `;`. **The block evaluates to its last expression:**

```jsonata
(
  $first := input.observations[0];
  $count := $first.measuredValue;
  { "population": $count }
)
```

An assignment is itself an expression that evaluates to the value assigned, so a
block ending in `$x := …;` returns `$x`. That is worth knowing because several
maps in the repository rely on it, and it looks like a bug when you first meet
it.

### Defining functions

```jsonata
$safeNumber := function($x, $fallback){
  ($exists($x) and $x != null) ? $number($x) : $fallback
};
```

Functions are values. Define them at the top of the map, before the object
constructor that uses them.

### String helpers and chaining

`$join`, `$split`, `$substring`, `$string`, `$number`, and `&` for
concatenation:

```jsonata
$string(input.ageBand.from) & "-" & $string(input.ageBand.to)
```

`~>` chains: `$a ~> $f($b)` means `$f($a, $b)`. It reads left to right and
keeps long transforms flat:

```jsonata
$map(input.summary.keywords, function($k){ $k.name })
  ~> $filter(function($v){ $v != null and $v != "" })
  ~> $join(';,;')
```

### Sorting

`^(field)` sorts a sequence ascending, `^(>field)` descending. The cookbook's
`$auto_fill_population_size` uses it to pick the earliest observation:

```jsonata
$observations[observedNode="Persons"]^(observationDate)[0].measuredValue
```

## The three GWDM conventions that bite

These are properties of the target model, not of JSONata. The
[GWDM reference](../schemas/gwdm.md) is the full account; these three are the
ones that will break your first map.

**1. List fields are `';,;'`-joined strings.** The GWDM does not store arrays for
fields like `keywords` or `datasetType`. Pass them through `$to_str`:

```jsonata
$to_str := function($x){
  $x = null ? "" :
  $type($x) = "array" ? $join($x,';,;') :
  $x
};
```

**2. Unknown numerics are `-1`, not `null`.** `populationSize` uses `-1` as its
"not known" sentinel.

**3. Do not emit `summary.publisher` or the `required` block.** Both are owned
by the Gateway API and are overwritten server-side after translation. Anything
your map puts there is discarded.

## Building your first map

A complete map for a small fictional schema. Assume `MyLab 1.0` documents look
like this:

```json title="input"
{
  "datasetName": "Cardiology Imaging Cohort 2019-2024",
  "shortDescription": "Cardiac MRI studies collected at two sites.",
  "topics": ["Cardiovascular", "Imaging types"],
  "tags": ["MRI", "cardiac"],
  "collection": { "from": "2019-01-01", "to": "2024-12-31" },
  "participantCount": null,
  "ageBand": { "from": 18, "to": 90 }
}
```

The map — this is the whole file, and it goes at
`maps/GWDM/2.0/MyLab/1.0/translation.jsonata`:

```jsonata title="maps/GWDM/2.0/MyLab/1.0/translation.jsonata"
(
$to_str := function($x){
  $x = null ? "" :
  $type($x) = "array" ? $join($x,';,;') :
  $x
};

$safeNumber := function($x, $fallback){
  ($exists($x) and $x != null) ? $number($x) : $fallback
};

{
  "summary": {
    "title": input.datasetName,
    "abstract": input.shortDescription,
    "keywords": $to_str(input.tags),
    "datasetType": $to_str(input.topics),
    "populationSize": $safeNumber(input.participantCount, -1)
  },
  "coverage": {
    "typicalAgeRange": $exists(input.ageBand)
      ? $string(input.ageBand.from) & "-" & $string(input.ageBand.to)
      : null
  },
  "provenance": {
    "temporal": {
      "startDate": input.collection.from,
      "endDate": input.collection.to
    }
  }
}
)
```

Evaluated against the document above, it produces:

```json title="output"
{
  "summary": {
    "title": "Cardiology Imaging Cohort 2019-2024",
    "abstract": "Cardiac MRI studies collected at two sites.",
    "keywords": "MRI;,;cardiac",
    "datasetType": "Cardiovascular;,;Imaging types",
    "populationSize": -1
  },
  "coverage": {
    "typicalAgeRange": "18-90"
  },
  "provenance": {
    "temporal": {
      "startDate": "2019-01-01",
      "endDate": "2024-12-31"
    }
  }
}
```

Note `populationSize`. The input carries an explicit `null`, and `$safeNumber`
turns it into the GWDM's `-1` sentinel. The obvious alternative —
`$null_to_number`, the helper the existing maps use — would have **aborted the
translation** here. That is [the next section](#debugging).

### Registering it

Develop the expression in the playground first; it is far faster than a
round trip through the API. When it is right:

1. Save it at
   `maps/{OutputModel}/{outputVersion}/{InputModel}/{inputVersion}/translation.jsonata`
   in a branch of
   [`traser-mapping-files`](https://github.com/HDRUK/traser-mapping-files).
2. Regenerate the registry — a map TRASER does not know about will not be used:

   ```bash
   python utils/list_maps.py
   ```

3. Commit the map **and** the regenerated `available.json` together.
4. Run TRASER locally with `TEMPLATES_LOCATION` pointing at your clone, so the
   instance picks up your file. The recipe is on
   [the developer tools page](../reference/traser-tools.md#running-traser-locally).
5. Prove it end to end:

   ```bash
   curl -s -X POST "http://localhost:3001/translate?input_schema=MyLab&input_version=1.0&output_schema=GWDM&output_version=2.0" \
     -H 'Content-Type: application/json' \
     --data '{"metadata": { "datasetName": "…", "tags": ["MRI"] }}'
   ```

   A 200 with your GWDM document is the success condition. A 400 means output
   validation failed and the body will tell you which fields; a 500 means the
   expression itself threw.

[Step 4](4-test.md) covers testing both directions properly.

## Debugging

The failure modes you will actually hit, in the order you will hit them.

### A field is silently missing

Almost always an undefined path. JSONata drops undefined keys without
complaining, so a typo in `input.summry.title` produces output that validates
and quietly lacks a title.

Check by evaluating just the path in the playground. If it returns
`<undefined>` rather than a value, the path is wrong.

The same thing happens one level down: a helper whose body evaluates to
undefined for the input it was given — `$extract_media` on an array of objects
with no `url` key, or `$tryMatchEnum` on a value outside the allow-list —
removes the key rather than erroring.

### An explicit `null` aborts the whole translation

This is the one that costs an afternoon. Compare:

```jsonata
/* the input has "participantCount": null */
$null_to_number := function($x){ $exists($x) ? $number($x) : -1 };
{ "summary": { "populationSize": $null_to_number(input.participantCount) } }
```
```text
ERROR T0410: Argument 1 of function "number" does not match function signature
```

```jsonata
/* the same expression where the key is absent entirely */
{ "summary": { "populationSize": $null_to_number(input.notThere) } }
```
```json
{"summary":{"populationSize":-1}}
```

Because `$exists(null)` is `true`, the guard passes and `$number(null)` throws.
It is reproducible through the API on the live ingest path:

```bash
# HDRUK 4.0.0 with "summary": {"populationSize": null}
curl -s -X POST "$TRASER/translate?input_schema=HDRUK&input_version=4.0.0&output_schema=GWDM&output_version=2.0" \
  -H 'Content-Type: application/json' --data @explicit-null.json
# HTTP 500 {"message":"Failed to execute translation between HDRUK:4.0.0 and GWDM:2.0","details":{}}
```

Note how little the error tells you: `details` is empty and no field is named.
If a translation 500s and you cannot see why, look for explicit nulls in the
input first.

### Array-versus-scalar surprises

A map that works on a dataset with three keywords and fails on one with a single
keyword is missing its `[ ]` wrapper. See
[the flattening rules](#arrays-flatten-when-they-have-one-element).

### `null` versus undefined versus `""`

Three distinct states that behave differently at every stage:

| | Key present? | `$exists` | Survives `$to_str` as |
|---|---|---|---|
| absent | no | `false` | *(key dropped)* |
| `null` | yes | `true` | `""` |
| `""` | yes | `true` | `""` |

An empty string satisfies neither an enum nor a `minLength` constraint, so a
`null` that becomes `""` on the way in can fail validation on the way back out.

### Output validates but is wrong

`/validate` checks structure, not meaning. A map that writes `startDate` into
`endDate` produces a perfectly valid GWDM document. Passing validation is
necessary, not sufficient — compare a translated document against its source
field by field, which is what [step 4](4-test.md) is for.

### Reading TRASER's errors

A malformed template gives a parse error naming a position; a template that
throws at evaluation time gives the `Failed to execute translation` message
above. Output-validation failures are the informative ones — they come back as
an AJV error array naming the failing path. [The errors
reference](../reference/errors.md) decodes the common codes.

---

Next: [4. Test your maps](4-test.md).
