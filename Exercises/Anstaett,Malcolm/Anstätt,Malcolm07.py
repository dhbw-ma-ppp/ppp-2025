# Solve the exercise described at https://adventofcode.com/2021/day/15 using the data at `data/exercise_cave.txt` as input. Prepare a PR as usual.

import numpy as np
import heapq

# Umwandlung der Eingabedaten in ein Numpy Array
try:
    with open("data/exercise_cave.txt", "r") as file:
        # Alle Zeilen der Datei lesen
        lines = file.readlines()
        # Array erstellen: Jede Zeile wird in eine Liste von Integern umgewandelt
        cave_array = np.array([[int(char) for char in line.strip()] for line in lines])
except FileNotFoundError:
    # Fehlerbehandlung, falls die Datei nicht gefunden wird
    print("Fehler: Die Datei 'exercise_cave.txt' wurde nicht gefunden.")
    exit()

def dijkstra_min_path(cave):
    rows, cols = cave.shape  # Dimensionen des Arrays
    # Priority Queue für Dijkstra: Start bei (0, 0) mit 0 Gefahrpunkten
    submarine = [(0, 0, 0)]
    visited = set()  # Set, um bereits besuchte Knoten zu speichern
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Bewegungsrichtungen: rechts, unten, links, oben

    while submarine:
        # Knoten mit den geringsten Kosten aus der Priority Queue entnehmen
        cost, x, y = heapq.heappop(submarine)
        if (x, y) in visited:  # Überspringen, wenn der Knoten bereits besucht wurde
            continue
        visited.add((x, y))  # Knoten als besucht markieren

        # Ziel erreicht: Rückgabe der minimalen Kosten
        if (x, y) == (rows - 1, cols - 1):
            return cost

        # Nachbarn des aktuellen Knotens besuchen
        for dx, dy in directions:
            nx, ny = x + dx, y + dy  # Koordinaten des Nachbarn berechnen
            # Prüfen, ob der Nachbar innerhalb der Grenzen liegt und noch nicht besucht wurde
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
                # Nachbarn in die Priority Queue einfügen mit aktualisierten Kosten
                heapq.heappush(submarine, (cost + cave[nx, ny], nx, ny))

# Kürzesten Pfad berechnen
min_cost = dijkstra_min_path(cave_array)
print(f"Die minimalen Kosten, um das Ziel zu erreichen, betragen: {min_cost}")  # Erwartete Ausgabe: 508
