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
    def __init__(self, balance=0): 
        if balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self._balance = balance

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("Insufficient funds for withdrawal")
        if amount < 0:
            raise ValueError("Withdrawal amount must be positive")
        self._balance -= amount

    def get_balance(self):
        return self._balance

    def transfer(self, other_account, amount):   
        self.withdraw(amount)
        other_account.deposit(amount)

# Testing BankAccount
account1 = BankAccount(1000)
account2 = BankAccount(2500)
account1.deposit(500)
print(f'Balance of account1: {account1.get_balance()}')  # 1500
account1.withdraw(750)
print(f'Balance of account1: {account1.get_balance()}')  # 750
account1.transfer(account2, 250)
print(f'Balance of account1: {account1.get_balance()}')  # 500
print(f'Balance of account2: {account2.get_balance()}')  # 2750



# PART 2:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
#   The deck of cards should behave like a sequence.
#   When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
#   I should be able to index into the deck to retrieve one card.
#   I should be able to iterate over all cards in the deck.
#   Printing a cards string representation should give me a nice, readable description of that card.
class Card:
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    SUITS = ['Diamonds', 'Hearts', 'Spades', 'Clubs']

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class FrenchDeck:
    def __init__(self):
        self.cards = []
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                card = Card(suit, rank)
                self.cards.append(card)

    def __getitem__(self, position):
        return self.cards[position]

    def __len__(self):
        return len(self.cards)

print(f'Erste Karte im Deck: {FrenchDeck()[0]}') # Ausgabe der ersten Karte im Deck
print("\nAlle Karten im Deck:")
for cards in FrenchDeck():
    print(cards) # Ausgabe jeder Karte im Deck einzeln
# PART 3:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.
class SkatDeck(FrenchDeck):
    def __init__(self):
        self.cards = []
        for suit in Card.SUITS:
            for rank in Card.RANKS[5:]:
                card = Card(suit, rank)
                self.cards.append(card)

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)
def test_decks():
    french_deck = FrenchDeck()
    skat_deck = SkatDeck()

    # Test FrenchDeck
    assert len(french_deck) == 52
    assert str(french_deck[0]) == "2 of Diamonds"
    assert str(french_deck[-1]) == "Ace of Clubs"
    assert FrenchDeck.__getitem__(french_deck, 10) == french_deck.cards[10]

    # Test SkatDeck
    assert len(skat_deck) == 32
    assert str(skat_deck[0]) == "7 of Diamonds"
    assert str(skat_deck[-1]) == "Ace of Clubs"
    assert SkatDeck.__getitem__(skat_deck, 10) == skat_deck.cards[10]

test_decks()



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
def is_valid(number): 
    digits = str(number)  # String conversion is faster than modulo operations
    
    # Check if digits only increase from left to right
    for i in range(len(digits) - 1):
        if digits[i] > digits[i + 1]:
            return False
    
    # Check for at least one group of exactly two adjacent same digits
    i = 0
    while i < len(digits):
        # Count consecutive same digits
        streak = 1
        while i + streak < len(digits) and digits[i] == digits[i + streak]:
            streak += 1
        
        if streak == 2:
            return True
        
        i += streak  # Skip to next different digit
    
    return False

def count_valid_numbers(lower_bound, upper_bound):
    valid_count = 0
    for num in range(lower_bound, upper_bound):
        if is_valid(num):
            valid_count += 1

    return valid_count

print("\nPART 4 - Valid numbers count:")

import time
start_time = time.time()
result = count_valid_numbers(13456471, 58515929)
end_time = time.time()

print(result) # result = 5234
print(f"Time taken: {end_time - start_time:.2f} seconds") # time taken: ~14s
# It should complete in a few seconds. Note the resulting count in your pull request, please.
