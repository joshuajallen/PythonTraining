from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from layout.global_variables import data

scatter = px.scatter(data, x=data['Gold'], y=data['Silver'])

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

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "50px",
    "left": 0,
    "bottom": 0,
    "width": "28rem",
    "padding": "2rem 1rem",
}

sidebar_card = html.Div(
    [
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Card([
            html.Br(),
            html.H2("Filters"),
            html.Hr(),
            html.P(
                "A simple sidebar layout with filters", className="lead"
            ),
            dbc.FormGroup(
                [
                    dcc.Dropdown(
                        id="metal_one",
                        className="dropdown",
                        options=[{"label": metal, "value": metal} for metal in data.columns[1:]],
                        clearable=False,
                        value=data.columns[1]
                    ),
                    html.Br(),
                    dcc.Dropdown(
                        id="metal_two",
                        className="dropdown",
                        options=[{"label": metal, "value": metal} for metal in data.columns[1:]],
                        clearable=False,
                        value=data.columns[2]
                    ),
                    html.Br(),
                    dcc.Dropdown(id='hold')
                ])
        ],
            body=True
        )
    ]
)
sidebar = html.Div(
    sidebar_card,
    style=SIDEBAR_STYLE,
)

page_two = dbc.Tab(label="Portfolio Properties 📊",
                   className="fas fa-globe",
                   # style=tab_style,
                   children=[
                       dbc.Container(
                           [
                               html.Div(
                                   children=[
                                       dbc.Row(
                                           [
                                               dbc.Col(
                                                   [sidebar],
                                                   md=3,
                                               ),
                                               dbc.Col(children=[dcc.Graph(id='page_two_scatter', figure=scatter)],
                                                       md=9,
                                                       ),
                                           ],
                                       ),
                                   ],
                                   className="m-4",
                               ),
                           ],
                           fluid=True,
                       )
                   ])
