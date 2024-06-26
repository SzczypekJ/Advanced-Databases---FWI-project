import requests
from datetime import datetime
from sqlalchemy import create_engine, Column, Float, DateTime, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.inspection import inspect
import time

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

# Funkcja do zapisywania danych do bazy danych


def save_data_to_db(data, symbol):
    session = Session()
    added_entries = 0
    try:
        for entry in data:
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
            print(f"Adding data for {symbol} at {entry_time} to the database.")

        if added_entries > 0:
            session.commit()
            print(f"Data for {symbol} committed to database.")
        else:
            print(f"No new data for {symbol} to commit to the database.")
    except Exception as e:
        print(f"Failed to commit data for {symbol}: {e}")
        session.rollback()
    finally:
        session.close()

# Pobierz dane z API dla wszystkich symboli


def fetch_data(symbol):
    now = datetime.now()
    end_date = now.strftime('%Y-%m-%d %H:%M:%S')
    url = f"https://api.twelvedata.com/time_series?apikey={api_key}&interval=1h&symbol={
        symbol}&format=JSON&start_date=2024-06-01 00:00:00&end_date={end_date}&timezone=Europe/Warsaw"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'values' in data:
            return data['values']
        else:
            print(f"No data available for {symbol}: {
                  data.get('message', 'Unknown error')}")
            return []
    else:
        print(f"Error fetching data for {symbol}: {response.status_code}")
        return []


# Pobierz i zapisz dane dla wszystkich symboli
for symbol in symbols:
    data = fetch_data(symbol)
    if data:
        save_data_to_db(data, symbol)
    time.sleep(10)  # Opóźnienie 10 sekund pomiędzy zapytaniami
