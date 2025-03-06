import sys
sys.path.append("../bfabric-web-apps")

import bfabric_web_apps
import redis
from rq import Queue
import os
import shutil


def run_main_job(filepaths: dict, 
                 bash_commands: list[str], 
                 resource_paths: list[str], 
                 attachment_paths: list[dict], 
                 token: str):
    """
    Main function to handle:
      1) File copy
      2) Execute local bash commands
      3) Create workunits in B-Fabric
      4) Register resources in B-Fabric
      5) Attach additional files (logs/reports/etc.) to entities in B-Fabric

    :param filepaths: {source_path: destination_path}
    :param bash_commands: List of bash commands to execute
    :param resource_paths: Paths to resources (.gz, .txt, etc.) to attach to new workunits
    :param attachment_paths: List of dictionaries describing attachments to be applied
                            to some B-Fabric entity (e.g. logs, final reports, etc.)
    :param token: Authentication token

    
Dev Notes:
    !!! All exceptions get logged (make sure to log the exception message i.e. "except Exception as e: log(e)") !!!
    !!! If an exception doesn't occur, log that some step ran successfully to the job object !!!
    """




    # STEP 0: Parse token, logger, etc.
    token, token_data, entity_data, app_data, page_title, session_details, job_link = bfabric_web_apps.process_url_and_token(token)
    
    L = bfabric_web_apps.get_logger(token_data)
    print("Token Data:", token_data)
    print("Entity Data:", entity_data)
    print("App Data:", app_data)


    # Ensure tdata is not None before proceeding
    if token_data is not None:
        # Get the list of container IDs
        container_ids = get_container_id(token_data)

    # Ensure entity_data is a dictionary before modifying it
    if isinstance(entity_data, dict):
        entity_data["container_ids"] = container_ids  # Add list of container IDs
    

    # Step 1: Copy files to the server
    try:
        summary = copy_files(filepaths, L)
        L.log_operation("Success", f"File copy summary: {summary}", params=None, flush_logs=True)
        print("Summary:", summary)
    except Exception as e:
        # If something unexpected blows up the entire process
        L.log_operation("Error", f"Failed to copy files: {e}", params=None, flush_logs=True)
        print("Error copying files:", e)

    
    # STEP 2: Execute bash commands
    try:
        bash_log = execute_and_log_bash_commands(bash_commands, L)
        L.log_operation("Success", f"Bash commands executed successfully:\n{bash_log}", 
                        params=None, flush_logs=True)
    except Exception as e:
        L.log_operation("Error", f"Failed to execute bash commands: {e}", 
                        params=None, flush_logs=True)
        print("Error executing bash commands:", e)


    # STEP 3: Create Workunits
    try:
        workunit_ids = create_workunits_step(token_data, app_data, entity_data, L)
    except Exception as e:
        L.log_operation("Error", f"Failed to create workunits in B-Fabric: {e}", 
                        params=None, flush_logs=True)
        print("Error creating workunits:", e)
        workunit_ids = []

    # STEP 4: Register Resources (Refactored)
    try:
        attach_resources_to_workunits(token_data, L, workunit_ids, resource_paths)
    except Exception as e:
        L.log_operation("Error", f"Failed to register resources: {e}", params=None, flush_logs=True)
        print("Error registering resources:", e)

    # STEP 5: Attach extra files (logs, reports, etc.) to B-Fabric entity
    try:
        #attach_files_to_entities(token_data, L, attachment_paths)
        print("Attachment Paths:", attachment_paths)
    except Exception as e:
        L.log_operation("Error", f"Failed to attach extra files: {e}", params=None, flush_logs=True)
        print("Error attaching extra files:", e)



#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Step 1: Copy Files
# -----------------------------------------------------------------------------

def copy_files(filepaths: dict, logger):
    """
    Copies files for each source -> destination mapping in 'filepaths'.
    Logs/prints each file's result *after* the entire loop completes.

    :param filepaths: Dictionary where keys are source paths and values are destination paths
    :param logger: Logging instance
    :return: Summary indicating how many files succeeded vs. failed
    """
    # Store results in a dict: (source, destination) -> True (if success) or error message (if failure)
    results = {}

    # First pass: attempt all copies
    for source, destination in filepaths.items():
        try:
            shutil.copy(source, destination)
            results[(source, destination)] = True
        except Exception as e:
            results[(source, destination)] = str(e)

    # Second pass: log/print successes and errors
    success_count = 0
    for (source, destination), result in results.items():
        if result is True:
            success_msg = f"Copied file: {source} -> {destination}"
            logger.log_operation("Info", success_msg, params=None, flush_logs=False)
            print(success_msg)
            success_count += 1
        else:
            error_msg = f"Error copying file: {source} -> {destination}, Error: {result}"
            logger.log_operation("Error", error_msg, params=None, flush_logs=False)
            print(error_msg)

    # Return a summary message
    total_files = len(filepaths)
    if success_count == total_files:
        return "All files copied successfully."
    else:
        failure_count = total_files - success_count
        return f"{success_count}/{total_files} files copied successfully, {failure_count} failed."


