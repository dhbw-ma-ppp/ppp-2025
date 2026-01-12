"""
For this weeks exercise you need to analyse a dataset and prepare a machine learning model to predict a property of that dataset.
The dataset is the data on Titanic passengers and can be found in the data folder.

There are two parts to todays exercise:
- Analyse and visualize the data.
    Look for missing values and for correlations between features, as well as between feature and target.
    Prepare a brief report with some visualisations of the data, and with a summary of what you observed.
    This can be a jupyter notebok, some other document, or just part of the PR description with images pasted into it.
- Train an ML model that will predict for any passenger whether they will survive. <-------------
    Determine whether this is a classification or regression task, and use an appropriate model.
    Spend some time on optimizing the algorithm and hyperparameters.
    Report the matthews correlation coefficient calculated on a test set as part of your submission.
"""

from numpy import ndarray
import pandas as pd
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, matthews_corrcoef
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

# --- prepare ---
df = pd.read_csv("exercises_06/titanic.csv")

df["SexNum"] = df["Sex"].map(
    {"male": 0, "female": 1}
)  # no more complex vectorization or TfidfTransformer needed

df["Age"] = df["Age"].fillna(df["Age"].median())

features = ["SexNum", "Age", "Fare", "SibSp", "Parch", "Pclass"]
X = df[features]
y = df["Survived"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# --- Test helper function ---
def test_compare_model(y_pred: ndarray, name: str = "Model-Test"):
    print(f"\n--- {name} ---\n")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    mcc = matthews_corrcoef(y_test, y_pred)
    print("\nMatthews Correlation Coefficient (MCC):", mcc)


# --- Training classification models (0, 1) ---
def try_logistic_regression():  # try, second example
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    test_compare_model(y_pred, "Logistic-Regression")


def try_decision_tree():
    dt = DecisionTreeClassifier(random_state=42)

    """ param_grid = {
        "max_depth": [20],
    } """  # only 0.743 accuracy and MCC 0.472

    param_grid = {
        "max_depth": [3, 5, 7, 9, None],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
    }

    grid_search = GridSearchCV(dt, param_grid, cv=5, scoring="accuracy")
    grid_search.fit(X_train, y_train)

    best_dt = grid_search.best_estimator_
    y_pred = best_dt.predict(X_test)
    test_compare_model(y_pred, "Decision-Tree")


if __name__ == "__main__":
    try_decision_tree()
