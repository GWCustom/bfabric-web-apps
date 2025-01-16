# Full-Featured Template - index.py

This chapter provides a comprehensive explanation of **index.py**, serving as a user-editable template for building applications with the **bfabric_web_apps** module. Users can customize the layout, callbacks, and components to match their needs.

## Prerequisites

Before starting, ensure familiarity with:
- [Dash Fundamentals](https://dash.plotly.com/layout)

## Getting Started

To preview the template:
1. Execute `index.py`.
2. Open the application in your browser via `localhost`.

---

## Importing Required Modules

```python
from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
from bfabric_web_apps import load_config, get_static_layout, get_logger, get_power_user_wrapper
import generic_bfabric
from generic_bfabric import app
```

### Explanation:
- **Dash components** (`html`, `dcc`, `Input`, `Output`, `State`) provide UI functionality.
- **Dash Bootstrap Components (dbc)** are used for layout styling.
- **Bfabric Web Apps Utilities**:
  - `load_config`: Loads app configurations (see [Configuration](#configuration)).
  - `get_static_layout`: Creates a structured app layout (see [Layout](#layout)).
  - `get_logger`: Handles system logging (see [Logging](#logging)).
  - `get_power_user_wrapper`: Provides advanced user functionalities (see [Power User Wrapper](#power-user-wrapper)).
- The **app instance** is imported from `generic_bfabric`.

---

## Sidebar Components

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

### Explanation:
- The **sidebar** is a UI component containing:
  - A paragraph (`html.P`) for displaying instructions.
  - A numeric **slider** for selecting values.
  - A **dropdown** for choosing categories.
  - A **text input field** for manual entries.
  - A **submit button** for user actions.

---

## Application Layout

```python
app_specific_layout = dbc.Row(
    id="page-content-main",
    children=[
        dbc.Col(
            html.Div(id="sidebar", children=sidebar, style={...}),
            width=3,
        ),
        dbc.Col(
            html.Div(id="page-content", children=[html.Div(id="auth-div")], style={...}),
            width=9,
        ),
    ],
    style={...}
)
```

### Explanation:
- **Layout structure**:
  - **Sidebar** (left column, width = 3): Contains the user input components.
  - **Main Content Area** (right column, width = 9): Displays authentication-related content.
- The `auth-div` element is updated dynamically based on user authentication status.

---

## Documentation Content

```python
documentation_content = [
    html.H2("Welcome to Bfabric App Template"),
    html.P(["This app serves as the user interface for ", html.A("Bfabric App Template,", href="#", target="_blank"),
           " a tool for building and customizing applications."]),
]
```

### Explanation:
- **Documentation content** is displayed in a separate tab within the UI.
- The main header introduces the template.
- A link to additional documentation is included.

---

## Loading Configuration

```python
config = load_config("./PARAMS.py")
```

### Explanation:
- Loads configuration parameters from **PARAMS.py**.
- Stores app-specific settings such as **host, port, and debug mode**.
- See [Configuration](#configuration) for details.

---

## Setting Up the App Title

```python
app_title = "My B-Fabric App (Basic)"
```

### Explanation:
- Defines the title of the app.
- Used in the UI for a consistent experience.

---

## Defining the App Layout

```python
app.layout = get_static_layout(app_title, app_specific_layout, documentation_content)
```

### Explanation:
- Uses `get_static_layout` to **combine** the app's title, main layout, and documentation content.
- See [Layout](#layout) for an in-depth explanation.

---

## Callback for UI Updates

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
```

### Explanation:
- **Purpose**: Dynamically updates the sidebar and authentication area based on user interaction.
- **Input Parameters**:
  - Values from the **slider, dropdown, text input, and button**.
  - **Token data** (authentication information).
  - **Entity data** (additional user context).
- **Output Parameters**:
  - Enables/disables sidebar components.
  - Updates the authentication display.

---

## Power User Wrapper

```python
power_user_wrapper = get_power_user_wrapper(token_data)
```

### Explanation:
- **Power User Wrapper** provides additional tools for managing users.
- It requires **token_data** for authentication.
- See [Power User Wrapper](#power-user-wrapper) for advanced usage.

---

## Logging System

```python
L = get_logger(token_data)
L.log_operation("Example Log", "This is an example of how to use the log_operation method.")
```

### Explanation:
- The **logger** records system events and user actions.
- The `log_operation` method logs a specific event.
- See [Logging](#logging) for more details.

The `Logger` class provides two primary ways to log operations:  
1. Using the `log_operation` method for general logging.  
2. Using the `logthis` method to wrap and log API calls.  
---

## Running the Application

```python
if __name__ == "__main__":
    app.run_server(debug=False, port=config["PORT"], host=config["HOST"])
```

### Explanation:
- Starts the **Dash server** with settings from **PARAMS.py**.

---

## Further Reading

- **[Configuration](#configuration)**: Understanding `PARAMS.py` settings.
- **[Layout](#layout)**: Overview of `get_static_layout`.
- **[Logging](#logging)**: How `get_logger` manages logs.
- **[Power User Wrapper](#power-user-wrapper)**: Advanced user functionalities.