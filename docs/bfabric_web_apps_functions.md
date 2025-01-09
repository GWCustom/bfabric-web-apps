# Bfabric\_web\_apps Functions

This section provides an in-depth explanation of the **core functions** used in bfabric\_web\_apps. These functions are responsible for **configuration, authentication, layout management, logging, API interactions, and bug reporting**.

---

## 1. Application Initialization

### create\_app()

```python
from generic_bfabric import app
```

#### Purpose:

- Initializes a **Dash application** pre-configured for B-Fabric.
- Automatically includes token processing and authentication mechanisms.
- Importing app from generic\_bfabric ensures that all **default settings** are applied.

#### Usage:

- You **should not modify** this function.
- Instead, use the app instance to define your **layout** and **callbacks**.

---

## 2. Configuration Management

### load\_config()

```python
config = load_config("./PARAMS.py")
```

#### Purpose:

- Loads **configuration settings** from PARAMS.py.
- Stores key parameters such as:
  - PORT
  - HOST
  - DEV (development mode)
  - Other app-specific settings

#### Usage:

- Used **once** in index.py to set up the environment.
- Example:

```python
if config["DEV"]:
    app.run_server(debug=True, port=config["PORT"])
else:
    app.run_server(debug=False, port=config["PORT"], host=config["HOST"])
```

---

## 3. UI and Layout Management

### get\_static\_layout()

```python
app.layout = get_static_layout(app_title, app_specific_layout, documentation_content)
```

#### Purpose:

- **Combines UI components** (main layout + documentation tab) into a **structured** Dash layout.
- Ensures the **B-Fabric look & feel** is consistent across applications.

#### Parameters:

1. **app\_title** - The title displayed in the browser tab.
2. **app\_specific\_layout** - The main UI content (defined in index.py).
3. **documentation\_content** - Static documentation displayed under the "Documentation" tab.

#### Usage:

- Example:

```python
sidebar = html.Div([...])
content = html.Div([...])
documentation = html.Div([...])

app.layout = get_static_layout("My App", sidebar, documentation)
```

---

## 4. Authentication & Token Handling

### process\_url\_and\_token()

#### Purpose:

- Extracts **authentication tokens** from the URL.
- Stores the token inside a **Dash dcc.Store** component (token\_data).
- Ensures **secure** interaction with B-Fabric.

#### Usage:

- Automatically applied inside generic\_bfabric.py.
- In **custom callbacks**, check the token before allowing actions:

```python
@app.callback(
    Output("auth-message", "children"),
    Input("token_data", "data")
)
def check_auth(token_data):
    if not token_data:
        return "Please log in with a valid token."
    return f"Authenticated as {token_data['user_data']}"
```

---
## 5. Logging

### get_logger()

```python
L = get_logger(token_data)
```

#### Purpose:

- Before logging any actions, we need to **initialize a Logger instance**.
- The logger tracks **user actions, API calls, and errors**.
- Requires **authentication (token_data)** to store logs in B-Fabric.

#### Usage:

- You need token_data to create the logger instance:

```python
if token_data:
    L = get_logger(token_data)
```

---

## Logging Methods

Once we have the logger instance (`L`), we can log actions in two different ways:

### 1. log_operation()

```python
L.log_operation(
    operation="Submit Data",
    message="User submitted a new sample.",
    params={"sample_id": 1234},
    flush_logs=True
)
```

#### Purpose:

- **Manually logs user actions** for auditing and debugging.
- Stores logs in **B-Fabric's job history**.

#### Parameters:

1. **operation** - Short event label (e.g., "Login", "Update Sample").
2. **message** - Descriptive message.
3. **params** - (Optional) Dictionary of **extra** metadata.
4. **flush_logs** - **True** to write logs immediately, **False** to batch logs.

#### Best Practices:

- Log critical user actions:

```python
L.log_operation("FileUpload", "User uploaded a CSV file", {"filename": "data.csv"})
```

- Batch logs for performance:

```python
L.log_operation("UserLogin", "User authenticated", flush_logs=False)
# Perform multiple actions...
L.flush_logs()  # Writes all logs at once
```

---

### 2. logthis()

```python
result = L.logthis(
    api_call=power_user_wrapper.read,
    endpoint="sample",
    obj={"id": [123]},
    flush_logs=True
)
```

#### Purpose:

- **Automatically wraps an API call** and logs:
  - The function name
  - Input parameters
  - Execution time
  - Return values

#### Usage:

- Example with an API read call:

```python
lane_samples = L.logthis(
    api_call=power_user_wrapper.read,
    endpoint="rununitlane",
    obj={"id": [456]},
    flush_logs=True
)
```

- Example with a write operation:

```python
new_entry = L.logthis(
    api_call=power_user_wrapper.save,
    obj={"name": "New Sample"},
    flush_logs=True
)
```

---

## 6. B-Fabric Power User Access

### get\_power\_user\_wrapper()

```python
power_user_wrapper = get_power_user_wrapper(token_data)
```

#### Purpose:

- Provides an **authenticated** wrapper to interact with the **B-Fabric API**.
- Used for API calls that require **Power User** rights.

---

## 7. Submit Bug Report

### generic\_handle\_bug\_report()

```python
def generic_handle_bug_report(n_clicks, bug_description, token, entity_data):
    """
    Handles the submission of bug reports by delegating to the submit_bug_report function.
    """
    return submit_bug_report(n_clicks, bug_description, token, entity_data)
```
