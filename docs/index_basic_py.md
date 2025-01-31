# Minimal Template - `index_basic.py`

This chapter provides a step-by-step breakdown of the `index_basic.py` script. It explains key functions and their roles in setting up a **basic but functional** B-Fabric web application.

---

## View the Demo  

Before diving into the details, you can preview a **live demo** of this template:

[View the Demo](https://small-template-d12.bfabric.org/)  

This will give you an idea of how the **Minimal Template** looks and functions.

---

## Running the Template  

To execute the template:

1. Run the following command in your terminal:  
   ```sh
   python index_basic.py
   ```
2. Open your browser and go to `localhost`.

---

## Importing Dependencies  

This section covers the **necessary imports** that make the template functional.

```python
from dash import html, dcc, Input, Output, State
from generic_bfabric import app
from bfabric_web_apps import get_static_layout, get_logger, HOST, PORT
import dash_bootstrap_components as dbc
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
   - **HOST & PORT**: Define **server configurations** (imported from `bfabric_web_apps`).  

---

## Setting Up the App Title  

The **title** of the application is defined here.

```python
app_title = "My B-Fabric App (Basic)"
```

### Explanation  
- This **title appears in the browser tab** and is used inside **[`get_static_layout`](bfabric_web_apps_functions.md#get-static-layout)** to maintain a consistent UI.  

---

## Defining the Layout  

This section defines the **structure of the app**, including the sidebar and main content.

```python
app_specific_layout = dbc.Row([
    dbc.Col(
        html.Div(style={"border-right": "2px solid #d4d7d9", "height": "70vh", "padding": "20px"}),
        width=3,  # Sidebar placeholder.
    ),
    dbc.Col([
        html.H1("Welcome to The Sample B-Fabric App", style={"margin": "2vh 0 2vh 0"}),
        html.Div(id='user-display', style={"margin": "2vh 0 2vh 0"}),
    ], width=9)
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

### Explanation  
- **`app_specific_layout`**: Defines **two columns**:
  - A **left sidebar** (currently empty, but can be extended).
  - A **main content area**, including:
    - A **welcome message**.
    - A **user display section** (`id='user-display'`), which updates dynamically based on login status.

- **`get_static_layout()`**:
  - Combines the **title**, **app layout**, and **documentation section**.
  - Uses **[`get_static_layout`](bfabric_web_apps_functions.md#get-static-layout)** for consistency across B-Fabric applications.

---

## Creating a Callback for User Display  

This callback function updates the **user display** dynamically based on authentication status.  

### **How It Works**
- **Listens for authentication changes** using `token_data`.  
- **Extracts user information** from `entity_data`.  
- **Logs the login event** using [`get_logger`](bfabric_web_apps_functions.md#get-logger).  
- **Updates the UI** to show the username if authenticated, otherwise prompts for login.  

```python
@app.callback(
    Output('user-display', 'children'),
    Input('token_data', 'data'),
    State('entity', 'data')
)
def update_user_display(token_data, entity_data):
    if token_data and entity_data:
        user_name = token_data.get("user_data", "Unknown User")  
        
        # Initialize the logger
        L = get_logger(token_data)  
        L.log_operation("User Login", "User logged in successfully.")
        
        return f"User {user_name} is logged in successfully!"
    else:
        return "Please log in."
```

#### **Args:**  
- **`token_data` (dict or None)** – User authentication token data.  
- **`entity_data` (dict or None)** – Entity information linked to the user.  

#### **Returns:**  
- **`str`** – A message indicating login success or prompting login.  

#### **Return Type:**  
- `str`
---

## Running the App  

This section ensures the app **runs on the correct server settings**.

```python
if __name__ == "__main__":
    app.run_server(debug=False, port=PORT, host=HOST)
```

### Explanation  
- **`PORT` and `HOST`** define the server's **address and port number** (imported from `bfabric_web_apps`).  

---

## Further Reading  

- **[Dash Callbacks](https://dash.plotly.com/basic-callbacks)**: Learn more about Dash interactions.  
- **[Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)**: Enhance UI elements.  
- **[bfabric_web_apps Functions](bfabric_web_apps_functions.md)**: Detailed explanations of helper functions like `get_static_layout`, `get_logger`, and authentication handling.  
