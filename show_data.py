import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, DateTime, Integer

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

# Rysowanie wykresu
plt.figure(figsize=(14, 7))
plt.plot(dates, opens, label='Open')
plt.plot(dates, highs, label='High')
plt.plot(dates, lows, label='Low')
plt.plot(dates, closes, label='Close')

# Dodanie tytułu i etykiet osi
plt.title('BTC/USD Price Data')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)

# Formatowanie osi daty
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gcf().autofmt_xdate()

# Wyświetlenie wykresu
plt.show()
