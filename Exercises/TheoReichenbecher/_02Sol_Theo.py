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

#test-input
test = [1, 1, 1, 4, 99, 5, 6, 0, 99]

def virtual_machine (input_list) -> int:

    #startindex/ laufindex
    i= 0
    
    while input_list[i] != 99:

        # next indixes point to the numbers for the calculation
        index_next = input_list[i+1]
        index_nextnext= input_list[i+2]

        #values at the indexes
        val_1 = input_list[index_next]
        val_2 = input_list[index_nextnext]

        # pointer.val() decides the calculation
        match input_list[i]:
            case 1:
                addition = val_1 + val_2
                res = "a"
            case 2:
                multiplikation = val_1 * val_2
                res = "m"
            case _: 
                print("'c' ist weder 1 noch 2 noch 99")
                break
        
        #Insertion point
        insert_point = input_list[i+3]

        #Insertion 
        if res == "a":
            input_list[insert_point] = addition 
        else:
            input_list[insert_point] = multiplikation
        

        i += 4 

    
    return input_list[0]

print("_____Lösung der virtuellen Machine_____")
print("99 wurde gefunden. Das erste Element, commands[0] ist:")
#Funktion call
print(virtual_machine(commands))
print("\n\n")


###########################################
# Write a function that takes an arbitrary number of unnamed arguments
# All inputs will be of type string.
# the function should return two lists:
#   The first list should contain all arguments which can be interpreted
#   as a number.
#   The second list should contain all strings which contain just one character.
# Think of some good inputs to test this functionality, write down at least three
# examples and verify that the output for these examples is correct.

import math

def sort_into_categories(*args):
    one_charakter_arguments= []

    string_index = 0

    while string_index < len(args):
        # checks if the length of the current argument is 1 
        # ==> if truthy fill the one_charakter_argument list
        if len(args[string_index]) == 1:
            one_charakter_arguments.append(args[string_index])

        string_index += 1

    number_argument= check_for_number(*args)
    print("_____Lösung der zweiten Aufgabe_____")
    print("The following elements are just one charakter")
    i = 0
    while i < len(one_charakter_arguments):
        print(f"--> {one_charakter_arguments[i]}")
        i += 1
    print("\n")
    print("The following integers can be interpretet as integers")
    i = 0
    while i < len(number_argument):
        print(f"--> {number_argument[i]}")
        i += 1

# Das bricht -- sucht nach Zahlen, wir suchen aber eine Möglichkeit Strings nach Zahlen auszulesen
# hex or binary integers are casted to an integer 
def check_for_number(*args):
    number_argument= []
    for num in args:
        
        # inbuild funktion checks if string is convertable to a int_like objekt
        try:
            num = eval(num)
        except:
            pass

        # 1. checks for intgers
        if isinstance(num, (int, float, complex)):
            number_argument.append(num)

        # 2. checks for bools (True/False) + for comparative expressions (bool → int)
        elif isinstance(num, bool):
            number_argument.append(num)

        # 3. checks for special numbers from the math lib
        elif num in [math.inf, -math.inf, math.nan]:
            number_argument.append(num)

        # 4. Enum or  objectives mit .value
        elif hasattr(num, "value"):
            return check_for_number(args.value)
    return number_argument
            



#testcases
test1 = ("hello", "True", "18", "a", "hkjhraifu", "7", "?", "gg")

test2_number_types = (
    "3",                       # int + single char
    "42",                      # int – Ganzzahl
    "-123",                    # int - negative Ganzzahl
    "3.1415",                  # float – Gleitkommazahl
    "2 + 3j",                  # complex – Komplexe Zahl
    "0b101",                  # binary
    "0x101",                  #Hex --> 257 in oct
    "True",                   # bool – Wahrheitswert (intern als 1 gespeichert)
    "math.inf",               # positive Unendlichkeit
    "-math.inf",              # negative Unendlichkeit
    "math.nan",               # NaN – Not a Number
    "math.e",                 # Eulersche Zahl (~2.718)
    "math.pi",                # Kreiszahl Pi (~3.1415)
    "math.tau",               # Tau = 2π (~6.2831)
    "math.sqrt(2)",           # Quadratwurzel von 2
    "math.log10(1000)",       # Logarithmus zur Basis 10
    "math.exp(1)",            # Exponentialfunktion e^1
    "math.isqrt(16)",         # Ganzzahlige Wurzel (int)
    "round(3.1415, 2)",       # Gerundete float-Zahl
    'float("1e-300")',        # Sehr kleine float-Zahl
    'float("1e+300")',        # Sehr große float-Zahl
    'complex(math.pi, math.e)', # Komplexe Zahl mit Pi und e
    'True == 1',              # → True
    'False == 0',              # → True
    'int(True)',               # → 1
    'int(False)',              # → 0
    '2 == 2',                  # → True → 1
    '3 > 5',                   # → False → 0
    "hello",                   # no integer
)

test3 =("hello", "ich", "bin")

#funktioncall
sort_into_categories(*test2_number_types)
