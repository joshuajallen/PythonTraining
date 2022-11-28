from dash import dash_table
from dash import Input, Output, State, html
import dash_bootstrap_components as dbc
from layout.global_variables import *
import pandas as pd
import numpy as np

pd.options.display.float_format = '${:.2f}'.format

df = pd.melt(data, id_vars='DateTime')
df = df.groupby('variable').agg(
    {
        "value": ["min", "max", "median", "skew", np.std]
    }
)
df = df.droplevel(0, axis=1).reset_index(level=0)
df = df.round(2)
cols = ["min", "max", "median", "skew", "std"]

(styles, legend) = discrete_background_color_bins(df, columns = cols)


summary = pd.melt(data, id_vars='DateTime')
summary = summary.groupby('variable').agg(
    {
        "value": ["min", "max", "median", "skew", np.std]
    }
)

summary = summary.droplevel(0, axis=1).reset_index(level=0)
cols = ["variable", "min", "max", "median", "skew", "std"]
summary.columns = cols

gold = summary[summary['variable'] == 'Gold']['std']
silver = summary[summary['variable'] == 'Silver']['std']
# df.loc[df['variable'] == 'Gold', 'std']

modal = html.Div(
    [
        dbc.Button("Open modal", id="open", n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader("Header"),
                dbc.ModalBody(html.Div([
                    dash_table.DataTable(
                        id='modal_table',
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.astype(str).to_dict('records'),
                        style_data_conditional=styles
                    ),
                ])),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal",
            is_open=False,
        ),
    ]
)


page_four = dbc.Tab(label='Data Report 🗓️',
                    className="fas fa-box",
                    children=[
                        dbc.Row([
                            dbc.Col(modal, md=4),
                            dbc.Col([
                                dbc.Alert(
                                    ["Gold sd: ", html.A(gold.values.round(1), href="Tab1", className="alert-link")],
                                    color="info",
                                )], md=2),
                            dbc.Col([
                                dbc.Alert(
                                    ["Silver: ", html.A(silver.values.round(1), href="#", className="alert-link")],
                                    color="info",
                                )], md=2),
                            dbc.Col([
                                dbc.Alert(
                                    "info",
                                    color="#8B0000",
                                )], md=2),
                            dbc.Col([
                                dbc.Alert(
                                    html.A("primary color", href="#", className="alert-link"),
                                    color="primary",
                                )], md=2)
                        ]),
                        html.Br(),
                        html.Hr(),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                            html.Div([
                                dash_table.DataTable(
                                    id='table',
                                    columns=[{"name": i, "id": i} for i in df.columns],
                                    data=df.astype(str).to_dict('records'),
                                    style_data_conditional=styles
                                ),
                            ])
                                ], md = 12)
                        ])

                    ])
