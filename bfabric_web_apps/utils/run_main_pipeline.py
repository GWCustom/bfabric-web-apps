import redis
from rq import Queue
import os
import shutil
import subprocess
from pathlib import Path
import time
from collections import defaultdict

from .get_logger import get_logger
from .get_power_user_wrapper import get_power_user_wrapper
from .callbacks import process_url_and_token
from bfabric_web_apps.objects import BfabricInterface
from .resource_utilities import (
    create_workunit, 
    create_resource, 
    create_workunits, 
    create_resources
)
from .dataset_utils import (
    dataset_to_dictionary,
    dictionary_to_dataset
)

from .charging import create_charge

from .config import settings as config
from datetime import datetime as dt

GSTORE_REMOTE_PATH = config.GSTORE_REMOTE_PATH
SCRATCH_PATH = config.SCRATCH_PATH
TRX_LOGIN = config.TRX_LOGIN
TRX_SSH_KEY = config.TRX_SSH_KEY
URL = config.URL
DATASET_TEMPLATE_ID = config.DATASET_TEMPLATE_ID

def run_main_job(
    files_as_byte_strings: dict, 
    bash_commands: list[str], 
    resource_paths: dict,
    attachment_paths: list[dict], 
    token: str,
    service_id: int = 0,
    charge: list[int] = [],
    dataset_dict: dict = {}
):


    """
    Main function to handle:
      1) Save Files on Server
      2) Execute local bash commands
      3) Create workunits in B-Fabric
      4) Create Dataset in B-Fabric
      5) Register resources in B-Fabric
      6) Attach additional gstore files (logs/reports/etc.) to entities in B-Fabric
      7) Automatically charge the relevant container for the service

    :param files_as_byte_strings: {destination_path: file as byte strings}
    :param bash_commands: List of bash commands to execute
    :param resource_paths: dict, {resource_path: container_id}
    :param attachment_paths: Dictionary mapping source file paths to their corresponding file names ({"path/test.txt": "name.txt"})
                             for attachment to a B-Fabric entity (e.g., logs, final reports, etc.)
    :param token: Authentication token
    :param service_id: ID of the service to charge
    :param charge: A list of container IDs to be charged.
    :param dataset_dict: A dictionary to create a dataset in B-Fabric. keys are container IDs and values are dictionaries whose keys are field names and values are lists of values.


    
    Dev Notes:
    !!! All exceptions get logged (make sure to log the exception message i.e. "except Exception as e: log(e)") !!!
    !!! If an exception doesn't occur, log that some step ran successfully to the job object !!!
    """

    # STEP 0: Parse token, logger, etc.
    token, token_data, entity_data, app_data, page_title, session_details, job_link = process_url_and_token(token)

    if token is None:
        raise ValueError("Error: 'token' is None")
    if token_data is None:
        raise ValueError("Error: 'token_data' is None")
    if entity_data is None:
        raise ValueError("Error: 'entity_data' is None")
    if app_data is None:
        raise ValueError("Error: 'app_data' is None")
    
    
    L = get_logger(token_data)
    print("Token Data:", token_data)
    print("Entity Data:", entity_data)
    print("App Data:", app_data)
     

    # Step 1: Save files to the server
    try:
        summary = save_files_from_bytes(files_as_byte_strings, L)
        L.log_operation("Success | ORIGIN: run_main_job function", f"File copy summary: {summary}", params=None, flush_logs=True)
        print("Summary:", summary)
        
    except Exception as e:
        # If something unexpected blows up the entire process
        L.log_operation("Error | ORIGIN: run_main_job function", f"Failed to copy files: {e}", params=None, flush_logs=True)
        print("Error copying files:", e)

    
    # STEP 2: Execute bash commands
    try:
        bash_log = execute_and_log_bash_commands(bash_commands)
        L.log_operation("Success | ORIGIN: run_main_job function", f"Bash commands executed success | origin: run_main_job functionfully:\n{bash_log}", 
                        params=None, flush_logs=True)
    except Exception as e:
        L.log_operation("Error | ORIGIN: run_main_job function", f"Failed to execute bash commands: {e}", 
                        params=None, flush_logs=True)
        print("Error executing bash commands:", e)


    # STEP 3: Create Workunits
    try:
        workunit_map, workunit_container_map = create_workunits_step(token_data, app_data, resource_paths, L)
    except Exception as e:
        L.log_operation("Error | ORIGIN: run_main_job function", f"Failed to create workunits in B-Fabric: {e}", 
                        params=None, flush_logs=True)
        print("Error creating workunits:", e)
        workunit_map = []


    # STEP 4: Create Dataset
    if dataset_dict:
        for container_id, dataset_data in dataset_dict.items():

            dataset_name = f'Dataset - {str(app_data.get("name", "Unknown App"))} - Container {container_id}'
            linked_workunit_id = workunit_container_map.get(str(container_id), None)

            try:
                dataset = dictionary_to_dataset(dataset_data, dataset_name, container_id, DATASET_TEMPLATE_ID, linked_workunit_id)
                dataset = create_dataset(token_data, dataset)
                L.log_operation("Success | ORIGIN: run_main_job function", f'Dataset {dataset.get("id", "Null")} created successfully for container {container_id}', params=None, flush_logs=True)
                print(f"Dataset created successfully for container {container_id}")
            except Exception as e:
                L.log_operation("Error | ORIGIN: run_main_job function", f"Failed to create dataset for container {container_id}: {e}", params=None, flush_logs=True)
                print(f"Error creating dataset for container {container_id}:", e)
    else:
        L.log_operation("Info | ORIGIN: run_main_job function", "No dataset creation requested.", params=None, flush_logs=True)
        print("No dataset creation requested.")


    # STEP 5: Register Resources (Refactored)
    try:
        attach_resources_to_workunits(token_data, L, workunit_map)
    except Exception as e:
        L.log_operation("Error | ORIGIN: run_main_job function", f"Failed to register resources: {e}", params=None, flush_logs=True)
        print("Error registering resources:", e)

    # STEP 6: Attach gstore files (logs, reports, etc.) to B-Fabric entity as a Link
    try:
        attach_gstore_files_to_entities_as_link(token_data, L, attachment_paths)
        print("Attachment Paths:", attachment_paths)
    except Exception as e:
        L.log_operation("Error | ORIGIN: run_main_job function", f"Failed to attach extra files: {e}", params=None, flush_logs=True)
        print("Error attaching extra files:", e)


    # STEP 7: Charge the container for the service
    if charge: 
        
        if service_id == 0:
            print("Service ID not provided. Skipping charge creation.")
            L.log_operation("Info | ORIGIN: run_main_job function", "Service ID not provided. Skipping charge creation.", params=None, flush_logs=True)
        else:
            container_ids = charge
            print("Container IDs to charge:", container_ids)
            if not container_ids:
                L.log_operation("Error | ORIGIN: run_main_job function", "No container IDs found for charging.", params=None, flush_logs=True)
                print("Error: No container IDs found for charging.")
                return
            for container_id in container_ids:
                charges = create_charge(token_data, container_id, service_id)
                charge_id = charges[0].get("id")
                L.log_operation("Success | ORIGIN: run_main_job function", f"Charge created for container {container_id} with service ID {service_id} and charge id {charge_id}", params=None, flush_logs=False)
                print(f"Charge created with id {charge_id} for container {container_id} with service ID {service_id}")
            L.flush_logs()
    else:
        L.log_operation("Info | ORIGIN: run_main_job function", "Charge creation skipped.", params=None, flush_logs=True)
        print("Charge creation skipped.")
    
    # Final log message
    L.log_operation("Success | ORIGIN: run_main_job function", "All steps completed successfully.", params=None, flush_logs=True)
    print("All steps completed successfully.")

