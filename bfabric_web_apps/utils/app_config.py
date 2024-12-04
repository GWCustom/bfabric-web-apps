import os

def load_config():
    """Load configuration for the Dash app."""
    if os.path.exists("./PARAMS.py"):
        try:
            from PARAMS import PORT, HOST, DEV
        except ImportError:
            PORT, HOST, DEV = 8050, 'localhost', True
    else:
        PORT, HOST, DEV = 8050, 'localhost', True
    return {"PORT": PORT, "HOST": HOST, "DEV": DEV}
