import io
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.metrics import confusion_matrix

# Data handling.
from sklearn.impute import KNNImputer

# Principal Component Analysis.
from sklearn import decomposition
from sklearn.preprocessing import StandardScaler

# Probabilistic classifiers.
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier, plot_tree

# Performance evaluation.
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
import time

t0 = time.time()

ds = pd.read_csv("dataset.csv", sep=",", header=0)

ds_nonnan = ds.dropna()

mask = ds_nonnan.label != "test"  # Get a boolean vector for each data row.

ds_clean = ds_nonnan.loc[mask]

# Back-up to plot properly.
ds_clean_all = ds_clean

# Save the target.
y = ds_clean["label"]

undesired_headers = ["label", "fields_num", "props_num", "#ref"]
for header in undesired_headers:
    del ds_clean[header]

X = ds_clean
X_shape = X.shape
XS = StandardScaler().fit_transform(X)
pca = decomposition.PCA(n_components=X_shape[1]).fit(XS)
Xproj = pca.transform(XS)

dfpca = pd.DataFrame(Xproj[:, 0:7], columns=['PCA1', 'PCA2','PCA3', 'PCA4','PCA5', 'PCA6','PCA7'])

fig = plt.figure(figsize=(8, 8))

sns.pairplot(data=dfpca, hue=y)
plt.show()
print("Debugging")
# fig = plt.figure(figsize=(14, 14))
# sns.pairplot(ds, hue="label")  # “hue” attribute is the one with which the data is colored.
# plt.show()

# Do feedback of the elapsed time running the program.
elapsed = time.time() - t0
print("Elapsed time: " + str(elapsed) + " s")
