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
from intcomputer import IntComputer
from matplotlib import pyplot as plt

def get_data():
    try:
        with open("data/breakout_commands.txt", "r") as file:
            content = file.read()
    except FileNotFoundError:
        with open("../../data/breakout_commands.txt", "r") as file:
            content = file.read()
            
    string_commands = content.splitlines()
    raw_commands = [int(commands) for commands in string_commands]
    return raw_commands

def convert_data_with_intcomputer(raw_commands, auto_play=True, show_frames_callback=None):
    outputs = []
    frames = []

    game_state = {"paddle_x": 0, "ball_x": 0, "score": 0, "grid": {}}
    
    def get_input_auto():
        if game_state["ball_x"] < game_state["paddle_x"]:
            return -1  # move left
        elif game_state["ball_x"] > game_state["paddle_x"]:
            return 1   # move right
        else:
            return 0 # stay
        
    def get_input_manual():
        if show_frames_callback:
            show_frames_callback(game_state["grid"], game_state["score"])
        
        print(f"\rScore: {game_state['score']} | Paddle: {game_state['paddle_x']} | Ball: {game_state['ball_x']}", end="")
        while True:
            user_input = input(" | Move (-1/0/1): ")
            if user_input in ['-1', '0', '1']:
                return int(user_input)
            print("Invalid input", end="")
    
    def collect_output(value):
        outputs.append(value)

        if len(outputs) % 3 == 0:
            x = outputs[-3]
            y = outputs[-2]
            tile_or_score = outputs[-1]

            if x == -1 and y == 0:
                game_state["score"] = tile_or_score
            else:
                game_state['grid'][(x, y)] = tile_or_score
                
                if tile_or_score == 3:
                    game_state["paddle_x"] = x
                elif tile_or_score == 4:
                    game_state["ball_x"] = x
            
            frames.append({
                'grid': dict(game_state['grid']),
                'score': game_state["score"]
            })
    
    input_function = get_input_auto if auto_play else get_input_manual
    computer = IntComputer(input_function, collect_output)
    computer.run(raw_commands)

    return frames

def update_plot(ax, grid, score, max_x, max_y):
    ax.clear()
    ax.set_facecolor("black")
    ax.set_ylim(max_y + 1, -1) 
    ax.set_xlim(-1, max_x + 1)
    ax.axis("off")
    
    color_map = {0: "k", 1: "g", 2: "b", 3: "r", 4: "w"}
    
    positions = [(pos, tile) for pos, tile in grid.items() if tile != 0]
    if positions:
        coords, tiles = zip(*positions)
        x, y = zip(*coords)
        colors = [color_map[t] for t in tiles]
        ax.scatter(x, y, c=colors, s=80, marker="s")
    
    ax.set_title(f"Breakout - Score: {score}", color="white", fontsize=14)

def animate_game(frames):
    if not frames:
        print("No frames!")
        return

    all_positions = set()
    for frame in frames:
        all_positions.update(frame['grid'].keys())
    
    if not all_positions:
        return

    xs = [pos[0] for pos in all_positions]
    ys = [pos[1] for pos in all_positions]
    max_x, max_y = max(xs), max(ys)
    

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("black")
    
    plt.ion()
    plt.show()
    
    step = max(1, len(frames) // 500) 

    for i in range(0, len(frames), step):
        frame = frames[i]
        update_plot(ax, frame['grid'], frame['score'], max_x, max_y)
        plt.pause(0.001)
    
    last_frame = frames[-1]
    update_plot(ax, last_frame['grid'], last_frame['score'], max_x, max_y)
    
    print(f"FINAL SCORE: {last_frame['score']}")
    
    plt.ioff()
    plt.show() 

def show_final_state(frames):
    if not frames:
        return
    
    final_frame = frames[-1]
    
    xs = [pos[0] for pos, _ in final_frame['grid'].items()]
    ys = [pos[1] for pos, _ in final_frame['grid'].items()]
    max_x, max_y = (max(xs), max(ys)) if xs else (44, 24)

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("black")
    
    update_plot(ax, final_frame['grid'], final_frame['score'], max_x, max_y)
    
    print(f"\nFinal Score: {final_frame['score']}")
    plt.show()

def game(mode, animate=True, auto_play=True):
    raw_commands = get_data()
    raw_commands[0] = mode
    
    # Case 1: Manual Play
    if not auto_play and animate:
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor("black")
        plt.ion()
        plt.show()

        max_x, max_y = 42, 24 

        def live_callback(grid, score):
            update_plot(ax, grid, score, max_x, max_y)
            plt.pause(0.01)

        frames = convert_data_with_intcomputer(
            raw_commands, 
            auto_play=False,
            show_frames_callback=live_callback 
        )
        
        plt.ioff()
        print(f"\nFINAL SCORE: {frames[-1]['score']}")
        plt.show()
        
    # Case 2: Auto Play
    else:
        frames = convert_data_with_intcomputer(raw_commands, auto_play=True)
        
        if animate and mode == 2:
            animate_game(frames)
        else:
            show_final_state(frames)

if __name__ == "__main__":
    # Part 2: Auto-play
    game(mode=2, animate=True, auto_play=True)
    
    # Part 2: Manual Control (Uncomment to play)
    # game(mode=2, animate=True, auto_play=False)

#Final Score: 17159