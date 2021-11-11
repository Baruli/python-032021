'''
Z datového souboru si vyber jednu kryptoměnu a urči průměrné denní tempo růstu měny za sledované období.
Můžeš využít funkci geometric_mean z modulu statistics.
Vyber si sloupec se změnou ceny, kterou máš vypočítanou z předchozího cvičení (případně si jej dopočti),
přičti k němu 1 (nemusíš dělit stem jako v lekci, hodnoty jsou jako desetinná čísla, nikoli jako procenta)
a převeď jej na seznam pomocí metody .tolist().
Následně vypočti geometrický průměr z těchto hodnot.

'''

import requests
import pandas as pd
from scipy.stats import gmean
import matplotlib.pyplot as plt
import seaborn as sns

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/crypto_prices.csv")
open("crypto_prices.csv", "wb").write(r.content)

krypto = pd.read_csv("crypto_prices.csv")

krypto["Date"] = pd.to_datetime(krypto["Date"])

# Z datového souboru si vyber jednu kryptoměnu:
btc_df = krypto[krypto["Name"] == "Bitcoin"]
btc_df = btc_df[["Name", "Date", "Close"]].reset_index(drop=True)

# Dopocti sloupec se zmenou ceny:
btc_df["Perc_change"] = btc_df["Close"].pct_change()
btc_df = btc_df.dropna()

# Přičti k němu 1 a převeď jej na seznam pomocí metody .tolist():
btc_perc_change = (btc_df["Perc_change"]+1).tolist()
# print(btc_perc_change)

# Pro nasledujici vypocet geometrickeho prumeru pouziju funkci gmeal z modulu scipy.stats,
# protoze geometric_mean() je soucasti medulu statistics az od verze Python 3.8. a ja pouzivam Python 3.7.
geometricky_prumer_btc = gmean(btc_perc_change)-1
print(f"\nPrůměrné denní tempo růstu Bitcoinu: {geometricky_prumer_btc}")






