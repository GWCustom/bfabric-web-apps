from dash import Dash
import dash_bootstrap_components as dbc

def create_app():
    """Initialize and return a Dash app instance."""
    return Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}],
    )
