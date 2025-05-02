import os

# Export objects and classes
from bfabric_web_apps.objects import BfabricInterface, Logger
from bfabric_web_apps.objects.BfabricInterface import bfabric_interface

# Export components
from .utils import components

# Export layouts
from .layouts.layouts import get_static_layout

# Export app initialization utilities
from .utils.app_init import create_app
from .utils.get_logger import get_logger
from .utils.get_power_user_wrapper import get_power_user_wrapper
from .utils.create_app_in_bfabric import create_app_in_bfabric
from .utils.dataset_utils import (
    dataset_to_dictionary, 
    dictionary_to_dataset
)

# Export callbacks
from .utils.callbacks import (
    process_url_and_token, 
    submit_bug_report,
    populate_workunit_details,
    get_redis_queue_layout
)

from .utils.config import settings as config

from. utils.run_main_pipeline import run_main_job, read_file_as_bytes

from .utils.resource_utilities import (
    create_workunit, 
    create_resource, 
    create_workunits, 
    create_resources
)

from .utils.charging import create_charge
from .utils.redis_worker_init import run_worker, test_job
from .utils.redis_queue import q

REDIS_HOST = config.REDIS_HOST
REDIS_PORT = config.REDIS_PORT

HOST = config.HOST
PORT = config.PORT
DEV = config.DEV
DEBUG = config.DEBUG

CONFIG_FILE_PATH = config.CONFIG_FILE_PATH

DEVELOPER_EMAIL_ADDRESS = config.DEVELOPER_EMAIL_ADDRESS
BUG_REPORT_EMAIL_ADDRESS = config.BUG_REPORT_EMAIL_ADDRESS

GSTORE_REMOTE_PATH = config.GSTORE_REMOTE_PATH
SCRATCH_PATH = config.SCRATCH_PATH
TRX_LOGIN = config.TRX_LOGIN
TRX_SSH_KEY = config.TRX_SSH_KEY
URL = config.URL

SERVICE_ID = config.SERVICE_ID
DATASET_TEMPLATE_ID = config.DATASET_TEMPLATE_ID