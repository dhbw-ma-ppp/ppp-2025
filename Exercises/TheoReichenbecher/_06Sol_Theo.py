# For this weeks exercise you need to analyse a dataset and prepare a machine learning model to predict a property of that dataset. The dataset is the data on Titanic passengers and can be found in the data folder.

# There are two parts to todays exercise:
# - Analyse and visualize the data. Look for missing values and for correlations between features, as well as between feature and target. Prepare a brief report with some visualisations of the data, and with a summary of what you observed. This can be a jupyter notebok, some other document, or just part of the PR description with images pasted into it.

# - Train an ML model that will predict for any passenger whether they will survive. Determine whether this is a classification or regression task, and use an appropriate model. Spend some time on optimizing the algorithm and hyperparameters. Report the matthews correlation coefficient calculated on a test set as part of your submission. 

import pandas as pd

# Import der wichtigen plot Libarys 
import matplotlib.pyplot as plt

# Import der Machinelearning-Lib
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split 
from sklearn.model_selection import cross_val_score
from sklearn.inspection import permutation_importance
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score, f1_score, matthews_corrcoef
from sklearn import tree

class DataVisualisation:
    def __init__(self):
        self.data = 'titanic.csv'

    def ausgabe_der_CSV_tabelle(self):
        print("Ausgabe der CSV-Tabelle")
        df = pd.read_csv(self.data)
        df["Gender_num"] = df["Sex"].map({"male": 0, "female": 1}) # hier wird eine neue Spalte angefügt die male den Wert 0 gibt und female den Wert 1
        return df
        
    def darstellen_der_werte(self, df):

        # Plot 1: Überlebensrate nach Geschlecht
        def plot_sex(df):
            # Mittelwerte berechnen
            rates = df.groupby("Sex")["Survived"].mean()
            plt.bar(rates.index, rates.values, color=["steelblue", "salmon"])
            plt.ylabel("Überlebensrate")
            plt.title("Überlebensrate nach Geschlecht")
            plt.show()


        # Plot 2: Überlebensrate nach Klasse
        def plot_class(df):
            rates = df.groupby("Pclass")["Survived"].mean()
            plt.bar(rates.index.astype(str), rates.values, color="lightgreen")
            plt.ylabel("Überlebensrate")
            plt.title("Überlebensrate nach Klasse")
            plt.show()


        # Plot 3: Alter vs. Überleben
        def plot_age(df):
            colors = {"male": "blue", "female": "red"}
            for sex in df["Sex"].unique():
                subset = df[df["Sex"] == sex]
                plt.scatter(subset["Age"], subset["Survived"],
                            c=colors[sex], label=sex, alpha=0.2)
            plt.xlabel("Alter")
            plt.ylabel("Überlebt (0/1)")
            plt.title("Alter vs. Überleben")
            plt.legend()
            plt.show()

        # Aufruf der drei Plots
        plot_sex(df)
        plot_class(df)
        plot_age(df)

class TrainTestSplit:
    def __init__(self):
        # x und y als globale Variablen vereibaren --> Die ML Modelle können so einfacher darauf zugrifen
        global x
        global y

        # den dataframe teilen in features und survived
        self.df = df
        x = df[['PassengerId', 'Pclass', 'Gender_num', 'Age', 'Fare' ]]
        y = df['Survived']

        self.train_test_split(x, y)

    def train_test_split(self, x, y):
        """
        Die Funktion nimmt zwei Dataframes und teilt sie in Test und Trainingsdaten
        """
        x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, stratify=y)
        print(x_train.head(), '\n')
        print(x_train.shape)
        print(y_train.head(), '\n')
        print(y_train.shape)

        return x_train, x_test, y_train, y_test

