# %%Dash v2
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import os

df1 = pd.read_csv('https://raw.githubusercontent.com/daniyar135/icebreaker/master/Icebreaker_stats_final.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/daniyar135/icebreaker/master/SV.CSV')
df3 = pd.read_csv('https://raw.githubusercontent.com/daniyar135/icebreaker/master/Silence.csv')

app = Dash(__name__)
server = app.server
fig2 = px.scatter(df1, y="Call duration", x="Number of silences", color="Recording ID", size="Silence Max")
fig3 = px.bar(df3, y="Silence duration", x="Recording ID")
fig4 = px.bar(df3, y="Class", x="Recording ID")
fig5 = px.bar(df2, y="Call Duration", x="Contact ID")

app.layout = html.Div(children=[
    html.H1(children='Icebreaker Dashboard'),

    html.Div(children='''
        Visualizing data from our longest SunVault related calls. The longest silences are represented in a bigger shape.
    '''),
    html.Div(children='''
        Use the slider at the bottom to see each week's longest calls that had silences > 2 minutes.
    '''),

    html.Div([

    dcc.Graph(
    id='graph-with-slider'
    ),

    dcc.Slider(
        df1['week'].min(),
        df1['week'].max(),
        step=None,
        value=df1['week'].min(),
        marks={str(week): ("week" + str(week)) for week in df1['week'].unique()},
        id='week-slider'
    )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    
    html.Div([
    dcc.Graph(
    id='silence-graph',
    figure=fig3
    ),

    dcc.Graph(
    id='blocker-graph',
    figure=fig4
    ),

    ], style={'display': 'inline-block', 'width': '49%'}),

    dcc.Graph(
    id='graph-with-slider2',
    figure=fig2
    ),

    dcc.Graph(
    id='alltime-graph',
    figure=fig5
    )

])

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('week-slider', 'value'))

def update_figure(selected_week):
    filtered_df = df1[df1.week == selected_week]

    fig = px.scatter(filtered_df, x="Number of silences", y="Call duration", size="Call duration", color="Recording ID",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server()
