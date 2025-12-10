from flask import Flask, render_template, request, send_file, abort
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import os
import sys
from sklearn import tree
import pandas as pd

# Daten laden
sys.path.append(os.path.join(os.path.dirname(__file__), "data"))
from data import (
    df as car_price_data,
    feature_value_to_ai_value,
    feature_value_to_df_value,
    features_in_median_order,
    feature_casts,
)

from DecissionTree import model as decission_tree_model
from DecissionTree import x_train, x_test, y_test
from RandomForest import model as random_forest_Model

rf_model = random_forest_Model
dt_model = decission_tree_model

app = Flask(__name__)


def is_discrete(series, threshold=25):
    try:
        return series.nunique() <= threshold
    except Exception:
        return True

def get_original_labels(feature, values):
    """Map numerische Werte zurück zu Original-Labels."""
    if feature in feature_value_to_df_value:
        reverse_map = {v: k for k, v in feature_value_to_df_value[feature].items()}
        return [reverse_map.get(v, str(v)) for v in values]
    return [str(v) for v in values]

def generate_plot(df, feature, plot_type):
    discrete = is_discrete(df[feature])
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(6, 4))

    if plot_type == "histogram":
        ax.hist(df[feature].dropna(), bins=30, color='cyan', edgecolor='black')
        ax.set_title(f"Histogram {feature}")
        ax.set_xlabel(feature)
        ax.set_ylabel("Count")

    elif plot_type == "boxplot":
        if discrete:
            data, labels = [], []
            for val in sorted(df[feature].dropna().unique()):
                y = df.loc[df[feature] == val, "Price"]
                data.append(y)
                labels.append(get_original_labels(feature, [val])[0])
            ax.boxplot(data, labels=labels, patch_artist=True,
                       boxprops=dict(facecolor='cyan'))
            ax.set_xlabel(feature)
            ax.set_ylabel("Price")
            ax.set_title(f"{feature} vs Price (Boxplot)")
        else:
            ax.boxplot(df["Price"].dropna(), patch_artist=True,
                       boxprops=dict(facecolor='cyan'))
            ax.set_title("Price (Boxplot)")

    elif plot_type == "scatter":
        if discrete:
            data, labels = [], []
            for val in sorted(df[feature].dropna().unique()):
                y = df.loc[df[feature] == val, "Price"]
                data.append(y)
                labels.append(get_original_labels(feature, [val])[0])
            ax.boxplot(data, labels=labels, patch_artist=True,
                       boxprops=dict(facecolor='cyan'))
            ax.set_xlabel(feature)
            ax.set_ylabel("Price")
            ax.set_title(f"{feature} vs Price (Boxplot)")
        else:
            ax.scatter(df[feature], df["Price"], alpha=0.6, color='cyan')
            ax.set_xlabel(feature)
            ax.set_ylabel("Price")
            ax.set_title(f"{feature} vs Price (Scatter)")

    fig.tight_layout()
    return fig

@app.route("/")
def index():
    df = car_price_data
    features = df.select_dtypes(include=["number"]).columns.tolist()
    features = [c for c in features if c != "Price"]
    return render_template("index.html", features=features)

@app.route("/plot_image")
def plot_image():
    df = car_price_data
    feature = request.args.get("feature")
    plot_type = request.args.get("plot_type")

    if feature not in df.columns:
        return abort(400, description=f"Feature {feature} nicht gefunden")
    if df[feature].dropna().empty or df["Price"].dropna().empty:
        return abort(400, description="Feature oder Price enthält keine Daten")

    try:
        fig = generate_plot(df, feature, plot_type)
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        return abort(500, description=f"Fehler beim Plotten: {e}")

@app.route("/plots/<feature>/<plot_type>")
def static_plot(feature, plot_type):
    df = car_price_data
    if feature not in df.columns:
        return abort(400, description=f"Feature {feature} nicht gefunden")
    try:
        fig = generate_plot(df, feature, plot_type)
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        return abort(500, description=f"Fehler beim Plotten: {e}")

@app.route('/plot_tree_png')
def plot_tree_png():
    rf_tree = rf_model.estimators_[0]
    fig, axes = plt.subplots(1, 2, figsize=(36, 12))
    fig.patch.set_facecolor("black")

    tree.plot_tree(dt_model, feature_names=x_train.columns,
                   filled=True, rounded=True, fontsize=9, ax=axes[0])
    axes[0].set_title("Decision Tree", color="white")
    axes[0].set_facecolor("black")

    tree.plot_tree(rf_tree, feature_names=x_train.columns,
                   filled=True, rounded=True, fontsize=9, ax=axes[1])
    axes[1].set_title("Random Forest – Baum 0", color="white")
    axes[1].set_facecolor("black")

    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close(fig)
    return send_file(buf, mimetype="image/png")

@app.route("/plot_predictions")
def plot_predictions():
    y_pred_dt = dt_model.predict(x_test)
    y_pred_rf = rf_model.predict(x_test)

    fig, ax = plt.subplots(1, 2, figsize=(16, 6))
    ax[0].scatter(y_test, y_pred_dt, alpha=0.6, color='cyan')
    ax[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    ax[0].set_title("Decision Tree: Prediction vs Reality")
    ax[0].set_xlabel("Real Price")
    ax[0].set_ylabel("Predicted Price")

    ax[1].scatter(y_test, y_pred_rf, alpha=0.6, color='orange')
    ax[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    ax[1].set_title("Random Forest: Prediction vs Reality")
    ax[1].set_xlabel("Real Price")
    ax[1].set_ylabel("Predicted Price")

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return send_file(buf, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)
