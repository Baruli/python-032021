'''
1. Použij zavírací cenu kryptoměny (sloupec Close) a vypočti procentuální změnu jednotlivých kryptoměn.
    Pozor na to, ať se ti nepočítají ceny mezi jednotlivými měnami.
2. Vytvoř korelační matici změn cen jednotlivých kryptoměn a zobraz je jako tabulku.
3. V tabulce vyber dvojici kryptoměn s vysokou hodnotou koeficientu korelace
    a jinou dvojici s koeficientem korelace blízko 0. Změny cen pro dvojice měn,
    které jsou nejvíce a nejméně korelované, si zobraz jako bodový graf.

Dobrovolny doplnek:
1. Vyzkoušej aplikovat Spearmenovu korelaci a porovnej, nakolik se liší výsledky.
2. Vyzkoušej si spočítat korelaci pro nějaké kratší časové období (například 1 měsíc)
     a pro dvě nejvíce a nejméně korelované hodnoty si zobraz vývoj zavíracích ceny v čase (jako liniový graf).
     Je možné korelaci vyčíst z tohoto grafu?
'''

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/crypto_prices.csv")
open("crypto_prices.csv", "wb").write(r.content)

krypto = pd.read_csv("crypto_prices.csv")

# PRIPRAVA DAT
#Vytvoreni prazdneho DataFramu obsahujici 1 sloupec:  distinct "Date":
dates = pd.DataFrame(sorted(set(krypto["Date"]), reverse=True))
dates.columns = ["Date"]

# Groupby DataFramu podle jmen jednotlivych kryptomen:
krypto_grouped = krypto[["Name", "Date", "Close"]].groupby(["Name"])

# Postupne najoinovani zaviracich cen jednotlivych kryptomen do stejneho DataFramu -> siroky format:
for group_title, group in krypto_grouped:
    group.rename(columns={"Close": group_title}, inplace=True)
    group.drop(["Name"], axis=1, inplace=True)
    dates = pd.merge(dates, group, how="outer", on=["Date"])
# print(dates)

# 1. Použij zavírací cenu kryptoměny (sloupec Close) a vypočti procentuální změnu jednotlivých kryptoměn.
krypto_perc_change = dates.set_index("Date").pct_change()
print(krypto_perc_change)

# 2. Vytvoř korelační matici změn cen jednotlivých kryptoměn a zobraz je jako tabulku.
# print(krypto_perc_change.corr().to_string())

# 3. V tabulce vyber dvojici kryptoměn s vysokou hodnotou koeficientu korelace
# a jinou dvojici s koeficientem korelace blízko 0. Změny cen pro tyto dvojice měn si zobraz jako bodový graf.

# 3.1. Nejvice korelovana krypta: Litecoin a Bitcoin
most_correlated_df = krypto_perc_change[["Litecoin", "Bitcoin"]].dropna(how="any", axis="rows")
# Zobrazeni jejich cenovych zmen jako bodovy graf:
sns.jointplot("Litecoin", "Bitcoin", most_correlated_df, kind="scatter", color="seagreen")

# 3.2. Nejmene korelovana krypta: Tether a Polkadot
# Pouziju puvodni DataFrame "dates", aby se mi zobrazili nulove hodnoty, kterych se zbavim
least_correlated_df = dates[["Date", "Tether", "Polkadot"]].dropna(how="any", axis="rows")
# Vypocitam si procentualni zmenu jejich zaviracich hodnot
least_correlated_df = least_correlated_df.set_index("Date").pct_change().dropna(how="any", axis="rows")

# Zobrazim si zmeny cen jako bodovy graf:
sns.jointplot("Tether", "Polkadot", least_correlated_df, kind="scatter", color="blue")
# plt.show()


# # DOPLNEK: 1. Vyzkoušej aplikovat Spearmenovu korelaci a porovnej, nakolik se liší výsledky.
print(f"Pearsonuv korelacni koeficient:\n {most_correlated_df.corr()}\n")
print(f"Spearmanuv korelacni koeficient:\n {most_correlated_df.corr(method='spearman')}\n")

print(f"Pearsonuv korelacni koeficient:\n {least_correlated_df.corr()}\n")
print(f"Spearmanuv korelacni koeficient:\n {least_correlated_df.corr(method='spearman')}\n")


# DOPLNEK: 2. Vyzkoušej si spočítat korelaci pro kratší časové období (např. 1 měsíc)
#  a pro dvě nejvíce a nejméně korelované hodnoty si zobraz vývoj zavíracích ceny v čase (jako liniový graf).
#  Je možné korelaci vyčíst z tohoto grafu?

krypto_30d = krypto_perc_change.head(30).corr()
print(krypto_30d.to_string())

# Nejvic korelovane: Litecoin a EOS
most_correlated_30d = dates[["Date", "Litecoin", "EOS"]].dropna(how="any", axis="rows")
most_correlated_30d.plot(legend=True)

# Nejmin korelovane: Cosmos a Tether
least_correlated_30d = dates[["Date", "Cosmos", "Tether"]].dropna(how="any", axis="rows")
least_correlated_30d.plot(legend=True)

# plt.show()

'''
Ja z tech grafu korelaci vycist neumim, vzhledem k tomu, ze je mezi jejich hodnotami velky rozdil. 
Asi by bylo potreba zvolit jine meritko? 
Navic Tether vypada, ze jeho hodnota je konstantni, takze by bylo fajn podivat se, co je to za menu.

'''




