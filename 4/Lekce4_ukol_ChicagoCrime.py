'''
Tabulka crime v naší databázi obsahuje informace o kriminalitě v Chicagu.

1. Pomocí SQL dotazu si připrav tabulku o krádeži motorových vozidel
    (sloupec PRIMARY_DESCRIPTION by měl mít hodnotu "MOTOR VEHICLE THEFT").
2. Tabulku dále pomocí pandasu vyfiltruj tak, aby obsahovala jen informace o krádeži aut
    (hodnota "AUTOMOBILE" ve sloupci SECONDARY_DESCRIPTION).
3. Ve kterém měsíci dochází nejčastěji ke krádeži auta?
'''

from sqlalchemy import create_engine, inspect
import pandas as pd

HOST = "czechitaspsql.postgres.database.azure.com"
PORT = 5432
USER = "barbora3ulicna"
USERNAME = f"{USER}@czechitaspsql"
DATABASE = "postgres"
PASSWORD = "bsc2mqTzVamDNxw2"

engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}", echo=False)

# Kontrola tabulky "crime":
# crime = pd.read_sql("SELECT * FROM crime LIMIT 5", con=engine)
# print(crime.to_string())

# Stazeni potrebneho datasetu do pandas
crime = pd.read_sql('''SELECT \"DATE_OF_OCCURRENCE\", \"SECONDARY_DESCRIPTION\"
                       FROM crime
                       WHERE \"PRIMARY_DESCRIPTION\" = 'MOTOR VEHICLE THEFT'
                       ''', con=engine)

# Vytvoreni sloupcu mesic a rok
crime["DATE_OF_OCCURRENCE"] = pd.to_datetime(crime["DATE_OF_OCCURRENCE"])
crime["year"] = crime["DATE_OF_OCCURRENCE"].dt.year
crime["month"] = crime["DATE_OF_OCCURRENCE"].dt.month

# Vyfiltrovani pouze kradezi aut
crime = crime[crime["SECONDARY_DESCRIPTION"] == "AUTOMOBILE"].reset_index(drop=True)

# Vypocet kradezi aut v jednotlivych mesicich
crimes_by_months = crime["month"].value_counts()
# print(crimes_by_months)

# Kontrola spravnosti vysledku:
# print(crime[crime["month"]==1].reset_index(drop=True).count())

print(f"Ke kradezim aut dochazi v Chicagu nejcasteji v {crimes_by_months.index[0]}. mesici.")