#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Step 1: Save Files from bytes
# -----------------------------------------------------------------------------

def save_files_from_bytes(files_as_byte_strings: dict, logger):
    """
    Saves byte string files to their respective paths.

    :param files_as_byte_strings: Dictionary where keys are destination paths and values are byte strings
    :param logger: Logging instance
    :return: Summary indicating how many files succeeded vs. failed
    """

    message = "All files saved successfully."

    # First pass: attempt to write all files
    for destination, file_bytes in files_as_byte_strings.items():
        try:
            # Write file from byte string
            with open(destination, "+wb") as f:
                f.write(file_bytes)
            logger.log_operation("File saved | ORIGIN: run_main_job function", f"File {destination} saved successfully.", params=None, flush_logs=True)
        
        except Exception as e:
            error_msg = f"Error saving file: {destination}, Error: {str(e)}"
            logger.log_operation("Error | ORIGIN: run_main_job function", error_msg, params=None, flush_logs=True)
            print(error_msg)
            message = f"Error saving some files." 

    return message


# -----------------------------------------------------------------------------
# Step 2: Execute Bash Commands
# -----------------------------------------------------------------------------

def execute_and_log_bash_commands(bash_commands: list[str]):
    """
    Executes a list of bash commands locally, logs and returns the output.

    :param bash_commands: List of commands to execute
    :return: A single string containing logs for all commands
    """
    logstring = ""

    for cmd in bash_commands:
        logstring += "---------------------------------------------------------\n"
        logstring += f"Executing Command\n"

        try:
            # Execute the command and capture both stdout and stderr
            result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
            output = result.stdout.strip()
            error_output = result.stderr.strip()

            # Check if command executed successfully
            if result.returncode == 0:
                status = "SUCCESS"
                log_entry = f"Command: {cmd}\nStatus: {status}\nOutput:\n{output}\n"
            else:
                status = "FAILURE"
                log_entry = f"Command: {cmd}\nStatus: {status}\nError Output:\n{error_output}\n"

            logstring += log_entry
            print(log_entry)

        except Exception as e:
            logstring += f"Command: {cmd}\nStatus: ERROR\nException: {str(e)}\n"
    
    return logstring


