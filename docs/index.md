# bfabric-web-apps Documentation

Welcome to the official documentation for **Bfabric-Web-Apps** – a Python library designed to streamline the development of satellite web applications for the B-Fabric Laboratory Information Management System (LIMS).

## Overview

**bfabric-web-apps** provides developers with a powerful yet user-friendly interface for building web applications that interact seamlessly with B-Fabric. By abstracting the complexities of API interactions and integrating with modern web technologies like Dash and Flask, this library allows you to focus on delivering custom solutions for scientific data management.

### Key Features:
- **Simplified B-Fabric Integration**: Directly connect to B-Fabric via its API with minimal setup.
- **Custom Dashboards**: Utilize Dash and Plotly to build interactive, dynamic dashboards for data visualization.
- **Data Validation and Management**: Ensure data accuracy before uploading and handle errors efficiently.
- **Modular and Extensible**: Start with a template and extend functionality to suit your use case.

Whether you’re building tools for scientific workflows, dashboards for visualization, or applications for managing data, **bfabric-web-apps** equips you with the tools to deliver high-quality solutions quickly.

---

## What Is Bfabric?

Bfabric is a Laboratory Information Management System (LIMS) developed for managing scientific experiments and their associated data. It offers a robust platform to track samples, analyze results, and organize workflows efficiently for researchers, laboratories, and core facilities.

For more information, visit the [Bfabric official website](https://fgcz-bfabric.uzh.ch/bfabric/).

---

## What Is BfabricPy?

**BfabricPy** is a Python library that serves as a programmatic interface to interact with the B-Fabric API. It enables developers to perform operations such as querying data, uploading results, and managing B-Fabric entities seamlessly from Python-based applications.

BfabricPy is a core dependency of **bfabric-web-apps** and powers API connections for building custom applications.

For more information, visit the [BfabricPy GitHub repository](https://github.com/fgcz/bfabricPy/tree/main).

---

## What Is Dash?

Dash is a Python framework for building interactive web applications with a focus on data visualization and analytics. It combines the power of Plotly for frontend visualizations and Flask for backend support, making it ideal for creating scientific and analytical dashboards.

For more details, refer to the [Dash official documentation](https://dash.plotly.com/).

---

## What Is This Library?

**bfabric-web-apps** is a Python library that simplifies the development of web applications around the B-Fabric system. It provides pre-built tools and functions to:
- Connect to B-Fabric via its API.
- Validate and process scientific data.
- Build custom dashboards using Dash and Plotly.

Developers can quickly get started by using the provided **[bfabric-web-app-template](https://github.com/GWCustom/bfabric-web-app-template)** repository, which demonstrates a complete example of how to set up a web application using the `bfabric-web-apps` library.

---

### Useful Links:
- **bfabric-web-apps**: [bfabric-web-apps](https://github.com/GWCustom/bfabric-web-apps)
- **Template App**: [bfabric-web-app-template](https://github.com/GWCustom/bfabric-web-app-template)
- **BfabricPy**: [BfabricPy GitHub](https://github.com/fgcz/bfabricPy/tree/main)

---

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   _source/modules

