from bfabric_web_apps.objects.Logger import Logger

def get_logger(token_data, config_file_path: str = "~/.bfabricpy.yml"):

    """ Extract logging-related information from token_data, with defaults for missing values """
    jobId = token_data.get('jobId', None)
    username = token_data.get("user_data", "None")
    environment = token_data.get("environment", "None")

    return Logger(
        jobid=jobId,
        username=username,
        environment=environment,
        config_file_path = config_file_path
    )