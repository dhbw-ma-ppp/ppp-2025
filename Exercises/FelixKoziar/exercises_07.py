import numpy as np
from pathlib import Path
import heapq

lines = Path("./data/exercise_cave.txt").read_text().splitlines()
grid = np.array([[int(ch) for ch in line.strip()] for line in lines], dtype=np.int8)

class Node:
    def __init__(self, x: int, y: int):
        self.coordinates = (x, y)
        self.shortest_distance = float('inf')
        self.previous_node: tuple[int, int] | None = None
        self.visited = False

def in_bounds(x: int, y: int, w: int, h: int) -> bool:
    return 0 <= x < w and 0 <= y < h

def neighbours(x: int, y: int, w: int, h: int):
    # gültige Nachbarn
    if in_bounds(x + 1, y, w, h): yield (x + 1, y)
    if in_bounds(x - 1, y, w, h): yield (x - 1, y)
    if in_bounds(x, y + 1, w, h): yield (x, y + 1)
    if in_bounds(x, y - 1, w, h): yield (x, y - 1)

def dijkstra_min_risk(grid: np.ndarray) -> int:
    h, w = grid.shape  # grid[y, x]
    nodes: dict[tuple[int, int], Node] = {(x, y): Node(x, y) for y in range(h) for x in range(w)}

    start = nodes[(0, 0)]
    start.shortest_distance = 0  # Start zählt nicht zur Summe
    target = (w - 1, h - 1)

    # Priority Queue: (dist, x, y)
    heap: list[tuple[int, int, int]] = [(0, 0, 0)]

    while heap:
        d, x, y = heapq.heappop(heap)
        node = nodes[(x, y)]
        if node.visited:
            continue
        node.visited = True

        if (x, y) == target:
            return d

        for nx, ny in neighbours(x, y, w, h):
            if nodes[(nx, ny)].visited:
                continue
            nd = d + int(grid[ny, nx])
            if nd < nodes[(nx, ny)].shortest_distance:
                nodes[(nx, ny)].shortest_distance = nd
                nodes[(nx, ny)].previous_node = (x, y)
                heapq.heappush(heap, (nd, nx, ny))

    return nodes[target].shortest_distance

def main():
    chitons = dijkstra_min_risk(grid)
    print(f"Min Chitons: {chitons}")

main()