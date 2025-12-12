# Flask-Webanwendung für die Notenvorhersage

from flask import Flask, request, render_template, send_from_directory
import pandas as pd
import joblib

app = Flask(__name__)

# === Beim Serverstart: Alle benötigten Dateien laden ===
# CSV für Dropdown-Optionen, trainiertes Modell und Hilfsobjekte
data = pd.read_csv('StudentPerformanceFactors.csv')
model = joblib.load('student_performance_model.joblib')        # Die trainierte Pipeline
model_columns = joblib.load('model_columns.joblib')            # Spaltenreihenfolge für Vorhersage
metrics = joblib.load('evaluation_metrics.joblib')             # R² und RMSE für Anzeige
label_encoders = joblib.load('label_encoders.joblib')          # Text->Zahl Umwandlung

# Dropdown-Optionen aus den Originaldaten extrahieren
categorical_columns = data.select_dtypes(include=['object', 'bool']).columns
dropdown_options = {col: data[col].unique().tolist() for col in categorical_columns}


@app.route("/", methods=['GET', 'POST'])
def main():
    """Hauptseite: Formular anzeigen und Vorhersage berechnen"""
    prediction = None
    form_data = {}

    if request.method == 'POST':
        if 'predict' in request.form:
            form_data = request.form.to_dict()
            prediction_data = form_data.copy()

            # --- Eingabevalidierung: Stunden pro Woche begrenzen ---
            hours_studied = float(prediction_data.get('Hours_Studied', 0) or 0)
            sleep_per_day = float(prediction_data.get('Sleep_Hours', 0) or 0)
            physical_week = float(prediction_data.get('Physical_Activity', 0) or 0)

            # Plausibilitätsgrenzen
            hours_studied = max(0.0, min(hours_studied, 168.0))
            sleep_per_day = max(0.0, min(sleep_per_day, 24.0))
            physical_week = max(0.0, min(physical_week, 168.0))

            # Prüfen ob Gesamtstunden realistisch (max 168h/Woche)
            weekly_sleep = sleep_per_day * 7.0
            total_weekly = weekly_sleep + hours_studied + physical_week

            scaled_notice = None
            if total_weekly > 168.0:
                # Proportional skalieren damit Summe = 168
                scale = 168.0 / total_weekly
                hours_studied *= scale
                sleep_per_day = (weekly_sleep * scale) / 7.0
                physical_week *= scale
                scaled_notice = "Eingaben wurden automatisch skaliert (max 168h/Woche)."

            # Skalierte Werte zurückschreiben
            prediction_data['Hours_Studied'] = hours_studied
            prediction_data['Sleep_Hours'] = sleep_per_day
            prediction_data['Physical_Activity'] = physical_week

            # --- Kategorische Werte umwandeln (Text -> Zahl) ---
            # LabelEncoder wurde beim Training erstellt und hier wiederverwendet
            for col, le in label_encoders.items():
                if col in prediction_data:
                    try:
                        prediction_data[col] = le.transform([prediction_data[col]])[0]
                    except Exception:
                        prediction_data[col] = 0

            # --- Numerische Werte: String -> Float ---
            for col in model_columns:
                if col not in label_encoders:
                    if col in prediction_data:
                        try:
                            prediction_data[col] = float(prediction_data[col])
                        except Exception:
                            prediction_data[col] = 0.0
                    else:
                        prediction_data[col] = 0.0

            # DataFrame erstellen (Spaltenreihenfolge muss mit Training übereinstimmen)
            input_df = pd.DataFrame([prediction_data], columns=model_columns)

            # === Vorhersage mit dem trainierten Modell ===
            pred_value = model.predict(input_df)[0]
            
            # Ergebnis auf 0-100 begrenzen
            pred_value = max(0.0, min(float(pred_value), 100.0))
            prediction = round(pred_value, 2)

            return render_template(
                'index.html',
                prediction=prediction,
                dropdown_options=dropdown_options,
                form_data=form_data,
                metrics=metrics,
                info=scaled_notice
            )

    # GET-Request: Leeres Formular anzeigen
    return render_template(
        'index.html',
        prediction=prediction,
        dropdown_options=dropdown_options,
        form_data=form_data,
        metrics=metrics
    )


@app.route("/notebook")
def notebook():
    """Route für das Jupyter Notebook (als HTML exportiert)"""
    return send_from_directory('templates', 'visualisation.html')