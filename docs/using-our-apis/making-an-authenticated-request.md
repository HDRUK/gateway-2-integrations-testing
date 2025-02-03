# Making an authenticated request
To make an authenticated request to our API, you need to ensure that you have a Private App configured on the Gateway, and have taken note of the `app_id` and `client_id`. These credentials must be included in the headers of any API requests where you are managing data.

## Code Examples
The code examples below demonstrate how to make an authenticated request to the Gateway API using a simple get request for a dataset. Please make sure you replace `YOUR_APP_ID` and `YOUR_CLIENT_ID` with the actual `app_id` and `client_id` you obtained when creating a Private App.

You can also test our APIs from the Swagger documentation in the link below.
[https://api.healthdatagateway.org/api/documentation#/](https://api.healthdatagateway.org/api/documentation#/)


=== "CURL"

    ``` bash
    curl -X GET "https://api.healthdatagateway.org/api/v1/integrations/datasets" \
        --header "x-application-id: <YOUR_APP_ID >" \
        --header "x-client-id: <YOUR_CLIENT_ID>"
    ```

=== " python "

    ``` python
    import requests

    url = "https://api.healthdatagateway.org/api/v1/integrations/datasets"
    headers = {
        "x-application-id": <YOUR_APP_ID>,
        "x-client-id": <YOUR_CLIENT_ID>
    }

    response = requests.get(url, headers)
    print(response.json())

    ```

=== " Node.js "

    ``` js
    const axios - require('axios')

    const url = "https://api.healthdatagateway.org/api/v1/integrations/datasets";
    const headers = {
        "x-application-id": <YOUR_APP_ID>,
        "x-client-id": <YOUR_CLIENT_ID>
    };

    axios.get(url, {headers: headers})
        .then(response => (
            console.log(response.data);
        ))
        .catch(error => {
            console.error(error);
        });
    ```

=== " C++ "

    ``` cpp
    #include <iostream>
    #include <curl/curl.h>

    int main() {
        CURL *curl;
        CURLcode res;

        curl = curl_easy_init();
        if(curl){
            curl_easy_setopt(curl, CURLOPT_URL, "https://api.healthdatagateway.org/api/v1/integrations/datasets");

            struct curl_slist *headers = NULL;
            headers - curl_slist_append(headers, "x-application-id: <YOUR_APP_ID>");
            headers - curl_slist_append(headers, "x-client-id: <YOUR_CLIENT_ID>");
            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

            res = curl_easy_perform(curl);

            curl_slist_freee_all(headers);
            curl_easy_cleanup(curl);
        }
        return 0
    }
    ```

=== " Go "

    ``` go
    package main

    import {
        "fmt"
        "io/ioutil"
        "net/http"
    }

    func main(){
        client := &http.Client{}
        req, err := http.NewRequest("GET", "https://api.healthdatagateway.org/api/v1/integrations/datasets", nil)
        if err != nil {
            panic(err)
        }

        req.Header.Add("x-application-id", <YOUR_APP_ID>)
        req.Header.Add("x-client-id", <YOUR_CLIENT_ID>)

        resp, err : client.Do(req)
        if err != nil {
            painc(err)
        }
        defer resp.Body.Close()

        body, err := ioutil.ReadAll(resp.body)
        if err != nil {
            panic(err)
        }

        fmt.Println(string(body))
    }
    ```
