from flask import Flask, render_template, request
import pickle
import numpy as np
import os

app = Flask(__name__)


# --- CONFIG ---
# FEATURE_GROUPS wurde entfernt, da dein HTML jetzt hardcoded ist.

# Liste der Namen für die Debug-Tabelle
FEATURE_NAMES = [
    "0: Marital status", "1: Application mode", "2: App order", "3: Course", "4: Daytime/Evening", "5: Prev Qual", 
    "6: Prev Qual Grade", "7: Nacionality", "8: Mother Qual", "9: Father Qual", "10: Mother Job", "11: Father Job",
    "12: Admission Grade", "13: Displaced", "14: Edu Needs", "15: Debtor", "16: Tuition Fees", "17: Gender", 
    "18: Scholarship", "19: Age", "20: International", "21: Cur 1 Credited", "22: Cur 1 Enrolled", "23: Cur 1 Eval", 
    "24: Cur 1 Approved", "25: Cur 1 Grade", "26: Cur 1 No Eval", "27: Cur 2 Credited", "28: Cur 2 Enrolled", 
    "29: Cur 2 Eval", "30: Cur 2 Approved", "31: Cur 2 Grade", "32: Cur 2 No Eval", "33: Unemp Rate", "34: Inflation", "35: GDP"
]

# --- MODELLE LADEN ---
models = {}
for version in ['v1', 'v2']:
    path = f'model_{version}.pkl'
    if os.path.exists(path):
        with open(path, 'rb') as f:
            models[version] = pickle.load(f)
            print(f"✅ {path} geladen.")

# --- DEFAULTS ---
DEFAULTS_GOOD = [1, 1, 5, 33, 1, 1, 140, 1, 3, 3, 5, 5, 140, 1, 0, 0, 1, 0, 0, 19, 0, 0, 5, 6, 5, 14.0, 0, 0, 5, 6, 5, 14.0, 0, 10.0, 1.4, 0.0]
DEFAULTS_RISK = [1, 1, 5, 33, 1, 1, 100, 1, 4, 4, 9, 9, 100, 1, 0, 1, 0, 0, 0, 35, 0, 0, 5, 6, 2, 10.0, 0, 0, 5, 6, 2, 10.0, 0, 10.0, 1.4, 0.0]

# --- VOLLSTÄNDIGES MAPPING ---
# Wichtig: Dieses Mapping muss alle Felder abdecken, damit das Kopieren funktioniert
IDX = {
    'marital_status': 0, 'application_mode': 1, 'application_order': 2, 'course': 3, 'daytime_evening': 4,
    'previous_qualification': 5, 'previous_qualification_grade': 6, 'nacionality': 7, 
    'mother_qualification': 8, 'father_qualification': 9, 'mother_occupation': 10, 'father_occupation': 11,
    'admission_grade': 12, 'displaced': 13, 'educational_special_needs': 14, 'debtor': 15, 'tuition_fees': 16,
    'gender': 17, 'scholarship': 18, 'age': 19, 'international': 20,
    
    # 1. Semester
    'cur_1_credited': 21, 'cur_1_enrolled': 22, 'cur_1_evaluations': 23, 
    'cur_1_approved': 24, 'cur_1_grade': 25, 'cur_1_without_eval': 26,
    
    # 2. Semester
    'cur_2_credited': 27, 'cur_2_enrolled': 28, 'cur_2_evaluations': 29, 
    'cur_2_approved': 30, 'cur_2_grade': 31, 'cur_2_without_eval': 32,
    
    'unemployment_rate': 33, 'inflation_rate': 34, 'gdp': 35
}

def convert_german_grade(grade_de):
    try:
        g = float(grade_de)
        # Deutsche Noten 1-6 in Punkte 20-0 umwandeln
        pt_grade = 20 - ((g - 1) * 4)
        return max(0, min(20, pt_grade))
    except:
        return 12.0

