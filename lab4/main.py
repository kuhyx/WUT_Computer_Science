"""
Program that predicts wine quality based on variant2.csv data
"""
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score, f1_score
from sklearn.linear_model import LogisticRegression


class LinearRegression:
    """Implements Linear regression method"""

    def __init__(self):
        self.theta = None

    def fit(self, x_values, y_values):
        """
        Fit linear regression model to our training data
        """
        # Add a column of ones to X for the intercept term
        x_values = np.concatenate((np.ones((x_values.shape[0], 1)), y_values), axis=1)

        # Compute the least squares solution using the normal equation
        self.theta = (
            np.linalg.inv(x_values.T.dot(x_values)).dot(x_values.T).dot(y_values)
        )

    def predict(self, x_values):
        """
        Predict target values for our input data using the trained linear regression model.
        """
        # Add a column of ones to X for the intercept term
        x_values = np.concatenate((np.ones((x_values.shape[0], 1)), x_values), axis=1)

        # Make predictions using the learned weights
        y_predicted = x_values.dot(self.theta)

        return y_predicted

    def score(self, x_values, y_values):
        """
        Compute the R-squared score of the linear regression model on our test data.
        """
        y_predicted = self.predict(x_values)
        ss_res = np.sum((y_values - y_predicted) ** 2)
        ss_tot = np.sum((y_values - np.mean(y_values)) ** 2)
        r2_score = 1 - (ss_res / ss_tot)

        return r2_score


wine_df = pd.read_csv("variant2.csv")
wine_df.head()
wine_df.describe()
wine_df.info()


X = wine_df.iloc[:, :-1].values
y = wine_df.iloc[:, -1].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

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
