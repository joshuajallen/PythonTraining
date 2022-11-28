
import os
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

MIN_DATE = pd.Timestamp(2010, 1, 4, 0).date()
MAX_DATE = pd.Timestamp(2018, 11, 7, 0).date()

def custom_date_parser(date):
    return pd.datetime.strptime(date, "%Y-%m-%d")


# Fetch prices from local CSV using pandas
prices = pd.read_csv(
    os.path.join(os.path.dirname('__file__'), 'data', "prices.csv"),
    # index_col=0,
    parse_dates=True,
    date_parser=custom_date_parser,
)

prices["date"] = pd.to_datetime(prices["date"], format="%Y-%m-%d")
tickers = prices["ticker"].unique()

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
                    dbc.Label("Choose a Stock Symbol"),
                    dcc.Dropdown(
                        id="stock-ticker-select",
                        options=[
                            {
                                "label": ticker,
                                "value": ticker,
                            }
                            for ticker in tickers
                        ],
                        multi=True,
                        value=[tickers[0]],
                    ),
                ]
            ),
            dbc.FormGroup(
                [
                    dbc.Label("Price"),
                    dbc.Col(
                        dbc.RadioItems(
                            id="stock-ticker-price",
                            options=[
                                {
                                    "label": "Open",
                                    "value": "open",
                                },
                                {
                                    "label": "High",
                                    "value": "high",
                                },
                                {
                                    "label": "Low",
                                    "value": "low",
                                },
                                {
                                    "label": "Close",
                                    "value": "close",
                                },
                            ],
                            value="close",
                        ),
                        width=10,
                    ),
                ]
            ),
            html.Div(
                [
                    dcc.Markdown(
                        """
    Selecting data in the **price** graph
    will adjust the x-axis date range in the bottom **volume** graph.
    """
                    ),
                    html.Pre(id="selected-data"),
                ],
            ),
        ],
            body=True
        )
    ]
)
sidebar = html.Div(
    sidebar_card,
    style=SIDEBAR_STYLE,
)

# price and volume graphs
graphs = [
    dbc.Alert(
        "📊 Hover over the charts to highlight data points and show graph utilities. "
        "All data is historical.",
        color="info",
    ),
    dcc.Graph(id="stock-price-graph", animate=True),
    dcc.Graph(
        id="stock-volume-graph",
        animate=True,
    ),
]

page_five = dbc.Tab(label="Stock prices 🗠",
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
                                                   sidebar,
                                                   md=4,
                                               ),
                                               dbc.Col(
                                                   graphs,
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
