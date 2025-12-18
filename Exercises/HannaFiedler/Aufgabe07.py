# - Solve the exercise described at https://adventofcode.com/2021/day/15 using the data at `data/exercise_cave.txt` as input. Prepare a PR as usual.
import numpy as np
import pandas as pd

def find_lowest_risk(risks):
    #Oben links anfangen
    pos = (0,0)
    rows = len(risks)
    columns = len(risks[0])
    #Ausgang ist unten links
    end = (rows-1, columns-1)

    #Matrix um das niedrigste Risiko der Position zu speichern
    optimal = np.zeros((rows, columns), dtype=float)
    optimal[pos] = risks[pos]

    #Matrix um das zwischenzeitlich niedrigste Risiko zu speichern
    best = np.full((rows, columns), np.inf)
    best[pos] = risks[pos]

    #Matrix um festzuhalten, welche Positionen schon das geringste Risiko haben / welche schon besucht wurden
    visited = np.zeros((rows, columns), dtype=bool)

    while True:
        row, column = pos
        visited[row, column] = True

        neighbours = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        #Prüfen ob der neue Weg zu den angrenzenden Positionen ein geringeres Risiko hat als die vorherigen
        for row_change, column_change in neighbours:
            neighbour_row, neighbour_column = row + row_change, column + column_change

            if 0 <= neighbour_row < rows and 0 <= neighbour_column < columns and not visited[neighbour_row, neighbour_column]:
                new_best = optimal[pos] + risks[neighbour_row, neighbour_column]

                if new_best < best[neighbour_row, neighbour_column]:
                    best[neighbour_row, neighbour_column] = new_best
            
        #Position mit migeringsten Risiko der noch nicht besuchten Positionen
        best_masked = np.where(visited, np.inf, best)
        min = np.unravel_index(np.argmin(best_masked), best_masked.shape)
        
        #Minimales Risiko in endgültige Matrix einfügen
        optimal[min] = best[min]

        #Prüfen, ob das minimale Risiko zum Ausgang gefunden wurde
        if min == end:
            #print_result(best, optimal, visited)
            return optimal[min]
        
        #Bei dem Minimum fortfahren
        pos = min

#Zur Kontrolle
def print_result(best, optimal, visited):
    print("Best:", best, "\n")
    print("optimal:", optimal, "\n")
    print("Visited:", visited, "\n")

from sys import path as system_path

risks = pd.read_csv(system_path[0]+"/cavern.txt", dtype=str, header=None, names=["columns"])
risks = risks["columns"].apply(lambda x: pd.Series(list(x))).astype(int)
risks = risks.to_numpy()
print("The lowest total risk is:", int(find_lowest_risk(risks)))