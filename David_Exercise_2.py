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
print("Aufgabe 1 \n")

def aufgabe2(arr):
    i = 0   # "i" gibt den Ort in der Liste an
    while(arr[i]!= 99):     # while Schleife endet sobald die Liste an der Stelle i den Wert 99 hat
        if arr[i] == 1: 
            adresse_1 = arr[i+1]    # der Wert an der Stelle i+1 wird in der Variable "adresse_1" gespeichert
            adresse_2 = arr[i+2]    # der Wert an der Stelle i+2 wird in der Variable "adresse_2"gespeichert
            adresse_3 = arr[i+3]    # der Wert an der Stelle i+3 wird in der Variable "adresse_3"gespeichert

            wert_1 = arr[adresse_1] # der Wert an der Stelle adresse_1 wird in der Variable "wert_1" gespeichert
            wert_2 = arr[adresse_2] # der Wert an der Stelle adresse_2 wird in der Variable "wert_2" gespeichert

            arr[adresse_3] = wert_1 + wert_2    # die Variablen wert_1 und wert_2 werden addiert und adn der Stelle von "adresse" in der Liste gespeichert

        if arr[i] == 2:
            adresse_1 = arr[i+1]
            adresse_2 = arr[i+2]
            adresse_3 = arr[i+3]

            wert_1 = arr[adresse_1]
            wert_2 = arr[adresse_2]

            arr[adresse_3] = wert_1 * wert_2     # die Variablen wert_1 und wert_2 werden multipliziert und adn der Stelle von "adresse" in der Liste gespeichert

        i += 4 
    return arr[0]   # der Wert der Stelle 0 wird von der Funktion zurückgegeben


print(f"The first integer of the procesed list is: {aufgabe2(commands)}\n\n")



###########################################
# Write a function that takes an arbitrary number of unnamed arguments
# All inputs will be of type string.
# the function should return two lists:
#   The first list should contain all arguments which can be interpreted
#   as a number.
#   The second list should contain all strings which contain just one character.
# Think of some good inputs to test this functionality, write down at least three
# examples and verify that the output for these examples is correct.

print("Aufgabe2\n")

def pruefe_argumente(*args):

    one_character_strings = [None] * len(args)  # liste der Länge von der Anzahl der übergebenen Werte, damit kein out of range Fahler kommt
    numbers = [None] * len(args)
    b = 0   # Variable die beim iterieren der Schleife hochzählt
    
    for argument in args:
        try:
            typecast = int(argument)    # hier wird ein typcast versucht, um zu überprüfen, 
                                        # ob der String als Integer interpretiert werden kann.
                                        # Wenn es klappt wird der Wert in der neuen Variable 
                                        # typecast gespeichert, wenn nicht dann nicht                           
                                        #           
            numbers[b] = typecast       # Wenn er als Integer interpretiert werden kann
                                        # kommt er auf meine numers Liste
        except ValueError:              # Sollte der String nicht als Integer interpretierbar sein
                                        # würde es zu einem ValueError kommen und das Programm bricht ab,
                                        # um das zu verhindern wird der Fehler hier rausgenommen
            try:
                typecast = float(argument)  # Da floats auch Zahlen sind, nochmal das gleiche
                                            # wie davor nur mit float 
                numbers[b] = typecast
            except ValueError:          

                if argument == "True":       #bool's sind auch nur 0 oder 1 gehören also auch zu den Zahlen
                    numbers[b] = argument + ("(1)")
                    continue
                if argument == "False":
                    numbers[b] = argument + ("(0)")
                    continue

                if len(argument) == 1:      # Hier wird geprüft ob der String mehr als einen Buchstaben hat
                    one_character_strings[b] = argument   # Sollte das passen, kommt er auf die one_character_strings Liste
                else:
                    print(f"{argument} muss leider draußen bleiben.\n")
        
        b +=1   # b wird um 1 erhöht, damit der nächste Wert nicht den alten überschreibt
    numbers = [x for x in numbers if x is not None]
    one_character_strings = [x for x in one_character_strings if x is not None]
        
    
    print(f"Alle als Zahlen interpretiebaren Übergabewerte: {numbers}\n")
    print(f"Alle Strings mit nur einem Buchstaben aus den Übergabewerten: {one_character_strings}")

pruefe_argumente("True","1.4","M","Jakob","True","False","a")    # Beispiele, bei denen es richtig funktioniert 