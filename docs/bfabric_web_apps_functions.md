# Library Documentation

The Library Documentation is structured into three main chapters: Global Variables, Important Components, and B-Fabric Web Apps Functions.

---

## 1. Global Variables

The first chapter explains how to configure the B-Fabric Web App environment. Global variables can be adapted to suit local infrastructure and use cases. These include paths, email contacts, development mode flags, and service integration parameters like Redis or SSH.

Readers will learn:

* Where and how these variables are stored
* How to override defaults for development or deployment
* How to manage remote service settings like `GSTORE_REMOTE_PATH` or `TRX_LOGIN`

See the full chapter **[here](global_variables.md)**

---

## 2. Important Components

The second chapter presents the most essential **session-specific components** extracted from the authentication token, including:

* **`app_data`**: Metadata for the currently running app
* **`entity_data`**: Dataset or sample-level metadata
* **`token_data`**: Session and user authentication metadata
* **`charge switch`**: Tool to create billing assignments in B-Fabric

This section also introduces the token-based authentication process with a visual diagram and shows how to access and use these components within Dash callbacks.

See the full chapter **[here](important_components.md)**

---

## 3. B-Fabric Web Apps Functions

The final chapter documents the **core utility functions** in the `bfabric_web_apps` library, including:

* App initialization
* Layout and UI generation
* Token handling and authentication
* Logging user interactions and API calls
* Accessing B-Fabric as a power user
* Sending bug reports and registering apps remotely

This section is especially useful for developers who want to extend or integrate the framework into new Dash apps. Each function is accompanied by usage examples and links to the GitHub source.

See the full chapter **[here](important_functions.md)**
