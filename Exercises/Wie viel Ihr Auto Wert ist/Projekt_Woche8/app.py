from flask import Flask, render_template, request, send_file, abort
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import os
import sys
from sklearn.tree import export_graphviz
from sklearn import tree
from sklearn.tree import export_text
import pandas as pd


#from RandomForest02 import train_random_forest
#from DecissionTree import train_decision_tree
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

    discrete = is_discrete(df[feature])

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(6, 4))

    try:
        if plot_type == "histogram":
            ax.hist(df[feature].dropna(), bins=30, color='cyan', edgecolor='black')
            ax.set_title(f"Histogram {feature}")
            ax.set_xlabel(feature)
            ax.set_ylabel("Count")

        elif plot_type == "boxplot":
            if discrete:
                data = []
                labels = []
                for val in sorted(df[feature].dropna().unique()):
                    y = df.loc[df[feature] == val, "Price"]
                    data.append(y)
                    labels.append(str(val))
                ax.boxplot(data, labels=labels, patch_artist=True,
                           boxprops=dict(facecolor='cyan'))
                ax.set_xlabel(feature)
                ax.set_ylabel("Price")
                ax.set_title(f"{feature} vs Price (Boxplot)")
            else:
                # Wenn nicht diskret, zeigen wir einfach Boxplot von Price
                ax.boxplot(df["Price"].dropna(), patch_artist=True, boxprops=dict(facecolor='cyan'))
                ax.set_title(f"Price (Boxplot)")

        elif plot_type == "scatter":
            if discrete:
                # Scatter nicht sinnvoll bei diskreten Features -> Boxplot als Ersatz
                data = []
                labels = []
                for val in sorted(df[feature].dropna().unique()):
                    y = df.loc[df[feature] == val, "Price"]
                    data.append(y)
                    labels.append(str(val))
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

        else:
            return abort(400, description="Unbekannter Plottyp")

        fig.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)

        return send_file(buf, mimetype='image/png')
    except Exception as e:
        plt.close(fig)
        return abort(500, description=f"Fehler beim Plotten: {e}")

@app.route('/plot_tree_png')
def plot_tree_png():
    #dt_model, x_train, x_test, y_train, y_test = train_decision_tree()
    #rf_model, x_train, x_test, y_train, y_test = train_random_forest()
    dt_model = decission_tree_model
    rf_model = random_forest_Model
    rf_tree = rf_model.estimators_[0]

    fig, axes = plt.subplots(1, 2, figsize=(36, 12))
    fig.patch.set_facecolor("black")  # Hintergrund schwarz

    # Decision Tree
    tree.plot_tree(
        dt_model,
        feature_names=x_train.columns,
        filled=True,
        rounded=True,
        fontsize=9,
        ax=axes[0]
    )
    axes[0].set_title("Decision Tree", color="white")
    axes[0].set_facecolor("black")  # Achsen-Hintergrund schwarz

    # Random Forest – erster Baum
    tree.plot_tree(
        rf_tree,
        feature_names=x_train.columns,
        filled=True,
        rounded=True,
        fontsize=9,
        ax=axes[1]
    )
    axes[1].set_title("Random Forest – Baum 0", color="white")
    axes[1].set_facecolor("black")

    # Alle Texte weiß einfärben
    for ax in axes:
        for artist in ax.get_children():
            if hasattr(artist, "set_color"):
                artist.set_color("white")

    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close(fig)

    return send_file(buf, mimetype="image/png")



@app.route("/plot_predictions")
def plot_predictions():
    #dt_model, x_train, x_test, y_train, y_test = train_decision_tree()
    #rf_model, x_train, x_test, y_train, y_test = train_random_forest()
    dt_model = decission_tree_model
    rf_model = random_forest_Model

    y_pred_dt = dt_model.predict(x_test)
    y_pred_rf = rf_model.predict(x_test)

    fig, ax = plt.subplots(1,2,figsize=(16,6))
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

@app.route("/predict", methods=["GET", "POST"])
def predict():
    df = car_price_data
    feature_names = [c for c in df.columns if c != "Price"]

    DROPDOWN_FEATURES = [
        "Manufacturer",
        "Model",
        "Category",
        "Color",
        "Fuel type",
        "Gear box type",
        "Wheel",
        "Leather interior",
    ]

    select_options: dict[str, list[str]] = {}

    for f in DROPDOWN_FEATURES:
        options = None
        
        if f in feature_casts and isinstance(feature_casts[f], dict):
            options = sorted(feature_casts[f].keys())

        elif f in feature_value_to_df_value:
            keys = [k for k in feature_value_to_df_value[f].keys() if k is not None]
            options = sorted(keys)

        if options:
            select_options[f] = options


    if request.method == "POST":
        input_values: dict[str, str] = {}
        ai_values: dict[str, float] = {}
        unknown_flags: dict[str, bool] = {}

        for f in feature_names:
            raw_val = request.form.get(f)

            # --- Fall 1: Feld leer -> Median-Wert verwenden ---
            if raw_val is None or raw_val.strip() == "":
                input_values[f] = ""  # Formular bleibt optisch leer

                if f in features_in_median_order and f in feature_value_to_df_value:
                    # Kategorie-Feature mit eigenem Median-Mapping
                    ai_val = feature_value_to_df_value[f][None]
                else:
                    # Numerisches Feature -> Spaltenmedian
                    ai_val = df[f].median()

                ai_values[f] = ai_val
                unknown_flags[f] = True  # "Standardwert/Median verwendet"
                continue

            # feature_value_to_ai_value benutzen 
            try:
                ai_val, known = feature_value_to_ai_value(f, raw_val)
            except Exception as e:
                return abort(400, description=f"Fehler beim Konvertieren von {f}: {e}")

            input_values[f] = raw_val
            ai_values[f] = ai_val
            unknown_flags[f] = not known  

        X_new = pd.DataFrame([ai_values], columns=feature_names)


        pred_price = rf_model.predict(X_new)[0]

        return render_template(
            "predict.html",
            feature_names=feature_names,
            input_values=input_values,
            unknown_flags=unknown_flags,
            pred_price=pred_price,
            select_options=select_options,
        )

    # GET: leeres Formular anzeigen
    return render_template(
        "predict.html",
        feature_names=feature_names,
        input_values=None,
        unknown_flags=None,
        pred_price=None,
        select_options=select_options,
    )


if __name__ == "__main__":
    app.run(debug=True)