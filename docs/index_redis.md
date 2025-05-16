# Redis Template

This chapter provides a comprehensive breakdown of the **`index_redis.py`** script, detailing the setup and use of Redis queues to handle job submissions within a B-Fabric web application using the `bfabric_web_apps` library.

If you're interested in a video demonstration on how to set up and register a Redis-powered Dash application using the Redis template, take a look at our tutorial: **[Deploying a Redis-Based B-Fabric App Template](deploying_video_tutorials.md#deploying-a-redis-based-b-fabric-app-template)**.

---

```{note}
**Version Compatibility Notice**  
To ensure proper functionality, the `bfabric_web_apps` library and the `bfabric_web_app_template` must have the **same version**. For example, if `bfabric_web_apps` is version `0.1.3`, then `bfabric_web_app_template` must also be `0.1.3`.  

Please verify and update the versions accordingly before running the application.
```

---

## Prerequisites

Before starting, ensure familiarity with:  
- [Dash Fundamentals](https://dash.plotly.com/layout) 
- [Dash Components](https://dash.plotly.com/dash-core-components)  
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)  
- [Dash App Object](https://github.com/plotly/dash/blob/7ba267bf9e1c956816f76900bbdbcf85dbf3ff6d/dash/dash.py#L197)  
- [bfabric_web_apps Documentation](bfabric_web_apps_functions.md)
- [Redis Documentation](https://redis.io/docs/latest/)

---

## Running the Template

To execute the template:

1. Run the following command in your terminal:  
   ```sh
   python index_redis.py
   ```
2. Open your browser and go to **localhost**.

---


## Importing Dependencies

```python
from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import bfabric_web_apps
from generic.callbacks import app
from generic.components import no_auth
```

### Explanation

* **Dash:** Used for UI components and interactions.
* **Dash Bootstrap Components:** Provides pre-styled UI elements.
* **bfabric\_web\_apps:** Contains **utilities and configurations** for seamless integration with B-Fabric. 
* **generic.callbacks:** Initializes the Dash application instance.
* **generic.components:** Contains default components for unauthorized access messages.


---

```{Important}
* The **`generic`** folder is a **core system component** and **must not be modified**. It contains shared files that handle authentication, layout, and integration with B-Fabric. Any changes may break app functionality or system compatibility.
* **All customization** should be done in **`index_large.py`**, **`index_redis.py`**, or **`index_basic.py`**.
```
---

## Setting Up Global Variables

This section defines global configuration settings required by the `bfabric_web_apps` library.

```python
bfabric_web_apps.CONFIG_FILE_PATH = "~/.bfabricpy.yml"
bfabric_web_apps.DEVELOPER_EMAIL_ADDRESS = "griffin@gwcustom.com"
bfabric_web_apps.BUG_REPORT_EMAIL_ADDRESS = "gwtools@fgcz.system"
```

### Explanation

- **CONFIG_FILE_PATH** – Defines the location of the **B-Fabric configuration file**.  
  - **Default:** "~/.bfabricpy.yml"
- **DEVELOPER_EMAIL_ADDRESS** – Specifies the developer's contact email for support.  
  - **Default:** "griffin@gwcustom.com"
- **BUG_REPORT_EMAIL_ADDRESS** – Sets the email where bug reports are sent.  
  - **Default:** "gwtools@fgcz.system"

For more details about these global variables, please refer to the chapter **[Global Variables](global_variables.md)**.

---

## Sidebar Configuration

The sidebar serves as the main user input interface for configuring jobs.

```python
sidebar = bfabric_web_apps.components.charge_switch + [
    html.P(id="sidebar_text", children="How Many Resources to Create?"),
    dcc.Slider(0, 10, 1, value=4, id='example-slider'),
    html.Br(),
    html.P(id="sidebar_text_2", children="For Which Internal Unit?"),
    dcc.Dropdown(
        options=[{'label': option, 'value': value} for option, value in zip(dropdown_options, dropdown_values)],
        value=dropdown_options[0],
        id='example-dropdown'
    ),
    html.Br(),
    html.P(id="sidebar_text_3", children="Submit job to which queue?"),
    dcc.Dropdown(
        options=[{'label': 'light', 'value': 'light'}, {'label': 'heavy', 'value': 'heavy'}],
        value='light',
        id='queue'
    ),
    html.Br(),
    dbc.Input(value='Content of Resources', id='example-input'),
    html.Br(),
    dbc.Button('Submit', id='sidebar-button'),
]
```

### Explanation

* **`charge_switch`**
  A toggle component from `bfabric_web_apps.components` that determines whether the job will be billed. For more details consult chapter **[Charge Switch](important_components.md#charge-switch)**.

* **Slider (`example-slider`)**
  Lets the user define how many resources (files) should be created. Value range: 0–10.

* **Dropdown (`example-dropdown`)**
  Selects the internal B-Fabric unit or container ID where resources will be stored.

* **Queue Selector (`queue`)**
  Allows the user to route the job to either the `'light'` or `'heavy'` Redis queue, depending on expected workload.

* **Input Field (`example-input`)**
  A simple text input field where the user can enter the content to be written into resource files.

* **Submit Button (`sidebar-button`)**
  Triggers the modal confirmation dialog before final submission.

---

## Modal Confirmation Window

A modal dialog is shown to confirm user intent before job execution begins.

```python
modal = html.Div([
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Ready to Prepare Create Workunits?")),
        dbc.ModalBody("Are you sure you're ready to create workunits?"),
        dbc.ModalFooter(dbc.Button("Yes!", id="Submit", className="ms-auto", n_clicks=0)),
    ],
    id="modal-confirmation",
    is_open=False),
])
```

### Explanation

* **Purpose**: Adds a confirmation step to prevent accidental job submissions.
* **Header/Body/Footer**: Structured using Dash Bootstrap Components.
* **Trigger**: Opens when the user clicks the initial **Submit** button from the sidebar.
* **Final Action Button**: Clicking **Yes!** (with ID `"Submit"`) initiates the job submission callback.

---

## Alert Messages

Alerts inform the user whether job submission was successful or failed.

```python
alerts = html.Div([
    dbc.Alert("Success: Workunit created!", color="success", id="alert-fade-success", dismissable=True, is_open=False),
    dbc.Alert("Error: Workunit creation failed!", color="danger", id="alert-fade-fail", dismissable=True, is_open=False),
], style={"margin": "20px"})
```

### Explanation

* **Success Alert**: Displayed when job submission and queueing succeed.
* **Error Alert**: Displayed when validation fails or an exception occurs during submission.
* **Dismissable**: Both alerts can be closed by the user.

These provide immediate visual feedback and improve user experience.

---

## Application Layout

Defines the structure of the app's visual interface using a two-column layout.

```python
app_specific_layout = dbc.Row(
    id="page-content-main",
    children=[
        dcc.Loading(alerts),
        modal,
        dbc.Col(
            html.Div(
                id="sidebar",
                children=sidebar,
                style={
                    "border-right": "2px solid #d4d7d9",
                    "height": "100%",
                    "padding": "20px",
                    "font-size": "20px",
                    "overflow-y": "scroll",
                    "overflow-x": "hidden",
                    "max-height": "65vh"
                }
            ),
            width=3,
        ),
        dbc.Col(
            html.Div(
                id="page-content",
                children=[html.Div(id="auth-div")],
                style={
                    "margin-top": "20vh",
                    "margin-left": "2vw",
                    "font-size": "20px",
                    "overflow-y": "scroll",
                    "overflow-x": "hidden",
                    "max-height": "65vh"
                }
            ),
            width=9,
        ),
    ],
    style={"margin-top": "0px", "min-height": "40vh"}
)
```

### Explanation

* **`dbc.Row`**: The main container that organizes the sidebar and content area horizontally.
* **Sidebar (`width=3`)**: Contains all user input controls, styled with borders, padding, and scrollable height.
* **Main Content (`width=9`)**: Displays dynamic authentication info (`auth-div`), entity data, and any results returned by the server.
* **`dcc.Loading`**: Wraps the alerts so that any loading states (e.g., during submission) are properly visualized.

This structure ensures the app remains responsive and user-friendly, even on smaller screens or when displaying long output.

---

## App Documentation Content

This section defines the informational content displayed within the app layout. It introduces the app to users and links to external documentation.

```python
documentation_content = [
    html.H2("Welcome to Bfabric App Template"),
    html.P([
        "This app serves as the user-interface for Bfabric App Template, "
        "a versatile tool designed to help build and customize new applications."
    ]),
    html.Br(),
    html.P([
        "It is a simple application which allows you to bulk-create resources, "
        "workunits, and demonstrates how to use the bfabric-web-apps library."
    ]),
    html.Br(),
    html.P([
        "Please check out the official documentation of ",
        html.A("Bfabric Web Apps", href="https://bfabric-docs.gwc-solutions.ch/index.html"),
        "."
    ])
]
```

### Explanation

* **`html.H2`**: Displays the documentation title at the top.
* **`html.P`**: Paragraphs explaining the app’s purpose and functionality.
* **`html.A`**: A hyperlink to the official B-Fabric Web Apps documentation.
* **`html.Br()`**: Used to add spacing between paragraphs for better visual structure.

This content is rendered in the app alongside the sidebar and main interface, providing context to new users.

---


## Setting the App Layout

The `get_static_layout()` function is a high-level utility provided by `bfabric_web_apps`. It wraps the app with a consistent layout structure and integrates documentation, configuration, and content sections into a unified interface.

```python
app_title = "Bfabric App Template"

app.layout = bfabric_web_apps.get_static_layout(
    base_title=app_title,
    main_content=app_specific_layout,
    documentation_content=documentation_content,
    layout_config={"workunits": True, "queue": True, "bug": True}
)
```

### Explanation

* **`base_title`**: Sets the page title displayed in the browser and the app header.
* **`main_content`**: The primary visual layout, including the sidebar and dynamic content area (`app_specific_layout`).
* **`documentation_content`**: The documentation section defined above.
* **`layout_config`**: Toggles display features such as:

  * `"workunits"`: Enables navigation related to workunits.
  * `"queue"`: Displays the queue selector.
  * `"bug"`: Enables the bug report submission button.

This function ensures that all apps built with `bfabric_web_apps` follow a consistent, predefined layout standard.
For more details about the `get_static_layout()` function, see the **[library documentation](important_functions.md#2-ui-and-layout-management)**.

---


## Defining the Modal Toggle Callback  

This **callback function** controls the visibility of the **confirmation modal**. It listens for clicks on both the **sidebar Submit button** and the **modal confirmation button**, toggling the modal open or closed accordingly.

```python
# This callback is necessary for the modal to pop up when the user clicks the submit button.
@app.callback(
    Output("modal-confirmation", "is_open"),
    [Input("example-button", "n_clicks"), Input("Submit", "n_clicks")],
    [State("modal-confirmation", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
```

### Explanation  
This **Dash callback** manages the open/close behavior of the confirmation modal:  
- **Inputs (`Input`)**:  
  - `example-button` – The sidebar button that **triggers the modal to open**.  
  - `Submit` – The confirmation button inside the modal, also used to **close the modal** after confirmation.  
- **State (`State`)**:  
  - Tracks the current state of the modal (`is_open`).  
- **Logic**:  
  - If either button is clicked, the modal **toggles its visibility** (open if closed, closed if open).  
  - If neither button is clicked, the modal **remains in its current state**.

This adds a safeguard confirmation step before executing any job.

---

## UI Update Callback (Authentication, Entity Data & State Control)

This callback dynamically updates the user interface based on authentication status and the current entity data. It controls the enabled/disabled state of input components, as well as the display of project-specific information.

```python
@app.callback(
    [
        Output('sidebar_text', 'hidden'),
        Output('example-slider', 'disabled'),
        Output('example-dropdown', 'disabled'),
        Output('example-input', 'disabled'),
        Output('sidebar-button', 'disabled'),
        Output('submit-bug-report', 'disabled'),
        Output('Submit', 'disabled'),
        Output('auth-div', 'children'),
    ],
    [
        Input('example-slider', 'value'),
        Input('example-dropdown', 'value'),
        Input('example-input', 'value'),
        Input('token_data', 'data'),
    ],
    [State('entity', 'data')]
)
def update_ui(slider_val, dropdown_val, input_val, token_data, entity_data):
```

### Explanation

This callback listens for changes in three user input fields and the token data. Based on authentication, it:

* Enables or disables the sidebar controls.
* Displays session and entity-specific data to the user.
* Shows a fallback message if authentication is missing.

For more details about `token_data` and `entity_data`, refer to the chapter **[Important Components](important_components.md#extracted-key-dictionaries)**.

---

### 1. Sidebar State Control Based on Authentication

```python
if token_data is None:
    sidebar_state = (True, True, True, True, True, True, True)
else:
    sidebar_state = (False, False, False, False, False, False, False)
```

**Purpose**: Disable or enable all relevant user interface elements depending on whether the user is authenticated.

* When `token_data` is `None`, the system assumes the user is **unauthenticated**. All inputs and buttons are disabled (`True`).
* If `token_data` is present, the user is authenticated, and all controls remain active (`False`).

**Controlled UI Elements**:

* `sidebar_text` (visibility)
* `example-slider`, `example-dropdown`, `example-input` (inputs)
* `sidebar-button`, `submit-bug-report`, `Submit` (action buttons)

---

### 2. Conditional UI Content Rendering

```python
if not entity_data or not token_data:
    auth_div_content = html.Div(children=no_auth)
```

**Purpose**: Render fallback content when authentication or entity information is missing.

* If either the `entity_data` or `token_data` is `None`, a default "Not authenticated" message (`no_auth`) is shown in the UI.
* This component likely includes a prompt instructing the user to re-launch the app from within B-Fabric.

---

### 3. Render Authenticated Session Details

```python
else:
    try:
        component_data = [
            html.H1("Component Data:"),
            html.P(f"Number of Resources to Create: {slider_val}"),
            html.P(f"Create workunit inside project: {dropdown_val}"),
            html.P(f"Resource Content: {input_val}")
        ]
```

**Purpose**: If the user is authenticated, the left column (`component_data`) displays a summary of the current UI input values.

* The user sees how many resources they've selected via the slider.
* The selected container/project is shown.
* The text input is echoed back for clarity.

---

```python
        entity_details = [
            html.H1("Entity Data:"),
            html.P(f"Entity Class: {token_data['entityClass_data']}"),
            html.P(f"Entity ID: {token_data['entity_id_data']}"),
            html.P(f"Created By: {entity_data['createdby']}"),
            html.P(f"Created: {entity_data['created']}"),
            html.P(f"Modified: {entity_data['modified']}")
        ]
```

**Purpose**: The right column (`entity_details`) displays metadata from the current B-Fabric entity.

* **`entityClass_data`** and **`entity_id_data`** come from the decoded token and identify the session context.
* **`createdby`**, **`created`**, and **`modified`** provide audit information from the entity record itself.

---

```python
        auth_div_content = dbc.Row([dbc.Col(component_data), dbc.Col(entity_details)])
```

**Purpose**: Renders both sections side-by-side in a responsive layout using Bootstrap columns.

* `dbc.Col` creates two vertical sections:

  * Left: Live input summary
  * Right: Entity metadata

---

### 4. Exception Handling

```python
    except Exception as e:
        return (*sidebar_state, html.P(f"Error Logging into B-Fabric: {str}"))
```

**Purpose**: If any error occurs while rendering the data (e.g., missing keys), an error message is shown in the `auth-div`.

* This protects the app from crashing on malformed `token_data` or `entity_data`.
* The error message helps with debugging during development.

---

### 5. Final Return

```python
return (*sidebar_state, auth_div_content)
```

**Purpose**: The function returns a tuple of:

1. The enable/disable state for 7 UI components.
2. The dynamically generated HTML layout for `auth-div`, containing either:

   * The fallback message (`no_auth`)
   * The component + entity data grid
   * An error message

This ensures the app reacts immediately to authentication changes and maintains UI consistency.

---

## Submitting Jobs with Redis Queue

This section explains how the app submits jobs using the `run_main_job` function via a Redis queue. This architecture is ideal for long-running or compute-intensive workflows that should be executed asynchronously on a background worker.

---

### Callback Definition

```python
@app.callback(
    [
        Output("alert-fade-success", "is_open"),
        Output("alert-fade-fail", "is_open"),
        Output("alert-fade-fail", "children"),
        Output("refresh-workunits", "children")
    ],
    [Input("Submit", "n_clicks")],
    [
        State("example-slider", "value"),
        State("example-dropdown", "value"),
        State("example-input", "value"),
        State("token_data", "data"),
        State("queue", "value"),
        State("charge_run", "on"),
        State('url', 'search')
    ],
    prevent_initial_call=True
)
```

This callback is triggered when the user clicks the **Submit** button inside the modal. It retrieves user inputs and session state, builds a job specification, and submits it to the Redis queue.

---

### Explanation of Inputs, States, and Outputs

#### Inputs

* `Submit (n_clicks)`: Triggers job submission after confirmation.

#### States

* `example-slider`: Number of resources to create (e.g., 0–10).
* `example-dropdown`: Selected project/container ID.
* `example-input`: Text input to be written into each resource file.
* `token_data`: Authentication and session state from B-Fabric.
* `queue`: Target Redis queue (`light`, `heavy`, etc.).
* `charge_run`: Boolean switch to indicate whether costs should be tracked.
* `url`: Raw B-Fabric token passed from the URL.

#### Outputs

* `alert-fade-success`: Shows success alert when job is submitted.
* `alert-fade-fail`: Shows error message if submission fails.
* `refresh-workunits`: Dummy trigger to update workunits.

---

### Submission Logic and Redis Execution

Each step of the job submission is explained below. For full details about `run_main_job`, see the **[library documentation](important_functions.md#main-job-execution)**.

---

#### Step 1 – Validate the Container Selection

```python
if dropdown_val:
    container_id = int(dropdown_val)
else:
    return False, True, "Error: No container ID provided", html.Div()
```

Ensures a valid project or container ID has been selected. If not, an error alert is returned immediately and the function exits.

---

#### Step 2 – Re-validate the Token

```python
token, tdata, entity_data, app_data, _, _, _ = bfabric_web_apps.process_url_and_token(raw_token)

if token is None or tdata is None or entity_data is None or app_data is None: 
    return False, True, f"Your session has expired. Please invoke the app again from B-Fabric: {token_data.get('webbase_data')}", html.Div()
```

Re-processes the raw token to ensure the session is still valid. If authentication has expired or the token is malformed, the user is prompted to reopen the app via B-Fabric.

---

#### Step 3 – Define Example Attachments

```python
attachment1_content = b"<html><body><h1>Hello World</h1></body></html>"
attachment1_name = f"attachment_1.html"

attachment2_content = b"<html><body><h1>Hello World a second time!!</h1></body></html>"
attachment2_name = f"attachment_2.html"
```

Creates two sample HTML files as byte strings. These files will be attached as links to the corresponding entity. In real-world applications, they could represent QC reports or log files.

---

#### Step 4 – Package Attachments for Transfer

```python
files_as_byte_strings = {
    attachment1_name: attachment1_content,
    attachment2_name: attachment2_content
}
```

Maps filenames to their byte content. These will be sent to the external compute server before job execution begins.

---

#### Step 5 – Generate Resource Files via Bash

```python
bash_commands = [f"echo '{input_val}' > resource_{i+1}.txt" for i in range(slider_val)]
```

Generates a list of Bash commands. Each command writes the user’s input into a separate file (`resource_1.txt`, `resource_2.txt`, etc.).

---

#### Step 6 – Prepare Charging Information

```python
project_id = "2220"

if charge_run and project_id:
    charge_run = [project_id]
else:
    charge_run = []
```

If charging is enabled and a valid project ID exists, it’s added to the `charge` list. This list tells B-Fabric which container should be billed.
For full details about `charging`, see the **[library documentation](important_components.md#charge-switch)**.

---

#### Step 7 – Define Attachment and Resource Paths

```python
attachment_paths = {
    attachment1_name: attachment1_name,
    attachment2_name: attachment2_name
}

resource_paths = {
    f"resource_{i+1}.txt": container_id for i in range(slider_val)
}
```

* `attachment_paths`: Maps file names to their display names in B-Fabric.
* `resource_paths`: Associates each generated resource with the target container ID.

---

#### Step 8 – Assemble Submission Arguments

```python
arguments = {
    "files_as_byte_strings": files_as_byte_strings,
    "bash_commands": bash_commands,
    "resource_paths": resource_paths,
    "attachment_paths": attachment_paths,
    "token": raw_token,
    "service_id": bfabric_web_apps.SERVICE_ID,
    "charge": charge_run
}
```

This dictionary contains everything required by `run_main_job`:

* What files to copy
* What commands to run
* Where to register results
* How to apply billing

---

#### Step 9 – Enqueue the Job to Redis

```python
bfabric_web_apps.q(queue).enqueue(
    bfabric_web_apps.run_main_job,
    kwargs=arguments
)
```

Sends the job to the Redis queue (`light` or `heavy`). The background worker will:

* Write all files
* Run the commands
* Register all outputs in B-Fabric

This allows the web app to remain responsive while the job is executed asynchronously.

For more details on the `run_main_job()` function, refer to the **[Library Documentation](important_functions.md#main-job-execution)**.

---

#### Step 10 – Return Success State

```python
return True, False, None, html.Div()
```

If everything completes successfully, the success alert is triggered and no error message is shown.

---

#### Step 11 – Handle Errors Gracefully

```python
except Exception as e:
    return False, True, f"Error: Workunit creation failed: {str(e)}", html.Div()
```

If anything fails (e.g., token is invalid, job submission fails, queue is down), the function catches the exception and shows the error message in the red alert box.

---

## Running the Application

The following section ensures the application executes on the specified host and port configuration.

```python
if __name__ == "__main__":
    app.run(debug=False, port=bfabric_web_apps.PORT, host=bfabric_web_apps.HOST)
```

### Explanation

* Runs the Dash server, respecting settings defined by the global configuration (`bfabric_web_apps.PORT`, `bfabric_web_apps.HOST`).
