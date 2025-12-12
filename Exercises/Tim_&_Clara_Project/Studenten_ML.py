# --- Imports of libarys ---
from ucimlrepo import fetch_ucirepo # type: ignore
import pandas as pd # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.preprocessing import StandardScaler # type: ignore
from sklearn.tree import DecisionTreeClassifier # type: ignore
from sklearn.metrics import accuracy_score # type: ignore
import plotnine as p9 # type: ignore

# --- Printing for Overview ---
print()
print('--------------------------------------')
print()

# --- getting dataset ready ---
print('Getting Data...')
predict_students_dropout_and_academic_success = fetch_ucirepo(id=697)
X = predict_students_dropout_and_academic_success.data.features
y = predict_students_dropout_and_academic_success.data.targets
full_df = pd.concat([X, y], axis=1)

# --- Printing for Overview ---
print()
print('--------------------------------------')
print()

# --- 1. Version Trainingsdata for Students > 2. Semester ---
y_v1 = full_df['Target']
X_v1 = full_df.drop(['Target'], axis=1) # using anything except...
X_v1_train, X_v1_test, y_v1_train, y_v1_test = train_test_split(X_v1, y_v1, test_size=0.2, random_state=42)

# --- 3. Version Trainingsdata for Students < 2. Semester ---
y_v2 = full_df['Target']
X_v2 = full_df.drop(['Target','Curricular units 2nd sem (approved)','Curricular units 2nd sem (without evaluations)','Curricular units 2nd sem (evaluations)','Curricular units 2nd sem (enrolled)','Curricular units 2nd sem (credited)','Curricular units 1st sem (without evaluations)','Curricular units 1st sem (approved)','Curricular units 1st sem (credited)','Curricular units 1st sem (grade)','Curricular units 2nd sem (grade)'], axis=1) # using anything except...
X_v2_train, X_v2_test, y_v2_train, y_v2_test = train_test_split(X_v2, y_v2, test_size=0.2, random_state=42)

# --- Bringing Features on one Level per Standartscale ---
print('Scaling Features...')
scaler = StandardScaler()
scaled_features = ['Previous qualification (grade)','Admission grade','Curricular units 1st sem (grade)','Curricular units 2nd sem (grade)','Unemployment rate','Inflation rate', 'GDP', 'Marital Status','Application mode','Application order', 'Course','Daytime/evening attendance', 'Previous qualification','Nacionality', 'Mother\'s qualification', 'Father\'s qualification', 'Mother\'s occupation', "Father's occupation", 'Displaced', 'Educational special needs', 'Debtor', 'Tuition fees up to date', 'Gender', 'Scholarship holder', 'Age at enrollment', 'International', 'Curricular units 1st sem (credited)', 'Curricular units 1st sem (enrolled)', 'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (approved)', 'Curricular units 1st sem (without evaluations)','Curricular units 2nd sem (credited)', 'Curricular units 2nd sem (enrolled)', 'Curricular units 2nd sem (evaluations)', 'Curricular units 2nd sem (approved)', 'Curricular units 2nd sem (without evaluations)'         ]
full_df[scaled_features] = scaler.fit_transform(full_df[scaled_features])

# --- Printing for Overview ---
print()
print('--------------------------------------')
print()

# --- 1. Verison Random Forest ---
print('Starting 1. Version Random Forest...')
from sklearn.ensemble import RandomForestClassifier
forest_model_v1 = RandomForestClassifier(max_depth= 10, min_samples_split= 5, n_estimators= 200)
forest_model_v1.fit(X_v1_train,y_v1_train)
prediction_v1 = forest_model_v1.predict(X_v1_test)

# --- Printing for Overview ---
print()
print('--------------------------------------')
print()

# --- 2.Version Random Forest ---
print('Starting 2. Version Random Forest....')
from sklearn.ensemble import RandomForestClassifier
forest_model_v2 = RandomForestClassifier(max_depth= 25, min_samples_split= 10, n_estimators= 100)
forest_model_v2.fit(X_v2_train,y_v2_train)
prediction_v2 = forest_model_v2.predict(X_v2_test)

# --- Printing for Overview ---
print()
print('--------------------------------------')
print()

# --- Giving an Output for Version 1 ---
accuracy_v1 = accuracy_score(y_v1_test, prediction_v1)

print(f"Testing Accurancy:{accuracy_v1}")

# --- Testing Overfitting for Version 1 ---
prediction_v1 = forest_model_v1.predict(X_v1_train)
accuracy_v1 = accuracy_score(y_v1_train, prediction_v1)
print(f"Training Accurancy: {accuracy_v1}")


# --- Printing for Overview ---
print()
print('--------------------------------------')
print()

# --- Giving an Output for Version 2 ---
accuracy_v2 = accuracy_score(y_v2_test, prediction_v2)
print(f"Testing Accurancy:{accuracy_v2}")

# --- Testing Overfitting for Version 2 ---
prediction_v2 = forest_model_v2.predict(X_v2_train)
accuracy_v2 = accuracy_score(y_v2_train, prediction_v2)
print(f"Training Accurancy: {accuracy_v2}")

# --- Printing for Overview ---
print()
print('--------------------------------------')
print()