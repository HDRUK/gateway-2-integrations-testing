### FMA Datasets

The main `datasets` payload for matches the [FMA schema](https://github.com/HDRUK/schemata-2/blob/master/hdr_schemata/models/FMA/fma.schema.json) and allows FMA to be able to pull metadata for your datasets:

[https://hdr-gateway-fma-test-server-dev-qmnkcg5qjq-ew.a.run.app/api/v1/noauth/exemplar/datasets](https://hdr-gateway-fma-test-server-dev-qmnkcg5qjq-ew.a.run.app/api/v1/noauth/exemplar/datasets)

```json
{
    "items": [
        {
            "name": "SAIL EDAD",
            "@schema": "https://raw.githubusercontent.com/HDRUK/schemata-2/master/hdr_schemata/models/HDRUK/2.1.2/schema.json",
            "description": "Examplar SAIL dataset Education Daily Attendance Dataset (EDAD)",
            "type": "dataset",
            "persistentId": "7eb5d9ff-0d54-4438-9c60-423848aebb4c",
            "self": "http://example-url.com/api/datasets/7eb5d9ff-0d54-4438-9c60-423848aebb4c",
            "version": "11.0.0",
            "issued": "2023-08-17T00:00:00.000Z",
            "modified": "2023-08-17T00:00:00.000Z",
            "source": "SAIL"
        },
        {
            "name": "Alleviate 1958 National Child Development Study ",
            "@schema": "https://raw.githubusercontent.com/HDRUK/schemata-2/master/hdr_schemata/models/HDRUK/2.1.2/schema.json",
            "description": "Examplar Alleviate dataset",
            "type": "dataset",
            "persistentId": "77dc7118-443c-4c85-a18c-e7bbe01e9e7a",
            "self": "http://example-url.com/api/datasets/77dc7118-443c-4c85-a18c-e7bbe01e9e7a",
            "version": "1.0.0",
            "issued": "2021-09-23T00:00:00.000Z",
            "modified": "2021-09-23T00:00:00.000Z",
            "source": "ALLEVIATE"
        },
        {
            "name": "UKBiobank with tissues",
            "@schema": "https://raw.githubusercontent.com/HDRUK/schemata-2/master/hdr_schemata/models/HDRUK/2.1.2/schema.json",
            "description": "Examplar UKBiobank",
            "type": "dataset",
            "persistentId": "1460e2b4-a985-4890-8e60-a21e78ce01f3",
            "self": "http://example-url.com/api/datasets/1460e2b4-a985-4890-8e60-a21e78ce01f3",
            "version": "11.0.0",
            "issued": "2022-04-19T00:00:00.000Z",
            "modified": "2022-04-19T00:00:00.000Z",
            "source": "UKBiobank"
        }
    ],
    "query": { "q": "", "total": 3, "limit": 0, "offset": 0 }
}
```

### Dataset Example

For example one of the datasets listed in the above datasets payload directs the service to the location of where to find metadata for a dataset that matches the HDRUK 2.1.2 schema.

Example:

[https://hdr-gateway-fma-test-server-dev-qmnkcg5qjq-ew.a.run.app/api/v1/noauth/exemplar/datasets/77dc7118-443c-4c85-a18c-e7bbe01e9e7a](https://hdr-gateway-fma-test-server-dev-qmnkcg5qjq-ew.a.run.app/api/v1/noauth/exemplar/datasets/77dc7118-443c-4c85-a18c-e7bbe01e9e7a)

```json
{
    "identifier": "https://web.www.healthdatagateway.org/77dc7118-443c-4c85-a18c-e7bbe01e9e7a",
    "version": "1.0.0",
    "issued": "2021-09-23T00:00:00.000Z",
    "modified": "2021-09-23T00:00:00.000Z",
    "revisions": [],
    "summary": {
        "title": "1958 National Child Development Study - Pain data",
        "abstract": "This collection specifically relates to a short pain survey (self-completion booklet) completed by NCDS participants in 2002-3.",
        "publisher": {
            "identifier": "https://web.www.healthdatagateway.org/613b2174b8b58d157f531e7a",
            "name": "ALLEVIATE",
            "logo": null,
            "description": null,
            "contactPoint": null,
            "memberOf": "HUB"
        },
        "contactPoint": "blah@blah.com",
        "keywords": "Alleviate,Pain,Pain Hub",
        "alternateIdentifiers": null,
        "doiName": "10.5255/UKDA-SN-8731-1"
    },
    ...
}
```
