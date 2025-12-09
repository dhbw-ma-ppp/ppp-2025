import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from data_selection import x, y

import joblib
import os
from sys import path as system_paths

test_size = 0.05
# size -> RMSE
# 0.07 -> 5775.5982
# 0.06 -> 5670.0744
# 0.04 -> 5283.0084
print(f"The test size is {test_size}")
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=42)

MODEL_FILE_PATH = os.path.join(system_paths[0], "Model_Data", 'random_forest_model.pkl')


if __name__ == "__main__" and os.path.exists(MODEL_FILE_PATH):
    os.remove(MODEL_FILE_PATH)

if os.path.exists(MODEL_FILE_PATH):
    print(f"Load model from: {MODEL_FILE_PATH}")
    model = joblib.load(MODEL_FILE_PATH)
else:
    print("Train model with GridSearchCV...")
    model = RandomForestRegressor(random_state=42)
    # GridSearchCV erstellen
    # Parameter, die optimiert werden sollen
    param_grid = {
        'n_estimators': [50, 75, 100, 150, 200,220,300,303,340,350,360,375,400], 
        'max_depth': [None, 5,10,15,20, 25,26,27,28,29,30,31,32, 40], 
        'min_samples_split': [1, 2, 3],
        'max_features': ['auto', 'sqrt', 'log2']
    }
    param_grid = {
        'n_estimators': [100], 
        'max_depth': [None], 
        'min_samples_split': [2],
        'max_features': ['sqrt']
    }
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)
    grid_search.fit(x_train, y_train.to_numpy().flatten())

    print(f"Beste Hyperparameter beim training des RandomForest sind: {grid_search.best_params_}")
    
    model = grid_search.best_estimator_
    
    joblib.dump(model, MODEL_FILE_PATH, compress=9)

y_pred = y_pred = model.predict(x_test)
feature_importance_df = pd.DataFrame({'Feature': x.columns, 'Importance': model.feature_importances_})
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

if __name__ == '__main__':
    mse = mean_squared_error(y_test, y_pred)
    print(f"MSE: {mse:.4f}")#9000
    print(f"RMSE: {mse**0.5:.4f}")
    mae = mean_absolute_error(y_test, y_pred)
    print(f"MAE: {mae:.4f}")#4800
    r2 = r2_score(y_test, y_pred)
    print(f"R2 score: {r2:.4f}") # 0.7x

    
    y_pred = model.predict(x_train)
    mse = mean_squared_error(y_train, y_pred)

    print(f"MSE(Train): {mse:.4f}")
    print(f"RMSE(Train): {mse**0.5:.4f}")
    
    #print(feature_importance_df)
