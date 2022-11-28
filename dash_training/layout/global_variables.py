import pandas as pd
import os
import colorlover
from dash import html

def RM_PATH(subpath):
    path = os.path.join(os.path.abspath('N:/Offdata/RM/_People/JA/Python/dash_intro'), os.path.abspath(str(subpath)))
    return path


data = pd.read_csv(RM_PATH("data/precious_metals_prices_2018_2021.csv"))
data['DateTime'] = pd.to_datetime(data['DateTime'], format="%Y-%m")

COLOUR_PALETTE = [
  "#12273F", # Dark Blue
  "#3CD7D9", # Aqua
  "#C4C9CF", # Stone
  "#FF7300", # Orange
  "#9E71FE", # Purple
  "#D4AF37"  # Gold
]

CUSTOM_PAL_LINES = [
    "#2c7bb6",
    "#F9543A",
    "#4DAF4A",
    "#984EA3",
    "#FF7F00",
    "#c1c1c1",
    "#A65628",
    "#F781BF"
]

def discrete_background_color_bins(df, n_bins=7, columns='all'):
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    if columns == 'all':
        if 'id' in df:
            df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
        else:
            df_numeric_columns = df.select_dtypes('number')
    else:
        df_numeric_columns = df[columns]
    df_max = df_numeric_columns.max().max()
    df_min = df_numeric_columns.min().min()
    ranges = [
        ((df_max - df_min) * i) + df_min
        for i in bounds
    ]
    styles = []
    legend = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        backgroundColor = colorlover.scales[str(n_bins + 4)]['div']['RdYlGn'][2:-2][i - 1]
        color = 'black'

        for column in df_numeric_columns:
            styles.append({
                'if': {
                    'filter_query': (
                            '{{{column}}} >= {min_bound}' +
                            (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': column
                },
                'backgroundColor': backgroundColor,
                'color': color
            })
        legend.append(
            html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
                html.Div(
                    style={
                        'backgroundColor': backgroundColor,
                        'borderLeft': '1px rgb(50, 50, 50) solid',
                        'height': '10px'
                    }
                ),
                html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
            ])
        )

    return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))
