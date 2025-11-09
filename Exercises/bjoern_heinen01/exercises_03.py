# pair programming Theo and Björn

# PART 1:
# Create a class BankAccount with:
# A “private” attribute _balance
# Methods:
#  deposit(amount) → increases the balance
#  withdraw(amount) → decreases it (if enough funds)
#  get_balance() → returns the balance
#  transfer(other_account, amount) -> It should withdraw from one account and deposit into the other.
#  Try depositing, withdrawing and transferring amounts and print the balance each time.
print("__Aufgabe 1 Bank Account__")

class Bank_Account: 
    def __init__(self, balance):
        self.__balance = balance
    
    def deposit(self, amount):
        self.__balance += int(amount)
        print(f"{amount} is now deposited in your bank account\n")
        print(f"Your Balance is {self.__balance}")


    def withdraw(self, amount):
        if int(amount) <= (self.__balance):
            self.__balance -= int(amount)
            print(f"{amount} is now withdrawn from your bank account\n")
            print(f"Your Balance is {self.__balance}\n")

            print("Please don't forget your money")
        else:
            print("Withdrawing denied")
            print(f"You can withdraw a maximum of your balance {self.__balance} deposit more money to increase this limit")


    def get_balance(self):
        print(self.__balance)
        

    def transfer(self, other_account, amount):
        if int(amount) <= (self.__balance):
            print("__TRANSFER__") 
            self.__balance -= int(amount)
            print(f"{amount} was transfered to {other_account}") 
            print(f"Your Balance is {self.__balance}")
        else: 
            print("Transfer declined")
            print(f"You can transfer a maximum of your balance {self.__balance} deposit more money to increase this limit")


my_bank_account = Bank_Account(balance=1000)


def ask_for_user_input():
    while True:
        print("What would you like to do?")
        print("Press 1 to deposit to your Account")
        print("Press 2 to withdraw from your Account")
        print("Press 3 to show your Balance")
        print("Press 4 to Transfer to another account")
        print("Press q/Q to Quit")


        user_input = input(" --> ")
        
        match user_input:
            case "1":
                print("__DEPOSIT__")
                print("How much would you like to deposit?")
                amount = input(" --> ")
                my_bank_account.deposit(amount)
                print("\n\n")
            case "2":
                print("__WITHDRAW__")
                print("How much would you like to withdraw?")
                amount = input(" --> ")
                my_bank_account.withdraw(amount)
                print("\n\n")
            case "3":
                print("__YOUR_BALANCE__")
                my_bank_account.get_balance()
                print("\n\n")
            case "4":
                print("__TRANSFER__")
                print("What is the IBAN?")
                other_account = input(" --> ")
                print("How much do you want to transfer")
                amount = input(" --> ")
                my_bank_account.transfer(other_account, amount) 
                print("\n\n")
            case "q" | "Q":
                print("Thanks for using our banking app")
                print("\n\n")
                return
            case _:
                print("Invalid input! Try again!")

ask_for_user_input()

# PART 2:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
#   The deck of cards should behave like a sequence.
#   When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
#   I should be able to index into the deck to retrieve one card.
#   I should be able to iterate over all cards in the deck.
#   Printing a cards string representation should give me a nice, readable description of that card.

print("__Aufgabe 2__")

card_symbols = {
            "hearts": "\u2764",
            "diamonds": "\u2B26",
            "spades": "\u2660",
            "clubs": "\u2663"
        }
class Card:
    # static private vars:
    __empty_card = """
+——————————+
|XX        |
|          |
|          |
|    Y     |
|          |
|          |
|          |
+——————————+
"""
    def __init__(self, color, val):
        self.color = color
        self.val = val 
    
    def __repr__(self):
        return f"Card('{self.val}', '{card_symbols[self.color]}')"
    
    def __str__(self):
        return f"{self.val} of {self.color}"

    def display(self):
        card_with_symbol = Card.__empty_card.replace("Y",self.color)
        card_with_symbol_and_val = card_with_symbol.replace("XX", f"{self.val:>2}")
        print(card_with_symbol_and_val)

