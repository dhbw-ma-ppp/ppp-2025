from flask import Flask, request, render_template
import pandas as pd
import joblib
import json

app = Flask(__name__)

# Load data and model artifacts
data = pd.read_csv('StudentPerformanceFactors.csv')
model = joblib.load('student_performance_model.joblib')
model_columns = joblib.load('model_columns.joblib')
metrics = joblib.load('evaluation_metrics.joblib')
feature_importances = joblib.load('feature_importances.joblib')


# Get options for dropdowns from the dataset
categorical_columns = data.select_dtypes(include=['object', 'bool']).columns
dropdown_options = {col: data[col].unique().tolist() for col in categorical_columns}


@app.route("/", methods=['GET', 'POST'])
def main():
    prediction = None
    form_data = {}

    if request.method == 'POST':
        # This part handles the prediction form
        if 'predict' in request.form:
            form_data = request.form.to_dict()
            
            # Convert numerical fields to numbers, with defaults
            numerical_inputs = {
                'Hours_Studied': float(form_data.get('Hours_Studied', 0)),
                'Attendance': float(form_data.get('Attendance', 0)),
                'Previous_Scores': float(form_data.get('Previous_Scores', 0)),
                'Sleep_Hours': float(form_data.get('Sleep_Hours', 0)),
                'Tutoring_Sessions': float(form_data.get('Tutoring_Sessions', 0)),
                'Physical_Activity': float(form_data.get('Physical_Activity', 0)),
            }
            
            # Prepare data for prediction
            input_df = pd.DataFrame([form_data], columns=model_columns)

            for col, val in numerical_inputs.items():
                input_df[col] = val

            # Predict
            pred_value = model.predict(input_df)[0]
            prediction = round(pred_value, 2)

    return render_template(
        'index.html', 
        prediction=prediction, 
        dropdown_options=dropdown_options, 
        form_data=form_data,
        metrics=metrics,
        feature_importances=feature_importances
    )