# This file allows the user to see what the virtual machine does

# imports
from simple_and_with_logs import calc_virtual_machine, commands

while True:
    match input("Enter the number of the example: -> ").lower():
        case "1":
            calc_virtual_machine([1002,4,3,4,33], log_operations=True)
        case "2":
            calc_virtual_machine([3,9,8,9,10,9,4,9,99,-1,8], use_auto_input=True, auto_input=8, log_operations=True)
        case "3":
            calc_virtual_machine([3,3,1107,-1,8,3,4,3,99], use_auto_input=True, auto_input=7, log_operations=True) == 1
        case "4":
            calc_virtual_machine([3,3,1105,-1,9,1101,0,0,12,4,12,99,1 ], use_auto_input=True, auto_input=0, log_operations=True) == 0
        case "5":
            calc_virtual_machine(commands.copy(), use_auto_input=True, auto_input=5, log_operations=True)
        case "exit":
            break
        case _:
            print("Invalid input!")
            print('Enter "exit" to end the programm.')

