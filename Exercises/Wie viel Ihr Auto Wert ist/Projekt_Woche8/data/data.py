import pandas as pd
from sys import path as system_paths
from sklearn.preprocessing import OneHotEncoder

# load data
car_price_prediction_data = pd.read_csv(system_paths[0]+"/car_price_prediction.csv")


# delete unecessary features
unecessary_features = [
    "ID",
    "Levy",
    "Color", # später testen, cast auf 3 featrues (rgb)
]
for feature in unecessary_features:
    car_price_prediction_data = car_price_prediction_data.drop(feature, axis="columns")

# split_features
feature = "Engine volume"
new_feature_name = "Has turbo engine"
car_price_prediction_data[new_feature_name] = car_price_prediction_data[feature].map(lambda txt: "Turbo" in txt)
#car_price_prediction_data.add(car_price_prediction_data[feature].map(lambda txt: "Turbo" in txt))


# mapping

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
    car_price_prediction_data[feature] = car_price_prediction_data[feature].map(map)


hot_encoding_features = [
    "Manufacturer",
    "Model",
    "Category",
    "Drive wheels",
    ]
# ordinal encoding
# one hot encoding
# value encoding

#OneHotEncoder(host_encoding_features)



# Diesel, Petrol, Hybrid, E
# Alle Gase
print(car_price_prediction_data.head())
print(car_price_prediction_data.info())


feature = "Fuel type"
for name in car_price_prediction_data[feature].unique():
    print(name)
