"""
V souboru london_merged.csv najdeš informace o počtu vypůjčení jízdních kol v Londýně.

1. Vytvoř sloupec, do kterého z časové značky (sloupec timestamp) ulož rok.
2. Vytvoř kontingenční tabulku, která porovná kód počasí (sloupec weather_code se sloupcem udávající rok.
3. Rozsireni: Jako hodnoty v kontingenční tabulce zobraz relativní počty jízd pro jednotlivé kódy počasí v jednom roce.
"""

import requests
import pandas as pd
pd.options.display.max_columns = None


r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/london_merged.csv")
with open("london_merged.csv", 'w', encoding='utf8') as file:
    file.write(r.text)
london = pd.read_csv('london_merged.csv')


# CHECK DATA
# print('\n',london.head())
# print('\n',london.info())


# 1. CREATE NEW COLUMN 'year' FROM 'timestamp'
london['timestamp'] = pd.to_datetime(london['timestamp'])
london['year'] = london['timestamp'].dt.year


# 2. PIVOT TABLE TO SHOW NUMBER OF RENTED BIKES BY YEAR AND WEATHER CONDITION
# Add new column with weather description to make the result more human user friendly :)
weather_dict_abbr = {
                1: 'Clear',
                2: 'Scattered clouds',
                3: 'Broken clouds',
                4: 'Cloudy',
                7: 'Rain',
                10: 'Rain with thunderstorm',
                26: 'Snowfall',
                94: 'Freezing Fog'
                }
london['weather'] = london['weather_code'].map(weather_dict_abbr)

london_pivot= pd.pivot_table(london, index='weather', columns='year', values='timestamp', aggfunc=len, margins=True)
print('\n', london_pivot)


# 3. SHOW PERCENTAGE OF RENTED BIKES FOR EACH YEAR BASED ON THE WEATHER CONDITION
london_pivot_percentage = round(london_pivot.div(london_pivot.iloc[-1, :], axis=1),4)
print('\n', london_pivot_percentage)
