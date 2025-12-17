#Solve the exercise described at https://adventofcode.com/2021/day/15 using the data at `data/exercise_cave.txt` as input. Prepare a PR as usual.
import heapq
import numpy as np
import timeit


# Datensatz improtieren
with open('data/exercise_cave.txt', 'r') as ifile:
    cave_data = ifile.readlines()

# strips the newline charakters created by reading the data
cleaned = [line.strip() for line in cave_data]

# seperates the rows 
rows = [list(map(int, line)) for line in cleaned] 

# creates an array with the rows
matrix = np.array(rows)

# print (matrix) # Visualisation if needed for better understanding
# print (matrix.shape)

def dijkstra_matrix(matrix, start, goal):
    """
    matrix: 2D np.array mit Kosten
    start: (row, col) Startkoordinate
    goal: (row, col) Zielkoordinate
    """
    rows, cols = matrix.shape
    distances = np.full((rows, cols), np.inf)
    distances[start] = matrix[start]  # Startkosten

    # Vorgänger für Pfadrekonstruktion
    prev = dict()

    # Min-Heap für Dijkstra
    heap = [(0, start)]

    # Bewegungen: 4 Richtungen
    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    while heap:
        current_dist, (row, col) = heapq.heappop(heap)

        if (row, col) == goal:
            break  # Ziel erreicht

        for (dr, dc) in directions:
            new_row, new_col = row + dr, col + dc

            if (0 <= new_row < rows) and (0 <= new_col < cols):
                new_dist = current_dist + matrix[new_row, new_col]

                if new_dist < distances[new_row, new_col]:
                    distances[new_row, new_col] = new_dist
                    prev[(new_row, new_col)] = (row, col)
                    heapq.heappush(heap, (new_dist, (new_row, new_col)))

    # Pfad rekonstruieren
    path = []
    node = goal
    while node in prev or node == start:
        path.append(node)
        if node == start:
            break
        node = prev[node]
    path.reverse()

    return path, distances[goal]

start = (0,0)
exit = (99, 99)

duration = timeit.timeit( lambda: dijkstra_matrix(matrix, start, exit), number=100)
print(f"The duration ist {duration / 100} s per funktion call\n\n")


def print_path_matrix(matrix, path):
    rows, cols = matrix.shape
    path_set = set(path)
    for i in range(rows):
        row_str = ""
        for j in range(cols):
            if (i,j) == path[0]:
                # Start blau mit Wert
                row_str += f"\033[94m{matrix[i,j]}\033[0m"
            elif (i,j) == path[-1]:
                # Ziel rot mit Wert
                row_str += f"\033[91m{matrix[i,j]}\033[0m"
            elif (i,j) in path_set:
                # Pfad grün mit Wert
                row_str += f"\033[92m{matrix[i,j]}\033[0m"
            else:
                # normale Zelle
                row_str += f"{matrix[i,j]}"
        print(row_str)




path, distance = dijkstra_matrix(matrix, start, exit)
print_path_matrix(matrix, path)



print(f"""\n Das geringste Risikolevel sind {distance}""")