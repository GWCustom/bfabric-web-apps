from dash import Input, Output, State, html, dcc
from bfabric_web_apps.objects.BfabricInterface import BfabricInterface
from . import components
import json
import dash_bootstrap_components as dbc
from bfabric_web_apps.objects.Logger_object import Logger

def display_page_generic(url_params, base_title):
    """
    Processes URL parameters to extract the token, validates it, and retrieves the corresponding data.

    Args:
        url_params (str): The URL parameters containing the token.
        base_title (str): The base title of the page.

    Returns:
        tuple: A tuple containing token data, entity data, and the page content.
               (token, token_data, entity_data, page_content, page_title)
    """
    if not url_params:
        return None, None, None, components.no_auth, base_title

    token = "".join(url_params.split('token=')[1:])
    print("display_page generic", token)
    bfabric_interface = BfabricInterface()
    tdata_raw = bfabric_interface.token_to_data(token)

    if tdata_raw:
        if tdata_raw == "EXPIRED":
            return None, None, None, components.expired, base_title
        else:
            tdata = json.loads(tdata_raw)
    else:
        return None, None, None, components.no_auth, base_title

    if tdata:
        entity_data_json = bfabric_interface.entity_data(tdata)
        entity_data = json.loads(entity_data_json)
        page_title = (
            f"{base_title} - {tdata['entityClass_data']} - {tdata['entity_id_data']} "
            f"({tdata['environment']} System)"
        ) if tdata else "Bfabric App Interface"

        if not entity_data:
            return token, tdata, None, components.no_entity, page_title
        else:
            return token, tdata, entity_data, components.auth, page_title
    else:
        return None, None, None, components.no_auth, base_title


def submit_bug_report(n_clicks, bug_description, token, entity_data):
    """
    Submits a bug report based on user input, token, and entity data.

    Args:
        n_clicks (int): The number of times the submit button has been clicked.
        bug_description (str): The description of the bug provided by the user.
        token (str): The authentication token.
        entity_data (dict): The data related to the current entity.

    Returns:
        tuple: A tuple containing two boolean values indicating success and failure status of the submission.
               (is_open_success, is_open_failure)
    """
    bfabric_interface = BfabricInterface()
    print("submit bug report", token)

    if token: 
        token_data = json.loads(bfabric_interface.token_to_data(token))
    else:
        token_data = ""

    print(token_data)
    jobId = token_data.get('jobId', None)
    username = token_data.get("user_data", "None")
    environment = token_data.get("environment", "None")

    L = Logger(
        jobid=jobId,
        username=username,
        environment= environment)

    if n_clicks:
        L.log_operation("bug report", "Initiating bug report submission process.", params=None, flush_logs=False)
        try:
            sending_result = bfabric_interface.send_bug_report(token_data, entity_data, bug_description)

            if sending_result:
                L.log_operation("bug report", f"Bug report successfully submitted. | DESCRIPTION: {bug_description}", params=None, flush_logs=True)
                return True, False
            else:
                L.log_operation("bug report", "Failed to submit bug report!", params=None, flush_logs=True)
                return False, True
        except:
            L.log_operation("bug report", "Failed to submit bug report!", params=None, flush_logs=True)
            return False, True

    return False, False
