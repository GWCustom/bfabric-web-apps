# Minimal Template - index_basic.py

This chapter explains the **index_basic.py** script step by step, linking key functions to their detailed discussions later in the chapter.

## Prerequisites

Before starting, ensure familiarity with:
- [Dash Fundamentals](https://dash.plotly.com/layout)

## Getting Started

To preview the template:
1. Execute `index_basic.py`.
2. Open the application in your browser via `localhost`.

---

## Importing Dependencies

```python
from dash import html, dcc, Input, Output, State
from bfabric_web_apps import load_config, get_static_layout, get_logger
from generic_bfabric import app
```

### Explanation:
   
1. **Dash Imports**  
   - `html` and `dcc` are used to build the app layout.
   - `Input`, `Output`, and `State` manage callbacks.

2. **bfabric_web_apps Imports**  
   - `load_config`: Loads configuration settings (see [Configuration](#configuration)).  
   - `get_static_layout`: Provides a base layout for the app (see [Layout](#layout)).  
   - `get_logger`: Creates a logging instance (see [Logger](#logger)).  

3. **generic_bfabric Import**  
   - `app` is the Dash instance managing the web app.

---

## Loading Configuration

```python
config = load_config("./PARAMS.py")
```

### Explanation:
- Loads settings from **PARAMS.py** (e.g., port, host, credentials).
- For more details, refer to [Configuration](#configuration).

---

## Setting Up the App Title

```python
app_title = "My B-Fabric App (Basic)"
```

### Explanation:
- Defines the title of the app.
- Used in the UI for a consistent experience.

---

## Defining the Layout

```python
app_specific_layout = html.Div([
    html.H1("Welcome to My B-Fabric App"),
    html.P("This is a quickstart example using bfabric_web_apps."),
    html.Div(id='user-display')
])

documentation_content = [
    html.H2("Documentation"),
    html.P("Describe your app's features here.")
]

app.layout = get_static_layout(
    app_title,  
    app_specific_layout,  
    documentation_content  
)
```

### Explanation:
- **app_specific_layout**  
  - Contains UI elements like `H1`, `P`, and `Div` components.
  - `id='user-display'` is where user login data will be shown dynamically.
  
- **documentation_content**  
  - Adds a section for documentation.

- **get_static_layout**  
  - Combines title, app layout, and documentation into a structured page.
  - See [Layout](#layout) for details.

---

## Creating a Callback for User Display

```python
@app.callback(
    Output('user-display', 'children'),
    Input('token_data', 'data'),
    State('entity', 'data')
)
def update_user_display(token_data, entity_data):
    if token_data and entity_data:
        user_name = token_data.get("user_data", "Unknown User")  
        
        L = get_logger(token_data)
        L.log_operation("User Login", "User logged in successfully.")
        
        return f"User {user_name} is logged in successfully!"
    else:
        return "Please log in."
```

### Explanation:
1. **Callback Definition**  
   - Listens for changes in `token_data` (authentication info).
   - Reads `entity_data` (user-related information).
   
2. **Processing Token Data**  
   - Extracts `user_data` to determine the logged-in user.
   - Defaults to `"Unknown User"` if no data is found.

3. **Logging the Login Event**  
   - Calls `get_logger(token_data)` to create a logger instance.
   - Logs the operation: *User logged in successfully.*  
   - See [Logger](#logger) for a deeper explanation.

4. **Returning the Response**  
   - If login is successful, displays a welcome message.
   - Otherwise, prompts the user to log in.

---

## Running the App

```python
if __name__ == "__main__":
    app.run_server(debug=False, port=config["PORT"], host=config["HOST"])
```

### Explanation:
- Runs the Dash app.
- Uses **config["PORT"]** and **config["HOST"]** to define the server settings.

---

## Further Reading

- **[Configuration](#configuration)**: Details on loading settings from `PARAMS.py`.  
- **[Layout](#layout)**: How `get_static_layout` structures the UI.  
- **[Logger](#logger)**: Explanation of logging in `bfabric_web_apps`.  