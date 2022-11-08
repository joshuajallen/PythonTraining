from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import os
import plotly.express as px
from layout.global_variables import data

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
    #"position": "fixed",
    "top": 300,
    "left": 0,
    "bottom": 0,
    "width": "27rem",
    "height": "100rem",
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "27rem",
    "margin-right": "2rem",
    "padding": "1rem 1rem",
}
# content_one_one = html.Div([
#     dbc.Label("Select metal", size="md"),
#     dcc.Dropdown(
#         id="metal-filter",
#         className="dropdown",
#         options=[{"label": metal, "value": metal} for metal in data.columns[1:]],
#         clearable=False,
#         value=data.columns[1]
#     )
# ], style={"width": 250, 'height': 150, 'display': 'inline-block'})

# content_one_two = html.Div([
#     dbc.Label("Select date range:", size="md"),
#     dcc.DatePickerRange(
#         id="date_range",
#         min_date_allowed=data.DateTime.min().date(),
#         max_date_allowed=data.DateTime.max().date(),
#         start_date=data.DateTime.min().date(),
#         end_date=data.DateTime.max().date()
#     )
# ]), #style={"width": 500, 'height': 200, 'display': 'inline-block'})

chart_page_one = html.Div(
    children=[
        dbc.Col(
            width=8,
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
        dbc.Col(width=8,
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

sidebar = html.Div(
    [
        html.H2("Filters"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with filters", className="lead"
        ),
        dbc.Nav(
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
                dcc.Dropdown(id = 'three')

            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

page_one = dbc.Tab(label="Asset prices",
                   className="fas fa-globe",
                   # style=tab_style,
                   children=[
                       #html.Br(),
                       dbc.Row([
                           dbc.Col([sidebar], style={'display': 'inline-block'}),
                           dbc.Col([
                               chart_page_one
                           ], style={'display': 'inline-block', 'margin-left': '15px', 'margin-top': '7px', 'margin-right': '15px'}),
                       ])
                   ])
