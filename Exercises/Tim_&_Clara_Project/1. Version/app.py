from flask import Flask, render_template, request
import pickle
import numpy as np
import os

app = Flask(__name__)

# ==============================================================================
# 1. FEATURE DEFINITION & CONFIG
# ==============================================================================
FEATURE_GROUPS = {
    "Persönlich & Demografie": [
        {"id": "card-age", "label": "Alter", "name": "age", "type": "number", "value": 20},
        {"id": "card-gender", "label": "Geschlecht", "name": "gender", "type": "select", "options": [{"v": 1, "t": "Männlich"}, {"v": 0, "t": "Weiblich"}]},
        {"id": "card-marital", "label": "Familienstand", "name": "marital_status", "type": "select", "options": [{"v": 1, "t": "Ledig"}, {"v": 2, "t": "Verheiratet"}, {"v": 4, "t": "Geschieden"}]}
    ],
    "Sozioökonomisch": [
        {"id": "card-scholarship", "label": "Stipendiat?", "name": "scholarship", "type": "select", "options": [{"v": 0, "t": "Nein"}, {"v": 1, "t": "Ja"}]},
        {"id": "card-debtor", "label": "Schulden?", "name": "debtor", "type": "select", "options": [{"v": 0, "t": "Nein"}, {"v": 1, "t": "Ja"}]},
        {"id": "card-fees", "label": "Studiengebühren bezahlt?", "name": "tuition_fees", "type": "select", "options": [{"v": 1, "t": "Ja"}, {"v": 0, "t": "Nein"}]}
    ],
    "Leistung: 1. Semester": [
        {"id": "card-cur1-grade", "label": "Note 1. Sem (Ø)", "name": "cur_1_grade", "type": "number", "value": 2.5, "step": 0.1},
        {"id": "card-cur1-approved", "label": "Kurse bestanden (1. Sem)", "name": "cur_1_approved", "type": "number", "value": 4},
        {"id": "card-cur1-enrolled", "label": "Kurse angemeldet (1. Sem)", "name": "cur_1_enrolled", "type": "number", "value": 5}
    ],
    "Leistung: 2. Semester": [
        {"id": "card-cur2-grade", "label": "Note 2. Sem (Ø)", "name": "cur_2_grade", "type": "number", "value": 2.5, "step": 0.1},
        {"id": "card-cur2-approved", "label": "Kurse bestanden (2. Sem)", "name": "cur_2_approved", "type": "number", "value": 4},
         {"id": "card-cur2-enrolled", "label": "Kurse angemeldet (2. Sem)", "name": "cur_2_enrolled", "type": "number", "value": 5}
    ],
    "Hintergrund": [
         {"id": "card-mother-job", "label": "Beruf Mutter", "name": "mother_occupation", "type": "select", "options": [{"v": 5, "t": "Angestellte"}, {"v": 1, "t": "Führungskraft"}]},
        {"id": "card-mother-qual", "label": "Bildung Mutter", "name": "mother_qualification", "type": "select", "options": [{"v": 3, "t": "Sekundarstufe"}, {"v": 1, "t": "Hochschulabschluss"}]}
    ],
    "Studium": [
        {"id": "card-course", "label": "Studiengang", "name": "course", "type": "select", "options": [{"v": 33, "t": "Management"}, {"v": 9119, "t": "Informatik"}]},
        {"id": "card-app-mode", "label": "Bewerbung", "name": "application_mode", "type": "select", "options": [{"v": 1, "t": "Normal"}, {"v": 17, "t": "2. Phase"}]}
    ]
}

FEATURE_NAMES = ["0: Marital", "1: AppMode", "2: AppOrd", "3: Course", "4: Day", "5: PrevQ", "6: PrevQG", "7: Nat", "8: MothQ", "9: FathQ", "10: MothJ", "11: FathJ", "12: AdmG", "13: Disp", "14: EduN", "15: Debt", "16: Fees", "17: Gen", "18: Schol", "19: Age", "20: Intl", "21: C1Cred", "22: C1Enr", "23: C1Eval", "24: C1Appr", "25: C1Grd", "26: C1NoEv", "27: C2Cred", "28: C2Enr", "29: C2Eval", "30: C2Appr", "31: C2Grd", "32: C2NoEv", "33: Unemp", "34: Infl", "35: GDP"]

# --- MODELLE LADEN ---
models = {}
for version in ['v1', 'v2']:
    path = f'model_{version}.pkl'
    if os.path.exists(path):
        with open(path, 'rb') as f:
            models[version] = pickle.load(f)

# --- DEFAULTS ---
DEFAULTS_GOOD = [1, 1, 5, 33, 1, 1, 140, 1, 3, 3, 5, 5, 140, 1, 0, 0, 1, 0, 0, 19, 0, 0, 5, 6, 5, 14.0, 0, 0, 5, 6, 5, 14.0, 0, 10.0, 1.4, 0.0]
DEFAULTS_RISK = [1, 1, 5, 33, 1, 1, 100, 1, 4, 4, 9, 9, 100, 1, 0, 1, 0, 0, 0, 35, 0, 0, 5, 6, 2, 10.0, 0, 0, 5, 6, 2, 10.0, 0, 10.0, 1.4, 0.0]

