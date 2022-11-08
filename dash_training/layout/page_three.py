from dash import Dash, dash_table, dcc, html
import dash_bootstrap_components as dbc
from layout.global_variables import data
import pandas as pd

df = pd.melt(data, id_vars='DateTime')
df = df.groupby('variable').agg(
    {
        "value": ["min", "max", "median", "skew"]
    }
)
df = df.droplevel(0, axis=1).reset_index(level=0)
cols = ["min", "max", "median", "skew"]

page_three = dbc.Tab(label='Data Tables',
                     className="fas fa-box",
                     children=[
                         html.Div([
                             dash_table.DataTable(
                                 df.to_dict('records'),
                                 [{"name": i, "id": i} for i in df.columns],
                                 filter_action="native",
                                 sort_action="native",
                                 sort_mode="multi",
                                 column_selectable="single",
                                 row_selectable="multi",
                                 selected_columns=[],
                                 selected_rows=[],
                                 page_action="native",
                                 page_current=0,
                                 page_size=10,
                                 style_data_conditional=[
                                     {
                                         'if': {
                                             'filter_query': '{min} < 1000',
                                             'column_id': 'Humidity'
                                         },
                                         'backgroundColor': 'tomato',
                                         'color': 'white'
                                     },
                                     {
                                         'if': {
                                             'column_id': 'skew',
                                             'filter_query': '{{skew}} = {}'.format(df['skew'].max())
                                         },
                                         'backgroundColor': '#85144b',
                                         'color': 'white'
                                     }
                                 ]
                             ),
                             html.Br(),
                             html.Hr(),
                             dash_table.DataTable(
                                 df.to_dict('records'),
                                 [{"name": i, "id": i} for i in df.columns],
                                 filter_action="native",
                                 sort_action="native",
                                 sort_mode="multi",
                                 column_selectable="single",
                                 row_selectable="multi",
                                 selected_columns=[],
                                 selected_rows=[],
                                 page_action="native",
                                 page_current=0,
                                 page_size=10,
                                 style_data_conditional=[
                                     {
                                         'if': {
                                             'filter_query': '{min} < 1000',
                                             'column_id': 'Humidity'
                                         },
                                         'backgroundColor': 'tomato',
                                         'color': 'white'
                                     },
                                     {
                                         'if': {
                                             'column_id': 'skew',
                                             'filter_query': '{{skew}} = {}'.format(df['skew'].max())
                                         },
                                         'backgroundColor': '#85144b',
                                         'color': 'white'
                                     }
                                 ]
                             )
                         ])
                     ])
