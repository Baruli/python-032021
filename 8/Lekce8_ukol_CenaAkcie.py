import pandas as pd
import yfinance as yf
import pandas
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.ar_model import AutoReg


# Pomocí modulu yfinance, stáhni ceny akcií společnosti Cisco (používají "Ticker" CSCO) za posledních 5 let.
cisco = yf.Ticker("CSCO")
cisco_df = cisco.history(period="5y")

# Dále pracuj s cenami akcie v závěru obchodního dne, tj. použij sloupec "Close".
df = cisco_df[["Close"]]
df.index = df.index.to_period('D')  # Bez tohoto scriptu mi python hazi warning

# 1. Zobraz si graf autokorelace a podívej se, jak je hodnota ceny závislá na svých vlastních hodnotách v minulosti.
print("Autokorelace casove rady je: ", df["Close"].autocorr(lag=1))
plot_acf(df["Close"])
# plt.show()

# 2. Zkus použít AR model k predikci cen akcie na příštích 5 dní.
model = AutoReg(df["Close"], lags=90, trend="ct")   # Protoze vysledky akcii se zverejnuji kvartalne
res = model.fit()
model_fit = model.fit()
predictions = res.predict(start=df.shape[0], end=df.shape[0] + 4)
dates = pd.date_range(start='2021-11-20', periods=5)
df_forecast = pandas.DataFrame(predictions, columns=['Prediction']).set_index(dates)

# 3. Zobraz v grafu historické hodnoty (např. hodnoty za posledních 50 dní) a tebou vypočítanou predikci.
df_with_predictions = pandas.concat([df, df_forecast]).tail(55)
df_with_predictions.plot()
plt.show()





