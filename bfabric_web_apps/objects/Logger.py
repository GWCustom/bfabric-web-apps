import os
import pickle
from typing import List
from bfabric import Bfabric
from datetime import datetime as dt
import base64
import bfabric_web_apps


class Logger:
    """
    A Logger class to manage and batch API call logs locally and flush them to the backend when needed.
    """
    def __init__(self, jobid: int, username: str, environment: str):
        """
        Initializes the Logger with a job ID, username, and environment.

        Args:
            jobid (int): The ID of the current job.
            username (str): The name of the user performing the operations.
            environment (str): The environment (e.g., Production, Test).
        """
        self.jobid = jobid
        self.username = username
        self.config_file_path = bfabric_web_apps.CONFIG_FILE_PATH
        self.power_user_wrapper = self._get_power_user_wrapper(environment)
        self.logs = []

    def _get_power_user_wrapper(self, environment) -> Bfabric:
        """
        Initializes a B-Fabric wrapper using the power user's credentials.

        Args:
            environment (str): The environment in which to initialize the wrapper.

        Returns:
            Bfabric: An authenticated Bfabric instance.
        """
        power_user_wrapper = Bfabric.from_config(
            config_path = os.path.expanduser(self.config_file_path),
            config_env = environment.upper()
        )
        return power_user_wrapper

    def to_pickle(self):
        """
        Serializes the Logger object and encodes it as a base64 string.

        Returns:
            dict: A dictionary containing the base64-encoded pickle string.
        """
        # Pickle the object and then encode it as a base64 string
        return {"data": base64.b64encode(pickle.dumps(self)).decode('utf-8')}

    @classmethod 
    def from_pickle(cls, pickle_object):
        """
        Deserializes a Logger object from a base64-encoded pickle string.

        Args:
            pickle_object (dict): A dictionary containing the base64-encoded pickle string.

        Returns:
            Logger: The deserialized Logger object.
        """
        # Decode the base64 string back to bytes and then unpickle
        return pickle.loads(base64.b64decode(pickle_object.get("data").encode('utf-8')))

    def log_operation(self, operation: str, message: str, params = None, flush_logs: bool = True):
        """
        Logs an operation locally or flushes it to the backend.

        Args:
            operation (str): The name of the operation being logged.
            message (str): A detailed message about the operation.
            params (dict, optional): Additional parameters to log. Defaults to None.
            flush_logs (bool, optional): Whether to immediately flush the logs to the backend. Defaults to True.
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
        Wraps an API call with logging functionality.

        Args:
            api_call (callable): The API call to be logged and executed.
            *args: Positional arguments to pass to the API call.
            params (dict, optional): Additional parameters to log. Defaults to None.
            flush_logs (bool, optional): Whether to flush logs immediately. Defaults to True.
            **kwargs: Keyword arguments to pass to the API call.

        Returns:
            any: The result of the API call.
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