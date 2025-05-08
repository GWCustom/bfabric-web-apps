# Important Components

This section introduces the most important components when working with the `bfabric_web_apps` library. It begins by explaining the **authentication and token handling** process, which is the foundation for securely linking users, datasets, and applications. Next, it covers the **key dictionaries** that are extracted from the token, such as `app_data`, `entity_data`, and `token_data`. Finally, it presents an important out-of-the-box UI component: the **Charge Switch**, which enables users to manage cost attribution within their B-Fabric workflows.

---

## Authentication & Token Handling

The B-Fabric authentication system ensures secure access to web applications and links each session to a specific dataset and user identity. This process enables personalized behavior and access control for each user.

![Authentication Token Flow](_images/Authentication_Token_Flow.png)

### Flow Overview

1. **Token sent via URL**
   A user accesses the app with a B-Fabric token included as a URL parameter.
   Example:
   `https://some.webapp/param1?token=abcxyz123`

2. **Web app validates the token**
   The app uses a REST API call to the B-Fabric backend to confirm the validity of the token.

3. **B-Fabric responds**
   If the token is valid, the backend returns a JSON payload with metadata about the user, app, and linked dataset.

4. **Web app uses the credentials**
   The app extracts relevant data from the response to configure the session, display context-specific information, and pre-fill app components.

---

The **[`process_url_and_token`](important_functions.md#authentication-token-handling)** function is a central utility used in almost every app built with `bfabric_web_apps`. It extracts the token from the URL and transforms the backend response into structured dictionaries that are reused across callbacks.

```python
process_url_and_token(url_params)
```

The function returns a tuple with the following elements:

```python
(token, token_data, entity_data, app_data, page_title, session_details, job_link)
```

Among these, the most important for downstream app logic are the dictionaries: `token_data`, `entity_data`, and `app_data`. These are explained in detail in the next section.

---

## Extracted Key Dictionaries

### App Data

**What is it?**
App data contains metadata related to the specific B-Fabric application currently running in the session.

**Structure Overview:**

* `id`: App ID in B-Fabric
* `name`: App name
* `description`: A brief explanation of the app’s purpose

**Example:**

```python
app_data = {
    'id': 543,
    'name': 'RNAseq',
    'description': 'A web application designed to run the nf-core RNA-seq pipeline.'
}
```

---


### Entity Data

**What is it?**
`entity_data` represents the full metadata of a dataset retrieved from B-Fabric. It contains general dataset metadata (creator, timestamps, ID), schema definitions (attributes), associated files, links to other B-Fabric objects, and a detailed item-level structure. This data is typically the basis for what the app will visualize, process, or submit as a job.

---

**Structure Overview:**

| Key                 | Description                                                                         |
| ------------------- | ----------------------------------------------------------------------------------- |
| `name`              | Human-readable name/title of the dataset.                                           |
| `createdby`         | Username of the user who originally uploaded or created the dataset.                |
| `created`           | Timestamp when the dataset was first created.                                       |
| `modified`          | Timestamp of the most recent modification.                                          |
| `full_api_response` | Complete raw metadata response from B-Fabric, including all subfields listed below. |

The actual B-Fabric metadata is located inside the `full_api_response` key, and includes the following keys:

| Sub-Key in `full_api_response` | Description                                                                                        |
| ------------------------------ | -------------------------------------------------------------------------------------------------- |
| `modifiedby`                   | Username of the last user who modified the dataset.                                                |
| `classname`                    | B-Fabric class of the object (typically `'dataset'`).                                              |
| `id`                           | Unique internal dataset ID.                                                                        |
| `container`                    | Dictionary with `classname` and `id` of the linked project or container.                           |
| `attribute`                    | List of dictionaries describing the dataset schema: `name`, `position`, and `type`.                |
| `item`                         | List of data rows. Each row has a `position` and a list of `field` entries (linked to attributes). |
| `numberofattributes`           | Number of columns (attributes) in the dataset.                                                     |
| `numberofitems`                | Number of rows (samples/items) in the dataset.                                                     |
| `link`                         | List of links (e.g., to resources like files), each with `classname` and `id`.                     |

---

**Example:**

```python
entity_data = {
    'name': 'Uploaded FASTQ Dataset (Run 1913)',
    'createdby': 'lopitz',
    'created': '2013-03-28 13:27:49',
    'modified': '2025-04-16 13:01:14',
    'full_api_response': {
        'modifiedby': 'gfeeder',
        'classname': 'dataset',
        'id': 2220,
        'container': {'classname': 'project', 'id': 703},
        'attribute': [
            {'name': 'Sample', 'position': '1', 'type': 'String'},
            {'name': 'FASTQ Read 1', 'position': '2', 'type': 'Resource'},
            {'name': 'FASTQ Read 2', 'position': '3', 'type': 'Resource'},
            {'name': 'Strandedness', 'position': '4', 'type': 'String'}
        ],
        'item': [
            {
                'position': '1',
                'field': [
                    {'attributeposition': '1', 'value': 'Run_1913_10'},
                    {'attributeposition': '2', 'value': '/path/to/R1_001.fastq.gz'},
                    {'attributeposition': '3', 'value': '/path/to/R2_001.fastq.gz'},
                    {'attributeposition': '4', 'value': 'auto'}
                ]
            },
            # Additional sample rows...
        ],
        'numberofattributes': '4',
        'numberofitems': '6',
        'link': [
            {'classname': 'link', 'id': 84502},
            {'classname': 'link', 'id': 84503},
            # Additional links...
        ]
    }
}
```

---

### Token Data

**What is it?**
Token data includes session-specific metadata like the authenticated user, app ID, dataset ID, and token expiry time.

**Structure Overview:**

* `environment`: Deployment environment (e.g., Test, Production)
* `user_data`: Username associated with the token
* `token_expires`: Expiry timestamp of the session token
* `entity_id_data`: ID of the selected entity (usually a dataset)
* `entityClass_data`: Type of the entity (e.g., `Dataset`)
* `webbase_data`: Base URL of the B-Fabric server
* `application_data`: App ID
* `application_params_data`: Optional app parameters
* `userWsPassword`: Web service password (for programmatic access)
* `jobId`: Linked job ID, if any

**Example:**

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
    'userWsPassword': 'dummypassword',
    'jobId': '2010'
}
```

---

## Charge Switch

### What Is It?

The **Charge Switch** is a predefined UI component that allows users to control whether the cost of running a job should be charged to a specific B-Fabric container (e.g., project, dataset). It integrates seamlessly into your Dash app and connects with the `run_main_job` function to enable or disable automatic service charging.

This is especially useful in shared computing environments where resource usage must be tracked and billed to the correct entity.

---

### How It Works

* When toggled **on**, the switch returns `True`, indicating that the job execution should be charged.
* When toggled **off**, it returns `False`, and no charge will be made.
* The switch is connected to a callback via `State("charge_run", "on")` and is typically used in conjunction with a project ID to populate the `charge` list.

---

### UI Integration (Sidebar Example)

You can embed the charge switch directly into your sidebar layout using the `charge_switch` component provided by the `bfabric_web_apps.components` module:

```python
from bfabric_web_apps.components import charge_switch

