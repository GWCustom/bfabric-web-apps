# Full-Featured Template

This chapter provides a step-by-step breakdown of the **index_large.py** script. It explains key functions and their roles in setting up a feature-rich B-Fabric web application.

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

> **Important:**  
> - **`generic_bfabric.py`** is a **core system file** and **must not be modified**. Any changes to this file may break authentication or system integration.  
> - **All customization** (for example, adding UI components, callbacks, or logging) should be done in **`index_large.py`, `index_redis.py` or `index_basic.py`**.  

---

## Setting Up Default Configuration

The application uses **global variables** in bfabric_web_apps to define important **default configuration values**.  

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


For more details, refer to the **[Global Configuration Variables](bfabric_web_apps_functions.md#dynamic-variable-configuration)** chapter.

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
- **Charge Switch (`bfabric_web_apps.components.charge_switch`)** – Toggles whether a job is billable or not.  
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
- **Modal Footer (`dbc.ModalFooter`)** – Contains a confirmation button labeled **"Yes!"** to proceed with job creation.  
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
- Uses **[`get_static_layout`](bfabric_web_apps_functions.md#get-static-layout)** to maintain a **consistent page structure** throughout the application.  
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

---

## Callback for UI Updates

This callback function **dynamically updates the user interface** based on user interactions and the authentication status. It manages the sidebar behavior, displays entity-related data, and provides informative feedback to the user.

For additional details on Dash callbacks, refer to the [Dash Callbacks Documentation](https://dash.plotly.com/basic-callbacks).

---

### Callback Definition

The callback listens for **changes in user input and authentication data**, updating the interface components accordingly.

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

    # Determine sidebar and input states based on authentication status.
    if token_data is None:
        sidebar_state = (True, True, True, True, True, True, True)
    else:
        sidebar_state = (False, False, False, False, False, False, False)

    # Handle UI based on the authentication and entity data.
    if not entity_data or not token_data:
        auth_div_content = html.Div(children=no_auth)
    else:
        try:
            component_data = [
                html.H1("Component Data:"),
                html.P(f"Number of Resources to Create: {slider_val}"),
                html.P(f"Create workunit inside project: {dropdown_val}"),
                html.P(f"Resource Content: {input_val}")
            ]
            entity_details = [
                html.H1("Entity Data:"),
                html.P(f"Entity Class: {token_data['entityClass_data']}"),
                html.P(f"Entity ID: {token_data['entity_id_data']}"),
                html.P(f"Created By: {entity_data['createdby']}"),
                html.P(f"Created: {entity_data['created']}"),
                html.P(f"Modified: {entity_data['modified']}")
            ]
            auth_div_content = dbc.Row([dbc.Col(component_data), dbc.Col(entity_details)])

        except Exception as e:
            auth_div_content = html.P(f"Error Logging into B-Fabric: {str(e)}")

    return (*sidebar_state, auth_div_content)
```

### Explanation

* **Outputs:**

  * Manages the visibility and enabled/disabled state of sidebar UI elements.
  * Updates the content in the `auth-div` element based on authentication data.

* **Inputs:**

  * Tracks the slider, dropdown, text input, and token data for changes to update UI dynamically.

* **State:**

  * Accesses stored entity information to personalize user experience and UI content.

---

### UI Behavior Based on Authentication

* If the user **is not authenticated** (`token_data is None`), the sidebar elements are **disabled**, preventing unauthorized interactions.
* If the user **is authenticated**, the sidebar elements become **interactive** and functional.

---

### Handling Authentication and Displaying Entity Data

* Displays a **login prompt** if the user is not authenticated.
* Upon authentication, displays:

  * Details of the current session's entity (class, ID, creator, timestamps).
  * User-selected input parameters (resource count, project, resource content).

---

### Final Return

Returns the sidebar state (enabled/disabled components) along with the dynamically generated authentication information.

```python
return (*sidebar_state, auth_div_content)
```

---

### Function Definition Details

#### Args:

* **`slider_val` (int):** Current slider value representing resource count.
* **`dropdown_val` (str):** Selected project identifier from dropdown.
* **`input_val` (str):** User-provided text input describing resources.
* **`token_data` (dict or None):** Authentication session data.
* **`entity_data` (dict or None):** Data about the currently authenticated entity.

#### Returns:

* A tuple containing the sidebar state settings and updated authentication UI.

#### Return Type:

* **`tuple`**

---


## Submit run_main_job Function

This callback function initiates the **workunit creation** process when the user confirms their input in the confirmation modal. It handles job submission logic, including file attachments, resource creation, and error handling.

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

### Explanation

* **Outputs:**

  * Success alert visibility (`alert-fade-success`)
  * Error alert visibility (`alert-fade-fail`)
  * Error message content
  * Workunits refresh trigger (`refresh-workunits`)

* **Inputs:**

  * Clicks on the confirmation button (`Submit`)

* **States:**

  * User-defined parameters: slider value, dropdown selection, text input, token data, charge toggle, URL token

---

### Submission Logic

This function processes the user's request to create new workunits and resources within the selected B-Fabric container.

```python
def submission(n_clicks, slider_val, dropdown_val, input_val, token_data, charge_run, raw_token):

    app_id = token_data.get("application_data", None)

    if dropdown_val is None:
        return False, True, "Error: Please select a container Id", html.Div()

    container_id = int(dropdown_val)

    if n_clicks:
        try:
            # Define attachments for the job
            attachment1_content = b"<html><body><h1>Hello World</h1></body></html>"
            attachment1_name = "attachment_1.html"

            attachment2_content = b"<html><body><h1>Hello World a second time!!</h1></body></html>"
            attachment2_name = "attachment_2.html"

            files_as_byte_strings = {
                attachment1_name: attachment1_content,
                attachment2_name: attachment2_content
            }

            # Generate resource creation commands
            bash_commands = [f"echo '{input_val}' > resource_{i+1}.txt" for i in range(slider_val)]

            project_id = "2220"
            charge_run = [project_id] if charge_run and project_id else []

            # Define file paths
            attachment_paths = {attachment1_name: attachment1_name, attachment2_name: attachment2_name}
            resource_paths = {f"resource_{i+1}.txt": container_id for i in range(slider_val)}

            # Construct dataset information
            dataset_info = {
                str(container_id): {
                    "resource_name": [f"resource_{i+1}" for i in range(slider_val)],
                    "resource_description": [f"Resource {i+1} created by Bfabric Web Apps" for i in range(slider_val)],
                    "resource_type": ["text/plain"] * slider_val,
                    "resource_size": [len(bash_commands[i]) for i in range(slider_val)],
                    "resource_path": [f"resource_{i+1}.txt" for i in range(slider_val)]
                }
            }

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

            # Execute job
            bfabric_web_apps.run_main_job(**arguments)

            return True, False, None, html.Div()

        except Exception as e:
            return False, True, f"Error: Workunit creation failed: {str(e)}", html.Div()
```

### Explanation

* **Attachments:** Files provided as byte strings.
* **Resources:** Generated via shell commands based on user input.
* **Charging Logic:** Determines whether the created workunits are billable.
* **Error Handling:** Displays error alert with exception details in case of failure.

---

## Running the Application

The following section ensures the application executes on the specified host and port configuration.

```python
if __name__ == "__main__":
    app.run(debug=False, port=bfabric_web_apps.PORT, host=bfabric_web_apps.HOST)
```

### Explanation

* Runs the Dash server, respecting settings defined by the global configuration (`bfabric_web_apps.PORT`, `bfabric_web_apps.HOST`).
