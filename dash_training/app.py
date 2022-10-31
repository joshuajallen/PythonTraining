# https://dash.plotly.com/dash-core-components

import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import webbrowser
from threading import Timer

data = pd.read_csv("02_03/precious_metals_prices_2018_2021.csv")
data['DateTime'] = pd.to_datetime(data['DateTime'], format="%Y-%m")
fig = px.line(data,
              x="DateTime",
              y=["Gold"],
              title="Line chart of selected asset prices")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.SUPERHERO],
                suppress_callback_exceptions=True,
                assets_folder='N:\\Offdata\\RM\\_People\\JA\\Python\\dash_intro\\assets')

app.title = "Asset price dashboard"

port = 5000  # or simply open on the default `8050` port


def open_browser():
    webbrowser.open_new("http://localhost:{}".format(port))


# app.layout = html.P("Hello world")  # p is a paragraph
# define layout using html div
# this section is essentially the UI, populating inputs/outputs/headings/containers etc.
app.layout = html.Div(
    id="app-container",
    children=[
        html.Div(
            id="header-area",
            children=[
                html.H1(
                    id="header-title",
                    children="Precious Metal Prices",

                ),
                html.P(
                    id="header-description",
                    children=("The cost of precious metals", html.Br(), "between 2018 and 2021"),
                ),
            ],
        ),
        html.Div(
            id="menu-area",
            children=[
                html.Div(
                    className="menu-title",
                    children="Metal"
                ),
                dbc.Row(children=[
                    dbc.Col(
                        html.Div(children=[
                            dbc.Label("Select metal", size="md"),
                            dcc.Dropdown(
                                id="metal-filter",
                                className="dropdown",
                                options=[{"label": metal, "value": metal} for metal in data.columns[1:]],
                                clearable=False,
                                value=data.columns[1]
                                # style={'width': '50%',
                                #        'height': '30px',
                                #        'lineHeight': '30px',
                                #        'borderWidth': '1px',
                                #        'borderStyle': 'solid',
                                #        'borderRadius': '5px',
                                #        'textAlign': 'center',
                                #        'margin': '10px'
                                #        }
                            )]
                        ), width=2),
                    dbc.Col(
                        html.Div(children=[
                            dbc.Label("Date Range", size="md"),
                            dcc.DatePickerRange(
                                id="date_range",
                                min_date_allowed=data.DateTime.min().date(),
                                max_date_allowed=data.DateTime.max().date(),
                                start_date=data.DateTime.min().date(),
                                end_date=data.DateTime.max().date()
                            )

                        ]
                        ), width=2),
                    dbc.Col(html.Div(), width=5),
                ]

                )
            ]
        ),
        html.Div(
            dbc.Row(
                dbc.Col(
                    html.Div(
                        id="graph-container",
                        children=dcc.Graph(
                            id="price-chart",
                            figure=fig,
                            config={"displayModeBar": False}
                        ),
                    ), style={'width': '50%',
                              'height': '400px',
                              'margin': '20px'
                              },
                    width="50%")
            )
        )

    ]
)


@app.callback(
    Output("price-chart", "figure"),
    Input("metal-filter", "value"),
    Input("date_range", "start_date"),
    Input("date_range", "end_date")
)
def update_chart(metal, start_date, end_date):
    # Create a plotly plot for use by dcc.Graph().
    plot_data = data.loc[(data.DateTime >= start_date) & (data.DateTime <= end_date)]
    fig = px.line(
        plot_data,
        title="Precious Metal Prices 2018-2021",
        x="DateTime",
        y=[metal],
        color_discrete_map={
            "Platinum": "#E5E4E2",
            "Gold": "gold",
            "Silver": "silver",
            "Palladium": "#CED0DD",
            "Rhodium": "#E2E7E1",
            "Iridium": "#3D3C3A",
            "Ruthenium": "#C9CBC8"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="Price (USD/oz)",
        font=dict(
            family="Verdana, sans-serif",
            size=18,
            color="white"
        ),
    )

    return fig


if __name__ == '__main__':
     Timer(1, open_browser).start();
     app.run_server(debug=False, port=port)