# -----------------------------------------------------------------------------
# Step 3: Create Workunits in B-Fabric
# -----------------------------------------------------------------------------

def create_workunits_step(token_data, app_data, resource_paths, logger):
    """
    Creates multiple workunits in B-Fabric based on unique order IDs found in resource_paths.

    :param token_data: dict with token/auth info
    :param app_data: dict with fields like {"id": <app_id>} or other app info
    :param resource_paths: Dictionary {file_path or dir_path: container_id}
    :param logger: a logger instance
    :return: A tuple containing: 
        A dictionary mapping file_paths to workunit objects {file_path: workunit_id}
        A dictionary mapping container_ids to workunit objects {container_id: workunit_id}
    """
    app_id = app_data["id"]  # Extract the application ID

    # Expand any directories into individual files
    expanded_paths = {}

    for path_str, container_id in resource_paths.items():
        path = Path(path_str)
        if path.is_file():
            expanded_paths[str(path)] = int(container_id)
        elif path.is_dir():
            for file in path.rglob("*"): #is a method that returns all files and folders in the directory and its subdirectories
                if file.is_file():
                    expanded_paths[str(file)] = int(container_id)
        else:
            logger.log_operation("Warning | ORIGIN: run_main_job function", f"Path {path_str} does not exist.", flush_logs=True)
            print(f"Warning: Path {path_str} does not exist or is not accessible.")

    if not expanded_paths:
        raise ValueError("No valid file paths found in resource_paths.")

    container_ids = list(set(expanded_paths.values()))

    # Create all workunits in one API call
    created_workunits = create_workunits(
        token_data=token_data,
        application_name="Test Workunit",
        application_description="Workunits for batch processing",
        application_id=app_id,
        container_ids=container_ids
    )

    if not created_workunits or len(created_workunits) != len(container_ids):
        raise ValueError(f"Mismatch in workunit creation: Expected {len(container_ids)} workunits, got {len(created_workunits)}.")

    workunit_map = {
        file_path: wu["id"]
        for wu in created_workunits
        for file_path, container_id in expanded_paths.items()
        if container_id == wu["container"]["id"]
    }

    workunit_container_map = {
        str(wu["container"]["id"]): wu["id"]
        for wu in created_workunits
    }

    workunit_ids = [wu.get("id") for wu in created_workunits]
    logger.log_operation("Success | ORIGIN: run_main_job function", f"Total created Workunits: {workunit_ids}", params=None, flush_logs=True)
    print(f"Total created Workunits: {workunit_ids}")
    print(workunit_map)

    return workunit_map, workunit_container_map  # Returning {file_path: workunit}



