from bfabric_web_apps.utils.get_logger import get_logger
from bfabric_web_apps.objects.BfabricInterface import bfabric_interface
from bfabric_web_apps.utils.get_power_user_wrapper import get_power_user_wrapper
from bfabric_scripts.bfabric_upload_resource import bfabric_upload_resource
from pathlib import Path

def create_workunit(token_data, application_name, application_description, application_id, container_ids):
    """
    Create a new workunit in B-Fabric for each container ID.

    Args:
        token_data (dict): Authentication token data.
        application_name (str): Name of the application.
        application_description (str): Description of the application.
        application_id (int): Application ID.
        container_ids (list): List of container IDs.
    
    Returns:
        list: List of created workunit IDs.
    """
    L = get_logger(token_data)
    wrapper = bfabric_interface.get_wrapper()
    workunit_ids = []

    # Ensure container_ids is a list
    if not isinstance(container_ids, list):
        container_ids = [container_ids]  # Convert to list if single value

    for container_id in container_ids:
        workunit_data = {
            "name": f"{application_name} - Order {container_id}",
            "description": f"{application_description} for Order {container_id}",
            "applicationid": int(application_id),
            "containerid": container_id,  # Assigning order ID dynamically
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
            workunit_ids.append(workunit_id)

        except Exception as e:
            L.log_operation(
                "Error",
                f"Failed to create workunit for Order {container_id}: {e}",
                params=None,
                flush_logs=True,
            )
            print(f"Failed to create workunit for Order {container_id}: {e}")
    
    # First we get the existing workunit_ids for the current job object: 
    pre_existing_workunit_ids = [elt.get("id") for elt in wrapper.read("job", {"id": token_data.get("jobId")})[0].get("workunit", [])]
    
    # Now we associate the job object with the workunits 
    job = L.logthis(
        api_call=L.power_user_wrapper.save,
        endpoint="job",
        obj={"id": token_data.get("jobId"), "workunitid": workunit_ids + pre_existing_workunit_ids},
        params=None,
        flush_logs=True
    )

    return workunit_ids  # Returning a list of all created workunits


def create_resource(token_data, workunit_id, gz_file_path):
    """
    Upload a .gz resource to an existing B-Fabric workunit.
    
    Args:
        token_data (dict): Authentication token data.
        workunit_id (int): ID of the workunit to associate the resource with.
        gz_file_path (str): Full path to the .gz file to upload.
    
    Returns:
        int: Resource ID if successful, None otherwise.
    """

    L = get_logger(token_data)
    wrapper = get_power_user_wrapper(token_data)

    try:
        file_path = Path(gz_file_path)

        # Use the proper upload function
        print("test", wrapper, file_path, workunit_id)
        result = bfabric_upload_resource(wrapper, file_path, workunit_id)

        if result:
            print(f"Resource uploaded: {file_path.name}")
            L.log_operation(
                "upload_resource",
                f"Resource uploaded successfully: {file_path.name}",
                params=None,
                flush_logs=True,
            )
            return result
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



'''



    # Upload a resource to the created workunit
    resource_name = "example_resource.txt"
    resource_content = b"This is an example resource content."

    try:
        resource_response = bfabric.upload_resource(
            resource_name=resource_name,
            content=resource_content,
            workunit_id=workunit_id
        )
        print(f"Resource '{resource_name}' uploaded successfully.")
    except Exception as e:
        print(f"Failed to upload resource: {e}")
        exit(1)

        







import subprocess
from zeep import Client
import os
from bfabric_web_apps.utils.get_logger import get_logger

BFABRIC_WORKUNIT_WSDL = "https://fgcz-bfabric-test.uzh.ch:443/bfabric/workunit?wsdl"
BFABRIC_RESOURCE_WSDL = "https://fgcz-bfabric-test.uzh.ch:443/bfabric/resource?wsdl"

def run_pipeline_and_register_in_bfabric(run_name: str, output_dir: str):
    """
    Startet die Nextflow-Pipeline und speichert die Ergebnisse in B-Fabric.
    
    :param run_name: Name des Sequenzierungslaufs
    :param output_dir: Verzeichnis, in dem die FASTQ-Dateien gespeichert werden
    """
    print(f"[INFO] Starte Nextflow-Pipeline für {run_name}...")
    
    # Nextflow Pipeline starten
    process = subprocess.run([
        "nextflow", "run", "nf-core/bclconvert", 
        "-profile", "docker", 
        "--outdir", output_dir,
        "-resume"
    ], capture_output=True, text=True)
    
    if process.returncode != 0:
        print(f"[ERROR] Nextflow Pipeline fehlgeschlagen: {process.stderr}")
        return False
    
    print(f"[INFO] Pipeline abgeschlossen. Ergebnisse werden registriert...")
    
    # Workunit in B-Fabric anlegen
    workunit_id = create_bfabric_workunit(run_name)
    
    # Falls Workunit erfolgreich erstellt, dann Ressourcen speichern
    if workunit_id:
        register_fastq_files_in_bfabric(output_dir, workunit_id)
    else:
        print("[ERROR] Konnte Workunit nicht in B-Fabric registrieren!")
    
    return True

def create_bfabric_workunit(run_name: str):
    """Erstellt eine Workunit in B-Fabric."""
    try:
        client = Client(BFABRIC_WORKUNIT_WSDL)
        workunit_data = {
            "name": run_name,
            "description": "Illumina BCL zu FASTQ Konvertierung",
            "status": "Completed"
        }
        L = get_logger({})
        response = L.logthis(
            api_call=client.service.createWorkunit,
            obj=workunit_data
        )[0]
        print(f"[INFO] Workunit erstellt mit ID: {response}")
        return response
    except Exception as e:
        print(f"[ERROR] Fehler beim Erstellen der Workunit: {e}")
        return None

def register_fastq_files_in_bfabric(output_dir: str, workunit_id: int):
    """Registriert alle FASTQ-Dateien aus dem Output-Verzeichnis in B-Fabric."""
    try:
        client = Client(BFABRIC_RESOURCE_WSDL)
        L = get_logger({})
        for file_name in os.listdir(output_dir):
            if file_name.endswith(".fastq.gz"):
                file_path = os.path.join(output_dir, file_name)
                resource_data = {
                    "name": file_name,
                    "description": "Erzeugt von nf-core/bclconvert",
                    "path": file_path,
                    "type": "FASTQ",
                    "workunitId": workunit_id
                }
                response = L.logthis(
                    api_call=client.service.createResource,
                    obj=resource_data
                )[0]
                print(f"[INFO] Ressource gespeichert mit ID: {response}")
    except Exception as e:
        print(f"[ERROR] Fehler beim Registrieren der Ressourcen: {e}")
'''