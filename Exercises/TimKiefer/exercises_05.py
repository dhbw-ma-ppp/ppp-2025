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




# COMPLETE INT COMPUTER
# This is only relevant if you decide to extend your own implementation with the necessary features.
# If you decide to use my implementation you can ignore this part.
#
#
# - The computer needs to implement memory much /larger/ than the set of initial commands.
#   Any memory address not part of the initial commands can be assumed to be initialized to 0.
#   (only positive addresses are valid). 

# Idee: json string for memory?


# - You need to support a new parameter mode, 'relative mode', denoted as mode 2 in the 'mode' part
#   of the instructions.
#   Relative mode is similar to position mode (the first access mode you implemented). However, 
#   parameters in relative mode count not from 0, but from a value called 'relative offset'. 

#   When the computer is initialized, the relative offset is initialized to 0, and as long as it remains
#   0 relative mode and position mode are identical.


#   In general though parameters in relative mode address the memory location at 'relative offset + parameter value'.
#   EXAMPLE: if the relative offset is 50, the mode is 2, and the value you read from memory is 7 you should 
#     retrieve data from the memory address 57.

# Idee: self.relative_offset variable

#     Equally, if you read -7, you should retrieve data from the memory address 43.
#   This applies to both read- and write operations.

# - You need to implement a new opcode, opcode 9. opcode 9 adjusts the relative offset by the value of its only parameter.
#   the offset increases by the value of the parameter (or decreases if that value is negative).
# --- Ab hier mein Code ---

import collections # wichtig fürr 'defaultdict'
import numpy as np # pyright: ignore[reportMissingImports] // pyright is nur damit VS Code kein Problem mir beim Schreiben anzeigt
from matplotlib import pyplot as plt # pyright: ignore[reportMissingModuleSource] 
from matplotlib.colors import ListedColormap # pyright: ignore[reportMissingModuleSource]


