
import dash
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from main import get_df


df_final = get_df()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
available_indicators = df_final['Indicator'].unique()
app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id = 'xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Infected (Total infections per day)'
            ),
            dcc.RadioItems(
                id = 'xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value = 'Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Infected (Total infections per day)'
            ),
        dcc.RadioItems(
                        id = 'yaxis-type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value = 'Linear',
                        labelStyle={'display': 'inline-block'}
                    )
        ],
        style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
    ]),

    dcc.Graph(id='indicator-graphic'),
    dcc.Slider(
        id='date-slider',
        min=df_final['date'].min(),
        max=df_final['date'].max(),
        value=df_final['date'].max(),
        marks={str(date): str(date) for date in df_final['date'].unique()},
        step=None
    )
])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-type', 'value'),
     Input('date-slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type, date_value):
    dff = df_final[df_final['date'] == date_value]

    return {
        'data': [dict(
            x=dff[dff['Indicator'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator'] == yaxis_column_name]['Country/Region'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
    )],
        'layout': dict(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'Log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'Log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)