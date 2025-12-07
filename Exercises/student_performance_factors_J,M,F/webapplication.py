from flask import Flask, request, render_template, send_from_directory
import pandas as pd
import joblib
import json

app = Flask(__name__)

# Load data and model artifacts
data = pd.read_csv('StudentPerformanceFactors.csv')
model = joblib.load('student_performance_model.joblib')
model_columns = joblib.load('model_columns.joblib')
metrics = joblib.load('evaluation_metrics.joblib')
label_encoders = joblib.load('label_encoders.joblib') # Encoder laden
# feature_importances = joblib.load('feature_importances.joblib') # Diese Zeile sollte bereits entfernt sein


# Get options for dropdowns from the dataset
categorical_columns = data.select_dtypes(include=['object', 'bool']).columns
dropdown_options = {col: data[col].unique().tolist() for col in categorical_columns}


@app.route("/", methods=['GET', 'POST'])
def main():
    prediction = None
    form_data = {}

    if request.method == 'POST':
        if 'predict' in request.form:
            form_data = request.form.to_dict()
            
            # Kopie für die Umwandlung erstellen
            prediction_data = form_data.copy()

            # Serverseitige Plausibilitätsprüfung: Schlaf ist pro Tag -> in Woche umrechnen
            try:
                hours_studied = float(prediction_data.get('Hours_Studied', 0) or 0)
            except ValueError:
                hours_studied = 0.0
            try:
                sleep_per_day = float(prediction_data.get('Sleep_Hours', 0) or 0)
            except ValueError:
                sleep_per_day = 0.0
            try:
                physical_week = float(prediction_data.get('Physical_Activity', 0) or 0)
            except ValueError:
                physical_week = 0.0

            # Grundwerte / Grenzen
            hours_studied = max(0.0, min(hours_studied, 168.0))
            sleep_per_day = max(0.0, min(sleep_per_day, 24.0))
            physical_week = max(0.0, min(physical_week, 168.0))

            weekly_sleep = sleep_per_day * 7.0
            total_weekly = weekly_sleep + hours_studied + physical_week

            scaled_notice = None
            if total_weekly > 168.0:
                # skaliere proportional auf 168 Stunden (behalte Verhältnisse)
                scale = 168.0 / total_weekly
                weekly_sleep *= scale
                hours_studied *= scale
                physical_week *= scale

                # zurück zu Sleep per day
                sleep_per_day = weekly_sleep / 7.0

                # runde Werte und sichere Grenzen nochmal ab
                hours_studied = round(max(0.0, min(hours_studied, 168.0)), 2)
                sleep_per_day = round(max(0.0, min(sleep_per_day, 24.0)), 2)
                physical_week = round(max(0.0, min(physical_week, 168.0)), 2)

                # in prediction_data eintragen (so wird für Vorhersage die skalierte Verteilung genutzt)
                prediction_data['Hours_Studied'] = hours_studied
                prediction_data['Sleep_Hours'] = sleep_per_day
                prediction_data['Physical_Activity'] = physical_week

                scaled_notice = "Eingaben wurden automatisch skaliert, damit Gesamtstunden pro Woche ≤ 168 sind."

            # --- robustes Parsen numerischer Eingaben (mehrere mögliche Feldnamen) ---
            def extract_float(data, keys, default=0.0):
                for k in keys:
                    if k in data:
                        v = data[k]
                        if v is None:
                            continue
                        s = str(v).strip().replace(',', '.')
                        if s == '':
                            continue
                        try:
                            return float(s)
                        except Exception:
                            continue
                return default

            hours_keys = ['Hours_Studied', 'HoursStudied', 'Hours Studied', 'Study_Hours', 'Learning_Hours', 'Hours_Studied_per_week']
            sleep_keys = ['Sleep_Hours', 'SleepHours', 'Sleep per day', 'Sleep_Per_Day']
            physical_keys = ['Physical_Activity', 'PhysicalActivity', 'Training_Hours', 'TrainingHours', 'Physical_Activity_hours', 'Sport_Hours']

            hours_studied = extract_float(prediction_data, hours_keys, 0.0)   # erwarteter Wert: pro Woche
            sleep_per_day = extract_float(prediction_data, sleep_keys, 0.0)   # pro Tag
            physical_week = extract_float(prediction_data, physical_keys, 0.0) # pro Woche

            # Grundwerte / elementare Grenzen
            hours_studied = max(0.0, min(hours_studied, 168.0))
            sleep_per_day = max(0.0, min(sleep_per_day, 24.0))
            physical_week = max(0.0, min(physical_week, 168.0))

            weekly_sleep = sleep_per_day * 7.0
            total_weekly = weekly_sleep + hours_studied + physical_week

            scaled_notice = None
            if total_weekly > 168.0:
                # skaliere proportional auf 168 Stunden (behalte Verhältnisse)
                scale = 168.0 / total_weekly
                weekly_sleep *= scale
                hours_studied *= scale
                physical_week *= scale

                # zurück zu Sleep per day
                sleep_per_day = weekly_sleep / 7.0

                # runde Werte und sichere Grenzen nochmal ab
                hours_studied = round(max(0.0, min(hours_studied, 168.0)), 2)
                sleep_per_day = round(max(0.0, min(sleep_per_day, 24.0)), 2)
                physical_week = round(max(0.0, min(physical_week, 168.0)), 2)

                # in prediction_data eintragen (mehrere mögliche Keys auffüllen)
                for k in hours_keys:
                    prediction_data[k] = hours_studied
                for k in sleep_keys:
                    prediction_data[k] = sleep_per_day
                for k in physical_keys:
                    prediction_data[k] = physical_week

                # zusätzlich: falls Model-Spalten andere Namen hat, fülle diese
                study_col = next((c for c in model_columns if 'study' in c.lower() or 'learn' in c.lower()), None)
                sleep_col = next((c for c in model_columns if 'sleep' in c.lower()), None)
                physical_col = next((c for c in model_columns if any(x in c.lower() for x in ['physical','train','sport'])), None)
                if study_col:
                    prediction_data[study_col] = hours_studied
                if sleep_col:
                    prediction_data[sleep_col] = sleep_per_day
                if physical_col:
                    prediction_data[physical_col] = physical_week

                scaled_notice = "Eingaben wurden automatisch skaliert, damit Gesamtstunden pro Woche ≤ 168 sind."

            # Falls keine Skalierung nötig: dennoch sicherstellen, dass die üblichen Keys im prediction_data vorhanden sind
            for k in hours_keys:
                if k not in prediction_data:
                    prediction_data[k] = hours_studied
            for k in sleep_keys:
                if k not in prediction_data:
                    prediction_data[k] = sleep_per_day
            for k in physical_keys:
                if k not in prediction_data:
                    prediction_data[k] = physical_week

            # --- KATEGORISCHE WERTE UMWANDELN ---
            for col, le in label_encoders.items():
                if col in prediction_data:
                    try:
                        prediction_data[col] = le.transform([prediction_data[col]])[0]
                    except Exception:
                        prediction_data[col] = 0

            # --- NUMERISCHE WERTE UMWANDELN (stellen sicher, dass strings zu Zahlen werden) ---
            for col in model_columns:
                if col not in label_encoders:
                    if col in prediction_data:
                        val = prediction_data[col]
                        try:
                            prediction_data[col] = float(val)
                        except Exception:
                            prediction_data[col] = 0.0
                    else:
                        # falls Spalte im model erwartet wird, aber kein Wert vorhanden: 0.0 setzen
                        prediction_data[col] = 0.0

            # DataFrame für die Vorhersage erstellen
            input_df = pd.DataFrame([prediction_data], columns=model_columns)

            # Predict
            pred_value = model.predict(input_df)[0]
            # Begrenze Vorhersage auf [0, 100]
            pred_value = float(pred_value)
            if pred_value > 100:
                pred_value = 100.0
            elif pred_value < 0:
                pred_value = 0.0

            prediction = round(pred_value, 2)

            # render mit optionaler Info über Skalierung
            return render_template(
                'index.html',
                prediction=prediction,
                dropdown_options=dropdown_options,
                form_data=form_data,
                metrics=metrics,
                info=scaled_notice
            )

    return render_template(
        'index.html',
        prediction=prediction, 
        dropdown_options=dropdown_options, 
        form_data=form_data,
        metrics=metrics
        # feature_importances=feature_importances # Diese Zeile sollte bereits entfernt sein
    )

@app.route("/notebook")
def notebook():
    # Serve the converted HTML version of the notebook from the templates folder
    return send_from_directory('templates', 'visualisation.html')