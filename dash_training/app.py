# https://dash.plotly.com/dash-core-components
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/input/
# https://emojipedia.org/

# load packages
import dash
from dash import dcc, State, Input, Output
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
from layout.page_five import *
from layout.global_variables import *

# set global options for formatting
pd.options.display.float_format = '${:.2f}'.format

load_figure_template('LUX')

tabs_styles = {'display': 'inlineBlock'}

titles = ["Asset prices 📊",
          "Portfolio Properties 📊",
          "Data Tables 🌎",
          "Data Report 🗓️",
          "Stock prices 🗠"]

contents = [page_one, page_two, page_three, page_four, page_five]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True,
                assets_folder='N:\\Offdata\\RM\\_People\\JA\\Python\\dash_intro\\assets')

app.title = "RM dashboard"

port = 1500  # or simply open on the default `8050` port


def open_browser():
    webbrowser.open_new("http://localhost:{}".format(port))


def make_a_tab(title, content):
    return dcc.Tab(
        label=title,
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

# top nav bar
nav = dbc.Navbar(
    children=[
        dbc.Row(
            [
                dbc.Col(dbc.NavbarBrand("RM dashboard", className="ml-2")),
            ],
            align="center",
            no_gutters=True,
        ),
    ],
    sticky="top",
)

body_container = dbc.Container(
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
                # html.Div(
                #     id="header-area",
                #     children=[
                #         html.H1(
                #             id="header-title",
                #             children="RM dashboard",
                #         ),
                #         html.Br(),
                #         html.P(
                #             id="header-description",
                #             children=(
                #                 "The cost of precious metals", html.Br(), "between 2018 and 2021"),
                #         ),
                #         html.Hr(),
                #
                #     ]
                # )
            ]
        ),
        html.Div([
            dcc.Tabs(
                parent_className='custom-tabs',
                className='custom-tabs-container',
                children=[make_a_tab(title, content) for title, content, in zip(titles, contents)],
                value="Asset prices")

        ])
    ]
)

app.layout = html.Div([nav, body_container])


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



def filter_data_by_date(df, ticker, start_date, end_date):
    """Apply filter to the input dataframe

    Args:
        df: dateframe to filter
        ticker: stock ticker symbol for filter criteria
        start_date: min date threshold
        end_date: max date threshold
    Returns:
        a filtered dataframe by ticker and date range
    """
    if start_date is None:
        start_date = MIN_DATE

    if end_date is None:
        end_date = MAX_DATE

    filtered = df[
        (df["ticker"] == ticker) & (df["date"] >= start_date) & (df["date"] <= end_date)
    ]
    return filtered


def volume_figure_layout(selected_tickers, xaxis_range=None):
    """Add layout specific to x-axis

    Args:
        selected_tickers: stock tickers for title
        xaxis_range: `dict` with layout.xaxis.range config
    Returns:
        a layout dict
    """
    layout = dict(xaxis={}, yaxis={})
    layout["title"] = "Trading Volume (%s)" % (" & ").join(selected_tickers)
    layout["yaxis"] = {"autorange": True}
    layout["yaxis"]["title"] = "Volume"
    layout["xaxis"]["title"] = "Trading Volume by Date"

    if xaxis_range:
        layout["xaxis"]["range"] = xaxis_range
        layout["xaxis"]["autorange"] = True

    return layout


@app.callback(
    Output("stock-price-graph", "figure"),
    [
        Input("stock-ticker-select", "value"),
        Input("stock-ticker-price", "value"),
    ],
)
def update_price_figure(tickers, price):
    """Create a plot of stock prices

    Args:
        tickers: ticker symbols from the dropdown select
        price: the radio button price selection
    Returns:
        a graph `figure` dict containing the specificed
        price data points per stock
    """

    return {
        "data": [
            {
                "x": [date for date in prices.loc[(prices.ticker == stock)]["date"]],
                "y": [p for p in prices.loc[(prices.ticker == stock)][price]],
                "type": "scatter",
                "mode": "lines",
                "name": stock,
            }
            for stock in tickers
        ],
        "layout": {
            "title": "Stock Price - %s (%s)" % (price.title(), (" & ").join(tickers)),
            "xaxis": {"title": "Date"},
            "yaxis": {"title": "Price"},
        },
    }


@app.callback(
    Output("stock-volume-graph", "figure"),
    [
        Input("stock-ticker-select", "value"),
        Input("stock-price-graph", "relayoutData"),
    ],
)
def update_volume_figure(selected_tickers, relayoutData):
    """Create a plot of stock volume

    Args:
        selected_tickers: ticker symbols from the dropdown select
        relayoutData: data emitted from a `selection` on the price graph
    Returns:
        a graph `figure` dict containing the specificed
        volume data points per stock within the relayoutData
        date range.
    """

    data = []
    from_date = None
    to_date = None

    if relayoutData:
        from_date = relayoutData.get("xaxis.range[0]", None)
        to_date = relayoutData.get("xaxis.range[1]", None)

        if from_date and to_date:
            from_date = pd.Timestamp(from_date)
            to_date = pd.Timestamp(to_date)

            for stock in selected_tickers:
                filtered = filter_data_by_date(prices, stock, from_date, to_date)
                data.append(
                    {
                        "x": filtered["date"],
                        "y": filtered["volume"],
                        "type": "bar",
                        "name": stock,
                    }
                )

            xaxis_range = [from_date, to_date]

            return {
                "data": data,
                "layout": volume_figure_layout(selected_tickers, xaxis_range),
            }

        else:
            data = [
                {
                    "x": [item for item in prices[(prices.ticker == stock)]["date"]],
                    "y": [item for item in prices[(prices.ticker == stock)]["volume"]],
                    "type": "bar",
                    "name": stock,
                }
                for stock in selected_tickers
            ]

            # default dates
            xaxis_range = [MIN_DATE, MAX_DATE]

            return {
                "data": data,
                "layout": volume_figure_layout(selected_tickers, xaxis_range),
            }

    return {"data": data, "layout": volume_figure_layout(selected_tickers)}

# model outputs

@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run_server(debug=False, port=port)