class Deck:
    def __init__(self):
        self._cards:list[Card] = None
    
    def __getitem__(self, index):
        return self._cards[index]
    def display_deck(self):
        for card in self._cards:
            print(f"{card}")

            card.display()

    def ask_user_for_card_search(self):
        while True:
            print("Gib den Index der gesuchten Karte aus dem French Deck ein: (q/Q to quit)")
            card_number = input(" --> ")
            if card_number == "q" or card_number == "Q":
                break

            if int(card_number) < 1 or int(card_number) > len(self._cards):
                print(f"Ungültiger Index. Bitte zwischen 0 und {len(self._cards)} eingeben.")
            else:
                self._cards[int(card_number)-1].display()
    
    def __iter__(self):
        return (card for card in self._cards)
    
    def __str__(self):
        return "Deck:\n"+ "".join([f" * {card}\n" for card in self])

class French_Deck(Deck):
    def __init__(self):
        values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self._cards = [Card(color, val) for color in card_symbols.values() for val in values]
    
a_french_deck = French_Deck()
a_french_deck.ask_user_for_card_search()

#Gibt alle Karten in geordneter Reihenfolge aus
print("Alle Karten geordnet ausgegeben...")
a_french_deck.display_deck()

print(a_french_deck)
print("\n\n")

# PART 3:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

print("__Aufgabe 3__")

class Skat_Deck(Deck):
    def __init__(self):
        values = ["7", "8", "9", "10", "J", "Q", "K", "A"]
        self._cards = [Card(color, val) for color in card_symbols.values() for val in values]
    
a_skat_deck = Skat_Deck()
a_skat_deck.ask_user_for_card_search()

#Gibt alle Karten in geordneter Reihenfolge aus
print("Alle Karten geordnet ausgegeben...")
a_skat_deck.display_deck()

print("\n\n")




# PART 4:
# write a function that accepts two numbers, a lower bound and an upper bound.
# the function should then return the count of all numbers that meet certain criteria:
# - they are within the (left-inclusive and right-exclusive) bounds passed to the function
# - there is at least one group of exactly two adjacent digits within the number which are the same (like 33 in 123345)
# - digits only increase going from left to right
#
# Examples:
# - 123345 is a valid number
# - 123341 is not a valid number, as the digits do not increase from left to right
# - 123334 is not a valid number as there is no group of exactly two repeated digits
# - 111334 is a valid number. while there are three 1s, there is also a group of exactly two 3s.
# - 112233 is a valid number. At least one group of two is fulfilled, there is no maximum to the number of such groups.
#
# run your function with the lower bound `13456471` and the upper bound `58515929`. 
# It should complete in a few seconds. Note the resulting count in your pull request, please.

from functools import lru_cache
import time

