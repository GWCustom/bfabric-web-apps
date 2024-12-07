from dash import html, dcc
import dash_bootstrap_components as dbc

def get_static_layout(base_title, main_content = None):
    """
    Returns a layout with static tabs for Main, Documentation, and Report a Bug.
    The main content is customizable, while the other tabs are generic.
    """
    return html.Div(
        children=[
            dcc.Location(id='url', refresh=False),
            dcc.Store(id='token', storage_type='session'),
            dcc.Store(id='entity', storage_type='session'),
            dcc.Store(id='token_data', storage_type='session'),
            dbc.Container(
                children=[
                    # Banner
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                className="banner",
                                children=[
                                    html.Div(
                                        children=[
                                            html.P(
                                                base_title,
                                                style={
                                                    'color': '#ffffff',
                                                    'margin-top': '15px',
                                                    'height': '80px',
                                                    'width': '100%',
                                                    'font-size': '40px',
                                                    'margin-left': '20px'
                                                }
                                            )
                                        ],
                                        style={"background-color": "#000000", "border-radius": "10px"}
                                    )
                                ],
                            ),
                        ),
                    ),
                    # Page Title
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                children=[
                                    html.P(
                                        id="page-title",
                                        children=[str(base_title)],
                                        style={"font-size": "40px", "margin-left": "20px", "margin-top": "10px"}
                                    )
                                ],
                                style={
                                    "margin-top": "0px",
                                    "min-height": "80px",
                                    "height": "6vh",
                                    "border-bottom": "2px solid #d4d7d9"
                                }
                            )
                        )
                    ),
                    # Tabs
                    dbc.Tabs(
                        [
                            dbc.Tab(main_content, label="Main", tab_id="main"),
                            dbc.Tab(get_documentation_tab(), label="Documentation", tab_id="documentation"),
                            dbc.Tab(get_report_bug_tab(), label="Report a Bug", tab_id="report-bug"),
                        ],
                        id="tabs",
                        active_tab="main",
                    ),
                ],
                fluid=True,
                style={"width": "100vw"}
            )
        ],
        style={"width": "100vw", "overflow-x": "hidden", "overflow-y": "scroll"}
    )


def get_documentation_tab():
    """
    Returns the content for the Documentation tab.
    """
    return html.Div(
        children=[
            html.H3("Documentation"),
            html.P("Here you can find detailed information about using this app."),
            html.Ul([
                html.Li("Step 1: Login using your Bfabric credentials."),
                html.Li("Step 2: Navigate through the features using the sidebar."),
                html.Li("Step 3: Access specific functionalities within the Main tab."),
            ])
        ],
        style={"margin": "20px"},
    )


def get_report_bug_tab():
    """
    Returns the content for the Report a Bug tab.
    """
    return html.Div(
        children=[
            html.H3("Report a Bug"),
            dcc.Textarea(
                id="bug-description",
                placeholder="Describe the bug here...",
                style={"width": "100%", "height": "150px"}
            ),
            dbc.Button(
                "Submit Bug Report",
                id="submit-bug-report",
                color="primary",
                style={"margin-top": "10px"}
            ),
            dbc.Alert(
                "Bug report submitted successfully!",
                id="alert-fade-bug",
                is_open=False,
                duration=4000,
                color="success",
            ),
            dbc.Alert(
                "Failed to submit the bug report.",
                id="alert-fade-bug-fail",
                is_open=False,
                duration=4000,
                color="danger",
            ),
        ],
        style={"margin": "20px"},
    )
