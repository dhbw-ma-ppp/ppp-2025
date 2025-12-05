# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error
import joblib

# Load the dataset
data = pd.read_csv('StudentPerformanceFactors.csv')

# Drop rows with missing target values
data.dropna(subset=['Exam_Score'], inplace=True)

# Separate target variable
X = data.drop('Exam_Score', axis=1)
y = data['Exam_Score']

# Identify categorical and numerical features
categorical_features = X.select_dtypes(include=['object', 'bool']).columns
numerical_features = X.select_dtypes(include=['int64', 'float64']).columns

# Handle missing values in features
for col in numerical_features:
    if X[col].isnull().any():
        X[col].fillna(X[col].median(), inplace=True)
for col in categorical_features:
    if X[col].isnull().any():
        X[col].fillna(X[col].mode()[0], inplace=True)

# --- Model Evaluation with Train/Test Split ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Create a preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough'
)

# Create the model pipeline
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Train the model on the training data
model_pipeline.fit(X_train, y_train)

# Make predictions on the test data
y_pred = model_pipeline.predict(X_test)

# Calculate evaluation metrics
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("--- Model Evaluation ---")
print(f'R² Score: {r2:.4f}')
print(f'Root Mean Squared Error (RMSE): {rmse:.4f}')

# --- Retrain on Full Data and Save Artifacts for Web App ---

# Retrain the model on the entire dataset to make the best use of the data
model_pipeline.fit(X, y)
print("\n--- Retraining on full dataset for deployment ---")

# Get feature importances
ohe_feature_names = model_pipeline.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(categorical_features)
all_feature_names = np.concatenate([numerical_features, ohe_feature_names])
importances = model_pipeline.named_steps['regressor'].feature_importances_

# Create a dictionary of feature importances
feature_importance_dict = dict(zip(all_feature_names, importances))

# Save the trained model pipeline
joblib.dump(model_pipeline, 'student_performance_model.joblib')
print("Model saved as 'student_performance_model.joblib'")

# Save model columns
joblib.dump(X.columns, 'model_columns.joblib')
print("Model columns saved as 'model_columns.joblib'")

# Save evaluation metrics and feature importances
joblib.dump({'r2': r2, 'rmse': rmse}, 'evaluation_metrics.joblib')
print("Evaluation metrics saved as 'evaluation_metrics.joblib'")
joblib.dump(feature_importance_dict, 'feature_importances.joblib')
print("Feature importances saved as 'feature_importances.joblib'")