def simulation_computer(initial_memory): #modifizierte Variante meines Computers von Woche 3 & 4
    memory = collections.defaultdict(int, {i: v for i, v in enumerate(initial_memory)}) #'defaultdict(int)': Zugriff auf eine unbekannte Speicheradresse == 0 // 'initial_memory' wird zudem initialisiert
    i = 0
    relative_base = 0 #wird für den Relativmodus benötigt
    while True:
        full_instruction = str(memory[i]).zfill(5)
        opcode = int(full_instruction[-2:]) # Extrahiert die letzten beiden Ziffern als 'Opcode' 
        mode1 = int(full_instruction[-3]) # ersten Parameter (dritte Ziffer von rechts)
        mode2 = int(full_instruction[-4]) # zweiten Parameter (vierte Ziffer von rechts)
        mode3 = int(full_instruction[-5]) # dritten Parameter (fünfte Ziffer von rechts)

        def get_param_value(mem, index, mode):
            if mode == 0: # Modus 0 (Positionsmodus)
                return mem[mem[index]]
            elif mode == 1: # Modus 1 (Direktmodus)
                return mem[index]
            elif mode == 2: # Modus 2 (Relativmodus)
                return mem[relative_base + mem[index]]
            else: # Fehler prävension... hatte den mehr als nur einmal
                raise ValueError(f"Unknown parameter mode for getting value: {mode} at index {index}")

        def get_target_address(mem, index, mode):
            if mode == 0:
                return mem[index]
            elif mode == 2: 
                return relative_base + mem[index]
            else: 
                raise ValueError(f"Invalid parameter mode for writing value: {mode} at index {index}")

        if opcode == 99: # Opcode 99: Halt
            break 
        elif opcode == 1: # Opcode 1: Addition
            val1 = get_param_value(memory, i + 1, mode1) 
            val2 = get_param_value(memory, i + 2, mode2) 
            target_address = get_target_address(memory, i + 3, mode3)
            memory[target_address] = val1 + val2
            i += 4 
        elif opcode == 2: # Opcode 2: Multiplikation
            val1 = get_param_value(memory, i + 1, mode1)
            val2 = get_param_value(memory, i + 2, mode2) 
            target_address = get_target_address(memory, i + 3, mode3) 
            memory[target_address] = val1 * val2 
            i += 4 
        elif opcode == 3: # Opcode 3: Eingabe
            target_address = get_target_address(memory, i + 1, mode1) 
            user_input = yield "INPUT" # Pausiert den Computer, gibt das Signal zurück & wartet Wert per .send()
            memory[target_address] = user_input 
            i += 2 
        elif opcode == 4: # Opcode 4: Ausgabe
            val1 = get_param_value(memory, i + 1, mode1) 
            yield val1 # Pausiert den Computer und gibt den Wert zurück.
            i += 2 
        elif opcode == 5: # Opcode 5: Springe-wenn-wahr (Jump-if-true).
            val1 = get_param_value(memory, i + 1, mode1) # Holt den ersten Parameter (die Bedingung).
            val2 = get_param_value(memory, i + 2, mode2) # Holt den zweiten Parameter (die Sprungadresse).
            if val1 != 0: 
                i = val2 
            else: 
                i += 3 
        elif opcode == 6: # Opcode 6: Springe-wenn-falsch (Jump-if-false)
            val1 = get_param_value(memory, i + 1, mode1) 
            val2 = get_param_value(memory, i + 2, mode2) 
            if val1 == 0: 
                i = val2
            else: 
                i += 3 
        elif opcode == 7: # Opcode 7: Kleiner als
            val1 = get_param_value(memory, i + 1, mode1) 
            val2 = get_param_value(memory, i + 2, mode2) 
            target_address = get_target_address(memory, i + 3, mode3)
            if val1 < val2: 
                memory[target_address] = 1 
            else:
                memory[target_address] = 0 
            i += 4 
        elif opcode == 8: # Opcode 8: Gleich
            val1 = get_param_value(memory, i + 1, mode1) 
            val2 = get_param_value(memory, i + 2, mode2) 
            target_address = get_target_address(memory, i + 3, mode3)
            if val1 == val2: 
                memory[target_address] = 1
            else:
                memory[target_address] = 0 
            i+= 4 
        elif opcode == 9: # Opcode 9: Relative Basis anpassen // Neu hinzugefügt für vollständigen Int-Computer 
            val1 = get_param_value(memory, i + 1, mode1) 
            relative_base += val1 # Addiert den Wert zur 'relative_base'.
            i += 2 
        else: 
            raise ValueError(f"Unknown opcode {opcode} encountered at position {i} with full instruction {full_instruction}") 
    return None # Kommunikation erfoglz über 'yield' => kein Rückgabe

def load_commands(filename): # Definiert eine Funktion zum Laden der Befehle aus einer Datei.
    """Reads Intcode commands from a file.""" # Docstring, der die Funktion beschreibt.
    with open(filename, 'r') as f: # Öffnet die angegebene Datei im Lesemodus ('r'). 'with' sorgt dafür, dass die Datei am Ende automatisch geschlossen wird.
        return [int(line.strip()) for line in f] # Erstellt eine Liste: Für jede Zeile in der Datei wird der Zeilenumbruch entfernt (.strip()) und der String in eine Ganzzahl (int()) umgewandelt.


#--- 1.Part der Aufgabe (Bild) ---


