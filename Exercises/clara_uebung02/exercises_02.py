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

def working_memory(liste):
    zaehler = 0
    while liste[zaehler] != 99:
        match liste[zaehler]:
            case 1:
                summe = liste[liste[zaehler + 1]] + liste[liste[zaehler + 2]]
                liste[liste[zaehler + 3]] = summe
                zaehler += 4
            case 2:
                produkt = liste[liste[zaehler + 1]] * liste[liste[zaehler + 2]]
                liste[liste[zaehler + 3]] = produkt
                zaehler += 4
            case _:
                print("Error")
                return 0
    return liste[0]


#beispiel1 = [1, 0, 0, 0, 99]
#beispiel2 = [1, 1, 1, 4, 99, 5, 6, 0, 99]

# print out which value is returned by your function for the following list:

commands = [1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 9, 19, 1, 5, 19, 23, 1, 6, 23, 27, 1, 27, 10, 31, 1, 31, 5, 35, 2, 10, 35, 39, 1, 9, 39, 43, 1, 43, 5, 47, 1, 47, 6, 51, 2, 51, 6, 55, 1, 13, 55, 59, 2, 6, 59, 63, 1, 63, 5, 67, 2, 10, 67, 71, 1, 9, 71, 75, 1, 75, 13, 79, 1, 10, 79, 83, 2, 83, 13, 87, 1, 87, 6, 91, 1, 5, 91, 95, 2, 95, 9, 99, 1, 5, 99, 103, 1, 103, 6, 107, 2, 107, 13, 111, 1, 111, 10, 115, 2, 10, 115, 119, 1, 9, 119, 123, 1, 123, 9, 127, 1, 13, 127, 131, 2, 10, 131, 135, 1, 135, 5, 139, 1, 2, 139, 143, 1, 143, 5, 0, 99, 2, 0, 14, 0]

ergebnis = working_memory(commands)

print("Das Ergebnis der working memory lautet:", ergebnis)

###########################################
# Write a function that takes an arbitrary (unbestimmte) number of unnamed arguments
# All inputs will be of type string.
# the function should return two lists:
#   The first list should contain all arguments which can be interpreted
#   as a number.
#   The second list should contain all strings which contain just one character.
# Think of some good inputs to test this functionality, write down at least three
# examples and verify that the output for these examples is correct.

def Klassifizierung(string_liste):
    index = 0
    zahlen_liste = []
    zeichen_liste = []

    while index < len(string_liste):
        try:
            float(string_liste[index])
            zahlen_liste.append(string_liste[index])
        except:
            pass
        
        if len(string_liste[index]) == 1:
            zeichen_liste.append(string_liste[index])
    
        index += 1
    return zahlen_liste, zeichen_liste

#Meine Definition einer Nummer beschränkt sich auf das, was in Python im Datentyp float enthalten ist

test_liste1 = ["Hallo", "+12e3", "A", "-45", "?674658", "9", "-6.87", "~"]
test_liste2 = ["Ich bin eine Zahl", "78375645e142", "l", "87545.5625", "4", "6+3", "7/ghdgf", "&"]
test_liste3 = ["6&33", "-67665e78", "6e-56","H", "§", "Pythonkurs", ".", "++6768"]

zahlen_liste, zeichen_liste = Klassifizierung(test_liste1)

print(test_liste1)

print("Folgende Zahlen sind in der Liste enthalten:", zahlen_liste)
print("Folgende einzelne Zeichen sind in der Liste enthalten:", zeichen_liste)

#Output Testliste 1: 
#   ['Hallo', '+12e3', 'A', '-45', '?674658', '9', '-6.87', '~']
#   Folgende Zahlen sind in der Liste enthalten: ['+12e3', '-45', '9', '-6.87']
#   Folgende einzelne Zeichen sind in der Liste enthalten: ['A', '9', '~']

#Output Testliste 2: 
#   ['Ich bin eine Zahl', '78375645e142', 'l', '87545.5625', '4', '6+3', '7/ghdgf', '&']
#   Folgende Zahlen sind in der Liste enthalten: ['78375645e142', '87545.5625', '4']
#   Folgende einzelne Zeichen sind in der Liste enthalten: ['l', '4', '&']

#Output Testliste 3: 
#   ['6&33', '-67665e78', '6e-56', 'H', '§', 'Pythonkurs', '.', '++6768'] 
#   Folgende Zahlen sind in der Liste enthalten: ['-67665e78', '6e-56'] 
#   Folgende einzelne Zeichen sind in der Liste enthalten: ['H', '§', '.']