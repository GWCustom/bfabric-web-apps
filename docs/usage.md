# Usage

This section explains how to use **bfabric-web-apps** in detail, with a special focus on **`index.py`**, where you’ll write most of your **custom logic**. By the end, you’ll understand how **authentication**, **logging**, **layouts**, and the **B-Fabric API** work together to power your custom B-Fabric web applications.

> **Important**: The file **`generic_bfabric.py`** contains core callbacks and essential code that should **not** be modified. All your customizations—new callbacks, layout changes, logging logic, etc.—should live in **`index.py`**.

---

## Overview

A typical **bfabric-web-app** project revolves around two files:

1. **`index.py`**  
   - **Where you**:  
     - Define and customize your **Dash layout**.  
     - Add or modify **callbacks** for user interactions.  
     - Configure **logging** and advanced B-Fabric **API** usage.  
   - **Exposes** a function called `update_ui` in the template (you can rename or add more callbacks if needed).

2. **`generic_bfabric.py`**  
   - Houses essential **authentication** and **bug-reporting** callbacks.  
   - Creates the core **Dash `app`** instance.  
   - Should be left **unmodified** to avoid breaking core functionality.

Here’s how the library’s key functions fit into your workflow:

- **`create_app()`** – Initializes the Dash application (found in `generic_bfabric.py`).  
- **`load_config()`** – Reads your `PARAMS.py` file for app settings (host, port, debug, etc.).  
- **`get_static_layout()`** – Provides a reusable layout structure (main UI + docs tab).  
- **`process_url_and_token()`** – Automatically handles **authentication** via B-Fabric tokens.  
- **`submit_bug_report()`** – Offers a ready-to-use method for logging bugs.  
- **`get_logger()`** and **`log_operation()`** – Simplify **logging** of user actions, errors, or custom events.  
- **`get_power_user_wrapper()`** – Provides advanced, low-level **B-Fabric API** operations (e.g., fetching entity details, running custom queries).

---

## 1. `index.py` – Your Main Workspace

Since **`generic_bfabric.py`** is hands-off, **`index.py`** is where you’ll do all your work. A typical `index.py` looks like this:

```python
from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

# Import essential bfabric-web-apps functions
from bfabric_web_apps import (
    load_config,
    get_static_layout,
    get_logger,
    get_power_user_wrapper
)

# Import the core app instance & essential callbacks from generic_bfabric
import generic_bfabric
from generic_bfabric import app

# 1) Define your sidebar (or other UI components)
sidebar = [ ... ]

# 2) Build your main layout with Dash/Bootstrap
app_specific_layout = dbc.Row([...])

# 3) Define documentation content (optional)
documentation_content = [ ... ]

# 4) Load your config (PORT, HOST, DEV, etc.)
config = load_config("./PARAMS.py")

# 5) Set the app title
app_title = "Bfabric App Template"

# 6) Create the final app layout using get_static_layout
app.layout = get_static_layout(
    app_title,
    app_specific_layout,
    documentation_content
)

# 7) Define any custom callbacks here
@app.callback(...)
def update_ui(...):
    # Manage UI based on token_data, user input, etc.
    ...

# 8) Run the application
if __name__ == "__main__":
    app.run_server(debug=True, port=config["PORT"], host=config["HOST"])
```

Let’s explore the **key steps** in more detail.

---

## 2. Authentication (Auth)

### How Authentication Works
- **`process_url_and_token()`** in `generic_bfabric.py` intercepts the token from the **`url`** component.
- This token is stored in **`token_data`** (a `dcc.Store`), which you check or reference in your `update_ui` function.

**Example** in `index.py`:
```python
@app.callback(
    [Output('sidebar_text', 'hidden'), ...],
    [Input('token_data', 'data')],
)
def update_ui(token_data):
    # If there's no token, disable everything
    if not token_data:
        return (True, ...)
    # Otherwise, allow normal usage
    return (False, ...)
```
---

## 3. Logging

**bfabric-web-apps** provides a simple yet powerful **logging** system that allows you to track user actions, API calls, and errors for **auditing**, **debugging**, and **compliance** purposes. You’ll interact with the logger in two main ways:

1. **`log_operation(...)`** – Log a specific event or message.  
2. **`logthis(...)`** – Wrap an **API call** to automatically log its parameters and result context.

Below is a **step-by-step guide** to setting up and using the logger in your **`index.py`** file.

---

### 1. Getting a Logger

**Always obtain your `Logger` instance after you confirm the user is authenticated**, because the logger depends on **`token_data`** to determine user credentials and environment.

