"""Breakout (static display) using an Intcode computer and matplotlib.

This script implements a complete Intcode computer (with relative mode and
expanded memory) and runs the program in `data/breakout_commands.txt` until
halt. It collects output values in triplets (x, y, tile) and draws a static
screen using matplotlib, saving the image `breakout_static.png`.

Usage: run this file from the repository root:
	python Exercises/LaurensDegler/exercises_05.py

This implements PART 1 of the exercise: create a visual representation of the
static screen produced by the program.
"""

from __future__ import annotations

import os
from typing import List, Dict, Tuple

import matplotlib.pyplot as plt
# legend
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

