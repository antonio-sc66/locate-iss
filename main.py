import time
import dash
import numpy as np
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


POS_URL = 'http://api.open-notify.org/iss-now.json'
HEROKU_DEPLOY = True
PORT = 80
HOST = '0.0.0.0' # 0.0.0.0 to publish on local network, 127.0.0.1 to publish on localhost
INTER_SEC = 5  # Refresh interval in seconds
FIG_WIDTH = 1280 # pixels
FIG_HEIGHT = 720 # pixels
SITE_TITLE = 'ISS Locator'
github_link= 'https://github.com/antonio-sc66/locate-iss'


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
                                   showocean=True,
                                   landcolor="LightGreen",
                                   oceancolor="LightBlue",
                                   lakecolor="LightGreen"
                                   ),
                        width = FIG_WIDTH, height = FIG_HEIGHT,
                        dragmode=False
                      )
    fig.update_traces(marker=dict(size=15, symbol="x", line=dict(width=2, color='DarkSlateGrey')),
                      mode="markers+text+lines", opacity=1)
    #fig.show()
    return fig


if __name__ == "__main__":
    app.layout = html.Div([
        html.A('Code on Github', href=github_link),
        dcc.Graph(id='live-update-graph', config={'displaylogo': False, 'scrollZoom': False, 'autosizable': True, 'fillFrame':True, 'displayModeBar': True}),
        dcc.Interval(
            id='interval-component',
            interval=INTER_SEC * 1000,  # in milliseconds
            n_intervals=0
        )
    ], style={"height" : "100%", "width" : "100%", "textAlign" : "center", "display" : "flex",
              "margin-left" : "auto", "margin-right" : "auto", "justify-content" : "center",
              "align-items" : "center"})

    server = app.server
    if not HEROKU_DEPLOY:
        app.run_server(debug=False, use_reloader=True, port=PORT, threaded=True, host=HOST)
    else:
        app.run_server()