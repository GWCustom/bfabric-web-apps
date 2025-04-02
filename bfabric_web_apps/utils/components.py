from dash import html
import dash_daq as daq

DEVELOPER_EMAIL = "gwhite@fgcz.ethz.ch"

expired = [
    html.P("Your session has expired. Please log into bfabric to continue:"),
    html.A('Login to Bfabric', href='https://fgcz-bfabric.uzh.ch/bfabric/')
]

no_entity = [
    html.P("There was an error fetching the data for your entity. Please try accessing the applicaiton again from bfabric:"),
    html.A('Login to Bfabric', href='https://fgcz-bfabric.uzh.ch/bfabric/')
]

dev = [html.P("This page is under development. Please check back later."),html.Br(),html.A("email the developer for more details",href="mailto:"+DEVELOPER_EMAIL)]

auth = [html.Div(id="auth-div")]

no_auth = [
    html.P("You are not currently logged into an active session. Please log into bfabric to continue:"),
    html.A('Login to Bfabric', href='https://fgcz-bfabric.uzh.ch/bfabric/')
]

charge_switch = [
    daq.BooleanSwitch(id='charge_run', on=True, label="Charge project for run"),
    html.Br()
]
