import sklearn
import pandas as pd
import plotnine as p9
from pathlib import Path


# --- Daten laden (robust gegenüber aktuellem Arbeitsverzeichnis) ---
repo_root = Path(__file__).resolve().parents[1]
csv_path = repo_root / "data" / "titanic.csv"
df = pd.read_csv("data\\titanic.csv")


# --- Modelltraining: Vorverarbeitung, GridSearch, Eval (MCC) ---
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import matthews_corrcoef, classification_report

# Features & Ziel
features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
target = 'Survived'

X = df[features].copy()
y = df[target].copy()

# Spalten für Pipelines
num_cols = ['Age', 'SibSp', 'Parch', 'Fare']
cat_cols = ['Pclass', 'Sex', 'Embarked']

# Numerische Pipeline: Median-Imputation + Skalierung
num_pipe = Pipeline([
    ('imputer', SimpleImputer(strategy='median')), # behandelt fehlende Werte
    ('scaler', StandardScaler())
])

# Kategoriale Pipeline: häufigsten Wert imputieren + OneHot
cat_pipe = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore')) # splittet in mehrere Spalten auf damit bsw. geschlecht als zwei spalten interpretiert werden kann, sodass man = 1 und frau = 0
])

preproc = ColumnTransformer([
    ('num', num_pipe, num_cols),
    ('cat', cat_pipe, cat_cols)
])

# Train-Test-Split (stratifiziert)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
print('Train size:', X_train.shape, 'Test size:', X_test.shape)

# Pipeline + GridSearch (RandomForest)
pipe = Pipeline([('preproc', preproc), ('clf', RandomForestClassifier(random_state=42))])
param_grid = {
    'clf__n_estimators': [50, 100],
    'clf__max_depth': [5, 10, None],
    'clf__min_samples_split': [2, 5]
}

grid = GridSearchCV(pipe, param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=1)
grid.fit(X_train, y_train)
best = grid.best_estimator_
print('Best params:', grid.best_params_)

# Vorhersage und MCC
y_pred = best.predict(X_test)
mcc = matthews_corrcoef(y_test, y_pred)
print(f'Matthews correlation coefficient (Test): {mcc:.4f}')
print('\nClassification report:')
print(classification_report(y_test, y_pred))


#       Best params: {'clf__max_depth': 10, 'clf__min_samples_split': 5, 'clf__n_estimators': 100}
#        Matthews correlation coefficient (Test): 0.6291
#
#        Classification report:
#                    precision    recall  f1-score   support
#
#                0       0.82      0.92      0.87       110
#                1       0.84      0.68      0.75        69
#
#            accuracy                           0.83       179
#           macro avg       0.83      0.80      0.81       179
#        weighted avg       0.83      0.83      0.82       179