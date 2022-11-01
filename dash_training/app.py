# https://dash.plotly.com/dash-core-components
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/input/

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
                external_stylesheets=[dbc.themes.LUMEN],
                suppress_callback_exceptions=True,
                assets_folder='N:\\Offdata\\RM\\_People\\JA\\Python\\dash_intro\\assets')

app.title = "Asset price dashboard"

port = 5000  # or simply open on the default `8050` port


def open_browser():
    webbrowser.open_new("http://localhost:{}".format(port))


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
        # style={'width': '50%',
        #        'height': '30px',
        #        'lineHeight': '30px',
        #        'borderWidth': '1px',
        #        'borderStyle': 'solid',
        #        'borderRadius': '5px',
        #        'textAlign': 'center',
        #        'margin': '10px'
        #        }
    )
], style={"width": 350, 'height': 150, 'display': 'inline-block'})

chart_page_one = html.Div(
    children=[
        html.Br(),
        dbc.Col(
            html.Div(
                id="graph-container",
                children=dcc.Graph(
                    id="price-chart",
                    figure=fig,
                    config={"displayModeBar": False}
                ),
            ), style={'width': '90%',
                      'margin': '20px'
                      }
        ),
        html.Hr()
    ],
    style={"width": 800, 'height': 400}
)

# app.layout = html.P("Hello world")  # p is a paragraph
# define layout using html div
# this section is essentially the UI, populating inputs/outputs/headings/containers etc.
app.layout = dbc.Container(
    fluid=True,
    children=[
        html.Div([
            dcc.Location(id='url', refresh=False),
            # html.Link(
            #     type="test/css",
            #     rel='stylesheet',
            #     href='N:\\Offdata\\RM\\_People\\JA\\Python\\dash_intro\\assets\\jquery.dataTables.min.css'
            # ),
            # html.Link(
            #     type="test/css",
            #     rel='stylesheet',
            #     href='N:\\Offdata\\RM\\_People\\JA\\Python\\dash_intro\\assets\\dc.css'
            # ),
            # html.Link(
            #     type="test/css",
            #     rel='stylesheet',
            #     href='N:\\Offdata\\RM\\_People\\JA\\Python\\dash_intro\\assets\\webix_modified.css'
            # ),
            # html.Link(
            #     type="test/css",
            #     rel='stylesheet',
            #     href='N:\\Offdata\\RM\\_People\\JA\\Python\\dash_intro\\assets\\custom.css'
            # ),
        ]),
        html.Div(id='page-content'),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="header-area",
                    children=[
                        html.H1(
                            id="header-title",
                            children="Precious Metal Prices",

                        ),
                        html.Br(),
                        html.P(
                            id="header-description",
                            children=("The cost of precious metals", html.Br(), "between 2018 and 2021"),
                        ),
                        html.Hr(),

                    ]
                )
            ]
        ),
        dbc.Row(
            [dbc.Col(content_one_one,
                     style={'display': 'inline-block', 'margin': '5px', 'width': '200px'}),
             dbc.Col(content_one_two,
                     style={'display': 'inline-block', 'margin': '5px', 'width': '200px'})
             ]),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(chart_page_one, style={"width": "100%"}),
                dbc.Col(style={"width": "100%"})
            ]
        )
    ]
)


# html.Div([
#     html.Col(
#         [
#             dbc.Label("Select metal", size="md"),
#             dcc.Dropdown(
#                 id="metal-filter",
#                 className="dropdown",
#                 options=[{"label": metal, "value": metal} for metal in data.columns[1:]],
#                 clearable=False,
#                 value=data.columns[1],
#                 style={'width': '50%',
#                        'height': '30px',
#                        'lineHeight': '30px',
#                        'borderWidth': '1px',
#                        'borderStyle': 'solid',
#                        'borderRadius': '5px',
#                        'textAlign': 'center',
#                        'margin': '10px'
#                        }
#             ),
#         ]),
#
#     html.Col(
#         [
#             dbc.Label("Date Range", size="md"),
#             dcc.DatePickerRange(
#                 id="date_range",
#                 min_date_allowed=data.DateTime.min().date(),
#                 max_date_allowed=data.DateTime.max().date(),
#                 start_date=data.DateTime.min().date(),
#                 end_date=data.DateTime.max().date(),
#                 style={'width': '50%',
#                        'height': '30px',
#                        'lineHeight': '30px',
#                        'borderWidth': '1px',
#                        'borderStyle': 'solid',
#                        'borderRadius': '5px',
#                        'textAlign': 'center',
#                        'margin': '10px'
#                        }
#             )
#         ]),
# ]),

# html.Div(
#     id="menu-area",
#     children=[
#         html.Br(),
#         dbc.Row(children=[
#             dbc.Col(html.Div(
#                 children=[
#                 dbc.Label("Select metal", size="md"),
#                 dcc.Dropdown(
#                     id="metal-filter",
#                     className="dropdown",
#                     options=[{"label": metal, "value": metal} for metal in data.columns[1:]],
#                     clearable=False,
#                     value=data.columns[1]
#                     # style={'width': '50%',
#                     #        'height': '30px',
#                     #        'lineHeight': '30px',
#                     #        'borderWidth': '1px',
#                     #        'borderStyle': 'solid',
#                     #        'borderRadius': '5px',
#                     #        'textAlign': 'center',
#                     #        'margin': '10px'
#                     #        }
#                 )]
#             ), width=2),
#             dbc.Col(html.Div(children=[
#                 dbc.Label("Date Range", size="md"),
#                 dcc.DatePickerRange(
#                     id="date_range",
#                     min_date_allowed=data.DateTime.min().date(),
#                     max_date_allowed=data.DateTime.max().date(),
#                     start_date=data.DateTime.min().date(),
#                     end_date=data.DateTime.max().date()
#                 )
#
#             ]
#             ), width=2),
#             dbc.Col(html.Div(), width=3),
#         ]
#
#         )
#     ]
# ),
# html.Div(
#     children=[
#         html.Br(),
#         dbc.Row(
#             dbc.Col(
#                 html.Div(
#                     id="graph-container",
#                     children=dcc.Graph(
#                         id="price-chart",
#                         figure=fig,
#                         config={"displayModeBar": False}
#                     ),
#                 ), style={'width': '50%',
#                           'margin': '20px'
#                           },
#                 width="50%")
#         ),
#         html.Hr()
#     ]
#
# )


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
        template="ggplot2",
        xaxis_title="Date",
        yaxis_title="Price (USD/oz)",
        font=dict(
            family="Verdana, sans-serif",
            size=18
        ),
    )

    return fig


if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run_server(debug=False, port=port)
