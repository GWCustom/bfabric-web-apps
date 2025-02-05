# Full-Featured Template - index.py

This chapter provides a step-by-step breakdown of the **index.py** script. It explains key functions and their roles in setting up a feature-rich B-Fabric web application.

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
import generic_bfabric
from generic_bfabric import app
```

### Explanation  

1. **Dash Imports**  
   - `html` and `dcc`: Used to construct the app layout.  
   - `Input`, `Output`, and `State`: Required for callback interactions.  

2. **Dash Bootstrap Components (DBC)**  
   - Provides **pre-styled UI elements** to enhance the look and functionality of the app.  

3. **bfabric_web_apps**  
   - Contains **utilities and configurations** for seamless integration with B-Fabric.  

4. **Generic B-Fabric**  
   - `generic_bfabric`: This file provides **generalized functions** that the template relies on.

5. **Generic B-Fabric app Import**  
   - `app`: The **Dash instance** that initializes and runs the web app.

---

> **Important:**  
> - **`generic_bfabric.py`** is a **core system file** and **must not be modified**. Any changes to this file may break authentication or system integration.  
> - **All customization** (for example, adding UI components, callbacks, or logging) should be done in **`index.py` or `index_basic.py`**.  

---

## Setting Up Default Configuration

The application uses **global variables** in bfabric_web_apps to define important **default configuration values**.  


```python
bfabric_web_apps.CONFIG_FILE_PATH = "~/.bfabricpy.yml"
bfabric_web_apps.DEVELOPER_EMAIL_ADDRESS = "marc@gwcustom.com"
bfabric_web_apps.BUG_REPORT_EMAIL_ADDRESS = "marc@gwcustom.com"
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
sidebar = [
    html.P(id="sidebar_text", children="Select a Value"),  # Sidebar header text.
    dcc.Slider(0, 20, 5, value=10, id='example-slider'),  # Slider for selecting a numeric value.
    html.Br(),
    dcc.Dropdown(
        ['Genomics', 'Proteomics', 'Metabolomics'],  # Dropdown options.
        'Genomics',  # Default value.
        id='example-dropdown'  # Dropdown ID for callback integration.
    ),
    html.Br(),
    dbc.Input(value='Enter Some Text', id='example-input'),  # Text input field.
    html.Br(),
    dbc.Button('Submit', id='example-button'),  # Button for user submission.
]
```

### Explanation  
The **sidebar** provides an intuitive interface for user interaction, consisting of:  
- **Text Header (`html.P`)** – Displays **instructions or labels** for users.  
- **Slider (`dcc.Slider`)** – Allows users to **select numeric values** within a defined range.  
- **Dropdown (`dcc.Dropdown`)** – Lets users **choose a category** from a predefined list.  
- **Text Input (`dbc.Input`)** – Provides a **field for manual data entry**.  
- **Submit Button (`dbc.Button`)** – Triggers an **action based on user input**.  

---

## Defining the Application Layout  

The **application layout** organizes the **sidebar and main content area** into a structured, two-column design. The **left column** houses interactive elements for user input, while the **right column** displays content dynamically based on authentication and user selections.  

```python
app_specific_layout = dbc.Row(
    id="page-content-main",
    children=[
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
    html.H2("Welcome to B-Fabric App Template"),
    html.P(
        [
            "This app serves as the user interface for B-Fabric App Template, "
            "a versatile tool designed to help build and customize new applications."
        ]
    ),
    html.Br(),
    html.P(
        [
            "Please check out the official documentation of ",
            html.A("B-Fabric Web Apps", href="https://pypi.org/project/bfabric-web-apps/", target="_blank"),
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
app.layout = bfabric_web_apps.get_static_layout(  # The function from bfabric_web_apps that sets up the app layout.
    app_title,  # The app title we defined previously.
    app_specific_layout,  # The main content for the app defined earlier.
    documentation_content  # Documentation content for the app.
)
```

### Explanation  
- Uses **[`get_static_layout`](bfabric_web_apps_functions.md#get-static-layout)** to maintain a **consistent page structure** throughout the application.  
- **`app_title`** – Defines the **main heading** of the application.  
- **`app_specific_layout`** – Contains the **sidebar and main content area**.  
- **`documentation_content`** – Displays **informational resources** for users.  

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