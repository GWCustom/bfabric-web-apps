# Minimal Template - index_basic.py

This chapter provides a step-by-step breakdown of the **index_basic.py** script. It explains key functions and their roles in setting up a **basic but functional** B-Fabric web application.

---

## View the Demo  

Before diving into the details, you can preview a **live demo** of this template:

[View the Demo](https://small-template-d12.bfabric.org/)  

This will give you an idea of how the **Minimal Template** looks and functions.

---

## Prerequisites

Before starting, ensure familiarity with:
- [Dash Fundamentals](https://dash.plotly.com/layout)
- [bfabric_web_apps Documentation](bfabric_web_apps_functions.md)  

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

## **Creating a Callback for User Display**  

This callback function dynamically updates the **user display** based on authentication status and the associated application details.

### **How It Works**
- **Listens for authentication changes** using `token_data`.  
- **Extracts user information** from `token_data` and **application details** from `app_data`.  
- **Logs the login event** using [`get_logger`](bfabric_web_apps_functions.md#get-logger).  
- **Updates the UI** to show the username, application name, and description if authenticated; otherwise, prompts for login.

```python
@app.callback(
    Output('user-display', 'children'),
    Input('token_data', 'data'),
    State('app_data', 'data')
)
def update_user_display(token_data, app_data):
    if token_data and app_data:
        user_name = token_data.get("user_data", "Unknown User")
        app_name = app_data.get("name", "Unknown App")
        app_description = app_data.get("description", "Unknown App")

        # Initialize logger and log the login event
        L = get_logger(token_data)
        L.log_operation("User Login", "User logged in successfully.")

        return html.Div([
            html.P(f"User {user_name} has successfully logged in!"),
            html.Br(),
            html.P(f"Application Name: {app_name}"),
            html.P(f"Application Description: {app_description}")
        ])

    else:
        return "Please log in."
```

### **Arguments**
- **`token_data` (dict or None)** – Contains user authentication token data.  
- **`app_data` (dict or None)** – Contains application details such as name and description.  

### **Returns**
- **`html.Div`** – A UI component displaying the login status, application name, and description.  
- **`str`** – `"Please log in."` if authentication data is missing.  

### **Return Type**
- `html.Div | str`

---

## Running the App  

This section ensures the app **runs on the correct server settings**.

```python
if __name__ == "__main__":
    app.run_server(debug=False, port=PORT, host=HOST)
```

### Explanation  
- **`PORT` and `HOST`** define the server's **address and port number** (imported from `bfabric_web_apps`).  

