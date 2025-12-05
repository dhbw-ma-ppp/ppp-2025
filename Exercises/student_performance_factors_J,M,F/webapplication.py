from flask import Flask, request, render_template_string
import pandas as pd
import joblib

app = Flask(__name__)

# Load data and model
data = pd.read_csv('StudentPerformanceFactors.csv')
model = joblib.load('student_performance_model.joblib')
model_columns = joblib.load('model_columns.joblib')

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

    # Jinja2 Template
    html_template = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Student Performance Prediction</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-100 text-gray-800">
            <div class="container mx-auto p-4">
                <div class="text-4xl p-4 text-center font-bold">
                    Student Performance Predictor
                </div>

                <div class="bg-white p-6 rounded-lg shadow-lg">
                    <h2 class="text-2xl font-semibold mb-4">Predict Your Exam Score</h2>
                    <form method="post">
                        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            
                            <!-- Numerical Inputs -->
                            <div>
                                <label for="Hours_Studied" class="block text-sm font-medium">Hours Studied</label>
                                <input type="number" name="Hours_Studied" value="{{ form_data.get('Hours_Studied', 20) }}" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
                            </div>
                            <div>
                                <label for="Attendance" class="block text-sm font-medium">Attendance (%)</label>
                                <input type="number" name="Attendance" value="{{ form_data.get('Attendance', 80) }}" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
                            </div>
                            <div>
                                <label for="Previous_Scores" class="block text-sm font-medium">Previous Scores</label>
                                <input type="number" name="Previous_Scores" value="{{ form_data.get('Previous_Scores', 75) }}" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
                            </div>
                            <div>
                                <label for="Sleep_Hours" class="block text-sm font-medium">Sleep Hours</label>
                                <input type="number" name="Sleep_Hours" value="{{ form_data.get('Sleep_Hours', 7) }}" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
                            </div>
                             <div>
                                <label for="Tutoring_Sessions" class="block text-sm font-medium">Tutoring Sessions</label>
                                <input type="number" name="Tutoring_Sessions" value="{{ form_data.get('Tutoring_Sessions', 1) }}" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
                            </div>
                             <div>
                                <label for="Physical_Activity" class="block text-sm font-medium">Physical Activity (hours/week)</label>
                                <input type="number" name="Physical_Activity" value="{{ form_data.get('Physical_Activity', 3) }}" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
                            </div>

                            <!-- Categorical Inputs -->
                            {% for col, options in dropdown_options.items() %}
                            <div>
                                <label for="{{ col }}" class="block text-sm font-medium">{{ col.replace('_', ' ') }}</label>
                                <select name="{{ col }}" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
                                    {% for option in options %}
                                    <option value="{{ option }}" {% if form_data.get(col) == option %}selected{% endif %}>{{ option }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                            {% endfor %}
                        </div>
                        <div class="mt-6 text-center">
                            <button type="submit" name="predict" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg">
                                Predict Score
                            </button>
                        </div>
                    </form>

                    {% if prediction is not none %}
                    <div class="mt-6 p-4 bg-green-100 border-l-4 border-green-500 text-green-700 rounded-lg">
                        <p class="font-bold text-lg">Predicted Exam Score: {{ prediction }}</p>
                    </div>
                    {% endif %}
                </div>
            </div>
        </body>
        </html>
    '''
    return render_template_string(html_template, prediction=prediction, dropdown_options=dropdown_options, form_data=form_data)



# Um die aktualisierte Webseite zu starten, verwenden Sie wieder diesen Befehl:

# python main.py um ml modell zu erstellen, dann
# flask --app webapplication.py run --reload