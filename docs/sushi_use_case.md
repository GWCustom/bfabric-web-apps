# Sushi Use Case

This use case explains how Sushi applications—like STAR, FastQC, and EdgeR—are architected using the `bfabric_web_apps` framework. These applications serve as interactive, modular tools to run bioinformatics pipelines through a Dash-based frontend and the Sushi backend system.

---

## 1. Overview

Sushi apps are proof-of-concept tools for launching and managing pipeline jobs on the FGCZ compute infrastructure using a user-friendly web interface. Built with `bfabric_web_apps`, each app dynamically loads its UI and logic based on user authentication and app context.

They rely on a consistent pattern:

* Collect user input (resources, parameters) through a Dash UI.
* Fetch metadata from B-Fabric.
* Generate dataset and parameter `.tsv` files.
* Construct and submit a Sushi job using a backend bash command.
* Return results through Sushi and register them via the B-Fabric API.

All apps share the same top-level layout (`index.py`) and are dynamically loaded based on app ID and token data.

---

## 2. App Structure

Each Sushi app (e.g., `STAR.py`, `FastqcApp.py`, `EdgeR.py`) is organized in **three main steps**:

### **Step 1: Get Data from the User**

The sidebar allows users to define:

* Generic job parameters: RAM, cores, scratch, partition, etc.
* Application-specific parameters (e.g., STAR-specific trimming options, EdgeR-specific statistical methods).
* Metadata for job naming and comments.
* Boolean charge switch and optional alerts.

Sidebar components are built with Dash Bootstrap Components and enriched with tooltips for better usability.

### **Step 2: Fetch Data from B-Fabric**

Each app calls `dataset_to_dictionary()` to transform B-Fabric API responses into a structured dataframe, which populates the DataTable shown in the main layout.

### **Step 3: Submit the Job**

Upon submission:

* The dataset and parameters are saved to `SCRATCH_PATH`.
* A bash command is constructed and sent to the Sushi backend using the `run_main_job()` utility.
* Submission status is returned to the user with success/failure alerts.

Each app defines its own parameters for submission, which are passed to Sushi via a command like:

```bash
bundle exec sushi_fabric --class FastqcApp --dataset ... --parameterset ... --run ...
```

---

## 3. Server Architecture

Sushi apps operate on a **three-tier architecture**, identical to the RNA-seq design.

### Architecture Diagram
### Description

* **User**
  Interacts via a Dash web UI to configure job settings and review sample metadata.

* **Web App Server**
  Hosts the Dash app and serves user-facing content. It dynamically loads the correct Sushi UI based on the token and app ID. Enqueues job submissions via Redis.

* **Compute Server**
  Executes `run_main_job()` and launches Sushi jobs based on submitted `.tsv` files. Output is stored locally.

* **B-Fabric System**
  Provides access to project metadata and datasets. Job results (e.g., logs, output files) are linked back to B-Fabric via API as resources or attachments.

* **Redis**
  Acts as the asynchronous communication bridge between the Web App Server and the Compute Server. Jobs are enqueued from the UI and dequeued for execution by the backend.
