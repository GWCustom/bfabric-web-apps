# Documentation for `index_redis.py`

This chapter provides a comprehensive breakdown of the **index\_redis.py** script, detailing the setup and use of Redis queues for handling job submissions within a B-Fabric web application.

---

```{note}
**Version Compatibility Notice**  
To ensure proper functionality, the `bfabric_web_apps` library and the `bfabric_web_app_template` must have the **same version**. For example, if `bfabric_web_apps` is version `0.1.3`, then `bfabric_web_app_template` must also be `0.1.3`.  

Please verify and update the versions accordingly before running the application.
```

---

## Importing Dependencies

```python
from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import bfabric_web_apps
from generic.callbacks import app
from generic.components import no_auth
from pathlib import Path
```

### Explanation

* **Dash:** Used for UI components and interactions.
* **Dash Bootstrap Components:** Provides pre-styled UI elements.
* **bfabric\_web\_apps:** Utilities for integrating the app with B-Fabric.
* **generic.callbacks:** Initializes the Dash application instance.
* **generic.components:** Contains default components for unauthorized access messages.
* **Pathlib:** Assists in managing file paths.

---

## Setting Up Default Configuration

```python
bfabric_web_apps.CONFIG_FILE_PATH = "~/.bfabricpy.yml"
bfabric_web_apps.DEVELOPER_EMAIL_ADDRESS = "griffin@gwcustom.com"
bfabric_web_apps.BUG_REPORT_EMAIL_ADDRESS = "gwtools@fgcz.system"
```

### Explanation

* Sets global configuration values required for running the application.

---

## Sidebar Configuration

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

* The sidebar allows user interaction to specify resource details and choose a processing queue.

---

## Modal Confirmation Window

```python
modal = html.Div([
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Ready to Prepare Create Workunits?")),
        dbc.ModalBody("Are you sure you're ready to create workunits?"),
        dbc.ModalFooter(dbc.Button("Yes!", id="Submit", className="ms-auto", n_clicks=0)),],
    id="modal-confirmation",
    is_open=False,),
])
```

### Explanation

* Provides a confirmation step before proceeding with job creation to prevent unintended submissions.

---

## Alert Messages

```python
alerts = html.Div([
    dbc.Alert("Success: Workunit created!", color="success", id="alert-fade-success", dismissable=True, is_open=False),
    dbc.Alert("Error: Workunit creation failed!", color="danger", id="alert-fade-fail", dismissable=True, is_open=False),
], style={"margin": "20px"})
```

### Explanation

* Alerts provide immediate feedback on job submission outcomes.

---

## Application Layout

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
                    "overflow-y":"scroll",
                    "overflow-x":"hidden",
                    "max-height":"65vh"
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
                    "overflow-y":"scroll",
                    "overflow-x":"hidden",
                    "max-height":"65vh"
                }
            ),
            width=9,
        ),
    ],
    style={"margin-top": "0px", "min-height": "40vh"}
)
```

### Explanation

* Two-column layout with sidebar for inputs and main content area displaying authentication and resource details.

---

## Redis Queue Job Submission Callback

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
def submission(n_clicks, slider_val, dropdown_val, input_val, token_data, queue, charge_run, raw_token):
    try:
        arguments = {
            "files_as_byte_strings": {
                "attachment_1.html": b"<html><body><h1>Hello World</h1></body></html>",
                "attachment_2.html": b"<html><body><h1>Hello World a second time!!</h1></body></html>"
            },
            "bash_commands": [f"echo '{input_val}' > resource_{i+1}.txt" for i in range(slider_val)],
            "resource_paths": {f"resource_{i+1}.txt": int(dropdown_val) for i in range(slider_val)},
            "attachment_paths": {"attachment_1.html": "attachment_1.html", "attachment_2.html": "attachment_2.html"},
            "token": raw_token,
            "service_id": bfabric_web_apps.SERVICE_ID,
            "charge": ["2220"] if charge_run else []
        }
        bfabric_web_apps.q(queue).enqueue(bfabric_web_apps.run_main_job, kwargs=arguments)
        return True, False, None, html.Div()
    except Exception as e:
        return False, True, f"Error: Workunit creation failed: {str(e)}", html.Div()
```

### Explanation

* Manages job submission using Redis queues.
* Prepares files, resources, and commands based on user input.
* Handles exceptions gracefully, providing error feedback.

---