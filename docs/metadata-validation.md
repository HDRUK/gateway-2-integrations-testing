## Schema Validation

Once you have created your metadata, for example for the HDRUK schema `3.0.0`, you can use [various routes](https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app/docs/) of the translation service to check to see if it validates against this schema.

Using the example file found at [https://github.com/HDRUK/gateway-2-integrations-testing/blob/master/example-hdruk300.json](https://github.com/HDRUK/gateway-2-integrations-testing/blob/master/example-hdruk300.json):

=== "python"

    Using python `requests`
    
    ``` python
    import json
    import requests

    metadata = json.load(open("example-hdruk300.json"))

    headers = {
        "Content-Type": "application/json",
    }

    traser_uri = "https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app"
    response = requests.post(
        f"{traser_uri}/find?with_errors=1", headers=headers, json=metadata
    )

    print(json.dumps(response.json(), indent=6))

    ```

=== "CURL"

    ```bash
     metadata='{"metadata": '$(cat example-hdruk300.json)'}'
     curl --location 'https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app/find?with_errors=1'\
     --header 'Content-Type: application/json' --data  \
     --data "$metadata"
    ```

Responds with:

```
[
    {
        "name": "HDRUK",
        "version": "2.1.2",
        "matches": false,
        "errors": [
            {
                "instancePath": "/summary",
                "schemaPath": "#/required",
                "keyword": "required",
                "params": {
                    "missingProperty": "publisher"
                },
                "message": "must have required property 'publisher'"
            }
        ]
    },
    {
        "name": "HDRUK",
        "version": "2.1.3",
        "matches": false,
        "errors": [
            {
                "instancePath": "/summary",
                "schemaPath": "#/required",
                "keyword": "required",
                "params": {
                    "missingProperty": "publisher"
                },
                "message": "must have required property 'publisher'"
            }
        ]
    },
    {
        "name": "HDRUK",
        "version": "2.1.0",
        "matches": false,
        "errors": [
            {
                "instancePath": "/summary",
                "schemaPath": "#/required",
                "keyword": "required",
                "params": {
                    "missingProperty": "publisher"
                },
                "message": "must have required property 'publisher'"
            }
        ]
    },
    {
        "name": "HDRUK",
        "version": "2.0.2",
        "matches": false,
        "errors": [
            {
                "instancePath": "",
                "schemaPath": "#/additionalProperties",
                "keyword": "additionalProperties",
                "params": {
                    "additionalProperty": "structuralMetadata"
                },
                "message": "must NOT have additional properties"
            }
        ]
    },
    {
        "name": "HDRUK",
        "version": "2.2.1",
        "matches": false,
        "errors": [
            {
                "instancePath": "/summary",
                "schemaPath": "#/required",
                "keyword": "required",
                "params": {
                    "missingProperty": "publisher"
                },
                "message": "must have required property 'publisher'"
            }
        ]
    },
    {
        "name": "HDRUK",
        "version": "2.2.0",
        "matches": false,
        "errors": [
            {
                "instancePath": "/summary",
                "schemaPath": "#/required",
                "keyword": "required",
                "params": {
                    "missingProperty": "publisher"
                },
                "message": "must have required property 'publisher'"
            }
        ]
    },
    {
        "name": "HDRUK",
        "version": "3.0.0",
        "matches": true,
        "errors": null
    },
    {
        "name": "GWDM",
        "version": "1.0",
        "matches": false,
        "errors": [
            {
                "instancePath": "",
                "schemaPath": "#/required",
                "keyword": "required",
                "params": {
                    "missingProperty": "required"
                },
                "message": "must have required property 'required'"
            }
        ]
    },
    {
        "name": "GWDM",
        "version": "1.1",
        "matches": false,
        "errors": [
            {
                "instancePath": "",
                "schemaPath": "#/required",
                "keyword": "required",
                "params": {
                    "missingProperty": "required"
                },
                "message": "must have required property 'required'"
            }
        ]
    },
    {
        "name": "GWDM",
        "version": "1.2",
        "matches": false,
        "errors": [
            {
                "instancePath": "",
                "schemaPath": "#/required",
                "keyword": "required",
                "params": {
                    "missingProperty": "required"
                },
                "message": "must have required property 'required'"
            }
        ]
    },
    {
        "name": "GWDM",
        "version": "2.0",
        "matches": false,
        "errors": [
            {
                "instancePath": "",
                "schemaPath": "#/required",
                "keyword": "required",
                "params": {
                    "missingProperty": "required"
                },
                "message": "must have required property 'required'"
            }
        ]
    },
    {
        "name": "SchemaOrg",
        "version": "default",
        "matches": false,
        "errors": [
            {
                "instancePath": "",
                "schemaPath": "#/required",
                "keyword": "required",
                "params": {
                    "missingProperty": "name"
                },
                "message": "must have required property 'name'"
            }
        ]
    },
    {
        "name": "SchemaOrg",
        "version": "BioSchema",
        "matches": false,
        "errors": [
            {
                "instancePath": "",
                "schemaPath": "#/required",
                "keyword": "required",
                "params": {
                    "missingProperty": "name"
                },
                "message": "must have required property 'name'"
            }
        ]
    },
    {
        "name": "SchemaOrg",
        "version": "GoogleRecommended",
        "matches": false,
        "errors": [
            {
                "instancePath": "",
                "schemaPath": "#/required",
                "keyword": "required",
                "params": {
                    "missingProperty": "name"
                },
                "message": "must have required property 'name'"
            }
        ]
    }
]
```

You can use the route `validate` instead of `find` to validate a payload against an expected schema.

=== "python"

    ```python

    import json
    import requests

    metadata = json.load(open("example-hdruk300.json"))

    headers = {
        "Content-Type": "application/json",
    }

    traser_uri = "https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app"

    response = requests.post(
        f"{traser_uri}/validate?input_schema=HDRUK&input_version=3.0.0",
        headers=headers, json={"metadata":metadata}
    )

    print(json.dumps(response.json(), indent=6))
    ```

    Will response with:
    ```
    {
        "details": "all ok"
    }
    ```
    If the metadata validates

    Otherwise you may see errors that give you details of problems, such as:
    ```
    [
      {
            "instancePath": "/provenance/temporal/timeLag",
            "schemaPath": "#/$defs/TimeLag/enum",
            "keyword": "enum",
            "params": {
                  "allowedValues": [
                        "LESS 1 WEEK",
                        "1-2 WEEKS",
                        "2-4 WEEKS",
                        "1-2 MONTHS",
                        "2-6 MONTHS",
                        "MORE 6 MONTHS",
                        "VARIABLE",
                        "NO TIMELAG",
                        "NOT APPLICABLE",
                        "OTHER",
                        null
                  ]
            },
            "message": "must be equal to one of the allowed values"
      },
        ...

    ```

=== "CURL"

    ```
    metadata='{"metadata": '$(cat example-hdruk300.json)'}'
    curl --location 'https://hdr-gateway-traser-dev-qmnkcg5qjq-ew.a.run.app/validate?input_schema=HDRUK&input_version=3.0.0' \
    --header 'Content-Type: application/json' \
    --data "$metadata"
    ```
