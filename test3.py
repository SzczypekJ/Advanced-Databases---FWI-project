import websocket
import json
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, String, Float, DateTime
from sqlalchemy.exc import OperationalError
from sqlalchemy.schema import CreateTable
from sqlalchemy import inspect
from datetime import datetime, timedelta
import threading
import time

API_KEY = 'cphfl9hr01qp5iv5en2gcphfl9hr01qp5iv5en30'
companies = [
    'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'CSCO', 'IBM', 'JNJ', 'JPM', 'V', 'PG',
    'UNH', 'NVDA', 'HD', 'MA', 'BAC', 'DIS', 'INTC', 'VZ', 'PFE', 'KO'
]

DATABASE_URI = 'sqlite:///intraday_data.db'
engine = create_engine(DATABASE_URI)
metadata = MetaData()
last_saved_time = {}

def create_table(symbol):
    table_name = symbol.replace('.', '_') + '_intraday'
    inspector = inspect(engine)
    if not inspector.has_table(table_name):
        table = Table(
            table_name, metadata,
            Column('Date', DateTime, primary_key=True),
            Column('Close', Float)
        )
        metadata.create_all(engine)
        print(f'Table {table_name} created')
    else:
        print(f'Table {table_name} already exists')

def upsert_data(symbol, date, close):
    table_name = symbol.replace('.', '_') + '_intraday'
    with engine.connect() as conn:
        conn.execute(f'''
            INSERT INTO "{table_name}" (Date, Close)
            VALUES (?, ?)
            ON CONFLICT(Date) DO UPDATE SET
                Close = excluded.Close
        ''', (date, close))

def on_message(ws, message):
    data = json.loads(message)
    if 'data' in data:
        for entry in data['data']:
            symbol = entry['s']
            current_time = datetime.fromtimestamp(entry['t'] / 1000.0)
            if symbol not in last_saved_time or current_time - last_saved_time[symbol] >= timedelta(hours=1):
                create_table(symbol)
                close = entry['p']
                upsert_data(symbol, current_time, close)
                last_saved_time[symbol] = current_time
                print(f'Latest data for {symbol} saved to database at {current_time}')

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for company in companies:
            ws.send(json.dumps({'type': 'subscribe', 'symbol': company}))
        while True:
            time.sleep(1)
    threading.Thread(target=run).start()

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(f"wss://ws.finnhub.io?token={API_KEY}",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
