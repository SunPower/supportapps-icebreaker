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
figa = px.scatter(df1, y="Call duration", x="Number of silences", color="Recording ID", size="Silence Max")
figs = px.bar(df3, y="Silence duration", x="Recording ID")
figb = px.bar(df3, y="Recording ID", x="Class")
figsv = px.histogram(df2, y="Contact ID", x="Call Duration")

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
    figure=figs
    ),

    dcc.Graph(
    id='blocker-graph',
    figure=figb,
    ),

    ], style={'display': 'inline-block', 'width': '49%'}),

    dcc.Graph(
    id='alltime-graph',
    figure=figa
    ),

    dcc.Graph(
    id='sv-graph',
    figure=figsv
    )

])

@app.callback(
    Output('graph-with-slider', 'figure'),
    Output('blocker-graph', 'figure'),
    Output('silence-graph', 'figure'),
    Input('week-slider', 'value'))

def update_figure(selected_week):
    filtered_df = df1[df1.week == selected_week]

    fig = px.scatter(filtered_df, x="Number of silences", y="Call duration", size="Call duration", color="Recording ID",
                     log_x=True, size_max=55)
    fig.update_layout(transition_duration=500)

    filtered_df3 = df3[df3.week == selected_week]

    fig1 = px.bar(filtered_df3, y="Silence duration", x="Recording ID")
    fig1.update_layout(transition_duration=500)

    fig2 = px.bar(filtered_df3, y="Recording ID", x="Class")
    fig2.update_layout(transition_duration=500)

    return fig, fig1, fig2

if __name__ == '__main__':
    app.run_server()

# %%
