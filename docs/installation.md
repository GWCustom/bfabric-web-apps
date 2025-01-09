# Installation & Deployment

## Dependencies
Before installing **bfabric_web_app**, ensure you have the following dependencies installed on your system. These are the dependencies required to install **bfabric_web_app**; additional packages (such as Dash and Flask) will be installed later with a single command during deployment.

- **Python** (>= 3.8)  
- **pip** (latest version recommended)  

---

## Installation Steps

### 1. Install via pip
You can install **bfabric_web_apps** directly from PyPI:

```sh
pip install bfabric_web_apps
```

### 2. Clone the Template (Optional but Recommended)
To get started quickly, clone the **bfabric_web_app-template**, which provides a ready-to-use project structure:

```sh
git clone https://github.com/GWCustom/bfabric-web-app-template.git
cd bfabric-web-app-template
```

---

## 3. Set Up a Virtual Environment

Choose one of the following options to create and activate a virtual environment:

#### Using `venv`:
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

#### Using `conda`:
```sh
conda create -n bfabric-web-apps pip
conda activate bfabric-web-apps
```

#### Using `mamba`:
```sh
mamba create -n bfabric-web-apps pip
mamba activate bfabric-web-apps
```

---

## 4. Install Dependencies
Once the virtual environment is active, install all required dependencies:

```sh
pip install -r requirements.txt
```

---

## 5. Configure Your Application

Create a file named `PARAMS.py` in the project root directory to define configuration parameters for the app.

**Example `PARAMS.py`**:
```python
# PARAMS.py
HOST = "0.0.0.0"  # Host to run the app (default: localhost)
PORT = 8050       # Port to serve the application
DEV = False       # Enable/disable debug mode
CONFIG_FILE_PATH = "~/.bfabricpy.yml"  # Path to the configuration file for credentials
```

---

## 6. Set Up `.bfabricpy.yml` Configuration File

The `.bfabricpy.yml` file is **essential for power users**. It provides credentials needed for interacting with the **B-Fabric API** and enables key functionalities like authentication, logging, and API access. 

Create a `.bfabricpy.yml` file in your home directory (e.g., `~/.bfabricpy.yml`) and format it as follows:

**Example `.bfabricpy.yml`**:
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

If you encounter any issues, refer to the [bfabricPy documentation](https://fgcz.github.io/bfabricPy/) for further guidance.

---

## 7. Run the Application

Start the development server by running:

```sh
python index.py
```

---

## 8. Check It Out

Visit the following URL to see your application in action:

```sh
http://localhost:8050
```

For additional setup details, refer to the **[bfabric-web-app-template](https://github.com/GWCustom/bfabric-web-app-template)** repository.
