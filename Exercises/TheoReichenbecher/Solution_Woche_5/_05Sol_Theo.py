# to solve todays exercise you will need a fully functional int-computer
# a fully functional int-computer has some additional features compared to the 
# last one you implemented.
# you can either use my implementation of an int-computer (see AtrejuTauschinsky/reference_int_computer.py)
# or you can extend your own int-computer with the necessary features. If you want to extend your own
# the features you need to implement will be described at the bottom.
#
#
# We will run 'breakout' -- the arcade game -- on our simulated computer. 
# (https://en.wikipedia.org/wiki/Breakout_(video_game))
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
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap

class IntComputer:
    def __init__(self, input_getter, output_collector):
        def get_input(modes):
            create_screen()
            target_mode = modes % 10
            if target_mode == 2:
                target = self.memory.get(self.ip, 0) + self.relative_mode_offset
            else:
                target = self.memory.get(self.ip, 0)
            self.memory[target] = input_getter()
            self.ip += 1

        def write_output(modes):
            x, = self.get_function_arguments(modes, 1)
            output_collector(x)

        def set_offset(modes):
            x,  = self.get_function_arguments(modes, 1)
            self.relative_mode_offset += x

        self.function_map = {
            1: self._make_register_setter(operator.add),
            2: self._make_register_setter(operator.mul),
            3: get_input,
            4: write_output,
            5: self._make_ip_setter(operator.ne),
            6: self._make_ip_setter(operator.eq),
            7: self._make_register_setter(operator.lt),
            8: self._make_register_setter(operator.eq),
            9: set_offset,
        }

    def _make_register_setter(self, func):
        # make generic function that sets a register
        def f(modes):
            x, y = self.get_function_arguments(modes, 2)
            target_mode = (modes // (10**2)) % 10
            if target_mode == 2:
                target = self.memory.get(self.ip, 0) + self.relative_mode_offset
            else:
                target = self.memory.get(self.ip, 0)
            self.memory[target] = int(func(int(x), int(y)))
            self.ip += 1
        return f

    def _make_ip_setter(self, func, comparison_value=0):
        # make a generic function that sets the instruction pointer
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
        arg_values = [self.memory[self.ip + x] for x in range(n_args)]
        arg_modes = [(modes // (10**i)) % 10 for i in range(n_args)]
        arguments = [self._resolve_argument_value(mode, value) for mode, value in zip(arg_modes, arg_values)]
        self.ip += n_args
        return arguments

    def split_command_and_modes(self):
        command = self.memory[self.ip]
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
            # calculate function arguments
            opcode_function = self.function_map[opcode]
            opcode_function(modes)



import sys
screen = None
img = None
fig = None
ax = None
# Für die Maße des Fensters
width = 0
height = 0
# Erste initialisierung des Fensters 
initialized = False
# Last Index gibt den Index des letzten geänderten Elements 
last_index = 0
# Für das automatische Spiel 
ball_x = None
paddle_x = None


if __name__ == '__main__':
    # Filepath --> einfügen der Intopcodes
    root = sys.path[0]
    path = root + "/int_opcodes.txt"

    with open(path, 'r') as ifile:
        content = ifile.readlines()
    
    # 
    input_codes = []
    for element in content:
        input_codes.append(int(element.replace("\n", "")))



    plot_list = []



    def listen_macher(x):
        """
        Nimmt den Output der Maschine und fügt ihn in die Plotliste ein
        """
        plot_list.append(x)
    
    
    def create_screen():
        """
        Liest neue Triplets aus plot_list, aktualisiert das screen-Array
        und das Plot-Fenster.
        """

        global plot_list, last_index, screen, img, fig, ax, initialized, height, width

        # -------- NUR NEUE WERTE HOLEN --------
        new_values = plot_list[last_index:]
        if len(new_values) < 3:
            return
        last_index = len(plot_list)

        # -------- TRIPLETS BAUEN --------
        triples = list(zip(*(iter(new_values),) * 3))

        tiles = {}
        score = None

        for (x, y, v) in triples:
            if x == -1 and y == 0:
                score = v
            else:
                tiles[(x, y)] = int(v)

        # -------- INITIALISIERUNG --------
        if not initialized:
            xs = [x for (x, y) in tiles.keys()]
            ys = [y for (x, y) in tiles.keys()]

            width = max(xs) + 1
            heigth = max(ys) + 1

            screen = np.zeros((heigth, width), dtype=int)
            screen = screen.astype(int)
            cmap = ListedColormap([
                "black",    # 0 EMPTY
                "purple",   # 1 WALL
                "orange",   # 2 BLOCK
                "cyan",     # 3 PADDLE
                "grey"      # 4 BALL
            ])

            plt.ion()
            fig, ax = plt.subplots(figsize=(12, 6))
            img = ax.imshow(screen, cmap=cmap, vmin= 0, vmax=4)
            plt.show(block=False)
            initialized = True

        # -------- UPDATE DES BILDES --------
        for (x, y), v in tiles.items():
            x = int(x)
            y = int(y)
            v = int(v)

            if 0 <= x < width and 0 <= y < heigth:
                screen[y, x] = v

        img.set_data(screen)
        plt.pause(0.0001)

        # -------- UPDATE DES SCORES, WENN ÄNDERUNG VORLIEGT --------
        if score is not None:
            print("Score:", score)

        # -------- PADDEL UND BALL POSITIONEN --------
        global ball_x, paddle_x

        positions = {v: [] for v in range(5)} 

        for (x, y), v in tiles.items():
            positions[v].append((x, y))

        # Koordinaten werden aus dem Dictionary gelöscht
        if positions[4]:
            ball_x = positions[4][0][0]  # x-Koordinate des Balls
        if positions[3]:
            paddle_x = positions[3][0][0]  # x-Koordinate des Paddles



    def automated_input():
        """
        Vergleicht die x Koordinaten des Panels und des Balls und gibt anhand des Vergleiches die Inputs vom Wert 0, 1, -1 ein 
        """
        global ball_x, paddle_x

        # Wenn keine Positionen bekannt sind, gib keine Bewegung
        if ball_x is None or paddle_x is None:
            return 0

        if ball_x < paddle_x:
            return -1
        elif ball_x > paddle_x:
            return 1
        else:
            return 0 


    print("GAME START")
    ic = IntComputer(automated_input, listen_macher)
    ic.run(input_codes)
    plt.show


# HIGHSCORE == 17.159