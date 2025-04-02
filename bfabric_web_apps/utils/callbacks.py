from dash import Input, Output, State, html, dcc
from bfabric_web_apps.objects.BfabricInterface import bfabric_interface
import json
import dash_bootstrap_components as dbc
from datetime import datetime as dt
from bfabric_web_apps.utils.get_logger import get_logger
from rq import Queue
from .redis_connection import redis_conn
from rq.registry import StartedJobRegistry, FailedJobRegistry, FinishedJobRegistry


def process_url_and_token(url_params):
    """
    Processes URL parameters to extract the token, validates it, and retrieves the corresponding data.
    Additionally, it constructs a dynamic job link based on the environment and job ID.

    Args:
        url_params (str): The URL parameters containing the token.

    Returns:
        tuple: A tuple containing:
               - token (str): Authentication token.
               - token_data (dict): Token metadata.
               - entity_data (dict): Retrieved entity information.
               - page_title (str): Title for the page header.
               - session_details (list): HTML-formatted session details.
               - job_link (str): Dynamically generated link to the job page.
    """
    base_title = " "

    if not url_params:
        return None, None, None, None, base_title, None, None

    token = "".join(url_params.split('token=')[1:])
    tdata_raw = bfabric_interface.token_to_data(token)

    if tdata_raw:
        if tdata_raw == "EXPIRED":
            return None, None, None, None, base_title, None, None
        else:
            tdata = json.loads(tdata_raw)
    else:
        return None, None, None, None, base_title, None, None

    if tdata:
        entity_data_json = bfabric_interface.entity_data(tdata)
        app_data_json = bfabric_interface.app_data(tdata)
        entity_data = json.loads(entity_data_json)
        app_data = json.loads(app_data_json)
        page_title = (
            f"{tdata.get('entityClass_data', 'Unknown')} - {entity_data.get('name', 'Unknown')} "
            f"({tdata.get('environment', 'Unknown')} System)"
        ) if tdata else "Bfabric App Interface"

        environment = tdata.get("environment", "").strip().lower()  # 'test' or 'prod'
        job_id = tdata.get("jobId", None)  # Extract job ID

        job_link = None
        if job_id:
            if "test" in environment:
                job_link = f"https://fgcz-bfabric-test.uzh.ch/bfabric/job/show.html?id={job_id}&tab=details"
            else:
                job_link = f"https://fgcz-bfabric.uzh.ch/bfabric/job/show.html?id={job_id}&tab=details"

        session_details = [
            html.P([
                html.B("Entity Name: "), entity_data.get('name', 'Unknown'),
                html.Br(),
                html.B("Entity Class: "), tdata.get('entityClass_data', 'Unknown'),
                html.Br(),
                html.B("Environment: "), tdata.get('environment', 'Unknown'),
                html.Br(),
                html.B("Entity ID: "), tdata.get('entity_id_data', 'Unknown'),
                html.Br(),
                html.B("Job ID: "), job_id if job_id else "Unknown",
                html.Br(),
                html.B("User Name: "), tdata.get('user_data', 'Unknown'),
                html.Br(),
                html.B("Session Expires: "), tdata.get('token_expires', 'Unknown'),
                html.Br(),
                html.B("App Name: "), app_data.get("name", "Unknown"),
                html.Br(),
                html.B("App Description: "), app_data.get("description", "No description available"),
                html.Br(),
                html.B("Current Time: "), str(dt.now().strftime("%Y-%m-%d %H:%M:%S"))
            ])
        ]

        return token, tdata, entity_data, app_data, page_title, session_details, job_link
    else:
        return None, None, None, None, base_title, None, None


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


def populate_workunit_details(token_data):

    """
    Function to populate workunit data for the current app instance.

    Args: 
        token_data (dict): Token metadata.

    Returns:
        html.Div: A div containing the populated workunit data.
    """

    environment_urls = {
        "Test": "https://fgcz-bfabric-test.uzh.ch/bfabric/workunit/show.html?id=",
        "Production": "https://fgcz-bfabric.uzh.ch/bfabric/workunit/show.html?id="
    }

    if token_data:

        jobId = token_data.get('jobId', None)
        print("jobId", jobId)
        
        job = bfabric_interface.get_wrapper().read("job", {"id": jobId})[0]
        workunits = job.get("workunit", [])

        if workunits:
            wus = bfabric_interface.get_wrapper().read(
                "workunit", 
                {"id": [wu["id"] for wu in workunits]}
            )
        else:
            return html.Div(
                [
                    html.P("No workunits found for the current job.")
                ]
            )

        wu_cards = []

        for wu in wus: 
            print(wu)
            wu_card = html.A(
                dbc.Card([
                    dbc.CardHeader(html.B(f"Workunit {wu['id']}")),
                    dbc.CardBody([
                        html.P(f"Name: {wu.get('name', 'n/a')}"),
                        html.P(f"Description: {wu.get('description', 'n/a')}"),
                        html.P(f"Num Resources: {len(wu.get('resource', []))}"),
                        html.P(f"Created: {wu.get('created', 'n/a')}"),
                        html.P(f"Status: {wu.get('status', 'n/a')}")
                    ])
                ], style={"width": "400px", "margin":"10px"}),
                href=environment_urls[token_data.get("environment", "Test")] + str(wu["id"]),
                target="_blank",
                style={"text-decoration": "none"}
            )

            wu_cards.append(wu_card)

        return dbc.Container(wu_cards, style={"display": "flex", "flex-wrap": "wrap"})
    else:
        return html.Div()

