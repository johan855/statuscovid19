import pandas as pd
import plotly.graph_objects as go


def get_df():
    #Read file
    df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/'
                    'csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    #Organize dataframe
    df_clean = df.drop('Lat',axis=1)
    df_clean = df_clean.drop('Long',axis=1)
    df_clean = df_clean.melt(id_vars=['Province/State','Country/Region'], var_name='Date',value_name='Value')
    #Fix dates and group
    df_clean['date'] = pd.to_datetime(df_clean['Date'])
    df_final = df_clean.groupby(['Country/Region','date']).sum()
    return df_final