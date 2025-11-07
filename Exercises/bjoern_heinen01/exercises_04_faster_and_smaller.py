# Extend the simulated computer from the second week:
# You will need to support a number of additional opcodes:
# - 3: read a single integer as input and save it to the position given
#      by its only parameter. the command 3,19 would read an input
#      and store the result at address 19
# - 4: output the value of the single parameter for this opcode.
#      for example 4,19 would output the value stored at address 19
# - 5: jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
# - 6: jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
# - 7: less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
# - 8: equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
#
# caution: since these opcodes expect a variable number of parameters the instruction pointer after executing an instruction should no longer always
# increase by four. Instead, it should increase  according to the number of parameters that instruction expects.
# If, however, the opcode directly manipulates the instruction pointer (5 and 6) there should be no additional modification of the instruction pointer.
# The next instruction to execute is stored directly at the location indicated by the parameter to these opcodes.
# caution: numbers in your storage, as well as inputs can be negative!
#
# Additionally, you need to support two different parameter modes: position mode (mode 0), and immediate mode (mode 1).
# Position mode: Opcode arguments are memory addresses. If an argument has the value 18 you fetch the 'calculation value'
#   from the memory at address 18. This is the mode you already know from last time.
# Immediate mode: In immediate mode a parameter is directly interpreted as a value. If the first argument to the 'sum' opcode is 8
#   then the first summand in your calculation is 8.
#
# Parameter modes are specified per-parameter as part of the opcode by extending the opcodes.
# When reading a number that specifies an opcode
#   - the two right-most digits contain the actual opcode
#   - any further digits contain the parameter mode of the parameters, reading digits from right-to-left
#     and parameters in-order from left to right. Any unspecified digits default to 0 (position mode).
#     NOTE: parameters for the target address of a write operation (e.g. the third parameter of the 'sum' or 'multiply' opcode)
#           are never given in immediate mode.
#
# Here's an example:
#   consider the sequence of instructions `1002,4,3,4,33`.
#   The two right-most digits of the first entry ('02') indicate the opcode: multiplication
#   Then, from right to left the next digit is '0', indicating that the first parameter is in position mode.
#   The next digit is '1' indicating the second parameter is in immediate mode.
#   The next digit is not present, defaulting to '0' so the third parameter is again in position mode.
#   No further parameter modes need to be determined as the multiply instruction accepts 3 parameters.
#   Reading the first parameter in position mode is the value at address '4' -- 33.
#   Reading the second parameter in immediate mode is the value '3'.
#   Executing the multiplication instruction gives us the result 33*3=99
#   The third parameter (4) in position mode assigns this value to the memory in location 4 (the location that used
#   to have value 33 is now 99).
#   Now moving the instruction pointer forward brings us to position 4 with opcode 99, halting the program.
#
# And here's some test cases:
#   3,9,8,9,10,9,4,9,99,-1,8 -- test whether the input is equal to 8 (using position mode)
#   3,3,1107,-1,8,3,4,3,99 -- test whether the input is less than 8 (using immediate mode)
#   3,3,1105,-1,9,1101,0,0,12,4,12,99,1 -- test whether the input is 0 using jump instructions
#
# Finally, run you code for the following instructions; when asked for input provide the number '5'. The program should print a single number when executed.
# Please take note of that number in your PR, so I don't need to run all the files myself :)
commands = [3,225,1,225,6,6,1100,1,238,225,104,0,1101,40,71,224,1001,224,-111,224,4,224,1002,223,8,223,101,7,224,224,1,224,223,223,1102,66,6,225,1102,22,54,225,1,65,35,224,1001,224,-86,224,4,224,102,8,223,223,101,6,224,224,1,224,223,223,1102,20,80,225,101,92,148,224,101,-162,224,224,4,224,1002,223,8,223,101,5,224,224,1,224,223,223,1102,63,60,225,1101,32,48,225,2,173,95,224,1001,224,-448,224,4,224,102,8,223,223,1001,224,4,224,1,224,223,223,1001,91,16,224,101,-79,224,224,4,224,1002,223,8,223,101,3,224,224,1,224,223,223,1101,13,29,225,1101,71,70,225,1002,39,56,224,1001,224,-1232,224,4,224,102,8,223,223,101,4,224,224,1,223,224,223,1101,14,59,225,102,38,143,224,1001,224,-494,224,4,224,102,8,223,223,101,3,224,224,1,224,223,223,1102,30,28,224,1001,224,-840,224,4,224,1002,223,8,223,101,4,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,107,677,226,224,1002,223,2,223,1005,224,329,1001,223,1,223,8,226,226,224,102,2,223,223,1006,224,344,101,1,223,223,7,226,677,224,1002,223,2,223,1005,224,359,101,1,223,223,1007,677,226,224,1002,223,2,223,1005,224,374,1001,223,1,223,1007,677,677,224,1002,223,2,223,1006,224,389,101,1,223,223,1008,226,226,224,1002,223,2,223,1005,224,404,1001,223,1,223,108,677,226,224,1002,223,2,223,1006,224,419,1001,223,1,223,1108,677,226,224,102,2,223,223,1006,224,434,1001,223,1,223,108,226,226,224,1002,223,2,223,1005,224,449,101,1,223,223,7,677,677,224,1002,223,2,223,1006,224,464,1001,223,1,223,8,226,677,224,1002,223,2,223,1005,224,479,1001,223,1,223,107,226,226,224,102,2,223,223,1006,224,494,101,1,223,223,1007,226,226,224,1002,223,2,223,1005,224,509,1001,223,1,223,1107,226,677,224,102,2,223,223,1005,224,524,1001,223,1,223,108,677,677,224,1002,223,2,223,1005,224,539,101,1,223,223,1107,677,226,224,102,2,223,223,1005,224,554,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,569,101,1,223,223,8,677,226,224,102,2,223,223,1005,224,584,1001,223,1,223,7,677,226,224,102,2,223,223,1006,224,599,101,1,223,223,1008,677,677,224,1002,223,2,223,1005,224,614,101,1,223,223,1008,677,226,224,102,2,223,223,1006,224,629,1001,223,1,223,1108,677,677,224,102,2,223,223,1006,224,644,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,659,1001,223,1,223,1107,226,226,224,102,2,223,223,1006,224,674,1001,223,1,223,4,223,99,226]
import time