# -----------------------------------------------------------------------------
# Step 2: Execute Bash Commands
# -----------------------------------------------------------------------------

def execute_and_log_bash_commands(bash_commands: list[str], logger):
    """
    Executes a list of bash commands locally, logs and returns the output.

    :param bash_commands: List of commands to execute
    :param logger: Logging instance
    :return: A single string containing logs for all commands
    """
    logstring = ""
    for cmd in bash_commands:
        # Separator line to help visually parse logs
        logstring += "---------------------------------------------------------\n"
        
        # Run the command, redirect output to a temporary file
        os.system(f"{cmd} > bash_log.txt 2>&1")

        # Read command output from the file
        with open("bash_log.txt", "r") as f:
            output = f.read()

        # Append command + output to logstring
        logstring += f"Command: {cmd}\n\nOutput:\n{output}\n"

        # You can also log each command’s output individually:
        logger.log_operation("Info", f"Executed command: {cmd}\nOutput:\n{output}", 
                             params=None, flush_logs=True)
        print(f"Executed: {cmd}\nOutput:\n{output}")

        try:
            os.remove("bash_log.txt")
        except OSError:
            pass  # If for some reason it doesn't exist or is locked


    return logstring

# -----------------------------------------------------------------------------
# Step 3: Create Workunits in B-Fabric
# -----------------------------------------------------------------------------
def create_workunits_step(token_data, app_data, entity_data, logger):
    """
    Creates one or more workunits in B-Fabric using:
      - 'app_data' for the application ID (and maybe other info)
      - 'entity_data' to extract container IDs
      - 'token_data' for authentication/logging

    :param token_data: dict with token/auth info
    :param app_data: dict with fields like {"id": <app_id>} or other app info
    :param entity_data: dict with fields like {"container_ids": [123, 456, ...]} 
    :param logger: a logger instance
    :return: a list of created workunit IDs
    """
    # Extract the application ID (example: from "app_data['id']")
    app_id = app_data["id"]  # Adjust if your data structure is different

    # Extract container IDs from 'entity_data'
    container_ids = entity_data.get("container_ids", [])
    if not container_ids:
        raise ValueError("No container IDs found in entity_data; cannot create workunits.")

    # We will create a new workunit for each container ID
    workunit_ids = []
    for container_id in container_ids:
        # Create your workunit(s). The library method might return a list of IDs or a single ID;
        # adjust accordingly. Example: we pass a *list* for container_ids if the library expects that.
        created_ids = bfabric_web_apps.create_workunits(
            token_data=token_data,
            application_name="Test Workunit",
            application_description=f"Workunit for Test Data - Order {container_id}",
            application_id=app_id,
            container_ids=[container_id]
        )

        # 'created_ids' might be a list or a single integer; 
        # in many code examples, create_workunits returns a list. 
        if created_ids:
            logger.log_operation("Info", f"Created Workunit(s): {created_ids} for Order {container_id}")
            print(f"Created Workunit(s): {created_ids}")
            
            # If create_workunits returned a list, we extend. If it's a single ID, we append.
            if isinstance(created_ids, list):
                workunit_ids.extend(created_ids)
            else:
                workunit_ids.append(created_ids)
        else:
            logger.log_operation("Error", f"Failed to create workunit for container_id={container_id}")
            print(f"Failed to create workunit for container_id={container_id}")

    if not workunit_ids:
        raise ValueError("No workunits were created in B-Fabric.")

    # At this point we have a non-empty list of workunit IDs 
    logger.log_operation("Success", f"Total created Workunits: {workunit_ids}", params=None, flush_logs=True)
    print(f"Total created Workunits: {workunit_ids}")
    return workunit_ids




