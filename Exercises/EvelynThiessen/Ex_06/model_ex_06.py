import pandas as pd
import numpy as np
from draw_data import draw
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn import tree
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import matthews_corrcoef
from sklearn.pipeline import Pipeline
from sklearn import datasets, linear_model

df = pd.read_csv("Exercises/EvelynThiessen/Ex_06/titanic.csv")

y = df['Survived']
x = df.drop(['Survived', 'Name', 'Cabin', 'Ticket'], axis = 1)

def find_optimal_decision_tree():
    pipeline = Pipeline([
        ('classifier', tree.DecisionTreeClassifier())
    ])

    param_grid = [
        {
            'classifier__max_depth': [2,5,10,20, None],
            'classifier__min_samples_split': [2,5,10,20, None], # wie wird der Baum geteilt?
        }
    ]

    grid = GridSearchCV(pipeline, param_grid, n_jobs=4, cv=3, scoring='matthews_corrcoef', verbose=1)
    grid.fit(x_train, y_train)

    grid.best_estimator_.fit(x_train, y_train)
    mc = matthews_corrcoef(y_test, grid.best_estimator_.predict(x_test))

    return mc, grid.best_estimator_

def find_optimal_linear_regressesion():
    regressor = linear_model.LinearRegression()
    regressor.fit(x_train, y_train)

    y_pred = regressor.predict(x_test)

    y_pred_class = np.round(y_pred).astype(int)

    mcc = matthews_corrcoef(y_test, y_pred_class)
    return mcc

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y)

le = LabelEncoder()

for col in x_train.columns:

    if x_train[col].dtype == 'object':
        x_train[col] = le.fit_transform(x_train[col].fillna('missing'))
        x_test[col] = le.transform(x_test[col].fillna('missing'))
    else:
        median = x_train[col].median()
        x_train[col] = x_train[col].fillna(median)
        x_test[col] = x_test[col].fillna(median)
       
mc_tree, best_tree = find_optimal_decision_tree()
mc_regression = find_optimal_linear_regressesion()

if mc_tree > mc_regression:
    print("Der Entscheidungsbaum mit folgenden Werten ist für diesen Datensatz optimal:")
    print(best_tree)
elif mc_tree == mc_regression:
    print("ist nur zufall, eigentlich ist der Binärbaum am besten. Hier die beste optimierung:")
    print(best_tree)

#Da wir nur ja oder Nein werte erwarten ist es eigentlich klar, dass der Decision Tree optimal ist.
#Trotzdem nur auf nummer sicher zu gehen vergleiche ich die Ergebnisse nochmal
# = classification Task :)

draw(df)