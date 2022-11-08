from dash import Dash, dash_table, dcc, html
import dash_bootstrap_components as dbc
from layout.global_variables import *
import pandas as pd

df = pd.melt(data, id_vars='DateTime')
df = df.groupby('variable').agg(
    {
        "value": ["min", "max", "median", "skew"]
    }
)
df = df.droplevel(0, axis=1).reset_index(level=0)
cols = ["min", "max", "median", "skew"]

cols = ["min", "max", "median", "skew"]
(styles, legend) = discrete_background_color_bins(df, columns = cols)

page_four = dbc.Tab(label='Data Tables',
                     className="fas fa-box",
                     children=[
                         html.Div([
                             dash_table.DataTable(
                                 id='table',
                                 columns=[{"name": i, "id": i} for i in df.columns],
                                 data=df.to_dict('records'),
                                 style_data_conditional=styles
                             ),

                         ])
                     ])
