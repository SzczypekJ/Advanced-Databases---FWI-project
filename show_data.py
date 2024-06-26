# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Float, DateTime, Integer

# # Konfiguracja SQLAlchemy
# engine = create_engine('sqlite:///crypto_data.db', echo=True)
# Base = declarative_base()

# # Klasa dla tabeli BTC/USD


# class CryptoData_BTC_USD(Base):
#     __tablename__ = 'crypto_data_BTC_USD'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     datetime = Column(DateTime)
#     open = Column(Float)
#     high = Column(Float)
#     low = Column(Float)
#     close = Column(Float)


# # Tworzenie sesji
# Session = sessionmaker(bind=engine)
# session = Session()

# # Pobieranie wszystkich danych dla BTC/USD
# btc_data = session.query(CryptoData_BTC_USD).all()

# # Zamknięcie sesji
# session.close()

# # Przygotowanie danych do wykresu
# dates = [data.datetime for data in btc_data]
# opens = [data.open for data in btc_data]
# highs = [data.high for data in btc_data]
# lows = [data.low for data in btc_data]
# closes = [data.close for data in btc_data]

# # Rysowanie wykresu
# plt.figure(figsize=(14, 7))
# plt.plot(dates, opens, label='Open')
# plt.plot(dates, highs, label='High')
# plt.plot(dates, lows, label='Low')
# plt.plot(dates, closes, label='Close')

# # Dodanie tytułu i etykiet osi
# plt.title('BTC/USD Price Data')
# plt.xlabel('Date')
# plt.ylabel('Price (USD)')
# plt.legend()
# plt.grid(True)

# # Formatowanie osi daty
# plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
# plt.gcf().autofmt_xdate()

# # Wyświetlenie wykresu
# plt.show()

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, DateTime, Integer
from mplfinance.original_flavor import candlestick_ohlc

# Konfiguracja SQLAlchemy
engine = create_engine('sqlite:///crypto_data.db', echo=True)
Base = declarative_base()

# Klasa dla tabeli BTC/USD
class CryptoData_BTC_USD(Base):
    __tablename__ = 'crypto_data_BTC_USD'
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)

# Tworzenie sesji
Session = sessionmaker(bind=engine)
session = Session()

# Pobieranie wszystkich danych dla BTC/USD
btc_data = session.query(CryptoData_BTC_USD).all()

# Zamknięcie sesji
session.close()

# Przygotowanie danych do wykresu
dates = [data.datetime for data in btc_data]
opens = [data.open for data in btc_data]
highs = [data.high for data in btc_data]
lows = [data.low for data in btc_data]
closes = [data.close for data in btc_data]

# Konwersja dat na numeryczne wartości dla matplotlib
dates_num = mdates.date2num(dates)

# Tworzenie DataFrame
df = pd.DataFrame({
    'datetime': dates,
    'open': opens,
    'high': highs,
    'low': lows,
    'close': closes
})

# Obliczanie RSI
def compute_rsi(data, window=14):
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

df['RSI'] = compute_rsi(df)

# Tworzenie wykresów
fig, (ax1, ax2) = plt.subplots(2, figsize=(12, 10), gridspec_kw={'height_ratios': [2, 1]})

# Wykres świeczkowy
candlestick_ohlc(ax1, df[['datetime', 'open', 'high', 'low', 'close']].assign(datetime=mdates.date2num(df['datetime'])).values, width=0.6, colorup='g', colordown='r', alpha=0.8)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
ax1.set_title('BTC/USD Candlestick Chart')
ax1.set_ylabel('Price [USD]')

# Wykres RSI
ax2.plot(df['datetime'], df['RSI'], label='RSI')
ax2.axhline(70, color='r', linestyle='--', label='Overbought (70)')
ax2.axhline(30, color='g', linestyle='--', label='Oversold (30)')
ax2.set_title('BTC/USD Relative Strength Index (RSI)')
ax2.set_ylabel('RSI')
ax2.set_xlabel('Date')
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
ax2.legend()

plt.tight_layout()
plt.show()

