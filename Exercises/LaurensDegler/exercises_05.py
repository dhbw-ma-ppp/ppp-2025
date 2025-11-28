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

from __future__ import annotations

import os
from typing import List, Dict, Tuple

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
import numpy as np



class IntcodeComputer:
	"""A simple Intcode computer with support for large memory and relative mode."""

	def __init__(self, program: List[int], inputs: List[int] = None):
		# copy program into expandable memory
		self.mem = list(program)
		self.ip = 0
		self.relative_base = 0
		self.inputs = inputs or []
		self.outputs: List[int] = []
		self.halted = False

	def _ensure(self, addr: int) -> None:
		if addr >= len(self.mem):
			self.mem.extend([0] * (addr + 1 - len(self.mem)))

	def _read(self, addr: int) -> int:
		self._ensure(addr)
		return self.mem[addr]

	def _write(self, addr: int, value: int) -> None:
		self._ensure(addr)
		self.mem[addr] = value

	def _get_param(self, offset: int, mode: int) -> int:
		val = self._read(self.ip + offset)
		if mode == 0:  # position
			return self._read(val)
		if mode == 1:  # immediate
			return val
		if mode == 2:  # relative
			return self._read(self.relative_base + val)
		raise ValueError(f"Unknown parameter mode: {mode}")

	def _get_write_addr(self, offset: int, mode: int) -> int:
		val = self._read(self.ip + offset)
		if mode == 0:
			return val
		if mode == 2:
			return self.relative_base + val
		raise ValueError("Invalid mode for write parameter: only 0 or 2 allowed")

	def add_input(self, value: int) -> None:
		self.inputs.append(value)

	def run(self, pause_on_output: bool = False, pause_on_input: bool = False) -> List[int]:
		"""Run until halt (or until output is produced when pause_on_output=True).

		Returns list of outputs produced since last call.
		"""
		out_start = len(self.outputs)
		while True:
			instr = self._read(self.ip)
			op = instr % 100
			modes = [(instr // 10 ** i) % 10 for i in range(2, 5)]

			if op == 1:  # add
				a = self._get_param(1, modes[0])
				b = self._get_param(2, modes[1])
				addr = self._get_write_addr(3, modes[2])
				self._write(addr, a + b)
				self.ip += 4
			elif op == 2:  # mul
				a = self._get_param(1, modes[0])
				b = self._get_param(2, modes[1])
				addr = self._get_write_addr(3, modes[2])
				self._write(addr, a * b)
				self.ip += 4
			elif op == 3:  # input
				if not self.inputs:
					if pause_on_input:
						return self.outputs[out_start:]
					raise RuntimeError("Input requested but no input available")
				addr = self._get_write_addr(1, modes[0])
				val = self.inputs.pop(0)
				self._write(addr, val)
				self.ip += 2
			elif op == 4:  # output
				val = self._get_param(1, modes[0])
				self.outputs.append(val)
				self.ip += 2
				if pause_on_output:
					return self.outputs[out_start:]
			elif op == 5:  # jump-if-true
				if self._get_param(1, modes[0]) != 0:
					self.ip = self._get_param(2, modes[1])
				else:
					self.ip += 3
			elif op == 6:  # jump-if-false
				if self._get_param(1, modes[0]) == 0:
					self.ip = self._get_param(2, modes[1])
				else:
					self.ip += 3
			elif op == 7:  # less than
				a = self._get_param(1, modes[0])
				b = self._get_param(2, modes[1])
				addr = self._get_write_addr(3, modes[2])
				self._write(addr, 1 if a < b else 0)
				self.ip += 4
			elif op == 8:  # equals
				a = self._get_param(1, modes[0])
				b = self._get_param(2, modes[1])
				addr = self._get_write_addr(3, modes[2])
				self._write(addr, 1 if a == b else 0)
				self.ip += 4
			elif op == 9:  # adjust relative base
				self.relative_base += self._get_param(1, modes[0])
				self.ip += 2
			elif op == 99:
				self.halted = True
				return self.outputs[out_start:]
			else:
				raise RuntimeError(f"Unknown opcode {op} at ip={self.ip}")


def load_program(path: str) -> List[int]:
	with open(path, "r", encoding="utf-8") as f:
		data = f.read().strip()
	# commands may be a single comma-separated line
	parts = [p for p in data.replace('\n', ',').split(',') if p != ""]
	return [int(x) for x in parts]


def draw_static_screen(program_path: str, out_image: str = "breakout_static.png") -> Tuple[str, Dict[Tuple[int, int], int]]:
	program = load_program(program_path)
	comp = IntcodeComputer(program)
	# run until halt
	comp.run()
	outputs = comp.outputs

	# collect triplets
	tiles: Dict[Tuple[int, int], int] = {}
	score = 0
	for i in range(0, len(outputs), 3):
		try:
			x, y, t = outputs[i], outputs[i + 1], outputs[i + 2]
		except IndexError:
			break
		if x == -1 and y == 0:
			score = t
		else:
			tiles[(x, y)] = t

	if not tiles:
		raise RuntimeError("No tiles were drawn by the program")

	xs = [p[0] for p in tiles.keys()]
	ys = [p[1] for p in tiles.keys()]
	min_x, max_x = min(xs), max(xs)
	min_y, max_y = min(ys), max(ys)

	width = max_x - min_x + 1
	height = max_y - min_y + 1

	grid = np.zeros((height, width), dtype=int)
	for (x, y), t in tiles.items():
		grid[y - min_y, x - min_x] = t

	# draw with matplotlib
	cmap_colors = ["black", "#777777", "gold", "dodgerblue", "red"]
	

	cmap = ListedColormap(cmap_colors)

	fig, ax = plt.subplots(figsize=(max(6, width / 8), max(4, height / 8)))
	# show origin at top-left similar to screen coordinates (y increases downward in many displays)
	ax.imshow(grid, cmap=cmap, origin="lower", interpolation="nearest")
	ax.set_title(f"Breakout static screen — blocks: {sum(1 for v in tiles.values() if v == 2)} — score: {score}")
	ax.set_xticks([])
	ax.set_yticks([])

	patch_labels = ["empty", "wall", "block", "paddle", "ball"]
	patches = [mpatches.Patch(color=cmap_colors[i], label=f"{i}: {patch_labels[i]}") for i in range(len(patch_labels))]
	ax.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc="upper left")

	plt.tight_layout()
	plt.savefig(out_image, dpi=200)
	print(f"Saved static breakout image to {out_image}")
	print(f"Screen size: {width}x{height}; blocks: {sum(1 for v in tiles.values() if v == 2)}; score: {score}")
	return out_image, tiles


def play_game(program_path: str, out_image: str = "breakout_play.png", save_frames: bool = False) -> Tuple[int, Dict[Tuple[int, int], int]]:
	"""Run the game (memory[0]=2) with an automatic joystick and return final score.

	The joystick strategy is simple: move = sign(ball_x - paddle_x).
	If save_frames is True, the final state image will be saved as out_image.
	"""
	program = load_program(program_path)
	# set memory address 0 to 2 to play for free
	if program:
		program[0] = 2

	comp = IntcodeComputer(program)

	tiles: Dict[Tuple[int, int], int] = {}
	score = 0
	ball_x = 0
	paddle_x = 0

	# run until halt
	while not comp.halted:
		# run until input requested (or halt)
		outputs = comp.run(pause_on_output=False, pause_on_input=True)

		# process outputs in triplets
		for i in range(0, len(outputs), 3):
			try:
				x, y, t = outputs[i], outputs[i + 1], outputs[i + 2]
			except IndexError:
				break
			if x == -1 and y == 0:
				score = t
			else:
				tiles[(x, y)] = t
				if t == 4:
					ball_x = x
				if t == 3:
					paddle_x = x

		if comp.halted:
			break

		# decide joystick input: -1 left, 0 neutral, 1 right
		move = 0
		if ball_x < paddle_x:
			move = -1
		elif ball_x > paddle_x:
			move = 1
		comp.add_input(move)

	# optionally save final screen
	if tiles:
		xs = [p[0] for p in tiles.keys()]
		ys = [p[1] for p in tiles.keys()]
		min_x, max_x = min(xs), max(xs)
		min_y, max_y = min(ys), max(ys)
		width = max_x - min_x + 1
		height = max_y - min_y + 1
		grid = np.zeros((height, width), dtype=int)
		for (x, y), t in tiles.items():
			grid[y - min_y, x - min_x] = t

		cmap_colors = ["black", "#777777", "gold", "dodgerblue", "red"]
		from matplotlib.colors import ListedColormap
		cmap = ListedColormap(cmap_colors)
		fig, ax = plt.subplots(figsize=(max(6, width / 8), max(4, height / 8)))
		ax.imshow(grid, cmap=cmap, origin="lower", interpolation="nearest")
		ax.set_title(f"Breakout final screen — blocks: {sum(1 for v in tiles.values() if v == 2)} — score: {score}")
		ax.set_xticks([])
		ax.set_yticks([])
		import matplotlib.patches as mpatches
		patch_labels = ["empty", "wall", "block", "paddle", "ball"]
		patches = [mpatches.Patch(color=cmap_colors[i], label=f"{i}: {patch_labels[i]}") for i in range(len(patch_labels))]
		ax.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc="upper left")
		plt.tight_layout()
		plt.savefig(out_image, dpi=200)
		print(f"Saved final play image to {out_image}")

	print(f"Game finished. Final score: {score}; remaining blocks: {sum(1 for v in tiles.values() if v == 2)}")
	return score, tiles


if __name__ == "__main__":
	repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
	data_path = os.path.join(repo_root, "data", "breakout_commands.txt")
	out_img = os.path.join(os.path.dirname(__file__), "breakout_static.png")
	draw_static_screen(data_path, out_img)
	# run part 2: play the game automatically and save final image
	play_img = os.path.join(os.path.dirname(__file__), "breakout_play.png")
	play_game(data_path, play_img)

