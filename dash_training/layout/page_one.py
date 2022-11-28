from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
from layout.global_variables import data

df = pd.melt(data, id_vars='DateTime')
df = df.groupby('variable').agg(
    {
        "value": [np.std]
    }
)
df = df.droplevel(0, axis=1).reset_index(level=0)
cols = ["min", "max", "median", "skew"]


fig = px.line(data,
              x="DateTime",
              y=["Gold"],
              title="Line chart of selected asset prices")

dist = px.scatter_matrix(data,
                         dimensions=data.columns[1:],
                         title="Scatter matrix:")

tab_style = {
    "background": "white",
    'color': 'white',
    'border': 'white',
    'font-size': '11px',
    'font-weight': 600,
    'align-items': 'center',
    'justify-content': 'right',
    'border-radius': '4px',
    'padding':'6px'
}

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "50px",
    "left": 0,
    "bottom": 0,
    "width": "28rem",
    "padding": "2rem 1rem",
}


CONTENT_STYLE = {
    "margin-left": "27rem",
    "margin-right": "2rem",
    "padding": "1rem 1rem",
}



chart_page_one = html.Div(
    children=[
        dbc.Row(
            #width=9,
            children=[
                html.Div(
                    id="graph-container",
                    children=dcc.Graph(
                        id="price-chart",
                        figure=fig,
                        config={"displayModeBar": False},
                        style={'display': 'inline-block'}
                    ),
                )
            ]),
        dbc.Row(#width=9,
                children=[
                    html.Div(
                        id="scatter-container",
                        children=dcc.Graph(
                            id="scatter-chart",
                            figure=dist,
                            style={'display': 'inline-block'}
                        ),
                    )
                ])
    ])

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
                    dbc.Label("Select metal", size="md"),
                    dcc.Dropdown(
                        id="metal-filter",
                        className="dropdown",
                        options=[{"label": metal, "value": metal} for metal in data.columns[1:]],
                        clearable=False,
                        value=data.columns[1]
                    ),
                    html.Br(),
                    dbc.Label("Select date range:", size="md"),
                    dcc.DatePickerRange(
                        id="date_range",
                        min_date_allowed=data.DateTime.min().date(),
                        max_date_allowed=data.DateTime.max().date(),
                        start_date=data.DateTime.min().date(),
                        end_date=data.DateTime.max().date()
                    ),
                    html.Br(),
                    dcc.Dropdown(id='three')
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


page_one = dbc.Tab(id = "Tab1",
                   tab_id="Tab1",
                   label="Portfolio Properties 📊",
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
                                                   md=4,
                                               ),
                                               dbc.Col([chart_page_one],
                                                       md=8,
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

