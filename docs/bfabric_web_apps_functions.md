# Core Concepts Overview

This section introduces three foundational building blocks that are essential for understanding and working with B-Fabric Web Apps: global configuration variables, critical runtime components, and core utility functions.

These chapters provide a structured overview of the internal mechanics of a typical B-Fabric Web App, from initialization to authentication and execution.

---

## 1. Global Variables

The first chapter explains how to configure the B-Fabric Web App environment. Global variables can be adapted to suit local infrastructure and use cases. These include paths, email contacts, development mode flags, and service integration parameters like Redis or SSH.

Readers will learn:
- Where and how these variables are stored
- How to override defaults for development or deployment
- How to manage remote service settings like `GSTORE_REMOTE_PATH` or `TRX_LOGIN`

---

## 2. Important Components

The second chapter presents the most essential **session-specific components** extracted from the authentication token, including:
- **`app_data`**: Metadata for the currently running app
- **`entity_data`**: Dataset or sample-level metadata
- **`token_data`**: Session and user authentication metadata
- **`charge switch`**: Tool to create billing assignments in B-Fabric

This section also introduces the token-based authentication process with a visual diagram and shows how to access and use these components within Dash callbacks.

---

## 3. B-Fabric Web Apps Functions

The final chapter documents the **core utility functions** in the `bfabric_web_apps` library. It covers:
- App initialization
- Layout and UI generation
- Token handling and authentication
- Logging user interactions and API calls
- Accessing B-Fabric as a power user
- Sending bug reports and registering apps remotely

This section is especially useful for developers who want to extend or integrate the framework into new Dash apps. Each function is accompanied by usage examples and links to the GitHub source.