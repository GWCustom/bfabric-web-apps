from dash import html, dcc
import dash_bootstrap_components as dbc

from dash import html, dcc
import dash_bootstrap_components as dbc

def get_base_layout(app, content):
    """
    A base layout with a customizable content area.
    """

    app.config.suppress_callback_exceptions = True

    return html.Div(
        children=[
            dcc.Location(id="url", refresh=False),
            dbc.Container(
                children=[
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                className="banner",
                                children=[
                                    html.Div(
                                        children=[
                                            html.P(
                                                'B-Fabric App Template',
                                                style={'color': '#ffffff', 'margin-top': '15px', 'height': '80px',
                                                       'width': '100%', "font-size": "40px", "margin-left": "20px"}
                                            )
                                        ],
                                        style={"background-color": "#000000", "border-radius": "10px"}
                                    ),
                                ],
                            ),
                        ),
                    ),
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                id="page-title",
                                children=["Bfabric App Template"],
                                style={"font-size": "40px", "margin-left": "20px", "margin-top": "10px"}
                            ),
                            style={"margin-top": "0px", "min-height": "80px", "height": "6vh",
                                   "border-bottom": "2px solid #d4d7d9"}
                        )
                    ),
                    dbc.Row(
                        id="page-content-main",
                        children=[
                            dbc.Col(
                                html.Div(
                                    id="page-content",
                                    children=content,  # Accept custom content here
                                    style={"margin-top": "20vh", "margin-left": "2vw", "font-size": "20px"}
                                ),
                                width=12
                            ),
                        ],
                        style={"margin-top": "0px", "min-height": "40vh"}
                    ),
                ], style={"width": "100vw"},
                fluid=True
            ),
            dcc.Store(id="token", storage_type="session"),
            dcc.Store(id="entity", storage_type="session"),
            dcc.Store(id="token_data", storage_type="session"),
        ], style={"width": "100vw", "overflow-x": "hidden", "overflow-y": "scroll"}
    )


def get_layout_with_sidebar(app, sidebar_content, main_content):
    """
    A layout with a sidebar.
    """
    app.config.suppress_callback_exceptions = True

    content = [
        dbc.Row(
            children=[
                dbc.Col(
                    html.Div(
                        id="sidebar",
                        children=sidebar_content,
                        style={"border-right": "2px solid #d4d7d9", "height": "100%", "padding": "20px", "font-size": "20px"}
                    ),
                    width=3,
                ),
                dbc.Col(
                    html.Div(
                        id="main-content",
                        children=main_content,
                        style={"margin-left": "2vw", "font-size": "20px"}
                    ),
                    width=9,
                ),
            ],
            style={"margin-top": "0px", "min-height": "40vh"}
        )
    ]
    return get_base_layout(app, content)


def get_layout_without_sidebar(app, main_content):
    """
    A layout without a sidebar.
    """

    app.config.suppress_callback_exceptions = True

    content = [
        html.Div(
            id="main-content",
            children=main_content,
            style={"margin-left": "2vw", "font-size": "20px"}
        )
    ]
    return get_base_layout(app, content)
