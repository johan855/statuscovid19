import requests
import pandas as pd
import plotly.graph_objects as go

#Read file
df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/'
                'csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
#Organize dataframe
df_clean = df.drop('Lat',axis=1)
df_clean = df_clean.drop('Long',axis=1)
df_clean = df_clean.melt(id_vars=['Province/State','Country/Region'], var_name='Date',value_name='Value')
df_clean = df_clean.groupby(['Country/Region','Date']).sum()

#Select country
country='Colombia'
df_final = df_clean.loc[country]

fig = go.Figure(go.Scatter(x = df_final.index, y = df_final['Value'],
                  name='Contagions'))
fig.update_layout(title='Contagions over time (2020)',
                   plot_bgcolor='rgb(230, 230,230)',
                   showlegend=True)
fig.show()