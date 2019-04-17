import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
import redis

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('Twitter Languages Count Live Feed For particular Tweets'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=10*1000, # in milliseconds
            n_intervals=0
        )
    ])
)


@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Twitter Languages ', style=style),
        #html.Span('Latitude: {0:.2f}'.format(lat), style=style),
        #html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
    ]


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    data = {'lang':[], 'count':[]}
    #Get Data from redis
    r_server = redis.Redis("localhost", charset="utf-8", decode_responses=True)
    lang = r_server.hgetall("lang")
    for i in lang.keys():
        data["lang"].append(i)
        data["count"].append(lang[i])    
    
    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 70, 'r': 70, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
    
    fig.append_trace({
        'x': data["lang"],
        'y': data['count'],
        'name': 'Languages Count',
        'mode': 'lines+markers',
        'type': 'scatter'
	#'type':'bar'
    }, 1, 1)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
