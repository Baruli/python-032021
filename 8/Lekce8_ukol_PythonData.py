import requests
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing


r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/MLTollsStackOverflow.csv")
with open("MLTollsStackOverflow.csv", "wb") as f:
  f.write(r.content)

data = pd.read_csv("MLTollsStackOverflow.csv")
# print(data.columns)

# 1. Vyber sloupec python.
df = data[["month", "python"]].reset_index(drop=True)
print(df)
df["month"] = pd.to_datetime(df["month"], format='%y-%b').dt.strftime("%m-%Y")
df.set_index(["month"], inplace=True)


# 2. Proveď dekompozici této časové řady pomocí multiplikativního modelu. Dekompozici zobraz jako graf.
decompose = seasonal_decompose(df, model='multiplicative', period=12)
# print(decompose)
decompose.plot()
# plt.show()

# 3. Vytvoř predikci hodnot časové řady pomocí Holt-Wintersovy metody na 12 měsíců.
# Sezónnost nastav jako 12 a uvažuj multiplikativní model pro trend i sezónnost. Výsledek zobraz jako graf.

# Holt-Wintersova metoda - ulozeni vyslednych hodnot do noveho sloupce
mod = ExponentialSmoothing(df, seasonal_periods=12, trend="mul",
                           seasonal="mul", initialization_method="estimated")
res = mod.fit()
df["HWM"] = res.fittedvalues

# Predikce na 12 mesicu
df_forecast = pd.DataFrame(res.forecast(12), columns=["HWM_Forecast"])
df_forecast.index = df_forecast.index.strftime("%m-%Y")
# print(df_forecast)

# Slouceni pozorovanych hodnot + predikce na 12M a jejich zobrazeni v grafu
df_with_forecast = pd.concat([df, df_forecast])
df_with_forecast.plot()
print(df_with_forecast)
plt.show()



