from bfabric_web_apps.utils.get_logger import get_logger
from bfabric_web_apps.objects.BfabricInterface import bfabric_interface
from bfabric_web_apps.utils.get_power_user_wrapper import get_power_user_wrapper
from bfabric_scripts.bfabric_upload_resource import bfabric_upload_resource
from pathlib import Path

def create_workunit(token_data, application_name, application_description, application_id, container_id):
    """
    Create a single workunit in B-Fabric.

    Args:
        token_data (dict): Authentication token data.
        application_name (str): Name of the application.
        application_description (str): Description of the application.
        application_id (int): Application ID.
        container_id (int): Container ID (Order ID).
    
    Returns:
        int: Created workunit ID or None if creation fails.
    """
    L = get_logger(token_data)
    wrapper = bfabric_interface.get_wrapper()

    workunit_data = {
        "name": f"{application_name} - Order {container_id}",
        "description": f"{application_description} for Order {container_id}",
        "applicationid": int(application_id),
        "containerid": container_id, 
    }

    try:
        workunit_response = L.logthis(
            api_call=wrapper.save,
            endpoint="workunit",
            obj=workunit_data,
            params=None,
            flush_logs=True
        )
        workunit_id = workunit_response[0].get("id")
        print(f"Created Workunit ID: {workunit_id} for Order ID: {container_id}")

        # First we get the existing workunit_ids for the current job object: 
        pre_existing_workunit_ids = [elt.get("id") for elt in wrapper.read("job", {"id": token_data.get("jobId")})[0].get("workunit", [])]
        
        # Now we associate the job object with the workunits 
        job = L.logthis(
            api_call=L.power_user_wrapper.save,
            endpoint="job",
            obj={"id": token_data.get("jobId"), "workunitid": [workunit_id] + pre_existing_workunit_ids},
            params=None,
            flush_logs=True
        )
        return workunit_id

    except Exception as e:
        L.log_operation(
            "Error",
            f"Failed to create workunit for Order {container_id}: {e}",
            params=None,
            flush_logs=True,
        )
        print(f"Failed to create workunit for Order {container_id}: {e}")
        return None


def create_workunits(token_data, application_name, application_description, application_id, container_ids):
    """
    Create multiple workunits in B-Fabric.

    Args:
        token_data (dict): Authentication token data.
        application_name (str): Name of the application.
        application_description (str): Description of the application.
        application_id (int): Application ID.
        container_ids (list): List of container IDs.
    
    Returns:
        list: List of created workunit IDs.
    """
    if not isinstance(container_ids, list):
        container_ids = [container_ids]  # Ensure it's a list

    workunit_ids = [
        create_workunit(token_data, application_name, application_description, application_id, container_id)
        for container_id in container_ids
    ]

    return [wu_id for wu_id in workunit_ids if wu_id is not None]  # Filter out None values


def create_resource(token_data, workunit_id, file_path):
    """
    Upload a single file as a resource to an existing B-Fabric workunit.

    Args:
        token_data (dict): Authentication token data.
        workunit_id (int): ID of the workunit to associate the resource with.
        file_path (str): Full path to the file to upload.
    
    Returns:
        int: Resource ID if successful, None otherwise.
    """
    L = get_logger(token_data)
    wrapper = get_power_user_wrapper(token_data)

    try:
        file_path = Path(file_path)
        
        # Upload the resource using the new API call
        print(f"Uploading: {file_path.name} to workunit: {workunit_id}")
        
        result = wrapper.save(
            endpoint="resource",
            obj={
                "workunitid": str(workunit_id),
                "name": file_path.name,
                "description": f"Resource uploaded for workunit {workunit_id}",
                "relativepath": file_path.name,
                "storageid": "20", #GWC server
            }
        )

        if result:
            resource_id = result[0]["id"]
            print(f"Resource uploaded: {file_path.name} (ID: {resource_id})")
            L.log_operation(
                "upload_resource",
                f"Resource uploaded successfully: {file_path.name}",
                params=None,
                flush_logs=True,
            )
            return resource_id
        else:
            raise ValueError(f"Failed to upload resource: {file_path.name}")

    except Exception as e:
        L.log_operation(
            "error",
            f"Failed to upload resource: {e}",
            params=None,
            flush_logs=True,
        )
        print(f"Failed to upload resource: {e}")
        return None


def create_resources(token_data, workunit_id, file_paths):
    """
    Upload multiple files as resources to an existing B-Fabric workunit.

    Args:
        token_data (dict): Authentication token data.
        workunit_id (int): ID of the workunit to associate the resources with.
        file_paths (list): List of full paths to files to upload.
    
    Returns:
        list: List of successfully uploaded resource IDs.
    """
    if not isinstance(file_paths, list):
        file_paths = [file_paths]  # Ensure it's a list

    resource_ids = [
        create_resource(token_data, workunit_id, file_path)
        for file_path in file_paths
    ]

    return [res_id for res_id in resource_ids if res_id is not None]  # Filter out None values
