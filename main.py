import time
import dash
import numpy as np
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly.validators.scatter.marker import SymbolValidator
import plotly.graph_objects as go

POS_URL = 'http://api.open-notify.org/iss-now.json'
PORT = 80
HOST = '0.0.0.0' # 0.0.0.0 to publish on local network, 127.0.0.1 to publish on localhost
INTER_SEC = 5  # Refresh interval in seconds
FIG_WIDTH = 1280 # pixels
FIG_HEIGHT = 720 # pixels
SITE_TITLE = 'ISS Locator'


app = dash.Dash()
app.title = SITE_TITLE

@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def get_figure(n):

    pos_df = pd.read_json(POS_URL)
    pos_df = pd.DataFrame(np.array([[pos_df['iss_position']['latitude'], pos_df['iss_position']['longitude']]]), columns=['lat', 'lon'])
    fig = px.scatter_geo(pos_df, lat=pos_df['lat'], lon=pos_df['lon'], projection='natural earth')
    fig.update_layout(title = 'International Space Station realtime location',
                        geo = dict(showcountries = True,
                                   showland = True,
                                   showlakes = True,
                                   showocean=True,
                                   landcolor="LightGreen",
                                   oceancolor="LightBlue",
                                   lakecolor="Blue"),
                        width = FIG_WIDTH, height = FIG_HEIGHT,
                      )
    fig.update_traces(marker=dict(size=15))
    #fig.show()
    return fig


if __name__ == "__main__":
    app.layout = html.Div([
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=INTER_SEC * 1000,  # in milliseconds
            n_intervals=0
        )
    ], style={"height" : "100%", "width" : "100%", "textAlign" : "center", "display" : "flex",
              "margin-left" : "auto", "margin-right" : "auto", "justify-content" : "center",
              "align-items" : "center"})

    server = app.server
    app.run_server(debug=False, use_reloader=True, port=PORT, threaded=True, host=HOST)