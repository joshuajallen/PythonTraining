# https://dash.plotly.com/dash-core-components
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/input/

# load packages
import dash
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import webbrowser
from threading import Timer

# import individual modules - either method works
# exec(open("./layout/page_one.py").read())
from layout.page_one import page_one, data
from layout.page_two import page_two
from layout.page_three import page_three
from layout.page_four import page_four
from layout.global_variables import *

load_figure_template('LUX')

tabs_styles = {'display': 'inlineBlock'}

icons = ["fas fa-globe",
         "fas fa-chart-area",
         "fas fa-box",
         "fas fa-chart-area"]

titles = ["Asset prices",
          "Portfolio Properties",
          "Data Tables",
          "Tab 4 placer"]

contents = [page_one, page_two, page_three, page_four]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.LUMEN],
                suppress_callback_exceptions=True,
                assets_folder='N:\\Offdata\\RM\\_People\\JA\\Python\\dash_intro\\assets')

app.title = "RM dashboard"

port = 1500  # or simply open on the default `8050` port


def open_browser():
    webbrowser.open_new("http://localhost:{}".format(port))


def make_a_tab(icon, title, content):
    return dcc.Tab(
        label=title, className=icon,
        value=title.lower().replace(" ", "-"),
        children=[
            html.Br(),
            html.Hr(),
            html.Br(),
            # html.H3(title),
            # html.P(f"This is the tab {title}."),
            content
        ])


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
                            children="RM dashboard",
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
        xaxis_title="Date",
        yaxis_title="Price (USD/oz)",
        font=dict(
            family="Verdana, sans-serif",
            size=10
        ),
    )

    return fig


@app.callback(
    Output("scatter-chart", "figure"),
    Input("date_range", "start_date"),
    Input("date_range", "end_date")
)
def update_scatter(start_date, end_date):
    # Create a plotly plot for use by dcc.Graph().
    plot_data=data.loc[(data.DateTime >= start_date) & (data.DateTime <= end_date)]
    dist=px.scatter_matrix(plot_data,
                         dimensions=plot_data.columns[1:],
                         title="Scatter matrix:")

    dist.update_layout(
        font=dict(
            family="Verdana, sans-serif",
            size=12
        ),
    )

    return dist


@app.callback(
    Output("page_two_scatter", "figure"),
    Input("metal_one", "value"),
    Input("metal_two", "value")
)
def update_page_two(metal_one, metal_two):
    # Create a plotly plot for use by dcc.Graph().
    plot_data=data
    scatter=px.scatter(plot_data,
                       x=data[metal_one],
                       y=data[metal_two],
                       color_discrete_sequence=COLOUR_PALETTE)

    scatter.update_layout(
        font=dict(
            family="Verdana, sans-serif",
            size=12
        ),
    )

    return scatter


if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run_server(debug=False, port=port)


