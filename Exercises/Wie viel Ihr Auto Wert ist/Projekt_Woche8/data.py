import pandas as pd
from sys import path as system_paths
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt


def plt_feature(df, feature):
    plt.figure(figsize=(10, 6))
    plt.scatter(df[feature], df['Price'], color='blue', marker='o')
    plt.title(feature+' vs. Price')
    plt.xlabel(feature)
    plt.ylabel('Price (in Euro)')
    plt.grid(True)
    plt.show()

# load data
df:pd.DataFrame = pd.read_csv(system_paths[0]+"/car_price_prediction.csv")

df = df[~(df['Price'] > 400_000)]
df = df[~(df['Price'] < 1000)]

# delete features
for feature in [
    "ID",
    "Levy",
    "Doors",
]:
    df = df.drop(feature, axis="columns")

if False:
    # Clean data from exceptions
    # Drop the top 10 most expensive cars from each unique feature values
    indices_to_drop = []
    for feature in df.columns:
        
        unique_feature_values = df[feature].unique()

        # skip features which have to many unique values
        if len(unique_feature_values) > 24:
            continue

        for unique_feature_value in unique_feature_values:
            top_entries = df[df[feature] == unique_feature_value].nlargest(0, "Price")
            indices_to_drop.extend(top_entries.index)

    df = df.drop(indices_to_drop)
    df = df.dropna()

feature_casts = {
    "Leather interior": {"No":0, "Yes":1},
    "Wheel": {"Left wheel":0, "Right-hand drive":1},
    "Airbags": int,
    #("Airbags", lambda txt: (1-int(txt) % 2)*100000), # todo believe in grade airbags
    "Engine volume": lambda txt: float(txt.replace("Turbo","")),
    # sortiert nach automatisierung
    "Mileage": lambda txt: int("".join(c for c in str(txt) if c.isdigit())) if str(txt).strip() != "" else None,
    "Drive wheels": lambda txt: int(txt == "Rear"),
    "Gear box type": {"Automatic":0, "Tiptronic":1, "Manual":2, "Variator":3}
}

# features to numerous values
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



# delete models which were just once 5 times
df = df.groupby('Model').filter(lambda x: len(x) > 5)

feature_value_to_df_value = {}

#for unique_feature_value in unique_feature_values:
    #top_entries = df[df[feature] == unique_feature_value].nlargest(10, 'Price')
    #indices_to_drop.extend(top_entries.index)

#df = df.drop(indices_to_drop)
df = df.dropna()

df = df[~(df['Prod. year'] < 1985)]
df = df[~((df['Engine volume'] > 19))]

# multiple values in price order
features_in_median_order = [
    "Color",
    "Model",
    "Manufacturer",
    "Category",
    "Fuel type",
    "Wheel",
    "Gear box type",
    "Airbags",
    "Leather interior",
]
for feature in features_in_median_order:
    medians = df.groupby(feature)['Price'].median()
    mapping = medians.to_dict()

    final_mapping = {key: value for key, value in mapping.items()}
    df[feature] = df[feature].map(final_mapping)

    feature_value_to_df_value[feature] = final_mapping
    feature_value_to_df_value[feature][None] = medians.median()


def feature_value_to_ai_value(feature: str, feature_value: str) -> tuple[float, bool]:
    if feature not in df.columns:
        raise RuntimeError(
            "You can not convert a feature value to an ai value if the feature of this feature value does not exist!"
        )

    # cast if necessary
    if feature in feature_casts:
        caster = feature_casts[feature]

        # Leerer Wert -> wir überlassen das der aufrufenden Logik (z.B. Median in Flask)
        if feature_value is None or str(feature_value).strip() == "":
            feature_value = None
        else:
            # dict-Mapping (z.B. Leather interior, Wheel, Gear box type)
            if isinstance(caster, dict):
                feature_value = caster.get(feature_value, None)
            else:
                # Funktion (int, lambda ...)
                feature_value = caster(feature_value)

    # Kategorie-Features, die über Median-Mapping laufen
    if feature in features_in_median_order:
        if feature_value in feature_value_to_df_value[feature]:
            return feature_value_to_df_value[feature][feature_value], True
        else:
            # Fallback: globaler Median dieser Kategorie
            return feature_value_to_df_value[feature][None], False
    else:
        # Numerische oder sonstige Features → direkt nutzen
        return feature_value, True



df = df[~(df['Prod. year'] < 1985)]
df = df[~((df['Engine volume'] > 19))]

# print(df.info())
df = df.dropna()
if __name__ == "__main__":
    print(df.head())
    print(df.info())


    for feature in df.columns.tolist():
        if feature != "Engine volume":
            continue
        plt_feature(df, feature)

        nan_spalten = df.isna().any()
        print("Nan Spalten:")
        print(nan_spalten)
        print(df.shape)
#todo wie wichtig ist petrol?

for feature in [
]:
    df = df.drop(feature, axis="columns")