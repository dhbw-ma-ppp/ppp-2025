#For this weeks exercise you need to analyse a dataset and prepare a machine learning model to predict a property of that dataset. The dataset is the data on Titanic passengers and can be found in the data folder.

#There are two parts to todays exercise:
#- Analyse and visualize the data. Look for missing values and for correlations between features, as well as between feature and target. Prepare a brief report with some visualisations of the data, and with a summary of what you observed. This can be a jupyter notebok, some other document, or just part of the PR description with images pasted into it.
#- Train an ML model that will predict for any passenger whether they will survive. Determine whether this is a classification or regression task, and use an appropriate model. Spend some time on optimizing the algorithm and hyperparameters. Report the matthews correlation coefficient calculated on a test set as part of your submission. 

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier # Modellwechsel hier
from sklearn.metrics import matthews_corrcoef
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

#First Task with analysis und visualisation of the data

df = pd.read_csv('C:/Users/X1 Yoga/OneDrive/Dokumente/DHBW/Python/Programme/titanic.csv')
print(df.head())

#   PassengerId  Survived  Pclass                                               Name     Sex  ...  Parch            Ticket     Fare Cabin  Embarked
#0            1         0       3                            Braund, Mr. Owen Harris    male  ...      0         A/5 21171   7.2500   NaN         S 
#1            2         1       1  Cumings, Mrs. John Bradley (Florence Briggs Th...  female  ...      0          PC 17599  71.2833   C85         C 
#2            3         1       3                             Heikkinen, Miss. Laina  female  ...      0  STON/O2. 3101282   7.9250   NaN         S 
#3            4         1       1       Futrelle, Mrs. Jacques Heath (Lily May Peel)  female  ...      0            113803  53.1000  C123         S 
#4            5         0       3                           Allen, Mr. William Henry    male  ...      0            373450   8.0500   NaN         S 


#[5 rows x 12 columns]

df.info()

#RangeIndex: 891 entries, 0 to 890
#Data columns (total 12 columns):
#   Column       Non-Null Count  Dtype
#---  ------       --------------  -----
# 0   PassengerId  891 non-null    int64
# 1   Survived     891 non-null    int64
# 2   Pclass       891 non-null    int64
# 3   Name         891 non-null    object
# 4   Sex          891 non-null    object
# 5   Age          714 non-null    float64
# 6   SibSp        891 non-null    int64
# 7   Parch        891 non-null    int64
# 8   Ticket       891 non-null    object
# 9   Fare         891 non-null    float64
# 10  Cabin        204 non-null    object
# 11  Embarked     889 non-null    object
#dtypes: float64(2), int64(5), object(5)

missing_values = df.isnull().sum()
print(missing_values[missing_values > 0])

#Age         177
#Cabin       687
#Embarked      2
#dtype: int64

print("Now there're a few stats in visualized in plots. -> I'll put screenshots in the pullrequest.")

#Survivalrate

plt.figure(figsize=(8,5))
survived_counts = df['Survived'].value_counts().sort_index()
colors = ['#666666', '#CA2E2E'] #grey - not survived, red - survived
plt.bar(survived_counts.index, survived_counts.values, color=colors)
plt.title('Survival Count')
plt.xlabel('Survival Status')
plt.ylabel('Number of Passengers')
plt.xticks([0, 1], ['Did not Survive', 'Survived'])
#plt.show()
print("Comparison whether a passenger survived or not.")
print("Observation: More passengers did not survive than survived.")

colors = ['#5568e3', '#5ff58c'] # Female - blue, Male - green
bar_colors = ['#074584', '#074584', '#074584'] # Pclass 1, 2, 3 / Embarked C, Q, S

# Gender vs. Survived
plt.figure(figsize=(8, 5))
gender_survival = df.groupby('Sex')['Survived'].mean().sort_values() # Sort for consistent color
plt.bar(gender_survival.index, gender_survival.values, color=colors)
plt.title('Survival Rate by Gender')
plt.ylabel('Survival Rate')
#plt.show()
print("A few comparisons between survival rate and other categories.")
print("Observation: Females had a much higher survival rate.")

