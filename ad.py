import requests
import pandas as pd
from sqlalchemy import create_engine

API_KEY = 'J6L1VIWTIAK6IGPU'  
SYMBOL = 'IBM'
INTERVAL = '60min'


DATABASE_URI = 'sqlite:///intraday_data.db'
engine = create_engine(DATABASE_URI)

def fetch_data():
    URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={SYMBOL}&interval={INTERVAL}&apikey={API_KEY}&datatype=json'
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        time_series_key = f'Time Series ({INTERVAL})'
        time_series = data[time_series_key]
        df = pd.DataFrame.from_dict(time_series, orient='index')
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'Date'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])
        df.to_sql(f'{SYMBOL}_intraday', engine, if_exists='append', index=False)
        print(f'Data successfully saved to database')
    else:
        print('Failed to retrieve data')

if __name__ == "__main__":
    fetch_data()
