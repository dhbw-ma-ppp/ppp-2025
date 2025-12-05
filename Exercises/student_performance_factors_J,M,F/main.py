import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
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
# For simplicity, we'll fill numerical with median and categorical with mode
for col in numerical_features:
    if X[col].isnull().any():
        X[col].fillna(X[col].median(), inplace=True)
for col in categorical_features:
    if X[col].isnull().any():
        X[col].fillna(X[col].mode()[0], inplace=True)

# Create a preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough'
)

# Create the model pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Train the model on the entire dataset
model.fit(X, y)

# Save the trained model pipeline
joblib.dump(model, 'student_performance_model.joblib')
joblib.dump(X.columns, 'model_columns.joblib')


print("Model training complete and saved as 'student_performance_model.joblib'")
print("Model columns saved as 'model_columns.joblib'")

# Example of how to load and predict (for testing)
# loaded_model = joblib.load('student_performance_model.joblib')
# example_data = pd.DataFrame([X.iloc[0]], columns=X.columns)
# prediction = loaded_model.predict(example_data)
# print(f"Example prediction: {prediction[0]}")
# print(f"Actual value: {y.iloc[0]}")
