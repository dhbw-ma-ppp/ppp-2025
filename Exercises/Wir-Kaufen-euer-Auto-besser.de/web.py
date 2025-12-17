import streamlit as st
import pandas as pd
import joblib

# 1. Laden des gespeicherten Modells und der Infos
data = joblib.load("car_price_model03Experiment.pkl")
model = data["model"]
model_columns = data["columns"]
top_100_models = data["top_100_models"]
top_30_manufacturer = data["top_30_manufacturer"]

st.title("Wir-Kaufen-Euer-Auto-Besser.de")
st.write("Geben Sie die Daten des Autos ein, um den geschätzten Preis zu erhalten.")

# --- 2. Eingabeformular für den Benutzer ---

# Wir gruppieren die Eingaben für bessere Übersicht
col1, col2 = st.columns(2)

with col1:
    manufacturer = st.selectbox("Hersteller", top_30_manufacturer + ["Other"])
    model_name = st.text_input("Modell (z.B. Camry, E 220, etc.)")
    prod_year = st.number_input("Baujahr", min_value=1950, max_value=2025, value=2015)
    category = st.selectbox("Kategorie", ['Jeep', 'Hatchback', 'Sedan', 'Microbus', 'Goods wagon', 'Universal', 'Coupe', 'Minivan', 'Pickup', 'Cabriolet', 'Limousine'])
    leather = st.radio("Lederausstattung", ["Yes", "No"])

with col2:
    fuel = st.selectbox("Kraftstoff", ['Hybrid', 'Petrol', 'Diesel', 'CNG', 'Plug-in Hybrid', 'LPG', 'Hydrogen'])
    engine_vol = st.number_input("Motorvolumen (z.B. 2.0)", value=2.0)
    mileage = st.number_input("Kilometerstand", value=100000)
    cylinders = st.number_input("Zylinder", value=4.0)
    gearbox = st.selectbox("Getriebe", ['Automatic', 'Tiptronic', 'Variator', 'Manual'])
    drive_wheels = st.selectbox("Antrieb", ['4x4', 'Front', 'Rear'])
    doors = st.selectbox("Türen", ["2-3", "4-5", ">5"])
    wheel = st.radio("Lenkrad", ["Left wheel", "Right-hand drive"])
    color = st.selectbox("Farbe", ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Green', 'Orange', 'Brown', 'Carnelian red', 'Golden', 'Beige', 'Sky blue', 'Yellow', 'Purple', 'Pink'])
    airbags = st.number_input("Airbags", value=4)

# Button zum Berechnen
if st.button("Preis berechnen"):
    
    # --- 3. Datenvorverarbeitung (Muss exakt wie im Training sein!) ---
    
    # Mapping für Doors
    doors_mapped = 5 # Default
    if doors == "2-3": doors_mapped = 3
    elif doors == "4-5": doors_mapped = 5
    elif doors == ">5": doors_mapped = 5
    
    # Mapping Ja/Nein
    leather_mapped = 1 if leather == "Yes" else 0
    wheel_mapped = 1 if wheel == "Left wheel" else 0
    
    # Handling Top 50 Models & Top 25 Manufacturer
    # Wenn User etwas eingibt, was nicht in der Top-Liste ist -> "Other"
    processed_model = model_name if model_name in top_100_models else "Other"
    processed_manufacturer = manufacturer if manufacturer in top_30_manufacturer else "Other"

    # Erstellen eines DataFrames mit EINER Zeile (den User-Eingaben)
    input_data = pd.DataFrame({
        'Prod. year': [prod_year],
        'Category': [category],
        'Leather interior': [leather_mapped],
        'Fuel type': [fuel],
        'Engine volume': [engine_vol],
        'Mileage': [mileage],
        'Cylinders': [cylinders],
        'Gear box type': [gearbox],
        'Drive wheels': [drive_wheels],
        'Doors': [doors_mapped],
        'Wheel': [wheel_mapped],
        'Color': [color],
        'Airbags': [airbags],
        'Manufacturer': [processed_manufacturer],
        'Model': [processed_model]
    })

    # One-Hot-Encoding anwenden
    # Wir sagen pandas, welche Spalten es umwandeln soll (die gleichen wie im Training)
    cols_to_encode = [
        'Category', 'Leather interior', 'Fuel type', 'Gear box type', 
        'Drive wheels', 'Color', 'Model', 'Manufacturer'
    ]
    
    # Achtung: get_dummies erzeugt hier nur Spalten für das, was ausgewählt wurde (z.B. nur "Color_Black").
    # Das Modell erwartet aber AUCH "Color_Red" (mit Wert 0).
    input_data_encoded = pd.get_dummies(input_data, columns=cols_to_encode, dtype=int)

    # --- 4. Angleichung an das Modell (Der wichtigste Schritt!) ---
    # Wir erzwingen, dass der Input exakt die gleichen Spalten hat wie das Training
    # Fehlende Spalten werden mit 0 aufgefüllt.
    input_data_final = input_data_encoded.reindex(columns=model_columns, fill_value=0)

    # --- 5. Vorhersage ---
    prediction = model.predict(input_data_final)
    
    st.success(f"Geschätzter Preis: {prediction[0]:,.2f}€")