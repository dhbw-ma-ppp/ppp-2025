import pandas as pd
import numpy as np
import seaborn as sns
import sklearn.tree as tree
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR

# --- 1. Daten laden und erste Übersicht ---
data = pd.read_csv("C:/Users/anst_ma/Desktop/StudentPerformanceFactors.csv")
print("Daten-Dimensionen:", data.shape)
print("Erste Zeilen der Daten:")
print(data.head())

# --- 2. String-Werte in Integer-Werte umwandeln ---
string_columns = data.select_dtypes(include=["object"]).columns
label_encoders = {}

for col in string_columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le  # Encoder speichern, falls Rücktransformation nötig

print("Daten nach Umwandlung von String-Werten:")
print(data.head())

# --- 3. Fehlende Werte behandeln ---
print("Anzahl fehlender Werte pro Spalte:")
print(data.isnull().sum())
data = data.dropna()  # Zeilen mit fehlenden Werten entfernen

# --- 4. Features und Zielvariable definieren ---
x = data.drop(columns=["Exam_Score"])  # Eingabevariablen
y = data["Exam_Score"]  # Zielvariable

# --- 5. Daten in Trainings- und Testdaten aufteilen ---
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=8)

# --- 6. Modelle und Hyperparameter definieren ---
models = {
    "LinearRegression": {
        "model": LinearRegression(),
        "param_grid": {},  # Keine Hyperparameter für GridSearch
    },
    "SVR": {
        "model": SVR(),
        "param_grid": {
            "kernel": ["linear", "poly", "rbf"],  # Sinnvolle Kernel für Regression
            "degree": [2, 3, 4],  # Nur für 'poly' relevant
            "gamma": ["scale", "auto"],  # Steuerung der Einflussweite
            "C": [0.1, 1, 10, 100],  # Regularisierungsparameter
            "epsilon": [0.1, 0.2, 0.5],  # Toleranz für Fehler
        },
    },
}

# --- 7. GridSearch für jedes Modell ---
best_models = {}
for model_name, model_info in models.items():
    print(f"Training {model_name}...")
    grid_search = GridSearchCV(
        estimator=model_info["model"],
        param_grid=model_info["param_grid"],
        scoring={"neg_mse": "neg_mean_squared_error", "r2": "r2"},  # Bewertungsmetriken: MSE und R²
        refit="neg_mse",  # Standardmäßig wird das Modell mit dem besten MSE ausgewählt
        cv=5,  # 5-fache Kreuzvalidierung
        n_jobs=-1  # Parallelverarbeitung
    )
    grid_search.fit(x_train, y_train)
    best_models[model_name] = {
        "best_estimator": grid_search.best_estimator_,
        "best_params": grid_search.best_params_,
        "best_neg_mse": grid_search.cv_results_["mean_test_neg_mse"][grid_search.best_index_],
        "best_r2": grid_search.cv_results_["mean_test_r2"][grid_search.best_index_],
    }
    print(f"Bestes Modell für {model_name}: {grid_search.best_estimator_}")
    print(f"Beste Parameter für {model_name}: {grid_search.best_params_}")
    print(f"Beste MSE (negativ): {best_models[model_name]['best_neg_mse']}")
    print(f"Beste R²-Score: {best_models[model_name]['best_r2']}")

# --- 8. Ergebnisse des besten Modells testen ---
# Wähle das Modell mit dem besten Score (basierend auf MSE)
best_model_name = max(best_models, key=lambda name: best_models[name]["best_neg_mse"])
best_model = best_models[best_model_name]["best_estimator_"]

print(f"\nBestes Modell insgesamt: {best_model_name}")
print(f"Beste Parameter: {best_models[best_model_name]['best_params']}")
print(f"Beste MSE (negativ): {best_models[best_model_name]['best_neg_mse']}")
print(f"Beste R²-Score: {best_models[best_model_name]['best_r2']}")

# Vorhersagen mit dem besten Modell
y_pred = best_model.predict(x_test)

# Optional: Vorhersagen auf einen Zielbereich beschränken (z. B. 0 bis 100)
y_pred = np.clip(y_pred, 0, 100)

# Bereich mit ±3 berechnen
tolerance = 2
lower_bound = np.clip(y_pred - tolerance, 0, 100)  # Untere Grenze (mindestens 0)
upper_bound = np.clip(y_pred + tolerance, 0, 100)  # Obere Grenze (höchstens 100)

# Ergebnisse anzeigen
print("Mean Squared Error (MSE):", mean_squared_error(y_test, y_pred))
print("Mean Absolute Error (MAE):", mean_absolute_error(y_test, y_pred))
print("R²-Score:", r2_score(y_test, y_pred))
# Aktuell mse: -5.2857 r2: 0.655

# Ergebnisse als DataFrame zusammenfassen
results = pd.DataFrame({
    "Actual": y_test,
    "Prediction": y_pred,
    "Lower_Bound": lower_bound,
    "Upper_Bound": upper_bound,
    "Difference": y_test - y_pred
})

print("Ergebnisse:")
print(results.head())
