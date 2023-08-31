# -*- coding: utf-8 -*-
"""ECG ML Emotion.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15KofjbGylIfdAHympnR8HavuYXsnqwSL
"""

import warnings
warnings.filterwarnings('ignore')

!pip install openpyxl
!pip install scikit-plot

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import randint
from scipy.stats import loguniform
import math

from sklearn import tree
from sklearn import preprocessing
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import BernoulliNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import RepeatedStratifiedKFold

from scikitplot.metrics import plot_roc_curve as auc_roc
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, \
f1_score, roc_auc_score, roc_curve, precision_score, recall_score

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.optimizers import Adam

from xgboost import XGBClassifier

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [10,6]


pd.set_option('display.max_columns', 50)

data = pd.read_csv("/content/ecg_game.csv")
data = data.drop(columns=['Unnamed: 0'])

data.head()

conditions = dict(data['emotion'].value_counts())
labels = list(conditions.keys())
counts = list(conditions.values())
plt.bar(labels,counts, color ='green',width = 0.4)

le = preprocessing.LabelEncoder()
le.fit(data['emotion'])
e = data['emotion'].unique()
data['emotion'] = le.transform(data['emotion'])

f = le.transform(e)
print(f)

g = le.inverse_transform(f)
print(g)

x = data.iloc[:,1:-1]
y = data.iloc[:,-1]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.25, random_state = 0)

plt.figure(figsize=(12,10))
corr = data.corr()
sns.heatmap(corr, annot=False, cmap=plt.cm.Reds)
plt.show()

def feature_selection(correlation, threshold):
    selected_features = []
    for i in range(corr.shape[0]):
      if corr.iloc[i,21] > threshold:
        selected_features.append(data.iloc[:,i])
    return pd.DataFrame(selected_features).T

data_copy = data.copy()
reduced_data = feature_selection(corr, 0.01) #correlation_threshold = 1%

target = 'emotion'
features = [i for i in reduced_data.columns.values if i not in [target]]
reduced_data.head()

x_data_copy = data_copy.iloc[:,:-1]
y_data_copy = data_copy.iloc[:,-1]

x_data = reduced_data.iloc[:,:-1]
y_data = reduced_data.iloc[:,-1]

x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size = 0.25, random_state = 0)

x_train_copy, x_test_copy, y_train_copy, y_test_copy = train_test_split(x_data_copy, y_data_copy, test_size = 0.25, random_state = 0)

Evaluation_Results = pd.DataFrame(np.zeros((5,5)), columns=['Accuracy', 'Precision','Recall','F1-score','AUC-ROC score'])
Evaluation_Results.index=[ 'Artificial Neural Networks (ANN)', 'Random Forest Classifier (RF)', 'Decision Tree Classifier (DT)', 'Naïve Bayes Classifier (NB)', 'Logistic Regression (LR)']
Evaluation_Results

#Evaluation_Results = pd.DataFrame(np.zeros((5,5)), columns=['Accuracy', 'Precision','Recall','F1-score','AUC-ROC score'])
#Evaluation_Results.index=['Artificial Neural Networks', 'Random Forest', 'Decision Tree', 'Naive Bayes', 'Logistic Regression']

def Classification_Summary(pred,pred_prob,i):
    Evaluation_Results.iloc[i]['Accuracy']=round(accuracy_score(y_test, pred),3)*100
    Evaluation_Results.iloc[i]['Precision']=round(precision_score(y_test, pred, average='weighted'),3)*100 #
    Evaluation_Results.iloc[i]['Recall']=round(recall_score(y_test, pred, average='weighted'),3)*100 #
    Evaluation_Results.iloc[i]['F1-score']=round(f1_score(y_test, pred, average='weighted'),3)*100 #
    Evaluation_Results.iloc[i]['AUC-ROC score']=round(roc_auc_score(y_test, pred_prob[:], multi_class='ovr'),3)*100 #[:, 1]
    print('{}{}\033[1m Evaluating {} \033[0m{}{}\n'.format('<'*3,'-'*35,Evaluation_Results.index[i], '-'*35,'>'*3))
    print('Accuracy = {}%'.format(round(accuracy_score(y_test, pred),3)*100))
    print('F1 Score = {}%'.format(round(f1_score(y_test, pred, average='weighted'),3)*100)) #
    print('\n \033[1mConfusiton Matrix:\033[0m\n',confusion_matrix(y_test, pred))
    print('\n\033[1mClassification Report:\033[0m\n',classification_report(y_test, pred))

    auc_roc(y_test, pred_prob, curves=['each_class'])
    plt.show()

