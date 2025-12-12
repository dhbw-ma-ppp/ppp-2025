import pandas as pd
import numpy as np
import seaborn as sns
import sklearn.tree as tree
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.pipeline import Pipeline
import time

#Daten laden und erste Übersicht
data = pd.read_csv('StudentPerformanceFactors.csv')
print("Daten-Dimensionen:", data.shape)
print("Erste Zeilen der Daten:")
print(data.head())

#String-Werte in Integer-Werte umwandeln
string_columns = data.select_dtypes(include=["object"]).columns
label_encoders = {}

for col in string_columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])  # einfache Label-Encoding (schnell)
    label_encoders[col] = le

print("Daten nach Umwandlung von String-Werten:")
print(data.head())

#Fehlende Werte behandeln
print("Anzahl fehlender Werte pro Spalte:")
print(data.isnull().sum())
data = data.dropna()  # schnelle Behandlung: Zeilen entfernen


x = data.drop(columns=["Exam_Score"])
y = data["Exam_Score"]

#Daten in Trainings- und Testdaten aufteilen
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=8)

#Modell Vergleich mit Hyperparameter-Suche
models = {
    "LinearRegression": {
        "pipeline": Pipeline([("scaler", StandardScaler()), ("lr", LinearRegression())]),
        "search": None  # keine Hyperparam-Suche nötig
    },
    "SVR": {
        "pipeline": Pipeline([("scaler", StandardScaler()), ("svr", SVR())]),
        # RandomizedSearch mit begrenzter Anzahl an Kombinationen (schneller als vollständiges Grid)
        "param_dist": {
            "svr__kernel": ["rbf", "linear", "poly"],
            "svr__C": [0.1, 1, 10, 50, 100],
            "svr__gamma": ["scale", "auto"],
            "svr__epsilon": [0.1, 0.2, 0.5]
        },
        "n_iter": 20
    },
    "RandomForest": {
        "pipeline": Pipeline([("scaler", StandardScaler()), ("rf", RandomForestRegressor(random_state=8))]),
        "param_dist": {
            "rf__n_estimators": [50, 100, 200],
            "rf__max_depth": [None, 5, 10, 20],
            "rf__min_samples_split": [2, 5, 10]
        },
        "n_iter": 20
    }
}

#RandomizedSearch/fit für jedes Modell
best_models = {}
start_all = time.time()
for name, info in models.items():
    print(f"Training {name}...")
    if info.get("search") is None and info.get("param_dist") is None:
        # Kein Search: direkt fitten (LinearRegression)
        t0 = time.time()
        info["pipeline"].fit(x_train, y_train)
        t1 = time.time()
        best_models[name] = {
            "best_estimator": info["pipeline"],
            "best_params": {},
            "best_score": None,
            "fit_time": t1 - t0
        }
    else:
        param_dist = info["param_dist"]
        n_iter = info.get("n_iter", 20)
        # RandomizedSearchCV: schneller, liefert oft vergleichbar gute Ergebnisse
        search = RandomizedSearchCV(
            estimator=info["pipeline"],
            param_distributions=param_dist,
            n_iter=n_iter,
            scoring="neg_mean_squared_error",  # direkt MSE optimieren
            cv=3,  # weniger folds = schneller, guter Kompromiss
            random_state=8,
            n_jobs=-1,
            verbose=0
        )
        t0 = time.time()
        search.fit(x_train, y_train)
        t1 = time.time()
        best_models[name] = {
            "best_estimator": search.best_estimator_,
            "best_params": search.best_params_,
            "best_score": search.best_score_,
            "fit_time": t1 - t0
        }
        print(f"{name} beste params: {search.best_params_}, Zeit: {t1 - t0:.1f}s")

end_all = time.time()
print(f"Gesamte Suchdauer: {end_all - start_all:.1f}s")


valid_models = {k: v for k, v in best_models.items() if v["best_score"] is not None}
if valid_models:
    best_model_name = max(valid_models, key=lambda name: valid_models[name]["best_score"])
else:
    # Fallback: erstes Modell
    best_model_name = list(best_models.keys())[0]

best_model = best_models[best_model_name]["best_estimator"]

print(f"\nBestes Modell insgesamt: {best_model_name}")
print(f"Beste Parameter: {best_models[best_model_name].get('best_params')}")
print(f"Beste (neg) MSE: {best_models[best_model_name].get('best_score')}")
print(f"Fit-Zeit: {best_models[best_model_name].get('fit_time')}s")

# Vorhersagen mit dem besten Modell
y_pred = best_model.predict(x_test)
y_pred = np.clip(y_pred, 0, 100)

tolerance = 2
lower_bound = np.clip(y_pred - tolerance, 0, 100)
upper_bound = np.clip(y_pred + tolerance, 0, 100)

print("Mean Squared Error (MSE):", mean_squared_error(y_test, y_pred))
print("Mean Absolute Error (MAE):", mean_absolute_error(y_test, y_pred))
print("R²-Score:", r2_score(y_test, y_pred))

results = pd.DataFrame({
    "Actual": y_test,
    "Prediction": y_pred,
    "Lower_Bound": lower_bound,
    "Upper_Bound": upper_bound,
    "Difference": y_test - y_pred
})

print("Ergebnisse:")
print(results.head())
