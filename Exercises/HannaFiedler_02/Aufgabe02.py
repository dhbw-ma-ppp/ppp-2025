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
def maschine_funktion(liste):
    pos = 0
    gefunden = False
    while gefunden == False:
        #print (liste[i])
        if liste[pos]==1: #addition
            #print("Addition")
            summe = liste[liste[pos+1]]+liste[liste[pos+2]]
            liste[liste[pos+3]] = summe
            #print("erfolgreich")
        elif liste[pos]==2: #multiplikation
            #print("Multiplikation")
            produkt = liste[liste[pos+1]]*liste[liste[pos+2]]
            liste[liste[pos+3]] = produkt
            #print("erfolgreich")
        elif liste[pos]==99:
            print ("99 gefunden.")
            gefunden = True
            return liste[0]
        else:
            print("Fehler im Code.")
            gefunden = True
            return 0
        pos+=4

# As an example, in the list of integers passed to your function is 
# [1, 0, 0, 0, 99] the 1 in the first position indicates you should read the values
# at position given by the second and third entries. Both of these indicate position 0, so you should read the value
# at position 0 twice. That value is 1. Adding 1 and 1 gives you two. You then look at the value in the fourth
# position, which is again 0, so you write the result to position 0. You then step forward by 4 steps, arriving at 99
# and ending the program. The final memory looks like [2, 0, 0, 0, 99]. Your function should return 2.
print("Teil 1:")
liste1 = [1, 0, 0, 0, 99]   
print("Wert an der ersten Position der 1.Liste:", maschine_funktion(liste1))
print("Liste1:", liste1,"\n")

# Here's another testcase:
# [1, 1, 1, 4, 99, 5, 6, 0, 99] should become [30, 1, 1, 4, 2, 5, 6, 0, 99]
# Your function should return 30.
liste2 = [1, 1, 1, 4, 99, 5, 6, 0, 99]   
print("Wert an der ersten Position der 2.Liste:", maschine_funktion(liste2))
print("Liste2:",liste2,"\n")


# print out which value is returned by your function for the following list:
commands = [1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 9, 19, 1, 5, 19, 23, 1, 6, 23, 27, 1, 27, 10, 31, 1, 31, 5, 35, 2, 10, 35, 39, 1, 9, 39, 43, 1, 43, 5, 47, 1, 47, 6, 51, 2, 51, 6, 55, 1, 13, 55, 59, 2, 6, 59, 63, 1, 63, 5, 67, 2, 10, 67, 71, 1, 9, 71, 75, 1, 75, 13, 79, 1, 10, 79, 83, 2, 83, 13, 87, 1, 87, 6, 91, 1, 5, 91, 95, 2, 95, 9, 99, 1, 5, 99, 103, 1, 103, 6, 107, 2, 107, 13, 111, 1, 111, 10, 115, 2, 10, 115, 119, 1, 9, 119, 123, 1, 123, 9, 127, 1, 13, 127, 131, 2, 10, 131, 135, 1, 135, 5, 139, 1, 2, 139, 143, 1, 143, 5, 0, 99, 2, 0, 14, 0]
print("Wert an der ersten Position von commands:", maschine_funktion(commands))
print("Commands:",commands,"\n")

###########################################
# Write a function that takes an arbitrary number of unnamed arguments
# All inputs will be of type string.
# the function should return two lists:
#   The first list should contain all arguments which can be interpreted
#   as a number.
#   The second list should contain all strings which contain just one character.
def sortieren_funktion(*args):
    liste_zahl = []
    liste_laenge = []
    for element in args:
        wert = element
        try: #kann der Wert als Dezimalzahl dargestellt werden?
             wert1=float(wert)   
        except ValueError as exception: #falls Typecast nicht möglich
            try: #kann der Wert als Hexadezimalzahl dargestellt werden?
                wert1=int(wert,16) 
            except ValueError as exception: #falls Typecast nicht möglich: nächster Schleifendurchlauf
                continue
            else:
                add_to_list(wert,liste_zahl)
        else: #falls Umwandlung möglich: Zahl zu liste_zahl hinzufügen
            add_to_list(wert,liste_zahl)
        if len(wert)==1: #wenn nur ein Character: Character zu liste_laenge hinzufügen
            add_to_list(wert,liste_laenge)
    return liste_laenge, liste_zahl

def add_to_list(wert,liste): #Wert an Liste anhängen 
    liste.append(wert)

# Think of some good inputs to test this functionality, write down at least three
# examples and verify that the output for these examples is correct.

print("Teil 2:") #Ausgabe der 3 sortierten Beispiele
print("1) ",sortieren_funktion("34382","r","3","ghvi","10010","0"),"\n")
print("2) ",sortieren_funktion("fünf","h","14-3","2*3",",","5"),"\n")
print("3) ",sortieren_funktion("2134.65","12,5","2^2","?","1A5"),"\n")