# Initializing the ANN
class_weight = {0: 1.,
                1: 50.,
                2: 2.}
ann = Sequential()
## Add the input layer and first hidden layer
ann.add(Dense(x_train_copy.shape[1], activation="relu", input_shape = (x_train_copy.shape[1],)))

ann.add(Dense(8))
ann.add(Activation('relu'))

ann.add(Dense(8))
ann.add(Activation('relu'))

#ann.add(Dense(8))
#ann.add(Activation('relu'))

#ann.add(Dense(4))
#ann.add(Activation('relu'))

ann.add(Dense(1, activation="softmax", kernel_initializer="normal"))
ann.summary()

ann.compile(optimizer='adam', loss='categorical_crossentropy', metrics=[tf.keras.metrics.AUC(curve='ROC'), 'accuracy'])
ann.fit(x_train_copy, y_train_copy, epochs=3)

#lab_enc = preprocessing.LabelEncoder()
#y_train = lab_enc.fit_transform(y_train)
#y_test = lab_enc.fit_transform(y_test)

#rf_model = RandomForestClassifier()
#rf_model.fit(x_train, y_train)

#dt_model = DecisionTreeClassifier(criterion="entropy", max_depth=14)
#dt_model = dt_model.fit(x_train,y_train)

rf_model = RandomForestClassifier()

param_dist={'bootstrap': [True, False],
            'max_depth': [10, 20, 50, 100, None],
            'max_features': ['auto', 'sqrt'],
            'min_samples_leaf': [1, 2, 4],
            'min_samples_split': [2, 5, 10],
            'n_estimators': [50, 100]}

cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)

rcv = RandomizedSearchCV(rf_model, param_dist, n_iter=50, scoring='roc_auc', n_jobs=-1, cv=5, random_state=1)

rf = rcv.fit(x_train, y_train).best_estimator_

dt_model = DecisionTreeClassifier()

param_dist = {"max_depth": [14, None],
              "max_features": randint(1, len(features)-1),
              "min_samples_leaf": randint(1, len(features)-1),
              "criterion": ["gini", "entropy"]}

cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)

rcv = RandomizedSearchCV(dt_model, param_dist, n_iter=50, scoring='roc_auc', n_jobs=-1, cv=5, random_state=1)

dt = rcv.fit(x_train, y_train).best_estimator_

#print('\n\033[1mInterpreting the output of Decision Tree:\n\033[0m')
#plt.figure(figsize=(25,25))
#tree.plot_tree(DT, fontsize=7)
#plt.show()

nb_model = BernoulliNB()

params = {'alpha': [0.01, 0.1, 0.5, 1.0, 10.0]}

cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
rcv = RandomizedSearchCV(nb_model, params, n_iter=50, scoring='roc_auc', n_jobs=-1, cv=5, random_state=1)
nb = rcv.fit(x_train, y_train).best_estimator_

lr_model = LogisticRegression()

space = dict()
space['solver'] = ['newton-cg', 'lbfgs', 'liblinear']
space['penalty'] = ['none'] #'none', 'l1', 'l2', 'elasticnet'
#space['C'] = loguniform(1e-5, 100)

cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
rcv = RandomizedSearchCV(lr_model, space, n_iter=50, scoring='roc_auc', n_jobs=-1, cv=5, random_state=1)
lr = rcv.fit(x_train, y_train).best_estimator_

def predict_prob(number):
  return [number[0],1-number[0]]

import tensorflow as tf

def auc(y_true, y_pred):
    auc = tf.metrics.AUC(y_true, y_pred)[1]
    #K.get_session().run(tf.local_variables_initializer())
    return auc

ann_prediction = ann.predict(x_test_copy)
rf_prediction = rf.predict(x_test)
dt_prediction = dt.predict(x_test)
nb_prediction = nb.predict(x_test)
lr_prediction = lr.predict(x_test)

ann_report = classification_report(y_test_copy,ann_prediction, output_dict=True)
rf_pred_prob = rf.predict_proba(x_test)
dt_pred_prob = dt.predict_proba(x_test)
nb_pred_prob = nb.predict_proba(x_test)
lr_pred_prob = lr.predict_proba(x_test)

