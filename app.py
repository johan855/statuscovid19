
import dash
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from main import get_df


df_final = get_df()

avaliable_indicators = df_final['Country/Region'].unique()

country = 'Argentina'
df_final = df_final.loc[country]
fig = go.Figure(go.Scatter(x = df_final.index, y = df_final['Value'],
                  name=country))
fig.update_layout(title='Contagions over time (2020)',
                   plot_bgcolor='rgb(230, 230,230)',
                   showlegend=True)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('COVID-19'),
    html.Div([
        html.Div('''Number of contagions over time.'''),
        dcc.Dropdown(
            id = 'xaxis-column',
            options = [{'label': i, 'value': i} for i in avaliable_indicators],
            value = 'Colombia'
        ),
        dcc.RadioItems(
            id = 'xaxis-type',
            options = [{'label': i, 'value': i} for i in ['Linear','Log']],
            value = 'Linear',
            labelStyle = {'display': 'inline-block'}
        )
    ], style = {'width': '48%', 'display': 'inline-block'}),
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

@app.callback(
    Output('example-graph', 'fig'),
    [Input('xaxis-column', 'value'),
     Input('xaxis-type', 'value')]
)
def update_graph(xaxis_column_name, xaxis_type, ):
    dff = df_final[df_final['Country/Region'] == country]
    return {
        'data': [dict(
            x=dff[dff['Country/Region'] == xaxis_column_name]['Value'],
        )]
    }

if __name__ == '__main__':
    app.run_server(debug=True)