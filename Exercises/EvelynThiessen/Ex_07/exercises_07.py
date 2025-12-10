import pandas as pd
import numpy as np

df = pd.read_csv("Exercises\EvelynThiessen\Ex_07\exercise_cave.txt", dtype=str, header=None, names=["columns"])
df_digits = df["columns"].apply(lambda x: pd.Series(list(x))).astype(int) 

x, y = df_digits.shape

distanzes = np.full((x,y), np.inf) #Erstellt Array das komplett mit unendlich gefüllt ist 
#Soll die Distanzen zu dem Punkt 0,0 speichern
distanzes[0,0] = df_digits.iloc[0,0] #Anfangs Entfernung

for i in range(x):
    for j in range(y): #durch iterieren und die Distanz immer vergleichen (ob links oder rechts größer ist)
        if i > 0: # solang wir nicht in der ersten Zeile sind, können wir schauen, was über uns ist
            distanzes[i, j] = min(distanzes[i, j] , distanzes[i-1, j] + df_digits.iloc[i, j])
        if j > 0: #solang wir nicht in der ersten Spalte sind können wir schauen, was links von uns ist
            distanzes[i, j] = min(distanzes[i, j], distanzes[i, j-1] + df_digits.iloc[i, j]) 
    print(distanzes)

print("Full Matrix:")
print(distanzes)

print("kürzester Weg: " + str(distanzes[99][99]))
# 517