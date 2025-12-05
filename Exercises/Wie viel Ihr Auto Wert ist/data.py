import pandas as pd
from sys import path as system_paths
import 

# load data
car_price_prediction_data = pd.read_csv(system_paths[0]+"/car_price_prediction.csv")


# delete unecessary features
unecessary_features = [
    "ID",
    "Levy",
    "Color" # später testen, cast auf 3 featrues (rgb)
]
for feature in unecessary_features:
    car_price_prediction_data = car_price_prediction_data.drop(feature, axis="columns")

# mapping

feature = "Leather interior"
car_price_prediction_data[feature] = car_price_prediction_data[feature].map({"No":0, "Yes":1})

feature = ""
# ordinal encoding
# one hot encoding
# value encoding
print(car_price_prediction_data.head())
print(car_price_prediction_data.info())