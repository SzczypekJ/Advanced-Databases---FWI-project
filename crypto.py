import requests
from datetime import datetime, timedelta
from time import sleep
from sqlalchemy import create_engine, Column, Float, DateTime, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.inspection import inspect
import schedule
import threading
import pandas as pd

# Wprowadź swój klucz API
api_key = '872ef91dcfc84f95aa34e7c92cd12e3c'

# Lista kryptowalut
symbols = ['BTC/USD', 'ETH/USD', 'LTC/USD', 'XRP/USD', 'BCH/USD',
           'ADA/USD', 'DOT/USD', 'BNB/USD', 'LINK/USD', 'DOGE/USD']

# Konfiguracja SQLAlchemy
engine = create_engine('sqlite:///crypto_data.db', echo=True)
Base = declarative_base()

# Szablon do tworzenia dynamicznych klas tabel


class CryptoDataTemplate(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    rsi = Column(Float)

# Funkcja do tworzenia dynamicznych klas tabel


def create_crypto_table(symbol):
    class CryptoData(CryptoDataTemplate):
        __tablename__ = f'crypto_data_{symbol.replace("/", "_")}'
    CryptoData.__name__ = f'CryptoData_{symbol.replace(
        "/", "_")}'  # Nadanie unikalnej nazwy klasie
    return CryptoData


# Tworzenie tabel w bazie danych, jeśli nie istnieją
tables = {}
inspector = inspect(engine)
for symbol in symbols:
    table_class = create_crypto_table(symbol)
    tables[symbol] = table_class
    # Sprawdzanie, czy tabela już istnieje
    if not inspector.has_table(table_class.__tablename__):
        Base.metadata.create_all(engine, tables=[table_class.__table__])

# Tworzenie sesji
Session = sessionmaker(bind=engine)

# Funkcja do obliczania RSI


def compute_rsi(data, window=14):
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def fetch_and_store_data():
    # Pobieranie danych i zapisywanie do odpowiednich tabel
    now = datetime.now()
    start_date = (now - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
    end_date = now.strftime('%Y-%m-%d %H:%M:%S')

    for symbol in symbols:
        url = f'https://api.twelvedata.com/time_series?apikey={api_key}&interval=1h&symbol={
            symbol}&format=JSON&start_date={start_date}&end_date={end_date}&timezone=Europe/Warsaw'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'values' in data:
                session = Session()
                added_entries = 0
                try:
                    for entry in data['values']:
                        entry_time = datetime.strptime(
                            entry['datetime'], '%Y-%m-%d %H:%M:%S')

                        # Sprawdź, czy rekord już istnieje w bazie danych
                        existing_entry = session.query(tables[symbol]).filter_by(
                            datetime=entry_time).first()
                        if existing_entry:
                            print(f"Data for {symbol} at {
                                  entry_time} already exists in the database.")
                            continue

                        data_entry = tables[symbol](
                            datetime=entry_time,
                            open=float(entry['open']),
                            high=float(entry['high']),
                            low=float(entry['low']),
                            close=float(entry['close'])
                        )
                        session.add(data_entry)
                        added_entries += 1
                        print(f"Adding data for {symbol} at {
                              entry_time} to the database.")

                    if added_entries > 0:
                        session.commit()
                        print(f"Data for {symbol} committed to database.")

                        # Aktualizacja RSI po dodaniu nowych danych
                        crypto_data = session.query(tables[symbol]).order_by(
                            tables[symbol].datetime).all()
                        data = {
                            'datetime': [data.datetime for data in crypto_data],
                            'open': [data.open for data in crypto_data],
                            'high': [data.high for data in crypto_data],
                            'low': [data.low for data in crypto_data],
                            'close': [data.close for data in crypto_data],
                        }
                        df = pd.DataFrame(data)
                        df['rsi'] = compute_rsi(df)

                        for i, row in df.iterrows():
                            matching_record = session.query(tables[symbol]).filter_by(
                                datetime=row['datetime']).first()
                            if matching_record:
                                matching_record.rsi = row['rsi']

                        session.commit()
                        print(f"RSI for {symbol} updated in the database.")

                    else:
                        print(f"No new data for {
                              symbol} to commit to the database.")
                except Exception as e:
                    print(f"Failed to commit data for {symbol}: {e}")
                    session.rollback()
                finally:
                    session.close()
            else:
                print(f'No data available for {symbol}: {
                      data.get("message", "Unknown error")}')
        else:
            print(f'Error fetching data for {symbol}: {response.status_code}')
        sleep(10)  # Opóźnienie, aby nie przekroczyć limitu API

# Funkcja uruchamiająca harmonogram w oddzielnym wątku


def run_schedule():
    while True:
        schedule.run_pending()
        sleep(60)


# Harmonogram wykonywania funkcji co godzinę, 5 minut po pełnej godzinie
schedule.every().hour.at(":05").do(fetch_and_store_data)

# Uruchomienie harmonogramu w oddzielnym wątku
schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.start()
