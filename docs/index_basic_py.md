# Minimal Template

This chapter provides a step-by-step breakdown of the **index_basic.py** script. It explains key functions and their roles in setting up a **basic B-Fabric web application**.

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

4. **Dash Bootstrap Components (DBC)**  
   - Provides **pre-styled UI elements** to enhance the look and functionality of the app.  

---

## Setting Up the App Title  

The **application title** provides a clear and identifiable name for the B-Fabric web app. This title appears in the **UI header** and helps users understand the purpose of the application.

```python
app_title = "My B-Fabric App (Basic)"
```

### Explanation  
- This title is used inside **[`get_static_layout`](bfabric_web_apps_functions.md#get-static-layout)** to maintain a consistent UI.  

---

## Designing the Main Page

The **application layout** organizes the **sidebar and main content area** into a structured, two-column design. The **left column** houses interactive elements for user input, while the **right column** displays content dynamically based on authentication and user selections.  

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
```

### Explanation  
- **app_specific_layout**: Defines **two columns**:
  - A **left sidebar** (currently empty, but can be extended).
  - A **main content area**, including:
    - A **welcome message**.
    - A **user display section** (id='user-display'), which updates dynamically based on login status.

---

## Defining the Documentation Section

The **documentation section** provides users with an introduction to the **B-Fabric App Template** and links to external resources for further learning.  

```python
documentation_content = [
    html.H2("Documentation"),
    html.P("Describe your app's features here.")
]
```

### Explanation  
- **Header (html.H2)** – Displays a **title** for the documentation section.  
- **Content (html.P)** – Placeholder for future documentation, explaining the **purpose of the application** and its customization options.  

---

## Integrating the App Layout

The `app.layout` function **establishes the final structure** of the application by integrating the **title, main content, and documentation** into a cohesive layout. This ensures a **consistent user experience** across all pages.  

```python
app.layout = get_static_layout(
    app_title,  # Application title
    app_specific_layout,  # The main content for the app
    documentation_content  # Documentation section
)
```

### Explanation  
- Uses **[`get_static_layout`](bfabric_web_apps_functions.md#get-static-layout)** to maintain a **consistent page structure** throughout the application.  
- **app_title** – Defines the **main heading** of the application.  
- **app_specific_layout** – Contains the **sidebar and main content area**.  
- **documentation_content** – Displays **informational resources** for users.  


---

## Callback for User Display

This callback **dynamically updates the UI** to reflect user authentication status and application information.  

For more details on Dash callbacks, see: **[Dash Callbacks Documentation](https://dash.plotly.com/basic-callbacks)**  

---

### Callback Definition

The callback **listens for authentication** (`token_data`) and **application details** (`app_data`) and decides what to display in the `user-display` component.

```python
@app.callback(
    Output('user-display', 'children'),
    Input('token_data', 'data'),
    State('app_data', 'data')
)
```

### Explanation
- **Output:**  
  - **`user-display`**: A Dash component to show user/app data or a login prompt.  
- **Input:**  
  - **`token_data`**: Tracks user authentication status.  
- **State:**  
  - **`app_data`**: Stores application information (e.g., name, description).

---

### Handling User and Application Data

```python
def update_user_display(token_data, app_data):
    if token_data and app_data:
        user_name = token_data.get("user_data", "Unknown User")
        app_name = app_data.get("name", "Unknown App")
        app_description = app_data.get("description", "Unknown App")
```

### Explanation
- Checks if both `token_data` and `app_data` exist.  
- Retrieves:
  - **`user_name`** from `token_data`.
  - **`app_name`** and **`app_description`** from `app_data`.  

---

### Logging the Event

```python
        # Initialize logger and log the login event
        L = get_logger(token_data)
        L.log_operation("User Login", "User logged in successfully.")
```

### Explanation
- The **['get_logger'](bfabric_web_apps_functions.md#get-logger)** method is used to capture user actions.  
- The **[`log_operation`](bfabric_web_apps_functions.mdl#log-operation)** method records a **“User Login”** event in the logs.

---

### Return Statements

```python
        return html.Div([
            html.P(f"User {user_name} has successfully logged in!"),
            html.Br(),
            html.P(f"Application Name: {app_name}"),
            html.P(f"Application Description: {app_description}")
        ])
    else:
        return "Please log in."
```

### Explanation
1. **If authenticated** (both `token_data` and `app_data` present):  
   - Returns an `html.Div` showing the user’s name, application name, and application description.  

2. **If not authenticated** (missing data):  
   - Returns the string **"Please log in."**, prompting the user to authenticate.


---

## Running the App  

This section ensures the app **runs on the correct server settings**.

```python
if __name__ == "__main__":
    app.run_server(debug=False, port=PORT, host=HOST)
```

### Explanation
- **`PORT` and `HOST`** define the server’s **address and port number**.
- These values are **imported by default from the `bfabric_web_apps` module**. If you want to modify them, refer to the **[Global Configuration Variables](bfabric_web_apps_functions.md#dynamic-variable-configuration)** chapter for more information.
