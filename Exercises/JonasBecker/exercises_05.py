from enum import Enum

import numpy as np
from numpy import ndarray

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from utils.user import get_user_input
from utils.computer import calculate_number_through_memory_list
from utils.mathplotlib.user import UserController

# ---------- Enums ----------


class Direction(Enum):
    LEFT = -1
    STAY = 0
    RIGHT = 1


class PlayMode(Enum):
    BOT = 0
    LIVE = 1
    RELAXED = 2


class Tile(Enum):
    EMPTY = (0, "#2E294E")
    WALL = (1, "#D90368")
    BLOCK = (2, "#F1E9DA")
    PADDLE = (3, "#FF69B4")
    BALL = (4, "#FFD400")

    def __new__(
        cls, value, color
    ):  # note: runs before init, creates object (special in enum)
        obj = object.__new__(cls)
        obj._value_ = value
        obj.color = color
        return obj


# ---------- Global Constants ----------

DIRECTIONS_TO_KEY = {
    Direction.LEFT: ["a", "left"],
    Direction.STAY: ["s", "down"],
    Direction.RIGHT: ["d", "right"],
}

COLORMAP = [tile.color for tile in Tile]


# ---------- Global State ----------
play_mode_number = get_user_input(  # ask for mode as CLI before showing plot
    "Please enter playmode:\n0 -> Bot,\n1 -> Ball is moving by itself,\n2 -> Ball is moving only on Input\nAnswer: ",
    type=int,
    accept=[0, 1, 2],
)
play_mode = PlayMode(play_mode_number)

plt.ion()
fig, ax = plt.subplots()
user_controller = UserController(fig)

create_grid_base: bool = True
grid: ndarray
score: int = 0
ball_x: int = -1
paddle_x: int = -1


# ---------- Functions ----------


def draw():
    ax.clear()
    fig.canvas.manager.set_window_title("Breakout Game")
    ax.set_title(f"Score: {score}", color="#F1E9DA")
    fig.patch.set_facecolor("#2E294E")
    cmap = ListedColormap(COLORMAP)
    ax.imshow(grid, cmap=cmap, origin="upper")
    ax.axis("off")
    plt.tight_layout(pad=0)
    plt.draw()


def get_next_move() -> int:
    timeout: int | None = None

    if play_mode == PlayMode.BOT:
        plt.pause(0.001)
        x_distance_to_ball = ball_x - paddle_x
        if x_distance_to_ball > 0:
            return Direction.RIGHT.value
        if x_distance_to_ball < 0:
            return Direction.LEFT.value
        else:
            return Direction.STAY.value
    elif play_mode == PlayMode.LIVE:
        timeout = 1

    next_input_direction = user_controller.get_next_key_input(
        case_sensitive=False,
        accept=DIRECTIONS_TO_KEY.values(),
        replace_by_key=DIRECTIONS_TO_KEY,
        timeout=timeout,
    )

    return (next_input_direction or Direction.STAY).value


def on_delta_stacked_output(val: list[int]):
    global create_grid_base, grid, score, ball_x, paddle_x

    triplets: list[tuple] = [tuple(val[i : i + 3]) for i in range(0, len(val), 3)]

    if create_grid_base:
        max_x = max(t[0] for t in triplets)
        max_y = max(t[1] for t in triplets)
        grid = np.zeros((max_y + 1, max_x + 1), dtype=int)
        create_grid_base = False

    for x, y, tile_number in triplets:
        if x == -1 and y == 0:
            score = tile_number
            continue

        tile = Tile(tile_number)
        if tile == Tile.PADDLE:
            paddle_x = x
        elif tile == Tile.BALL:
            ball_x = x

        grid[y, x] = tile.value

    draw()


# ---------- Load external file ----------

numbers: list[int] = []

with open("breakout_commands.txt", "r") as f:
    for line in f:
        line = line.strip()
        if line:
            numbers.append(int(line))


# ---------- Start ----------

numbers[0] = 2  # set interactive play mode for Int-Code-Program

calculate_number_through_memory_list(
    numbers,
    input_callback=get_next_move,
    output_delta_stacked_callback=on_delta_stacked_output,
)

plt.ioff()
plt.show()