```python
from bfabric_web_apps import get_logger

def update_ui(token_data, ...):
    # If the user is authenticated, get the logger
    if token_data:
        L = get_logger(token_data)  # Returns a Logger instance
    else:
        L = None
    ...
```

- **`get_logger(token_data)`**:
  - Reads key fields from `token_data` (like `jobId`, `user_data`, `environment`).
  - Constructs a `Logger` object that’s ready to store and flush logs to B-Fabric.

---

### 2. Using `log_operation(...)`

**`log_operation(operation, message, params=None, flush_logs=True)`** is the simplest way to log a discrete event:

```python
L.log_operation(
    operation="ExampleOperation", 
    message="User triggered an example operation",
    params={"button_id": "btn-1"},
    flush_logs=True
)
```

- **`operation`** – A short label, like `"Submit Bug"`, `"Fetch Data"`, or `"Authentication Check"`.
- **`message`** – A descriptive string about what happened.
- **`params`** – (Optional) A dictionary of extra details you want to store.
- **`flush_logs`** – If `True`, the log immediately writes to B-Fabric; if `False`, it stays in memory until a later flush.

**Use cases**:
- Recording **button clicks**, **page loads**, or **custom warnings**.
- **batching** logs by setting `flush_logs=False` and then calling `L.flush_logs()` at the end of your process.

Example:
```python
if L:
    L.log_operation(
        operation="UserLogin",
        message="User successfully logged in",
        params={"user": token_data["user_data"]},
        flush_logs=False
    )
    # do some more stuff...
    L.flush_logs()  # Actually write everything at once
```

---

### 3. Using `logthis(...)`

**`logthis(...)`** is designed to **wrap** an API call (like a B-Fabric operation) and automatically log both the **call** and **result context**. It’s especially useful when you want consistent, structured logging around external service calls.

```python
# Suppose we have an authenticated B-Fabric power user wrapper
power_user_wrapper = get_power_user_wrapper(token_data)

# Wrap the 'read' call using L.logthis
lane_samples = L.logthis(
    api_call=power_user_wrapper.read,
    endpoint="rununitlane",
    obj={"id": [123, 456]},    # Example request data
    max_results=None,
    flush_logs=False           # Defer writing logs
)
```

1. **`api_call`** – The function you’re calling (e.g., `power_user_wrapper.read`).  
2. **Positional and keyword args** – You pass them directly into `logthis`, which forwards them to the actual function. In this example, we pass `endpoint`, `obj`, and `max_results` as named arguments.  
3. **`params`** – Optional logging parameters (like in `log_operation`).  
4. **`flush_logs`** – Whether to push logs immediately or batch them.

**How It Works**:
- Executes the function (`power_user_wrapper.read(...)`) with your arguments.  
- Builds a descriptive log message (e.g., `"read(endpoint='rununitlane', obj={'id': [123, 456]}, max_results=None)"`).  
- Calls `log_operation(...)` behind the scenes to store the log entry.  
- Returns whatever the actual API call returns (e.g., the data from B-Fabric).

**Example** with more detail:

```python
# The user clicked a button to fetch data from B-Fabric
if L and token_data:
    # Wrap a B-Fabric read operation to automatically log it
    fetched_data = L.logthis(
        api_call=power_user_wrapper.read,
        endpoint="sample",
        obj={"id": [789]},
        flush_logs=True
    )
    # 'fetched_data' now contains the result from B-Fabric's read call
    # Meanwhile, a log entry describing the call is saved in your logs
```

---

### 4. `Logger` Under the Hood

**`Logger`** internally:
- Stores log messages in a **local list** (`self.logs`) until you flush them.
- On flush (either automatic or manual), it calls `power_user_wrapper.save("job", {...})` to **append** these logs to the specified job record in B-Fabric, associating them with the user and environment.

**Important**:
- If you never **flush** logs, they won’t appear in B-Fabric.
- If your `token_data` lacks valid credentials, the logger can’t save logs to B-Fabric.

---

### Best Practices & Tips

1. **Initialize the Logger Once** per callback session:
   ```python
   def update_ui(token_data, ...):
       L = get_logger(token_data) if token_data else None
       ...
   ```
2. **Use `log_operation`** for **simple events** (button clicks, validations, data transformations).
3. **Use `logthis`** for **API calls** or **complex interactions** (queries, data fetches, inserts).
4. **Control Log Flow** with `flush_logs=False` if you want to batch multiple log entries, then `L.flush_logs()` when you’re ready.
5. **Check B-Fabric** to ensure logs appear as expected. If they don’t:
   - Verify the user has the correct **permissions**.
   - Confirm **`jobId`** (or environment data) is set in `token_data`.
   - Look for **exceptions** printed in the console.
