'''
Ich habe mich dafür entschieden, den Dijkstra-Algorithmus zu benutzen.
Ob es genau der Dijkstra-Algorithmus wurde, weiß ich nicht genau.
Wer sich das Verfahren nochmal durchlesen will, kann das in Algorithmen-05-Graphen
machen oder sich schnell auf Wikipedia einlesen.
'''



import numpy as np
import heapq

with open("exercise_cave.txt", "r") as cave:
    commands = cave.read()
    

rows = commands.split("\n")
len_rows = len(rows[1])
print(len_rows)


commands = list(commands.replace("\n", ""))
ways = []
for i in range(len(commands)):
    ways.append(int(commands[i]))

ways = np.array(ways)
matrix = ways.reshape(100, 100)



def finding_shortest_way(matrix):
    rows, cols = matrix.shape
    dist = np.full((rows, cols), np.inf)
    dist[0][0] = matrix[0][0]

    parent = [[None] * cols for _ in range(rows)]

    heap = [(matrix[0, 0], 0, 0)]

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while heap:
        cost, r, c = heapq.heappop(heap)

        
        
        if cost > dist[r, c]:
            continue

        if (r, c) == (rows - 1, cols - 1):
            path = []
            cur = (r, c)
            while cur is not None:
                path.append(cur)
                cur = parent[cur[0]][cur[1]]
            path.reverse()
            return cost, path



        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < rows and 0 <= nc < cols:
                new_cost = cost + matrix[nr][nc]
                if new_cost < dist[nr, nc]:
                    dist[nr, nc] = new_cost
                    parent[nr][nc] = (r, c)
                    heapq.heappush(heap, (new_cost, nr, nc))
    
    return dist[rows - 1, cols - 1], None

min_cost, path = finding_shortest_way(matrix)
print(min_cost)