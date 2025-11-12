
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

# Erweitern Sie den simulierten Computer aus der zweiten Woche:
# Sie müssen eine Reihe zusätzlicher Opcodes unterstützen:
# - 3: Liest eine einzelne Ganzzahl als Eingabe und speichert sie an der Position, die
#      durch ihren einzigen Parameter angegeben wird. Der Befehl 3,19 würde eine Eingabe lesen
#      und das Ergebnis an Adresse 19 speichern.
# - 4: Gibt den Wert des einzigen Parameters für diesen Opcode aus.
#      Beispielsweise würde 4,19 den unter Adresse 19 gespeicherten Wert ausgeben.
# - 5: Sprung bei Wahr: Wenn der erste Parameter ungleich Null ist, setzt er den Befehlszeiger auf den Wert aus dem zweiten Parameter. Andernfalls wird nichts unternommen.
# - 6: Sprung bei Falsch: Wenn der erste Parameter Null ist, setzt er den Befehlszeiger auf den Wert aus dem zweiten Parameter. Andernfalls wird nichts unternommen.
# - 7: kleiner als: Wenn der erste Parameter kleiner als der zweite Parameter ist, speichert er 1 an der durch den dritten Parameter angegebenen Position. Andernfalls speichert er 0.
# - 8: gleich: Wenn der erste Parameter gleich dem zweiten Parameter ist, speichert er 1 an der durch den dritten Parameter angegebenen Position. Andernfalls speichert er 0.
#
# Achtung: Da diese Opcodes eine variable Anzahl von Parametern erwarten, sollte der Befehlszeiger nach der Ausführung eines Befehls nicht mehr immer
# um vier erhöht werden. Stattdessen sollte er entsprechend der Anzahl der Parameter erhöht werden, die der Befehl erwartet.
# Wenn der Opcode jedoch den Befehlszeiger direkt manipuliert (5 und 6), sollte keine zusätzliche Änderung des Befehlszeigers erfolgen.
# Die nächste auszuführende Anweisung wird direkt an der Stelle gespeichert, die durch den Parameter dieser Opcodes angegeben wird.
# Achtung: Zahlen in Ihrem Speicher sowie Eingaben können negativ sein!
#
# Zusätzlich müssen Sie zwei verschiedene Parametermodi unterstützen: den Positionsmodus (Modus 0) und den Immediate-Modus (Modus 1).
# Positionsmodus: Opcode-Argumente sind Speicheradressen. Wenn ein Argument den Wert 18 hat, holen Sie den „Berechnungswert”
#   aus dem Speicher an Adresse 18. Dies ist der Modus, den Sie bereits vom letzten Mal kennen.
# Direktmodus: Im Direktmodus wird ein Parameter direkt als Wert interpretiert. Wenn das erste Argument des Opcodes „sum” 8 ist,
#   dann ist der erste Summand in Ihrer Berechnung 8.
#
# Parametermodi werden pro Parameter als Teil des Opcodes durch Erweiterung der Opcodes festgelegt.
# Beim Lesen einer Zahl, die einen Opcode angibt,
#   - enthalten die beiden Ziffern ganz rechts den eigentlichen Opcode,
#   - alle weiteren Ziffern enthalten den Parametermodus der Parameter, wobei die Ziffern von rechts nach links gelesen werden
#     und die Parameter in der Reihenfolge von links nach rechts. Alle nicht angegebenen Ziffern werden standardmäßig auf 0 gesetzt (Positionsmodus).
#     HINWEIS: Parameter für die Zieladresse einer Schreiboperation (z. B. der dritte Parameter des Opcodes „sum” oder „multiply”)
#           werden niemals im Immediate-Modus angegeben.
#
# Hier ein Beispiel:
#   Betrachten Sie die Befehlsfolge „1002,4,3,4,33”.
#   Die beiden Ziffern ganz rechts im ersten Eintrag („02”) geben den Opcode an: Multiplikation.
#   Dann ist die nächste Ziffer von rechts nach links eine „0“, was bedeutet, dass sich der erste Parameter im Positionsmodus befindet.
#   Die nächste Ziffer ist eine „1“, was bedeutet, dass sich der zweite Parameter im Direktmodus befindet.
#   Die nächste Ziffer ist nicht vorhanden, sodass standardmäßig „0“ gilt und sich der dritte Parameter ebenfalls im Positionsmodus befindet.
#   Es müssen keine weiteren Parametermodi bestimmt werden, da die Multiplikationsanweisung drei Parameter akzeptiert.
#   Der erste Parameter im Positionsmodus ist der Wert an der Adresse „4“ – 33.
#   Der zweite Parameter im Direktmodus ist der Wert „3“.
#   Die Ausführung der Multiplikationsanweisung ergibt das Ergebnis 33*3=99.
#   Der dritte Parameter (4) im Positionsmodus weist diesen Wert dem Speicherplatz 4 zu (der Speicherplatz, der zuvor
#   zuvor den Wert 33 hatte, nun den Wert 99).
#   Wenn wir nun den Befehlszeiger vorwärts bewegen, gelangen wir zu Position 4 mit dem Opcode 99, wodurch das Programm angehalten wird.
#
# Und hier sind einige Testfälle:
#   3,9,8,9,10,9,4,9,99,-1,8 – testet, ob die Eingabe gleich 8 ist (im Positionsmodus)
#   3,3,1107,-1,8,3,4,3,99 -- testet, ob die Eingabe kleiner als 8 ist (im Direktmodus)
#   3,3,1105,-1,9,1101,0,0,12,4,12,99,1 -- testet, ob die Eingabe 0 ist, unter Verwendung von Sprunganweisungen
#
# Führen Sie abschließend Ihren Code für die folgenden Anweisungen aus. Geben Sie bei der Eingabeaufforderung die Zahl „5” ein. Das Programm sollte bei der Ausführung eine einzelne Zahl ausgeben.
# Bitte notieren Sie sich diese Zahl in Ihrem PR, damit ich nicht alle Dateien selbst ausführen muss :)
import logging