def get_redis_queue_layout():
    # Get all queues dynamically
    queues = Queue.all(connection=redis_conn)

    queue_cards = []

    print("QUEUES", queues)
    
    for queue in queues:
        queue_name = queue.name

        # Get queue stats
        started_registry = StartedJobRegistry(queue_name, connection=redis_conn)
        failed_registry = FailedJobRegistry(queue_name, connection=redis_conn)
        finished_registry = FinishedJobRegistry(queue_name, connection=redis_conn)

        stats = {
            "Jobs in queue": queue.count,
            "Running": started_registry.count,
            "Failed": failed_registry.count,
            "Completed": finished_registry.count,
        }

        print("STAT", stats)

        stats_row = dbc.Row([
            dbc.Col([
                html.P([html.B("Jobs in queue: "), f"{queue.count}"]),
                html.P([html.B("Running: "), f"{started_registry.count}"]),
            ],width=6),
            dbc.Col([
                html.P([html.B("Failed: "), f"{failed_registry.count}"]),
                html.P([html.B("Completed: "), f"{finished_registry.count}"]),
            ], width=6)
        ])

        # Fetch job details
        job_cards = []
        for job_id in started_registry.get_job_ids():
            job = queue.fetch_job(job_id)
            if job:
                job_cards.append(
                    dbc.Card(
                        dbc.CardBody([
                            html.H6(f"Job ID: {job.id}", className="card-title"),
                            html.P(f"Function: {job.func_name}", className="card-text"),
                            html.P(f"Status: Running", className="text-success"),
                        ]),
                        style={"maxWidth": "36vw", "backgroundColor": "#d4edda"}, className="mb-2"
                    )
                )

        for job_id in failed_registry.get_job_ids():
            job = queue.fetch_job(job_id)
            if job:
                job_cards.append(
                    dbc.Card(
                        dbc.CardBody([
                            html.H6(f"Job ID: {job.id}", className="card-title"),
                            html.P(f"Function: {job.func_name}", className="card-text"),
                            html.P(f"Status: Failed", className="text-danger"),
                        ]),
                        style={"maxWidth": "36vw", "backgroundColor": "#f8d7da"}, className="mb-2"
                    )
                )

        for job_id in finished_registry.get_job_ids():
            job = queue.fetch_job(job_id)
            if job:
                finished_time = job.ended_at.strftime("%Y-%m-%d %H:%M:%S") if job.ended_at else "Unknown"
                job_cards.append(
                    dbc.Card(
                        dbc.CardBody([
                            html.H6(f"Job ID: {job.id}", className="card-title"),
                            html.P(f"Function: {job.func_name}", className="card-text"),
                            html.P(f"Status: Completed", className="text-primary"),
                            html.P(f"Finished at: {finished_time}", className="text-muted"),
                        ]),
                        style={"maxWidth": "36vw", "backgroundColor": "#d1ecf1"}, className="mb-2"
                    )
                )

        # Create queue card
        queue_card = dbc.Col([
            dbc.Card(
                [
                    dbc.CardHeader(html.H5(f"Queue: {queue_name}")),
                    dbc.CardBody([
                        stats_row,  # Fixed: Convert dictionary to list
                        html.Hr(),
                        *job_cards  # Add job sub-cards
                    ], style={"maxHeight": "58vh", "overflow-y": "scroll"})
                ],
                style={"maxWidth": "36vw", "backgroundColor": "#f8f9fa", "max-height":"60vh"}, className="mb-4"
            )
        ])

        queue_cards.append(queue_card)

    container_children = dbc.Row(queue_cards)

    return dbc.Container(container_children, className="mt-4")
