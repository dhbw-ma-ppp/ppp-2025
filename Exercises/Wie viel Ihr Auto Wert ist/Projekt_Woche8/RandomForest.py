import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error
from data_selection import x, y

# Daten aufteilen
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Hyperparameter-Pipeline erstellen
model = RandomForestRegressor(random_state=42)

# Parameter, die optimiert werden sollen
param_grid = {
    'n_estimators': [50, 75, 100, 150, 200,220,300,303,340,350,360,375,400], 
    'max_depth': [None, 5,10,15,20, 25,26,27,28,29,30,31,32, 40], 
    'min_samples_split': [1, 2, 3],
    'max_features': ['auto', 'sqrt', 'log2']
}
if False:
    param_grid = {
        'n_estimators': [50, 100, 200], 
        'max_depth': [None, 5,10, 15], 
        'min_samples_split': [2, 3, 5, 10],
        'max_features': ['auto', 'sqrt', 'log2']
    }
if False:
    param_grid = {
        'n_estimators': [100], 
        'max_depth': [10], 
        'min_samples_split': [10],
        'max_features': ['auto', 'sqrt']
    }
param_grid = {
    'n_estimators': [50,100,300,350,400,450], 
    'max_depth': [10,15,20,25,26,27,28,29,None], 
    'min_samples_split': [2, 3],
    'max_features': ['sqrt']
}
# GridSearchCV erstellen
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)
grid_search.fit(x_train, y_train)

# Bestes Modell und Hyperparameter
best_model = grid_search.best_estimator_
best_params = grid_search.best_params_

# Vorhersagen mit dem besten Modell
y_pred = best_model.predict(x_test)

# Metriken ausgeben
if __name__ == '__main__':
    mse = mean_squared_error(y_test, y_pred)
    print(f"Beste Hyperparameter: {best_params}")
    print(f"MSE: {mse:.4f}")
    print(f"RMSE: {mse**0.5:.4f}")

    # Feature Importances anzeigen
    importances = best_model.feature_importances_
    feature_importance_df = pd.DataFrame({'Feature': x.columns, 'Importance': importances})
    # Sortieren nach Importance in absteigender Reihenfolge
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
    print(feature_importance_df)
