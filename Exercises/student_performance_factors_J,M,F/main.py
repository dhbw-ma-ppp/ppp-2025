import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error
import joblib

#Daten laden
data = pd.read_csv('StudentPerformanceFactors.csv')

#Datenvorverarbeitung

# String-Werte mit LabelEncoder umwandeln
string_columns = data.select_dtypes(include=["object"]).columns
label_encoders = {} # Dictionary zum Speichern der Encoder
for col in string_columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

# Fehlende Werte behandeln entfernen
data.dropna(inplace=True)

#Features und Zielvariable definieren
X = data.drop('Exam_Score', axis=1)
y = data['Exam_Score']

#Model in Trainings- und Testdaten aufteilen
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=8)

#Pipeline erstellen
model_pipeline = Pipeline(steps=[
    ('scaler', StandardScaler()),
    ('regressor', LinearRegression())
])

#Modell trainieren und evaluieren
model_pipeline.fit(X_train, y_train)
y_pred = model_pipeline.predict(X_test)

# Metriken berechnen
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("--- Model Evaluation (Linear Regression) ---")
print(f'R² Score: {r2:.4f}')
print(f'Root Mean Squared Error (RMSE): {rmse:.4f}')

# --- 7. Auf kompletten Daten neu trainieren und für die Web App speichern ---
model_pipeline.fit(X, y)
print("\n--- Retraining on full dataset for deployment ---")

# Speichere die Artefakte für die Webanwendung
joblib.dump(model_pipeline, 'student_performance_model.joblib')
print("Model saved as 'student_performance_model.joblib'")

joblib.dump(X.columns, 'model_columns.joblib')
print("Model columns saved as 'model_columns.joblib'")

joblib.dump(label_encoders, 'label_encoders.joblib')
print("Label encoders saved as 'label_encoders.joblib'")

joblib.dump({'r2': r2, 'rmse': rmse}, 'evaluation_metrics.joblib')
print("Evaluation metrics saved as 'evaluation_metrics.joblib'")