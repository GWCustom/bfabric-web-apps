import os
import pickle
from typing import List
from bfabric import Bfabric
from datetime import datetime as dt
import base64
from ..utils.app_config import load_config

CONFIG_FILE_PATH = load_config()["CONFIG_FILE_PATH"]

class Logger:
    """
    A Logger class to manage and batch API call logs locally and flush them to the backend when needed.
    """
    def __init__(self, jobid: int, username: str, environment: str):
        self.jobid = jobid
        self.username = username
        self.power_user_wrapper = self._get_power_user_wrapper(environment)
        self.logs = []

    def _get_power_user_wrapper(self, environment) -> Bfabric:
        """
        Initializes a B-Fabric wrapper using the power user's credentials.
        """
        power_user_wrapper = Bfabric.from_config(
            config_path = os.path.expanduser(CONFIG_FILE_PATH),
            config_env = environment.upper()
        )
        return power_user_wrapper

    def to_pickle(self):
        # Pickle the object and then encode it as a base64 string
        return {"data": base64.b64encode(pickle.dumps(self)).decode('utf-8')}

    @classmethod 
    def from_pickle(cls, pickle_object):
        # Decode the base64 string back to bytes and then unpickle
        return pickle.loads(base64.b64decode(pickle_object.get("data").encode('utf-8')))

    def log_operation(self, operation: str, message: str, params = None, flush_logs: bool = True):
        """
        Log an operation either locally (if flush_logs=False) or flush to the backend.
        Creates well-structured, readable log entries.
        """
        # Define the timestamp format
        timestamp = dt.now().strftime('%Y-%m-%d %H:%M:%S')

        # Build the base log entry
        log_entry = (
            f"[{timestamp}] "      
            f"USER: {self.username} | "
            f"OPERATION: {operation.upper()} | "
            f"MESSAGE: {message}"
        )

        # Add parameters if provided
        if params is not None:
            log_entry += f" | PARAMETERS: {params}"

        # Flush or store the log entry
        if flush_logs:
            self.logs.append(log_entry)  # Temporarily append for flushing
            self.flush_logs()  # Flush all logs, including the new one
        else:
            self.logs.append(log_entry)  # Append to local logs



    def flush_logs(self):
        """
        Send all accumulated logs for this job to the backend and clear the local cache.
        """
        if not self.logs:
            return  # No logs to flush

        try:
            full_log_message = "\n".join(self.logs)
            self.power_user_wrapper.save("job", {"id": self.jobid, "logthis": full_log_message})
            self.logs = []  # Clear logs after successful flush
        except Exception as e:
            print(f"Failed to save log to B-Fabric: {e}")

    def logthis(self, api_call: callable, *args, params=None , flush_logs: bool = True, **kwargs) -> any:
        """
        Generic logging function to wrap any API call using a Logger instance.
        """
        # Construct a message describing the API call
        call_args = ', '.join([repr(arg) for arg in args])
        call_kwargs = ', '.join([f"{key}={repr(value)}" for key, value in kwargs.items()])
        log_message = f"{api_call.__name__}({call_args}, {call_kwargs})"

        # Execute the actual API call
        result = api_call(*args, **kwargs)

        # Log the operation
        self.log_operation(api_call.__name__, log_message, params, flush_logs=flush_logs)

        return result