@app.route('/')
def index():
    # Kein feature_groups mehr nötig, da HTML hardcoded ist
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    form_data = request.form
    
    # 1. Stimmung prüfen (Riskant oder Gut?)
    is_risky_input = False
    if form_data.get('debtor') == '1' or form_data.get('tuition_fees') == '0': is_risky_input = True
    if float(form_data.get('cur_1_grade', 1.0)) > 4.0: is_risky_input = True
    
    # 2. Basis laden
    features = list(DEFAULTS_RISK) if is_risky_input else list(DEFAULTS_GOOD)
    
    # 3. Nationalität (Pflichtfeld)
    user_nation = form_data.get('user_nationality', 'DE')
    if user_nation == 'DE':
        features[IDX['nacionality']] = 1; features[IDX['gdp']] = 1.9; features[IDX['inflation_rate']] = 5.0; features[IDX['unemployment_rate']] = 6.4
    elif user_nation == 'USA':
        features[IDX['nacionality']] = 10; features[IDX['gdp']] = 2.5; features[IDX['inflation_rate']] = 3.5; features[IDX['unemployment_rate']] = 4.2
    elif user_nation == 'PT':
        features[IDX['nacionality']] = 1; features[IDX['gdp']] = 1.0; features[IDX['inflation_rate']] = 1.4; features[IDX['unemployment_rate']] = 3.5

    # 4. Formular-Daten mappen
    for key, val in form_data.items():
        if key in ['user_nationality', 'semester_progress']: continue 
        
        # Spezialfall Noten (Umrechnung)
        if key in ['cur_1_grade', 'cur_2_grade']:
            grade_pt = convert_german_grade(val)
            if key in IDX: features[IDX[key]] = grade_pt
        
        # Normale Werte
        elif key in IDX and val:
            try: features[IDX[key]] = float(val)
            except: pass 

    # 5. DIE LOGIK-WEICHE
    progress = int(form_data.get('semester_progress', 1))
    
    results = {
        'v1': {'status': -1, 'raw_score': 0.0, 'error': 'Nicht aktiv (Nur 1. Semester)', 'n_features': 36},
        'v2': {'status': -1, 'raw_score': 0.0, 'error': 'Nicht aktiv (V1 ist präziser)', 'n_features': 26}
    }

    # FALL A: Nur 1. Semester -> Nutze NUR V2 (schneide Features ab)
    if progress == 1:
        if 'v2' in models:
            features_v2 = features[:26] # Nur die ersten 26 Features
            vector_v2 = np.array(features_v2).reshape(1, -1)
            try:
                prob = models['v2'].predict_proba(vector_v2)[0][1]
                # Logik: >= 0.5 ist Dropout (1)
                results['v2'] = {'status': 1 if prob >= 0.5 else 0, 'raw_score': round(prob, 4), 'n_features': 26}
                results['v1']['error'] = "Deaktiviert: Datenbasis reicht nur für V2"
            except Exception as e:
                results['v2']['error'] = str(e)
    
    # FALL B: Beide Semester -> Nutze NUR V1 (Synce Sem 1 zu Sem 2)
    else:
        # Kopiere Sem 1 Werte auf Sem 2, falls Sem 2 leer ist
        if 'cur_1_grade' in form_data and 'cur_2_grade' not in form_data: features[IDX['cur_2_grade']] = features[IDX['cur_1_grade']]
        if 'cur_1_approved' in form_data and 'cur_2_approved' not in form_data: features[IDX['cur_2_approved']] = features[IDX['cur_1_approved']]
        if 'cur_1_enrolled' in form_data and 'cur_2_enrolled' not in form_data: features[IDX['cur_2_enrolled']] = features[IDX['cur_1_enrolled']]
        if 'cur_1_evaluations' in form_data and 'cur_2_evaluations' not in form_data: features[IDX['cur_2_evaluations']] = features[IDX['cur_1_evaluations']]

        if 'v1' in models:
            vector_v1 = np.array(features).reshape(1, -1)
            try:
                prob = models['v1'].predict_proba(vector_v1)[0][1]
                # Logik: >= 0.5 ist Dropout (1)
                results['v1'] = {'status': 1 if prob >= 0.5 else 0, 'raw_score': round(prob, 4), 'n_features': 36}
                results['v2']['error'] = "Deaktiviert: V1 hat mehr Daten"
            except Exception as e:
                results['v1']['error'] = str(e)

    # Debug Data
    debug_features = []
    for i, val in enumerate(features):
        debug_features.append({'index': i, 'name': FEATURE_NAMES[i], 'value': round(val, 2)})

    return render_template('results.html', 
                           results=results, 
                           input_nation=user_nation, 
                           progress=progress, 
                           mode="RISK" if is_risky_input else "GOOD", 
                           debug_features=debug_features)

if __name__ == '__main__':
    app.run(debug=True, port=5000)