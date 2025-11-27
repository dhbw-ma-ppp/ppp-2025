#For this weeks exercise you need to analyse a dataset and prepare a machine learning model to predict a property of that dataset.
#  The dataset is the data on Titanic passengers and can be found in the data folder.

#There are two parts to todays exercise:
#- Analyse and visualize the data. Look for missing values and for correlations between features, as 
# well as between feature and target. Prepare a brief report with some visualisations of the data, and with 
# a summary of what you observed. This can be a jupyter notebok, some other document, or just part of the PR description 
# with images pasted into it.

#- Train an ML model that will predict for any passenger whether they will survive. Determine whether this is 
# a classification or regression task, and use an appropriate model. Spend some time on optimizing the algorithm 
# and hyperparameters. Report the matthews correlation coefficient calculated on a test set as part of your submission. 


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import matthews_corrcoef
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


try:
    df = pd.read_csv("titanic.csv")
except FileNotFoundError:
    print("Fehler: Die Datei wurde nicht gefunden ")
print(df.head())


print("\nFehlende Werte:")
print(df.isna().sum())

# Überlebensrate
df['Survived'].value_counts().plot(kind='bar')
plt.title("Überlebensverteilung")
plt.xlabel("0 = nicht überlebt | 1 = überlebt")
plt.ylabel("Anzahl")
plt.show()

# Überlebensrate nach Geschlecht
df.groupby("Sex")["Survived"].mean().plot(kind='bar')
plt.title("Überlebensrate nach Geschlecht")
plt.ylabel("Rate")
plt.show()


data = df.copy()

# cabin wird in der analyse nicht mitgezählt, weil sehr viele Werte fehlen
data["HasCabin"] = data["Cabin"].notna().astype(int)


data = data.drop(columns=["PassengerId", "Name", "Ticket", "Cabin"])

# Überall wo alter fehlt, wird median benutzt (Mittelwert)
imputer = SimpleImputer(strategy="median")
data["Age"] = imputer.fit_transform(data[["Age"]])


data["Embarked"] = data["Embarked"].fillna(data["Embarked"].mode()[0])


data = pd.get_dummies(data, columns=["Sex", "Embarked"], drop_first=True) # geschlecht wird in Zahlen umgewandelt 


y = data["Survived"]
X = data.drop(columns=["Survived"])



X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
model = RandomForestClassifier(
    n_estimators=150,
    max_depth=6,
    random_state=42
)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
mcc = matthews_corrcoef(y_test, y_pred)

print("\nMatthews Correlation Coefficient (MCC):", mcc)



