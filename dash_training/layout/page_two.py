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
    "top": 300,
    "left": 0,
    "bottom": 0,
    "width": "27rem",
    "height": "100rem",
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
}


sidebar = html.Div(
    [
        html.H2("Filters"),
        html.Hr(),
        html.P(
            "Please select inputs from options belows:", className="lead"
        ),
        dbc.Nav(
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
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

page_two = dbc.Tab(label='Portfolio Properties',
                   className="fas fa-chart-bar",
                   # style=tab_style,
                   children=[
                       html.Div(children=[
                           dbc.Row(
                               [dbc.Col(sidebar),
                                dbc.Col(children=[dcc.Graph(id='page_two_scatter', figure=scatter)],
                                        width=7,
                                        style={'margin-left': '20px', 'margin-top': '7px', 'margin-right': '15px'})
                                ])
                       ]
                       )
                   ])
