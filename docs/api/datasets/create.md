---
title: Create a dataset
description: POST metadata to the Gateway integrations endpoint to create a dataset.
tags:
  - api
  - datasets
---

The endpoint [`/api/v1/integrations/datasets`](https://api.dev.hdruk.cloud/api/documentation#/Datasets/create_datasets_integrations) should be used to create dataset(s) on the gateway by posting metadata describing these datasets to our API endpoint.

You should POST application/JSON data to the endpoint where your metadata validates against one of [our supported schemas](https://github.com/HDRUK/schemata-2/blob/master/available.json)

```json
{"metadata": <metadata>}
```

=== " python "

    Initialise your request client
    ``` python
    import requests
    import json


    client_id = <your client id>
    app_id = <your app id>

    api_path = "https://api.dev.hdruk.cloud/api/v1"


    headers = {
        "x-client-id": client_id,
        "x-application-id": app_id,
        "Content-Type": "application/json",
    }

    metadata = {"metadata": <JSON metadata conforming to supported schema>}


    response = requests.post(
        f"{api_path}/integrations/datasets",
        headers=headers,
        json=metadata
    )

    print(json.dumps(response.json(), indent=6))
    ```

=== "CURL"

    ```
    curl --location 'https://api.dev.hdruk.cloud/api/v1/integrations/datasets' \
        --header 'x-application-id: <your app ID >' \
        --header 'x-client-id: <your client ID >' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "metadata": {<JSON metadata conforming to supported schema>}
        }'
    ```

Running this returns:

```json
    {
        "message": "created",
        "data": <dataset_id : Integer>,
        "version": <dataset_version_id: Integer>
    }
```

You should make a record of the dataset ID that is returned in the `data` field when the dataset is created. There are various endpoints that you can use to retrieve all your datasets and the IDs for them.

### Errors

Please find below a summary of likely errors and their meanings.

#### Unauthorised permissions to create

If your app did enable permissions to create a dataset then you'll see the following response (code `400`).

```json
{
      "code": 400,
      "message": "Application permissions do not allow this request",
      "details": {...}
}
```

This will need fixing on the Permissions tab for the app.

#### No x-application-id or x-client-id in your headers

```json
{
    "code": 401,
    "message": "Please provide a x-application-id and x-client-id in your headers",
    "details": ...
}
```

You must set these in the request headers. To find the values of these identifiers, navigate (on the Gateway) to `Integrations > API Management page > Manage API`, select your App, make sure it is set to 'Enabled' on the 'App Info' tab, and then click on the 'Authentication' tab to find the Client ID and App ID.

#### Invalid App credentials

App ID and Client ID have been supplied, but don't match an existing integration. Please check you have copied the credentials correctly.

```json
{
    "code": 401,
    "message": "No known integration matches the credentials provided"
    ...
}
```

#### App not enabled

```json
{
    "code": 400,
    "message": "Application has not been enabled!",
    ...
}
```

Navigate (on the Gateway) to `Integrations > API Management > Manage API`, and select the App. Ensure the App is set to 'Enabled' on the 'App Info' tab.

#### Invalid format

```json
{
      "message": "metadata is in an unknown format and cannot be processed",
      "details": {
            "traser_message": {
                  "message": "Input metadata object matched no known schemas",
                  "details": {
                        "available_schemas": {
                              "HDRUK": [
                                    "2.1.2",
                                    "2.1.3",
                                    "2.1.0",
                                    "2.0.2",
                                    "2.2.1",
                                    "2.2.0",
                                    "3.0.0"
                              ],
                              "GWDM": [
                                    "1.0",
                                    "1.1",
                                    "1.2",
                                    "2.0"
                              ],
                              "SchemaOrg": [
                                    "default",
                                    "BioSchema",
                                    "GoogleRecommended"
                              ]
                        }
                  }
            },
            "wasTranslated": false,
            "metadata": null,
            "statusCode": 400
      }
}
```

The supplied metadata is not in any valid format. Use the TRASER `find` endpoint (navigate within these docs to `Metadata > Validate`) to understand the reasons for invalidity.
