# -*- coding: utf-8 -*-
"""Assignment2_BUSS6002-3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jc8n0EWdo6LLCGHlQI2rFUxUrXZ_MjJw
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("SolarSurvey.csv")

"""### Data Cleaning and Preparation"""

#drop rows with missing values for more accurate analysis
df = df.dropna()

# Identify if there are any rows with negative values for Generation
negative_rows = df[df['Generation'] < 0]

#Consider greater that zero values for solar generation
df = df[df['Generation'] > 0]

# convert azimuth to integer
azimuth_values = df['Roof_Azimuth'].astype(int)

#For normalisation of roof azimuth
def normalised_azimuth(azimuth):

    if azimuth == 360:
        normalised_azimuth = 0
    elif (azimuth > 180) and (azimuth < 360):
        normalised_azimuth = 360 - azimuth
    else:
        normalised_azimuth = azimuth
    return normalised_azimuth

df['Normalised_Azimuth'] = azimuth_values.apply(normalised_azimuth)

"""### Data Splitting for Model 1 and 2"""

X = df[['Latitude', 'Normalised_Azimuth', 'Panel_Capacity']].to_numpy().reshape(-1, 3)
y = df['Generation'].to_numpy()

# Split the dataset into training, validation and testing sets
#tv and test set
X_tv, X_test, y_tv, y_test = train_test_split(X, y, test_size=0.25, random_state=1)
#train, vali and test
X_train, X_vali, y_train, y_vali = train_test_split(X_tv, y_tv, test_size=0.25, random_state=1)

print(f"This is the shape for the training data: {X_train.shape}")
print(f"This is the shape for the validation data: {X_vali.shape}")
print(f"This is the shape for the testing data: {X_test.shape}")

"""### Model 1: Multiple Linear Regression"""

dim = 3
linear_reg = LinearRegression()
linear_reg.fit(X_tv[:,:dim], y_tv)

# Print the estimated beta coefficients
beta0 = linear_reg.intercept_
beta = linear_reg.coef_

print("beta0:", beta0)
print("beta coefficients:", beta)

dim = 3
linear_reg = LinearRegression()
linear_reg.fit(X_train[:,:dim], y_train)

# Print the estimated beta coefficients
beta0 = linear_reg.intercept_
beta = linear_reg.coef_

print("beta0:", beta0)
print("beta coefficients:", beta)

y_test_pred_m1 = linear_reg.predict(X_test)
mse_m1_final = mean_squared_error(y_test, y_test_pred_m1)

print(f"{mse_m1_final:.2f}")

#then for this X_train, y_train na kasi yun yung na split na yung tv into train at vali

y_val_pred_m1 = linear_reg.predict(X_vali)
mse_m1 = mean_squared_error(y_vali, y_val_pred_m1)

mse_m1

#hindi ba X_tv,y_tv muna gagamitin dito since yun yung unang hati ng data?

y_train_pred_m1 = linear_reg.predict(X_train)
residuals = y_train - y_train_pred_m1

# Plot residuals against predicted values
plt.scatter(y_train_pred_m1, residuals, alpha = 0.5)
plt.xlabel('Predicted values')
plt.axhline(y=0, color='red', linestyle='--')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted values')
plt.show()

# Histogram of residuals
sns.histplot(residuals, kde=True)
plt.title('Distribution of Residuals')
plt.show()

# Check for normality
stats.probplot(residuals, dist="norm", plot=plt)
plt.show()

model_m1 = LinearRegression()
model_m1.fit(X_tv, y_tv)
y_test_pred_m1 = model_m1.predict(X_test)
mse_m1_final = mean_squared_error(y_test, y_test_pred_m1)

print(f"{mse_m1_final:.2f}")

"""## Model 2: Polynomial Regression"""

poly = PolynomialFeatures(degree=2, include_bias=False)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.fit_transform(X_test)

# Fit the linear regression model
model_m2 = LinearRegression()
model_m2.fit(X_train_poly, y_train)

# Print the estimated beta coefficients
beta0 = model_m2.intercept_
beta = model_m2.coef_

print("beta0:", beta0)
print("beta coefficients:", beta)

#model_m2 = make_pipeline(PolynomialFeatures(2), LinearRegression())
#model_m2.fit(X_train, y_train)
#y_val_pred_m2 = model_m2.predict(X_vali)
#mse_m2 = mean_squared_error(y_vali, y_val_pred_m2)

#mse_m2

# Make predictions on the test set
y_val_pred_m2 = model_m2.predict(X_test_poly)

# Calculate mean squared error
mse_m2_final = mean_squared_error(y_test, y_val_pred_m2)

print(mse_m2_final)

# Create polynomial features with interaction terms
X_vali_poly = poly.transform(X_vali)

# Make predictions on the validation set
y_val_pred_m2 = model_m2.predict(X_vali_poly)

