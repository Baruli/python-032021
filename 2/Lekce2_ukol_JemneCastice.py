'''
Zadani ukolu:
1. Načti dataset a převeď sloupec date (datum měření) na typ datetime.
2. Přidej sloupce s rokem a číslem měsíce, které získáš z data měření.
3. Vytvoř pivot tabulku s průměrným počtem množství jemných částic (sloupec pm25)
    v jednotlivých měsících a jednotlivých letech.

Dobrovolný doplněk:
4. Zobrat výsledek analýzy jako teplotní mapu.
5. Použij metodu dt.dayofweek a přidej si do sloupce den v týdnu.
    Porovnej, jestli se průměrné množství jemných částic liší ve všední dny a o víkendu.

'''

import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from seaborn import heatmap

with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/air_polution_ukol.csv") as r:
  open("air_polution_ukol.csv", 'w', encoding="utf-8").write(r.text)

# 1. Načti dataset a převeď sloupec date (datum měření) na typ datetime.
data = pd.read_csv("air_polution_ukol.csv")
data['date'] = pd.to_datetime(data['date'])

# 2. Přidej sloupce s rokem a číslem měsíce, které získáš z data měření.
data['year'] = data['date'].dt.year
data['month'] = data['date'].dt.month
# print(data.head(10).to_string())

# 3. Vytvoř pivot tabulku s průměrným počtem množství jemných částic v jednotlivých měsících a jednotlivých letech.
data_pivot = pd.pivot_table(data, values='pm25',
                            index='year', columns='month',
                            aggfunc=np.mean)
print(data_pivot.to_string(), '\n')

# 4. Zobraz výsledek analýzy jako teplotní mapu.
heatmap(data_pivot, annot=True, fmt='.1f')
plt.show()


# 5. Porovnej, jestli se průměrné množství jemných částic liší ve všední dny a o víkendu.
# Pridani sloupce: den v tydnu
data['dayOfWeek'] = data['date'].dt.dayofweek
# Pridani dalsiho sloupce: vsedni den nebo vikend
data['is_weekend'] = np.where(data['dayOfWeek'] < 5, 0, 1)
# Vypocet prumernych hodnot po jednotlivych mesicich -->  2 nove sloupce: prumer vsedni dny a prumer vikendy
data_grouped = data.groupby(['year', 'month'])['pm25'].mean()
data_grouped = pd.DataFrame(data_grouped).rename(columns={'pm25':'avg_pm25'})
data_grouped['avg_weekdays'] = data[data['is_weekend'] == 0].groupby(['year', 'month'])['pm25'].mean()
data_grouped['avg_weekend'] = data[data['is_weekend'] == 1].groupby(['year', 'month'])['pm25'].mean()
data_grouped = data_grouped.dropna()
data_grouped = data_grouped.reset_index()

# Rozdil predchozich 2 sloupcu: Prumer ve vsednich dnech minus prumer o vikendech po mesicich
data_grouped['diff'] = data_grouped['avg_weekdays'] - data_grouped['avg_weekend']
data_grouped['diff_text'] = np.where(data_grouped['diff'] > 0,
                                     'Pocet tydnu, ve kterych byl prumer o vikendech nizsi',
                                     'Pocet tydnu, ve kterych byl prumer o vikendech vyssi')
# print(data_grouped.head().to_string())
print(f"\nVysledek hodnot jemnych castic v ovzdusi za obdobi 1/2014 - 9/2021:\n{data_grouped['diff_text'].value_counts()}")
