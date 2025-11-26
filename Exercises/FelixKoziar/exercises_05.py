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
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle

# ------------------------- Loading breakout commands -------------------------
breakout_commands_list = []

script_dir = Path(__file__).parent
file_path = script_dir / 'breakout_commands.txt'

with open(file_path) as file:
    for line in file:
        stripped_line = line.strip()
        if stripped_line:
            try:
                breakout_commands_list.append(int(stripped_line))
            except ValueError:
                raise Exception("Warning: invalid integer line")
# ------------------------- My Virtual Machine ------------------------
class IntComputer:
    
    def __init__(self, program):
        # Convert list to dictionary for unlimited memory
        self.memory = {i: v for i, v in enumerate(program)}
        self.ip = 0  # instruction pointer
        self.relative_offset = 0  # for relative mode (mode 2)
        self.output_list = []
        self.paddle_x = 0
        self.ball_x =0
        
        # Opcode mapping: opcode -> (function, num_parameters)
        self.opcode_info = {
            1: (self.add, 3),
            2: (self.multiply, 3),
            3: (self.read_input, 1),
            4: (self.write_output, 1),
            5: (self.jump_if_true, 2),
            6: (self.jump_if_false, 2),
            7: (self.less_than, 3),
            8: (self.equals, 3),
            9: (self.adjust_offset, 1)
        }
    
    # ------------------------- OPCODE IMPLEMENTATIONS -------------------------
    
    def add(self, parameters):
        self.memory[parameters[2]] = parameters[0] + parameters[1]
    
    def multiply(self, parameters):
        self.memory[parameters[2]] = parameters[0] * parameters[1]
    
    def read_input(self, parameters):
        if self.paddle_x < self.ball_x:
            input = 1
        elif self.paddle_x > self.ball_x:
            input = -1
        else:
            input = 0
        self.memory[parameters[0]] = input
    
    def write_output(self, parameters):
        self.output_list.append(parameters[0])
        if len(self.output_list) % 3 == 0:
            x = self.output_list[-3]
            y = self.output_list[-2]
            tile = self.output_list[-1]
            if tile == 4:
                self.ball_x = x
            elif tile == 3:
                self.paddle_x = x

    
    def jump_if_true(self, parameters):
        if parameters[0] != 0:
            return parameters[1]  # new instruction pointer
        return None
    
    def jump_if_false(self, parameters):
        if parameters[0] == 0:
            return parameters[1]  # new instruction pointer
        return None
    
    def less_than(self, parameters):
        self.memory[parameters[2]] = 1 if parameters[0] < parameters[1] else 0
    
    def equals(self, parameters):
        self.memory[parameters[2]] = 1 if parameters[0] == parameters[1] else 0
    
    def adjust_offset(self, parameters):
        self.relative_offset += parameters[0]
    
    # ------------------------- HELPER METHODS -------------------------
    
    def get_opcode(self, instruction):
        return instruction % 100
    
    def get_modes(self, instruction):
        modes = []
        instruction //= 100  # remove opcode part
        while instruction > 0:
            modes.append(instruction % 10)
            instruction //= 10
        return modes
    
    def get_parameters(self, num_parameters, modes, opcode):
        parameters = []
        write_opcodes = {1, 2, 3, 7, 8}  # opcodes with write parameters (NOT 9!)
        
        for i in range(num_parameters):
            parameter_address = self.ip + i + 1
            mode = modes[i] if i < len(modes) else 0  # default to position mode
            
            # The last parameter for write_opcodes is a write address
            is_write_parameter = (opcode in write_opcodes) and (i == num_parameters - 1)
            
            if is_write_parameter:
                # Write parameter: return the address (adjusted for mode)
                if mode == 0:  # position mode
                    parameters.append(self.memory.get(parameter_address, 0))
                elif mode == 2:  # relative mode
                    parameters.append(self.memory.get(parameter_address, 0) + self.relative_offset)
            else:
                # Read parameter: return the value
                if mode == 0:  # position mode
                    address = self.memory.get(parameter_address, 0)
                    parameters.append(self.memory.get(address, 0))
                elif mode == 1:  # immediate mode
                    parameters.append(self.memory.get(parameter_address, 0))
                elif mode == 2:  # relative mode
                    address = self.memory.get(parameter_address, 0) + self.relative_offset
                    parameters.append(self.memory.get(address, 0))
        
        return parameters

    # ------------------------- MAIN EXECUTION -------------------------
    
    def run(self):
        while True:
            opcode = self.get_opcode(self.memory.get(self.ip, 0))
            
            if opcode == 99:  # halt
                break
            
            if opcode not in self.opcode_info:
                raise ValueError("Unknown opcode {} at position {}".format(opcode, self.ip))
            
            # Get instruction details
            modes = self.get_modes(self.memory.get(self.ip, 0))
            function, num_parameters = self.opcode_info[opcode]
            
            # Resolve parameters
            resolved_parameters = self.get_parameters(num_parameters, modes, opcode)
            
            # Execute instruction
            result = function(resolved_parameters)
            
            # Update instruction pointer
            if result is not None:  # jump instructions return new IP
                self.ip = result
            else:
                self.ip += num_parameters + 1

