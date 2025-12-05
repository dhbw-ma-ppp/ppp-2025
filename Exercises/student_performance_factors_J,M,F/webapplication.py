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

            # KATEGORISCHE WERTE UMWANDELN
            for col, le in label_encoders.items():
                if col in prediction_data:
                    # Den Textwert aus dem Formular in eine Zahl umwandeln
                    prediction_data[col] = le.transform([prediction_data[col]])[0]

            # NUMERISCHE WERTE UMWANDELN
            for col in model_columns:
                if col not in label_encoders and col in prediction_data:
                    # Konvertiere den Wert zu float, wenn es keine kategoriale Spalte ist
                    prediction_data[col] = float(prediction_data[col])


            # DataFrame für die Vorhersage erstellen
            input_df = pd.DataFrame([prediction_data], columns=model_columns)

            # Predict
            pred_value = model.predict(input_df)[0]
            prediction = round(pred_value, 2)

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