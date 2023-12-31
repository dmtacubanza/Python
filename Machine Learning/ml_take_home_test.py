# -*- coding: utf-8 -*-
"""ML-take-home-test

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NwMnVFJxTIurkoYH7dIdqTryB82uufxx

**Instruction: **
Using the file, create a simple K-Nearest program in python
by getting the closest value based from the following parameters or inputs:

cx = 6.63518038

cy = - 4.37991231

cz = - 0.06342713
"""

# Commented out IPython magic to ensure Python compatibility.
#Engr. Darwin Tacubanza

# load requiered libraries
import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
import pandas as pd
import matplotlib.ticker as ticker
from sklearn import preprocessing
from sklearn.feature_extraction.text import CountVectorizer
# %matplotlib inline

#Load Data From CSV File
df = pd.read_csv('sample_ML_test.csv')
df.head()

#Data Visualization and Analysis
df['psize'].value_counts()

df['type'].value_counts()

df.describe()

df.info()

df.isna().sum().sum()

df['type_num'] = (df['type'].str[-1])

#Drop all NaN Values
df.dropna(inplace=True)

df = df.drop(['type'], axis=1)
df.head()

import matplotlib.pyplot as plt
df["type_num"].hist(bins=15)
plt.show()

correlation_matrix = df.corr()
correlation_matrix['type_num']

#Feature Engineering
df.columns

y = df[['type_num']].values
y[0:5]

#To use scikit-learn library, we have to convert the Pandas data frame to a Numpy array:
X = df[['tx', 'ty', 'tz', 'cx', 'cy', 'cz', 'size', 'ptx', 'pty', 'ptz', 'pcx', 'pcy', 'pcz', 'psize']].values
X[0:5]

#Normalize Data

X = preprocessing.StandardScaler().fit(X).transform(X.astype(float))
X[0:5]

#Train Test Split

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.2, random_state=4)
print ('Train set:', X_train.shape,  y_train.shape)
print ('Test set:', X_test.shape,  y_test.shape)

#Classification
#K nearest neighbor (K-NN)
#Import library
#Classifier implementing the k-nearest neighbors vote

from sklearn.neighbors import KNeighborsClassifier

#Training
k = 3

#Train Model and Predict
neigh = KNeighborsClassifier(n_neighbors = k).fit(X_train,y_train)
neigh

yhat = neigh.predict(X_test)
yhat[0:5]

from sklearn import metrics
print("Train set Accuracy: ", metrics.accuracy_score(y_train, neigh.predict(X_train)))
print("Test set Accuracy: ", metrics.accuracy_score(y_test, yhat))

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.datasets import make_blobs
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

plt.style.use('seaborn')
plt.figure(figsize = (10,10))
plt.scatter(X[:,0], X[:,1], c=y, marker= '*',s=100,edgecolors='black')
plt.show()

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 0)

knn5 = KNeighborsClassifier(n_neighbors = 5)
knn1 = KNeighborsClassifier(n_neighbors=1)

knn5.fit(X_train, y_train)
knn1.fit(X_train, y_train)

y_pred_5 = knn5.predict(X_test)
y_pred_1 = knn1.predict(X_test)

plt.figure(figsize = (15,5))
plt.subplot(1,2,1)
plt.scatter(X_test[:,0], X_test[:,1], c=y_pred_5, marker= '*', s=100,edgecolors='black')
plt.title("Predicted values with k=5", fontsize=20)

plt.subplot(1,2,2)
plt.scatter(X_test[:,0], X_test[:,1], c=y_pred_1, marker= '*', s=100,edgecolors='black')
plt.title("Predicted values with k=1", fontsize=20)
plt.show()