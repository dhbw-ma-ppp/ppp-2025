import pandas as pd
import numpy as np
import seaborn as sns
import sklearn.tree as tree
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

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

# --- 6. Entscheidungsbaum-Regressionsmodell trainieren ---
regressor = tree.DecisionTreeRegressor(random_state=8)
regressor.fit(x_train, y_train)

# --- 7. Vorhersagen und Ergebnisse ---
y_pred = regressor.predict(x_test)

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
