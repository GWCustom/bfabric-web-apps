# Full-Featured Template

This chapter provides a step-by-step breakdown of the **index_large.py** script. It explains key functions and their roles in setting up a feature-rich B-Fabric web application.

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
   python index.py
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

This callback **dynamically updates the UI** based on user interactions and authentication status. It manages sidebar behavior, displays entity-related data, and logs user actions.  

For more details on Dash callbacks, see: **[Dash Callbacks Documentation](https://dash.plotly.com/basic-callbacks)**  

---

### Callback Definition

The callback function listens for **user input changes** and modifies the UI accordingly.  

```python
@app.callback(
    [
        Output('sidebar_text', 'hidden'),  # Controls sidebar text visibility.
        Output('example-slider', 'disabled'),  # Disables slider when needed.
        Output('example-dropdown', 'disabled'),  # Disables dropdown when needed.
        Output('example-input', 'disabled'),  # Disables input field when needed.
        Output('example-button', 'disabled'),  # Disables submit button when needed.
        Output('auth-div', 'children'),  # Updates authentication UI.
    ],
    [
        Input('example-slider', 'value'),  # Listens to slider value changes.
        Input('example-dropdown', 'value'),  # Listens to dropdown selection changes.
        Input('example-input', 'value'),  # Listens to text input changes.
        Input('example-button', 'n_clicks'),  # Tracks button clicks.
        Input('token_data', 'data'),  # Tracks authentication token updates.
    ],
    [State('entity', 'data')]  # Retrieves stored entity data for authentication.
)
```

### Explanation
- **Outputs:**  
  - Controls the sidebar’s elements (hiding text, disabling inputs).  
  - Updates the `auth-div` element to show authentication details.  
- **Inputs:**  
  - Tracks changes in the sidebar elements and authentication status.  
- **State:**  
  - Retrieves stored **entity data** to determine user-specific behavior.  

---

### Handling Sidebar Behavior

The function determines whether to enable or disable sidebar elements based on authentication status.  

```python
def update_ui(slider_val, dropdown_val, input_val, n_clicks, token_data, entity_data):
    
    if token_data is None:
        sidebar_state = (True, True, True, True, True)  # Disable all elements if no token.
    elif not bfabric_web_apps.DEV:
        sidebar_state = (False, False, False, False, False)  # Enable elements in production mode.
    else:
        sidebar_state = (True, True, True, True, True)  # Disable elements in development mode.
```

### Explanation  
- If the user is not authenticated (`token_data is None`), all sidebar elements are disabled.  
- If running in production (`bfabric_web_apps.DEV is False`), all elements remain enabled.  
- If in development mode, the elements are disabled by default.

---

### Handling Authentication and Entity Data

If authentication is valid, the function updates the UI to display user-related data.  

```python
    if not entity_data or not token_data:
        auth_div_content = html.Div(children=generic_bfabric.no_auth)  # Shows login prompt if unauthorized.
    else:
        component_data = [
            html.H1("Component Data:"),
            html.P(f"Slider Value: {slider_val}"),
            html.P(f"Dropdown Value: {dropdown_val}"),
            html.P(f"Input Value: {input_val}"),
            html.P(f"Button Clicks: {n_clicks}")
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
```

### Explanation  
- If no authentication data exists, it prompts the user to **log in**.  
- If authenticated, it **displays user-related data**, including:  
  - The entity class, ID, creator, and modification details.  
  - Sidebar input values (slider, dropdown, text input, button clicks).  

---

### Integrating Power User Wrapper  

The **Power User Wrapper** provides **advanced functionalities** for authorized users.  

```python
        power_user_wrapper = bfabric_web_apps.get_power_user_wrapper(token_data) 
```

For more details, refer to: **[Power User Wrapper](bfabric_web_apps_functions.md#get-power-user-wrapper)**  

---

### Logging User Activity  

User interactions are logged to track authentication and system events.  

```python
        L = bfabric_web_apps.get_logger(token_data)  # Initializes logger with token data.

        L.log_operation(
            "Example Log",  # Log operation title.
            "This is an example of how to use the log_operation method.",  # Log message.
            params=None,  # (Optional) Additional log parameters.
            flush_logs=True  # Ensures logs are stored immediately.
        )
```

For more details, refer to: **[Logging Functions](bfabric_web_apps_functions.md#get-logger)**  

---

### Final Return Statement  

The function returns:  
- **Sidebar state settings** (enabled/disabled components).  
- **Authentication UI content** (updated authentication UI).  

```python
    return (*sidebar_state, auth_div_content)
```

---

### Function Definition  

#### **Args:**  
- **`slider_val` (int)** – The value of the slider.  
- **`dropdown_val` (str)** – The selected dropdown option.  
- **`input_val` (str)** – The text input value.  
- **`n_clicks` (int)** – Number of times the button was clicked.  
- **`token_data` (dict or None)** – Authentication token data.  
- **`entity_data` (dict or None)** – Entity information linked to the user.  

---

#### Returns:  
- Contains sidebar state settings and updated authentication UI.  

---

#### Return Type: 
- **`tuple`**  

---

## Running the Application

This section ensures the app **runs on the correct server settings**.

```python
if __name__ == "__main__":
    app.run_server(debug=False, port=bfabric_web_apps.PORT, host=bfabric_web_apps.HOST)
```
---

### Explanation
- Runs the **Dash server** with the specified **host** and **port** settings.