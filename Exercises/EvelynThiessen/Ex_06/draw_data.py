import numpy as np
import pandas as pd
from collections import Counter
from matplotlib import pyplot as plt 

fig = plt.figure(figsize=(10,10))
sub_1 = fig.add_subplot(3,2,1)
sub_2 = fig.add_subplot(3,2,2)
sub_3 = fig.add_subplot(3,2,3)
sub_4 = fig.add_subplot(3,2,4)
sub_6 = fig.add_subplot(3,2,5)
plt.subplots_adjust(hspace=0.5)

def draw(df):
    female_not_survived = df[(df['Survived'] == 0) & (df['Sex'] == 'female')]
    male_not_survived = df[(df['Survived'] == 0) & (df['Sex'] == 'male')]

    draw_deaths_per_gender(len(female_not_survived), len(male_not_survived))

    pers_per_class_not_survived = df.loc[(df['Survived'] == 0), "Pclass"]
    draw_deaths_per_class(pers_per_class_not_survived)

    not_survived_per_age = df.loc[(df['Survived'] == 0), "Age"]
    draw_deaths_per_age(not_survived_per_age)

    not_survived_per_embark = df.loc[(df['Survived'] == 0), 'Embarked']
    draw_deaths_per_embarked(not_survived_per_embark)

    missing = df.isna()
    missing_features(missing, df.columns)

    plt.show()


def draw_deaths_per_gender(f, m):
    sub_1.set_xlabel("Gender")
    sub_1.set_ylabel("Deahts")

    sub_1.bar("female", f, color = "pink")
    sub_1.bar("male", m, color = "blue")

def draw_deaths_per_class(f):
    sub_2.set_xlabel("Passenger Classes")
    sub_2.set_ylabel("Deaths")

    sub_2.bar("Class 1", f.value_counts()[1])
    sub_2.bar("Class 2", f.value_counts()[2])
    sub_2.bar("Class 3", f.value_counts()[3])

def draw_deaths_per_age(a):
    sub_3.set_xlabel("Age")
    sub_3.set_ylabel("Deaths")
    sub_3.locator_params(axis="both", integer="true")

    a_counts = Counter(a)
    sub_3.bar(a_counts.keys(), a_counts.values())

def draw_deaths_per_embarked(e):
    sub_4.set_xlabel("Embarked")
    sub_4.set_ylabel("Deaths")

    sub_4.bar("Southampton", (e == 'S').sum(), color="red")
    sub_4.bar("Cherbourg", (e == 'C').sum(), color="pink")
    sub_4.bar("Queenstown", (e == 'Q').sum(), color="purple")

def missing_features(missing, c):
    sub_6.imshow(missing.T, cmap='Pastel1_r', aspect='auto', interpolation='none')
    
    sub_6.set_yticks(range(len(c)), c)