# -----------------------------------------------------------------------------
# Step 4: Create Dataset in B-Fabric
# -----------------------------------------------------------------------------
def create_dataset(token_data, dataset_data): 

    """
    Creates a dataset in B-Fabric using the provided dataset data.
    :param dataset_data: Dictionary containing dataset information
    :param token_data: B-Fabric token data
    :return: The created dataset object
    """

    wrapper = get_power_user_wrapper(token_data) 
    dataset = wrapper.save("dataset", dataset_data)  # Save the dataset

    return dataset[0]



# -----------------------------------------------------------------------------
# Step 5: Attach Resources in B-Fabric
# -----------------------------------------------------------------------------

def attach_resources_to_workunits(token_data, logger, workunit_map):
    """
    Attaches each file to its corresponding workunit.

    Uses `create_resource` to upload files one by one.

    :param token_data: B-Fabric token data
    :param logger: Logger instance
    :param workunit_map: Dictionary mapping file_path to workunit_id {file_path: workunit_id}
    """
    if not workunit_map:
        logger.log_operation("Info | ORIGIN: run_main_job function", "No workunits found, skipping resource registration.",
                             params=None, flush_logs=True)
        print("No workunits found, skipping resource registration.")
        return

    print("Workunit Map:", workunit_map)

    # Dictionary to count successfully created resources per workunit
    # defaultdict(int) automatically starts each new key with a value of 0
    workunit_resource_count = defaultdict(int)

    for file_path, workunit_id in workunit_map.items():
        print(f"Processing file: {file_path}, Workunit ID: {workunit_id}")
        # Upload the file as a resource
        resource = create_resource(token_data, workunit_id, file_path)
        resource_id = resource.get("id")
        print("Resource ID:", resource_id)
        if resource_id:
            workunit_resource_count[workunit_id] += 1
            print(f"Resource {resource_id} attached to Workunit {workunit_id}")
        else:
            logger.log_operation("Error | ORIGIN: run_main_job function", f"Failed to attach resource {file_path} for Workunit {workunit_id}",
                                 params=None, flush_logs=True)
            print(f"Failed to attach resource {file_path} for Workunit {workunit_id}")

    # Log a summary per workunit
    for workunit_id, count in workunit_resource_count.items():
        logger.log_operation(
            "Success | ORIGIN: run_main_job function",
            f"Created {count} resource(s) for Workunit ID {workunit_id}",
            params=None,
            flush_logs=True
        )
        print(f"Created {count} resource(s) for Workunit ID {workunit_id}")



# -----------------------------------------------------------------------------
# Step 6: Attachments of gstore in B-Fabric as a Link
# -----------------------------------------------------------------------------

def attach_gstore_files_to_entities_as_link(token_data, logger, attachment_paths: dict):
    

    """
    Attaches files to a B-Fabric entity by copying them to the FGCZ storage and creating an API link.

    Args:
        token_data (dict): Authentication token data.
        logger: Logger instance for logging operations.
        attachment_paths (dict): Dictionary mapping source file paths to their corresponding file names.
    
    Returns:
        None
    """

    # Extract entity details from token data
    entity_class = token_data.get("entityClass_data", None)
    entity_id = token_data.get("entity_id_data", None)

    # Check if we have access to the FGCZ server
    local = local_access(GSTORE_REMOTE_PATH)

    # Process each attachment
    for source_path, file_name in attachment_paths.items():
        if not source_path or not file_name:
            logger.log_operation("Error | ORIGIN: run_main_job function", f"Missing required attachment details: {source_path} -> {file_name}", params=None, flush_logs=True)
            print(f"Error: Missing required attachment details: {source_path} -> {file_name}")
            continue

        try:
            # Define entity folder
            entity_folder = f"{entity_class}_{entity_id}" if entity_class and entity_id else "unknown_entity"
            final_remote_path = f"{GSTORE_REMOTE_PATH}/{entity_folder}/"

            print("local access:", local)
            print("source path:", source_path)
            print("file name:", file_name)
            print("final remote path:", final_remote_path)

            if local:  # We have direct access → Copy directly
                g_req_copy(source_path, final_remote_path)
                
            else:  # We don't have direct access → Send to migration folder first
                remote_tmp_path = f"{SCRATCH_PATH}/{file_name}"
                scp_copy(source_path, TRX_LOGIN, TRX_SSH_KEY, remote_tmp_path)
                print("scp copy done:")

                # Move to final location
                ssh_move(TRX_LOGIN, TRX_SSH_KEY, remote_tmp_path, final_remote_path)
                print("ssh move done:")

            # Log success
            success_msg = f"Successfully attached '{file_name}' to {entity_class} (ID={entity_id})"
            print(success_msg)

            # Step 3: Create API link
            create_attachment_link(token_data, logger, entity_class, entity_id, file_name, entity_folder)

        except Exception as e:
            error_msg = f"Exception while processing '{file_name}': {e}"
            logger.log_operation("Error | ORIGIN: run_main_job function", error_msg, params=None, flush_logs=True)
            print(error_msg)

