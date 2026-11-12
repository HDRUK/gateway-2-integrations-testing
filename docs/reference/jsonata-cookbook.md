---
title: JSONata cookbook
description: The canonical helper library and the patterns that come up in every Gateway translation map.
tags:
  - reference
  - jsonata
---

# JSONata cookbook

**Applies to:** HDRUK 2.0.2 – 4.1.0 · GWDM 1.0 – 2.2

Every translation map in
[`traser-mapping-files`](https://github.com/HDRUK/traser-mapping-files) opens by
defining a handful of the same helper functions. This page is the canonical
source for them: what each one does, what it returns for the inputs that catch
people out, and which maps currently use it.

If you are writing your first map, start with
[Write your JSONata maps](../byos/3-map.md) and come back here for the
functions.

!!! danger "There is no import mechanism, so these are copy-pasted"
    JSONata has no `import`. Every map that needs `$to_str` defines `$to_str`
    at the top of the file. Across the 57 maps in `traser-mapping-files` that
    produces **16 copies of `$to_str`, 11 of `$safeSplit`, 9 of `$truncate`**,
    and so on — and a fix applied to one copy does not reach the others.

    **Copy from this page**, not from whichever map you happened to open. If
    you improve a function, say so in your pull request so the team can decide
    whether to propagate it.

    We know this is unsatisfactory and it is on the backlog. **Do not try to
    solve it as part of a mapping PR** — no preprocessor, no bundler, no
    shared-function injection.

## Three traps, before you copy anything

These are the failure modes that actually cost people an afternoon. All three
were reproduced against the deployed development TRASER, not inferred from
reading the source.

### 1. An explicit `null` is not the same as an absent key

`$null_to_number` exists to supply the GWDM's `-1` "unknown" sentinel. It does
that only when the key is **missing**. When the key is present and set to
`null`, it throws, and the whole translation returns HTTP 500.

```bash
TRASER=https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app

# summary.populationSize omitted entirely
curl -s -X POST "$TRASER/translate?input_schema=HDRUK&input_version=4.0.0&output_schema=GWDM&output_version=2.0" \
  -H 'Content-Type: application/json' --data @omitted.json
# HTTP 200, summary.populationSize -> -1

# summary.populationSize present, set to null
curl -s -X POST "$TRASER/translate?input_schema=HDRUK&input_version=4.0.0&output_schema=GWDM&output_version=2.0" \
  -H 'Content-Type: application/json' --data @explicit-null.json
# HTTP 500 {"message":"Failed to execute translation between HDRUK:4.0.0 and GWDM:2.0","details":{}}
```

The cause is that `$exists()` is a test for *definedness*, not for
truthiness — a JSON `null` exists:

| Expression | Result |
|---|---|
| `$exists(a.missing)` | `false` |
| `$exists(a.n)` where `a.n` is `null` | `true` |
| `$type(a.n)` where `a.n` is `null` | `"null"` |

So `$exists($x) ? $number($x) : -1` takes the `$number(null)` branch and raises
`T0410`. Guard on the value, not on existence, whenever your input might carry
explicit nulls — see [the recipe below](#defaulting-a-field-that-may-be-an-explicit-null).

### 2. `$to_str` throws on an array of numbers

`$join` requires an array of strings. Six of the seven `$to_str` variants pass
their array straight to it, so a numeric array aborts the translation with
`T0412`.

| Expression | Result |
|---|---|
| `$to_str(["a","b"])` | `"a;,;b"` |
| `$to_str([1,2])` | **`ERROR T0412`** |

If your source field can hold numbers, coerce first — the
`GWDM/2.0/HDRUK/3.0.0` map already does this:

```jsonata
$to_str := function($x){
  $type($x)="array"
  ? $join($map($x, function($v){ $string($v) }), ';,;')
  : $string($x)
};
```

### 3. `0` is falsy, and most of these helpers test truthiness

`$defaultValue(0, "fallback")` returns `"fallback"`, not `0`. Where `0` is a
legitimate value — an age range minimum, a count — test for it explicitly, as
`$joinTypicalAgeRange` does for its lower bound.

---

## The library

Each entry gives the canonical body, then a table of tested results. Every row
was produced by evaluating the expression; paste any of them into
[the playground](traser-tools.md#playground-the-jsonata-sandbox) to reproduce it.

### `$to_str` — coerce an array to a delimited string

The GWDM stores list-valued fields as a single `';,;'`-delimited string. This is
the function that produces them, and it is the most-copied helper in the repo.

```jsonata title="canonical — as used by HDRUK 4.1.0 → GWDM 2.2"
$to_str := function($x){
  $x = null ? "" :
  $type($x) = "array" ? $join($x,';,;') :
  $x
};
```

| Expression | Result |
|---|---|
| `$to_str(["a","b"])` | `"a;,;b"` |
| `$to_str(["a"])` | `"a"` |
| `$to_str("a")` | `"a"` |
| `$to_str([])` | `""` |
| `$to_str(null)` | `""` |
| `$to_str(0)` | `0` |
| `$to_str([1,2])` | `ERROR T0412` |

!!! warning "`null` becomes an empty string, and an empty string is not `null`"
    An empty string satisfies neither an enum nor a `minLength` constraint on
    the way back out. Maps translating *out of* the GWDM generally have to undo
    this — the `HDRUK 4.1.0 → GWDM 2.2` pair carries explicit guards for
    `resourceCreator` and `deliveryLeadTime` for exactly this reason.

**Used by:** 16 maps, in [7 variants](#where-the-copies-disagree).

### `$safeSplit` — split a delimited string back into an array

The inverse of `$to_str`, used by every map translating out of the GWDM.

```jsonata title="canonical — as used by HDRUK 4.0.0 → GWDM 2.0"
$safeSplit := function($x, $delim) {
    ($x != null and $x != "null" and $type($x) = "string") ? $x ~> $split($delim) : []
};
```

| Expression | Result |
|---|---|
| `$safeSplit("a;,;b", ";,;")` | `["a","b"]` |
| `$safeSplit("a", ";,;")` | `["a"]` |
| `$safeSplit(null, ";,;")` | `[]` |
| `$safeSplit("null", ";,;")` | `[]` |
| `$safeSplit("", ";,;")` | `[""]` |
| `$safeSplit(["a","b"], ";,;")` | `[]` |

Note the last two rows. An empty string yields a one-element array containing an
empty string, not `[]`; and an array passed in by mistake is silently swallowed
rather than passed through. Other copies of this function behave differently on
both — see the [divergence table](#where-the-copies-disagree).

**Used by:** 11 maps, in 5 variants.

### `$null_to_number` — the `-1` unknown sentinel

```jsonata title="canonical — identical in all 8 maps that define it"
$null_to_number := function($x){
  $exists($x) ? $number($x) : -1
};
```

| Expression | Result |
|---|---|
| `$null_to_number(42)` | `42` |
| `$null_to_number("42")` | `42` |
| `$null_to_number(0)` | `0` |
| `$null_to_number(null)` | **`ERROR T0410`** |
| `$null_to_number("abc")` | **`ERROR D3030`** |

This is [trap 1](#1-an-explicit-null-is-not-the-same-as-an-absent-key). The
function is consistent across every copy, so there is no drift here — the
behaviour is simply surprising.

### `$auto_fill_population_size` — derive a population from observations

Where `populationSize` is unknown, fall back to the earliest `Persons`
observation.

```jsonata title="canonical — identical in all 5 maps that define it"
$auto_fill_population_size := function($populationSize, $observations){
    $populationSize = -1 ? $observations[observedNode="Persons"]^(observationDate)[0].measuredValue ~> $null_to_number : $populationSize ~> $null_to_number
};
```

`^(observationDate)` is JSONata's sort operator: it orders the filtered
observations ascending by date, and `[0]` takes the earliest. Because both
branches end in `$null_to_number`, this function inherits trap 1.

### `$truncate` — cut a string to a maximum length

```jsonata title="canonical — as used by the GWDM 2.x maps"
$truncate := function($x,$length){
  $type($x)="number" ? $x : $x ? $substring($x,0,$length) : null
};
```

| Expression | Result |
|---|---|
| `$truncate("abcdef", 3)` | `"abc"` |
| `$truncate(12345, 3)` | `12345` |
| `$truncate(0, 3)` | `0` |
| `$truncate("", 3)` | `null` |
| `$truncate(null, 3)` | `null` |

The `$type($x)="number"` guard is what lets numbers through untouched. **The
older four-map variant omits it**, and `$truncate(12345, 3)` raises `T0410`
there. If you are working in a GWDM 1.x map, check which one you have.

### `$extract_media` — flatten media objects to a URL list

```jsonata title="canonical — as used by 6 maps"
$extract_media := function($x){
  $type($x) = "array"
    ? $join($map($x, function($v){ $type($v) = "object" ? $v.url : $v }), ',')
    : $x
};
```

| Expression | Result |
|---|---|
| `$extract_media([{"url":"a"},{"url":"b"}])` | `"a,b"` |
| `$extract_media(["a","b"])` | `"a,b"` |
| `$extract_media(null)` | `null` |
| `$extract_media([{"noturl":"x"}])` | `<undefined>` |

The last row is the one to watch: an array of objects with no `url` key
produces **undefined**, and JSONata drops undefined keys from the output object
without complaint. The field simply will not appear.

Note also that this helper joins with `,`, not `';,;'`, even in maps that
target the GWDM.

### `$isValidString`, `$isValidArray`, `$isEmptyValue` — emptiness tests

```jsonata title="canonical — identical in every map that defines them"
$isValidString := function($str) { $type($str) = "string" and $str != null and $str != "" };
$isValidArray := function($arr) { $type($arr) = "array"  };
$isEmptyValue := function($value) { $value = null or $value = "" or $value = {} };
```

| Expression | Result |
|---|---|
| `$isValidString("a")` | `true` |
| `$isValidString("")` | `false` |
| `$isValidString(42)` | `false` |
| `$isValidArray([])` | `true` |
| `$isValidArray("a")` | `false` |
| `$isEmptyValue(null)` | `true` |
| `$isEmptyValue({})` | `true` |
| `$isEmptyValue(0)` | `false` |

`$isValidArray([])` is `true` — it is a type test, not an emptiness test.

### `$defaultValue` and `$ageRangeDefault` — supplying a fallback

```jsonata title="canonical — identical in all 6 maps that define it"
$defaultValue := function($value,$defaultValue){
    $value ? $value : $defaultValue
};
```

| Expression | Result |
|---|---|
| `$defaultValue("x", "fallback")` | `"x"` |
| `$defaultValue(null, "fallback")` | `"fallback"` |
| `$defaultValue("", "fallback")` | `"fallback"` |
| `$defaultValue(0, "fallback")` | `"fallback"` |
| `$defaultValue(false, "fallback")` | `"fallback"` |

`$ageRangeDefault` is `$defaultValue` with a `0` guard bolted on:

```jsonata title="canonical — as corrected in the GWDM 2.2 map"
$ageRangeDefault := function($value, $defaultValue){
    $value ? $value :
        $value = 0 ? $value : $defaultValue
};
```

!!! warning "Four maps carry a typo'd copy of this function"
    In `CRUK 1.0.0 → GWDM 2.0`, `CRUK 1.0.0 → GWDM 2.1`,
    `HDRUK 3.0.0 → GWDM 2.0` and `HDRUK 4.0.0 → GWDM 2.0`, the final branch
    reads `$defaultvalue` — lowercase `v` — which is an undefined variable.
    The fallback is therefore never applied and the result is undefined:

    | Expression | Typo'd copy | Corrected copy |
    |---|---|---|
    | `$ageRangeDefault(18, 0)` | `18` | `18` |
    | `$ageRangeDefault(0, 150)` | `0` | `0` |
    | `$ageRangeDefault(null, 150)` | **`<undefined>`** | `150` |

    All four call it on `typicalAgeRangeMin` and `typicalAgeRangeMax`. Since
    they pass `null` as the default, the visible effect is a dropped key rather
    than a wrong value. Recorded, not fixed.

### `$nullString`, `$nullableValues`, `$nullList` — normalising "no value"

Partner data spells "nothing here" many ways. These map the common spellings
onto a real `null`.

```jsonata title="canonical — the camelCase family, 5 maps"
$nullableValues := ["",''," ","\"","Not Applicable","Not Available",
                     "Not applicable",'[]',
                     "NOT AVAILABLE","NOT APPLICABLE",[null]];

$nullString := function($x){
  ($x in $nullableValues or $type($x) != "string" or $not($exists($x)) ) ? null : $x
};

$nullList := function($x){
    [$filter($x, function($xx){
        $map($nullString($xx), function($item){ $item != null })
    })]
};
```

| Expression | Result |
|---|---|
| `$nullString("real")` | `"real"` |
| `$nullString("")` | `null` |
| `$nullString(" ")` | `null` |
| `$nullString("NOT AVAILABLE")` | `null` |
| `$nullString("[]")` | `null` |
| `$nullString(42)` | `null` |
| `$nullList(["a","","b"])` | `["a","b"]` |
| `$nullList(["Not Available","a"])` | `["a"]` |

`$nullString(42)` returns `null` because the function requires a string —
passing a number through it destroys it.

!!! warning "The same function also exists under a snake_case name, and differs"
    Four maps define `$null_string` and `$nullable_values` instead. The
    sentinel list is the same **except that it omits `''` and `'[]'`**:

    | Expression | `$nullString` (camelCase) | `$null_string` (snake_case) |
    |---|---|---|
    | `$nullString("[]")` | `null` | `"[]"` |

    `$nullList` and `$null_array` are likewise the same idea under two names
    with two implementations. Check which spelling your map uses.

### `$tryMatchEnum`, `$cleanEnumSingle`, `$cleanEnum` — matching enum values

The GWDM and HDRUK schemas constrain many fields to an enum. Partner data
rarely matches the casing, so maps carry an allow-list and a fuzzy matcher.

```jsonata title="canonical — as used by the GWDM 2.x maps"
$tryMatchEnum := function($x, $allowed){(
    $cleaned := $x ? $x : "";
    $lowered := $join([$uppercase($substring($cleaned, 0, 1)), $substring($lowercase($cleaned), 1, $length($cleaned))]);
    $match := $filter($allowed, function($v, $i, $a){(
        $allowedLowered := $join([$uppercase($substring($v, 0, 1)), $substring($lowercase($v), 1, $length($v))]);
        $allowedLowered = $lowered ? $a[$i] : null
    )})
)};

$cleanEnumSingle := function($x, $allowed){
    $tryMatchEnum($x, $allowed)
};

$cleanEnum := function($x, $allowed){
    ($isValidString($x) ?
        [$map($split($x, ","), function($v){
            $tryMatchEnum($v, $allowed)
        })] :
        ($isValidArray($x) ? [$map($x, function($v){
            $tryMatchEnum($v, $allowed)
        })] : null )
    )
};
```

With `$allowed` = `["Cancer","Mental health","Other"]`:

| Expression | Result |
|---|---|
| `$tryMatchEnum("cancer", $allowed)` | `"Cancer"` |
| `$tryMatchEnum("CANCER", $allowed)` | `"Cancer"` |
| `$tryMatchEnum("nope", $allowed)` | `<undefined>` |
| `$tryMatchEnum(null, $allowed)` | `<undefined>` |
| `$cleanEnum("Cancer,Other", $allowed)` | `["Cancer","Other"]` |
| `$cleanEnum(["Cancer","nope"], $allowed)` | `["Cancer"]` |
| `$cleanEnum(null, $allowed)` | `null` |

!!! warning "Unmatched values are dropped silently"
    `$cleanEnum(["Cancer","nope"], …)` returns `["Cancer"]`. Nothing is logged
    and no error is raised. If a partner's vocabulary does not line up with the
    allow-list, their values disappear without trace — this is the single most
    common cause of "my field went missing" reports.

    The matcher normalises to sentence case only. `"mental Health"` matches
    `"Mental health"`; `"Mental Health"` does not.

The allow-lists themselves (`$allowedPurpose`, `$allowedSetting`,
`$allowedTimeLag`, and about 25 others) are **deliberately** different in
different maps — each carries the enum of the schema version it is writing to.
`HDRUK 2.2.1` uses `"LESS 1 WEEK"` where `HDRUK 3.0.0` uses
`"Less than 1 week"`. Do not "harmonise" them.

### `$joinTypicalAgeRange` — build the GWDM age-range string

```jsonata title="canonical — identical in all 5 maps that define it"
$joinTypicalAgeRange := function($min, $max){(
    $minStr := $min ? $string($min) : $min = 0 ? $string($min) : null;
    $maxStr := $max ? $string($max) : null;
    $minStr ? $maxStr ? $join([$minStr, "-", $maxStr]) : null : null
)};
```

| Expression | Result |
|---|---|
| `$joinTypicalAgeRange(18, 65)` | `"18-65"` |
| `$joinTypicalAgeRange(0, 65)` | `"0-65"` |
| `$joinTypicalAgeRange(18, 0)` | **`null`** |
| `$joinTypicalAgeRange(null, 65)` | `null` |
| `$joinTypicalAgeRange(18, null)` | `null` |

The `0` guard is applied to `$min` but not to `$max`, so an upper bound of `0`
discards the whole range. That asymmetry is in every copy.

### `$getDatasetLinkage` — assemble the linkage block

Unlike the rest of the library this one takes no arguments and reads `input.*`
directly, so it is not portable between maps — each direction has its own body.

```jsonata title="input HDRUK 4.1.0 → output GWDM 2.2"
$getDatasetLinkage := function() {
  (
    $datasetLinkage := {
      "isDerivedFrom": input.enrichmentAndLinkage.derivedFrom,
      "isPartOf": input.enrichmentAndLinkage.isPartOf,
      "isMemberOf": input.enrichmentAndLinkage.similarToDatasets,
      "linkedDatasets": input.enrichmentAndLinkage.linkableDatasets
    };
    $datasetLinkage
  )
};
```

Four other maps carry the same body **without** the final `$datasetLinkage`
line. That reads like a bug and has been reported as one, but it is not: in
JSONata an assignment is itself an expression that evaluates to the value
assigned, so a block ending in `$x := …;` returns `$x`. Both forms emit the key.

```bash
# HDRUK 4.0.0 -> GWDM 2.0, the map without the final expression
curl -s -X POST "$TRASER/translate?input_schema=HDRUK&input_version=4.0.0&output_schema=GWDM&output_version=2.0&validate_input=0&validate_output=0" \
  -H 'Content-Type: application/json' --data @linked.json | jq .linkage.datasetLinkage
# {"isDerivedFrom":["DS-A"],"isPartOf":["DS-B"],"isMemberOf":["DS-C"],"linkedDatasets":["DS-D"]}
```

Adding the explicit final line is still better style — it says what the function
returns — but it is not a fix.

### Dates and URLs

```jsonata title="$to_iso8601 — SchemaOrg maps, 5 copies, identical"
$to_iso8601 := function($x){
    $replace($x, /(\.\d{6})$/, 'Z')
};
```

| Expression | Result |
|---|---|
| `$to_iso8601("2024-10-08T11:30:43.290910")` | `"2024-10-08T11:30:43Z"` |
| `$to_iso8601("2024-10-08T11:30:43Z")` | `"2024-10-08T11:30:43Z"` |

It replaces a six-digit fractional-seconds suffix with `Z`. It does not convert
time zones and it does not validate — anything not ending in exactly six digits
passes through untouched.

```jsonata title="$get_date — the datasetv2 maps"
$get_date := function($x){
  $type($x) = "number" ? $fromMillis($x) : $fromMillis($toMillis($x,'[D01]/[M01]/[Y0001]'))
};
```

!!! danger "`$force_url` never returns a URL"
    Two maps define:

    ```jsonata
    $force_url := function($x){
        $x = /^http(s)?:\/\// ? $x : null
    };
    ```

    JSONata's `=` is equality, not a match operator, and a string is never
    equal to a regex — so this returns `null` for **every** input, including
    `"https://example.org"`. Use `$contains($x, /^https?:\/\//)` instead.

    Neither map actually calls it, so nothing is broken today. Recorded so that
    nobody copies it.

### The form-hydration maps are a different language

`maps/Hydration/**` defines a further 36 functions — `$textField`,
`$selectBox`, `$define_components`, `$stringValidation` and friends. They build
the form definition that drives the Gateway's manual onboarding UI rather than
translating metadata, and they share **no** function names with the translation
maps. Nothing on this page applies to them.

---

## Where the copies disagree

Of the 98 function names defined across the 52 translation maps, 28 are defined
in more than one map. **Eight of those 28 have drifted** — the copies are not
byte-identical after normalising whitespace and comments.

| Function | Copies | Variants | Is the drift meaningful? |
|---|:-:|:-:|---|
| `$to_str` | 16 | 7 | **Yes** — four different delimiters and three different `null` results |
| `$safeSplit` | 11 | 5 | **Yes** — an array argument returns the array, `[]`, or raises `T0410` |
| `$extract_media` | 9 | 3 | **Yes** — joins with `,` or `';,;'`; one variant drops plain-string arrays |
| `$truncate` | 9 | 2 | **Yes** — the older variant raises `T0410` on a number |
| `$getDatasetLinkage` | 7 | 4 | No — each direction reads a different input shape |
| `$tryMatchEnum` | 7 | 3 | **Yes** — sentence-case matching versus uppercase matching |
| `$ageRangeDefault` | 5 | 2 | **Yes** — four copies reference an undefined `$defaultvalue` |
| `$getMaterialType` | 5 | 2 | No — the CRUK copies accept a bare string as well as an object |

The other 20 shared helpers — including `$null_to_number`, `$defaultValue`,
`$isValidString`, `$isEmptyValue`, `$joinTypicalAgeRange`, `$nullString`,
`$auto_fill_population_size` and `$to_iso8601` — are identical everywhere they
appear.

Roughly 60 further names are **value tables** rather than logic:
`$allowedPurpose`, `$cleanDatasetType`, `$map_accrualPeriodicity` and so on.
Eighteen of the 35 shared ones differ between maps, and that is correct — they
encode the target schema's enum, which changes by version.

### `$to_str` in detail

The worst case, and worth seeing in full, because two maps writing **the same
output version** disagree:

| Variant | Maps | `["a","b"]` | `null` | `[]` |
|---|---|---|---|---|
| `;,;`, null→`""` | 4, incl. `HDRUK 4.1.0 → GWDM 2.2` | `"a;,;b"` | `""` | `""` |
| `,` | 5 SchemaOrg maps | `"a,b"` | `null` | `""` |
| `,` | `GWDM 1.0 ← HDRUK 2.1.2`, `GWDM 1.1 ← HDRUK 2.2.0`, `GWDM 1.2 ← HDRUK 2.2.1` | `"a,b"` | `null` | `""` |
| `;,;` | `GWDM 1.1 ← HDRUK 2.1.2` | `"a;,;b"` | `null` | `""` |
| `;,;`, `$string()` coerced | `GWDM 2.0 ← HDRUK 3.0.0` | `"a;,;b"` | `"null"` | `<undefined>` |
| `;,;`, nulls filtered | 2 `datasetv2` maps | `"a;,;b"` | `null` | `<undefined>` |

Rows three and four are the problem: **a dataset arriving as HDRUK 2.1.2 gets
`';,;'`-delimited GWDM 1.1 lists, and the same dataset arriving as HDRUK 2.2.0
gets comma-delimited ones.** Comma delimiting is indistinguishable from a
single value containing a comma, so that is lossy. Both maps are in production.

The `,` in the SchemaOrg rows is correct — schema.org expects comma-separated
lists, not the GWDM convention.

---

## Recipes

Patterns that recur across the maps, beyond the named helpers.

### Emitting a key only when the source has a value

JSONata drops undefined keys from an object constructor, so the idiom is to let
the expression evaluate to undefined rather than to guard the key:

```jsonata
{
  "doi": input.summary.doiName    /* absent from the output if the path misses */
}
```

Where you need an explicit `null` instead of an absent key — the GWDM generally
does — force it:

```jsonata
{
  "doi": $exists(input.summary.doiName) ? input.summary.doiName : null
}
```

### Defaulting a field that may be an explicit null

The guard that survives both a missing key and an explicit `null`:

```jsonata
$safeNumber := function($x, $fallback){
  ($exists($x) and $x != null) ? $number($x) : $fallback
};
```

| Expression | Result |
|---|---|
| `$safeNumber(input.missing, -1)` | `-1` |
| `$safeNumber(input.isNull, -1)` where the value is `null` | `-1` |
| `$safeNumber(input.n, -1)` where the value is `42` | `42` |

### Mapping an enum with a lookup object

For a fixed rename rather than a fuzzy match, `$lookup` against an object beats
a chain of conditionals:

```jsonata
$accrualMap := {
  "STATIC": "Static",
  "IRREGULAR": "Irregular",
  "CONTINUOUS": "Continuous"
};

$mapped := $lookup($accrualMap, $uppercase($x));
$exists($mapped) ? $mapped : "Other"
```

`$lookup` returns undefined for an unmapped key, so the `$exists` branch is what
stops the field vanishing. Several maps wrap this as `$applyMap`:

```jsonata
$applyMap := function($x,$theMap){
  $type($x) = 'array' ? [$map($x, function($el){ $applyMap($el,$theMap)})] ~> $null_array : ($x ? $lookup($theMap,$x) ~> $null_string : null)
};
```

### Flattening a nested array into a delimited string

Pull the field out of each object, drop the empties, then join:

```jsonata
$map(input.summary.keywords, function($k){ $k.name })
  ~> $filter(function($v){ $v != null and $v != "" })
  ~> $join(';,;')
```

`~>` is function chaining: `$a ~> $f($b)` is `$f($a, $b)`. It reads left to
right and avoids the nesting that makes long transforms unreadable.

### Splitting a delimited string back into objects

The reverse direction, as the GWDM 2.0 → 1.2 map does it:

```jsonata
[$map($safeSplit(input.linkage.datasetLinkage.isDerivedFrom, ';,;'),
      function($v){ {'title': $v} })]
```

The outer `[...]` forces an array even when there is a single element — without
it a one-item result collapses to a bare object and fails an `array` schema
constraint. This is the most common shape bug in a new map.

### Normalising a date to ISO 8601

```jsonata
$toIso := function($x){
  $exists($x) and $x != null
    ? $fromMillis($toMillis($x), '[Y0001]-[M01]-[D01]T[H01]:[m01]:[s01]Z')
    : null
};
```

| Expression | Result |
|---|---|
| `$toIso("2024-10-08T11:30:43Z")` | `"2024-10-08T11:30:43Z"` |
| `$toIso("2024-10-08")` | `"2024-10-08T00:00:00Z"` |
| `$toIso(null)` | `null` |

`$toMillis` raises `D3110` on a string it cannot parse, so validate the input
format before relying on this in a map that accepts partner data.

### Carrying an unmapped field through `extra`

Every template is evaluated against `{ input: …, extra: … }`. Anything the
caller passes as `extra` in the request body is readable as `extra.*`, which is
how a map reaches values that are not part of the input document:

```jsonata
{
  "publisher": $exists(extra.publisherName) ? extra.publisherName : input.summary.publisher.publisherName
}
```

See [the TRASER API reference](traser-api.md) for how to populate `extra` on a
`/translate` call.

---

## What was measured, and how

The inventory behind this page was produced by parsing all 57
`translation.jsonata` files, extracting every top-level assignment, normalising
comments and whitespace, and grouping the bodies by hash. The scripts are in
`plans/state/scripts/` in this repository.

Every result table was produced by evaluating the expression with JSONata
2.2.1 — the version TRASER pins — and the two HTTP examples were run against the
deployed development TRASER on 2026-09-10.