def run_part1(commands):
    """Runs the Intcode computer and collects screen drawing output.""" 
    print("--- Running Part 1: Drawing initial screen ---") 
    computer = simulation_computer(commands)
    outputs = [] 
    for output in computer: # bei jedem 'yield' wird der Wert in 'output' gespeichert
        outputs.append(output) 

    print(f"Program finished, produced {len(outputs)} output values.") 

    # --- Visuialusierung vom Code --- 

    tiles = {}
    for i in range(0, len(outputs), 3): # Iteriert durch die 'outputs'-Liste in 3er-Schritten (x, y, id)
        x, y, tile_id = outputs[i], outputs[i+1], outputs[i+2]
        if x == -1 and y == 0:
            continue 
        tiles[(x, y)] = tile_id # Speichert die Kachel-ID(x, y)

    # Bestimmung Größe des Rasters
    max_x = max(k[0] for k in tiles.keys())
    max_y = max(k[1] for k in tiles.keys())
    screen = np.zeros((max_y + 1, max_x + 1), dtype=int) # 2D-Array als bildschrim

    #Füllen des Rasters
    for (x, y), tile_id in tiles.items(): 
        screen[y, x] = tile_id 

    # Erstellung Farbpalette
    # 0: empty (black), 1: wall (grey), 2: block (blue), 3: paddle (green), 4: ball (red) 
    cmap = ListedColormap(['black', 'grey', 'blue', 'green', 'red']) 
    plt.imshow(screen, cmap=cmap, interpolation='nearest') #'screen'-Array als Bild // 'cmap' legt Farben fest // 'interpolation' für scharfe Kanten.
    plt.title("Breakout - Part 1")
    plt.show()


    # --- Part 2: Interaktives Game ---


def run_part2(commands):
    """Runs the Intcode computer to play the Breakout game automatically.""" 
    print("\n--- Running Part 2: Playing the game ---") 

    commands[0] = 2 # Gamemode

    computer = simulation_computer(commands)
    
    score = 0 
    ball_x, paddle_x = 0, 0 # Initialisierung für Gegner
    outputs = [] 

    
    screen = np.zeros((24, 44), dtype=int) # 2D-Array aus Part 1

    # Plotten => spiel läuft flüssig lädt nur neue Pixel
    plt.ion()
    fig, ax = plt.subplots()
    cmap = ListedColormap(['black', 'grey', 'blue', 'green', 'red']) 
    # vmin/vmax stellt sicher, dass die Farben gleich bleiben
    screen_img = ax.imshow(screen, cmap=cmap, vmin=0, vmax=4, interpolation='nearest')
    score_text = ax.text(0, -1, f"Score: {score}", color='white', fontsize=12) # Live Score funktioniert noch nicht :-/
    plt.title("Breakout - Part 2")

    game_running = True 
    is_first_run = True 
    while True: 

        # --- Player des Spieles --- 

        #Logik: bewege das Paddel in Richtung des Balls.
        joystick_input = np.sign(ball_x - paddle_x) # Berechnet für nächsten Zug: -1 (links), 0 (neutral), 1 (rechts).
        

        while True: # Innere Schleife, um alle Ausgaben für einen Frame zu sammel => Fokus auf Flüssigkeit
            try: 
                output = next(computer) if is_first_run else computer.send(joystick_input)
                is_first_run = False
                joystick_input = None

                if output == "INPUT": 
                    break #  innere Schleife stoppen =>  Bildschirm & Player Zug erneuern 

                x = output 
                y = next(computer)
                val = next(computer) 

                if x == -1 and y == 0: # Wenn es eine Punktestand-Ausgabe ist...
                    score = val # ...wird die 'score'-Variable aktualisiert.
                else: 
                    screen[y, x] = val 
                    # Wichtig für player
                    if val == 4: ball_x = x 
                    elif val == 3: paddle_x = x 
            
            except StopIteration: 
                game_running = False
                break 
        
        # Aktualisiert Diagramm einmal pro Frame
        score_text.set_text(f"Score: {score}") 
        screen_img.set_data(screen)
        fig.canvas.draw() 
        fig.canvas.flush_events() 
        plt.pause(0.001) # minimale Pause, damit es fürs Auge flüssiger aussieht stadt pixel für pixel

        if not game_running: 
            print("Game has finished.") 
            break 

    plt.ioff()
    print(f"Final Score: {score}")
    plt.show() #damit endstand sichbar ist

if __name__ == "__main__":
    try:
        breakout_commands = load_commands('/Users/timkiefer/Desktop/Dual/Studium/1._Semester/Python/exc_05/breakout_commands.txt') 
        run_part2(breakout_commands.copy())
    except FileNotFoundError: # Bei Code Review müsste dieser erscheinen, da es auf meinen Lokalen Laptop läuft... konnte es nicht per Remote machen
        print("Error: breakout_commands.txt not found. Please check the file path.") 
    