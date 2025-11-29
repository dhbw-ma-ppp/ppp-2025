"""
For this weeks exercise you need to analyse a dataset and prepare a machine learning model to predict a property of that dataset.
The dataset is the data on Titanic passengers and can be found in the data folder.

There are two parts to todays exercise:
- Analyse and visualize the data. <-------------
    Look for missing values and for correlations between features, as well as between feature and target.
    Prepare a brief report with some visualisations of the data, and with a summary of what you observed.
    This can be a jupyter notebok, some other document, or just part of the PR description with images pasted into it.
- Train an ML model that will predict for any passenger whether they will survive.
    Determine whether this is a classification or regression task, and use an appropriate model.
    Spend some time on optimizing the algorithm and hyperparameters.
    Report the matthews correlation coefficient calculated on a test set as part of your submission.
"""

from matplotlib.axes import Axes
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

# --- Ini Plotting ---
TITLE_SIZE = 14


plt.rcParams.update(
    {
        "axes.titlesize": TITLE_SIZE,
    }
)

# --- Read ---
df = pd.read_csv("exercises_06/titanic.csv")
# --- Extend ---
df["SexNum"] = df["Sex"].map({"male": 0, "female": 1})


# --- Plot funcs ---
def plot_missing_values(axe: Axes):
    missing_count = df.isnull().sum()
    missing_percent = (df.isnull().mean() * 100).round(1)
    labels = [
        f"{col}\n{missing_count[col]} ({missing_percent[col]}%)" for col in df.columns
    ]

    axe.imshow(df.isnull(), aspect="auto", cmap="gray_r", interpolation="nearest")
    axe.set_title("Missing values matrix")
    axe.set_ylabel("Passenger Entry")
    axe.set_xticks(range(len(df.columns)))
    axe.set_xticklabels(labels)


def plot_age(axe_relative: Axes, axe_absolute: Axes):
    df_age_clean = df.dropna(subset=["Age"])
    max_age = df_age_clean["Age"].max()
    range_auto = (0, np.ceil(max_age / 5) * 5 + 2)

    bins = 20
    hist_died, edges = np.histogram(
        df_age_clean[df_age_clean["Survived"] == 0]["Age"], bins=bins, range=range_auto
    )
    hist_surv, _ = np.histogram(
        df_age_clean[df_age_clean["Survived"] == 1]["Age"], bins=bins, range=range_auto
    )
    total = hist_died + hist_surv
    total[total == 0] = 1

    percent_died = hist_died / total * 100

    axe_relative.bar(
        edges[:-1],
        percent_died,
        width=np.diff(edges),
        color="red",
        alpha=0.9,
        label="Died",
    )
    axe_relative.bar(
        edges[:-1],
        100 - percent_died,
        bottom=percent_died,
        width=np.diff(edges),
        color="green",
        alpha=0.7,
        label="Survived",
    )
    axe_relative.set_title("Death: relative by age group")
    axe_relative.set_xlabel("Age")
    axe_relative.set_ylabel("Rrobability (%)")
    axe_relative.set_ylim(0, 100)
    axe_relative.grid(axis="y", alpha=0.3)
    axe_relative.legend()

    axe_absolute.hist(
        [
            df_age_clean[df_age_clean["Survived"] == 0]["Age"],
            df_age_clean[df_age_clean["Survived"] == 1]["Age"],
        ],
        bins=20,
        color=["red", "green"],
        alpha=0.7,
        label=["Died", "Survived"],
    )
    axe_absolute.set_title("Death: absolute numbers")
    axe_absolute.set_xlabel("Age")
    axe_absolute.set_ylabel("Count")
    axe_absolute.legend()


