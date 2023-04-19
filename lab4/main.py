import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, mean_squared_error

filename = '/home/kuchy/EARIN/lab4/variant2.csv'

# Load the dataset
wine_data = pd.read_csv(filename)

# Split into features and labels
X = wine_data.drop("quality", axis=1)
y = wine_data["quality"]

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Linear Regression
lin_reg = LinearRegression()
lin_reg.fit(X_train, y_train)
y_pred_lin = lin_reg.predict(X_test)
lin_reg_rmse = mean_squared_error(y_test, y_pred_lin, squared=False)

# Logistic Regression
log_reg = LogisticRegression(multi_class='multinomial', solver='newton-cg')
log_reg.fit(X_train, y_train)
y_pred_log = log_reg.predict(X_test)
log_reg_accuracy = accuracy_score(y_test, y_pred_log)

# SVM
svm = SVC()
svm.fit(X_train, y_train)
y_pred_svm = svm.predict(X_test)
svm_accuracy = accuracy_score(y_test, y_pred_svm)

# Compare performance
print("Linear Regression RMSE:", lin_reg_rmse)
print("Logistic Regression accuracy:", log_reg_accuracy)
print("SVM accuracy:", svm_accuracy)
