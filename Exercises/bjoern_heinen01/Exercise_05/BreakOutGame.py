from reference_int_computer import IntComputer
from pathlib import Path
from math import inf

import tkinter as tk
import time

class BreakOutGameUI():
    class BlockTypes:
        empty = 0
        border = 1
        enemy = 2
        player = 3
        ball = 4

        class GetColor:
            @staticmethod
            def empty(relative_x:float, relative_y:float):
                return 0, 64 + int(relative_x*128), 64 + int(relative_y*128)
            
            @staticmethod
            def border(relative_x:float, relative_y:float):
                r, g, b = BreakOutGameUI.BlockTypes.GetColor.empty(relative_x, relative_y)
                return r+32, g+32, b+32
            
            @staticmethod
            def enemy(relative_x:float, relative_y:float):
                color = -int(((1-relative_x)+relative_y)*32) + 192
                return color, color, color
            
            @staticmethod
            def player(relative_x:float, relative_y:float):
                color = int(relative_x*128)+64
                return color, color, color
            
            @staticmethod
            def ball(relative_x:float, relative_y:float):
                color = 128-int(relative_x*128)
                return color//2+64, color//2+64, color+128
        
        type_to_color = {
            empty: GetColor.empty,
            border: GetColor.border,
            enemy: GetColor.enemy,
            player: GetColor.player,
            ball: GetColor.ball
        }
    
    def __key_down(self, event):
        self.__last_key_input = event.keysym

    def __init__(self, auto_play = True, target_frame_rate = inf):
        text_margin = 4
        text_height = 10

        self.__pixel_size = 20

        ## set up window
        self.__root = tk.Tk()
        self.__root.title("Break Out! The Game")

        width  = 43*self.__pixel_size
        height = 23*self.__pixel_size+text_height+text_margin*2
        self.__canvas = tk.Canvas(self.__root, width=width, height=height)
        self.__canvas.pack()

        # maps the coords (x,y) with the canvas element id
        self.__coord_to_elment_id:dict = { }
        self.__input_buffer:list[int] = []

        self.__auto_play = auto_play
        self.__last_key_input = None

        # the function self.key_down is called every time a key is hit
        self.__root.bind("<KeyPress>", self.__key_down)

        # time data
        self.__last_frame_time = time.monotonic()
        self.__target_frame_rate = target_frame_rate

        self.__ball_x_pos = None
        self.__player_x_pos = None

        self._current_score = 0

        self.__score_element_id = self.__canvas.create_text(text_margin, height-text_height-text_margin, anchor="nw", text=f"Score: {self._current_score}", fill="black")
    
    def __slow_frame_time_down_to_target_fps(self):
        delta_time = time.monotonic() - self.__last_frame_time
        time_to_sleep = 1 / self.__target_frame_rate - delta_time

        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

        self.__last_frame_time = time.monotonic()

    @staticmethod
    def __normalize(n:int):
        if n:
            return n // abs(n)
        return 0
    
    def out_put(self):
        self.__slow_frame_time_down_to_target_fps()
        
        self.__canvas.update()

        if self.__auto_play:
            return self.__normalize(self.__ball_x_pos - self.__player_x_pos)
            
        else:
            while True:
                self.__root.update()
                match self.__last_key_input:
                    case "a":
                        self.__last_key_input = None
                        return -1
                    case "s":
                        self.__last_key_input = None
                        return 0
                    case "d":
                        self.__last_key_input = None
                        return 1

    def input(self, new_value):
        self.__input_buffer += [new_value]

        if len(self.__input_buffer) != 3:
            return

        if self.__input_buffer[0] == -1:
            self._set_score(self.__input_buffer[2])
        else:
            self._set_pixel(*self.__input_buffer)

        self.__input_buffer.clear()


    def _set_score(self, score):
        self._current_score = score
        self.__canvas.itemconfigure(self.__score_element_id, text=f"Score: {score}")

    def _set_pixel(self, x_input, y_input, pixel_type):
        # scale coords to window coords
        x_scaled = x_input * self.__pixel_size
        y_scaled = y_input * self.__pixel_size

        # get color
        r, g, b = BreakOutGameUI.BlockTypes.type_to_color[pixel_type](x_input/43, y_input/23)
        color = f'#{r:02x}{g:02x}{b:02x}'
        
        # destroy pixel if it exists
        if (x_input, y_input) in self.__coord_to_elment_id:
            self.__canvas.delete(self.__coord_to_elment_id.pop((x_input, y_input)))
        
        # create actual "pixel"/rectangle
        id = self.__canvas.create_rectangle(x_scaled, y_scaled, x_scaled + self.__pixel_size, y_scaled + self.__pixel_size, fill=color, width=0)
        self.__coord_to_elment_id[(x_input, y_input)] = id

        # update position data
        match pixel_type:
            case BreakOutGameUI.BlockTypes.player:
                self.__player_x_pos = x_input
            case BreakOutGameUI.BlockTypes.ball:
                self.__ball_x_pos = x_input

if __name__ == "__main__":
    with open(Path("./data/breakout_commands.txt").absolute(), "r") as file:
        memory = [int(line) for line in file.readlines()]

    myGameInstance = BreakOutGameUI(auto_play=True, target_frame_rate=12)  
    ic = IntComputer(myGameInstance.out_put, myGameInstance.input)

    # Part one:
    # ic.run(memory)

    # Part two:
    memory[0] = 2
    ic.run(memory)

    print(f"Your score was {myGameInstance._current_score}!!!")
    # the high schore is 17159