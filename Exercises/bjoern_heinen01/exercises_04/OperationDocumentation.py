### OPERATIONS ###

# ABC or CBA are the numbers before the opcode
# e.g. 12302 => C = 1, B = 2, A = 3, Op-Code = 1 or 01 (add)
# e.g. 0199 => C = 0, B = 0, A = 1, Op-Code = 99 (exit)
# A, B, C ∈ {0,1}

# Add
# CBA01
# accepts 3 params
# 1 is value1 in mode A
# 2 is value2 in mode B
# 3 is index to store in mode C
# TODO: store value1 + value2 at index

# Multiply
# CBA02
# accepts 3 params
# 1 is value1 in mode A
# 2 is value2 in mode B
# 3 is  index to store in mode C
# TODO: store value1 * value2 at index

# Input
# A03
# accepts one param
# 1 is index to store in mode A
# this function has a temp var which is set by an input()
# TODO: get input from consol and store it at index [input should be 5]

# Output
# A04
# accepts 1 param
# 1 is value in mode A
# TODO: print value 

# Jump if True
# BA05
# accepts 2 params
# 1 is condition in mode A
# 2 is new´_function_pointer in mode B
# TODO: set func_ptr to new_function_pointer if condition != 0

# Jump if False
# BA06
# accepts 2 params
# 1 is condition in mode A
# 2 is new´_function_pointer in mode B
# TODO: set func_ptr to new_function_pointer if condition == 0

# Less than
# CBA07
# accepts 3 params
# 1 is value1 in mode A
# 2 is value2 in mode B
# 3 is index in mode C
# TODO: if value1 < value2 store 1 at index else store 0 at index

# Equal
# CBA08
# accepts 3 params
# 1 is value1 in mode A
# 2 is value2 in mode B
# 3 is index in mode C
# TODO: if value1 == value2 store 1 at index else store 0 at index

# Exit
# 99
# accepts 0 params
# TODO: return all outputs