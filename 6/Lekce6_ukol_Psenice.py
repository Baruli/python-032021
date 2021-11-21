'''
V souboru jsou data o délce zrn pšenice v milimetrech pro dvě odrůdy - Rosa a Canadian.
Proveď statistický test hypotézy o tom, zda se délka těchto dvou zrn liší.
K testu použij Mann–Whitney U test.
'''

import requests
from pandas import read_csv
from scipy.stats import mannwhitneyu, binom

with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/psenice.csv") as r:
  open("psenice.csv", 'w', encoding="utf-8").write(r.text)

data = read_csv("psenice.csv")

# (H0) Nulova hypoteza: Prumerne delky zrn jednotlivych odrud jsou stejne.
# (H1) Alternativni hypoteza: Prumerne delky zrn jednotlivych odrud jsou ruzne.

x = data["Rosa"]
y = data["Canadian"]

# Mann-Whitney U test
H0_test = mannwhitneyu(x, y)

# Urci p-hodnotu testu a porovnej ji s hladinou významnosti 5 %
print(f"Hodnota p-value je: {H0_test.pvalue}, tedy nizsi nez hladina vyznamnosti, proto nulovou hypotezu nezamitane. ")