def local_access(remote_path):
    """Checks if the remote gstore path (i.e. /srv/gstore/projects/) exists locally""" 
    result = os.path.exists(remote_path)
    print("Remote Path Exists:", result)
    return result


def scp_copy(source_path, ssh_user, ssh_key, remote_path):
    """Copies a file to a remote location using SCP with the correct FGCZ server address."""
    print("SCP Copying...")
    cmd = ["scp", "-i", ssh_key, source_path, f"{ssh_user}:{remote_path}"]
    print("SCP Command:")
    subprocess.run(cmd, check=True)
    print("SCP Command Executed:", cmd)
    print(f"Copied {source_path} to {remote_path}")


def ssh_move(ssh_user, ssh_key, remote_tmp_path, final_remote_path):
    """Moves a file on the remote server to its final location using SSH."""
    cmd = ["ssh", "-i", ssh_key, ssh_user, f"/usr/local/ngseq/bin/g-req copynow -f {remote_tmp_path} {final_remote_path}"]

    subprocess.run(cmd, check=True)
    print(f"Moved {remote_tmp_path} to {final_remote_path}")
    
    # Wait 10 second before next move
    time.sleep(10)


def g_req_copy(source_path, destination_path):
    """Copies a file using g-req command when direct access is available."""
    cmd = ["/usr/local/ngseq/bin/g-req", "copynow", "-f", source_path, destination_path]
    subprocess.run(cmd, check=True)
    print(f"Copied {source_path} using g-req")


def create_attachment_link(token_data, logger, entity_class, entity_id, file_name, folder_name):
    """Creates an attachment link in B-Fabric for the attached file."""
    wrapper = get_power_user_wrapper(token_data)
    url = f"{URL}/{folder_name}/{file_name}"
    timestamped_filename = f"{dt.now().strftime('%Y-%m-%d_%H:%M:%S')}_{file_name}"

    data = {
        "name": timestamped_filename,
        "parentclassname": entity_class,
        "parentid": entity_id,
        "url": url
    }

    try:
        link_result = wrapper.save("link", data)
        if link_result:
            success_msg = f"Attachment link created for '{file_name}': {url}"
            logger.log_operation("Success | ORIGIN: run_main_job function", success_msg, params=None, flush_logs=True)
            print(success_msg)
        else:
            raise ValueError("Attachment link creation failed")
    except Exception as e:
        error_msg = f"Failed to create attachment link for '{file_name}': {e}"
        logger.log_operation("Error | ORIGIN: run_main_job function", error_msg, params=None, flush_logs=True)
        print(error_msg)


def read_file_as_bytes(file_path, max_size_mb=400):
    """Reads any file type and stores it as a byte string in a dictionary."""
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)  # Convert bytes to MB
    if file_size_mb > max_size_mb:
        raise ValueError(f"File {file_path} exceeds {max_size_mb}MB limit ({file_size_mb:.2f}MB).")

    with open(file_path, "rb") as f:  # Read as bytes
        file_as_bytes = f.read()

    return file_as_bytes