class MachineLearning (TrainTestSplit):
    """
    Trainiert einen Entscheidungsbaum auf Grundlage des global angelgten Datenframes
    """
    def __init__(self):
        data_split = TrainTestSplit ()
        x_train, x_test, y_train, y_test = data_split.train_test_split(x, y)
        self.der_gärtner(x_train, x_test, y_train, y_test)

    def der_gärtner(self, x_train, x_test, y_train, y_test):
        # Der Gärtner nimmt die Trainings und Testdaten und trainiert einen Entscheidungsbaum 
        classifier = tree.DecisionTreeClassifier()
        classifier.fit(x_train, y_train)

        # Gibt den Predictionwert für die Person auf 
        y_pred = classifier.predict(x_test)
        y_pred = pd.DataFrame(y_pred, columns=['prediction'], index=y_test.index)#
        print("Die vom Entscheidungsbaum vorhergesaten Werte")
        print(y_pred)

        # Weitere Ausgaben und Metriken zum Entscheiden ob es sich um ein gutes Modell handelt 
        self.moment_der_wahrheit(y_pred, y_test)
        self.metric_tests(y_test, y_pred)
        self.das_resultat(classifier, x_train, x_test, y_train, y_test, df)

    def moment_der_wahrheit(self, y_pred, y_test):
        # Stellt der Vorhersage den tatsächlichen Wert gegenüber und gibt correct zurück falls sie übereinstimmen
        results = pd.concat([y_test, y_pred], axis=1)
        results['correct'] = results.Survived == results.prediction
        print("Ausgabe einer Vergleichstabelle")
        print(results.head())

        
    def metric_tests(self, y_test, y_pred):
        # Verschiedene Metriken zur Einschätzung des Modells 
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='macro')
        mcc = matthews_corrcoef(y_test, y_pred)

        print('\n acc:', acc, '\n f1 :', f1, '\n mcc:', mcc, '\n')

    def das_resultat(self, classifier, x_train, x_test, y_train, y_test, df):
        ConfusionMatrixDisplay.from_estimator(classifier, x_test, y_test)
        #==========Zwei plots desselben Baumes==========#
        # Plot zeigt die generelle Structur des Baumes
        tree.plot_tree(
            classifier,
            feature_names=x_train.columns,
            class_names=[str(c) for c in y_train.unique()],
            filled=True
        )

        # Plot zeigt einzelne Entscheidungen
        plt.figure(figsize=(300,30))  
        plot_tree(
            classifier,
            filled=True,              
            feature_names=x_train.columns,  
            class_names=["Nicht überlebt", "Überlebt"],  
            rounded=True,             
            fontsize=10
        )
        plt.title("Decition tree without any improvements")
        plt.show()

class MachineLearningHyperparameterTuning (TrainTestSplit):
    def __init__(self):
        data_split = TrainTestSplit ()
        x_train, x_test, y_train, y_test = data_split.train_test_split(x, y)
        self.der_spezial_gärtner(x_train, x_test, y_train, y_test)
    
    def der_spezial_gärtner(self, x_train, x_test, y_train, y_test):
        # der spezial Gärtner trainiert verschiedene Bäume und schaut welche Baumtiefe am besten ist
        classifier = DecisionTreeClassifier()
        mean_scores = []
        depth_list = [2, 5, 10, 20, 30]
        for depth in depth_list:
            print(f'Running cross-validation for {depth=}')
            classifier = DecisionTreeClassifier(max_depth=depth)
            scores = cross_val_score(classifier, x_train, y_train, cv=3, scoring='matthews_corrcoef')
            mean_scores.append((scores.mean()))

        maximal = 0 
        index = 0
        for i, score in enumerate(mean_scores):
            print(float(score))
            if score > maximal:
                maximal = score
                index = i

        classifier = DecisionTreeClassifier(max_depth=depth_list[index])
        classifier.fit(x_train, y_train)
        
        #==========Plottet den 'Besten' Baum des Depthtunings zum Vergleich mit den ohne Einschränkungen==========#
        plt.figure(figsize=(20,10))  
        plot_tree(
            classifier,
            filled=True,              
            feature_names=x_train.columns,  
            class_names=["Nicht überlebt", "Überlebt"],  
            rounded=True,             
            fontsize=10
        )
        plt.title("Decition tree with depth tuning")
        plt.show()


if __name__ == '__main__':
    titanic_survivors = DataVisualisation()
    df = titanic_survivors.ausgabe_der_CSV_tabelle()
    print(df)
    titanic_survivors.darstellen_der_werte(df)
    tree = MachineLearning()
    hyper_tree = MachineLearningHyperparameterTuning()