def calc_virtual_machine(commands:list[int], use_auto_input:bool=False, auto_input:int=None, should_print:bool = False) -> list[int]:

    ### DEFINE ALL OPERATIONS ###

    def op_add(commands:list[int], instr_index:int, v1_index:int, v2_index:int, store_at_index:int):
        commands[store_at_index] = commands[v1_index] + commands[v2_index]
        return instr_index + 4

    def op_multiplication(commands:list[int], instr_index:int, v1_index:int, v2_index:int, store_at_index:int):
        commands[store_at_index] = commands[v1_index] * commands[v2_index]
        return instr_index + 4
    
    if use_auto_input:
        def op_input(commands:list[int], instr_index:int, store_at_index:int):
            commands[store_at_index] = auto_input
            return instr_index + 2
    else:
        def op_input(commands:list[int], instr_index:int, store_at_index:int):
            commands[store_at_index] = input(" -> ")
            return instr_index + 2
    
    if should_print:
        def op_output(commands:list[int], instr_index:int, value_index):
            nonlocal prints
            prints += [commands[value_index]]
            print(commands[value_index])
            return instr_index + 2
        
    else:
        def op_output(commands:list[int], instr_index:int, value_index):
            nonlocal prints
            prints += [commands[value_index]]
            return instr_index + 2

    def op_jump_if_true(commands:list[int], instr_index:int, condition_value_index:int, index_to_new_instr_index:int):
        if commands[condition_value_index] != 0:
            return commands[index_to_new_instr_index]
        return instr_index + 3
        
    def op_jump_if_false(commands:list[int], instr_index:int, condition_value_index:int, index_to_new_instr_index:int):
        if commands[condition_value_index] == 0:
            return commands[index_to_new_instr_index]
        return instr_index + 3
    
    def op_less_than(commands:list[int], instr_index:int, v1_index:int, v2_index:int, store_at_index:int):
        commands[store_at_index] = int(commands[v1_index] < commands[v2_index])
        return instr_index + 4
    
    def op_equal(commands:list[int], instr_index:int, v1_index:int, v2_index:int, store_at_index:int):
        commands[store_at_index] = int(commands[v1_index] == commands[v2_index])
        return instr_index + 4
    
    def op_exit(commands:list, instr_index:int):
        nonlocal dont_stop_calculation
        dont_stop_calculation = False
    
    ### (END) DEFINE ALL OPERATIONS ###

    operations = {
        "1"  : (op_add, 3),
        "2"  : (op_multiplication, 3),
        "3"  : (op_input, 1),
        "4"  : (op_output, 1),
        "5"  : (op_jump_if_true, 2),
        "6"  : (op_jump_if_false, 2),
        "7"  : (op_less_than, 3),
        "8"  : (op_equal, 3),
        "99" : (op_exit, 0)
    }

    def get_opp_and_arg_indexes(operations:list[int], args_start_index:int, op_value:str) -> tuple[function, list[int]]:
        # get opp_code
        op_code = op_value[-2:]
        if op_code[0] == "0":
            op_code = op_code[-1]
        
        # fetch
        opp_func, op_args_count = operations[op_code]
        args_indexes = [None] * op_args_count

        for arg_index_in_args in range(op_args_count):
            reversed_op_arg_index = 3 + arg_index_in_args
            is_immidiate_mode = reversed_op_arg_index <= len(op_value) and op_value[-reversed_op_arg_index] == "1"
            if is_immidiate_mode:
                args_indexes[arg_index_in_args] = args_start_index+arg_index_in_args
            else:
                args_indexes[arg_index_in_args] = commands[args_start_index+arg_index_in_args]
        
        return opp_func, args_indexes
    
    # Define local variables:
    instr_index = 0
    
    prints = []

    dont_stop_calculation = True

    # Calculate:

    while dont_stop_calculation:
        op_value = str(commands[instr_index])

        opp_func, op_arg_indexes = get_opp_and_arg_indexes(operations, instr_index+1, op_value)
        
        instr_index = opp_func(commands, instr_index, *op_arg_indexes)
    
    return prints

