import requests
import pandas as pd
from scipy.stats import mannwhitneyu

with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/air_polution_ukol.csv") as r:
  open("air_polution_ukol.csv", 'w', encoding="utf-8").write(r.text)

# 1. Načti dataset a převeď sloupec date (datum měření) na typ datetime.
data = pd.read_csv("air_polution_ukol.csv")
data['date'] = pd.to_datetime(data['date'])

# 2. Z dat vyber data za leden roku 2019 a 2020.
data = data.set_index(['date'])
x = data.loc['2019-01-01':'2019-01-31']["pm25"]
y = data.loc['2020-01-01':'2020-01-31']["pm25"]
# print(x)
# print(y)

# 3. Porovnej průměrné množství jemných částic ve vzduchu v těchto dvou měsících pomocí Mann–Whitney U testu.

# 3.1. Formuluj hypotézy pro oboustranný test (nulovou i alternativní) a napiš je do komentářů v programu.
# H0: Prumerne mnozstvi jemnych castic ve vzduchu bylo v obou mesicich stejne.
# H1: Prumerne mnozstvi jemnych castic ve vzduchu bylo v kazdem mesici jine.

# 3.2. Mann–Whitney U test
print(mannwhitneyu(x, y))

# 3.3. Rozhodni, zda bys na hladině významnosti 5 % zamítla nulovou hypotézu. Své rozhodnutí napiš do programu.
# ODPOVED: P-hodnota 1.17 % je nizsi nez hladina vyznamnosti a proto musime nulovou hypotezu zamitnout.



