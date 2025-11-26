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
    def __init__(self, iban, name, initial_balance = 0):
        self.iban = iban
        self.name = name
        self._balance = initial_balance
    
    def __str__(self):
        return f"BankAccount(name='{self.name}', iban='{self.iban}', balance={self._balance:.2f}€)"
    
    def get_balance(self):
        return self._balance
    
    def deposit(self, amount):
        if (amount <= 0):
            print(f"Deposit amount must be positive - tried to deposit: {amount}€")
            return
        
        self._balance += amount
        print(f"Deposited {amount:.2f}€ to {self.name}'s account. New balance: {self._balance:.2f}€")

    def withdraw(self, amount):
        if (amount <= 0):
            print(f"Withdrawal amount must be positive - tried to withdraw: {amount}€")
            return
        if (amount > self._balance):
            print(f"Insufficient funds. Tried to withdraw {amount:.2f}€, but balance is {self._balance:.2f}€")
            return
        
        self._balance -= amount
        print(f"Withdrew {amount:.2f}€ from {self.name}'s account. New balance: {self._balance:.2f}€")
    
    def transfer(self, other_account:'BankAccount', amount):
        if (amount <= 0):
            print(f"Transfer amount must be positive - tried to transfer: {amount}€")
            return
        if (amount > self._balance):
            print(f"Insufficient funds. Tried to transfer {amount:.2f}€, but balance is {self._balance:.2f}€")
            return
        
        self.withdraw(amount)
        other_account.deposit(amount)

        print(f"Transferred {amount:.2f}€ from {self.name} to {other_account.name}")
        print(f"{self.name}'s new balance: {self._balance:.2f}€")
        print(f"{other_account.name}'s new balance: {other_account._balance:.2f}€")

def test_01():
    max = BankAccount("DE1234567890987654321", "Max", 100)
    rudolf = BankAccount("DE987654321234567890", "Rudolf", 20)

    print(max)
    print(rudolf)

    print("\n Test deposit:")
    max.deposit(50)
    
    print("\n Test withdraw:")
    max.withdraw(30)
    
    print("\n Test transfer:")
    max.transfer(rudolf, 30)
    
    print("\n Test Errors:")
    max.withdraw(200)
    rudolf.deposit(-10)
    rudolf.transfer(max, 400)

# test_01()

# PART 2:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
#   The deck of cards should behave like a sequence.
#   When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
#   I should be able to index into the deck to retrieve one card.
#   I should be able to iterate over all cards in the deck.
#   Printing a cards string representation should give me a nice, readable description of that card.

class Card:
    SUITS = ['Diamonds', 'Hearts', 'Spades', 'Clubs']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
   
    SUIT_SYMBOLS = {
        'Diamonds': '♦',
        'Hearts': '♥',
        'Spades': '♠',
        'Clubs': '♣'
    }
   
    def __init__(self, rank, suit):
        if rank not in self.RANKS:
            raise ValueError(f"Invalid rank: {rank}")
        if suit not in self.SUITS:
            raise ValueError(f"Invalid suit: {suit}")
       
        self.rank = rank
        self.suit = suit
   
    def __str__(self):
        symbol = self.SUIT_SYMBOLS[self.suit]
        return f"{self.rank} of {self.suit} {symbol}"
   
    def __repr__(self) -> str:
        return f"Card(rank='{self.rank}', suit='{self.suit}')"

class FrenchDeck:   
    def __init__(self):
        self._cards = []
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self._cards.append(Card(rank, suit))
   
    def __len__(self):
        return len(self._cards)
   
    def __getitem__(self, position):
        return self._cards[position]
   
    def __iter__(self):
        return iter(self._cards)
   
    def __str__(self):
        return f"French-Deck with {len(self)} cards"

def test_french_deck():
    deck = FrenchDeck()
   
    print(f"\n{deck}")
    print(f"Number of cards: {len(deck)}")
   
    print("\nTesting position access:")
    print(f"First card: {deck[0]}")
    print(f"Last card: {deck[-1]}")

    print("\nAll Hearts:")
    for card in deck:
        if card.suit == 'Hearts':
            print(f"  {card}")
   
    print("\nCards 10-15 (slicing):")
    for card in deck[10:15]:
        print(f"  {card}")
   
    print("\nVerify order:")
    for card in deck:
        print(f"  {card}")

# test_french_deck()

# PART 3:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

class SkatDeck:
    RANKS = ['7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in Card.SUITS for rank in self.RANKS]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):   
        return self._cards[position]

    def __iter__(self):
        return iter(self._cards)

    def __str__(self):
        return f"SkatDeck with {len(self)} cards"


def test_skat_deck():
    deck = SkatDeck()
    print(f"\n{deck}")
    print(f"Number of cards: {len(deck)}")

    print("\nTesting position access:")
    print(f"First card: {deck[0]}")
    print(f"Last card: {deck[-1]}")

    print("\nAll Clubs:")
    for card in deck:
        if card.suit == 'Clubs':
            print(f" {card}")

    print("\nCards 10-15 (slicing):")
    for card in deck[10:15]:
        print(f" {card}")

    print("\nVerify order:")
    for card in deck:
        print(f" {card}")

# test_skat_deck()

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

def has_exact_double(number_str):
    i = 0
    while i < len(number_str):
        count = 1
        while i + count < len(number_str) and number_str[i] == number_str[i + count]:
            count += 1
        if count == 2:
            return True
        i += count
    return False

def is_increasing(number_str):
    for i in range(len(number_str) - 1):
        if number_str[i] > number_str[i + 1]:
            return False
    return True

def count_numbers(lower, upper):
    count = 0
    for num in range(lower, upper):
        s = str(num)
        if is_increasing(s) and has_exact_double(s):
            count += 1
    return count

def test_count_numbers():
    lower = 13456471
    upper = 58515929
    result = count_numbers(lower, upper)
    print(f"Count of valid numbers between {lower} and {upper}: {result}")

# test_count_numbers()