def get_number_of_increasing_digits_with_pair_in_range_to_nine_row(lower_bound:int, upper_bound:int) -> int:
    
    def convert_number_into_increasing_digits(num:str) -> list[int]:
        chars = list(num)
        for i in range(1,len(chars)):
            # char comparrison works without casting to int
            # because of the structure of askii/utf-8
            if chars[i-1] > chars[i]: 
                for ii in range(i,len(chars)):
                    chars[ii] = chars[i-1]
                break

        coefficients = [int(char) for char in chars]
        return coefficients
    
    def get_second_pair_index(num:list[int]) -> int:
        # example [1,2,2,3] -> 2
        for digit_index in range(1, len(num)):
            is_blocked_by_right = digit_index+1 < len(num) and num[digit_index] == num[digit_index+1]
            is_blocked_by_left = digit_index-2 >= 0 and num[digit_index] == num[digit_index-2]
            is_equal = num[digit_index-1] == num[digit_index]

            if not is_blocked_by_right and not is_blocked_by_left and is_equal:
                return digit_index
        
        # if the num contains no pairs:
        return -1
    
    # define comparator
    def less(a:list[int],b:list[int]):
        if len(a) == len(b):
            for i in range(len(a)):
                if a[i] == b[i]:
                    continue
                return a[i] < b[i]
        return len(a) < len(b)
    
    # this function is very fast (0.0023) but is called very often (2868)
    def valid_increase_by_one(valid_num:list[int]):
        for i in range(len(valid_num)-1, -1, -1): 
            if valid_num[i] == 9: 
                continue
            value = valid_num[i] + 1
            for ii in range(i, len(valid_num)):
                valid_num[ii] = value
            return
        
        # this happens log_10(upper_bound)-log_10(lower_bound)
        for i in range(len(valid_num)):
            valid_num[i] = 1
        valid_num += [1]
    
    @lru_cache(maxsize=None)
    # VERY FAST
    def combinations_of_clean_row(row_value:int, row_length:int) -> int:
        # return number of valid combinations in a clean row
        if row_length == 1:
            return 10-row_value
        
        combinations = 0
        for i in range(row_value, 10):
            combinations += combinations_of_clean_row(i, row_length-1)
        
        return combinations
    
    # fast
    def increase_to_row_of_ten_with_lower_bound(lower:list[int], index) -> int:
        if index == len(lower)-1:
            combinations = 10 - lower[-1]
            lower[index] = 9
        else:
            combinations = 0
            combinations += increase_to_row_of_ten_with_lower_bound(lower, index+1)
            clean_row_value = lower[index] + 1
            combinations += combinations_of_clean_row(clean_row_value, len(lower)-index)
            for i in range(index, len(lower)):
                lower[i] = 9

        return combinations

    def get_next_pair_num(valid_num:list[int]) -> int:
        # Checks if the valid_num has a pair if not it increases until it has!
        while True:
            index = get_second_pair_index(valid_num)
            if index != -1:
                return index
            valid_increase_by_one(valid_num)
    
    def calc(lower_bound, upper_bound):
        # convert numbers into usefull values
        # this helps later to perform specific operations with them
        valid_lower_bound:list[int] = convert_number_into_increasing_digits(str(lower_bound))
        upper_bound_as_list:list[int] = [int(char) for char in str(upper_bound)]

        first_matching_number = valid_lower_bound
        if get_second_pair_index(first_matching_number) == -1:
            get_next_pair_num(first_matching_number)
        
        ## Check Bounds
        # Return one wenn upper_bound == lower_bound und valide_matching_numm
        # return 0 if upperbound < lower_bound
        # return 0 if no matching num is between lower_bound and upperbound
        if valid_lower_bound == upper_bound_as_list:
            # no pair -> no matiching num -> 0 numbers in range
            if get_second_pair_index(valid_lower_bound) == -1:
                return 0
            # 1 nmatching num is in range
            return 1
        
        # get the first matching num
        pair_count = 0
        valid_num = valid_lower_bound.copy()
        pair_index = get_next_pair_num(valid_num)
        # boundary check
        if less(upper_bound_as_list, valid_num):
            return 0
        # if this point of the function is reached 
        # there has to be atleast one matching number
        
        
        # increase valid_num
        while less(valid_num, upper_bound_as_list):
            # is pair at the end of the num?
            if pair_index == len(valid_num)-1:
                pair_count += 10-valid_num[-1]
                # set pair to pair of 9
                valid_num[-2] = 9
                valid_num[-1] = 9

            elif valid_num[pair_index] != 9:
                pair_count += increase_to_row_of_ten_with_lower_bound(valid_num, pair_index+1)
                    
            if not less(valid_num, upper_bound_as_list):
                break
            
            # destroy pair
            valid_increase_by_one(valid_num)
            
            # get next pair
            pair_index = get_next_pair_num(valid_num)
        
        return pair_count
    
    return calc(lower_bound,upper_bound)
      
def get_number_of_increasing_digits_with_pair_in_range(lower_bound, upper_bound):
    max = int("9"*len(str(upper_bound)))
    
    a = get_number_of_increasing_digits_with_pair_in_range_to_nine_row(lower_bound, max)
    b = get_number_of_increasing_digits_with_pair_in_range_to_nine_row(upper_bound, max)

    return a-b

n = 1000
count_of_special_numbers = None

bounds = (13456471, 58515929)
start = time.time()
for i in range(n):
    count_of_special_numbers = get_number_of_increasing_digits_with_pair_in_range(*bounds)
end = time.time()
print(f"The result of the matching numbers in the bounds {bounds[0]}, {bounds[1]} is {count_of_special_numbers}")
print(f"Average runtime of the calculation: {(end-start)/n}")

# time ~ 0.00588 seconds
# result 5234

assert get_number_of_increasing_digits_with_pair_in_range(0, 89)      == 8
assert get_number_of_increasing_digits_with_pair_in_range(0, 90)      == 8
assert get_number_of_increasing_digits_with_pair_in_range(601, 1096)  == 12
assert get_number_of_increasing_digits_with_pair_in_range(0, 0)       == 0
assert get_number_of_increasing_digits_with_pair_in_range(0, 1)       == 0
assert get_number_of_increasing_digits_with_pair_in_range(0, 111)     == 9
assert get_number_of_increasing_digits_with_pair_in_range(9, 199)     == 24
assert get_number_of_increasing_digits_with_pair_in_range(0, 900)     == 81

