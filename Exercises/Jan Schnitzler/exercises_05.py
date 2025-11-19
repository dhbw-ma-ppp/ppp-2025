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
import numpy as np  
import matplotlib.pyplot as plt


class IntComputer:
    def __init__(self, input_getter, output_collector):
        def get_input(modes):
            # Liest einen Eingabewert und schreibt ihn an die Zieladresse (unter Berücksichtigung des Modi)
            target_mode = modes % 10
            if target_mode == 2:
                # relativer Modus: Basisoffset addieren
                target = self.memory.get(self.ip, 0) + self.relative_mode_offset
            else:
                # positionaler Modus: Adresse direkt nehmen
                target = self.memory.get(self.ip, 0)
            self.memory[target] = input_getter()
            self.ip += 1

        def write_output(modes):
            # Liest ein Argument (berechnet nach Modi) und gibt es an den Collector weiter
            x, = self.get_function_arguments(modes, 1)
            output_collector(x)

        def set_offset(modes):
            # Ändert den relativen Basisoffset um den übergebenen Wert
            x, = self.get_function_arguments(modes, 1)
            self.relative_mode_offset += x

        # Zuordnung von Opcode -> Funktion (CRUD der Operationen)
        self.function_map = {
            1: self._make_register_setter(operator.add),   # addieren und speichern
            2: self._make_register_setter(operator.mul),   # multiplizieren und speichern
            3: get_input,                                  # eingabe
            4: write_output,                               # ausgabe
            5: self._make_ip_setter(operator.ne),          # springe wenn wahr (non-zero)
            6: self._make_ip_setter(operator.eq),          # springe wenn falsch (zero)
            7: self._make_register_setter(operator.lt),    # kleiner-than => speichern
            8: self._make_register_setter(operator.eq),    # equals => speichern
            9: set_offset,                                 # relativen offset anpassen
        }

    def _make_register_setter(self, func):
        # Erzeugt eine Funktion, die zwei Operanden liest, die Funktion darauf anwendet und das Ergebnis in ein Ziel schreibt
        def f(modes):
            x, y = self.get_function_arguments(modes, 2)  # zwei Operanden lesen (Modi berücksichtigen)
            target_mode = (modes // (10**2)) % 10         # Ziel-Parameter-Modus (drittes Argument)
            if target_mode == 2:
                # relativer Zielmodus
                target = self.memory.get(self.ip, 0) + self.relative_mode_offset
            else:
                # positionsziel
                target = self.memory.get(self.ip, 0)
            self.memory[target] = int(func(x, y))        # Ergebnis schreiben
            self.ip += 1
        return f

    def _make_ip_setter(self, func, comparison_value=0):
        # Erzeugt eine Funktion, die ggf. den Instruction Pointer (ip) setzt (Bedingung wird über func geprüft)
        def f(modes):
            x, y = self.get_function_arguments(modes, 2)  # zwei Argumente: Bedingungswert und Zieladresse
            if func(x, comparison_value):
                # Bedingung erfüllt -> ip auf y setzen (kein zusätzliches ip += nötig)
                self.ip = y
        return f

    def _resolve_argument_value(self, arg_mode, arg_value):
        # Gibt den Wert eines Arguments zurück, abhängig vom Modus:
        # 0 = positionell (Speicher an dieser Adresse), 1 = unmittelbar (direkter Wert),
        # 2 = relativ (Adresse + relative_mode_offset)
        if arg_mode == 0:
            return self.memory.get(arg_value, 0)
        if arg_mode == 1:
            return arg_value
        if arg_mode == 2:
            return self.memory.get(arg_value + self.relative_mode_offset, 0)

    def get_function_arguments(self, modes, n_args):
        # Liest n_args Rohwerte aus dem Speicher (nachfolgende Speicherplätze),
        # berechnet jeweils den effektiven Wert abhängig vom jeweiligen Modus und erhöht ip
        arg_values = [self.memory[self.ip + x] for x in range(n_args)]
        arg_modes = [(modes // (10**i)) % 10 for i in range(n_args)]
        arguments = [self._resolve_argument_value(mode, value) for mode, value in zip(arg_modes, arg_values)]
        self.ip += n_args
        return arguments

    def split_command_and_modes(self):
        # Trennt das aktuelle Kommando in Opcode (letzte zwei Ziffern) und die Modi (restliche Ziffern)
        command = self.memory[self.ip]
        self.ip += 1
        return command % 100, command // 100

    def run(self, data):
        # Initialisiert Speicher als dict (sparse memory), ip und relativen Offset und führt das Programm aus
        self.memory = {i: v for i, v in enumerate(data)}
        self.ip = 0
        self.relative_mode_offset = 0

        while True:
            opcode, modes = self.split_command_and_modes()
            if opcode == 99:
                # Programmende
                break

            # die passende Funktion für den Opcode aufrufen
            opcode_function = self.function_map[opcode]
            opcode_function(modes)

def load_program_data(filename):
    with open(filename, 'r') as f:
        data = f.read().strip()
    return [int(x) for x in data.splitlines()] 
    
def solve_part_1(program_data):
    print("Part 1 solution:")

    output_buffer = []

    def collect_output(value):
        # sammle Ausgabewerte im Puffer
        output_buffer.append(value)

    def dummy_input():
        # Dummy-Eingabefunktion (wird nicht benötigt in Teil 1)
        print("Unerwartete Eingabeanforderung!")
        return 0
    
    computer = IntComputer(input_getter=dummy_input, output_collector=collect_output) 
    computer.run(program_data.copy()) 
    
    screen = {}

    for i in range(0, len(output_buffer), 3):
        x = output_buffer[i]
        y = output_buffer[i + 1]
        tile_type = output_buffer[i + 2]
        if (x, y) == (-1, 0):
            # Score-Ausgabe (kann ignoriert werden in Teil 1)
            continue
        screen[(x, y)] = tile_type

    block_count = list(screen.values()).count(2)
    print(f"Anzahl der Block-Tiles: {block_count}")

    # Visualisierung des Bildschirms
    max_x = max(pos[0] for pos in screen.keys())
    max_y = max(pos[1] for pos in screen.keys())

    grid = np.zeros((max_y + 1, max_x + 1), dtype=int)

    for (x, y), tile_type in screen.items():
        grid[y, x] = tile_type

    # Plotten des Bildschirms
    plt.imshow(grid)
    plt.title("Breakout Screen - Part 1")
    plt.show() # Anzeige des Plots
    print("Plot Fenster muss geschlossen werden, um fortzufahren.")



class game_state:
    def __init__(self, grid_shape, target_display, ax):
        self.grid = np.zeros(grid_shape, dtype=int)
        self.score = 0
        self.ball_x = 0
        self.paddle_x = 0
        self.output_buffer = []

        self.img = target_display
        self.ax = ax

    def collect_output(self, value): 
        self.output_buffer.append(value) 

        if len(self.output_buffer) == 3: # wir haben ein komplettes Triplet
            #x = self.output_buffer[0]
            #y = self.output_buffer[1]
            x,y, tile_type = self.output_buffer
            self.output_buffer = []

            if (x, y) == (-1, 0): # score update
                self.score = tile_type
            else:
                if 0 <= y < self.grid.shape[0] and 0 <= x < self.grid.shape[1]:
                    self.grid[y, x] = tile_type

                    if tile_type == 4: # ball
                        self.ball_x = x
                    elif tile_type == 3: # paddle
                        self.paddle_x = x

    def get_move(self): 
        self.img.set_data(self.grid) # aktualisiere das Bild
        self.ax.set_title(f"Breakout Game - Score: {self.score}")
        plt.pause(0.01) # kurze Pause, um das Bild zu aktualisieren
        if self.ball_x < self.paddle_x:
            return -1
        elif self.ball_x > self.paddle_x:
            return 1
        else:
            return 0
        
def solve_part_2(program_data):
    print("Part 2 solution:")

    MAX_X = 44  # basierend auf der Analyse des Bildschirms in Teil 1
    MAX_Y = 24 
    plt.ion()  # interaktiver Modus an

    fig, ax = plt.subplots() # Erstelle eine Figur und Achse
    ax.set_title("Breakout Game - Part 2")


    initial_grid = np.zeros((MAX_Y + 1, MAX_X + 1), dtype=int)
    img = ax.imshow(initial_grid, vmin=0, vmax=4, cmap='plasma') # Farbschema für die Kacheln


    plt.show() # Anzeige des Plots
    print("Plot Fenster muss geschlossen werden, um fortzufahren.")

    program_data = program_data.copy() 
    program_data[0] = 2  # setze erstes Kommando auf 2

    state = game_state(grid_shape=(MAX_Y + 1, MAX_X + 1), target_display=img, ax=ax)

    computer = IntComputer(input_getter=state.get_move, output_collector=state.collect_output) 

    computer.run(program_data)
    print(f"Endscore: {state.score}")

    ax.set_title(f"Breakout Game - Final Score: {state.score}") 

    plt.ioff()  # interaktiver Modus aus
    plt.show()  # finale Anzeige des Plots


    

   


if __name__ == '__main__':

    game_program_data = load_program_data('data/breakout_commands.txt')
    #solve_part_1(game_program_data)
    solve_part_2(game_program_data)