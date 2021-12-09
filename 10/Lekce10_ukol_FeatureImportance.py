import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split


r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/soybean-2-rot.csv")
open("soybean-2-rot.csv", "wb").write(r.content)

data = pd.read_csv("soybean-2-rot.csv")
# print(data.head().to_string())

# 1. Připomeň si, co dělá OneHotEncoder.
# Kolik proměnných jsme měli původně, a kolik jich máme po "zakódovaní" (nápověda: X.shape)?

X = data.drop(columns=["class"])    # vstupni promenne
input_features = X.columns          # nazvy vstupnich promennych

y = data["class"]                   # vystupni promenna
# print(data["class"].value_counts())

# Vypsani unikatnich hodnot pro kazdy sloupec
for col in X:
    print(col, set(X[col]))

# Zobrazeni vstupnich promennych pred pouzitim OneHotEncoder
print(f"\nPocet sloupcu pred pouzitim OneHotEncoderu: {X.shape[1]}")  # 23 sloupcu

# Pouziti OneHotEncoderu
oh_encoder = OneHotEncoder()
X = oh_encoder.fit_transform(X)

# Zobrazeni vstupnich promennych po pouziti OneHotEncoder
print(f"Pocet sloupcu po pouziti OneHotEncoderu: {X.shape[1]}\n")  # 56 sloupcu

encoder = LabelEncoder()
y = encoder.fit_transform(y)

# Pouziti modelu Decision Tree
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)

clf = DecisionTreeClassifier(max_depth=3, min_samples_leaf=1)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print(f1_score(y_test, y_pred, average="weighted"), '\n')

# 2. Podívej se na atribut feature_importances_, který říká, které vstupní proměnné model použil pro rozhodování.
# Některé budou mít nulovou hodnotu, to znamená, že vůbec potřeba nejsou.

importance = clf.feature_importances_
feature = oh_encoder.get_feature_names_out(input_features=input_features)

# funkce zip(col1, col2): zadame vic sloupcu a ona nam udela dvojice
feature_importance = list(zip(feature, importance))
[print(l) for l in feature_importance if l[1] != 0]


# 3. Která vstupní proměnná má největší "důležitost"? Stačí nám tato proměnná pro úspěšnou klasifikaci?
# Odpoved: pouzit pouze jednu vstupni promennou neni pro Decision Tree model mozne (error raised), proto zkusim pouzit
# vsechny vstupni promenne s nenulovoun vyznamnosti pred one-hot encodingem (protoze jinak to asi nejde).

# Trenovani modelu s vybranymi promennymi
X = data[['plant-stand', 'plant-growth', 'leafspots-halo', 'lodging']]
y = data["class"]

# Pouziti OneHotEncoderu
oh_encoder = OneHotEncoder()
X = oh_encoder.fit_transform(X)

encoder = LabelEncoder()
y = encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)

clf = DecisionTreeClassifier(max_depth=3, min_samples_leaf=1)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print(f1_score(y_test, y_pred, average="weighted"), '\n')

# Jaký je rozdíl mezi hodnotou f1_score při použití všech proměnných a jen této jedné "nejdůležitější" proměnné?
# Odpoved: F1 score je 1.0 v obou pripadech.


# Vykresli graf, ze kterého je vidět rozložení hodnot této jedné nejdůležitější proměnné.
# a) Vyuziti knihovny Seaborn
# sns.countplot(x="plant-stand", hue="class", data=data, palette='Set1_r')

# b) Pivot table + plot
data_pivot = pd.pivot_table( data[['class', 'plant-stand']],
                             index='plant-stand', columns='class',
                             aggfunc=len,
                             margins=False )


data_pivot.plot(kind='bar', rot=0)
plt.show()



