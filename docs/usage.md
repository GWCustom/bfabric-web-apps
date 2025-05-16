# Template Usage

This section explains how to use **bfabric\_web\_apps** with the help of the **bfabric\_web\_app\_template**.

---

```{note}
**Version Compatibility Notice**  
To ensure proper functionality, the `bfabric_web_apps` library and the `bfabric_web_app_template` must have the **same version**. For example, if `bfabric_web_apps` is version `0.1.3`, then `bfabric_web_app_template` must also be `0.1.3`.  

Please verify and update the versions accordingly before running the application.
```

---


## bfabric_web_apps Application Structure

B-Fabric web applications built with the `bfabric_web_apps` library follow a modular design that ensures clarity, maintainability, and flexibility. Each app typically implements the following three core components:

### 1. **Collect User Data**

This step provides a user-friendly Dash interface where users can configure parameters such as CPU, RAM, reference files, email address, and Charge Switch settings. It also allows users to review and edit sample metadata before submitting a job.

### 2. **Collect B-Fabric Data**

This component manages interactions with the B-Fabric API. It retrieves relevant project, dataset, and sample metadata needed for job execution. The collected data is typically used to generate sample sheets or other input files for the workflow.

### 3. **Invoke Application**

This part contains the core logic for executing the computational workflow. It builds execution commands (e.g., for Nextflow), converts input files, configures output paths, queues the job via Redis, and optionally charges the selected B-Fabric container.

---

This architecture highlights the modularity and extensibility of the `bfabric_web_apps` library, enabling developers to rapidly build robust applications that integrate seamlessly with the B-Fabric ecosystem.

---


## Application Types

bfabric_web_apps supports different categories of applications:

- **One-off helper apps** – Small tools such as barcode generators or project-specific utilities.  
- **Big-data apps** – Robust applications that execute pipelines like **nf-core RNA-seq** or **SUSHI-based** workflows, requiring queueing and scalable backend processing.

These app types can be mixed and matched depending on user needs and computing resources.


---

## Redis Integration

**Redis** is used in bfabric_web_apps to support **job queuing** and **decoupled server architecture**. This allows resource-intensive or asynchronous jobs to be executed in background workers, improving performance and reliability of B-Fabric applications.

You can try out a working implementation in the **[Redis Template](index_redis.md)**, which demonstrates:

- How to enqueue background jobs  
- How to transfer files and parameters to job runners  

For more details, refer to the [Redis official documentation](https://redis.io/docs/latest/).

---

## Overview

The **bfabric\_web\_app\_template** provides three ready-to-use starting points:

* **`index_large.py`** – A full-featured template for complex applications.
* **`index_basic.py`** – A minimal template for simple apps.
* **`index_redis.py`** – A template specifically designed for using Redis queues.

All templates are designed to be **modified and extended** by users, serving as the main entry points for custom B-Fabric web applications.

Additionally, within the **bfabric\_web\_app\_template**, the following files are available:

 * **`generic` folder** – All templates **import** and **rely** on modules within the `generic` folder for core functionality.
* **`bfabric_apps_auto_registration.py`** – Calls the [`create_web_app()`](bfabric_web_apps_functions.md#remote-creation-of-web-applications) function to remotely create a B-Fabric web application.

Unlike the index files, these files are not intended to be modified and are meant to remain untouched. This structure ensures a modular and reusable approach to web application development within B-Fabric.

---


## Choosing the Right Template

This section helps you decide between the **Minimal Template (`index_basic.py`)** and the **Full-Featured Template (`index_large.py`)** based on your use case. If your application utilizes Redis for asynchronous job execution, consider using the **Redis Template (`index_redis.py`)**.

### Core Integration

Both templates **import** and **rely** on teh **`generic` folder**, which provides essential functions such as:
✔ **Authentication Handling** via B-Fabric tokens
✔ **Session Management** and user entity tracking
✔ **Bug Reporting System** for issue tracking
✔ **Dynamic Page Title & Session Details**

These functionalities are **built-in** to both templates, so they work out of the box with B-Fabric.

| Feature                             | **Minimal Template (`index_basic.py`)** | **Full-Featured Template (`index_large.py`)**                     |
| ----------------------------------- | --------------------------------------- | ----------------------------------------------------------- |
| **Integrates `generic` folder**     | ✅ Yes                                   | ✅ Yes                                                       |
| **Logging**                         | ✅ Minimal (only login events)           | ✅ Extensive (logs multiple actions)                         |
| **Dynamic Variable Configuration**  | ❌ No                                    | ✅ Yes (sets default variables like config paths and emails) |
| **Sidebar UI**                      | ❌ No                                    | ✅ Yes (includes dropdowns, sliders, and text input)         |
| **Dynamic Callbacks**               | ❌ No                                    | ✅ Yes (interactive UI with callbacks)                       |
| **Power User Features**             | ❌ No                                    | ✅ Yes (enables power-user access)                           |
| **Use Case**                        | Simpler starting point                  | Full-featured starting point                                |

---


```{Important}
 * **`generic` folder** contains **core system file** and **must not be modified**. Any changes to this folder may break authentication or system integration.
 * **All customization** (for example, adding UI components, callbacks, or logging) should be done in **`index_large.py`, `index_basic.py`, or `index_redis.py`**.
```

---

## Next Steps

Now that you understand the structure, the next sections will explore:

1. **[Template Deployment Guide](installation_template.md)**
2. **[Full-Featured Template (`index_large.py`)](index_py.md)**
3. **[Minimal Template (`index_basic.py`)](index_basic_py.md)**
4. **[Redis Template (`index_redis.py`)](index_redis.md)**