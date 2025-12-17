import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import joblib

if __name__=='__main__':

#Lesen
    df=pd.read_csv("Exercises/Wir-Kaufen-euer-Auto-besser.de/car_price_prediction.csv")

#Bereinigung
    # 1. Levy und ID entfernen
    df=df.drop(columns=['Levy', 'ID'])

    # 2. Mileage bereinigen
    # ' km' entfernen und in Integer umwandeln
    df['Mileage'] = df['Mileage'].str.replace(' km', '')
    df['Mileage'] = df['Mileage'].astype(int)
    

    # 3. Engine volume bereinigen
    df['Engine volume'] = df['Engine volume'].str.replace(' Turbo', '')
    df['Engine volume'] = df['Engine volume'].astype(float)

    # 4. Doors (Türen) korrigieren ---- NOTE: Später in Website 2 in 3 und 4 in 5
    door_mapping = {
        '04-May': 5,
        '02-Mar': 3,
        '>5': 5 
    }
    df['Doors'] = df['Doors'].replace(door_mapping)
    #To retain the old behavior, explicitly call `result.infer_objects(copy=False)`.
    #To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
    #df['Doors'] = df['Doors'].replace(door_mapping)

    # 5. Duplikate entfernen
    initial_rows = len(df)
    df = df.drop_duplicates()
    final_rows = len(df)


    # 6. Umwandeln in Zahlen
    df["Leather interior"] = df["Leather interior"].map({"No": 0, "Yes": 1})
    df["Wheel"] = df["Wheel"].map({"Right-hand drive": 0, "Left wheel": 1})

    # 7. Filtern 
    df = df[df['Price'] > 1000]
    df = df[df['Price'] < 200000] #800.000
    df = df[df['Mileage'] < 500000]
    df = df[df['Cylinders'] >= 3.0]
    df = df[df['Prod. year'] > 1985] #Frage:

    # 7.1
    top_100_models = df['Model'].value_counts().nlargest(100).index.tolist()

    top_30_manufacturer = df['Manufacturer'].value_counts().nlargest(30).index.tolist()

    # 7.11 Die Spalte transformieren 
    df['Model'] = df['Model'].apply(lambda x: x if x in top_100_models else 'Other')

    df['Manufacturer'] = df['Manufacturer'].apply(lambda x: x if x in top_30_manufacturer else 'Other')

    #One-Hot-Encoding
    #Liste der Spalten, die wir umwandeln wollen 
    cols_to_encode = [
    'Category', 
    'Leather interior', 
    'Fuel type', 
    'Gear box type', 
    'Drive wheels',  
    'Color',
    'Model',
    'Manufacturer'
    ]
    df = pd.get_dummies(df, columns=cols_to_encode, dtype=int)

     # --- 5. Split 

    # X (Features) sind alle Spalten außer 'Price'
    X = df.drop(columns=['Price'])
    
    # y (Target) ist der Preis
    y = df['Price']

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=42) #standard 0.2
    
    print(f"Training mit {len(X_train)} Datensätzen, Test mit {len(X_test)} Datensätzen.")

    # --- 6. Modell Training ---

    # Modell initialisieren
    model = RandomForestRegressor(random_state=42, max_depth=None, n_estimators=95, min_samples_split=2, min_samples_leaf=1, n_jobs=-1) 

    print("Training läuft...")
    model.fit(X_train, y_train)

    # Vorhersage
    predictions = model.predict(X_test)

    # --- 7. Auswertung ---
    mae = mean_absolute_error(y_test, predictions)
    mae_sqr=(mean_squared_error(y_test, predictions))**0.5
    r2 = r2_score(y_test, predictions)

    print("\nErgebnisse:")
    print(f"Mean Absolute Error (Durchschnittlicher Fehler): {mae:.2f}")
    print(f"Mean Squared Error (Durchschnittlicher Fehler): {mae_sqr:.2f}")
    print(f"R2 Score (Genauigkeit 0-1): {r2:.4f}")


   

    


    
    """
    # --- 8. Speichern für die Website ---

    print("\nSpeichere Modell und Metadaten...")

    # Wir müssen nicht nur das Modell speichern, sondern auch die Spaltennamen nach dem One-Hot-Encoding,
    # damit die Website die Eingabedaten in genau die gleiche Form bringen kann.
    model_data = {
        "model": model,
        "columns": X_train.columns,  # Die fertigen Spaltennamen (inkl. dummies)
        "top_100_models": top_100_models,
        "top_30_manufacturer": top_30_manufacturer

    }

    joblib.dump(model_data, "car_price_model03Experiment.pkl")
    print("Gespeichert als 'car_price_model03Experiment.pkl'")
    """