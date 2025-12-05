import pandas as pd

from data import df
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


if __name__ == "__main__":
    print(df.head())
    print(df.info())
df:pd.DataFrame = df

target = "Price"
x = df.drop(target, axis="columns")
y = df[[target]]
print(y.shape)
print(y.head())

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2, random_state=42) # stratify=y.map(int)//1000

from sklearn.tree import DecisionTreeRegressor

import matplotlib.pyplot as plt

# Entscheidungsbaum-Regression
model = DecisionTreeRegressor(random_state=42, max_depth=10)
print("fitting...")
model.fit(x_train, y_train)
print("predicting...")
y_pred = model.predict(x_test)

if __name__ == "__main__":
    print(x_train.shape)
    print(x_test.shape)

"""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, plot_tree
plt.figure(figsize=(12,8))
plot_tree(model, feature_names=x.columns, filled=True, rounded=True)
plt.title("Entscheidungsbaum")
plt.show()
"""

mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.4f}")
print(f"Mean Squared Error: {mse**0.5:.4f}")


importances = model.feature_importances_
feature_importance_df = pd.DataFrame({'Feature': x.columns, 'Importance': importances})

print(feature_importance_df)