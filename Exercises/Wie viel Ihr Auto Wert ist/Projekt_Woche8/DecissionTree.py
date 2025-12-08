import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from data_selection import x, y
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

def train_decision_tree():
    model = DecisionTreeRegressor(random_state=42, max_depth=10)
    model.fit(x_train, y_train)
    return model, x_train, x_test, y_train, y_test

if __name__ == "__main__":
    model, x_train, x_test, y_train, y_test = train_decision_tree()
    y_pred = model.predict(x_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Decision Tree MSE: {mse:.4f}, RMSE: {mse**0.5:.4f}")
