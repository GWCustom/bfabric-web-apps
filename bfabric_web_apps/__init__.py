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
from .utils.callbacks import (
    process_url_and_token, 
    submit_bug_report,
    populate_workunit_details
)

from .utils.config import settings as config

from bfabric_web_apps.utils.resource_utilities import (
    create_workunit, 
    create_resource, 
    create_workunits, 
    create_resources
)

REDIS_HOST = config.REDIS_HOST
REDIS_PORT = config.REDIS_PORT

HOST = config.HOST
PORT = config.PORT
DEV = config.DEV
CONFIG_FILE_PATH = config.CONFIG_FILE_PATH

DEVELOPER_EMAIL_ADDRESS = config.DEVELOPER_EMAIL_ADDRESS
BUG_REPORT_EMAIL_ADDRESS = config.BUG_REPORT_EMAIL_ADDRESS

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
    'populate_workunit_details',
]
