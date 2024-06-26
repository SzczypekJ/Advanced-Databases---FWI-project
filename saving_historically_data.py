import pandas as pd
from sqlalchemy import create_engine, Column, Float, DateTime, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

# Konfiguracja SQLAlchemy
engine = create_engine('sqlite:///crypto_data.db', echo=True)
Base = declarative_base()

# Klasa bazowa dla tabeli kryptowalut


class CryptoData(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    rsi = Column(Float)

# Klasy dla poszczególnych kryptowalut


class CryptoData_BTC_USD(CryptoData):
    __tablename__ = 'crypto_data_BTC_USD'


class CryptoData_ETH_USD(CryptoData):
    __tablename__ = 'crypto_data_ETH_USD'


class CryptoData_LTC_USD(CryptoData):
    __tablename__ = 'crypto_data_LTC_USD'


class CryptoData_XRP_USD(CryptoData):
    __tablename__ = 'crypto_data_XRP_USD'


class CryptoData_BCH_USD(CryptoData):
    __tablename__ = 'crypto_data_BCH_USD'


class CryptoData_ADA_USD(CryptoData):
    __tablename__ = 'crypto_data_ADA_USD'


class CryptoData_DOT_USD(CryptoData):
    __tablename__ = 'crypto_data_DOT_USD'


class CryptoData_BNB_USD(CryptoData):
    __tablename__ = 'crypto_data_BNB_USD'


class CryptoData_LINK_USD(CryptoData):
    __tablename__ = 'crypto_data_LINK_USD'


class CryptoData_DOGE_USD(CryptoData):
    __tablename__ = 'crypto_data_DOGE_USD'


# Tworzenie tabel
Base.metadata.create_all(engine)

# Funkcja do obliczania RSI


def compute_rsi(data, window=14):
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


# Lista kryptowalut
symbols = ['BTC/USD', 'ETH/USD', 'LTC/USD', 'XRP/USD', 'BCH/USD',
           'ADA/USD', 'DOT/USD', 'BNB/USD', 'LINK/USD', 'DOGE/USD']

# Mapa symboli do klas
symbol_to_class = {
    'BTC_USD': CryptoData_BTC_USD,
    'ETH_USD': CryptoData_ETH_USD,
    'LTC_USD': CryptoData_LTC_USD,
    'XRP_USD': CryptoData_XRP_USD,
    'BCH_USD': CryptoData_BCH_USD,
    'ADA_USD': CryptoData_ADA_USD,
    'DOT_USD': CryptoData_DOT_USD,
    'BNB_USD': CryptoData_BNB_USD,
    'LINK_USD': CryptoData_LINK_USD,
    'DOGE_USD': CryptoData_DOGE_USD,
}

# Tworzenie sesji
Session = sessionmaker(bind=engine)
session = Session()

# Przetwarzanie każdej kryptowaluty
for symbol in symbols:
    # Pobieranie danych
    crypto_class = symbol_to_class[symbol.replace('/', '_')]
    crypto_data = session.query(crypto_class).order_by(
        crypto_class.datetime).all()

    # Przygotowanie danych do DataFrame
    data = {
        'datetime': [data.datetime for data in crypto_data],
        'open': [data.open for data in crypto_data],
        'high': [data.high for data in crypto_data],
        'low': [data.low for data in crypto_data],
        'close': [data.close for data in crypto_data],
    }
    df = pd.DataFrame(data)

    # Sortowanie danych po czasie
    df = df.sort_values(by='datetime').reset_index(drop=True)

    # Obliczanie RSI
    df['rsi'] = compute_rsi(df)

    # Wpisywanie 0 dla pierwszych wartości, gdzie nie ma wystarczających danych
    df['rsi'].fillna(0, inplace=True)

    # Aktualizacja wartości RSI w bazie danych tylko dla pełnych okresów
    for i, row in df.iterrows():
        matching_record = session.query(crypto_class).filter_by(
            datetime=row['datetime']).first()
        if matching_record:
            matching_record.rsi = row['rsi']

    session.commit()

session.close()