```

### More Advanced Logging
- Use `logthis` decorator to **wrap** function calls and auto-log.
- Adjust **`flush_logs`** if you want logs to be written immediately or batched.

---

## 4. Layouts

### Using `get_static_layout()`
`get_static_layout(app_title, main_layout, doc_content)`:

1. **`app_title`**: String for the browser tab title.
2. **`main_layout`**: A Dash layout you create (commonly a `dbc.Row` or `dbc.Container`).
3. **`doc_content`**: A list of Dash/HTML components shown when the user clicks the “Documentation” tab in your app’s top menu.

### Example
```python
sidebar = [
    html.P("Sidebar Header"),
    dcc.Slider(...),
    ...
]

app_specific_layout = dbc.Row([
    dbc.Col(sidebar, width=3),
    dbc.Col(..., width=9)
])

documentation_content = [
    html.H2("About This App"),
    html.P("Detailed usage instructions..."),
]

app.layout = get_static_layout(app_title, app_specific_layout, documentation_content)
```

### Customizing Layout
- Add or remove columns, sidebars, or new tabs.  
- Swap out `dbc.Row` for your own container design.  
- Include advanced Dash components (plots, interactive controls, etc.) in `app_specific_layout`.

---

## 5. B-Fabric API

### Why Use the Power User Wrapper?
By default, **bfabric-web-apps** abstracts many calls for you. However, if you need **direct** or **advanced** access to B-Fabric data, you’ll use:

```python
from bfabric_web_apps import get_power_user_wrapper

power_user_wrapper = get_power_user_wrapper(token_data)
```

### Common Use Cases
1. **Fetch Detailed Entity Info**  
   ```python
   details = power_user_wrapper.get_entity_details(
       token_data["entityClass_data"],
       token_data["entity_id_data"]
   )
   ```
2. **Run Custom Queries**  
   If your version of bfabric-web-apps or B-Fabric API supports specialized calls, you can call them here.
3. **Update or Create Entities**  
   Insert or modify B-Fabric records (samples, projects, etc.) if your user has permissions.

**Note**: The actual methods on `power_user_wrapper` can vary. Check the **bfabric-web-apps** or B-Fabric API docs for available functions.

---

## 6. Callbacks & User Interaction

### Defining New Callbacks
In `index.py`, you have **one** example callback: `update_ui`. You can **add as many** as you need. All standard **Dash** rules apply:

```python
@app.callback(
    Output("my-div", "children"),
    Input("my-button", "n_clicks"),
    State("my-input", "value")
)
def do_something(n_clicks, user_value):
    # Possibly log an operation
    L.log_operation("User Action", f"Clicked {n_clicks} times, user typed: {user_value}")
    return f"You typed: {user_value}"
```

### Keep `generic_bfabric.py` Intact
- That file houses crucial callbacks for **auth** and **bug reports**.  
- If you break them, your token handling or bug reporting might fail.

---

## 7. Tying It All Together

Let’s look at how everything flows during a typical user session:

1. **User clicks a link** from B-Fabric containing a token parameter (e.g., `https://your-app?token=abc123`).  
2. **`generic_bfabric.py`** extracts the token → stores it in **`token_data`**.  
3. **`index.py`** sees `token_data`, logs user actions, and customizes the UI.  
4. If the user performs advanced actions (e.g., fetching more details), you do:
   ```python
   power_user_wrapper = get_power_user_wrapper(token_data)
   details = power_user_wrapper.get_entity_details(...)
   ```
5. Meanwhile, you track logs using **`L.log_operation(...)`**.  
6. The user sees dynamic updates in your **Dash** layout, built by `get_static_layout()` and any **custom** layout code.

---

## Summary

- **`index.py`** is your primary file to **edit** and **extend**:
  - **Add custom UI** (sidebar, main content, docs).
  - **Define callbacks** for user interactions.
  - **Use the logger** to track events.
  - **Call the B-Fabric API** via the power user wrapper.
- **`generic_bfabric.py`** is a **core** module that handles:
  - **Authentication** (via `process_url_and_token`).
  - **Bug reporting** with `submit_bug_report`.
  - **Dash app creation** (`create_app()`).

With **bfabric-web-apps**, you can **rapidly** develop **interactive** LIMS tools for **B-Fabric**, saving time on boilerplate and focusing on the features that **truly matter** for your scientific or data-driven environment. If you need to learn more, see the official [bfabric-web-app-template](https://github.com/GWCustom/bfabric-web-app-template) or consult the [bfabric-web-apps](https://github.com/GWCustom/bfabric-web-apps) GitHub for advanced usage examples.
