import heapq

with open("data/exercise_cave.txt") as f:
    cave_map = []
    for line in f:
        line = line.strip()
        if line:
            row = []
            for ch in line:
                row.append(int(ch))
            cave_map.append(row)

rows = len(cave_map)
cols = len(cave_map[0])

min_risk = [] # Wir merken uns für jedes Feld, wie gering das Risiko ist, dorthin zu gelangen.
for r in range(rows):
    min_risk.append([float('inf')] * cols)
min_risk[0][0] = 0

heap = []
heapq.heappush(heap, (0, 0, 0))

while heap:
    current_risk, r, c = heapq.heappop(heap)

    if r == rows - 1 and c == cols - 1:
        print("Lowest total risk:", current_risk)
        break

    neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
    for nr, nc in neighbors:
        if 0 <= nr < rows and 0 <= nc < cols:
            risk_through_neighbor = current_risk + cave_map[nr][nc]
            if risk_through_neighbor < min_risk[nr][nc]:
                min_risk[nr][nc] = risk_through_neighbor
                heapq.heappush(heap, (risk_through_neighbor, nr, nc))
