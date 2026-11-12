# Gateway Technical Guides

Published at
**[https://hdruk.github.io/gateway-2-integrations-testing/](https://hdruk.github.io/gateway-2-integrations-testing/)**

An [MkDocs-Material](https://squidfunk.github.io/mkdocs-material/) site
documenting how dataset metadata gets into and out of the HDR UK Gateway — the
GWDM, the HDRUK and partner schemas, TRASER translation, and the Gateway APIs.

## Running the docs locally

```bash
pip install -r requirements.txt
mkdocs serve
```

Then open **<http://127.0.0.1:8000/gateway-2-integrations-testing/>**.

> [!NOTE]
> The site is served under the `/gateway-2-integrations-testing/` path, not at
> the root, because `site_url` in `mkdocs.yml` points at a GitHub Pages project
> subpath. `http://127.0.0.1:8000/` on its own will answer, but every link off
> it will 404 — use the full URL above.

`mkdocs serve` watches the tree and rebuilds on save. Use `-a` to change the
address, for example `mkdocs serve -a 127.0.0.1:8123`.

## Before you open a PR

```bash
mkdocs build --strict
```

**This must pass with zero warnings.** `--strict` turns broken internal links
and pages missing from the nav into build failures.

CI runs it on every pull request, and deploys to GitHub Pages only on a push to
`master`. `master` has no required status checks, though, so a red build will
not block a merge — run it yourself before you open the PR.

`mkdocs build` writes to `site/`, which is git-ignored.

## Layout

| Path | What it holds |
|---|---|
| `docs/` | the published pages |
| `docs/examples/` | frozen example payloads, field inventories, and the scripts that regenerate them |
| `docs/stylesheets/custom.css` | the HDR UK colour scheme |
| `mkdocs.yml` | navigation, theme, plugins, and the redirect map for old page URLs |

Contributions branch from `master`, which is protected and needs one approving
review.
