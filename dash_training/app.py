# https://dash.plotly.com/dash-core-components
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/input/

# load packages

import os
import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import webbrowser
from threading import Timer

# import individual modules - either method works
# exec(open("./layout/page_one.py").read())
from layout.page_one import page_one, data
from layout.page_two import page_two


tabs_styles = {'display': 'inlineBlock'}
icons = ["fa-globe", "fa-chart-area", "fa-chart-area", "fa-chart-area"]
titles = ["Asset prices", "Portfolio Properties", "Tab 3 placer", "Tab 4 placer"] #html.I("Asset prices", className="fas fa-shield")
contents = [page_one, page_two, html.Div(), html.Div()]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.LUMEN],
                suppress_callback_exceptions=True,
                assets_folder='N:\\Offdata\\RM\\_People\\JA\\Python\\dash_intro\\assets')

app.title = "Asset price dashboard"

port = 1500  # or simply open on the default `8050` port

def open_browser():
    webbrowser.open_new("http://localhost:{}".format(port))


def make_a_tab(icon, title, content):
    return dcc.Tab(
        label=title, className=icon + " custom-tab",
        selected_className="custom-tab--selected",
        value=title.lower().replace(" ", "-"),
        children=[
            html.Br(),
            # html.H3(title),
            # html.P(f"This is the tab {title}."),
            content
        ])

# app.layout = html.P("Hello world")  # p is a paragraph
# define layout using html div
# this section is essentially the UI, populating inputs/outputs/headings/containers etc.
app.layout = dbc.Container(
    fluid=True,
    children=[
        html.Link(
            type="text/css",
            rel='stylesheet',
            href='./assets/custom.css'
        ),
        html.Div([
            dcc.Location(id='url', refresh=False)
        ]),
        html.Div(id='page-content'),
        html.Div(
            id="app-container",
            children=[
                html.Br(),
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
                            children=(
                                "The cost of precious metals", html.Br(), "between 2018 and 2021"),
                        ),
                        html.Hr(),

                    ]
                )
            ]
        ),
        html.Div([
            dcc.Tabs(
                parent_className='custom-tabs',
                className='custom-tabs-container',
                children=[make_a_tab(icon, title, content) for icon, title, content, in zip(icons, titles, contents)],
                value="Asset prices")

# dbc.Tabs(id="tabs",
#          style=tabs_styles,
#          className='custom-tabs-container',
#          active_tab="Asset prices",
#          children=[
#              # section for tabs
#              page_one,
#              page_two
#          ])
])
]
)

server = app.server

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
            size=14
        ),
    )

    return fig


if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run_server(debug=False, port=port)