#ann_pred_prob=ann.predict(x_test_copy)
#ann_prediction=np.argmax(ann_pred_prob,axis=1)

Evaluation_Results.iloc[0]['Accuracy']=round(accuracy_score(y_test_copy, ann_prediction),3)*100
Evaluation_Results.iloc[0]['Precision']=round(precision_score(y_test_copy, ann_prediction, average='weighted'),3)*100 #
Evaluation_Results.iloc[0]['Recall']=round(recall_score(y_test_copy, ann_prediction, average='weighted'),3)*100 #
Evaluation_Results.iloc[0]['F1-score']=round(f1_score(y_test_copy, ann_prediction, average='weighted'),3)*100 #
#auc = roc_auc_score(y_test_copy, ann_prediction, multi_class='ovr')
#print(auc)
Evaluation_Results.iloc[0]['AUC-ROC score']=50
#Evaluation_Results.iloc[0]['AUC-ROC score']=round(roc_auc_score(y_test, ann_prediction.flatten()[:], multi_class='ovr'),3)*100 #[:, 1]

#Classification_Summary(ann_prediction,ann_prediction,0)
Classification_Summary(rf_prediction,rf_pred_prob,1)
Classification_Summary(dt_prediction,dt_pred_prob,2)
Classification_Summary(nb_prediction,nb_pred_prob,3)
Classification_Summary(lr_prediction,lr_pred_prob,4)

#ann_prediction = ann.predict(x_test_copy)
#rf_prediction = rf_model.predict(x_test)
#dt_prediction = dt_model.predict(x_test)

print("Neural Networks")
print(classification_report(y_test_copy,ann_prediction))
print("Random Forest")
print(classification_report(y_test,rf_prediction))
print("Decision Tree")
print(classification_report(y_test,dt_prediction))
print("Naive Bayes")
print(classification_report(y_test,nb_prediction))
print("Logistic Regression")
print(classification_report(y_test,lr_prediction))

print('\033[1mML Algorithms Comparison'.center(100))
plt.figure(figsize=[12,8])
sns.heatmap(Evaluation_Results, annot=True, vmin=85, vmax=100, cmap='Blues', fmt='.1f')
plt.show()

#Plotting Confusion-Matrix of all the predictive Models

def plot_cm(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred, labels=np.unique(y_true))
    cm_sum = np.sum(cm, axis=1, keepdims=True)
    cm_perc = cm / cm_sum.astype(float) * 100
    annot = np.empty_like(cm).astype(str)
    nrows, ncols = cm.shape
    for i in range(nrows):
        for j in range(ncols):
            c = cm[i, j]
            p = cm_perc[i, j]
            if i == j:
                s = cm_sum[i]
                annot[i, j] = '%.1f%%\n%d/%d' % (p, c, s)
            elif c == 0:
                annot[i, j] = ''
            else:
                annot[i, j] = '%.1f%%\n%d' % (p, c)
    cm = pd.DataFrame(cm, index=np.unique(y_true), columns=np.unique(y_true))
    cm.columns=labels
    cm.index=labels
    cm.index.name = 'Actual'
    cm.columns.name = 'Predicted'
    sns.heatmap(cm, annot=annot, fmt='')# cmap= "GnBu"

def conf_mat_plot(all_models, name):
    plt.figure(figsize=[20,3.5*math.ceil(len(all_models)*len(labels)/14)])

    for i in range(len(all_models)):
        if len(labels)<=4:
            plt.subplot(2,4,i+1)
        else:
            plt.subplot(math.ceil(len(all_models)/3),3,i+1)
        #print(i)
        #if i == 0:
        if name == 'Artificial Neural Network':
          pred = all_models[i].predict(x_test_copy)
        else:
          pred = all_models[i].predict(x_test)
        sns.heatmap(confusion_matrix(y_test, pred), annot=True, cmap='Blues', fmt='.0f') #vmin=0,vmax=5
        plt.title(name)
    plt.tight_layout()
    plt.show()

conf_mat_plot([ann], 'Artificial Neural Network')
conf_mat_plot([rf], 'Random Forest')
conf_mat_plot([dt], 'Decision Tree')
conf_mat_plot([nb], 'Naive Bayes')
conf_mat_plot([lr], 'Logistic Regression')