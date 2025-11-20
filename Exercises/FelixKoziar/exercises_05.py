from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
# Load breakout commands
breakout_commands_list = []

script_dir = Path(__file__).parent
file_path = script_dir / 'breakout_commands.txt'

with open(file_path) as file:
    for line in file:
        stripped_line = line.strip()
        if stripped_line:
            try:
                breakout_commands_list.append(int(stripped_line))
            except ValueError:
                print(f"Warning: Skipping invalid integer line: '{stripped_line}'")


class IntComputer:
    
    def __init__(self, program):
        # Convert list to dictionary for unlimited memory
        self.memory = {i: v for i, v in enumerate(program)}
        self.ip = 0  # instruction pointer
        self.relative_offset = 0  # for relative mode (mode 2)
        self.output_list = []
        
        # Opcode mapping: opcode -> (function, num_parameters)
        self.opcode_info = {
            1: (self.add, 3),
            2: (self.multiply, 3),
            3: (self.read_input, 1),
            4: (self.write_output, 1),
            5: (self.jump_if_true, 2),
            6: (self.jump_if_false, 2),
            7: (self.less_than, 3),
            8: (self.equals, 3),
            9: (self.adjust_offset, 1)
        }
    
    # ==================== OPCODE IMPLEMENTATIONS ====================
    
    def add(self, parameters):
        self.memory[parameters[2]] = parameters[0] + parameters[1]
    
    def multiply(self, parameters):
        self.memory[parameters[2]] = parameters[0] * parameters[1]
    
    def read_input(self, parameters):
        user_input = int(input('Enter your Input: '))
        self.memory[parameters[0]] = user_input
    
    def write_output(self, parameters):
        self.output_list.append(parameters[0])
    
    def jump_if_true(self, parameters):
        if parameters[0] != 0:
            return parameters[1]  # new instruction pointer
        return None
    
    def jump_if_false(self, parameters):
        if parameters[0] == 0:
            return parameters[1]  # new instruction pointer
        return None
    
    def less_than(self, parameters):
        self.memory[parameters[2]] = 1 if parameters[0] < parameters[1] else 0
    
    def equals(self, parameters):
        self.memory[parameters[2]] = 1 if parameters[0] == parameters[1] else 0
    
    def adjust_offset(self, parameters):
        self.relative_offset += parameters[0]
    
    # ==================== HELPER METHODS ====================
    
    def get_opcode(self, instruction):
        return instruction % 100
    
    def get_modes(self, instruction):
        modes = []
        instruction //= 100  # remove opcode part
        while instruction > 0:
            modes.append(instruction % 10)
            instruction //= 10
        return modes
    
    def get_parameters(self, num_parameters, modes, opcode):
        parameters = []
        write_opcodes = {1, 2, 3, 7, 8}  # opcodes with write parameters (NOT 9!)
        
        for i in range(num_parameters):
            parameter_address = self.ip + i + 1
            mode = modes[i] if i < len(modes) else 0  # default to position mode
            
            # The last parameter for write_opcodes is a write address
            is_write_parameter = (opcode in write_opcodes) and (i == num_parameters - 1)
            
            if is_write_parameter:
                # Write parameter: return the address (adjusted for mode)
                if mode == 0:  # position mode
                    parameters.append(self.memory.get(parameter_address, 0))
                elif mode == 2:  # relative mode
                    parameters.append(self.memory.get(parameter_address, 0) + self.relative_offset)
            else:
                # Read parameter: return the value
                if mode == 0:  # position mode
                    address = self.memory.get(parameter_address, 0)
                    parameters.append(self.memory.get(address, 0))
                elif mode == 1:  # immediate mode
                    parameters.append(self.memory.get(parameter_address, 0))
                elif mode == 2:  # relative mode
                    address = self.memory.get(parameter_address, 0) + self.relative_offset
                    parameters.append(self.memory.get(address, 0))
        
        return parameters
    
    # ==================== MAIN EXECUTION ====================
    
    def run(self):
        while True:
            opcode = self.get_opcode(self.memory.get(self.ip, 0))
            
            if opcode == 99:  # halt
                break
            
            if opcode not in self.opcode_info:
                raise ValueError(f"Unknown opcode {opcode} at position {self.ip}")
            
            # Get instruction details
            modes = self.get_modes(self.memory.get(self.ip, 0))
            function, num_parameters = self.opcode_info[opcode]
            
            # Resolve parameters
            resolved_parameters = self.get_parameters(num_parameters, modes, opcode)
            
            # Execute instruction
            result = function(resolved_parameters)
            
            # Update instruction pointer
            if result is not None:  # jump instructions return new IP
                self.ip = result
            else:
                self.ip += num_parameters + 1


# ==================== RUN THE PROGRAM ====================

computer = IntComputer(breakout_commands_list)
computer.run()
vm_output = computer.output_list
print(vm_output)
print('\n')

data_x = []
data_y = []
tile_type = []
colors = []
i = 0
while i < len(vm_output):
    data_x.append(vm_output[i])
    data_y.append(vm_output[i+1])
    tile_type.append(vm_output[i+2])
    i += 3
j = 0
while j < len(tile_type):
    if tile_type[j] == 0:
        colors.append("black")
    elif tile_type[j] == 1:
        colors.append("red")
    elif tile_type[j] == 2:
        colors.append("green")
    elif tile_type[j] == 3:
        colors.append("blue")
    elif tile_type[j] == 4:
        colors.append("pink")
    j += 1
print(data_x)
print('\n')
print(data_y)
print('\n')
print(tile_type)
print('\n')


plt.scatter(data_x, data_y, c = colors, marker = "s", s=60)
plt.title("breakout - the arcade game")
plt.xlabel("x-axis")
plt.ylabel("y-axis")
plt.show()