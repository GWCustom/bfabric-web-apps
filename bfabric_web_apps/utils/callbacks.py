from dash import Input, Output, State, html, dcc
from bfabric_web_apps.objects.BfabricInterface import BfabricInterface
import json
import dash_bootstrap_components as dbc
from datetime import datetime as dt
from bfabric_web_apps.utils.get_logger import get_logger

def process_url_and_token(url_params):
    """
    Processes URL parameters to extract the token, validates it, and retrieves the corresponding data.

    Args:
        url_params (str): The URL parameters containing the token.
        base_title (str): The base title of the page.

    Returns:
        tuple: A tuple containing token data, entity data, and the page content.
               (token, token_data, entity_data, page_content, page_title)
    """
    base_title = " "

    if not url_params:
        return None, None, None, base_title, None

    token = "".join(url_params.split('token=')[1:])
    bfabric_interface = BfabricInterface()
    tdata_raw = bfabric_interface.token_to_data(token)

    if tdata_raw:
        if tdata_raw == "EXPIRED":
            return None, None, None, base_title, None
        else:
            tdata = json.loads(tdata_raw)
    else:
        return None, None, None, base_title, None

    if tdata:
        entity_data_json = bfabric_interface.entity_data(tdata)
        entity_data = json.loads(entity_data_json)
        page_title = (
            f"{tdata['entityClass_data']} - {entity_data['name']} "
            f"({tdata['environment']} System)"
        ) if tdata else "Bfabric App Interface"

        if not entity_data:
            return token, tdata, None, page_title, None
        else:
            session_details = [
            html.P([
                html.B("Entity Name: "), entity_data['name'],
                html.Br(),
                html.B("Entity Class: "), tdata['entityClass_data'],
                html.Br(),
                html.B("Environment: "), tdata['environment'],
                html.Br(),
                html.B("Entity ID: "), tdata['entity_id_data'],
                html.Br(),
                html.B("User Name: "), tdata['user_data'],
                html.Br(),
                html.B("Session Expires: "), tdata['token_expires'],
                html.Br(),
                html.B("Current Time: "), str(dt.now().strftime("%Y-%m-%d %H:%M:%S"))
            ])
        ]
            return token, tdata, entity_data, page_title, session_details
    else:
        return None, None, None, base_title, None


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

    # Parse token data if token is provided, otherwise set it to an empty dictionary
    if token:
        token_data = json.loads(bfabric_interface.token_to_data(token))
    else:
        token_data = {}

    print(token_data)

    # Extract logging-related information from token_data, with defaults for missing values
    jobId = token_data.get('jobId', None)
    username = token_data.get("user_data", "None")
    environment = token_data.get("environment", "None")

    # Initialize the logger only if token_data is available
    L = None
    if token_data:
        L = get_logger(token_data)

    if n_clicks:
        # Log the operation only if the logger is initialized
        if L:
            L.log_operation(
                "bug report",
                "Initiating bug report submission process.",
                params=None,
                flush_logs=False,
            )
        try:
            sending_result = bfabric_interface.send_bug_report(
                token_data, entity_data, bug_description
            )

            if sending_result:
                if L:
                    L.log_operation(
                        "bug report",
                        f"Bug report successfully submitted. | DESCRIPTION: {bug_description}",
                        params=None,
                        flush_logs=True,
                    )
                return True, False
            else:
                if L:
                    L.log_operation(
                        "bug report",
                        "Failed to submit bug report!",
                        params=None,
                        flush_logs=True,
                    )
                return False, True
        except Exception as e:
            if L:
                L.log_operation(
                    "bug report",
                    f"Failed to submit bug report! Error: {str(e)}",
                    params=None,
                    flush_logs=True,
                )
            return False, True

    return False, False

