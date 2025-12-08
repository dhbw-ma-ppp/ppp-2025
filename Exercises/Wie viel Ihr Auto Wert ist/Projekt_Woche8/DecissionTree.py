import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from data_selection import x, y
from sklearn.model_selection import train_test_split

import joblib
import os
from sys import path as system_paths

MODEL_FILE_PATH = os.path.join(system_paths[0], "Model_Data", 'DecissionTree.pkl')

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

if __name__ == "__main__" and os.path.exists(MODEL_FILE_PATH):
    os.remove(MODEL_FILE_PATH)

if os.path.exists(MODEL_FILE_PATH):
    print("Load model from: {MODEL_FILE_PATH}")

    model = joblib.load(MODEL_FILE_PATH)
else:
    print("Train model...")

    model = DecisionTreeRegressor(random_state=42, max_depth=10)
    model.fit(x_train, y_train)

    joblib.dump(model, MODEL_FILE_PATH)

y_pred = model.predict(x_test)

mse = mean_squared_error(y_test, y_pred)
feature_importance_df = pd.DataFrame({'Feature': x.columns, 'Importance': model.feature_importances_})


if __name__ == "__main__":
    print(f"Mean Squared Error: {mse:.4f}")
    print(f"Mean Squared Error: {mse**0.5:.4f}")
    print(feature_importance_df)
