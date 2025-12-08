# For this weeks exercise you need to analyse a dataset and prepare a machine learning model to 
# predict a property of that dataset. The dataset is the data on Titanic passengers and can be found 
# in the data folder.

# There are two parts to todays exercise:
# - Analyse and visualize the data. Look for missing values and for correlations between features, 
# as well as between feature and target. Prepare a brief report with some visualisations of the data, 
# and with a summary of what you observed. This can be a jupyter notebok, some other document, or 
# just part of the PR description with images pasted into it.
#
# - Train an ML model that will predict for any passenger whether they will survive. Determine 
# whether this is a classification or regression task, and use an appropriate model. Spend some 
# time on optimizing the algorithm and hyperparameters. Report the matthews correlation coefficient 
# calculated on a test set as part of your submission. 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay, matthews_corrcoef
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

df = pd.read_csv(r"C:\Users\hanna\DHBW\1.Semester\Programming and Problemsolving with Python\ppp-2025\data\titanic.csv")

#Age distribution
plt.figure()
plt.hist(df["Age"].dropna(), bins=30)
plt.xlabel("Age")
plt.ylabel("Count")
plt.title("Age Distribution")
plt.savefig("age_distribution.png")

#Survival Rate
surv_rate = df["Survived"].mean()
print(f"Survival Rate: {surv_rate:.3f}")
# Survival Rate: 0.384

#Survival by age
age_survival = df.groupby("Age")["Survived"].mean()
plt.figure()
plt.bar(age_survival.index, age_survival.values)
plt.title("Survival Rate by Age")
plt.ylabel("Survival Rate")
plt.savefig("survival_by_age.png")

#Survival by gender
gender_survival = df.groupby("Sex")["Survived"].mean()
plt.figure()
plt.bar(gender_survival.index, gender_survival.values)
plt.title("Survival Rate by Gender")
plt.ylabel("Survival Rate")
plt.savefig("survival_by_gender.png")

#Survival by class
class_survival = df.groupby("Pclass")["Survived"].mean()
plt.figure()
plt.bar(class_survival.index, class_survival.values)
plt.title("Survival Rate by Class")
plt.ylabel("Survival Rate")
plt.savefig("survival_by_class.png")

#Correlation Heatmap
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
plt.figure(figsize=(10,8))
sns.heatmap(df[num_cols].corr(), annot=True, fmt='.2f', cmap='coolwarm')
plt.title('Correlation Matrix')
plt.tight_layout()
plt.savefig('correlation_heatmap.png')

#Missing Values
plt.figure(figsize=(10,6))
sns.heatmap(df.isnull(), cbar=False)
plt.title("Missing Values Heatmap")
plt.savefig("missing_values_heatmap.png")

#Handling columns with missing values
df['Age'].fillna(df['Age'].median(), inplace=True)
df.drop(columns=['Cabin', 'Embarked'], inplace=True)

#Part 2
#Drop insignificant columns
df.drop(columns=['PassengerId', 'Name', 'Ticket'], inplace=True)
#convert to number
df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
#Split into inputs and target
y = df['Survived']
x = df.drop(columns='Survived')

#Train/Test Split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y, random_state=42)

#Train Decision Tree
titanic_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', tree.DecisionTreeClassifier())
])

#Hyperparameter grid for different classifiers
param_grid = [
    {
        'classifier': [tree.DecisionTreeClassifier(random_state=42)],
        'classifier__max_depth': [3, 5, 7, None],
        'classifier__min_samples_split': [2, 5, 10]
    },
    {
        'classifier': [RandomForestClassifier(random_state=42)],
        'classifier__n_estimators': [50, 100],
        'classifier__max_depth': [3, 5, None],
        'classifier__min_samples_split': [2, 5, 10]
    },
    {
        'classifier': [SGDClassifier(max_iter=1000, tol=1e-3, random_state=42)],
        'classifier__loss': ['hinge', 'log_loss'],
        'classifier__alpha': [1e-3, 1e-4]
    },
]

#Grid search
grid = GridSearchCV(titanic_pipeline, param_grid, n_jobs=1, cv=3, scoring='matthews_corrcoef', verbose=1)
grid.fit(x_train, y_train)
#Show best parameters and model
print("Best params:", grid.best_params_, "\nBest Estimator: ", grid.best_estimator_)

#Evalutaion on test set 
y_pred = grid.predict(x_test)
print("Matthews Correlation Coefficient:", matthews_corrcoef(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))

#Confusion Matrix
ConfusionMatrixDisplay.from_estimator(grid.best_estimator_, x_test, y_test)
plt.savefig("confusion_matrix.png")