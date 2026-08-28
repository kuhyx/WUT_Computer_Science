#!/usr/bin/env python3
"""Program that predicts wine quality based on variant2.csv data."""

import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(message)s", level=logging.INFO)


class LinearRegression:
    """Implements Linear regression method."""

    def __init__(self) -> None:
        """Start with no fitted coefficients."""
        self.theta = None

    def fit(self, x_values: object, y_values: object) -> None:
        """Fit linear regression model to our training data."""
        # Add a column of ones to X for the intercept term
        x_values = np.concatenate((np.ones((x_values.shape[0], 1)), y_values), axis=1)

        # Compute the least squares solution using the normal equation
        self.theta = (
            np.linalg.inv(x_values.T.dot(x_values)).dot(x_values.T).dot(y_values)
        )

    def predict(self, x_values: object) -> object:
        """Predict the target values for the given inputs.

        Uses the trained linear regression

            model.
        """
        # Add a column of ones to X for the intercept term
        x_values = np.concatenate((np.ones((x_values.shape[0], 1)), x_values), axis=1)

        # Make predictions using the learned weights
        return x_values.dot(self.theta)

    def score(self, x_values: object, y_values: object) -> float:
        """Compute the R-squared score of the model.

        Measured on our test"
            " data.
        """
        y_predicted = self.predict(x_values)
        ss_res = np.sum((y_values - y_predicted) ** 2)
        ss_tot = np.sum((y_values - np.mean(y_values)) ** 2)
        return 1 - (ss_res / ss_tot)


wine_df = pd.read_csv("variant2.csv")
wine_df.head()
wine_df.describe()
wine_df.info()


X = wine_df.iloc[:, :-1].to_numpy()
y = wine_df.iloc[:, -1].to_numpy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
regressor = LinearRegression()
regressor.fit(X_train, y_train)

y_pred = regressor.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
logger.info("MSE: %s", mse)
classifier = LogisticRegression()
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
logger.info("Accuracy: %s", accuracy)
y_pred_train = regressor.predict(X_train)

train_mse = mean_squared_error(y_train, y_pred_train)
logger.info("Training MSE: %s", train_mse)

train_r_squared = regressor.score(X_train, y_train)
logger.info("Training R^2: %s", train_r_squared)

test_r_squared = regressor.score(X_test, y_test)
logger.info("Testing R^2: %s", test_r_squared)
y_pred_train = classifier.predict(X_train)

train_accuracy = accuracy_score(y_train, y_pred_train)
logger.info("Training Accuracy: %s", train_accuracy)

train_f1_score = f1_score(y_train, y_pred_train, average="weighted")
logger.info("Training F1 Score: %s", train_f1_score)

test_f1_score = f1_score(y_test, y_pred, average="weighted")
logger.info("Testing F1 Score: %s", test_f1_score)

Data1 = sns.countplot(x="quality", data=wine_df)
plt.draw()
plt.waitforbuttonpress(0)
plt.close()
Data2 = sns.heatmap(wine_df.corr(), annot=True)
plt.draw()
plt.waitforbuttonpress(0)
plt.close()
