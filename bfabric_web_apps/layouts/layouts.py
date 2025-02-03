from dash import html, dcc
import dash_bootstrap_components as dbc
import bfabric_web_apps

def get_static_layout(base_title=None, main_content=None, documentation_content=None):
    """
    Returns a layout with static tabs for Main, Documentation, and Report a Bug.
    The main content is customizable, while the other tabs are generic.

    Args:
        base_title (str): The main title to be displayed in the banner.
        main_content (html.Div): Content to be displayed in the "Main" tab.
        documentation_content (html.Div): Content for the "Documentation" tab.

    Returns:
        html.Div: The complete static layout of the web app.
    """
    return html.Div(
        children=[
            dcc.Location(id='url', refresh=False),
            dcc.Store(id='token', storage_type='session'),
            dcc.Store(id='entity', storage_type='session'),
            dcc.Store(id='app_data', storage_type='session'),
            dcc.Store(id='token_data', storage_type='session'),
            dcc.Store(id='dynamic-link-store', storage_type='session'),  # Store for dynamic job link

            dbc.Container(
                children=[
                    # Banner Section
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                className="banner",
                                children=[
                                    # Title
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
                                    ),
                                ],
                                style={"position": "relative", "padding": "10px"}
                            ),
                        ),
                    ),

                    # Page Title Section + View Logs Button (Aligned Right)
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                children=[
                                    # Page Title (Aligned Left)
                                    html.P(
                                        id="page-title",
                                        children=[str(" ")],
                                        style={"font-size": "40px", "margin-left": "20px", "margin-top": "10px"}
                                    ),

                                    # View Logs Button (Aligned Right)
                                    html.Div(
                                        children=[
                                            html.A(
                                                dbc.Button(
                                                    "View Logs",
                                                    id="dynamic-link-button",
                                                    color="secondary",  # Greyish color
                                                    style={
                                                        "font-size": "18px",
                                                        "padding": "10px 20px",
                                                        "border-radius": "8px"
                                                    }
                                                ),
                                                id="dynamic-link",
                                                href="#",  # Will be dynamically set in the callback
                                                target="_blank"
                                            )
                                        ],
                                        style={
                                            "position": "absolute",
                                            "right": "20px",
                                            "top": "10px",  # Aligns with title
                                        }
                                    ),
                                ],
                                style={
                                    "position": "relative",  # Ensures absolute positioning works
                                    "margin-top": "0px",
                                    "min-height": "80px",
                                    "height": "6vh",
                                    "border-bottom": "2px solid #d4d7d9",
                                    "display": "flex",
                                    "align-items": "center",
                                    "justify-content": "space-between",  # Title left, button right
                                    "padding-right": "20px"  # Space between button & right edge
                                }
                            ),
                        ),
                    ),

                    # Bug Report Alerts (Restored)
                    dbc.Row(
                        dbc.Col(
                            [
                                dbc.Alert(
                                    "Your bug report has been submitted. Thanks for helping us improve!",
                                    id="alert-fade-bug-success",
                                    dismissable=True,
                                    is_open=False,
                                    color="info",
                                    style={
                                        "max-width": "50vw",
                                        "margin-left": "10px",
                                        "margin-top": "10px",
                                    }
                                ),
                                dbc.Alert(
                                    "Failed to submit bug report! Please email the developers directly at the email below!",
                                    id="alert-fade-bug-fail",
                                    dismissable=True,
                                    is_open=False,
                                    color="danger",
                                    style={
                                        "max-width": "50vw",
                                        "margin-left": "10px",
                                        "margin-top": "10px",
                                    }
                                ),
                            ]           
                        )
                    ),

                    # Tabs Section
                    dbc.Tabs(
                        [
                            dbc.Tab(main_content, label="Main", tab_id="main"),
                            dbc.Tab(get_documentation_tab(documentation_content), label="Documentation", tab_id="documentation"),
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


def get_documentation_tab(documentation_content):
    """
    Returns the content for the Documentation tab with the upgraded layout.
    """
    return dbc.Row(
        id="page-content-docs",
        children=[
            dbc.Col(
                html.Div(
                    id="sidebar_docs",
                    children=[],
                    style={
                        "border-right": "2px solid #d4d7d9",
                        "height": "100%",
                        "padding": "20px",
                        "font-size": "20px",
                    },
                ),
                width=3,
            ),
            dbc.Col(
                html.Div(
                    id="page-content-docs-children",
                    children= documentation_content,
                    style={"margin-top":"2vh", "margin-left":"2vw", "font-size":"20px", "padding-right":"40px", "overflow-y": "scroll", "max-height": "60vh"},
                ),
                width=9,
            ),
        ],
        style={"margin-top": "0px", "min-height": "40vh"},
    )


def get_report_bug_tab():
    """
    Returns the content for the Report a Bug tab with the upgraded layout.
    """
    return dbc.Row(
        id="page-content-bug-report",
        children=[
            dbc.Col(
                html.Div(
                    id="sidebar_bug_report",
                    children=[],  # Optional: Add sidebar content here if needed
                    style={
                        "border-right": "2px solid #d4d7d9",
                        "height": "100%",
                        "padding": "20px",
                        "font-size": "20px",
                    },
                ),
                width=3,
            ),
            dbc.Col(
                html.Div(
                    id="page-content-bug-report-children",
                    children=[
                        html.H2("Report a Bug"),
                        html.P(
                            [
                                "Please use the form below to report a bug. If you have any questions, please email the developer at ",
                                html.A(
                                    bfabric_web_apps.DEVELOPER_EMAIL_ADDRESS,
                                    href=f"mailto:{bfabric_web_apps.DEVELOPER_EMAIL_ADDRESS}",
                                ),
                            ]
                        ),
                        html.Br(),
                        html.H4("Session Details: "),
                        html.Br(),
                        html.P(id="session-details", children="No Active Session"),
                        html.Br(),
                        html.H4("Bug Description"),
                        dbc.Textarea(
                            id="bug-description",
                            placeholder="Please describe the bug you encountered here.",
                            style={"width": "100%"},
                        ),
                        html.Br(),
                        dbc.Button(
                            "Submit Bug Report",
                            id="submit-bug-report",
                            n_clicks=0,
                            style={"margin-bottom": "60px"},
                        ),   
                    ],
                    style={
                        "margin-top": "2vh",
                        "margin-left": "2vw",
                        "font-size": "20px",
                        "padding-right": "40px",
                    },
                ),
                width=9,
            ),
        ],
        style={"margin-top": "0px", "min-height": "40vh"},
    )