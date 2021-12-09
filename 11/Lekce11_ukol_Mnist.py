import numpy as np
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

from sklearn.datasets import load_digits


digits = load_digits()
X = digits.data

# DOBROVOLNÝ DOPLNEK:
# O jaký typ dat by se mohlo jednat?
# Zkus nastavovat různé hodnoty proměnné idx, která indexuje řádky původních dat - před redukcí dimenzionality!
# Uměli bychom jednotlivé clustery označit? Podle čeho se data shlukují?

# idx = 0
# print(len(X[idx]))
# image = np.reshape(X[idx], (8, 8))
# plt.imshow(image, cmap="gray_r")
# plt.show()

# ODPOVED: Data se shlukuji podle stupne odstinu sedi. Jedna se o dataset rukou psanych cisel 0-16.


# 1. Data normalizuj
scaler = StandardScaler()
X = scaler.fit_transform(X)

# 2. Redukuj počet vstupních proměnných na dvě pomocí TSNE. Můžeš vyzkoušet různé parametry.
tsne = TSNE(
            init="pca",
            n_components=2,
            perplexity=100,          # pocet sousedu, podle kterych se metoda ridi
            learning_rate="auto",
            random_state=0,
            )
X = tsne.fit_transform(X)
print(X.shape)

# 3. Vykresli data do bodového grafu. Kolik odhaduješ shluků (clusterů)?
plt.scatter(X[:, 0], X[:, 1], s=50)
plt.show()

# 4. Aplikuj algoritmus KMeans s počtem shluků, který jsi odhadl/a v předchozím kroku
model = KMeans(n_clusters=8, random_state=42)   # dopredu si urcime pocet clusteru (zhluku)
labels = model.fit_predict(X)

# Zobrazeni vysledku v grafuV
plt.scatter(X[:, 0], X[:, 1], c=labels, s=50, cmap="Pastel2")
centers = model.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c="blue", s=200, alpha=0.5)   # zakresleni centralnich bodu
plt.show()

# 5. Vyhodnoť výsledek pomocí silhouette_score, který by měl být alespoň 0.5
print(silhouette_score(X, labels))  # OK, vysledek je 0.57



