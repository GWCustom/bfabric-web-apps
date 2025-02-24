from bfabric_web_apps.utils.get_logger import get_logger
from bfabric_web_apps.objects.BfabricInterface import bfabric_interface
from bfabric_web_apps.utils.get_power_user_wrapper import get_power_user_wrapper

def create_workunit(token_data, application_name, application_description, application_id, container_id=2220):
    """
    Create a new workunit in B-Fabric.
    
    Args:
        token_data (dict): Authentication token data.
        application_name (str): Name of the application.
        application_description (str): Description of the application.
        application_id (int): Application ID.
        container_id (int): Container ID (default: 2220).
    
    Returns:
        int: Workunit ID if successful, None otherwise.
    """
    workunit_data = {
        "name": application_name,
        "description": application_description,
        "applicationid": int(application_id),
        "containerid": container_id,
    }

    L = get_logger(token_data)
    wrapper = bfabric_interface.get_wrapper()

    try:
        workunit_response = L.logthis(
            api_call=wrapper.save,
            endpoint="workunit",
            obj=workunit_data,
            params=None,
            flush_logs=True
        )
        workunit_id = workunit_response[0].get("id")
        print(f"Workunit created with ID: {workunit_id}")
        return workunit_id

    except Exception as e:
        L.log_operation(
            "Error",
            f"Failed to create workunit: {e}",
            params=None,
            flush_logs=True,
        )
        print(f"Failed to create workunit: {e}")
        return None


def create_resource(token_data, workunit_id, resource_name, file_content):
    """
    Upload a resource to an existing B-Fabric workunit.
    
    Args:
        token_data (dict): Authentication token data.
        workunit_id (int): ID of the workunit to associate the resource with.
        resource_name (str): Name of the resource.
        file_content (bytes): Binary content of the file to upload.
    
    Returns:
        int: Resource ID if successful, None otherwise.
    """
    L = get_logger(token_data)
    wrapper = get_power_user_wrapper(token_data)

    try:
        resource_response = wrapper.upload_resource(resource_name, file_content, workunit_id)
        resource_id = resource_response[0].get("id")
        if resource_id:
            print(f"Resource uploaded with ID: {resource_id}")
            L.log_operation(
                "upload_resource",
                f"Resource uploaded successfully with ID: {resource_id}",
                params=None,
                flush_logs=True,
            )
            return resource_id
        else:
            raise ValueError("Resource ID not found in the response.")

    except Exception as e:
        L.log_operation(
            "Error",
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