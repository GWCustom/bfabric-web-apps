import os
from bfabric import Bfabric
from .app_config import load_config

CONFIG_FILE_PATH = load_config()["CONFIG_FILE_PATH"]

def get_power_user_wrapper(token_data):

    environment = token_data.get("environment", "None")

    return  Bfabric.from_config(
            config_path = os.path.expanduser(CONFIG_FILE_PATH),
            config_env = environment.upper()
    )