import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
from sklearn.metrics import precision_score, f1_score, accuracy_score, recall_score
import matplotlib.pyplot as plt

# 1. Definice problemu: Je voda pitna nebo ne? (na zaklade jejiho chemickeho rozboru)

# r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/water-potability.csv")
# open("water-potability.csv", 'wb').write(r.content)

# 2. Data:
data = pd.read_csv("water-potability.csv")
data = data.dropna()
# print(data["Potability"].value_counts(normalize=True))    # Rozlozeni cilovych hodnot v nasem datasetu

# Rozdeleni dat na trenovaci a testovaci sadu:
X = data.drop(columns=["Potability"])
y = data["Potability"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalizace dat:
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 3.+ 4. Vyber algoritmu a trenovani modelu:
# K-NEAREST NEIGHBORS (KNN) - Vysledna predikce z lekce vybrana na zaklade F1_score (Precision + Recall)
clf = KNeighborsClassifier(n_neighbors=3)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print(f1_score(y_test, y_pred))

# 5. Vyhodnoceni  modelu (defaultni hodnota: n_neighbors=5)
y_pred = clf.predict(X_test)

# Confusion matrix
print(confusion_matrix(y_true=y_test, y_pred=y_pred))


# DOMACI UKOL:
# Zopakuj experiment, ale tentokrát vyber hodnotu parametru n_neighbors na základě metriky precision.
# Znamená to, že pro nás bude důležité, abychom raději označili pitnou vodu za nepitnou, než nepitnou za pitnou.

# 6. Uprava modelu
ks = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
for k in ks:
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(k, precision_score(y_test, y_pred))


# 7. Zaverecna predikce - pouzita hodnota parametru, ktera dava nejlepsi vysledek pri volani precision().
clf = KNeighborsClassifier(n_neighbors=13)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print('\n', precision_score(y_test, y_pred))

# Confusion matrix
print(confusion_matrix(y_true=y_test, y_pred=y_pred))

# ConfusionMatrixDisplay.from_estimator(clf, X_test, y_test,
#                                       display_labels=clf.classes_,
#                                       cmap=plt.cm.Blues)


# ZAVER: Oproti modelu z hodiny, ted nas model zalozeny na Precision() mnohem lepe zachycuje nepitne vzorky, a to ty
# ktere skutecne pitne nejsou, ale bohuzel ve vetsi mire urcuje skutecne pitne vzorky za falesne nepitne.
# Vysledkem je tedy mene vyvazeny model, ktery je prilis "opatrny". Coz by byla dobra volba, pokud by voda zpusobovala
# opravdu vazne zdravotni problemy a chteli bychom minimalizovat riziko.


# DOBROVOLNY DOPLNEK
# Vytvoř graf, který bude pro několik parametrů n_neighbors obsahovat všechny čtyři výsledné metriky,
# které jsme si v kurzu ukázali: accuracy, precision, recall, f1_score.

ks = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
accuracy = []
precision = []
recall = []
f1_scores = []

for k in ks:
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy.append(accuracy_score(y_test, y_pred))
    precision.append(precision_score(y_test, y_pred))
    recall.append(recall_score(y_test, y_pred))
    f1_scores.append(f1_score(y_test, y_pred))


plt.plot(ks, accuracy, label='accuracy')
plt.plot(ks, precision, label='precision')
plt.plot(ks, recall, label='recall')
plt.plot(ks, f1_scores, label='f1_scores')
plt.xlabel("n_neighbors")
plt.ylabel("Model evaluation")
plt.legend()

plt.show()
