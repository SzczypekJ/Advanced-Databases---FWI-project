import pandas as pd
from sqlalchemy import create_engine

# Ustawienia bazy danych
DATABASE_URI = 'sqlite:///intraday_data.db'
engine = create_engine(DATABASE_URI)

# Pobranie danych z bazy
query = "SELECT * FROM IBM_intraday"
df = pd.read_sql(query, engine)

# Wyświetlenie danych
print(df.head()) 
print(df)         
