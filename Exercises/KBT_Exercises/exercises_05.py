from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def run_intcode(memory, input_callback=None):
    mem = defaultdict(int)
    for i, val in enumerate(memory):
        mem[i] = val

    ip = 0
    relative_base = 0
    outputs = []

    def get_param(offset, mode):
        val = mem[ip + offset]
        if mode == 0:
            return mem[val]
        elif mode == 1:
            return val
        elif mode == 2:
            return mem[relative_base + val]

    def get_write_address(offset, mode):
        val = mem[ip + offset]
        if mode == 0:
            return val
        elif mode == 2:
            return relative_base + val

    while True:
        instr = str(mem[ip]).zfill(5)
        opcode = int(instr[-2:])
        p1, p2, p3 = int(instr[-3]), int(instr[-4]), int(instr[-5])

        if opcode == 99:
            break

        if opcode == 1:
            mem[get_write_address(3, p3)] = get_param(1, p1) + get_param(2, p2)
            ip += 4
        elif opcode == 2:
            mem[get_write_address(3, p3)] = get_param(1, p1) * get_param(2, p2)
            ip += 4
        elif opcode == 3:
            mem[get_write_address(1, p1)] = input_callback() if input_callback else 0
            ip += 2
        elif opcode == 4:
            outputs.append(get_param(1, p1))
            if len(outputs) == 3:
                yield tuple(outputs)
                outputs = []
            ip += 2
        elif opcode == 5:
            ip = get_param(2, p2) if get_param(1, p1) != 0 else ip + 3
        elif opcode == 6:
            ip = get_param(2, p2) if get_param(1, p1) == 0 else ip + 3
        elif opcode == 7:
            mem[get_write_address(3, p3)] = 1 if get_param(1, p1) < get_param(2, p2) else 0
            ip += 4
        elif opcode == 8:
            mem[get_write_address(3, p3)] = 1 if get_param(1, p1) == get_param(2, p2) else 0
            ip += 4
        elif opcode == 9:
            relative_base += get_param(1, p1)
            ip += 2

# Load the txt file
with open("data/breakout_commands.txt", "r") as f:
    program = list(map(int, f.read().strip().split()))

program_part1 = program.copy()
tiles = {}
for x, y, tile_id in run_intcode(program_part1):
    tiles[(x, y)] = tile_id

max_x = max(x for x, _ in tiles.keys())
max_y = max(y for _, y in tiles.keys())

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(-0.5, max_x + 0.5)
ax.set_ylim(-(max_y + 0.5), 0.5)
ax.set_aspect('equal')
ax.axis('off')
colors = {0: "black", 1: "gray", 2: "blue", 3: "green", 4: "red"}
for (x, y), tile in tiles.items():
    rect = Rectangle((x - 0.5, -y - 0.5), 1, 1, facecolor=colors[tile], edgecolor="black")
    ax.add_patch(rect)
plt.title("Breakout Static Screen")
plt.show()

program_part2 = program.copy()
program_part2[0] = 2
ball_x = paddle_x = 0
score = 0

def joystick():
    if ball_x < paddle_x:
        return -1
    elif ball_x > paddle_x:
        return 1
    return 0

for x, y, val in run_intcode(program_part2, input_callback=joystick):
    if x == -1 and y == 0:
        score = val
    else:
        if val == 3:
            paddle_x = x
        elif val == 4:
            ball_x = x

print(f"Final score after beating the game: {score}")
