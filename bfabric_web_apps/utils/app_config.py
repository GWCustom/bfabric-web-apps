import os
import importlib.util

def load_config(params_path="./PARAMS.py"):
    """Load configuration for the Dash app."""
    if os.path.exists(params_path):
        try:
            # Dynamically import the PARAMS module
            spec = importlib.util.spec_from_file_location("PARAMS", params_path)
            params_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(params_module)
            
            # Retrieve values with defaults
            PORT = getattr(params_module, "PORT", 8050)
            HOST = getattr(params_module, "HOST", "localhost")
            DEV = getattr(params_module, "DEV", True)
            CONFIG_FILE_PATH = getattr(params_module, "CONFIG_FILE_PATH", "~/.bfabricpy.yml")
        except ImportError:
            # Fallback to default values in case of import errors
            PORT, HOST, DEV = 8050, 'localhost', True
            CONFIG_FILE_PATH = "~/.bfabricpy.yml"
    else:
        # Fallback to default values if PARAMS.py is not found
        PORT, HOST, DEV = 8050, 'localhost', True
        CONFIG_FILE_PATH = "~/.bfabricpy.yml"

    return {"PORT": PORT, "HOST": HOST, "DEV": DEV, "CONFIG_FILE_PATH": CONFIG_FILE_PATH}
