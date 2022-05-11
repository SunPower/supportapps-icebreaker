# %%Dash v2
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import os

df1 = pd.read_csv('https://raw.githubusercontent.com/daniyar135/supportapps-icebreaker/master/Icebreaker_stats_final.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/daniyar135/supportapps-icebreaker/master/Silence.csv')
df3 = pd.read_csv('https://raw.githubusercontent.com/daniyar135/supportapps-icebreaker/master/SV.csv')
df4 = pd.read_csv('https://raw.githubusercontent.com/daniyar135/supportapps-icebreaker/master/Top10.csv')

app = Dash(__name__)
server = app.server
figa = px.scatter(df1, y="Call duration", x="Number of silences", color="Contact ID", size="Silence Max")
figs = px.bar(df2, y="Silence duration (seconds)", x="Contact ID")
figb = px.bar(df2, y="Contact ID", x="Class", color="Subclass")
figsv = px.bar(df3, y="callduration", x="week")
figtop = px.bar(df4, y="callduration", x="skillname", color="skillname")

app.layout = html.Div(children=[
    html.H1(children='Icebreaker Dashboard'),

    html.Div(children='''
        Visualizing data from our longest SunVault related calls.
    '''),
    html.Div(children='''
        Use the slider below to see each week's longest SunVault related calls that had silences > 2 minutes. Larger shapes represent longer silences.
    '''),
    html.Div(children='''
        The upper graph on the right represents the type of issue that prompted the silence.
    '''),
    html.Div(children='''
        The lower graph on the right represents the length of the silence for each call.
    '''),

    html.Div([

    dcc.Graph(
    id='graph-with-slider',
    figure=figa
    ),

    dcc.Slider(
        min=df1['week'].min(),
        max=df1['week'].max(),
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

    html.Div(children='''
        The graph below represents all of the longest SunVault related calls for 2022 (5 per week)
    '''),

    dcc.Graph(
    id='alltime-graph',
    figure=figa
    ),

    html.Div(children='''
        The histogram below represents the call duration for all SunVault related calls for 2022.
    '''),

    dcc.Slider(
        min=df3['callduration'].min(),
        max=df3['callduration'].max(),
        step=None,
        marks={
        0: {'label': 'all', 'style': {'color': '#77b0b1'}},
        60: {'label': '>1hr'},
        120: {'label': '>2hr'},
        180: {'label': '>3hr'},
        240: {'label': '>4hr'},
        300: {'label': ">5hr", 'style': {'color': '#f50'}},
        360: {'label': ">6hr", 'style': {'color': '#f50'}},
        },
        value=df3['callduration'].min(),
        #tooltip={"placement": "bottom", "always_visible": True},
        id='sv-slider'
    ),

    dcc.Graph(
    id='sv-graph',
    figure=figsv
    ),

    html.Div(children='''
        The histogram below represents the call duration for ALL calls for 2022 (top 10 skills including SunVault).
    '''),

    dcc.Slider(
        min=df4['callduration'].min(),
        max=df4['callduration'].max(),
        step=None,
        marks={
        0: {'label': 'all', 'style': {'color': '#77b0b1'}},
        60: {'label': '>1hr'},
        120: {'label': '>2hr'},
        180: {'label': '>3hr'},
        240: {'label': '>4hr'},
        300: {'label': ">5hr", 'style': {'color': '#f50'}},
        360: {'label': ">6hr", 'style': {'color': '#f50'}},
        },
        value=df4['callduration'].min(),
        #tooltip={"placement": "bottom", "always_visible": True},
        id='top10-slider'
    ),

    dcc.Graph(
    id='top10-graph',
    figure=figtop
    )

])

@app.callback(
    Output('graph-with-slider', 'figure'),
    Output('blocker-graph', 'figure'),
    Output('silence-graph', 'figure'),
    [Input('week-slider', 'value')])

def update_figure(selected_week):

    filtered_df = df1[df1.week == selected_week]
    fig = px.scatter(filtered_df, x="Number of silences", y="Call duration", size="Silence Max", color="Contact ID",
                     log_x=True, size_max=55)
    fig.update_layout(transition_duration=500)

    filtered_df2 = df2[df2.week == selected_week]
    fig1 = px.bar(filtered_df2, y="Silence duration (seconds)", x="Contact ID")
    fig1.update_layout(transition_duration=500)
    fig2 = px.bar(filtered_df2, y="Contact ID", x="Class", color="Subclass")
    fig2.update_layout(transition_duration=500)

    return fig, fig1, fig2

@app.callback(
    Output('sv-graph', 'figure'),
    [Input('sv-slider', 'value')])

def update_figure2(selected_duration):

    filtered_df3 = df3[df3.callduration >= selected_duration]
    fig3 = px.bar(filtered_df3, y="callduration", x="week")
    fig3.update_layout(transition_duration=500)
    return fig3

@app.callback(
    Output('top10-graph', 'figure'),
    [Input('top10-slider', 'value')])

def update_figure3(selected_duration):

    filtered_df4 = df4[df4.callduration >= selected_duration]
    fig4 = px.bar(filtered_df4, y="callduration", x="skillname", color="skillname")
    fig4.update_layout(transition_duration=500)
    return fig4

if __name__ == '__main__':
    app.run_server()
# %%
