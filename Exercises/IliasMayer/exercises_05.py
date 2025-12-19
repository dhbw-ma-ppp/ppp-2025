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

from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np


class IntcodeComputer:
    """Vollständiger Intcode-Computer mit relativer Adressierung."""
    
    def __init__(self, program, input_callback=None):
        # Speicher als defaultdict, um beliebig großen Speicher zu unterstützen
        self.memory = defaultdict(int)
        for i, val in enumerate(program):
            self.memory[i] = val
        
        self.ip = 0  # Instruction Pointer
        self.relative_base = 0  # Relative Base für Modus 2
        self.input_callback = input_callback
        self.outputs = []
        self.halted = False
    
    def get_parameter(self, offset, mode):
        """Gibt den Parameterwert basierend auf dem Modus zurück."""
        value = self.memory[self.ip + offset]
        
        if mode == 0:  # Position mode
            return self.memory[value]
        elif mode == 1:  # Immediate mode
            return value
        elif mode == 2:  # Relative mode
            return self.memory[self.relative_base + value]
        else:
            raise ValueError(f"Unbekannter Parameter-Modus: {mode}")
    
    def get_write_address(self, offset, mode):
        """Gibt die Schreibadresse basierend auf dem Modus zurück."""
        value = self.memory[self.ip + offset]
        
        if mode == 0:  # Position mode
            return value
        elif mode == 2:  # Relative mode
            return self.relative_base + value
        else:
            raise ValueError(f"Ungültiger Schreibmodus: {mode}")
    
    def run(self):
        """Führt das Programm aus und gibt Outputs als Triplets zurück."""
        while not self.halted:
            # Instruction dekodieren
            instruction = self.memory[self.ip]
            opcode = instruction % 100
            mode1 = (instruction // 100) % 10
            mode2 = (instruction // 1000) % 10
            mode3 = (instruction // 10000) % 10
            
            if opcode == 99:  # Halt
                self.halted = True
                break
            
            elif opcode == 1:  # Addition
                param1 = self.get_parameter(1, mode1)
                param2 = self.get_parameter(2, mode2)
                target = self.get_write_address(3, mode3)
                self.memory[target] = param1 + param2
                self.ip += 4
            
            elif opcode == 2:  # Multiplikation
                param1 = self.get_parameter(1, mode1)
                param2 = self.get_parameter(2, mode2)
                target = self.get_write_address(3, mode3)
                self.memory[target] = param1 * param2
                self.ip += 4
            
            elif opcode == 3:  # Input
                target = self.get_write_address(1, mode1)
                if self.input_callback:
                    self.memory[target] = self.input_callback()
                else:
                    self.memory[target] = int(input("Eingabe: "))
                self.ip += 2
            
            elif opcode == 4:  # Output
                param1 = self.get_parameter(1, mode1)
                self.outputs.append(param1)
                
                # Wenn wir ein komplettes Triplet haben, yielden
                if len(self.outputs) == 3:
                    yield tuple(self.outputs)
                    self.outputs = []
                
                self.ip += 2
            
            elif opcode == 5:  # Jump-if-true
                param1 = self.get_parameter(1, mode1)
                param2 = self.get_parameter(2, mode2)
                if param1 != 0:
                    self.ip = param2
                else:
                    self.ip += 3
            
            elif opcode == 6:  # Jump-if-false
                param1 = self.get_parameter(1, mode1)
                param2 = self.get_parameter(2, mode2)
                if param1 == 0:
                    self.ip = param2
                else:
                    self.ip += 3
            
            elif opcode == 7:  # Less than
                param1 = self.get_parameter(1, mode1)
                param2 = self.get_parameter(2, mode2)
                target = self.get_write_address(3, mode3)
                self.memory[target] = 1 if param1 < param2 else 0
                self.ip += 4
            
            elif opcode == 8:  # Equals
                param1 = self.get_parameter(1, mode1)
                param2 = self.get_parameter(2, mode2)
                target = self.get_write_address(3, mode3)
                self.memory[target] = 1 if param1 == param2 else 0
                self.ip += 4
            
            elif opcode == 9:  # Adjust relative base
                param1 = self.get_parameter(1, mode1)
                self.relative_base += param1
                self.ip += 2
            
            else:
                raise ValueError(f"Unbekannter Opcode: {opcode} bei Position {self.ip}")


def visualize_screen(tiles):
    """Erstellt eine visuelle Darstellung des Spielfelds."""
    if not tiles:
        print("Keine Tiles zum Visualisieren")
        return
    
    max_x = max(x for x, y in tiles.keys())
    max_y = max(y for x, y in tiles.keys())
    
    # Array erstellen
    screen = np.zeros((max_y + 1, max_x + 1), dtype=int)
    for (x, y), tile_type in tiles.items():
        screen[y, x] = tile_type
    
    # Farben für verschiedene Tile-Typen
    colors = ['black', 'gray', 'blue', 'green', 'red']
    cmap = plt.cm.colors.ListedColormap(colors)
    
    # Plot erstellen
    plt.figure(figsize=(12, 8))
    plt.imshow(screen, cmap=cmap, interpolation='nearest')
    plt.colorbar(ticks=[0, 1, 2, 3, 4], 
                 label='Tile Type',
                 orientation='vertical')
    plt.title('Breakout Game - Static Screen')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.tight_layout()
    plt.show()


def play_breakout(program, auto_play=False):
    """
    Spielt das Breakout-Spiel.
    
    Args:
        program: Das Intcode-Programm
        auto_play: Wenn True, wird der Paddle automatisch gesteuert
    """
    # Für automatisches Spielen
    game_state = {'ball_x': 0, 'paddle_x': 0, 'score': 0}
    
    def auto_input():
        """Automatische Paddle-Steuerung: Folge dem Ball."""
        if game_state['ball_x'] < game_state['paddle_x']:
            return -1
        elif game_state['ball_x'] > game_state['paddle_x']:
            return 1
        else:
            return 0
    
    def manual_input():
        """Manuelle Steuerung."""
        inp = input("Paddle bewegen (-1: links, 0: bleiben, 1: rechts): ")
        return int(inp)
    
    input_callback = auto_input if auto_play else manual_input
    computer = IntcodeComputer(program, input_callback)
    
    tiles = {}
    
    for x, y, value in computer.run():
        if x == -1 and y == 0:
            # Score Update
            game_state['score'] = value
            if not auto_play:
                print(f"Score: {value}")
        else:
            # Tile Update
            tiles[(x, y)] = value
            
            # Positionen aktualisieren für Auto-Play
            if value == 3:  # Paddle
                game_state['paddle_x'] = x
            elif value == 4:  # Ball
                game_state['ball_x'] = x
    
    return tiles, game_state['score']

if __name__ == "__main__":
    filepath = "data/breakout_commands.txt"
    
    with open(filepath, "r") as f:
        content = f.read().strip()
        program = list(map(int, content.split(',' if ',' in content else None)))
    
    # PART 1
    print("PART 1: Statisches Spielfeld")
    computer_part1 = IntcodeComputer(program.copy(), input_callback=lambda: 0)
    tiles_part1 = {(x, y): tile for x, y, tile in computer_part1.run()}
    print(f"Blöcke: {sum(1 for t in tiles_part1.values() if t == 2)}")
    visualize_screen(tiles_part1)
    
    # PART 2
    print("\nPART 2: Spiel spielen")
    program[0] = 2
    tiles_part2, final_score = play_breakout(program, auto_play=True)
    print(f"Finaler Score: {final_score}")