import time

import numpy as np
from numpy import ndarray

import matplotlib.pyplot as plt
from matplotlib.backend_bases import KeyEvent
from matplotlib.colors import ListedColormap

from utils.computer import calculate_number_through_memory_list

plt.ion()
fig, ax = plt.subplots()

# ---------- Input Handling ----------
user_inputs: list[int] = []


def on_key(event: KeyEvent):
    event_name = event.key
    if not isinstance(event_name, str): # or is None
        return
    lower_event_name: str = event_name.lower()
    if lower_event_name in ["a", "left"]:
        user_inputs.append(-1)
    elif lower_event_name in ["d", "right"]:
        user_inputs.append(1)
    elif lower_event_name in ["s", "down"]:
        user_inputs.append(0)


def get_user_input(waiting: bool = False, timeout: float = 0.75) -> int:
    start_time = time.time()
    while True:
        if user_inputs:
            return user_inputs.pop(0)
        plt.pause(0.05)
        if time.time() - start_time >= timeout and not waiting:
            return 0


fig.canvas.mpl_connect("key_press_event", on_key)


# ---------- Load external file ----------
numbers: list[int] = []
with open("breakout_commands.txt", "r") as f:
    for line in f:
        line = line.strip()
        if line:
            numbers.append(int(line))


# ---------- Plotting ----------


def draw(grid: ndarray, score):
    ax.clear()
    fig.canvas.manager.set_window_title("Breakout Game")
    ax.set_title(f"Score: {score}", color="#F1E9DA")
    colors: list[str] = ["#2E294E", "#D90368", "#F1E9DA", "#FF69B4", "#FFD400"]
    fig.patch.set_facecolor("#2E294E")
    cmap: ListedColormap = ListedColormap(colors)
    ax.imshow(grid, cmap=cmap, origin="upper")
    ax.axis("off")
    plt.tight_layout(pad=0)
    plt.draw()


def create_grid_update_callback():
    create_grid_base: bool = True
    grid: ndarray
    score: int = 0

    def on_delta_stacked_output(val: list[int]):
        nonlocal create_grid_base, grid, score

        triplets: list[tuple] = [tuple(val[i : i + 3]) for i in range(0, len(val), 3)]
        if create_grid_base:
            max_x: int = max(t[0] for t in triplets)
            max_y: int = max(t[1] for t in triplets)

            grid = np.zeros((max_y + 1, max_x + 1), dtype=int)
            create_grid_base = False

        for x, y, tile in triplets:
            if x == -1 and y == 0:
                score = tile
                continue
            grid[y, x] = tile
        draw(grid, score)

    return on_delta_stacked_output


# ---------- Start ----------
on_output = create_grid_update_callback()
numbers[0] = 2
calculate_number_through_memory_list(
    numbers, [0], input_callback=get_user_input, output_delta_stacked_callback=on_output
)
plt.ioff()
plt.show()
