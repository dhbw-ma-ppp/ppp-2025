# to solve todays exercise you will need a fully functional int-computer
# a fully functional int-computer has some additional features compared to the 
# last one you implemented.
# you can either use my implementation of an int-computer (see AtrejuTauschinsky/reference_int_computer.py)
# or you can extend your own int-computer with the necessary features. If you want to extend your own
# the features you need to implement will be described at the bottom.
#
#
# We will run 'breakout' -- the arcade game -- on our simulated computer. 
#(https://en.wikipedia.org/wiki/Breakout_(video_game)) 
# The code for the computer will be provided under data/breakout_commands.txt
# the code will produce outputs in triplets. every triplet that is output
# specifies (x-position, y-position, tile_type).
# tiles can be of the following types:
# 0: empty tile
# 1: wall. walls are indestructible
# 2: block. blocks can be destroyed by the ball
# 3: paddle. the paddle is indestructible
# 4: ball. the ball moves diagonally and bounces off objects
# 
# EXAMPLE:
# a sequence of output values like 1, 2, 3, 6, 5, 4 would
#  - draw a paddle (type 3) at x=1, y=2
#  - draw the ball (type 4) at x=6, y=5
#
#
# PART 1:
# run the game until it exits. Analyse the output produced during the run, and create
# a visual representation of the screen display using one of the plotting libraries we discussed today.
# mark the different tile types as different colors or symbols. Upload the picture with your PR.
#
# PART 2:
# The game didn't actually run in part 1, it just drew a single static screen.
# Change the first instruction of the commands from 1 to 2. Now the game will actually run.
# when the game actually runs you need to provide inputs to steer the paddle. whenever the computer
# requests you to provide an input, you can chose to provide
# -  0: the paddle remains in position
# - -1: move the paddle to the left
# - +1: move the paddle to the right
#
# the game also outputs a score. when an output triplet is in position (-1, 0) the third value of
# the triplet is not a tile type, but your current score.
# You need to beat the game by breaking all tiles without ever letting the ball cross the bottom 
# edge of the screen. What is your high-score at the end of the game? provide the score as part of your PR.
#
# BONUS: (no extra points, just for fun)
# make a movie of playing the game :)
#
#
# COMPLETE INT COMPUTER
# This is only relevant if you decide to extend your own implementation with the necessary features.
# If you decide to use my implementation you can ignore this part.
#
#
# - The computer needs to implement memory much /larger/ than the set of initial commands.
#   Any memory address not part of the initial commands can be assumed to be initialized to 0.
#   (only positive addresses are valid).
# - You need to support a new parameter mode, 'relative mode', denoted as mode 2 in the 'mode' part
#   of the instructions.
#   Relative mode is similar to position mode (the first access mode you implemented). However, 
#   parameters in relative mode count not from 0, but from a value called 'relative offset'. 
#   When the computer is initialized, the relative offset is initialized to 0, and as long as it remains
#   0 relative mode and position mode are identical.
#   In general though parameters in relative mode address the memory location at 'relative offset + parameter value'.
#   EXAMPLE: if the relative offset is 50, the mode is 2, and the value you read from memory is 7 you should 
#     retrieve data from the memory address 57.
#     Equally, if you read -7, you should retrieve data from the memory address 43.
#   This applies to both read- and write operations.
# - You need to implement a new opcode, opcode 9. opcode 9 adjusts the relative offset by the value of its only parameter.
#   the offset increases by the value of the parameter (or decreases if that value is negative).
import operator
import matplotlib.pyplot as plt
import numpy as np

# Lade Breakout-Kommandos
bc = []
try:
    with open("breakout_commands.txt") as file:
        for line in file:
            bc.append(int(line.strip()))
except FileNotFoundError:
    print("Error: The file breakout_commands.txt not found.")