# Mapping (Vollständig)
IDX = {
    'marital_status': 0, 'application_mode': 1, 'course': 3, 'nacionality': 7, 
    'mother_qualification': 8, 'father_qualification': 9, 'mother_occupation': 10, 'father_occupation': 11, 
    'displaced': 13, 'debtor': 15, 'tuition_fees': 16, 'gender': 17, 'scholarship': 18, 'age': 19, 'international': 20,
    'cur_1_enrolled': 22, 'cur_1_approved': 24, 'cur_1_grade': 25, 
    'cur_2_enrolled': 28, 'cur_2_approved': 30, 'cur_2_grade': 31, 
    'inflation': 34, 'gdp': 35
}

def convert_german_grade(grade_de):
    try:
        g = float(grade_de)
        pt_grade = 20 - ((g - 1) * 4)
        return max(0, min(20, pt_grade))
    except: return 12.0

@app.route('/')
def index():
    return render_template('index.html', feature_groups=FEATURE_GROUPS)

@app.route('/predict', methods=['POST'])
def predict():
    form_data = request.form
    
    # 1. Stimmung prüfen
    is_risky_input = False
    if form_data.get('debtor') == '1' or form_data.get('tuition_fees') == '0': is_risky_input = True
    if float(form_data.get('cur_1_grade', 1.0)) > 4.0: is_risky_input = True
    
    features = list(DEFAULTS_RISK) if is_risky_input else list(DEFAULTS_GOOD)
    
    # 2. User Daten mappen
    user_nation = form_data.get('user_nationality', 'DE')
    if user_nation == 'DE': features[IDX['nacionality']] = 1; features[IDX['gdp']] = 1.9; features[IDX['inflation']] = 5.0
    elif user_nation == 'USA': features[IDX['nacionality']] = 10; features[IDX['gdp']] = 2.5; features[IDX['inflation']] = 3.5
    elif user_nation == 'PT': features[IDX['nacionality']] = 1; features[IDX['gdp']] = 1.0; features[IDX['inflation']] = 1.4

    for key, val in form_data.items():
        if key in ['user_nationality', 'semester_progress']: continue 
        if key in ['cur_1_grade', 'cur_2_grade']:
            grade_pt = convert_german_grade(val)
            if key in IDX: features[IDX[key]] = grade_pt
        elif key in IDX and val:
            try: features[IDX[key]] = float(val)
            except: pass 

    # --- DIE ENTSCHEIDUNG: WELCHES MODELL? ---
    progress = int(form_data.get('semester_progress', 1))
    
    # Standard: Beide auf "Nicht genutzt" setzen
    results = {
        'v1': {'status': -1, 'raw_score': 0.0, 'error': 'Nicht aktiv (Nur 1. Semester)'},
        'v2': {'status': -1, 'raw_score': 0.0, 'error': 'Nicht aktiv (V1 ist präziser)'}
    }

    # FALL A: Nur 1. Semester -> Nutze V2
    if progress == 1:
        if 'v2' in models:
            # Nur ersten 26 Features nehmen
            features_v2 = features[:26]
            vector_v2 = np.array(features_v2).reshape(1, -1)
            try:
                prob = models['v2'].predict_proba(vector_v2)[0][1]
                # Logik: >= 0.5 ist Dropout
                results['v2'] = {'status': 1 if prob >= 0.5 else 0, 'raw_score': round(prob, 4), 'n_features': 26}
                # Hinweis für V1 setzen
                results['v1']['error'] = "Deaktiviert: Datenbasis reicht nur für V2"
            except Exception as e:
                results['v2']['error'] = str(e)
    
    # FALL B: Beide Semester -> Nutze V1
    else:
        # Sync Logik (Lückenfüller Sem 2)
        if 'cur_1_grade' in form_data and 'cur_2_grade' not in form_data: features[IDX['cur_2_grade']] = features[IDX['cur_1_grade']]
        if 'cur_1_approved' in form_data and 'cur_2_approved' not in form_data: features[IDX['cur_2_approved']] = features[IDX['cur_1_approved']]
        if 'cur_1_enrolled' in form_data and 'cur_2_enrolled' not in form_data: features[IDX['cur_2_enrolled']] = features[IDX['cur_1_enrolled']]

        if 'v1' in models:
            vector_v1 = np.array(features).reshape(1, -1)
            try:
                prob = models['v1'].predict_proba(vector_v1)[0][1]
                # Logik: >= 0.5 ist Dropout
                results['v1'] = {'status': 1 if prob >= 0.5 else 0, 'raw_score': round(prob, 4), 'n_features': 36}
                # Hinweis für V2 setzen
                results['v2']['error'] = "Deaktiviert: V1 hat mehr Daten"
            except Exception as e:
                results['v1']['error'] = str(e)

    # Debug Data
    debug_features = []
    for i, val in enumerate(features):
        debug_features.append({'index': i, 'name': FEATURE_NAMES[i], 'value': round(val, 2)})

    return render_template('results.html', results=results, input_nation=user_nation, progress=progress, mode="RISK" if is_risky_input else "GOOD", debug_features=debug_features)

if __name__ == '__main__':
    app.run(debug=True, port=5000)