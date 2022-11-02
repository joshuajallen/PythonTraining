from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import os
import plotly.express as px

def RM_PATH(subpath):
    path=os.path.join(os.path.abspath('N:/Offdata/RM/_People/JA/Python/dash_intro'), os.path.abspath(str(subpath)))
    return path

data = pd.read_csv(RM_PATH("data/precious_metals_prices_2018_2021.csv"))
data['DateTime'] = pd.to_datetime(data['DateTime'], format="%Y-%m")
fig = px.line(data,
              x="DateTime",
              y=["Gold"],
              title="Line chart of selected asset prices")


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
    "top": 320,
    "left": 0,
    "bottom": 50,
    "width": "25rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "25rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
content_one_one = html.Div([
    dbc.Label("Select metal", size="md"),
    dcc.Dropdown(
        id="metal-filter",
        className="dropdown",
        options=[{"label": metal, "value": metal} for metal in data.columns[1:]],
        clearable=False,
        value=data.columns[1]
    )
], style={"width": 250, 'height': 150, 'display': 'inline-block'})

content_one_two = html.Div([
    dbc.Label("Select date range:", size="md"),
    dcc.DatePickerRange(
        id="date_range",
        min_date_allowed=data.DateTime.min().date(),
        max_date_allowed=data.DateTime.max().date(),
        start_date=data.DateTime.min().date(),
        end_date=data.DateTime.max().date()
    )
], style={"width": 400, 'height': 150, 'display': 'inline-block'})

chart_page_one = html.Div(
    children=[
        dbc.Col(
            html.Div(
                id="graph-container",
                children=dcc.Graph(
                    id="price-chart",
                    figure=fig,
                    config={"displayModeBar": False}
                ),
            ), style={'width': '95%',
                      'margin': '10px'
                      }
        )
    ],
    style={"width": 900, 'height': 400}
)

sidebar = html.Div(
    [   html.Br(),
        html.P(
        "Please select parameter options below:", className="lead"
    ),
        html.Hr(),
        dbc.Row(
            [dbc.Col(content_one_one,
                     style={'display': 'inline-block', 'margin': '1px', 'width': '200px'}),
             dbc.Col(content_one_two,
                     style={'display': 'inline-block', 'margin': '1px', 'width': '200px'}),
             dbc.Col(style={'display': 'inline-block', 'margin': '1px', 'width': '700px'})
             ]),
        html.Hr()
        # dbc.Nav(
        #     [
        #         dbc.NavLink("Home", href="/", active="exact"),
        #         dbc.NavLink("Page 1", href="/page-1", active="exact"),
        #         dbc.NavLink("Page 2", href="/page-2", active="exact"),
        #     ],
        #     vertical=True,
        #     pills=True,
        # ),
    ],
    style=SIDEBAR_STYLE,
)

page_one = dbc.Tab(label="Asset prices",
                   style=tab_style,
                   children=[
                           html.Br(),
                           dbc.Row([
                               html.Br(),
                               dbc.Col([sidebar]),
                               dbc.Col([
                                   dbc.Row([
                                       dbc.Col(chart_page_one, style={'height': '420px'}),
                                       dbc.Col(style={"width": "100%"})
                                   ])
                               ]),
                           ]),
                   ])
