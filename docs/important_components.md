# Important Components

This section introduces the most critical variables and data structures used in a B-Fabric Web App session. These components are automatically extracted from the B-Fabric token and are reused across callbacks to personalize and configure the session dynamically.

---

## App Data

**App data** holds metadata about the currently running web application.

Example:
```python
app_data = {
    'id': 543,
    'name': 'RNAseq',
    'description': 'A web application designed to run the nf-core RNA-seq pipeline.'
}
```

---

## Entity Data

**Entity data** describes the dataset or project associated with the app session. This typically includes metadata, sample information, and file references.

Example:
```python
entity_data = {
    'name': 'Uploaded FASTQ Dataset (Run 1913)',
    'createdby': 'lopitz',
    'created': '2013-03-28 13:27:49',
    'modified': '2025-04-16 13:01:14',
    'full_api_response': {...}  # Full dataset metadata
}
```

---

## Token Data

**Token data** includes session metadata, such as the authenticated user, session expiry time, application info, and dataset ID.

Example:
```python
token_data = {
    'environment': 'Test',
    'user_data': 'appdeveloper',
    'token_expires': '2025-05-01 22:54:56',
    'entity_id_data': '2220',
    'entityClass_data': 'Dataset',
    'webbase_data': 'https://fgcz-bfabric-test.uzh.ch/bfabric',
    'application_params_data': {},
    'application_data': '543',
    'userWsPassword': 'bdab8b2413c2b2dc2d7bc2fb994dd080',
    'jobId': '2010'
}
```

---

## Charge Switch

The charge switch is used to assign costs for running applications to specific containers and services in B-Fabric.

Example implementation:
```python
from bfabric_web_apps.utils.get_logger import get_logger
from bfabric_web_apps.utils.get_power_user_wrapper import get_power_user_wrapper

def create_charge(token_data, container_id, service_id):
    L = get_logger(token_data)
    wrapper = get_power_user_wrapper(token_data)
    usr_id = wrapper.read("user", {"login": token_data.get("user_data")})[0]['id']

    charge_data = {
        "serviceid": service_id,
        "containerid": container_id,
        "chargerid": usr_id
    }

    charge = L.logthis(
        api_call=wrapper.save,
        endpoint="charge",
        obj=charge_data,
        params=None,
        flush_logs=True
    )

    return charge
```

---

## Authentication & Token Handling

The B-Fabric authentication system ensures secure access and links users to specific datasets and apps.

![Authentication Token Flow](_images/Authentication_Token_Flow.png)

### Flow Overview

1. **Token sent via URL**  
   `https://some.webapp/param1?token=abcxyz123`

2. **Web app validates the token** using FGCZ’s REST endpoint.

3. **B-Fabric responds** with a JSON payload of auth data.

4. **Web app uses credentials** to fetch entity and app metadata.

---

### process_url_and_token()

This utility extracts token data from the URL and populates global variables.

```python
process_url_and_token(url_params)
```

### Return Tuple:
```python
(token, token_data, entity_data, app_data, page_title, session_details, job_link)
```

---

## Example Dash Callback

```python
@app.callback(
    [
        Output('token', 'data'),
        Output('token_data', 'data'),
        Output('entity', 'data'),
        Output('app_data', 'data'),
        Output('page-title', 'children'),
        Output('session-details', 'children'),
        Output('dynamic-link', 'href')
    ],
    [Input('url', 'search')]
)
def generic_process_url_and_token(url_params):
    return process_url_and_token(url_params)
```