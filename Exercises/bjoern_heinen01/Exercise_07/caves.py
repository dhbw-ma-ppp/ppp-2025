from myMath import vector2

def _string_to_cave(text):
    cave = [[int(e) for e in line] for line in text.split("\n")]
    if [] in cave:
        cave.remove([])
    return cave

example_cave = _string_to_cave("""1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""")


def print_cave(cave:list[list[int]] ):
    for line in cave:
        print(*line, sep="")


with open("data/exercise_cave.txt", "r") as file:
    exercise_cave = _string_to_cave(file.read())


correct_path = [vector2(*args) for args in [(0,0),(0,1),(0,2),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(6,3),(7,3),(7,4),(7,5),(8,5),(8,6),(8,7),(8,8),(9,8),(9,9)]]