logging.basicConfig(filename='logger.log', level=logging.DEBUG, force=True)

def calculate_number_in_list(lst: list[int]):
    handler = make_handlers()
    pointer = 0
    while True:
        opcode, modes = parse_opcode_and_modes(lst[pointer])
        if opcode not in handler:
            raise RuntimeError(f"Unknown opcode {opcode} at pointer {pointer}")
        next_pointer = handler[opcode](lst, pointer, modes)
        if next_pointer is None:
            break
        pointer = next_pointer
    
def parse_opcode_and_modes(code: int):
    s = str(code)
    opcode = int(s[-2:]) if len(s) >= 2 else int(s)
    # digits left of opcode, reversed => modes in order m1,m2,m3...
    modes_str = s[:-2][::-1]  # '' -> no modes
    modes = [int(ch) for ch in modes_str] if modes_str else []
    return opcode, modes

def get_param_value(lst: list[int], pointer: int, param_index, modes: list[int]):
    mode = modes[param_index-1] if param_index - 1 < len(modes) else 0
    raw_index = pointer + param_index
    if raw_index >= len(lst):
        raise IndexError(f"Parameter {param_index} außerhalb der Liste ({pointer=}).")
    raw = lst[raw_index]
    if mode == 0:
        if raw < 0 or raw >= len(lst):
            raise IndexError(f"Position mode: Adresse {raw} ungültig.")
        return lst[raw]
    elif mode == 1:
        return raw
    else:
        raise ValueError(f"Unbekannter Parametermodus {mode}")

def get_write_address(lst, pointer, param_index):
    raw_index = pointer + param_index
    if raw_index >= len(lst):
        raise IndexError(f"Write-Parameter {param_index} außerhalb der Liste (pointer={pointer}).")
    addr = lst[raw_index]
    if addr < 0 or addr >= len(lst):
        raise IndexError(f"Write-Adresse {addr} ungültig.")
    return addr

def make_handlers():
    handlers = {}
    
    #   opcode 1: add
    def op_add(lst, pointer, modes):
        a = get_param_value(lst, pointer, 1, modes)
        b = get_param_value(lst, pointer, 2, modes)
        dest = get_write_address(lst, pointer, 3)
        lst[dest] = a + b
        return pointer + 4
    handlers[1] = op_add
    
    #   opcode 2: multiply
    def op_mul(lst, pointer, modes):
        a = get_param_value(lst, pointer, 1, modes)
        b = get_param_value(lst, pointer, 2, modes)
        dest = get_write_address(lst, pointer, 3)
        lst[dest] = a * b
        return pointer + 4
    handlers[2] = op_mul
    
    #   opcode 3: input (write)
    def op_input(lst, pointer, modes):
        dest = get_write_address(lst, pointer, 1)
        lst[dest] = int(input(f"Please enter an integer:\n"))
        return pointer + 2
    handlers[3] = op_input
    
    #   opcode 4: output (read)
    def op_output(lst, pointer, modes):
        val = get_param_value(lst, pointer, 1, modes)
        print(val)
        return None
    handlers[4] = op_output
    
    #   opcode 5: jump-if-true
    def op_jump_true(lst, pointer, modes):
        test = get_param_value(lst, pointer, 1, modes)
        target = get_param_value(lst, pointer, 2, modes)
        return target if test != 0 else pointer + 3
    handlers[5] = op_jump_true
    
    #   opcode 6: jump-if-false
    def op_jump_false(lst, pointer, modes):
        test = get_param_value(lst, pointer, 1, modes)
        target = get_param_value(lst, pointer, 2, modes)
        return target if test == 0 else pointer + 3
    handlers[6] = op_jump_false
    
    #   opcode 7: less than
    def op_less_than(lst, pointer, modes):
        a = get_param_value(lst, pointer, 1, modes)
        b = get_param_value(lst, pointer, 2, modes)
        dest = get_write_address(lst, pointer, 3)
        lst[dest] = 1 if a < b else 0
        return pointer + 4
    handlers[7] = op_less_than
    
    #   opcode 8: equals
    def op_equals(lst, pointer, modes):
        a = get_param_value(lst, pointer, 1, modes)
        b = get_param_value(lst, pointer, 2, modes)
        dest = get_write_address(lst, pointer, 3)
        lst[dest] = 1 if a == b else 0
        return pointer + 4
    handlers[8] = op_equals
    
    #   opcode 99: halt
    def op_halt(lst, pointer, modes):
        return None
    handlers[99] = op_halt
    return handlers
    
calculate_number_in_list(commands)