# ========================= RUNNING THE PROGRAM =========================

# Activate play-mode and run the game
breakout_commands_list[0] = 2  # Comment this for Part 1 (static image)
computer = IntComputer(breakout_commands_list)
computer.run()

print("Game finished! Score: {}".format(max(computer.output_list[2::3])))


# ========================= EXTRACT FRAMES =========================

# Process outputs: Build screen state and save frames when ball moves
frames = []
screen = {}
last_ball_pos = None
game_started = False

for i in range(0, len(computer.output_list), 3):
    x, y, tile = computer.output_list[i], computer.output_list[i+1], computer.output_list[i+2]
    
    # Check if game started (score becomes > 0)
    if x == -1 and y == 0 and tile > 0:
        game_started = True
    
    # Update screen
    if x >= 0:
        screen[(x, y)] = tile
    
    # Save frame when ball moves (after game started)
    if game_started and tile == 4 and (x, y) != last_ball_pos:
        last_ball_pos = (x, y)
        
        # Build frame from current screen state
        frame = np.zeros((23, 43), dtype=int)
        for (px, py), tile_type in screen.items():
            frame[py, px] = tile_type
        frames.append(frame)

# If no frames were created (Part 1: static image), create one from final screen
if len(frames) == 0:
    frame = np.zeros((23, 43), dtype=int)
    for (px, py), tile_type in screen.items():
        frame[py, px] = tile_type
    frames.append(frame)
    print("Created static image (Part 1)")
else:
    print("Extracted {} frames (Part 2)".format(len(frames)))

# ========================= VISUALIZE ANIMATION =========================

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle

# Define colors for each tile type
def get_tile_color(tile_type, y_position):
    if tile_type == 0:
        return 'black'  # Empty
    elif tile_type == 1:
        return 'white'  # Wall
    elif tile_type == 2:
        # Blocks: Rainbow gradient based on Y position
        if y_position <= 3: return 'red'
        elif y_position <= 5: return 'darkorange'
        elif y_position <= 7: return 'gold'
        elif y_position <= 9: return 'limegreen'
        elif y_position <= 11: return 'cyan'
        elif y_position <= 13: return 'blue'
        else: return 'mediumpurple'
    elif tile_type == 3:
        return 'grey'  # Paddle
    elif tile_type == 4:
        return 'white'  # Ball
    return 'black'

# Setup matplotlib figure
fig, ax = plt.subplots(figsize=(14, 8))
ax.set_facecolor('black')
fig.patch.set_facecolor('black')
ax.set_xlim(-0.5, 43.5)
ax.set_ylim(-0.5, 23.5)
ax.invert_yaxis()
ax.set_aspect('equal')

# Create all rectangles (one per grid position)
rectangles = {}
for y in range(23):
    for x in range(43):
        rect = Rectangle((x, y), 1, 1, facecolor='black', edgecolor='black', linewidth=0.5)
        ax.add_patch(rect)
        rectangles[(x, y)] = rect

# Animation update function: called for each frame
def update(frame_num):
    frame = frames[frame_num]
    
    # Update each rectangle's color
    for y in range(23):
        for x in range(43):
            tile = frame[y, x]
            rectangles[(x, y)].set_facecolor(get_tile_color(tile, y))
    
    return list(rectangles.values())

# Create animation (if only 1 frame = static image, if many = animation)
if len(frames) == 1:
    # Static image - just show it
    update(0)
    plt.title('Breakout - Start Screen (Part 1)', fontsize=16, color='white', weight='bold')
else:
    # Animation - play every 2nd frame for speed
    frame_indices = range(0, len(frames), 2)
    ani = FuncAnimation(fig, update, frames=frame_indices, interval=1, blit=True, repeat=False)
    plt.title('Breakout Game (Part 2)', fontsize=16, color='white', weight='bold')

# Show
plt.show()


