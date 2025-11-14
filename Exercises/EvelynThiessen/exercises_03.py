# PART 1:
# Create a class BankAccount with:
# A “private” attribute _balance
# Methods:
#  deposit(amount) → increases the balance
#  withdraw(amount) → decreases it (if enough funds)
#  get_balance() → returns the balance
#  transfer(other_account, amount) -> It should withdraw from one account and deposit into the other.
#  Try depositing, withdrawing and transferring amounts and print the balance each time.

class BankAccount:

    def __init__(self, _balance):
        self._balance = _balance

    def deposit(self, amount):
        self._balance += amount

        print("amount is added")
        print(f"new balance: {self._balance}")
        return self._balance
    
    def withdraw(self,amount):

        if self.get_balance() < amount:
            print("not enough money")
            return False
        self._balance -= amount

        print("amount is withdrawn")
        print(f"new balance: {self._balance}")
        return self._balance
    
    def get_balance(self):
        return self._balance
    
    def transfer(self, other_account, amount):
        self.withdraw(amount)
        other_account.deposit(amount)
        return self.get_balance
    
def erste_aufgabe():
    bankAccount01 = BankAccount(300)
    bankAccount02 = BankAccount(200)

    bankAccount01.deposit(200)
    bankAccount01.withdraw(100)
    bankAccount01.transfer(bankAccount02, 300)
    bankAccount01.withdraw(200)

# PART 2:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
#   The deck of cards should behave like a sequence.
#   When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
#   I should be able to index into the deck to retrieve one card.
#   I should be able to iterate over all cards in the deck.
#   Printing a cards string representation should give me a nice, readable description of that card.

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    @property
    def description(self):
        return f"{self.rank} of {self.suit}"
    
class FrenchDeck:
    def __init__(self):
        ranks = ["Ace", "King", "Queen", "Jack", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
        suits = ["diamonds []", "hearts <3", "spades ", "clubs %"]

        self._cards = [Card(rank, suit) for suit in suits for rank in ranks]

    def __len__(self):
        return len(self._cards) 

    def __getitem__(self, position):
        return self._cards[position].description

def zweite_aufgabe():
    firstDeck = FrenchDeck()
    print(len(firstDeck))
    print(firstDeck[51])

# PART 3:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

class SkatDeck:
    def __init__(self):
        ranks = ["Ace", "King", "Queen", "Jack", "10", "9", "8", "7"]
        suits = ["diamonds []", "hearts <3", "spades", "clubs %"]

        self._cards = [Card(rank, suit) for rank in ranks for suit in suits]

    def __len__(self):
        return len(self._cards)
    
    def __getitem__(self, position):
        return self._cards[position].description()
    
    def __iter__(self):
        return iter(self._cards)
    
def dritte_aufgabe():
    deck = SkatDeck()
    for item in deck:
        print(item.description())

#dritteAufgabe()

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

def count_valid_numbers(lower_bound, upper_bound):

    if lower_bound >= upper_bound :
        raise ValueError("lower bound must be smaller")
    
    is_valid_count = 0
    
    for num in range(lower_bound, upper_bound):
        if is_valid_number_2(num) == True:
            is_valid_count += 1
            #print(num)

    print(is_valid_count)

def is_valid_number_2(num):
    last_digit = 10
    is_twin = False
    streak = 0
    numy = num

    while numy > 0:
        digit = numy % 10
        numy //= 10

        if digit > last_digit:
            return False
        
        if digit == last_digit:
            streak += 1
        else:
            if streak == 2:
                is_twin = True
            streak = 1
        last_digit = digit

    if streak == 2:
        is_twin = True

    return is_twin

# 5234
# 22 Sekunden
count_valid_numbers(13456471, 58515929)   