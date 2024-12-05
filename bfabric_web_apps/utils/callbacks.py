from dash import Input, Output, State, html, dcc
from bfabric_web_apps.objects.BfabricInterface import BfabricInterface
from . import components
import json
import dash_bootstrap_components as dbc

def display_page_generic(url_params, base_title):
    """
    Generic callback for processing URL parameters and managing authentication.
    """
    if not url_params:
        return None, None, None, components.no_auth, base_title

    token = "".join(url_params.split('token=')[1:])
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
