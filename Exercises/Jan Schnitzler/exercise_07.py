import numpy as np
import heapq

def find_lowest_risk_path(risk_grid):
    rows, cols = len(risk_grid), len(risk_grid[0])
    
    risk_array = np.array([[int(cell) for cell in row] for row in risk_grid])
    total_risk = np.full((rows, cols), np.inf)
    total_risk[0, 0] = 0
    visited = np.zeros((rows, cols), dtype=bool)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    priority_queue = [(0, 0, 0)]  # (Risiko, Zeile, Spalte)

    while (len(priority_queue) > 0):
        current_risk, row, col = heapq.heappop(priority_queue)
        
        if (visited[row, col] == True):
            continue
            
        visited[row, col] = True

        if (row == rows - 1 and col == cols - 1):
            return current_risk

        for d_row, d_col in directions:
            n_row, n_col = row + d_row, col + d_col
            
            if (0 <= n_row < rows and 0 <= n_col < cols and not visited[n_row, n_col]):
                new_risk = current_risk + risk_array[n_row, n_col]
                if (new_risk < total_risk[n_row, n_col]):
                    total_risk[n_row, n_col] = new_risk
                    heapq.heappush(priority_queue, (new_risk, n_row, n_col))

    return int(total_risk[rows - 1, cols - 1])

if __name__ == "__main__":
    print(find_lowest_risk_path(open("./data/exercise_cave.txt").read().splitlines()))
