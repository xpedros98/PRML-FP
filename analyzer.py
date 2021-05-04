import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.metrics import confusion_matrix
import time

t0 = time.time()

ds = pd.read_csv("dataset.csv", sep=",", header=0)
fig = plt.figure(figsize=(14, 14))
sns.pairplot(ds, hue="label")  # “hue” attribute is the one with which the data is colored.
plt.show()

# Do feedback of the elapsed time running the program.
elapsed = time.time() - t0
print("Elapsed time: " + str(elapsed) + " s")
