import pandas as pd

from data import df
from sklearn.model_selection import train_test_split


if __name__ == "__main__":
    print(df.head())
    print(df.info())

df:pd.DataFrame = df

target = "Price"
x = df.drop(target, axis="columns")
y = df[[target]]

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2, random_state=42) # stratify=y.map(int)//1000