sidebar = charge_switch + [
    html.P("Select Lane:"),
    dcc.Dropdown(
        id="lane-dropdown",
        options=[],  # Populate dynamically
        value=None,
    ),
    html.Br(),
    html.P("Submit job to which queue?"),
    dcc.Dropdown(
        options=[
            {'label': 'light', 'value': 'light'},
            {'label': 'heavy', 'value': 'heavy'}
        ],
        value='light',
        id='queue'
    ),
    html.Br(),
    dbc.Button('Submit', id='example-button'),
]
```

This layout inserts the switch at the top of the sidebar, followed by your workflow-specific inputs and the submit button.

---

### Return Value

The charge switch returns a **Boolean** value (`True` or `False`), which you can access in a callback using:

```python
State("charge_run", "on")
```

This Boolean value determines whether the computation should be billed.

---

### Usage in a Callback

You can use the return value to conditionally create a list of container IDs to be charged. If `charge_run = False`, the `charge` list will be empty. If it is `True`, it will be a list populated with the corresponding `project_id`.

```python
if charge_run and project_id:
    charge = [project_id]
else:
    charge = []
```

This list is then passed to the `run_main_job` function as the `charge` parameter.

---

### Example: Passing the Charge Parameter to `run_main_job` via Redis

```python
q(queue).enqueue(run_main_job, kwargs={
    "files_as_byte_strings": files_as_byte_strings,
    "bash_commands": bash_commands,
    "resource_paths": resource_paths,
    "attachment_paths": attachment_paths,
    "token": url_params,
    "service_id": bfabric_web_apps.SERVICE_ID,
    "charge": charge  # Populated using the switch
})
```

If the switch is off, `charge` will be an empty list (`[]`), and no billing occurs. If the switch is on and a valid `project_id` is available, the execution will be billed accordingly.

---

### Summary

| Feature            | Description                                                               |
| ------------------ | ------------------------------------------------------------------------- |
| Component ID       | `charge_run`                                                              |
| Return Value       | `True` (on) or `False` (off)                                              |
| Purpose            | Allows end users to choose whether or not to charge the current execution |
| Integration Target | `run_main_job(..., charge=[...])`                                         |
