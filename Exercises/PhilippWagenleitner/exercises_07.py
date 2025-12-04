#You've almost reached the exit of the cave, but the walls are getting closer
# together. Your submarine can barely still fit, though; the main problem is
# that the walls of the cave are covered in chitons, and it would be best not
# to bump any of them.
# The cavern is large, but has a very low ceiling, restricting your motion to
# two dimensions. The shape of the cavern resembles a square; a quick scan
# of chiton density produces a map of risk level throughout the cave
# (your puzzle input).
# 
# 
# You start in the top left position, your destination is the bottom right position,
# and you cannot move diagonally. The number at each position is its risk level;
# to determine the total risk of an entire path, add up the risk levels of each
# position you enter (that is, don't count the risk level of your starting position
# unless you enter it; leaving it adds no risk to your total).


import numpy as np
import heapq  
import time

 
def dijkstra_algorithm(grid):
    rows, cols = grid.shape
    
    # Zielkoordinaten (unten rechts)
    target = (rows - 1, cols - 1)
    
    # Priority Queue speichert Tupel: (Aktuelles_Gesamtrisiko, Zeile, Spalte)
    pq = [(0, 0, 0)]
    
    # Dictionary - Key: (zeile, spalte), Value: geringstes Risiko
    min_costs = {(0, 0): 0}
    
    # Richtungen
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    print("Dijkstra gestartet...")
    
    while pq:
        # (r & c = row & column)
        current_risk, r, c = heapq.heappop(pq)
        
        # Ziel erreicht?: 
        if (r, c) == target:
            return current_risk
        
        if current_risk > min_costs.get((r, c), float('inf')): 
            continue
        
        # Nachbarn untersuchen
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < rows and 0 <= nc < cols:
                new_risk = current_risk + grid[nr][nc]

                if new_risk < min_costs.get((nr, nc), float('inf')):
                    min_costs[(nr, nc)] = new_risk
                    heapq.heappush(pq, (new_risk, nr, nc))

    return -1 # Sollte theoretisch nicht erreicht werden, wenn ein Weg existiert


def einlesen():
    #Einlesen als 2d-Liste
    raw_arr=[]
    ebenen=0
    with open("data/exercise_cave.txt", 'r') as f:
        for line in f:
            raw_arr.append(line)
            ebenen+=1
    
    print("Anzahl Ebenen -", ebenen)
    spalten=len(raw_arr[0]) - 1
    print("Anzahl Spalten -" , spalten)
    np_arr=np.zeros((ebenen, spalten), dtype=int)

    #Allokierung in 2d-Array
    for ebene in range(ebenen):
        for spalte in range(spalten):
            number=raw_arr[ebene]
            np_arr[ebene][spalte] = number[spalte]
    
    # -> Fertiges np-2d-Array 
    return np_arr


if __name__=='__main__':
   
    start_1=time.time()
    np_arr=einlesen()
    end_1=time.time()
    print(f"Benötigte Zeit für Einlesen: {end_1-start_1:.4f}s\n")

    #Algorithmus zur geringsten Risiko-Pfad Bestimmung
    start_2=time.time()
    risk = dijkstra_algorithm(np_arr)
    end_2=time.time()
    print("Minimales Total-Risiko:", risk)
    print(f"Benötigte Zeit: {end_2-start_2:.4f}s")
    