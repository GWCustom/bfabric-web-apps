# Redis Template

This chapter provides a step-by-step breakdown of the **index_redis.py** script. It demonstrates how to use Redis queues to submit background jobs and bulk-create resources within a B-Fabric web application.

---

## Overview and Version Check

Before running this application, ensure that the versions of `bfabric_web_apps` and `bfabric_web_app_template` match exactly. For example, if one is version `0.1.3`, the other must also be `0.1.3`. This avoids compatibility issues.

---

## Importing Dependencies

```python
from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import bfabric_web_apps
from generic.callbacks import app
from generic.components import no_auth
from pathlib import Path
```

This script imports required modules for:
- UI layout (`dash`, `dash_bootstrap_components`)
- B-Fabric support (`bfabric_web_apps`)
- Core components and callbacks shared across templates

---

## Global Configuration

```python
bfabric_web_apps.CONFIG_FILE_PATH = "~/.bfabricpy.yml"
bfabric_web_apps.DEVELOPER_EMAIL_ADDRESS = "griffin@gwcustom.com"
bfabric_web_apps.BUG_REPORT_EMAIL_ADDRESS = "gwtools@fgcz.system"
```

Customizes app-wide global settings like config path and email contacts.

---

## Sidebar Layout

Defines the interactive UI components, including a **charge switch**, **slider**, **dropdowns**, and **input field**:

```python
sidebar = bfabric_web_apps.components.charge_switch + [...]
```

Notable elements include:
- **Charge switch** – Toggles whether the job should be charged
- **Slider** – Specifies how many resources to create
- **Dropdowns** – Choose target project and job queue
- **Text Input** – Content to write to the resource
- **Submit Button** – Opens confirmation modal

---

## Modal Confirmation

Displays a confirmation popup before triggering resource creation.

```python
modal = dbc.Modal([...], id="modal-confirmation", is_open=False)
```

---

## Alert System

Displays success or error alerts based on job submission outcome.

```python
alerts = dbc.Alert(...)
```

---

## Main Application Layout

Combines the sidebar and main content area in a 2-column responsive layout.

```python
app_specific_layout = dbc.Row([...])
```

---

## Documentation Section

Provides users with an overview of the template and links to official documentation.

```python
documentation_content = [html.H2(...), html.P(...)]
```

---

## Static Layout Initialization

Assembles the final app layout using `get_static_layout()`:

```python
app.layout = bfabric_web_apps.get_static_layout(...)
```

Also configures layout features like the **workunit tab**, **queue selection**, and **bug reporting**.

---

## Modal Trigger Callback

```python
@app.callback(...)
def toggle_modal(...):
    if n1 or n2:
        return not is_open
```

Toggles the confirmation modal when the submit button is clicked.

---

## Sidebar UI Activation Logic

```python
@app.callback(...)
def update_ui(...):
    ...
    if not entity_data or not token_data:
        auth_div_content = html.Div(children=no_auth)
    else:
        auth_div_content = dbc.Row([...])
```

Disables components for unauthenticated users and shows entity-specific data if available.

---

## Job Submission with Redis Queue

Handles workunit and resource creation, then enqueues the job to Redis.

```python
@app.callback(...)
def submission(...):
    ...
    bfabric_web_apps.q(queue).enqueue(
        bfabric_web_apps.run_main_job,
        kwargs=arguments
    )
```

Includes:
- File attachments
- Resource file creation using bash
- Target queue submission
- Charge control

---

## Running the Application

```python
if __name__ == "__main__":
    app.run(debug=..., port=..., host=...)
```

---

## Summary

This template is ideal for applications that:
- Perform **batch processing**
- Need **background execution** via Redis
- Create **multiple workunits/resources** from UI input
- Require **charge tracking** and **job logging**

---

For Redis setup and worker execution, refer to the **[deployment guide](installation_template.md)**.