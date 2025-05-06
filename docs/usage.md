# Template Usage

This section explains how to use **bfabric\_web\_apps** with the help of the **bfabric\_web\_app\_template**.

---

```{note}
**Version Compatibility Notice**  
To ensure proper functionality, the `bfabric_web_apps` library and the `bfabric_web_app_template` must have the **same version**. For example, if `bfabric_web_apps` is version `0.1.3`, then `bfabric_web_app_template` must also be `0.1.3`.  

Please verify and update the versions accordingly before running the application.
```

---

## Overview

The **bfabric\_web\_app\_template** provides three ready-to-use starting points:

* **`index.py`** – A full-featured template for complex applications.
* **`index_basic.py`** – A minimal template for simple apps.
* **`index_redis.py`** – A template specifically designed for using Redis queues.

All templates are designed to be **modified and extended** by users, serving as the main entry points for custom B-Fabric web applications.

Additionally, within the **bfabric\_web\_app\_template**, the following files are available:

* **`generic_bfabric.py`** – All templates **import** and **rely** on `generic_bfabric.py` for core functionality.
* **`bfabric_apps_auto_registration.py`** – Calls the [`create_web_app()`](bfabric_web_apps_functions.md#remote-creation-of-web-applications) function to remotely create a B-Fabric web application.

This structure ensures a modular and reusable approach to web application development within B-Fabric.

---

## Modular Structure

B-Fabric web applications built with the **bfabric_web_app** framework generally follow the same modular structure to ensure clarity, maintainability, and flexibility:

### 1. **B-Fabric Integration**

The **GetDataFromBfabric.py** module handles all API interactions with B-Fabric. It retrieves necessary metadata, sample information, and creates the input files (samplesheets) required to execute pipelines or workflows.

### 2. **User Interface**

The **GetDataFromUser.py** module provides a clear, interactive interface where users can view, edit, and manage samplesheets or input data. This component allows users to modify entries, verify details, and ensure data correctness before executing the pipeline.

### 3. **Execution of the Main Job**

The **ExecuteRunMainJob.py** module contains logic and helper functions that manage the execution of the primary computational workflow. It includes managing command-line executions (e.g., bash commands), creating resource paths, handling charges via the **Charge Switch**, and queuing jobs asynchronously using Redis.

Together, these three parts demonstrate the modularity, extensibility, and robustness of the B-Fabric web-app development approach, allowing developers to quickly adapt the general architecture to new applications and use cases.

---

## Choosing the Right Template

This section helps you decide between the **Minimal Template (`index_basic.py`)** and the **Full-Featured Template (`index.py`)** based on your use case. If your application utilizes Redis for asynchronous job execution, consider using the **Redis Template (`index_redis.py`)**.

### Core Integration

Both templates **import** and **rely** on `generic_bfabric.py`, which provides essential functions such as:
✔ **Authentication Handling** via B-Fabric tokens
✔ **Session Management** and user entity tracking
✔ **Bug Reporting System** for issue tracking
✔ **Dynamic Page Title & Session Details**

These functionalities are **built-in** to both templates, so they work out of the box with B-Fabric.

| Feature                             | **Minimal Template (`index_basic.py`)** | **Full-Featured Template (`index.py`)**                     |
| ----------------------------------- | --------------------------------------- | ----------------------------------------------------------- |
| **Integrates `generic_bfabric.py`** | ✅ Yes                                   | ✅ Yes                                                       |
| **Logging**                         | ✅ Minimal (only login events)           | ✅ Extensive (logs multiple actions)                         |
| **Dynamic Variable Configuration**  | ❌ No                                    | ✅ Yes (sets default variables like config paths and emails) |
| **Sidebar UI**                      | ❌ No                                    | ✅ Yes (includes dropdowns, sliders, and text input)         |
| **Dynamic Callbacks**               | ❌ No                                    | ✅ Yes (interactive UI with callbacks)                       |
| **Power User Features**             | ❌ No                                    | ✅ Yes (enables power-user access)                           |
| **Use Case**                        | Simpler starting point                  | Full-featured starting point                                |

---

> **Important:**
>
> * **`generic_bfabric.py`** is a **core system file** and **must not be modified**. Any changes to this file may break authentication or system integration.
> * **All customization** (for example, adding UI components, callbacks, or logging) should be done in **`index.py`, `index_basic.py`, or `index_redis.py`**.

---

## Next Steps

Now that you understand the structure, the next sections will explore:

1. **[Template Deployment Guide](installation_template.md)**
2. **[Full-Featured Template (`index.py`)](index_py.md)**
3. **[Minimal Template (`index_basic.py`)](index_basic_py.md)**
4. **[Redis Template (`index_redis.py`)](index_redis.md)**