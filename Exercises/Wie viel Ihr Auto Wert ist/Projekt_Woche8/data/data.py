import pandas as pd
from sys import path as system_paths
from sklearn.preprocessing import OneHotEncoder

# load data
df:pd.DataFrame = pd.read_csv(system_paths[0]+"/car_price_prediction.csv")

# delete opal astra
to_great_prices = 10_000_000
df = df.query("Price < 160000").reset_index(drop=True)
#df = df.query("Price > 1000").reset_index(drop=True)

df = df.drop("Wheel", axis="columns")

#df = df.drop("Airbags", axis="columns")
#df["Prod. year"] = df["Prod. year"] - 2000

# ToDo


# delete unecessary features
unecessary_features = [
    "ID",
    "Levy"
]
for feature in unecessary_features:
    df = df.drop(feature, axis="columns")

# delete important features which are not convertable
important_features = [
    "Model",
    "Manufacturer",
    "Color",
    "Category",
    "Fuel type",
    #"Leather interior",
    "Doors",
    #"Mileage"
    #"Gear box type"
]
for feature in important_features:
    df = df.drop(feature, axis="columns")

# split_features
if False:
    feature = "Engine volume"
    new_feature_name = "Has turbo engine"
    df[new_feature_name] = df[feature].map(lambda txt: "Turbo" in txt)


# mapping the Features to numerous values
for feature, map in [
    ("Leather interior", {"No":0, "Yes":1}),
    # soritert nach Anzahl der Türen
    #("Doors", {"02-Mar":2, "04-May":4, ">5": 6}),
    #("Wheel", {"Left wheel":0, "Right-hand drive":1}),
    ("Airbags", int),
    #("Airbags", lambda txt: (1-int(txt) % 2)*100000), # todo believe in grade airbags
    ("Engine volume", lambda txt: float(txt.replace("Turbo",""))),
    # sortiert nach automatisierung
    ("Gear box type",{"Manual":0,"Tiptronic":1,"Variator":2,"Automatic":3}) ,
    ("Mileage", lambda txt: int(txt[:-2])),
    ("Drive wheels", lambda txt: txt == "Rear")
]:
    df[feature] = df[feature].map(map)

#df = df.query("Mileage < 10000").reset_index(drop=True)



hot_encoding_features = [
        "Manufacturer",
        "Model",
        "Category",
        "Fuel type", # später mal testen in einem feature
        #"Drive wheels",
        "Color",
        #"Gear box type"
        ]
for feature in important_features:
    if feature in hot_encoding_features:
        hot_encoding_features.remove(feature)

if True:
    encoder = OneHotEncoder(sparse_output=False)
    encoded_features = encoder.fit_transform(df[hot_encoding_features])
    encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(hot_encoding_features))

    df = df.drop(columns=hot_encoding_features) 

    df = pd.concat([df, encoded_df], axis=1) 
else:
    df = df.drop(hot_encoding_features, axis="columns")



if __name__ == "__main__":
    print(df.head())
    print(df.info())

    if False:
        feature = "Doors"
        for name in df[feature].unique():
            print(name)


    for feature in df.columns.tolist():
        print(feature)
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 6))
        plt.scatter(df[feature], df['Price'], color='blue', marker='o')
        plt.title(feature+' vs. Price')
        plt.xlabel(feature)
        plt.ylabel('Price (in Euro)')
        plt.grid(True)
        plt.show()