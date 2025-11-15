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
    def __init__(self, iban = "Empty", name = "Empty", initial_balance = 0):
        self.iban = iban
        self.name = name
        self._balance = initial_balance
        print(f"Bank Account for {self.name} created with {self._balance}$")

    def __str__(self):
        return f"{self.name}'s account with IBAN {self.iban}."

    @property
    def balance(self):
        return self._balance
    def get_balance(self):
        print(f"{self.name}'s Current Balance: {self.balance}$")

    def deposit(self, amount):
        if (amount > 0):
            self._balance += amount
            print(f"Successfully deposited {amount}$ into {self.name}'s account.")
        else:
            print("Invalid deposit amount. Please enter a positive value.")

    def withdraw(self, amount):
        if (amount > 0 and amount <= self._balance):
            self._balance -= amount
            print(f"Successfully withdrew {amount}$ from {self.name}'s account.")
        else:
            print("Invalid withdrawal amount or insufficient funds.")

    def transfer(self, other_account, amount):
        if (amount > 0 and amount <= self._balance):
            self._balance -= amount
            print(f"Successfully transferred {amount}$ from {self.name} to {other_account.name}.")
            other_account.deposit(amount)         
        else:
            print("Transfer failed: invalid amount or insufficient funds.")

acc_names = {
    "Alice Thompson":BankAccount("DE123454321", "Alice Thompson", 0),
    "Bob Ross":BankAccount("DE543212345", "Bob Marley Ross Jackson II", 0)
}

iban_to_names = {
    "DE123454321":"Alice Thompson",
    "DE543212345":"Bob Ross"
}

def test_bank_accounts():
    acc_names["Alice Thompson"].deposit(140)
    acc_names["Alice Thompson"].get_balance()
    acc_names["Alice Thompson"].withdraw(30)
    acc_names["Alice Thompson"].get_balance()
    acc_names["Alice Thompson"].transfer(acc_names[iban_to_names["DE543212345"]], 49.99) #if you dont know the name or need to specifically target the right account
    acc_names["Alice Thompson"].get_balance()
    acc_names["Bob Ross"].get_balance()

    print(acc_names["Alice Thompson"])

test_bank_accounts()


# PART 2:
# Write a class for a French deck of cards (From 2 to Ace with the 4 suites: diamonds, hearts, spades and clubs).
#   The deck of cards should behave like a sequence.
#   When initialized, the cards should all be in a well-defined order (2 to the Ace of each suite, suites in the order above)
#   I should be able to index into the deck to retrieve one card.
#   I should be able to iterate over all cards in the deck.
#   Printing a cards string representation should give me a nice, readable description of that card.

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):   #printing a cards string repr gives a nice, readable description of itself
        return f"{self.rank} of {self.suit}"

class FrenchDeck:
    suits = ["Diamonds", "Hearts", "Spades", "Clubs"]
    ranks = [str(n) for n in range(2, 11)] + ["Jack", "Queen", "King", "Ace"]

    def __init__(self):
        self._cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __iter__(self):
        return iter(self._cards)
    
def french_deck():
    deck = FrenchDeck()
    #index a card in the deck and print it
    print(deck[0])
    #iterate over all cards in the deck
    for card in deck:
        print(card)

french_deck()


# PART 3:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

class SkatDeck:
    suits = ["Diamonds", "Hearts", "Spades", "Clubs"]
    ranks = [str(n) for n in range(7, 11)] + ["Jack", "Queen", "King", "Ace"]

    def __init__(self):
        self._cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __iter__(self):
        return iter(self._cards)
    
def test_decks():
    fr_deck = FrenchDeck()
    sk_deck = SkatDeck()
    #index a card in the deck and print it
    print(fr_deck[0])
    print(sk_deck[0])
    #iterate over all cards in the deck
    for card in fr_deck:
        print(card)
    for card in sk_deck:
        print(card)

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
# It should complete in a few seconds. Note the resulting count in your pull request, please.

def double_digits(s):
    i = 0
    while i < len(s) - 1:
        count = 1
        while i + 1 < len(s) and s[i] == s[i + 1]:
            count += 1
            i += 1
        if count == 2:
            return True
        i += 1
    return False

def weird_algorithm(x, y):
    valid_numbers = 0
    for i in range(x, y):
        s = str(i)
        if list(s) != sorted(s):
            continue  # digits must not decrease
        if double_digits(s):
            valid_numbers += 1
    return valid_numbers

print(weird_algorithm(13456471, 58515929))