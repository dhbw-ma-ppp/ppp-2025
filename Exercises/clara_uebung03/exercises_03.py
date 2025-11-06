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
    def __init__(self, balance):
        self._balance = balance
    
    def deposit(self, amount):
        self._balance += amount
        return self._balance
    
    def withdraw(self, amount):
        if amount < self._balance:
            self._balance -= amount
            return self._balance
        
        else:
            print("Kontostand zu niedrig")
        
    def get_balance(self):
        return self._balance
    
    def transfer(self, other_account, amount):
        self._balance = my_BankAccount.deposit(amount)
        other_BankAccount = BankAccount(other_account)
        other_account = other_BankAccount.withdraw(amount)
        return self._balance, other_account

#Testing der Klasse

my_BankAccount = BankAccount(9000)

print("Mein Kontostand:", my_BankAccount.get_balance())
print("Mein Kontostand:", my_BankAccount.deposit(500))
my, other = my_BankAccount.transfer(10000, 500)
print(f"Mein Kontostand: {my}\nAnderer Kontostand: {other}")

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

    def __repr__(self):
        return f"\n{self.rank} of {self.suit}"

class FrenchDeck:
    suit = ["Diamonds", "Hearts", "Spades", "Clubs"]
    rank = [str(numbers) for numbers in range(2, 11)] + ["Jack", "Queen", "King", "Ace"]

    def __init__(self):
        self.cards = [Card(rank, suit)
                       for suit in self.suit
                       for rank in self.rank]
    
    def one_card(self, position):
        return self.cards[position]
    
    def hole_deck(self):
        return self.cards

myCard = Card('7', 'Hearts')
#print(myCard)

myDeck = FrenchDeck()

index = 45

print(f"Die Karte am Index {index} ist die:", myDeck.one_card(index))
#print("Das ist ein volles französisches Kartendeck:", myDeck.hole_deck())

# PART 3:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

class SkatDeck:
    suit = ["Diamonds", "Hearts", "Spades", "Clubs"]
    rank = [str(numbers) for numbers in range(7, 11)] + ["Jack", "Queen", "King", "Ace"]

    def __init__(self):
        self.cards = [Card(rank, suit)
                       for suit in self.suit
                       for rank in self.rank]
    
    def one_card(self, position):
        return self.cards[position]
    
    def hole_deck(self):
        return self.cards

myskat_deck = SkatDeck()
#print("Das ist ein vollständiges Skatdeck:", myskat_deck.hole_deck())

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

import time

def countnumbers(lower_bound, upper_bound):
    valid_numbers = 0
    
    for count in range(lower_bound, upper_bound):
        current_number = str(count)

        if tests_increase(current_number) is True:
            if tests_duplicates(current_number) is True:
                valid_numbers += 1
                print(current_number)
    
    return valid_numbers

def tests_increase(current_number):

    index = 1

    while index < len(current_number):

        if current_number[index - 1] <= current_number[index]:
            pass
        else:
            return False
            
        index += 1

    return True

def tests_duplicates(current_number):
     
    current_number = '#' + current_number + '#'
    index = 1

    for index in range(len(current_number) - 1):
        if current_number[index] == current_number[index + 1]:                  # schauen nach 2 gleichen Zahlen
            if current_number[index] != current_number[index - 1]:              # wenn recht und links jeweils andere Zahlen stehen, haben wir ein Paar gefunden
                if current_number[index] != current_number[index + 2]:
                    return True

        index += 1

    return False   

start = time.time()

validnumbers = countnumbers(13456471, 58515929)

end = time.time()

print(f"There're {validnumbers} valid numbers.")
print("Die Funktion braucht:", end - start)