import heapq
import numpy as np


def lowest_risk(grid):
    h, w = grid.shape
    dist = np.full(
        (h, w), np.inf, dtype=np.float64
    )  # Auffüllen mit Infinity, wir wissen ja noch noch keine Wege-Ergebnisse, oder gar beste Wege
    dist[0, 0] = 0  # Starfeld neutralisieren

    pq = [(0, 0, 0)]  # Starten mit x=0, y=0

    while pq:
        cost, y, x = heapq.heappop(pq)  # besten (sicheren) Knoten bekommen

        if (y, x) == (h - 1, w - 1):
            return cost  # Sicher die besten Kosten nach Dijkstra-Algo, alle anderen besten wurden schon abgearbeitet

        for dy, dx in [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        ]:  # Nachbar-Knoten prüfen (nicht diagonal)
            ny, nx = y + dy, x + dx  # Neue Koordinate berechnen für neuen Knoten
            if 0 <= ny < h and 0 <= nx < w:  # Grenzen prüfen
                new_cost = cost + grid[ny, nx]  # Neu Kosten berechnen
                if (
                    new_cost < dist[ny, nx]
                ):  # Falls bessere Kosten als zuvor gefunden, updaten und in den Heap
                    dist[ny, nx] = new_cost
                    heapq.heappush(pq, (new_cost, ny, nx))

    raise RuntimeError(
        "Kein Pfad zum Ziel gefunden!"
    )  # Sollte eigentlich nicht auftreten bei korrektem Array


# Daten einlesen
with open("./exercise_cave.txt") as f:
    lines = f.read().strip().splitlines()

# Daten in ein Grid überführen
grid = np.array([[int(c) for c in line] for line in lines], dtype=np.int32)

result = lowest_risk(grid)
print(result)
