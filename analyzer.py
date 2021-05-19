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
import statistics as st

t0 = time.time()

complete_ds = pd.read_csv("dataset.csv", sep=",", header=0)
ds_shape = complete_ds.shape

# Eliminate the test samples.
mask = complete_ds.label != "test"  # Get a boolean vector for each data row.
ds = complete_ds.loc[mask]

# Discard sample with NaNs.
ds_nonnan = ds.dropna()

# Save the target.
target = ds["label"]
labels = list(set(target))

# Remove last headers (because they are not data, are checksums to debug).
undesired_headers = ["fields_num", "props_num", "#ref", "Time_max", "Time_min", "Time_mean", "Time_q1", "Time_q2", "Time_q3", "LatitudeDegrees_max", "LatitudeDegrees_min", "LatitudeDegrees_mean", "LatitudeDegrees_q1", "LatitudeDegrees_q2", "LatitudeDegrees_q3", "LongitudeDegrees_max", "LongitudeDegrees_min", "LongitudeDegrees_mean", "LongitudeDegrees_q1", "LongitudeDegrees_q2", "LongitudeDegrees_q3"]
for header in undesired_headers:
    del ds[header]


# Check the NaN gaps.
for label in labels:
    mask = ds.label == label
    curr_ds = ds.loc[mask]
    print(label)

    for header in ds.keys():
        curr_list = list(curr_ds[header])
        if header != "label":
            curr_nonnans = []
            index_list = []  # Save a reference to know which values are not a number.
            for i in range(len(curr_list)):
                if not np.isnan(curr_list[i]):
                    curr_nonnans.append(curr_list[i])
                else:
                    index_list.append(curr_ds.index[i])

            if len(curr_nonnans) != 0 and len(index_list) != 0:
                curr_mean = st.mean(curr_nonnans)
                for i in index_list:
                    ds[header][i] = curr_mean
                # mask = bool_list
                # column = header
                # complete_ds.loc[mask, column] = curr_mean  # Substitute the true values of mask in the specified column.
            elif len(curr_nonnans) == 0:
                print("All nans for: " + label + " -> " + header)


# Do feedback of the time elapsed running the program.
elapsed = time.time() - t0
print("Elapsed time: " + str(round(elapsed, 2)) + " s")
