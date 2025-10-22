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

def simulatedComputerMemory(lst=None):
    if(lst is None):
        return 0
    
    for position in range(0,len(lst), 4):
        match lst[position]:
            case 1:
                num = lst[lst[position + 1]] + lst[lst[position + 2]]
                lst[lst[position + 3]] = num
            case 2:
                num = lst[lst[position + 1]] * lst[lst[position + 2]]
                lst[lst[position + 3]] = num
            case 99:
               return lst[0]
            case _:
                print("error")
                return 0

# print out which value is returned by your function for the following list:
commands = [1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 9, 19, 1, 5, 19, 23, 1, 6, 23, 27, 1, 27, 10, 31, 1, 31, 5, 35, 2, 10, 35, 39, 1, 9, 39, 43, 1, 43, 5, 47, 1, 47, 6, 51, 2, 51, 6, 55, 1, 13, 55, 59, 2, 6, 59, 63, 1, 63, 5, 67, 2, 10, 67, 71, 1, 9, 71, 75, 1, 75, 13, 79, 1, 10, 79, 83, 2, 83, 13, 87, 1, 87, 6, 91, 1, 5, 91, 95, 2, 95, 9, 99, 1, 5, 99, 103, 1, 103, 6, 107, 2, 107, 13, 111, 1, 111, 10, 115, 2, 10, 115, 119, 1, 9, 119, 123, 1, 123, 9, 127, 1, 13, 127, 131, 2, 10, 131, 135, 1, 135, 5, 139, 1, 2, 139, 143, 1, 143, 5, 0, 99, 2, 0, 14, 0]

print(f"returned value:  {simulatedComputerMemory(commands)} \n")
    


###########################################
# Write a function that takes an arbitrary (willkürlich) number of unnamed arguments
# All inputs will be of type string.
# the function should return two lists:
#   The first list should contain all arguments which can be interpreted
#   as a number.
#   The second list should contain all strings which contain just one character.
# Think of some good inputs to test this functionality, write down at least three
# examples and verify that the output for these examples is correct.


list_01 = ["11", "h", "hey", "1", "a"]
    # gewünschte Ausgabe: Character List = "h" , "a", "1" | Number List = 11 , 1
list_02 = ["Hallo mein Name ist Eve", "19", "299", "1", "Ha11o"]
    # gewünschte Ausgabe: Character List = "1" | Number List = 19, 299, 1
list_03 = ["11.1" , "2893.46", "Hey", "h"]
    #gewünschte Ausgabe: Character List = "h" | Number List = 11.1, 2893.46


def sortList(lst = None):
    if(lst is None):
        return 0
    characterLst = []
    numLst = []
    
    for item in lst:
        if len(item) == 1:
            characterLst.append(item)
        if(item.count(".") <= 1 and item.replace(".", "").isdigit()): # prüft ob es sich um eine nummer handelt. Damit auch floats akzeptiert werden, wird einfach geschaut ob es einen Punkt gibt und dieser wird kurz durch nichts ersetzt, damit "isdigit()" funktioniert
            numLst.append(item)

    return characterLst, numLst

def printAll(cLst, nLst):
    print("Character List")
    for item in cLst:
        print(item)

    print("_\n")
    print("Number List")
    for item in nLst:
        print(item)      

cList, nList = sortList(list_01)

print("\nList 01:")
printAll(cList, nList)

cList, nList = sortList(list_02)
print("\nList 02:")
printAll(cList, nList)

cList, nList = sortList(list_03)
print("\nList 03:")
printAll(cList, nList)

