"""
Program that predicts wine quality based on variant2.csv data
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, accuracy_score, f1_score

wine_df = pd.read_csv("variant2.csv")
wine_df.head()
wine_df.describe()
wine_df.info()


X = wine_df.iloc[:, :-1].values
y = wine_df.iloc[:, -1].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
regressor = LinearRegression()
regressor.fit(X_train, y_train)

y_pred = regressor.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
print("MSE:", mse)
classifier = LogisticRegression()
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
y_pred_train = regressor.predict(X_train)

train_mse = mean_squared_error(y_train, y_pred_train)
print("Training MSE:", train_mse)

train_r_squared = regressor.score(X_train, y_train)
print("Training R^2:", train_r_squared)

test_r_squared = regressor.score(X_test, y_test)
print("Testing R^2:", test_r_squared)
y_pred_train = classifier.predict(X_train)

train_accuracy = accuracy_score(y_train, y_pred_train)
print("Training Accuracy:", train_accuracy)

train_f1_score = f1_score(y_train, y_pred_train, average="weighted")
print("Training F1 Score:", train_f1_score)

test_f1_score = f1_score(y_test, y_pred, average="weighted")
print("Testing F1 Score:", test_f1_score)

Data1 = sns.countplot(x="quality", data=wine_df)
plt.draw()
plt.waitforbuttonpress(0)
plt.close()
Data2 = sns.heatmap(wine_df.corr(), annot=True)
plt.draw()
plt.waitforbuttonpress(0)
plt.close()
