import io
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.style.use("dark_background")
from flask import Flask, send_file, request, abort, render_template
import joblib
from sklearn import tree
from sklearn.model_selection import train_test_split
import sys

from data import df as car_price_data
from data import df as cleaned_df



# Flask App
app = Flask(__name__)

# -----------------------------
# Globale Variablen / Modelle
# -----------------------------
DECISION_TREE_PATH = sys.path[0] + "\Model_Data\\DecissionTree.pkl"
RANDOM_FOREST_PATH = sys.path[0] + "\Model_Data\\random_forest_model.pkl"

_dt_model = None
_rf_model = None

# -----------------------------
# Plot-Funktionen
# -----------------------------
def create_plot_image(raw_df, feature, plot_type):
    """Erzeugt Histogramm, Scatter oder Boxplot für ein Feature."""

    if feature not in raw_df.columns:
        raise ValueError(f"Feature '{feature}' existiert nicht.")

    fig, ax = plt.subplots(figsize=(6, 4))
    

    if plot_type == "scatter":
        ax.scatter(raw_df[feature], raw_df["Price"], s=10, alpha=0.6, color="cyan")
        ax.set_ylabel("Price")
        ax.set_title(f"{feature} vs Price")
        plt.xticks(rotation=90, color="white")

    elif plot_type == "histogram":
        ax.hist(raw_df[feature], bins=40, color="skyblue")
        ax.set_title(f"Histogram: {feature}")
        plt.xticks(rotation=90, color="white")

    elif plot_type == "boxplot":
        ax.boxplot( raw_df[feature], vert=True)
        ax.set_title(f"Boxplot: {feature}")
        plt.xticks(rotation=90, color="white")

    else:
        raise ValueError(f"Unbekannter Plot-Typ: {plot_type}")

    img_bytes = io.BytesIO()
    plt.tight_layout()
    fig.savefig(img_bytes, format="png")
    plt.close(fig)
    img_bytes.seek(0)
    return img_bytes

def create_tree_plot(model):
    """Zeichnet einen Entscheidungsbaum."""
    fig, ax = plt.subplots(figsize=(20, 12))
    tree.plot_tree(model, filled=True, fontsize=6)
    img = io.BytesIO()
    plt.tight_layout()
    fig.savefig(img, format="png")
    plt.close(fig)
    img.seek(0)
    return img

def create_prediction_plot(model, X_test, y_test):
    """Vergleich Vorhersagen vs. Realität."""
    y_pred = model.predict(X_test)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(y_test, y_pred, alpha=0.5, color="orange")
    ax.set_xlabel("Real Price")
    ax.set_ylabel("Predicted Price")
    ax.set_title("Predicted vs Real Price")

    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    ax.plot([min_val, max_val], [min_val, max_val], "r--")

    # gleiche Skalierung für x und y
    ax.set_xlim(min_val, max_val)
    ax.set_ylim(min_val, max_val)

    img = io.BytesIO()
    plt.tight_layout()
    fig.savefig(img, format="png")
    plt.close(fig)
    img.seek(0)
    return img



