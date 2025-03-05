import os

# Export objects and classes
from bfabric_web_apps.objects import BfabricInterface, Logger

# Export components
from .utils import components

# Export layouts
from .layouts.layouts import get_static_layout

# Export app initialization utilities
from .utils.app_init import create_app
from .utils.get_logger import get_logger
from .utils.get_power_user_wrapper import get_power_user_wrapper
from .utils.create_app_in_bfabric import create_app_in_bfabric

# Export callbacks
from .utils.callbacks import process_url_and_token, submit_bug_report

from .utils import defaults

from bfabric_web_apps.utils.resource_utilities import create_workunit, create_resource, create_workunits, create_resources
HOST = os.getenv("HOST", defaults.HOST)
PORT = int(os.getenv("PORT", defaults.PORT))  # Convert to int since env variables are strings
DEV = os.getenv("DEV", str(defaults.DEV)).lower() in ["true", "1", "yes"]  # Convert to bool
CONFIG_FILE_PATH = os.getenv("CONFIG_FILE_PATH", defaults.CONFIG_FILE_PATH)

DEVELOPER_EMAIL_ADDRESS = os.getenv("DEVELOPER_EMAIL_ADDRESS", defaults.DEVELOPER_EMAIL_ADDRESS)
BUG_REPORT_EMAIL_ADDRESS = os.getenv("BUG_REPORT_EMAIL_ADDRESS", defaults.BUG_REPORT_EMAIL_ADDRESS)


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
    'DEVELOPER_EMAIL_ADDRESS',
    'BUG_REPORT_EMAIL_ADDRESS',
    'create_app_in_bfabric',
    'create_workunit',
    'create_resource',
    'create_workunits',
    'create_resources',
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
