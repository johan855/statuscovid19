import pandas as pd
import plotly.graph_objects as go

class covid_data():
    def __init__(self, data):
        self.df = data
        self.columns = data.keys()
        self.df_clean = self.df.drop('Lat', axis=1)
        self.df_clean = self.df_clean.drop('Long', axis=1)
        self.df_clean = self.df_clean.melt(id_vars=['Province/State', 'Country/Region', 'Indicator'], var_name='Date', value_name='Value')
        # Fix dates and group
        self.df_clean['date'] = pd.to_datetime(self.df_clean['Date']).dt.dayofyear
        self.df_clean['year'] = pd.to_datetime(self.df_clean['Date']).dt.year


def get_df():
    #Read file
    df_infected = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/'
                            'csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    df_infected['Indicator'] = 'infected'
    df_infected_clean = covid_data(df_infected)
    df_deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/'
                            'csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    df_deaths['Indicator'] = 'deaths'
    df_deaths_clean = covid_data(df_deaths)
    df_recoveries = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/'
                                'csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    df_recoveries['Indicator'] = 'recoveries'
    df_recoveries_clean = covid_data(df_recoveries)
    #Organize dataframe
    df_list = [df_infected_clean, df_deaths_clean, df_recoveries_clean]
    df_final = pd.DataFrame(columns=df_infected_clean.df_clean.keys())
    for df in df_list:
        df_final = df_final.append(df.df_clean)
    return df_final


if __name__== '__main__':
    get_df()
