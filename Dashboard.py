# %%Dash v2
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
app = Dash(__name__)

df1 = pd.read_csv(r'C:/Users/dsadykhanov/OneDrive - Sunpower Corporation\Documents/Icebreaker/Icebreaker/Icebreaker_stats_final.csv')
#fig = px.box(df, y="totalDurationMinutes", x="day")

app.layout = html.Div(children=[
    html.H1(children='Icebreaker Dashboard'),

    html.Div(children='''
        Visualizing data from our calls
    '''),

    dcc.Graph(id='graph-with-slider'),

    dcc.Slider(
        df1['week'].min(),
        df1['week'].max(),
        step=None,
        value=df1['week'].min(),
        marks={str(week): str(week) for week in df1['week'].unique()},
        id='week-slider'
    )
])

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('week-slider', 'value'))
def update_figure(selected_week):
    filtered_df = df1[df1.week == selected_week]

    fig = px.scatter(filtered_df, x="silencecount", y="callduration",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server()
# %%
