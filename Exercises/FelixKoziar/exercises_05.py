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

def add(memory, parameters):
    memory[parameters[2]] = parameters[0] + parameters[1]

def multiply(memory, parameters):
    memory[parameters[2]] = parameters[0] * parameters[1]

def read_input(memory, parameters):
#----------only for stopping the time----------
    global input_time
    # pausing the timer for input
    start_input = time.perf_counter()
    user_input = int(input('Enter your Input: '))
    # adding the input time to the global variable
    input_time += time.perf_counter() - start_input
#----------------------------------------------
    
    memory[parameters[0]] = user_input

def write_output(_, parameters):
    print(parameters[0])

def jump_if_true(_, parameters):
    if parameters[0] != 0:
        new_ip = parameters[1]
        return new_ip
    else:
        return None

def jump_if_false(_, parameters):
    if parameters[0] == 0:
        new_ip = parameters[1]
        return new_ip
    else:
        return None

def less_than(memory, parameters):
    if parameters[0] < parameters[1]:
        memory[parameters[2]] = 1
    else:
        memory[parameters[2]] = 0

def equals(memory, parameters):
    if parameters[0] == parameters[1]:
        memory[parameters[2]] = 1
    else:
        memory[parameters[2]] = 0

def get_opcode(instruction):
    return instruction % 100 # getting the last 2 digits

def get_modes(instruction): 
    modes = []
    instruction //= 100  # removes the opcode part
    while instruction > 0:
        modes.append(instruction % 10)
        instruction //= 10
    return modes

def get_num_parameters(opcode):
    val = opcode_info[opcode]
    return val[1]

def get_function(opcode):
    val = opcode_info[opcode]
    return val[0]

def get_parameters(memory, ip, num_parameters, modes, opcode):

    parameters = []
    # write parameters are the last parameter for these opcodes
    write_opcodes = {1, 2, 3, 7, 8}
    
    for i in range(num_parameters): # iterate over each parameter
        parameter_address = ip + i + 1 # address of the current parameter
        if i < len(modes):
            mode = modes[i]
        else: # default to position mode
            mode = 0
        
        # The last parameter for write_opcodes is always an address
        is_write_parameter = (opcode in write_opcodes) and (i == num_parameters - 1)
        
        if is_write_parameter:
            # Write-Parameter: always position mode
            parameters.append(memory[parameter_address])
        elif mode == 0:  # position mode
            parameters.append(memory[memory[parameter_address]])
        elif mode == 1:  # immediate mode
            parameters.append(memory[parameter_address])
    
    return parameters

# opcode_info -> opcode: (function, number of parameters)
opcode_info = { 
    1: (add, 3),
    2: (multiply, 3),
    3: (read_input, 1),
    4: (write_output, 1),
    5: (jump_if_true, 2),
    6: (jump_if_false, 2),
    7: (less_than, 3),
    8: (equals, 3)
}

# --------------------The main simulation function--------------------
def simulate_virtual_machine(memory):
    ip = 0 # the instruction pointer
    while ip < len(memory):
        opcode = get_opcode(memory[ip])
        if opcode == 99: # halt-opcode
            break
        modes = get_modes(memory[ip])
        num_parameters = get_num_parameters(opcode)
        function = get_function(opcode)
        resolved_parameters = get_parameters(memory, ip, num_parameters, modes, opcode) # list of all "real" parameter values

        result = function(memory, resolved_parameters)
        if result != None:
            ip = result
        else:
            ip += num_parameters +1

simulate_virtual_machine() # When providing input '5' the program outputs: 16694270

