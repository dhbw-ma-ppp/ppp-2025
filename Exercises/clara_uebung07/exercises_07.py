#-solve the exercise described at https://adventofcode.com/2021/day/15 using the data at `data/exercise_cave.txt` as input. Prepare a PR as usual.

import numpy as np
import heapq

def finding_lowest_risk(grid):
    rows = len(grid)
    columns = len(grid[0])

    array = np.array([[int(cell) for cell in row] for row in grid])
    risk = np.full((rows, columns), np.inf)
    risk[0, 0] = 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    already_visited = np.zeros((rows, columns), dtype = bool)

    priority_queue = [(0, 0, 0)]

    while (len(priority_queue)) > 0:
        current, row, column = heapq.heappop(priority_queue)

        if already_visited[row, column]:
            continue

        already_visited[row, column] = True

        if row == rows - 1 and column == columns - 1:
            return current
        
        for direction_row, direction_column in directions:
            new_row, new_column = row + direction_row, column + direction_column

            if 0 <= new_row < rows and 0 <= new_column < columns and not already_visited[new_row, new_column]:
                new_risk = current + array[new_row, new_column]

                if new_risk < risk[new_row, new_column]:
                    risk[new_row, new_column] = new_risk
                    heapq.heappush(priority_queue, (new_risk, new_row, new_column))
    return int(risk[rows - 1, columns - 1])

lowest_risk = finding_lowest_risk(open("cave.txt").read().splitlines())

print("The lowest risk is:", lowest_risk)