import requests
import pandas as pd
import statsmodels.formula.api as smf

# V souboru Fish.csv najdeš informace o rybách z rybího trhu:
# délku (vertikální - Length1, diagonální - Length2 a úhlopříčnou - Length3),
# výšku,
# šířku,
# živočišný druh ryby,
# hmotnost ryby.

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/Fish.csv")
with open("Fish.csv", "wb") as f:
  f.write(r.content)

df = pd.read_csv("Fish.csv")

# 1. Vytvoř regresní model, který bude predikovat hmnotnost ryby na základě její diagonální délky (sloupec Length2).
mod = smf.ols(formula='Weight ~ Length2', data=df)
res1 = mod.fit()
# print(res1.summary())


# 2. Zkus přidat do modelu výšku ryby (sloupec Height) a porovnej, jak se zvýšila kvalita modelu.
mod = smf.ols(formula='Weight ~ Length2 + Height', data=df)
res2 = mod.fit()
# print(res2.summary())

print("\nNa zaklade rozdilne delky ryb umime vysvetlit", r"{:.2%}".format(res1.rsquared_adj),
      "rozptylu hodnot jejich hmotnosti. Pokud do modelu pridame navic vysku ryby, tak vysvetlime",
      "{:.2%}".format(res2.rsquared_adj), "vysledne hmotnosti ryb.")


# 3. Nakonec pomocí metody target encoding zapracuj do modelu živočišný druh ryby.
# print(df["Species"].unique())
prumery = df.groupby(["Species"])["Weight"].mean()
df["Species_prumer"] = df["Species"].map(prumery)

mod = smf.ols(formula='Weight ~ Length2 + Height + Species', data=df)
res = mod.fit()
# print(res.summary())
print(f"\nKoeficient determinace naseho modelu po pridani promenne 'druh ryby': {res.rsquared_adj}")