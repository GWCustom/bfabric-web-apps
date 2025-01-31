# Template Usage

This section explains how to use **bfabric_web_apps** with the help of the  **bfabric_web_app_template**.

---

## Overview

The **bfabric_web_app_template** provides two ready-to-use starting points:  

- **`index.py`** – A full-featured template for complex applications.
- **`index_basic.py`** – A minimal template for simple apps.

Both templates are designed to be **modified and extended** by users, serving as the main entry points for custom B-Fabric web applications.

---

## Choosing the Right Template

This section helps you decide between the **Minimal Template (`index_basic.py`)** and the **Full-Featured Template (`index.py`)** based on your use case.

### Core Integration  
Both templates **import** and **rely** on `generic_bfabric.py`, which provides essential functions such as:  
✔ **Authentication Handling** via B-Fabric tokens  
✔ **Session Management** and user entity tracking  
✔ **Bug Reporting System** for issue tracking  
✔ **Dynamic Page Title & Session Details**  

These functionalities are **built-in** to both templates, so they work out of the box with B-Fabric.

| Feature                   | **Minimal Template (`index_basic.py`)** | **Full-Featured Template (`index.py`)** |
|---------------------------|--------------------------------|--------------------------------|
| **Integrates `generic_bfabric.py`** | ✅ Yes | ✅ Yes |
| **Logging**               | ✅ Minimal (only login events) | ✅ Extensive (logs multiple actions) |
| **Dynamic Variable Configuration** | ❌ No | ✅ Yes (sets default variables like config paths and emails) |
| **Sidebar UI**            | ❌ No | ✅ Yes (includes dropdowns, sliders, and text input) |
| **Dynamic Callbacks**      | ❌ No | ✅ Yes (interactive UI with callbacks) |
| **Power User Features**    | ❌ No | ✅ Yes (enables power-user access) |
| **Use Case**              | Simpler starting point | Full-featured starting point |

---

> **Important:**  
> - **`generic_bfabric.py`** is a **core system file** and **must not be modified**. Any changes here may break authentication or system integration.  
> - **All customization** (e.g., adding UI components, callbacks, or logging) should be done in **`index.py` or `index_basic.py`**.  

---

## Next Steps  

Now that you understand the structure, the next sections will explore:  

1. **[Full-Featured Template (`index.py`)](index_py.md)**  
2. **[Minimal Template (`index_basic.py`)](index_basic_py.md)**  