# -----------------------------
# Daten laden & vorbereiten
# -----------------------------
def load_and_prepare_data():
    """Lädt und bereinigt den Car Price Datensatz."""
    DATA_PATH = os.path.join(os.path.dirname(__file__), "car_price_prediction.csv")
    df = pd.read_csv(DATA_PATH)

    # Preisfilter
    df = df[(df["Price"] >= 1000) & (df["Price"] <= 400_000)]

    # Unnötige Spalten löschen
    df = df.drop(columns=["ID", "Levy", "Doors"], errors="ignore")

    # Feature-Casts
    feature_casts = {
        "Leather interior": {"No": 0, "Yes": 1},
        "Wheel": {"Left wheel": 0, "Right-hand drive": 1},
        "Airbags": int,
        "Engine volume": lambda txt: float(str(txt).replace("Turbo", "")),
        "Mileage": lambda txt: int("".join(c for c in str(txt) if c.isdigit()))
                               if str(txt).strip() != "" else None,
        "Drive wheels": lambda txt: int(txt == "Rear"),
        "Gear box type": {"Automatic": 0, "Tiptronic": 1, "Manual": 2, "Variator": 3},
    }

    for feature, caster in feature_casts.items():
        if feature in df.columns:
            if isinstance(caster, dict):
                df[feature] = df[feature].map(caster)
            else:
                df[feature] = df[feature].apply(lambda x: caster(x) if pd.notna(x) else None)

    # Modelle entfernen, die zu selten vorkommen
    if "Model" in df.columns:
        df = df.groupby("Model").filter(lambda x: len(x) > 5)

    # harte Filter
    if "Prod. year" in df.columns:
        df = df[(df["Prod. year"] >= 1985) & (df["Engine volume"] <= 19)]

    # Fehlende Werte droppen
    df = df.dropna()

    return df

# Daten global laden
print("📊 Lade Daten...")
df = load_and_prepare_data()
print("✔ Daten geladen.")

# -----------------------------
# Modell-Ladefunktionen
# -----------------------------
def load_decision_tree():
    global _dt_model
    if _dt_model is None:
        _dt_model = joblib.load(DECISION_TREE_PATH)
    return _dt_model

def load_random_forest():
    global _rf_model
    if _rf_model is None:
        _rf_model = joblib.load(RANDOM_FOREST_PATH)
    return _rf_model


# -----------------------------
# Flask Routes
# -----------------------------
@app.route("/")
def index():
    """Startseite mit Feature-Liste."""
    features = [c for c in df.columns if c != "Price"]
    return render_template("index.html", features=features)

@app.route("/plot_image")
def plot_image():
    """Route für Feature-Plots."""
    feature = request.args.get("feature")
    plot_type = request.args.get("plot_type")
    if not feature or not plot_type:
        return abort(400, "feature oder plot_type fehlt")
    try:
        img_bytes = create_plot_image(df, feature, plot_type)
        return send_file(img_bytes, mimetype="image/png")
    except Exception as e:
        return abort(500, str(e))

@app.route("/plot_trees")
def plot_trees():
    """Route für Decision Tree Plot."""
    try:
        dt = load_decision_tree()
        img = create_tree_plot(dt)
        return send_file(img, mimetype="image/png")
    except Exception as e:
        return abort(500, str(e))

@app.route("/plot_predictions")
def plot_predictions():
    try:
        rf = load_random_forest()

        # 👉 Bereinigte Daten verwenden
        X = cleaned_df.drop(columns=["Price"])
        y = cleaned_df["Price"]

        print("Spalten im X:", X.columns.tolist())  
        print("Erste Zeile:", X.iloc[0].to_dict())  

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        img = create_prediction_plot(rf, X_test, y_test)
        return send_file(img, mimetype="image/png")

    except Exception as e:
        print("Fehler in plot_predictions:", e)  
        return abort(500, str(e))

@app.route("/plot_predictions_tree")
def plot_predictions_tree():
    """Route für Vorhersagevergleich mit Decision Tree."""
    try:
        dt = load_decision_tree()

        # 👉 Bereinigte Daten verwenden
        X = cleaned_df.drop(columns=["Price"])
        y = cleaned_df["Price"]

        # Nur die Features nehmen, die das Modell kennt
        expected_features = dt.feature_names_in_
        X = X[expected_features]

        # Train/Test Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Nutze denselben Plot wie bei Random Forest
        img = create_prediction_plot(dt, X_test, y_test)
        return send_file(img, mimetype="image/png")

    except Exception as e:
        print("Fehler in plot_predictions_tree:", e)
        return abort(500, str(e))



# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)

# / zeigt die Feature‑Liste (wie bisher)
# /plot_image?feature=XYZ&plot_type=scatter -> generiert Plots
# /plot_trees -> zeigt den Decision Tree
# /plot_predictions -> zeigt Vorhersage vs. Realität