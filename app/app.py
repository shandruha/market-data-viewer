import pandas as pd
from flask import Flask
import dash
from dash.dependencies import Output, Input
from dash import dcc
from dash import html as html
import dash_bootstrap_components as dbc
import plotly
import plotly.graph_objs as go
from utils.db import get_connection


def get_tickers():
    with get_connection('app', 'app') as conn:
        cursor = conn.cursor()
        tickers = []

        cursor.execute('SELECT id, name FROM tickers ORDER BY id')

        for id, name in cursor.fetchall():
            tickers.append({'label': name, 'value': id})

        return tickers


def get_prices(ticker_id):
    with get_connection('app', 'app') as conn:
        query = 'SELECT date_time, price FROM price_history WHERE ticker_id = %s ORDER BY date_time'
        df = pd.read_sql(query, con=conn, params=(ticker_id,))
        return df


server = Flask(__name__)
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title='Realtime Market Data Viewer',
    server=server
)


app.layout = html.Div(
    children=[
        dbc.Row([
            dbc.Col(
                dbc.InputGroup([
                    dbc.InputGroupText('Ticker:'),
                    dbc.Select(options=get_tickers(), id='select-ticker', value=1)
                ]),
                width={'size': 4}
            )
        ]),
        dbc.Row([dbc.Col(dcc.Graph(id='live-graph', animate=True))]),
        dcc.Interval(
            id='graph-update',
            interval=1000,
            n_intervals=0
        ),
    ]
)


@app.callback(
    Output('live-graph', 'figure'),
    [Input('graph-update', 'n_intervals'), Input(component_id='select-ticker', component_property='value')]
)
def update_prices(n, ticker_id):
    df = get_prices(ticker_id)

    data = plotly.graph_objs.Scatter(
        x=df['date_time'],
        y=df['price'],
        name='Scatter',
        mode='lines+markers'
    )

    y_range = [min(df['price'].min(), -5), max(df['price'].max(), 5)]

    return {
        'data': [data],
        'layout': go.Layout(
            yaxis=dict(range=y_range, title='Price'),
            xaxis=dict(range=[df['date_time'].min(), df['date_time'].max()], title='Timestamp')
        )
    }


if __name__ == '__main__':
    app.run_server()