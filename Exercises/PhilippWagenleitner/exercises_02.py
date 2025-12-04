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

def programm(eingabe):
    index=0
    while True:
        match eingabe[index]:
            case 1: 
                index=addition(index)
            case 2:
                index=multiplikation(index)
            case 99:
                ninetynine()
                break
            case _:
                print("Kein Opcode gefunden. Programm wird beendet")
                break 

def addition(index):
    add_nr1=eingabe[index+1]
    add_nr2=eingabe[index+2]
    speicherplatz_add=eingabe[index+3]
    eingabe[speicherplatz_add]=eingabe[add_nr1]+eingabe[add_nr2]
    return index+4

def multiplikation(index):
    mul_nr1=eingabe[index+1]
    mul_nr2=eingabe[index+2]
    speicherplatz_mul=eingabe[index+3]
    eingabe[speicherplatz_mul]=eingabe[mul_nr1]*eingabe[mul_nr2]
    return index+4

def ninetynine():
    print("99 gefunden! Programm wurde erfolreich ausgeführt!")


if __name__ == '__main__':
    print("Programm 1 von exercise_02: \n")
    #in Eingabe die jeweilige Liste
    eingabe = [1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 9, 19, 1, 5, 19, 23, 1, 6, 23, 27, 1, 27, 10, 31, 1, 31, 5, 35, 2, 10, 35, 39, 1, 9, 39, 43, 1, 43, 5, 47, 1, 47, 6, 51, 2, 51, 6, 55, 1, 13, 55, 59, 2, 6, 59, 63, 1, 63, 5, 67, 2, 10, 67, 71, 1, 9, 71, 75, 1, 75, 13, 79, 1, 10, 79, 83, 2, 83, 13, 87, 1, 87, 6, 91, 1, 5, 91, 95, 2, 95, 9, 99, 1, 5, 99, 103, 1, 103, 6, 107, 2, 107, 13, 111, 1, 111, 10, 115, 2, 10, 115, 119, 1, 9, 119, 123, 1, 123, 9, 127, 1, 13, 127, 131, 2, 10, 131, 135, 1, 135, 5, 139, 1, 2, 139, 143, 1, 143, 5, 0, 99, 2, 0, 14, 0]
    programm(eingabe)
    print(f"Die neue Liste: {eingabe}") #Kontrolle 2
    print(f"Der Wert an der Stelle 0 beträgt: {eingabe[0]}")

#Programm funktioniert. Vergleiche mit anderen


# print out which value is returned by your function for the following list:
commands = [1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 9, 19, 1, 5, 19, 23, 1, 6, 23, 27, 1, 27, 10, 31, 1, 31, 5, 35, 2, 10, 35, 39, 1, 9, 39, 43, 1, 43, 5, 47, 1, 47, 6, 51, 2, 51, 6, 55, 1, 13, 55, 59, 2, 6, 59, 63, 1, 63, 5, 67, 2, 10, 67, 71, 1, 9, 71, 75, 1, 75, 13, 79, 1, 10, 79, 83, 2, 83, 13, 87, 1, 87, 6, 91, 1, 5, 91, 95, 2, 95, 9, 99, 1, 5, 99, 103, 1, 103, 6, 107, 2, 107, 13, 111, 1, 111, 10, 115, 2, 10, 115, 119, 1, 9, 119, 123, 1, 123, 9, 127, 1, 13, 127, 131, 2, 10, 131, 135, 1, 135, 5, 139, 1, 2, 139, 143, 1, 143, 5, 0, 99, 2, 0, 14, 0]


###########################################
# Write a function that takes an arbitrary number of unnamed arguments
# All inputs will be of type string.
# the function should return two lists:
#   The first list should contain all arguments which can be interpreted
#   as a number.
#   The second list should contain all strings which contain just one character.
# Think of some good inputs to test this functionality, write down at least three
# examples and verify that the output for these examples is correct.

#Filtert nur 'typische' Zahlen (alles was sich in Float konvertieren lässt).

import string
import collections

def filter(eingabe):
    Liste1=eingabe.split()
    lenght = len(Liste1)
    ListeChar = []
    ListeNummer = []
    for i in range (lenght):
        laengei = len(Liste1[i]) 
        if laengei==1:
            if Liste1[i] in "1234567890":
                ListeNummer.append(Liste1[i])
                ListeChar.append(Liste1[i])  
            else:
                ListeChar.append(Liste1[i])
        else:
            try:
                nummer=float(Liste1[i])
                ListeNummer.append(nummer)
            except ValueError:
                continue
    print(f"Alle Nummern im Input: {ListeNummer}")
    print(f"Alle einzelnen Charaktere: {ListeChar}")

def NummerListeFilter(ListeNummer, ListeNummerEnd):
    for i in range (len(ListeNummer)):
        try:
            nummerEnd=float(ListeNummer[i])
            ListeNummerEnd.append(nummerEnd)
        except ValueError:
            continue
    ListeNummer.clear()


if __name__ == '__main__':
    print("Programm 2 von exercises_02: \n")
    #Inputs zum Prüfen: 
    #der hundnr.12 mag 1 tier oder nur c
    #ein einzelnes c oder 3.16839 c12 w 0
    #123 1.23 12.3 a b c acb123
    y=input("Geben sie etwas ein: ")
    filter(y)


