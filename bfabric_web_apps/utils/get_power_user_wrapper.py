import os
from bfabric import Bfabric

def get_power_user_wrapper(token_data, config_file_path: str = "~/.bfabricpy.yml"):
    """
    Initializes and returns a Bfabric power user instance configured for a specific environment.

    This function retrieves the environment information from the provided `token_data` 
    and uses it to initialize a Bfabric instance. The configuration file path is 
    determined by the `CONFIG_FILE_PATH` from the application's configuration.

    Args:
        token_data (dict): A dictionary containing token information. 
            The key "environment" is used to determine the environment 
            (default is "None" if not specified).

    Returns:
        Bfabric: A Bfabric instance initialized with the configuration 
        corresponding to the specified environment.
    """
    environment = token_data.get("environment", "None")

    return  Bfabric.from_config(
            config_path = os.path.expanduser(config_file_path),
            config_env = environment.upper()
    )