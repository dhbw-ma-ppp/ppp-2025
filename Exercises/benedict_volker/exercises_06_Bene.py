import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path


#creating the visualizations

data = pd.read_csv(Path('./data/titanic.csv').absolute())
passenger_class = data["Pclass"]
passenger_survived = data["Survived"]
passenger_sex = data["Sex"].map(lambda x: 0 if x == "male" else 1)
passenger_Age = data["Age"]


#plt.boxplot(np.array(Y,X))


def plot_survived_vs_not_survived(data):
    data["Age"] = data["Age"].fillna(data["Age"].median())
    survived = data[data["Survived"] == 1]["Age"]
    died = data[data["Survived"] == 0]["Age"]

    plt.boxplot([died, survived])
    plt.xlabel("survival")
    plt.ylabel("age")
    plt.title("Age vs survival")
    plt.show()

def survival_by_class(data):
    class_groups = data.groupby("Pclass")["Survived"].mean()
    plt.bar(class_groups.index, class_groups.values)
    plt.title("Überleben nach Klassse")
    plt.show()

def age_hist(data):
    plt.hist(data["Age"].dropna())
    plt.title("Alterhistogramm aller Passagiere")
    plt.show()

plot_survived_vs_not_survived(data)
survival_by_class(data)
age_hist(data)

#ml-model
from sklearn import linear_model, tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import matthews_corrcoef

class SurvivalRatePredictor:
    def __init__(self, data):
        self._train_model_random_forest(data)

    def _split_data(self):
        x=self.cleaned_data[["Pclass", "Sex", "Age"]]
        y=self.cleaned_data[["Survived"]]

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y, test_size=0.2, stratify=y)

    def _clean_data(self, data):
        data["Sex"] = data["Sex"].map(lambda x: 0 if x == "male" else 1)
        
        average_age = data["Age"].median()
        data["Age"] = data["Age"].fillna(average_age)
        
        data = data[["Pclass", "Sex", "Age", "Survived"]]
        data = data.fillna(0)
        self.cleaned_data = data

#        prediction_data = pd.DataFrame(data["Survived"])
 #       prediction_data = prediction_data.fillna(0)
  #      self.prediction_data = prediction_data

    def _train_model(self, data): # linear regression model
        self._clean_data(data)
        self._split_data()
        self.predictor = linear_model.LinearRegression()
        self.predictor.fit(self.x_train, self.y_train) 
        self.model = "lineare Regression"
    
    def _train_model_random_forest(self, data): # random forest
        self._clean_data(data)
        self._split_data()
        self.predictor = tree.DecisionTreeRegressor(max_depth=22)
        self.predictor.fit(self.x_train, self.y_train) 
        self.model = "random forest"

    def predict(self, pclass, sex, age):
        if sex == "male":
            sex = 0
        else:
            sex = 1
        passenger_attributes = pd.DataFrame({
            "Pclass" : [pclass],
            "Sex" : [sex],
            "Age" : [age]
        })
        
        return self.predictor.predict(passenger_attributes)
    
    def test(self):
        predictet_results = self.predictor.predict(self.x_test)
        rounded_results = np.round(predictet_results)
        results = matthews_corrcoef(self.y_test, rounded_results)
        print(f"Die Wahrscheinlichkeit für eine Korrekte Vorhersage mit dem Modell {self.model} ist: {results}")
        return results


titanic_survival_rate = SurvivalRatePredictor(data)
print(titanic_survival_rate.predict(1,"female", 12))
titanic_survival_rate.test()
