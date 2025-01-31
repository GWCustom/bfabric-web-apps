# Full-Featured Template - index.py

This chapter provides a step-by-step breakdown of the **index.py** script. It explains key functions and their roles in setting up a **feature-rich B-Fabric web application**. Each function is linked to its respective detailed documentation.

---

## View the Demo  

Before diving into the details, you can preview a **live demo** of this template:

[View the Demo](https://template-d12.bfabric.org/)  

This will give you an idea of how the **Full-Featured Template** looks and functions.

---

## Prerequisites

Before starting, ensure familiarity with:
- [Dash Fundamentals](https://dash.plotly.com/layout)

---

## Running the Template  

To execute the template:

1. Run the following command in your terminal:  
   ```sh
   python index.py
   ```
2. Open your browser and go to `localhost`.

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

2. **Generic B-Fabric Imports**  
   - `app`: The **Dash instance** that runs the web app.  

3. **bfabric_web_apps Imports**  
   - **[`get_static_layout`](bfabric_web_apps_functions.md#get-static-layout)**: Provides a **consistent page layout**.  
   - **[`get_logger`](bfabric_web_apps_functions.md#get-logger)**: Handles **logging of user actions**.  
   - **[`get_power_user_wrapper`](bfabric_web_apps_functions.md#get-power-user-wrapper)**: Provides **advanced user functionalities**.  
   - **HOST & PORT**: Define **server configurations** (imported from **bfabric_web_apps**).  

---

## Setting Up Default Configuration  

The application defines default **configuration values** for various settings.

```python
bfabric_web_apps.CONFIG_FILE_PATH = "~/.bfabricpy.yml"
bfabric_web_apps.DEVELOPER_EMAIL_ADDRESS = "marc@gwcustom.com"
bfabric_web_apps.BUG_REPORT_EMAIL_ADDRESS = "marc@gwcustom.com"
```

### Explanation  
- **Configuration file path** is set using `CONFIG_FILE_PATH`.  
- **Developer and bug report email addresses** are defined.  

---

## Defining the Sidebar  

The **sidebar** includes input fields, a slider, and a button for user interaction.

```python
sidebar = [
    html.P(id="sidebar_text", children="Select a Value"),  
    dcc.Slider(0, 20, 5, value=10, id='example-slider'),  
    html.Br(),
    dcc.Dropdown(['Genomics', 'Proteomics', 'Metabolomics'], 'Genomics', id='example-dropdown'),
    html.Br(),
    dbc.Input(value='Enter Some Text', id='example-input'),
    html.Br(),
    dbc.Button('Submit', id='example-button'),
]
```

### Explanation  
- The **sidebar** contains:  
  - A **text header** for user instructions.  
  - A **slider** for selecting numeric values.  
  - A **dropdown** for selecting categories.  
  - A **text input field** for manual entries.  
  - A **submit button** for user interaction.  

---

## Defining the Application Layout  

This section defines the **main content and sidebar structure**.

```python
app_specific_layout = dbc.Row(
    id="page-content-main",
    children=[
        dbc.Col(
            html.Div(id="sidebar", children=sidebar, style={
                "border-right": "2px solid #d4d7d9",
                "height": "100%",
                "padding": "20px",
                "font-size": "20px"
            }),
            width=3,
        ),
        dbc.Col(
            html.Div(id="page-content", children=[html.Div(id="auth-div")], style={
                "margin-top": "20vh",
                "margin-left": "2vw",
                "font-size": "20px"
            }),
            width=9,
        ),
    ],
    style={"margin-top": "0px", "min-height": "40vh"}
)
```

### Explanation  
- The **layout consists of two columns**:  
  - **Sidebar (left column, width = 3)**: Holds the interactive elements.  
  - **Main Content (right column, width = 9)**: Displays authentication and user-specific content.  

---

## Documentation Content  

The application includes **static documentation content**.

```python
documentation_content = [
    html.H2("Welcome to Bfabric App Template"),
    html.P([
        "This app serves as the user-interface for Bfabric App Template, ",
        "a versatile tool designed to help build and customize new applications."
    ]),
    html.Br(),
    html.P([
        "Please check out the official documentation of ",
        html.A("Bfabric Web Apps", href="https://pypi.org/project/bfabric-web-apps/", target="_blank"),
        "."
    ])
]
```

### Explanation  
- **Header** introduces the B-Fabric App Template.  
- **Paragraph** provides documentation links.  

---

## Defining the App Layout  

The `app.layout` function sets up the **final UI structure**.

```python
app.layout = bfabric_web_apps.get_static_layout(
    app_title,
    app_specific_layout,
    documentation_content
)
```

### Explanation  
- Uses **[`get_static_layout`](bfabric_web_apps_functions.md#get-static-layout)** to create a **consistent** page structure.  

---

## Callback for UI Updates  

This callback **controls UI behavior dynamically**.

```python
@app.callback(
    [
        Output('sidebar_text', 'hidden'),
        Output('example-slider', 'disabled'),
        Output('example-dropdown', 'disabled'),
        Output('example-input', 'disabled'),
        Output('example-button', 'disabled'),
        Output('auth-div', 'children'),
    ],
    [
        Input('example-slider', 'value'),
        Input('example-dropdown', 'value'),
        Input('example-input', 'value'),
        Input('example-button', 'n_clicks'),
        Input('token_data', 'data'),
    ],
    [State('entity', 'data')]
)
def update_ui(slider_val, dropdown_val, input_val, n_clicks, token_data, entity_data):
    if token_data is None:
        sidebar_state = (True, True, True, True, True)
    elif not bfabric_web_apps.DEV:
        sidebar_state = (False, False, False, False, False)
    else:
        sidebar_state = (True, True, True, True, True)

    if not entity_data or not token_data:
        auth_div_content = html.Div(children=generic_bfabric.no_auth)
    else:
        auth_div_content = html.Div(children="Authenticated User Content")

    return (*sidebar_state, auth_div_content)
```

### Function Definition  

**Controls sidebar interaction and authentication-based UI updates.**  

#### **Args:**  
- **`slider_val, dropdown_val, input_val, n_clicks`** – User inputs from the sidebar.  
- **`token_data`** – User authentication token data.  
- **`entity_data`** – Entity-specific user information.  

#### **Returns:**  
- **Tuple**: Sidebar state updates and dynamic content for `auth-div`.  

#### **Return Type:**  
- `tuple`  

---

## Running the Application  

The script starts the **Dash server**.

```python
if __name__ == "__main__":
    app.run_server(debug=False, port=bfabric_web_apps.PORT, host=bfabric_web_apps.HOST)
```

### Explanation  
- Runs the **Dash server** with the specified **host** and **port** settings.  

---

## Further Reading  

- **[Dash Callbacks](https://dash.plotly.com/basic-callbacks)**: Learn more about Dash interactions.  
- **[Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)**: Enhance UI elements.  
- **[bfabric_web_apps Functions](bfabric_web_apps_functions.md)**: Detailed explanations of helper functions like `get_static_layout`, `get_logger`, and authentication handling.  