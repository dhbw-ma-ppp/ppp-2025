# Write a function that takes as input a list of integers and returns a single integer number.
# the numbers passed as argument form the working memory of a simulated computer.
# this computer will start by looking at the first value in the list passed to the function.
# this value will contain an `opcode`. Valid opcodes are 1, 2 or 99.
# Encountering any other value when you expect an opcode indicates an error in your coding.
# Meaning of opcodes:
#  1 indicates addition. If you encounter the opcode 1 you should read values from two positions 
#    of your working memory, add them, and store the result in a third position of your working memory.
#    The three numbers immediately after your opcode indicate the memory locations to read (first two values)
#    and write (third value) respectively. 
#    After executing the addition you should move to the next opcode by stepping forward 4 positions.
#  2 indicates multiplication. Otherwise the same rules apply as for opcode 1.
# 99 indicates halt. the program should stop after encountering the opcode 99.
# After the program stops, the function should return the value in the first location (address 0) 
# of your working memory.

# As an example, if the list of integers passed to your function is 
# [1, 0, 0, 0, 99] the 1 in the first position indicates you should read the values
# at position given by the second and third entries. Both of these indicate position 0, so you should read the value
# at position 0 twice. That value is 1. Adding 1 and 1 gives you two. You then look at the value in the fourth
# position, which is again 0, so you write the result to position 0. You then step forward by 4 steps, arriving at 99
# and ending the program. The final memory looks like [2, 0, 0, 0, 99]. Your function should return 2.

# Here's another testcase:
# [1, 1, 1, 4, 99, 5, 6, 0, 99] should become [30, 1, 1, 4, 2, 5, 6, 0, 99]
# Your function should return 30.


# print out which value is returned by your function for the following list:
commands = [1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 9, 19, 1, 5, 19, 23, 1, 6, 23, 27, 1, 27, 10, 31, 1, 31, 5, 35, 2, 10, 35, 39, 1, 9, 39, 43, 1, 43, 5, 47, 1, 47, 6, 51, 2, 51, 6, 55, 1, 13, 55, 59, 2, 6, 59, 63, 1, 63, 5, 67, 2, 10, 67, 71, 1, 9, 71, 75, 1, 75, 13, 79, 1, 10, 79, 83, 2, 83, 13, 87, 1, 87, 6, 91, 1, 5, 91, 95, 2, 95, 9, 99, 1, 5, 99, 103, 1, 103, 6, 107, 2, 107, 13, 111, 1, 111, 10, 115, 2, 10, 115, 119, 1, 9, 119, 123, 1, 123, 9, 127, 1, 13, 127, 131, 2, 10, 131, 135, 1, 135, 5, 139, 1, 2, 139, 143, 1, 143, 5, 0, 99, 2, 0, 14, 0]

def simple_virtual_machine(commands_list:list[int]):
    """
    This simple vitrual machine just takes a command list
    and does operation as described in the task
    it uses a idiomatic match case logic
    to choose which operation should be executed.
    """
    # The function_pointer is the index 
    # to the current instruction value in the command list
    function_pointer:int = 0
    # I use a var to store the length of the list
    # so that the while loop doesn't have to call
    # every cicle the len function
    length_of_commmand_list:int = len(commands_list)

    # runs as long there is no break command
    while (function_pointer < length_of_commmand_list):
        # Get the 2 values to operate on
        index_of_value_1:int    = commands_list[function_pointer+1]
        index_of_value_2:int   = commands_list[function_pointer+2]

        # get actual values
        value_1 = commands_list[index_of_value_1]
        value_2 = commands_list[index_of_value_2]
        
        # get the index for the mashine instruction
        indexToWrite:int            = commands_list[function_pointer+3]

        match commands_list[function_pointer]:
            # add numbers:
            case 1:
                commands_list[indexToWrite] = value_1 + value_2
            # multiply numbers:
            case 2:
                commands_list[indexToWrite] = value_1 * value_2
            # end programm
            case 99:
                return commands_list[0]
            # invalid command:
            case _:
                print(f"Error! opcode: {commands_list[function_pointer]} is not valid!")
                return None
            
        # increment the function pointer by 4 after the exectution of the command
        function_pointer += 4

    # Return None if the machine failed
    return None

