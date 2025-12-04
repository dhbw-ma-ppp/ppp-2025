#Solve the exercise described at https://adventofcode.com/2021/day/15 using the data at `data/exercise_cave.txt` as input. Prepare a PR as usual.

def getdata_and_transform_into_matrix():
    with open('exercise_cave.txt') as f:
        lines = f.read().strip().split('\n')
        if not lines:
            return None
        
        numbers = [[int(digit) for digit in line] for line in lines]
        matrix = np.array(numbers)
        return matrix

#--------------Trying to recreate the A* Algotithm---------------------#

import numpy as np
import heapq

class Node:
    def __init__(self, position, parent = None):
        self.position = position
        self.parent = parent
        self.f = 0
        self.g = 0
        self.h = 0
    
    def __lt__(self, other): #for the priority queue
        return self.f < other.f

def get_distance(node, goal): #get_distance using the manhattan method
    return abs(node.position[0] - goal.position[0]) + abs(node.position[1] - goal.position[1])

def a_star_search(grid, start, goal):

    open_list = [(0, 0, start)]  # (f, g, position)
    min_g = {start: 0} # minimal cost to reach each position

    visited = set() # visited positions

    rows, cols = grid.shape
    goal_pos = goal

    while open_list:
        current_f, current_g, current_pos = heapq.heappop(open_list)
        if current_pos in visited:
            continue
        visited.add(current_pos)

        if current_pos == goal_pos:
            return current_g

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current_pos[0] + dx, current_pos[1] + dy)

            if not (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols):
                continue
            
            #calculate new g cost
            new_g = current_g + grid[neighbor[0]][neighbor[1]]
            
            #only consider this new path if its better
            if new_g < min_g.get(neighbor, 999):
                min_g[neighbor] = new_g
                h = get_distance(Node(neighbor), Node(goal_pos))
                f = new_g + h
                heapq.heappush(open_list, (f, new_g, neighbor))
                
    return None

if __name__ == "__main__":
    grid = getdata_and_transform_into_matrix()
    start = (0, 0)
    goal = (grid.shape[0] - 1, grid.shape[1] - 1)
    
    min_risk = a_star_search(grid, start, goal)
    
    print(f"Yipiiii wir haben es gefunden")
    print(f"Das minimale Risiko ist: {min_risk}")