# Calculate mean squared error
mse_m2 = mean_squared_error(y_vali, y_val_pred_m2)

print(mse_m2)

y_train_pred_m2 = model_m2.predict(X_train_poly)
residuals = y_train - y_train_pred_m2

# Plot residuals against predicted values
plt.scatter(y_train_pred_m2, residuals, alpha = 0.5)
plt.xlabel('Predicted values')
plt.axhline(y=0, color='red', linestyle='--')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted values')
plt.show()

# Histogram of residuals
sns.histplot(residuals, kde=True)
plt.title('Distribution of Residuals')
plt.show()

# Check for normality
stats.probplot(residuals, dist="norm", plot=plt)
plt.show()

"""## Model 3: Multiple Linear Regression with Shading"""

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df["Shading_Label"] = le.fit_transform(df["Shading"].fillna("NaN"))

print(df)

X = df[['Latitude', 'Normalised_Azimuth', 'Panel_Capacity','Shading_Label']].to_numpy().reshape(-1, 4)
y = df['Generation'].to_numpy()

# Split the dataset into training, validation and testing sets
X_tv, X_test, y_tv, y_test = train_test_split(X, y, test_size=0.25, random_state=1)
X_train, X_vali, y_train, y_vali = train_test_split(X_tv, y_tv, test_size=0.25, random_state=1)

dim = 4
linear_reg = LinearRegression()
linear_reg.fit(X_train[:,:dim], y_train)

# Print the estimated beta coefficients
beta0 = linear_reg.intercept_
beta = linear_reg.coef_

print("beta0:", beta0)
print("beta coefficients:", beta)

model_m3 = LinearRegression()
model_m3.fit(X_tv, y_tv)
y_val_pred_m3 = model_m3.predict(X_test)
mse_m3_final = mean_squared_error(y_test, y_val_pred_m3)

mse_m3_final

#Step 4 re-estimate on the combined set

model_m3 = LinearRegression()
model_m3.fit(X_train, y_train)
y_val_pred_m3 = model_m3.predict(X_vali)
mse_m3 = mean_squared_error(y_vali, y_val_pred_m3)

mse_m3

y_train_pred_m3 = model_m3.predict(X_train)
residuals = y_train - y_train_pred_m3

# Plot residuals against predicted values
plt.scatter(y_train_pred_m3, residuals, alpha = 0.5)
plt.xlabel('Predicted values')
plt.axhline(y=0, color='red', linestyle='--')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted values')
plt.show()

# Histogram of residuals
sns.histplot(residuals, kde=True)
plt.title('Distribution of Residuals')
plt.show()

# Check for normality
stats.probplot(residuals, dist="norm", plot=plt)
plt.show()

"""### Substitute: Quadratic Polynomial with Shading"""

poly = PolynomialFeatures(degree=2, include_bias=False)
X_train_poly = poly.fit_transform(X_train)

# Fit the linear regression model
model = LinearRegression()
model.fit(X_train_poly, y_train)

# Print the estimated beta coefficients
beta0 = model.intercept_
beta = model.coef_

print("beta0:", beta0)
print("beta coefficients:", beta)

# Create polynomial features with interaction terms
poly = PolynomialFeatures(degree=2, include_bias=False)
X_tv_poly = poly.fit_transform(X_tv)
X_test_poly = poly.transform(X_test)

# Fit the linear regression model
model_m4 = LinearRegression()
model_m4.fit(X_tv_poly, y_tv)

# Make predictions on the test set
y_val_pred_m4 = model_m4.predict(X_test_poly)

# Calculate mean squared error
mse_m4_final = mean_squared_error(y_test, y_val_pred_m4)

print(mse_m4_final)

# Create polynomial features with interaction terms
poly = PolynomialFeatures(degree=2, include_bias=False)
X_train_poly = poly.fit_transform(X_train)
X_vali_poly = poly.transform(X_vali)

# Fit the linear regression model
model_m4 = LinearRegression()
model_m4.fit(X_train_poly, y_train)

# Make predictions on the validation set
y_val_pred_m4 = model_m4.predict(X_vali_poly)

# Calculate mean squared error
mse_m4 = mean_squared_error(y_vali, y_val_pred_m4)

print(mse_m4)

y_train_pred_m4 = model_m4.predict(X_train_poly)
residuals = y_train - y_train_pred_m4

# Plot residuals against predicted values
plt.scatter(y_train_pred_m4, residuals, alpha = 0.5)
plt.xlabel('Predicted values')
plt.axhline(y=0, color='red', linestyle='--')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted values')
plt.show()

# Histogram of residuals
sns.histplot(residuals, kde=True)
plt.title('Distribution of Residuals')
plt.show()

# Check for normality
stats.probplot(residuals, dist="norm", plot=plt)
plt.show()

"""## Benchmark"""

