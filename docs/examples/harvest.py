#!/usr/bin/env python3
"""Regenerate the frozen example fixtures in this directory.

Usage:  python3 docs/examples/harvest.py

Fetches the stored GWDM for a fixed set of dev-environment datasets, redacts
every contact detail, then asks TRASER to translate each record into the
output schemas the documentation uses. Writes one JSON file per artefact.

Every fixture is redacted before it is written. Nothing that leaves this
script contains a real email address, telephone number or personal name.

Note the request-body asymmetry: /find takes the bare metadata object, while
/translate and /validate take it wrapped as {"metadata": ...}. Wrapping the
payload for /find makes every schema report no match.
"""

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.dev.hdruk.cloud/api/v1"
TRASER = "https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app"
HERE = Path(__file__).parent

FIXTURES = [
    {"id": 868, "slug": "rich", "note": "NHS England Diagnostic Imaging Dataset"},
    {"id": 607, "slug": "minimal", "note": "required fields only, no structural metadata"},
    {"id": 2233, "slug": "awkward", "note": "populationSize -1, typicalAgeRange, observations"},
    {"id": 2187, "slug": "cruk-gwdm21", "note": "GWDM 2.1 under the CRUK partner context"},
]

OUTPUTS = [
    ("HDRUK", "4.0.0"),
    ("SchemaOrg", "default"),
    ("SchemaOrg", "GoogleRecommended"),
    ("SchemaOrg", "BioSchema"),
]

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"(?:\+44[\d ()-]{7,}|\b0[17]\d{8,9}\b)")


def redact(node):
    if isinstance(node, dict):
        return {k: redact(v) for k, v in node.items()}
    if isinstance(node, list):
        return [redact(v) for v in node]
    if isinstance(node, str):
        node = EMAIL.sub("user@example.com", node)
        node = PHONE.sub("+44 7700 000000", node)
        return node
    return node


def get(url):
    with urllib.request.urlopen(url, timeout=180) as response:
        return json.load(response)


def post(url, payload):
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as error:
        body = error.read().decode()
        try:
            return error.code, json.loads(body)
        except json.JSONDecodeError:
            return error.code, {"raw": body}


def write(name, payload):
    path = HERE / name
    path.write_text(json.dumps(payload, indent=2) + "\n")
    blob = path.read_text()
    leaked = [m for m in EMAIL.findall(blob) if not m.endswith("@example.com")]
    if leaked or PHONE.findall(blob.replace("+44 7700 000000", "")):
        path.unlink()
        sys.exit(f"REDACTION FAILED for {name} — file removed")
    print(f"  wrote {name} ({len(blob)} bytes)")


for fixture in FIXTURES:
    dataset_id, slug = fixture["id"], fixture["slug"]
    print(f"{slug} (dataset {dataset_id}) — {fixture['note']}")
    record = get(f"{API}/datasets/{dataset_id}")["data"]
    wrapper = record["versions"][0]["metadata"]
    gwdm_version = wrapper["gwdmVersion"]
    stored = redact(wrapper["metadata"])

    write(f"gwdm-{gwdm_version}-{slug}.json", stored)

    status, found = post(f"{TRASER}/find?with_errors=1", stored)
    write(f"find-{slug}.json", {"status_code": status, "response": found})

    for model, version in OUTPUTS:
        url = (
            f"{TRASER}/translate?output_schema={model}&output_version={version}"
            f"&input_schema=GWDM&input_version={gwdm_version}"
        )
        status, translated = post(url, {"metadata": stored})
        name = f"{model.lower()}-{version.lower()}-{slug}.json"
        write(name, {"status_code": status, "response": redact(translated)})
