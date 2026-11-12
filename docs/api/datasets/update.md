---
title: Update a dataset
description: PUT a new version of your dataset metadata.
tags:
  - api
  - datasets
---

Using the `PUT` method to [`/api/v1/integrations/datasets/{id}`](https://api.dev.hdruk.cloud/api/documentation#/Datasets/update_datasets_integrations) you can update your dataset metadata with a new _version_.

=== " python "

    ```python

    response = requests.put(
        f"{api_path}/integrations/datasets/",
        headers=headers,
        json={"metadata": metadata},
    )

    ```

=== "CURL"

    ```
    curl -X PUT \
        --location 'https://api.dev.hdruk.cloud/api/v1/integrations/datasets/<dataset_id>' \
        --header 'x-application-id: <your app ID >' \
        --header 'x-client-id: <your client ID >' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "metadata": {<JSON metadata conforming to supported schema>}
        }'
    ```

Running this returns a structure like:

```
{
      "message": "success",
      "data": {
            "id": 875,
            ...
            "create_origin": "API",
            "status": "ACTIVE",
            "versions": [
                  {
                        "id": 875,
                        ...
                  },
                  {
                        "id": 882,
                        ...
                  },
                  ...
            ]
      }
}
```

This shows the data we now hold for this dataset (i.e. multiple versions as you have now updated your dataset with a new version).

### Errors

Please see the previous page regarding dataset creation (`Using the API > Datasets > Create`) for details of the likely error messages you may receive from the `PUT` endpoint.
