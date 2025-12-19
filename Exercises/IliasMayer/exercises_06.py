# For this weeks exercise you need to analyse a dataset and prepare a machine learning model
# to predict a property of that dataset. The dataset is the data on Titanic passengers and can be found in the data folder.
# 
# There are two parts to todays exercise:
# - Analyse and visualize the data. Look for missing values and for correlations between features, as well as between feature and target. Prepare a brief report with some visualisations of the data, and with a summary of what you observed. This can be a jupyter notebok, some other document, or just part of the PR description with images pasted into it.
# - Train an ML model that will predict for any passenger whether they will survive. Determine whether this is a classification or regression task, and use an appropriate model. Spend some time on optimizing the algorithm and hyperparameters. Report the matthews correlation coefficient calculated on a test set as part of your submission.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import matthews_corrcoef

# Daten laden
df = pd.read_csv('data/titanic.csv')

# ============================================
# TEIL 1: DATENANALYSE UND VISUALISIERUNG
# ============================================

print("=" * 60)
print("TEIL 1: DATENANALYSE")
print("=" * 60)

# Fehlende Werte
print("\nFehlende Werte:")
print(df.isnull().sum())

# Korrelationen
print("\nKorrelationen mit Survived:")
print(df.corr(numeric_only=True)['Survived'].sort_values(ascending=False))

# Visualisierungen
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 1. Überlebensrate nach Geschlecht
sns.barplot(data=df, x='Sex', y='Survived', ax=axes[0, 0])
axes[0, 0].set_title('Überlebensrate nach Geschlecht')

# 2. Überlebensrate nach Klasse
sns.barplot(data=df, x='Pclass', y='Survived', ax=axes[0, 1])
axes[0, 1].set_title('Überlebensrate nach Klasse')

# 3. Altersverteilung
df[df['Survived']==1]['Age'].hist(bins=30, alpha=0.5, label='Überlebt', ax=axes[1, 0])
df[df['Survived']==0]['Age'].hist(bins=30, alpha=0.5, label='Nicht überlebt', ax=axes[1, 0])
axes[1, 0].set_title('Altersverteilung')
axes[1, 0].legend()

# 4. Korrelations-Heatmap
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', ax=axes[1, 1])
axes[1, 1].set_title('Korrelations-Heatmap')

plt.tight_layout()
plt.show()

print("\nBeobachtungen:")
print("- Frauen hatten eine deutlich höhere Überlebensrate")
print("- 1. Klasse Passagiere überlebten häufiger")
print("- Cabin hat zu viele fehlende Werte (nicht nutzbar)")
print("- Age korreliert negativ mit Überleben")

# ============================================
# TEIL 2: MACHINE LEARNING MODELL
# ============================================

print("\n" + "=" * 60)
print("TEIL 2: ML MODELL TRAINING")
print("=" * 60)

# Daten vorbereiten
data = df.copy()

# Unwichtige Spalten entfernen
data = data.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1)

# Fehlende Werte füllen
data['Age'].fillna(data['Age'].median(), inplace=True)
data['Embarked'].fillna(data['Embarked'].mode()[0], inplace=True)
data['Fare'].fillna(data['Fare'].median(), inplace=True)

# Kategorische Variablen kodieren
le = LabelEncoder()
data['Sex'] = le.fit_transform(data['Sex'])
data['Embarked'] = le.fit_transform(data['Embarked'])

# Features und Target
X = data.drop('Survived', axis=1)
y = data['Survived']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modell trainieren (Random Forest)
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    random_state=42
)

model.fit(X_train, y_train)

# Vorhersage
y_pred = model.predict(X_test)

# Matthews Correlation Coefficient
mcc = matthews_corrcoef(y_test, y_pred)

print(f"\nMatthews Correlation Coefficient (MCC): {mcc:.4f}")
print(f"Accuracy: {model.score(X_test, y_test):.4f}")

# Feature Importance
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\nFeature Importance:")
print(feature_importance)
