from dash import html, dcc
import dash_bootstrap_components as dbc

def get_layout_with_side_panel(base_title):
    """
    Returns the generic layout for the app with a placeholder for page-content.
    """
    return html.Div(
        children=[
            dcc.Location(id='url', refresh=False),
            dcc.Store(id='token', storage_type='session'),
            dcc.Store(id='entity', storage_type='session'),
            dcc.Store(id='token_data', storage_type='session'),
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
                                style={"margin-top": "0px", "min-height": "80px", "height": "6vh", "border-bottom": "2px solid #d4d7d9"}
                            )
                        )
                    ),
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                id="page-content",  # Add placeholder for page-content
                                children=[],       # Empty children as placeholder
                                style={            # Style to make it invisible when empty
                                    "min-height": "40vh",
                                    "margin-top": "20px",
                                    "display": "none"  # Hide by default
                                }
                            )
                        )
                    ),
                ],
                fluid=True,
                style={"width": "100vw"}
            )
        ],
        style={"width": "100vw", "overflow-x": "hidden", "overflow-y": "scroll"}
    )
