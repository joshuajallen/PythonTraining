import dash
from dash import html

app = dash.Dash(__name__)

app.layout = html.P("Hello world")  # p is a paragraph

if __name__ == "__main__":
    app.run_server(debug=False)     # run the application 