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
#commands
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

from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from int_computer import IntComputer
import numpy as np




class game:
    def __init__(self):
        self.manual_input = False # Choose whether you want to play yourself or let it play itself
        self.pixels = np.zeros((23,43), dtype=int)
        self.score = 0
        self.temp_collection_of_outputs = []
        self.outputs_given_this_frame = 0
        self.is_first_build_finished = False
        self.x_coordinate_of_ball = 0

        self.cmap = ListedColormap([
            "black", # Background
            "white", # Border
            "blue", #stones
            "red", #Ball
            "white" #Player
        ]) 
        self.fig, self.ax = plt.subplots()
        self.im = self.ax.imshow(self.pixels, cmap=self.cmap, vmin=0, vmax=4)
        plt.ion()
        plt.show()

    def input_func(self):
        #print(self.score)
        self.update_screen()
        if self.manual_input == True:
            given_input = input("plase input \n 1: For moving right \n 0 for staying still \n -1 for moving left: \n ")
            if given_input == "1" or given_input == "-1" or given_input == "0":
                return int(given_input)
            else: 
                continue_playing = input("Thats not an option, sorry :( Try again (1) or give up (2)")
                if continue_playing == "1":
                    return self.input_func()
                else:
                    quit()
        else: # automatically set x coordinate of ball to that of player
            if self.x_coordinate_of_ball < self.x_coordinate_of_player:
                return 1
            elif self.x_coordinate_of_ball > self.x_coordinate_of_player:
                return -1
            elif self.x_coordinate_of_ball == self.x_coordinate_of_player:
                return 0
            
    def collect_output(self, output):
        self.temp_collection_of_outputs.append(output)
        #collect 3 outputs
        if len(self.temp_collection_of_outputs) == 3: 
            # catch the score
            if self.temp_collection_of_outputs[0] == -1:
                self.score = self.temp_collection_of_outputs[2]
            # fill matrix to display
            else:
                self.pixels[self.temp_collection_of_outputs[1] , self.temp_collection_of_outputs[0] ] = self.temp_collection_of_outputs[2]
                # additional auto-play logic
                if self.temp_collection_of_outputs[2] == 3:
                    self.x_coordinate_of_ball = self.temp_collection_of_outputs[0]
                elif self.temp_collection_of_outputs[2] == 4:
                    self.x_coordinate_of_player = self.temp_collection_of_outputs[0]
            # clear temporary list
            self.temp_collection_of_outputs = []

    def update_screen(self):
            self.im.set_data(self.pixels)
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            
            
                

if __name__ == "__main__":
    with open('breakout_commands.txt', 'r') as ifile:
        content = ifile.readlines()

    commands = []
    for element in content:
        element = element.replace("\n", "")
        commands.append(int(element))

    curr_game = game()

    ic = IntComputer(curr_game.input_func, curr_game.collect_output)

    ic.run(commands)



# Final Score
# 17086