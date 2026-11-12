# Frozen example payloads

Every example in these guides cites a file from this directory rather than a
live API call, so the documentation cannot drift when the development database
is refreshed.

Harvested **2026-09-10** from `https://api.dev.hdruk.cloud/api/v1` and the
development translation service.

!!! warning "Redacted"
    These payloads originate from real dataset metadata. Every email address
    has been replaced with `user@example.com` and every telephone number with
    `+44 7700 000000` before the file was written. Publisher names, dataset
    titles and organisation identifiers are public metadata and are unchanged.

## What each fixture demonstrates

| Fixture | Source dataset | Why it is here |
|---|---|---|
| `gwdm-2.0-rich.json` | NHS England Diagnostic Imaging Dataset | 72 structural-metadata tables, full coverage and provenance, an observation, and a populated linkage block |
| `gwdm-2.0-minimal.json` | Oxford University Hospitals, ARIA Radonc | The required fields and little else — no structural metadata, no observations |
| `gwdm-2.0-awkward.json` | Sussex Integrated Dataset, Primary Care Appointments | `populationSize: -1`, a `typicalAgeRange` string, and an `observations` array |
| `gwdm-2.1-cruk-gwdm21.json` | Pancreatic Cancer Radiomics and Biomarker Cohort | The only GWDM **2.1** shape available: carries the five sections 2.1 adds, under the `CRUK` partner context |

For each of those four, this directory also holds:

- `find-<fixture>.json` — the `/find?with_errors=1` response for the stored record
- `hdruk-4.0.0-<fixture>.json` — translated to the current public schema
- `schemaorg-googlerecommended-<fixture>.json` — translated for Google Dataset Search
- `schemaorg-default-<fixture>.json` and `schemaorg-bioschema-<fixture>.json` —
  **both currently fail with HTTP 500.** That is not a harvesting error; see the
  note below.

## Known-failing translations

`SchemaOrg:default` and `SchemaOrg:BioSchema` cannot be reached from any GWDM
2.x record. The only route runs `GWDM 2.0 → 1.2 → 1.1 → SchemaOrg`, and the
`GWDM 1.2 → GWDM 1.1` edge returns HTTP 500 for every payload tried. The
failure files are kept deliberately, because the response body is what a caller
actually sees today.

`translation-routes.tsv` shows the route for each of these, and
`translation-edges.tsv` the whole graph, so the hop count is checkable rather
than asserted.

## Schema field inventories

| File | Contents |
|---|---|
| `fields-gwdm-2.0.tsv` | 149 fields |
| `fields-gwdm-2.1.tsv` | 169 fields |
| `fields-hdruk-4.0.0.tsv` | 123 fields |
| `fields-hdruk-4.1.0.tsv` | 126 fields |
| `fields-gwdm-2.2-UNVERIFIED.tsv` | 152 fields, **none of them verified** |

Each row is `path`, `type`, `required`, `enum`, `description`. Array members
appear as `parent[].child`.

!!! warning "This inventory predates GWDM 2.2's schema"
    GWDM 2.2 is now **published and deployed** — it has a `schema.json` in
    `schemata` and is served by the deployed TRASER (checked 2026-09-21). The
    inventory in this directory, however, was derived from
    `maps/GWDM/2.2/HDRUK/4.1.0/translation.jsonata` before that happened, and
    its rows are still marked `UNVERIFIED`.

    **Regenerate it against the real schema** rather than trusting the marked
    rows. The map it was derived from is a copy of the GWDM 2.0-targeted map
    plus two additions, so it omits the five sections GWDM 2.1 introduced.

## Regenerating

```bash
# fixtures and their translations
python3 docs/examples/harvest.py

# field inventories (pass the path to your schemata checkout)
python3 docs/examples/field_inventory.py ../schemata-2

# translation graph and route table
python3 docs/examples/translation_graph.py
```

`harvest.py` re-applies redaction on every run and deletes the output file
rather than writing an unredacted payload, so a source record that gains a new
contact field cannot leak. After regenerating, confirm it:

```bash
grep -rhoE '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' docs/examples/ | sort -u
# expect exactly: user@example.com
```

The dataset IDs are pinned at the top of `harvest.py`. They point at the
development environment, which holds a copy of the old production database, so
they are stable but not permanent — if a fetch 404s, pick a replacement with
the same characteristics and update the table above.
