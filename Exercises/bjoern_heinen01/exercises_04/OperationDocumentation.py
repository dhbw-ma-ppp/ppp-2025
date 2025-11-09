### OPERATIONS ###

# ABC or CBA are the numbers before the opcode
# they represent the access mode of the argumetns
# A, B, C ∈ {0,1}
# Examples:
#   * 10102 => C = 1, B = 0, A = 1, Op-Code = 1 or 01 (add)
#   * 0199 => C = 0, B = 0, A = 1, Op-Code = 99 (exit)

# Add
# CBA01
# accepts 3 params
# 1 is value1 in mode A
# 2 is value2 in mode B
# 3 is index to store in mode C
# TODO: store value1 + value2 at index
# TODO: instruction index += 4

# Multiply
# CBA02
# accepts 3 params
# 1 is value1 in mode A
# 2 is value2 in mode B
# 3 is  index to store in mode C
# TODO: store value1 * value2 at index
# TODO: instruction index += 4

# Input
# A03
# accepts one param
# 1 is index to store in mode A
# this function has a temp var which is set by an input()
# TODO: get input from consol and store it at index [input should be 5]
# TODO: instruction index += 2

# Output
# A04
# accepts 1 param
# 1 is value in mode A
# TODO: print value 
# TODO: instruction index += 2

# Jump if True
# BA05
# accepts 2 params
# 1 is condition in mode A
# 2 is the new instruction index in mode B
# TODO: set set the instruction index to the new instruction index if condition != 0

# Jump if False
# BA06
# accepts 2 params
# 1 is condition in mode A
# 2 is the new instruction index in mode B
# TODO: set the instruction index to the new instruction index if condition == 0

# Less than
# CBA07
# accepts 3 params
# 1 is value1 in mode A
# 2 is value2 in mode B
# 3 is index in mode C
# TODO: if value1 < value2 store 1 at index else store 0 at index
# TODO: instruction index += 4

# Equal
# CBA08
# accepts 3 params
# 1 is value1 in mode A
# 2 is value2 in mode B
# 3 is index in mode C
# TODO: if value1 == value2 store 1 at index else store 0 at index
# TODO: instruction index += 4

# Exit
# 99
# accepts 0 params
# TODO: return all outputs
