import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.metrics import confusion_matrix
ds = pd.read_csv("dataset.csv", sep=",", header=0)
fig = plt.figure(figsize=(14, 14))
sns.pairplot(ds, hue="label")  # “hue” attribute is the one with which the data is colored.
plt.show()