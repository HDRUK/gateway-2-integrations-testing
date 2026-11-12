---
title: Delete a dataset
description: DELETE a dataset from the Gateway.
tags:
  - api
  - datasets
---

Deleting an dataset using `DELETE` on the endpoint [`/api/v1/integrations/datasets/{id}`](https://api.dev.hdruk.cloud/api/documentation#/Datasets/delete_datasets_integrations)
=== " python "

    ```python

    response = requests.delete(
        f"{api_path}integrations/datasets/<dataset_id>",
        headers=headers
    )


    ```

=== "CURL"

    ```bash
    curl -X DELETE \
            --location 'https://api.dev.hdruk.cloud/api/v1/integrations/datasets/<dataset_id>' \
            --header 'x-application-id: <application id>' \
            --header 'x-client-id: <client id>' \
    ```

If successful, this returns

```
{
    "message": "success"
}
```

Please see the previous page regarding dataset creation (`Using the API > Datasets > Create`) for details of the likely error messages you may receive from the `DELETE` endpoint.
