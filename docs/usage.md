# Usage

This section explains **how to use `bfabric_web_apps`** with the help of the **bfabric_web_app_template**.  
The **bfabric_web_app_template** provides a structured starting point.  
After discussing the **bfabric_web_app_template**, we will explore the **core functions of `bfabric_web_apps`** in detail.

---

## Overview

The **bfabric_web_app_template** consists of **three key files**:

### 1. `index.py` – The Full-Featured Template
Designed for **complex applications**, this template includes:
   - A **sidebar** with interactive **Dash** components.
   - A **main content** area that updates dynamically.
   - **Authentication handling** to restrict access.
   - **Extensive logging** for user actions and debugging.
   - **Optional B-Fabric API integration** for data access and modifications.

### 2. `index_basic.py` – The Minimal Template
A **lightweight alternative** suited for **quick-start projects**:
   - **No sidebar** or extra UI components.
   - Displays a **basic login check**.
   - Implements **minimal logging** (only logs successful logins).
   - Ideal for **small apps, prototypes, or testing**.

### 3. `generic_bfabric.py` – The Core File
This **must not be modified**, as it provides:
   - **Authentication handling** via B-Fabric tokens.
   - **Bug reporting** and essential system callbacks.
   - **The Dash app instance**, which both templates rely on.
   - **Breaking this file may cause authentication failures.**

> **Important:** All modifications—such as adding callbacks, logging, or UI changes—should be made in **`index.py`** or **`index_basic.py`**.  
> **`generic_bfabric.py`** should remain unchanged.

---

## Choosing the Right Template

| Feature                 | `index_basic.py` | `index.py` |
|-------------------------|-----------------|------------|
| **Authentication**      | ✅ Yes           | ✅ Yes      |
| **Logging**             | ✅ Minimal       | ✅ Extensive |
| **Sidebar UI**          | ❌ No           | ✅ Yes      |
| **Dynamic Callbacks**   | ❌ No           | ✅ Yes      |
| **Power User Access**   | ❌ No           | ✅ Yes      |
| **Use Case**            | Simple apps, testing | Full-featured apps |

### When to Use `index_basic.py`
- You **only need authentication** (e.g., checking if a user is logged in).
- You **don’t need a sidebar** or extra UI components.
- You want a **quick start** with minimal code.
- You just want to **log basic events** (e.g., logins).

### When to Use `index.py`
- You need **interactive UI elements** (sidebar, buttons, sliders).
- You want **detailed logging** of user actions.
- You need **B-Fabric API access** to fetch and modify entity data.
- You plan to develop a **full-fledged B-Fabric web application**.

---

## Key Functions in `bfabric_web_apps`

Both `index_basic.py` and `index.py` rely on several **bfabric_web_apps** functions:

- **`create_app()`** – Initializes the Dash application (defined in `generic_bfabric.py`).
- **`load_config()`** – Reads `PARAMS.py` for app settings (host, port, debug mode).
- **`get_static_layout()`** – Provides a reusable layout structure (main UI + documentation tab).
- **`process_url_and_token()`** – Handles **authentication** via B-Fabric tokens.
- **`submit_bug_report()`** – Enables built-in bug reporting functionality.
- **`get_logger()`** and **`log_operation()`** – Manage **logging** for user actions, errors, and system events.
- **`get_power_user_wrapper()`** – Provides access to **B-Fabric API operations**.

---

## Next Steps

Now that you understand the structure, the next sections will explore:
1. **`index.py`** – Its extended functionality, including UI components.
2. **`index_basic.py`** – How it is built and how it works.
3. **`bfabric_web_apps` functions** – Detailed explanations of authentication, logging, and API integration.