#For this weeks exercise you need to analyse a dataset
#and prepare a machine learning model to predict a property of that dataset. 
#The dataset is the data on Titanic passengers and can be found in the data folder.

#There are two parts to todays exercise:
#- Analyse and visualize the data. Look for missing values and for correlations between features,
#  as well as between feature and target. Prepare a brief report with some visualisations of the data,
#  and with a summary of what you observed. This can be a jupyter notebok, some other document,
#  or just part of the PR description with images pasted into it.
#- Train an ML model that will predict for any passenger whether they will survive.
#  Determine whether this is a classification or regression task, and use an appropriate model.
#  Spend some time on optimizing the algorithm and hyperparameters. 
#  Report the matthews correlation coefficient calculated on a test set as part of your submission. 


#Part 2 - machine-learning model:


import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split 
from sklearn.metrics import accuracy_score, matthews_corrcoef
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelEncoder


if __name__=='__main__':

    print(10*"="+"Exercise-06"+10*"=")
    print("\n")

#Lesen
    df=pd.read_csv("data/titanic.csv")

#Bereinigen der Daten aufgrund der Analyse und Betrachtung der Daten
    df=df.drop(columns=["Ticket", "PassengerId", "Cabin"])
    mean_fare=df["Fare"].mean()
    df["Fare"] = df["Fare"].fillna(mean_fare)
    mean_age=df["Age"].mean()
    df["Age"]=df["Age"].fillna(mean_age)
    #die 2 fehlenden Werte in Embarked auffüllen
    most_embarked_in = df["Embarked"].mode()[0] #häufigster wert
    df['Embarked'] = df['Embarked'].fillna(most_embarked_in)

#Konvertierung von Sex und Embarked zu Zahlen
    df["Sex"] = df["Sex"].map({"male": 0, "female": 1})
    le = LabelEncoder()
    df["Embarked"] = le.fit_transform(df["Embarked"])

#Describe:
    print("\nBeschreibung nach Bereinigen:")
    print(df.describe())
    print("\n")

#seperate feature and target
    x = df.drop(columns=['Survived', 'Name']) 
    y = df['Survived']

#train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y, random_state=42) 

#classifier
    classifier = RandomForestClassifier(random_state=42) 
# training the classifier
    classifier.fit(x_train, y_train)

#make predictions
    y_pred1 = classifier.predict(x_test)

#test accuracy
    print(f"Accuracy {accuracy_score(y_test, y_pred1):.4f}")
    print(f"matthews corrcoef {matthews_corrcoef(y_test, y_pred1):.4f}")
    

#Optimierung mit GridSearchCV und Random Forest
    print(20*"=")
    print("\nOptimierung GridSearchCV:\n")

    param_grid = {
        'n_estimators': [100, 125, 150, 200],
        'max_depth': [None, 3, 4, 5, 6, 8],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 5]
    }

    print("Starte Training mit GridSearch...")
    grid = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5, scoring='matthews_corrcoef', n_jobs=-1)
    grid.fit(x_train, y_train)

    best_model = grid.best_estimator_
    print(f"Beste Parameter: {grid.best_params_}")

    # 6. Prediction 
    y_pred2 = best_model.predict(x_test)

    # 7. Evaluation
    print("\n--- Ergebnisse ---")
    print(f"Accuracy:          {accuracy_score(y_test, y_pred2):.4f}")
    print(f"Matthews CorrCoef: {matthews_corrcoef(y_test, y_pred2):.4f}")
    print(f"Bester CV-Score: {grid.best_score_:.4f}")