# Vorlage kopiert
class IntComputer:
    def __init__(self, input_getter, output_collector):
        self.memory = {}
        self.ip = 0 
        self.relative_mode_offset = 0
        self.input_getter = input_getter
        self.output_collector = output_collector

        self.function_map = {
            1: self._make_register_setter(operator.add),
            2: self._make_register_setter(operator.mul),
            3: self.get_input,
            4: self.write_output,
            5: self._make_ip_setter(operator.ne),
            6: self._make_ip_setter(operator.eq),
            7: self._make_register_setter(operator.lt),
            8: self._make_register_setter(operator.eq),
            9: self.set_offset,
        }

    def get_input(self, modes):
        target_mode = modes % 10
        if target_mode == 2:
            target = self.memory.get(self.ip, 0) + self.relative_mode_offset
        else:
            target = self.memory.get(self.ip, 0)

        val = self.input_getter()
        self.memory[target] = val
        self.ip += 1

    def write_output(self, modes):
        x, = self.get_function_arguments(modes, 1)
        self.output_collector(x)

    def set_offset(self, modes):
        x, = self.get_function_arguments(modes, 1)
        self.relative_mode_offset += x

    def _make_register_setter(self, func):
        def f(modes):
            x, y = self.get_function_arguments(modes, 2)
            target_mode = (modes // (10**2)) % 10
            if target_mode == 2:
                target = self.memory.get(self.ip, 0) + self.relative_mode_offset
            else:
                target = self.memory.get(self.ip, 0)
            self.memory[target] = int(func(x, y))
            self.ip += 1
        return f

    def _make_ip_setter(self, func, comparison_value=0):
        def f(modes):
            x, y = self.get_function_arguments(modes, 2)
            if func(x, comparison_value):
                self.ip = y
        return f

    def _resolve_argument_value(self, arg_mode, arg_value):
        if arg_mode == 0:
            return self.memory.get(arg_value, 0)
        if arg_mode == 1:
            return arg_value
        if arg_mode == 2:
            return self.memory.get(arg_value + self.relative_mode_offset, 0)

    def get_function_arguments(self, modes, n_args):
        arg_values = [self.memory.get(self.ip + x, 0) for x in range(n_args)]
        arg_modes = [(modes // (10**i)) % 10 for i in range(n_args)]
        arguments = [self._resolve_argument_value(mode, value) for mode, value in zip(arg_modes, arg_values)]
        self.ip += n_args
        return arguments

    def split_command_and_modes(self):
        command = self.memory.get(self.ip, 0)
        self.ip += 1
        return command % 100, command // 100

    def run(self, data):
        self.memory = {i: v for i, v in enumerate(data)}
        self.ip = 0
        self.relative_mode_offset = 0

        while True:
            opcode, modes = self.split_command_and_modes()
            if opcode == 99:
                break
            if opcode in self.function_map:
                self.function_map[opcode](modes)
            else:
                print(f"Unbekannter Opcode: {opcode}")
                break
# Part 1 startisches Bild 
output_data = []

def collect_output(x):
    output_data.append(x)

ic = IntComputer(lambda: 0, collect_output)
ic.run(bc)

# Bildschirm rekonstruieren
xs = output_data[0::3]
ys = output_data[1::3]
tiles = output_data[2::3]

width = max(xs) + 1
height = max(ys) + 1

screen = np.zeros((height, width), dtype=int)
for x, y, t in zip(xs, ys, tiles):
    screen[y, x] = t

# Farblegende
colors = {
    0: "black",
    1: "gray",
    2: "blue",
    3: "green",
    4: "red"
}

# Zeichnen
plt.figure(figsize=(10, 6))
for y in range(height):
    for x in range(width):
        plt.scatter(x, height-y, color=colors[screen[y, x]], s=50)

plt.axis("off")
plt.show()


# Part 2 Spielbares Breckout 
bc2 = bc.copy()
bc2[0] = 2   # Spiel aktivieren

paddle_x = 0
ball_x = 0
score = 0

buffer = []

def game_input():
    if ball_x > paddle_x:
        return 1
    if ball_x < paddle_x:
        return -1
    return 0

def game_output(v):
    global paddle_x, ball_x, score

    buffer.append(v)
    if len(buffer) == 3:
        x, y, tile = buffer

        if x == -1 and y == 0:
            score = tile
        else:
            if tile == 3:
                paddle_x = x
            elif tile == 4:
                ball_x = x

        buffer.clear()

ic2 = IntComputer(game_input, game_output)
ic2.run(bc2)

print("FINAL SCORE:", score)

# LEIDER HABE ICH PROBLEME MIT MEIN CONDA AUF MEIN ARBEITES LAPTOP 
# DESWEGEN KANN ICH MEIN BILD NICHT HOCHLADEN ICH HABE ABER AUF MEIN PRIVAT LAPTO VERSUCHT UND DA GING ES :l

     
    


