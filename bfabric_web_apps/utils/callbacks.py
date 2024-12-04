from dash import Input, Output, State, html, dcc
from ..objects import BfabricInterface
from ..objects import components
import json
import dash_bootstrap_components as dbc

def display_page_callback(app, DEV):
    @app.callback(
        [
            Output('token', 'data'),
            Output('token_data', 'data'),
            Output('entity', 'data'),
            Output('page-content', 'children'),
            Output('page-title', 'children'),
            Output('sidebar_text', 'hidden'),
            Output('example-slider', 'disabled'),
            Output('example-dropdown', 'disabled'),
            Output('example-input', 'disabled'),
            Output('example-button', 'disabled'),
        ],
        [Input('url', 'search')]
    )
    def display_page(url_params):
    
        base_title = "Bfabric App Template"

        if not url_params:
            return None, None, None, components.no_auth, base_title, True, True, True, True, True
        
        token = "".join(url_params.split('token=')[1:])
        bfabric_interface = BfabricInterface()
        tdata_raw = bfabric_interface.token_to_data(token)
        
        
        if tdata_raw:
            if tdata_raw == "EXPIRED":
                return None, None, None, components.expired, base_title, True, True, True, True, True

            else: 
                tdata = json.loads(tdata_raw)
        else:
            return None, None, None, components.no_auth, base_title, True, True, True, True, True
        
        if tdata:
            entity_data_json = bfabric_interface.entity_data(tdata)
            entity_data = json.loads(entity_data_json)
            page_title = f"{base_title} - {tdata['entityClass_data']} - {tdata['entity_id_data']} ({tdata['environment']} System)" if tdata else "Bfabric App Interface"

            if not tdata:
                return token, None, None, components.no_auth, page_title, True, True, True, True, True
            
            elif not entity_data:
                return token, None, None, components.no_entity, page_title, True, True, True, True, True
            
            else:
                if not DEV:
                    return token, tdata, entity_data, components.auth, page_title, False, False, False, False, False
                else: 
                    return token, tdata, entity_data, components.dev, page_title, True, True, True, True, True
        else: 
            return None, None, None, components.no_auth, base_title, True, True, True, True, True


def update_auth_div_callback(app):
    @app.callback(
        Output('auth-div', 'children'),
        [
            Input('example-slider', 'value'),
            Input('example-dropdown', 'value'),
            Input('example-input', 'value'),
            Input('example-button', 'n_clicks')
        ],
        [
            State('entity', 'data'),
            State('token_data', 'data'),
        ]
    )
    def callback(slider_val, dropdown_val, input_val, n_clicks, entity_data, token_data):
        if not entity_data or not token_data:
            return None

        entity_details = [
            html.H1("Entity Data:"),
            html.P(f"Entity Class: {token_data['entityClass_data']}"),
            html.P(f"Entity ID: {token_data['entity_id_data']}"),
            html.P(f"Created By: {entity_data['createdby']}"),
            html.P(f"Created: {entity_data['created']}"),
            html.P(f"Modified: {entity_data['modified']}"),
        ]

        output = dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Component Data:"),
                        html.P(f"Slider Value: {slider_val}"),
                        html.P(f"Dropdown Value: {dropdown_val}"),
                        html.P(f"Input Value: {input_val}"),
                        html.P(f"Button Clicks: {n_clicks}")
                    ]
                ),
                dbc.Col(entity_details)
            ]
        )

        return output

