
import requests
import pandas as pd
import statsmodels.formula.api as smf


r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/Concrete_Data_Yeh.csv")
with open("Concrete_Data_Yeh.csv", "wb") as f:
  f.write(r.content)

# V souboru Concrete_Data_Yeh.csv najdeš informace o kvalitě cementu.
# Sloupce 1-7 udávají množství jednotlivých složek v kg, které byly přimíchány do krychlového metru betonu
# (např. cement, voda, kamenivo, písek atd.).
# Ve sloupci 8 je stáří betonu a ve sloupci 9 kompresní síla betonu v megapascalech.
df = pd.read_csv("Concrete_Data_Yeh.csv")


# 1. Vytvoř regresní model,
# který bude predikovat kompresní sílu betonu na základě všech množství jednotlivých složek a jeho stáří.
slozky = df.columns[0:-1]
formula = ('csMPa ~ ' + ' + '.join(slozky))

mod = smf.ols(formula=formula, data=df)
res = mod.fit()


# 2. Zhodnoť kvalitu modelu.
rsquared = res.rsquared_adj   # Koeficient determinace naseho modelu
print(f"Koeficient determinace naseho modelu je {rsquared}, coz znamena, "
      f"ze nevysvetluje {round((1-rsquared)*100,2)} % rozptylu hodnot.")


# 3. Tipni si, která ze složek betonu ovlivňuje sílu betonu negativní (tj. má záporný regresní koeficient).
# Napiš, o kterou složku jde, do komentáře svého programu.

# print(res.summary())
# ODPOVED: Vypada to, ze negativne ovlivnuje silu betonu voda.


