import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor, plot_tree
import matplotlib.pyplot as plt
from data_selection import x_test, x_train, y_test, y_train, x

# Entscheidungsbaum-Regression
model = DecisionTreeRegressor(random_state=42, max_depth=10)
model.fit(x_train, y_train)
y_pred = model.predict(x_test)

if __name__ == "__main__" and False:
    plt.figure(figsize=(12,8))
    plot_tree(model, feature_names=x.columns, filled=True, rounded=True)
    plt.title("Entscheidungsbaum")
    plt.show()


mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.4f}")
print(f"Mean Squared Error: {mse**0.5:.4f}")


importances = model.feature_importances_
feature_importance_df = pd.DataFrame({'Feature': x.columns, 'Importance': importances})

print(feature_importance_df)