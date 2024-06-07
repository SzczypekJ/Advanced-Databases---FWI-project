import requests
import pandas as pd
import time
from sqlalchemy import create_engine

API_KEY = 'J6L1VIWTIAK6IGPU'
INTERVAL = '60min'

companies = [
    'AAPL'
]

DATABASE_URI = 'sqlite:///intraday_data.db'
engine = create_engine(DATABASE_URI)


def fetch_data(symbol):
    URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={
        symbol}&interval={INTERVAL}&apikey={API_KEY}&datatype=json'
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        # Print the entire response for debugging
        print(f'API response for {symbol}: {data}')
        time_series_key = f'Time Series ({INTERVAL})'
        if time_series_key in data:
            time_series = data[time_series_key]
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df.reset_index(inplace=True)
            df.rename(columns={'index': 'Date'}, inplace=True)
            df['Date'] = pd.to_datetime(df['Date'])
            # Handle symbols like BRK.B
            table_name = symbol.replace('.', '_') + '_intraday'
            df.to_sql(table_name, engine, if_exists='append', index=False)
            print(f'Data for {symbol} successfully saved to database')
        else:
            error_message = data.get(
                "Note", "No time series key found in response")
            print(f'Failed to retrieve data for {symbol}: {error_message}')
    else:
        print(f'Failed to retrieve data for {
              symbol}: HTTP {response.status_code}')


if __name__ == "__main__":
    for company in companies:
        fetch_data(company)
        time.sleep(12)  # Sleep to handle rate limits (5 requests per minute)
