from utils.test import test_function  # imports a function to simplify testing

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

print("1)")


def calculate_number_through_memory_list(
    memory_integer_list: list[int], opcode_index: int = 0
) -> int:
    """Process a list of integers through opcodes (1: add, 2: multiply, 99: halt).

    Recursively executes the program stored in `memory_integer_list` until opcode 99 is reached.

    Parameters
    ----------
    memory_integer_list : list[int]
        Program "memory" containing opcodes and parameters.
    opcode_index : int, optional
        Current opcode position (default 0).

    Returns
    -------
    int
        Value at position 0 after execution.
    """

    # expecting list with correct values, else runtime error when accessing items through outbound indices
    opcode = memory_integer_list[opcode_index]

    if opcode == 99:  # halt
        return memory_integer_list[0]
    elif opcode not in [1, 2]:  # guard, expecting valid opcode
        raise RuntimeError("No valid opcode provided!")

    read_1_index = memory_integer_list[opcode_index + 1]
    read_2_index = memory_integer_list[opcode_index + 2]

    read_1 = memory_integer_list[read_1_index]
    read_2 = memory_integer_list[read_2_index]

    write_index = memory_integer_list[opcode_index + 3]

    memory_integer_list[write_index] = (
        (read_1 + read_2) if opcode == 1 else (read_1 * read_2)
    )  # () for better structure, alternatively to ternary you could use if else compound statement

    return calculate_number_through_memory_list(memory_integer_list, opcode_index + 4)


test_function(
    calculate_number_through_memory_list,
    params=(
        [1, 1, 1, 4, 99, 5, 6, 0, 99],
    ),  # to be able to keep list as such & dont unpack the list itself!
    expected=30,
)

# print out which value is returned by your function for the following list:
# fmt: off
commands = [1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 9, 19, 1, 5, 19, 23, 1, 6, 23, 27, 1, 27, 10, 31, 1, 31, 5, 35, 2, 10, 35, 39, 1, 9, 39, 43, 1, 43, 5, 47, 1, 47, 6, 51, 2, 51, 6, 55, 1, 13, 55, 59, 2, 6, 59, 63, 1, 63, 5, 67, 2, 10, 67, 71, 1, 9, 71, 75, 1, 75, 13, 79, 1, 10, 79, 83, 2, 83, 13, 87, 1, 87, 6, 91, 1, 5, 91, 95, 2, 95, 9, 99, 1, 5, 99, 103, 1, 103, 6, 107, 2, 107, 13, 111, 1, 111, 10, 115, 2, 10, 115, 119, 1, 9, 119, 123, 1, 123, 9, 127, 1, 13, 127, 131, 2, 10, 131, 135, 1, 135, 5, 139, 1, 2, 139, 143, 1, 143, 5, 0, 99, 2, 0, 14, 0]
# fmt: on

print(
    f"Result of number-calculation of the commands-list is: {calculate_number_through_memory_list(commands)}"
)


###########################################
# Write a function that takes an arbitrary number of unnamed arguments
# All inputs will be of type string.
# the function should return two lists:
#   The first list should contain all arguments which can be interpreted
#   as a number.
#   The second list should contain all strings which contain just one character.
# Think of some good inputs to test this functionality, write down at least three
# examples and verify that the output for these examples is correct.

print("\n2)")


def split_numbers_and_single_chars(*args: str) -> tuple[list[str], list[str]]:
    """
    Returns numbers and signle chars as two seperate arrays

    Parameters
    ----------
    *args: str
        Variable amount of paramters of type string.

    Returns
    -------
    tuple[list[str], list[str]]
        Tuple with two lists. First one listing the numbers, second one listing single characters.
    """

    numbers = []
    chars = []
    for arg in args:
        # case number
        try:  # alternatively check instead of error-proofing "EAFP" -> "Easier to ask for forgiveness than permission" or "European Association of Fish Pathologists e.V."
            float(arg)  # to support fractions (operations) -> e.g. use Fraction(arg)
            numbers.append(arg)
        except (
            ValueError
        ):  # ValueError is the only type of error that could happen and the one we are interested in
            pass

        # case char, can also be a one-digit number
        if len(arg) == 1:
            chars.append(arg)
    return (numbers, chars)


# test if arg can be in both lists
test_function(
    split_numbers_and_single_chars,
    params=("1", "2", "3"),
    expected=(["1", "2", "3"], ["1", "2", "3"]),
)

# test for floats
test_function(
    split_numbers_and_single_chars,
    params=("1.3", "2", "1.5", "1.8e+308", "1.8e+3321321321312321"),
    expected=(["1.3", "2", "1.5", "1.8e+308", "1.8e+3321321321312321"], ["2"]),
)

# test for letters and other unicodes
test_function(
    split_numbers_and_single_chars,
    params=("ab", "a", "d", "z", "🐈", "🌳"),
    expected=([], ["a", "d", "z", "🐈", "🌳"]),
)

# expected special cases

## test for whitespaces
test_function(
    split_numbers_and_single_chars,
    params=("         3.14 ", " ", "           "),
    expected=(["         3.14 "], [" "]),
)

## test for \
test_function(
    split_numbers_and_single_chars,
    params=("\n", "\t"),
    expected=([], ["\n", "\t"]),
)

## test for keywords or fractions (operations & names not supported)
test_function(
    split_numbers_and_single_chars,
    params=("1/3", "pi"),
    expected=([], []),
)

# test for infinity
test_function(
    split_numbers_and_single_chars,
    params=("infinity", "inf", "-inf"),
    expected=(["infinity", "inf", "-inf"], []),
)

# test for NaN (can be **interpreted** as "number" by float)
test_function(
    split_numbers_and_single_chars,
    params=("nan", "NAN", "NaN"),
    expected=(["nan", "NAN", "NaN"], []),
)
