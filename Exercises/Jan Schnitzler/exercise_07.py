import numpy as np  # für Array-Operationen und np.inf


def find_lowest_risk_path(risk_grid):
    rows, cols = len(risk_grid), len(risk_grid[0])  # Anzahl Zeilen und Spalten im Grid

    # Konvertiere Eingabe (Liste von Strings) in ein 2D-Array aus ints
    risk_array = np.array([[int(cell) for cell in row] for row in risk_grid])
    # Matrix mit kumulativem Risiko, initial mit unendlich füllen
    total_risk = np.full((rows, cols), np.inf)
    total_risk[0, 0] = 0  # Startpunkt hat kein anfängliches Risiko (wir zählen nur betretene Zellen)
    visited = np.zeros((rows, cols), dtype=bool)  # Marke für besuchte Knoten
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # vier Nachbarn: rechts, unten, links, oben

    # Einfachste Form von Dijkstra: wiederholt den unbesuchten Knoten mit kleinstem Risiko wählen
    while True:
        min_risk = np.inf
        min_coords = (-1, -1)
        # Finde unbesuchten Knoten mit kleinstem aktuellen Risiko
        for row in range(rows):
            for col in range(cols):
                if not visited[row, col] and total_risk[row, col] < min_risk:
                    min_risk = total_risk[row, col]
                    min_coords = (row, col)
        if min_coords == (-1, -1):  # Kein erreichbarer unbesuchter Knoten mehr
            break

        row, col = min_coords
        visited[row, col] = True  # markiere den Knoten als besucht

        # Betrachte alle gültigen Nachbarn und aktualisiere deren kumulatives Risiko
        for d_row, d_col in directions: 
            n_row, n_col = row + d_row, col + d_col # Koordinaten des Nachbarn
            if 0 <= n_row < rows and 0 <= n_col < cols and not visited[n_row, n_col]:
                new_risk = total_risk[row, col] + risk_array[n_row, n_col]  # Risiko bei Betreten des Nachbarn addieren
                if new_risk < total_risk[n_row, n_col]:  # besserer Pfad gefunden?
                    total_risk[n_row, n_col] = new_risk  # aktualisiere geringstes bekanntes Risiko

    # Rückgabe des minimalen kumulativen Risikos zum Ziel (unten rechts) als int
    return int(total_risk[rows - 1, cols - 1])


test_case = [
    "1163751742",
    "1381373672",
    "2136511328",
    "3694931569",
    "7463417111",
    "1319128137",
    "1359912421",
    "3125421639",
    "1293138521",
    "2311944581",
]

if __name__ == "__main__":

    print(find_lowest_risk_path(open("./data/exercise_cave.txt").read().splitlines()))