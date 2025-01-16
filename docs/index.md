# Bfabric_web_apps Documentation

**bfabric_web_apps** is a Python library that streamlines the creation of **satellite web applications** for the **B-Fabric Laboratory Information Management System (LIMS)**. Built around a **template-based approach**, it provides both a **ready-to-use project structure** and a set of **powerful utilities** for integrating with the B-Fabric API, handling authentication, logging, and more.

---

## Overview

Designed to work seamlessly with [Dash](https://dash.plotly.com/), **bfabric_web_apps** abstracts away complex B-Fabric API calls, allowing you to focus on creating intuitive, data-driven user interfaces for scientific data management. By combining B-Fabric’s robust backend with Dash’s interactive capabilities, you can rapidly build **custom dashboards** and **management tools** without reinventing the wheel.

### Key Features

- **Simplified B-Fabric Integration**  
  - **Token Data Management** – Securely handle **authentication tokens** for API access.  
  - **Entity Data Handling** – Retrieve, modify, and update **B-Fabric entities** dynamically.  
  - **Authentication** – Built-in **token-based authentication** for a seamless user experience.  
  - **Logger** – Integrated logging for **API calls, application events**, and errors.  
  - **Dash Resource Management** – Efficiently handle stored data to reduce unnecessary API calls.

- **Custom Dashboards**  
  Create **interactive and dynamic** dashboards using Dash and Plotly to visualize and manage your data.

- **Layouts**  
  Utilize **predefined Dash layouts** for structured, consistent UI design that’s easy to extend.

---

## What Is This Library?

**bfabric_web_apps** is your **foundation** for building web applications that **interface directly** with B-Fabric. Its core objectives include:

- **Automating repetitive tasks** like token handling and entity lookups.  
- **Simplifying** the creation of dashboards with **Dash** and **Plotly** for data visualization.

To see the **full source code** or to **contribute**, visit the main GitHub repository:  
[**bfabric_web_apps**](https://github.com/GWCustom/bfabric-web-apps)


## Get Started Quickly

Developers can hit the ground running with the **[bfabric_web_app_template](https://github.com/GWCustom/bfabric-web-app-template)**, a **ready-made** project that demonstrates how to configure and deploy a `bfabric_web_apps` application end-to-end. It includes:

- **Preconfigured layout** using Dash and Bootstrap.  
- **Authentication flow** for B-Fabric.  
- **Examples** of logging, API interaction, and entity handling.

By combining the **template** with the **bfabric_web_apps** library, you’ll have a **flexible**, **scalable** starting point for **building custom web apps** that tap into B-Fabric’s powerful capabilities.

> Alternatively, if you want to get started quickly, you can find a simple template example here:  
> **[Basic Usage Example](https://github.com/GWCustom/bfabric-web-apps/blob/main/README.md#Basic-Usage-Example)**
---

## What Is B-Fabric?

B-Fabric is a Laboratory Information Management System (LIMS) developed for managing scientific experiments and their associated data. It offers a robust platform to track samples, analyze results, and organize workflows efficiently for researchers, laboratories, and core facilities.

For more information, visit the [Bfabric official website](https://fgcz-bfabric.uzh.ch/bfabric/).

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

### Useful Links:
- **bfabric_web_apps**: [bfabric-web-apps](https://github.com/GWCustom/bfabric-web-apps)  
- **Template App**: [bfabric-web-app-template](https://github.com/GWCustom/bfabric-web-app-template)  
- **BfabricPy**: [BfabricPy GitHub](https://github.com/fgcz/bfabricPy/tree/main)  
- **Dash Docs**: [Dash Documentation](https://dash.plotly.com/)  
- **Dash Bootstrap Components Docs**: [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/)  
- **BfabricPy Docs Page**: [BfabricPy Documentation](https://fgcz.github.io/bfabricPy/)  
- **B-Fabric Website**: [Bfabric Official Website](https://www.bfabric.org/)  
- **B-Fabric User Manual**: [Bfabric User Manual](https://www.bfabric.org/usermanual)  

