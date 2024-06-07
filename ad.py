import requests
import pandas as pd
import time
from sqlalchemy import create_engine, MetaData, Table, select
from datetime import datetime, timedelta

API_KEY = 'J6L1VIWTIAK6IGPU'
INTERVAL = '60min'

companies = [
    'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'CSCO', 'IBM', 'JNJ', 'JPM', 'V', 'PG',
    'UNH', 'NVDA', 'HD', 'MA', 'BAC', 'DIS', 'INTC', 'VZ', 'PFE', 'KO'
]

DATABASE_URI = 'sqlite:///intraday_data.db'
engine = create_engine(DATABASE_URI)


def fetch_data(symbol):
    URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={
        symbol}&interval={INTERVAL}&apikey={API_KEY}&datatype=json'
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        time_series_key = f'Time Series ({INTERVAL})'
        if time_series_key in data:
            time_series = data[time_series_key]
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df.reset_index(inplace=True)
            df.rename(columns={'index': 'Date'}, inplace=True)
            df['Date'] = pd.to_datetime(df['Date'])

            # Get the previous hour's data
            current_hour = datetime.now().replace(minute=0, second=0, microsecond=0)
            previous_hour = current_hour - timedelta(hours=1)
            latest_data = df[df['Date'] == previous_hour]

            if not latest_data.empty:
                table_name = symbol.replace('.', '_') + '_intraday'
                latest_data.to_sql(table_name, engine,
                                   if_exists='replace', index=False)
                print(f'Latest data for {
                      symbol} successfully saved to database')
            else:
                print(f'No latest data available for {
                      symbol} at {previous_hour}')
        else:
            print(f'Failed to retrieve data for {
                  symbol}: No time series key found in response')
    else:
        print(f'Failed to retrieve data for {
              symbol}: HTTP {response.status_code}')


if __name__ == "__main__":
    for company in companies:
        fetch_data(company)
        time.sleep(12)  # Sleep to handle rate limits (5 requests per minute)
