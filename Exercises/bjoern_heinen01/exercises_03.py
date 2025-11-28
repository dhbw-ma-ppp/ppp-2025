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
    
    ### defenition of sub functions: ### 

    def convert_number_into_increasing_digits(num:int) -> list[int]:
        chars = list(str(num))
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
        # ind_rev => index_reversed
        for ind_rev in range(len(valid_num)-1, -1, -1): 
            if valid_num[ind_rev] == 9: 
                continue
            value = valid_num[ind_rev] + 1

            for digit_index in range(ind_rev, len(valid_num)):
                valid_num[digit_index] = value

            return
        
        # this happens log_10(upper_bound)-log_10(lower_bound) times
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
    
    def get_combinations_to_row_of_nines_with_lower_bound(lower:list[int], index) -> int:
        combinations = 10 - lower[-1]

        for i in range(len(lower)-2,index-1, -1):
            clean_row_value = lower[i] + 1
            combinations += combinations_of_clean_row(clean_row_value, len(lower) - i)
        return combinations
    
    # This function is VERY slow
    def get_next_pair_num(valid_num:list[int]) -> int:
        # Checks if the valid_num has a pair if not it increases until it has!
        while True:
            index = get_second_pair_index(valid_num)
            if index != -1:
                return index
            valid_increase_by_one(valid_num)

    ### defenition of sub functions is finished ### 

    upper_bound_as_list:list[int] = [int(char) for char in str(upper_bound)]

    # valid num is always a number with increasing digits
    # a matchin_num is a valid_num wich has at least one pair
    valid_num:list[int] = convert_number_into_increasing_digits(lower_bound)

    matching_num_count = 0
    pair_index = get_next_pair_num(valid_num)
    
    ## Check Bounds
    if valid_num == upper_bound_as_list:
        return 1
    if less(upper_bound_as_list, valid_num):
        return 0
    
    
    ### Main loop: ###

    while less(valid_num, upper_bound_as_list):
        
        ## get combinations until pair gets destroyed:

        # is pair at the end of the num?
        if pair_index == len(valid_num)-1:
            matching_num_count += 10-valid_num[-1]
            # set pair to pair of 9
            valid_num[-2] = 9
            valid_num[-1] = 9
        else:
            matching_num_count += get_combinations_to_row_of_nines_with_lower_bound(valid_num, pair_index+1)
            
            # update valid_num
            for i in range(pair_index+1, len(valid_num)):
                valid_num[i] = 9
        
        if not less(valid_num, upper_bound_as_list):
            break
        
        ## destroy pair
        valid_increase_by_one(valid_num)
        
        ## get next pair
        pair_index = get_next_pair_num(valid_num)
    
    return matching_num_count
    
      
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

# short unit test:

assert get_number_of_increasing_digits_with_pair_in_range(97, 99)      == 0
assert get_number_of_increasing_digits_with_pair_in_range(99, 100)      == 1
assert get_number_of_increasing_digits_with_pair_in_range(99, 99)      == 0
assert get_number_of_increasing_digits_with_pair_in_range(100, 100)      == 0

assert get_number_of_increasing_digits_with_pair_in_range(0, 89)      == 8
assert get_number_of_increasing_digits_with_pair_in_range(0, 90)      == 8
assert get_number_of_increasing_digits_with_pair_in_range(601, 1096)  == 12
assert get_number_of_increasing_digits_with_pair_in_range(0, 0)       == 0
assert get_number_of_increasing_digits_with_pair_in_range(0, 1)       == 0
assert get_number_of_increasing_digits_with_pair_in_range(0, 111)     == 9
assert get_number_of_increasing_digits_with_pair_in_range(9, 199)     == 24
assert get_number_of_increasing_digits_with_pair_in_range(0, 900)     == 81

# long unit test:

assert get_number_of_increasing_digits_with_pair_in_range(602400332, 1557275973) == 18986
assert get_number_of_increasing_digits_with_pair_in_range(952916804, 1681816258) == 19084
assert get_number_of_increasing_digits_with_pair_in_range(366819351, 1297174798) == 16964
assert get_number_of_increasing_digits_with_pair_in_range(865381094, 1182046857) == 10748
assert get_number_of_increasing_digits_with_pair_in_range(615297311, 851890430) == 110
assert get_number_of_increasing_digits_with_pair_in_range(690979506, 827104524) == 19
assert get_number_of_increasing_digits_with_pair_in_range(429746522, 1117241797) == 5615
assert get_number_of_increasing_digits_with_pair_in_range(693501000, 1095140364) == 21
assert get_number_of_increasing_digits_with_pair_in_range(565462426, 1364533229) == 17909
assert get_number_of_increasing_digits_with_pair_in_range(475913018, 1229421055) == 13977
assert get_number_of_increasing_digits_with_pair_in_range(220485589, 915530461) == 8352
assert get_number_of_increasing_digits_with_pair_in_range(534260339, 1313235322) == 16039
assert get_number_of_increasing_digits_with_pair_in_range(468606563, 570126323) == 315
assert get_number_of_increasing_digits_with_pair_in_range(556015842, 1259345258) == 15846
assert get_number_of_increasing_digits_with_pair_in_range(495300789, 1073204075) == 425
assert get_number_of_increasing_digits_with_pair_in_range(145330617, 860878517) == 8845
assert get_number_of_increasing_digits_with_pair_in_range(639670675, 804343459) == 110
assert get_number_of_increasing_digits_with_pair_in_range(46887367, 558078104) == 18437
assert get_number_of_increasing_digits_with_pair_in_range(690361521, 1136430612) == 9369
assert get_number_of_increasing_digits_with_pair_in_range(481800909, 871711919) == 425
assert get_number_of_increasing_digits_with_pair_in_range(563744892, 1055160838) == 197
assert get_number_of_increasing_digits_with_pair_in_range(976381353, 1021383131) == 0
assert get_number_of_increasing_digits_with_pair_in_range(6116820, 404056676) == 26606
assert get_number_of_increasing_digits_with_pair_in_range(245818163, 1012085689) == 3854
assert get_number_of_increasing_digits_with_pair_in_range(521827288, 927604340) == 425
assert get_number_of_increasing_digits_with_pair_in_range(716902926, 1498848466) == 18703
assert get_number_of_increasing_digits_with_pair_in_range(298969439, 972847574) == 3493
assert get_number_of_increasing_digits_with_pair_in_range(359116451, 471127055) == 952
assert get_number_of_increasing_digits_with_pair_in_range(533619671, 945961859) == 425
assert get_number_of_increasing_digits_with_pair_in_range(165067409, 1067848774) == 8437
assert get_number_of_increasing_digits_with_pair_in_range(396563543, 802744495) == 1308
assert get_number_of_increasing_digits_with_pair_in_range(112425339, 159544762) == 6727
assert get_number_of_increasing_digits_with_pair_in_range(681017273, 1230259917) == 13558
assert get_number_of_increasing_digits_with_pair_in_range(460037288, 1111619584) == 2376
assert get_number_of_increasing_digits_with_pair_in_range(561674354, 1080630896) == 197
assert get_number_of_increasing_digits_with_pair_in_range(739619683, 1702705540) == 19107
assert get_number_of_increasing_digits_with_pair_in_range(987065836, 1319904841) == 15614
assert get_number_of_increasing_digits_with_pair_in_range(564211496, 1386115572) == 17992
assert get_number_of_increasing_digits_with_pair_in_range(71470656, 987368235) == 18348
assert get_number_of_increasing_digits_with_pair_in_range(5716445, 826369862) == 27927
assert get_number_of_increasing_digits_with_pair_in_range(930336483, 1409296214) == 17797
assert get_number_of_increasing_digits_with_pair_in_range(265021559, 1039386136) == 3578
assert get_number_of_increasing_digits_with_pair_in_range(37233193, 892895445) == 19185
assert get_number_of_increasing_digits_with_pair_in_range(681873027, 1001922889) == 23
assert get_number_of_increasing_digits_with_pair_in_range(375228407, 542215036) == 903
assert get_number_of_increasing_digits_with_pair_in_range(37290016, 238193041) == 14850
assert get_number_of_increasing_digits_with_pair_in_range(447271068, 546677370) == 331
assert get_number_of_increasing_digits_with_pair_in_range(766736797, 1700597951) == 19107
assert get_number_of_increasing_digits_with_pair_in_range(6716400, 86200550) == 9548
assert get_number_of_increasing_digits_with_pair_in_range(599153932, 762519989) == 91
assert get_number_of_increasing_digits_with_pair_in_range(7998461, 817459138) == 27852
assert get_number_of_increasing_digits_with_pair_in_range(982024160, 1446074540) == 18267
assert get_number_of_increasing_digits_with_pair_in_range(191036432, 855690153) == 8350
assert get_number_of_increasing_digits_with_pair_in_range(790157326, 1566587344) == 18912
assert get_number_of_increasing_digits_with_pair_in_range(809071276, 1763853340) == 19088
assert get_number_of_increasing_digits_with_pair_in_range(959721896, 1514180287) == 18682
assert get_number_of_increasing_digits_with_pair_in_range(26338070, 592731549) == 20361
assert get_number_of_increasing_digits_with_pair_in_range(871167545, 1457982005) == 18597
assert get_number_of_increasing_digits_with_pair_in_range(412667440, 520339043) == 885
assert get_number_of_increasing_digits_with_pair_in_range(260442187, 1199908179) == 14332
assert get_number_of_increasing_digits_with_pair_in_range(722443777, 1688069705) == 19105
assert get_number_of_increasing_digits_with_pair_in_range(367986760, 1076444530) == 1330
assert get_number_of_increasing_digits_with_pair_in_range(673330281, 873612704) == 37
assert get_number_of_increasing_digits_with_pair_in_range(689104192, 1192447001) == 10775
assert get_number_of_increasing_digits_with_pair_in_range(508854254, 1051908977) == 425
assert get_number_of_increasing_digits_with_pair_in_range(305381113, 613273410) == 3381
assert get_number_of_increasing_digits_with_pair_in_range(35011939, 180710471) == 11016
assert get_number_of_increasing_digits_with_pair_in_range(216984610, 471662560) == 7909
assert get_number_of_increasing_digits_with_pair_in_range(147795053, 768206581) == 8631
assert get_number_of_increasing_digits_with_pair_in_range(952763809, 1427712868) == 17797
assert get_number_of_increasing_digits_with_pair_in_range(47311553, 475630323) == 18197
assert get_number_of_increasing_digits_with_pair_in_range(558761584, 723841326) == 184
assert get_number_of_increasing_digits_with_pair_in_range(585935493, 1196160425) == 10868
assert get_number_of_increasing_digits_with_pair_in_range(452318509, 1273384694) == 16316
assert get_number_of_increasing_digits_with_pair_in_range(190888916, 802866004) == 8350
assert get_number_of_increasing_digits_with_pair_in_range(205890965, 1178129080) == 19090
assert get_number_of_increasing_digits_with_pair_in_range(890099624, 1849564478) == 19105
assert get_number_of_increasing_digits_with_pair_in_range(679900576, 1612338100) == 19018
assert get_number_of_increasing_digits_with_pair_in_range(207242796, 390659194) == 7042
assert get_number_of_increasing_digits_with_pair_in_range(578562176, 678572461) == 91
assert get_number_of_increasing_digits_with_pair_in_range(333987760, 1009663459) == 2942
assert get_number_of_increasing_digits_with_pair_in_range(565357257, 1452886426) == 18584
assert get_number_of_increasing_digits_with_pair_in_range(329899792, 358399154) == 2096
assert get_number_of_increasing_digits_with_pair_in_range(815921793, 938404985) == 2
assert get_number_of_increasing_digits_with_pair_in_range(693956567, 796622233) == 19
assert get_number_of_increasing_digits_with_pair_in_range(556311122, 1280949188) == 15929
assert get_number_of_increasing_digits_with_pair_in_range(952101952, 1828303564) == 19105
assert get_number_of_increasing_digits_with_pair_in_range(263869002, 507656073) == 3153
assert get_number_of_increasing_digits_with_pair_in_range(444601570, 761686398) == 1075
assert get_number_of_increasing_digits_with_pair_in_range(139013531, 561320145) == 8995
assert get_number_of_increasing_digits_with_pair_in_range(3862027, 864630180) == 28368
assert get_number_of_increasing_digits_with_pair_in_range(107266979, 440036919) == 17020
assert get_number_of_increasing_digits_with_pair_in_range(894059116, 1426603939) == 17797
assert get_number_of_increasing_digits_with_pair_in_range(874543227, 1328095766) == 15616
assert get_number_of_increasing_digits_with_pair_in_range(436386777, 662006295) == 1198
assert get_number_of_increasing_digits_with_pair_in_range(193527527, 635610562) == 8240
assert get_number_of_increasing_digits_with_pair_in_range(403116012, 712920949) == 1289
assert get_number_of_increasing_digits_with_pair_in_range(855685116, 1423100671) == 17799
assert get_number_of_increasing_digits_with_pair_in_range(112301464, 425108437) == 14316
assert get_number_of_increasing_digits_with_pair_in_range(594349177, 1062726876) == 112