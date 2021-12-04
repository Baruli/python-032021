import requests
import pandas as pd
from sklearn.model_selection import train_test_split    # metoda rozdeluji data na trenovaci a testovaci sadu
from sklearn.preprocessing import StandardScaler        # jeho pomoci standardizujeme/normalizujeme data
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, precision_score, f1_score
import matplotlib.pyplot as plt

# ZADANI UKOLU:
# Pokud použijeme stejný algoritmus jako v prvním úkolu, tj. KNeighborsClassifier,
# je možné předpovědět typ kosatce na základě těchto dat tak, aby metrika f1_score dosáhla alespoň 85%?


# 1. Definice problemu
# Na zaklade dat předpovědět typ kosatce (klasifikace do 2 skupin).

# 2. Priprava dat
# r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/kosatce.csv")
# open("kosatce.csv", "wb").write(r.content)

data = pd.read_csv("kosatce.csv")

# Zavery po prozkoumani dat:
# V datasetu nejsou nulove hodnoty a cilova promenne ma rozlozeni hodnot 50:50.
# Data ani nebudeme muset normalizovat - jsou ve stejne skale.

# Rozdeleni dat na trenovaci a testovaci sadu:
X = data.drop(columns=["target"])
y = data["target"]

# Velikost testovacích dat nastavime na 30%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=612)

# 3.+ 4. Trenovani vybraneho algoritmu - K-Nearest Neighbors
clf = KNeighborsClassifier()
clf.fit(X_train, y_train)

# 5. Vyhodnoceni  modelu
y_pred = clf.predict(X_test)

print(f1_score(y_test, y_pred))

# 6. Uprava modelu
ks = [1, 3, 5, 7, 9, 11]
f1_scores = []  # data pro graf
for k in ks:
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(k, f1_score(y_test, y_pred))
    f1_scores.append(f1_score(y_test, y_pred))  # data pro graf

# plt.plot(ks, f1_scores)
# plt.show()

# 7. Zaverecna predikce
clf = KNeighborsClassifier(n_neighbors=1)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print(f1_score(y_test, y_pred))

ConfusionMatrixDisplay.from_estimator(clf, X_test, y_test,
                                      display_labels=clf.classes_,
                                      cmap=plt.cm.Blues)
# plt.show()

# ZAVER: Ano, je mozne, natrenovat model tak, aby metrika f1_score dosahla vic nez 85 %, ale dat je velmi malo,
# bylo by vhodne ziskat vetsi dataset a vysledek overit. Anebo zvolit jiny algoritmus.