# -----------------------------------------------------------------------------
# Step 4: Register Resources in B-Fabric
# -----------------------------------------------------------------------------
def attach_resources_to_workunits(token_data, logger, workunit_ids, resource_paths):
    """
    Attaches each file in resource_paths to each workunit ID in workunit_ids.
    Uses bfabric_web_apps.create_resources internally.
    
    :param token_data: B-Fabric token data
    :param logger: logger instance
    :param workunit_ids: List of B-Fabric workunit IDs
    :param resource_paths: List of file paths to attach as resources
    """
    if not workunit_ids:
        logger.log_operation("Info", "No workunits found, skipping resource registration.", 
                             params=None, flush_logs=True)
        print("No workunits found, skipping resource registration.")
        return

    if not resource_paths:
        logger.log_operation("Info", "No resource paths provided, skipping resource registration.", 
                             params=None, flush_logs=True)
        print("No resource paths provided, skipping resource registration.")
        return

    for wuid in workunit_ids:
        # For each file in resource_paths, we attach it to the current workunit ID
        # Your library function can handle multiple files at once, or one-by-one – 
        # that depends on your bfabric_web_apps.create_resources implementation.
        resource_ids = bfabric_web_apps.create_resources(token_data, wuid, resource_paths)
        print("Resource IDs:", resource_ids)
        
        if resource_ids:
            logger.log_operation("Success", f"Resources {resource_ids} attached to Workunit {wuid}",
                                params=None, flush_logs=True)
            print(f"Resources {resource_ids} attached to Workunit {wuid}")
        else:
            logger.log_operation("Error", f"Failed to attach resources for Workunit {wuid}", 
                                 params=None, flush_logs=True)
            print(f"Failed to attach resources for Workunit {wuid}")

# -----------------------------------------------------------------------------
# Step 5: Attachments in B-Fabric
# -----------------------------------------------------------------------------

def attach_files_to_entities(token_data, logger, attachment_paths: list[dict]):
    """
    Attaches files (logs, reports, or other documentation) to a B-Fabric entity.
    Each item in 'attachment_paths' is a dict with keys, for example:
        {
          "file_name": "some_log.log",
          "file_path": "./some_log.log",
          "entity_class": "workunit" or "order" or ...
          "entity_id": 1234
        }

    :param token_data: B-Fabric token data (dict)
    :param logger: logger instance
    :param attachment_paths: List of file attachments to create
    :return: None (logs success/failure for each attachment)
    """

    if not attachment_paths:
        logger.log_operation("Info", "No attachment paths provided, skipping attachment step.",
                             params=None, flush_logs=True)
        print("No attachment paths provided, skipping attachment step.")
        return

    for attachment_info in attachment_paths:
        # Extract fields from the dict. Adjust naming to match your actual keys.
        file_name = attachment_info.get("file_name")
        file_path = attachment_info.get("file_path")
        entity_class = attachment_info.get("entity_class")
        entity_id = attachment_info.get("entity_id")

        # Ensure required info is present
        if not all([file_name, file_path, entity_class, entity_id]):
            msg = f"Missing one or more required fields in attachment_info: {attachment_info}"
            logger.log_operation("Error", msg, params=None, flush_logs=True)
            print("Error:", msg)
            continue  # Skip this entry

        # Attempt to attach the file to the entity
        try:
            # Pseudocode calling your B-Fabric library:
            # result = bfabric_web_apps.attach_file_to_entity(
            #       token_data=token_data,
            #       entity_class=entity_class,
            #       entity_id=entity_id,
            #       attachment_name=file_name,
            #       attachment_path=file_path
            #   )
            #

            # The library function might return True, or an ID, or some info about the attachment.
            if result:
                success_msg = (f"Successfully attached '{file_name}' ({file_path}) "
                               f"to {entity_class} with ID={entity_id}")
                logger.log_operation("Success", success_msg, params=None, flush_logs=True)
                print(success_msg)
            else:
                error_msg = (f"Failed to attach '{file_name}' ({file_path}) "
                             f"to {entity_class} with ID={entity_id}")
                logger.log_operation("Error", error_msg, params=None, flush_logs=True)
                print(error_msg)

        except Exception as e:
            error_msg = (f"Exception while attaching '{file_name}' "
                         f"to {entity_class} {entity_id}: {e}")
            logger.log_operation("Error", error_msg, params=None, flush_logs=True)
            print(error_msg)

# -----------------------------------------------------------------------------
# Additional Helper Functions
# -----------------------------------------------------------------------------

def get_container_id(token_data):

    L = bfabric_web_apps.get_logger(token_data)
    wrapper = bfabric_web_apps.BfabricInterface.bfabric_interface.get_wrapper()

    samples = L.logthis(
        api_call=wrapper.read,
        endpoint="sample",
        obj={"runid": token_data['entity_id_data']},  # Falls jobId eigentlich ein Sample-ID ist
        params=None,
        flush_logs=True
    )

    print("Samples retrieved:", samples)

    # Extract unique order IDs from samples
    container_ids = list(set(sample["container"]["id"] for sample in samples if "container" in sample))

    print("Unique Order IDs:", container_ids)

    # Create a workunit for each order ID
    return(container_ids) 