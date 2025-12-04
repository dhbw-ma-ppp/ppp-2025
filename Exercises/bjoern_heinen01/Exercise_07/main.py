from caves import print_cave, example_cave, correct_path, exercise_cave
from myMath import vector2
import heapq
import timeit

    
class Node:
    def __init__(self):
        self.parent_x = 0
        self.parent_y = 0

        self.f = float('inf')
        self.g = float('inf')
        self.h = 0

def trace_path(cell_details, dest, ROW, COL):
    path:list[vector2] = []
    row = dest.y
    col = dest.x

    while not cell_details[row][col].parent_y is None and not cell_details[row][col].parent_x is None:
        path.append(vector2(x=col, y=row))
        temp_row = cell_details[row][col].parent_y
        temp_col = cell_details[row][col].parent_x
        row = temp_row
        col = temp_col

    path.append(vector2(x=col, y=row))
    path.reverse()

    return path


def a_star_search(grid, src:vector2, dest:vector2, ROW, COL):
    if not src.y in range(ROW) or not src.x in range(COL): return
    if not dest.y in range(ROW) or not dest.x in range(COL): return
    if src == dest: return

    closed_list:list[list[bool]] = [[False for _ in range(COL)] for _ in range(ROW)]
    cell_details = [[Node() for _ in range(COL)] for _ in range(ROW)]

    y = src.y
    x = src.x

    # Set root element values:
    cell_details[y][x].f = 0
    cell_details[y][x].g = 0
    cell_details[y][x].h = 0
    cell_details[y][x].parent_y = None
    cell_details[y][x].parent_x = None

    open_list = []
    heapq.heappush(open_list, (0.0, y, x))

    while len(open_list):
        _, y, x = heapq.heappop(open_list)
        
        # get current cell:
        c_cell = cell_details[y][x]

        closed_list[y][x] = 1

        direction_off_sets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for direction_off_set in direction_off_sets:
            n_x = x + direction_off_set[0]
            n_y = y + direction_off_set[1]

            if n_y in range(ROW) and n_x in range(COL) and not closed_list[n_y][n_x]:
                # get neighbour cell
                n_cell = cell_details[n_y][n_x]

                if n_y == dest.y and n_x == dest.x:
                    n_cell.parent_x = x
                    n_cell.parent_y = y


                    return trace_path(cell_details, dest, ROW, COL), closed_list
                else:
                    # Calculate the new f, g, and h values
                    g_new = c_cell.g + grid[n_y][n_x]

                    # wenn man nicht den besten pfad sucht, kann man auch anstatt mit 1 
                    # zu multiplizieren mit 3 multiplizieren
                    h_new = (abs(n_x - dest.x) + abs(n_y - dest.y)) * 1 # * 3 for performance!!!
                    f_new = g_new + h_new

                    # are the costs of this way the currently lowest to this node?
                    if f_new < n_cell.f:
                        # update path values in cell
                        n_cell.f = f_new
                        n_cell.g = g_new
                        n_cell.h = h_new

                        n_cell.parent_x = x
                        n_cell.parent_y = y
                        

                        heapq.heappush(open_list, (f_new, n_y, n_x))

    return None, None

def print_path(path: list[vector2], cave: list[list[int]], visited_nodes:list[list[bool]]):
    ROW = len(cave)
    COL = len(cave[0])
    cost = 0
    grid = [[f"\033[90m{item}\033[0m" for item in row] for row in cave]

    for y in range(len(visited_nodes)):
        for x in range(len(visited_nodes[0])):
            if visited_nodes[y][x]:
                grid[y][x] = f"\033[32m{cave[y][x]}\033[0m"

    for coord in path:
        y, x = coord.y, coord.x
        grid[y][x] = f"\033[34m{cave[y][x]}\033[0m"
        cost += cave[y][x]

    cost -= cave[path[0].y][path[0].x]

    path_as_string = "\n\n"
    for line in grid:
        path_as_string += "".join(line) + "\n"

    print(path_as_string, f"Die Kosten des Pfades betragen {cost}.", sep="")

grid = exercise_cave

ROW = len(grid)
COL = len(grid[0])

n = 33
duration = timeit.timeit(lambda: a_star_search(grid, vector2(0, 0), vector2(ROW-1, COL-1), ROW, COL), number=n)

path, visited_nodes = a_star_search(grid, vector2(0,0), vector2(ROW-1,COL-1), ROW, COL)


print_path(path, grid, visited_nodes)
print("=== === ===")

print(f"Pathfinding took {duration/n} seconds.")