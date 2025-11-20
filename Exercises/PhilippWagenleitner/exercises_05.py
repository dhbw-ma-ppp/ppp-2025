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


class IntComputer:
    def __init__(self, input_getter, output_collector):
        def get_input(modes):
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
            self.memory[target] = int(func(x, y))
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
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def get_play_mode():
    """Für Play_mode-Auswahl"""
    print("Wähle den Game-Mode:")
    print("(1) - Statisches-Bild\n(2) - BOT-Zuschauen")
    play_mode=input("Eingabe: ")
    match play_mode:
        case '1':
            return 0
        case '2':
            return 1
        case _:
            print("Kein Modus ausgewählt - Statisches Bild")
            return 0

def collect_output(x):
    """Nimmt Outputs des Int-Computers und fügt sie einer Liste hinzu"""
    outputs.append(x)

def size_of_picture(outputs): 
        """nimmt den Output des IntComputers, gliedert diesen in Triplets und 
        gibt den größten 1. (x-wert) und 2. (y-wert) zurück"""
        temp_list=[]
        x=0
        xmax=0
        ymax=0
        for i in range(len(outputs)): #gibt xmax und ymax zurück
            x+=1
            temp_list.append(outputs[i])
            if x==3:
                if xmax<temp_list[0]:
                    xmax=temp_list[0]
                if ymax<temp_list[1]:
                    ymax=temp_list[1]
                temp_list.clear()
                x=0 
                continue
        return xmax, ymax

def allocate(picture, output): 
        """nimmt die Triplets aus den Output, den 1. Wert als X-Wert, den 2. als Y-Wert, den
        3. als Wert und fügt sie in das 2d-Array ein
        !Achtung!: Vertauschung von X und Y bei 2d-Array"""
        #(0, len(outputs), 3) = führt for schleife mit i in 3er Schritten aus
        for i in range(0, len(outputs), 3): 
            x_wert=output[i]
            y_wert=output[i+1]
            typ=output[i+2]
            #Atari-Breakout Look
            if typ==2:
                typ = 5 + ((y_wert // 3) % 6) 
            picture[y_wert, x_wert]=typ
        return picture



def bot_input():
    """Automatischer Input von dem Bot, abhängig von der 
    X-Paddle-Position und X-Ball-Position"""
    global x_ball, x_paddle, img_obj, score

    img_obj.set_data(picture)
    ax.set_title(f"Breakout - Score: {score}", color='white', fontname='monospace')

    plt.pause(0.001)


    if x_ball>x_paddle:
        return 1
    elif x_ball==x_paddle:
        return 0
    else:
        return -1


def auto_collect_output(x):
    """Output aufnehmen und anschließend direkt in 2d-Array verarbeiten"""
    global x_ball, x_paddle, score, picture
    outputs.append(x)
    
    if len(outputs)==3:
        x_wert=outputs[0]
        y_wert=outputs[1]
        typ=outputs[2]
        outputs.clear()
        if x_wert==-1 and y_wert==0:
            score=typ
        else:
            # Atari Rainbow:
            if typ == 2:
            # Berechnet Farbe basierend auf Zeile 
                typ = 5 + ((y_wert // 3) % 6)
            picture[y_wert, x_wert] = typ
            if typ==4:
                x_ball=x_wert
            if typ==3:
                x_paddle=x_wert
    

#Globale Variablen
x_ball = 0
x_paddle = 0
score = 0


# Setup für Atari Farben
atari_colors = [
    'black',   # 0: Leer
    'dimgray', # 1: Wand
    'gold',    # 2: Block (Fallback)
    'red',     # 3: Paddle
    'white',   # 4: Ball
    # Regenbogen Farben für die Zeilen (IDs 5-10)
    'red', 'orange', 'yellow', 'lime', 'cyan', 'magenta'
]
cmap = ListedColormap(atari_colors)


if __name__ == '__main__':

    game_choice=get_play_mode()

    commands= []
    #NOTE: breakout_commands.txt muss in dem Ordner von der Python-Datei liegen
    path=sys.path[0]
    data=path + "/breakout_commands.txt"
    #einlesen von breakout_commands.txt
    with open(data, 'r') as numbers: 
        for line in numbers:
            commands.append(int(line))


    #---Static-Mode---
    if game_choice==0:

    #Hier: Ausführung des IntComputers, der den Output in Liste speichert   
        outputs = []
        ic = IntComputer(lambda: 0, collect_output)
        ic.run(commands)

        
    #Hier: Bestimmung der Größe des 2D-Arrays    
        [xmax,ymax]=size_of_picture(outputs)
    #Hier: Erstellung eines zero-2D-Arrays
        picture=np.zeros((ymax+1,xmax+1))
        
        
    #Einführen der Triplets in das 2D-Arrays
        picture=allocate(picture, outputs)
    #Ausgeben des "Graphen" (Atari-Style)
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('black')
        ax.axis('off')
        ax.set_title("Breakout", color='white', fontname='monospace')
        plt.imshow(picture, cmap=cmap, vmin=0, vmax=10)
        plt.show()
    

    #---Bot-Mode---
    if game_choice==1: 
        commands[0]=2 #Play-Mode
        outputs = []
    
    #Hier: Nur Ausführung für Berechnung von xmax und ymax
        ic_2 = IntComputer(lambda: 0, collect_output)
        ic_2.run(commands)

    #Hier: Bestimmung der Größe des 2D-Arrays    
        [xmax,ymax]=size_of_picture(outputs)

    #outputs leeren:
        outputs = []

    #Zero-Array in passender Größe
        picture=np.zeros((ymax+1,xmax+1)) 

    #Ausführung
        plt.ion()
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('black')
        img_obj = ax.imshow(picture, cmap=cmap, vmin=0, vmax=10)  
        ax.axis('off')
        ic = IntComputer(bot_input, auto_collect_output)
        ic.run(commands)
        plt.ioff()
        plt.show
        print(f"Score: {score}")

