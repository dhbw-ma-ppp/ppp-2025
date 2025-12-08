import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error
from data_selection import x, y

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

def train_random_forest():
    model = RandomForestRegressor(random_state=42)
    param_grid = {
        'n_estimators': [210, 220, 230, 240, 250], 
        'max_depth': [24,25,26], 
        'min_samples_split': [2, 3, 4],
        'max_features': ['sqrt']
    }
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, n_jobs=-1, verbose=0)
    grid_search.fit(x_train, y_train)
    best_model = grid_search.best_estimator_
    return best_model, x_train, x_test, y_train, y_test

if __name__ == "__main__":
    best_model, x_train, x_test, y_train, y_test = train_random_forest()
    y_pred = best_model.predict(x_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Beste Hyperparameter: {grid_search.best_params_}")
    print(f"MSE: {mse:.4f}, RMSE: {mse**0.5:.4f}")