import pandas as pd
from sklearn.model_selection import train_test_split


df = pd.read_csv('SolarSurvey.csv')
df

#drop rows with missing values for more accurate analysis
df = df.dropna()

# Identify if there are any rows with negative values for Generation
negative_rows = df[df['Generation'] < 0]

#Consider greater that zero values for solar generation
df = df[df['Generation'] > 0]

years = [2019, 2020, 2021]
D = df[df['Year'].isin(years)]

df_tv, df_test = train_test_split(df, test_size=0.25, random_state=1)

BM1 = D.groupby('City')['Generation'].mean()
BM1

BM2 = D.groupby(['City','Panel_Capacity'])['Generation'].mean()
BM2

#df_tv split into X and y
X_train = df_tv[['City']].to_numpy().reshape(-1, 1)
y_train = df_tv['Generation'].to_numpy()

#df_train split into X and y
X_test = df_test[['City']].to_numpy().reshape(-1, 1)
y_test = df_test['Generation'].to_numpy()

from sklearn.metrics import mean_squared_error

# Create a new DataFrame for training
df_tv = pd.DataFrame(X_train, columns=['City'])
df_tv['Generation'] = y_train

# Create a new DataFrame for testing
df_test = pd.DataFrame(X_test, columns=['City'])
df_test['Generation'] = y_test

# Create a dictionary with city names as keys and average generation for that city as values
city_avg_gen = df_train.groupby('City')['Generation'].mean().to_dict()

# Map city names in the training and testing data to their corresponding average generation
df_tv['BM1_Predictions'] = df_tv['City'].map(city_avg_gen)
df_test['BM1_Predictions'] = df_test['City'].map(city_avg_gen)

# Calculate MSE for the Benchmark Model 1 on the test set
benchmark1_mse = mean_squared_error(df_test['Generation'], df_test['BM1_Predictions'])
benchmark1_mse

df_tv, df_test = train_test_split(df, test_size=0.25, random_state=1)

# df_tv split into X and y
X_train = df_tv[['City', 'Panel_Capacity']].to_numpy().reshape(-1, 2)
y_train = df_tv['Generation'].to_numpy()

# df_test split into X and y
X_test = df_test[['City', 'Panel_Capacity']].to_numpy().reshape(-1, 2)
y_test = df_test['Generation'].to_numpy()

from sklearn.metrics import mean_squared_error
import numpy as np

# Create a new DataFrame for training
df_train = pd.DataFrame(X_train, columns=['City','Panel_Capacity'])
df_train['Generation'] = y_train

# Create a new DataFrame for testing
df_test = pd.DataFrame(X_test, columns=['City','Panel_Capacity'])
df_test['Generation'] = y_test

# Create a dictionary with city names and panel capacities as keys and average generation for that city and panel capacity as values
city_capacity_avg_gen = df_train.groupby(['City', 'Panel_Capacity'])['Generation'].mean().to_dict()

# Map city names and panel capacities in the training and testing data to their corresponding average generation
df_train['BM2_Predictions'] = df_train.apply(lambda row: city_capacity_avg_gen.get((row['City'], row['Panel_Capacity'])), axis=1)
df_test['BM2_Predictions'] = df_test.apply(lambda row: city_capacity_avg_gen.get((row['City'], row['Panel_Capacity'])), axis=1)

# If there are still NaN values, it means those cities did not appear in the training set. Fill these with the overall average.
df_test['BM2_Predictions'] = df_test['BM2_Predictions'].fillna(np.mean(y_train))

# Calculate MSE for the Benchmark Model 2 on the test set
benchmark2_mse = mean_squared_error(df_test['Generation'], df_test['BM2_Predictions'])
benchmark2_mse

# Create a dictionary with city and panel capacity as keys and average generation for that city and capacity as values
city_capacity_avg_gen = df_tv.groupby(['City', 'Panel_Capacity'])['Generation'].mean().to_dict()

# Fill NaN values in the 'BM2_Predictions' column with the city average generation
df_test['BM2_Predictions'] = df_test['BM2_Predictions'].fillna(df_test['City'].map(city_avg_gen))

# If there are still NaN values, it means those cities did not appear in the training set. Fill these with the overall average.
df_test['BM2_Predictions'] = df_test['BM2_Predictions'].fillna(np.mean(y_train))

# Map city names and panel capacity in the training and testing data to their corresponding average generation
df_tv['BM2_Predictions'] = df_tv.set_index(['City', 'Panel_Capacity']).index.map(city_capacity_avg_gen)
df_test['BM2_Predictions'] = df_test.set_index(['City', 'Panel_Capacity']).index.map(city_capacity_avg_gen)

# Calculate MSE for the Benchmark Model 2 on the test set
benchmark2_mse = mean_squared_error(df_test['Generation'], df_test['BM2_Predictions'])
benchmark2_mse