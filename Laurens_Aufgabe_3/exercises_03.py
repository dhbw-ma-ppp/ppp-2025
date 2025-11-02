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
    def __init__(self):
        self._balance = 0

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount        

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount

    def get_balance(self):
        return self._balance

    def transfer(self, other_account, amount):
        if 0 < amount <= self._balance:
            self.withdraw(amount)
            other_account.deposit(amount)

print("PART 1:")
account1 = BankAccount()
account2 = BankAccount()
print("Account 1 balance:", account1.get_balance())

account1.deposit(100)
print("Account 1 balance:", account1.get_balance())
account1.withdraw(50)
print("Account 1 balance:", account1.get_balance())
account1.transfer(account2, 25)

print("Account 1 balance:", account1.get_balance())
print("Account 2 balance:", account2.get_balance())

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

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"


# PART 2: Deck implementation
class Deck:
    """A French deck (2-Ace of Diamonds, Hearts, Spades, Clubs).

    Behaves like a sequence: supports len(), indexing, iteration.
    Cards are created in the well-defined order: for each suit in
    Card.SUITS (in that order) create cards with ranks in Card.RANKS
    (2 up to Ace).
    """

    def __init__(self):
        # create cards in the order: Diamonds 2..Ace, Hearts 2..Ace, Spades 2..Ace, Clubs 2..Ace
        self._cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, index):
        # delegate to underlying list (supports int indexing and slices)
        return self._cards[index]

    def __iter__(self):
        return iter(self._cards)

    def __repr__(self):
        return f"<Deck {len(self)} cards>"


# Quick checks / asserts to validate behavior (how to check):
print("PART 2 quick checks for Deck and SkatDeck")

deck = Deck()
# basic properties
assert len(deck) == 52, f"expected 52 cards, got {len(deck)}"
# ordering: first card should be 2 of Diamonds
assert str(deck[0]) == '2 of Diamonds'
# last card should be Ace of Clubs
assert str(deck[-1]) == 'Ace of Clubs'
# iteration yields the same first card
it = iter(deck)
assert str(next(it)) == str(deck[0])

# slicing works (delegated to list)
first_four = deck[0:4]
assert isinstance(first_four, list) and len(first_four) == 4

print('Deck checks passed.')

# PART 3:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

class SkatDeck(Deck):
    """Deck for Skat: ranks 7..Ace for each suit (7,8,9,10,Jack,Queen,King,Ace).

    Subclasses Deck but constructs only the Skat ranks.
    """

    SKAT_RANKS = ['7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self):
        self._cards = [Card(suit, rank) for suit in Card.SUITS for rank in self.SKAT_RANKS]

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

skat = SkatDeck()
assert len(skat) == 32, f"expected 32 cards in skat deck, got {len(skat)}"
assert str(skat[0]) == '7 of Diamonds'
assert str(skat[-1]) == 'Ace of Clubs'
print('SkatDeck checks passed.')


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
    def is_valid(number):
        digits = [int(d) for d in str(number)]
        has_exactly_two_adjacent = False
        count = 1

        for i in range(1, len(digits)):
            if digits[i] < digits[i - 1]:
                return False  # digits do not increase
            if digits[i] == digits[i - 1]:
                count += 1
            else:
                if count == 2:
                    has_exactly_two_adjacent = True
                count = 1

        if count == 2:
            has_exactly_two_adjacent = True

        return has_exactly_two_adjacent

    valid_count = 0
    for num in range(lower_bound, upper_bound):
        if is_valid(num):
            valid_count += 1

    return valid_count

print("PART 4:")
print(count_valid_numbers(123345, 123346)) # should be 1