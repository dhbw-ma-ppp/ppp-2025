def memory_machine(memory):
    mem = memory.copy() # Kopie -> Behalten der Originalliste
    index = 0
    
    while True:
        opcode = mem[index]
        match opcode:
            case 99:
                return mem[0]
            case 1:
                val1 = mem[mem[index + 1]]
                val2 = mem[mem[index + 2]]
                dest = mem[index + 3]
                mem[dest] = val1 + val2
                index += 4
            case 2:
                val1 = mem[mem[index + 1]]
                val2 = mem[mem[index + 2]]
                dest = mem[index + 3]
                mem[dest] = val1 * val2
                index += 4
            case _:
                print(f"FEHLER: Ungültiger Opcode {opcode} an Position {index}")
                return None

def klassifiziere_strings(*args):
    zahlen_liste = []
    einzelzeichen_liste = []
    
    for text in args:
        ist_zahl = False
        try:
            float(text)
            ist_zahl = True
        except ValueError:
            ist_zahl = False
        
        if ist_zahl:
            zahlen_liste.append(text)

        if len(text) == 1 :
            einzelzeichen_liste.append(text)
    
    return zahlen_liste, einzelzeichen_liste

# ---------
# | TESTS |
# ---------

print("AUFGABE 1:")
commands = [1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 9, 19, 1, 5, 19, 23, 1, 6, 23, 27, 1, 27, 10, 31, 1, 31, 5, 35, 2, 10, 35, 39, 1, 9, 39, 43, 1, 43, 5, 47, 1, 47, 6, 51, 2, 51, 6, 55, 1, 13, 55, 59, 2, 6, 59, 63, 1, 63, 5, 67, 2, 10, 67, 71, 1, 9, 71, 75, 1, 75, 13, 79, 1, 10, 79, 83, 2, 83, 13, 87, 1, 87, 6, 91, 1, 5, 91, 95, 2, 95, 9, 99, 1, 5, 99, 103, 1, 103, 6, 107, 2, 107, 13, 111, 1, 111, 10, 115, 2, 10, 115, 119, 1, 9, 119, 123, 1, 123, 9, 127, 1, 13, 127, 131, 2, 10, 131, 135, 1, 135, 5, 139, 1, 2, 139, 143, 1, 143, 5, 0, 99, 2, 0, 14, 0]
print(f"Commands: {memory_machine(commands)}" + "\n")

print("AUFGABE 2:")
test_strings = ("52", "hello", "a", "pi", "3.14", "x", "7", "abcd", "!", "5h7Q!", "-10", "0")
print("Eingabe:", test_strings)
nums, chars = klassifiziere_strings(*test_strings)
print(f"Zahlen: {nums}")
print(f"Einzelzeichen: {chars}")