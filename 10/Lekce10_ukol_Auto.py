import requests
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score

# r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/auto.csv")
# open("auto.csv", "wb").write(r.content)

# Načti data. Při volání metody read_csv nastav parametr na_values: na_values=["?"].
# Neznámé/prázdné hodnoty jsou totiž reprezentované jako znak otazníku.
df = pd.read_csv("auto.csv", na_values="?")

# Po načtení dat se zbav řádek, které mají nějakou neznámou/prázdnou hodnotu.
df = df.dropna()

# Naše výstupní proměnná bude sloupec "origin". Pod kódy 1, 2 a 3 se skrývají regiony USA, Evropa a Japonsko.
# Zkus odhadnout (třeba pomocí sloupce "name"), který region má který kód :-)

# Pridani noveho sloupce obsahujiciho nazvy regionu misto kodu 1,2,3
df.loc[df.origin == 1, "region"] = "usa"
df.loc[df.origin == 2, "region"] = "europe"
df.loc[df.origin == 3, "region"] = "japan"


# Podívej se, jak se měnila spotřeba aut v letech 1970-1982.
# Vytvoř graf, který ukáže průměrnou spotřebu v jednotlivých letech tak, aby byly rozlišené tři regiony.

cons = df.groupby(["year", "region"])["mpg"].agg("mean").to_frame()
cons.pivot_table(index="year", columns="region", aggfunc="min").plot()
# plt.show()

# Rozděl data na vstupní a výstupní proměnnou, a následně na trénovací a testovací sadu v poměru 70:30.
X = df.drop(columns=["origin", "name", "region"])
y = df["origin"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

# Data normalizuj:
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Použij klasifikační algoritmus rozhodovacího stromu, a vyber jeho parametry technikou GridSearchCV:
model = DecisionTreeClassifier(random_state=42)
clf = GridSearchCV(model, param_grid={'max_depth': range(2, 20), 'min_samples_leaf': range(2, 30)},
                   scoring="f1_weighted")

clf.fit(X_train, y_train)
print(clf.best_params_)
# print(round(clf.best_score_, 2))

# Winner
clf_win = DecisionTreeClassifier(random_state=42, max_depth=9, min_samples_leaf=3)
clf_win.fit(X_train, y_train)
y_pred = clf_win.predict(X_test)

# Jaké jsi dosáhl/a metriky f1_score?
f1 = round(f1_score(y_test, y_pred, average="weighted"), 3)
print(f"Hodnota metriky f1_score pro predikci na testovacich datech je: {f1} ")