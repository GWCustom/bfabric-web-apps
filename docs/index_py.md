# Full-Featured Template

This chapter provides a step-by-step breakdown of the **index_large.py** script. It explains key functions and their roles in setting up a B-Fabric web application.

---

```{note}
**Version Compatibility Notice**  
To ensure proper functionality, the `bfabric_web_apps` library and the `bfabric_web_app_template` must have the **same version**. For example, if `bfabric_web_apps` is version `0.1.3`, then `bfabric_web_app_template` must also be `0.1.3`.  

Please verify and update the versions accordingly before running the application.
```

---


## View the Demo

Before diving into the details, you can preview a **live demo** of this template:  

[View the Demo](https://template-d12.bfabric.org/)  

This will give you an idea of how the **Full-Featured Template** looks and functions.

---

## Prerequisites

Before starting, ensure familiarity with:  
- [Dash Fundamentals](https://dash.plotly.com/layout) 
- [Dash Components](https://dash.plotly.com/dash-core-components)  
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)  
- [Dash App Object](https://github.com/plotly/dash/blob/7ba267bf9e1c956816f76900bbdbcf85dbf3ff6d/dash/dash.py#L197)  
- [bfabric_web_apps Documentation](bfabric_web_apps_functions.md)  


---

## Running the Template

To execute the template:

1. Run the following command in your terminal:  
   ```sh
   python index_large.py
   ```
2. Open your browser and go to **localhost**.

---

## Importing Dependencies  

This section covers the **necessary imports** that make the template functional.  

```python
from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import bfabric_web_apps
from generic.callbacks import app
from generic.components import no_auth
```

### Explanation  

1. **Dash Imports**  
   - `html` and `dcc`: Used to construct the app layout.  
   - `Input`, `Output`, and `State`: Required for callback interactions.  

2. **Dash Bootstrap Components (DBC)**  
   - Provides **pre-styled UI elements** to enhance the look and functionality of the app.  

3. **bfabric_web_apps**  
   - Contains **utilities and configurations** for seamless integration with B-Fabric.  

4. **Generic Callbacks B-Fabric app Import**  
   - `app`: The **Dash instance** that initializes and runs the web app.

5. **Generic B-Fabric no_auth Import**  
   - `no_auth`: Message displayed in the UI to users who are not authenticated.

---

```{Important}
* The **`generic`** folder is a **core system component** and **must not be modified**. It contains shared files that handle authentication, layout, and integration with B-Fabric. Any changes may break app functionality or system compatibility.
* **All customization** should be done in **`index_large.py`**, **`index_redis.py`**, or **`index_basic.py`**.
```

---


## Defining the Sidebar  

The **sidebar** serves as the **left-hand panel** of the application, providing interactive elements for user input. It includes a **slider, dropdown menu, text input field, and a submit button**, allowing users to configure values before submitting data.  

```python

# Predefine dropdown options / values
dropdown_options = ['Genomics (project 2220)', 'Proteomics (project 3000)', 'Metabolomics (project 31230)']
dropdown_values = ['2220', '3000', '31230']

sidebar = bfabric_web_apps.components.charge_switch + [
    html.P(id="sidebar_text", children="How Many Resources to Create?"),  # Sidebar header text.
    dcc.Slider(0, 10, 1, value=4, id='example-slider'),  # Slider for selecting a numeric value.
    html.Br(),
    html.P(id="sidebar_text_2", children="For Which Internal Unit?"),
    dcc.Dropdown(
        options=[{'label': option, 'value': value} for option, value in zip(dropdown_options, dropdown_values)],
        value=dropdown_options[0],
        id='example-dropdown'  # Dropdown ID for callback integration.
    ),
    html.Br(),
    dbc.Input(value='Content of Resources', id='example-input'),  # Text input field.
    html.Br(),
    dbc.Button('Submit', id='example-button'),  # Button for user submission.
]

```

### Explanation  
The **sidebar** is the left-hand panel of the app that allows users to configure job parameters before submitting. It includes:  
- **Charge Switch (`bfabric_web_apps.components.charge_switch`)** – Toggles whether a job is billable or not. For additional details, see the [Charge Switch section](important_components.md#charge-switch).
- **Text Header (`html.P`)** – Displays a prompt for the number of resources to create.  
- **Slider (`dcc.Slider`)** – Selects a numeric value (e.g. number of resources) between 0 and 10.  
- **Second Text Header (`html.P`)** – Prompts the user to choose an internal unit or project.  
- **Dropdown (`dcc.Dropdown`)** – Lets the user choose from a list of predefined project options.  
- **Text Input (`dbc.Input`)** – Allows free-text entry (e.g. for naming or describing resources).  
- **Submit Button (`dbc.Button`)** – Opens a modal window where the actual submission button is located

---

## Defining the Modal Confirmation Window  

The **modal** provides a **confirmation step** before executing critical actions, such running a pipeline. It appears when the user clicks the **Submit button** in the sidebar.

```python
# Here we define the modal that will pop up when the user clicks the submit button.
modal = html.Div([
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Ready to Prepare Create Workunits?")),  # Modal title.
        dbc.ModalBody("Are you sure you're ready to create workunits?"),  # Confirmation message.
        dbc.ModalFooter(
            dbc.Button("Yes!", id="Submit", className="ms-auto", n_clicks=0)  # Final confirmation button.
        ),
    ],
    id="modal-confirmation",  # Modal component ID for callback control.
    is_open=False),  # Initially hidden until triggered.
])
```

### Explanation  
The **modal** is a pop-up confirmation dialog triggered by the **Submit button** in the sidebar. It consists of:  
- **Modal Header (`dbc.ModalHeader`)** – Displays the title at the top of the modal.  
- **Modal Body (`dbc.ModalBody`)** – Shows a message asking for user confirmation.  
- **Modal Footer (`dbc.ModalFooter`)** – Contains a confirmation button labeled **"Yes!"**, which initiates the execution of `run_main_job`.
- **`is_open=False`** – The modal is **initially closed** and only appears in response to user interaction.

---

## Defining the Alert Messages  

The **alerts** notify the user whether the **workunit creation process succeeded or failed**, providing immediate visual feedback.

```python
# Here are the alerts which will pop up when the user creates workunits 
alerts = html.Div(
    [
        dbc.Alert("Success: Workunit created!", color="success", id="alert-fade-success", dismissable=True, is_open=False),
        dbc.Alert("Error: Workunit creation failed!", color="danger", id="alert-fade-fail", dismissable=True, is_open=False),
    ],
    style={"margin": "20px"}
)
```

### Explanation  
The **alerts** are used to display **success or error messages** based on job outcome.  
Each alert includes:  
- **Message (`dbc.Alert`)** – Informs the user of a success or failure event.  
- **Color** – Green for success (`"success"`), red for error (`"danger"`).  
- **Dismissable** – Alerts can be manually closed by the user.  
- **`is_open=False`** – Both alerts are hidden by default and displayed dynamically after job submission.

---

## Defining the Application Layout  

The **application layout** organizes the **sidebar and main content area** into a structured, two-column design. The **left column** houses interactive elements for user input, while the **right column** displays content dynamically based on authentication and user selections.

```python
app_specific_layout = dbc.Row(
    id="page-content-main",
    children=[
        dcc.Loading(alerts), 
        modal,  # Modal defined earlier.
        dbc.Col(
            html.Div(
                id="sidebar",
                children=sidebar,  # Sidebar content defined earlier.
                style={
                    "border-right": "2px solid #d4d7d9",
                    "height": "100%",
                    "padding": "20px",
                    "font-size": "20px"
                }
            ),
            width=3,  # Width of the sidebar column.
        ),
        dbc.Col(
            html.Div(
                id="page-content",
                children=[
                    html.Div(id="auth-div")  # Placeholder for `auth-div` to be updated dynamically.
                ],
                style={
                    "margin-top": "20vh",
                    "margin-left": "2vw",
                    "font-size": "20px"
                }
            ),
            width=9,  # Width of the main content column.
        ),
    ],
    style={"margin-top": "0px", "min-height": "40vh"}  # Overall styling for the row layout.
)
```

### Explanation  
The **layout consists of two primary sections**:  
- **Sidebar (left column, width = 3)** – Contains interactive UI elements such as sliders, dropdowns, and buttons for user input.  
- **Main Content (right column, width = 9)** – Displays authentication details and dynamically updated content based on user interactions.  

---

## Defining the Documentation  

The **documentation section** provides users with an introduction to the **B-Fabric App Template** and links to external resources for further learning.  

```python
documentation_content = [
    html.H2("Welcome to Bfabric App Template"),
    html.P(
        [
            "This app serves as the user-interface for Bfabric App Template, "
            "a versatile tool designed to help build and customize new applications."
        ]
    ),
    html.Br(),
    html.P(
        [
            "It is a simple application which allows you to bulk-create resources, "
            "workunits, and demonstrates how to use the bfabric-web-apps library."
        ]
    ),
    html.Br(),
    html.P(
        [
            "Please check out the official documentation of ",
            html.A("Bfabric Web Apps", href="https://bfabric-docs.gwc-solutions.ch/index.html"),
            "."
        ]
    )
]
```

### Explanation  
- **Header (`html.H2`)** – Displays a **title** for the documentation section.  
- **Introduction (`html.P`)** – Briefly explains the **purpose of the application** and its customization options.  
- **External Link (`html.A`)** – Provides a **clickable link** to the official **B-Fabric Web Apps** documentation.  

---

## Defining the Application Title  

The **application title** provides a clear and identifiable name for the B-Fabric web app. This title appears in the **UI header** and helps users understand the purpose of the application.  

```python
app_title = "B-Fabric App Template"
```

---

## Defining the App Layout  

The `app.layout` function **establishes the final structure** of the application by integrating the **title, main content, and documentation** into a cohesive layout. This ensures a **consistent user experience** across all pages.  

```python
app.layout = bfabric_web_apps.get_static_layout(
    base_title=app_title,
    main_content=app_specific_layout,
    documentation_content=documentation_content,
    layout_config={"workunits": True, "queue": False, "bug": True}
)
```

### Explanation  
- Uses **[`get_static_layout`](important_functions.md#get-static-layout)** to maintain a **consistent page structure** throughout the application.  
- **`app_title`** – Defines the **main heading** of the application.  
- **`app_specific_layout`** – Contains the **sidebar and main content area**.  
- **`documentation_content`** – Displays **informational resources** for users.
- **`layout_config`** –  Configuration settings for the layout

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

## Callback: Authentication & Sidebar State Management

This callback dynamically adjusts the state of the user interface based on authentication and session context. It ensures that unauthenticated users are restricted from interaction, and authenticated users receive personalized data and context-aware controls.

For general information on Dash callbacks, refer to the [Dash Callback Documentation](https://dash.plotly.com/basic-callbacks).

---

### Callback Definition

This callback is triggered when any of the following inputs change:

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
```

#### Explanation:

* **Outputs**: This callback modifies the state (visibility or enable/disable) of sidebar components and updates the `auth-div` content.
* **Inputs**: Changes to the user-selected slider, dropdown, text input, or token data trigger the callback.
* **State**: Reads the current `entity` data from memory to personalize the UI.

For more details about `token_data` and `entity_data`, see the chapter:
**[Important Components → Extracted Key Dictionaries](important_components.md#extracted-key-dictionaries)**.

---

### Function Definition

```python
def update_ui(slider_val, dropdown_val, input_val, token_data, entity_data):
```

This function receives user inputs and authentication data, then determines how to update the UI accordingly.

---

### Step 1 – Toggle UI Elements Based on Authentication

```python
if token_data is None:
    sidebar_state = (True, True, True, True, True, True, True)
else:
    sidebar_state = (False, False, False, False, False, False, False)
```

If the user is **not authenticated** (`token_data is None`), all interactive elements in the sidebar are **disabled** by setting them to `True`.
If the user is authenticated, all elements remain **enabled** (`False`).


---

### Step 2 – Display Message If User is Not Authenticated

```python
if not entity_data or not token_data:
    auth_div_content = html.Div(children=no_auth)
```

If either `token_data` or `entity_data` is missing or invalid, the UI will show a predefined message (`no_auth`) instructing the user to log in via B-Fabric.

---

### Step 3 – Build UI Content for Authenticated Users

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

In the `else` block, the user is authenticated. The `component_data` list shows the current input values:

* Number of resources (from the slider)
* Selected container/project ID
* Entered text content

This forms the **left column** of the authenticated view.

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

The `entity_details` list shows key metadata associated with the current entity. These fields come from the token and entity data and provide:

* Entity type (e.g., Dataset, Analysis, Workunit)
* Entity ID
* Creation and modification metadata

This forms the **right column** of the authenticated view.

---

```python
        auth_div_content = dbc.Row([dbc.Col(component_data), dbc.Col(entity_details)])
```

The two columns (`component_data` and `entity_details`) are wrapped in a Bootstrap `Row`, allowing them to be displayed side-by-side in the `auth-div` section of the layout.

---

### Step 4 – Error Handling

```python
    except Exception as e:
        return (*sidebar_state, html.P(f"Error Logging into B-Fabric: {str(e)}"))
```

If something goes wrong while accessing the token or entity data (e.g., a missing key), the callback returns an error message.
This ensures the app fails gracefully and provides helpful feedback.

---

### Step 5 – Return Updated UI State and Content

```python
return (*sidebar_state, auth_div_content)
```

The final return provides:

1. The enabled/disabled state of sidebar components (`sidebar_state`)
2. The content to display in the authentication div (`auth_div_content`)

This return structure ensures the entire UI updates reactively based on user context.

---

## Submitting run_main_job

This callback function is triggered when the user confirms their input by clicking the **"Yes!"** button in the modal. It initiates the execution of the `run_main_job` method, which submits the job, attaches files, creates resources, and handles both success and error cases.

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
        State("charge_run", "on"),
        State('url', 'search')
    ],
    prevent_initial_call=True
)
```

---

### Explanation of Arguments

#### **Inputs**

These values trigger the callback.

* **`Input("Submit", "n_clicks")`**
  The callback is executed when the user clicks the confirmation button inside the modal. This acts as a signal to begin job submission.

#### **States**

These values are **read** during the callback execution but **do not** trigger it.

* **`State("example-slider", "value")`**
  Represents the number of resources the user wants to create. It's an integer ranging from 0 to 10.

* **`State("example-dropdown", "value")`**
  The selected project or container ID (e.g., `"2220"`). Determines the B-Fabric container where the resources will be stored.

* **`State("example-input", "value")`**
  Free-text input provided by the user. This content is written into each created resource file.

* **`State("token_data", "data")`**
  A dictionary containing authentication and session information such as `application_data`, `entity_id_data`, and authorization token.

* **`State("charge_run", "on")`**
  A boolean flag indicating whether the job should be marked as **billable** in B-Fabric. This is controlled via the **charge switch** component.

* **`State("url", "search")`**
  The full search string from the app URL. It is passed along to `run_main_job` as a token for authorization.

---

### Explanation of Outputs

These values are updated by the callback and affect the UI:

* **`Output("alert-fade-success", "is_open")`**
  A boolean value that controls the **success alert** visibility. Set to `True` if the job runs successfully.

* **`Output("alert-fade-fail", "is_open")`**
  Controls the **error alert** visibility. Set to `True` if the job fails (e.g., due to missing dropdown selection or a runtime error).

* **`Output("alert-fade-fail", "children")`**
  Provides the **content of the error message** shown in the alert. Includes exception details to help users understand what went wrong.

* **`Output("refresh-workunits", "children")`**
  This dummy output is used to **trigger a refresh** of the workunit section, allowing updates without user interaction. While it's set to an empty `html.Div()`, it can later be extended to update live data.

---

### Submission Logic

This function prepares and triggers the job submission process. It collects user input, creates temporary resource definitions, and calls `run_main_job()` a general-purpose utility that handles:

* File saving (as byte strings)
* Bash command execution
* Resource registration
* Workunit creation
* Download link attachments
* Optional project-based charging in B-Fabric

Let's walk through each step with code and explanation.

For more details, please refer to the [**run_main_job function**](important_functions.md#9-main-job-execution) in the library documentation.

---

#### Step 1 – Validate Input and Extract Container ID

```python
if dropdown_val is None:
    return False, True, "Error: Please select a container Id", html.Div()

container_id = int(dropdown_val)
```

**Explanation:**
The function first ensures that the user selected a valid container (`dropdown_val`). If not, it immediately returns an error alert.

---

#### Step 2 – Define Attachments

```python
attachment1_content = b"<html><body><h1>Hello World</h1></body></html>"
attachment1_name = "attachment_1.html"

attachment2_content = b"<html><body><h1>Hello World a second time!!</h1></body></html>"
attachment2_name = "attachment_2.html"

files_as_byte_strings = {
    attachment1_name: attachment1_content,
    attachment2_name: attachment2_content
}
```

**Explanation:**
These attachments are passed to `run_main_job` as `files_as_byte_strings`.
This mimics a common use case in B-Fabric, where reports or logs (e.g., `multiqc_report.html`) are attached and made downloadable after the job.

Attachments are stored in `attachment_paths` for linking them in the UI (see Step 5).

---

#### Step 3 – Generate Bash Commands

```python
bash_commands = [f"echo '{input_val}' > resource_{i+1}.txt" for i in range(slider_val)]
```

**Explanation:**
Each command creates a file named `resource_X.txt` containing the user’s input (`input_val`).
These Bash commands will be run sequentially via `run_main_job`, and their logs will be captured.

This simulates what more complex pipelines (e.g., Nextflow, R scripts) would do.

---

#### Step 4 – Determine Charge Containers

```python
project_id = "2220"

if charge_run and project_id:
    charge_run = [project_id]
else:
    charge_run = []
    
```

**Explanation:**
If the charge switch (`charge_run`) is enabled, the project ID is included in the `charge` argument.
This enables automatic billing in B-Fabric and logs the activity under the correct container.
If charging is off, this list remains empty (`[]`).

---

#### Step 5 – Define Resource and Attachment Paths

```python
attachment_paths = {
    attachment1_name: attachment1_name,
    attachment2_name: attachment2_name
}

resource_paths = {
    f"resource_{i+1}.txt": container_id for i in range(slider_val)
}
```

**Explanation:**
These paths tell `run_main_job`:

* Where the output files should be registered (`resource_paths`)
* Which files should appear as downloadable links (`attachment_paths`)

All files listed in `resource_paths` will be registered in B-Fabric under the specified container.

---

#### Step 6 – Build the Dataset Dictionary

```python
dataset_info = {
    str(container_id): {
        "resource_name": [f"resource_{i+1}" for i in range(slider_val)],
        "resource_description": [f"Resource {i+1} created by Bfabric Web Apps" for i in range(slider_val)],
        "resource_type": ["text/plain"] * slider_val,
        "resource_size": [len(bash_commands[i]) for i in range(slider_val)],
        "resource_path": [f"resource_{i+1}.txt" for i in range(slider_val)]
    }
}
```

**Explanation:**
This structure mirrors how B-Fabric stores resource metadata:

* **`resource_name`** – Human-readable name
* **`resource_description`** – Optional context
* **`resource_type`** – MIME type
* **`resource_size`** – Useful for display and quota checking
* **`resource_path`** – Where to find the file after job completion

`run_main_job` uses this dictionary to create and register resources in the container.

---

#### Step 7 – Call run_main_job()

```python
arguments = {
    "files_as_byte_strings": files_as_byte_strings,
    "bash_commands": bash_commands,
    "resource_paths": resource_paths,
    "attachment_paths": attachment_paths,
    "token": raw_token,
    "service_id": bfabric_web_apps.SERVICE_ID,
    "charge": charge_run,
    "dataset_dict": dataset_info
}

bfabric_web_apps.run_main_job(**arguments)
```

**Explanation:**
Here, all components are passed to the central function `run_main_job()`:

* Transfers files via `files_as_byte_strings`
* Executes Bash commands
* Registers output files as resources
* Creates workunits automatically
* Attaches download links
* Charges the project container if `charge` is set

Behind the scenes, logs are written, errors are captured, and all job metadata is stored in B-Fabric.

---

#### Step 8 – Handle Success or Failure

```python
return True, False, None, html.Div()
```

**Explanation:**
If everything runs successfully, this opens the success alert and clears the error message.

If anything fails (e.g., exception during job execution), an error message is returned:

```python
except Exception as e:
    return False, True, f"Error: Workunit creation failed: {str(e)}", html.Div()
```

All exceptions are caught and shown in the UI for better debugging.

---


## Running the Application

The following section ensures the application executes on the specified host and port configuration.

```python
if __name__ == "__main__":
    app.run(debug=False, port=bfabric_web_apps.PORT, host=bfabric_web_apps.HOST)
```

### Explanation

* Runs the Dash server, respecting settings defined by the global configuration (`bfabric_web_apps.PORT`, `bfabric_web_apps.HOST`).
