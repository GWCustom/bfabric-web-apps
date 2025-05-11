# Introduction

**bfabric_web_apps** is a Python library designed for developing and integrating satellite applications with the **B-Fabric Laboratory Information Management System (LIMS)**.

---

## Overview

Built to work seamlessly with [Dash](https://dash.plotly.com/), **bfabric_web_apps** simplifies the development of web applications that interact with B-Fabric. Using a **template-based approach**, it standardizes common patterns, streamlines development, and provides a modular foundation for extending B-Fabric with satellite applications.

---

## Key Features

### Seamless B-Fabric Integration

* **Token Management**
  Securely handle authentication tokens to enable user sessions and API access.

* **Entity Data Management**
  Dynamically retrieve, update, and manage B-Fabric entities in your application.

* **Application Management**
  Register and manage applications in B-Fabric.

* **Integrated Job Logging**
  Capture job activity, command execution, and application-specific events out of the box.

* **Automatic Charging**
  Bill resource usage to the appropriate project containers through an integrated charge switch.

---

### Generalized Workflow Support

* **Resource Creation**
  Automatically generate and register B-Fabric resources (e.g., text files, reports, output folders).

* **Workunit Creation**
  Easily define and create workunits programmatically during job submission.

* **Report and Link Creation**
  Attach HTML reports or downloadable files directly to B-Fabric entities.

---

### Pipeline Execution Wrapper

* **`run_main_job()` Function**
  Generic wrapper for executing Bash-based workflows, saving files, creating resources, and logging execution steps. Includes support for Redis queue submission and remote processing.

---

### UI Framework & Developer Utilities

* **Prebuilt Dash Components and Layouts**
  Leverage boilerplate UIs, layout helpers, and responsive components to accelerate app development and ensure consistency across apps.

* **Callback Templates**
  Ready-to-use callbacks for modals, alerts, authentication logic, and submission actions.

* **Bug Reporting Integration**
  Automatically send bug reports to a specified email address when a submission fails or throws an exception.

---

## What Is This Library?

**bfabric_web_apps** is your **foundation** for building web applications that **interface directly** with B-Fabric. Its core objectives include:

- **Automating repetitive tasks** like token handling and entity lookups.  
- **Simplifying** the creation of dashboards with **Dash** and **Plotly** for data visualization.

To see the **full source code** or to **contribute**, visit the main GitHub repository:  
[**bfabric_web_apps**](https://github.com/GWCustom/bfabric-web-apps)

---

## Quickstart

Developers can hit the ground running with the **[bfabric_web_app_template](https://github.com/GWCustom/bfabric-web-app-template)**, a **ready-made** project that demonstrates how to configure and deploy a `bfabric_web_apps` application end-to-end. It includes:

- **Preconfigured layout** using Dash and Bootstrap  
- **Authentication flow** for B-Fabric  
- **Examples** of logging, API interaction, and entity handling  

> Alternatively, if you want to get started quickly, you can find a simple template example here:  
> **[Basic Usage Example](https://github.com/GWCustom/bfabric-web-apps/blob/main/README.md#Basic-Usage-Example)**

---

## Learn by Watching

If you prefer learning by video, check out our dedicated **[Video Tutorials](video_tutorials.md)** section.
It includes step-by-step deployment guides, use case walkthroughs, and insights into best practices using `bfabric_web_apps`.

---

## Templates

The [bfabric-web-app-template](https://github.com/GWCustom/bfabric-web-app-template) repository provides a flexible foundation for building Dash applications that integrate with B-Fabric using the `bfabric_web_apps` library. It includes three preconfigured templates suited for different levels of complexity:

* [Minimal Template](index_basic_py.md) – A minimal template for simple apps
* [Full-Featured Template](index_py.md) – A full-featured template for complex applications
* [Redis Template](index_redis.md) – A template specifically designed for using Redis queues

All templates follow a shared structure built around three core components: collecting user input, retrieving metadata from B-Fabric, and triggering workflow execution. This modular design promotes consistency and reusability across applications.

To get started with the templates, please refer to the **[Template Usage section](usage.md)**.

---

## Use Cases

The bfabric_web_apps library has been successfully used to build multiple proof-of-concept applications. The following chapters provide detailed examples of how bfabric_web_apps can be used in practice:

```{note}
**Work in Progress**  
The following use case chapters are currently under construction and not yet complete. Content will be added and refined continuously to better showcase applications built with the bfabric_web_apps library.
```

* **[RNA-seq](rna_seq_use_case.md)** – Demonstrates how to run a large-scale pipeline like RNA-seq via a fully integrated Dash interface using bfabric_web_apps.
* **[Demultiplex](demultiplex_use_case.md)** – A web application designed to run the nf-core pipeline for BCL to FASTQ demultiplexing, providing a streamlined interface for initiating and monitoring demultiplexing jobs.
* **[SUSHI Apps](sushi_use_case.md)** – Showcases an application wrapper for Sushi applications via B-Fabric that enables flexible job configuration and execution through the Sushi backend.

---

## What Is B-Fabric?

B-Fabric is a Laboratory Information Management System (LIMS) developed for managing scientific experiments and their associated data. It offers a robust platform to track samples, analyze results, and organize workflows efficiently for researchers, laboratories, and core facilities.

For more information, visit the [B-Fabric official website](https://fgcz-bfabric.uzh.ch/bfabric/).

---

## What Is BfabricPy?

**BfabricPy** is a Python library that serves as a programmatic interface to interact with the B-Fabric API. It enables developers to perform operations such as querying data, uploading results, and managing B-Fabric entities seamlessly from Python-based applications.

BfabricPy is a core dependency of **bfabric_web_apps** and powers API connections for building custom applications.

For more information, visit the [BfabricPy GitHub repository](https://github.com/fgcz/bfabricPy/tree/main).

---

## What Is Dash?

Dash is a Python framework for building interactive web applications with a focus on data visualization and analytics. It combines the power of Plotly for frontend visualizations and Flask for backend support, making it ideal for creating scientific and analytical dashboards.

For more details, refer to the [Dash official documentation](https://dash.plotly.com/).

---

## Useful Links:
- **bfabric_web_apps**: [bfabric-web-apps](https://github.com/GWCustom/bfabric-web-apps)  
- **Template App**: [bfabric-web-app-template](https://github.com/GWCustom/bfabric-web-app-template)  
- **Redis Docs**: [Redis Template](https://redis.io/docs/latest/)  
- **BfabricPy**: [BfabricPy GitHub](https://github.com/fgcz/bfabricPy/tree/main)  
- **Dash Docs**: [Dash Documentation](https://dash.plotly.com/)  
- **Dash Bootstrap Components**: [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/)  
- **BfabricPy Docs Page**: [BfabricPy Documentation](https://fgcz.github.io/bfabricPy/)  
- **B-Fabric Website**: [B-Fabric Official Website](https://fgcz-bfabric.uzh.ch/bfabric/)  
- **B-Fabric User Manual**: [B-Fabric User Manual](https://www.bfabric.org/usermanual)  