# Passengerclass vs. Survived
plt.figure(figsize=(8, 5))
pclass_survival = df.groupby('Pclass')['Survived'].mean().sort_index()
plt.bar(pclass_survival.index, pclass_survival.values, color=bar_colors)
plt.title('Survival Rate by Passenger Class')
plt.xlabel('Passenger Class')
plt.ylabel('Survival Rate')
plt.xticks(pclass_survival.index)
#plt.show()
print("Observation: 1st class passengers had a much higher survival rate")

# Age vs. Survived
plt.figure(figsize=(10, 6))
# Get age data for survivors and non-survivors
age_survived = df[df['Survived'] == 1]['Age'].dropna()
age_not_survived = df[df['Survived'] == 0]['Age'].dropna()

plt.hist([age_survived, age_not_survived], 
         bins=30, 
         stacked=True, 
         color=['#666666', '#CA2E2E'], 
         label=['Survived', 'Did not Survive'])
plt.title('Age Distribution by Survival Status')
plt.xlabel('Age')
plt.ylabel('Number of Passengers')
plt.legend()
#plt.show()
print("Observation: Passengers under 40 have a much higher survival rate.")

# Embarked vs. Survived
plt.figure(figsize=(8, 5))
embarked_survival = df.groupby('Embarked')['Survived'].mean().sort_index()
plt.bar(embarked_survival.index, embarked_survival.values, color=bar_colors)
plt.title('Survival Rate by Port of Embarkation')
plt.xlabel('Port (C=Cherbourg, Q=Queenstown, S=Southampton)')
plt.ylabel('Survival Rate')
#plt.show()
print("Observation: Passengers from Cherbourg had a higher survival rate")

numeric_cols = df.select_dtypes(include=np.number).columns
corr_matrix = df[numeric_cols].corr()

print("\nSummary of the Analysis")
print("""
1.  Missing Values:
    Age: ~20% missing. This is a key feature and will need to be imputed (e.g., using the median).
    Cabin: ~77% missing. It's mostly unusable.
    Embarked: Only 2 values missing. We can impute this with the mode most frequent value.

2.  Survival rate summary:
    Sex: Females had a survival rate of over 70%, while males were below 20%.
    P_class: 1st class passengers had a survival rate > 60%, while 3rd class was < 30%.
    Age: Passengers under 40 had a higher survival rate.
    Embarked: Passengers embarking from Cherbourg had a higher survival rate.
""")

#Second Task - Training the ML Modell
y = df['Survived']
X = df[['Pclass', 'Sex', 'Age', 'Fare', 'SibSp', 'Parch', 'Embarked']].copy()

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

numerical_features = ['Age', 'Fare', 'SibSp', 'Parch'] 
categorical_features = ['Pclass', 'Sex', 'Embarked']

numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median'))
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', drop='first'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ],
    remainder='passthrough'
)

dt_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                              ('classifier', DecisionTreeClassifier(random_state=42))])

param_grid = {
    'classifier__max_depth': [3, 5, 8, 10], 
    'classifier__min_samples_split': [5, 10, 15],
    'classifier__min_samples_leaf': [3, 5, 8],
    'classifier__criterion': ['gini', 'entropy']
}

# Grid Search
grid_search = GridSearchCV(dt_pipeline, param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=0)
grid_search.fit(x_train, y_train)

best_model = grid_search.best_estimator_
y_pred = best_model.predict(x_test)

#calculation of MCC
mcc = matthews_corrcoef(y_test, y_pred)

print(f"Best parameter: {grid_search.best_params_}")
print(f"Matthews Correlation Coefficient (MCC) on this test set: {mcc:.4f}")

#The result from the MCC is 0.5809