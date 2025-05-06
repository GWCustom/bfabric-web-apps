# Template Deployment Guide

This chapter provides a step-by-step guide for deploying **bfabric-web-app-template**, templates built with the **bfabric_web_apps** framework that serve as entry points for custom B-Fabric web applications.

---

```{note}
**Version Compatibility Notice**  
To ensure proper functionality, the `bfabric_web_apps` library and the `bfabric_web_app_template` must have the **same version**. For example, if `bfabric_web_apps` is version `0.1.3`, then `bfabric_web_app_template` must also be `0.1.3`.  

Please verify and update the versions accordingly before running the application.
```

---

## Dependencies
Before installing **bfabric_web_apps**, ensure you have the following dependencies installed on your system. These are the dependencies required to install **bfabric_web_apps**; additional packages (such as Dash and Flask) will be installed later with a single command during deployment.

- **Python** (>= 3.8)  
- **pip** (latest version recommended)  

---

## Installation Steps

### 1. Install via pip
You can install **bfabric_web_apps** directly from PyPI:

```sh
pip install bfabric_web_apps
```

---

### 2. Clone the Template (Optional but Recommended)
To get started quickly, clone the **bfabric_web_app-template**, which provides a ready-to-use project structure:

```sh
git clone https://github.com/GWCustom/bfabric-web-app-template.git
cd bfabric-web-app-template
```

---

### 3. Set Up a Virtual Environment

Choose one of the following options to create and activate a virtual environment:

#### Using venv:
**For Linux/Mac:**
```sh
python3 -m venv venv
source venv/bin/activate
```

**For Windows:**
```sh
python -m venv venv
venv\Scripts\activate
```

#### Using conda:
```sh
conda create -n bfabric-web-apps pip
conda activate bfabric-web-apps
```

#### Using mamba:
```sh
mamba create -n bfabric-web-apps pip
mamba activate bfabric-web-apps
```

---

### 4. Install Dependencies
Once the virtual environment is active, install all required dependencies:

```sh
pip install -r requirements.txt
```

---

### 5. Set Up .bfabricpy.yml Configuration File as Described in [bfabricPy](https://fgcz.github.io/bfabricPy/)

The **.bfabricpy.yml** file is **essential for power users**. It provides credentials needed for interacting with the **B-Fabric API** and enables key functionalities like authentication, logging, and API access. 

> **Note:** By default, the application expects the configuration file to be located at `~/.bfabricpy.yml`. However, this default location can be changed. For details on how to modify the configuration path, see the [How to Modify Global Variables](bfabric_web_apps_functions.md#how-to-modify-global-variables) section.


Create a **.bfabricpy.yml** file in your home directory (e.g., **~/.bfabricpy.yml**) and format it as follows:

**Example .bfabricpy.yml**:
```yaml
GENERAL:
  default_config: PRODUCTION

PRODUCTION:
  login: your_username
  password: your_password
  base_url: https://your-bfabric-api-endpoint
```

- **`login`**: The B-Fabric user login.
- **`password`**: The corresponding password for the user.
- **`base_url`**: The base API endpoint for your B-Fabric instance.

Ensure the file is saved in the specified path and accessible by the application.

As mentioned above, if you encounter any issues, please refer to the [bfabricPy documentation](https://fgcz.github.io/bfabricPy/) for further guidance.

---

### 6. Run the Application

Start the development server by running:

```sh
python index.py
```

---

### 7. Test the Application

Visit the following URL to see your application in action:

```sh
http://localhost:8050
```

For additional setup details, visit the **[bfabric-web-app-template](https://github.com/GWCustom/bfabric-web-app-template)** repository.
