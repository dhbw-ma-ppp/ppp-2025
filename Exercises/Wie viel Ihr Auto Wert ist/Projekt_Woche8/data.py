import pandas as pd
from sys import path as system_paths
from sklearn.preprocessing import OneHotEncoder

# load data
df:pd.DataFrame = pd.read_csv(system_paths[0]+"/car_price_prediction.csv")

# delete opal astra
to_great_prices = 10_000_000
df = df.query("Price < 100_000").reset_index(drop=True)
df = df.query("Price > 1000").reset_index(drop=True)

# delete features
for feature in [
    "ID",
    "Levy",
    "Doors",
]:
    df = df.drop(feature, axis="columns")

# mapping the Features to numerous values
for feature, map in [
    ("Leather interior", {"No":0, "Yes":1}),
    ("Wheel", {"Left wheel":0, "Right-hand drive":1}),
    ("Airbags", int),
    #("Airbags", lambda txt: (1-int(txt) % 2)*100000), # todo believe in grade airbags
    ("Engine volume", lambda txt: float(txt.replace("Turbo",""))),
    # sortiert nach automatisierung
    ("Mileage", lambda txt: int(txt[:-2])),
    ("Drive wheels", lambda txt: int(txt == "Rear")),
    ("Gear box type", {"Automatic":0, "Tiptronic":1, "Manual":2, "Variator":3})
]:
    df[feature] = df[feature].map(map)


# Drop the top 10 most expensive cars from each unique feature values

indices_to_drop = []
for feature in df.columns:
    unique_feature_values = df[feature].unique()

    # skip features which have to many unique values
    if len(unique_feature_values) > 24:
        continue

    for unique_feature_value in unique_feature_values:
        top_entries = df[df[feature] == unique_feature_value].nlargest(10, 'Price')
        indices_to_drop.extend(top_entries.index)
    
df = df.drop(indices_to_drop)
df = df.dropna()

# multiple values in price order
for feature in [
    "Color",
    "Model",
    "Manufacturer",
    "Category",
    "Fuel type",
    "Wheel",
    "Gear box type",
    "Airbags"
]:
    sorted_features = df.groupby(feature)['Price'].median().sort_values()
    maping = {feature: index for index, feature in enumerate(sorted_features.index)}
    df[feature] = df[feature].map(maping)


# Clean data from exceptions
df = df[~(df['Prod. year'] < 1985)]
df = df[~((df['Engine volume'] > 10))] # enable

print(df.info())
df = df.dropna()
if __name__ == "__main__":
    print(df.head())
    print(df.info())


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

        nan_spalten = df.isna().any()
        print("Nan Spalten:")
        print(nan_spalten)
        print(df.shape)

#todo wie wichtig ist petrol?