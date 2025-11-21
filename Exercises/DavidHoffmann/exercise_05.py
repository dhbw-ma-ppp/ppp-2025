import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

class names:
    empty_tile = "empty_tile"
    wall = "wall"
    block = "block"
    paddle = "paddle"
    ball = "ball"
# paar Namen festgelegt um die Leserlichkeit zu verbessern
class simulated_computer:

    tile_types_map = {
            0: names.empty_tile,
            1: names.wall,
            2: names.block,
            3: names.paddle,
            4: names.ball
        }
    
    color_map = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}

    def __init__(self):
        self.opcode = 0
        self.commands = []
        self.relative_offset = 0
        self.parameters = [None]
        self.instruction_ptr = 0
        self.address = 0
        self.outputs = []
        self.bildschirm = {}
        self.game_mode = 0
        self.score = 0
        self.auto_input = False
        self.ball_x = 19
        self.paddle_x = 21
        self.height = 26 
        self.width = 45
        self.grid_array = np.zeros((self.height, self.width))
        self.fig = None
        self.img_obj = None
        self.keinBockmehr = False

        self.opcode_map = {
        1: self.add,
        2: self.mul,
        3: self.get_input,
        4: self.write_output,
        5: self.jump_if_true,
        6: self.jump_if_false,
        7: self.is_less_then,
        8: self.is_equal_to,
        9: self.adjust_relative_offset
    }

    def get_parameters(self, number_of_parameters):
        self.parameters = [None] * (number_of_parameters + 1)
        y = 100
        parameter = 1
        while parameter < number_of_parameters + 1:
            if self.instruction_ptr >= len(self.commands):
                self.commands += [0] * 100

            mode = (self.commands[self.instruction_ptr] // y)  % 10
            write_parameter = False
            try:
                match mode:
                    case 0: # position_mode
                        if self.opcode in [1, 2, 7, 8] and parameter == 3: write_parameter = True
                        elif self.opcode == 3 and parameter == 1: write_parameter = True
                        
                        if write_parameter:
                            self.parameters[parameter] = self.commands[self.instruction_ptr + parameter]
                            if self.parameters[parameter] >= len(self.commands):
                                self.commands += [0] * (self.parameters[parameter] - len(self.commands) + 100)
                        else:
                            self.address = self.commands[self.instruction_ptr + parameter]
                            if self.address >= len(self.commands): self.commands += [0] * (self.address - len(self.commands) + 100)
                            self.parameters[parameter] = self.commands[self.address]
                            
                    case 1: # immediate_mode
                            self.parameters[parameter] = self.commands[self.instruction_ptr + parameter]
                            
                    case 2: # relative_mode
                        if self.opcode in [1, 2, 7, 8] and parameter == 3: write_parameter = True
                        elif self.opcode == 3 and parameter == 1: write_parameter = True

                        if write_parameter:
                            self.parameters[parameter] = self.relative_offset + self.commands[self.instruction_ptr + parameter]
                            if self.parameters[parameter] >= len(self.commands):
                                self.commands += [0] * (self.parameters[parameter] - len(self.commands) + 100)
                        else:
                            self.address = self.relative_offset + self.commands[self.instruction_ptr + parameter]
                            if self.address >= len(self.commands): 
                                self.commands += [0] * (self.address - len(self.commands) + 100)
                            self.parameters[parameter] = self.commands[self.address]
                y *= 10
                parameter += 1
            except IndexError:
                self.commands += [0] * 1000
        return self.parameters
    
        
    def add(self):
        self.get_parameters(3)
        self.commands[self.parameters[3]] = self.parameters[1] + self.parameters[2]
        self.instruction_ptr += 4

    def mul(self):
        self.get_parameters(3)
        self.commands[self.parameters[3]] = self.parameters[1] * self.parameters[2]
        self.instruction_ptr += 4

    def get_input(self):
        self.get_parameters(1)

        if self.game_mode == 2 and self.fig and not self.keinBockmehr: # Prüfung ob wir im Game Mode 2 sind und ob ein Fenster mit dem Spiel bereits geöffnet ist und ob du noch Bock hast bzw. ob das Fenster geschlossen wurde
            self.img_obj.set_data(self.grid_array) # Macht, dass das Spiel flüssiger läuft, da nicht jedesmal ein neues Koordnatensystem erstellt wird, sonder lediglich die Daten im bestehenden System verändert werden
            plt.title(f"Breakout - Score: {self.score}") # Macht das der Score pber dem Spiel angezeigt wird und sich immer aktualisiert
            plt.pause(0.001) #0.01 # hier kann man die Geschwindigkeit des Balls bzw. des Spiels verändern

        
        if self.auto_input:
            if self.ball_x < self.paddle_x:
                value = -1 
            elif self.ball_x > self.paddle_x:
                value = 1  
            else:
                value = 0
            self.commands[self.parameters[1]] = value # wenn auto_input aktiviert ist, bewegt sich das paddel automatisch abhängig von der Position des Balls
        else:
            for _ in range(3):
                try:
                    value = int(input("Geben Sie 1  oder 0 oder  -1 ein\n"))
                    self.commands[self.parameters[1]] = value       # wenn man will könnte man auch selber spielen, man muss aber manuell den auto input auf False stellen
                    print("Top")
                    break
                except ValueError:
                    print("1 oder 0 oder -1")
            else:
                print("Sie hatten 3 Versuche und haben es nicht geschafft eine ganze Zahl einzugebn. Dafür haben Sie meinen vollsten Respekt verdient\n")
                print("Der input wird automatisch auf 0 gesetzt")
                value = 0
        self.commands[self.address] = value
        self.instruction_ptr += 2

    def write_output(self):
        self.get_parameters(1)
        self.outputs.append(self.parameters[1])
        if len(self.outputs) == 3:
            pos_x = self.outputs[0]
            pos_y = self.outputs[1]
            tile_id = self.outputs[2]   # hier werden die Informationen aus den Triplets gezogen und zugeordnet
            if self.game_mode == 2:
                if pos_x == -1 and pos_y == 0:
                    self.score = tile_id    # hier kriegt wird der Score geholt
                else:
                    if 0 <= pos_y < self.height and 0 <= pos_x < self.width: #Nur wenn man innerhalb der festgelegten Grenzen ist, wird das Koordinatensystem erneuert 
                        self.grid_array[pos_y, pos_x] = tile_id
                    if tile_id == 4: 
                        self.ball_x = pos_x
                    elif tile_id == 3: 
                        self.paddle_x = pos_x  # Infos für das automatische Paddel
                self.outputs.clear()
        self.instruction_ptr += 2
    
    def jump_if_true(self):
        self.get_parameters(2)
        if self.parameters[1] != 0:
            self.instruction_ptr = self.parameters[2]
        else:
            self.instruction_ptr += 3

    def jump_if_false(self):
        self.get_parameters(2)
        if self.parameters[1] == 0:
            self.instruction_ptr = self.parameters[2]
        else:
            self.instruction_ptr += 3

    def is_less_then(self):
        self.get_parameters(3)
        if self.parameters[1] < self.parameters[2]:
            self.commands[self.parameters[3]] = 1
        else:
            self.commands[self.parameters[3]] = 0
        self.instruction_ptr += 4

    def is_equal_to(self):
        self.get_parameters(3)
        if self.parameters[1] == self.parameters[2]:
            self.commands[self.parameters[3]] = 1
        else:
            
            self.commands[self.parameters[3]] = 0
        self.instruction_ptr += 4

    def adjust_relative_offset(self):
        self.get_parameters(1)
        self.relative_offset += self.parameters[1]
        self.instruction_ptr += 2

    def get_commands(self):
            with open("commands_ex_5.txt", "r") as file:
                self.commands = [int(line.strip()) for line in file]    # Hier werden die Commands aus der vorgegebenen txt datei in ein Liste aus integern ohne Zeilenumbruch umgewandelt 

    def run_computer(self):
        self.get_commands()
        trys = 0
        while trys < 2:
            try:
                self.game_mode = int(input("For Startscrenn press 1 , for Gameplay press 2"))
                break
            except ValueError:
                self.game_mode = 1
            
        if self.game_mode == 1:
            self.run_part1()
        elif self.game_mode == 2:
            self.run_part2()
        else:
            print("Dann halt nicht")
            exit
    
    def run_part1(self):
        while 1:
            self.opcode = self.commands[self.instruction_ptr] % 100
            if self.opcode == 99:
                print(f"Opcode ({self.opcode}) occured\n")
                print("Here's the Startscreen")

                tile_types = list(set(self.bildschirm.values()))  # hier wird aus allen tily Typen eine Liste erstellt
                str_to_int = {label: type for type, label in enumerate(tile_types)} # hier werden die verschiedenen Typen Zahlen zugeordent, damit der Computer damit etwas anfangen kann

                coordinates = list(self.bildschirm.keys())
                max_x = max(i[0] for i in coordinates)
                max_y = max(i[1] for i in coordinates)  
                grid = np.zeros((max_y + 1, max_x + 1)) # hier werden die maximalen x und y Werte gesucht, um die Maße für das Koordiatensystem zu bekommen

                for (x, y), tile_type in self.bildschirm.items():
                    grid[y, x] = str_to_int[tile_type]  # hier wird jedem Feld auf dem Koordnatensystem ein tile Typ zugeordnet
                plt.imshow(grid, cmap='viridis', interpolation='nearest')   # hier entsteht das Bild
                                                                            # in grid ist ein np array mit allen möglichen Koordnatenkombinationen gespeichert
                                                                            # und dem dazugehörigen tile Typ. cmap='virdis' ordnet den til Typen die Farben zu(color_map oben wird dabei aufgerufen)
                                                                            # 'virdis' ist Standart für dunkle blau-lila Töne 
                plt.title("Breakout")
                plt.show()
                break
            else:
                self.opcode = self.opcode % 10
            if self.opcode in self.opcode_map:
                self.opcode_map[self.opcode]()
            
            else:
                print(f"Undefined opcode ({self.opcode}) occured, that's blöd\n")
                print("We stop right here")
                break
        

    def run_part2(self):
        self.commands[0] = 2

        plt.ion()  #Öffnet das Fenster, lässt den Code im Hintergrund allerdings weiterlaufen
        self.fig, ax = plt.subplots() # hier wird das Fenster samt Koordinatensystem gebaut
        self.img_obj = ax.imshow(self.grid_array, cmap='nipy_spectral', vmin=0, vmax=4) # hier wird das Bild im Koordinatensystem gemacht. 
                                                                                        # mit vmin und vmax werden die Farben festgelegt auch, wenn der Ball mal außerhalb des Bildes ist und wieder zurückkommt
        self.keinBockmehr = False # Unsere Notbremse

        def on_close(event):
            self.keinBockmehr = True    # Wenn das Fenster geschlossen wird, wird die keinBockmehr Variable auf True gesetzt -> Der Code stoppt bei Prüfungen, ob du noch Bock hast
                                        # Vorteil der Code stoppt auch wenn das Fenster geschlossen wird und versucht nicht neue Fenster zu öffnen
            print("\nFenster wurde geschlossen. Stoppe Computer...")
        self.fig.canvas.mpl_connect('close_event', on_close)
        while 1: 
            if self.keinBockmehr:
                print("Schluss, Aus, Vorbei")
                break
            if self.instruction_ptr >= len(self.commands): 
                self.commands += [0] * 100
            self.opcode = self.commands[self.instruction_ptr] % 100
            
            if self.opcode == 99:
                print(f"GAME OVER. Final Score: {self.score}")
                plt.ioff() # Interaktiver Modus aus
                plt.show() # Damit das Fenster offen bleibt
                break
            
            if self.opcode in self.opcode_map:
                self.opcode_map[self.opcode]()
            else:
                break
        
my_Machine = simulated_computer()
my_Machine.run_computer()