def plot_sex_survive(axe: Axes):
    survival_by_sex = df.groupby("Sex")["Survived"].mean() * 100
    survival_by_sex = survival_by_sex.round(1)

    bars = axe.bar(
        survival_by_sex.index,
        survival_by_sex.values,
        color=["pink", "lightblue"],
        edgecolor="black",
        linewidth=1.2,
        alpha=0.9,
    )

    for bar, percent in zip(bars, survival_by_sex.values):
        axe.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 2,
            f"{percent}%",
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    # Schön machen
    axe.set_title("Relative survival-rate by sex")
    axe.set_ylabel("Survivors (%)")
    axe.set_xlabel("Sex")
    axe.set_ylim(0, 100)
    axe.grid(axis="y", alpha=0.5, linestyle="--")

    axe.set_yticks(range(0, 101, 20))


def plot_class_survive(axe: Axes):
    survival_by_class = df.groupby("Pclass")["Survived"].mean() * 100
    survival_by_class = survival_by_class.round(1)

    bars = axe.bar(
        survival_by_class.index,
        survival_by_class.values,
        color=["gold", "silver", "#CD7F32"],
        edgecolor="black",
        linewidth=1.2,
        alpha=0.9,
    )

    for bar, percent in zip(bars, survival_by_class.values):
        axe.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 2,
            f"{percent}%",
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    axe.set_title("Relative survival-rate by class")
    axe.set_ylabel("Survivors (%)")
    axe.set_xlabel("Class")
    axe.set_ylim(0, 100)
    axe.grid(axis="y", alpha=0.5, linestyle="--")
    axe.set_yticks(range(0, 101, 20))

    axe.set_xticks([1, 2, 3])
    axe.set_xticklabels(["First", "Second", "Third"])


def plot_feature_scatter(axe: Axes, x_feature: str, y_feature: str):

    data = df[[x_feature, y_feature]].dropna()

    axe.scatter(data[x_feature], data[y_feature], alpha=0.6)

    axe.set_xlabel(x_feature)
    axe.set_ylabel(y_feature)
    axe.set_title(f"{y_feature} vs {x_feature}")


def plot_feature_correlation(axe: Axes, features=None):
    if features is None:
        features = df.select_dtypes(include="number").columns.tolist()

    corr = df[features].corr()

    cax = axe.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)

    axe.set_xticks(np.arange(len(features)))
    axe.set_yticks(np.arange(len(features)))
    axe.set_xticklabels(features)
    axe.set_yticklabels(features)

    for i in range(len(features)):
        for j in range(len(features)):
            axe.text(
                j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", color="black"
            )

    plt.colorbar(cax, ax=axe, fraction=0.046, pad=0.04)
    axe.set_title("Korrelationsmatrix der Features")


# --- Main plot funcs ---
def create_detailed_plot():
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(
        4, 2, figure=fig, height_ratios=[1.4, 1.0, 1.0, 1.0], wspace=0.4, hspace=0.9
    )
    axe_missing = fig.add_subplot(gs[0, :])
    plot_missing_values(axe_missing)
    axe_relative = fig.add_subplot(gs[1, 0])
    axe_absolute = fig.add_subplot(gs[1, 1])
    plot_age(axe_relative, axe_absolute)
    axe_sex = fig.add_subplot(gs[2, 0])
    plot_sex_survive(axe_sex)
    axe_class = fig.add_subplot(gs[2, 1])
    plot_class_survive(axe_class)
    axe_scatter_age_fare = fig.add_subplot(gs[3, :])
    plot_feature_scatter(axe_scatter_age_fare, "Age", "Pclass")  # not the best one

    plt.suptitle("Titanic Stats: Detail", fontsize=20, y=0.98)


def create_correlation_plot():
    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(1, 1, 1)

    plot_feature_correlation(
        ax,
        features=["Survived", "SexNum", "Age", "Fare", "SibSp", "Parch", "Pclass"],
    )
    plt.suptitle("Titanic Stats: Correlations", fontsize=20, y=0.98)


if __name__ == "__main__":
    create_detailed_plot()
    create_correlation_plot()
    plt.show()