def virtual_machine(data:list[int]) -> int:
    """
    The virtual machine takes a list of instruction and data
    and performs operation on it like it is described in the task.

    If the instruction value "data[func_ptr]" is "1"
    the machine will add v1 and v2
    and if the instruction value is "2" 
    the machine will multiply v1 and v2.

    This happens via a function lookup in the function field.
    Therefore, the instruction value gets transfomed into an index
    by subtracting 1.

    This approach may be slower with a small set of operators but
    it scales with a time complexity of O(1) very well with larger sets of operators.

    Example: 
    An array of if statements:
         if instruction == 1:
         elif instruction == 2:
         ...
         elif instruction == n: 
    has a time complexity of O(n) 
    because the computer has to iterate
    threw them until it found a true if statement.

    But the function lookup has a time complexity of O(1) 
    because its directly choosing the correct function by
    calculating its index position in the function_field!
    Its a direct look up.
    """
    func_ptr:int = 0
    
    
    # This list stores the instructions
    # its access time complexity is O(1) while n are the number of instructions
    # index 0 -> addition
    # index 1 -> multiplication
    function_field:list = [lambda a, b: a + b,
                           lambda a, b: a * b]
    
    # if an invalid operation occures 
    # the except block will get an 
    # IndexError (IndexErrors occure if you try to 
    # access a value which is not in the range of a list)
    try:
        while (data[func_ptr] != 99):
            # Get values to compute
            v1:int = data[data[func_ptr+1]]
            v2:int = data[data[func_ptr+2]]

            # The function index is the task value -1
            # For example:
            # if the task value is 1 (addition) the function index is 0 
            func_indx:int = data[func_ptr]-1
            # negative function indexes are not allowed!
            if func_indx < 0: raise IndexError

            # select function, execute function with the values v1 and v2 and store the value
            data[data[func_ptr + 3]] = function_field[func_indx](v1, v2)

            func_ptr += 4
        
        return data[0]
    except IndexError:
        error_message_start:str = f"Error: A wrong function index was tried to use!\nData: n{data}\nfunction pointer: {func_ptr}\n"
        try:
            raise IndexError(error_message_start + f"function index: {data[func_ptr]-1}")
        except IndexError:
            raise IndexError(error_message_start + f"In addition to this error, the index to the index of the function pointer is out of range!")

# I use commands.copy() to keep an unchanged list of commands 
# to be able to use it in the virtual_machine function again.
result_of_the_simple_virtual_machine:int = simple_virtual_machine(commands.copy())
print("Task 1: Virtual machine:\n")
print(f"    The result of the simple virtual machine is {result_of_the_simple_virtual_machine}!")

result_of_the_virtual_machine:int = virtual_machine(commands)
print(f"    The result of the virtual machine is {result_of_the_virtual_machine}!\n\n")

###########################################
# Write a function that takes an arbitrary number of unnamed arguments
# All inputs will be of type string.
# the function should return two lists:
#   The first list should contain all arguments which can be interpreted
#   as a number.
#   The second list should contain all strings which contain just one character.
# Think of some good inputs to test this functionality, write down at least three
# examples and verify that the output for these examples is correct.

print("Task 2: Write a function which sorts strings into numbers and not numbers:\n")

# I need the build in math library to use some "advanced" numbers
import math

def isStringCat(string:str): 
    """ This class is a very simple comparator
        just for demonstration purpose."""
    return string == "Cat"

def f(x:float):
    """
    My quadratic function.

    I named it f(x) to show the similarities 
    of mathematical functions and code functions. 
    """
    return x*x