# UNIT TESTS:
assert calc_virtual_machine([1002,4,3,4,33], should_print=False) == []

assert calc_virtual_machine([3,9,8,9,10,9,4,9,99,-1,8], use_auto_input=True, auto_input=8) == [1]
assert calc_virtual_machine([3,9,8,9,10,9,4,9,99,-1,8], use_auto_input=True, auto_input=-1, should_print=False) == [0]

assert calc_virtual_machine([3,3,1107,-1,8,3,4,3,99], use_auto_input=True, auto_input=7, should_print=False) == [1]
assert calc_virtual_machine([3,3,1107,-1,8,3,4,3,99], use_auto_input=True, auto_input=8, should_print=False) == [0]

assert calc_virtual_machine([3,3,1105,-1,9,1101,0,0,12,4,12,99,1 ], use_auto_input=True, auto_input=0, should_print=False) == [0]
assert calc_virtual_machine([3,3,1105,-1,9,1101,0,0,12,4,12,99,1 ], use_auto_input=True, auto_input=-1, should_print=False) == [1]

assert calc_virtual_machine(commands.copy(), use_auto_input=True, auto_input=5, should_print=False) == [16694270]

# Performance test:

n = 1000

start = time.time()
for i in range(n):
    result= calc_virtual_machine(commands.copy(), use_auto_input=True, auto_input=5)
end = time.time()

print(f"The calculation took: {(end-start)* 10**6 /n } μs")
print(f"The result of the virtual function calculation is {result[0]}.")

# Result 16694270
# Time: ~114 μs
# this function is round about 5% faster!!!

