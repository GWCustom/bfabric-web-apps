import os

# Export objects and classes
from bfabric_web_apps.objects import BfabricInterface, Logger

# Export components
from .utils.components import *

# Export layouts
from .layouts.layouts import get_static_layout

# Export app initialization utilities
from .utils.app_init import create_app
from .utils.get_logger import get_logger
from .utils.get_power_user_wrapper import get_power_user_wrapper

# Export callbacks
from .utils.callbacks import process_url_and_token, submit_bug_report

from .utils import defaults

HOST = '0.0.0.0'
PORT = 8050
DEV = False 
CONFIG_FILE_PATH = os.getenv("CONFIG_FILE_PATH", defaults.CONFIG_FILE_PATH)

# Define __all__ for controlled imports
__all__ = [
    "BfabricInterface",
    "Logger",
    "components",
    "get_static_layout",
    "create_app",
    "process_url_and_token",
    "submit_bug_report",
    'get_logger',
    'get_power_user_wrapper',
    'HOST',
    'PORT', 
    'DEV',
    'CONFIG_FILE_PATH',
]




'''
import os
from .utils import defaults

# Private variable for CONFIG_FILE_PATH
_CONFIG_FILE_PATH = os.getenv("CONFIG_FILE_PATH", defaults.CONFIG_FILE_PATH)

def set_config_file_path(path):
    """
    Setter for the CONFIG_FILE_PATH variable.
    """
    global _CONFIG_FILE_PATH
    if not isinstance(path, str):
        raise ValueError("CONFIG_FILE_PATH must be a string.")
    _CONFIG_FILE_PATH = path

def get_config_file_path():
    """
    Getter for the CONFIG_FILE_PATH variable.
    """
    return _CONFIG_FILE_PATH

# Expose CONFIG_FILE_PATH as a read-only property
class Config:
    @property
    def CONFIG_FILE_PATH(self):
        return get_config_file_path()

config = Config()

'''



'''
from bfabric import config

config.CONFIG_FILE_PATH
'''

'''
from bfabric import set_config_file_path
set_config_file_path("new/path/to/config.json")
'''
