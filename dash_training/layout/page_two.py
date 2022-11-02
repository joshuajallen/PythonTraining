from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

tab_style = {
    "background": "white",
    'text-transform': 'uppercase',
    'color': 'white',
    'border': 'white',
    'font-size': '11px',
    'font-weight': 600,
    'align-items': 'center',
    'justify-content': 'right',
    'border-radius': '4px',
    'padding':'6px'
}


page_two = dbc.Tab(label='Portfolio Properties',
                   style=tab_style,
                   children=[
                       dbc.Row(
                           [
                               dbc.Col(),
                               dbc.Col(),
                               dbc.Col([
                                   dbc.Row(),
                                   dbc.Row()
                               ]),
                               dbc.Col(),
                           ]),
                       html.Hr(),
                       dbc.Row(dbc.Col()),
                       dbc.Row(dbc.Col([
                           dbc.Row(),
                           dbc.Row()
                       ]),
                       )
                   ])
