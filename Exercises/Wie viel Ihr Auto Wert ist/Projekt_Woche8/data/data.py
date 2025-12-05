import pandas as pd
from sys import path as system_paths
<<<<<<< Updated upstream
from sklearn.preprocessing import OneHotEncoder
=======

>>>>>>> Stashed changes

# load data
df = pd.read_csv(system_paths[0]+"/car_price_prediction.csv")


# delete unecessary features
unecessary_features = [
    "ID",
    "Levy",
    "Color", # später testen, cast auf 3 featrues (rgb)
]
for feature in unecessary_features:
    df = df.drop(feature, axis="columns")

# delete important features which are not convertable
important_features = [
    "Model",
    #"Manufacturer"
]
for feature in important_features:
    df = df.drop(feature, axis="columns")

# split_features
feature = "Engine volume"
new_feature_name = "Has turbo engine"
df[new_feature_name] = df[feature].map(lambda txt: "Turbo" in txt)


# mapping the Features to numerous values
for feature, map in [
    ("Leather interior", {"No":0, "Yes":1}),
    # soritert nach Anzahl der Türen
    ("Doors", {"02-Mar":2, "04-May":4, ">5": 6}),
    ("Wheel", {"Left wheel":0, "Right-hand drive":1}),
    ("Airbags", int),
    ("Engine volume", lambda txt: float(txt.replace("Turbo",""))),
    # sortiert nach automatisierung
    ("Gear box type",{"Manual":0,"Tiptronic":1,"Variator":2,"Automatic":3}) ,
    ("Mileage", lambda txt: int(txt[:-2]))
]:
    df[feature] = df[feature].map(map)


hot_encoding_features = [
    "Manufacturer",
    #"Model",
    "Category",
    "Fuel type", # später mal testen in einem feature
    "Drive wheels",
    ]

encoder = OneHotEncoder(sparse_output=False)
encoded_features = encoder.fit_transform(df[hot_encoding_features])
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(hot_encoding_features))

df = df.drop(columns=hot_encoding_features) 
df = pd.concat([df, encoded_df], axis=1) 

if __name__ == "__main__":
    print(df.head())
    print(df.info())

    if False:
        feature = "Doors"
        for name in df[feature].unique():
            print(name)