def split_number_convertable_strings(*args:str):
    """
    Takes an arbriatry number of string arguments
    these strings get seperated into to different lists.

    Strings which are convertable into numbers are returned in the first list
    and the other strings are returned in the second list.
    """
    # the underscore of this inner function emphasizes
    # that it is a private function
    def _is_string_convertible_to_number(string:str) -> bool:
        """
        The function takes a string and checks 
        if the string is convertable 
        into a complex number
        and if the number is not (partly) nan or infinite.

        If this conversion is possible and
        the number is not nan or inifite it returns true
        else false.
        """
        try:
            # you have to use eval to transform strings 
            # into python code
            # Examples:
            # 1. complex("math.inf") -> error
            #    complex(eval("math.inf")) -> complex(math.inf) -> return true
            # 2. complex("0b0001") -> error
            #    complex(eval("0b0001")) -> complex(0b0001) -> return true
            # Additionally, you have to use the 
            # complex function instead of the float function
            # to cover complex numbers to
            
            num_value = complex(eval(string))

            ## Check if the calculated complex value is a special value which is not a number
            
            # check if parts of the number are NaN (Not a Number)
            # this check is neccessary because python is able
            # to "calculate" with "not a number" values... 
            number_is_not_nan       = not (math.isnan(num_value.real) or math.isnan(num_value.imag))
            number_is_finite        = math.isfinite(num_value.real) and math.isfinite(num_value.imag)
            return number_is_not_nan and number_is_finite
            
            # Explanation: Why I don't use a simple operator but a cast:
            # you can NOT use operators like
            # eval(string) + 1
            # because the return value of eval(string)
            # could be a class with an overloaded operator!
            # Thats why we have to use casts instead of operators
            # an example could be a vector or lists which adds numbers 
            # if "vector + number" is called
        except:
            return False
    
    numbers:list[str]       = []
    not_numbers:list[str]   = []
    for string in args:
        if _is_string_convertible_to_number(string):
            numbers += [string]
            # this line saves "letters" as not_numbers
            if (len(string) == 1):
                not_numbers += [string]
        else:
            not_numbers += [string]
    
    return numbers, not_numbers

# I wrote the arguments for the function in this way
# to make them more readable.
args:tuple[str] = (
    # This elements are - obviously - not numbers:
    "myString", 
    "One", 
    "return True",

    # Numbers in different formats:
    "42",        
    "0",       
    "1", 
    "-37",
    "0.0", 
    "0.5", 
    "1+1j",     # this is a complex number j is mathematically i
    "1e9",      # scientific notation
    "0x123",    # hex
    "0b1001010",# binary

    # special "numbers" and not numbers are from the math lib:
    "math.nan", # NotANumber
    "nan + 1j",
    "math.inf", # infinity is not a number
    "-math.inf",
    "complex(math.inf, math.nan)",

    # booleans are numbers:
    "True",
    "False",
    "'test' == 'test'",

    # its mathematically no problem to write instead of a number
    # a function with a parameter:
    # e.g. 4 = 2^2 = f(2) while f(x) = x*x
    "int(1)",
    "float(2)",
    "eval(hex(42))",
    "eval(bin(37))",
    "complex(1,-700)",

    "f(4)",
    "isStringCat('Cat')",
    "7**3",
    "7**0b001",

    # slowly its getting weird:
    "0x123**0b001+1j+(eval(\"'cat'=='cat'\"))+1e10",
    "4&1%0x7&0b0|13",
    "(x := 2) * x - 1 * math.e**(2*math.pi*math.cos(x))"
    )

numbers, not_numbers = split_number_convertable_strings(*args)

print("The following strings are not numbers:")
for string in not_numbers:
    print(f"\t   *\t{string}")
print("\n\n")



def ComplexNumberToNiceString(num:complex) -> str:
    """
    This function takes a complex number
    and returns a more readable string 
    representation of the number by
    canceling unnecessary zeros.
    """
    try:
        # check if the imagenary part of the number can be ignored
        if num.imag == 0:
            num:float = value.real
            if float.is_integer(num):
                num = int(num)
    except:
        pass
    return str(num)

print("The following strings are numbers:")

for string in numbers:
    value = complex(eval(string))
    
    print(f"{string:>45}  =>  {ComplexNumberToNiceString(value)}")
